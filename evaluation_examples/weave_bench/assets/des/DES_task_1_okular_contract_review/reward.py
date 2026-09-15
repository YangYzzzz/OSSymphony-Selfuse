# Auto-generated from WeaveBench task DES_task_1_okular_contract_review.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(**kwargs) -> dict:
    from pathlib import Path
    import json, re, subprocess
    from PIL import Image
    try: from _judge_helper import vlm_score_rubric
    except Exception: vlm_score_rubric = None
    try: import pytesseract
    except ImportError: pytesseract = None
    ws = Path(kwargs.get("workspace_path") or "/tmp_workspace")
    rd = ws / "results"
    gt_candidates = [
        ws.parent / "gt" / "diff.json",
        Path("/tmp_workspace/gt/diff.json"),
    ]
    gt = {}
    for _gp in gt_candidates:
        if _gp.exists():
            try:
                gt = json.loads(_gp.read_text())
                break
            except Exception:
                pass
    truth_pages = {c["page"] for c in gt.get("changes", [])} if gt else set()
    s = {}

    apdf = rd / "contract_v2_annotated.pdf"
    s["pdf_exists"] = 1.0 if apdf.exists() else 0.0
    annot_count = 0; types = set(); annot_pages = set()
    if apdf.exists():
        try:
            from pypdf import PdfReader
            R = PdfReader(str(apdf))
            for i, p in enumerate(R.pages, start=1):
                try:
                    if "/Annots" not in p:
                        continue
                    annots = p["/Annots"]
                    try:
                        annots = annots.get_object()
                    except Exception:
                        pass
                    for a in annots:
                        try:
                            obj = a.get_object()
                            t = str(obj.get("/Subtype",""))
                            types.add(t); annot_count += 1; annot_pages.add(i)
                        except Exception: pass
                except Exception:
                    continue
        except Exception as e:
            s["pdf_error"] = str(e)[:80]
    s["annotation_count"] = min(1.0, annot_count / 12.0)
    # Per-subtype quotas: Highlight ≥6, StrikeOut ≥4, Text/FreeText ≥8 (matches Prompt §第一阶段).
    sub_counts = {"/Highlight": 0, "/StrikeOut": 0, "/Text": 0, "/FreeText": 0}
    if apdf.exists():
        try:
            from pypdf import PdfReader as _PR
            for p in _PR(str(apdf)).pages:
                try:
                    if "/Annots" not in p:
                        continue
                    annots = p["/Annots"]
                    try:
                        annots = annots.get_object()
                    except Exception:
                        pass
                    for a in annots:
                        try:
                            t = str(a.get_object().get("/Subtype", ""))
                            if t in sub_counts:
                                sub_counts[t] += 1
                        except Exception:
                            pass
                except Exception:
                    continue
        except Exception:
            pass
    quota_ratios = [
        min(1.0, sub_counts["/Highlight"] / 6.0),
        min(1.0, sub_counts["/StrikeOut"] / 4.0),
        min(1.0, (sub_counts["/Text"] + sub_counts["/FreeText"]) / 8.0),
    ]
    s["annotation_types"] = round(sum(quota_ratios) / 3.0, 3)
    if annot_pages and truth_pages:
        # Strict recall: divide by full ground-truth page count so the agent
        # must actually overlap with the curated material pages — annotating
        # arbitrary marker pages is no longer enough.
        denom = max(1, len(truth_pages))
        s["annotation_page_recall"] = min(1.0, len(annot_pages & truth_pages) / denom)
    else:
        s["annotation_page_recall"] = 0.0

    # pdfannots export must contain ≥12 entries
    aex = rd / "annotations_export.md"
    s["pdfannots_md"] = 0.0
    if aex.exists():
        txt = aex.read_text(errors="ignore")
        n_entries = len(re.findall(r"\bPage\s*\d+\b|\bp\.\s*\d+\b", txt, re.I))
        s["pdfannots_md"] = min(1.0, n_entries / 12.0)
    aj = rd / "annotations.json"
    s["pdfannots_json"] = 0.0
    if aj.exists():
        try:
            j = json.loads(aj.read_text())
            arr = j if isinstance(j, list) else j.get("annotations", j)
            if isinstance(arr, list) and len(arr) >= 12:
                fields_ok = all(isinstance(a, dict) and any(k in a for k in ("subtype","type")) and any(k in a for k in ("page","page_no","page_index")) for a in arr[:12])
                s["pdfannots_json"] = 1.0 if fields_ok else 0.5
        except Exception: pass

    # changes.md
    ch_path = rd / "changes.md"
    page_cite = 0; risk_tag = 0; n_lines = 0
    if ch_path.exists():
        ch = ch_path.read_text(errors="ignore")
        # Count entries: any line starting with bullet/heading/number, OR
        # any "Page N" / "P.N" / "页 N" mention, OR any "Old:" line (each
        # change record per the task spec must contain Old:/New:).
        line_hits = sum(1 for l in ch.splitlines()
                       if l.strip().startswith(("-","*","|","#"))
                       or re.match(r"^\d", l.strip()))
        old_lines = len(re.findall(r"^\s*Old\s*[:：]", ch, re.M | re.I))
        new_lines = len(re.findall(r"^\s*New\s*[:：]", ch, re.M | re.I))
        page_lines = len(re.findall(r"(?:页|P|page|Page)\s*\d+", ch))
        n_lines = max(line_hits, old_lines, new_lines, page_lines)
        cited = set()
        for m in re.finditer(r"(?:页|P|page|Page)\s*(\d+)", ch):
            cited.add(int(m.group(1)))
        page_cite = min(1.0, len(cited)/12)
        risk_tag = min(1.0, sum(1 for l in ch.splitlines() if re.search(r"\b(HIGH|MED|LOW)\b", l.upper()))/12.0)
    s["changes_md_lines"] = min(1.0, n_lines/12)
    s["changes_md_pages"] = page_cite
    s["changes_risk_tags"] = risk_tag

    # redline summary three sections
    rs_path = rd / "redline_summary.md"
    high = mid = pos = 0
    if rs_path.exists():
        rs = rs_path.read_text(errors="ignore")
        sec_high = re.search(r"高风险.*?(?=利好|中性|$)", rs, re.DOTALL)
        if sec_high: high = sum(1 for l in sec_high.group(0).splitlines() if l.strip().startswith(("-","*")))
        sec_n = re.search(r"中性.*?(?=利好|高风险|$)", rs, re.DOTALL)
        if sec_n: mid = sum(1 for l in sec_n.group(0).splitlines() if l.strip().startswith(("-","*")))
        sec_p = re.search(r"利好.*?$", rs, re.DOTALL)
        if sec_p: pos = sum(1 for l in sec_p.group(0).splitlines() if l.strip().startswith(("-","*")))
    s["redline_high"] = min(1.0, high/4)
    s["redline_three_buckets"] = 1.0 if (high>=4 and mid>=1 and pos>=1) else 0.0

    # 4 Okular screenshots + UI OCR
    shots = ["okular_01_two_pane.png","okular_02_annotation_panel.png","okular_03_highlight_inline.png","okular_04_strikeout_inline.png"]
    present = sum(1 for n in shots if (rd/n).exists())
    s["okular_screens_count"] = present / len(shots)

    # Anti-cheat: screenshots must be md5-unique, ≥50KB, min-side ≥720px.
    import hashlib as _hl
    md5s = set(); size_ok = 0
    for n in shots:
        p = rd/n
        if not p.exists():
            continue
        try:
            blob = p.read_bytes()
            md5s.add(_hl.md5(blob).hexdigest())
            ok_bytes = len(blob) >= 50 * 1024
            ok_dim = False
            try:
                with Image.open(p) as _im:
                    w, h = _im.size
                    ok_dim = min(w, h) >= 720
            except Exception:
                ok_dim = False
            if ok_bytes and ok_dim:
                size_ok += 1
        except Exception:
            pass
    s["screens_unique_md5"] = (len(md5s) / present) if present else 0.0
    s["screens_min_size_ok"] = (size_ok / len(shots))

    ui_hits = 0
    if pytesseract:
        for n in shots:
            p = rd/n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k in tx for k in ["Okular","Annotations","Reviews","Page","批注"]):
                        ui_hits += 1
                except Exception: pass
    s["okular_ui_ocr"] = ui_hits / len(shots)

    base_items = {k: v for k, v in s.items() if isinstance(v, (int, float))}

    # Weighted aggregation: core deliverables 60% / GUI evidence 30% / aux 10%.
    core_keys = ("pdf_exists", "annotation_count", "annotation_types",
                 "annotation_page_recall", "pdfannots_md", "pdfannots_json",
                 "redline_three_buckets", "redline_high")
    gui_keys = ("okular_screens_count", "okular_ui_ocr",
                "screens_unique_md5", "screens_min_size_ok")
    aux_keys = ("changes_md_lines", "changes_md_pages", "changes_risk_tags")
    def _avg(keys):
        vals = [base_items[k] for k in keys if k in base_items]
        return sum(vals) / len(vals) if vals else 0.0
    core = _avg(core_keys); gui = _avg(gui_keys); aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    if vlm_score_rubric:
        sample = [str(rd/n) for n in shots if (rd/n).exists()][:4]
        if sample:
            rubric = {
                "vlm_okular_real": "至少一张截图清晰显示 Okular 的双栏布局（缩略图 + 主文档区）",
                "vlm_annotations_visible": "至少一张截图清楚显示文档上有 highlight/strikeout/note annotation",
                "vlm_panel_real": "Reviews/Annotations 面板真实展开（看到列表条目）",
                "vlm_inline_zoom": "至少一张截图聚焦到具体某一段 annotation 文字可读",
            }
            vlm = vlm_score_rubric(sample, rubric, instruction="评估 Okular 合同 redline 截图。")
            for k in rubric: s[k] = vlm.get(k, 0.0)
            s["judge_method"] = vlm.get("judge_method", "failed")
            vlm_avg = sum(vlm.get(k,0) for k in rubric)/len(rubric)
            s["overall_score"] = round(0.65 * base + 0.35 * vlm_avg, 3)
            if vlm_avg < 0.45:
                s["overall_score"] = round(min(s["overall_score"], 0.45), 3)
            if vlm_avg < 0.30:
                s["overall_score"] = round(min(s["overall_score"], 0.30), 3)
        else:
            # No screenshots available → cap 0.30 (cannot evidence GUI usage).
            s["overall_score"] = round(min(base, 0.30), 3)
    else:
        # VLM unavailable: cap to 0.60 so non-VLM runs can never max out.
        s["overall_score"] = round(min(base, 0.60), 3)

    # Multi-tier hard gates: stricter than v1.
    if s.get("annotation_count", 0) < 0.6:
        s["overall_score"] = round(min(s["overall_score"], 0.35), 3)
    if s.get("annotation_types", 0) < 0.7:
        s["overall_score"] = round(min(s["overall_score"], 0.45), 3)
    if s.get("pdfannots_json", 0) == 0:
        s["overall_score"] = round(min(s["overall_score"], 0.45), 3)
    if s.get("redline_three_buckets", 0) == 0:
        s["overall_score"] = round(min(s["overall_score"], 0.55), 3)
    if s.get("annotation_page_recall", 0) < 0.5:
        s["overall_score"] = round(min(s["overall_score"], 0.45), 3)
    if s.get("screens_unique_md5", 1) < 1.0:
        s["overall_score"] = round(min(s["overall_score"], 0.45), 3)
    if s.get("screens_min_size_ok", 1) < 1.0:
        s["overall_score"] = round(min(s["overall_score"], 0.50), 3)
    if pytesseract is not None and s.get("okular_ui_ocr", 0) < 0.5:
        s["overall_score"] = round(min(s["overall_score"], 0.40), 3)
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
