#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 saved 轨迹中构建 <Screen1, action, Screen2> 三元组，
并调用 config.json 中配置的 external_model API 生成 GUI 测试指令。

支持两种目录格式：
1. 旧格式: saved-*/trajectories/*/traj.jsonl
2. oscaliber 格式: meta_{UUID}.json + UUID/step_*.png（自动检测）

逻辑：先检索三元组作为池，每次随机取 2 个，让模型根据这两个三元组生成 2 条不同指令，
从而保证指令多样性。所有指令保存到单个 JSON 文件。

用法:
  # 旧格式
  python run_instructions_from_triples.py -s saved-0 saved-1 -o generated_instructions.json
  # oscaliber 格式
  python run_instructions_from_triples.py -s oscaliber_results/os-caliber-kimi-k2.5-human0310-setup-0310/all_w_setup \\
      --task-config-dir evaluation_examples/ubuntu_online_rollout/human/human_0310/all_w_setup \\
      -o generated_instructions.json
"""

import argparse
import base64
import json
import mimetypes
import random
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Union


def encode_image_to_base64(image_path: Path) -> str:
    """Read an image file and return a data URI with base64 encoding."""
    if not image_path.is_file():
        return ""
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/png"
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

# ── API 日志记录（可选依赖，依赖 local_api_logger 包） ─────────────────
# _API_LOGGER_AVAILABLE = False
# try:
#     _LOGGER_PKG_DIR = Path(__file__).resolve().parent.parent / "API-Playground-HKRC-xufangzhi"
#     if str(_LOGGER_PKG_DIR) not in sys.path:
#         sys.path.insert(0, str(_LOGGER_PKG_DIR))
#     from local_api_logger import log_completion as _log_completion, set_log_dir as _set_log_dir
#     _API_LOGGER_AVAILABLE = True
# except Exception:
#     pass


# def _init_api_logger(log_dir: str) -> None:
#     """初始化 API 日志目录。"""
#     if _API_LOGGER_AVAILABLE:
#         try:
#             _set_log_dir(log_dir)
#         except Exception:
#             pass


# def _do_log_completion(
#     model: str,
#     request_data: dict,
#     response_data: dict,
#     api_key: str | None,
#     duration_ms: float,
# ) -> None:
#     """记录一次 API 调用，失败时静默忽略。"""
#     if not _API_LOGGER_AVAILABLE:
#         return
#     try:
#         _log_completion(
#             model=model,
#             request_data=request_data,
#             response_data=response_data,
#             api_key=api_key,
#             user="generate_instructions",
#             duration_ms=duration_ms,
#         )
#     except Exception:
#         pass


# 不生成与这些应用相关的任务（不区分大小写）
EXCLUDED_APPS = ()


def _is_excluded_triple(screen1: str, screen2: str, cur: dict, nxt: dict) -> bool:
    """若界面/窗口涉及 PyCharm、GIMP、Zoom、Outlook 则排除该三元组。"""
    text = " ".join([
        screen1,
        screen2,
        (cur.get("window_title") or ""),
        (nxt.get("window_title") or ""),
    ]).lower()
    return any(app in text for app in EXCLUDED_APPS)


def _is_excluded_instruction(inst: dict) -> bool:
    """若生成的指令的 app 或 instruction 涉及排除应用（含 Outlook）则排除。"""
    app = (inst.get("app") or "").lower()
    instruction = (inst.get("instruction") or "").lower()
    return any(exc in app or exc in instruction for exc in EXCLUDED_APPS)


def load_config(config_path: str) -> dict:
    """从 config.json 加载 API 配置，使用 external_model 作为生成指令的模型。"""
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    base_url = (cfg.get("OPENAI_BASE_URL") or "").rstrip("/")
    api_key = cfg.get("OPENAI_API_KEY") or ""
    ext = cfg.get("external_model") or {}
    model = ext.get("model") or "gemini-3-pro-preview"
    if not base_url or not api_key:
        raise SystemExit("config 中需要 OPENAI_BASE_URL 和 OPENAI_API_KEY")
    return {"base_url": base_url, "api_key": api_key, "model": model}


def read_text_file(dir_path: Path, filename: str) -> str:
    """若文件存在则读取并返回内容，否则返回空字符串。"""
    path = dir_path / filename
    if path.is_file():
        try:
            return path.read_text(encoding="utf-8", errors="replace").strip()
        except Exception:
            return ""
    return ""


# ── oscaliber 格式（meta_{UUID}.json + UUID/step_*.png）支持 ─────────────


def _is_oscaliber_format(save_dir: Path) -> bool:
    """检测目录是否为 oscaliber 格式（包含 meta_*.json 文件）。"""
    return any(save_dir.glob("meta_*.json"))

def build_triples_from_meta(meta_path: Path, max_triples: int) -> list:
    """
    从 meta_{UUID}.json 构建三元组。
    每个三元组: {screen1, action, screen2, task_id, screenshot_before, screenshot_after}。
    """
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    trajectory = meta.get("trajectory", [])
    task_id = meta.get("task_id", "")
    instruction = meta.get("instruction", "")

    # 获取 UUID 子目录路径 (meta_UUID.json -> UUID/)
    uuid = meta_path.stem.replace("meta_", "")
    root_dir = meta_path.parent

    triples = []
    for i in range(len(trajectory) - 1):
        if len(triples) >= max_triples:
            break
        cur_step = trajectory[i]
        nxt_step = trajectory[i + 1]

        action = (cur_step.get("action") or "").strip()
        if not action or action == "DONE":
            continue
        # 跳过 meta_action 为 DONE 的步骤
        meta_actions = cur_step.get("meta_action", [])
        if meta_actions and all("DONE" in str(a) for a in meta_actions):
            continue

        # 处理图片路径
        img_before_name = cur_step.get("screenshot_path")
        img_after_name = nxt_step.get("screenshot_path")

        if not img_before_name or not img_after_name:
            continue

        img_before_path = root_dir / img_before_name
        img_after_path = root_dir / img_after_name

        if not img_before_path.is_file() or not img_after_path.is_file():
            continue

        triples.append({
            "action": action,
            "task_id": task_id,
            "screenshot_before": str(img_before_path.absolute()),
            "screenshot_after": str(img_after_path.absolute()),
        })
    return triples


def collect_triples_from_oscaliber(
    save_dir,  # type: Path
    max_triples_per_meta,  # type: int
    max_triples_total=None,  # type: Optional[int]
    tag_source=False,  # type: bool
):
    """从 oscaliber 格式目录收集三元组（meta_{UUID}.json + UUID/step_*.png）。"""
    meta_files = sorted(save_dir.glob("meta_*.json"))
    if not meta_files:
        return []

    all_triples = []
    for meta_path in meta_files:
        if max_triples_total is not None and len(all_triples) >= max_triples_total:
            break
        triples = build_triples_from_meta(meta_path, max_triples_per_meta)
        if tag_source:
            for t in triples:
                t["source"] = save_dir.name
        if max_triples_total is not None:
            need = max_triples_total - len(all_triples)
            all_triples.extend(triples[:need])
        else:
            all_triples.extend(triples)
    return all_triples


# ── 应用检测与教程 ────────────────────────────────────────────────────────


def detect_apps_for_task(
    task_id,  # type: str
    meta_data=None,  # type: Optional[dict]
    task_config_dir=None,  # type: Optional[Path]
):
    """
    检测任务对应的应用名称。
    优先级: meta.snapshot > task_config.snapshot > task_config.related_apps
    """
    # 1. 检查 meta 中的 snapshot 字段
    if meta_data and meta_data.get("snapshot"):
        snap = meta_data["snapshot"]
        return [snap] if isinstance(snap, str) else list(snap)
    # 2. 从 task config 文件获取
    if task_config_dir and task_id:
        config_path = task_config_dir / f"{task_id}.json"
        if config_path.is_file():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                if config.get("snapshot"):
                    snap = config["snapshot"]
                    return [snap] if isinstance(snap, str) else list(snap)
                if config.get("related_apps"):
                    return list(config["related_apps"])
            except (json.JSONDecodeError, OSError):
                pass
    return []


def build_app_map_from_oscaliber(
    save_dir,  # type: Path
    task_config_dir,  # type: Optional[Path]
):
    # type: (...) -> Dict[str, List[str]]
    """从 oscaliber 目录构建 task_id -> [app_names] 映射。"""
    app_map = {}  # type: Dict[str, List[str]]
    for meta_path in save_dir.glob("meta_*.json"):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            tid = meta.get("task_id", "")
            if tid:
                apps = detect_apps_for_task(tid, meta, task_config_dir)
                if apps:
                    app_map[tid] = apps
        except (json.JSONDecodeError, OSError):
            continue
    return app_map


def load_app_tutorial(app_name: str, tutorial_dir: Path) -> str:
    """加载指定应用的教程 .md 内容。"""
    if not tutorial_dir or not tutorial_dir.is_dir():
        return ""
    tutorial_path = tutorial_dir / f"{app_name}.md"
    if tutorial_path.is_file():
        try:
            return tutorial_path.read_text(encoding="utf-8").strip()
        except Exception:
            return ""
    return ""


def build_system_prompt_with_tutorial(
    base_prompt,  # type: str
    app_names,  # type: List[str]
    tutorial_dir,  # type: Optional[Path]
):
    """在系统提示中附加应用教程内容作为先验知识。"""
    if not tutorial_dir or not tutorial_dir.is_dir() or not app_names:
        return base_prompt

    tutorial_parts = []
    seen = set()  # type: Set[str]
    for app_name in app_names:
        if app_name in seen:
            continue
        seen.add(app_name)
        content = load_app_tutorial(app_name, tutorial_dir)
        if content:
            tutorial_parts.append(f"## {app_name}\n{content}")

    if not tutorial_parts:
        return base_prompt

    tutorial_section = "\n\n---\n\n".join(tutorial_parts)
    return (
        base_prompt
        + "\n\n# Application Reference\n"
        "Below is reference information about the applications involved in the triples. "
        "Use this knowledge to generate more diverse and realistic GUI tasks.\n\n"
        + tutorial_section
    )


def format_triples_for_prompt(triples: list) -> List[dict]:
    """Format triples as a list of content blocks for a multimodal model prompt."""
    content_blocks = [
        {"type": "text", "text": "Synthesize this triple into TWO DIFFERENT instructions. Return only valid JSON as specified.\n\n"}
    ]
    for i, t in enumerate(triples, 1):
        content_blocks.append({"type": "text", "text": f"Screen1 (before action)\n"})
        if "screenshot_before" in t:
            img_b64 = encode_image_to_base64(Path(t["screenshot_before"]))
            if img_b64:
                content_blocks.append({
                    "type": "image_url",
                    "image_url": {"url": img_b64}
                })

        content_blocks.append({"type": "text", "text": f"\nAction:\n{t['action']}\n\nScreen2 (after action):\n"})

        if "screenshot_after" in t:
            img_b64 = encode_image_to_base64(Path(t["screenshot_after"]))
            if img_b64:
                content_blocks.append({
                    "type": "image_url",
                    "image_url": {"url": img_b64}
                })
        content_blocks.append({"type": "text", "text": "\n---\n\n"})

    return content_blocks


def parse_instructions_json(response: str) -> dict:
    """Extract and parse JSON from model response. Strips markdown code blocks if present."""
    text = response.strip()
    # Remove markdown code block
    for start in ("```json", "```"):
        if text.startswith(start):
            text = text[len(start):].lstrip()
    if text.endswith("```"):
        text = text[:-3].rstrip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # If truncated, try to close unclosed strings/arrays and reparse
        text = _repair_truncated_json(text)
        return json.loads(text)


def _repair_truncated_json(text: str) -> str:
    """Attempt to repair truncated JSON (close open strings/arrays/objects)."""
    in_string = False
    escape = False
    quote = None
    depth = []
    i = 0
    while i < len(text):
        c = text[i]
        if escape:
            escape = False
            i += 1
            continue
        if c == "\\" and in_string:
            escape = True
            i += 1
            continue
        if in_string:
            if c == quote:
                in_string = False
            i += 1
            continue
        if c in ('"', "'"):
            in_string = True
            quote = c
            i += 1
            continue
        if c in "{[":
            depth.append("}]" if c == "{" else "]")
            i += 1
            continue
        if c in "}]" and depth:
            depth.pop()
            i += 1
            continue
        i += 1
    # Close open string if any
    if in_string:
        text += quote
    # Close open brackets
    while depth:
        text += depth.pop()
    return text


def _is_retryable_error(exc: BaseException) -> bool:
    """判断异常是否可重试（网络/超时/限流/服务端错误）。401 等认证错误不可重试。"""
    if isinstance(exc, SystemExit):
        return False
    # urllib
    exc_name = type(exc).__name__
    if exc_name == "HTTPError":
        code = getattr(exc, "code", 0)
        if code == 401:
            return False
        return code == 429 or code >= 500
    if exc_name == "URLError":
        return True
    # 网络/超时
    if isinstance(exc, (TimeoutError, ConnectionError, OSError)):
        return True
    # openai 库
    if exc_name in ("APITimeoutError", "APIConnectionError", "RateLimitError"):
        return True
    if exc_name == "APIStatusError":
        code = getattr(exc, "status_code", 0)
        return code == 429 or code >= 500
    return False


def call_chat_api(base_url: str, api_key: str, model: str, system_prompt: str, user_content: Union[str, List[dict]], max_tokens: int = 4096) -> str:
    """使用 OpenAI 兼容接口发送 chat completions 请求，返回助手回复文本。"""
    if not (api_key or "").strip():
        raise SystemExit("config 中 OPENAI_API_KEY 为空，请检查 config.json（或 --config 指定文件）并填写有效 API key。")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    request_data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }

    try:
        from openai import OpenAI
    except ImportError:
        # 回退：无 openai 包时用 urllib，建议安装 openai 以获得更好兼容性： pip install openai
        import urllib.request
        import urllib.error
        url = f"{base_url.rstrip('/')}/chat/completions"
        body = json.dumps(request_data, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": f"Bearer {api_key.strip()}",
            },
            method="POST",
        )
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            # _do_log_completion(model, request_data, data, api_key, (time.time() - t0) * 1000)
            return (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise SystemExit(
                    "API 返回 401 Unauthorized：请检查 config 中的 OPENAI_API_KEY 是否正确、是否对该端点有效。"
                    "建议安装 openai 后再试: pip install openai"
                ) from e
            raise

    client = OpenAI(api_key=api_key, base_url=base_url)
    t0 = time.time()
    create_kwargs: dict = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
    }
    # 要求模型严格输出 JSON（部分端点支持，不支持时静默回退）
    try:
        resp = client.chat.completions.create(
            **create_kwargs,
            response_format={"type": "json_object"},
        )
    except Exception:
        resp = client.chat.completions.create(**create_kwargs)
    duration_ms = (time.time() - t0) * 1000
    response_data = {
        "choices": [{
            "message": {
                "role": resp.choices[0].message.role,
                "content": resp.choices[0].message.content,
            },
            "finish_reason": resp.choices[0].finish_reason,
        }],
        "usage": {
            "prompt_tokens": resp.usage.prompt_tokens if resp.usage else 0,
            "completion_tokens": resp.usage.completion_tokens if resp.usage else 0,
            "total_tokens": resp.usage.total_tokens if resp.usage else 0,
        } if resp.usage else None,
        "model": resp.model,
        "id": resp.id,
    }
    # _do_log_completion(model, request_data, response_data, api_key, duration_ms)
    return (resp.choices[0].message.content or "").strip()


def call_chat_api_with_retry(
    base_url: str,
    api_key: str,
    model: str,
    system_prompt: str,
    user_content: Union[str, List[dict]],
    max_tokens: int = 4096,
    max_retries: int = 3,
    retry_delay: float = 5.0,
) -> str:
    """带重试的 API 调用：对可重试错误进行指数退避重试。"""
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            return call_chat_api(base_url, api_key, model, system_prompt, user_content, max_tokens)
        except SystemExit:
            raise
        except BaseException as e:
            last_exc = e
            if attempt < max_retries and _is_retryable_error(e):
                delay = retry_delay * (2**attempt)
                print(f"    请求失败 ({type(e).__name__}: {e})，{delay:.0f}s 后重试 ({attempt + 1}/{max_retries})...", file=sys.stderr, flush=True)
                time.sleep(delay)
                continue
            raise last_exc
    raise last_exc  # 不应到达


SYSTEM_PROMPT = """You are an assistant that designs high-semantic, executable instructions for GUI agent evaluation.

You will receive ONE <Screen1, action, Screen2> triple with screenshots for reference. Synthesize this triple to generate TWO DIFFERENT instructions:
- Screen1: the screenshot before the action
- action: the action performed (e.g. mouse click, keyboard input)
- Screen2: the screenshot after the action

Generate TWO DIFFERENT instructions in English, each inspired by this triple. The instructions must be executable, high-semantic, and strictly grounded in the visual evidence to avoid hallucinations.

Requirements:

1. **Language**: Write all instructions in English only.

2. **Feasibility**: Make sure each instruction is feasible to be executed and finished by a GUI agent.

3. **High Semantic & Executable**: Instructions should describe high-level goals or specific operations that are semantically rich (e.g., "Apply the 'Web_Animation_Optimized' preset" instead of "Click the Video tab").

4. **File Path Constraints**:
   - Input files MUST be assumed to be in `~/Desktop/test_files`.
   - Output files should be saved in `~` (the home directory).
   - Use absolute or home-relative paths in your instructions when referring to files.

5. **Be divergent**: Do NOT simply copy or paraphrase the screen and action. Use the triple as inspiration. Create different but related tasks that test similar GUI abilities. Avoid "Open [App]" or "Launch [App]" boilerplate; assume apps are already open.

6. **CRITICAL — Output format**:
- Your ENTIRE response must be a single valid JSON object and nothing else.
- Do NOT include any markdown, code fences (```), explanation, preamble, or trailing text.
- Use EXACTLY this structure:
{"instructions": [{"app": "App name 1", "instruction": "First instruction text."}, {"app": "App name 2", "instruction": "Second instruction text."}]}

"app" is the exact application name.
"instruction" is the task description. Do NOT start with "Open [app]". Assume the app is already open.
You MUST return exactly 2 instructions and nothing else."""


def main():
    parser = argparse.ArgumentParser(description="从 saved 目录构建三元组并用 external_model 生成 GUI 测试指令")
    parser.add_argument(
        "--saved-dirs",
        "-s",
        nargs="+",
        default=["saved-3", "saved-2"],
        help="saved 目录列表（支持旧格式 saved-* 和 oscaliber 格式 meta_*.json，自动检测）",
    )
    parser.add_argument("--config", "-c", default="/nvme/yangbowen/yangbowen/OSSymphony/evaluation_examples/ubuntu_online_rollout/config/config.json", help="config.json 路径")
    parser.add_argument("--max-trajectories", type=int, default=100, help="每个 saved 目录最多使用几条轨迹（范围更广）")
    parser.add_argument("--max-triples-per-traj", type=int, default=8, help="每条轨迹/meta 最多取几个三元组")
    parser.add_argument("--pool-size", type=int, default=200, help="三元组池大小：先检索出的三元组数量（默认 200）")
    parser.add_argument("--num-instructions", type=int, default=50, help="三元组对数（每对随机取 2 个三元组生成 2 条指令，总指令数=2×此值，默认 50）")
    parser.add_argument("--seed", type=int, default=200, help="随机种子，保证抽样可复现")
    parser.add_argument("--output", "-o", default="generated_instructions.json", help="输出 JSON 文件路径，所有指令保存到此文件（默认 generated_instructions.json）")
    parser.add_argument("--max-retries", type=int, default=3, help="API 请求失败时最大重试次数（默认 3）")
    parser.add_argument("--retry-delay", type=float, default=5.0, help="重试前等待秒数，随后按指数退避（默认 5.0）")
    parser.add_argument(
        "--task-config-dir",
        default=None,
        help="任务配置文件目录（包含 {task_id}.json，用于获取 snapshot/related_apps 以识别应用）",
    )
    parser.add_argument(
        "--app-tutorial-dir",
        default="evaluation_examples/ubuntu_online_rollout/app_tutorial",
        help="应用教程目录（包含 {app_name}.md，提供先验知识，默认: evaluation_examples/ubuntu_online_rollout/app_tutorial）",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent

    # ── 解析 saved 目录 ──
    saved_dirs = []  # type: List[Path]
    for name in args.saved_dirs:
        p = Path(name)
        if not p.is_absolute():
            p = root / p
        if not p.is_dir():
            print(f"Warning: saved dir not found, skipping: {p}", file=sys.stderr)
            continue
        saved_dirs.append(p)
    if not saved_dirs:
        print("错误: 没有有效的 saved 目录", file=sys.stderr)
        sys.exit(1)

    # ── 解析 task config 目录 ──
    task_config_dir = None  # type: Optional[Path]
    if args.task_config_dir:
        task_config_dir = Path(args.task_config_dir)
        if not task_config_dir.is_absolute():
            task_config_dir = root / task_config_dir
        if not task_config_dir.is_dir():
            print(f"Warning: task config dir not found: {task_config_dir}", file=sys.stderr)
            task_config_dir = None

    # ── 解析应用教程目录 ──
    tutorial_dir = None  # type: Optional[Path]
    _td = Path(args.app_tutorial_dir)
    if not _td.is_absolute():
        _td = root / _td
    if _td.is_dir():
        tutorial_dir = _td

    # ── 加载 API 配置 ──
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = root / config_path
    if not config_path.is_file():
        config_path = root / "config.json"
    if not config_path.is_file():
        print("错误: 找不到 config.json", file=sys.stderr)
        sys.exit(1)

    cfg = load_config(str(config_path))

    print(f"使用 API: {cfg['base_url']}, model: {cfg['model']}")
    print(f"数据目录: {[d.name for d in saved_dirs]}")
    if task_config_dir:
        print(f"任务配置目录: {task_config_dir}")
    if tutorial_dir:
        print(f"应用教程目录: {tutorial_dir}")

    # ── 收集三元组（自动检测格式） ──
    pool_size = max(2, args.pool_size)
    all_triples = []  # type: List[dict]
    app_map = {}  # type: Dict[str, List[str]]  # task_id -> [app_names]

    for save_dir in saved_dirs:
        if _is_oscaliber_format(save_dir):
            # oscaliber 格式: meta_{UUID}.json + UUID/step_*.png
            print(f"  [{save_dir.name}] 检测到 oscaliber 格式，从 meta_*.json 提取三元组...")
            dir_triples = collect_triples_from_oscaliber(
                save_dir,
                max_triples_per_meta=args.max_triples_per_traj,
                max_triples_total=None,
                tag_source=len(saved_dirs) > 1,
            )
            # 构建应用映射
            dir_app_map = build_app_map_from_oscaliber(save_dir, task_config_dir)
            app_map.update(dir_app_map)
            print(f"    提取 {len(dir_triples)} 个三元组，识别 {len(dir_app_map)} 个任务的应用信息")
            all_triples.extend(dir_triples)


    if not all_triples:
        print("未找到任何三元组，请检查目录格式（旧格式需要 trajectories/*/traj.jsonl，oscaliber 格式需要 meta_*.json）", file=sys.stderr)
        sys.exit(1)

    # 打乱并截取池
    rng = random.Random(args.seed)
    rng.shuffle(all_triples)
    triples = all_triples[:pool_size]

    print(f"共构建 {len(all_triples)} 个三元组，取前 {len(triples)} 个作为池")
    if app_map:
        from collections import Counter
        app_counter = Counter()
        for apps in app_map.values():
            app_counter.update(apps)
        print(f"  应用分布: {dict(app_counter)}")
    if triples and "source" in triples[0]:
        from collections import Counter
        sources = Counter(t.get("source") for t in triples)
        print(f"  来源: {dict(sources)}")

    # ── 生成指令 ──
    if len(triples) < 1:
        print("错误: 三元组池为空", file=sys.stderr)
        sys.exit(1)
    num_iterations = max(1, args.num_instructions)
    all_instructions = []  # type: List[dict]

    for idx in range(num_iterations):
        # 每次随机取 1 个三元组
        target_triple = rng.choice(triples)
        pair = [target_triple]

        # 确定涉及的应用
        pair_apps = []  # type: List[str]
        tid = target_triple.get("task_id", "")
        if tid and tid in app_map:
            pair_apps.extend(app_map[tid])

        # 构建系统提示（附加应用教程先验知识）
        sys_prompt = build_system_prompt_with_tutorial(SYSTEM_PROMPT, pair_apps, tutorial_dir)

        user_content = format_triples_for_prompt(pair)
        print(f"  第 {idx + 1}/{num_iterations} 次（随机取 1 个三元组 → 生成 2 条指令）...", flush=True)
        if pair_apps:
            print(f"    涉及应用: {list(dict.fromkeys(pair_apps))}", flush=True)

        batch_insts = []  # type: List[dict]
        for parse_attempt in range(args.max_retries + 1):
            response = call_chat_api_with_retry(
                cfg["base_url"],
                cfg["api_key"],
                cfg["model"],
                sys_prompt,
                user_content,
                max_tokens=4096,
                max_retries=args.max_retries,
                retry_delay=args.retry_delay,
            )
            print(f"    第 {idx + 1} 次 API 返回内容 {response}", flush=True)
            if not response:
                if parse_attempt < args.max_retries:
                    delay = args.retry_delay * (2**parse_attempt)
                    print(f"    第 {idx + 1} 次 API 未返回内容，{delay:.0f}s 后重试 ({parse_attempt + 1}/{args.max_retries})...", file=sys.stderr, flush=True)
                    time.sleep(delay)
                    continue
                print(f"  Warning: 第 {idx + 1} 次 API 未返回内容，跳过", file=sys.stderr)
                break
            try:
                data = parse_instructions_json(response)
                if isinstance(data, dict) and isinstance(data.get("instructions"), list):
                    batch_insts = [x for x in data["instructions"] if isinstance(x, dict) and x.get("instruction")]
                elif isinstance(data, list):
                    batch_insts = [x for x in data if isinstance(x, dict) and x.get("instruction")]
                elif isinstance(data, dict) and data.get("instruction"):
                    batch_insts = [{"app": data.get("app", ""), "instruction": data["instruction"]}]
                else:
                    batch_insts = []
                break
            except json.JSONDecodeError as e:
                if parse_attempt < args.max_retries:
                    delay = args.retry_delay * (2**parse_attempt)
                    print(f"    第 {idx + 1} 次 JSON 解析失败: {e}，{delay:.0f}s 后重试 ({parse_attempt + 1}/{args.max_retries})...", file=sys.stderr, flush=True)
                    time.sleep(delay)
                    continue
                print(f"  Warning: 第 {idx + 1} 次 JSON 解析失败: {e}，跳过", file=sys.stderr)
                break
        for inst in batch_insts:
            if isinstance(inst, dict) and inst.get("instruction"):
                if pair[0].get("source"):
                    inst["source"] = pair[0]["source"]
                inst["id"] = len(all_instructions) + 1
                all_instructions.append(inst)

    if not all_instructions:
        print("未得到任何有效指令", file=sys.stderr)
        sys.exit(1)

    # 排除相关任务，并重新编号
    excluded_count = sum(1 for inst in all_instructions if _is_excluded_instruction(inst))
    all_instructions = [inst for inst in all_instructions if not _is_excluded_instruction(inst)]
    if excluded_count:
        print(f"  已排除 {excluded_count} 条与排除列表相关的指令", flush=True)
    for i, inst in enumerate(all_instructions, 1):
        inst["id"] = i
    if not all_instructions:
        print("过滤后未剩余任何指令", file=sys.stderr)
        sys.exit(1)

    print("\n========== Generated instructions ==========\n")
    for inst in all_instructions:
        text = (inst.get("instruction") or "")[:80]
        if len(inst.get("instruction") or "") > 80:
            text += "..."
        print(f"  [{inst['id']}] {inst.get('app', '')}: {text}")

    if args.output:
        out_path = Path(args.output)
        if not out_path.is_absolute():
            out_path = root / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        output_obj = {
            "instructions": [
                {
                    "id": inst["id"],
                    "app": (inst.get("app") or "").strip(),
                    "instruction": (inst.get("instruction") or "").strip(),
                    **({"source": inst["source"]} if inst.get("source") else {}),
                }
                for inst in all_instructions
            ],
        }
        out_path.write_text(json.dumps(output_obj, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n已写入 {len(all_instructions)} 条指令到文件: {out_path}")


if __name__ == "__main__":
    main()
