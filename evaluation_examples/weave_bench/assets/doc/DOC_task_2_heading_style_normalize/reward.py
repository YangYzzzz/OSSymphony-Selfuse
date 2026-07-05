# Auto-generated from WeaveBench task DOC_task_2_heading_style_normalize.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    import re, zipfile, subprocess
    from pathlib import Path
    try:
        from PIL import Image
    except Exception:
        Image = None
    try:
        from _judge_helper import vlm_score_rubric, audit_chat_jsonl_for_banned
    except Exception:
        vlm_score_rubric = None
        audit_chat_jsonl_for_banned = None

    ws = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = ws / "results"
    gt_dir = ws.parent / "gt" if (ws.parent / "gt").exists() else Path("/tmp_workspace/gt")
    scores = {}

    rep = rd / "report.md"
    text = rep.read_text(encoding="utf-8", errors="ignore") if rep.exists() else ""
    text_l = text.lower()
    scores["report_exists"] = 1.0 if text.strip() else 0.0

    # 1+2. odt + heading count (exact 15 required for full credit)
    odt = rd / "report.odt"
    scores["odt_exists"] = 1.0 if odt.exists() else 0.0
    scores["heading_count_15"] = 0.0
    h1_count = 0
    if odt.exists():
        try:
            with zipfile.ZipFile(odt) as z:
                content = z.read("content.xml").decode("utf-8", errors="ignore")
            h1_count = len(re.findall(r'<text:h[^>]*outline-level="1"', content))
            scores["heading_count"] = h1_count
            if h1_count == 15:
                scores["heading_count_15"] = 1.0
            elif h1_count == 14:
                scores["heading_count_15"] = 0.5
            elif h1_count >= 12:
                scores["heading_count_15"] = 0.25
        except Exception as e:
            scores["odt_xml_err"] = str(e)[:120]

    # 3. PDF + sections (require all 15 for full credit)
    pdf = rd / "report.pdf"
    scores["pdf_exists"] = 1.0 if (pdf.exists() and pdf.stat().st_size >= 10*1024) else 0.0
    scores["pdf_has_15_sections"] = 0.0
    if pdf.exists():
        try:
            out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                                  capture_output=True, text=True, timeout=30).stdout
            sections = ["Background","Methodology","Results","Discussion","Conclusion",
                        "Appendix A","Appendix B","Limitations","Future Work",
                        "Acknowledgments","Funding","References","Glossary","Index","Author Bios"]
            present = sum(1 for s in sections if s in out)
            scores["pdf_section_count"] = present
            if present == 15:
                scores["pdf_has_15_sections"] = 1.0
            elif present >= 14:
                scores["pdf_has_15_sections"] = 0.5
            elif present >= 10:
                scores["pdf_has_15_sections"] = 0.25
        except Exception as e:
            scores["pdftotext_err"] = str(e)[:80]

    # 4. wrong_titles match (full credit only at 7/7)
    expected_set = set()
    if (gt_dir / "expected_wrong_titles.txt").exists():
        expected_set = {t.strip() for t in (gt_dir / "expected_wrong_titles.txt").read_text().split(",") if t.strip()}
    m = re.search(r"wrong_titles\s*[:=]\s*([^\n]+)", text)
    scores["wrong_titles_match"] = 0.0
    matched_titles = 0
    if m and expected_set:
        reported = {t.strip().rstrip(".,;:") for t in m.group(1).split(",") if t.strip()}
        matched_titles = len(expected_set & reported)
        # penalize over-reporting (false positives) too
        false_positives = len(reported - expected_set)
        scores["wrong_titles_matched"] = matched_titles
        scores["wrong_titles_false_positives"] = false_positives
        if matched_titles == 7 and false_positives == 0:
            scores["wrong_titles_match"] = 1.0
        elif matched_titles >= 6 and false_positives <= 1:
            scores["wrong_titles_match"] = 0.6
        elif matched_titles >= 4:
            scores["wrong_titles_match"] = matched_titles / 14.0  # capped 0.5

    # 5. tool_used (whitelist) + explanation + GUI mention (BOTH terms)
    tool_whitelist = {"libreoffice", "lowriter", "writer", "navigator", "style_dropdown"}
    tm = re.search(r"tool_used\s*[:=]\s*([A-Za-z_][\w_]*)", text)
    scores["tool_field"] = 1.0 if (tm and tm.group(1).strip().lower() in tool_whitelist) else 0.0
    explain = "\n".join(
        ln for ln in text.splitlines()
        if not re.match(r"\s*(wrong_titles|tool_used)\s*[:=]", ln, re.IGNORECASE)
    ).strip()
    scores["explanation_len"] = 1.0 if len(explain) >= 80 else (len(explain) / 80.0)
    has_navigator = ("navigator" in text_l) or ("f5" in text_l)
    has_style = ("style dropdown" in text_l) or ("样式下拉" in text) or ("style box" in text_l) or ("paragraph style" in text_l)
    if has_navigator and has_style:
        scores["mentions_gui"] = 1.0
    elif has_navigator or has_style:
        scores["mentions_gui"] = 0.5
    else:
        scores["mentions_gui"] = 0.0

    # 6. proof.png — size + resolution
    pp = rd / "proof.png"
    scores["proof_png"] = 0.0
    proof_ok = False
    if pp.exists() and pp.stat().st_size >= 20 * 1024:
        if Image is not None:
            try:
                with Image.open(pp) as im:
                    w, h = im.size
                scores["proof_resolution"] = f"{w}x{h}"
                if w >= 1024 and h >= 600:
                    scores["proof_png"] = 1.0
                    proof_ok = True
                elif w >= 800 and h >= 480:
                    scores["proof_png"] = 0.5
            except Exception as e:
                scores["proof_img_err"] = str(e)[:80]
        else:
            scores["proof_png"] = 0.5  # cannot verify resolution without PIL

    # 7. audit (extended banned list)
    audit_cap = None
    if audit_chat_jsonl_for_banned:
        a = audit_chat_jsonl_for_banned([
            "import uno",
            "python3-uno",
            "unohelper",
            "uno:socket",
            "StarOffice.ServiceManager",
            "unzip /tmp_workspace/report.odt",
            "unzip report.odt",
            "zipfile.ZipFile",
            "<text:h",
            "<text:p ",
            "outline-level=",
            "sed -i",
        ])
        scores["audit_banned"] = a.get("any_banned", False)
        scores["audit_screenshots"] = a.get("computer_screenshots", 0)
        if a.get("any_banned"):
            audit_cap = 0.25

    # Weighted overall: core 60% / GUI evidence 30% / aux 10%
    core = (
        0.20 * scores["odt_exists"] +
        0.40 * scores["heading_count_15"] +
        0.15 * scores["pdf_exists"] +
        0.25 * scores["pdf_has_15_sections"]
    )
    gui = (
        0.55 * scores["wrong_titles_match"] +
        0.30 * scores["mentions_gui"] +
        0.15 * scores["proof_png"]
    )
    aux = (
        0.30 * scores["report_exists"] +
        0.30 * scores["tool_field"] +
        0.40 * scores["explanation_len"]
    )
    base = 0.6 * core + 0.3 * gui + 0.1 * aux
    scores["score_core"] = round(core, 3)
    scores["score_gui"] = round(gui, 3)
    scores["score_aux"] = round(aux, 3)

    # Stricter non-VLM structural hard gates
    if scores["heading_count_15"] < 1.0:
        base = min(base, 0.40)
    if h1_count == 0:
        base = min(base, 0.20)
    if scores["wrong_titles_match"] < 0.6:
        base = min(base, 0.45)
    if scores["pdf_has_15_sections"] < 1.0:
        base = min(base, 0.60)
    if not proof_ok:
        base = min(base, 0.50)
    scores["overall_score"] = round(base, 3)

    # 8. VLM HARD GATE — stricter caps and penalty for missing VLM
    vlm_done = False
    if vlm_score_rubric and proof_ok:
        rubric = {
            "vlm_relevant_view":  "proof.png 是 LibreOffice Writer Navigator 面板,或 Style 下拉框,或一份 PDF 的 TOC 页面;不是空白图、错误页、终端文本、桌面壁纸、文件管理器。",
            "vlm_lots_headings":  "proof.png 中能清楚数出 ≥ 14 条章节标题(无论是 Navigator entries 还是 TOC 行);恰好 15 条最佳。",
            "vlm_no_h2_distractor":"proof.png 如果是 Navigator 截图,所有条目都在同一缩进层级 (即都是 H1),不再有 2 条以 H2 缩进;如果是 TOC,所有项是同级。",
        }
        try:
            vlm = vlm_score_rubric([str(pp)], rubric,
                instruction="判断 proof.png 是否真显示了 LO Writer Navigator 含 15 条同级 H1 (修复后状态)。")
            for k in rubric: scores[k] = vlm.get(k, 0.0)
            scores["judge_method"] = vlm.get("judge_method", "failed")
            vlm_avg = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
            if scores.get("judge_method") not in ("failed", None, ""):
                vlm_done = True
                scores["overall_score"] = round(0.5 * base + 0.5 * vlm_avg, 3)
                if scores.get("vlm_relevant_view", 0.0) < 0.6:
                    scores["overall_score"] = min(scores["overall_score"], 0.25)
                if scores.get("vlm_lots_headings", 0.0) < 0.6:
                    scores["overall_score"] = min(scores["overall_score"], 0.40)
                if scores.get("vlm_no_h2_distractor", 0.0) < 0.5:
                    scores["overall_score"] = min(scores["overall_score"], 0.55)
        except Exception:
            pass

    # No VLM available → cap at 0.60 (can't fully trust GUI evidence)
    if not vlm_done:
        scores["overall_score"] = min(scores["overall_score"], 0.60)

    if audit_cap is not None:
        scores["overall_score"] = min(scores["overall_score"], audit_cap)
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
