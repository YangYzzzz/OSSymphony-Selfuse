import gradio as gr
import json
import os
import argparse

# --- 全局常量 ---
# 图片根目录
IMG_ROOT_DIR = "/nvme/yangbowen/jinkaiming/InternGUIFramework/tmp_instruction_img1"
# 原始数据文件路径 (用于首次加载)
DATA_FILE_PATH = "/nvme/yangbowen/yangbowen/OSWorld/gradio/rewritten_instruction.jsonl"
# 修改后保存的目标文件路径
OUTPUT_DATA_FILE_PATH = "/nvme/yangbowen/yangbowen/OSWorld/gradio/rewritten_instruction_refine.jsonl"

# --- 辅助函数 ---

def load_records_from_file(filepath):
    """
    从指定的文件路径读取并解析JSONL数据。
    返回一个记录列表。
    """
    try:
        if not filepath:
            raise ValueError("文件路径不能为空。")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            records = [json.loads(line) for line in f if line.strip()]
        
        if not records:
            raise ValueError("文件为空或格式不正确。")
            
        return records
    except FileNotFoundError:
        raise gr.Error(f"错误：文件未找到 '{filepath}'")
    except json.JSONDecodeError as e:
        raise gr.Error(f"错误：文件内容不是有效的JSONL格式。解析错误: {e}")
    except Exception as e:
        raise gr.Error(f"加载文件时发生未知错误: {e}")

