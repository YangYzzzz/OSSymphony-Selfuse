from __future__ import annotations

import ast
import copy
import json
import logging
import os
import re
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from desktop_env.osworld.desktop_env import DesktopEnv
from mm_agents.os_symphony.core.mllm import LMMAgent

logger = logging.getLogger("desktopenv.instruction_generation_workflow")

APP_MEMORY_DIR = os.path.join(
    "mm_agents",
    "os_symphony",
    "agents",
    "instruction_generator",
    "app_memory",
)

ALLOWED_GETTER_TYPES = {"vm_file", "vm_command_line", "empty"}
DANGEROUS_IMPORTS = {
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "httpx",
    "shutil",
    "pathlib",
}
DANGEROUS_CALLS = {
    "system",
    "popen",
    "remove",
    "unlink",
    "rmdir",
    "removedirs",
    "rename",
    "write",
    "writelines",
}


@dataclass
class GenerationContext:
    main_app: str
    apps_for_group: List[str]
    task_setup_config: List[Dict[str, Any]]
    launch_paths: List[str]
    golden_paths: List[str]
    setup_image: bytes
    app_tutorial_md: str
    app_memory: Dict[str, Any]
    app_name: str
    allowed_apps: List[str]
    observation: Dict[str, Any]


class WorkflowCostTracker:
    def __init__(self, output_dir: str):
        self.output_path = os.path.join(output_dir, "agentworkflow_cost.jsonl")
        os.makedirs(output_dir, exist_ok=True)
        self.calls: Dict[str, int] = {}

    def record(
        self,
        agent_name: str,
        duration_ms: float,
        success: bool,
        usage: Any = None,
        error: str | None = None,
    ) -> None:
        self.calls[agent_name] = self.calls.get(agent_name, 0) + 1
        payload = {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "agent_name": agent_name,
            "call_index": self.calls[agent_name],
            "duration_ms": duration_ms,
            "success": success,
            "error": error,
        }
        if usage is not None:
            payload["usage"] = {
                "prompt_tokens": getattr(usage, "prompt_tokens", None),
                "completion_tokens": getattr(usage, "completion_tokens", None),
                "total_tokens": getattr(usage, "total_tokens", None),
            }
        try:
            with open(self.output_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.warning("Failed to write workflow cost log: %s", e)


class AppMemoryStore:
    def __init__(self, memory_dir: str = APP_MEMORY_DIR):
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)

    def _path(self, app: str) -> str:
        safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", app)
        return os.path.join(self.memory_dir, f"{safe_name}.json")

    def load(self, app: str) -> Dict[str, Any]:
        path = self._path(app)
        if not os.path.exists(path):
            return self._default_memory(app)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return self._default_memory(app)
            data.setdefault("app", app)
            data.setdefault("version", 1)
            data.setdefault("covered_features", {})
            data.setdefault("recent_tasks", [])
            data.setdefault("known_good_verification_channels", [])
            data.setdefault("failure_patterns", [])
            data.setdefault("next_generation_bias", {})
            return data
        except Exception:
            return self._default_memory(app)

    def save(self, app: str, memory: Dict[str, Any]) -> None:
        path = self._path(app)
        tmp_path = f"{path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)

    def summary(self, memory: Dict[str, Any]) -> str:
        return json.dumps(
            {
                "covered_features": memory.get("covered_features", {}),
                "known_good_verification_channels": memory.get("known_good_verification_channels", []),
                "failure_patterns": memory.get("failure_patterns", [])[-8:],
                "next_generation_bias": memory.get("next_generation_bias", {}),
                "recent_tasks": memory.get("recent_tasks", [])[-8:],
            },
            ensure_ascii=False,
        )

    def record_finalized(self, app: str, memory: Dict[str, Any], task: Dict[str, Any]) -> None:
        feature_tags = task.get("feature_tags") or task.get("target_features") or []
        if not isinstance(feature_tags, list):
            feature_tags = []
        covered = memory.setdefault("covered_features", {})
        for tag in feature_tags:
            tag = str(tag)
            covered[tag] = int(covered.get(tag, 0)) + 1
        recent = memory.setdefault("recent_tasks", [])
        recent.append(
            {
                "task_id": task.get("id"),
                "feature_tags": feature_tags,
                "category": task.get("category"),
                "instruction_summary": str(task.get("instruction") or task.get("description") or "")[:180],
                "preflight_passed": True,
            }
        )
        memory["recent_tasks"] = recent[-30:]
        memory["version"] = int(memory.get("version", 1)) + 1
        self._update_bias(memory)
        self.save(app, memory)

    def record_failure(self, app: str, memory: Dict[str, Any], failure_type: str, lesson: str) -> None:
        failures = memory.setdefault("failure_patterns", [])
        failures.append({"type": failure_type, "lesson": lesson})
        memory["failure_patterns"] = failures[-30:]
        memory["version"] = int(memory.get("version", 1)) + 1
        self.save(app, memory)

    def _update_bias(self, memory: Dict[str, Any]) -> None:
        covered = memory.get("covered_features", {})
        if not covered:
            memory["next_generation_bias"] = {}
            return
        ordered = sorted(covered.items(), key=lambda item: item[1])
        memory["next_generation_bias"] = {
            "undercovered_features": [k for k, _ in ordered[:5]],
            "overcovered_features": [k for k, _ in ordered[-5:]],
        }

    def _default_memory(self, app: str) -> Dict[str, Any]:
        return {
            "app": app,
            "version": 1,
            "covered_features": {},
            "recent_tasks": [],
            "known_good_verification_channels": [],
            "failure_patterns": [],
            "next_generation_bias": {},
        }


