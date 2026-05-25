import os
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import gradio as gr
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

MAX_BUTTONS = 100


def load_meta(path: Path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _format_kv_tree(value: Any, prefix: str = "") -> List[str]:
    """把任意结构展平为 path: value 多行文本。"""
    lines: List[str] = []

    def walk(v: Any, path: str):
        if isinstance(v, dict):
            for k, vv in v.items():
                new_path = f"{path}.{k}" if path else k
                walk(vv, new_path)
        elif isinstance(v, list):
            for i, vv in enumerate(v):
                new_path = f"{path}[{i}]" if path else f"[{i}]"
                walk(vv, new_path)
        else:
            lines.append(f"{path}: {v}")

    walk(value, prefix)
    return lines


def _split_evaluator_items(evaluator: Any) -> List[Dict[str, str]]:
    """将 evaluator 中的 code/result/expected/desc 拆成一条条 item。"""
    if not isinstance(evaluator, dict):
        return []

    codes = evaluator.get("code") or []
    results = evaluator.get("result") or []
    expecteds = evaluator.get("expected") or []
    descs = evaluator.get("desc") or []

    if isinstance(codes, str):
        codes = [codes]
    if isinstance(results, dict):
        results = [results]
    if isinstance(expecteds, dict):
        expecteds = [expecteds]
    if isinstance(descs, str):
        descs = [descs]

    max_len = max(
        len(codes),
        len(results),
        len(expecteds),
        len(descs),
    )

    items: List[Dict[str, str]] = []
    for i in range(max_len):
        code = codes[i] if i < len(codes) else ""
        result_val = results[i] if i < len(results) else None
        expected_val = expecteds[i] if i < len(expecteds) else None
        desc = descs[i] if i < len(descs) else ""

        result_text = "\n".join(_format_kv_tree(result_val, prefix=f"result[{i}]") or [])
        expected_text = "\n".join(_format_kv_tree(expected_val, prefix=f"expected[{i}]") or [])

        items.append(
            {
                "code": str(code or ""),
                "result": result_text,
                "expected": expected_text,
                "desc": str(desc or ""),
            }
        )

    return items


def draw_coordinate_on_image(img_path: Path, coordinate) -> Path:
    """在截图上根据 coordinate 画一个红色叉号并返回新文件路径。"""
    if not coordinate:
        return img_path

    x, y = coordinate
    img = Image.open(img_path).convert("RGB")
    width, height = img.width, img.height
    x, y = x / 1000.0 * width, y / 1000.0 * height
    draw = ImageDraw.Draw(img)

    size = 10
    color = (255, 0, 0)
    draw.line((x - size, y - size, x + size, y + size), fill=color, width=3)
    draw.line((x - size, y + size, x + size, y - size), fill=color, width=3)

    annotated_path = img_path.with_name(img_path.stem + "_coord.png")
    img.save(annotated_path)
    return annotated_path


def scan_results_root(root_dir: str) -> Dict[str, List[Path]]:
    """扫描 oscaliber_results 结构，返回 {domain: [meta_json_path, ...]}"""
    root = Path(root_dir)
    domain_map: Dict[str, List[Path]] = {}

    if not root.exists():
        return domain_map

    for domain_dir in root.iterdir():
        if not domain_dir.is_dir():
            continue
        metas = list(domain_dir.glob("meta_*.json"))
        if not metas:
            continue
        domain_map[domain_dir.name] = sorted(metas)
    return domain_map


def calc_stats(domain_map: Dict[str, List[Path]]) -> Tuple[str, Dict[str, List[Dict]]]:
    """计算每个 domain 和 overall 的正确率（score 为准）以及步数分布数据。"""
    stats_markdown_lines: List[str] = []
    step_data: Dict[str, List[Dict]] = {}

    total_tasks = 0
    total_vlm_tasks = 0
    total_rule_tasks = 0
    total_correct = 0.0
    total_rule_correct = 0.0
    total_vlm_correct = 0.0

    stats_markdown_lines.append("### 全局统计 (以 score 为准)")
    stats_markdown_lines.append("")
    stats_markdown_lines.append("| Domain | 任务数 | 正确率(%) | VLM 正确率(%) | Rule-Base 正确率(%) |")
    stats_markdown_lines.append("|--------|--------|-----------|-----------|-----------|")

    for domain, metas in sorted(domain_map.items()):
        domain_scores: List[float] = []
        domain_steps: List[int] = []
        domain_vlm_scores = []
        domain_rule_scores = []
        for meta_path in metas:
            meta = load_meta(meta_path)
            score = float(meta.get("score", 0))
            vlm_score = float(meta.get("model_judge", {}).get("binary_reward", -1))
            rule_score = float(meta.get("rule_judge", {}).get("reward", -1))
            traj_len = int(meta.get("trajectory_length", len(meta.get("trajectory", []))))
            domain_scores.append(score)
            domain_steps.append(traj_len)
            if vlm_score != -1:
                domain_vlm_scores.append(vlm_score)
            if rule_score != -1:
                domain_rule_scores.append(rule_score)
            if "overall" not in step_data:
                step_data["overall"] = []
            if domain not in step_data:
                step_data[domain] = []
            step_success = rule_score >= 1 or vlm_score >= 1
            step_data["overall"].append({"success": step_success, "step": traj_len})
            step_data[domain].append({"success": step_success, "step": traj_len})

        n = len(domain_scores)
        if n == 0:
            continue
        domain_acc = sum(domain_scores) / n * 100.0
        # 统计时去除那些不含对应评测的任务
        domain_vlm_acc = sum(domain_vlm_scores) / len(domain_vlm_scores) * 100.0 if len(domain_vlm_scores) != 0 else -1
        domain_rule_acc = sum(domain_rule_scores) / len(domain_rule_scores) * 100.0 if len(domain_rule_scores) != 0 else -1
        total_tasks += n
        total_vlm_tasks += len(domain_vlm_scores)
        total_rule_tasks += len(domain_rule_scores)
        total_correct += sum(domain_scores)
        total_rule_correct += sum(domain_rule_scores)
        total_vlm_correct += sum(domain_vlm_scores)

        stats_markdown_lines.append(f"| {domain} | {n} | {domain_acc:.2f} | {domain_vlm_acc:.2f} | {domain_rule_acc:.2f} |")

    overall_rate = (total_correct / total_tasks * 100.0) if total_tasks > 0 else -1
    overall_vlm_rate = (total_vlm_correct / total_vlm_tasks * 100.0) if total_vlm_tasks > 0 else -1
    overall_rule_rate = (total_rule_correct / total_rule_tasks * 100.0) if total_rule_tasks > 0 else -1
    stats_markdown_lines.append(f"| **Overall** | {total_tasks} | {overall_rate:.2f} | {overall_vlm_rate:.2f} | {overall_rule_rate:.2f} |")
    # print(stats_markdown_lines)
    return "\n".join(stats_markdown_lines), step_data


def plot_step_histogram(step_data: Dict[str, List[Dict]], save_root: Path) -> None:
    """按照 rule 或 vlm 是否达到阈值 1 把任务划分为 success 和 failure，绘制步数直方图。"""
    for name, items in step_data.items():
        success_steps = [it["step"] for it in items if it.get("success", False)]
        failure_steps = [it["step"] for it in items if not it.get("success", False)]

        if not success_steps and not failure_steps:
            continue

        fig, ax = plt.subplots(figsize=(8, 4))
        bins = range(1, max(success_steps + failure_steps) + 2)

        if success_steps:
            ax.hist(success_steps, bins=bins, alpha=0.7, label="Success", color="mediumseagreen")
        if failure_steps:
            ax.hist(failure_steps, bins=bins, alpha=0.7, label="Failure", color="tomato")

        ax.set_xlabel("Number of Steps")
        ax.set_ylabel("Task Count")
        ax.set_title("Step Distribution - {}".format("Overall" if name == "overall" else name))
        ax.legend()
        plt.tight_layout()

        out_path = save_root / ("overall_step_distribution.png" if name == "overall" else f"step_distribution_{name}.png")
        fig.savefig(out_path)
        plt.close(fig)


def create_os_caliber_app(root_dir: str, task_meta_dir: str):
    """基于 oscaliber meta_json 的 Gradio 可视化。"""
    domain_map = scan_results_root(root_dir)
    stats_md, step_data = calc_stats(domain_map)

    # 生成一次步长直方图
    plot_step_histogram(step_data, Path(root_dir))

    domains = sorted(domain_map.keys())

    with gr.Blocks(theme=gr.themes.Soft()) as app:
        state_root_dir = gr.State(root_dir)
        state_domain_map = gr.State(domain_map)
        state_selected_domain = gr.State()
        state_selected_meta_list = gr.State([])
        state_selected_meta_idx = gr.State(0)
        state_current_meta = gr.State()
        state_current_step_idx = gr.State(0)
        state_task_meta_dir = gr.State(task_meta_dir)

        with gr.Column(visible=True) as domain_view:
            gr.Markdown(f"# OS-Caliber 结果浏览器 ({os.path.basename(root_dir)})")
            global_stats_display = gr.Markdown(stats_md)

            with gr.Row():
                overall_step_img = gr.Image(
                    label="整体步数分布",
                    value=str(Path(root_dir) / "overall_step_distribution.png"),
                    type="filepath",
                    interactive=False,
                )

            gr.Markdown("### 选择 Domain:")
            with gr.Group():
                domain_buttons = []
                for i in range(MAX_BUTTONS):
                    btn = gr.Button(visible=False)
                    domain_buttons.append(btn)

            for i, d in enumerate(domains):
                if i < MAX_BUTTONS:
                    domain_buttons[i].value = d
                    domain_buttons[i].visible = True

        with gr.Column(visible=False) as task_view:
            task_view_title = gr.Markdown("# 请选择一个任务")
            domain_stats_md = gr.Markdown("")

            with gr.Row():
                back_to_domains_btn = gr.Button("⬅️ 返回 Domain 选择")

            with gr.Row():
                domain_step_img = gr.Image(
                    label="Domain 步数分布",
                    type="filepath",
                    interactive=False,
                )

            with gr.Group():
                task_buttons = []
                score_labels = []
                for i in range(MAX_BUTTONS):
                    with gr.Row():
                        btn = gr.Button(visible=False)
                        lab = gr.Button(visible=False, interactive=False)
                    task_buttons.append(btn)
                    score_labels.append(lab)

        with gr.Column(visible=False) as viewer_view:
            viewer_title = gr.Markdown("# 任务详情")
            with gr.Row():
                back_to_tasks_btn = gr.Button("⬅️ 返回 Task 选择")

            # 任务整体三个得分
            score_md = gr.Markdown("")

            step_counter = gr.Markdown("步骤 1 / N")
            with gr.Row():
                prev_step_btn = gr.Button("◀️ 上一步")
                next_step_btn = gr.Button("▶️ 下一步")

            with gr.Row():
                with gr.Column(scale=3):
                    screenshot_img = gr.Image(label="步骤截图", type="filepath", interactive=False)
                with gr.Column(scale=2):
                    raw_resp_box = gr.Textbox(label="raw_response", lines=6, interactive=False)
                    thought_box = gr.Textbox(label="thought", lines=6, interactive=False)
                    action_box = gr.Textbox(label="action", lines=4, interactive=False)

            # evaluator 展示（直接展示全部条目拼接）
            with gr.Row():
                with gr.Column(scale=2):
                    evaluator_desc_box = gr.TextArea(
                        label="evaluator desc",
                        interactive=False,
                        lines=8,
                    )
                with gr.Column(scale=3):
                    evaluator_code_box = gr.Code(
                        label="evaluator code (Python)",
                        language="python",
                        interactive=False,
                        lines=16,
                    )
                with gr.Column(scale=2):
                    evaluator_result_box = gr.TextArea(
                        label="evaluator result",
                        interactive=False,
                        lines=8,
                    )
                    evaluator_expected_box = gr.TextArea(
                        label="evaluator expected",
                        interactive=False,
                        lines=8,
                    )

        # ======================== 逻辑函数 ========================

        def on_select_domain(domain_name, domain_map, root_dir):
            metas: List[Path] = domain_map.get(domain_name, [])
            updates = {
                state_selected_domain: domain_name,
                state_selected_meta_list: metas,
                state_selected_meta_idx: 0,
                domain_view: gr.update(visible=False),
                task_view: gr.update(visible=True),
                task_view_title: gr.update(value=f"# Domain: {domain_name}"),
            }

            # domain 统计：只显示该 domain 步长图
            domain_step_path = Path(root_dir) / f"step_distribution_{domain_name}.png"
            updates[domain_stats_md] = gr.update(value=f"### {domain_name} 共有 {len(metas)} 个任务")
            updates[domain_step_img] = gr.update(value=str(domain_step_path) if domain_step_path.exists() else None)

            for i in range(MAX_BUTTONS):
                if i < len(metas):
                    meta = load_meta(metas[i])
                    task_id = meta.get("task_id") or meta.get("trace_id")
                    score = float(meta.get("score", 0))
                    vlm_score = float(meta.get("model_judge", {}).get("binary_reward", -1))
                    rule_score = float(meta.get("rule_judge", {}).get("reward", -1))
                    traj_len = int(meta.get("trajectory_length", len(meta.get("trajectory", []))))
                    v_str = f"{vlm_score:.2f}" if vlm_score != -1 else "NA"
                    r_str = f"{rule_score:.2f}" if rule_score != -1 else "NA"
                    score_text = f"Step: {traj_len} | Score: {score:.2f} (Rule: {r_str}, VLM: {v_str})"
                    updates[task_buttons[i]] = gr.update(value=str(task_id), visible=True)
                    updates[score_labels[i]] = gr.update(value=score_text, visible=True)
                else:
                    updates[task_buttons[i]] = gr.update(visible=False)
                    updates[score_labels[i]] = gr.update(visible=False)

            return updates

        def on_select_task(btn_label, selected_domain, meta_list, task_meta_dir):
            # btn_label 是 task_id，但 meta_list 储存的是路径，只按顺序索引
            if not meta_list:
                return {}
            # 找到 index
            idx = 0
            for i, p in enumerate(meta_list):
                m = load_meta(p)
                if str(m.get("task_id")) == str(btn_label) or str(m.get("trace_id")) == str(btn_label):
                    idx = i
                    break

            meta_path = meta_list[idx]
            meta = load_meta(meta_path)

            score = float(meta.get("score", 0))
            mj = meta.get("model_judge", {}) or {}
            rj = meta.get("rule_judge", {}) or {}
            binary_reward = mj.get("binary_reward", 0)
            rationale = mj.get("rationale", "")
            rule_reward = rj.get("reward", 0)

            score_text = (
                f"### 任务评分\n"
                f"- model_judge.binary_reward = {binary_reward}\n"
                f"- rule_judge.reward = {rule_reward}\n"
                f"- score = {score}\n\n"
                f"#### model_judge.rationale\n{rationale}"
            )

            # 读取 task_meta_dir 下的任务说明 evaluator
            task_id = meta.get("task_id") or meta.get("trace_id")
            evaluator_desc = ""
            evaluator_result = ""
            evaluator_code = ""
            evaluator_expected = ""

            if task_id and task_meta_dir and selected_domain:
                tmeta_path = Path(task_meta_dir) / selected_domain / f"{task_id}.json"
                if tmeta_path.exists():
                    with open(tmeta_path, "r", encoding="utf-8") as f:
                        task_meta = json.load(f)
                    evaluator = task_meta.get("evaluator")
                    items = _split_evaluator_items(evaluator)
                    if items:
                        sep = "\n\n---\n\n"
                        evaluator_desc = sep.join(it.get("desc", "") for it in items)
                        evaluator_result = sep.join(it.get("result", "") for it in items)
                        evaluator_code = sep.join(it.get("code", "") for it in items)
                        evaluator_expected = sep.join(it.get("expected", "") for it in items)

            traj = meta.get("trajectory", []) or []

            updates = {
                state_current_meta: meta,
                state_current_step_idx: 0,
                task_view: gr.update(visible=False),
                viewer_view: gr.update(visible=True),
                viewer_title: gr.update(value=f"## Task: {meta.get('instruction')} ({meta.get('task_id')})"),
                score_md: gr.update(value=score_text),
                evaluator_desc_box: gr.update(value=evaluator_desc),
                evaluator_result_box: gr.update(value=evaluator_result),
                evaluator_code_box: gr.update(value=evaluator_code),
                evaluator_expected_box: gr.update(value=evaluator_expected),
            }

            if not traj:
                updates.update({
                    step_counter: "没有轨迹",
                    screenshot_img: None,
                    raw_resp_box: "",
                    thought_box: "",
                    action_box: "",
                    prev_step_btn: gr.update(interactive=False),
                    next_step_btn: gr.update(interactive=False),
                })
            else:
                step_updates = _show_step(meta, 0, root_dir, domain=selected_domain)
                updates.update(step_updates)

            return updates

        def _show_step(meta: Dict, idx: int, root_dir: str, domain: str):
            traj = meta.get("trajectory", []) or []
            n = len(traj)
            if not (0 <= idx < n):
                idx = 0

            step = traj[idx]
            img_rel = step.get("screenshot_path")
            coordinate = step.get("coordinate")
            img_path = Path(root_dir) / Path(domain) / img_rel if img_rel else None

            if img_path and img_path.exists():
                if coordinate:
                    img_path = draw_coordinate_on_image(img_path, coordinate)
                img_val = str(img_path)
            else:
                img_val = None

            raw_resp = step.get("raw_response", "")
            thought = step.get("thought", "")
            action = step.get("action", "")

            updates = {
                step_counter: gr.update(value=f"步骤 {idx + 1} / {n}"),
                screenshot_img: gr.update(value=img_val),
                raw_resp_box: gr.update(value=raw_resp),
                thought_box: gr.update(value=thought),
                action_box: gr.update(value=action),
                prev_step_btn: gr.update(interactive=idx > 0),
                next_step_btn: gr.update(interactive=idx < n - 1),
            }
            return updates

        def on_change_step(cur_idx, delta, meta, root_dir, selected_domain):
            traj = meta.get("trajectory", []) or []
            n = len(traj)
            if n == 0:
                return {state_current_step_idx: 0}
            new_idx = cur_idx + delta
            if new_idx < 0 or new_idx >= n:
                new_idx = cur_idx
            updates = _show_step(meta, new_idx, root_dir, domain=selected_domain)
            updates[state_current_step_idx] = new_idx
            return updates

        def back_to_domains(root_dir):
            domain_map = scan_results_root(root_dir)
            stats_md, step_data = calc_stats(domain_map)
            plot_step_histogram(step_data, Path(root_dir))
            return {
                domain_view: gr.update(visible=True),
                task_view: gr.update(visible=False),
                viewer_view: gr.update(visible=False),
                global_stats_display: gr.update(value=stats_md),
                overall_step_img: gr.update(value=str(Path(root_dir) / "overall_step_distribution.png")),
            }

        def back_to_tasks(selected_domain, domain_map, root_dir):
            metas: List[Path] = domain_map.get(selected_domain, [])
            updates = {
                viewer_view: gr.update(visible=False),
                task_view: gr.update(visible=True),
                task_view_title: gr.update(value=f"# Domain: {selected_domain}"),
            }
            domain_step_path = Path(root_dir) / f"step_distribution_{selected_domain}.png"
            updates[domain_stats_md] = gr.update(value=f"### {selected_domain} 共有 {len(metas)} 个任务")
            updates[domain_step_img] = gr.update(value=str(domain_step_path) if domain_step_path.exists() else None)

            for i in range(MAX_BUTTONS):
                if i < len(metas):
                    meta = load_meta(metas[i])
                    task_id = meta.get("task_id") or meta.get("trace_id")
                    score = float(meta.get("score", 0))
                    vlm_score = float(meta.get("model_judge", {}).get("binary_reward", -1))
                    rule_score = float(meta.get("rule_judge", {}).get("reward", -1))
                    traj_len = int(meta.get("trajectory_length", len(meta.get("trajectory", []))))
                    v_str = f"{vlm_score:.2f}" if vlm_score != -1 else "NA"
                    r_str = f"{rule_score:.2f}" if rule_score != -1 else "NA"
                    score_text = f"Step: {traj_len} | Score: {score:.2f} (Rule: {r_str}, VLM: {v_str})"
                    updates[task_buttons[i]] = gr.update(value=str(task_id), visible=True)
                    updates[score_labels[i]] = gr.update(value=score_text, visible=True)
                else:
                    updates[task_buttons[i]] = gr.update(visible=False)
                    updates[score_labels[i]] = gr.update(visible=False)

            return updates


        # 事件绑定
        domain_click_outputs = [
            state_selected_domain,
            state_selected_meta_list,
            state_selected_meta_idx,
            domain_view,
            task_view,
            task_view_title,
            domain_stats_md,
            domain_step_img,
        ] + task_buttons + score_labels

        for btn in domain_buttons:
            btn.click(
                fn=on_select_domain,
                inputs=[btn, state_domain_map, state_root_dir],
                outputs=domain_click_outputs,
            )

        task_click_outputs = [
            state_current_meta,
            state_current_step_idx,
            task_view,
            viewer_view,
            viewer_title,
            score_md,
            step_counter,
            screenshot_img,
            raw_resp_box,
            thought_box,
            action_box,
            prev_step_btn,
            next_step_btn,
            evaluator_desc_box,
            evaluator_result_box,
            evaluator_code_box,
            evaluator_expected_box,
        ]

        for btn in task_buttons:
            btn.click(
                fn=on_select_task,
                inputs=[btn, state_selected_domain, state_selected_meta_list, state_task_meta_dir],
                outputs=task_click_outputs,
            )

        step_click_outputs = [
            state_current_step_idx,
            step_counter,
            screenshot_img,
            raw_resp_box,
            thought_box,
            action_box,
            prev_step_btn,
            next_step_btn,
        ]

        prev_step_btn.click(
            fn=on_change_step,
            inputs=[state_current_step_idx, gr.State(-1), state_current_meta, state_root_dir, state_selected_domain],
            outputs=step_click_outputs,
        )
        next_step_btn.click(
            fn=on_change_step,
            inputs=[state_current_step_idx, gr.State(1), state_current_meta, state_root_dir, state_selected_domain],
            outputs=step_click_outputs,
        )

        back_to_domains_btn.click(
            fn=back_to_domains,
            inputs=[state_root_dir],
            outputs=[domain_view, task_view, viewer_view, global_stats_display, overall_step_img],
        )

        back_to_tasks_btn.click(
            fn=back_to_tasks,
            inputs=[state_selected_domain, state_domain_map, state_root_dir],
            outputs=[viewer_view, task_view, task_view_title, domain_stats_md, domain_step_img] + task_buttons + score_labels,
        )

    return app


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir", type=str, required=True)
    parser.add_argument("--task_meta_dir", type=str, default="/nvme/yangbowen/yangbowen/OSSymphony/evaluation_examples/ubuntu_online_rollout/synthesis/oscaliber_os-caliber-gemini-3.1-pro-preview-generate-600-0325")
    parser.add_argument("--port", type=int, default=12888)
    args = parser.parse_args()

    app = create_os_caliber_app(args.root_dir, args.task_meta_dir)
    app.launch(server_name="0.0.0.0", server_port=args.port, allowed_paths=["/nvme/yangbowen/"])
