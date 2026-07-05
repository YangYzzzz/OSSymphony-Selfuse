# Auto-generated from WeaveBench task DOC_task_6_asciidoc_vscode_pdf.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DOC_task_6 grader."""
    import re
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. CLI artifacts
    cli_files = ["asciidoctor_warnings_before.txt","asciidoctor_warnings_after.txt","error_locations.txt","undefined_attrs.txt","output_html_after.html"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 3

    # 1b. before-snapshot HTML (Prompt 产物 1)
    bh = rd / "output_html_before.html"
    s["html_before_snapshot"] = 1.0 if (bh.exists() and bh.stat().st_size > 0) else 0.0

    # 2. warnings before vs after
    warn_score = 0.0
    bf = rd / "asciidoctor_warnings_before.txt"
    af = rd / "asciidoctor_warnings_after.txt"
    if bf.exists() and af.exists():
        try:
            bb = bf.read_text(); aa = af.read_text()
            n_b = len(re.findall(r"WARN|warn|include file not found|skipping include|undefined", bb, re.I))
            n_a = len(re.findall(r"WARN|warn|include file not found|skipping include|undefined", aa, re.I))
            if n_b >= 3 and n_a == 0: warn_score = 1.0
            elif n_b >= 3 and n_a < n_b * 0.3: warn_score = 0.6
        except Exception: pass
    s["warnings_resolved"] = warn_score

    # 3. PDF (v2: 必须 ≥4 页才满分；2-3 页只给 0.4；无 pdfinfo 顶配 0.5)
    pdf_score = 0.0
    pdf = rd / "main.pdf"
    if pdf.exists() and pdf.stat().st_size >= 30000:
        try:
            pinfo = rd / "pdfinfo.txt"
            if pinfo.exists():
                txt = pinfo.read_text()
                m = re.search(r"Pages:\s*(\d+)", txt)
                if m and int(m.group(1)) >= 4: pdf_score = 1.0
                elif m and int(m.group(1)) >= 2: pdf_score = 0.4
            else:
                if pdf.stat().st_size >= 50000: pdf_score = 0.5
        except Exception: pass
    s["pdf_pages"] = pdf_score

    # 4. HTML no literal placeholder (v2: 同步检查 expected_html_required_strings)
    html_score = 0.0
    h = rd / "output_html_after.html"
    required_html = ["Architecture", "Deployment", "Summary", "Introduction"]
    if h.exists():
        try:
            txt = h.read_text(errors="ignore")
            no_placeholder = ("{build_system}" not in txt) and ("{deploy_target}" not in txt)
            has_html = "<html" in txt.lower()
            kw_hits = sum(1 for k in required_html if k in txt)
            if no_placeholder and has_html and kw_hits == len(required_html):
                html_score = 1.0
            elif no_placeholder and has_html and kw_hits >= 2:
                html_score = 0.6
            elif has_html:
                html_score = 0.3
        except Exception: pass
    s["html_attributes_resolved"] = html_score

    # 5. GUI screenshots (v2: 加文件大小下限 5KB 防占位 PNG)
    gui_shots = ["view_vscode_preview_broken.png","view_vscode_include_error.png","view_vscode_preview_fixed.png","view_evince_pdf.png","view_evince_pdf_p3.png"]
    valid_shots = [n for n in gui_shots if (rd / n).exists() and (rd / n).stat().st_size >= 5120]
    gui_present = len(valid_shots)
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui = gui_present >= 3

    try:
        import pytesseract
        from PIL import Image
        kws_any = ["VSCode","Code","Asciidoctor","preview","Architecture","Deployment","Summary","Introduction","Page","Evince"]
        ocr_hits = 0
        for n in valid_shots:
            p = rd / n
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k in tx for k in kws_any): ocr_hits += 1
            except Exception: pass
        # v2: 命中率按总应有数计算（不是已存在数），强制全栈 OCR 命中
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
        ocr_available = True
    except Exception:
        s["gui_screenshots_ocr"] = 0.0
        ocr_available = False

    # 6. fix_report.md
    rp_score = 0.0
    rp = rd / "fix_report.md"
    if rp.exists():
        try:
            txt = rp.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            rp_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["fix_report"] = rp_score

    # 7. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_available = False
    if vlm_score_rubric and (rd / "view_vscode_preview_fixed.png").exists():
        rubric = {
            "vlm_vscode_window": "VSCode 截图能看到双栏(editor + preview)",
            "vlm_preview_complete": "fixed preview 截图渲染完整(无缺 section)",
            "vlm_pdf_pages": "Evince PDF 截图能看到完整文档页 + ToC",
            "vlm_no_placeholder": "渲染后没有 {xxx} 字面占位符",
        }
        try:
            imgs = [str(rd / n) for n in ["view_vscode_preview_fixed.png","view_evince_pdf.png","view_evince_pdf_p3.png"] if (rd / n).exists()]
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 VSCode preview + Evince PDF 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
            vlm_available = True
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_vscode_window","vlm_preview_complete","vlm_pdf_pages","vlm_no_placeholder"]:
            s[k] = 0.0

    # GUI hard-gate sub-scores: trajectory diversity + chrome OCR + window geometry
    import hashlib
    try:
        from PIL import Image as _PILImage
    except Exception:
        _PILImage = None
    # v2: 只数大小 ≥5KB 的有效截图，且要求 4/5 全 unique 才满分
    gui_shot_paths = [rd / n for n in gui_shots if (rd / n).exists() and (rd / n).stat().st_size >= 5120]
    if len(gui_shot_paths) >= 4:
        hashes = set(hashlib.md5(p.read_bytes()).hexdigest() for p in gui_shot_paths)
        unique = len(hashes)
        if unique == len(gui_shot_paths) and unique >= 5: gui_real = 1.0
        elif unique >= 4: gui_real = 0.7
        elif unique >= 3: gui_real = 0.4
        else: gui_real = 0.0
    elif len(gui_shot_paths) >= 3:
        hashes = set(hashlib.md5(p.read_bytes()).hexdigest() for p in gui_shot_paths)
        gui_real = 0.3 if len(hashes) == len(gui_shot_paths) else 0.0
    else:
        gui_real = 0.0
    s["gui_real_interaction"] = gui_real

    geom_hits = 0
    if _PILImage and gui_shot_paths:
        for p in gui_shot_paths:
            try:
                w, h = _PILImage.open(p).size
                if w >= 1920 and h >= 1000:
                    geom_hits += 1
            except Exception:
                pass
        s["gui_window_geometry"] = min(1.0, geom_hits / max(2.0, len(gui_shot_paths) * 0.6))
    else:
        s["gui_window_geometry"] = 0.0

    chrome_kws = ["Visual Studio Code", "Code", "AsciiDoc", "Preview", "Explorer",
                  "Evince", "File", "Edit", "View", "Terminal", "Run"]
    chrome_hits = 0
    try:
        import pytesseract as _pyt
        if _PILImage and gui_shot_paths:
            for p in gui_shot_paths:
                try:
                    tx = _pyt.image_to_string(_PILImage.open(p))
                    if sum(1 for k in chrome_kws if k.lower() in tx.lower()) >= 2:
                        chrome_hits += 1
                except Exception:
                    pass
            s["gui_chrome_ocr"] = min(1.0, chrome_hits / max(2.0, len(gui_shot_paths) * 0.5))
        else:
            s["gui_chrome_ocr"] = 0.0
    except Exception:
        s["gui_chrome_ocr"] = 0.0

    # v2: 加权评分 (核心交付 60% / GUI 证据 30% / VLM 辅助 10%)
    core_keys = ["cli_artifacts", "html_before_snapshot", "warnings_resolved",
                 "pdf_pages", "html_attributes_resolved", "fix_report"]
    gui_keys = ["gui_screenshots_count", "gui_screenshots_ocr",
                "gui_real_interaction", "gui_window_geometry", "gui_chrome_ocr"]
    vlm_keys = ["vlm_vscode_window", "vlm_preview_complete",
                "vlm_pdf_pages", "vlm_no_placeholder"]

    def _avg(keys):
        vals = [s.get(k, 0.0) for k in keys]
        return sum(vals) / len(vals) if vals else 0.0

    core_score = _avg(core_keys)
    gui_score = _avg(gui_keys)
    vlm_score = _avg(vlm_keys)
    base = 0.60 * core_score + 0.30 * gui_score + 0.10 * vlm_score

    # v2: 多层 hard gate（阈值整体上拉）
    if not has_cli: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.25)
    if s["warnings_resolved"] < 0.6: base = min(base, 0.40)
    if s["pdf_pages"] < 1.0: base = min(base, 0.55)
    if s["html_attributes_resolved"] < 0.6: base = min(base, 0.50)
    # GUI real-interaction hard gate: 纯 CLI 跑不允许超 0.35
    if s.get("gui_real_interaction", 0) < 0.7: base = min(base, 0.35)
    if s.get("gui_chrome_ocr", 0) < 0.5: base = min(base, 0.45)
    if s.get("gui_window_geometry", 0) < 0.5: base = min(base, 0.55)
    # 防 cheat：OCR / VLM 不可用时退化分上限封顶
    if not ocr_available: base = min(base, 0.55)
    if not vlm_available: base = min(base, 0.60)

    s["overall_score"] = round(base, 4)
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
