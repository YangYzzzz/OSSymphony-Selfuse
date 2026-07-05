# Auto-generated from WeaveBench task DOC_task_10_lo_writer_trackchanges_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Track-changes audit grader.

    Sub-scores cover: CLI redline parsing, policy decision audit,
    GUI screenshot count + OCR + diversity, final.docx structural cleanup,
    money-phrase fidelity, PDF export, audit report content, and a VLM rubric.
    Empty results dir -> overall_score == 0.000.
    """
    import json, re, hashlib, subprocess, zipfile
    from pathlib import Path
    try:
        from PIL import Image
    except Exception:
        Image = None
    try:
        import pytesseract
    except Exception:
        pytesseract = None
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    # Prefer root-only /opt/doc10_gt to prevent answer leakage; fall back
    # to /tmp_workspace/gt for legacy mounts.
    gt = Path("/opt/doc10_gt") if Path("/opt/doc10_gt/expected.json").exists() else workspace / "gt"

    sub_keys = [
        "redlines_raw_schema", "redlines_raw_total",
        "redlines_full_csv", "policy_audit_schema",
        "policy_audit_match",
        "screenshots_count", "screenshot_ocr",
        "gui_diversity", "gui_chrome_ocr", "gui_resolution",
        "final_docx_exists", "final_docx_no_ins_del",
        "final_text_money_kept", "final_text_money_rejected",
        "final_pdf_pages", "redline_diff_lines",
        "audit_report_len", "audit_report_table",
        "audit_report_money_listed", "audit_report_sec3_listed",
        "deliverables_schema",
        "cross_channel",
        "vlm_panel_visible", "vlm_redline_marks",
        "vlm_after_clean", "vlm_layout_final",
    ]
    s = {k: 0.0 for k in sub_keys}

    if not rd.exists() or not any(rd.iterdir()):
        s["overall_score"] = 0.000
        return s

    # ------------------------------------------------------------------
    # 1. redlines_raw.json
    # ------------------------------------------------------------------
    raw = rd / "redlines_raw.json"
    raw_total = 0
    if raw.exists():
        try:
            d = json.loads(raw.read_text())
            need = {"total", "ins", "del", "by_author"}
            if need.issubset(d.keys()) and isinstance(d["by_author"], dict):
                s["redlines_raw_schema"] = 1.0
                raw_total = int(d.get("total", 0))
        except Exception:
            pass
    # GT total ~30; tolerate ±2 (the generator may not place every anchor)
    if 27 <= raw_total <= 32:
        s["redlines_raw_total"] = 1.0
    elif raw_total > 0:
        s["redlines_raw_total"] = max(0.0, 1.0 - abs(raw_total - 29) / 10.0)

    # ------------------------------------------------------------------
    # 2. redlines_full.csv
    # ------------------------------------------------------------------
    csv_path = rd / "redlines_full.csv"
    if csv_path.exists():
        import csv as _csv
        try:
            rows = list(_csv.DictReader(csv_path.open()))
            need_cols = {"id", "kind", "author", "section", "text_preview",
                         "is_money_related", "planned_decision"}
            if rows and need_cols.issubset(set(rows[0].keys())) and len(rows) >= 25:
                good = sum(1 for r in rows
                           if r.get("author") in {"Senior Partner", "Reviewer B", "Reviewer C"}
                           and r.get("kind") in {"ins", "del"}
                           and str(r.get("is_money_related", "")).lower() in {"true", "false"}
                           and str(r.get("planned_decision", "")).lower() in {"accept", "reject"}
                           and str(r.get("section", "")).strip().startswith(tuple("123456")))
                s["redlines_full_csv"] = good / len(rows)
            elif rows:
                s["redlines_full_csv"] = 0.2
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 3. policy_audit.json
    # ------------------------------------------------------------------
    pa = rd / "policy_audit.json"
    pa_data = {}
    if pa.exists():
        try:
            pa_data = json.loads(pa.read_text())
            authors = ["Senior Partner", "Reviewer B", "Reviewer C"]
            if all(a in pa_data and "accept" in pa_data[a] and "reject" in pa_data[a]
                   for a in authors):
                s["policy_audit_schema"] = 1.0
        except Exception:
            pass

    expected = {}
    ej = gt / "expected.json"
    if ej.exists():
        try:
            expected = json.loads(ej.read_text())
        except Exception:
            pass
    if pa_data and expected.get("by_author"):
        # Match within ±1 per cell
        hits = 0; total = 0
        for a, d in expected["by_author"].items():
            for k, v in d.items():
                total += 1
                if int(pa_data.get(a, {}).get(k, -99)) == int(v):
                    hits += 1
        s["policy_audit_match"] = hits / total if total else 0.0

    # ------------------------------------------------------------------
    # 4. screenshots
    # ------------------------------------------------------------------
    shots_planned = ["view_01_manage_panel_initial", "view_02_panel_filter_author_a",
                     "view_03_money_redline_zoom", "view_04_section3_redline_zoom",
                     "view_05_panel_after_apply", "view_06_final_clean_layout"]
    shots = []
    for n in shots_planned:
        f = list(rd.glob(f"{n}*.png"))
        if f and f[0].stat().st_size > 3000:
            shots.append(f[0])
    s["screenshots_count"] = min(1.0, len(shots) / 5.0)

    if Image and shots:
        ok = 0
        for p in shots:
            try:
                w, h = Image.open(p).size
                if w >= 1280 and h >= 720:
                    ok += 1
            except Exception:
                pass
        s["gui_resolution"] = ok / max(1, len(shots))

    if shots:
        hashes = {hashlib.md5(p.read_bytes()).hexdigest() for p in shots}
        s["gui_diversity"] = 1.0 if len(hashes) / len(shots) >= 0.8 else (
            0.5 if len(hashes) / len(shots) >= 0.5 else 0.0)

    if pytesseract and Image and shots:
        body_kws = ["Manage", "Track", "Changes", "Author", "Confidential",
                    "USD", "Reviewer", "Senior", "Accept", "Reject", "Redline"]
        chrome_kws = ["Writer", "LibreOffice", "File", "Edit", "Format",
                      "Insert", "View", "Tools"]
        body_hits = 0
        chrome_hits = 0
        for p in shots:
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k in tx for k in body_kws):
                    body_hits += 1
                if sum(1 for k in chrome_kws if k.lower() in tx.lower()) >= 2:
                    chrome_hits += 1
            except Exception:
                pass
        s["screenshot_ocr"] = min(1.0, body_hits / 4.0)
        s["gui_chrome_ocr"] = min(1.0, chrome_hits / 2.0)

    # ------------------------------------------------------------------
    # 5. final.docx structural cleanup
    # ------------------------------------------------------------------
    final_doc = rd / "final.docx"
    final_xml_text = ""
    if final_doc.exists() and final_doc.stat().st_size > 500:
        s["final_docx_exists"] = 1.0
        try:
            with zipfile.ZipFile(final_doc) as z:
                if "word/document.xml" in z.namelist():
                    final_xml_text = z.read("word/document.xml").decode("utf-8", errors="ignore")
        except Exception:
            pass
        if final_xml_text and "<w:ins " not in final_xml_text and "<w:del " not in final_xml_text:
            s["final_docx_no_ins_del"] = 1.0
        elif final_xml_text:
            n_ins = final_xml_text.count("<w:ins ")
            n_del = final_xml_text.count("<w:del ")
            s["final_docx_no_ins_del"] = max(0.0, 1.0 - (n_ins + n_del) / 30.0)

    # ------------------------------------------------------------------
    # 6. money phrases in final text
    # ------------------------------------------------------------------
    final_text = ""
    ft = rd / "final_text.txt"
    if ft.exists():
        final_text = ft.read_text(errors="ignore")
    elif final_xml_text:
        final_text = re.sub(r"<[^>]+>", " ", final_xml_text)
    must_keep = expected.get("expected_money_phrases_remaining",
                             ["USD 120,000", "USD 8,500", "USD 250 per week"])
    must_absent = expected.get("expected_money_phrases_added_must_be_absent",
                               ["150,000", "12,000", "1.5% per month"])
    if final_text:
        xml_clean = bool(final_xml_text) and "<w:ins " not in final_xml_text and "<w:del " not in final_xml_text
        kept = sum(1 for p in must_keep if p in final_text)
        absent = sum(1 for p in must_absent if p not in final_text)
        mult = 1.0 if xml_clean else 0.3
        s["final_text_money_kept"] = mult * kept / max(1, len(must_keep))
        s["final_text_money_rejected"] = mult * absent / max(1, len(must_absent))

    # ------------------------------------------------------------------
    # 7. final.pdf
    # ------------------------------------------------------------------
    fpdf = rd / "final.pdf"
    if fpdf.exists() and fpdf.stat().st_size > 500:
        try:
            r = subprocess.run(["pdfinfo", str(fpdf)],
                               capture_output=True, text=True, timeout=10)
            n = 0
            for line in r.stdout.splitlines():
                if line.startswith("Pages:"):
                    n = int(line.split()[1])
            tx = subprocess.run(["pdftotext", str(fpdf), "-"],
                                capture_output=True, text=True, timeout=15).stdout
            if n >= 1 and len(tx.strip()) >= 200:
                s["final_pdf_pages"] = 1.0
            elif n >= 1:
                s["final_pdf_pages"] = 0.5
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 8. redline_diff.txt
    # ------------------------------------------------------------------
    rdf = rd / "redline_diff.txt"
    if rdf.exists():
        nl = sum(1 for _ in rdf.open(errors="ignore"))
        s["redline_diff_lines"] = 1.0 if nl >= 25 else nl / 25.0

    # ------------------------------------------------------------------
    # 9. audit_report.md
    # ------------------------------------------------------------------
    ar = rd / "audit_report.md"
    if ar.exists():
        txt = ar.read_text(errors="ignore")
        s["audit_report_len"] = 1.0 if len(txt) >= 400 else len(txt) / 400.0
        if "|" in txt and re.search(r"\|\s*[-:]+\s*\|.*\|\s*[-:]+\s*\|", txt):
            s["audit_report_table"] = 1.0
        rejected_money = ["150,000", "12,000", "1.5% per month"]
        money_hits = sum(1 for t in rejected_money
                         if t in txt and "Reviewer B" in txt.split(t)[0][-200:])
        s["audit_report_money_listed"] = money_hits / len(rejected_money)
        sec3_blocks = re.findall(r"Reviewer C[^\n]{0,300}?(Confidentiality|Section\s*3)", txt, re.I)
        s["audit_report_sec3_listed"] = min(1.0, len(sec3_blocks) / 2.0)

    # ------------------------------------------------------------------
    # 10. deliverables.json
    # ------------------------------------------------------------------
    dl = rd / "deliverables.json"
    if dl.exists():
        try:
            d = json.loads(dl.read_text())
            sha_hits = sum(1 for k in ["final_docx_sha256", "final_pdf_sha256"]
                           if isinstance(d.get(k), str) and len(d[k]) >= 32)
            list_ok = isinstance(d.get("screenshots"), list) and isinstance(d.get("files"), list)
            s["deliverables_schema"] = (sha_hits / 2.0) * (1.0 if list_ok else 0.5)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 11. cross-channel
    # ------------------------------------------------------------------
    required_cli = ["redlines_raw.json", "redlines_full.csv",
                    "policy_audit.json", "redline_diff.txt",
                    "final_document_xml.txt"]
    has_cli = all((rd / n).exists() for n in required_cli)
    has_gui = len(shots) >= 5
    s["cross_channel"] = 1.0 if (has_cli and has_gui) else (0.5 if (has_cli or has_gui) else 0.0)

    # ------------------------------------------------------------------
    # 12. VLM rubric
    # ------------------------------------------------------------------
    if vlm_score_rubric and shots:
        rubric = {
            "vlm_panel_visible": "截图中可见 Manage Track Changes 面板，列出按作者归类的多条修订条目",
            "vlm_redline_marks": "正文中可见红色 / 彩色 ins/del 修订标注（删除线 / 下划线 / 边栏条）",
            "vlm_after_clean": "处理完毕后的截图中 Track Changes 面板基本清空，正文几乎无残留修订",
            "vlm_layout_final": "最终文档截图整体排版整齐，章节标题与正文清晰",
        }
        try:
            vlm = vlm_score_rubric([str(p) for p in shots[:4]], rubric,
                                   instruction="评估合同 docx 修订审计任务的 GUI 截图真实性。")
            for k in rubric:
                s[k] = float(vlm.get(k, 0.0) or 0.0)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Aggregate + hard gates
    # ------------------------------------------------------------------
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums) / len(nums) if nums else 0.0

    if not has_cli:
        base = min(base, 0.4)
    # NOTE: We deliberately do NOT cap on missing GUI screenshots —
    # whether the agent invokes Writer UI tooling is not a scoring axis.
    # Missing PNGs already cost the screenshots_count / OCR / VLM
    # sub_scores; no additional hard cap is applied here.
    if s.get("final_docx_no_ins_del", 0) < 0.5 and s.get("final_docx_exists", 0) > 0:
        base = min(base, 0.55)
    if s.get("final_text_money_rejected", 0) < 0.5 and s.get("final_docx_exists", 0) > 0:
        base = min(base, 0.55)
    if s.get("gui_diversity", 0) < 0.5 and len(shots) >= 3:
        base = min(base, 0.4)
    if s.get("gui_chrome_ocr", 0) < 0.3 and len(shots) >= 3:
        base = min(base, 0.5)
    vlm_avg = sum(s.get(k, 0) for k in ["vlm_panel_visible", "vlm_redline_marks",
                                         "vlm_after_clean", "vlm_layout_final"]) / 4.0
    # Only enforce the VLM cap when the helper actually ran — otherwise
    # the 0.0 fallback would unfairly cap correct runs.
    if vlm_score_rubric is not None and vlm_avg < 0.6 and shots:
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
