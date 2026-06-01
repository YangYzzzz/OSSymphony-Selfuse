from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any, Dict, List, Tuple

from mm_agents.os_symphony.agents.instruction_generator.base_agent import WorkflowCostTracker, WorkflowLLMAgent
from mm_agents.os_symphony.agents.instruction_generator.models import ExplorationContext, ExplorationResult, ProposalCandidate, TaskCandidate, VerificationRepairInput, VerificationSynthesisInput, WorkflowSharedState
from mm_agents.os_symphony.agents.instruction_generator.prompts import load_prompt


class EvaluatorSynthesisAgent(WorkflowLLMAgent):
    def __init__(self, name: str, engine_params: Dict[str, Any], cost_tracker: WorkflowCostTracker, platform: str = "linux"):
        super().__init__(name, engine_params, cost_tracker, platform)

    def synthesize(
        self,
        shared_state: WorkflowSharedState,
        proposal: ProposalCandidate,
        exploration_result: ExplorationResult,
        app_memory_summary: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        system_prompt = load_prompt("evaluator_synthesizer.md")
        synthesis_input = VerificationSynthesisInput(
            proposal=proposal,
            sampled_apps=shared_state.sampled_apps,
            app_versions=shared_state.app_versions,
            app_file_support=shared_state.app_file_support,
            sampled_files=shared_state.sampled_files,
            app_tutorials=shared_state.app_tutorials,
            verification_experience=self._matching_verification_experience(proposal, app_memory_summary or {}),
            exploration_context=ExplorationContext(
                trajectory=exploration_result.trajectory,
                generation_notes=exploration_result.generation_notes,
            ),
        )
        user_text = json.dumps(synthesis_input.to_dict(), ensure_ascii=False)
        verification_spec = self.call_json(system_prompt, user_text).get("verification")
        return verification_spec if isinstance(verification_spec, dict) else {}

    def _matching_verification_experience(self, proposal: ProposalCandidate, app_memory_summary: Dict[str, Any]) -> Dict[str, Any]:
        query_features = proposal.target_features or self._fallback_query_features(proposal)
        related_apps = proposal.related_apps or list(app_memory_summary.keys())
        matches: Dict[str, List[Dict[str, Any]]] = {}
        for app in related_apps:
            app_summary = app_memory_summary.get(str(app), {})
            experiences = app_summary.get("verification_experience", {}) if isinstance(app_summary, dict) else {}
            if not isinstance(experiences, dict):
                continue
            ranked = self._rank_feature_experiences(query_features, experiences)
            if ranked:
                matches[str(app)] = ranked[:3]
        return matches

    def _rank_feature_experiences(self, query_features: List[str], experiences: Dict[str, Any]) -> List[Dict[str, Any]]:
        ranked: List[Tuple[float, str, List[str]]] = []
        for memory_feature, lessons in experiences.items():
            if not isinstance(lessons, list):
                continue
            normalized_lessons = [str(item) for item in lessons if item is not None]
            if not normalized_lessons:
                continue
            score = max((self._feature_similarity(query, str(memory_feature)) for query in query_features), default=0.0)
            if score <= 0.0:
                continue
            ranked.append((score, str(memory_feature), normalized_lessons))
        ranked.sort(key=lambda item: (-item[0], item[1]))
        return [
            {"feature": feature, "score": round(score, 3), "experience": lessons}
            for score, feature, lessons in ranked
        ]

    def _fallback_query_features(self, proposal: ProposalCandidate) -> List[str]:
        features: List[str] = []
        if proposal.instruction:
            features.append(proposal.instruction)
        if proposal.category:
            features.append(proposal.category)
        features.extend(proposal.success_criteria)
        return features

    def _feature_similarity(self, query: str, target: str) -> float:
        query_norm = self._normalize_feature(query)
        target_norm = self._normalize_feature(target)
        if not query_norm or not target_norm:
            return 0.0
        query_ngrams = self._char_ngrams(query_norm)
        target_ngrams = self._char_ngrams(target_norm)
        ngram_score = self._jaccard_similarity(query_ngrams, target_ngrams)
        query_tokens = Counter(query_norm.split())
        target_tokens = Counter(target_norm.split())
        token_score = self._weighted_jaccard_similarity(query_tokens, target_tokens)
        exact_score = 1.0 if query_norm == target_norm else 0.0
        containment_score = 0.9 if query_norm in target_norm or target_norm in query_norm else 0.0
        return max(ngram_score, token_score, exact_score, containment_score)

    def _char_ngrams(self, value: str, n: int = 3) -> set[str]:
        compact = value.replace(" ", "")
        if len(compact) < n:
            return {compact} if compact else set()
        return {compact[idx : idx + n] for idx in range(len(compact) - n + 1)}

    def _jaccard_similarity(self, left: set[str], right: set[str]) -> float:
        if not left or not right:
            return 0.0
        return len(left & right) / len(left | right)

    def _weighted_jaccard_similarity(self, left: Counter[str], right: Counter[str]) -> float:
        if not left or not right:
            return 0.0
        keys = set(left) | set(right)
        numerator = sum(min(left[key], right[key]) for key in keys)
        denominator = sum(max(left[key], right[key]) for key in keys)
        return numerator / denominator if denominator else 0.0

    def _normalize_feature(self, value: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", value.lower())).strip()


class EvaluatorCritiqueAgent(WorkflowLLMAgent):
    def __init__(self, name: str, engine_params: Dict[str, Any], cost_tracker: WorkflowCostTracker, platform: str = "linux"):
        super().__init__(name, engine_params, cost_tracker, platform)

    def critique_and_repair(self, shared_state: WorkflowSharedState, task_draft: TaskCandidate, failure: Dict[str, Any], exploration_context: ExplorationContext) -> Dict[str, Any]:
        system_prompt = load_prompt("evaluator_critic.md")
        repair_input = VerificationRepairInput(
            candidate=task_draft,
            failure=failure,
            sampled_apps=shared_state.sampled_apps,
            app_file_support=shared_state.app_file_support,
            sampled_files=shared_state.sampled_files,
            exploration_context=exploration_context,
        )
        user_text = json.dumps(repair_input.to_dict(), ensure_ascii=False)
        verification_spec = self.call_json(system_prompt, user_text).get("verification")
        return verification_spec if isinstance(verification_spec, dict) else task_draft.verification.to_dict()
