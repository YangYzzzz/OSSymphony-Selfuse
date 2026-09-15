# Auto-generated from WeaveBench task DES_task_3_print_ready_cmyk.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Print-ready CMYK pipeline grader: CLI preflight + GUI panels + CMYK conversion."""
    import json, re, subprocess, hashlib
    from pathlib import Path

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    if not rd.exists() or not any(rd.iterdir()):
        return {"overall_score": 0.0}

    # 1. svg_analysis.json — schema + GT-value cross-check (anti zero-cheat)
    sa_f = rd / "svg_analysis.json"
    s["svg_analysis_exists"] = 0.0
    s["svg_analysis_accuracy"] = 0.0
    if sa_f.exists():
        try:
            d = json.loads(sa_f.read_text())
            req = {"transparent_objects", "hairline_paths", "text_nodes", "rgb_color_objects"}
            if req.issubset(set(d.keys())):
                s["svg_analysis_exists"] = 1.0
                gt = {"transparent_objects": 7, "hairline_paths": 5, "text_nodes": 11}
                hits = 0
                for k, exp in gt.items():
                    try:
                        v = int(d.get(k, -1))
                        if v == exp:
                            hits += 1
                        elif abs(v - exp) <= 1 and v > 0:
                            hits += 0.5
                    except Exception:
                        pass
                try:
                    if int(d.get("rgb_color_objects", 0)) > 0:
                        hits += 1
                except Exception:
                    pass
                s["svg_analysis_accuracy"] = round(hits / 4.0, 3)
            else:
                s["svg_analysis_exists"] = 0.3
        except Exception:
            pass

    # 2. preflight_round1.log
    r1 = rd / "preflight_round1.log"
    if r1.exists():
        txt = r1.read_text(errors="ignore").lower()
        warn_count = sum(1 for kw in ["warning", "error", "fail", "rgb",
                                       "transparency", "font"] if kw in txt)
        s["preflight_r1_exists"] = 1.0
        s["preflight_r1_issues"] = min(1.0, warn_count / 3.0)
    else:
        s["preflight_r1_exists"] = 0.0
        s["preflight_r1_issues"] = 0.0

    # 3-4. GUI overview + fill-stroke screenshots
    gui_shots = {
        "view_inkscape_overview.png": ["Inkscape", "SVG", "poster", "View"],
        "view_fill_stroke_panel.png": ["Stroke", "Fill", "Width", "Opacity", "pt", "px"],
        "view_xml_editor_no_text.png": ["XML", "Editor", "svg", "path", "node"],
        "view_pdf_export_dialog.png": ["PDF", "Export", "Save", "DPI", "path"],
        "view_inkscape_doc_props_cmyk.png": ["Document", "Properties", "Inkscape", "ICC"],
    }
    gui_present = 0
    gui_ocr_hits = 0
    gui_valid_size = 0
    md5_set = set()

    try:
        import pytesseract
        from PIL import Image as PILImage
        can_ocr = True
    except ImportError:
        can_ocr = False

    for fname, keywords in gui_shots.items():
        fp = rd / fname
        if fp.exists():
            gui_present += 1
            try:
                sz = fp.stat().st_size
                if sz >= 5000:
                    gui_valid_size += 1
                md5_set.add(hashlib.md5(fp.read_bytes()).hexdigest())
            except Exception:
                pass
            if can_ocr:
                try:
                    img = PILImage.open(fp)
                    if img.size[0] >= 800 and img.size[1] >= 600:
                        tx = pytesseract.image_to_string(img)
                        if any(k.lower() in tx.lower() for k in keywords):
                            gui_ocr_hits += 1
                except Exception:
                    pass

    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    s["gui_screenshots_valid_size"] = gui_valid_size / len(gui_shots)
    s["gui_screenshots_unique"] = (len(md5_set) / gui_present) if gui_present else 0.0
    s["gui_ocr_quality"] = (gui_ocr_hits / len(gui_shots)) if can_ocr else 0.0
    s["_can_ocr"] = 1.0 if can_ocr else 0.0

    # 5. fix_verification.txt
    fv = rd / "fix_verification.txt"
    if fv.exists():
        txt = fv.read_text(errors="ignore").lower()
        s["fix_verification"] = 1.0 if any(kw in txt for kw in ["0", "pass", "ok", "fixed"]) else 0.3
    else:
        s["fix_verification"] = 0.0

    # 6. poster_fixed.pdf
    fixed_pdf = rd / "poster_fixed.pdf"
    s["fixed_pdf_exists"] = 1.0 if (fixed_pdf.exists() and fixed_pdf.stat().st_size >= 50000) else 0.0

    # 7. poster_cmyk.pdf + PDF version check
    cmyk_pdf = rd / "poster_cmyk.pdf"
    s["cmyk_pdf_exists"] = 0.0
    s["cmyk_pdf_version"] = 0.0
    if cmyk_pdf.exists():
        s["cmyk_pdf_exists"] = 1.0
        try:
            info = subprocess.run(["pdfinfo", str(cmyk_pdf)],
                                  capture_output=True, text=True, timeout=10)
            for line in info.stdout.splitlines():
                if line.startswith("PDF version:"):
                    ver = float(line.split(":")[1].strip())
                    s["cmyk_pdf_version"] = 1.0 if ver <= 1.3 else 0.5
        except Exception:
            pass

    # 8. preflight_round2.log
    r2 = rd / "preflight_round2.log"
    s["preflight_r2_exists"] = 0.0
    if r2.exists():
        txt2 = r2.read_text(errors="ignore").lower()
        has_inkcov = any(kw in txt2 for kw in ["cmyk", "ink", "cyan", "magenta", "coverage"])
        s["preflight_r2_exists"] = 1.0 if has_inkcov else 0.5

    # 9. ink_coverage.json
    ink_f = rd / "ink_coverage.json"
    s["ink_coverage_exists"] = 0.0
    s["ink_total_safe"] = 0.0
    s["ink_safe_field_consistent"] = 0.0
    if ink_f.exists():
        try:
            ink = json.loads(ink_f.read_text())
            req_k = {"cyan", "magenta", "yellow", "black", "total"}
            if req_k.issubset(set(ink.keys())):
                s["ink_coverage_exists"] = 1.0
                total = float(ink.get("total", 999))
                s["ink_total_safe"] = 1.0 if total <= 300 else (0.5 if total <= 350 else 0.0)
                if "safe" in ink:
                    expected_safe = (total <= 300)
                    s["ink_safe_field_consistent"] = 1.0 if bool(ink.get("safe")) == expected_safe else 0.0
                else:
                    s["ink_safe_field_consistent"] = 0.0
            else:
                s["ink_coverage_exists"] = 0.3
                s["ink_safe_field_consistent"] = 0.0
        except Exception:
            pass

    # 10. color_check.txt — no RGB
    cc_f = rd / "color_check.txt"
    s["color_check_no_rgb"] = 0.0
    if cc_f.exists():
        txt = cc_f.read_text(errors="ignore").lower()
        has_rgb = "rgb" in txt
        s["color_check_no_rgb"] = 0.0 if has_rgb else 1.0

    # 11. summary.md
    sm = rd / "summary.md"
    s["summary_exists"] = 0.0
    if sm.exists():
        stxt = sm.read_text(errors="ignore").lower()
        kw_hits = sum(1 for kw in ["preflight", "cmyk", "ink", "coverage",
                                     "透明", "text", "round", "fix"]
                      if kw in stxt)
        s["summary_exists"] = min(1.0, kw_hits / 4.0)

    # VLM rubric (≥4 items)
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    vlm_keys = ["vlm_inkscape_ui", "vlm_panel_content",
                "vlm_export_dialog", "vlm_xml_editor"]
    vlm_img_names = ["view_inkscape_overview.png", "view_fill_stroke_panel.png",
                     "view_pdf_export_dialog.png", "view_xml_editor_no_text.png"]
    vlm_imgs = [str(rd / n) for n in vlm_img_names if (rd / n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_inkscape_ui": "截图中可见 Inkscape 工具栏、菜单栏等 UI 元素",
            "vlm_panel_content": "截图面板中有实际数值或属性（非空白面板）",
            "vlm_export_dialog": "截图中出现 PDF 导出或保存选项对话框",
            "vlm_xml_editor": "截图中可见 XML Editor 面板（含节点树结构）",
        }
        vlm = vlm_score_rubric(vlm_imgs, rubric,
                               instruction="判断 Inkscape GUI 交互截图质量")
        for k in vlm_keys:
            s[k] = vlm.get(k, 0.0)
    else:
        for k in vlm_keys:
            s[k] = 0.0

    # Weighted aggregation: core deliverables 60%, GUI evidence 30%, aux 10%
    core_keys = ["svg_analysis_exists", "svg_analysis_accuracy",
                 "preflight_r1_exists", "preflight_r1_issues",
                 "fix_verification", "fixed_pdf_exists",
                 "cmyk_pdf_exists", "cmyk_pdf_version",
                 "preflight_r2_exists", "ink_coverage_exists",
                 "ink_total_safe", "ink_safe_field_consistent",
                 "color_check_no_rgb"]
    gui_keys_w = ["gui_screenshots_count", "gui_screenshots_valid_size",
                  "gui_screenshots_unique", "gui_ocr_quality",
                  "vlm_inkscape_ui", "vlm_panel_content",
                  "vlm_export_dialog", "vlm_xml_editor"]
    aux_keys = ["summary_exists"]

    def _avg(keys):
        vals = [float(s.get(k, 0.0)) for k in keys if k in s]
        return sum(vals) / len(vals) if vals else 0.0

    core = _avg(core_keys)
    gui = _avg(gui_keys_w)
    aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Hard gates (越严越好)
    has_cli = s.get("preflight_r1_exists", 0) > 0 and s.get("preflight_r2_exists", 0) > 0
    has_gui = s.get("gui_screenshots_count", 0) >= 0.6
    has_core_pdf = s.get("fixed_pdf_exists", 0) > 0 and s.get("cmyk_pdf_exists", 0) > 0
    accurate_diag = s.get("svg_analysis_accuracy", 0) >= 0.5
    if not has_cli:
        base = min(base, 0.4)
    if not has_gui:
        base = min(base, 0.4)
    if not has_core_pdf:
        base = min(base, 0.4)
    if not accurate_diag:
        base = min(base, 0.5)
    if s.get("gui_ocr_quality", 0) < 0.4 and s.get("_can_ocr", 0) > 0:
        base = min(base, 0.5)
    if s.get("gui_screenshots_unique", 0) < 0.8 and s.get("gui_screenshots_count", 0) > 0:
        base = min(base, 0.45)
    if s.get("color_check_no_rgb", 0) < 1.0:
        base = min(base, 0.55)
    # VLM unavailable degradation cap
    vlm_sum = sum(float(s.get(k, 0.0)) for k in
                  ["vlm_inkscape_ui", "vlm_panel_content",
                   "vlm_export_dialog", "vlm_xml_editor"])
    if vlm_sum == 0.0:
        base = min(base, 0.6)

    s.pop("_can_ocr", None)
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
