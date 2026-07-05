# Auto-generated from WeaveBench task OPS_task_1_pyspy_flamegraph.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    import re
    from pathlib import Path
    try:
        from PIL import Image
    except Exception:
        Image = None
    try:
        from _judge_helper import vlm_score_rubric, audit_chat_jsonl_for_banned
    except Exception:
        vlm_score_rubric = None
        audit_chat_jsonl_for_banned = None

    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/tmp_workspace/gt")
    scores = {}

    rep = rd / "report.md"
    text = rep.read_text(encoding="utf-8", errors="ignore") if rep.exists() else ""
    scores["report_exists"] = 1.0 if text.strip() else 0.0

    pj = rd / "profile.json"
    scores["profile_json"] = 1.0 if (pj.exists() and pj.stat().st_size >= 8*1024) else 0.0
    fp = rd / "flame.png"
    flame_size = fp.stat().st_size if fp.exists() else 0
    scores["flame_png"] = 1.0 if (fp.exists() and flame_size >= 30*1024) else 0.0
    scores["flame_size_bytes"] = flame_size

    # explanation length: ≥ 80 chars in report (excluding the top_hotspots line)
    explain_text = re.sub(r"top_hotspots\s*[:=].*", "", text, flags=re.IGNORECASE)
    scores["explain_long"] = 1.0 if len(explain_text.strip()) >= 80 else 0.0

    # parse top_hotspots field
    expected = []
    if (gt_dir / "expected_hot.txt").exists():
        try:
            expected = [ln.strip() for ln in (gt_dir / "expected_hot.txt").read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()]
        except Exception:
            expected = []
    th = re.search(r"top_hotspots\s*[:=]\s*(.+)", text, re.IGNORECASE)
    reported_names = []
    reported_pcts = []
    if th:
        line = th.group(1)
        # tokens like "worker_a=28%, worker_b=27%, worker_c=25%"
        for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\d+(?:\.\d+)?)\s*%?", line):
            reported_names.append(m.group(1))
            reported_pcts.append(float(m.group(2)))

    # 4. all 3 names present
    name_set = set(n.lower() for n in reported_names)
    expected_set = set(n.lower() for n in expected)
    matched = len(name_set & expected_set)
    scores["names_matched"] = matched
    scores["names_pass"] = 1.0 if matched >= 3 else (matched / 3.0)

    # 5. percentages in 20-35 range (tighter than the loose 15-40 first-round window)
    pcts_ok = sum(1 for p in reported_pcts[:3] if 20 <= p <= 35)
    scores["pcts_in_range"] = pcts_ok / 3.0 if reported_pcts else 0.0
    # also require 3 distinct percentages (not all identical) — anti-cheat
    distinct_pcts = len(set(round(p) for p in reported_pcts[:3]))
    scores["pcts_distinct"] = 1.0 if distinct_pcts >= 2 else 0.0

    # 6. correct order: report first 3 names should match expected[0..2]
    order_ok = 0
    for i, n in enumerate(reported_names[:3]):
        if i < len(expected) and n.lower() == expected[i].lower():
            order_ok += 1
    scores["order_pass"] = order_ok / 3.0

    # 7. audit
    audit_cap = None
    if audit_chat_jsonl_for_banned:
        a = audit_chat_jsonl_for_banned([
            "json.load",
            "import json",
            "py-spy top",
            "py-spy dump",
            "speedscope.json",  # accidental, but if grep'd profile.json text
        ])
        scores["audit_banned"] = a.get("any_banned", False)
        scores["audit_screenshots"] = a.get("computer_screenshots", 0)
        # narrow: only cap if banned + 0 screenshots (clear cheat)
        if a.get("any_banned") and a.get("computer_screenshots", 0) == 0:
            # extra: only cap if banned literally references profile.json
            if any("profile.json" in ex for ex in a.get("banned_examples", [])):
                audit_cap = 0.20

    # weighted base: core deliverable (names + order + flame/profile artifacts) 70%, evidence 20%, aux 10%
    core = (
        0.45 * scores["names_pass"] +
        0.30 * scores["order_pass"] +
        0.15 * scores["flame_png"] +
        0.10 * scores["profile_json"]
    )
    gui = (
        0.6 * scores["flame_png"] +
        0.4 * scores["pcts_in_range"]
    )
    aux = (
        0.5 * scores["report_exists"] +
        0.3 * scores["explain_long"] +
        0.2 * scores["pcts_distinct"]
    )
    base = 0.70 * core + 0.20 * gui + 0.10 * aux
    scores["overall_score"] = round(base, 3)

    # structural hard gates
    # core deliverable (flame.png) missing -> cap 0.35
    if scores["flame_png"] < 1.0:
        scores["overall_score"] = min(scores["overall_score"], 0.35)
    # profile.json too small / missing -> cap 0.40 (didn't actually record)
    if scores["profile_json"] < 1.0:
        scores["overall_score"] = min(scores["overall_score"], 0.40)
    # all 3 names not matched -> cap 0.45 (must identify all hot funcs)
    if scores["names_pass"] < 1.0:
        scores["overall_score"] = min(scores["overall_score"], 0.45)
    # order completely wrong -> cap 0.50
    if scores["order_pass"] < 1.0/3.0 + 1e-6:
        scores["overall_score"] = min(scores["overall_score"], 0.50)
    # percentages all out of plausible range -> cap 0.55 (didn't read flame numbers)
    if scores["pcts_in_range"] < 1.0/3.0 + 1e-6:
        scores["overall_score"] = min(scores["overall_score"], 0.55)

    # 8. VLM HARD GATE
    vlm_ran = False
    if vlm_score_rubric and fp.exists() and fp.stat().st_size >= 30*1024:
        rubric = {
            "vlm_is_speedscope_flamegraph": "flame.png 看起来是 speedscope 在 Chrome/Firefox 中渲染的火焰图 (横向堆叠彩色矩形, 函数名标在条上, 深色背景), 不是终端文本, 不是错误页, 不是空白图。",
            "vlm_three_hotspots_visible": "flame.png 中能看到至少 3 条几乎一样宽的 hot frame (而不是只一条很宽其它都细)。",
            "vlm_three_names_visible": "flame.png 中能直接读出 3 个 hot worker 函数名 (例如 worker_a / worker_b / worker_c, 至少 2 个能直接看见)。",
        }
        try:
            vlm = vlm_score_rubric([str(fp)], rubric,
                instruction="判断 flame.png 是否真是 speedscope 火焰图,并显示了 3 条相近宽度的 hot frame 含 3 个函数名。")
            for k in rubric: scores[k] = vlm.get(k, 0.0)
            scores["judge_method"] = vlm.get("judge_method", "failed")
            vlm_avg = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
            # weight base 40%, vlm 60% — VLM evidence dominates (real GUI proof)
            scores["overall_score"] = round(0.4*base + 0.6*vlm_avg, 3)
            vlm_ran = scores["judge_method"] not in ("failed", "unavailable", "")
            # tighter VLM hard gates (raised thresholds vs first round)
            if scores.get("vlm_is_speedscope_flamegraph", 0.0) < 0.7:
                scores["overall_score"] = min(scores["overall_score"], 0.25)
            if scores.get("vlm_three_hotspots_visible", 0.0) < 0.7:
                scores["overall_score"] = min(scores["overall_score"], 0.40)
            if scores.get("vlm_three_names_visible", 0.0) < 0.6:
                scores["overall_score"] = min(scores["overall_score"], 0.50)
            if vlm_avg < 0.4:
                scores["overall_score"] = min(scores["overall_score"], 0.30)
        except Exception:
            pass

    # VLM unavailable cap: cannot get full score without GUI evidence
    if not vlm_ran:
        scores["overall_score"] = min(scores["overall_score"], 0.60)

    if audit_cap is not None:
        scores["overall_score"] = min(scores["overall_score"], audit_cap)
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
