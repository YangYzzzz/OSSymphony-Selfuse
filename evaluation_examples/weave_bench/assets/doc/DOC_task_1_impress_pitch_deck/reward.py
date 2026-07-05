# Auto-generated from WeaveBench task DOC_task_1_impress_pitch_deck.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

from pathlib import Path
try:
    from pdf2image import convert_from_path
except ImportError:
    convert_from_path = None
try:
    import pytesseract
except ImportError:
    pytesseract = None
import zipfile, re
from PIL import Image
import numpy as np

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    r={"checks":{},"overall_score":0.0}; s=0; t=7
    pdf=workspace/"pitch.pdf"
    if pdf.exists():
        pgs = []
        if convert_from_path:
            try:
                pgs = convert_from_path(str(pdf), dpi=100)
            except Exception:
                pgs = []
        if not pgs:
            # Fall back to pdfinfo for page count
            try:
                import subprocess
                info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                                       text=True, timeout=15).stdout
                npages = 0
                for line in info.splitlines():
                    if line.startswith("Pages:"):
                        npages = int(line.split()[1]); break
                # synthesize a stub list to satisfy len() check
                pgs = [None] * npages
            except Exception:
                pgs = []
        if len(pgs)==14: r["checks"]["pages=14"]=True; s+=1
        ok=0
        for i,p in enumerate(pgs[:14],1):
            if p is None: continue  # pdfinfo fallback — no PIL image
            w,h=p.size
            crop=p.crop((int(w*0.85),int(h*0.85),w,h))
            try:
                tx=pytesseract.image_to_string(crop) if pytesseract else ""
            except Exception:
                tx=""
            if str(i) in tx: ok+=1
        if ok>=10: r["checks"][f"pagenums={ok}"]=True; s+=1
        # circles on page 9
        try:
            import cv2
            if pgs[8] is None: raise RuntimeError("no image")
            a=cv2.cvtColor(np.array(pgs[8]),cv2.COLOR_RGB2GRAY)
            cs=cv2.HoughCircles(a,cv2.HOUGH_GRADIENT,1,30,param1=80,param2=30,minRadius=10,maxRadius=80)
            if cs is not None and len(cs[0])>=5:
                r["checks"]["timeline_circles"]=True; s+=1
        except: pass
    sd=workspace/"slides"
    if sd.exists() and len(list(sd.glob("slide_*.png")))>=14:
        r["checks"]["per_slide_png"]=True; s+=1
    odp=workspace/"draft.odp"
    if odp.exists():
        try:
            with zipfile.ZipFile(odp) as z:
                content=z.read("content.xml").decode("utf-8",errors="ignore")
            if len(re.findall(r"<draw:circle", content))>=5:
                r["checks"]["odp_circles"]=True; s+=1
            if "Montserrat" in content or "Inter" in content:
                r["checks"]["fonts"]=True; s+=1
        except: pass
    log=workspace/"actions.log"
    if not log.exists() or "python-uno" not in log.read_text(errors="ignore"):
        r["checks"]["no_uno"]=True; s+=1

    # New: Master Slide check (master-page style with font + logo)
    if odp.exists():
        try:
            with zipfile.ZipFile(odp) as z:
                styles_xml = z.read("styles.xml").decode("utf-8", errors="ignore")
            if re.search(r"<style:master-page[^>]+>.+?Montserrat.+?</style:master-page>", styles_xml, re.DOTALL):
                r["checks"]["master_font_set"] = True; s += 1; t += 1
            if "<draw:image" in styles_xml or "logo" in styles_xml.lower():
                r["checks"]["master_logo"] = True; s += 1; t += 1
            # Animation paths
            if "presentation:animation" in content or "presentation:path" in content:
                r["checks"]["has_animation"] = True; s += 1; t += 1
            # Notes
            if content.count("<presentation:notes") >= 14:
                r["checks"]["notes_per_page"] = True; s += 1; t += 1
        except Exception: pass

    # PDF outline (bookmarks) check — only credit when outline actually exists
    if pdf.exists():
        try:
            n_outline = 0
            try:
                import pikepdf
                with pikepdf.open(str(pdf)) as pp:
                    n_outline = len(list(pp.open_outline().root))
            except Exception:
                n_outline = 0
            t += 1
            if n_outline >= 1:
                r["checks"]["pdf_outline"] = True; s += 1
            if n_outline >= 14:
                r["checks"]["pdf_outline_count"] = n_outline
        except Exception: pass

    # New: 4 Impress UI screenshots — check both workspace/ and workspace/results/
    rd_results = workspace
    rd_alt = workspace / "results"
    ui_shots = ["view_01_master_slide_edit.png","view_02_animation_dialog.png",
                "view_03_smart_alignment.png","view_04_export_pdf_dialog.png"]
    ui_present = sum(1 for n in ui_shots
                     if (rd_results/n).exists() or (rd_alt/n).exists())
    r["checks"]["impress_ui_shots"] = ui_present / len(ui_shots)
    s += ui_present / len(ui_shots); t += 1
    base = s/t
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    sd=workspace/"slides"
    slide_imgs = sorted(sd.glob("slide_*.png"))[:6] if sd.exists() else []
    if vlm_score_rubric and slide_imgs:
        rubric = {
            "vlm_consistent_style": "多张幻灯片在配色、字体、版式上保持一致的视觉风格",
            "vlm_no_overflow": "正文文本无明显溢出 / 截断 / 重叠图形的现象",
            "vlm_meaningful_visuals": "至少 2 张幻灯片含有有意义的图表/图标/插图（非空白页或纯文字堆砌）",
            "vlm_title_hierarchy": "每页标题字号明显大于正文，建立清晰的视觉层级",
        }
        vlm = vlm_score_rubric([str(p) for p in slide_imgs], rubric, instruction="评估 LibreOffice Impress pitch deck 的设计质量。")
        for k in rubric: r["checks"][k] = vlm.get(k, 0.0)
        r["judge_method"] = vlm.get("judge_method", "failed")
        vlm_avg = sum(vlm.get(k, 0.0) for k in rubric)/len(rubric)
        final = (base + vlm_avg) / 2
    else:
        # No VLM available → cap at 0.6 to prevent silent full-score on degraded judging
        final = min(base, 0.6)
        r["judge_method"] = r.get("judge_method", "no_vlm_capped")

    # Weighted re-aggregation: core (60%) + gui (30%) + aux (10%)
    core_keys = ["pages=14", "odp_circles", "fonts", "master_font_set",
                 "master_logo", "has_animation", "notes_per_page", "per_slide_png"]
    gui_keys  = ["impress_ui_shots", "no_uno"]
    aux_keys  = ["pdf_outline", "timeline_circles"]
    def _v(k):
        v = r["checks"].get(k, 0.0)
        return float(v) if isinstance(v, (int, float, bool)) else 0.0
    core = sum(_v(k) for k in core_keys) / len(core_keys)
    gui  = sum(_v(k) for k in gui_keys)  / len(gui_keys)
    aux  = sum(_v(k) for k in aux_keys)  / len(aux_keys)
    weighted = 0.6 * core + 0.3 * gui + 0.1 * aux
    final = min(final, max(weighted, 0.0) * 0.5 + final * 0.5)

    # Multi-layer hard gates
    if not (workspace / "pitch.pdf").exists():
        final = min(final, 0.30)
    if not r["checks"].get("pages=14"):
        final = min(final, 0.40)
    if not r["checks"].get("odp_circles"):
        final = min(final, 0.40)
    if not r["checks"].get("master_font_set"):
        final = min(final, 0.40)
    if not r["checks"].get("has_animation"):
        final = min(final, 0.50)
    if not r["checks"].get("notes_per_page"):
        final = min(final, 0.50)
    # GUI evidence gate: agent must have produced ≥ 3 of 4 UI screenshots
    if float(r["checks"].get("impress_ui_shots", 0.0)) < 0.75:
        final = min(final, 0.50)

    r["overall_score"] = round(float(max(0.0, final)), 3)
    return r


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
