# Auto-generated from WeaveBench task DOC_task_0_latex_layout_fix.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import subprocess, re, hashlib
from pathlib import Path
try:
    import pytesseract
except ImportError:
    pytesseract = None
from PIL import Image

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    r = {"checks": {}, "overall_score": 0.0}
    # bucketed sub-scores: core deliverable (0..1), gui evidence (0..1), aux (0..1)
    core_pts, core_max = 0, 4   # compile_ok, overfull<3, pages>=9, strategy_used
    gui_pts,  gui_max  = 0, 4   # screens exist+sized, screens md5 unique, tex_toolbar OCR, log_before
    aux_pts,  aux_max  = 0, 1   # changes>=20

    tex = workspace / "paper.tex"
    overfull_n = None
    if tex.exists():
        c = tex.read_text(errors="ignore")
        # starter already ships \usepackage{tabularx}? No — starter ships without it
        # in v3. Require agent to add \sloppy or \FloatBarrier explicitly.
        if any(k in c for k in ["\\sloppy", "FloatBarrier"]):
            r["checks"]["strategy_used"] = True; core_pts += 1
        try:
            p = subprocess.run(["pdflatex", "-interaction=nonstopmode", "paper.tex"],
                               cwd=str(workspace), capture_output=True, timeout=120)
            if p.returncode == 0:
                r["checks"]["compile_ok"] = True; core_pts += 1
            log = workspace / "paper.log"
            if log.exists():
                overfull_n = len(re.findall(r"Overfull", log.read_text(errors="ignore")))
                if overfull_n < 3:
                    r["checks"][f"overfull={overfull_n}<3"] = True; core_pts += 1
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            pass
        pdf = workspace / "paper.pdf"
        npages = 0
        try:
            from pdf2image import convert_from_path
            pgs = convert_from_path(str(pdf), dpi=80)
            npages = len(pgs)
        except Exception:
            try:
                info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                                      text=True, timeout=15).stdout
                for line in info.splitlines():
                    if line.startswith("Pages:"):
                        npages = int(line.split()[1]); break
            except Exception:
                pass
        if npages >= 9:
            r["checks"]["pages>=9"] = True; core_pts += 1

    # --- GUI evidence: screenshots must exist, be sized, md5-unique ---
    shots = [workspace / f"pdf_p{n}.png" for n in (3, 6, 9)]
    if all(p.exists() for p in shots):
        sized = True
        for p in shots:
            try:
                if p.stat().st_size < 5 * 1024:
                    sized = False; break
                with Image.open(p) as im:
                    w, h = im.size
                if w < 1024 or h < 600:
                    sized = False; break
            except Exception:
                sized = False; break
        if sized:
            r["checks"]["screens_sized"] = True; gui_pts += 1
        try:
            md5s = {hashlib.md5(p.read_bytes()).hexdigest() for p in shots}
            if len(md5s) == 3:
                r["checks"]["screens_unique"] = True; gui_pts += 1
        except Exception:
            pass

    cm = workspace / "changes.md"
    if cm.exists() and cm.read_text(errors="ignore").count("\n- ") >= 20:
        r["checks"]["changes>=20"] = True; aux_pts += 1

    # log_before.png: evidence that agent compiled once and screenshotted Log panel
    log_before = workspace / "log_before.png"
    if log_before.exists():
        try:
            if log_before.stat().st_size >= 5 * 1024:
                r["checks"]["log_before"] = True; gui_pts += 1
        except Exception:
            pass

    # OCR for TeXstudio toolbar: require ≥2 of the 3 screenshots to hit a
    # TeXstudio keyword (raises the bar vs. the v1 single-screenshot check).
    if pytesseract is not None:
        hits = 0
        for p in shots:
            if not p.exists():
                continue
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k in tx for k in ["TeXstudio", "Build", "Log", "Messages"]):
                    hits += 1
            except Exception:
                pass
        if hits >= 2:
            r["checks"]["tex_toolbar"] = True; gui_pts += 1
        r["checks"]["tex_toolbar_hits"] = hits

    core = core_pts / core_max
    gui  = gui_pts  / gui_max
    aux  = aux_pts  / aux_max
    base = round(0.6 * core + 0.3 * gui + 0.1 * aux, 3)

    # --- VLM rubric ---
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    pdf_imgs = [str(p) for p in shots if p.exists()]
    vlm_avg = None
    if vlm_score_rubric and pdf_imgs:
        rubric = {
            "vlm_no_overfull_text": "页面内容未出现明显超出页边的文字、表格或公式（无 overfull box）",
            "vlm_figure_aligned": "图表整齐位于其引用段落附近，未漂离上下文（不在错误的页码末尾）",
            "vlm_table_fits_page": "表格不溢出页面、列宽合理、表头清晰",
            "vlm_typography_normal": "正文段落对齐自然，无超长间距、不规则换行或单字行尾",
        }
        vlm = vlm_score_rubric(pdf_imgs[:3], rubric, instruction="评估 LaTeX 修复后的 PDF 排版质量。")
        for k in rubric:
            r["checks"][k] = vlm.get(k, 0.0)
        r["judge_method"] = vlm.get("judge_method", "failed")
        vlm_avg = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
        zero_overfull = (overfull_n is not None and overfull_n == 0) and r["checks"].get("compile_ok", False)
        if zero_overfull:
            overall = round(0.7 * base + 0.3 * vlm_avg, 3)
        else:
            overall = round(0.5 * base + 0.5 * vlm_avg, 3)
    else:
        overall = base

    # --- Hard gates (multi-layer, raised vs. v1) ---
    # 1. Core deliverable broken → cap 0.40
    if not (r["checks"].get("compile_ok") and r["checks"].get("strategy_used")):
        overall = min(overall, 0.40)
    # 2. PDF too short → cap 0.45
    if not r["checks"].get("pages>=9"):
        overall = min(overall, 0.45)
    # 3. GUI evidence missing (no sized screenshots OR not md5-unique) → cap 0.45
    if not (r["checks"].get("screens_sized") and r["checks"].get("screens_unique")):
        overall = min(overall, 0.45)
    # 4. TeXstudio OCR not detected (only enforce when OCR backend available) → cap 0.50
    if pytesseract is not None and not r["checks"].get("tex_toolbar"):
        overall = min(overall, 0.50)
    # 5. VLM unavailable → cap 0.60 (cannot reach top tier without visual judge)
    if vlm_avg is None:
        overall = min(overall, 0.60)
    # 6. Strict VLM degradation
    if vlm_avg is not None:
        if vlm_avg < 0.4:
            overall = min(overall, 0.30)
        elif vlm_avg < 0.6:
            overall = min(overall, 0.45)

    r["overall_score"] = round(overall, 3)
    r["sub_scores"] = {"core": round(core, 3), "gui": round(gui, 3), "aux": round(aux, 3),
                       "base": base, "vlm": vlm_avg}
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
