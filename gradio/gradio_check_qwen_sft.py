import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

import gradio as gr


def load_trajectories(meta_dir: Path) -> List[Dict[str, Any]]:
    """加载一个 meta_dir 下的所有轨迹（按文件顺序）。

    目前假设 meta_dir 里的 jsonl 文件，每一行是一个样本，且包含 messages。
    这里简单地把同一 jsonl 文件里的样本视为一个任务轨迹，按行顺序展示。"""

    trajectories: List[Dict[str, Any]] = []

    for jsonl_file in sorted(meta_dir.glob("*.jsonl")):
        with jsonl_file.open("r", encoding="utf-8") as f:
            samples = []
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    samples.append(json.loads(line))
                except Exception:
                    continue
        if samples:
            trajectories.append({
                "file": jsonl_file,
                "samples": samples,
            })

    return trajectories


def segment_turns(messages: List[Dict[str, Any]]) -> List[str]:
    """将一整条 messages 按轮次划分成若干段文本，用于展示。

    简单策略：
    - 从 system 开始，遇到 user 开始新一轮；
    - 将这一轮内的 assistant、tool_call、tool_response 一起拼在一段里。
    """

    turns: List[str] = []
    current: List[str] = []

    def flush():
        nonlocal current
        if current:
            turns.append("\n".join(current))
            current = []

    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")
        if not isinstance(content, str):
            content = str(content)

        prefix = role.upper()
        line = f"[{prefix}] {content}"

        if role == "user" and current:
            # 新一轮，先结束上一轮
            flush()
        current.append(line)

    flush()
    return turns


class TrajectoryBrowser:
    def __init__(self, meta_dir: Path, image_dir: Path):
        self.meta_dir = meta_dir
        self.image_dir = image_dir
        self.trajectories = load_trajectories(meta_dir)

    def get_trajectory_options(self) -> List[Tuple[str, int]]:
        opts: List[Tuple[str, int]] = []
        for idx, traj in enumerate(self.trajectories):
            fname = traj["file"].name
            opts.append((f"{idx}: {fname}", idx))
        return opts

    def load_turns(self, traj_index: int) -> Tuple[List[str], List[str]]:
        """返回 (turn_text_list, image_paths)。

        image 展示策略先简单处理：
        - 若样本里有 images 字段（list），全部列出来，按文件名在 image_dir 下查找。"""

        if traj_index < 0 or traj_index >= len(self.trajectories):
            return [], []
        samples = self.trajectories[traj_index]["samples"]

        # 合并所有 messages
        all_messages: List[Dict[str, Any]] = []
        image_files = set()
        for s in samples:
            msgs = s.get("messages")
            if isinstance(msgs, list):
                all_messages.extend(msgs)
            imgs = s.get("images")
            if isinstance(imgs, list):
                for name in imgs:
                    image_files.add(name)

        turns = segment_turns(all_messages)
        image_paths: List[str] = []
        for name in sorted(image_files):
            path = self.image_dir / name
            if path.is_file():
                image_paths.append(str(path))

        return turns, image_paths


def build_interface(meta_dir: Path, image_dir: Path) -> gr.Blocks:
    browser = TrajectoryBrowser(meta_dir, image_dir)

    with gr.Blocks() as demo:
        gr.Markdown("# Qwen SFT 轨迹可视化检查")

        if not browser.trajectories:
            gr.Markdown("**未在 meta_dir 中找到任何 jsonl 轨迹文件。**")
            return demo

        traj_dropdown = gr.Dropdown(
            label="选择轨迹 (按文件/索引)",
            choices=[opt[0] for opt in browser.get_trajectory_options()],
            value=browser.get_trajectory_options()[0][0],
        )
        traj_index_state = gr.State(0)

        turn_slider = gr.Slider(
            label="交互轮次 (index)",
            minimum=0,
            maximum=0,
            step=1,
            value=0,
        )
        turn_text = gr.Textbox(
            label="当前轮次内容",
            lines=20,
            interactive=False,
        )
        gallery = gr.Gallery(
            label="相关截图（按文件名在 image_dir 下匹配）",
            show_label=True,
            columns=3,
            height=400,
        )

        all_turns_state = gr.State([])

        def on_select_traj(traj_label: str):
            # 解析 label 前缀中的索引
            try:
                idx_str = traj_label.split(":", 1)[0]
                idx = int(idx_str)
            except Exception:
                idx = 0
            turns, image_paths = browser.load_turns(idx)
            if not turns:
                return 0, 0, "", [], turns
            return 0, len(turns) - 1, turns[0], image_paths, turns

        def on_change_turn(turn_idx: int, turns: List[str]):
            if not turns:
                return ""
            if turn_idx < 0:
                turn_idx = 0
            if turn_idx >= len(turns):
                turn_idx = len(turns) - 1
            return turns[turn_idx]

        traj_dropdown.change(
            fn=on_select_traj,
            inputs=[traj_dropdown],
            outputs=[turn_slider, turn_slider, turn_text, gallery, all_turns_state],
        )

        turn_slider.change(
            fn=on_change_turn,
            inputs=[turn_slider, all_turns_state],
            outputs=[turn_text],
        )

        # 初始化一次
        first_label = browser.get_trajectory_options()[0][0]
        init_turn_idx, init_max, init_text, init_images, init_turns = on_select_traj(first_label)
        turn_slider.value = init_turn_idx
        turn_slider.maximum = init_max
        turn_text.value = init_text
        gallery.value = init_images
        all_turns_state.value = init_turns

    return demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Gradio 可视化检查 Qwen SFT 轨迹")
    parser.add_argument("meta_dir", type=str, help="包含 SFT jsonl 的目录")
    parser.add_argument("image_dir", type=str, help="包含截图图片的目录")
    parser.add_argument("--port", type=int, default=7860, help="Gradio 端口")
    args = parser.parse_args()

    meta_dir = Path(args.meta_dir)
    image_dir = Path(args.image_dir)

    demo = build_interface(meta_dir, image_dir)
    demo.launch(server_name="0.0.0.0", server_port=args.port)


if __name__ == "__main__":
    main()
