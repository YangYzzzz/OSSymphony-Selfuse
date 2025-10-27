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


# ==============================================================================
# 辅助函数：创建虚拟数据以便于测试
# 在实际使用中，您可以注释掉或删除这部分。
# ==============================================================================
def create_dummy_data(root_dir="trajectory_data"):
    """创建一个符合描述的虚拟目录结构和文件，用于演示和测试。"""
    if os.path.exists(root_dir):
        print(f"虚拟数据目录 '{root_dir}' 已存在，跳过创建。")
        return root_dir

    print(f"正在创建虚拟数据目录: '{root_dir}'...")
    root_path = Path(root_dir)
    root_path.mkdir(exist_ok=True)

    domains = ["web_shopping", "data_entry", "file_management"]
    for domain in domains:
        (root_path / domain).mkdir(exist_ok=True)
        num_tasks = random.randint(2, 4)
        for i in range(1, num_tasks + 1):
            task_name = f"task_{domain[:4]}_{i:03d}"
            task_path = root_path / domain / task_name
            task_path.mkdir(exist_ok=True)

            # 创建 result.txt
            result = random.choice(['0', '1'])
            (task_path / "result.txt").write_text(result)

            # 创建 traj.jsonl 和截图
            steps_data = []
            num_steps = random.randint(3, 8)
            for step_num in range(1, num_steps + 1):
                # 创建虚拟截图
                img_filename = f"step_{step_num}_{random.randint(1000,9999)}.png"
                img_path = task_path / img_filename
                img = Image.new('RGB', (600, 400), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                draw = ImageDraw.Draw(img)
                try:
                    # 尝试使用系统字体，如果失败则使用默认
                    font = ImageFont.truetype("arial.ttf", 20)
                except IOError:
                    font = ImageFont.load_default()
                draw.text((10, 10), f"Domain: {domain}\nTask: {task_name}\nStep: {step_num}", fill=(255,255,255), font=font)
                img.save(img_path)

                # 创建虚拟步骤数据
                step_info = {
                    "step_num": step_num,
                    "action_timestamp": f"20240101@{100000 + step_num}",
                    "action": f"pyautogui.click({step_num * 10}, {step_num * 20})",
                    "response": {
                        "plan": f"(Step {step_num}) This is a detailed plan for this step. The goal is to accomplish XYZ. This text can be quite long to demonstrate the scrolling capability of the textbox. The agent will now proceed with the planned code.",
                        "plan_code": f"agent.click_element('button_{step_num}')",
                        "reflection": f"Case 1 - Step {step_num} reflection. The previous action was successful. The current observation matches the expectation. Why: The UI element was found and clicked as planned. The trajectory is going according to plan.",
                        "reflection_thoughts": "This is a thought for step " + str(step_num),
                        "code_agent_output": None
                    },
                    "reward": 0,
                    "done": step_num == num_steps,
                    "info": {},
                    "screenshot_file": img_filename
                }
                steps_data.append(json.dumps(step_info))

            (task_path / "traj.jsonl").write_text("\n".join(steps_data))
    
    print("虚拟数据创建完成。")
    return root_dir

# ==============================================================================
# Gradio 应用核心逻辑
# ==============================================================================

MAX_BUTTONS = 100 # 预先定义UI中支持的最大按钮数量（适用于domain和task）

def get_domains(root_dir):
    """获取根目录下的所有domain目录"""
    if not os.path.isdir(root_dir):
        return []
    return [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

def get_tasks(root_dir, domain):
    """获取指定domain下的所有task目录"""
    domain_path = os.path.join(root_dir, domain)
    if not os.path.isdir(domain_path):
        return []
    task_name_list = [t for t in os.listdir(domain_path) if os.path.isdir(os.path.join(domain_path, t))]
    success_list = []
    for i, task_name in enumerate(task_name_list):
        result_file = Path(domain_path) / task_name / "result.txt"
        result_text = "未知"
        if result_file.exists():
            result_num = float(result_file.read_text().strip())
        if result_num > 0:
            result_text = f'✅成功 {result_num}✅'
        elif result_num == 0:
            result_text = '❌失败 0.0❌'
        success_list.append(result_text)
    return task_name_list, success_list

def load_task_data(root_dir, domain, task):
    """加载一个任务的所有步骤数据和结果"""
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
    print(steps)
    result_file = task_path / "result.txt"
    result_text = "未知"
    if result_file.exists():
        result_num = float(result_file.read_text().strip())
        if result_num > 0:
            result_text = f'<span class="success-text">成功 {result_num}</span>'
        elif result_num == 0:
            result_text = '<span class="failure-text">失败 0.0</span>'
    
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

    with gr.Blocks(theme=gr.themes.Soft(), css="""
        .gr-button-group { display: flex; flex-wrap: wrap; gap: 10px; }
        .gr-button-group > button { flex-grow: 1; }
        .success-text { color: #28a745; font-weight: bold; } /* 成功的绿色，加粗 */
        .failure-text { color: #dc3545; font-weight: bold; } /* 失败的红色，加粗 */
                   
        #sticky-image-column {
            position: -webkit-sticky; /* 兼容旧版 Safari */
            position: sticky;
            top: 20px; /* 距离视口顶部的距离，可以按需调整 */
            align-self: flex-start; /* 确保列在 flex 容器顶部对齐 */
            /* 设置一个最大高度，防止图片本身过高导致无法查看全部 */
            max-height: 95vh; 
        }
    """) as app:
        # --- 状态存储 ---
        state_root_dir = gr.State(root_dir)
        state_selected_domain = gr.State()
        state_selected_task = gr.State()
        state_steps_data = gr.State()
        state_current_step_index = gr.State(0)

        # --- 视图1: Domain选择 ---
        with gr.Column(visible=True) as domain_view:
            gr.Markdown(f"# 任务轨迹浏览器({os.path.basename(root_dir)})\n请选择一个 Domain：")
            with gr.Row():
                gr.Image(label="成功率", value=os.path.join(root_dir, "domain_success_rates.png"), type="filepath", interactive=False)
                gr.Image(label="动作使用率", value=os.path.join(root_dir, "overall_action_usage.png"), type="filepath", interactive=False)
                gr.Image(label="步长/成功率", value=os.path.join(root_dir, "overall_step_distribution.png"), type="filepath", interactive=False)
            with gr.Group(elem_classes="gr-button-group"):
                domain_buttons = []
                for i in range(MAX_BUTTONS):
                    btn = gr.Button(visible=False)
                    domain_buttons.append(btn)
            
            # 动态填充Domain按钮
            for i, domain_name in enumerate(domains):
                if i < MAX_BUTTONS:
                    domain_buttons[i].value = domain_name
                    domain_buttons[i].visible = True


        # --- 视图2: Task选择 ---
        with gr.Column(visible=False) as task_view:
            task_view_title = gr.Markdown("# 请选择一个 Task")
            with gr.Row():
                back_to_domains_btn = gr.Button("⬅️ 返回 Domain 选择")
            with gr.Row():
                domain_action_img = gr.Image(label=f"动作使用率", type="filepath", interactive=False)
                domain_step_img = gr.Image(label=f"步长/成功率", type="filepath", interactive=False)
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
                with gr.Column(scale=4, elem_id="sticky-image-column"):
                    screenshot_img = gr.Image(label="步骤截图", type="filepath", interactive=False)
                    evaluator_json = gr.Code(
                        label="Evaluator",
                        language="json",
                        interactive=False
                    )
                    
                with gr.Column(scale=2):
                    plan_text = gr.Textbox(label="Plan", lines=8, interactive=False)
                    plan_code_text = gr.Code(label="Plan Code", language="python", interactive=False)
                    reflection_text = gr.Textbox(label="Reflection", lines=5, interactive=False)

                    with gr.Accordion(label="Code Agent Plan Details", open=True, visible=False) as code_agent_accordion:
                        task_instruction_text = gr.Textbox(label="Task Instruction", lines=3, interactive=False)
                        completion_reason_text = gr.Textbox(label="Completion Reason", lines=1, interactive=False)
                        summary_text = gr.Textbox(label="Summary", lines=8, interactive=False) # Summary 可能会比较长
                        
                        # 用于显示合并后的历史记录
                        execution_history_json = gr.Code(
                            label="Combined Execution History",
                            language="json",
                            interactive=False,
                            elem_classes=["code-wrap-container"] # 复用自动换行样式
                        )
        # =================================================================
        # 函数与事件处理
        # =================================================================

        def select_domain(domain_name, current_root_dir):
            """当一个domain按钮被点击时触发"""
            tasks, success_list = get_tasks(current_root_dir, domain_name)
            updates = {
                state_selected_domain: domain_name,
                domain_view: gr.update(visible=False),
                task_view: gr.update(visible=True),
                task_view_title: gr.update(value=f"# Domain: {domain_name}\n请选择一个 Task："),
                domain_action_img: gr.update(value=f"{os.path.join(root_dir, f'action_usage_{domain_name}.png')}"),
                domain_step_img: gr.update(value=f"{os.path.join(root_dir, f'step_distribution_{domain_name}.png')}"),
            }
            # 更新并显示Task按钮
            for i, btn in enumerate(task_buttons):
                if i < len(tasks):
                    updates[btn] = gr.update(value=tasks[i], visible=True)

            for i, su in enumerate(success_buttons):
                if i < len(tasks):
                    updates[su] = gr.update(value=success_list[i], visible=True)

            return updates

        def select_task(task_name, current_root_dir, selected_domain):
            """当一个task按钮被点击时触发"""

            steps, result, instruction = load_task_data(current_root_dir, selected_domain, task_name)
            
            updates = {
                state_selected_task: task_name,
                state_steps_data: steps,
                state_current_step_index: 0,
                task_view: gr.update(visible=False),
                viewer_view: gr.update(visible=True),
                viewer_title: gr.update(value=f"## {task_name}: {instruction}\n### 最终结果: {result}")
            }

            if not steps:
                # 如果没有步骤数据
                updates.update({
                    step_counter: "没有可显示的步骤。",
                    screenshot_img: None,
                    plan_text: "无数据",
                    plan_code_text: "无数据",
                    reflection_text: "无数据",
                    prev_step_btn: gr.update(interactive=False),
                    next_step_btn: gr.update(interactive=False),
                })
            else:
                # 显示第一步的数据
                step_updates = _get_step_display_updates(steps, 0, current_root_dir, selected_domain, task_name)
                updates.update(step_updates)

            return updates

        def change_step(index, change, steps, root_dir, domain, task):
            """处理上一步/下一步按钮点击"""
            new_index = index + change
            if not (0 <= new_index < len(steps)):
                # 如果索引越界，则不更新
                return {state_current_step_index: index}

            updates = _get_step_display_updates(steps, new_index, root_dir, domain, task)
            updates[state_current_step_index] = new_index
            return updates

        def _get_step_display_updates(steps, index, root_dir, domain, task):
            step_data = steps[index]
            response = step_data.get("response", {})
            img_path = Path(root_dir) / domain / task / step_data.get("screenshot_file", "")
            
            img_name_phase = step_data.get("screenshot_file").split("_")
            if len(img_name_phase) == 3:
                annotated_img_path = Path(root_dir) / domain / task / (img_name_phase[0] + "_" + img_name_phase[1] + "_draw_" + img_name_phase[2])
            else:
                annotated_img_path = Path(root_dir) / domain / task / (step_data.get("screenshot_file")[:-4] + "_draw.png")
            if annotated_img_path.exists():
                img_path = annotated_img_path
            # 原有的更新字典
            updates = {
                step_counter: gr.update(value=f"步骤 {index + 1} / {len(steps)}"),
                screenshot_img: gr.update(value=str(img_path) if img_path.exists() else None),
                plan_text: gr.update(value=response.get("plan", "N/A")),
                plan_code_text: gr.update(value=response.get("plan_code", "N/A")),
                reflection_text: gr.update(value=response.get("reflection", "N/A")),
                prev_step_btn: gr.update(interactive=index > 0),
                next_step_btn: gr.update(interactive=index < len(steps) - 1),
            }

            # --- 新增: 处理并更新 Code Agent UI ---
            code_agent_output = response.get("code_agent_output")
            (task_instruction, completion_reason, summary, 
            history_json, is_visible) = process_code_agent_output(code_agent_output)

            evaluator_path = os.path.join("/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/examples", domain, f"{task}.json")
            evaluator_data = json.load(open(evaluator_path, "r", encoding="utf-8"))["evaluator"]
            # print(evaluator_data)
            if "postconfig" in evaluator_data:
                del evaluator_data["postconfig"]
            print(evaluator_data)

            updates.update({
                code_agent_accordion: gr.update(visible=is_visible),
                task_instruction_text: gr.update(value=task_instruction),
                completion_reason_text: gr.update(value=completion_reason),
                summary_text: gr.update(value=summary),
                execution_history_json: gr.update(value=history_json),
                evaluator_json: gr.update(value=json.dumps(evaluator_data, indent=2))
            })
            # json.dumps(evaluator_data, indent=2)
            # -----------------------------------------

            return updates

        def back_to_domains_fn():
            """返回Domain选择视图"""
            return {
                domain_view: gr.update(visible=True),
                task_view: gr.update(visible=False),
            }

        def back_to_tasks_fn(selected_domain):
            """返回Task选择视图"""
            return {
                task_view: gr.update(visible=True),
                viewer_view: gr.update(visible=False),
                task_view_title: gr.update(value=f"# Domain: {selected_domain}\n请选择一个 Task：")
            }

        # --- 绑定事件 ---
        for btn in domain_buttons:
            btn.click(
                fn=select_domain,
                inputs=[btn, state_root_dir],
                outputs=[state_selected_domain, domain_view, task_view, task_view_title, domain_action_img, domain_step_img] + task_buttons + success_buttons
            )
        
        task_select_outputs = [
            state_selected_task, state_steps_data, state_current_step_index, task_view, viewer_view, viewer_title,
            step_counter, screenshot_img, plan_text, plan_code_text, reflection_text, prev_step_btn, next_step_btn,
            code_agent_accordion, task_instruction_text, completion_reason_text, summary_text, execution_history_json, evaluator_json
        ]
        for btn in task_buttons: 
            btn.click(
                fn=select_task, 
                inputs=[btn, state_root_dir, state_selected_domain], 
                outputs=task_select_outputs
            )
        
        step_change_outputs = [
            state_current_step_index, step_counter, screenshot_img, plan_text, plan_code_text, reflection_text,
            prev_step_btn, next_step_btn,
            code_agent_accordion, task_instruction_text, completion_reason_text, summary_text, execution_history_json, evaluator_json
        ]
        prev_step_btn.click(
            fn=change_step, 
            inputs=[state_current_step_index, gr.State(-1), state_steps_data, state_root_dir, state_selected_domain, state_selected_task], 
            outputs=step_change_outputs
        )

        next_step_btn.click(
            fn=change_step, 
            inputs=[state_current_step_index, gr.State(1), state_steps_data, state_root_dir, state_selected_domain, state_selected_task], 
            outputs=step_change_outputs
        )
        
        back_to_domains_btn.click(fn=back_to_domains_fn, inputs=None, outputs=[domain_view, task_view])
        back_to_tasks_btn.click(fn=back_to_tasks_fn, inputs=[state_selected_domain], outputs=[task_view, viewer_view, task_view_title])

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
    
    # 【修改 1】: 删除了 ax1.invert_yaxis()，使Y轴正向显示
    
    # 【修改 2】: 即使共享X轴，也强制显示上子图的X轴刻度标签
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

def get_result(target_dir):
    """
    Analyzes experiment results from a target directory, calculates success rates,
    gathers action statistics, and generates plots including step distribution histograms.

    Args:
        target_dir (str): The path to the root directory of the experiment results.

    Returns:
        list or None: A list of all results (as floats), or None if no results are found.
    """
    if not os.path.exists(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.")
        return None

    # --- Data Structures for Analysis ---
    all_result = []
    domain_result_raw = {}  # Stores lists of 0s and 1s for each domain
    all_result_for_analysis = {} # For the JSON output

    # New structures for action statistics
    overall_action_counts = Counter()
    domain_action_counts = {} # {domain: Counter()}

    print("Starting analysis...")
    # --- Data Collection Loop ---
    for domain in os.listdir(target_dir):
        domain_path = os.path.join(target_dir, domain)
        if not os.path.isdir(domain_path):
            continue

        domain_action_counts[domain] = Counter()
        
        for example_id in os.listdir(domain_path):
            example_path = os.path.join(domain_path, example_id)
            if not os.path.isdir(example_path):
                continue

            result_file = os.path.join(example_path, "result.txt")
            
            # 初始化存储字典
            if domain not in all_result_for_analysis:
                all_result_for_analysis[domain] = {}
            if example_id not in all_result_for_analysis[domain]:
                all_result_for_analysis[domain][example_id] = {}

            final_result = 0.0
            if os.path.exists(result_file):
                # --- 1. Process Success/Failure Result ---
                try:
                    with open(result_file, "r") as f:
                        result_str = f.read().strip()
                    
                    try:
                        result_val = float(result_str)
                    except (ValueError, TypeError):
                        result_val = float(eval(result_str))

                    final_result = result_val

                except Exception as e:
                    print(f"Warning: Could not parse result file {result_file}. Defaulting to 0.0. Error: {e}")
                    final_result = 0.0

                if domain not in domain_result_raw:
                    domain_result_raw[domain] = []
                domain_result_raw[domain].append(final_result)
                all_result.append(final_result)
                
                all_result_for_analysis[domain][example_id]["score"] = final_result

            # --- 2. Process Trajectory for Action and Step Statistics ---
            traj_file = os.path.join(example_path, "traj.jsonl")
            if os.path.exists(traj_file):
                try:
                    total_step = 0
                    with open(traj_file, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        total_step = len(lines) # 总步数就是文件行数
                        for line in lines:
                            try:
                                data = json.loads(line)
                                # 假设 "response" 键存在于较新版本的日志中
                                if "response" in data:
                                    plan_code = data.get("response", {}).get("plan_code")
                                # 兼容旧版本，可能直接在顶层有 plan_code
                                elif "plan_code" in data:
                                    plan_code = data.get("plan_code")
                                else:
                                    plan_code = None

                                action = extract_action_from_plan(plan_code)
                                
                                if action:
                                    overall_action_counts[action] += 1
                                    domain_action_counts[domain][action] += 1
                            except (json.JSONDecodeError, AttributeError):
                                continue
                        # 记录总步数
                        all_result_for_analysis[domain][example_id]["step"] = total_step
                except Exception as e:
                    print(f"Warning: Could not read or process trajectory file {traj_file}. Error: {e}")

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
        with open(json_output_path, "w", encoding="utf-8") as f:
            json.dump(all_result_for_analysis, f, indent=4)
        print(f"\nAnalysis summary saved to {json_output_path}")
    except Exception as e:
        print(f"Error saving summary JSON: {e}")

    # --- Plotting Section ---
    print("\nGenerating plots...")

    # 横坐标：执行步数；纵坐标：
    # Plot 1: Overall Action Usage
    if overall_action_counts:
        try:
            save_path = os.path.join(target_dir, "overall_action_usage.png")
            if not os.path.exists(save_path):
                plt.figure(figsize=(12, 8))
                sorted_actions = overall_action_counts.most_common()
                actions = [item[0] for item in sorted_actions]
                counts = [item[1] for item in sorted_actions]
                
                # 捕获 bar 对象
                bars = plt.barh(actions, counts, color='skyblue')
                
                plt.xlabel('Usage Count')
                plt.ylabel('Action Type')
                plt.title('Overall Action Usage Frequency')
                plt.gca().invert_yaxis()
                
                # 【新增】为标签腾出空间，将X轴范围扩大15%
                if counts:
                    plt.xlim(right=max(counts) * 1.15)

                # 【新增】在每个条形图的末尾添加计数值
                for bar in bars:
                    xval = bar.get_width()
                    plt.text(
                        xval + (max(counts) * 0.01),  # X坐标: 条形末端再往右一点
                        bar.get_y() + bar.get_height() / 2.0, # Y坐标: 条形垂直中心
                        f' {int(xval)}({int(xval) / sum(counts):.2f}%)', # 显示的文本 (整数)
                        ha='left',      # 水平对齐: 左
                        va='center'     # 垂直对齐: 中
                    )

                plt.tight_layout()
                plt.savefig(save_path)
                plt.close()
                print(f"Saved overall action usage plot to {save_path}")
        except Exception as e:
            print(f"Error generating overall action usage plot: {e}")

    # Plot 2: Per-Domain Action Usage
    for domain, counts in domain_action_counts.items():
        if not counts:
            continue
        try:
            save_path = os.path.join(target_dir, f"action_usage_{domain}.png")
            if not os.path.exists(save_path):
                plt.figure(figsize=(10, 6))
                sorted_actions = counts.most_common()
                actions = [item[0] for item in sorted_actions]
                action_counts = [item[1] for item in sorted_actions]

                # 捕获 bar 对象
                bars = plt.barh(actions, action_counts, color='lightgreen')
                
                plt.xlabel('Usage Count')
                plt.ylabel('Action Type')
                plt.title(f'Action Usage Frequency in Domain: {domain}')
                plt.gca().invert_yaxis()

                # 【新增】为标签腾出空间，将X轴范围扩大15%
                if action_counts:
                    plt.xlim(right=max(action_counts) * 1.15)

                # 【新增】在每个条形图的末尾添加计数值
                for bar in bars:
                    xval = bar.get_width()
                    plt.text(
                        xval + (max(action_counts) * 0.01), # X坐标
                        bar.get_y() + bar.get_height() / 2.0, # Y坐标
                        f' {int(xval)}({int(xval) / sum(action_counts) * 100:.2f}%)', # 显示的文本
                        ha='left',      # 水平对齐
                        va='center'     # 垂直对齐
                    )

                plt.tight_layout()
                plt.savefig(save_path)
                plt.close()
                print(f"Saved action usage plot for domain '{domain}' to {save_path}")
        except Exception as e:
            print(f"Error generating action usage plot for domain {domain}: {e}")

    # Plot 3: Success Rate by Domain
    if domain_success_rate:
        try:
            save_path = os.path.join(target_dir, "domain_success_rates.png")
            if not os.path.exists(save_path):
                # Prepare data including the average
                domains_sorted = sorted(domain_success_rate.keys())
                rates_sorted = [domain_success_rate[d] for d in domains_sorted]
                
                # Add average rate
                plot_labels = domains_sorted + ['Average']
                plot_values = rates_sorted + [overall_rate]
                
                colors = ['#87CEEB'] * len(domains_sorted) + ['#FF6347'] # SkyBlue for domains, Tomato for Average

                plt.figure(figsize=(max(10, len(plot_labels) * 0.8), 7))
                bars = plt.bar(plot_labels, plot_values, color=colors)
                
                plt.ylabel('Success Rate (%)')
                plt.title('Success Rate by Domain and Overall Average')
                plt.xticks(rotation=45, ha='right')
                plt.ylim(0, 110) # Set y-limit to 110% for better visualization
                plt.grid(axis='y', linestyle='--', alpha=0.7)

                # Add percentage text on top of each bar
                for bar in bars:
                    yval = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f'{yval:.1f}%', ha='center', va='bottom')

                plt.tight_layout()
                plt.savefig(save_path)
                plt.close()
                print(f"Saved success rate plot to {save_path}")
        except Exception as e:
            print(f"Error generating success rate plot: {e}")

    print("\nAnalysis complete.")

        # 1. 准备数据
    step_stats = {}
    step_stats['overall'] = {'success_steps': [], 'failure_steps': []}

    for domain, tasks in all_result_for_analysis.items():
        if domain not in step_stats:
            step_stats[domain] = {'success_steps': [], 'failure_steps': []}
        
        for task_id, data in tasks.items():
            score = data.get('score')
            step = data.get('step')

            if score is not None and step is not None:
                # 定义成功：分数 > 0.5 (可以根据需要调整)
                if score > 0.0:
                    step_stats[domain]['success_steps'].append(step)
                    step_stats['overall']['success_steps'].append(step)
                else:
                    step_stats[domain]['failure_steps'].append(step)
                    step_stats['overall']['failure_steps'].append(step)

    # 2. 循环生成 N+1 张图
    for name, data in step_stats.items():
        if name == 'overall':
            title = 'Overall Task Outcome by Number of Steps'
            save_path = os.path.join(target_dir, "overall_step_distribution.png")
        else:
            title = f'Task Outcome by Number of Steps in Domain: {name}'
            save_path = os.path.join(target_dir, f"step_distribution_{name}.png")
        
        # 仅在文件不存在时生成，避免重复工作
        # if not os.path.exists(save_path):
        plot_step_histogram(
            success_steps=data['success_steps'],
            failure_steps=data['failure_steps'],
            title=title,
            save_path=save_path
        )

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
    gradio_app.launch(server_name="0.0.0.0", server_port=args.port)
