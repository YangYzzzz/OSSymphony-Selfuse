# Auto-generated from WeaveBench task DAV_task_0_spyder_step_debug.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    import hashlib, re
    from pathlib import Path
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    rd = Path("/tmp_workspace/results")
    scores = {}
    shot_names = ["step1_before_call.png", "step2_after_merge.png", "step3_after_calc.png", "pandas_head.png"]

    # ---- 1. Existence + anti-cheat (size, md5 uniqueness, resolution) ----
    md5s, sizes, resolutions = [], [], []
    for n in shot_names:
        p = rd / n
        if not p.exists():
            scores[n] = 0.0
            continue
        try:
            data = p.read_bytes()
        except Exception:
            scores[n] = 0.0
            continue
        sz = len(data)
        sizes.append(sz)
        md5s.append(hashlib.md5(data).hexdigest())
        # crude PNG resolution parse (IHDR @ offset 16: width(4) height(4) big-endian)
        w = h = 0
        if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
            w = int.from_bytes(data[16:20], "big")
            h = int.from_bytes(data[20:24], "big")
        resolutions.append((w, h))
        # ≥ 20 KB and ≥ 800x500 to defeat blank/placeholder screenshots
        ok_size = sz >= 20 * 1024
        ok_res = (w >= 800 and h >= 500)
        scores[n] = 1.0 if (ok_size and ok_res) else (0.4 if sz >= 5 * 1024 else 0.0)

    md5_unique_ratio = (len(set(md5s)) / len(md5s)) if md5s else 0.0
    scores["screenshot_diversity"] = round(md5_unique_ratio, 3)

    # ---- 2. root_cause.md: length AND must mention real concepts ----
    rc = ""
    if (rd / "root_cause.md").exists():
        try:
            rc = (rd / "root_cause.md").read_text(encoding="utf-8", errors="ignore")
        except Exception:
            rc = ""
    rc_len_ok = 80 <= len(rc) <= 600
    rc_low = rc.lower()
    # require evidence of real diagnosis: mentions category/case mismatch + merge/NaN
    has_case_concept = any(k in rc_low for k in ["大小写", "case", "lowercase", "uppercase", "lower", "upper"])
    has_merge_concept = any(k in rc_low for k in ["merge", "join", "匹配", "match", "category"])
    has_nan_concept = any(k in rc_low for k in ["nan", "缺失", "null", "missing"])
    rc_concept_hits = sum([has_case_concept, has_merge_concept, has_nan_concept])
    scores["root_cause_len"] = 1.0 if rc_len_ok else 0.0
    scores["root_cause_concept"] = round(rc_concept_hits / 3.0, 3)

    # ---- 3. fix.patch validity + must touch DISCOUNT_RULES / category ----
    patch = ""
    if (rd / "fix.patch").exists():
        try:
            patch = (rd / "fix.patch").read_text(encoding="utf-8", errors="ignore")
        except Exception:
            patch = ""
    valid_diff = ("---" in patch and "+++" in patch and "@@" in patch and len(patch) >= 80)
    scores["valid_patch"] = 1.0 if valid_diff else 0.0
    # patch must touch the offending area (category column or DISCOUNT_RULES literal)
    p_low = patch.lower()
    touches_target = (
        "discount_rules" in p_low
        or "category" in p_low
        or ".str.lower" in p_low
        or ".str.upper" in p_low
        or re.search(r"\['?[abc]'?", p_low) is not None
    )
    scores["patch_targets_bug"] = 1.0 if (valid_diff and touches_target) else 0.0

    # ---- 4. parquet must be NaN-free AND row count == 5 (no truncation cheat) ----
    parquet_ok = 0.0
    parquet_full = 0.0
    out = Path("/tmp_workspace/buggy_pipeline/output.parquet")
    if out.exists():
        try:
            import pandas as pd
            df = pd.read_parquet(out)
            if "discounted_price" in df.columns:
                parquet_ok = 1.0 if df["discounted_price"].notna().all() else 0.0
                parquet_full = 1.0 if (parquet_ok == 1.0 and len(df) >= 5) else 0.0
        except Exception:
            pass
    scores["parquet_ok"] = parquet_ok
    scores["parquet_full"] = parquet_full

    # ---- 5. VLM rubric on actual screenshots ----
    imgs = [str(rd/n) for n in shot_names if (rd/n).exists()]
    vlm_available = False
    if vlm_score_rubric and imgs:
        rubric = {
            "vlm_spyder_window": "截图显示 Spyder IDE 界面（含 Variable Explorer 面板和编辑器）",
            "vlm_variable_explorer": "至少一张截图清晰展示了 Variable Explorer 中 df 变量的列与样本值",
            "vlm_breakpoint_indicator": "编辑器栏显示了断点（红点 / 高亮行）或调试器停在断点处",
            "vlm_pandas_head_visible": "pandas_head.png 显示 DataFrame.head() 输出，且 discounted_price 列没有 NaN",
        }
        try:
            vlm = vlm_score_rubric(imgs[:4], rubric, instruction="评估 Spyder 调试器单步追踪 silent NaN bug 的截图质量；只在确实可见时给高分。")
            for k in rubric:
                scores[k] = float(vlm.get(k, 0.0) or 0.0)
            scores["judge_method"] = vlm.get("judge_method", "failed")
            vlm_available = scores["judge_method"] != "failed"
        except Exception:
            for k in rubric: scores[k] = 0.0
            scores["judge_method"] = "failed"

    # ---- 6. Weighted aggregation ----
    # Core deliverables (parquet fixed + valid patch + root cause concept) 60%
    core = (
        0.30 * scores.get("parquet_full", 0.0)
        + 0.15 * scores.get("patch_targets_bug", 0.0)
        + 0.10 * scores.get("root_cause_concept", 0.0)
        + 0.05 * scores.get("root_cause_len", 0.0)
    )
    # GUI evidence (4 screenshots + diversity + VLM Spyder UI confirmation) 30%
    shot_avg = sum(scores.get(n, 0.0) for n in shot_names) / 4.0
    vlm_ui = (
        scores.get("vlm_spyder_window", 0.0)
        + scores.get("vlm_variable_explorer", 0.0)
        + scores.get("vlm_breakpoint_indicator", 0.0)
    ) / 3.0
    gui = (
        0.10 * shot_avg
        + 0.05 * scores.get("screenshot_diversity", 0.0)
        + 0.15 * vlm_ui
    )
    # Aux (pandas head VLM + valid patch structure) 10%
    aux = (
        0.05 * scores.get("vlm_pandas_head_visible", 0.0)
        + 0.05 * scores.get("valid_patch", 0.0)
    )
    base = core + gui + aux

    # ---- 7. Multi-layer hard gates ----
    # Gate A: core deliverable broken → cap 0.40
    if scores.get("parquet_full", 0.0) < 1.0:
        base = min(base, 0.40)
    # Gate B: no real GUI evidence (Spyder UI not visible) → cap 0.45
    spyder_ui = max(
        scores.get("vlm_spyder_window", 0.0),
        scores.get("vlm_variable_explorer", 0.0),
        scores.get("vlm_breakpoint_indicator", 0.0),
    )
    if spyder_ui < 0.5:
        base = min(base, 0.45)
    if spyder_ui < 0.3:
        base = min(base, 0.30)
    # Gate C: screenshot duplication / cheating → cap 0.40
    if md5s and md5_unique_ratio < 0.75:
        base = min(base, 0.40)
    # Gate D: missing patch or root cause → cap 0.50
    if scores.get("patch_targets_bug", 0.0) < 1.0 or scores.get("root_cause_concept", 0.0) < 0.66:
        base = min(base, 0.50)
    # Gate E: VLM unavailable → cap 0.60 (cannot verify GUI claims)
    if not vlm_available:
        base = min(base, 0.60)

    scores["overall_score"] = round(max(0.0, min(1.0, base)), 3)
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
