"""
给定 root_dir (支持动态配置), e.g.
    /nvme/yangbowen/yangbowen/OSSymphony/evaluation_examples/ubuntu_online_rollout/synthesis/oscaliber_os-caliber-gpt-5-generate-0322-1_20260322_184604
里面每个子文件夹都是一个 domain, domain 文件夹下都是 .json 的任务文件。
可视化界面解析并展示每个任务 json 的核心字段, 需要展示:
    "id", "related_apps", "instruction", "complexity", "estimated_steps", "category", "evaluator"
注意 evaluator 里面的 func, code 等字段可能是列表形式, 需要依次展示。
其中 code 是 str python 代码, 你需要转成人类可视的格式。
这份脚本目的是可视化查看生成的任务情况。
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import gradio as gr


CORE_FIELDS = [
    "id",
    "related_apps",
    "instruction",
    "complexity",
    "estimated_steps",
    "category",
    "evaluator",
]


def _safe_read_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"__error__": f"Failed to read {path}: {e}"}


def list_domains(root_dir: str) -> List[str]:
    if not root_dir:
        return []
    p = Path(root_dir)
    if not p.exists() or not p.is_dir():
        return []
    domains = [d.name for d in p.iterdir() if d.is_dir()]
    domains.sort()
    return domains


def list_tasks(root_dir: str, domain: str) -> List[str]:
    if not root_dir or not domain:
        return []
    domain_path = Path(root_dir) / domain
    if not domain_path.exists() or not domain_path.is_dir():
        return []
    tasks = [f.name for f in domain_path.glob("*.json") if f.is_file()]
    tasks.sort()
    return tasks


# ---------- evaluator 条目拆分 ----------

EvaluatorItem = Dict[str, str]


def _format_kv_tree(value: Any, prefix: str = "") -> List[str]:
    """把任意嵌套结构展开为 path: value 的多行文本。"""
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


def _split_evaluator_items(evaluator: Any) -> List[EvaluatorItem]:
    """按照 index 把 func/code/result/expected/desc 聚合成条目列表。"""
    if not isinstance(evaluator, dict):
        return []

    funcs = evaluator.get("func") or []
    codes = evaluator.get("code") or []
    results = evaluator.get("result") or []
    expecteds = evaluator.get("expected") or []
    descs = evaluator.get("desc") or []

    # 支持单个字符串/对象的情况，统一转成 list
    if isinstance(funcs, str):
        funcs = [funcs]
    if isinstance(codes, str):
        codes = [codes]
    if isinstance(results, dict):
        results = [results]
    if isinstance(expecteds, dict):
        expecteds = [expecteds]
    if isinstance(descs, str):
        descs = [descs]

    max_len = max(
        len(funcs),
        len(codes),
        len(results),
        len(expecteds),
        len(descs),
    )
    items: List[EvaluatorItem] = []

    for i in range(max_len):
        func = funcs[i] if i < len(funcs) else ""
        code = codes[i] if i < len(codes) else ""
        result_val = results[i] if i < len(results) else None
        expected_val = expecteds[i] if i < len(expecteds) else None
        desc = descs[i] if i < len(descs) else ""

        result_text = "\n".join(_format_kv_tree(result_val, prefix=f"result[{i}]") or [])
        expected_text = "\n".join(
            _format_kv_tree(expected_val, prefix=f"expected[{i}]") or []
        )

        items.append(
            {
                "func": str(func or ""),
                "code": str(code or ""),
                "result": result_text,
                "expected": expected_text,
                "desc": str(desc or ""),
            }
        )

    return items


def _flatten_evaluator_meta(evaluator: Any) -> str:
    """把 evaluator 里除 func/code/result/expected/desc 外的剩余字段，展平为 meta 文本。"""
    if not isinstance(evaluator, dict):
        return ""

    rest = {
        k: v
        for k, v in evaluator.items()
        if k not in {"func", "code", "result", "expected", "desc"}
    }
    lines = _format_kv_tree(rest, prefix="evaluator")
    return "\n".join(lines)


def load_task(
    root_dir: str, domain: str, task_file: str
) -> Tuple[
    str,  # id
    str,  # domain
    str,  # related_apps
    str,  # instruction
    str,  # complexity
    str,  # estimated_steps
    str,  # category
    str,  # evaluator_meta
    str,  # evaluator_items_json
]:
    if not (root_dir and domain and task_file):
        return ("",) * 9

    path = Path(root_dir) / domain / task_file
    data = _safe_read_json(path)

    if "__error__" in data:
        err = data["__error__"]
        return err, domain, "", "", "", "", "", "", "[]"

    def get_field(name: str) -> Any:
        return data.get(name, "")

    task_id = str(get_field("id") or "")
    related_apps = get_field("related_apps")
    if isinstance(related_apps, list):
        related_apps_str = ", ".join(map(str, related_apps))
    else:
        related_apps_str = str(related_apps or "")

    instruction = str(get_field("instruction") or "")
    complexity = str(get_field("complexity") or "")
    estimated_steps = str(get_field("estimated_steps") or "")
    category = str(get_field("category") or "")

    evaluator = get_field("evaluator")
    evaluator_meta = _flatten_evaluator_meta(evaluator)
    evaluator_items = _split_evaluator_items(evaluator)
    evaluator_items_json = json.dumps(evaluator_items, ensure_ascii=False)

    return (
        task_id,
        domain,
        related_apps_str,
        instruction,
        complexity,
        estimated_steps,
        category,
        evaluator_meta,
        evaluator_items_json,
    )


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Synthesis Instruction Viewer") as demo:
        gr.Markdown(
            """
