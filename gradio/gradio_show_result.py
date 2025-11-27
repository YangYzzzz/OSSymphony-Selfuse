from typing import Literal
import gradio as gr
import os
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random
import shutil
import matplotlib.pyplot as plt
from collections import Counter
import re
import numpy as np

# ==============================================================================
# Gradio 应用核心逻辑
# ==============================================================================

MAX_BUTTONS = 100 # 预先定义UI中支持的最大按钮数量（适用于domain和task）

def get_domains(root_dir):
    """获取根目录下的所有domain目录"""
    if not os.path.isdir(root_dir):
        return []
    return [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

def _get_result_status(result_file):
    """
    一个内部辅助函数，用于读取result.txt并返回一个状态码。
    返回: 1 (成功), 0 (失败), -1 (未知)
    """
    if not result_file.exists():
        return -1
    try:
        result_num = float(result_file.read_text().strip())
        if result_num > 0:
            return 1
        elif result_num == 0:
            return 0
    except (ValueError, TypeError):
        return -1
    return -1

def _read_result_value(result_file):
    """读取具体的result数值，用于显示"""
    if not result_file.exists():
        return "未知"
    try:
        return result_file.read_text().strip()
    except:
        return "Error"

def _get_best_task_result(root_dir, domain, task_name, merge_dirs):
    """
    核心逻辑：在 Base 路径和所有 Merge 路径中，为指定任务寻找最优结果。
    返回: (best_status, best_root, best_result_str)
    """
    candidate_roots = [root_dir]
    if merge_dirs:
        candidate_roots.extend(merge_dirs)

    best_status = -2 
    best_root = root_dir
    best_result_str = "0.0"

    for r_dir in candidate_roots:
        current_task_path = Path(r_dir) / domain / task_name
        if not current_task_path.exists():
            continue
        
        res_file = current_task_path / "result.txt"
        status = _get_result_status(res_file)
        
        # 简单的打擂台逻辑：成功(1) > 失败(0) > 未知(-1)
        if status > best_status:
            best_status = status
            best_root = r_dir
            best_result_str = _read_result_value(res_file)
        elif status == best_status and status == 1:
            # 如果都是成功，数值大的优先
            try:
                curr_val = float(_read_result_value(res_file))
                best_val = float(best_result_str)
                if curr_val > best_val:
                    best_root = r_dir
                    best_result_str = str(curr_val)
            except:
                pass
    
    return best_status, best_root, best_result_str

def calculate_global_stats(root_dir, merge_dirs=None):
    """
    计算全局统计信息（遍历所有Domain）。
    用于在 Domain 选择界面展示。
    """
    domains = get_domains(root_dir)
    total_tasks = 0
    total_success = 0
    
    for domain in domains:
        domain_path = os.path.join(root_dir, domain)
        tasks = [t for t in os.listdir(domain_path) if os.path.isdir(os.path.join(domain_path, t))]
        
        for task in tasks:
            total_tasks += 1
            status, _, _ = _get_best_task_result(root_dir, domain, task, merge_dirs)
            if status == 1:
                total_success += 1
                
    if total_tasks == 0:
        return "### 📊 全局统计: 暂无任务数据"
    
    success_rate = (total_success / total_tasks) * 100
    stats_text = f"### 🌍 全局任务成功率: {success_rate:.2f}% ({total_success}/{total_tasks})"
    if merge_dirs:
        stats_text += f" <span style='font-size:0.8em; color:gray'>(合并模式已开启, 共合并 {len(merge_dirs)+1} 个路径)</span>"
    return stats_text


def get_tasks_merged(root_dir, domain, compare_dir=None, merge_dirs=None):
    """
    获取指定domain下的所有task，支持合并模式和对比模式。
    
    逻辑：
    1. 以 root_dir (Base) 中的任务列表为基准。
    2. 如果启用 merge_dirs，则在 Base 和所有 Merge 路径中寻找该任务的最优结果。
    3. 统计合并后的成功率。
    4. 如果启用 compare_dir，将 (步骤2中的最优结果) 与 Compare 路径的结果进行对比。
    
    返回: 
    - task_name_list
    - success_list (显示的文字)
    - css_class_list (样式)
    - task_source_map (字典: {task_name: best_path_root}) -> 用于点击任务时知道去哪里加载
    - stats_text (统计信息的Markdown文本)
    """
    domain_path = os.path.join(root_dir, domain)
    if not os.path.isdir(domain_path):
        return [], [], [], {}, ""
    
    # 以当前启动路径的任务为基准
    task_name_list = [t for t in os.listdir(domain_path) if os.path.isdir(os.path.join(domain_path, t))]
    task_name_list.sort() # 排序一下比较好看

    success_list = []
    css_class_list = []
    task_source_map = {} # 记录每个任务应该从哪个根目录加载
    
    # 统计变量
    total_tasks = 0
    merged_success_count = 0

    # 准备待检查的路径列表: [Base, Merge1, Merge2, ...]
    candidate_roots = [root_dir]
    if merge_dirs:
        candidate_roots.extend(merge_dirs)

    for task_name in task_name_list:
        total_tasks += 1
        
        # --- 1. 合并逻辑：寻找最优结果 ---
        best_status = -2 # 初始化一个很低的状态
        best_root = root_dir
        best_result_str = "0.0"
        
        # 遍历所有候选路径，找分最高的
        for r_dir in candidate_roots:
            # 检查该路径下是否存在此任务
            current_task_path = Path(r_dir) / domain / task_name
            if not current_task_path.exists():
                continue
            
            res_file = current_task_path / "result.txt"
            status = _get_result_status(res_file)
            
            # 简单的打擂台逻辑：成功(1) > 失败(0) > 未知(-1)
            # 如果状态更好，或者状态一样但之前的是默认路径而现在是新路径(可选)，则更新
            if status > best_status:
                best_status = status
                best_root = r_dir
                best_result_str = _read_result_value(res_file)
            elif status == best_status and status == 1:
                # 如果都是成功，数值大的优先 (例如 0.8 vs 1.0)
                try:
                    curr_val = float(_read_result_value(res_file))
                    best_val = float(best_result_str)
                    if curr_val > best_val:
                        best_root = r_dir
                        best_result_str = str(curr_val)
                except:
                    pass

        # 记录这个任务的最优源路径
        task_source_map[task_name] = best_root
        
        # 统计成功数
        if best_status == 1:
            merged_success_count += 1

        # 生成显示的文字
        display_text = "未知"
        if best_status == 1:
            display_text = f'✅成功 {best_result_str}✅'
        elif best_status == 0:
            display_text = '❌失败 0.0❌'
        
        # 如果最优解来自合并路径，可以在文字上做个标记(可选)，这里暂不加，保持简洁
        success_list.append(display_text)

        # --- 2. 对比逻辑 ---
        # 使用 "最优结果(best_status)" 去和 "对比路径结果" 比较
        current_css_class = ""
        
        # 检查 Search 标记 (优先检查最优路径下的 search.txt)
        search_flag_file = Path(best_root) / domain / task_name / "search.txt"
        is_search = search_flag_file.exists() and int(search_flag_file.read_text().strip()) == 1
        code_flag_file = Path(best_root) / domain / task_name / "code.txt"
        is_code = code_flag_file.exists() and int(code_flag_file.read_text().strip()) == 1
        
        if compare_dir and os.path.isdir(compare_dir):
            compare_result_file = Path(compare_dir) / domain / task_name / "result.txt"
            compare_status = _get_result_status(compare_result_file)
            
            # 应用颜色规则
            if best_status == 1 and compare_status == 0:
                current_css_class = "compare-main-win" # 赢 (合并后的结果赢)
            elif best_status == 0 and compare_status == 1:
                current_css_class = "compare-comp-win" # 输
        
        # 叠加 Search 样式
        if is_search and not is_code:
            if best_status == 1:
                current_css_class += " search-and-success"
            else:
                current_css_class += " search-and-failure"

        if is_code and not is_search:
            if best_status == 1:
                current_css_class += " code-and-success"
            else:
                current_css_class += " code-and-failure"
        if is_code and is_search:
            if best_status == 1:
                current_css_class += " code-and-search-success"
            else:
                current_css_class += " code-and-search-failure"
        css_class_list.append(current_css_class)

    # 生成统计文本
    if total_tasks > 0:
        success_rate = (merged_success_count / total_tasks) * 100
        stats_text = f"### 🏆 当前展示任务成功率: {success_rate:.2f}% ({merged_success_count}/{total_tasks})"
        if merge_dirs:
            stats_text += " <span style='font-size:0.8em; color:gray'>(已应用合并模式)</span>"
    else:
        stats_text = "### 暂无任务数据"

    return task_name_list, success_list, css_class_list, task_source_map, stats_text

def load_task_data(root_dir, domain, task):
    """加载一个任务的所有步骤数据和结果"""
    # 注意：这里的 root_dir 应该是 task_source_map 中记录的那个最优路径
    task_path = Path(root_dir) / domain / task
    
    # 加载 traj.jsonl
    steps = []
    traj_file = task_path / "traj.jsonl"
    if traj_file.exists():
        with open(traj_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    steps.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    print(f"警告: 在 {traj_file} 中发现无效的JSON行")

    # 加载 result.txt
    result_file = task_path / "result.txt"
    result_text = "未知"
    if result_file.exists():
        result_num = float(result_file.read_text().strip())
        if result_num > 0:
            result_text = f'<span class="success-text">成功 {result_num}</span>'
        elif result_num == 0:
            result_text = '<span class="failure-text">失败 0.0</span>'
    
    instruction = "无指令"
    if steps and "instruction" in steps[0]:
        instruction = steps[0]["instruction"]
        
    return steps, result_text, instruction

def process_code_agent_output(code_agent_output):
    """
    处理 code_agent_output 字典，提取字段并合并历史记录。
    返回提取的数据和可见性标志。
    """
    if not code_agent_output or not isinstance(code_agent_output, dict):
        # 如果没有数据，返回空值和 False（不可见）
        return "N/A", "N/A", "N/A", "[]", False

    task_instruction = code_agent_output.get("task_instruction", "N/A")
    completion_reason = code_agent_output.get("completion_reason", "N/A")
    summary = code_agent_output.get("summary", "N/A")
    
    exec_history = code_agent_output.get("execution_history", [])
    result_history = code_agent_output.get("execution_result_history", [])

    # 为了高效合并，创建一个以 step 为键的结果字典
    results_map = {item.get('step'): item.get('result') for item in result_history if 'step' in item}

    combined_history = []
    if isinstance(exec_history, list):
        for step_action in exec_history:
            step_num = step_action.get("step")
            # 将 action 和 result 合并到同一个对象中
            combined_step = {
                "step": step_num,
                "thoughts": step_action.get("thoughts", "N/A"),
                "action": step_action.get("action", "N/A"),
                "result": results_map.get(step_num, "Result not found for this step.")
            }
            combined_history.append(combined_step)
    
    # 将合并后的列表转换为格式化的JSON字符串
    history_json = json.dumps(combined_history, indent=2)

    # 返回所有处理好的数据和 True（可见）
    return task_instruction, completion_reason, summary, history_json, True

def create_gradio_app(root_dir):
    """创建并返回Gradio应用"""
    
    domains = get_domains(root_dir)
    
    # 初始计算一次全局统计
    initial_global_stats = calculate_global_stats(root_dir, merge_dirs=None)

    CUSTOM_CSS = """
        .gr-button-group { display: flex; flex-wrap: wrap; gap: 10px; }
        .gr-button-group > button { flex-grow: 1; }
        .success-text { color: #28a745; font-weight: bold; }
        .failure-text { color: #dc3545; font-weight: bold; }
        #screenshot-container.milestone .gradio-label {
            color: red !important;
            font-weight: bold !important;
        }
        .compare-main-win {
            background: #d4edda !important; 
            border-color: #c3e6cb !important;
        }
        .compare-comp-win {
            background: #f8d7da !important; 
            border-color: #f5c6cb !important;
        }
        .search-and-success::before {
            content: 'search';
            background-image: linear-gradient(to bottom, #2ecc71, #28a745);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 8px;
            display: inline-block;
            vertical-align: middle;
            border: 1px solid #1e7e34;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }
        .search-and-failure::before {
            content: 'search';
            background-image: linear-gradient(to bottom, #e74c3c, #dc3545);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 8px;
            display: inline-block;
            vertical-align: middle;
            border: 1px solid #b21f2d;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }
        .code-and-success::before {
            content: 'code';
            background-image: linear-gradient(to bottom, #2ecc71, #28a745);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 8px;
            display: inline-block;
            vertical-align: middle;
            border: 1px solid #1e7e34;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }
        .code-and-failure::before {
            content: 'code';
            background-image: linear-gradient(to bottom, #e74c3c, #dc3545);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 8px;
            display: inline-block;
            vertical-align: middle;
            border: 1px solid #b21f2d;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }
        .code-and-search-success::before {
            content: 'code & search';
            background-image: linear-gradient(to bottom, #2ecc71, #28a745);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 8px;
            display: inline-block;
            vertical-align: middle;
            border: 1px solid #1e7e34;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }
        .code-and-search-failure::before {
            content: 'code & search';
            background-image: linear-gradient(to bottom, #e74c3c, #dc3545);
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 8px;
            display: inline-block;
            vertical-align: middle;
            border: 1px solid #b21f2d;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }
        .stats-header h3 {
            font-size: 1.5rem !important;
            color: #333;
            margin-bottom: 0.5rem;
        }
    """

    with gr.Blocks(theme=gr.themes.Soft(), css=CUSTOM_CSS) as app:
        # --- 状态存储 ---
        state_root_dir = gr.State(root_dir)
        state_compare_root_dir = gr.State(None)
        state_merge_paths = gr.State([])
        
        state_selected_domain = gr.State()
        state_selected_task = gr.State()
        state_task_source_map = gr.State({}) 
        state_current_viewing_root = gr.State(root_dir)
        
        state_steps_data = gr.State()
        state_current_step_index = gr.State(0)

        # --- 视图1: Domain选择 ---
        with gr.Column(visible=True) as domain_view:
            gr.Markdown(f"# 任务轨迹浏览器({os.path.basename(root_dir)})\n")
            
            # 1. Domain 界面显示全局统计
            global_stats_display = gr.Markdown(initial_global_stats, elem_classes="stats-header")

            with gr.Accordion("🛠️ 高级设置 (对比 & 合并)", open=False):
                with gr.Tab("📊 对比模式"):
                    compare_path_input = gr.Textbox(
                        label="输入对比结果路径", 
                        placeholder="/path/to/another/result",
                        info="输入另一个实验结果的根目录，然后点击开启对比。"
                    )
                    compare_toggle_btn = gr.Button("🚀 开启/更新 对比模式")
                    compare_status_text = gr.Markdown("", visible=False)
                
                with gr.Tab("🔗 合并模式"):
                    merge_paths_input = gr.Textbox(
                        label="输入合并路径列表 (每行一个路径)",
                        placeholder="/path/to/result_A\n/path/to/result_B",
                        lines=3,
                        info="输入多个路径，系统将自动合并当前路径与这些路径，取每个任务的最高分结果展示。"
                    )
                    merge_toggle_btn = gr.Button("🔗 开启/更新 合并模式")
                    merge_status_text = gr.Markdown("", visible=False)

            with gr.Row():
                gr.Image(label="成功率", value=os.path.join(root_dir, "domain_success_rates.png"), type="filepath", interactive=False)
                gr.Image(label="动作使用率", value=os.path.join(root_dir, "overall_action_usage.png"), type="filepath", interactive=False)
                gr.Image(label="步长/成功率", value=os.path.join(root_dir, "overall_step_distribution.png"), type="filepath", interactive=False)
                gr.Image(label="Token使用率", value=os.path.join(root_dir, "overall_token_usage_stacked.png"), type="filepath", interactive=False)

            gr.Markdown("### 选择 Domain:")
            with gr.Group(elem_classes="gr-button-group"):
                domain_buttons = []
                for i in range(MAX_BUTTONS):
                    btn = gr.Button(visible=False)
                    domain_buttons.append(btn)
            
            for i, domain_name in enumerate(domains):
                if i < MAX_BUTTONS:
                    domain_buttons[i].value = domain_name
                    domain_buttons[i].visible = True

        # --- 视图2: Task选择 ---
        with gr.Column(visible=False) as task_view:
            task_view_title = gr.Markdown("# 请选择一个 Task")
            # 2. Task 界面显示 Domain 统计
            domain_stats_display = gr.Markdown("", elem_classes="stats-header")
            
            with gr.Row():
                back_to_domains_btn = gr.Button("⬅️ 返回 Domain 选择")
            with gr.Row():
                domain_action_img = gr.Image(label=f"动作使用率", type="filepath", interactive=False)
                domain_step_img = gr.Image(label=f"步长/成功率", type="filepath", interactive=False)
                domain_token_img = gr.Image(label="Token使用率", type="filepath", interactive=False)

            with gr.Group(elem_classes="gr-button-group"):
                task_buttons = []
                success_buttons = []
                for i in range(MAX_BUTTONS):
                    with gr.Row():
                        btn = gr.Button(visible=False)
                        success = gr.Button(visible=False, interactive=False)
                    success_buttons.append(success)
                    task_buttons.append(btn)

        # --- 视图3: 轨迹查看器 ---
        with gr.Column(visible=False) as viewer_view:
            viewer_title = gr.Markdown("# 正在查看任务")
            with gr.Row():
                back_to_tasks_btn = gr.Button("⬅️ 返回 Task 选择")
            
            step_counter = gr.Markdown("步骤 1 / N")
            with gr.Row():
                prev_step_btn = gr.Button("◀️ 上一步")
                next_step_btn = gr.Button("▶️ 下一步")

            with gr.Row():
                with gr.Column(scale=4):
                    screenshot_img = gr.Image(
                        label="步骤截图", type="filepath", interactive=False, elem_id="screenshot-container"
                    )                    
                    evaluator_json = gr.Code(label="Evaluator", language="json", interactive=False)
                    
                with gr.Column(scale=2):
                    plan_text = gr.Textbox(label="Plan", lines=8, interactive=False)
                    plan_code_text = gr.Code(label="Plan Code", language="python", interactive=False)
                    reflection_text = gr.Textbox(label="Reflection", lines=5, interactive=False)

                    with gr.Accordion(label="Code Agent Plan Details", open=True, visible=False) as code_agent_accordion:
                        task_instruction_text = gr.Textbox(label="Task Instruction", lines=3, interactive=False)
                        completion_reason_text = gr.Textbox(label="Completion Reason", lines=1, interactive=False)
                        summary_text = gr.Textbox(label="Summary", lines=8, interactive=False)
                        execution_history_json = gr.Code(label="Combined Execution History", language="json", interactive=False)
                    with gr.Accordion(label="Search Agent Tutorials", open=True, visible=False) as search_agent_accordion:
                        tutorial_text = gr.Textbox(label="Tutorials", lines=8, interactive=False)

        # =================================================================
        # 函数与事件处理
        # =================================================================

        def toggle_comparison(path):
            if path and os.path.isdir(path):
                status_md = f"✅ **对比模式已开启。** 对比路径: `{path}`"
                return {
                    state_compare_root_dir: path,
                    compare_status_text: gr.update(value=status_md, visible=True),
                    compare_toggle_btn: gr.update(value="🔄 更新对比路径"),
                }
            else:
                return {
                    state_compare_root_dir: None,
                    compare_status_text: gr.update(value="❌ 路径无效，对比模式关闭。", visible=True),
                    compare_toggle_btn: gr.update(value="🚀 开启对比模式"),
                }

        def toggle_merge(text_input, root_dir):
            """开启合并模式时，需要立即计算一次全局统计"""
            paths = [line.strip() for line in text_input.split('\n') if line.strip()]
            valid_paths = [p for p in paths if os.path.isdir(p)]
            
            # 计算新的全局统计
            new_stats = calculate_global_stats(root_dir, merge_dirs=valid_paths)
            
            if valid_paths:
                status_md = f"✅ **合并模式已开启。** 有效路径数: {len(valid_paths)}<br>"
                for p in valid_paths:
                    status_md += f"- `{p}`<br>"
                if len(paths) > len(valid_paths):
                    status_md += f"⚠️ 忽略了 {len(paths) - len(valid_paths)} 个无效路径。"
                
                return {
                    state_merge_paths: valid_paths,
                    merge_status_text: gr.update(value=status_md, visible=True),
                    merge_toggle_btn: gr.update(value="🔄 更新合并列表"),
                    global_stats_display: gr.update(value=new_stats) # 更新全局统计
                }
            else:
                return {
                    state_merge_paths: [],
                    merge_status_text: gr.update(value="❌ 无有效路径，合并模式关闭。", visible=True),
                    merge_toggle_btn: gr.update(value="🔗 开启合并模式"),
                    global_stats_display: gr.update(value=new_stats) # 更新全局统计
                }

        def select_domain(domain_name, current_root_dir, compare_root_dir, merge_dirs):
            """选择Domain：计算并展示该Domain的统计信息"""
            # 获取任务列表和Domain统计
            tasks, success_list, css_classes, source_map, domain_stats_text = get_tasks_merged(
                current_root_dir, domain_name, compare_dir=compare_root_dir, merge_dirs=merge_dirs
            )
            
            updates = {
                state_selected_domain: domain_name,
                state_task_source_map: source_map,
                domain_view: gr.update(visible=False),
                task_view: gr.update(visible=True),
                task_view_title: gr.update(value=f"# Domain: {domain_name}\n请选择一个 Task："),
                domain_stats_display: gr.update(value=domain_stats_text), # 更新 Task 界面的 Domain 统计
                domain_action_img: gr.update(value=f"{os.path.join(root_dir, f'action_usage_{domain_name}.png')}"),
                domain_step_img: gr.update(value=f"{os.path.join(root_dir, f'step_distribution_{domain_name}.png')}"),
                domain_token_img: gr.update(value=f"{os.path.join(root_dir, f'token_usage_stacked_{domain_name}.png')}"),
            }
            
            for i in range(MAX_BUTTONS):
                if i < len(tasks):
                    updates[task_buttons[i]] = gr.update(
                        value=tasks[i], visible=True, elem_classes=css_classes[i]
                    )
                    updates[success_buttons[i]] = gr.update(
                        value=success_list[i], visible=True
                    )
                else:
                    updates[task_buttons[i]] = gr.update(visible=False, elem_classes="")
                    updates[success_buttons[i]] = gr.update(visible=False)

            return updates
        
        def select_task(task_name, source_map, selected_domain, base_root_dir):
            target_root = source_map.get(task_name, base_root_dir)
            steps, result, instruction = load_task_data(target_root, selected_domain, task_name)
            
            updates = {
                state_selected_task: task_name,
                state_current_viewing_root: target_root,
                state_steps_data: steps,
                state_current_step_index: 0,
                task_view: gr.update(visible=False),
                viewer_view: gr.update(visible=True),
                viewer_title: gr.update(value=f"## {task_name}: {instruction}\n### 最终结果: {result}")
            }
            if not steps:
                updates.update({
                    step_counter: "没有可显示的步骤。", screenshot_img: None, plan_text: "无数据",
                    plan_code_text: "无数据", reflection_text: "无数据",
                    prev_step_btn: gr.update(interactive=False), next_step_btn: gr.update(interactive=False),
                })
            else:
                step_updates = _get_step_display_updates(steps, 0, target_root, selected_domain, task_name)
                updates.update(step_updates)
            return updates

        def change_step(index, change, steps, viewing_root, domain, task):
            new_index = index + change
            if not (0 <= new_index < len(steps)):
                return {state_current_step_index: index}
            updates = _get_step_display_updates(steps, new_index, viewing_root, domain, task)
            updates[state_current_step_index] = new_index
            return updates

        def _get_step_display_updates(steps, index, root_dir, domain, task):
            step_data = steps[index]
            response = step_data.get("response", {})
            base_path = Path(root_dir) / domain / task
            filename = step_data.get("screenshot_file", "")
            
            img_path = base_path / filename
            annotated_img_path = base_path / (filename[:-4] + "_draw.png")
            milestone_img_path = base_path / (filename[:-4] + "_milestone.png")
            
            if annotated_img_path.exists():
                img_path = annotated_img_path
            elif milestone_img_path.exists():
                img_path = milestone_img_path
            
            is_milestone = "milestone" in str(img_path)
            new_label = "Milestone!" if is_milestone else "步骤截图"
            new_classes = ["milestone"] if is_milestone else []
            
            updates = {
                step_counter: gr.update(value=f"步骤 {index + 1} / {len(steps)}"),
                screenshot_img: gr.update(value=str(img_path) if img_path.exists() else None, label=new_label, elem_classes=new_classes),
                plan_text: gr.update(value=response.get("plan", "N/A")),
                plan_code_text: gr.update(value=response.get("plan_code", "N/A")),
                reflection_text: gr.update(value=response.get("reflection", "N/A")),
                prev_step_btn: gr.update(interactive=index > 0),
                next_step_btn: gr.update(interactive=index < len(steps) - 1),
            }
            
            code_agent_output = response.get("code_agent_output")
            (task_instruction, completion_reason, summary, history_json, is_code_visible) = process_code_agent_output(code_agent_output)
            is_search_visible, tutorial = (True, response["search_agent_output"]["final_answer"]) if response.get("search_agent_output") else (False, "N/A")
            
            evaluator_path = base_path.parent.parent.parent / "evaluation_examples/osworld" / "examples" / domain / f"{task}.json"
            if not evaluator_path.exists():
                 evaluator_path = Path("/nvme/yangbowen/yangbowen/InternGUIFramework/evaluation_examples/osworld/examples") / domain / f"{task}.json"

            if evaluator_path.exists():
                try:
                    evaluator_data = json.load(open(evaluator_path, "r", encoding="utf-8"))["evaluator"]
                    if "postconfig" in evaluator_data: del evaluator_data["postconfig"]
                    updates[evaluator_json] = gr.update(value=json.dumps(evaluator_data, indent=2))
                except:
                    updates[evaluator_json] = gr.update(value="无法加载 Evaluator 文件")
            
            updates.update({
                code_agent_accordion: gr.update(visible=is_code_visible),
                search_agent_accordion: gr.update(visible=is_search_visible),
                task_instruction_text: gr.update(value=task_instruction),
                completion_reason_text: gr.update(value=completion_reason),
                summary_text: gr.update(value=summary),
                execution_history_json: gr.update(value=history_json),
                tutorial_text: gr.update(value=tutorial),
            })
            return updates

        def back_to_domains_fn(root_dir, merge_dirs):
            """返回Domain列表时，重新计算/刷新全局统计"""
            stats = calculate_global_stats(root_dir, merge_dirs)
            return {
                domain_view: gr.update(visible=True), 
                task_view: gr.update(visible=False),
                global_stats_display: gr.update(value=stats) # 刷新全局统计
            }

        def back_to_tasks_fn(selected_domain, stats_text):
            return {
                task_view: gr.update(visible=True), 
                viewer_view: gr.update(visible=False), 
                task_view_title: gr.update(value=f"# Domain: {selected_domain}\n请选择一个 Task："),
                domain_stats_display: gr.update(value=stats_text) # 保持 Domain 统计
            }

        # --- 绑定事件 ---
        
        compare_toggle_btn.click(
            fn=toggle_comparison,
            inputs=[compare_path_input],
            outputs=[state_compare_root_dir, compare_status_text, compare_toggle_btn]
        )

        merge_toggle_btn.click(
            fn=toggle_merge,
            inputs=[merge_paths_input, state_root_dir],
            outputs=[state_merge_paths, merge_status_text, merge_toggle_btn, global_stats_display]
        )

        domain_click_outputs = [
            state_selected_domain, state_task_source_map, 
            domain_view, task_view, task_view_title, domain_stats_display, 
            domain_action_img, domain_step_img, domain_token_img
        ] + task_buttons + success_buttons
        
        for btn in domain_buttons:
            btn.click(
                fn=select_domain,
                inputs=[btn, state_root_dir, state_compare_root_dir, state_merge_paths],
                outputs=domain_click_outputs
            )
        
        task_select_outputs = [
            state_selected_task, state_current_viewing_root, state_steps_data, state_current_step_index, 
            task_view, viewer_view, viewer_title,
            step_counter, screenshot_img, plan_text, plan_code_text, reflection_text, prev_step_btn, next_step_btn,
            code_agent_accordion, search_agent_accordion, task_instruction_text, completion_reason_text, summary_text, execution_history_json, tutorial_text, evaluator_json
        ]
        for btn in task_buttons: 
            btn.click(
                fn=select_task, 
                inputs=[btn, state_task_source_map, state_selected_domain, state_root_dir], 
                outputs=task_select_outputs
            )
        
        step_change_outputs = [
            state_current_step_index, step_counter, screenshot_img, plan_text, plan_code_text, reflection_text,
            prev_step_btn, next_step_btn,
            code_agent_accordion, search_agent_accordion, task_instruction_text, completion_reason_text, summary_text, execution_history_json, tutorial_text, evaluator_json
        ]
        prev_step_btn.click(
            fn=change_step, 
            inputs=[state_current_step_index, gr.State(-1), state_steps_data, state_current_viewing_root, state_selected_domain, state_selected_task], 
            outputs=step_change_outputs
        )

        next_step_btn.click(
            fn=change_step, 
            inputs=[state_current_step_index, gr.State(1), state_steps_data, state_current_viewing_root, state_selected_domain, state_selected_task], 
            outputs=step_change_outputs
        )
        
        back_to_domains_btn.click(
            fn=back_to_domains_fn, 
            inputs=[state_root_dir, state_merge_paths], 
            outputs=[domain_view, task_view, global_stats_display]
        )
        
        back_to_tasks_btn.click(
            fn=back_to_tasks_fn, 
            inputs=[state_selected_domain, domain_stats_display], 
            outputs=[task_view, viewer_view, task_view_title, domain_stats_display]
        )

    return app

# Helper function to safely extract action from plan_code string
def extract_action_from_plan(plan_code):
    """
    Extracts the action name from a plan_code string like 'agent.click(...)'.
    It looks for the string between the first '.' and the first '('.
    
    Args:
        plan_code (str): The plan code string.
        
    Returns:
        str or None: The extracted action name, or None if the format is unexpected.
    """
    if not isinstance(plan_code, str):
        return None
    
    # Use regex for a more robust extraction
    # This pattern finds a word (alphanumeric + underscore) that is preceded by a '.'
    # and followed by a '('.
    match = re.search(r'\.(.*?)\(', plan_code)
    if match:
        return match.group(1)
    
    # Fallback for simple cases if regex fails, though less robust
    try:
        dot_index = plan_code.find('.')
        paren_index = plan_code.find('(')
        if 0 <= dot_index < paren_index:
            return plan_code[dot_index + 1:paren_index]
    except Exception:
        pass # Ignore errors in string manipulation
        
    return None

# ==============================================================================
# 新增的绘图辅助函数
# ==============================================================================
from matplotlib.ticker import MaxNLocator
def plot_step_histogram(success_steps, failure_steps, title, save_path):
    """
    为成功和失败的任务创建步长分布的上下对比直方图。
    (新版：两个子图均为正向，且上子图也显示X轴刻度)

    Args:
        success_steps (list): 成功任务的步长列表。
        failure_steps (list): 失败任务的步长列表。
        title (str): 图表的总标题。
        save_path (str): 图片保存路径。
    """
    if not success_steps and not failure_steps:
        print(f"Skipping plot for '{title}' as there is no step data.")
        return

    # 创建两个垂直排列的子图，并共享X轴
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    fig.suptitle(title, fontsize=16)

    # 计算合适的bins范围，确保覆盖所有步数
    all_steps = success_steps + failure_steps
    max_step = max(all_steps) if all_steps else 1
    # bins从1到max_step+2，确保每个整数步长都有独立的条柱
    bins = range(1, max_step + 3) 

    # --- 上子图: 成功的任务 ---
    ax1.hist(success_steps, bins=bins, color='mediumseagreen', alpha=0.8, rwidth=0.8, label='Success')
    ax1.set_title('Successful Tasks')
    ax1.set_ylabel('Number of Tasks')
    
    ax1.tick_params(axis='x', labelbottom=True)
    
    # 确保Y轴刻度为整数
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.grid(axis='y', linestyle='--', alpha=0.6)
    # 为上子图也添加Y轴的0线，使其看起来更完整
    ax1.axhline(0, color='black', linewidth=0.8)


    # --- 下子图: 失败的任务 ---
    ax2.hist(failure_steps, bins=bins, color='tomato', alpha=0.8, rwidth=0.8, label='Failure')
    ax2.set_title('Failed Tasks')
    ax2.set_xlabel('Number of Steps')
    ax2.set_ylabel('Number of Tasks')
    # 确保Y轴刻度为整数
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.grid(axis='y', linestyle='--', alpha=0.6)
    # 为下子图也添加Y轴的0线
    ax2.axhline(0, color='black', linewidth=0.8)

    # 调整子图之间的间距
    fig.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=3) # 增加垂直间距 h_pad

    plt.savefig(save_path)
    plt.close(fig)
    print(f"Saved step distribution plot to {save_path}")


def parse_reflection_type(reflection: str):
    if reflection == "":
        return "On Track"
    if "gui operation error" in reflection.lower():
        return "GUI Operation Error"
    elif "lack of tutorial" in reflection.lower():
        return "Lack of Tutorial"
    elif "code error" in reflection.lower():
        return "Code Error"
    else:
        return "On Track"
    
def plot_token_usage_stacked(stats_data, title, save_path):
    """
    Generates and saves a stacked bar chart for prompt and completion token usage.
    This version prevents error bars from going below zero and adds a combined
    total/percentage label on top of each bar in the format '100k (98.7%/1.3%)'.

    Args:
        stats_data (dict): Dict with agent names as keys and dicts of token lists as values.
        title (str): The title for the plot.
        save_path (str): The file path to save the plot.
    """
    if not stats_data:
        print(f"Skipping stacked token plot for '{title}' due to no data.")
        return

    try:
        # --- 确定任务总数 (num_tasks) ---
        num_tasks = 0
        if "orchestrator" in stats_data and stats_data["orchestrator"].get('prompt'):
            num_tasks = len(stats_data["orchestrator"]['prompt'])
        else:
            for agent_data in stats_data.values():
                num_tasks = max(num_tasks, len(agent_data.get('prompt', [])), len(agent_data.get('completion', [])))
        
        if num_tasks == 0:
            print(f"Skipping stacked token plot for '{title}' as num_tasks is zero.")
            return

        agents = sorted(stats_data.keys())
        prompt_avgs = []
        completion_avgs = []
        total_stds = []

        total_prompt_avg_sum = 0
        total_completion_avg_sum = 0
        
        # --- 计算每个 Agent 的统计数据 ---
        for agent in agents:
            prompt_tokens_orig = stats_data[agent].get('prompt', [])
            completion_tokens_orig = stats_data[agent].get('completion', [])

            prompt_tokens_padded = prompt_tokens_orig + [0] * (num_tasks - len(prompt_tokens_orig))
            completion_tokens_padded = completion_tokens_orig + [0] * (num_tasks - len(completion_tokens_orig))
            
            prompt_avg = np.mean(prompt_tokens_padded)
            completion_avg = np.mean(completion_tokens_padded)
            
            prompt_avgs.append(prompt_avg)
            completion_avgs.append(completion_avg)

            total_prompt_avg_sum += prompt_avg
            total_completion_avg_sum += completion_avg

            total_tokens = [p + c for p, c in zip(prompt_tokens_padded, completion_tokens_padded)]
            total_std = np.std(total_tokens) if total_tokens else 0
            total_stds.append(total_std)

        # --- 计算 "Total" 条目的统计数据 ---
        task_grand_totals = [0] * num_tasks
        for agent in agents:
            prompts_orig = stats_data[agent].get('prompt', [])
            completions_orig = stats_data[agent].get('completion', [])
            prompts_padded = prompts_orig + [0] * (num_tasks - len(prompts_orig))
            completions_padded = completions_orig + [0] * (num_tasks - len(completions_orig))
            for i in range(num_tasks):
                task_grand_totals[i] += prompts_padded[i] + completions_padded[i]

        total_all_agents_std = np.std(task_grand_totals) if task_grand_totals else 0
        
        # --- 添加 "Total" 条目 ---
        agents.append('Total')
        prompt_avgs.append(total_prompt_avg_sum)
        completion_avgs.append(total_completion_avg_sum)
        total_stds.append(total_all_agents_std)

        # --- 开始绘图 ---
        plt.figure(figsize=(max(10, len(agents) * 1.5), 8))
        
        bar_width = 0.6
        indices = np.arange(len(agents))
        prompt_avgs_np = np.array(prompt_avgs)
        completion_avgs_np = np.array(completion_avgs)

        plt.bar(indices, prompt_avgs_np, bar_width, label='Prompt Tokens', color='#1f77b4', alpha=0.8)
        plt.bar(indices, completion_avgs_np, bar_width, bottom=prompt_avgs_np, label='Completion Tokens', color='#ff7f0e', alpha=0.8)

        total_avgs = prompt_avgs_np + completion_avgs_np
        total_stds_np = np.array(total_stds)
        lower_errors = np.minimum(total_avgs, total_stds_np)
        asymmetric_errors = np.array([lower_errors, total_stds_np])
        plt.errorbar(indices, total_avgs, yerr=asymmetric_errors, fmt='none', ecolor='black', capsize=5, elinewidth=1.5, markeredgewidth=1.5)

        plt.ylabel('Average Token Count per Task')
        plt.title(title)
        plt.xticks(indices, agents, rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend()

        # ==============================================================================
        # =================== 核心修改: 在柱状图上添加新的组合标签 =====================
        # ==============================================================================
        for i in range(len(agents)):
            total_height = total_avgs[i]
            prompt_height = prompt_avgs_np[i]
            completion_height = completion_avgs_np[i]

            # 1. 格式化总数部分
            total_label_part = f'{total_height/1000:,.1f}k' if total_height >= 1000 else f'{total_height:,.0f}'
            
            final_label = total_label_part

            # 2. 如果总数大于0且两种token都存在，则添加百分比部分
            if total_height > 0 and prompt_height > 0 and completion_height > 0:
                prompt_perc = (prompt_height / total_height) * 100
                completion_perc = (completion_height / total_height) * 100
                # 拼接成最终标签
                final_label += f' ({prompt_perc:.1f}%/{completion_perc:.1f}%)'

            # 3. 将最终标签放置在图表上
            plt.text(indices[i], total_height, final_label, ha='center', va='bottom', fontsize=8, fontweight='bold')
        # ==============================================================================
        # =============================== 修改结束 =====================================
        # ==============================================================================

        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        print(f"Saved stacked token usage plot to {save_path}")

    except Exception as e:
        print(f"An unexpected error occurred while generating stacked token usage plot for '{title}': {e}")

def get_result(target_dir):
    """
    Analyzes experiment results from a target directory, calculates success rates,
    gathers action and token statistics, and generates various plots including Error Analysis.
    """
    if not os.path.exists(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.")
        return None

    # --- Data Structures for Analysis ---
    all_result = []
    domain_result_raw = {}
    all_result_for_analysis = {}
    overall_action_counts = Counter()
    domain_action_counts = {}

    # --- Token 统计结构 ---
    domain_token_stats = {}
    overall_token_stats = {}

    # --- Error/Reflection 统计结构 ---
    def init_error_stats():
        return {
            'categories': {
                'GUI Operation Error': {'hint': 0, 'type': 0, 'match': 0},
                'Lack of Tutorial':    {'hint': 0, 'type': 0, 'match': 0},
                'Code Error':          {'hint': 0, 'type': 0, 'match': 0}
            },
            'type_counts': Counter(),
            'total_steps': 0
        }

    domain_error_stats = {}
    overall_error_stats = init_error_stats()

    print("Starting analysis...")
    # --- Data Collection Loop ---
    for domain in os.listdir(target_dir):
        domain_path = os.path.join(target_dir, domain)
        if not os.path.isdir(domain_path): continue

        domain_action_counts[domain] = Counter()
        domain_token_stats[domain] = {}
        domain_error_stats[domain] = init_error_stats()
        
        for example_id in os.listdir(domain_path):
            example_path = os.path.join(domain_path, example_id)
            if not os.path.isdir(example_path): continue

            if domain not in all_result_for_analysis: all_result_for_analysis[domain] = {}
            if example_id not in all_result_for_analysis[domain]: all_result_for_analysis[domain][example_id] = {}

            # --- 1. Process Success/Failure Result ---
            result_file = os.path.join(example_path, "result.txt")
            final_result = 0.0
            if os.path.exists(result_file):
                try:
                    with open(result_file, "r") as f: result_str = f.read().strip()
                    try: result_val = float(result_str)
                    except (ValueError, TypeError): result_val = float(eval(result_str))
                    final_result = result_val
                except Exception as e:
                    print(f"Warning: Could not parse result file {result_file}. Defaulting to 0.0. Error: {e}")
                    final_result = 0.0
                if domain not in domain_result_raw: domain_result_raw[domain] = []
                domain_result_raw[domain].append(final_result)
                all_result.append(final_result)
                all_result_for_analysis[domain][example_id]["score"] = final_result

            # --- 2. Process Trajectory for Action and Step Statistics ---
            traj_file = os.path.join(example_path, "traj.jsonl")
            if os.path.exists(traj_file):
                try:
                    with open(traj_file, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        all_result_for_analysis[domain][example_id]["step"] = len(lines)
                        for line in lines:
                            try:
                                data = json.loads(line)
                                plan_code = data.get("response", {}).get("plan_code") or data.get("plan_code")
                                
                                # 模拟 action 获取 (实际请替换为你的 extract_action_from_plan)
                                action = "unknown"
                                if plan_code: action = plan_code.split('(')[0]

                                if action:
                                    overall_action_counts[action] += 1
                                    domain_action_counts[domain][action] += 1
                                if "call_search_agent" in action:
                                    with open(os.path.join(example_path, "search.txt"), "w", encoding="utf-8") as f:
                                        f.write("1")
                                if "call_code_agent" in action:
                                    with open(os.path.join(example_path, "code.txt"), "w", encoding="utf-8") as f:
                                        f.write("1")
                                # --- ErrorType 统计逻辑 ---
                                reflection = data.get("response", {}).get("reflection", {})
                                error_hint = reflection.get("hint", {})
                                
                                # 获取 Hint (Boolean)
                                gui_hint = error_hint.get("gui_operation_error", False)
                                lack_of_tutorial_hint = error_hint.get("lack_of_tutorial", False)
                                code_hint = error_hint.get("code_error", False)
                                
                                # 获取 Reflection Type (String)
                                reflection_type = parse_reflection_type(reflection.get("reflection", "None"))

                                # 定义映射关系
                                error_mapping = [
                                    ("GUI Operation Error", gui_hint),
                                    ("Lack of Tutorial", lack_of_tutorial_hint),
                                    ("Code Error", code_hint)
                                ]

                                # 更新 Domain 统计
                                domain_stats = domain_error_stats[domain]
                                domain_stats['total_steps'] += 1
                                domain_stats['type_counts'][reflection_type] += 1

                                # 更新 Overall 统计
                                overall_error_stats['total_steps'] += 1
                                overall_error_stats['type_counts'][reflection_type] += 1
 
                                for err_name, is_hint_present in error_mapping:
                                    is_type_present = (reflection_type == err_name)
                                    is_true_positive = (is_hint_present and is_type_present)

                                    # Domain Level Update
                                    if is_hint_present:  domain_stats['categories'][err_name]['hint'] += 1
                                    if is_type_present:  domain_stats['categories'][err_name]['type'] += 1
                                    if is_true_positive: domain_stats['categories'][err_name]['match'] += 1
                                    
                                    # Overall Level Update
                                    if is_hint_present:  overall_error_stats['categories'][err_name]['hint'] += 1
                                    if is_type_present:  overall_error_stats['categories'][err_name]['type'] += 1
                                    if is_true_positive: overall_error_stats['categories'][err_name]['match'] += 1

                            except (json.JSONDecodeError, AttributeError): continue
                except Exception as e:
                    print(f"Warning: Could not read or process trajectory file {traj_file}. Error: {e}")

            # --- 3. Process Token Usage ---
            token_log_file = os.path.join(example_path, "token.jsonl")
            if os.path.exists(token_log_file):
                task_token_summary = {}
                try:
                    with open(token_log_file, "r", encoding="utf-8") as f:
                        for line in f:
                            try:
                                data = json.loads(line.strip())
                                agent_name = data.get("agent_name")
                                if not agent_name: continue
                                if agent_name not in task_token_summary:
                                    task_token_summary[agent_name] = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}
                                task_token_summary[agent_name]["completion_tokens"] += data.get("completion_tokens", 0)
                                task_token_summary[agent_name]["prompt_tokens"] += data.get("prompt_tokens", 0)
                                task_token_summary[agent_name]["total_tokens"] += data.get("total_tokens", 0)
                            except (json.JSONDecodeError, AttributeError): continue
                    
                    if task_token_summary:
                        task_token_output_path = os.path.join(example_path, "token.json")
                        with open(task_token_output_path, "w", encoding="utf-8") as f:
                            json.dump(task_token_summary, f, indent=4)
                        
                        for agent, tokens in task_token_summary.items():
                            if agent not in domain_token_stats[domain]:
                                domain_token_stats[domain][agent] = {'prompt': [], 'completion': []}
                            domain_token_stats[domain][agent]['prompt'].append(tokens['prompt_tokens'])
                            domain_token_stats[domain][agent]['completion'].append(tokens['completion_tokens'])
                            
                            if agent not in overall_token_stats:
                                overall_token_stats[agent] = {'prompt': [], 'completion': []}
                            overall_token_stats[agent]['prompt'].append(tokens['prompt_tokens'])
                            overall_token_stats[agent]['completion'].append(tokens['completion_tokens'])

                except Exception as e:
                    print(f"Warning: Could not process token file {token_log_file}. Error: {e}")

    # --- Result Summary and JSON Output ---
    if not all_result:
        print("New experiment or no valid results found.")
        return None

    print("\n--- Success Rate Summary ---")
    domain_success_rate = {}
    for domain, results in domain_result_raw.items():
        if results:
            rate = sum(results) / len(results) * 100
            domain_success_rate[domain] = rate
            print(f"Domain: {domain:<20} | Runs: {len(results):<5} | Success Rate: {rate:.2f}%")
    overall_rate = sum(all_result) / len(all_result) * 100
    print("-" * 60)
    print(f"Overall                  | Runs: {len(all_result):<5} | Avg. Success Rate: {overall_rate:.2f}%")
    print("-" * 60)
    json_output_path = os.path.join(target_dir, "all_result_summary.json")
    try:
        with open(json_output_path, "w", encoding="utf-8") as f: json.dump(all_result_for_analysis, f, indent=4)
        print(f"\nAnalysis summary saved to {json_output_path}")
    except Exception as e: print(f"Error saving summary JSON: {e}")

    # --- Plotting Section ---
    print("\nGenerating plots...")

    # Plot 1: Overall Action Usage
    if overall_action_counts:
        try:
            save_path = os.path.join(target_dir, "overall_action_usage.png")
            plt.figure(figsize=(12, 8)); sorted_actions = overall_action_counts.most_common(); actions = [i[0] for i in sorted_actions]; counts = [i[1] for i in sorted_actions]
            bars = plt.barh(actions, counts, color='skyblue'); plt.xlabel('Usage Count'); plt.ylabel('Action Type'); plt.title('Overall Action Usage Frequency'); plt.gca().invert_yaxis()
            if counts: plt.xlim(right=max(counts) * 1.15)
            for bar in bars: xval = bar.get_width(); plt.text(xval + (max(counts) * 0.01), bar.get_y() + bar.get_height() / 2.0, f' {int(xval)} ({int(xval) / sum(counts) * 100:.1f}%)', ha='left', va='center')
            plt.tight_layout(); plt.savefig(save_path); plt.close(); print(f"Saved overall action usage plot to {save_path}")
        except Exception as e: print(f"Error generating overall action usage plot: {e}")

    # Plot 2: Per-Domain Action Usage
    # Plot 2: Per-Domain Action Usage
    for domain, counts in domain_action_counts.items():
        if not counts: continue
        try:
            save_path = os.path.join(target_dir, f"action_usage_{domain}.png")
            plt.figure(figsize=(10, 6))
            
            sorted_actions = counts.most_common()
            actions = [i[0] for i in sorted_actions]
            action_counts = [i[1] for i in sorted_actions] # 这是一个纯数字的列表
            
            bars = plt.barh(actions, action_counts, color='lightgreen')
            plt.xlabel('Usage Count')
            plt.ylabel('Action Type')
            plt.title(f'Action Usage Frequency in Domain: {domain}')
            plt.gca().invert_yaxis()
            
            if action_counts: 
                plt.xlim(right=max(action_counts) * 1.15)
            
            # --- 修复点开始 ---
            # 计算总数时，使用 sum(action_counts) 或者 sum(counts.values())
            total_count = sum(action_counts)
            # --- 修复点结束 ---

            for bar in bars: 
                xval = bar.get_width()
                # 这里将原本的 sum(counts) 替换为了 total_count
                plt.text(xval + (max(action_counts) * 0.01), 
                         bar.get_y() + bar.get_height() / 2.0, 
                         f' {int(xval)} ({int(xval) / total_count * 100:.1f}%)', 
                         ha='left', va='center')
            
            plt.tight_layout()
            plt.savefig(save_path)
            plt.close()
            print(f"Saved action usage plot for domain '{domain}' to {save_path}")
        except Exception as e: 
            print(f"Error generating action usage plot for domain {domain}: {e}")

    # Plot 3: Success Rate by Domain
    if domain_success_rate:
        try:
            save_path = os.path.join(target_dir, "domain_success_rates.png"); domains_sorted = sorted(domain_success_rate.keys()); rates_sorted = [domain_success_rate[d] for d in domains_sorted]
            plot_labels = domains_sorted + ['Average']; plot_values = rates_sorted + [overall_rate]; colors = ['#87CEEB'] * len(domains_sorted) + ['#FF6347']
            plt.figure(figsize=(max(10, len(plot_labels) * 0.8), 7)); bars = plt.bar(plot_labels, plot_values, color=colors)
            plt.ylabel('Success Rate (%)'); plt.title('Success Rate by Domain and Overall Average'); plt.xticks(rotation=45, ha='right'); plt.ylim(0, 110); plt.grid(axis='y', linestyle='--', alpha=0.7)
            for bar in bars: yval = bar.get_height(); plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f'{yval:.1f}%', ha='center', va='bottom')
            plt.tight_layout(); plt.savefig(save_path); plt.close(); print(f"Saved success rate plot to {save_path}")
        except Exception as e: print(f"Error generating success rate plot: {e}")

    # --- Plot 6: Error & Reflection Analysis (Combined & Enhanced) ---
    print("\nGenerating error analysis plots...")

    def plot_error_analysis(stats, title_prefix, save_path):
        """
        Generates a single combined grouped bar chart:
        - Bar 1 (Left): Agent Prediction Count (Type)
        - Bar 2 (Right): Ground Truth Hint Count (Hint)
        - Annotation: Precision & Recall displayed above each group.
        """
        if stats['total_steps'] == 0:
            return

        # 1. 准备数据
        categories = list(stats['categories'].keys()) # ['GUI Operation Error', ...]
        
        # 提取 Type (分母: Agent 预测数量)
        type_counts = [stats['categories'][c]['type'] for c in categories]
        # 提取 Hint (分母: Ground Truth 数量)
        hint_counts = [stats['categories'][c]['hint'] for c in categories]
        # 提取 Match (分子: 交集数量，用于计算指标)
        match_counts = [stats['categories'][c]['match'] for c in categories]

        x = np.arange(len(categories))
        width = 0.35  # 柱子宽度

        fig, ax = plt.subplots(figsize=(12, 8))

        # 2. 绘制分组柱状图
        # 左侧柱子：Type (Agent Prediction)
        rects1 = ax.bar(x - width/2, type_counts, width, label='Agent Prediction (Type)', color='#8da0cb')
        # 右侧柱子：Hint (Ground Truth)
        rects2 = ax.bar(x + width/2, hint_counts, width, label='Ground Truth (Hint)', color='#fc8d62')

        # 3. 设置图表属性
        ax.set_ylabel('Count')
        ax.set_title(f'{title_prefix}: Reflection Analysis (Type vs Hint)\nPrecision = Match/Type | Recall = Match/Hint')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()

        # 4. 辅助函数：在柱子上显示原始数量
        def autolabel_counts(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9)
        
        autolabel_counts(rects1)
        autolabel_counts(rects2)

        # 5. 核心逻辑：在柱子组上方显示 Precision 和 Recall
        for i in range(len(categories)):
            n_type = type_counts[i]
            n_hint = hint_counts[i]
            n_match = match_counts[i]

            # 计算 Precision (精确率) = Match / Type
            precision = (n_match / n_type * 100) if n_type > 0 else 0.0
            
            # 计算 Recall (召回率) = Match / Hint
            recall = (n_match / n_hint * 100) if n_hint > 0 else 0.0

            # 确定文字显示的 Y 轴高度 (取两个柱子中较高的那个，再往上抬一点)
            max_height = max(n_type, n_hint)
            # 动态调整高度偏移，防止文字贴太紧
            text_y = max_height + (max(type_counts + hint_counts) * 0.02) if (type_counts + hint_counts) else 1

            # 显示文本
            label_text = f"Prec: {precision:.1f}%\nRec: {recall:.1f}%"
            ax.text(i, text_y, label_text, 
                    ha='center', va='bottom', 
                    fontsize=11, color='darkred', fontweight='bold',
                    bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1))

        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        print(f"Saved error analysis plot to {save_path}")

    # Generate Overall Plot
    plot_error_analysis(overall_error_stats, "Overall", os.path.join(target_dir, "overall_error_analysis.png"))

    # Generate Per-Domain Plots
    for domain, stats in domain_error_stats.items():
        plot_error_analysis(stats, f"Domain: {domain}", os.path.join(target_dir, f"error_analysis_{domain}.png"))

    print("\nAnalysis complete.")
    return all_result


# ==============================================================================
# 主程序入口
# ==============================================================================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    # environment config
    parser.add_argument("--root_dir", type=str, required=True)
    parser.add_argument("--port", type=int, default=10000)
    args = parser.parse_args()
    
    get_result(args.root_dir)
    gradio_app = create_gradio_app(args.root_dir)
    gradio_app.launch(server_name="0.0.0.0", server_port=args.port, allowed_paths=["/nvme/yangbowen/"])
