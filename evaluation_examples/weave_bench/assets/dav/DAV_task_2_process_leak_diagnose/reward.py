# Auto-generated from WeaveBench task DAV_task_2_process_leak_diagnose.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    import json, re
    from pathlib import Path
    try:
        from PIL import Image
    except Exception:
        Image = None
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/tmp_workspace/gt")
    meta_path = Path("/tmp/leaker_meta.json")
    scores = {}

    # 1. report.md
    rep = rd / "report.md"
    text = rep.read_text(encoding="utf-8", errors="ignore") if rep.exists() else ""
    scores["report_exists"] = 1.0 if text.strip() else 0.0

    # 2. PID match
    gt_pid = None
    if meta_path.exists():
        try:
            gt_pid = json.loads(meta_path.read_text())["pid"]
        except Exception:
            pass
    pid_match = 0.0
    m = re.search(r"pid\s*[:=]\s*(\d+)", text, re.IGNORECASE)
    if m and gt_pid is not None:
        if int(m.group(1)) == int(gt_pid):
            pid_match = 1.0
    scores["pid_match"] = pid_match

    # 3. growth rate sanity (TIGHTENED: GT ~12 MB/s; full credit only
    # within ±50%, partial otherwise). Anything wildly off is 0.
    gr_ok = 0.0
    g = re.search(r"growth_mb_per_sec\s*[:=]\s*([\d.]+)", text, re.IGNORECASE)
    if g:
        try:
            v = float(g.group(1))
            scores["growth_reported"] = v
            if 8.0 <= v <= 18.0:    # GT ~12 MB/s, full credit ±50%
                gr_ok = 1.0
            elif 5.0 <= v <= 25.0:  # partial credit
                gr_ok = 0.5
        except Exception:
            pass
    scores["growth_rate_ok"] = gr_ok

    # 4. log smoking-gun phrase (TIGHTENED: must include the dynamic
    # cache-size MB number that only appears in the actual log line)
    phrases = []
    if (gt_dir / "expected_log_phrases.txt").exists():
        phrases = [p.strip().lower() for p in
                   (gt_dir / "expected_log_phrases.txt").read_text().splitlines()
                   if p.strip()]
    text_l = text.lower()
    matched = sum(1 for p in phrases if p in text_l)
    scores["log_phrase_count"] = matched
    scores["log_phrase_pass"] = 1.0 if matched >= 3 else (matched / 3.0)
    # extra: must contain a specific MB count from the log (proves real grep)
    scores["log_dynamic_value"] = 0.0
    if re.search(r"cache size\s*=\s*\d+\s*mb", text_l):
        scores["log_dynamic_value"] = 1.0

    # 5. remediation: any non-empty line after a "remediation"/"建议"/"fix" header,
    #    or simply: at least one line with >= 8 non-whitespace characters in the report
    #    that is NOT just the pid/growth/log-quote.
    extra_lines = [
        ln for ln in text.splitlines()
        if len(ln.strip()) >= 8
        and not re.match(r"\s*(pid|growth_mb_per_sec)\s*[:=]", ln, re.IGNORECASE)
        and not ln.strip().startswith(">")
        and not ln.strip().startswith("```")
    ]
    scores["remediation_line"] = 1.0 if len(extra_lines) >= 2 else 0.0

    # 6. proof.png exists + size sane
    pp = rd / "proof.png"
    proof_ok = 0.0
    if pp.exists() and pp.stat().st_size >= 5 * 1024:
        proof_ok = 1.0
        if Image is not None:
            try:
                Image.open(pp).verify()
            except Exception:
                proof_ok = 0.5
    scores["proof_png"] = proof_ok

    base = (
        0.05 * scores["report_exists"] +
        0.15 * scores["pid_match"] +
        0.20 * scores["growth_rate_ok"] +
        0.15 * scores["log_phrase_pass"] +
        0.15 * scores["log_dynamic_value"] +
        0.10 * scores["remediation_line"] +
        0.10 * scores["proof_png"]
    )
    # Hard gates (non-VLM path):
    #  - PID wrong → cannot exceed 0.45 (used to be 0.5)
    #  - Did not capture the dynamic `cache size = N MB` value from the
    #    *running* log → cap 0.55 (proves the agent actually `tail`ed
    #    the live log instead of fabricating from the source, which now
    #    contains no literal phrases).
    #  - Did not match all three log phrases → cap 0.6
    if scores["pid_match"] < 1.0:
        base = min(base, 0.45)
    if scores["log_dynamic_value"] < 1.0:
        base = min(base, 0.55)
    if scores["log_phrase_pass"] < 1.0:
        base = min(base, 0.60)
    scores["overall_score"] = round(base, 3)

    # 7. VLM
    if vlm_score_rubric and pp.exists() and pp.stat().st_size >= 5*1024:
        # Pass the leaker PID into the rubric so VLM has a concrete check.
        leaker_pid_str = ""
        try:
            if Path("/tmp/leaker_meta.json").exists():
                leaker_pid_str = str(json.loads(Path("/tmp/leaker_meta.json").read_text()).get("pid", ""))
        except Exception:
            pass
        rubric = {
            "vlm_memory_view":           "proof.png 看起来像是 htop / GNOME System Monitor / ps 输出 / top 输出 — 即一个内存或进程监控界面,而不是空白图、网页截图或 Hello World。",
            "vlm_shows_process_list":    "图中能看到一个进程列表(多行,每行有 PID/RSS/COMMAND 等字段)。",
            "vlm_high_rss_visible":      "图中能直接读出某个进程的 RSS 数值非常大(数百 MB 到 GB 级别),即真的暴露出泄漏迹象,不只是普通进程列表。",
            "vlm_pid_present":           f"图中可见 PID 列含有 `{leaker_pid_str}` 这个数字 (即 leaker 进程的 PID)。" if leaker_pid_str else "图中至少有一个具体 PID 数字 (而不是模糊或马赛克)。",
            "vlm_indexer_visible":       "图中可见命令名 `photo_indexer.py` 或对应进程的 cmd 字段提到 indexer / python3 含 photo,证明图截到的是真正的泄漏进程。",
        }
        try:
            vlm = vlm_score_rubric([str(pp)], rubric,
                instruction="判断 proof.png 是否是一张真有效的内存/进程检查界面截图,且能直接看到泄漏进程的 PID 和高 RSS。")
            for k in rubric: scores[k] = vlm.get(k, 0.0)
            scores["judge_method"] = vlm.get("judge_method", "failed")
            vlm_avg = sum(vlm.get(k,0.0) for k in rubric)/len(rubric)
            scores["overall_score"] = round(0.5*base + 0.5*vlm_avg, 3)
            # HARD GATE: VLM judges the visual rubric.
            if scores.get("vlm_memory_view", 0.0) < 0.6:
                scores["overall_score"] = min(scores["overall_score"], 0.40)
            if scores.get("vlm_indexer_visible", 0.0) < 0.6:
                scores["overall_score"] = min(scores["overall_score"], 0.55)

        except Exception:
            pass
    return scores


def _run_grade():
    sig = inspect.signature(grade)
    kwargs = {}
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
        print(f"REWARD: {max(0.0, min(1.0, _score(result))):.6f}")
    except Exception:
        traceback.print_exc()
        print("REWARD: 0.0")
