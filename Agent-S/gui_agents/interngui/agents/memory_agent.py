import logging
import json
from typing import List, Dict, Any, Optional, Tuple
from gui_agents.interngui.utils.common_utils import (
    call_llm_safe,
    call_llm_formatted,
    split_thinking_response,
)
from functools import partial
from gui_agents.interngui.utils.formatters import JSON_ANSWER_FORMATTER
from gui_agents.interngui.core.mllm import LMMAgent
from gui_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY
import textwrap
import base64
import io
from PIL import Image, ImageDraw



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
    def __init__(self, is_milestone: bool, gen_output: str, summary: str, obs: Dict):
        self.is_milestone = is_milestone
        self.gen_output = gen_output
        self.obs = obs
        self.summary = summary
    


class ReflectionMemoryAgent:
    """
    Reflection Memory Agent (RMA).
    Responsible for maintaining long-term memory, extracting narratives from trajectories,
    providing reflections to the Main Agent, and validating task completion status.
    """
    
    def __init__(self, engine_params: Dict):
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
        """

        self.engine_params = engine_params
        
        self.instruction = None


        self.trajectory: List[StepBehavior] = []
        
        self.reset()

        logger.info(f"ReflectionMemoryAgent initialized with:\n {self.engine_params}")
        

    def reset(self):
        """Reset the code agent state."""
        logger.debug("Resetting CodeAgent state")
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

    def _enhance_observation(self, obs: Dict, coordinates: List, expansion_pixels: int = 400) -> bytes:
        """
        根据给定的坐标点，在截图上绘制标记并裁剪一个“聚焦”区域。

        Args:
            obs (Dict): 包含 'screenshot' 键的观测字典，值为 base64 图像字符串。
            coordinates (List[Tuple[int, int]]): 包含 1 个或 2 个 (x, y) 坐标的列表。
            expansion_pixels (int): 从坐标点或坐标框向外扩展的像素数，用于定义裁剪区域。

        Returns:
            str: 经过标记和裁剪后的新图像的 base64 字符串。
                 如果发生错误或没有坐标，将返回原始（或仅标记）的 base64 图像。
        """
        image_data = obs['screenshot']
        # 使用 io.BytesIO 来打开二进制数据流
        image = Image.open(io.BytesIO(image_data)).convert("RGBA")
        
        draw = ImageDraw.Draw(image)

        img_width, img_height = image.size

        X_MARKER_SIZE = 40   # 'X' 标记的大小（像素）
        X_MARKER_WIDTH = 10   # 标记线条宽度
        
        def _draw_x(draw_context: ImageDraw.ImageDraw, center_x: int, center_y: int, 
            size: int = X_MARKER_SIZE, color: str = "red", width: int = X_MARKER_WIDTH):
            """
            一个辅助函数，用于在给定坐标 (center_x, center_y) 处绘制一个 'X'。
            """
            half_size = size // 2
            # 绘制 '\'
            draw_context.line(
                (center_x - half_size, center_y - half_size,
                center_x + half_size, center_y + half_size),
                fill=color, width=width
            )
            # 绘制 '/'
            draw_context.line(
                (center_x - half_size, center_y + half_size,
                center_x + half_size, center_y - half_size),
                fill=color, width=width
            )

        # --- 2. 根据坐标数量定义裁剪框 (crop_left, crop_top, crop_right, crop_bottom) ---
        
        if len(coordinates) == 2:
            # --- Case 1: 1 个坐标 ---
            x, y = coordinates[0], coordinates[1]
            
            # 2a. 在该点画 'X'
            _draw_x(draw, x, y)
            
            # 2b. 以该点为中心，定义裁剪区域
            crop_left = x - expansion_pixels
            crop_top = y - expansion_pixels
            crop_right = x + expansion_pixels
            crop_bottom = y + expansion_pixels

        else:
            # --- Case 2: 2 个或更多坐标 ---
            # (我们只取前两个)
            x1, y1 = coordinates[0], coordinates[1]
            x2, y2 = coordinates[2], coordinates[3]
            
            # 2a. 在两个点上都画 'X'
            _draw_x(draw, x1, y1, color="red")
            _draw_x(draw, x2, y2, color="blue")

            # 2a. 画一条连接两个中心的绿线
            draw.line(
                (x1, y1, x2, y2),
                fill="green",
                width=5
            )
            
            # 2b. 找到由这两点形成的矩形
            box_left = min(x1, x2)
            box_top = min(y1, y2)
            box_right = max(x1, x2)
            box_bottom = max(y1, y2)
            
            # 2c. 以该矩形为基础向外扩展
            crop_left = box_left - expansion_pixels
            crop_top = box_top - expansion_pixels
            crop_right = box_right + expansion_pixels
            crop_bottom = box_bottom + expansion_pixels

        # --- 3. 安全裁剪 (确保裁剪区域不超出图像边界) ---
        crop_left = max(0, int(crop_left))
        crop_top = max(0, int(crop_top))
        crop_right = min(img_width, int(crop_right))
        crop_bottom = min(img_height, int(crop_bottom))

        # --- 4. 执行裁剪并编码返回 ---
        crop_box = (crop_left, crop_top, crop_right, crop_bottom)
        cropped_image = image.crop(crop_box)

        # 将裁剪后的图像编码回 Base64
        buffered = io.BytesIO()
        cropped_image.save(buffered, format="PNG")
        return buffered.getvalue()

    def _summarize_step_behavior(self, generator_output: str, cur_obs: Dict, enhanced_obs: bytes | None, is_milestone: bool):
        """
        [Interface] Main -> RMA
        The Main Agent (MA) calls this method to "feed" the information of the just-completed step to the RMA.
        RMA will internally process and store this step.
        """

        prev_obs = self.trajectory[-1].obs

        text_content = textwrap.dedent(
            f"""
            Task Description: {self.instruction}
            Generative Agent's Output: {generator_output}
            Current Trajectory below:
            """
        )
        self.behavior_agent.reset()     # don't need history messages
        updated_sys_prompt = (
            self.behavior_agent.system_prompt + "\n" + text_content
        )
        self.behavior_agent.add_system_prompt(updated_sys_prompt)
        self.behavior_agent.add_message(
            text_content="This is the observation before executing action.",
            image_content=prev_obs['screenshot'],
            role="user"
        )
        self.behavior_agent.add_message(
            text_content="This is the enhanced observation, which may help you to identify the operational region.",
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

        response = call_llm_formatted(
            self.behavior_agent,
            format_checkers
        )

        response = call_llm_safe(self.behavior_agent)
        behavior_summary, _ = split_thinking_response(response)

        print("Summary Response: ", response)

        step_behavior = StepBehavior(is_milestone, generator_output, behavior_summary, cur_obs)

        self.trajectory.append(step_behavior)
        return

    def get_reflection(self, cur_obs: Dict, generator_output: str, coordinates: List[Tuple]) -> Tuple[str, str]:
        """
        [Interface] RMA -> Main
        The Main Agent (MA) calls this method to get RMA's reflection before deciding the next action.
        
        Args:
        - current_observation (str): The Main Agent's current observation (o_k).
        
        Returns:
        - full_reflection (str): RMA's reflection. NEED to parse 'thought' in Main Agent.
        """
        logger.info(f"\n--- [Main Agent requesting reflection from RMA] ---")
        
        reflection = ""
        reflection_thought = ""
        if len(self.trajectory) == 0:
            step_behavior = StepBehavior(
                True, 
                "The initial screen is provided. No action has been taken yet.",
                "The initial screen is provided. No action has been taken yet.", 
                cur_obs
            )
            self.trajectory.append(step_behavior)
            
        else: 
            self.reflection_agent.reset()

            for i, step in enumerate(self.trajectory):

                text_content = textwrap.dedent(
                    f"""
                    (Step {i}) action_history:
                    {step.summary}
                    """
                )
                self.reflection_agent.add_message(
                    text_content=text_content,
                    image_content=step.obs['screenshot'] if step.is_milestone else None,
                    role="user",
                )
            
            text_content = textwrap.dedent(
                f"""
                (Latest Step) thought and action:
                {generator_output}
                """
            )
            self.reflection_agent.add_message(
                text_content=text_content,
                image_content=cur_obs['screenshot'],
                role="user",
            )
            
            required_fields = ["is_milestone", "reflection"]
        
            format_checkers = [
                partial(JSON_ANSWER_FORMATTER, required_fields)
            ]

            response = call_llm_formatted(
                self.reflection_agent,
                format_checkers
            )
            print("Reflection Response: \n", response)

            response, reflection_thought = split_thinking_response(response)
            
            data = json.loads(response)
            reflection = data['reflection']
            is_milestone = data["is_milestone"]
            
            if isinstance(is_milestone, str):
                is_milestone = True if "true" in data['is_milestone'].lower() else False
            

            # 图像增强，coordinates可能包含了一个或两个坐标，以他们为中心，向周围外扩一些
            prev_obs = self.trajectory[-1].obs
            enhanced_obs = self._enhance_observation(prev_obs, coordinates) if coordinates else None
            
            if enhanced_obs:        # debug 记得把这段代码和文件夹都删了
                image = Image.open(io.BytesIO(enhanced_obs)).convert("RGBA")
                image.save(f'tmp_enhance_obs/step_{len(self.trajectory)}_enhanced.png')

            self._summarize_step_behavior(generator_output, cur_obs, enhanced_obs, is_milestone)     
        
        return reflection, reflection_thought


    