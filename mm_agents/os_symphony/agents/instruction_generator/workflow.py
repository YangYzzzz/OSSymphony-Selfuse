from __future__ import annotations

import ast
import json
import logging
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

from desktop_env.osworld.desktop_env import DesktopEnv

from .app_memory import AppMemoryStore
from .base_agent import WorkflowCostTracker
from .evaluator_agents import EvaluatorCritiqueAgent, EvaluatorSynthesisAgent
from .exploration_proposal_agent import ExplorationProposalAgent
from .models import GenerationContext
from .proposal_critic_agent import ProposalCritiqueAgent
from .validators import PreflightValidator, StaticEvaluatorValidator

logger = logging.getLogger("desktopenv.instruction_generation_workflow")


class InstructionGenerationWorkflow:
    def __init__(
        self,
        rollout_task_dir: str,
        env: DesktopEnv,
        engine_params: Dict[str, Any],
        build_evaluator_fn,
        app_version_lookup,
        platform: str = "linux",
        max_repair_rounds: int = 2,
        exploration_max_actions: int = 10,
        scorer_engine_params: Dict[str, Any] | None = None,
    ):
        self.rollout_task_dir = rollout_task_dir
        self.env = env
        self.build_evaluator_fn = build_evaluator_fn
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
        )
        self.proposal_critic = ProposalCritiqueAgent("workflow_proposal_critic", scorer_engine_params, self.cost_tracker, platform)
        self.evaluator = EvaluatorSynthesisAgent("workflow_evaluator_synthesizer", engine_params, self.cost_tracker, platform)
        self.evaluator_critic = EvaluatorCritiqueAgent("workflow_evaluator_critic", scorer_engine_params, self.cost_tracker, platform)
        self.static_validator = StaticEvaluatorValidator()
        self.preflight_validator = PreflightValidator()

    def run(self, context: GenerationContext, task_nums: int, rollout_dir: str) -> Dict[str, List[str]]:
        os.makedirs(rollout_dir, exist_ok=True)
        context.app_memory, raw_memories = self.memory_store.load_many_summary(context.sampled_apps)
        generation_context = self.exploration_proposer.generate(context, self.env, task_nums, screenshot_dir=rollout_dir)
        self.env.reset(task_config={"config": context.initial_config, "id": "init_id", "instruction": "init_instruction"})
        accepted = self._generate_and_select(context, generation_context, task_nums, rollout_dir)
        generated_ids: List[str] = []
        failures: List[Dict[str, Any]] = []
        for proposal in accepted:
            if len(generated_ids) >= task_nums:
                break
            candidate = self.evaluator.synthesize(context, proposal, generation_context)
            task_config, failure, finalized_candidate = self._validate_repair_and_finalize_candidate(context, candidate, proposal, generation_context)
            self.env.reset(task_config={"config": context.initial_config, "id": "init_id", "instruction": "init_instruction"})
            if task_config:
                task_id = task_config["id"]
                json_path = os.path.join(rollout_dir, f"{task_id}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(task_config, f, indent=4, ensure_ascii=False)
                with open(os.path.join(rollout_dir, f"{task_id}.png"), "wb") as f:
                    f.write(context.setup_image)
                generated_ids.append(task_id)
                memory_task = dict(finalized_candidate or candidate)
                memory_task["id"] = task_id
                memory_task["instruction"] = task_config.get("instruction")
                memory_task["related_apps"] = task_config.get("related_apps", [])
                self.memory_store.record_finalized_many(context.sampled_apps, raw_memories, memory_task)
            elif failure:
                failures.append(failure)
                self.memory_store.record_failure_many(
                    context.sampled_apps,
                    raw_memories,
                    failure.get("failure_type", "unknown"),
                    failure.get("lesson", "Candidate failed workflow validation."),
                )
        self._write_sidecar_log(rollout_dir, context, generation_context, accepted, generated_ids, failures)
        return {self._domain_key(context): generated_ids}

    def _generate_and_select(
        self,
        context: GenerationContext,
        generation_context: Dict[str, Any],
        task_nums: int,
        rollout_dir: str,
    ) -> List[Dict[str, Any]]:
        feedback: List[Dict[str, Any]] = []
        accepted: List[Dict[str, Any]] = []
        proposals = self._proposal_list(generation_context)
        for attempt_idx in range(3):
            if attempt_idx > 0:
                self.env.reset(task_config={"config": context.initial_config, "id": "init_id", "instruction": "init_instruction"})
                generation_context = self.exploration_proposer.generate(
                    context,
                    self.env,
                    task_nums - len(accepted),
                    feedback=feedback,
                    screenshot_dir=rollout_dir,
                )
                proposals = self._proposal_list(generation_context)
            if not proposals:
                continue
            critique = self.proposal_critic.select(context, proposals, task_nums - len(accepted))
            accepted.extend([p for p in critique.get("accepted", []) if isinstance(p, dict)])
            feedback = critique.get("rejected", [])
            if len(accepted) >= task_nums:
                break
        return accepted[:task_nums]

    def _proposal_list(self, generation_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        proposals = generation_context.get("proposals") if isinstance(generation_context, dict) else []
        return [p for p in proposals if isinstance(p, dict)] if isinstance(proposals, list) else []

    def _validate_repair_and_finalize_candidate(
        self,
        context: GenerationContext,
        candidate: Dict[str, Any],
        proposal: Dict[str, Any],
        generation_context: Dict[str, Any],
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        current = self._normalize_candidate(candidate, proposal)
        last_failure: Optional[Dict[str, Any]] = None
        for round_idx in range(self.max_repair_rounds + 1):
            static = self.static_validator.validate(current)
            if not static["passed"]:
                last_failure = {
                    "failure_type": static["errors"][0] if static["errors"] else "static_validation_failed",
                    "static_validation": static,
                    "lesson": "Repair evaluator schema/code before preflight.",
                }
            else:
                task_config = self._candidate_to_task_config(context, current)
                preflight = self.preflight_validator.validate(self.env, task_config)
                if preflight["passed"]:
                    return task_config, None, current
                last_failure = {
                    "failure_type": preflight.get("failure_type") or "preflight_failed",
                    "preflight": preflight,
                    "lesson": "Initial state must not already satisfy the evaluator.",
                }
            if round_idx >= self.max_repair_rounds:
                break
            current = self._normalize_candidate(self.evaluator_critic.critique_and_repair(context, current, last_failure, generation_context), proposal)
        return None, last_failure, current

    def _normalize_candidate(self, candidate: Dict[str, Any], proposal: Dict[str, Any]) -> Dict[str, Any]:
        candidate = dict(candidate or {})
        candidate.setdefault("instruction", proposal.get("instruction") or proposal.get("description", ""))
        candidate.setdefault("config", proposal.get("config", []))
        candidate.setdefault("complexity", proposal.get("complexity", "medium"))
        candidate.setdefault("category", proposal.get("category", "mixed"))
        candidate.setdefault("estimated_steps", proposal.get("estimated_steps", -1))
        candidate.setdefault("related_apps", proposal.get("related_apps", []))
        candidate.setdefault("used_files", proposal.get("used_files", []))
        candidate.setdefault("feature_tags", proposal.get("target_features", []))
        verification = candidate.get("verification") or candidate.get("evaluation") or {}
        rule_items = verification.get("rule_items") or []
        verification["rule_items"] = rule_items if isinstance(rule_items, list) else []
        if verification["rule_items"]:
            verification["need_rule_judge"] = True
        candidate["verification"] = verification
        for idx, item in enumerate(verification.get("rule_items") or [], start=1):
            if isinstance(item, dict) and "function_name" not in item and isinstance(item.get("code"), str):
                try:
                    tree = ast.parse(item["code"])
                    for node in tree.body:
                        if isinstance(node, ast.FunctionDef):
                            item["function_name"] = node.name
                            break
                except Exception:
                    item["function_name"] = f"call_rule_judge_{idx}"
        return candidate

    def _candidate_to_task_config(self, context: GenerationContext, candidate: Dict[str, Any]) -> Dict[str, Any]:
        task_id = str(uuid.uuid4())
        related_apps = self._normalize_related_apps(candidate.get("related_apps"), context)
        launch_paths = self._normalize_launch_paths(candidate.get("used_files"), context)
        return {
            "id": task_id,
            "snapshot": related_apps[0] if related_apps else (context.sampled_apps[0] if context.sampled_apps else "ubuntu"),
            "related_apps": related_apps,
            "related_apps_version": [self.app_version_lookup(app) for app in related_apps],
            "instruction": candidate.get("instruction"),
            "config": candidate.get("config", []),
            "complexity": candidate.get("complexity"),
            "estimated_steps": candidate.get("estimated_steps"),
            "category": candidate.get("category"),
            "evaluator": self.build_evaluator_fn(candidate),
            "setup_image": f"{task_id}.png",
            "launch_paths": launch_paths,
        }

    def _normalize_related_apps(self, related_apps: Any, context: GenerationContext) -> List[str]:
        if not isinstance(related_apps, list) or not related_apps:
            return list(context.sampled_apps)
        version_to_internal = {self.app_version_lookup(app): app for app in context.sampled_apps}
        normalized: List[str] = []
        for app in related_apps:
            app = str(app)
            internal = app if app in context.sampled_apps else version_to_internal.get(app, app)
            if internal in context.sampled_apps and internal not in normalized:
                normalized.append(internal)
        return normalized or list(context.sampled_apps)

    def _normalize_launch_paths(self, used_files: Any, context: GenerationContext) -> List[str]:
        sampled = set(context.candidate_file_paths)
        if not isinstance(used_files, list):
            return []
        return [str(path) for path in used_files if str(path) in sampled]

    def _domain_key(self, context: GenerationContext) -> str:
        return "__".join(context.sampled_apps) if context.sampled_apps else context.rollout_id

    def _write_sidecar_log(
        self,
        rollout_dir: str,
        context: GenerationContext,
        generation_context: Dict[str, Any],
        accepted: List[Dict[str, Any]],
        generated_ids: List[str],
        failures: List[Dict[str, Any]],
    ) -> None:
        log_path = os.path.join(rollout_dir, "agentworkflow_generation_log.jsonl")
        payload = {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "rollout_id": context.rollout_id,
            "sampled_apps": context.sampled_apps,
            "app_file_support": context.app_file_support,
            "sampled_files": context.sampled_files,
            "initial_config": context.initial_config,
            "generation_context": generation_context,
            "accepted_count": len(accepted),
            "generated_ids": generated_ids,
            "failures": failures,
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
