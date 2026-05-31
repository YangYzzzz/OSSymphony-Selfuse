from __future__ import annotations

import ast
import copy
import json
import logging
import os
import re
import shlex
import time
import uuid
from dataclasses import dataclass, field
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
DANGEROUS_IMPORTS = {"subprocess", "socket", "requests", "urllib", "httpx", "shutil", "pathlib"}
DANGEROUS_CALLS = {"system", "popen", "remove", "unlink", "rmdir", "removedirs", "rename", "write", "writelines"}
PROMPT_DIR = os.path.dirname(__file__)
_PROMPT_CACHE: Dict[str, str] = {}


def load_prompt(filename: str) -> str:
    if filename not in _PROMPT_CACHE:
        with open(os.path.join(PROMPT_DIR, filename), "r", encoding="utf-8") as f:
            _PROMPT_CACHE[filename] = f.read().strip()
    return _PROMPT_CACHE[filename]


EXPLORATION_TOOL_SCHEMA: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "open",
            "description": "Use a sampled application to open a sampled file, or open an empty app window, through desktop_env.controller.run_bash_script.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app": {"type": "string", "description": "One app from sampled_apps."},
                    "path": {"type": "string", "description": "One path from sampled_files, or empty for app-only exploration."},
                    "purpose": {"type": "string"},
                },
                "required": ["app"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "click",
            "description": "Click a screen coordinate for non-destructive UI inspection.",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}, "purpose": {"type": "string"}},
                "required": ["x", "y"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scroll",
            "description": "Scroll for non-destructive UI inspection.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "integer", "description": "Positive scrolls up, negative scrolls down."},
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "purpose": {"type": "string"},
                },
                "required": ["amount"],
                "additionalProperties": False,
            },
        },
    },
]


@dataclass
class GenerationContext:
    rollout_id: str
    sampled_apps: List[str]
    app_file_support: Dict[str, List[str]]
    sampled_files: List[Dict[str, Any]]
    app_tutorials: Dict[str, str]
    app_memory: Dict[str, Any]
    app_versions: Dict[str, str]
    app_open_commands: Dict[str, List[List[str]]]
    observation: Dict[str, Any]
    setup_image: bytes
    initial_config: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def candidate_file_paths(self) -> List[str]:
        paths: List[str] = []
        for item in self.sampled_files:
            if isinstance(item, dict) and item.get("path"):
                paths.append(str(item["path"]))
        return paths


