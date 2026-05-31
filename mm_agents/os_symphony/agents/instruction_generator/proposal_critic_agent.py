from __future__ import annotations

import json
from typing import Any, Dict, List

from mm_agents.os_symphony.agents.instruction_generator.base_agent import WorkflowCostTracker, WorkflowLLMAgent
from mm_agents.os_symphony.agents.instruction_generator.models import GenerationContext
from mm_agents.os_symphony.agents.instruction_generator.prompts import load_prompt


class ProposalCritiqueAgent(WorkflowLLMAgent):
    def __init__(self, name: str, engine_params: Dict[str, Any], cost_tracker: WorkflowCostTracker, platform: str = "linux"):
        super().__init__(name, engine_params, cost_tracker, platform)

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
