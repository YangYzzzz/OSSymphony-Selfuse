from __future__ import annotations

import json
import logging
import os
import shlex
import time
from typing import Any, Dict, List, Tuple

from desktop_env.osworld.desktop_env import DesktopEnv

from mm_agents.os_symphony.agents.instruction_generator.base_agent import WorkflowCostTracker, WorkflowLLMAgent
from mm_agents.os_symphony.agents.instruction_generator.constants import EXPLORATION_PROPOSAL_TOOL_SCHEMA
from mm_agents.os_symphony.agents.instruction_generator.models import GenerationContext
from mm_agents.os_symphony.agents.instruction_generator.prompts import load_prompt

logger = logging.getLogger("desktopenv.instruction_generation_workflow")


class ExplorationProposalAgent(WorkflowLLMAgent):
    def __init__(self, name: str, engine_params: Dict[str, Any], cost_tracker: WorkflowCostTracker, platform: str = "linux", max_actions: int = 10):
        super().__init__(name, engine_params, cost_tracker, platform)
        self.max_actions = max_actions

    def generate(
        self,
        context: GenerationContext,
        env: DesktopEnv,
        target_count: int,
        feedback: List[Dict[str, Any]] | None = None,
        screenshot_dir: str | None = None,
    ) -> Dict[str, Any]:
        fallback_actions = self._fallback_actions(context)
        obs = env._get_obs()
        self._start_generation_conversation(context, obs, target_count, feedback)
        step_idx = 0
        while step_idx < self.max_actions:
            step_idx += 1
            response, action = self._next_action()
            if not action and fallback_actions:
                action = fallback_actions.pop(0)
                response = {"source": "fallback", "actions": [action]}
                if self.agent.messages[-1]["role"] != "assistant":
                    self._append_assistant_message(json.dumps(response, ensure_ascii=False))
            if not action:
                break
            tool = self._action_tool(action)
            if tool == "done":
                record = self._build_step_record(step_idx, action, response, True)
                self._write_step_trajectory(context, screenshot_dir, record, action)
                return self._build_generation_result(context, action, target_count)

            screenshot_path = self._save_obs_screenshot(obs, screenshot_dir, step_idx)
            obs, reward, env_done, info = self._step_action(context, env, action)
            record = self._build_step_record(step_idx, action, response, env_done, reward, info, screenshot_path)
            self._write_step_trajectory(context, screenshot_dir, record, action)
            self._append_tool_response_message(record, obs, step_idx, target_count)
            if env_done:
                break
        return self._force_done_generation(context, screenshot_dir, obs, step_idx, target_count)

    def _start_generation_conversation(
        self,
        context: GenerationContext,
        obs: Dict[str, Any],
        target_count: int,
        feedback: List[Dict[str, Any]] | None,
    ) -> None:
        self.agent.reset()
        self.agent.add_system_prompt(load_prompt("exploration_proposal_generator.md"))
        user_text = json.dumps(
            {
                "turn_type": "initial_observation",
                "requested_proposal_count": target_count,
                "max_actions": self.max_actions,
                "step_num": 1,
                "remaining_actions": self.max_actions,
                "tool_schema": EXPLORATION_PROPOSAL_TOOL_SCHEMA,
                "sampled_apps": context.sampled_apps,
                "app_versions": context.app_versions,
                "app_file_support": context.app_file_support,
                "sampled_files": context.sampled_files,
                "app_tutorials": context.app_tutorials,
                "app_memory_summary": context.app_memory,
                "previous_rejection_feedback": feedback or [],
            },
            ensure_ascii=False,
        )
        image_content = obs.get("screenshot") if isinstance(obs, dict) else None
        self.agent.add_message(text_content=user_text, image_content=image_content, role="user")

    def _next_action(self, retries: int = 2) -> Tuple[Dict[str, Any], Dict[str, Any] | None]:
        last_error = ""
        for attempt in range(1, retries + 1):
            start = time.time()
            usage = None
            success = False
            raw_response = ""
            try:
                response = self.agent.get_response(temperature=self.temperature)
                if isinstance(response, tuple):
                    response, usage = response
                raw_response = str(response or "")
                data = json.loads(self._strip_json_fence(raw_response))
                action = self._extract_action(data)
                success = action is not None
                self._append_assistant_message(raw_response)
                return data, action
            except Exception as e:
                last_error = str(e)
                logger.warning("Exploration-proposal step failed attempt %s/%s: %s", attempt, retries, e)
                if raw_response:
                    self._append_assistant_message(raw_response)
                    self.agent.add_message(
                        text_content="Return valid JSON only. Use exactly one action in the actions list. Use done with proposals if exploration should finish.",
                        role="user",
                    )
            finally:
                self.cost_tracker.record(self.name, (time.time() - start) * 1000.0, success, usage, None if success else last_error)
        return {"error": last_error, "actions": []}, None

    def _append_assistant_message(self, text: str) -> None:
        self.agent.messages.append({"role": "assistant", "content": [{"type": "text", "text": text}]})

    def _append_tool_response_message(self, record: Dict[str, Any], obs: Dict[str, Any], step_idx: int, target_count: int) -> None:
        user_text = json.dumps(
            {
                "turn_type": "tool_response",
                "requested_proposal_count": target_count,
                "step_num": step_idx + 1,
                "remaining_actions": max(self.max_actions - step_idx, 0),
                "tool_result": record.get("info"),
                "instruction": "Return exactly one next safe action, or return done with exactly requested_proposal_count grounded proposals if enough has been observed.",
            },
            ensure_ascii=False,
        )
        image_content = obs.get("screenshot") if isinstance(obs, dict) else None
        self.agent.add_message(text_content=user_text, image_content=image_content, role="user")

    def _append_force_done_message(self, obs: Dict[str, Any], target_count: int) -> None:
        user_text = json.dumps(
            {
                "turn_type": "force_done",
                "requested_proposal_count": target_count,
                "remaining_actions": 0,
                "instruction": "Exploration budget is exhausted or no safe action remains. Return exactly one done action whose arguments contain proposals generated from the visual trajectory.",
            },
            ensure_ascii=False,
        )
        image_content = obs.get("screenshot") if isinstance(obs, dict) else None
        self.agent.add_message(text_content=user_text, image_content=image_content, role="user")

    def _extract_action(self, data: Dict[str, Any]) -> Dict[str, Any] | None:
        if not isinstance(data, dict):
            return None
        if self._action_tool(data):
            return data
        actions = data.get("actions") if isinstance(data.get("actions"), list) else []
        for action in actions[:1]:
            if isinstance(action, dict) and self._action_tool(action):
                return action
        return None

    def _action_tool(self, action: Dict[str, Any]) -> str:
        return str(action.get("tool") or action.get("name") or "") if isinstance(action, dict) else ""

    def _action_arguments(self, action: Dict[str, Any]) -> Dict[str, Any]:
        arguments = action.get("arguments") if isinstance(action.get("arguments"), dict) else action
        return arguments if isinstance(arguments, dict) else {}

    def _build_step_record(
        self,
        step_idx: int,
        action: Dict[str, Any],
        response: Dict[str, Any],
        done: bool,
        reward: float | None = None,
        info: Dict[str, Any] | None = None,
        screenshot_path: str | None = None,
    ) -> Dict[str, Any]:
        record = {
            "step_num": step_idx,
            "tool": self._action_tool(action),
            "arguments": self._redact_large(self._action_arguments(action)),
            "response": self._redact_large(response),
            "done": done,
        }
        if reward is not None:
            record["reward"] = reward
        if info is not None:
            record["info"] = self._redact_large(info)
        if screenshot_path:
            record["screenshot"] = os.path.basename(screenshot_path)
        return record

    def _build_generation_result(self, context: GenerationContext, action: Dict[str, Any], target_count: int) -> Dict[str, Any]:
        arguments = self._action_arguments(action)
        proposals = arguments.get("proposals") if isinstance(arguments.get("proposals"), list) else []
        generation_notes = arguments.get("generation_notes") if isinstance(arguments.get("generation_notes"), list) else []
        return {
            "proposals": [p for p in proposals if isinstance(p, dict)][:target_count],
            "generation_notes": generation_notes,
            "trajectory": {"rollout_id": context.rollout_id, "log": "traj.jsonl"},
        }

    def _force_done_generation(
        self,
        context: GenerationContext,
        screenshot_dir: str | None,
        obs: Dict[str, Any],
        step_idx: int,
        target_count: int,
    ) -> Dict[str, Any]:
        self._append_force_done_message(obs, target_count)
        response, action = self._next_action(retries=2)
        if action and self._action_tool(action) == "done":
            record = self._build_step_record(step_idx + 1, action, response, True)
            self._write_step_trajectory(context, screenshot_dir, record, action)
            return self._build_generation_result(context, action, target_count)
        logger.warning("Exploration-proposal forced done failed, returning empty proposal set.")
        return {"proposals": [], "generation_notes": ["forced_done_failed"], "trajectory": {"rollout_id": context.rollout_id, "log": "traj.jsonl"}}

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

    def _step_action(self, context: GenerationContext, env: DesktopEnv, action: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        tool = self._action_tool(action)
        arguments = self._action_arguments(action)
        try:
            if tool == "open":
                result = self._execute_open(context, env, arguments)
                time.sleep(5)
                return env._get_obs(), 0.0, False, {"tool_result": result}
            if tool in {"click", "scroll"}:
                step_action = self._to_pyautogui_action(tool, arguments)
                obs, reward, done, info = env.step(step_action, 2)
                return obs, float(reward or 0.0), bool(done), info
            return env._get_obs(), 0.0, False, {"tool_result": {"status": "skipped", "error": f"unknown_tool:{tool}", "output": ""}}
        except Exception as e:
            logger.warning("Exploration action execution failed: %s", e)
            return env._get_obs(), 0.0, False, {"tool_result": {"status": "error", "error": str(e), "output": ""}}

    def _to_pyautogui_action(self, tool: str, arguments: Dict[str, Any]) -> str:
        if tool == "click":
            x = int(arguments.get("x", 0))
            y = int(arguments.get("y", 0))
            return f"pyautogui.click({x}, {y})"
        amount = int(arguments.get("amount", 0))
        x = arguments.get("x")
        y = arguments.get("y")
        if x is not None and y is not None:
            return f"pyautogui.moveTo({int(x)}, {int(y)})\npyautogui.scroll({amount})"
        return f"pyautogui.scroll({amount})"

    def _save_obs_screenshot(self, obs: Dict[str, Any], screenshot_dir: str | None, step_idx: int) -> str | None:
        if not screenshot_dir or not isinstance(obs, dict):
            return None
        screenshot = obs.get("screenshot")
        if not screenshot:
            return None
        try:
            os.makedirs(screenshot_dir, exist_ok=True)
            path = os.path.join(screenshot_dir, f"explore_step_{step_idx}.png")
            with open(path, "wb") as f:
                f.write(screenshot)
            return path
        except Exception as e:
            logger.warning("Failed to save exploration screenshot explore_step_%s: %s", step_idx, e)
            return None

    def _write_step_trajectory(self, context: GenerationContext, screenshot_dir: str | None, record: Dict[str, Any], action: Dict[str, Any]) -> None:
        if not screenshot_dir:
            return
        try:
            payload = {
                "rollout_id": context.rollout_id,
                "step_num": record.get("step_num"),
                "action": action,
                "tool": record.get("tool"),
                "arguments": record.get("arguments"),
                "response": record.get("response"),
                "reward": record.get("reward"),
                "done": record.get("done", False),
                "info": record.get("info"),
                "screenshot_file": record.get("screenshot"),
            }
            with open(os.path.join(screenshot_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            with open(os.path.join(screenshot_dir, f"traj_{record.get('step_num')}.json"), "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.warning("Failed to write exploration trajectory step_%s: %s", record.get("step_num"), e)

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
        return []

    def _redact_large(self, obj: Any) -> Any:
        if isinstance(obj, str):
            return obj[:2000] + "[truncated]" if len(obj) > 2000 else obj
        if isinstance(obj, dict):
            return {k: self._redact_large(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._redact_large(v) for v in obj[:20]]
        return obj
