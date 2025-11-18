import gradio as gr
import json
import os

# --- 全局常量 ---
# 您指定的图片根目录
IMG_ROOT_DIR = "/nvme/yangbowen/jinkaiming/InternGUIFramework/tmp_instruction_img1"

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

def get_record_data(index, records):
    """
    根据索引从记录列表中获取并格式化单条记录的数据，包括图片路径。
    """
    total_records = len(records)
    if not (records and 0 <= index < total_records):
        # 如果没有数据或索引无效，返回所有字段的默认空值
        return "N/A", "N/A", "", "", "无数据", None

    record = records[index]
    task_id = record.get("task_id", "N/A")
    domain = record.get("domain", "N/A")
    original = record.get("original_instruction", "")
    rewritten = record.get("rewritten_instruction", "")
    progress_text = f"第 {index + 1} / {total_records} 条"
    
    # --- 新增：构造并验证图片路径 ---
    image_path = None
    if task_id != "N/A" and domain != "N/A":
        # 构造预期的图片路径
        potential_path = os.path.join(IMG_ROOT_DIR, domain, task_id, "step_1_img.png")
        # 检查文件是否存在
        if os.path.exists(potential_path):
            image_path = potential_path
            
    return task_id, domain, original, rewritten, progress_text, image_path

# --- Gradio 界面逻辑函数 ---

def load_data():
    """
    当用户点击“加载数据”按钮时触发。
    加载数据并更新UI显示第一条记录及其图片。
    """
    filepath = "/nvme/yangbowen/yangbowen/OSWorld/gradio/rewritten_instruction.jsonl"
    records = load_records_from_file(filepath)
    total_records = len(records)
    
    # 获取第一条记录的数据（包括图片路径）
    task_id, domain, original, rewritten, progress, image = get_record_data(0, records)
    
    # 返回更新后的状态和UI组件的值
    return {
        records_state: records,
        current_index: 0,
        task_id_display: task_id,
        domain_display: domain,
        original_inst: original,
        rewritten_inst: rewritten,
        progress_display: progress,
        image_display: image, # 更新图片组件
        viewer_group: gr.update(visible=True), # 显示主视图
        status_display: gr.update(value=f"**成功加载 {total_records} 条记录。**")
    }

def navigate(current_index, direction, records):
    """
    处理“上一条”和“下一条”的导航逻辑。
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
    
    # 获取新记录的数据（包括图片路径）
    task_id, domain, original, rewritten, progress, image = get_record_data(new_index, records)
    
    # 返回新的索引和该索引对应的数据
    return new_index, task_id, domain, original, rewritten, progress, image

# --- 构建 Gradio 界面 ---

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    
    # 状态变量，用于在会话中存储数据
    records_state = gr.State([])
    current_index = gr.State(0)

    # 界面布局
    gr.Markdown("# 指令对比查看器 (含图片)")
    
    load_button = gr.Button("加载数据", variant="primary", scale=1)

    status_display = gr.Markdown("")

    # 将主要浏览区域放入一个组，以便整体控制其可见性
    with gr.Column(visible=False) as viewer_group:
        with gr.Row():
            task_id_display = gr.Textbox(label="任务 ID (Task ID)", interactive=False)
            domain_display = gr.Textbox(label="领域 (Domain)", interactive=False)
            progress_display = gr.Textbox(label="进度", interactive=False, scale=0.5)

        with gr.Row():
            with gr.Column(scale=2):
            # 新增的图片显示组件
                image_display = gr.Image(label="关联图像 (Associated Image)", interactive=False)
            with gr.Column(scale=1):
                with gr.Column():
                    original_inst = gr.Textbox(
                        label="原始指令 (Original Instruction)", 
                        lines=10, 
                        interactive=False
                    )
                    rewritten_inst = gr.Textbox(
                        label="重写后指令 (Rewritten Instruction)", 
                        lines=10, 
                        interactive=False
                    )
        
        with gr.Row():
            prev_btn = gr.Button("<< 上一条")
            next_btn = gr.Button("下一条 >>")

    # --- 事件监听器 ---

    # 点击“加载数据”按钮
    load_button.click(
        fn=load_data,
        outputs=[
            records_state, current_index, task_id_display, domain_display,
            original_inst, rewritten_inst, progress_display, image_display,
            viewer_group, status_display
        ]
    )

    # 点击“下一条”按钮
    next_btn.click(
        fn=lambda idx, recs: navigate(idx, "next", recs),
        inputs=[current_index, records_state],
        outputs=[
            current_index, task_id_display, domain_display, original_inst, 
            rewritten_inst, progress_display, image_display
        ]
    )

    # 点击“上一条”按钮
    prev_btn.click(
        fn=lambda idx, recs: navigate(idx, "prev", recs),
        inputs=[current_index, records_state],
        outputs=[
            current_index, task_id_display, domain_display, original_inst, 
            rewritten_inst, progress_display, image_display
        ]
    )

# --- 启动 Gradio 应用 ---
import argparse
if __name__ == "__main__":
    # 添加了 os 模块的导入
    import os
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=10000)
    args = parser.parse_args()
    
    # --- 关键修改在这里 ---
    # 使用 allowed_paths 参数将图片根目录声明为可信路径
    demo.launch(
        server_name="0.0.0.0", 
        server_port=args.port,
        allowed_paths=[IMG_ROOT_DIR]  # 将您的图片根目录添加到允许列表中
    )