# Auto-generated from WeaveBench task DOC_task_3_okular_annotate_fact.
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
    gt_dir = Path("/tmp_workspace/gt")
    scores = {}

    rep = rd / "report.md"
    text = rep.read_text(encoding="utf-8", errors="ignore") if rep.exists() else ""
    scores["report_exists"] = 1.0 if text.strip() else 0.0

    pdf = rd / "facts.pdf"
    scores["pdf_exists"] = 1.0 if (pdf.exists() and pdf.stat().st_size >= 5 * 1024) else 0.0

    # 2. /Highlight annotation present
    pdf_bytes = pdf.read_bytes() if pdf.exists() else b""
    scores["has_highlight_annot"] = 1.0 if (b"/Highlight" in pdf_bytes) else 0.0

    # 3. popup text contains "factually wrong"
    has_popup = False
    for needle in [b"factually wrong", b"factually\\040wrong", b"FACTUALLY WRONG"]:
        if needle in pdf_bytes:
            has_popup = True
            break
    if not has_popup:
        utf16 = "factually wrong".encode("utf-16-be")
        if utf16 in pdf_bytes:
            has_popup = True
    scores["popup_text_present"] = 1.0 if has_popup else 0.0

    # 4. highlight /Rect IoU vs sentence bbox
    iou = 0.0
    scores["mars_bbox_found"] = 0.0
    if pdf.exists():
        try:
            out = subprocess.run(
                ["pdftotext", "-bbox-layout", str(pdf), "-"],
                capture_output=True, text=True, timeout=30).stdout
            mars_bbox = None
            for ln in out.splitlines():
                if "Mars is the largest" in ln:
                    bb_m = re.search(r'xMin="([\d.]+)"\s+yMin="([\d.]+)"\s+xMax="([\d.]+)"\s+yMax="([\d.]+)"', ln)
                    if bb_m:
                        mars_bbox = tuple(float(x) for x in bb_m.groups())
                        break
            scores["mars_bbox_found"] = 1.0 if mars_bbox else 0.0
            rect_matches = re.findall(rb"/Rect\s*\[\s*([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s*\]", pdf_bytes)
            highlight_rects = []
            for hm in re.finditer(rb"/Subtype\s*/Highlight[\s\S]{0,2000}?/Rect\s*\[\s*([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s*\]", pdf_bytes):
                highlight_rects.append(hm.groups())
            for hm in re.finditer(rb"/Rect\s*\[\s*([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s+([\d.\-]+)\s*\][\s\S]{0,2000}?/Subtype\s*/Highlight", pdf_bytes):
                highlight_rects.append(hm.groups())
            candidates = highlight_rects if highlight_rects else rect_matches
            if mars_bbox and candidates:
                mx0, my0, mx1, my1 = mars_bbox
                best_iou = 0.0
                for r in candidates:
                    rx0, ry0, rx1, ry1 = (float(x) for x in r)
                    if rx0 > rx1: rx0, rx1 = rx1, rx0
                    if ry0 > ry1: ry0, ry1 = ry1, ry0
                    ox = max(0, min(mx1, rx1) - max(mx0, rx0))
                    ux = max(mx1, rx1) - min(mx0, rx0)
                    if ux > 0:
                        x_iou = ox / ux
                        if x_iou > best_iou:
                            best_iou = x_iou
                iou = best_iou
        except Exception as e:
            scores["bbox_err"] = str(e)[:100]
    scores["highlight_iou"] = round(iou, 3)
    scores["highlight_position_ok"] = 1.0 if iou >= 0.3 else (0.5 if iou >= 0.15 else 0.0)

    # 5. wrong_sentence field
    m = re.search(r"wrong_sentence\s*[:=]\s*([^\n]+)", text)
    scores["wrong_sentence_field"] = 0.0
    if m:
        s = m.group(1).lower()
        if "mars" in s and "largest" in s:
            scores["wrong_sentence_field"] = 1.0

    # 6. tool_used + explanation
    scores["tool_field"] = 1.0 if re.search(r"tool_used\s*[:=]\s*\S+", text) else 0.0
    explain = "\n".join(
        ln for ln in text.splitlines()
        if not re.match(r"\s*(wrong_sentence|tool_used)\s*[:=]", ln, re.IGNORECASE)
    ).strip()
    scores["explanation_len"] = 1.0 if len(explain) >= 30 else (len(explain) / 30.0)

    # 7. proof.png — 强化反作弊：尺寸 + 分辨率
    pp = rd / "proof.png"
    proof_ok_size = pp.exists() and pp.stat().st_size >= 20 * 1024
    scores["proof_png"] = 1.0 if proof_ok_size else 0.0
    proof_resolution_ok = False
    if proof_ok_size and Image is not None:
        try:
            with Image.open(pp) as im:
                w, h = im.size
                scores["proof_w"] = w
                scores["proof_h"] = h
                if w >= 1024 and h >= 600:
                    proof_resolution_ok = True
        except Exception:
            pass
    scores["proof_resolution_ok"] = 1.0 if proof_resolution_ok else 0.0

    # 加权聚合：核心交付 60% / GUI 证据 30% / 辅助 10%
    core = (
        0.20 * scores["pdf_exists"] +
        0.25 * scores["has_highlight_annot"] +
        0.25 * scores["popup_text_present"] +
        0.30 * scores["highlight_position_ok"]
    )
    gui_evidence = (
        0.40 * scores["proof_png"] +
        0.30 * scores["proof_resolution_ok"] +
        0.30 * scores["wrong_sentence_field"]
    )
    aux = (
        0.30 * scores["report_exists"] +
        0.30 * scores["tool_field"] +
        0.40 * scores["explanation_len"]
    )
    base = 0.60 * core + 0.30 * gui_evidence + 0.10 * aux
    scores["core_score"] = round(core, 3)
    scores["gui_evidence_score"] = round(gui_evidence, 3)
    scores["aux_score"] = round(aux, 3)
    scores["overall_score"] = round(base, 3)

    # 多层结构性 hard gate（VLM 不可用也生效）
    if scores["has_highlight_annot"] < 1.0:
        scores["overall_score"] = min(scores["overall_score"], 0.40)
    if scores["popup_text_present"] < 1.0:
        scores["overall_score"] = min(scores["overall_score"], 0.40)
    if scores["highlight_position_ok"] < 0.5:
        scores["overall_score"] = min(scores["overall_score"], 0.50)
    if scores["wrong_sentence_field"] < 1.0:
        scores["overall_score"] = min(scores["overall_score"], 0.55)
    if scores["proof_png"] < 1.0 or scores["proof_resolution_ok"] < 1.0:
        scores["overall_score"] = min(scores["overall_score"], 0.55)

    # 8. VLM HARD GATE
    vlm_used = False
    if vlm_score_rubric and pp.exists() and pp.stat().st_size >= 20 * 1024:
        rubric = {
            "vlm_pdf_view":       "proof.png 是 PDF 阅读器界面 (Okular / Evince) 的截图;不是空白图、Hello World、源代码窗口。",
            "vlm_yellow_highlight": "proof.png 中能看到一段文字被黄色 / 半透明色块覆盖 — 即真有高亮 annotation 视觉效果。",
            "vlm_target_sentence": "proof.png 中可读出 'Mars is the largest planet' 这句话 (highlight 应该盖在这上面)。",
            "vlm_popup_visible":   "proof.png 中能看到 popup / sticky note 弹窗, 文字含 'factually wrong'。",
        }
        try:
            vlm = vlm_score_rubric([str(pp)], rubric,
                instruction="判断 proof.png 是否真显示了 Okular 把 'Mars is the largest planet' 这句话用黄色高亮 + popup 'factually wrong' 标注出来。")
            for k in rubric: scores[k] = vlm.get(k, 0.0)
            scores["judge_method"] = vlm.get("judge_method", "failed")
            if scores["judge_method"] != "failed":
                vlm_used = True
                vlm_avg = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
                scores["overall_score"] = round(0.5*base + 0.5*vlm_avg, 3)
                # HARD GATES — 阈值上拉
                if scores.get("vlm_pdf_view", 0.0) < 0.7:
                    scores["overall_score"] = min(scores["overall_score"], 0.25)
                if scores.get("vlm_target_sentence", 0.0) < 0.7:
                    scores["overall_score"] = min(scores["overall_score"], 0.45)
                if scores.get("vlm_yellow_highlight", 0.0) < 0.7:
                    scores["overall_score"] = min(scores["overall_score"], 0.50)
                if scores.get("vlm_popup_visible", 0.0) < 0.6:
                    scores["overall_score"] = min(scores["overall_score"], 0.55)
                # 全部 VLM 维度都低 → 视为伪截图
                if vlm_avg < 0.4:
                    scores["overall_score"] = min(scores["overall_score"], 0.30)
        except Exception:
            pass
    # VLM 不可用时退化分上限封顶 0.6（不能让无 VLM 也满分）
    if not vlm_used:
        scores["vlm_unavailable_cap"] = 0.6
        scores["overall_score"] = min(scores["overall_score"], 0.60)
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
