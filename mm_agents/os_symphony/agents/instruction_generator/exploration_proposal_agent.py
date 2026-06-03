from __future__ import annotations

import io
import json
import logging
import os
import shlex
import time
from typing import Any, Dict, List, Tuple

from PIL import Image, ImageDraw

from desktop_env.osworld.desktop_env import DesktopEnv

from mm_agents.os_symphony.agents.instruction_generator.base_agent import WorkflowCostTracker, WorkflowLLMAgent
from mm_agents.os_symphony.agents.instruction_generator.constants import EXPLORATION_PROPOSAL_TOOL_SCHEMA
from mm_agents.os_symphony.agents.instruction_generator.models import WorkflowSharedState
from mm_agents.os_symphony.agents.instruction_generator.prompts import load_prompt

logger = logging.getLogger("desktopenv.instruction_generation_workflow")


class ExplorationProposalAgent(WorkflowLLMAgent):
    def __init__(
        self,
        name: str,
        engine_params: Dict[str, Any],
        cost_tracker: WorkflowCostTracker,
        platform: str = "linux",
        max_actions: int = 10,
        input_screen_size: Tuple[int, int] | None = None,
    ):
        super().__init__(name, engine_params, cost_tracker, platform)
        self.max_actions = max_actions
        self.input_screen_size = input_screen_size

    def generate(
        self,
        shared_state: WorkflowSharedState,
        env: DesktopEnv,
        target_count: int,
        feedback: List[Dict[str, Any]] | None = None,
        screenshot_dir: str | None = None,
    ) -> Dict[str, Any]:
        obs = env._get_obs()
        model_obs = self._model_obs(obs)
        self._start_generation_conversation(shared_state, model_obs, target_count, feedback)
        step_idx = 0
        while step_idx < self.max_actions:
            step_idx += 1
            response, action = self._next_action()
            if not action:
                break
            tool = self._action_tool(action)
            if tool == "done":
                record = self._build_step_record(step_idx, action, response, True)
                self._write_step_trajectory(shared_state, screenshot_dir, record)
                return self._build_generation_result(shared_state, action, target_count)

            screenshot_path = self._save_obs_screenshot(model_obs, screenshot_dir, step_idx)
            draw_path = self._save_action_draw_screenshot(model_obs, screenshot_dir, step_idx, action)
            obs, _, env_done, info = self._step_action(shared_state, env, action, obs)
            model_obs = self._model_obs(obs)
            record = self._build_step_record(step_idx, action, response, env_done, info, screenshot_path, draw_path)
            self._write_step_trajectory(shared_state, screenshot_dir, record)
            self._append_tool_response_message(record, model_obs, step_idx, target_count)
            if env_done:
                break
        return self._force_done_generation(shared_state, screenshot_dir, model_obs, step_idx, target_count)

    def _start_generation_conversation(
        self,
        shared_state: WorkflowSharedState,
        obs: Dict[str, Any],
        target_count: int,
        feedback: List[Dict[str, Any]] | None,
    ) -> None:
        self.agent.reset()
        self.agent.add_system_prompt(load_prompt("exploration_proposal_generator.md"))
        screen_size = self._obs_screen_size(obs)
        user_text = json.dumps(
            {
                "turn_type": "initial_observation",
                "requested_proposal_count": target_count,
                "max_actions": self.max_actions,
                "step_num": 1,
                "remaining_actions": self.max_actions,
                "input_screen_size": list(screen_size) if screen_size else None,
                "screen_resolution_instruction": f"Screenshots are shown at input_screen_size ({screen_size[0]} x {screen_size[1]}). Use this resolution for every click/scroll x,y coordinate." if screen_size else "Use the screenshot resolution for every click/scroll x,y coordinate.",
                "tool_schema": EXPLORATION_PROPOSAL_TOOL_SCHEMA,
                "sampled_apps": shared_state.sampled_apps,
                "app_versions": shared_state.app_versions,
                "app_open_commands": shared_state.app_open_commands,
                "app_file_support": shared_state.app_file_support,
                "sampled_files": shared_state.sampled_files,
                "app_tutorials": shared_state.app_tutorials,
                "app_memory_summary": shared_state.app_memory,
                "previous_rejection_feedback": feedback or [],
            },
            ensure_ascii=False,
        )
        image_content = obs.get("screenshot") if isinstance(obs, dict) else None
        self.agent.add_message(text_content=user_text, image_content=image_content, role="user")

    def _next_action(self, retries: int = 2) -> Tuple[str, Dict[str, Any] | None]:
        last_error = ""
        for attempt in range(1, retries + 1):
            start = time.time()
            usage = None
            success = False
            raw_response = ""
            try:
                raw_response, data = self.agent.get_json_response(temperature=self.temperature)
                logger.info(f"Raw Response: {raw_response}, data: {data}")
                usage = self.agent.last_usage
                action = self._extract_action(data)
                success = action is not None
                self._append_assistant_message(raw_response)
                return raw_response, action
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
        return last_error, None

    def _append_assistant_message(self, text: str) -> None:
        self.agent.messages.append({"role": "assistant", "content": [{"type": "text", "text": text}]})

    def _append_tool_response_message(self, record: Dict[str, Any], obs: Dict[str, Any], step_idx: int, target_count: int) -> None:
        screen_size = self._obs_screen_size(obs)
        user_text = json.dumps(
            {
                "turn_type": "tool_response",
                "requested_proposal_count": target_count,
                "step_num": step_idx + 1,
                "remaining_actions": max(self.max_actions - step_idx, 0),
                "input_screen_size": list(screen_size) if screen_size else None,
                "tool_result": record.get("info", "Success"),
                "instruction": f"Return exactly one next safe action using input_screen_size ({screen_size[0]} x {screen_size[1]}) coordinates, or return done with exactly requested_proposal_count grounded proposals if enough has been observed." if screen_size else "Return exactly one next safe action, or return done with exactly requested_proposal_count grounded proposals if enough has been observed.",
            },
            ensure_ascii=False,
        )
        image_content = obs.get("screenshot") if isinstance(obs, dict) else None
        self.agent.add_message(text_content=user_text, image_content=image_content, role="user")

    def _append_force_done_message(self, obs: Dict[str, Any], target_count: int) -> None:
        screen_size = self._obs_screen_size(obs)
        user_text = json.dumps(
            {
                "turn_type": "force_done",
                "requested_proposal_count": target_count,
                "remaining_actions": 0,
                "input_screen_size": list(screen_size) if screen_size else None,
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
        response: str,
        done: bool,
        info: Dict[str, Any] | None = None,
        screenshot_path: str | None = None,
        draw_path: str | None = None,
    ) -> Dict[str, Any]:
        record = {
            "step_num": step_idx,
            "tool": self._action_tool(action),
            "arguments": self._redact_large(self._action_arguments(action)),
            "response": self._redact_large(response),
            "done": done,
        }
        if info is not None:
            record["info"] = self._redact_large(info)
        if screenshot_path:
            record["screenshot"] = os.path.basename(screenshot_path)
        if draw_path:
            record["draw_screenshot"] = os.path.basename(draw_path)
        return record

    def _build_generation_result(self, shared_state: WorkflowSharedState, action: Dict[str, Any], target_count: int) -> Dict[str, Any]:
        arguments = self._action_arguments(action)
        proposals = arguments.get("proposals") if isinstance(arguments.get("proposals"), list) else []
        generation_notes = arguments.get("generation_notes") if isinstance(arguments.get("generation_notes"), list) else []
        normalized_proposals = [self._normalize_proposal_setup_config(shared_state, proposal) for proposal in proposals if isinstance(proposal, dict)]
        return {
            "proposals": normalized_proposals[:target_count],
            "generation_notes": generation_notes,
        }

    def _normalize_proposal_setup_config(self, shared_state: WorkflowSharedState, proposal: Dict[str, Any]) -> Dict[str, Any]:
        normalized = dict(proposal)
        raw_config = normalized.get("config") if isinstance(normalized.get("config"), list) else []
        normalized["config"] = [
            setup_config
            for cfg in raw_config
            if isinstance(cfg, dict)
            for setup_config in self._normalize_setup_config_item(shared_state, cfg)
        ]
        return normalized

    def _normalize_setup_config_item(self, shared_state: WorkflowSharedState, cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
        if cfg.get("type") == "launch" and isinstance(cfg.get("parameters"), dict):
            return [cfg]
        app = str(cfg.get("app") or "")
        path = self._normalize_config_path(str(cfg.get("path") or ""))
        if cfg.get("type") == "launch" or app:
            if not app:
                return []
            command = self._build_open_command_for_config(shared_state, app, path)
            return [{"type": "launch", "parameters": {"command": command}}] if command else []
        return [cfg]

    def _normalize_config_path(self, path: str) -> str:
        return path.replace("~/", "/home/user/", 1) if path.startswith("~/") else path

    def _build_open_command_for_config(self, shared_state: WorkflowSharedState, app: str, path: str) -> List[str]:
        if app not in shared_state.sampled_apps:
            return []
        if path and path not in set(shared_state.candidate_file_paths):
            return []
        return self._build_open_command(shared_state, app, path)

    def _force_done_generation(
        self,
        shared_state: WorkflowSharedState,
        screenshot_dir: str | None,
        obs: Dict[str, Any],
        step_idx: int,
        target_count: int,
    ) -> Dict[str, Any]:
        self._append_force_done_message(obs, target_count)
        response, action = self._next_action(retries=2)
        if action and self._action_tool(action) == "done":
            record = self._build_step_record(step_idx + 1, action, response, True)
            self._write_step_trajectory(shared_state, screenshot_dir, record)
            return self._build_generation_result(shared_state, action, target_count)
        logger.warning("Exploration-proposal forced done failed, returning empty proposal set.")
        return {"proposals": [], "generation_notes": ["forced_done_failed"]}

    def _step_action(self, shared_state: WorkflowSharedState, env: DesktopEnv, action: Dict[str, Any], obs: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        tool = self._action_tool(action)
        arguments = self._rescale_action_arguments(tool, self._action_arguments(action), obs)
        try:
            if tool == "open":
                result = self._execute_open(shared_state, env, arguments)
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

    def _save_action_draw_screenshot(self, obs: Dict[str, Any], screenshot_dir: str | None, step_idx: int, action: Dict[str, Any]) -> str | None:
        if not screenshot_dir or self._action_tool(action) not in {"click", "scroll"}:
            return None
        arguments = self._action_arguments(action)
        if arguments.get("x") is None or arguments.get("y") is None:
            return None
        screenshot = obs.get("screenshot") if isinstance(obs, dict) else None
        if not screenshot:
            return None
        try:
            image = Image.open(io.BytesIO(screenshot)).convert("RGB")
            x = int(float(arguments.get("x", 0)))
            y = int(float(arguments.get("y", 0)))
            draw = ImageDraw.Draw(image)
            radius = 14
            draw.line((x - radius, y - radius, x + radius, y + radius), fill="red", width=4)
            draw.line((x - radius, y + radius, x + radius, y - radius), fill="red", width=4)
            path = os.path.join(screenshot_dir, f"explore_step_{step_idx}_draw.png")
            image.save(path)
            return path
        except Exception as e:
            logger.warning("Failed to save exploration draw screenshot explore_step_%s: %s", step_idx, e)
            return None

    def _model_obs(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        if not self.input_screen_size or not isinstance(obs, dict) or not obs.get("screenshot"):
            return obs
        try:
            image = Image.open(io.BytesIO(obs["screenshot"]))
            if image.size == self.input_screen_size:
                return obs
            output = io.BytesIO()
            image.resize(self.input_screen_size, Image.LANCZOS).save(output, format="PNG")
            model_obs = dict(obs)
            model_obs["screenshot"] = output.getvalue()
            return model_obs
        except Exception as e:
            logger.warning("Failed to resize exploration observation: %s", e)
            return obs

    def _obs_screen_size(self, obs: Dict[str, Any]) -> Tuple[int, int] | None:
        screenshot = obs.get("screenshot") if isinstance(obs, dict) else None
        if not screenshot:
            return None
        try:
            return Image.open(io.BytesIO(screenshot)).size
        except Exception:
            return None

    def _rescale_action_arguments(self, tool: str, arguments: Dict[str, Any], obs: Dict[str, Any]) -> Dict[str, Any]:
        if tool not in {"click", "scroll"} or not self.input_screen_size:
            return arguments
        if arguments.get("x") is None or arguments.get("y") is None:
            return arguments
        screen_size = self._obs_screen_size(obs)
        if not screen_size or screen_size == self.input_screen_size:
            return arguments
        scaled = dict(arguments)
        scaled["x"] = round(float(arguments["x"]) * screen_size[0] / self.input_screen_size[0])
        scaled["y"] = round(float(arguments["y"]) * screen_size[1] / self.input_screen_size[1])
        return scaled

    def _write_step_trajectory(self, shared_state: WorkflowSharedState, screenshot_dir: str | None, record: Dict[str, Any]) -> None:
        if not screenshot_dir:
            return
        try:
            payload = {
                "rollout_id": shared_state.rollout_id,
                "step_num": record.get("step_num"),
                "action": record.get("action"),
                "tool": record.get("tool"),
                "arguments": record.get("arguments"),
                "response": record.get("response"),
                "done": record.get("done", False),
                "info": record.get("info"),
                "screenshot_file": record.get("screenshot"),
                "draw_screenshot_file": record.get("draw_screenshot"),
            }
            with open(os.path.join(screenshot_dir, "traj.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            with open(os.path.join(screenshot_dir, f"traj_{record.get('step_num')}.json"), "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.warning("Failed to write exploration trajectory step_%s: %s", record.get("step_num"), e)

    def _execute_open(self, shared_state: WorkflowSharedState, env: DesktopEnv, arguments: Dict[str, Any]) -> Dict[str, Any]:
        app = str(arguments.get("app") or "")
        path = str(arguments.get("path") or "")
        if app not in shared_state.sampled_apps:
            return {"status": "blocked", "output": "", "error": f"app_not_sampled:{app}", "returncode": -1}
        allowed_paths = set(shared_state.candidate_file_paths)
        if path and path not in allowed_paths:
            return {"status": "blocked", "output": "", "error": f"path_not_sampled:{path}", "returncode": -1}
        command = self._build_open_command(shared_state, app, path)
        if not command:
            return {"status": "error", "output": "", "error": f"no_open_command:{app}", "returncode": -1}
        quoted = " ".join(shlex.quote(part) for part in command)
        script = f"nohup {quoted} > /dev/null 2>&1 &"
        return env.controller.run_bash_script(script=script, timeout=10) or {"status": "error", "output": "", "error": "run_bash_script returned None", "returncode": -1}

    def _build_open_command(self, shared_state: WorkflowSharedState, app: str, path: str) -> List[str]:
        variants = shared_state.app_open_commands.get(app) or []
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
