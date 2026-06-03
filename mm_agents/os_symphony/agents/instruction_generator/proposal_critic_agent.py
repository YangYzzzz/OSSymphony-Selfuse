from __future__ import annotations

import json
from typing import Any, Dict, List

from mm_agents.os_symphony.agents.instruction_generator.base_agent import WorkflowCostTracker, WorkflowLLMAgent
from mm_agents.os_symphony.agents.instruction_generator.models import ProposalCandidate, ProposalSelectionInput, WorkflowSharedState
from mm_agents.os_symphony.agents.instruction_generator.prompts import load_prompt


class ProposalCritiqueAgent(WorkflowLLMAgent):
    def __init__(
        self,
        name: str,
        engine_params: Dict[str, Any],
        cost_tracker: WorkflowCostTracker,
        platform: str = "linux",
        rationality_threshold: float = 0.8,
    ):
        super().__init__(name, engine_params, cost_tracker, platform)
        self.rationality_threshold = rationality_threshold

    def select(self, shared_state: WorkflowSharedState, proposals: List[Dict[str, Any]], target_count: int) -> Dict[str, Any]:
        system_prompt = load_prompt("proposal_critic.md")
        selection_input = ProposalSelectionInput(
            target_count=target_count,
            sampled_apps=shared_state.sampled_apps,
            app_file_support=shared_state.app_file_support,
            sampled_files=shared_state.sampled_files,
            app_memory_summary=shared_state.app_memory,
            proposals=[ProposalCandidate.from_dict(proposal) for proposal in proposals],
        )
        user_text = json.dumps(selection_input.to_dict(), ensure_ascii=False)
        data = self.call_json(system_prompt, user_text)
        accepted = data.get("accepted") if isinstance(data.get("accepted"), list) else []
        rejected = data.get("rejected") if isinstance(data.get("rejected"), list) else []
        score_items = data.get("proposal_scores") if isinstance(data.get("proposal_scores"), list) else []
        scores_by_id = {
            str(item.get("proposal_id")): self._score_dict(item)
            for item in score_items
            if isinstance(item, dict) and item.get("proposal_id")
        }
        proposals_by_id = {str(proposal.get("proposal_id")): proposal for proposal in proposals if proposal.get("proposal_id")}
        normalized_accepted = [
            proposal
            for item in accepted
            for proposal in [self._accepted_to_proposal(item, proposals_by_id, scores_by_id)]
            if proposal is not None
        ]
        thresholded_accepted = [
            proposal
            for proposal in normalized_accepted
            if proposal.get("critic_scores", {}).get("rationality_score", 0.0) >= self.rationality_threshold
        ]
        thresholded_accepted.sort(key=lambda proposal: proposal.get("critic_scores", {}).get("rationality_score", 0.0), reverse=True)
        return {
            "accepted": thresholded_accepted[:target_count],
            "rejected": rejected,
            "coverage_summary": data.get("coverage_summary", {}),
            "proposal_scores": score_items,
        }

    def _accepted_to_proposal(
        self,
        item: Any,
        proposals_by_id: Dict[str, Dict[str, Any]],
        scores_by_id: Dict[str, Dict[str, float]],
    ) -> Dict[str, Any] | None:
        if isinstance(item, str):
            proposal_id = item
            proposal = proposals_by_id.get(proposal_id)
        elif isinstance(item, dict):
            proposal_id = str(item.get("proposal_id") or "")
            proposal = item if item.get("instruction") else proposals_by_id.get(proposal_id)
        else:
            return None
        if not isinstance(proposal, dict):
            return None
        normalized = dict(proposal)
        scores = dict(scores_by_id.get(proposal_id, {}))
        scores.update(self._score_dict(item) if isinstance(item, dict) else {})
        if scores:
            normalized["critic_scores"] = scores
        return normalized

    def _score_dict(self, item: Dict[str, Any]) -> Dict[str, float]:
        raw_scores = item.get("critic_scores") if isinstance(item.get("critic_scores"), dict) else item
        scores: Dict[str, float] = {}
        for key in ("rationality_score", "complexity_score"):
            try:
                scores[key] = max(0.0, min(1.0, float(raw_scores.get(key))))
            except (AttributeError, TypeError, ValueError):
                continue
        return scores
