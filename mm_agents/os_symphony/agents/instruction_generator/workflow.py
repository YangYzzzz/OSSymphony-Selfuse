from __future__ import annotations

import json
import logging
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

from desktop_env.osworld.desktop_env import DesktopEnv

from mm_agents.os_symphony.agents.instruction_generator.app_memory import AppMemoryStore
from mm_agents.os_symphony.agents.instruction_generator.base_agent import WorkflowCostTracker
from mm_agents.os_symphony.agents.instruction_generator.evaluator_agents import EvaluatorCritiqueAgent, EvaluatorSynthesisAgent
from mm_agents.os_symphony.agents.instruction_generator.exploration_proposal_agent import ExplorationProposalAgent
from mm_agents.os_symphony.agents.instruction_generator.models import AcceptedProposalWorkItem, ExplorationContext, ExplorationResult, GenerationRunLog, ProposalCandidate, TaskCandidate, WorkflowSharedState
from mm_agents.os_symphony.agents.instruction_generator.proposal_critic_agent import ProposalCritiqueAgent
from mm_agents.os_symphony.agents.instruction_generator.validators import PreflightValidator, StaticEvaluatorValidator

logger = logging.getLogger("desktopenv.instruction_generation_workflow")


class InstructionGenerationWorkflow:
    def __init__(
        self,
        rollout_task_dir: str,
        env: DesktopEnv,
        engine_params: Dict[str, Any],
        build_evaluator_from_task_fn,
        app_version_lookup,
        platform: str = "linux",
        max_repair_rounds: int = 2,
        exploration_max_actions: int = 10,
        scorer_engine_params: Dict[str, Any] | None = None,
        input_screen_size: Tuple[int, int] | None = None,
    ):
        self.rollout_task_dir = rollout_task_dir
        self.env = env
        self.build_evaluator_from_task_fn = build_evaluator_from_task_fn
        self.app_version_lookup = app_version_lookup
        self.max_repair_rounds = max_repair_rounds
        self.cost_tracker = WorkflowCostTracker(rollout_task_dir)
        self.memory_store = AppMemoryStore()
        scorer_engine_params = scorer_engine_params or engine_params
        self.exploration_proposer = ExplorationProposalAgent(
            "workflow_exploration_proposal_generator",
            engine_params,
            self.cost_tracker,
            platform,
            max_actions=exploration_max_actions,
            input_screen_size=input_screen_size,
        )
        self.proposal_critic = ProposalCritiqueAgent("workflow_proposal_critic", scorer_engine_params, self.cost_tracker, platform)
        self.verification_synthesizer = EvaluatorSynthesisAgent("workflow_evaluator_synthesizer", engine_params, self.cost_tracker, platform)
        self.verification_critic = EvaluatorCritiqueAgent("workflow_evaluator_critic", scorer_engine_params, self.cost_tracker, platform)
        self.static_validator = StaticEvaluatorValidator()
        self.preflight_validator = PreflightValidator()

    def run(self, shared_state: WorkflowSharedState, task_nums: int, rollout_dir: str) -> Dict[str, List[str]]:
        os.makedirs(rollout_dir, exist_ok=True)
        proposal_memory, evaluator_memory, raw_memories = self.memory_store.load_many_summaries(shared_state.sampled_apps)

        shared_state.app_memory = proposal_memory
        exploration_result = ExplorationResult.from_dict(self.exploration_proposer.generate(shared_state, self.env, task_nums, screenshot_dir=rollout_dir))
        accepted_work_items = self._generate_and_select(shared_state, exploration_result, task_nums, rollout_dir)
        generated_ids: List[str] = []
        failures: List[Dict[str, Any]] = []
        logger.info(f"Generation Accepted Proposals: {[item.proposal.to_dict() for item in accepted_work_items]}")

        self.env.reset(task_config={"config": shared_state.initial_config, "id": "init_id", "instruction": "init_instruction"})
        time.sleep(60)
        obs = self.env._get_obs()
        with open(os.path.join(rollout_dir, f"setup.png"), "wb") as f:
            f.write(obs["screenshot"])

        for work_item in accepted_work_items:
            if len(generated_ids) >= task_nums:
                break
            shared_state.app_memory = evaluator_memory
            verification_spec = self.verification_synthesizer.synthesize(
                shared_state,
                work_item.proposal,
                work_item.exploration_result,
                evaluator_memory,
            )
            task_config, failure, finalized_task_draft = self._validate_repair_and_build_task_config(
                shared_state,
                work_item.proposal,
                verification_spec,
                ExplorationContext(
                    trajectory=work_item.exploration_result.trajectory,
                    generation_notes=work_item.exploration_result.generation_notes,
                ),
            )
            if task_config:
                task_id = task_config["id"]
                json_path = os.path.join(rollout_dir, f"{task_id}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(task_config, f, indent=4, ensure_ascii=False)
                generated_ids.append(task_id)
                memory_task = dict(finalized_task_draft)
                memory_task["id"] = task_id
                memory_task["instruction"] = task_config.get("instruction")
                memory_task["related_apps"] = task_config.get("related_apps", [])
                self.memory_store.record_finalized_many(shared_state.sampled_apps, raw_memories, memory_task)
            elif failure:
                failures.append(failure)
        self._write_sidecar_log(rollout_dir, shared_state, exploration_result, accepted_work_items, generated_ids, failures)
        return {shared_state.rollout_id: generated_ids}

    def _generate_and_select(
        self,
        shared_state: WorkflowSharedState,
        exploration_result: ExplorationResult,
        task_nums: int,
        rollout_dir: str,
    ) -> List[AcceptedProposalWorkItem]:
        feedback: List[Dict[str, Any]] = []
        accepted: List[AcceptedProposalWorkItem] = []
        proposals = [proposal.to_dict() for proposal in exploration_result.proposals]
        for attempt_idx in range(2):
            if attempt_idx > 0:
                self.env.reset(task_config={"config": shared_state.initial_config, "id": "init_id", "instruction": "init_instruction"})
                exploration_result = ExplorationResult.from_dict(
                    self.exploration_proposer.generate(
                        shared_state,
                        self.env,
                        task_nums - len(accepted),
                        feedback=feedback,
                        screenshot_dir=rollout_dir,
                    )
                )
                proposals = [proposal.to_dict() for proposal in exploration_result.proposals]
            if not proposals:
                continue
            critique = self.proposal_critic.select(shared_state, proposals, task_nums - len(accepted))
            proposals_by_id = {p.get("proposal_id"): p for p in proposals if p.get("proposal_id")}
            for item in critique.get("accepted", []):
                if isinstance(item, dict):
                    accepted.append(AcceptedProposalWorkItem(ProposalCandidate.from_dict(item), exploration_result))
                elif isinstance(item, str) and item in proposals_by_id:
                    accepted.append(AcceptedProposalWorkItem(ProposalCandidate.from_dict(proposals_by_id[item]), exploration_result))
            feedback = critique.get("rejected", [])
            if len(accepted) >= task_nums:
                break
        return accepted[:task_nums]

    def _validate_repair_and_build_task_config(
        self,
        shared_state: WorkflowSharedState,
        accepted_proposal: ProposalCandidate,
        initial_verification_spec: Dict[str, Any],
        exploration_context: ExplorationContext,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], Dict[str, Any]]:
        task_draft = self._build_task_draft(accepted_proposal, initial_verification_spec)
        last_failure: Optional[Dict[str, Any]] = None
        for round_idx in range(self.max_repair_rounds + 1):
            static = self.static_validator.validate(task_draft)
            if not static["passed"]:
                last_failure = {
                    "failure_type": static["errors"][0] if static["errors"] else "static_validation_failed",
                    "static_validation": static,
                    "lesson": "Repair verification schema/code before preflight.",
                }
            else:
                task_config = self._task_draft_to_task_config(shared_state, task_draft)
                preflight = self.preflight_validator.validate(self.env, task_config)
                if preflight["passed"]:
                    return task_config, None, task_draft
                last_failure = {
                    "failure_type": preflight.get("failure_type") or "preflight_failed",
                    "preflight": preflight,
                    "lesson": "Initial state must not already satisfy the evaluator." + preflight.get("details", ""),
                }
            if round_idx >= self.max_repair_rounds:
                break
            repaired_verification_spec = self.verification_critic.critique_and_repair(
                shared_state,
                task_draft,
                last_failure,
                exploration_context,
            )
            task_draft = self._build_task_draft(accepted_proposal, repaired_verification_spec)
        return None, last_failure, task_draft

    def _build_task_draft(self, accepted_proposal: ProposalCandidate, verification_spec: Dict[str, Any]) -> Dict[str, Any]:
        verification = dict(verification_spec) if isinstance(verification_spec, dict) else {}
        if isinstance(verification.get("rule_items"), list) and verification["rule_items"]:
            verification["need_rule_judge"] = True
        for idx, rule_item in enumerate(verification.get("rule_items") or [], start=1):
            if isinstance(rule_item, dict) and "function_name" not in rule_item and isinstance(rule_item.get("code"), str):
                rule_item["function_name"] = f"call_rule_judge_{idx}"
        return TaskCandidate.from_proposal(accepted_proposal, verification).to_dict()

    def _list_or_default(self, value: Any) -> List[Any]:
        return value if isinstance(value, list) else []

    def _int_or_default(self, value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _task_draft_to_task_config(self, shared_state: WorkflowSharedState, task_draft: Dict[str, Any]) -> Dict[str, Any]:
        task_id = str(uuid.uuid4())
        related_apps = self._normalize_related_apps(task_draft.get("related_apps"), shared_state)
        launch_paths = self._normalize_launch_paths(task_draft.get("used_files"), shared_state)
        return {
            "id": task_id,
            "snapshot": related_apps[0] if related_apps else (shared_state.sampled_apps[0] if shared_state.sampled_apps else "ubuntu"),
            "related_apps": related_apps,
            "related_apps_version": [self.app_version_lookup(app) for app in related_apps],
            "instruction": task_draft.get("instruction"),
            "config": task_draft.get("config", []),
            "complexity": task_draft.get("complexity"),
            "estimated_steps": task_draft.get("estimated_steps"),
            "category": task_draft.get("category"),
            "evaluator": self.build_evaluator_from_task_fn(task_draft),
            "setup_image": f"setup.png",
            "launch_paths": launch_paths,
        }

    def _normalize_related_apps(self, related_apps: Any, shared_state: WorkflowSharedState) -> List[str]:
        if not isinstance(related_apps, list) or not related_apps:
            return list(shared_state.sampled_apps)
        version_to_internal = {self.app_version_lookup(app): app for app in shared_state.sampled_apps}
        normalized: List[str] = []
        for app in related_apps:
            app = str(app)
            internal = app if app in shared_state.sampled_apps else version_to_internal.get(app, app)
            if internal in shared_state.sampled_apps and internal not in normalized:
                normalized.append(internal)
        return normalized or list(shared_state.sampled_apps)

    def _normalize_launch_paths(self, used_files: Any, shared_state: WorkflowSharedState) -> List[str]:
        sampled = set(shared_state.candidate_file_paths)
        if not isinstance(used_files, list):
            return []
        return [str(path) for path in used_files if str(path) in sampled]

    def _write_sidecar_log(
        self,
        rollout_dir: str,
        shared_state: WorkflowSharedState,
        exploration_result: ExplorationResult,
        accepted: List[AcceptedProposalWorkItem],
        generated_ids: List[str],
        failures: List[Dict[str, Any]],
    ) -> None:
        log_path = os.path.join(rollout_dir, "agentworkflow_generation_log.jsonl")
        payload = GenerationRunLog(
            time=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            rollout_id=shared_state.rollout_id,
            sampled_apps=shared_state.sampled_apps,
            app_file_support=shared_state.app_file_support,
            sampled_files=shared_state.sampled_files,
            initial_config=shared_state.initial_config,
            exploration_result=exploration_result.to_dict(),
            accepted_count=len(accepted),
            generated_ids=generated_ids,
            failures=failures,
        ).to_dict()
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
