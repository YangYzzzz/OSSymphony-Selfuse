# Auto-generated from WeaveBench task DOC_task_2_pandoc_docx_roundtrip.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DOCX roundtrip grader: CLI evidence + GUI screenshots + text fidelity + visual diff.
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
        "docx_structure", "docx_contents",
        "first_pass_exists", "first_pass_pages", "pandoc_log",
        "first_text", "first_metrics_schema",
        "evince_initial_shots",
        "odt_head_dump",
        "lo_writer_shots",
        "final_pdf_exists", "final_pdf_pages", "lo_convert_log",
        "final_text", "text_fidelity", "text_diff",
        "evince_final_shots",
        "visual_diff_exists", "diff_result_schema",
        "evince_diff_shots",
        "structural_audit",
        "report_length", "report_table",
        "deliverables_schema",
        "screenshots_count", "screenshot_ocr",
        "cross_channel",
        "gui_real_interaction", "gui_chrome_ocr", "gui_window_geometry",
        "vlm_lo_visible", "vlm_table_fixed",
        "vlm_header_present", "vlm_diff_marks",
    ]
    s = {k: 0.0 for k in sub_keys}

    if not rd.exists() or not any(rd.iterdir()):
        s["overall_score"] = 0.000
        return s

    def pdf_pages(p):
        try:
            r = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True, timeout=10)
            for line in r.stdout.splitlines():
                if line.startswith("Pages:"):
                    return int(line.split()[1])
        except Exception:
            return 0
        return 0

    # 1
    ds = rd / "docx_structure.json"
    if ds.exists():
        try:
            d = json.loads(ds.read_text())
            need = {"paragraphs", "headings", "tables", "images", "cross_refs"}
            s["docx_structure"] = 1.0 if need.issubset(d.keys()) else 0.4
        except Exception:
            pass
    if (rd / "docx_contents.txt").exists() and (rd / "docx_contents.txt").stat().st_size > 50:
        s["docx_contents"] = 1.0

    # 2
    fp = rd / "first_pass.pdf"
    if fp.exists() and fp.stat().st_size > 1000:
        s["first_pass_exists"] = 1.0
        n = pdf_pages(fp)
        s["first_pass_pages"] = 1.0 if n >= 2 else (n / 2.0 if n else 0.0)
    if (rd / "pandoc_first_pass.log").exists():
        s["pandoc_log"] = 1.0

    # 3
    if (rd / "first_text.txt").exists() and (rd / "first_text.txt").stat().st_size > 50:
        s["first_text"] = 1.0
    fpm = rd / "first_pass_metrics.json"
    if fpm.exists():
        try:
            d = json.loads(fpm.read_text())
            s["first_metrics_schema"] = 1.0 if all(k in d for k in ["pages", "word_count"]) else 0.3
        except Exception:
            pass

    # 4 evince initial screenshots (>=5KB to reject placeholders)
    init_shots = ["view_01_table_overflow", "view_02_broken_xref", "view_03_missing_header"]
    init_present = []
    for n in init_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and f[0].stat().st_size > 5120:
            init_present.append(f[0])
    s["evince_initial_shots"] = len(init_present) / len(init_shots)

    # 5 odt
    if (rd / "odt_head.xml").exists() and (rd / "odt_head.xml").stat().st_size > 100:
        s["odt_head_dump"] = 1.0

    # 6 LibreOffice Writer GUI shots
    lo_shots = ["view_04_lo_table_props", "view_05_lo_header_edit",
                "view_06_lo_xref_dialog", "view_07_lo_overview"]
    lo_present = []
    for n in lo_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and f[0].stat().st_size > 5120:
            lo_present.append(f[0])
    s["lo_writer_shots"] = len(lo_present) / len(lo_shots)

    # 7 final PDF + log
    fo = rd / "final_output.pdf"
    if fo.exists() and fo.stat().st_size > 1000:
        s["final_pdf_exists"] = 1.0
        n = pdf_pages(fo)
        s["final_pdf_pages"] = 1.0 if n >= 2 else (n / 2.0 if n else 0.0)
    if (rd / "lo_convert.log").exists():
        s["lo_convert_log"] = 1.0

    # 8 text fidelity
    ft = rd / "final_text.txt"
    if ft.exists() and ft.stat().st_size > 50:
        s["final_text"] = 1.0
    if ft.exists() and (rd / "first_text.txt").exists():
        try:
            w_first = len((rd / "first_text.txt").read_text(errors="ignore").split())
            w_final = len(ft.read_text(errors="ignore").split())
            if w_first > 0:
                dev = abs(w_final - w_first) / w_first
                s["text_fidelity"] = 1.0 if dev <= 0.15 else max(0.0, 1.0 - dev)
        except Exception:
            pass
    if (rd / "text_diff.txt").exists():
        s["text_diff"] = 1.0

    # 9 evince final shots
    final_shots = ["view_08_final_table_ok", "view_09_final_header_ok", "view_10_final_image_ok"]
    final_present = []
    for n in final_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and f[0].stat().st_size > 5120:
            final_present.append(f[0])
    s["evince_final_shots"] = len(final_present) / len(final_shots)

    # 10 visual diff
    vd = rd / "visual_diff.pdf"
    if vd.exists() and vd.stat().st_size > 200:
        s["visual_diff_exists"] = 1.0
    dr = rd / "diff_result.json"
    if dr.exists():
        try:
            d = json.loads(dr.read_text())
            s["diff_result_schema"] = 1.0 if all(k in d for k in ["pages_differ", "exit_code"]) else 0.3
        except Exception:
            pass

    # 11 diff evince shots
    diff_shots = ["view_11_diff_pdf_first", "view_12_diff_pdf_pageN"]
    diff_present = []
    for n in diff_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and f[0].stat().st_size > 5120:
            diff_present.append(f[0])
    s["evince_diff_shots"] = len(diff_present) / len(diff_shots)

    # 12 structural audit
    sa = rd / "structural_audit.json"
    if sa.exists():
        try:
            d = json.loads(sa.read_text())
            need = {"unresolved_refs", "table_labels", "header_keyword_hits"}
            s["structural_audit"] = 1.0 if need.issubset(d.keys()) else 0.3
        except Exception:
            pass

    # 13 report
    cr = rd / "conversion_report.md"
    if cr.exists():
        txt = cr.read_text(errors="ignore")
        s["report_length"] = 1.0 if len(txt) >= 400 else len(txt) / 400.0
        s["report_table"] = 1.0 if ("|" in txt and re.search(r"\|\s*[-:]+\s*\|", txt)) else 0.0

    # 14 deliverables
    dl = rd / "deliverables.json"
    if dl.exists():
        try:
            d = json.loads(dl.read_text())
            keys = ["final_output_pdf_sha256", "visual_diff_pdf_sha256", "first_pass_pdf_sha256"]
            present = sum(1 for k in keys if isinstance(d.get(k), str) and len(d[k]) >= 32)
            s["deliverables_schema"] = present / 3.0
        except Exception:
            pass

    # screenshots aggregate
    all_shots = init_present + lo_present + final_present + diff_present
    s["screenshots_count"] = len(all_shots) / 12.0

    if pytesseract and Image and all_shots:
        kws = ["LibreOffice", "Writer", "Evince", "Table", "Header", "Footer",
               "Cross", "Reference", "Properties", "Page"]
        hits = 0
        for sp in all_shots:
            try:
                tx = pytesseract.image_to_string(Image.open(sp))
                if any(k in tx for k in kws):
                    hits += 1
            except Exception:
                pass
        s["screenshot_ocr"] = min(1.0, hits / 5.0)

    # cross channel
    has_cli = (s["pandoc_log"] > 0 and s["final_pdf_exists"] > 0 and s["visual_diff_exists"] > 0)
    has_gui = s["screenshots_count"] >= 0.5
    s["cross_channel"] = 1.0 if (has_cli and has_gui) else (0.5 if (has_cli or has_gui) else 0.0)

    # VLM rubric
    if vlm_score_rubric and all_shots:
        rubric = {
            "vlm_lo_visible": "截图中可见 LibreOffice Writer 界面（菜单栏 / 工具栏 / 编辑区）",
            "vlm_table_fixed": "修复后截图中表格完全在页面边距内，无横向截断",
            "vlm_header_present": "修复后截图中页眉区域有可读文字内容",
            "vlm_diff_marks": "diff-pdf 截图中可见红 / 彩色差异叠加标记",
        }
        try:
            vlm = vlm_score_rubric([str(p) for p in all_shots[:4]], rubric,
                                   instruction="评估 DOCX 转换 + 修复任务的截图真实性。")
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
    s["gui_real_interaction"] = 1.0 if gui_diversity >= 0.9 else (0.5 if gui_diversity >= 0.7 else 0.0)

    geom_hits = 0
    if Image and gui_shot_paths:
        for p in gui_shot_paths:
            try:
                w, h = Image.open(p).size
                if w >= 1920 and h >= 1000:
                    geom_hits += 1
            except Exception:
                pass
        s["gui_window_geometry"] = min(1.0, geom_hits / max(3.0, len(gui_shot_paths) * 0.6))
    else:
        s["gui_window_geometry"] = 0.0

    chrome_kws = ["LibreOffice", "Writer", "Track Changes", "Styles", "File",
                  "Edit", "Format", "Evince", "Insert", "Sidebar"]
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

    # Weighted aggregation: core delivery 60% / GUI evidence 30% / aux 10%
    core_keys = [
        "docx_structure", "docx_contents",
        "first_pass_exists", "first_pass_pages", "pandoc_log",
        "first_text", "first_metrics_schema",
        "odt_head_dump",
        "final_pdf_exists", "final_pdf_pages", "lo_convert_log",
        "final_text", "text_fidelity", "text_diff",
        "visual_diff_exists", "diff_result_schema",
        "structural_audit",
        "report_length", "report_table",
        "deliverables_schema",
    ]
    gui_keys = [
        "evince_initial_shots", "lo_writer_shots", "evince_final_shots",
        "evince_diff_shots", "screenshots_count", "screenshot_ocr",
        "gui_real_interaction", "gui_chrome_ocr", "gui_window_geometry",
        "vlm_lo_visible", "vlm_table_fixed",
        "vlm_header_present", "vlm_diff_marks",
    ]
    aux_keys = ["cross_channel"]

    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vals) / len(vals) if vals else 0.0

    core_score = _avg(core_keys)
    gui_score = _avg(gui_keys)
    aux_score = _avg(aux_keys)
    base = 0.6 * core_score + 0.3 * gui_score + 0.1 * aux_score

    # Hard gates (v2: tightened)
    if not has_cli:
        base = min(base, 0.35)
    if not has_gui:
        base = min(base, 0.35)
    # Core delivery failures cap aggressively
    if s["final_pdf_exists"] == 0 or s["visual_diff_exists"] == 0:
        base = min(base, 0.4)
    if s["text_fidelity"] == 0 and s["final_pdf_exists"] > 0:
        base = min(base, 0.5)
    # GUI real-interaction: layered gates
    if s.get("gui_real_interaction", 0) < 0.5:
        base = min(base, 0.4)
    if s.get("gui_real_interaction", 0) < 0.9:
        base = min(base, 0.6)
    # GUI chrome OCR: layered gates (only when OCR stack available)
    if pytesseract and Image:
        if s.get("gui_chrome_ocr", 0) < 0.3:
            base = min(base, 0.35)
        elif s.get("gui_chrome_ocr", 0) < 0.5:
            base = min(base, 0.5)
    # Screenshot count gate: <50% present cap aggressively
    if s.get("screenshots_count", 0) < 0.5:
        base = min(base, 0.4)
    # VLM unavailable cap: cannot earn full credit without rubric eval
    vlm_keys = ["vlm_lo_visible", "vlm_table_fixed", "vlm_header_present", "vlm_diff_marks"]
    if all(s.get(k, 0) == 0 for k in vlm_keys):
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
