from __future__ import annotations

import json
from typing import Any, Dict

from .base_agent import WorkflowCostTracker, WorkflowLLMAgent
from .models import GenerationContext
from .prompts import load_prompt


class EvaluatorSynthesisAgent(WorkflowLLMAgent):
    def __init__(self, name: str, engine_params: Dict[str, Any], cost_tracker: WorkflowCostTracker, platform: str = "linux"):
        super().__init__(name, engine_params, cost_tracker, platform)

    def synthesize(self, context: GenerationContext, proposal: Dict[str, Any], generation_context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = load_prompt("evaluator_synthesizer.md")
        user_text = json.dumps(
            {
                "proposal": proposal,
                "sampled_apps": context.sampled_apps,
                "app_versions": context.app_versions,
                "app_file_support": context.app_file_support,
                "sampled_files": context.sampled_files,
                "generation_context": generation_context,
                "app_tutorials": context.app_tutorials,
            },
            ensure_ascii=False,
        )
        data = self.call_json(system_prompt, user_text, context.setup_image)
        candidate = data.get("task_candidate")
        return candidate if isinstance(candidate, dict) else {}


class EvaluatorCritiqueAgent(WorkflowLLMAgent):
    def __init__(self, name: str, engine_params: Dict[str, Any], cost_tracker: WorkflowCostTracker, platform: str = "linux"):
        super().__init__(name, engine_params, cost_tracker, platform)

    def critique_and_repair(self, context: GenerationContext, candidate: Dict[str, Any], failure: Dict[str, Any], generation_context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = load_prompt("evaluator_critic.md")
        user_text = json.dumps(
            {
                "candidate": candidate,
                "failure": failure,
                "sampled_apps": context.sampled_apps,
                "app_file_support": context.app_file_support,
                "sampled_files": context.sampled_files,
                "generation_context": generation_context,
            },
            ensure_ascii=False,
        )
        data = self.call_json(system_prompt, user_text, context.setup_image)
        repaired = data.get("task_candidate")
        return repaired if isinstance(repaired, dict) else candidate
