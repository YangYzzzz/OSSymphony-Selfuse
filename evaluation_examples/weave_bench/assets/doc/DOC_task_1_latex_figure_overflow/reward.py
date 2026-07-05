# Auto-generated from WeaveBench task DOC_task_1_latex_figure_overflow.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    import re, subprocess
    from pathlib import Path
    try:
        from PIL import Image
    except Exception:
        Image = None
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    rd = Path("/tmp_workspace/results")
    ws = Path("/tmp_workspace")
    scores = {}

    rep = rd / "report.md"
    text = rep.read_text(encoding="utf-8", errors="ignore") if rep.exists() else ""
    scores["report_exists"] = 1.0 if text.strip() else 0.0

    # 1. results/paper.pdf exists
    pdf = rd / "paper.pdf"
    scores["pdf_exists"] = 1.0 if (pdf.exists() and pdf.stat().st_size >= 5 * 1024) else 0.0

    # 2. width fix in tex
    tex = ws / "paper.tex"
    scores["width_fixed"] = 0.0
    if tex.exists():
        t = tex.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"\\includegraphics\[[^]]*width\s*=\s*([0-9.]+)\\textwidth", t)
        if m:
            w = float(m.group(1))
            scores["width_value"] = w
            if w <= 1.0:
                scores["width_fixed"] = 1.0

    # 3. same-page check via pdftotext -layout
    scores["same_page"] = 0.0
    if pdf.exists():
        try:
            out = subprocess.run(
                ["pdftotext", "-layout", str(pdf), "-"],
                capture_output=True, text=True, timeout=30).stdout
            # split per page (pdftotext separates with form feed \f)
            pages = out.split("\f")
            for pg in pages:
                if ("Figure 1:" in pg or "Figure\u00a01:" in pg) and \
                   ("Figure 1 shows" in pg or "Figure~1 shows" in pg or "Figure\u00a01 shows" in pg):
                    scores["same_page"] = 1.0
                    break
        except Exception as e:
            scores["pdftotext_err"] = str(e)[:100]

    # 4. report fields
    scores["width_field"] = 1.0 if re.search(r"width_token\s*[:=]\s*\S+", text) else 0.0
    sp_m = re.search(r"same_page\s*[:=]\s*(yes|no)", text, re.IGNORECASE)
    scores["same_page_field_yes"] = 1.0 if (sp_m and sp_m.group(1).lower() == "yes") else 0.0
    scores["tool_field"] = 1.0 if re.search(r"tool_used\s*[:=]\s*\S+", text) else 0.0
    explain = "\n".join(
        ln for ln in text.splitlines()
        if not re.match(r"\s*(width_token|same_page|tool_used)\s*[:=]", ln, re.IGNORECASE)
    ).strip()
    scores["explanation_len"] = 1.0 if len(explain) >= 30 else (len(explain) / 30.0)

    # 5. proof.png — must be a real screenshot, not a tiny placeholder
    pp = rd / "proof.png"
    pp_size = pp.stat().st_size if pp.exists() else 0
    scores["proof_png"] = 1.0 if (pp.exists() and pp_size >= 20 * 1024) else (
        0.4 if (pp.exists() and pp_size >= 5 * 1024) else 0.0
    )
    scores["proof_png_size"] = pp_size
    # resolution gate: real desktop screenshot should be >= 1024x600
    scores["proof_png_resolution"] = 0.0
    if pp.exists() and Image is not None:
        try:
            with Image.open(pp) as im:
                w, h = im.size
                scores["proof_png_w"] = w
                scores["proof_png_h"] = h
                if w >= 1024 and h >= 600:
                    scores["proof_png_resolution"] = 1.0
                elif w >= 800 and h >= 480:
                    scores["proof_png_resolution"] = 0.5
        except Exception:
            pass

    # 加权分组：core 60% / gui 30% / aux 10%
    core = (
        0.45 * scores["width_fixed"] +
        0.45 * scores["same_page"] +
        0.10 * scores["pdf_exists"]
    )
    gui = (
        0.55 * scores["proof_png"] +
        0.45 * scores["proof_png_resolution"]
    )
    aux = (
        0.20 * scores["report_exists"] +
        0.20 * scores["width_field"] +
        0.20 * scores["same_page_field_yes"] +
        0.20 * scores["tool_field"] +
        0.20 * scores["explanation_len"]
    )
    base = 0.6 * core + 0.3 * gui + 0.1 * aux
    scores["core"] = round(core, 3)
    scores["gui"] = round(gui, 3)
    scores["aux"] = round(aux, 3)
    scores["overall_score"] = round(base, 3)

    # Structural hard gates (无 VLM 也必须卡住退化路径)
    if scores.get("width_fixed", 0.0) < 0.5 or scores.get("same_page", 0.0) < 0.5:
        scores["overall_score"] = min(scores["overall_score"], 0.4)
        base = min(base, 0.4)
    if scores.get("proof_png", 0.0) < 0.5 or scores.get("proof_png_resolution", 0.0) < 0.5:
        scores["overall_score"] = min(scores["overall_score"], 0.5)
        base = min(base, 0.5)

    # 6. VLM HARD GATE
    if vlm_score_rubric and pp.exists() and pp_size >= 20 * 1024:
        rubric = {
            "vlm_pdf_view":           "proof.png 是 PDF 阅读器 (TeXstudio 预览面板 / Okular / Evince) 或 pdftoppm 渲染的 PDF 页面截图;不是空白图、终端文本、源代码窗口。",
            "vlm_figure_visible":     "proof.png 中能直接看到一张柱状图 (Q3 throughput 直方图) + 它的 caption 'Figure 1: Sustained throughput ...'。",
            "vlm_reference_visible":  "proof.png 同一张图里能直接看到正文 'Figure 1 shows' 那段话 — 即图与引用它的段落同时出现在画面里。",
            "vlm_no_overflow":        "proof.png 中那张图没有明显冲出右边距 (没有图被裁/超出页面边界)。",
        }
        try:
            vlm = vlm_score_rubric([str(pp)], rubric,
                instruction="判断 PDF 截图里 figure 是否与 'Figure 1 shows' 段落同页且不出血。")
            for k in rubric: scores[k] = vlm.get(k, 0.0)
            scores["judge_method"] = vlm.get("judge_method", "failed")
            vlm_avg = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
            scores["vlm_avg"] = round(vlm_avg, 3)
            # VLM 占 50%；同时再次卡硬阈值
            scores["overall_score"] = round(0.5*base + 0.5*vlm_avg, 3)
            # HARD GATES (上拉)
            if scores.get("vlm_pdf_view", 0.0) < 0.7:
                scores["overall_score"] = min(scores["overall_score"], 0.25)
            if scores.get("vlm_reference_visible", 0.0) < 0.7:
                scores["overall_score"] = min(scores["overall_score"], 0.45)
            if scores.get("vlm_figure_visible", 0.0) < 0.6:
                scores["overall_score"] = min(scores["overall_score"], 0.45)
            if scores.get("vlm_no_overflow", 0.0) < 0.5:
                scores["overall_score"] = min(scores["overall_score"], 0.55)
            if vlm_avg < 0.4:
                scores["overall_score"] = min(scores["overall_score"], 0.30)
        except Exception:
            pass
    else:
        # VLM 不可用 → 封顶 0.6，避免无视觉证据也满分
        scores["judge_method"] = "vlm_unavailable"
        scores["overall_score"] = min(scores["overall_score"], 0.6)
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
