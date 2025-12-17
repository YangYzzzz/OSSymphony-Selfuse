import re
from typing import Any, Dict, List

import pytesseract
from PIL import Image
import io
from mm_agents.interngui.core.mllm import LMMAgent
from mm_agents.interngui.utils.common_utils import call_llm_safe, enhance_observation, smart_resize
from mm_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY
import logging

logger = logging.getLogger("desktopenv.agent")

class GrounderAgent:
    """
    专门用于与GUI环境交互的父类, 用于GroundingAgent和VLMSearcherAgent与OS-World GUI操作
    """
    def __init__(self, engine_params: Dict, screen_width: int, screen_height: int):
        print("!!!!", engine_params)
        self.engine_params_for_grounder = engine_params # grounder_params
        system_prompt, self.user_message = PROCEDURAL_MEMORY.construct_grounder_procedural_memory(model_name=engine_params["model"])
        self.grounding_model = LMMAgent(engine_params, system_prompt=system_prompt)
        # 送入Grounder的长宽
        self.width = engine_params['grounding_width']
        self.height = engine_params['grounding_height']
        print(f"[Grounder]: 初始化的长为 {self.width}, 宽为 {self.height}")
        self.zoom_in_time = engine_params.get('grounder_zoom_in_time', 1)
        # 屏幕的长宽
        self.screen_width = screen_width
        self.screen_height = screen_height

    # Given the state and worker's referring expression, use the grounding model to generate (x,y)
    # self.zoom_in_time 不好使, 已废弃
    def generate_coords(self, ref_expr: str, obs: Dict, detail=False, expansion_pixels=400, **kwargs) -> List:
        # zoom_in_time: 增强次数, 若>1, 则在第一次grounding后根据grounding位置裁剪,依此类推,默认为1
        cur_screenshot = obs["screenshot"]
        
        # 存储全局偏移量
        global_offset_x = 0
        global_offset_y = 0
        
        # 用于存储最终计算出的全局坐标
        final_global_x = 0
        final_global_y = 0

        cur_width, cur_height = self.screen_width, self.screen_height
        zoom_in_time = max(1, self.zoom_in_time)
        
        print(f"[Grounder] start to ground in {zoom_in_time} times!")
        for _ in range(zoom_in_time):
            self.grounding_model.reset()

            # Configure the context
            prompt = self.user_message.replace("REF_EXPR", ref_expr)
            if 'claude' in self.engine_params_for_grounder['model']:
                ### 规范一下系统提示词!!!
                self.grounding_model.add_system_prompt("""Please strictly follow the output format: (x1="100", y1="100") """)
                screenshot_image = Image.open(io.BytesIO(cur_screenshot))
                ### Claude 只接受 (1280, 800) 分辨率的图片，Resize the image!!!
                resized_image = screenshot_image.resize((self.width, self.height), Image.Resampling.LANCZOS)
                # Convert back to bytes
                output_buffer = io.BytesIO()
                resized_image.save(output_buffer, format='PNG')
                cur_screenshot = output_buffer.getvalue()
            elif 'Holo' in self.engine_params_for_grounder['model']:
                prompt += """\nPlease strictly follow the output format: (x1="100", y1="100") """
            elif 'gta' in self.engine_params_for_grounder['model']:
                self.grounding_model.add_system_prompt("You are a GUI agent. You are given a task and a screenshot of the screen. You need to perform a series of pyautogui actions to complete the task.")
            
            self.grounding_model.add_message(
                text_content=prompt, image_content=cur_screenshot, put_text_last=True, role="user"
            )

            # Generate and parse coordinates
            response = call_llm_safe(self.grounding_model, temperature=0.05, **kwargs)
            print(f"[Grounder] prompt: {prompt}\nmodel: {self.engine_params_for_grounder['model']}, \nresponse: {response}")

            # 为了测试HOLO，整理代码时需要删掉！Holo基于司马Qwen3-VL微调，会输出思考过程，尽管已经让他只输出一个点的坐标。
            if 'Holo' in self.engine_params_for_grounder['model']:
                if '</think>' in response:
                    response = response.split('</think>')[1]
                print('[Grounder] Holo输出了</think>, 解析后的回答为:', response)

            # 1. 第一优先级：尝试匹配明确带 key 的格式 (x1="...", y1="...", x="...", y="...")
            numericals = re.findall(r'(?:x1|y1|x|y)=["\']?(\d+)["\']?', response)
            # 2. 第二优先级：如果上面没找到坐标，说明格式可能是纯数字或标签内没有 key 例如：<points>653 42</points> 或 [653, 42]
            if len(numericals) < 2:
                # 关键步骤：先将 "x1", "y1", "x2" 等可能导致误判的字符串剔除
                # 这样 <points x1 ...> 中的 '1' 就不会被当成坐标提取出来了
                clean_response = re.sub(r'[xXyY]\d', '', response)
                numericals = re.findall(r'\d+', clean_response)
            assert len(numericals) >= 2
            
            print(f"[Grounder] 匹配到的坐标: {numericals}")

            local_x, local_y = self._resize_coordinates([int(numericals[0]), int(numericals[1])], width=cur_width, height=cur_height)
            
            # 计算当前的全局坐标 = 局部坐标 + 之前的累计偏移
            final_global_x = local_x + global_offset_x
            final_global_y = local_y + global_offset_y


            # 调用 enhance_observation 获取裁剪后的图,偏移量与新图长宽
            cur_screenshot, delta_x, delta_y, cur_width, cur_height = enhance_observation(
                cur_screenshot, [local_x, local_y], expansion_pixels=expansion_pixels, draw=False
            )
            
            # delta_x/y 是本次裁剪框左上角相对于本次输入图片的偏移
            global_offset_x += delta_x
            global_offset_y += delta_y
            # print(f'[Grounder]: g_o_x {global_offset_x}; g_o_y: {global_offset_y}; f_g_x: {final_global_x}; f_g_y: {final_global_y}')

        if detail:
            return [cur_screenshot, global_offset_x, global_offset_y]
        else:
            return [final_global_x, final_global_y]
    
    def dynamic_set_width_height(self, width: int, height: int):
        self.width = width
        self.height = height
        
    # Resize from grounding model dim into OSWorld dim (1920 * 1080)
    def _resize_coordinates(self, coordinates: List[int], width:int, height:int) -> List[int]:
        """
            width, height: 当前真实图像的长宽
            grounding_width, grounding_height: 对于 Grounding模型 而言的长宽(1000分制 or 1280x800)
        """
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
            smart_height, smart_width = smart_resize(height, width)
            return [
                round(coordinates[0] * width / smart_width),
                round(coordinates[1] * height / smart_height)
            ]
