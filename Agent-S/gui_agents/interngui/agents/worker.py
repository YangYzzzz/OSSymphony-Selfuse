from functools import partial
import logging
import textwrap
from typing import Dict, List, Tuple

from gui_agents.interngui.agents.os_aci import OSWorldACI
from gui_agents.interngui.core.module import BaseModule
from gui_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY
from gui_agents.interngui.utils.common_utils import (
    call_llm_safe,
    call_llm_formatted,
    parse_code_from_string,
    split_thinking_response,
    create_pyautogui_code,
)
from gui_agents.interngui.utils.formatters import (
    SINGLE_ACTION_FORMATTER,
    CODE_VALID_FORMATTER,
)

logger = logging.getLogger("desktopenv.agent")


class Worker(BaseModule):
    def __init__(
        self,
        engine_params_for_orchestrator: Dict,
        engine_params_for_reflector: Dict,
        os_aci: OSWorldACI,
        platform: str = "ubuntu",
        max_trajectory_length: int = 8,
        enable_reflection: bool = True,
        enable_rewrite_instruction: bool = False,
        use_search_first: bool = False,
    ):
        """
        Worker receives the main task and generates actions, without the need of hierarchical planning
        Args:
            worker_engine_params: Dict
                Parameters for the worker agent
            os_aci: Agent
                The grounding agent to use
            platform: str
                OS platform the agent runs on (darwin, linux, windows)
            max_trajectory_length: int
                The amount of images turns to keep
            enable_reflection: bool
                Whether to enable reflection
        """
        super().__init__(platform=platform)

        # 每个地方不一样
        self.temperature = engine_params_for_orchestrator.get("temperature", 0.0)
        self.tool_config = engine_params_for_orchestrator.get("tool_config", "")
        self.use_thinking = engine_params_for_orchestrator.get("model", "") in [
            "claude-opus-4-20250514",
            "claude-sonnet-4-20250514",
            "claude-3-7-sonnet-20250219",
            "claude-sonnet-4-5-20250929",
        ]
        self.engine_params_for_orchestrator = engine_params_for_orchestrator
        self.engine_params_for_reflector = engine_params_for_reflector
        self.os_aci: OSWorldACI = os_aci
        self.max_trajectory_length = max_trajectory_length
        self.enable_reflection = enable_reflection
        self.enable_rewrite_instruction = enable_rewrite_instruction
        self.use_search_first = use_search_first
        self.reset()

    def reset(self):
        # 根据环境动态调整 Agent，我们也要编写出来这种代码！
        if self.platform != "linux":
            skipped_actions = ["set_cell_values"]
        else:
            skipped_actions = []

        # Hide code agent action entirely if no env/controller is available
        if not getattr(self.os_aci, "env", None) or not getattr(
            getattr(self.os_aci, "env", None), "controller", None
        ):
            skipped_actions.append("call_code_agent")

        sys_prompt = PROCEDURAL_MEMORY.construct_simple_worker_procedural_memory(
            agent_class=type(self.os_aci), 
            skipped_actions=skipped_actions,
            tool_config=self.tool_config
        ).replace("CURRENT_OS", self.platform)

        # Worker 内设置了 重写Agent，反思Agent，规划Agent 三个智能体
        self.orchestrator_agent = self._create_agent(
            engine_params=self.engine_params_for_orchestrator, 
            system_prompt=sys_prompt
        )
        self.reflector_agent = self._create_agent(
            engine_params=self.engine_params_for_reflector,
            system_prompt=PROCEDURAL_MEMORY.REFLECTION_ON_TRAJECTORY
        )
        # 复用规划者的配置即可, 仅使用一次
        self.rewrite_agent = self._create_agent(
            engine_params=self.engine_params_for_orchestrator,
            system_prompt=PROCEDURAL_MEMORY.REWRITE_GUI_INSTRUCTION
        )
        self.instruction = None
        self.turn_count = 0
        self.worker_history = []
        self.reflections = []
        self.cost_this_turn = 0
        self.screenshot_inputs = []

    def flush_messages(self):
        """Flush messages based on the model's context limits.

        This method ensures that the agent's message history does not exceed the maximum trajectory length.

        Side Effects:
            - Modifies the messages of generator, reflection, and bon_judge agents to fit within the context limits.
        """
        engine_type = self.engine_params_for_orchestrator.get("engine_type", "")

        # Flush strategy for long-context models: keep all text, only keep latest images
        if engine_type in ["anthropic", "openai", "gemini"]:
            max_images = self.max_trajectory_length
            for agent in [self.orchestrator_agent, self.reflector_agent]:
                if agent is None:
                    continue
                # keep latest k images
                img_count = 0
                for i in range(len(agent.messages) - 1, -1, -1):
                    for j in range(len(agent.messages[i]["content"])):
                        if "image" in agent.messages[i]["content"][j].get("type", ""):
                            img_count += 1
                            if img_count > max_images:
                                del agent.messages[i]["content"][j]

        # Flush strategy for non-long-context models: drop full turns
        else:
            # generator msgs are alternating [user, assistant], so 2 per round
            if len(self.orchestrator_agent.messages) > 2 * self.max_trajectory_length + 1:
                self.orchestrator_agent.messages.pop(1)
                self.orchestrator_agent.messages.pop(1)
            # reflector msgs are all [(user text, user image)], so 1 per round
            if len(self.reflector_agent.messages) > self.max_trajectory_length + 1:
                self.reflector_agent.messages.pop(1)

    def _generate_reflection(self, instruction: str, obs: Dict):
        """
        Generate a reflection based on the current observation and instruction.

        Args:
            instruction (str): The task instruction.
            obs (Dict): The current observation containing the screenshot.

        Returns:
            Optional[str, str]: The generated reflection text and thoughts, if any (turn_count > 0).

        Side Effects:
            - Updates reflection agent's history
            - Generates reflection response with API call
        """
        reflection = None
        reflection_thoughts = None
        if self.enable_reflection:
            # Load the initial message
            if self.turn_count == 0:
                text_content = textwrap.dedent(
                    f"""
                    Task Description: {instruction}
                    Current Trajectory below:
                    """
                )
                updated_sys_prompt = (
                    self.reflector_agent.system_prompt + "\n" + text_content
                )
                self.reflector_agent.add_system_prompt(updated_sys_prompt)
                self.reflector_agent.add_message(
                    text_content="The initial screen is provided. No action has been taken yet.",
                    image_content=obs["screenshot"],
                    role="user",
                )
            # Load the latest action
            else:
                self.reflector_agent.add_message(
                    text_content=self.worker_history[-1],
                    image_content=obs["screenshot"],
                    role="user"
                )
                full_reflection = call_llm_safe(
                    self.reflector_agent,
                    temperature=self.engine_params_for_reflector.get("temperture", 0.1),
                    use_thinking=self.use_thinking,
                )
                reflection, reflection_thoughts = split_thinking_response(
                    full_reflection
                )
                self.reflections.append(reflection)
                logger.info("REFLECTION THOUGHTS: %s", reflection_thoughts)
                logger.info("REFLECTION: %s", reflection)
        return reflection, reflection_thoughts

    def generate_next_action(self, instruction: str, obs: Dict, is_last_step: bool) -> Tuple[Dict, List]:
        """
        Predict the next action(s) based on the current observation.
        """
        # Query Rewrite First
        if self.instruction is None and self.enable_rewrite_instruction:
            self.rewrite_agent.add_message(
                text_content=instruction,
                image_content=obs["screenshot"],
                role="user"
            )
            self.instruction = call_llm_safe(self.rewrite_agent)
        if self.instruction:
            instruction = self.instruction
            
        self.os_aci.assign_screenshot(obs)
        self.os_aci.set_task_instruction(instruction)

        generator_message = (
            ""
            if self.turn_count > 0
            else "The initial screen is provided. No action has been taken yet."
        )

        if self.turn_count == 0 and self.use_search_first:
            generator_message += " Note: 'USE SEARCH FIRST' mode is enabled. You are required to begin by using a search-related action(call_search_agent). This is to gather helpful tutorials or information to guide the subsequent steps of your execution."
        
        # Load the task into the system prompt
        if is_last_step:
            # Eager mode: must decide done / fail
            prompt_with_instructions = PROCEDURAL_MEMORY.construct_eager_mode_procedural_memory(agent_class=type(self.os_aci)).replace(
                "TASK_DESCRIPTION", instruction
            ).replace(
                "CURRENT_OS", self.platform
            )
            self.orchestrator_agent.add_system_prompt(prompt_with_instructions)
        else:
            tutorials = ""
            for idx, t in enumerate(self.os_aci.tutorials, start=1):
                tutorials += f"Tutorial {idx}: {t}\n"
            
            prompt_with_instructions = self.orchestrator_agent.system_prompt.replace(
                "TASK_DESCRIPTION", instruction
            ).replace(
                "TUTORIAL_PLACEHOLDER", tutorials
            )

            self.orchestrator_agent.add_system_prompt(prompt_with_instructions)

        # Get the per-step reflection
        reflection, reflection_thoughts = self._generate_reflection(instruction, obs)
        if reflection:
            generator_message += f"REFLECTION: You may use this reflection on the previous action and overall trajectory:\n{reflection}\n"

        # Get the grounding agent's knowledge base buffer
        # Important By Yang! 有一个专门的“记笔记”的操作，目的是解决上下文过少的问题，即可以将重要的文字信息记录在列表内，即使长距离也能保有。
        generator_message += (
            f"\nCurrent Text Buffer = [{','.join(self.os_aci.notes)}]\n"
        )

        # Add code agent result from previous step if available (from full task or subtask execution)
        if (
            hasattr(self.os_aci, "last_code_agent_result")
            and self.os_aci.last_code_agent_result is not None
        ):
            code_result = self.os_aci.last_code_agent_result
            generator_message += f"\nCODE AGENT RESULT:\n"
            generator_message += (
                f"Task/Subtask Instruction: {code_result['task_instruction']}\n"
            )
            generator_message += f"Steps Completed: {code_result['steps_executed']}\n"
            generator_message += f"Max Steps: {code_result['budget']}\n"
            generator_message += (
                f"Completion Reason: {code_result['completion_reason']}\n"
            )
            generator_message += f"Summary: {code_result['summary']}\n"
            # if code_result["execution_history"]:
            #     generator_message += f"Execution History:\n"
            #     for i, step in enumerate(code_result["execution_history"]):
            #         action = step["action"]
            #         # Format code snippets with proper backticks
            #         if "```python" in action:
            #             # Extract Python code and format it
            #             code_start = action.find("```python") + 9
            #             code_end = action.find("```", code_start)
            #             if code_end != -1:
            #                 python_code = action[code_start:code_end].strip()
            #                 generator_message += (
            #                     f"Step {i+1}: \n```python\n{python_code}\n```\n"
            #                 )
            #             else:
            #                 generator_message += f"Step {i+1}: \n{action}\n"
            #         elif "```bash" in action:
            #             # Extract Bash code and format it
            #             code_start = action.find("```bash") + 7
            #             code_end = action.find("```", code_start)
            #             if code_end != -1:
            #                 bash_code = action[code_start:code_end].strip()
            #                 generator_message += (
            #                     f"Step {i+1}: \n```bash\n{bash_code}\n```\n"
            #                 )
            #             else:
            #                 generator_message += f"Step {i+1}: \n{action}\n"
            #         else:
            #             generator_message += f"Step {i+1}: \n{action}\n"
            generator_message += "\n"
            # Reset the code agent result after adding it to context
            self.os_aci.last_code_agent_result = None

        if (
            hasattr(self.os_aci, "last_search_agent_result")
            and self.os_aci.last_search_agent_result is not None
        ):
            # Retrieve the result dictionary
            search_result = self.os_aci.last_search_agent_result

            # Add a clear, distinct header for this section in the prompt
            generator_message += f"\nSEARCH AGENT RESULT:\n"
            
            # Add contextual metadata from the search task
            generator_message += f"Search Query: {search_result['query']}\n"
            generator_message += f"Search Completion Reason: {search_result['completion_reason']}\n"
            generator_message += "Search Result: "
            # Add the most important part: the tutorial found by the agent.
            # This is given a prominent sub-header so the LLM knows to pay close attention.
            if search_result["completion_reason"] == "DONE":
                generator_message += f'Search is completed, the tutorial it found has already add to your system prompt.\n'
            elif search_result["completion_reason"] == "FAIL":
                generator_message += f"Search is fail, the failure reason or the hint is as follow: {search_result['final_answer']}\n"
        
            
            # CRITICAL: Reset the search agent result after adding it to the context.
            # This prevents it from being added to the prompt again in the next turn.
            self.os_aci.last_search_agent_result = None

        # Finalize the generator message
        self.orchestrator_agent.add_message(
            generator_message, image_content=obs["screenshot"], role="user"
        )

        # Generate the plan and next action
        format_checkers = [
            SINGLE_ACTION_FORMATTER,
            partial(CODE_VALID_FORMATTER, self.os_aci, obs),
        ]
        plan = call_llm_formatted(
            self.orchestrator_agent,
            format_checkers,
            temperature=self.engine_params_for_orchestrator.get("temperture", 0.1),
            use_thinking=self.use_thinking,
        )
        self.worker_history.append(plan)
        self.orchestrator_agent.add_message(plan, role="assistant")
        logger.info("PLAN:\n %s", plan)

        # Extract the next action from the plan
        # 此时的plan code e.g. agent.click('xxxxx', 1)
        plan_code = parse_code_from_string(plan)
        coordinates = None
        try:
            assert plan_code, "Plan code should not be empty"
            # 此时的exec_code e.g. import pyautogui; pyautogui.click(1, 2);
            exec_code, coordinates = create_pyautogui_code(self.os_aci, plan_code, obs)
        except Exception as e:
            logger.error(
                f"Could not evaluate the following plan code:\n{plan_code}\nError: {e}"
            )
            exec_code = self.os_aci.wait(
                1.333
            )  # Skip a turn if the code cannot be evaluated

        executor_info = {
            "refined_instruction": self.instruction,
            "plan": plan,
            "plan_code": plan_code,
            "exec_code": exec_code,
            "coordinates": coordinates,
            "reflection": reflection,
            "reflection_thoughts": reflection_thoughts,
            "code_agent_output": (
                self.os_aci.last_code_agent_result
                if hasattr(self.os_aci, "last_code_agent_result")
                and self.os_aci.last_code_agent_result is not None
                else None
            ),
        }
        self.turn_count += 1
        self.screenshot_inputs.append(obs["screenshot"])
        self.flush_messages()
        return executor_info, [exec_code]
