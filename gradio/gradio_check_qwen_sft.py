import gradio as gr
import json
import os
import math
from PIL import Image, ImageDraw
from transformers import AutoTokenizer

# 全局 tokenizer，延迟加载
tokenizer = None
MAX_IMAGE_TOKENS_PER_IMAGE = 2500

def get_tokenizer():
    global tokenizer
    if tokenizer is None:
        try:
            # 这里以 Qwen 为例进行 token 计算
            tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-VL-8B-Instruct", trust_remote_code=True)
            print("Tokenizer loaded successfully")
        except Exception as e:
            print(f"Error loading tokenizer: {e}")
    return tokenizer

def count_text_tokens(messages):
    tok = get_tokenizer()
    if not tok:
        return 0

    try:
        full_text = ""
        for msg in messages:
            # 兼容不同的键名 (from/value 或 role/content)
            role = msg.get("from", msg.get("role", "unknown"))
            
            # 角色映射标准化
            if role in ["human", "user"]:
                role = "user"
            elif role in ["gpt", "assistant", "tool_response"]:
                role = "assistant"
            elif role in ["system"]:
                role = "system"
            # tool_call 等其他角色保持原样即可，Qwen 的 ChatML 格式可以兼容任意 role 字符串

            content = msg.get("value", msg.get("content", ""))
            
            # 如果 content 是列表（多模态格式），提取其中的文本
            if isinstance(content, list):
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                    elif isinstance(item, str):
                        text_parts.append(item)
                content = "\n".join(text_parts)
            elif not isinstance(content, str):
                content = str(content)

            # 手动拼接 Qwen 的 ChatML 格式
            # 格式: <|im_start|>role\ncontent<|im_end|>\n
            full_text += f"<|im_start|>{role}\n{content}<|im_end|>\n"
            
        # 加上模型生成的起始符
        full_text += "<|im_start|>assistant\n"

        # 使用 encode 计算，必须加上 allowed_special="all" 否则遇到特殊字符会报错
        tokens = tok.encode(full_text, allowed_special="all")
        return len(tokens)

    except Exception as e:
        print(f"Token counting error: {e}")
        return 0


def count_image_refs(content):
    if isinstance(content, str):
        return content.count("<image>")
    if isinstance(content, list):
        total = 0
        for item in content:
            if isinstance(item, dict):
                item_type = item.get("type")
                if item_type in ["image", "image_url"]:
                    total += 1
                text = item.get("text", "")
                if isinstance(text, str):
                    total += text.count("<image>")
            elif isinstance(item, str):
                total += item.count("<image>")
        return total
    return 0

def find_coordinate(obj):
    if isinstance(obj, dict):
        coord = obj.get("coordinate")
        if isinstance(coord, (list, tuple)) and len(coord) >= 2:
            try:
                return float(coord[0]), float(coord[1])
            except (TypeError, ValueError):
                return None
        for value in obj.values():
            found = find_coordinate(value)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = find_coordinate(item)
            if found is not None:
                return found
    return None

def extract_tool_call_coordinate(content):
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            return None
    return find_coordinate(content)

def get_coordinates_by_image(conversations, image_count):
    coordinates_by_image = {i: [] for i in range(image_count)}
    current_image_idx = -1

    for step in conversations:
        role = step.get("from", step.get("role", "unknown"))
        content = step.get("value", step.get("content", ""))

        image_refs = count_image_refs(content)
        if image_refs:
            current_image_idx = min(image_count - 1, current_image_idx + image_refs)

        if role == "tool_call" and 0 <= current_image_idx < image_count:
            coordinate = extract_tool_call_coordinate(content)
            if coordinate is not None:
                coordinates_by_image[current_image_idx].append(coordinate)

    return coordinates_by_image

