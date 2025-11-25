from ast import parse
import logging
import json
from typing import List, Dict, Any, Optional, Tuple
from mm_agents.interngui.utils.common_utils import (
    call_llm_safe,
    call_llm_formatted,
    enhance_observation,
    split_thinking_response,
    parse_code_from_string
)
from functools import partial
from mm_agents.interngui.utils.formatters import JSON_ANSWER_FORMATTER
from mm_agents.interngui.core.mllm import LMMAgent
from mm_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY
import textwrap
import imagehash
import io
import os
from PIL import Image, ImageDraw
import numpy as np
from skimage.metrics import structural_similarity as ssim

logger = logging.getLogger("desktopenv.agent")

'''
统一一下：所有obs存的都是字典，调用llm时才解包
'''


class StepBehavior:
    """
    Narrative Step Behavior.
    Description of each step, cosists of generative agent (main agent)'s output, screenshot (if this step is milestone), and textual description.
    The textual description shows that how the agent thought and did, and how the state changes. 
    """
    def __init__(self, is_milestone: bool, gen_output: str, summary: str, obs: Dict, action_dict: Dict):
        self.is_milestone = is_milestone
        self.gen_output = gen_output
        self.obs = obs
        self.summary = summary
        self.action_dict = action_dict
        # 优化循环检测复杂度的变量
        # --- 1. pHash ---
        self.phash = None
        # --- 2. SSIM 历史比较 ---
        self.ssim_list = [] # 计算当前图片与历史图片的ssim值
    
    def _update_phash_ssim(self, history: List):
        # 根据历史的图片信息计算当前图片的 ssim_list, 优化循环检测的复杂度
        # 首先更新 pHash
        cur_img = Image.open(io.BytesIO(self.obs["screenshot"]))
        cur_img_gray = cur_img.convert('L')
        cur_img_np = np.array(cur_img_gray)
        self.phash = imagehash.phash(cur_img)
        # 更新 ssim_list
        for hs in history:
            compare_img = Image.open(io.BytesIO(hs.obs["screenshot"]))
            compare_img_gray = compare_img.convert('L')
            compare_img_np = np.array(compare_img_gray)
            self.ssim_list.append(ssim(cur_img_np, compare_img_np, data_range=cur_img_np.max() - compare_img_np.min()))

