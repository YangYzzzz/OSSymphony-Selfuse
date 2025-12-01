import gradio as gr
from PIL import Image, ImageDraw
import io
import os
import argparse
import csv
import time
import uuid
from typing import Literal, Dict, Any
import sys

sys.path.insert(0, "/nvme/yangbowen/jinkaiming/InternGUIFramework")
from mm_agents.interngui.agents.grounder_agent import GrounderAgent

# --- 配置与初始化 ---
ModelName = Literal["ui-tars-1.5-7b", "holo-72b", "scalecua-32b", "groundnext-7b", "claude-sonnet-4.5"]
example_folder = "gradio/grounding_examples"  # 示例保存路径
log_file = os.path.join(example_folder, "data_log.csv") # 数据日志文件

# 确保目录存在
os.makedirs(example_folder, exist_ok=True)
# 确保日志文件存在
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["image_path", "query"]) # Header

model_dict: Dict[ModelName, Dict[str, Any]] = {
    "ui-tars-1.5-7b": {
        "engine_type": "vllm",
        "model": "ui-tars-1.5-7b",
        "base_url": "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework.yangbowen/10001/v1",
        "api_key": "none",
        "grounding_smart_resize": True,
        "grounding_width": 1920,
        "grounding_height": 1080
    },
    # "holo-72b": {
    #     "engine_type": "vllm",
    #     "model": "Holo1_5_72B", # 确保模型名称正确
    #     "base_url": "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-2wtdb-2960570-worker-0.yangbowen/8001/v1",
    #     "api_key": "none",
    #     "grounding_smart_resize": True,
    #     "grounding_width": None,
    #     "grounding_height": None
    # },
    # "scalecua-32b": {
    #     "engine_type": "vllm",
    #     "model": "ScaleCUA-32B", # 确保模型名称正确
    #     "base_url": "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-2wtdb-2960570-worker-0.yangbowen/8002/v1", # 请替换为真实的URL
    #     "api_key": "none",
    #     "grounding_smart_resize": True,
    #     "grounding_width": None,
    #     "grounding_height": None
    # },
    # "groundnext-7b": {
    #     "engine_type": "vllm",
    #     "model": "GroundNext-7B", # 确保模型名称正确
    #     "base_url": "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-2wtdb-2960570-worker-0.yangbowen/8004/v1", # 请替换为真实的URL
    #     "api_key": "none",
    #     "grounding_smart_resize": True,
    #     "grounding_width": None,
    #     "grounding_height": None
    # },
    "claude-sonnet-4.5": {
        "engine_type": "openai",
        "model": "claude-sonnet-4-5-20250929", # 确保模型名称正确
        "base_url": "https://api.boyuerichdata.opensphereai.com/v1", 
        "api_key": "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D",
        "grounding_smart_resize": False,
        "grounding_width": 1280,
        "grounding_height": 800
    },
}

# 初始化模型
ui_tars_15_7b_model = GrounderAgent(engine_params=model_dict["ui-tars-1.5-7b"], screen_width=1920, screen_height=1080)
# holo_72b_model = GrounderAgent(engine_params=model_dict["holo-72b"], width=1920, height=1080)
# scalecua_32b_model = GrounderAgent(engine_params=model_dict["scalecua-32b"], width=1920, height=1080)
# groundnext_7b_model = GrounderAgent(engine_params=model_dict["groundnext-7b"], width=1920, height=1080)
claude_sonnet_model = GrounderAgent(engine_params=model_dict["claude-sonnet-4.5"], screen_width=1920, screen_height=1080)

model_dict["ui-tars-1.5-7b"]["var"] = ui_tars_15_7b_model
# model_dict["holo-72b"]["var"] = holo_72b_model
# model_dict["scalecua-32b"]["var"] = scalecua_32b_model
# model_dict["groundnext-7b"]["var"] = groundnext_7b_model
model_dict['claude-sonnet-4.5']['var'] = claude_sonnet_model