def draw_coordinate_crosses(image_path, coordinates):
    with Image.open(image_path) as img:
        marked = img.convert("RGB")

    draw = ImageDraw.Draw(marked)
    width, height = marked.size
    size = max(8, min(width, height) // 50)
    line_width = max(3, size // 4)

    for x_norm, y_norm in coordinates:
        x = round(max(0, min(1000, x_norm)) / 1000 * (width - 1))
        y = round(max(0, min(1000, y_norm)) / 1000 * (height - 1))
        draw.line((x - size, y - size, x + size, y + size), fill="red", width=line_width)
        draw.line((x - size, y + size, x + size, y - size), fill="red", width=line_width)

    return marked

def load_data(file_path):
    if not file_path or not os.path.exists(file_path):
        return [], "找不到文件，请检查路径。"
    
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data.append(json.loads(line))
        return data, f"成功加载 {len(data)} 条样本。"
    except Exception as e:
        return [], f"加载文件时发生错误: {str(e)}"

def calculate_qwen_image_tokens(width: int, height: int, max_tokens: int = 16384) -> int:
    """估算 Qwen-VL 图像对应的 token 数量。"""
    FACTOR = 28  # Qwen-VL 的空间合并因子 (14 * 2)

    max_pixels = max_tokens * (FACTOR ** 2)
    current_pixels = width * height

    if current_pixels > max_pixels:
        scale = math.sqrt(max_pixels / current_pixels)
        new_width = width * scale
        new_height = height * scale
    else:
        new_width = width
        new_height = height

    aligned_width = max(FACTOR, round(new_width / FACTOR) * FACTOR)
    aligned_height = max(FACTOR, round(new_height / FACTOR) * FACTOR)

    tokens = (aligned_width // FACTOR) * (aligned_height // FACTOR)
    return tokens


def estimate_image_tokens_by_size(path):
    try:
        with Image.open(path) as img:
            w, h = img.size
        return min(
            calculate_qwen_image_tokens(w, h, max_tokens=MAX_IMAGE_TOKENS_PER_IMAGE),
            MAX_IMAGE_TOKENS_PER_IMAGE,
        )
    except Exception as e:
        print(f"Open image failed for {path}: {e}")
        return MAX_IMAGE_TOKENS_PER_IMAGE

def format_sample(sample_idx, data):
    if not data or sample_idx >= len(data):
        return "数据为空或索引无效", [], 0

    sample = data[sample_idx]

    # 处理图片
    images = []
    img_paths = sample.get("images", sample.get("image", []))
    if isinstance(img_paths, str):
        img_paths = [img_paths]

    for path in img_paths:
        # 使用你真实的图片根目录，保持不变
        if not path.startswith("/"):
            path = os.path.join("/nvme/yangbowen/yangbowen/OSSymphony/qwen3vl_sft_dataset/image", path)  # 已按你的真实图片根目录配置
        print(f'path: {path}')
        if os.path.exists(path):
            images.append(path)
            
    conversations = sample.get("conversations", [])
    if not conversations and "messages" in sample:
        conversations = sample["messages"]

    coordinates_by_image = get_coordinates_by_image(conversations, len(images))
    display_images = []
    for idx, path in enumerate(images):
        coordinates = coordinates_by_image.get(idx, [])
        if coordinates:
            display_images.append(draw_coordinate_crosses(path, coordinates))
        else:
            display_images.append(path)

    # 计算图片 token
    try:
        image_token_count = 0
        for p in images:
            try:
                with Image.open(p) as img:
                    w, h = img.size
            except Exception as e:
                print(f"Open image failed for {p}: {e}")
                image_token_count += MAX_IMAGE_TOKENS_PER_IMAGE
                continue

            image_token_count += min(
                calculate_qwen_image_tokens(w, h, max_tokens=MAX_IMAGE_TOKENS_PER_IMAGE),
                MAX_IMAGE_TOKENS_PER_IMAGE,
            )
    except Exception as e:
        print(f"Image token estimation error: {e}")
        image_token_count = len(images) * MAX_IMAGE_TOKENS_PER_IMAGE

    # 格式化对话
    conv_html = "<div style='display: flex; flex-direction: column; gap: 15px;'>"

    # 计算 Token
    text_token_count = count_text_tokens(conversations)
    token_count = text_token_count + image_token_count

    token_info = f"文本 Tokens: {text_token_count:,} + 图像 Tokens: {image_token_count:,} = 总 Tokens: {token_count:,}"

    # 高亮大 token 数量的数据
    if token_count > 50000:
        token_warning = f"<div style='background-color: #fff1f0; border: 1px solid #ffa39e; color: #cf1322; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-weight: bold; font-size: 1.1em;'>⚠️ 警告: 该数据包含超大 Token 数量 ({token_info})</div>"
    else:
        token_warning = f"<div style='background-color: #f6ffed; border: 1px solid #b7eb8f; color: #389e0d; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-weight: bold;'>{token_info}</div>"

    conv_html += token_warning

    for i, step in enumerate(conversations):
        role = step.get("from", step.get("role", "unknown"))
        content = step.get("value", step.get("content", ""))

        # 根据角色应用不同样式
        if role in ["human", "user", "tool_response"]:
            bg_color = "#e6f7ff"
            border_color = "#91d5ff"
            align = "flex-start"
            role_display = role
        elif role in ["gpt", "assistant", "tool_call"]:
            bg_color = "#f6ffed"
            border_color = "#b7eb8f"
            align = "flex-end"
            role_display = role
        elif role in ["system"]:
            bg_color = "#fffbe6"
            border_color = "#ffe58f"
            align = "center"
            role_display = "System"
        else:
            bg_color = "#f5f5f5"
            border_color = "#d9d9d9"
            align = "flex-start"
            role_display = role.capitalize()

        content_html = content.replace('\n', '<br>')

        step_html = f"""
        <div style='align-self: {align}; max-width: 80%; border: 1px solid {border_color}; border-radius: 8px; padding: 10px; background-color: {bg_color};'>
            <div style='font-weight: bold; margin-bottom: 5px; color: #555;'>第 {i+1} 步: {role_display}</div>
            <div style='word-wrap: break-word;'>{content_html}</div>
        </div>
        """
        conv_html += step_html

    conv_html += "</div>"

    return conv_html, display_images, token_count, text_token_count, image_token_count

def update_view(file_path, sample_idx):
    data, msg = load_data(file_path)
    if not data:
        return msg, "", gr.update(maximum=1, value=0), []

    sample_idx = min(max(0, int(sample_idx)), len(data) - 1)

    conv_html, images, token_count, text_token_count, image_token_count = format_sample(sample_idx, data)

    status = f"加载了 {len(data)} 条样本。正在显示第 {sample_idx + 1} 条 | 总Tokens: {token_count:,} (文字: {text_token_count:,}, 图像: {image_token_count:,})"

    return status, conv_html, gr.update(maximum=max(1, len(data)-1), value=sample_idx), images

def filter_large_tokens(file_path, current_idx, min_tokens):
    data, msg = load_data(file_path)
    if not data:
        return msg, "", gr.update(maximum=1, value=0), []
        
    # 从当前索引的下一个开始查找
    start_idx = int(current_idx) + 1 if int(current_idx) < len(data) - 1 else 0
    
    # 循环查找满足条件的样本
    for i in range(start_idx, len(data)):
        sample = data[i]
        convs = sample.get("conversations", sample.get("messages", []))

        img_paths = sample.get("images", sample.get("image", []))
        if isinstance(img_paths, str):
            img_paths = [img_paths]
        image_token_count = 0
        for path in img_paths:
            # 使用你真实的图片根目录，保持不变
            if not path.startswith("/"):
                path = os.path.join("/nvme/yangbowen/yangbowen/OSSymphony/qwen3vl_sft_dataset/image", path)
            if os.path.exists(path):
                image_token_count += estimate_image_tokens_by_size(path)

        tc = count_text_tokens(convs) + image_token_count
        if tc >= min_tokens:
            return update_view(file_path, i)

    # 如果没找到，从头再找一遍到当前位置
    for i in range(0, start_idx):
        sample = data[i]
        convs = sample.get("conversations", sample.get("messages", []))

        img_paths = sample.get("images", sample.get("image", []))
        if isinstance(img_paths, str):
            img_paths = [img_paths]
        image_token_count = 0
        for path in img_paths:
            # 使用你真实的图片根目录，保持不变
            if not path.startswith("/"):
                path = os.path.join("/nvme/yangbowen/yangbowen/OSSymphony/qwen3vl_sft_dataset/image", path)
            if os.path.exists(path):
                image_token_count += estimate_image_tokens_by_size(path)

        tc = count_text_tokens(convs) + image_token_count
        if tc >= min_tokens:
            return update_view(file_path, i)
            
    status = f"未找到 Token 数大于 {min_tokens} 的样本。"
    # 保持原样
    conv_html, images, _, _, _ = format_sample(int(current_idx), data)
    return status, conv_html, gr.update(value=int(current_idx)), images

with gr.Blocks(title="SFT Dataset Viewer & Token Analyzer", theme=gr.themes.Default()) as demo:
    gr.Markdown("# 🚀 SFT Dataset Viewer & Token Analyzer")
    gr.Markdown("用于可视化 SFT 数据的每一步交互（支持图文），并统计 Token 数。使用 Qwen3VL 的 tokenizer 结合 chat template 进行精准估算。")
    
    with gr.Row():
        with gr.Column(scale=4):
            file_input = gr.Textbox(label="SFT JSONL 文件路径", placeholder="例如: /path/to/dataset.jsonl", value="/nvme/yangbowen/yangbowen/OSSymphony/qwen3vl_sft_dataset/meta/meta_os-caliber-claude-opus-4-6-with-code-1000-ybw-0407_easy.jsonl")
        with gr.Column(scale=1, min_width=100):
            load_btn = gr.Button("加载数据", variant="primary")
            
    status_text = gr.Markdown("状态: 等待加载文件...")
    
    with gr.Row(variant="panel"):
        with gr.Column(scale=3):
            sample_slider = gr.Slider(minimum=0, maximum=100, step=1, value=0, label="样本序号控制")
        with gr.Column(scale=1, min_width=150):
            with gr.Row():
                prev_btn = gr.Button("⬅️ 上一条")
                next_btn = gr.Button("下一条 ➡️")
                
    with gr.Row(variant="panel"):
        with gr.Column(scale=1):
            min_tokens_input = gr.Number(label="筛选阈值 (Token数大于)", value=50000, step=1000)
        with gr.Column(scale=1):
            filter_btn = gr.Button("🔍 查找下一个长文本数据", variant="stop")
            
    with gr.Row():
        with gr.Column(scale=2):
            conversation_output = gr.HTML(label="多轮对话内容", value="<div style='text-align:center; padding: 20px; color:#999;'>数据加载后在此处显示</div>")
        with gr.Column(scale=1):
            images_output = gr.Gallery(label="图像", columns=1, height="auto")
            
    # 绑定事件
    def on_load(file_path):
        return update_view(file_path, 0)
        
    def on_slide(file_path, idx):
        return update_view(file_path, idx)
        
    def go_prev(file_path, idx):
        return update_view(file_path, max(0, int(idx) - 1))
        
    def go_next(file_path, idx):
        return update_view(file_path, int(idx) + 1)
        
    def on_filter(file_path, current_idx, min_tok):
        # UI 可能在查找期间会卡住，提示用户
        return filter_large_tokens(file_path, current_idx, min_tok)
        
    load_btn.click(on_load, inputs=[file_input], outputs=[status_text, conversation_output, sample_slider, images_output])
    sample_slider.release(on_slide, inputs=[file_input, sample_slider], outputs=[status_text, conversation_output, sample_slider, images_output])
    prev_btn.click(go_prev, inputs=[file_input, sample_slider], outputs=[status_text, conversation_output, sample_slider, images_output])
    next_btn.click(go_next, inputs=[file_input, sample_slider], outputs=[status_text, conversation_output, sample_slider, images_output])
    filter_btn.click(on_filter, inputs=[file_input, sample_slider, min_tokens_input], outputs=[status_text, conversation_output, sample_slider, images_output])

if __name__ == "__main__":
    # 为了避免下载问题，确保设置了必要的环境变量，如果在有网环境下可不加
    import os
    # 启动前加载一下 Tokenizer，以避免第一次查询卡顿
    print("Initializing Viewer...")
    get_tokenizer()
    demo.launch(server_name="0.0.0.0", server_port=20000)