class WorkflowLLMAgent:
    def __init__(self, name: str, engine_params: Dict[str, Any], cost_tracker: WorkflowCostTracker, platform: str = "linux"):
        self.name = name
        self.engine_params = copy.deepcopy(engine_params)
        self.engine_params["agent_name"] = name
        self.temperature = self.engine_params.get("temperature", 0.5)
        self.platform = platform
        self.cost_tracker = cost_tracker
        self.agent = LMMAgent(engine_params=self.engine_params, system_prompt="")

    def call_json(self, system_prompt: str, user_text: str, image_content: bytes | None = None, retries: int = 3) -> Dict[str, Any]:
        last_error = ""
        for attempt in range(1, retries + 1):
            self.agent.reset()
            self.agent.add_system_prompt(system_prompt)
            self.agent.add_message(text_content=user_text, image_content=image_content, role="user")
            start = time.time()
            usage = None
            success = False
            try:
                response = self.agent.get_response(temperature=self.temperature)
                if isinstance(response, tuple):
                    response, usage = response
                response = self._strip_json_fence(str(response or ""))
                data = json.loads(response)
                success = True
                return data
            except Exception as e:
                last_error = str(e)
                logger.warning("%s attempt %s/%s failed: %s", self.name, attempt, retries, e)
            finally:
                self.cost_tracker.record(
                    agent_name=self.name,
                    duration_ms=(time.time() - start) * 1000.0,
                    success=success,
                    usage=usage,
                    error=None if success else last_error,
                )
        raise ValueError(f"{self.name} failed to return valid JSON: {last_error}")

    def _strip_json_fence(self, response: str) -> str:
        response = response.strip()
        match = re.search(r"^```(?:json)?\s*\n?(.*?)\n?```$", response, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response


class SandboxExplorationAgent(WorkflowLLMAgent):
    def explore(self, context: GenerationContext, env: DesktopEnv) -> Dict[str, Any]:
        file_inventory = self._build_file_inventory(context.launch_paths, env)
        system_prompt = """
You summarize a GUI task generation sandbox. Return only valid JSON.
Schema: {"visible_state": string, "file_inventory": array, "app_affordances_seen": array, "safe_verification_channels": array, "constraints": array}
Use only the screenshot and read-only file metadata provided. Do not propose task completion steps.
""".strip()
        user_text = json.dumps(
            {
                "main_app": context.app_name,
                "allowed_apps": context.allowed_apps,
                "launch_paths": context.launch_paths,
                "golden_paths": context.golden_paths,
                "file_inventory": file_inventory,
                "app_memory": context.app_memory,
            },
            ensure_ascii=False,
        )
        try:
            data = self.call_json(system_prompt, user_text, context.setup_image)
        except Exception as e:
            logger.warning("Exploration summary failed, using deterministic fallback: %s", e)
            data = {}
        return {
            "visible_state": str(data.get("visible_state") or "Initial application screenshot is available."),
            "file_inventory": data.get("file_inventory") if isinstance(data.get("file_inventory"), list) else file_inventory,
            "app_affordances_seen": data.get("app_affordances_seen") if isinstance(data.get("app_affordances_seen"), list) else [],
            "safe_verification_channels": data.get("safe_verification_channels") if isinstance(data.get("safe_verification_channels"), list) else self._infer_channels(context.launch_paths),
            "constraints": data.get("constraints") if isinstance(data.get("constraints"), list) else [],
        }

    def _build_file_inventory(self, paths: List[str], env: DesktopEnv) -> List[Dict[str, Any]]:
        inventory = []
        for path in paths[:10]:
            entry = {"path": path, "type": os.path.splitext(path)[1].lstrip(".") or "directory"}
            try:
                result = env.controller.execute_python_command("import os, json, sys\n" + f"p={path!r}\n" + "print(json.dumps({'exists': os.path.exists(p), 'is_dir': os.path.isdir(p), 'size': os.path.getsize(p) if os.path.exists(p) and not os.path.isdir(p) else None}))")
                output = (result or {}).get("output", "").strip()
                if output:
                    entry.update(json.loads(output.splitlines()[-1]))
            except Exception:
                entry["exists"] = None
            inventory.append(entry)
        return inventory

    def _infer_channels(self, paths: List[str]) -> List[str]:
        channels = ["vm_command_line"]
        for path in paths:
            ext = os.path.splitext(path)[1].lower().lstrip(".")
            if ext:
                channels.append(f"vm_file:{ext}")
        return sorted(set(channels))


class ProposalGenerationAgent(WorkflowLLMAgent):
    def generate_proposals(self, context: GenerationContext, exploration: Dict[str, Any], target_count: int, feedback: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
        oversample = max(target_count + 3, int(target_count * 1.6))
        system_prompt = f"""
You generate GUI task proposals for Ubuntu applications. Return only valid JSON.
Generate exactly {oversample} proposals. Each proposal must follow this schema:
{{"proposal_id":"p01","description":"goal-oriented user request","category":"file_only|app_only|mixed","complexity":"simple|medium|complex","estimated_steps":20,"related_apps":[],"target_features":[],"required_artifacts":[],"success_criteria":[],"verification_plan_hint":{{"preferred":"rule|vlm|hybrid","channels":[],"rationale":""}}}}
Requirements:
- The main app must be used in every proposal.
- Prefer medium/complex realistic user tasks, not one-step edits.
- Include exact ~/ or /home/user paths for evaluator-critical files.
- Use current launch_paths and exploration summary; do not assume unstated files.
- Diversify across content, settings/preferences, layout, import/export, cross-app, file transformation when possible.
- Down-rank overcovered app-memory features and avoid repeated failure patterns.
""".strip()
        user_text = json.dumps(
            {
                "main_app": context.app_name,
                "allowed_apps": context.allowed_apps,
                "launch_paths": context.launch_paths,
                "golden_paths": context.golden_paths,
                "app_tutorial_md": context.app_tutorial_md,
                "app_memory_summary": context.app_memory,
                "exploration_summary": exploration,
                "previous_rejection_feedback": feedback or [],
            },
            ensure_ascii=False,
        )
        data = self.call_json(system_prompt, user_text, context.setup_image)
        proposals = data.get("proposals", [])
        if not isinstance(proposals, list):
            return []
        return [p for p in proposals if isinstance(p, dict)]


class ProposalCritiqueAgent(WorkflowLLMAgent):
    def select(self, context: GenerationContext, proposals: List[Dict[str, Any]], target_count: int) -> Dict[str, Any]:
        system_prompt = f"""
You critique GUI task proposals. Return only valid JSON.
Select up to {target_count} accepted proposals. Score specificity, realism, complexity, verifiability, data fit, diversity, and non-destructiveness.
Reject tasks that are single-step, subjective, destructive, dependent on unstable network data, or not grounded in launch_paths/exploration.
Schema: {{"accepted": [proposal objects], "rejected": [{{"proposal_id":"...","reason":"...","suggested_repair":"..."}}], "coverage_summary": {{}}}}
""".strip()
        user_text = json.dumps(
            {
                "main_app": context.app_name,
                "allowed_apps": context.allowed_apps,
                "launch_paths": context.launch_paths,
                "golden_paths": context.golden_paths,
                "app_memory_summary": context.app_memory,
                "proposals": proposals,
            },
            ensure_ascii=False,
        )
        data = self.call_json(system_prompt, user_text, context.setup_image)
        accepted = data.get("accepted") if isinstance(data.get("accepted"), list) else []
        rejected = data.get("rejected") if isinstance(data.get("rejected"), list) else []
        return {"accepted": accepted[:target_count], "rejected": rejected, "coverage_summary": data.get("coverage_summary", {})}


class EvaluatorSynthesisAgent(WorkflowLLMAgent):
    def synthesize(self, context: GenerationContext, proposal: Dict[str, Any], exploration: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = """
You synthesize a complete evaluator for one accepted GUI task proposal. Return only valid JSON.
Return schema: {"task_candidate":{"description":"...","complexity":"simple|medium|complex","category":"file_only|app_only|mixed","related_apps":[],"estimated_steps":20,"feature_tags":[],"verification":{"need_rule_judge":bool,"need_vlm_judge":bool,"vlm_desc":"","rule_items":[{"result_getter":{},"expected_getter":{},"code":"full python function"}]}}}
Rule getter types allowed: vm_file, vm_command_line, empty.
Rule function names must start with call_rule_judge_ and signature must be def call_rule_judge_N(result, expected, **options) -> float.
Prefer rule-based checks. VLM-only candidates are weak and should be avoided.
Do not use dangerous operations in rule code: subprocess, os.system, network access, writing/deleting files.
""".strip()
        user_text = json.dumps(
            {
                "proposal": proposal,
                "main_app": context.app_name,
                "allowed_apps": context.allowed_apps,
                "launch_paths": context.launch_paths,
                "golden_paths": context.golden_paths,
                "exploration_summary": exploration,
                "app_tutorial_md": context.app_tutorial_md,
            },
            ensure_ascii=False,
        )
        data = self.call_json(system_prompt, user_text, context.setup_image)
        candidate = data.get("task_candidate")
        return candidate if isinstance(candidate, dict) else {}


class CandidateRepairAgent(WorkflowLLMAgent):
    def repair(self, context: GenerationContext, candidate: Dict[str, Any], failure: Dict[str, Any], exploration: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = """
You repair one GUI task candidate without changing its core intent unless required by the failure.
Return only valid JSON with schema {"task_candidate": {...}} using the same candidate schema.
For code_invalid, repair only evaluator code. For init_reward_positive, make the success conditions stricter or change the output target.
Prefer adding stable rule-based negative/preflight checks over VLM-only judgement.
""".strip()
        user_text = json.dumps(
            {
                "candidate": candidate,
                "failure": failure,
                "main_app": context.app_name,
                "allowed_apps": context.allowed_apps,
                "launch_paths": context.launch_paths,
                "golden_paths": context.golden_paths,
                "exploration_summary": exploration,
            },
            ensure_ascii=False,
        )
        data = self.call_json(system_prompt, user_text, context.setup_image)
        repaired = data.get("task_candidate")
        return repaired if isinstance(repaired, dict) else candidate


class StaticEvaluatorValidator:
    def validate(self, task: Dict[str, Any]) -> Dict[str, Any]:
        warnings: List[str] = []
        errors: List[str] = []
        verification = task.get("verification") or {}
        need_rule = bool(verification.get("need_rule_judge"))
        need_vlm = bool(verification.get("need_vlm_judge"))
        rule_items = verification.get("rule_items") or []
        if not need_rule and not need_vlm:
            errors.append("no_judge_enabled")
        if need_rule and not rule_items:
            errors.append("missing_rule_items")
        if need_vlm and not str(verification.get("vlm_desc", "")).strip():
            warnings.append("missing_vlm_desc")
        if need_vlm and not need_rule:
            errors.append("vlm_only_weak")
        if not isinstance(rule_items, list):
            errors.append("rule_items_not_list")
            rule_items = []
        for idx, item in enumerate(rule_items, start=1):
            self._validate_rule_item(item, idx, errors, warnings)
        return {"passed": not errors, "errors": errors, "warnings": warnings}

    def _validate_rule_item(self, item: Any, idx: int, errors: List[str], warnings: List[str]) -> None:
        if not isinstance(item, dict):
            errors.append(f"rule_{idx}_not_object")
            return
        for key in ("result_getter", "expected_getter"):
            getter = item.get(key) or {"type": "empty"}
            self._validate_getter(getter, f"rule_{idx}_{key}", errors)
        code = item.get("code")
        if not isinstance(code, str) or not code.strip():
            errors.append(f"rule_{idx}_missing_code")
            return
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            errors.append(f"rule_{idx}_code_invalid:{e}")
            return
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        if not functions:
            errors.append(f"rule_{idx}_missing_function")
            return
        fn = functions[0]
        if not fn.name.startswith("call_rule_judge_"):
            errors.append(f"rule_{idx}_bad_function_name")
        if item.get("function_name") and item.get("function_name") != fn.name:
            warnings.append(f"rule_{idx}_function_name_mismatch")
        args = [arg.arg for arg in fn.args.args]
        has_kwargs = fn.args.kwarg is not None and fn.args.kwarg.arg == "options"
        if args[:2] != ["result", "expected"] or not has_kwargs:
            errors.append(f"rule_{idx}_bad_signature")
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name.split(".")[0] for alias in node.names]
                if any(name in DANGEROUS_IMPORTS for name in names):
                    errors.append(f"rule_{idx}_dangerous_import")
                    break
            if isinstance(node, ast.Call):
                call_name = self._call_name(node.func)
                if call_name.split(".")[-1] in DANGEROUS_CALLS or call_name in {"os.system", "subprocess.run", "subprocess.Popen"}:
                    errors.append(f"rule_{idx}_dangerous_call:{call_name}")
                    break

    def _validate_getter(self, getter: Any, label: str, errors: List[str]) -> None:
        if not isinstance(getter, dict):
            errors.append(f"{label}_not_object")
            return
        getter_type = getter.get("type")
        if getter_type not in ALLOWED_GETTER_TYPES:
            errors.append(f"{label}_bad_type:{getter_type}")
            return
        if getter_type == "vm_file":
            path = str(getter.get("path", ""))
            if not path.startswith("/"):
                errors.append(f"{label}_path_not_absolute")
        if getter_type == "vm_command_line" and not isinstance(getter.get("command"), list):
            errors.append(f"{label}_command_not_list")

    def _call_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            prefix = self._call_name(node.value)
            return f"{prefix}.{node.attr}" if prefix else node.attr
        return ""


class PreflightValidator:
    def validate(self, env: DesktopEnv, task_config: Dict[str, Any]) -> Dict[str, Any]:
        try:
            env.reset(
                task_config={
                    "config": task_config.get("config", []),
                    "id": task_config["id"],
                    "instruction": task_config.get("instruction", ""),
                    "evaluator": task_config.get("evaluator", {}),
                }
            )
            reward = float(env.evaluate())
            return {
                "passed": reward <= 1e-6,
                "init_rule_reward": reward,
                "details": [],
                "failure_type": "init_reward_positive" if reward > 1e-6 else None,
            }
        except Exception as e:
            return {
                "passed": False,
                "init_rule_reward": None,
                "details": [str(e)],
                "failure_type": "getter_failed",
            }


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
    ):
        self.rollout_task_dir = rollout_task_dir
        self.env = env
        self.build_evaluator_fn = build_evaluator_fn
        self.app_version_lookup = app_version_lookup
        self.max_repair_rounds = max_repair_rounds
        self.cost_tracker = WorkflowCostTracker(rollout_task_dir)
        self.memory_store = AppMemoryStore()
        self.explorer = SandboxExplorationAgent("workflow_sandbox_explorer", engine_params, self.cost_tracker, platform)
        self.proposer = ProposalGenerationAgent("workflow_proposal_generator", engine_params, self.cost_tracker, platform)
        self.critic = ProposalCritiqueAgent("workflow_proposal_critic", engine_params, self.cost_tracker, platform)
        self.evaluator = EvaluatorSynthesisAgent("workflow_evaluator_synthesizer", engine_params, self.cost_tracker, platform)
        self.repairer = CandidateRepairAgent("workflow_candidate_repairer", engine_params, self.cost_tracker, platform)
        self.static_validator = StaticEvaluatorValidator()
        self.preflight_validator = PreflightValidator()

    def run(self, context: GenerationContext, task_nums: int, domain_dir: str) -> Dict[str, List[str]]:
        os.makedirs(domain_dir, exist_ok=True)
        image_base_dir = os.path.join(domain_dir, "image")
        os.makedirs(image_base_dir, exist_ok=True)
        app_memory = self.memory_store.load(context.main_app)
        context.app_memory = json.loads(self.memory_store.summary(app_memory))
        exploration = self.explorer.explore(context, self.env)
        self.env.reset(task_config={"config": context.task_setup_config, "id": "init_id", "instruction": "init_instruction"})
        accepted = self._generate_and_select(context, exploration, task_nums)
        generated_ids: List[str] = []
        failures: List[Dict[str, Any]] = []
        for proposal in accepted:
            if len(generated_ids) >= task_nums:
                break
            candidate = self.evaluator.synthesize(context, proposal, exploration)
            task_config, failure = self._validate_repair_and_finalize_candidate(context, candidate, proposal, exploration)
            self.env.reset(task_config={"config": context.task_setup_config, "id": "init_id", "instruction": "init_instruction"})
            if task_config:
                task_id = task_config["id"]
                json_path = os.path.join(domain_dir, f"{task_id}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(task_config, f, indent=4, ensure_ascii=False)
                with open(os.path.join(image_base_dir, f"{task_id}.png"), "wb") as f:
                    f.write(context.setup_image)
                generated_ids.append(task_id)
                memory_task = dict(candidate)
                memory_task["id"] = task_id
                memory_task["instruction"] = task_config.get("instruction")
                self.memory_store.record_finalized(context.main_app, app_memory, memory_task)
            elif failure:
                failures.append(failure)
                self.memory_store.record_failure(
                    context.main_app,
                    app_memory,
                    failure.get("failure_type", "unknown"),
                    failure.get("lesson", "Candidate failed workflow validation."),
                )
        self._write_sidecar_log(domain_dir, context, exploration, accepted, generated_ids, failures)
        return {context.main_app: generated_ids}

    def _generate_and_select(self, context: GenerationContext, exploration: Dict[str, Any], task_nums: int) -> List[Dict[str, Any]]:
        feedback: List[Dict[str, Any]] = []
        accepted: List[Dict[str, Any]] = []
        for _ in range(3):
            proposals = self.proposer.generate_proposals(context, exploration, task_nums, feedback)
            critique = self.critic.select(context, proposals, task_nums - len(accepted))
            accepted.extend([p for p in critique.get("accepted", []) if isinstance(p, dict)])
            feedback = critique.get("rejected", [])
            if len(accepted) >= task_nums:
                break
        return accepted[:task_nums]

    def _validate_repair_and_finalize_candidate(
        self,
        context: GenerationContext,
        candidate: Dict[str, Any],
        proposal: Dict[str, Any],
        exploration: Dict[str, Any],
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
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
                    return task_config, None
                last_failure = {
                    "failure_type": preflight.get("failure_type") or "preflight_failed",
                    "preflight": preflight,
                    "lesson": "Initial state must not already satisfy the evaluator.",
                }
            if round_idx >= self.max_repair_rounds:
                break
            current = self._normalize_candidate(self.repairer.repair(context, current, last_failure, exploration), proposal)
        return None, last_failure

    def _normalize_candidate(self, candidate: Dict[str, Any], proposal: Dict[str, Any]) -> Dict[str, Any]:
        candidate = dict(candidate or {})
        candidate.setdefault("description", proposal.get("description", ""))
        candidate.setdefault("complexity", proposal.get("complexity", "medium"))
        candidate.setdefault("category", proposal.get("category", "mixed"))
        candidate.setdefault("estimated_steps", proposal.get("estimated_steps", -1))
        candidate.setdefault("related_apps", proposal.get("related_apps", []))
        candidate.setdefault("feature_tags", proposal.get("target_features", []))
        verification = candidate.get("verification") or candidate.get("evaluation") or {}
        if "rule_items" not in verification:
            verification["rule_items"] = []
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
        related_apps = candidate.get("related_apps") or [context.main_app]
        related_apps_internal = [self._version_to_internal_name(app, context) for app in related_apps]
        if context.main_app not in related_apps_internal:
            related_apps_internal.insert(0, context.main_app)
        return {
            "id": task_id,
            "snapshot": context.main_app,
            "related_apps": related_apps_internal,
            "related_apps_version": [self.app_version_lookup(app) for app in related_apps_internal],
            "instruction": candidate.get("description"),
            "config": context.task_setup_config,
            "complexity": candidate.get("complexity"),
            "estimated_steps": candidate.get("estimated_steps"),
            "category": candidate.get("category"),
            "evaluator": self.build_evaluator_fn(candidate),
            "setup_image": f"image/{task_id}.png",
            "launch_paths": context.launch_paths,
        }

    def _version_to_internal_name(self, app: str, context: GenerationContext) -> str:
        if app in context.apps_for_group:
            return app
        version_to_internal = {self.app_version_lookup(internal): internal for internal in context.apps_for_group}
        return version_to_internal.get(app, app)

    def _write_sidecar_log(
        self,
        domain_dir: str,
        context: GenerationContext,
        exploration: Dict[str, Any],
        accepted: List[Dict[str, Any]],
        generated_ids: List[str],
        failures: List[Dict[str, Any]],
    ) -> None:
        log_path = os.path.join(domain_dir, "agentworkflow_generation_log.jsonl")
        payload = {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "main_app": context.main_app,
            "apps_for_group": context.apps_for_group,
            "launch_paths": context.launch_paths,
            "golden_paths": context.golden_paths,
            "exploration": exploration,
            "accepted_count": len(accepted),
            "generated_ids": generated_ids,
            "failures": failures,
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
