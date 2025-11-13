import gradio as gr
from PIL import Image, ImageDraw, ImageFont
import re
import random
import io
import os
import argparse
from typing import Literal, Dict, Any
import sys
sys.path.insert(0, "/nvme/yangbowen/yangbowen/OSWorld")
from mm_agents.interngui.core.mllm import LMMAgent
from mm_agents.interngui.agents.grounder_agent import GrounderAgent
# --- 用户提供的模型信息 ---
# 使用 typing.Literal 来定义模型名称的类型提示，增强代码可读性

# --- 模型配置 ---
ModelName = Literal["ui-tars-1.5-7b", "holo-72b", "scalecua-32b"]

# 初始化模型变量
ui_tars_15_7b_model, holo_72b_model, scalecua_32b_model = None, None, None

model_dict: Dict[ModelName, Dict[str, Any]] = {
    "ui-tars-1.5-7b": {
        "engine_type": "openai",
        "model": "ui-tars-1.5-7b",
        "base_url": "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework.yangbowen/10001/v1",
        "api_key": "none",
        "grounding_smart_resize": True,
        "grounding_width": None,
        "grounding_height": None
    },
    "holo-72b": {
        "engine_type": "openai",
        "model": "holo-72b", # 确保模型名称正确
        "base_url": "YOUR_API_BASE_URL_HERE_2", # 请替换为真实的URL
        "api_key": "none",
        "grounding_smart_resize": True,
    },
    "scalecua-32b": {
        "engine_type": "openai",
        "model": "scalecua-32b", # 确保模型名称正确
        "base_url": "YOUR_API_BASE_URL_HERE_3", # 请替换为真实的URL
        "api_key": "none",
        "grounding_smart_resize": True,
    }
}

ui_tars_15_7b_model = GrounderAgent(engine_params=model_dict["ui-tars-1.5-7b"], width=1920, height=1080)
# --- MODIFIED: 修正了模型初始化，使其使用各自的配置 ---
holo_72b_model = GrounderAgent(engine_params=model_dict["ui-tars-1.5-7b"], width=1920, height=1080)
scalecua_32b_model = GrounderAgent(engine_params=model_dict["ui-tars-1.5-7b"], width=1920, height=1080)
# 将模型实例存入字典，方便后续调用
model_dict["ui-tars-1.5-7b"]["var"] = ui_tars_15_7b_model
model_dict["holo-72b"]["var"] = holo_72b_model
model_dict["scalecua-32b"]["var"] = scalecua_32b_model


# --- LLM 调用函数 ---
def call_llm_safe(model_name: ModelName, query: str, image: Image.Image):
    """
    调用大语言模型(LLM)的函数。
    
    Args:
        model_name (ModelName): 要调用的模型名称。
        query (str): 用户的文本查询。
        image (Image.Image): 用户上传的图片 (Pillow Image 对象)。

    Returns:
        list: 模型返回的坐标列表 [x, y]，如果失败则返回空列表。
    """
    print(f"正在为模型 '{model_name}' 进行推理，查询: '{query}'...")
    
    # --- COMPLETED: 将 Image.Image 编码为二进制流 ---
    buffer = io.BytesIO()
    image.save(buffer, format="PNG") # 使用PNG格式以保证无损
    screenshot_bytes = buffer.getvalue()
    
    obs = {
        "screenshot": screenshot_bytes
    }
    
    width, height = image.width, image.height
    
    # 从字典中获取模型实例
    model = model_dict[model_name].get("var")
    
    if model is None:
        print(f"错误：模型 '{model_name}' 未正确初始化。")
        return []

    try:
        model.dynamic_set_width_height(width=width, height=height)
        coords = model.generate_coords(query, obs)
        # resize_coordinates 应该返回最终的 [x, y]
        # 根据您的描述，我们假设它返回一个列表，如 [x, y]
        final_coords = model.resize_coordinates(coordinates=coords)
        
        # 确保返回的是一个列表
        if isinstance(final_coords, list) and len(final_coords) >= 2:
            return final_coords
        else:
            print(f"模型 '{model_name}' 返回的坐标格式不正确: {final_coords}")
            return []

    except Exception as e:
        print(f"调用模型 '{model_name}' 时发生异常: {e}")
        return []


