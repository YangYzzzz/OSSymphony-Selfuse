# Auto-generated from WeaveBench task DOC_task_1_epub_validation_repair.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """EPUB validation-repair grader: CLI evidence + GUI screenshots + fix quality.
    Empty results → overall_score == 0.000.
    """
    import json, re, subprocess
    from pathlib import Path
    try:
        from PIL import Image
    except ImportError:
        Image = None
    try:
        import pytesseract
    except ImportError:
        pytesseract = None
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    gt = workspace / "gt"

    sub_keys = [
        "initial_log_present", "initial_summary_schema", "initial_error_count",
        "xmllint_log", "missing_assets",
        "zip_audit_initial", "nav_spine_diff",
        "edit_book_screenshots", "viewer_initial_screenshots",
        "mid_epubcheck", "zip_audit_fixed",
        "viewer_fixed_screenshots", "okular_screenshots",
        "pdf_exists", "pdf_pages",
        "final_errors_low", "error_reduction",
        "report_length", "report_has_table",
        "screenshots_count", "screenshot_ocr",
        "cross_channel",
        "gui_real_interaction", "gui_chrome_ocr", "gui_window_geometry",
        "vlm_calibre_visible", "vlm_edit_book_real",
        "vlm_fix_evidence", "vlm_okular_pdf",
    ]
    s = {k: 0.0 for k in sub_keys}

    if not rd.exists() or not any(rd.iterdir()):

        s["overall_score"] = 0.000
        return s

    # 1. epubcheck initial
    init_log = rd / "epubcheck_initial.log"
    if init_log.exists() and init_log.stat().st_size > 0:
        s["initial_log_present"] = 1.0 if re.search(r"ERROR|FATAL", init_log.read_text(errors="ignore")) else 0.3
    init_json = rd / "error_summary_initial.json"
    init_data = {}
    if init_json.exists():
        try:
            init_data = json.loads(init_json.read_text())
            s["initial_summary_schema"] = 1.0 if all(k in init_data for k in ["errors", "warnings"]) else 0.0
            ne = int(init_data.get("errors", 0) or 0)
            s["initial_error_count"] = 1.0 if ne >= 4 else ne / 4.0
        except Exception:
            pass

    # 2. xmllint + missing assets
    if (rd / "xmllint_initial.log").exists():
        s["xmllint_log"] = 1.0
    ma = rd / "missing_assets.txt"
    if ma.exists():
        lines = [l for l in ma.read_text(errors="ignore").splitlines() if l.strip()]
        s["missing_assets"] = 1.0 if len(lines) >= 2 else len(lines) / 2.0

    # 3. zip audit + nav/spine diff (initial)
    za_init = rd / "zip_audit_initial.json"
    if za_init.exists():
        try:
            d = json.loads(za_init.read_text())
            s["zip_audit_initial"] = 1.0 if "mimetype_first" in d and "entry_count" in d else 0.3
        except Exception:
            pass
    nsd = rd / "nav_spine_diff.json"
    if nsd.exists():
        try:
            d = json.loads(nsd.read_text())
            s["nav_spine_diff"] = 1.0 if all(k in d for k in ["in_spine_only", "in_nav_only", "matched"]) else 0.3
        except Exception:
            pass

    # 4-5. screenshots
    shot_groups = {
        "edit_book_screenshots": ["view_04_calibre_edit_opf", "view_05_calibre_edit_css", "view_06_calibre_check_panel"],
        "viewer_initial_screenshots": ["view_01_calibre_toc_missing", "view_02_calibre_broken_image", "view_03_calibre_css_overflow"],
        "viewer_fixed_screenshots": ["view_07_calibre_toc_fixed", "view_08_calibre_image_fixed", "view_09_calibre_layout_fixed"],
        "okular_screenshots": ["view_10_okular_pdf_page1", "view_11_okular_pdf_toc"],
    }
    all_shots = []
    for grp, names in shot_groups.items():
        present = 0
        for n in names:
            found = list(rd.glob(f"{n}*.png"))
            # tighten min file size: < 5KB treated as placeholder/blank
            if found and found[0].stat().st_size > 5000:
                present += 1
                all_shots.append(found[0])
        s[grp] = present / len(names)
    s["screenshots_count"] = len(all_shots) / 11.0

    # 6. mid-stage epubcheck + zip audit
    if (rd / "epubcheck_mid.log").exists() and (rd / "epubcheck_mid.log").stat().st_size > 0:
        s["mid_epubcheck"] = 1.0
    za_fix = rd / "zip_audit_fixed.json"
    if za_fix.exists():
        try:
            d = json.loads(za_fix.read_text())
            s["zip_audit_fixed"] = 1.0 if d.get("mimetype_first") is True and d.get("mimetype_uncompressed") is True else 0.4
        except Exception:
            pass

    # 7. PDF
    pdf = rd / "final_output.pdf"
    if pdf.exists() and pdf.stat().st_size > 1000:
        s["pdf_exists"] = 1.0
    pdf_pages = 0
    pi_json = rd / "pdfinfo.json"
    if pi_json.exists():
        try:
            d = json.loads(pi_json.read_text())
            pdf_pages = int(d.get("pages", 0) or 0)
        except Exception:
            pass
    if pdf_pages == 0 and pdf.exists():
        try:
            r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=10)
            for line in r.stdout.splitlines():
                if line.startswith("Pages:"):
                    pdf_pages = int(line.split()[1])
        except Exception:
            pass
    s["pdf_pages"] = 1.0 if pdf_pages >= 3 else (pdf_pages / 3.0 if pdf_pages else 0.0)

    # 8. final epubcheck + diff
    final_json = rd / "error_summary_final.json"
    if final_json.exists():
        try:
            d = json.loads(final_json.read_text())
            fe = int(d.get("errors", 99) or 99)
            s["final_errors_low"] = 1.0 if fe <= 1 else (0.5 if fe <= 3 else 0.0)
        except Exception:
            pass
    diff_json = rd / "error_diff.json"
    if diff_json.exists():
        try:
            d = json.loads(diff_json.read_text())
            r = float(d.get("reduction_ratio", 0) or 0)
            s["error_reduction"] = 1.0 if r >= 0.8 else max(0.0, r / 0.8)
        except Exception:
            pass

    # 9. repair report
    rr = rd / "repair_report.md"
    if rr.exists():
        txt = rr.read_text(errors="ignore")
        s["report_length"] = 1.0 if len(txt) >= 350 else len(txt) / 350.0
        s["report_has_table"] = 1.0 if ("|" in txt and re.search(r"\|\s*[-:]+\s*\|", txt)) else 0.0

    # 10. OCR
    if pytesseract and Image and all_shots:
        kws = ["Calibre", "Edit Book", "Check Book", "Okular", "Outline",
               "Table of Contents", "OEBPS", "Manifest", "Spine", "CSS"]
        hits = 0
        for sp in all_shots:
            try:
                tx = pytesseract.image_to_string(Image.open(sp))
                if any(k.lower() in tx.lower() for k in kws):
                    hits += 1
            except Exception:
                pass
        s["screenshot_ocr"] = min(1.0, hits / 5.0)

    # 11. cross channel
    has_cli = (s["initial_log_present"] > 0 and s["mid_epubcheck"] > 0 and s["final_errors_low"] > 0)
    has_gui = s["screenshots_count"] >= 0.5
    s["cross_channel"] = 1.0 if (has_cli and has_gui) else (0.5 if (has_cli or has_gui) else 0.0)

    # VLM rubric (≥4 items)
    if vlm_score_rubric and all_shots:
        rubric = {
            "vlm_calibre_visible": "截图中可见 Calibre 应用界面（书籍查看器或 Edit Book 编辑器）",
            "vlm_edit_book_real": "至少一张截图显示 Calibre Edit Book 的 OPF/CSS 编辑面板或 Check Book 结果",
            "vlm_fix_evidence": "修复后截图与修复前截图存在明显差异（ToC 出现 / 图片渲染 / 排版收敛）",
            "vlm_okular_pdf": "Okular 中可见 PDF 渲染内容、工具栏与左侧 Outline",
        }
        try:
            vlm = vlm_score_rubric([str(p) for p in all_shots[:4]], rubric,
                                   instruction="评估 EPUB 修复任务的 Calibre / Okular 截图真实性。")
            for k in rubric:
                s[k] = float(vlm.get(k, 0.0) or 0.0)
        except Exception:
            pass

    # GUI hard-gate sub-scores: trajectory diversity + chrome OCR + window geometry
    import hashlib
    gui_shot_paths = [p for p in all_shots if p.exists()]
    if len(gui_shot_paths) >= 4:
        hashes = set(hashlib.md5(p.read_bytes()).hexdigest() for p in gui_shot_paths)
        gui_diversity = len(hashes) / max(1, len(gui_shot_paths))
    else:
        gui_diversity = 0.0
    # tighten: require ≥ 0.9 unique for full credit
    s["gui_real_interaction"] = 1.0 if gui_diversity >= 0.9 else (0.5 if gui_diversity >= 0.6 else 0.0)

    geom_hits = 0
    if Image and gui_shot_paths:
        for p in gui_shot_paths:
            try:
                w, h = Image.open(p).size
                if w >= 1280 and h >= 720:
                    geom_hits += 1
            except Exception:
                pass
        s["gui_window_geometry"] = min(1.0, geom_hits / max(3.0, len(gui_shot_paths) * 0.6))
    else:
        s["gui_window_geometry"] = 0.0

    chrome_kws = ["Calibre", "Edit Book", "Check Book", "Okular", "Table of Contents",
                  "Metadata", "Library", "Bookmarks", "ebook-viewer"]
    chrome_hits = 0
    if pytesseract and Image and gui_shot_paths:
        for p in gui_shot_paths:
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if sum(1 for k in chrome_kws if k.lower() in tx.lower()) >= 2:
                    chrome_hits += 1
            except Exception:
                pass
        s["gui_chrome_ocr"] = min(1.0, chrome_hits / max(3.0, len(gui_shot_paths) * 0.5))
    else:
        s["gui_chrome_ocr"] = 0.0

    # Triple-gate anti-cheat composite: md5-unique × resolution-ok × ocr-hit must all hold
    triple_pass = 0
    if Image and pytesseract and gui_shot_paths:
        seen_md5 = {}
        for p in gui_shot_paths:
            try:
                md5 = hashlib.md5(p.read_bytes()).hexdigest()
                w, h = Image.open(p).size
                tx = pytesseract.image_to_string(Image.open(p))
                ok_unique = seen_md5.setdefault(md5, p) == p
                ok_res = (w >= 1280 and h >= 720)
                ok_ocr = any(k.lower() in tx.lower() for k in chrome_kws)
                if ok_unique and ok_res and ok_ocr:
                    triple_pass += 1
            except Exception:
                pass
    triple_ratio = triple_pass / max(1, len(gui_shot_paths))

    # Aggregate — weighted by group instead of flat mean to reflect task focus.
    core_keys = [
        "initial_log_present", "initial_summary_schema", "initial_error_count",
        "xmllint_log", "missing_assets",
        "zip_audit_initial", "nav_spine_diff",
        "mid_epubcheck", "zip_audit_fixed",
        "pdf_exists", "pdf_pages",
        "final_errors_low", "error_reduction",
        "report_length", "report_has_table",
    ]
    gui_keys = [
        "edit_book_screenshots", "viewer_initial_screenshots",
        "viewer_fixed_screenshots", "okular_screenshots",
        "screenshots_count", "screenshot_ocr",
        "gui_real_interaction", "gui_chrome_ocr", "gui_window_geometry",
        "vlm_calibre_visible", "vlm_edit_book_real",
        "vlm_fix_evidence", "vlm_okular_pdf",
    ]
    aux_keys = ["cross_channel"]

    def _avg(keys):
        vs = [s[k] for k in keys if isinstance(s.get(k), (int, float))]
        return sum(vs) / len(vs) if vs else 0.0

    core_score = _avg(core_keys)
    gui_score = _avg(gui_keys)
    aux_score = _avg(aux_keys)
    base = 0.5 * core_score + 0.35 * gui_score + 0.15 * aux_score

    # Hard gates (tightened)
    if not has_cli:
        base = min(base, 0.35)
    if not has_gui:
        base = min(base, 0.35)
    if s["pdf_exists"] == 0 and s["mid_epubcheck"] == 0:
        base = min(base, 0.45)
    # Core deliverable gates: missing fixed-EPUB OR missing reduction → cap 0.4
    if s["final_errors_low"] < 0.5 or s["error_reduction"] < 0.5:
        base = min(base, 0.4)
    # GUI real-interaction hard gate: pure CLI / replicated shots cannot exceed 0.35
    if s.get("gui_real_interaction", 0) < 0.5:
        base = min(base, 0.35)
    # Chrome OCR raised: <0.5 caps at 0.4 (was <0.3 cap 0.5)
    if s.get("gui_chrome_ocr", 0) < 0.5:
        base = min(base, 0.4)
    # Triple anti-cheat gate: < 50% truly real screenshots → cap 0.5
    if triple_ratio < 0.5:
        base = min(base, 0.5)
    # VLM unavailable / all 0 → cap 0.6 (cannot get full credit purely on heuristics)
    vlm_keys = ["vlm_calibre_visible", "vlm_edit_book_real", "vlm_fix_evidence", "vlm_okular_pdf"]
    if vlm_score_rubric is None or all(s.get(k, 0) == 0 for k in vlm_keys):
        base = min(base, 0.6)

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
