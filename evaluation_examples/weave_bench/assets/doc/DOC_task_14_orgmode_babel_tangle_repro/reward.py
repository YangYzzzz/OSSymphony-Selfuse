# Auto-generated from WeaveBench task DOC_task_14_orgmode_babel_tangle_repro.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-axis grader for Org-mode Babel reproducibility task.
    Reads /tmp_workspace/results/ and /tmp_workspace/paper/. Cross-references
    against /tmp_workspace/gt/expected.json . Uses VLM rubric where available.
    """
    import json, os, re, hashlib, subprocess
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    pd = Path("/tmp_workspace/paper")
    # Prefer root-only /opt/doc14_gt to prevent answer leakage; fall back
    # to /tmp_workspace/gt for legacy mounts.
    gt = Path("/opt/doc14_gt") if Path("/opt/doc14_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    exp = {}
    try:
        exp = json.loads((gt / "expected.json").read_text())
    except Exception:
        exp = {}
    s = {}

    text_files = ["baseline_tangle.log", "baseline_tangle_files.txt",
                  "fixed_tangle.log", "means.txt", "paper.html",
                  "pandoc.log", "repro_hash.json", "paper.fixed.org",
                  "notes.md"]
    present = sum(1 for n in text_files if (rd / n).exists() and (rd / n).stat().st_size > 0)
    s["results_textfiles"] = present / len(text_files)

    shots = ["view_emacs_fontlock.png", "view_emacs_tangle_msg.png",
             "view_emacs_inline_image.png", "view_browser_mathjax.png"]
    s["screenshots_present"] = sum(1 for n in shots if (rd / n).exists()) / len(shots)

    # baseline log must contain evidence of the WRONG file or a noweb error
    base_log = ""
    try: base_log = (rd / "baseline_tangle.log").read_text(errors="ignore")
    except Exception: pass
    sigs = sum([
        bool(re.search(r"src/load_data_WRONG\.py", base_log)),
        bool(re.search(r"(unbound|undefined|NameError|name 'mean').*mean|mean.*not defined", base_log, re.I)),
        bool(re.search(r"(noweb|reference).*missing-helper|missing-helper.*(unresolved|not found)", base_log, re.I)),
    ])
    has_cmd = bool(re.search(r"(emacs.*--batch|org-babel-tangle|org-babel-execute)", base_log))
    s["baseline_evidence"] = 1.0 if (sigs >= 2 and has_cmd) else (0.5 if sigs >= 1 and has_cmd else 0.0)

    # Fixed paper.org structure
    fixed_org = ""
    try: fixed_org = (rd / "paper.fixed.org").read_text(errors="ignore")
    except Exception: pass
    s["bug_a_tangle_fixed"] = 1.0 if (
        re.search(r":tangle\s+src/load_data\.py(\s|$)", fixed_org) and
        "load_data_WRONG.py" not in fixed_org
    ) else 0.0
    cm_src = ""
    try: cm_src = (pd / "src/compute_means.py").read_text(errors="ignore")
    except Exception: pass
    s["bug_b_helper_block"] = 1.0 if (
        re.search(r"#\+name:\s*helper-mean", fixed_org, re.I) and
        "<<missing-helper>>" not in fixed_org and
        re.search(r"<<helper-mean>>", fixed_org) and
        re.search(r"def\s+mean\s*\(", cm_src) and "mean(" in cm_src
    ) else 0.0
    s["bug_c_results_file"] = 1.0 if (
        re.search(r"#\+name:\s*bar-chart[\s\S]{0,200}?:results[^\n]*file", fixed_org, re.I) and
        re.search(r"#\+name:\s*bar-chart[\s\S]{0,200}?graphics", fixed_org, re.I)
    ) else 0.0

    # Tangled python files exist & runnable
    src_files_ok = 0
    needles = {"src/load_data.py": "csv.DictReader",
               "src/compute_means.py": "buckets",
               "src/plot_bar.py": "savefig"}
    for fn in exp.get("expected_tangle_files", []):
        p = pd / fn
        if p.exists() and p.stat().st_size >= 200 and needles.get(fn, "") in p.read_text(errors="ignore"):
            src_files_ok += 1
    s["tangled_files"] = src_files_ok / max(1, len(exp.get("expected_tangle_files", [])))
    forbidden_present = any((pd / f).exists() for f in exp.get("forbidden_tangle_files", []))
    s["forbidden_absent"] = 0.0 if forbidden_present else 1.0

    # means.txt numeric agreement
    means_txt = ""
    try: means_txt = (rd / "means.txt").read_text(errors="ignore")
    except Exception: pass
    def _grab(key):
        m = re.search(rf"{key}\s+([\-\d\.]+)", means_txt)
        return float(m.group(1)) if m else None
    setosa = _grab("setosa_mean"); versi = _grab("versicolor_mean"); delta = _grab("delta")
    in_range = 0; total_n = 0
    for v, lo, hi in [(setosa, exp.get("setosa_mean_min"), exp.get("setosa_mean_max")),
                      (versi, exp.get("versicolor_mean_min"), exp.get("versicolor_mean_max")),
                      (delta, exp.get("delta_min"), exp.get("delta_max"))]:
        if lo is not None and hi is not None:
            total_n += 1
            if v is not None and lo <= v <= hi:
                in_range += 1
    s["means_numeric"] = in_range / max(1, total_n)

    # paper.html sanity
    html = ""
    try: html = (rd / "paper.html").read_text(errors="ignore")
    except Exception: pass
    html_min = exp.get("html_min_chars", 1500)
    html_kw = exp.get("html_must_contain", [])
    s["html_size"] = 1.0 if len(html) >= html_min else len(html) / float(html_min)
    s["html_keywords"] = (sum(1 for k in html_kw if k in html) / len(html_kw)) if html_kw else 0.0

    # figure exists
    fig = pd / exp.get("fig_path", "build/figs/means_bar.png")
    fig_kb = (fig.stat().st_size / 1024.0) if fig.exists() else 0.0
    s["fig_present"] = 1.0 if fig_kb >= exp.get("fig_min_kb", 5) else (fig_kb / float(exp.get("fig_min_kb", 5)))

    # repro_hash.json schema
    hash_ok = 0.0
    try:
        hj = json.loads((rd / "repro_hash.json").read_text())
        if fig.exists() and isinstance(hj.get("fig_sha256"), str):
            want = hashlib.sha256(fig.read_bytes()).hexdigest()
            if want == hj["fig_sha256"] and len(hj["fig_sha256"]) == 64 \
               and isinstance(hj.get("fig_bytes"), int) and hj["fig_bytes"] == fig.stat().st_size \
               and isinstance(hj.get("html_bytes"), int):
                hash_ok = 1.0
    except Exception: pass
    s["repro_hash"] = hash_ok

    # notes.md length
    notes = ""
    try: notes = (rd / "notes.md").read_text(errors="ignore")
    except Exception: pass
    s["notes_len"] = 1.0 if len(notes) >= 200 else len(notes) / 200.0

    # OCR over screenshots
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_emacs_fontlock.png":   ["Org", "begin_src", "TITLE", "Iris", "PROPERTY"],
            "view_emacs_tangle_msg.png": ["Tangled", "tangle"],
            "view_emacs_inline_image.png": ["RESULTS", "bar", "setosa", "versicolor"],
            "view_browser_mathjax.png":  ["Iris", "setosa", "versicolor", "Methods", "Results"],
        }
        for n, ks in kws.items():
            p = rd / n
            if not p.exists(): continue
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k in tx for k in ks): ocr_hits += 1
            except Exception:
                pass
        s["screenshots_ocr"] = ocr_hits / len(kws)
    except Exception:
        s["screenshots_ocr"] = 0.5

    # VLM rubric on the two visually-decisive shots
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd / n) for n in
                ["view_emacs_inline_image.png", "view_browser_mathjax.png"]
                if (rd / n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_inline_image_visible": "Emacs buffer 截图里能看到 means_bar 条形图被作为 inline image 嵌入 RESULTS 区块",
            "vlm_mathjax_rendered":     "浏览器截图里数学公式以 MathJax 排版方式渲染（不是裸 \\bar{x} 源码）",
            "vlm_layout_clean":         "截图布局清晰、无截断、无遮挡",
        }
        try:
            vlm = vlm_score_rubric(vlm_imgs[:2], rubric,
                instruction="判断 Org-mode buffer 是否真正显示了 inline 图像、浏览器是否真正渲染了 MathJax 公式。")
            for k in rubric: s[k] = vlm.get(k, 0.0)
        except Exception:
            for k in rubric: s[k] = 0.0
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums) / len(nums) if nums else 0.0

    # Hard gates
    has_cli = (rd / "fixed_tangle.log").exists() and (rd / "means.txt").exists()
    has_gui = (rd / "view_emacs_fontlock.png").exists() and (rd / "view_browser_mathjax.png").exists()
    vlm_avg = 0.0
    vlm_keys = ["vlm_inline_image_visible", "vlm_mathjax_rendered"]
    vk = [s.get(k, 0.0) for k in vlm_keys if k in s]
    if vk: vlm_avg = sum(vk) / len(vk)
    if not has_cli: base = min(base, 0.4)
    # NOTE: We deliberately do NOT cap on missing GUI screenshots —
    # whether the agent invokes Emacs / browser UI is not a scoring axis.
    # Missing PNGs already cost the screenshots_present / screenshots_ocr /
    # vlm_* sub_scores; no additional hard cap is applied here.
    if vlm_score_rubric is not None and vk and vlm_avg < 0.6: base = min(base, 0.6)
    if s.get("screenshots_present", 0) < 0.75: base = min(base, 0.5)
    if s.get("screenshots_ocr", 0) < 0.5: base = min(base, 0.55)
    if s.get("screenshots_ocr", 0) < 0.25: base = min(base, 0.45)
    if s.get("bug_a_tangle_fixed", 0) + s.get("bug_b_helper_block", 0) + s.get("bug_c_results_file", 0) < 2:
        base = min(base, 0.5)
    s["overall_score"] = round(base, 3)
    return s


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
