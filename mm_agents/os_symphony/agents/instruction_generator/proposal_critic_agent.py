from __future__ import annotations

import json
from typing import Any, Dict, List

from mm_agents.os_symphony.agents.instruction_generator.base_agent import WorkflowCostTracker, WorkflowLLMAgent
from mm_agents.os_symphony.agents.instruction_generator.models import ProposalCandidate, ProposalSelectionInput, WorkflowSharedState
from mm_agents.os_symphony.agents.instruction_generator.prompts import load_prompt


class ProposalCritiqueAgent(WorkflowLLMAgent):
    def __init__(self, name: str, engine_params: Dict[str, Any], cost_tracker: WorkflowCostTracker, platform: str = "linux"):
        super().__init__(name, engine_params, cost_tracker, platform)

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
        return_data = {"accepted": accepted[:target_count], "rejected": rejected, "coverage_summary": data.get("coverage_summary", {})}
        return return_data
