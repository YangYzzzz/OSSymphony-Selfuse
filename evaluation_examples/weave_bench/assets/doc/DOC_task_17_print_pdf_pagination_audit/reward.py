# Auto-generated from WeaveBench task DOC_task_17_print_pdf_pagination_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi sub-score grader for DOC_task_17_print_pdf_pagination_audit.

    Hard gates:
      - no CLI evidence (baseline + fixed pdfs)            -> cap 0.4
      - no GUI screenshot present                          -> cap 0.4
      - VLM rubric < 0.6 on the two print-preview shots    -> cap 0.6
      - parity_ok != True OR figure/caption split          -> cap 0.55
    """
    import json, re, hashlib, subprocess, shutil
    from pathlib import Path

    ws = Path(workspace_path or ".").resolve()
    rd = ws / "results"
    # Prefer root-only /opt/doc17_gt to prevent answer leakage; fall back
    # to the in-workspace gt for legacy mounts.
    gt = Path("/opt/doc17_gt") if Path("/opt/doc17_gt/expected.json").exists() else ws / "gt"
    s = {}

    expected = {}
    ej = gt / "expected.json"
    if ej.exists():
        try: expected = json.loads(ej.read_text())
        except Exception: expected = {}

    # --------------------------------------------- 1. file presence
    base_files = [
        "baseline_weasy.pdf", "baseline_chromium.pdf",
        "baseline_weasy.log", "baseline_chromium.log",
        "baseline_pages.jsonl", "baseline_text_diff.txt",
        "preview_save.pdf",
        "fixed_weasy.pdf", "fixed_chromium.pdf", "fixed_pages.jsonl",
        "pagination_report.json", "article.fixed.css", "notes.md",
    ]
    present = sum(1 for n in base_files if (rd / n).exists() and (rd / n).stat().st_size > 0)
    s["files_present"] = present / len(base_files)

    # weasy_pages dir
    wp_dir = rd / "weasy_pages"
    pngs = sorted(wp_dir.glob("page-*.png")) if wp_dir.exists() else []
    s["weasy_pages_dir"] = 1.0 if len(pngs) >= 3 else (0.5 if pngs else 0.0)

    shots = ["view_chromium_preview_before.png",
             "view_okular_orphan_caption.png",
             "view_chromium_preview_after.png"]
    shot_paths = [rd / n for n in shots if (rd / n).exists() and (rd / n).stat().st_size > 3000]
    s["screenshots_present"] = len(shot_paths) / len(shots)

    # --------------------------------------------- 2. baseline_pages.jsonl
    def _read_jsonl(p):
        out = []
        if not p.exists(): return out
        for ln in p.read_text(errors="ignore").splitlines():
            ln = ln.strip()
            if not ln: continue
            try: out.append(json.loads(ln))
            except Exception: pass
        return out

    bj = _read_jsonl(rd / "baseline_pages.jsonl")
    eng = {x.get("engine"): x for x in bj if isinstance(x, dict)}
    if {"weasy", "chromium"}.issubset(eng.keys()) and \
       all(isinstance(eng[e].get("pages"), int) and eng[e].get("sha256") for e in ("weasy", "chromium")):
        s["baseline_pages_schema"] = 1.0
    elif bj:
        s["baseline_pages_schema"] = 0.5
    else:
        s["baseline_pages_schema"] = 0.0

    # baseline diff non-empty
    btd = (rd / "baseline_text_diff.txt").read_text(errors="ignore") if (rd / "baseline_text_diff.txt").exists() else ""
    diff_lines = [l for l in btd.splitlines() if l.startswith(("+","-")) and not l.startswith(("+++","---"))]
    has_section = sum(1 for l in diff_lines if re.search(r"(Section|Figure|\f|page\s*\d)", l, re.I)) >= 2
    s["baseline_diff_nonempty"] = 1.0 if (len(diff_lines) >= 8 and has_section) else (0.5 if diff_lines else 0.0)

    # --------------------------------------------- 3. fixed_pages.jsonl
    fj = _read_jsonl(rd / "fixed_pages.jsonl")
    feng = {x.get("engine"): x for x in fj if isinstance(x, dict)}
    diff_abs = None
    if {"weasy", "chromium"}.issubset(feng.keys()):
        try:
            diff_abs = abs(int(feng["weasy"]["pages"]) - int(feng["chromium"]["pages"]))
        except Exception:
            diff_abs = None
    s["fixed_pages_schema"]   = 1.0 if diff_abs is not None else 0.0
    s["fixed_pages_parity"]   = 1.0 if (diff_abs is not None and diff_abs <= 1) else 0.0

    # --------------------------------------------- 4. pagination_report.json
    pr = {}
    if (rd / "pagination_report.json").exists():
        try: pr = json.loads((rd / "pagination_report.json").read_text())
        except Exception: pr = {}
    need_keys = {"weasy_pages", "chromium_pages", "page_diff_abs",
                 "parity_ok", "figure_caption_same_page", "all_figures_intact"}
    s["pagination_report_schema"] = 1.0 if need_keys.issubset(set(pr.keys())) else (0.5 if pr else 0.0)
    def _pdf_pages(p):
        try: return int(re.search(r"Pages:\s*(\d+)", subprocess.check_output(["pdfinfo",str(p)],stderr=subprocess.DEVNULL).decode()).group(1))
        except Exception: return None
    wp,cp = _pdf_pages(rd/"fixed_weasy.pdf"), _pdf_pages(rd/"fixed_chromium.pdf")
    real_parity = (wp is not None and cp is not None and abs(wp-cp) <= 1)
    s["pagination_parity_ok"]   = 1.0 if (pr.get("parity_ok") is True and real_parity and pr.get("weasy_pages")==wp and pr.get("chromium_pages")==cp) else 0.0
    s["pagination_figs_intact"] = 1.0 if (pr.get("all_figures_intact") is True and isinstance(pr.get("figure_caption_same_page",{}).get("weasy"),list) and len(pr["figure_caption_same_page"]["weasy"])==expected.get("expected_figures",4) and all(pr["figure_caption_same_page"]["weasy"]) and all(pr["figure_caption_same_page"]["chromium"])) else 0.0

    # --------------------------------------------- 5. article.fixed.css patches
    css = (rd / "article.fixed.css").read_text(errors="ignore") if (rd / "article.fixed.css").exists() else ""
    orig_css = (Path("/tmp_workspace/article/article.css").read_text(errors="ignore")
                if Path("/tmp_workspace/article/article.css").exists() else "")
    nonbug_lines = [l.strip() for l in orig_css.splitlines() if l.strip() and "@page" not in l and "figure" not in l and "h2" not in l]
    preserved = sum(1 for l in nonbug_lines if l in css) / max(1,len(nonbug_lines))
    bug_a = bool(re.search(r"@page[^{]*\{[^}]*\bsize\s*:\s*(letter|a4)\b[^}]*\bmargin\s*:", css, re.I | re.S))
    bug_b = bool(re.search(r"\bfigure\b[^{]*\{[^}]*((page-)?break-inside\s*:\s*avoid)", css, re.I | re.S))
    bug_c = bool(re.search(r"\bh2\b[^{]*\{[^}]*((page-)?break-before\s*:\s*(always|page))", css, re.I | re.S))
    s["css_bug_a_page_size"]      = 1.0 if (bug_a and preserved >= 0.8) else 0.0
    s["css_bug_b_figure_avoid"]   = 1.0 if (bug_b and preserved >= 0.8) else 0.0
    s["css_bug_c_h2_pagebreak"]   = 1.0 if (bug_c and preserved >= 0.8) else 0.0

    # --------------------------------------------- 6. preview_save.pdf bytes
    ps = rd / "preview_save.pdf"; bc = rd / "baseline_chromium.pdf"
    def _sha(p):
        try: return hashlib.sha256(p.read_bytes()).hexdigest()
        except Exception: return None
    s["preview_save_bytes"] = 1.0 if (ps.exists() and ps.stat().st_size > 5000
        and bc.exists() and _sha(ps) != _sha(bc)) else 0.0

    # --------------------------------------------- 7. notes.md length
    nm = (rd / "notes.md").read_text(errors="ignore") if (rd / "notes.md").exists() else ""
    s["notes_len"] = 1.0 if len(nm) >= 250 else len(nm) / 250.0

    # --------------------------------------------- 8. OCR over screenshots
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_chromium_preview_before.png": ["Print", "Save as PDF", "Pages", "Destination", "Total"],
            "view_okular_orphan_caption.png":   ["Figure", "Okular", "Pages", "thumbnail", "Section"],
            "view_chromium_preview_after.png":  ["Print", "Save as PDF", "Pages", "Destination", "Figure"],
        }
        for n, ks in kws.items():
            p = rd / n
            if not p.exists(): continue
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k.lower() in tx.lower() for k in ks): ocr_hits += 1
            except Exception:
                pass
        s["screenshots_ocr"] = ocr_hits / len(kws)
    except Exception:
        s["screenshots_ocr"] = 0.5

    # --------------------------------------------- 9. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd / n) for n in
                ["view_chromium_preview_before.png",
                 "view_okular_orphan_caption.png",
                 "view_chromium_preview_after.png"]
                if (rd / n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_print_preview_visible":  "Chromium 截图里能看到 print preview 面板(多页缩略图 + Destination=Save as PDF 设置)",
            "vlm_before_orphan_visible":  "before 截图里能看到至少一处 figure 与 caption 被分到不同页",
            "vlm_after_intact":           "after 截图里所有 figure 与 caption 都同页,排版整齐",
            "vlm_okular_orphan_visible":  "Okular 截图能清晰显示 orphan caption(figure 与 caption 跨页)",
            "vlm_layout_clean":           "截图布局清晰、无截断、无遮挡",
        }
        try:
            vlm = vlm_score_rubric(vlm_imgs[:2], rubric,
                instruction="判断 Chromium print preview 是否真正显示了多页缩略图,以及修复前/后 figure+caption 是否同页。")
            for k in rubric: s[k] = vlm.get(k, 0.0)
        except Exception:
            for k in rubric: s[k] = 0.0

    # --------------------------------------------- aggregate + hard gates
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums) / len(nums) if nums else 0.0

    has_cli = (rd / "baseline_weasy.pdf").exists() and (rd / "fixed_weasy.pdf").exists()
    has_gui = any((rd / n).exists() and (rd / n).stat().st_size > 3000 for n in shots)
    vlm_keys = ["vlm_print_preview_visible", "vlm_before_orphan_visible", "vlm_after_intact", "vlm_okular_orphan_visible"]
    vk = [s.get(k, 0.0) for k in vlm_keys if k in s]
    vlm_avg = sum(vk) / len(vk) if vk else 1.0

    if not has_cli: base = min(base, 0.4)
    # NOTE: We deliberately do NOT cap on missing GUI screenshots —
    # whether the agent invokes Chromium / Okular UI is not a scoring
    # axis. Missing PNGs already cost the screenshots_present /
    # screenshots_ocr / vlm_* sub_scores; no additional hard cap here.
    if vlm_score_rubric is not None and vk and vlm_avg < 0.6: base = min(base, 0.6)
    if s.get("screenshots_present", 0) < 0.66: base = min(base, 0.55)
    if s.get("pagination_parity_ok", 0) + s.get("pagination_figs_intact", 0) < 2.0:
        base = min(base, 0.45)
    if s.get("css_bug_a_page_size", 0) + s.get("css_bug_b_figure_avoid", 0) + s.get("css_bug_c_h2_pagebreak", 0) < 3:
        base = min(base, 0.45)
    if s.get("preview_save_bytes", 0) < 1.0:
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
