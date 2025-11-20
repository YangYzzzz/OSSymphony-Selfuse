import re
from typing import Any, Dict, List

import pytesseract
from PIL import Image

from mm_agents.interngui.core.mllm import LMMAgent
from mm_agents.interngui.utils.common_utils import call_llm_safe, enhance_observation, smart_resize

class GrounderAgent:
    """
    专门用于与GUI环境交互的父类, 用于GroundingAgent和VLMSearcherAgent与OS-World GUI操作
    """
    def __init__(self, engine_params: Dict, width: int, height: int):
        self.engine_params_for_grounder = engine_params # grounder_params
        self.grounding_model = LMMAgent(engine_params)
        self.width = width
        self.height = height

    # Given the state and worker's referring expression, use the grounding model to generate (x,y)
    def generate_coords(self, ref_expr: str, obs: Dict, zoom_in_time=1, detail=False) -> List:
        # zoom_in_time: 增强次数, 若>1, 则在第一次grounding后根据grounding位置裁剪,依此类推,默认为1
        cur_screenshot = obs["screenshot"]
        
        # 存储全局偏移量
        global_offset_x = 0
        global_offset_y = 0
        
        # 用于存储最终计算出的全局坐标
        final_global_x = 0
        final_global_y = 0

        cur_width, cur_height = self.width, self.height
        if zoom_in_time < 1:
            zoom_in_time = 1
            
        for _ in range(zoom_in_time):
            self.grounding_model.reset()

            # Configure the context
            prompt = f"Query:{ref_expr}\nOutput only the coordinate of one point in your response.\n"
            self.grounding_model.add_message(
                text_content=prompt, image_content=cur_screenshot, put_text_last=True
            )

            # Generate and parse coordinates
            response = call_llm_safe(self.grounding_model)
            numericals = re.findall(r"\d+", response)
            local_x, local_y = self._resize_coordinates([int(numericals[0]), int(numericals[1])], width=cur_width, height=cur_height)
            
            # 计算当前的全局坐标 = 局部坐标 + 之前的累计偏移
            final_global_x = local_x + global_offset_x
            final_global_y = local_y + global_offset_y
            
            # 调用 enhance_observation 获取裁剪后的图,偏移量与新图长宽
            cur_screenshot, delta_x, delta_y, cur_width, cur_height = enhance_observation(
                cur_screenshot, [local_x, local_y], expansion_pixels=400, draw=False
            )
            
            # delta_x/y 是本次裁剪框左上角相对于本次输入图片的偏移
            global_offset_x += delta_x
            global_offset_y += delta_y

        if detail:
            return [cur_screenshot, global_offset_x, global_offset_y]
        else:
            return [final_global_x, final_global_y]
    
    def dynamic_set_width_height(self, width: int, height: int):
        self.width = width
        self.height = height
        
    # Resize from grounding model dim into OSWorld dim (1920 * 1080)
    def _resize_coordinates(self, coordinates: List[int], width:int, height:int) -> List[int]:
        grounding_width = self.engine_params_for_grounder["grounding_width"]
        grounding_height = self.engine_params_for_grounder["grounding_height"]
        grounding_smart_resize = self.engine_params_for_grounder["grounding_smart_resize"]

        # Important：这段逻辑很重要，当不需要smart_resize时，grounding_width/height 代表图像坐标归一化系数，有 1 的(很少有了)，有 1000 的(QWen2.5以前都是1000)
        # 当需要 smart_resize 时, 使用 smart_resize 动态计算归一化系数
        if not grounding_smart_resize:
            return [
                round(coordinates[0] * width / grounding_width),
                round(coordinates[1] * height / grounding_height),
            ]
        else:
            smart_height, smart_width = smart_resize(self.height, self.width)
            return [
                round(coordinates[0] * width / smart_width),
                round(coordinates[1] * height / smart_height)
            ]
