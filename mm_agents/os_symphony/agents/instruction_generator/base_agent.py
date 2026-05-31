from __future__ import annotations

import copy
import json
import logging
import os
import re
import time
from typing import Any, Dict

from mm_agents.os_symphony.core.mllm import LMMAgent

logger = logging.getLogger("desktopenv.instruction_generation_workflow")


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