def save_records_to_file(filepath, records):
    """
    将记录列表以JSONL格式写回指定文件。
    这是一个覆盖写操作。
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    except Exception as e:
        raise gr.Error(f"保存文件时发生错误: {e}")

def get_record_data(index, records):
    """
    根据索引从记录列表中获取并格式化单条记录的数据，包括图片路径。
    """
    total_records = len(records)
    if not (records and 0 <= index < total_records):
        return "N/A", "N/A", "", "", "无数据", None

    record = records[index]
    task_id = record.get("task_id", "N/A")
    domain = record.get("domain", "N/A")
    original = record.get("original_instruction", "")
    rewritten = record.get("rewritten_instruction", "")
    progress_text = f"第 {index + 1} / {total_records} 条"
    
    image_path = None
    if task_id != "N/A" and domain != "N/A":
        potential_path = os.path.join(IMG_ROOT_DIR, domain, task_id, "step_1_img.png")
        if os.path.exists(potential_path):
            image_path = potential_path
            
    return task_id, domain, original, rewritten, progress_text, image_path

# --- Gradio 界面逻辑函数 ---

def load_data():
    """
    智能加载数据：优先加载修改后的文件，如果不存在则加载原始文件。
    更新UI以显示第一条记录。
    """
    load_path = ""
    initial_load_message = ""
    
    # --- 修改点 1: 智能加载逻辑 ---
    # 检查输出文件是否存在且不为空，如果存在，则加载它以继续工作
    if os.path.exists(OUTPUT_DATA_FILE_PATH) and os.path.getsize(OUTPUT_DATA_FILE_PATH) > 0:
        load_path = OUTPUT_DATA_FILE_PATH
        initial_load_message = f"**检测到已有的修改文件，已从 '{os.path.basename(OUTPUT_DATA_FILE_PATH)}' 加载。**"
    else:
        # 否则，加载原始文件
        load_path = DATA_FILE_PATH
        initial_load_message = f"**未找到修改文件，已从原始文件 '{os.path.basename(DATA_FILE_PATH)}' 加载。所有修改将保存到新文件中。**"

    records = load_records_from_file(load_path)
    total_records = len(records)
    
    task_id, domain, original, rewritten, progress, image = get_record_data(0, records)
    
    status_message = f"{initial_load_message}\n**成功加载 {total_records} 条记录。**"

    return {
        records_state: records,
        current_index: 0,
        task_id_display: task_id,
        domain_display: domain,
        original_inst: original,
        rewritten_inst: rewritten,
        progress_display: progress,
        image_display: image,
        viewer_group: gr.update(visible=True),
        status_display: gr.update(value=status_message),
        jump_input: gr.update(maximum=total_records)
    }

def navigate(current_index, direction, records):
    """
    处理导航，完全在内存中操作。
    """
    total_records = len(records)
    if not records:
        return current_index, "N/A", "N/A", "", "", "无数据", None

    if direction == "next":
        new_index = min(current_index + 1, total_records - 1)
    elif direction == "prev":
        new_index = max(current_index - 1, 0)
    else:
        new_index = current_index
    
    task_id, domain, original, rewritten, progress, image = get_record_data(new_index, records)
    
    return new_index, task_id, domain, original, rewritten, progress, image

def save_single_record(current_index, records, new_rewritten_text):
    """
    在内存中更新记录，并将整个记录列表保存到新的目标文件中。
    """
    if not records:
        return records, "**错误：没有加载数据，无法保存。**"
    
    # --- 修改点 2: 在内存中更新 ---
    records[current_index]['rewritten_instruction'] = new_rewritten_text
    
    # --- 修改点 3: 保存到新的目标文件 ---
    save_records_to_file(OUTPUT_DATA_FILE_PATH, records)
    
    # 返回更新后的内存记录和成功消息
    success_message = f"**成功：第 {current_index + 1} 条记录已更新并保存到 '{os.path.basename(OUTPUT_DATA_FILE_PATH)}'。**"
    return records, success_message

def jump_to_record(jump_target, records):
    """
    跳转到指定的记录，完全在内存中操作。
    """
    total_records = len(records)
    if not jump_target:
        raise gr.Error("请输入要跳转的条目编号！")

    jump_target = int(jump_target)
    new_index = jump_target - 1

    if not (0 <= new_index < total_records):
        raise gr.Error(f"输入无效！请输入 1 到 {total_records} 之间的数字。")

    task_id, domain, original, rewritten, progress, image = get_record_data(new_index, records)
    
    return new_index, task_id, domain, original, rewritten, progress, image

# --- 构建 Gradio 界面 (UI部分无重大变化) ---

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    
    records_state = gr.State([])
    current_index = gr.State(0)

    gr.Markdown("# 指令对比查看器 (安全保存版)")
    
    load_button = gr.Button("加载数据", variant="primary", scale=1)

    status_display = gr.Markdown("")

    with gr.Column(visible=False) as viewer_group:
        with gr.Row():
            task_id_display = gr.Textbox(label="任务 ID (Task ID)", interactive=False)
            domain_display = gr.Textbox(label="领域 (Domain)", interactive=False)
            progress_display = gr.Textbox(label="进度", interactive=False, scale=0.5)

        with gr.Row():
            with gr.Column(scale=2):
                image_display = gr.Image(label="关联图像", interactive=False)
            with gr.Column(scale=1):
                original_inst = gr.Textbox(label="原始指令", lines=10, interactive=False)
                rewritten_inst = gr.Textbox(label="重写后指令 (可编辑)", lines=10, interactive=True)
                save_button = gr.Button("保存当前修改", variant="primary")
        
        with gr.Row(equal_height=True):
            prev_btn = gr.Button("<< 上一条")
            next_btn = gr.Button("下一条 >>")
            jump_input = gr.Number(label="跳转到第 N 条", precision=0, minimum=1, step=1)
            jump_button = gr.Button("跳转")

    # --- 事件监听器 ---

    load_button.click(
        fn=load_data,
        outputs=[
            records_state, current_index, task_id_display, domain_display,
            original_inst, rewritten_inst, progress_display, image_display,
            viewer_group, status_display, jump_input
        ]
    )

    next_btn.click(
        fn=lambda idx, recs: navigate(idx, "next", recs),
        inputs=[current_index, records_state],
        outputs=[
            current_index, task_id_display, domain_display, original_inst, 
            rewritten_inst, progress_display, image_display
        ]
    )

    prev_btn.click(
        fn=lambda idx, recs: navigate(idx, "prev", recs),
        inputs=[current_index, records_state],
        outputs=[
            current_index, task_id_display, domain_display, original_inst, 
            rewritten_inst, progress_display, image_display
        ]
    )
    
    save_button.click(
        fn=save_single_record,
        inputs=[current_index, records_state, rewritten_inst],
        outputs=[records_state, status_display]
    )

    jump_button.click(
        fn=jump_to_record,
        inputs=[jump_input, records_state],
        outputs=[
            current_index, task_id_display, domain_display, original_inst, 
            rewritten_inst, progress_display, image_display
        ]
    )

# --- 启动 Gradio 应用 ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=10000)
    args = parser.parse_args()
    
    demo.launch(
        server_name="0.0.0.0", 
        server_port=args.port,
        allowed_paths=[IMG_ROOT_DIR]
    )