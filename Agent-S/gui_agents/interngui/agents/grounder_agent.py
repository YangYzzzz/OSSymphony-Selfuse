import re
from typing import Any, Dict, List

import pytesseract
from PIL import Image

from gui_agents.interngui.core.mllm import LMMAgent
from gui_agents.interngui.utils.common_utils import call_llm_safe, smart_resize

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
    def generate_coords(self, ref_expr: str, obs: Dict) -> List[int]:

        # Reset the grounding model state
        self.grounding_model.reset()

        # Configure the context, UI-TARS demo does not use system prompt
        prompt = f"Query:{ref_expr}\nOutput only the coordinate of one point in your response.\n"
        self.grounding_model.add_message(
            text_content=prompt, image_content=obs["screenshot"], put_text_last=True
        )

        # Generate and parse coordinates
        response = call_llm_safe(self.grounding_model)
        # print("RAW GROUNDING MODEL RESPONSE:", response)
        numericals = re.findall(r"\d+", response)
        assert len(numericals) >= 2
        return [int(numericals[0]), int(numericals[1])]
    
    # Resize from grounding model dim into OSWorld dim (1920 * 1080)
    def resize_coordinates(self, coordinates: List[int]) -> List[int]:
        grounding_width = self.engine_params_for_grounder["grounding_width"]
        grounding_height = self.engine_params_for_grounder["grounding_height"]
        grounding_smart_resize = self.engine_params_for_grounder["grounding_smart_resize"]

        # Important：这段逻辑很重要，当不需要smart_resize时，grounding_width/height 代表图像坐标归一化系数，有 1 的(很少有了)，有 1000 的(QWen2.5以前都是1000)
        # 当需要 smart_resize 时, 使用 smart_resize 动态计算归一化系数
        if not grounding_smart_resize:
            return [
                round(coordinates[0] * self.width / grounding_width),
                round(coordinates[1] * self.height / grounding_height),
            ]
        else:
            smart_height, smart_width = smart_resize(self.height, self.width)
            return [
                round(coordinates[0] * self.width / smart_width),
                round(coordinates[1] * self.height / smart_height)
            ]