class WorkflowCostTracker:
    def __init__(self, output_dir: str):
        self.output_path = os.path.join(output_dir, "agentworkflow_cost.jsonl")
        os.makedirs(output_dir, exist_ok=True)
        self.calls: Dict[str, int] = {}

    def record(self, agent_name: str, duration_ms: float, success: bool, usage: Any = None, error: str | None = None) -> None:
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
            default = self._default_memory(app)
            default.update(data)
            return default
        except Exception:
            return self._default_memory(app)

    def load_many_summary(self, apps: List[str]) -> Tuple[Dict[str, Any], Dict[str, Dict[str, Any]]]:
        memories = {app: self.load(app) for app in apps}
        summaries = {app: self.summary(memory) for app, memory in memories.items()}
        return summaries, memories

    def save(self, app: str, memory: Dict[str, Any]) -> None:
        path = self._path(app)
        tmp_path = f"{path}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)

    def summary(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "covered_features": memory.get("covered_features", {}),
            "known_good_verification_channels": memory.get("known_good_verification_channels", []),
            "failure_patterns": memory.get("failure_patterns", [])[-8:],
            "next_generation_bias": memory.get("next_generation_bias", {}),
            "recent_tasks": memory.get("recent_tasks", [])[-8:],
        }

    def record_finalized_many(self, apps: List[str], memories: Dict[str, Dict[str, Any]], task: Dict[str, Any]) -> None:
        related_apps = task.get("related_apps") if isinstance(task.get("related_apps"), list) else apps
        for app in apps:
            memory = memories.setdefault(app, self._default_memory(app))
            if app in related_apps:
                self._record_finalized(app, memory, task)
            else:
                self._record_couse(memory, related_apps)
            self.save(app, memory)

    def record_failure_many(self, apps: List[str], memories: Dict[str, Dict[str, Any]], failure_type: str, lesson: str) -> None:
        for app in apps:
            memory = memories.setdefault(app, self._default_memory(app))
            failures = memory.setdefault("failure_patterns", [])
            failures.append({"type": failure_type, "lesson": lesson})
            memory["failure_patterns"] = failures[-30:]
            memory["version"] = int(memory.get("version", 1)) + 1
            self.save(app, memory)

    def _record_finalized(self, app: str, memory: Dict[str, Any], task: Dict[str, Any]) -> None:
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
        self._record_couse(memory, task.get("related_apps") or [])
        memory["version"] = int(memory.get("version", 1)) + 1
        self._update_bias(memory)

    def _record_couse(self, memory: Dict[str, Any], related_apps: List[str]) -> None:
        counts = memory.setdefault("co_use_counts", {})
        for app in related_apps:
            app = str(app)
            if app and app != memory.get("app"):
                counts[app] = int(counts.get(app, 0)) + 1

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
            "co_use_counts": {},
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
                data = json.loads(self._strip_json_fence(str(response or "")))
                success = True
                return data
            except Exception as e:
                last_error = str(e)
                logger.warning("%s attempt %s/%s failed: %s", self.name, attempt, retries, e)
            finally:
                self.cost_tracker.record(self.name, (time.time() - start) * 1000.0, success, usage, None if success else last_error)
        raise ValueError(f"{self.name} failed to return valid JSON: {last_error}")

    def _strip_json_fence(self, response: str) -> str:
        response = response.strip()
        match = re.search(r"^```(?:json)?\s*\n?(.*?)\n?```$", response, re.DOTALL)
        return match.group(1).strip() if match else response