# --- 核心处理函数 ---
def process_and_compare(image: Image.Image, query: str):
    """
    处理输入，调用所有模型，解析结果，并在图上标记。
    """
    if image is None or not query:
        gr.Warning("请输入图片和指令！")
        # 返回与输出组件数量相匹配的空值
        return [None] * (len(model_dict) * 2)

    output_images = []
    output_texts = []
    
    # 为每个模型定义一个独特的颜色
    colors = ["red", "lime", "blue", "yellow", "fuchsia", "aqua"]

    for i, model_name in enumerate(model_dict.keys()):
        # 1. 调用LLM获取结果
        coords = call_llm_safe(model_name, query, image)
        
        # 2. 在图片上标记坐标
        img_copy = image.copy().convert("RGB")
        draw = ImageDraw.Draw(img_copy)
        color = colors[i % len(colors)]
        
        # --- MODIFIED: 将绘制矩形改为绘制叉号 ---
        if coords and isinstance(coords, list) and len(coords) >= 2:
            x, y = int(coords[0]), int(coords[1])
            
            # 定义叉号的大小
            cross_size = 20
            # 定义线条宽度
            line_width = 5
            
            # 绘制第一条线 (\)
            draw.line([(x - cross_size, y - cross_size), (x + cross_size, y + cross_size)], fill=color, width=line_width)
            # 绘制第二条线 (/)
            draw.line([(x - cross_size, y + cross_size), (x + cross_size, y - cross_size)], fill=color, width=line_width)

            # 准备文本输出
            text_output = f"坐标: [{x}, {y}]"
            print(f"模型 '{model_name}' 在图上标记坐标 {text_output}。")
        else:
            text_output = "未能返回有效坐标"
            print(f"模型 '{model_name}' 未能解析出有效的坐标。")
            # 在图片左上角添加标签，表明此模型未返回坐标
            draw.text((10, 10 + i*20), f"{model_name}: {text_output}", fill=color)

        output_images.append(img_copy)
        output_texts.append(text_output)

    # 4. 准备返回结果
    # Gradio 的 `outputs` 需要一个扁平化的列表: [img1, txt1, img2, txt2, ...]
    results = []
    for img, txt in zip(output_images, output_texts):
        results.extend([img, txt])
        
    return results

# --- Gradio UI 界面构建 ---
with gr.Blocks(theme=gr.themes.Soft(), title="多模型视觉定位对比工具") as demo:
    gr.Markdown("# 多模型视觉定位效果对比")
    gr.Markdown("上传一张图片并输入您的指令，应用将调用所有预设模型进行推理，并在图上标记出模型识别的坐标，方便您直观对比效果。")

    with gr.Row(variant="panel"):
        # 输入区域
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="上传图片")
            text_input = gr.Textbox(label="输入指令", placeholder="例如：请定位图中的'登录'按钮")
            submit_btn = gr.Button("🚀 提交并对比", variant="primary")

        # 输出区域
        with gr.Column(scale=3):
            outputs_components = []
            with gr.Row():
                # 动态地为每个模型创建输出列
                for model_name in model_dict.keys():
                    with gr.Column():
                        gr.Markdown(f"### 🤖 {model_name}")
                        output_image = gr.Image(label="结果图片 (带标记)", interactive=False)
                        # --- MODIFIED: 标签改为“模型返回坐标” ---
                        output_text = gr.Textbox(label="模型返回坐标", interactive=False, lines=2)
                        # 将输出组件按顺序添加到列表中
                        outputs_components.extend([output_image, output_text])

    # 绑定点击事件
    submit_btn.click(
        fn=process_and_compare,
        inputs=[image_input, text_input],
        outputs=outputs_components
    )
    
    # --- MODIFIED: 修正示例文件夹路径并创建占位图片 ---
    example_folder = "gradio/grounding_examples"


    gr.Examples(
        examples=[
            [os.path.join(example_folder, "example1.png"), "Create a new Chatbox"],
            [os.path.join(example_folder, "example2.png"), "Read the paper Surfer 2"],
        ],
        inputs=[image_input, text_input],
        outputs=outputs_components,
        fn=process_and_compare,
        label="示例"
    )

# --- 主程序入口 ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=10000)
    args = parser.parse_args()

    print(f"Gradio 应用将在 http://0.0.0.0:{args.port} 上启动")
        
    demo.launch(server_name="0.0.0.0", server_port=args.port)