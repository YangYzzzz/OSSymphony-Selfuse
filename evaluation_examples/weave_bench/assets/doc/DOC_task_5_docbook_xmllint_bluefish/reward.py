# Auto-generated from WeaveBench task DOC_task_5_docbook_xmllint_bluefish.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DOC_task_5 grader."""
    import re
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. CLI artifacts
    cli_files = ["xmllint_errors_before.txt","xmllint_errors_after.txt","error_locations.txt","xsltproc.log","output.html"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 3

    # 1b. extra Prompt-required artifacts (working.docbook + after_fix1)
    extra_files = ["working.docbook", "xmllint_after_fix1.txt"]
    extra_present = sum(1 for f in extra_files if (rd / f).exists())
    s["extra_artifacts"] = extra_present / len(extra_files)

    # 2. xmllint errors before vs after
    err_score = 0.0
    bf = rd / "xmllint_errors_before.txt"
    af = rd / "xmllint_errors_after.txt"
    if bf.exists() and af.exists():
        try:
            bb = bf.read_text(); aa = af.read_text()
            n_before = len(re.findall(r"line\s+\d+|element|expected", bb))
            n_after = len(re.findall(r"line\s+\d+|element|expected", aa))
            if n_before >= 5 and n_after == 0: err_score = 1.0
            elif n_before >= 5 and n_after < n_before * 0.2: err_score = 0.7
            elif n_after < n_before: err_score = 0.4
        except Exception: pass
    s["xmllint_clean"] = err_score

    # 3. output.html (size > 2KB + 必须含 html/body + 至少 2 个 DocBook 渲染元素)
    html_score = 0.0
    oh = rd / "output.html"
    if oh.exists():
        try:
            sz = oh.stat().st_size
            txt = oh.read_text(errors="ignore").lower()
            doc_elems = sum(1 for tag in ["<h1", "<h2", "<p", "<a ", "<img", "<ul", "<ol", "<li"] if tag in txt)
            if sz > 2048 and "<html" in txt and "<body" in txt and doc_elems >= 3:
                html_score = 1.0
            elif sz > 1024 and "<html" in txt and "<body" in txt:
                html_score = 0.6
            elif sz > 200:
                html_score = 0.3
        except Exception: pass
    s["html_rendered"] = html_score

    # 4. GUI screenshots (size >= 50KB 才算真截图，过滤纯黑/占位 PNG)
    gui_shots = ["view_bluefish_open.png","view_bluefish_outline.png","view_bluefish_fixing.png","view_firefox_html.png","view_bluefish_final.png"]
    gui_present_paths = [rd / n for n in gui_shots if (rd / n).exists() and (rd / n).stat().st_size >= 50 * 1024]
    gui_present = len(gui_present_paths)
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui = gui_present >= 3

    try:
        import pytesseract
        from PIL import Image
        kws_any = ["Bluefish","Outline","DocBook","section","chapter","Firefox","XML"]
        ocr_hits = 0
        for n in gui_shots:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k in tx for k in kws_any): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
    except Exception:
        s["gui_screenshots_ocr"] = 0.5 if gui_present > 0 else 0.0

    # 5. xsltproc.log no fatal
    xs_score = 0.0
    xs = rd / "xsltproc.log"
    if xs.exists():
        try:
            txt = xs.read_text()
            if "fatal" not in txt.lower() and "error" not in txt.lower():
                xs_score = 1.0
            elif "fatal" not in txt.lower():
                xs_score = 0.5
        except Exception: pass
    s["xsltproc_clean"] = xs_score

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
    vlm_keys = ["vlm_bluefish_editor","vlm_xml_highlight","vlm_outline_visible","vlm_html_rendered"]
    if vlm_score_rubric and (rd / "view_bluefish_outline.png").exists():
        rubric = {
            "vlm_bluefish_editor": "Bluefish 截图能看到编辑器 + 行号",
            "vlm_xml_highlight": "XML 内容有语法高亮(关键字 / tag 不同色)",
            "vlm_outline_visible": "outline 截图能看到 tag 树结构",
            "vlm_html_rendered": "Firefox 截图显示渲染的 DocBook HTML(标题 / 段落 / 链接)",
        }
        try:
            imgs = [str(rd / n) for n in ["view_bluefish_outline.png","view_firefox_html.png","view_bluefish_final.png"] if (rd / n).exists()]
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 Bluefish XML editor + Firefox HTML 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            for k in rubric: s[k] = 0.0
    # else: VLM 不可用时不写入 vlm_* 键，避免拉低 base 分母

    # GUI hard-gate sub-scores: trajectory diversity + chrome OCR + window geometry
    import hashlib
    try:
        from PIL import Image as _PILImage
    except Exception:
        _PILImage = None
    gui_shot_paths = [rd / n for n in gui_shots if (rd / n).exists() and (rd / n).stat().st_size >= 50 * 1024]
    if len(gui_shot_paths) >= 4:
        hashes = set(hashlib.md5(p.read_bytes()).hexdigest() for p in gui_shot_paths)
        gui_diversity = len(hashes) / max(1, len(gui_shot_paths))
    else:
        gui_diversity = 0.0
    s["gui_real_interaction"] = 1.0 if gui_diversity >= 1.0 else (0.5 if gui_diversity >= 0.75 else 0.0)

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

    chrome_kws = ["Bluefish", "Document", "XML", "Outline", "Firefox",
                  "File", "Edit", "View", "Tools", "section", "chapter"]
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

    # 加权综合：核心交付 60% / GUI 证据 30% / 辅助 10%
    core_keys = ["cli_artifacts", "extra_artifacts", "xmllint_clean", "html_rendered", "xsltproc_clean"]
    gui_keys = ["gui_screenshots_count", "gui_screenshots_ocr", "gui_real_interaction",
                "gui_window_geometry", "gui_chrome_ocr"]
    aux_keys = ["fix_report"]
    vlm_keys_present = [k for k in s if k.startswith("vlm_")]

    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vals) / len(vals) if vals else 0.0

    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys + vlm_keys_present)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # 多层 hard gate（v2 收紧）
    if not has_cli: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.25)
    if s["xmllint_clean"] < 0.7: base = min(base, 0.40)
    if s["xmllint_clean"] < 0.4: base = min(base, 0.30)
    if s["html_rendered"] < 0.7: base = min(base, 0.50)
    if s["html_rendered"] < 0.4: base = min(base, 0.35)
    # GUI 真实交互 hard gate：截图全相同/缺失 → 直接封顶 0.35
    if s.get("gui_real_interaction", 0) < 0.5: base = min(base, 0.35)
    if s.get("gui_chrome_ocr", 0) < 0.5: base = min(base, 0.50)
    if s.get("gui_chrome_ocr", 0) < 0.3: base = min(base, 0.40)
    if s.get("gui_window_geometry", 0) < 0.5: base = min(base, 0.55)
    # VLM 不可用时整体封顶 0.6（不能没 VLM 也满分）
    if not vlm_keys_present:
        base = min(base, 0.60)
    else:
        vlm_avg = sum(s[k] for k in vlm_keys_present) / len(vlm_keys_present)
        if vlm_avg < 0.6: base = min(base, 0.55)
        if vlm_avg < 0.4: base = min(base, 0.40)

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