class ReflectionMemoryAgent:
    """
    Reflection Memory Agent (RMA).
    Responsible for maintaining long-term memory, extracting narratives from trajectories,
    providing reflections to the Main Agent, and validating task completion status.
    """
    def __init__(self, engine_params: Dict, max_img_len: int = 9):
        """
        Initialize the RMA.

        Args:
        - engine_params: 
            {
                "engine_type": args.provider,
                "model": args.model,
                "base_url": args.model_url,
                "api_key": args.model_api_key,
                "temperature": getattr(args, "model_temperature", None),
            }
        - max_img_len: max image number to use in reflection process, 按照更新逻辑, 相当于历史图片是 max_img_len-1 张, 加一张当前图片, 一共是 max_img_len 张
        - memoryer_level: 为了消融实验设计的变量, 整理最终版本代码时需移除
            - 1: 和agents3类似, last k轮的generator output和图片
            - 2: 文字信息采用Step Behavior, 图片采用last k
            - 3: 和设计版本一致
        """

        self.engine_params = engine_params

        self.max_img_len = max_img_len

        self.memoryer_level = engine_params['memoryer_level']
        
        self.reset()

        logger.info(f"ReflectionMemoryAgent initialized with:\n {self.engine_params}")
        

    def reset(self):
        """Reset the code agent state."""
        logger.debug("Resetting RMA state")

        self.instruction = None

        self.trajectory: List[StepBehavior] = []

        self.knowledge_base: List[str] = []

        self.last_code_step_idx = -1        # 没点卵用

        '''
        用于控制图片数量，始终存放max_img_len张图片
        更新逻辑是第0张screenshot始终保留。总图片数量小于max_img_len，保留全部；大于max_img_len，milestone从索引为1开始进行FIFO。
        '''
        self.active_img_idx = []        

        self.reflection_agent = LMMAgent(
            engine_params=self.engine_params,
            system_prompt=PROCEDURAL_MEMORY.REFLECTION_SYSTEM_PROMPT,
        )
        self.behavior_agent = LMMAgent(
            engine_params=self.engine_params,       # 暂定两个agent用同一个模型
            system_prompt=PROCEDURAL_MEMORY.SUMMARIZE_STEP_SYSTEM_PROMPT
        )
    
    def add_instruction(self, instruction):
        """
        [Interface] Main -> RMA
        Main agent set the instruction to RMA.
        """
        self.instruction = instruction

    def _update_trajectory(self, step_behavior):
        self.trajectory.append(step_behavior)
        if len(self.active_img_idx) >= self.max_img_len:
            if step_behavior.is_milestone:
                self.active_img_idx.append(len(self.trajectory) - 1)      # 超过max_img_len，只喂milestone的图片
                del self.active_img_idx[1]          # 从索引为1开始FIFO
        else:
            self.active_img_idx.append(len(self.trajectory) - 1)        # 不足max_img_len, 全塞入
            
        assert len(self.active_img_idx) <= self.max_img_len, "[RMA] StepBehavior更新逻辑有问题!!"

    def _summarize_step_behavior(
            self, 
            generator_output: str, 
            cur_obs: Dict, 
            enhanced_obs: bytes | None, 
            is_milestone: bool,
            mode: str = "gui",
            code_exec_summary: str = "",
            action_dict: Dict = {}
        ) -> Tuple[StepBehavior, str]:
        """
        [Interface] Main -> RMA
        The Main Agent (MA) calls this method to "feed" the information of the just-completed step to the RMA.
        RMA will internally process and store this step.
        """

        if mode == "search":
            is_success = "success"
            # summary直接写死
            step_behavior = StepBehavior(
                False, 
                generator_output,
                "Search Agent was called last step, and a tutorial has been generated.", 
                cur_obs,
                action_dict
            )
        elif mode == "code":
            self.last_code_step_idx = len(self.trajectory)

            is_success = "success"
            # summary直接存code agent返回的summary
            step_behavior = StepBehavior(
                False, 
                generator_output,
                f"Code Agent was called last step, and the summary of its trajectory is: \n---\n{code_exec_summary}\n---", 
                cur_obs,
                action_dict
            )
        else:       # 普遍的GUI操作，用LLM来生成summary
            prev_obs = self.trajectory[-1].obs

            text_content = f"""Computer Use Agent's Output: \n{generator_output}"""
            
            
            self.behavior_agent.reset()     # don't need history messages
            
            updated_sys_prompt = (
                self.behavior_agent.system_prompt + "\n" + text_content
            )
            self.behavior_agent.add_system_prompt(updated_sys_prompt)

            # 添加三张图片
            self.behavior_agent.add_message(
                text_content="This is the observation before executing action.",
                image_content=prev_obs['screenshot'],
                role="user"
            )
            self.behavior_agent.add_message(
                text_content="This is the zoom-in view, which may help you to identify the operational region.",
                image_content=enhanced_obs,
                role="user"
            )
            self.behavior_agent.add_message(
                text_content="This is the observation after executing action.",
                image_content=cur_obs['screenshot'],
                role="user"
            )

            required_fields = ["summary", "evaluation"]
            format_checkers = [
                partial(JSON_ANSWER_FORMATTER, required_fields)
            ]

            full_response = call_llm_formatted(
                self.behavior_agent,
                format_checkers,
                temperature=self.engine_params.get("temperture", 0.1),
            )

            response = parse_code_from_string(full_response)

            try:
                data = json.loads(response)
                behavior_summary = data['summary']
                is_success = data["evaluation"]
            except Exception as e:
                print("[RMA] 处理step summary时遇到错误: ", e)
                logger.info("Response is not a JSON object or miss required keys!")
                behavior_summary = response           # 把所有内容都当作reflection
                is_success = "success"

            # print("@@@@@@@@@@ Summary Response: ", response)

            step_behavior = StepBehavior(is_milestone, generator_output, behavior_summary, cur_obs, action_dict)

        return step_behavior, is_success

    def get_reflection(
            self, 
            cur_obs: Dict, 
            generator_output: str, 
            coordinates: List, 
            mode: str="gui", 
            code_exec_summary: str = "",
            action_dict: Dict = {}
        ) -> Dict:
        """
        [Interface] RMA -> Main
        The Main Agent (MA) calls this method to get RMA's reflection before deciding the next action.
        
        Args:
        - cur_obs (Dict): The Main Agent's current observation (o_k).
        - generator_output (str): The thoughts, screen analysis and action of Main Agent.
        - coordinates (List): coordinates in the last operation step of Main Agent.
        - mode(str): [gui, code, search]. Indicate which agent that main agent called last step.
        - code_exec_summary: execution summary for code agent.
        - action_dict: extracted action from generator output.
        
        Returns:
        - reflection_info(Dict): all the info related to reflection
        """   
        if self.memoryer_level == 0:
            return {
                "reflection": None,
                "reflection_thoughts": None,
                "existing_knowledge": None,
                "is_milestone": False,
                "new_knowledge": None,
                "step_summary": None,
                "hint": {
                    "gui_operation_error": False,
                    "lack_of_tutorial": False,
                    "code_error": False, # Code Error: True 不代表产生错误, 仅是一个辅助提醒
                    "loop_detection": None,
                }
            } 

        reflection = None
        reflection_thought = None
        if len(self.trajectory) == 0:
            step_behavior = StepBehavior(
                True, 
                "The initial screen is provided. No action has been taken yet.",
                "The initial screen is provided. No action has been taken yet.", 
                cur_obs,
                action_dict
            )
            step_behavior._update_phash_ssim(self.trajectory)
            self._update_trajectory(step_behavior)
            reflection_info = {
                "reflection": reflection,
                "reflection_thoughts": reflection_thought,
                "existing_knowledge": "\n".join(self.knowledge_base),
                "is_milestone": True,
                "new_knowledge": "",
                "step_summary": "",
                "loop_detection": None
            } 
        else: 
            ### Step Summary
            # 图像增强，coordinates可能包含了一个或两个坐标，以他们为中心，向周围外扩一些
            prev_obs = self.trajectory[-1].obs
            enhanced_obs = None
            if coordinates:
                enhanced_obs, _, _, _, _ = enhance_observation(
                    prev_obs["screenshot"], 
                    coordinates,
                    draw=True
                )
        
            # 制作step behavior
            step_behavior, last_gui_check = self._summarize_step_behavior(  # 先进行step summary，目的是获取单步gui操作的评估结果，这里的is_milestone未知，先置为False。
                generator_output, 
                cur_obs, 
                enhanced_obs, 
                False, 
                mode, 
                code_exec_summary, 
                action_dict
            )    
            step_behavior._update_phash_ssim(self.trajectory)
            
            ### make additional hints
            additional_hints = []
            if not last_gui_check:
                additional_hints.append(f"\t- Warning: The last GUI operation might be failed. Careful review is required to avoid GUI Operation Error.")

            code_error_hint = False
            if len(self.trajectory) - self.last_code_step_idx < 5 and self.last_code_step_idx != -1:      # 5步之内都有可能是验证
                code_error_hint = True
                additional_hints.append(f"\t- Warning: The Computer Use Agent might in the verification stage of Code Agent. Careful review is required to avoid Code Error.")
            # 循环检测, 检测出的Step号是从0开始标注的
            from mm_agents.interngui.utils.loop_detection import detect_loop
            # print(f'当前长度为: {len(self.trajectory)+1}, 开始检测循环!!!!!!!!')
            is_loop, loop_details = detect_loop(full_trajectory=self.trajectory + [step_behavior], N=3)
            if is_loop and loop_details:
                match_sequence_indices = loop_details["match_sequence_indices"]
                loop_hint_message = f"\t- Warning: A potential LOOP has been detected between Step {match_sequence_indices[0]} and Step {match_sequence_indices[-1]}. Careful review is required to avoid Repetitive Behavior Error."
                additional_hints.append(loop_hint_message)

            self.reflection_agent.reset()

            updated_sys_prompt = (
                PROCEDURAL_MEMORY.REFLECTION_SYSTEM_PROMPT + "\n\n" + 
                f"---\n- **user instruction**: {self.instruction}\n" + 
                "- **existing knowledge**: \n" + "\n".join(self.knowledge_base) + 
                "\n - **additional_hints**: " + "\n".join(additional_hints) + "\n---"
            )

            self.reflection_agent.add_system_prompt(updated_sys_prompt)


            ### 消融实验的修改部分
            print(f"=== Current Memoryer Level is {self.memoryer_level}! ===")
            if self.memoryer_level == 1:
                start_idx = max(0, len(self.trajectory) - (self.max_img_len - 1))   # 确定起始索引
                print("=" * 30)
                for i, step in enumerate(self.trajectory[start_idx:], start=start_idx):
                    text_content = f"""### (Step {i}) history:\nsummary: '''\n{step.gen_output}\n'''"""     # 喂main agent完整的输出
        
                    print(text_content)

                    text_content += f"\nscreenshot (after executing action): (attached below)"
                    self.reflection_agent.add_message(
                        text_content=text_content,
                        image_content=step.obs['screenshot'],     
                        role="user",
                    )
                print("=" * 30)
            elif self.memoryer_level == 2:
                print("=" * 30)
                for i, step in enumerate(self.trajectory):
                    text_content = f"""### (Step {i}) history:\nsummary: '''\n{step.summary}\n'''"""        # 文字部分采用summary
                    active_img_idx = list(range(len(self.trajectory) - (self.max_img_len - 1), len(self.trajectory)))   # 只做一个last k的索引列表
                    if i in active_img_idx:
                        text_content += f"\nscreenshot (after executing action): (attached below)"

                    print(text_content)

                    self.reflection_agent.add_message(
                        text_content=text_content,
                        image_content=step.obs['screenshot'] if i in active_img_idx else None,     
                        role="user",
                    )
                print("=" * 30)
            else:
                for i, step in enumerate(self.trajectory):
                    text_content = f"""### (Step {i}) history:\nsummary: '''\n{step.summary}\n'''"""
                    if i in self.active_img_idx:
                        if i == 0:
                            text_content += f"\ninitial screenshot:"
                        else: 
                            text_content += f"\nscreenshot (after executing action): (attached below)"

                    self.reflection_agent.add_message(
                        text_content=text_content,
                        image_content=step.obs['screenshot'] if i in self.active_img_idx else None,     
                        role="user",
                    )
                
            text_content = f"""### (Last Step) CUA's output (has been finished):\n---\n{generator_output}\n---\n\nlatest_screenshot:  (attached below)"""
            self.reflection_agent.add_message(
                text_content=text_content,
                image_content=cur_obs['screenshot'],
                role="user",
            )
            
            required_fields = ["is_milestone", "reflection", "knowledge"]
        
            format_checkers = [
                partial(JSON_ANSWER_FORMATTER, required_fields)
            ]

            full_response = call_llm_formatted(
                self.reflection_agent,
                format_checkers
            )

            # print("=" * 30)
            # print(full_response)
            # print("=" * 30)

            reflection_thought = full_response      # 这里直接传full response了，反正也没有实际用途

            response = parse_code_from_string(full_response)
            
            try:
                data = json.loads(response)
                reflection = data['reflection']
                is_milestone = data["is_milestone"]
                knowledge = data['knowledge']
            except Exception as e:
                print("[RMA] 处理reflection时遇到错误: ", e)
                logger.info("Response is not a JSON object or miss required keys!")
                reflection = response           # 把所有内容都当作reflection
                is_milestone = False
                knowledge = ""

            if len(knowledge) > 0:
                self.knowledge_base.append(knowledge)
            
            if isinstance(is_milestone, str):
                is_milestone = True if "true" in is_milestone.lower() else False
            
            # update is_milestone
            step_behavior.is_milestone = is_milestone
            self._update_trajectory(step_behavior)

            reflection_info = {
                "reflection": reflection,
                "reflection_thoughts": reflection_thought,
                "existing_knowledge": "\n".join(self.knowledge_base),
                "is_milestone": is_milestone,
                "new_knowledge": knowledge,
                "step_summary": step_behavior.summary,
                "hint": {
                    "gui_operation_error": not last_gui_check,
                    "lack_of_tutorial": is_loop,
                    "code_error": code_error_hint, # Code Error: True 不代表产生错误, 仅是一个辅助提醒
                    "loop_detection": loop_details,
                }
            } 
            # with open(f'results/debug_memory_agent/multi_apps/c7c1e4c3-9e92-4eba-a4b8-689953975ea4/supp_info_{supp_info["step_num"]}', 'w', encoding='utf-8') as f:
            #     json.dump(supp_info, f, indent=4, ensure_ascii=False)
            
        return reflection_info
    
    def _get_reflection_level_1(self, cur_obs: Dict, generator_output: str):
        """
        最简单的reflection, 图片和文字都是last k

        Args:
        - cur_obs (Dict): The Main Agent's current observation (o_k).
        - generator_output (str): The thoughts, screen analysis and action of Main Agent.

        Returns:
        - reflection_info(Dict): all the info related to reflection
        """

        updated_sys_prompt = (
            PROCEDURAL_MEMORY.REFLECTION_SYSTEM_PROMPT + "\n\n" + 
            f"---\n- **user instruction**: {self.instruction}\n" + 
            "- **existing knowledge**: \n" + "\n".join(self.knowledge_base)
        )

        self.reflection_agent.add_system_prompt(updated_sys_prompt)
        
        for i, step in enumerate(self.trajectory):

            text_content = f"""### (Step {i}) history:\nsummary: '''\n{step.summary}\n'''"""

            if i in self.active_img_idx:
                if i == 0:
                    text_content += f"\ninitial screenshot:"
                else: 
                    text_content += f"\nscreenshot (after executing action): (attached below)"
            
            # debug
            # print(text_content)
            # if i in self.active_img_idx:
            #     print(f"image content: step_{i + 1}.png")

            self.reflection_agent.add_message(
                text_content=text_content,
                image_content=step.obs['screenshot'] if i in self.active_img_idx else None,     
                role="user",
            )



    