def save_sample(image: Image.Image, query: str):
    """保存图片和Query到本地"""
    if image is None or not query:
        return

    try:
        # 生成唯一文件名
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        filename = f"sample_{timestamp}_{unique_id}.png"
        file_path = os.path.join(example_folder, filename)
        
        # 保存图片
        image.save(file_path)
        
        # 写入 CSV 日志
        with open(log_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([file_path, query])
            
        print(f"已保存示例: {file_path} | {query}")
    except Exception as e:
        print(f"保存示例失败: {e}")

def load_samples():
    """读取 CSV 返回样本列表，格式符合 gr.Dataset 要求 [[img_path, text], ...]"""
    samples = []
    if os.path.exists(log_file):
        try:
            with open(log_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None) # 跳过标题行
                for row in reader:
                    if len(row) >= 2 and os.path.exists(row[0]):
                        samples.append([row[0], row[1]])
        except Exception as e:
            print(f"读取样本失败: {e}")
    
    # 如果没有样本，提供默认空样本或预设样本，防止报错
    if not samples:
        # 这里可以放你原本的预设样本
        pass 
        
    # 倒序排列，最新的在最前面
    return samples[::-1]


# --- LLM 调用函数 ---
def call_llm_safe(model_name: ModelName, query: str, image: Image.Image, zoom_in_time=1):
    # ... (保持原有逻辑不变) ...
    print(f"正在为模型 '{model_name}' 进行推理...")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    screenshot_bytes = buffer.getvalue()
    obs = {"screenshot": screenshot_bytes}
    width, height = image.width, image.height
    model = model_dict[model_name].get("var")
    assert model
    # try:

    if "claude" not in model_name:
        model.dynamic_set_width_height(width=width, height=height)
    
    final_coords = model.generate_coords(query, obs)
    
    print(f'[Final coords]: {final_coords}')
    if isinstance(final_coords, list) and len(final_coords) >= 2:
        return final_coords
    return []
    # except Exception as e:
    #     print(f"Error {model_name}: {e}")
    #     return []

# --- 核心处理函数 (修改) ---
def process_and_compare_with_save(image: Image.Image, query: str, zoom_in_time: int = 1):
    """
    1. 保存输入数据
    2. 执行推理
    3. 返回推理结果 + 更新后的 Dataset 数据
    """
    if image is None or not query:
        gr.Warning("请输入图片和指令！")
        # 返回空结果 + 不更新 Dataset
        return [None] * (len(model_dict) * 2) + [gr.Dataset.update()]

    # 1. 保存数据 (实时保存)
    save_sample(image, query)

    output_images = []
    output_texts = []
    colors = ["red", "lime", "blue", "yellow", "fuchsia", "aqua"]

    # 2. 执行原有推理逻辑
    for i, model_name in enumerate(model_dict.keys()):
        coords = call_llm_safe(model_name, query, image, zoom_in_time=zoom_in_time)
        
        img_copy = image.copy().convert("RGB")
        draw = ImageDraw.Draw(img_copy)
        color = colors[i % len(colors)]
        
        if coords and isinstance(coords, list) and len(coords) >= 2:
            x, y = int(coords[0]), int(coords[1])
            cross_size = 20
            line_width = 5
            draw.line([(x - cross_size, y - cross_size), (x + cross_size, y + cross_size)], fill=color, width=line_width)
            draw.line([(x - cross_size, y + cross_size), (x + cross_size, y - cross_size)], fill=color, width=line_width)
            text_output = f"坐标: [{x}, {y}]"
        else:
            text_output = "未能返回有效坐标"
            draw.text((10, 10 + i*20), f"{model_name}: {text_output}", fill=color)

        output_images.append(img_copy)
        output_texts.append(text_output)

    results = []
    for img, txt in zip(output_images, output_texts):
        results.extend([img, txt])
    
    # 3. 获取最新的样本列表，用于更新 Dataset
    new_samples = load_samples()
    
    # 将 Dataset 的更新操作添加到返回结果的最后
    results.append(gr.Dataset(samples=new_samples))
        
    return results

# --- Gradio UI 界面构建 ---
with gr.Blocks(theme=gr.themes.Soft(), title="多模型视觉定位对比工具") as demo:
    gr.Markdown("# 多模型视觉定位效果对比")
    gr.Markdown("上传图片并输入指令，系统会自动保存您的输入作为新的示例。")
    
    # 组件定义
    zoomin_time_input = gr.Number(label="ZoomIn次数", value=1, precision=0)
    
    with gr.Row(variant="panel"):
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="上传图片")
            text_input = gr.Textbox(label="输入指令", placeholder="例如：请定位图中的'登录'按钮")
            submit_btn = gr.Button("🚀 提交并对比 (自动保存)", variant="primary")

            # --- 替换 gr.Examples 为 gr.Dataset ---
            gr.Markdown("### 📚 历史示例 (点击加载)")
            # 初始化时加载一次
            initial_samples = load_samples()
            example_dataset = gr.Dataset(
                label="点击下方列表快速测试",
                components=[image_input, text_input], # 指定每列对应哪个输入组件
                samples=initial_samples,
                samples_per_page=5,
                type="values" # 传递值
            )

        with gr.Column(scale=len(model_dict)):
            outputs_components = []
            with gr.Row():
                for model_name in model_dict.keys():
                    with gr.Column():
                        gr.Markdown(f"### 🤖 {model_name}")
                        out_img = gr.Image(label="结果", interactive=False)
                        out_txt = gr.Textbox(label="坐标", interactive=False, lines=2)
                        outputs_components.extend([out_img, out_txt])

    # --- 事件绑定 ---
    
    # 1. 提交按钮逻辑
    # 注意：outputs 列表最后加了一个 example_dataset，用于接收 update
    submit_btn.click(
        fn=process_and_compare_with_save,
        inputs=[image_input, text_input, zoomin_time_input],
        outputs=outputs_components + [example_dataset] 
    )
    
    # 2. Dataset 点击逻辑
    # 点击 Dataset 中的某一行，将其填充回输入框
    def load_example_to_inputs(sample):
        # sample 是一个列表 [image_path, query_text]
        return sample[0], sample[1]

    example_dataset.click(
        fn=load_example_to_inputs,
        inputs=[example_dataset],
        outputs=[image_input, text_input]
    )

# --- 主程序入口 ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=10000)
    args = parser.parse_args()
    print(f"Gradio 应用将在 http://0.0.0.0:{args.port} 上启动")
    demo.launch(server_name="0.0.0.0", server_port=args.port)