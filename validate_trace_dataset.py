"""
递归检查轨迹数据目录是否符合 RMAnnot 当前新格式要求。

识别规则：
- 仅当 JSON 顶层是 dict 且含 trace_id + task_id，才视为轨迹文件
"""
import argparse
import json
import os
from typing import Any, Dict, List, Optional, Tuple

REQUIRED_TRACE_KEYS = [
    "trace_id",
    "task_id",
    "platform",
    "instruction",
    "agent",
    "trajectory",
    "trajectory_length",
]

REQUIRED_STEP_KEYS = [
    "step_index",
    "screenshot_path",
    "raw_response",
    "thought",
    "action",
    "coordinate",
    "coordinate2",
]

CLICK_ACTION_TYPES = {
    "click",
    "left_click",
    "right_click",
    "double_click",
    "long_press",
    "tap",
}


def validate_trace_dataset(dataset_dir: str) -> int:
    """
    校验一个数据集目录，返回不合规（errors）文件数量。
    规则：
    - 只把顶层 dict 且含 trace_id + task_id 的 JSON 识别为轨迹文件
    - screenshot_path 不能为绝对路径
    - screenshot_path 允许相对 JSON 目录定位，但最终不能跳出 dataset_dir
    """

    def iter_json_files_recursive(directory: str) -> List[str]:
        json_paths: List[str] = []
        for root, _, files in os.walk(directory):
            for name in files:
                if name.startswith("."):
                    continue
                if name.lower().endswith(".json"):
                    json_paths.append(os.path.join(root, name))
        return sorted(json_paths)

    def load_json(file_path: str) -> Any:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def is_trace_dict(data: Any) -> bool:
        return isinstance(data, dict) and bool(data.get("trace_id")) and bool(data.get("task_id"))

    def is_norm_point(value: Any) -> bool:
        if not (isinstance(value, list) and len(value) == 2):
            return False
        try:
            x = float(value[0])
            y = float(value[1])
        except (TypeError, ValueError):
            return False
        return 0 <= x <= 1000 and 0 <= y <= 1000

    def validate_trace_data(
        trace_data: Dict[str, Any],
        source_json_path: Optional[str],
        dataset_root_path: Optional[str],
    ) -> Tuple[List[str], List[str]]:
        errors: List[str] = []
        warnings: List[str] = []

        for key in REQUIRED_TRACE_KEYS:
            if key not in trace_data:
                errors.append(f"缺少必需字段: {key}")

        if "trace_id" in trace_data and not isinstance(trace_data.get("trace_id"), str):
            errors.append("trace_id 必须是字符串")
        if "task_id" in trace_data and not isinstance(trace_data.get("task_id"), str):
            errors.append("task_id 必须是字符串")
        if "instruction" in trace_data and not isinstance(trace_data.get("instruction"), str):
            errors.append("instruction 必须是字符串")
        if "agent" in trace_data and not isinstance(trace_data.get("agent"), str):
            errors.append("agent 必须是字符串")

        if "trajectory" in trace_data and not isinstance(trace_data.get("trajectory"), list):
            errors.append("trajectory 必须是 list")
            return errors, warnings

        trajectory = trace_data.get("trajectory", [])
        if isinstance(trajectory, list):
            if trace_data.get("trajectory_length") != len(trajectory):
                errors.append(
                    f"trajectory_length 不匹配: 声明={trace_data.get('trajectory_length')} 实际={len(trajectory)}"
                )

            for idx, step in enumerate(trajectory):
                if not isinstance(step, dict):
                    errors.append(f"step[{idx}] 不是 dict")
                    continue

                for key in REQUIRED_STEP_KEYS:
                    if key not in step:
                        errors.append(f"step[{idx}] 缺少必需字段: {key}")

                if step.get("step_index") != idx:
                    errors.append(f"step[{idx}].step_index 应为 {idx}，当前={step.get('step_index')}")

                if "screenshot_path" in step and not isinstance(step.get("screenshot_path"), str):
                    errors.append(f"step[{idx}].screenshot_path 必须是字符串")
                elif "screenshot_path" in step:
                    screenshot_path = str(step.get("screenshot_path"))
                    if os.path.isabs(screenshot_path):
                        errors.append(
                            f"step[{idx}].screenshot_path 必须是相对 JSON 目录的相对路径（不能是绝对路径）"
                        )
                    elif source_json_path:
                        json_dir = os.path.dirname(os.path.abspath(source_json_path))
                        abs_screenshot_path = os.path.normpath(os.path.join(json_dir, screenshot_path))
                        boundary_dir = (
                            os.path.abspath(dataset_root_path) if dataset_root_path else json_dir
                        )
                        try:
                            common = os.path.commonpath([boundary_dir, abs_screenshot_path])
                        except ValueError:
                            common = ""

                        if common != boundary_dir:
                            if dataset_root_path:
                                errors.append(f"step[{idx}].screenshot_path 非法（不能跳出数据集目录）")
                            else:
                                errors.append(f"step[{idx}].screenshot_path 非法（不能跳出 JSON 所在目录）")
                        elif not os.path.exists(abs_screenshot_path):
                            errors.append(f"step[{idx}].screenshot_path 文件不存在: {screenshot_path}")

                if "action" in step and not isinstance(step.get("action"), str):
                    errors.append(f"step[{idx}].action 必须是字符串")

                action_text = (step.get("action") or "").lower()
                meta_action = step.get("meta_action") if isinstance(step.get("meta_action"), dict) else {}
                action_type = str(meta_action.get("type", "")).lower()
                maybe_click = any(t in action_text for t in CLICK_ACTION_TYPES) or (action_type in CLICK_ACTION_TYPES)

                coord = step.get("coordinate")
                if coord is not None and not is_norm_point(coord):
                    errors.append(f"step[{idx}].coordinate 需为 [0,1000] 归一化点或 None")
                if maybe_click and coord is None:
                    warnings.append(f"step[{idx}] 疑似点击动作但 coordinate 为 None")

                coord2 = step.get("coordinate2")
                if coord2 is not None:
                    if not (
                        isinstance(coord2, list)
                        and len(coord2) == 2
                        and is_norm_point(coord2[0])
                        and is_norm_point(coord2[1])
                    ):
                        errors.append(f"step[{idx}].coordinate2 需为 [[x1,y1],[x2,y2]] 或 None")

        return errors, warnings

    json_paths = iter_json_files_recursive(dataset_dir)
    print(f"\n🔎 检查目录: {dataset_dir}")
    print(f"📁 发现 JSON 文件: {len(json_paths)}")

    trace_files = []
    skipped_non_trace = 0
    for path in json_paths:
        try:
            data = load_json(path)
        except Exception as e:
            print(f"❌ JSON 解析失败: {path} | {e}")
            continue
        if is_trace_dict(data):
            trace_files.append(path)
        else:
            skipped_non_trace += 1

    print(f"🧩 识别为轨迹文件: {len(trace_files)}")
    print(f"⏭️  跳过非轨迹 JSON: {skipped_non_trace}")

    failed = 0
    warned = 0
    for path in trace_files:
        raw_data = load_json(path)
        errors, warnings = validate_trace_data(
            raw_data,
            source_json_path=path,
            dataset_root_path=dataset_dir,
        )

        if errors:
            failed += 1
            rel = os.path.relpath(path, dataset_dir)
            print(f"\n❌ 不合规: {rel}")
            for e in errors:
                print(f"   - {e}")
        elif warnings:
            warned += 1
            rel = os.path.relpath(path, dataset_dir)
            print(f"\n⚠️  警告: {rel}")
            for w in warnings:
                print(f"   - {w}")

    print("\n📊 结果统计")
    print(f"   轨迹文件总数: {len(trace_files)}")
    print(f"   不合规文件:   {failed}")
    print(f"   仅警告文件:   {warned}")
    print(f"   通过文件:     {len(trace_files) - failed - warned}")
    return failed


def main() -> None:
    parser = argparse.ArgumentParser(description="校验轨迹数据格式")
    parser.add_argument("directories", nargs="+", help="要检查的目录（可多个）")
    args = parser.parse_args()

    total_failed = 0
    for directory in args.directories:
        total_failed += validate_trace_dataset(directory)

    if total_failed > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
