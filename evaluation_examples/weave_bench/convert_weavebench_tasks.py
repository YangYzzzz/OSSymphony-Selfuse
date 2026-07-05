#!/usr/bin/env python3
"""Convert WeaveBench markdown tasks to OSSymphony/OSWorld task JSONs."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tarfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


DEFAULT_SOURCE = Path("/nvme/yangbowen/yangbowen/WeaveBench/cache/tasks")
DEFAULT_OUTPUT = Path("evaluation_examples/weave_bench")
JUDGE_HELPER = Path("/nvme/yangbowen/yangbowen/WeaveBench/weavebench/eval/judge_helper.py")
JUDGE_ENV_VARS = (
    "OPENROUTER_BASE_URL",
    "OPENROUTER_API_KEY",
    "JUDGE_MODEL",
    "WEAVEBENCH_JUDGE_PROTOCOL",
)


def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    raw = text[4:end].strip()
    meta: Dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip("'\"")
    return meta, text[end + len("\n---") :].lstrip()


def section(text: str, title: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(title)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def first_code_block(text: str, language: Optional[str] = None) -> str:
    if language:
        pattern = re.compile(rf"^```{re.escape(language)}[^\n]*\n(.*?)^```\s*$", re.DOTALL | re.MULTILINE)
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
    match = re.search(r"^```[^\n]*\n(.*?)^```\s*$", text, re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_workspace_path(body: str, meta: Dict[str, str]) -> str:
    raw = first_code_block(section(body, "Workspace Path"))
    if not raw:
        raw = section(body, "Workspace Path").strip("` \n")
    raw = raw.strip().rstrip("/")
    if raw.startswith("workspace/"):
        raw = raw[len("workspace/") :]
    if raw:
        return raw
    category = meta.get("category", "")
    task_id = meta.get("id", "")
    short = task_id
    if category and short.startswith(f"{category}_"):
        short = short[len(category) + 1 :]
    return f"{category}/{short}"


def extract_grader_code(body: str) -> str:
    checks = section(body, "Automated Checks")
    code = first_code_block(checks, "python") or first_code_block(checks)
    if not code:
        raise ValueError("missing Automated Checks python code block")
    if "def grade" not in code:
        raise ValueError("Automated Checks code block does not define grade()")
    return code


def reward_source(grader_code: str, task_id: str) -> str:
    return f'''# Auto-generated from WeaveBench task {task_id}.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

{grader_code}


def _run_grade():
    sig = inspect.signature(grade)
    kwargs = {{}}
    if "workspace_path" in sig.parameters:
        kwargs["workspace_path"] = "/tmp_workspace"
    if "transcript" in sig.parameters:
        chat = Path("/home/user/.openclaw/agents/main/sessions/chat.jsonl")
        kwargs["transcript"] = chat.read_text(errors="ignore") if chat.exists() else ""
    try:
        return grade(**kwargs)
    except TypeError:
        try:
            return grade("/tmp_workspace")
        except TypeError:
            return grade()


def _score(result):
    if isinstance(result, dict):
        for key in ("overall_score", "score", "reward"):
            if key in result:
                return float(result[key])
    return float(result)


if __name__ == "__main__":
    try:
        result = _run_grade()
        print("WEAVEBENCH_SCORE_JSON:", json.dumps(result, ensure_ascii=False, default=str))
        print(f"REWARD: {{max(0.0, min(1.0, _score(result))):.6f}}")
    except Exception:
        traceback.print_exc()
        print("REWARD: 0.0")
'''


def iter_tasks(source: Path) -> Iterable[Path]:
    for path in sorted(source.glob("*/*.md")):
        if path.parent.name == "workspace":
            continue
        yield path


def tar_directory(src: Path, dest: Path) -> bool:
    if not src.is_dir():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(dest, "w:gz") as tar:
        for child in sorted(src.iterdir()):
            tar.add(child, arcname=child.name)
    return True


def json_task(
    *,
    meta: Dict[str, str],
    md_path: Path,
    workspace_path: Path,
    workspace_rel: str,
    warmup: str,
    env_text: str,
    output_dir: Path,
    has_gt: bool,
    has_vlm: bool,
) -> Dict[str, object]:
    task_id = meta["id"]
    category = meta.get("category") or md_path.parent.name
    domain = category.lower()
    timeout = int(meta.get("timeout_seconds") or 1800)
    asset_dir = output_dir / "assets" / domain / task_id
    reward_rel = (asset_dir / "reward.py").as_posix()
    helper_rel = (output_dir / "assets" / "_judge_helper.py").as_posix()
    gt_rel = (asset_dir / "gt.tar.gz").as_posix()

    full_env = "\n".join([env_text.strip(), *JUDGE_ENV_VARS]).strip()
    post_files = [
        {"local_path": reward_rel, "path": f"/opt/eval/weave_bench/{task_id}/reward.py"},
        {"local_path": helper_rel, "path": "/opt/eval/_judge_helper.py"},
    ]
    if has_gt:
        post_files.append({"local_path": gt_rel, "path": f"/opt/eval/weave_bench/{task_id}/gt.tar.gz"})

    postconfig: List[Dict[str, object]] = [
        {
            "type": "execute",
            "parameters": {
                "command": [
                    "/bin/bash",
                    "-lc",
                    f"mkdir -p /opt/eval/weave_bench/{task_id} /tmp_workspace/gt",
                ]
            },
        },
        {"type": "upload_file", "parameters": {"files": post_files}},
    ]
    if has_gt:
        postconfig.append(
            {
                "type": "execute",
                "parameters": {
                    "command": [
                        "/bin/bash",
                        "-lc",
                        f"rm -rf /tmp_workspace/gt && mkdir -p /tmp_workspace/gt && "
                        f"tar xzf /opt/eval/weave_bench/{task_id}/gt.tar.gz -C /tmp_workspace/gt",
                    ]
                },
            }
        )

    return {
        "id": task_id,
        "snapshot": "weave_bench",
        "instruction": section(md_path.read_text(encoding="utf-8"), "Prompt"),
        "source": str(md_path),
        "config": [
            {
                "type": "weavebench",
                "parameters": {
                    "workspace_path": str(workspace_path),
                    "env": full_env,
                    "warmup": warmup,
                    "timeout": max(timeout, 1800),
                },
            }
        ],
        "trajectory": "trajectories/",
        "related_apps": [domain],
        "evaluator": {
            "func": "parse_cua_gym_reward",
            "conj": "avg",
            "result": {
                "type": "vm_command_line",
                "command": [
                    "/bin/bash",
                    "-lc",
                    "set -a; [ -f /tmp/openclaw_task_env.sh ] && . /tmp/openclaw_task_env.sh; "
                    "set +a; python3 "
                    f"/opt/eval/weave_bench/{task_id}/reward.py",
                ],
            },
            "need_rule_judge": True,
            "need_vlm_judge": has_vlm,
            "desc": "Run the WeaveBench rule-based grade() inside the VM and parse its REWARD score.",
            "postconfig": postconfig,
        },
        "platform": "desktop",
        "weave_bench_source": {
            "task_md": str(md_path),
            "workspace_path": str(workspace_path),
            "workspace_relative": workspace_rel,
            "uses_vlm_helper": has_vlm,
            "has_gt": has_gt,
        },
    }


def convert(source: Path, output: Path) -> None:
    examples_dir = output / "examples"
    assets_dir = output / "assets"
    examples_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)
    if JUDGE_HELPER.exists():
        shutil.copy2(JUDGE_HELPER, assets_dir / "_judge_helper.py")
    else:
        (assets_dir / "_judge_helper.py").write_text(
            "def vlm_score_rubric(*args, **kwargs):\n"
            "    return {'judge_method': 'failed', 'judge_error': 'missing-helper'}\n",
            encoding="utf-8",
        )

    test_all: Dict[str, List[str]] = {}
    converted = 0
    skipped: List[Tuple[Path, str]] = []
    for md_path in iter_tasks(source):
        try:
            text = md_path.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
            task_id = meta.get("id") or md_path.stem
            category = meta.get("category") or md_path.parent.name
            meta.setdefault("id", task_id)
            meta.setdefault("category", category)
            domain = category.lower()
            workspace_rel = extract_workspace_path(body, meta)
            workspace_path = source / "workspace" / workspace_rel
            grader_code = extract_grader_code(body)
            warmup = first_code_block(section(body, "Warmup"), "bash") or first_code_block(section(body, "Warmup"))
            env_text = first_code_block(section(body, "Env"))
            has_vlm = "vlm_score_rubric" in grader_code or "llm_score_text" in grader_code

            asset_dir = assets_dir / domain / task_id
            if asset_dir.exists():
                shutil.rmtree(asset_dir)
            asset_dir.mkdir(parents=True, exist_ok=True)
            (asset_dir / "reward.py").write_text(reward_source(grader_code, task_id), encoding="utf-8")
            has_gt = tar_directory(workspace_path / "gt", asset_dir / "gt.tar.gz")

            task_json = json_task(
                meta=meta,
                md_path=md_path,
                workspace_path=workspace_path,
                workspace_rel=workspace_rel,
                warmup=warmup,
                env_text=env_text,
                output_dir=output,
                has_gt=has_gt,
                has_vlm=has_vlm,
            )
            out_path = examples_dir / domain / f"{task_id}.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(task_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            test_all.setdefault(domain, []).append(task_id)
            converted += 1
        except Exception as exc:
            skipped.append((md_path, str(exc)))

    for ids in test_all.values():
        ids.sort()
    (output / "test_all.json").write_text(json.dumps(test_all, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Converted {converted} tasks into {output}")
    if skipped:
        print(f"Skipped {len(skipped)} tasks:")
        for path, reason in skipped:
            print(f"  {path}: {reason}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    convert(args.source.resolve(), args.output)


if __name__ == "__main__":
    main()