class SandboxExplorationAgent(WorkflowLLMAgent):
    def __init__(self, name: str, engine_params: Dict[str, Any], cost_tracker: WorkflowCostTracker, platform: str = "linux", max_actions: int = 10):
        super().__init__(name, engine_params, cost_tracker, platform)
        self.max_actions = max_actions

    def explore(self, context: GenerationContext, env: DesktopEnv) -> Dict[str, Any]:
        file_inventory = self._build_file_inventory(context.sampled_files, env)
        planned_actions = self._plan_actions(context, file_inventory)
        tool_results = self._execute_actions(context, env, planned_actions[: self.max_actions])
        summary = self._summarize(context, file_inventory, tool_results)
        return {
            "visible_state": summary.get("visible_state") or "Empty initial desktop state with sampled apps/files available for exploration.",
            "opened_files": summary.get("opened_files") if isinstance(summary.get("opened_files"), list) else [],
            "file_inventory": summary.get("file_inventory") if isinstance(summary.get("file_inventory"), list) else file_inventory,
            "app_affordances_seen": summary.get("app_affordances_seen") if isinstance(summary.get("app_affordances_seen"), list) else [],
            "safe_verification_channels": summary.get("safe_verification_channels") if isinstance(summary.get("safe_verification_channels"), list) else self._infer_channels(context.sampled_files),
            "constraints": summary.get("constraints") if isinstance(summary.get("constraints"), list) else [],
            "tool_schema": EXPLORATION_TOOL_SCHEMA,
            "tool_results": tool_results,
        }

    def _plan_actions(self, context: GenerationContext, file_inventory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        system_prompt = load_prompt("exploration_action_planner.md")
        user_text = json.dumps(
            {
                "max_actions": self.max_actions,
                "tool_schema": EXPLORATION_TOOL_SCHEMA,
                "sampled_apps": context.sampled_apps,
                "app_versions": context.app_versions,
                "app_file_support": context.app_file_support,
                "sampled_files": context.sampled_files,
                "file_inventory": file_inventory,
                "app_memory_summary": context.app_memory,
            },
            ensure_ascii=False,
        )
        try:
            data = self.call_json(system_prompt, user_text, context.setup_image)
        except Exception as e:
            logger.warning("Exploration action planning failed, using deterministic fallback: %s", e)
            return self._fallback_actions(context)
        actions = data.get("actions") if isinstance(data.get("actions"), list) else []
        return [action for action in actions if isinstance(action, dict)] or self._fallback_actions(context)

    def _fallback_actions(self, context: GenerationContext) -> List[Dict[str, Any]]:
        actions: List[Dict[str, Any]] = []
        for file_info in context.sampled_files[: self.max_actions]:
            if isinstance(file_info, dict):
                apps = file_info.get("supported_apps") if isinstance(file_info.get("supported_apps"), list) else context.sampled_apps
                app = apps[0] if apps else (context.sampled_apps[0] if context.sampled_apps else "")
                if app:
                    actions.append({"tool": "open", "arguments": {"app": app, "path": file_info.get("path", "")}, "purpose": "Inspect sampled file."})
        if not actions and context.sampled_apps:
            actions.append({"tool": "open", "arguments": {"app": context.sampled_apps[0]}, "purpose": "Inspect empty app window."})
        return actions

    def _execute_actions(self, context: GenerationContext, env: DesktopEnv, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for action in actions:
            tool = str(action.get("tool") or action.get("name") or "")
            arguments = action.get("arguments") if isinstance(action.get("arguments"), dict) else action
            if tool == "open":
                result = self._execute_open(context, env, arguments)
            elif tool == "click":
                result = self._execute_pyautogui(env, "click", arguments)
            elif tool == "scroll":
                result = self._execute_pyautogui(env, "scroll", arguments)
            else:
                result = {"status": "skipped", "error": f"unknown_tool:{tool}", "output": ""}
            results.append({"tool": tool, "arguments": self._redact_large(arguments), "result": self._redact_large(result)})
        return results

    def _execute_open(self, context: GenerationContext, env: DesktopEnv, arguments: Dict[str, Any]) -> Dict[str, Any]:
        app = str(arguments.get("app") or "")
        path = str(arguments.get("path") or "")
        if app not in context.sampled_apps:
            return {"status": "blocked", "output": "", "error": f"app_not_sampled:{app}", "returncode": -1}
        allowed_paths = set(context.candidate_file_paths)
        if path and path not in allowed_paths:
            return {"status": "blocked", "output": "", "error": f"path_not_sampled:{path}", "returncode": -1}
        command = self._build_open_command(context, app, path)
        if not command:
            return {"status": "error", "output": "", "error": f"no_open_command:{app}", "returncode": -1}
        quoted = " ".join(shlex.quote(part) for part in command)
        script = f"nohup {quoted} > /dev/null 2>&1 &"
        return env.controller.run_bash_script(script=script, timeout=10) or {"status": "error", "output": "", "error": "run_bash_script returned None", "returncode": -1}

    def _build_open_command(self, context: GenerationContext, app: str, path: str) -> List[str]:
        variants = context.app_open_commands.get(app) or []
        for variant in variants:
            if not isinstance(variant, list) or not variant:
                continue
            command = [str(part).replace("PATH", path) for part in variant]
            command = [part for part in command if part != ""]
            has_placeholder = any("PATH" in str(part) for part in variant)
            if path and has_placeholder:
                return command
            if not path and not has_placeholder:
                return command
        if path:
            return ["xdg-open", path]
        version = context.app_versions.get(app, app)
        return [version]

    def _execute_pyautogui(self, env: DesktopEnv, tool: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool == "click":
            x = int(arguments.get("x", 0))
            y = int(arguments.get("y", 0))
            script = f"python - <<'PY'\nimport pyautogui, time\npyautogui.click({x}, {y})\ntime.sleep(0.5)\nPY"
        else:
            amount = int(arguments.get("amount", 0))
            x = arguments.get("x")
            y = arguments.get("y")
            move = f"pyautogui.moveTo({int(x)}, {int(y)})\n" if x is not None and y is not None else ""
            script = f"python - <<'PY'\nimport pyautogui, time\n{move}pyautogui.scroll({amount})\ntime.sleep(0.5)\nPY"
        return env.controller.run_bash_script(script=script, timeout=5) or {"status": "error", "output": "", "error": "run_bash_script returned None", "returncode": -1}

    def _summarize(self, context: GenerationContext, file_inventory: List[Dict[str, Any]], tool_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        system_prompt = load_prompt("exploration_summarizer.md")
        user_text = json.dumps(
            {
                "sampled_apps": context.sampled_apps,
                "app_file_support": context.app_file_support,
                "sampled_files": context.sampled_files,
                "initial_file_inventory": file_inventory,
                "tool_results": tool_results,
                "app_memory_summary": context.app_memory,
            },
            ensure_ascii=False,
        )
        try:
            return self.call_json(system_prompt, user_text, context.setup_image)
        except Exception as e:
            logger.warning("Exploration summary failed, using deterministic fallback: %s", e)
            return {}

    def _build_file_inventory(self, sampled_files: List[Dict[str, Any]], env: DesktopEnv) -> List[Dict[str, Any]]:
        inventory = []
        for file_info in sampled_files[:20]:
            if not isinstance(file_info, dict):
                continue
            path = str(file_info.get("path") or "")
            if not path:
                continue
            entry = dict(file_info)
            script = "python - <<'PY'\nimport os, json\np = " + repr(path) + "\nprint(json.dumps({'exists': os.path.exists(p), 'is_dir': os.path.isdir(p), 'size': os.path.getsize(p) if os.path.exists(p) and not os.path.isdir(p) else None}))\nPY"
            try:
                result = env.controller.run_bash_script(script=script, timeout=10)
                output = (result or {}).get("output", "").strip()
                if output:
                    entry.update(json.loads(output.splitlines()[-1]))
            except Exception:
                entry["exists"] = None
            inventory.append(entry)
        return inventory

    def _infer_channels(self, sampled_files: List[Dict[str, Any]]) -> List[str]:
        channels = ["vm_command_line"]
        for file_info in sampled_files:
            if isinstance(file_info, dict) and file_info.get("type"):
                channels.append(f"vm_file:{file_info['type']}")
        return sorted(set(channels))

    def _redact_large(self, obj: Any) -> Any:
        if isinstance(obj, str):
            return obj[:2000] + "[truncated]" if len(obj) > 2000 else obj
        if isinstance(obj, dict):
            return {k: self._redact_large(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._redact_large(v) for v in obj[:20]]
        return obj


class ProposalGenerationAgent(WorkflowLLMAgent):
    def generate_proposals(self, context: GenerationContext, exploration: Dict[str, Any], target_count: int, feedback: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
        system_prompt = load_prompt("proposal_generator.md")
        user_text = json.dumps(
            {
                "requested_proposal_count": target_count,
                "sampled_apps": context.sampled_apps,
                "app_versions": context.app_versions,
                "app_file_support": context.app_file_support,
                "sampled_files": context.sampled_files,
                "app_tutorials": context.app_tutorials,
                "app_memory_summary": context.app_memory,
                "exploration_summary": exploration,
                "previous_rejection_feedback": feedback or [],
            },
            ensure_ascii=False,
        )
        data = self.call_json(system_prompt, user_text, context.setup_image)
        proposals = data.get("proposals", [])
        proposals = [p for p in proposals if isinstance(p, dict)] if isinstance(proposals, list) else []
        return proposals[:target_count]


class ProposalCritiqueAgent(WorkflowLLMAgent):
    def select(self, context: GenerationContext, proposals: List[Dict[str, Any]], target_count: int) -> Dict[str, Any]:
        system_prompt = load_prompt("proposal_critic.md")
        user_text = json.dumps(
            {
                "target_count": target_count,
                "sampled_apps": context.sampled_apps,
                "app_file_support": context.app_file_support,
                "sampled_files": context.sampled_files,
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
        system_prompt = load_prompt("evaluator_synthesizer.md")
        user_text = json.dumps(
            {
                "proposal": proposal,
                "sampled_apps": context.sampled_apps,
                "app_versions": context.app_versions,
                "app_file_support": context.app_file_support,
                "sampled_files": context.sampled_files,
                "exploration_summary": exploration,
                "app_tutorials": context.app_tutorials,
            },
            ensure_ascii=False,
        )
        data = self.call_json(system_prompt, user_text, context.setup_image)
        candidate = data.get("task_candidate")
        return candidate if isinstance(candidate, dict) else {}


class CandidateRepairAgent(WorkflowLLMAgent):
    def repair(self, context: GenerationContext, candidate: Dict[str, Any], failure: Dict[str, Any], exploration: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = load_prompt("candidate_repairer.md")
        user_text = json.dumps(
            {
                "candidate": candidate,
                "failure": failure,
                "sampled_apps": context.sampled_apps,
                "app_file_support": context.app_file_support,
                "sampled_files": context.sampled_files,
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
        if not need_rule:
            errors.append("missing_required_rule_judge")
        if need_rule and not rule_items:
            errors.append("missing_rule_items")
        if need_vlm and not str(verification.get("vlm_desc", "")).strip():
            warnings.append("missing_vlm_desc")
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
        if getter_type == "vm_file" and not str(getter.get("path", "")).startswith("/"):
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
            return {"passed": False, "init_rule_reward": None, "details": [str(e)], "failure_type": "getter_failed"}


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
    ):
        self.rollout_task_dir = rollout_task_dir
        self.env = env
        self.build_evaluator_fn = build_evaluator_fn
        self.app_version_lookup = app_version_lookup
        self.max_repair_rounds = max_repair_rounds
        self.cost_tracker = WorkflowCostTracker(rollout_task_dir)
        self.memory_store = AppMemoryStore()
        self.explorer = SandboxExplorationAgent("workflow_sandbox_explorer", engine_params, self.cost_tracker, platform, max_actions=exploration_max_actions)
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
        context.app_memory, raw_memories = self.memory_store.load_many_summary(context.sampled_apps)
        exploration = self.explorer.explore(context, self.env)
        self.env.reset(task_config={"config": context.initial_config, "id": "init_id", "instruction": "init_instruction"})
        accepted = self._generate_and_select(context, exploration, task_nums)
        generated_ids: List[str] = []
        failures: List[Dict[str, Any]] = []
        for proposal in accepted:
            if len(generated_ids) >= task_nums:
                break
            candidate = self.evaluator.synthesize(context, proposal, exploration)
            task_config, failure, finalized_candidate = self._validate_repair_and_finalize_candidate(context, candidate, proposal, exploration)
            self.env.reset(task_config={"config": context.initial_config, "id": "init_id", "instruction": "init_instruction"})
            if task_config:
                task_id = task_config["id"]
                json_path = os.path.join(domain_dir, f"{task_id}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(task_config, f, indent=4, ensure_ascii=False)
                with open(os.path.join(image_base_dir, f"{task_id}.png"), "wb") as f:
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
        self._write_sidecar_log(domain_dir, context, exploration, accepted, generated_ids, failures)
        return {self._domain_key(context): generated_ids}

    def _generate_and_select(self, context: GenerationContext, exploration: Dict[str, Any], task_nums: int) -> List[Dict[str, Any]]:
        feedback: List[Dict[str, Any]] = []
        accepted: List[Dict[str, Any]] = []
        for _ in range(3):
            proposals = self.proposer.generate_proposals(context, exploration, task_nums - len(accepted), feedback)
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
            current = self._normalize_candidate(self.repairer.repair(context, current, last_failure, exploration), proposal)
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
            "setup_image": f"image/{task_id}.png",
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
            "rollout_id": context.rollout_id,
            "sampled_apps": context.sampled_apps,
            "app_file_support": context.app_file_support,
            "sampled_files": context.sampled_files,
            "initial_config": context.initial_config,
            "exploration": exploration,
            "accepted_count": len(accepted),
            "generated_ids": generated_ids,
            "failures": failures,
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
