"""
    第一阶段粗糙生成指令的Agent
    输入: 软件名 + 初始截图
    输出: 结构化列表, task_nums 个具体的可被验证的任务 (最好给出验证的逻辑,这样是否能更简单) 
    使用强模型, 同时需要具体设计一个generate的prompt
"""
import logging
from typing import Dict, List, Any
import re

from mm_agents.os_symphony.memory.procedural_memory import PROCEDURAL_MEMORY
from mm_agents.os_symphony.utils.common_utils import call_llm_safe
from mm_agents.os_symphony.core.mllm import LMMAgent

logger = logging.getLogger("desktopenv.coarse_instruction_generation_agent")


class CoarseInstructionGenerationAgent:
    """A dedicated agent for generating coarse instructions from initial screenshots."""

    def __init__(self, engine_params: Dict, platform: str = "linux"):
        """Initialize the agent."""
        if not engine_params:
            raise ValueError("engine_params cannot be None or empty")

        self.engine_params = engine_params
        self.temperature = engine_params.get("temperature", 0.3)
        self.platform = platform
        self.reset()

    def reset(self):
        """Reset the agent state."""
        logger.debug("Resetting CoarseInstructionGenerationAgent state")
        self.agent = LMMAgent(
            engine_params=self.engine_params,
            system_prompt=""
        )
        self.system_prompt_template = PROCEDURAL_MEMORY.construct_instruction_generation_procedural_memory(
            platform=self.platform
        )

    def parse_instruction(self, response: str) -> List[Dict[str, Any]]:
        """
        Parse LLM response to extract structured task list using regex.
        
        Args:
            response: LLM response text
            
        Returns:
            List[Dict]: List of tasks, each with description, verification, and complexity
        """
        tasks = []
        
        try:
            # Extract all <task> blocks
            task_blocks = re.findall(r'<task>(.*?)</task>', response, re.DOTALL)
            
            if not task_blocks:
                logger.warning("No <task> blocks found in response")
                return tasks
            
            for block in task_blocks:
                task = self._parse_single_task(block)
                if task:
                    tasks.append(task)
            
            logger.info(f"Successfully parsed {len(tasks)} tasks from XML")
            
        except Exception as e:
            logger.error(f"Error parsing instruction response: {e}")
            tasks = []
        
        return tasks

    def _parse_single_task(self, block: str) -> Dict[str, Any]:
        """Parse a single task block."""
        try:
            # Extract description
            desc_match = re.search(r'<description>(.*?)</description>', block, re.DOTALL)
            if not desc_match:
                logger.warning("No description found in task block")
                return {}
            
            description = desc_match.group(1).strip()
            
            # Extract condition
            cond_match = re.search(r'<condition>(.*?)</condition>', block, re.DOTALL)
            if not cond_match:
                logger.warning("No condition found in task block")
                return {}
            
            condition = cond_match.group(1).strip()
            
            # Extract expected_result
            result_match = re.search(r'<expected_result>(.*?)</expected_result>', block, re.DOTALL)
            expected_result = result_match.group(1).strip() if result_match else "Task completed successfully"
            
            # Extract complexity
            comp_match = re.search(r'<complexity>(.*?)</complexity>', block, re.DOTALL)
            if not comp_match:
                logger.warning("No complexity found in task block")
                complexity = "medium"
            else:
                complexity = comp_match.group(1).strip().lower()
                if complexity not in ['low', 'medium', 'high']:
                    complexity = "medium"
            
            return {
                "description": description,
                "verification": {
                    "condition": condition,
                    "expected_result": expected_result
                },
                "complexity": complexity
            }
            
        except Exception as e:
            logger.warning(f"Failed to parse task block: {e}")
            return {}

    def generate(self, app_name: str, observation: Dict, task_nums: int = 10) -> List[Dict[str, Any]]:
        """
        Generate coarse-grained task list.
        
        Args:
            app_name: Software name
            observation: Observation data containing screenshot
            task_nums: Number of tasks to generate
            
        Returns:
            List[Dict]: Generated task list
            [
                {           
                    "description": description,
                    "verification": {
                        "condition": condition,
                        "expected_result": expected_result
                    },
                    "complexity": complexity
                }
            ]
        """
        try:
            # Prepare system prompt
            system_prompt = self.system_prompt_template.replace("APPNAME", app_name).replace("TASKNUMBERS", str(task_nums))
            self.agent.add_system_prompt(system_prompt=system_prompt)
            
            # Add user input with screenshot
            screenshot_msg = f"Here is the screenshot of the software. Please generate {task_nums} tasks based on this interface:"
            self.agent.add_message(
                text_content=screenshot_msg,
                image_content=observation.get("screenshot"),
                role="user"
            )
            
            # Call LLM
            logger.info(f"Generating {task_nums} tasks for {app_name}")
            response = call_llm_safe(
                self.agent,
                temperature=self.temperature
            )
            
            if not response:
                logger.error("Empty response from LLM")
                return []
            
            # Parse response
            tasks = self.parse_instruction(response)
            
            # Limit to requested number of tasks
            if len(tasks) < task_nums:
                logger.warning(f"Requested {task_nums} tasks but only generated {len(tasks)}")
            
            # Log results
            for i, task in enumerate(tasks):
                logger.info(f"Task {i+1}: {task['description'][:80]}...")
                logger.debug(f"  Condition: {task['verification']['condition'][:80]}...")
                logger.debug(f"  Complexity: {task['complexity']}")
            
            return tasks
            
        except Exception as e:
            logger.error(f"Error in generate method: {e}", exc_info=True)
            return []