# 任务合成结果查看器

- 在左侧输入根目录 `root_dir`，会自动加载第一个 domain 的第一个 task
- 可以通过下拉框手动选择 domain 和 task
- 也可以使用上一条/下一条按钮在任务间快速翻页
- evaluator 的每一条 (func+code+result+expected) 可通过下拉框单独查看
            """.strip()
        )

        with gr.Row():
            with gr.Column(scale=1):
                root_dir = gr.Textbox(
                    label="root_dir",
                    placeholder="输入包含各个 domain 子目录的根目录路径",
                    lines=2,
                )
                init_btn = gr.Button("加载 root_dir 并跳到第一个任务")

                domain_dropdown = gr.Dropdown(
                    label="domain (子文件夹)",
                    choices=[],
                    interactive=True,
                )
                task_dropdown = gr.Dropdown(
                    label="任务 JSON 文件",
                    choices=[],
                    interactive=True,
                )

                with gr.Row():
                    prev_btn = gr.Button("上一条")
                    next_btn = gr.Button("下一条")

                current_domain_index = gr.Number(
                    label="_domain_index", value=0, visible=False
                )
                current_task_index = gr.Number(
                    label="_task_index", value=0, visible=False
                )

            with gr.Column(scale=3):
                id_box = gr.Textbox(label="id", interactive=False)
                domain_box = gr.Textbox(label="domain", interactive=False)
                related_apps_box = gr.Textbox(
                    label="related_apps", interactive=False
                )
                instruction_box = gr.TextArea(
                    label="instruction",
                    interactive=False,
                    lines=4,
                )

                with gr.Row():
                    complexity_box = gr.Textbox(
                        label="complexity", interactive=False
                    )
                    estimated_steps_box = gr.Textbox(
                        label="estimated_steps", interactive=False
                    )
                    category_box = gr.Textbox(
                        label="category", interactive=False
                    )

                evaluator_meta_box = gr.TextArea(
                    label="evaluator 其他字段 (meta)",
                    interactive=False,
                    lines=6,
                )

                evaluator_items_state = gr.Textbox(
                    label="_evaluator_items_json",
                    visible=False,
                )
                evaluator_item_index = gr.Number(
                    label="_evaluator_item_index", value=0, visible=False
                )
                evaluator_item_dropdown = gr.Dropdown(
                    label="当前 evaluator 条目",
                    choices=[],
                    value=None,
                    interactive=True,
                )

                evaluator_desc_box = gr.TextArea(
                    label="desc",
                    interactive=False,
                    lines=4,
                )
                with gr.Row():
                    evaluator_func_box = gr.TextArea(
                        label="func",
                        interactive=False,
                        lines=4,
                    )
                    evaluator_result_box = gr.TextArea(
                        label="result",
                        interactive=False,
                        lines=8,
                    )
                with gr.Row():
                    evaluator_code_box = gr.Code(
                        label="code (Python)",
                        language="python",
                        interactive=False,
                    )
                    evaluator_expected_box = gr.TextArea(
                        label="expected",
                        interactive=False,
                        lines=8,
                    )

        # ---------- 后端逻辑 ----------

        def _load_and_first_item(root_dir_val: str, domain: str, task: str):
            (
                task_id,
                domain_name,
                related_apps_str,
                instruction,
                complexity,
                estimated_steps,
                category,
                evaluator_meta,
                evaluator_items_json,
            ) = load_task(root_dir_val, domain, task)

            try:
                items = json.loads(evaluator_items_json or "[]")
            except Exception:
                items = []

            if items:
                item0 = items[0]
                func = item0.get("func", "")
                code = item0.get("code", "")
                result = item0.get("result", "")
                expected = item0.get("expected", "")
                desc = item0.get("desc", "")
                choices = [f"item {i}" for i in range(len(items))]
            else:
                func = code = result = expected = desc = ""
                choices = []

            return (
                task_id,
                domain_name,
                related_apps_str,
                instruction,
                complexity,
                estimated_steps,
                category,
                evaluator_meta,
                evaluator_items_json,
                0,
                gr.Dropdown(choices=choices, value="item 0" if choices else None),
                desc,
                func,
                result,
                code,
                expected,
            )

        def init_from_root(root_dir_val: str):
            domains = list_domains(root_dir_val)
            if not domains:
                empty_dd = gr.Dropdown(choices=[], value=None)
                return (
                    empty_dd,
                    empty_dd,
                    0,
                    0,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "[]",
                    0,
                    gr.Dropdown(choices=[], value=None),
                    "",
                    "",
                    "",
                    "",
                )

            domain = domains[0]
            tasks = list_tasks(root_dir_val, domain)
            if not tasks:
                task_dd = gr.Dropdown(choices=[], value=None)
                return (
                    gr.Dropdown(choices=domains, value=domain),
                    task_dd,
                    0,
                    0,
                    "",
                    domain,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "[]",
                    0,
                    gr.Dropdown(choices=[], value=None),
                    "",
                    "",
                    "",
                    "",
                )

            task = tasks[0]
            (
                task_id,
                domain_name,
                related_apps_str,
                instruction,
                complexity,
                estimated_steps,
                category,
                evaluator_meta,
                evaluator_items_json,
                item_index,
                item_dropdown,
                desc,
                func,
                result,
                code,
                expected,
            ) = _load_and_first_item(root_dir_val, domain, task)

            return (
                gr.Dropdown(choices=domains, value=domain),
                gr.Dropdown(choices=tasks, value=task),
                0,
                0,
                task_id,
                domain_name,
                related_apps_str,
                instruction,
                complexity,
                estimated_steps,
                category,
                evaluator_meta,
                evaluator_items_json,
                item_index,
                item_dropdown,
                desc,
                func,
                result,
                code,
                expected,
            )

        init_btn.click(
            fn=init_from_root,
            inputs=[root_dir],
            outputs=[
                domain_dropdown,
                task_dropdown,
                current_domain_index,
                current_task_index,
                id_box,
                domain_box,
                related_apps_box,
                instruction_box,
                complexity_box,
                estimated_steps_box,
                category_box,
                evaluator_meta_box,
                evaluator_items_state,
                evaluator_item_index,
                evaluator_item_dropdown,
                evaluator_desc_box,
                evaluator_func_box,
                evaluator_result_box,
                evaluator_code_box,
                evaluator_expected_box,
            ],
        )

        def on_domain_change(root_dir_val: str, domain_val: str):
            domains = list_domains(root_dir_val)
            tasks = list_tasks(root_dir_val, domain_val)
            domain_idx = domains.index(domain_val) if domain_val in domains else 0
            if tasks:
                task = tasks[0]
                (
                    task_id,
                    domain_name,
                    related_apps_str,
                    instruction,
                    complexity,
                    estimated_steps,
                    category,
                    evaluator_meta,
                    evaluator_items_json,
                    item_index,
                    item_dropdown,
                    desc,
                    func,
                    result,
                    code,
                    expected,
                ) = _load_and_first_item(root_dir_val, domain_val, task)
            else:
                task = None
                (
                    task_id,
                    domain_name,
                    related_apps_str,
                    instruction,
                    complexity,
                    estimated_steps,
                    category,
                    evaluator_meta,
                    evaluator_items_json,
                    item_index,
                    item_dropdown,
                    desc,
                    func,
                    result,
                    code,
                    expected,
                ) = (
                    "",
                    domain_val,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "[]",
                    0,
                    gr.Dropdown(choices=[], value=None),
                    "",
                    "",
                    "",
                    "",
                )

            return (
                gr.Dropdown(choices=domains, value=domain_val),
                gr.Dropdown(choices=tasks, value=task),
                domain_idx,
                0,
                task_id,
                domain_name,
                related_apps_str,
                instruction,
                complexity,
                estimated_steps,
                category,
                evaluator_meta,
                evaluator_items_json,
                item_index,
                item_dropdown,
                desc,
                func,
                result,
                code,
                expected,
            )

        domain_dropdown.change(
            fn=on_domain_change,
            inputs=[root_dir, domain_dropdown],
            outputs=[
                domain_dropdown,
                task_dropdown,
                current_domain_index,
                current_task_index,
                id_box,
                domain_box,
                related_apps_box,
                instruction_box,
                complexity_box,
                estimated_steps_box,
                category_box,
                evaluator_meta_box,
                evaluator_items_state,
                evaluator_item_index,
                evaluator_item_dropdown,
                evaluator_desc_box,
                evaluator_func_box,
                evaluator_result_box,
                evaluator_code_box,
                evaluator_expected_box,
            ],
        )

        def on_task_change(root_dir_val: str, domain_val: str, task_val: str):
            domains = list_domains(root_dir_val)
            tasks = list_tasks(root_dir_val, domain_val)
            domain_idx = domains.index(domain_val) if domain_val in domains else 0
            task_idx = tasks.index(task_val) if task_val in tasks else 0

            (
                task_id,
                domain_name,
                related_apps_str,
                instruction,
                complexity,
                estimated_steps,
                category,
                evaluator_meta,
                evaluator_items_json,
                item_index,
                item_dropdown,
                desc,
                func,
                result,
                code,
                expected,
            ) = _load_and_first_item(root_dir_val, domain_val, task_val)

            return (
                domain_idx,
                task_idx,
                task_id,
                domain_name,
                related_apps_str,
                instruction,
                complexity,
                estimated_steps,
                category,
                evaluator_meta,
                evaluator_items_json,
                item_index,
                item_dropdown,
                desc,
                func,
                result,
                code,
                expected,
            )

        task_dropdown.change(
            fn=on_task_change,
            inputs=[root_dir, domain_dropdown, task_dropdown],
            outputs=[
                current_domain_index,
                current_task_index,
                id_box,
                domain_box,
                related_apps_box,
                instruction_box,
                complexity_box,
                estimated_steps_box,
                category_box,
                evaluator_meta_box,
                evaluator_items_state,
                evaluator_item_index,
                evaluator_item_dropdown,
                evaluator_desc_box,
                evaluator_func_box,
                evaluator_result_box,
                evaluator_code_box,
                evaluator_expected_box,
            ],
        )

        def step_task(
            root_dir_val: str,
            domain_val: str,
            domain_idx_val: float,
            task_idx_val: float,
            direction: str,
        ):
            domains = list_domains(root_dir_val)
            if not domains:
                return (
                    0,
                    0,
                    gr.Dropdown(choices=[], value=None),
                    gr.Dropdown(choices=[], value=None),
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "[]",
                    0,
                    gr.Dropdown(choices=[], value=None),
                    "",
                    "",
                    "",
                    "",
                )

            domain_idx = int(domain_idx_val)
            task_idx = int(task_idx_val)

            if domain_val not in domains:
                domain_idx = 0
                domain_val = domains[0]

            tasks = list_tasks(root_dir_val, domain_val)
            if not tasks:
                return (
                    domain_idx,
                    0,
                    gr.Dropdown(choices=domains, value=domain_val),
                    gr.Dropdown(choices=[], value=None),
                    "",
                    domain_val,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "[]",
                    0,
                    gr.Dropdown(choices=[], value=None),
                    "",
                    "",
                    "",
                    "",
                )

            if direction == "next":
                task_idx += 1
                if task_idx >= len(tasks):
                    domain_idx = (domain_idx + 1) % len(domains)
                    domain_val = domains[domain_idx]
                    tasks = list_tasks(root_dir_val, domain_val)
                    task_idx = 0 if tasks else 0
            elif direction == "prev":
                task_idx -= 1
                if task_idx < 0:
                    domain_idx = (domain_idx - 1) % len(domains)
                    domain_val = domains[domain_idx]
                    tasks = list_tasks(root_dir_val, domain_val)
                    task_idx = len(tasks) - 1 if tasks else 0

            if not tasks:
                return (
                    domain_idx,
                    task_idx,
                    gr.Dropdown(choices=domains, value=domain_val),
                    gr.Dropdown(choices=[], value=None),
                    "",
                    domain_val,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "[]",
                    0,
                    gr.Dropdown(choices=[], value=None),
                    "",
                    "",
                    "",
                    "",
                )

            task_val = tasks[task_idx]
            (
                task_id,
                domain_name,
                related_apps_str,
                instruction,
                complexity,
                estimated_steps,
                category,
                evaluator_meta,
                evaluator_items_json,
                item_index,
                item_dropdown,
                desc,
                func,
                result,
                code,
                expected,
            ) = _load_and_first_item(root_dir_val, domain_val, task_val)

            return (
                domain_idx,
                task_idx,
                gr.Dropdown(choices=domains, value=domain_val),
                gr.Dropdown(choices=tasks, value=task_val),
                task_id,
                domain_name,
                related_apps_str,
                instruction,
                complexity,
                estimated_steps,
                category,
                evaluator_meta,
                evaluator_items_json,
                item_index,
                item_dropdown,
                desc,
                func,
                result,
                code,
                expected,
            )

        prev_btn.click(
            fn=lambda rd, d, di, ti: step_task(rd, d, di, ti, "prev"),
            inputs=[root_dir, domain_dropdown, current_domain_index, current_task_index],
            outputs=[
                current_domain_index,
                current_task_index,
                domain_dropdown,
                task_dropdown,
                id_box,
                domain_box,
                related_apps_box,
                instruction_box,
                complexity_box,
                estimated_steps_box,
                category_box,
                evaluator_meta_box,
                evaluator_items_state,
                evaluator_item_index,
                evaluator_item_dropdown,
                evaluator_desc_box,
                evaluator_func_box,
                evaluator_result_box,
                evaluator_code_box,
                evaluator_expected_box,
            ],
        )

        next_btn.click(
            fn=lambda rd, d, di, ti: step_task(rd, d, di, ti, "next"),
            inputs=[root_dir, domain_dropdown, current_domain_index, current_task_index],
            outputs=[
                current_domain_index,
                current_task_index,
                domain_dropdown,
                task_dropdown,
                id_box,
                domain_box,
                related_apps_box,
                instruction_box,
                complexity_box,
                estimated_steps_box,
                category_box,
                evaluator_meta_box,
                evaluator_items_state,
                evaluator_item_index,
                evaluator_item_dropdown,
                evaluator_desc_box,
                evaluator_func_box,
                evaluator_result_box,
                evaluator_code_box,
                evaluator_expected_box,
            ],
        )

        def on_item_change(items_json: str, selected: str):
            try:
                items = json.loads(items_json or "[]")
            except Exception:
                items = []
            if not items or not selected:
                return 0, "", "", "", "", ""

            try:
                idx = int(selected.split()[1])
            except Exception:
                idx = 0

            idx = max(0, min(idx, len(items) - 1))
            item = items[idx]
            return (
                idx,
                item.get("desc", ""),
                item.get("func", ""),
                item.get("result", ""),
                item.get("code", ""),
                item.get("expected", ""),
            )

        evaluator_item_dropdown.change(
            fn=on_item_change,
            inputs=[evaluator_items_state, evaluator_item_dropdown],
            outputs=[
                evaluator_item_index,
                evaluator_desc_box,
                evaluator_func_box,
                evaluator_result_box,
                evaluator_code_box,
                evaluator_expected_box,
            ],
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_name="0.0.0.0", server_port=18888)
