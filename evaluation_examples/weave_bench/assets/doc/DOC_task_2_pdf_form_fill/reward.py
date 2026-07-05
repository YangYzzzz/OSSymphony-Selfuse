# Auto-generated from WeaveBench task DOC_task_2_pdf_form_fill.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(**kwargs) -> dict:
    """Strict grader against REAL IRS f1040+f1065+f1120s+f706 (1265 fields, 18 pages).

    Scoring: weighted 0.6*core + 0.3*gui + 0.1*aux, with multi-layer hard gates
    (no-cli-fill, fields_filled, buttons, images, AcroForm-kept, OCR proof of GUI).
    """
    from pathlib import Path
    import json, subprocess
    s = {}
    pdf = Path("/tmp_workspace/lease_signed.pdf")
    inp = Path("/tmp_workspace/inputs/tenant.json")
    gt  = Path("/tmp_workspace/gt/expected.json")
    expected = json.loads(gt.read_text()) if gt.exists() else {}
    tenant   = json.loads(inp.read_text()) if inp.exists() else {}
    s["pdf_exists"] = 1.0 if pdf.exists() else 0.0
    n_filled = n_data_hits = n_images = pages_ok = acroform_ok = 0
    n_buttons_checked = 0
    page4_radio_set = 0
    if pdf.exists():
        try:
            from pypdf import PdfReader
            R = PdfReader(str(pdf))
            pages_ok = 1 if len(R.pages) >= 18 else 0
            fields_dict = R.get_form_text_fields() or {}
            # strict: ≥50 text fields actually filled (≥4% of 1265 fields, hard-gate at 0.6 = 30)
            n_filled = sum(1 for v in fields_dict.values() if v and str(v).strip())
            tenant_strs = [str(v).strip() for v in tenant.values() if v]
            for ts in tenant_strs:
                if any(ts in (str(v) or "") for v in fields_dict.values()): n_data_hits += 1
            root = R.trailer["/Root"]
            acroform_ok = 1 if "/AcroForm" in root else 0
            # Count button/checkbox/radio fields that are toggled on (value not empty/Off)
            try:
                all_fields = R.get_fields() or {}
                for fname, fobj in all_fields.items():
                    try:
                        ftype = fobj.get("/FT")
                        fval = fobj.get("/V")
                        if ftype == "/Btn" and fval is not None:
                            sval = str(fval)
                            if sval and sval not in ("/Off", "Off", "/", ""):
                                n_buttons_checked += 1
                    except Exception: pass
                # Detect any radio/button selection on page 4
                try:
                    p4 = R.pages[3]
                    annots = p4.get("/Annots") or []
                    for a in annots:
                        try:
                            ao = a.get_object()
                            if ao.get("/Subtype") == "/Widget" and ao.get("/FT") == "/Btn":
                                v = ao.get("/V") or ao.get("/AS")
                                if v is not None and str(v) not in ("/Off", "Off", "/", ""):
                                    page4_radio_set = 1
                                    break
                        except Exception: pass
                except Exception: pass
            except Exception: pass
            for p in R.pages:
                xo = (p.get("/Resources") or {}).get("/XObject") or {}
                for k in xo:
                    try:
                        if xo[k].get_object().get("/Subtype")=="/Image": n_images += 1
                    except Exception: pass
        except Exception as e:
            s["pdf_error"] = str(e)[:100]
    # Stricter: require ≥50 actually-filled text fields (was 30) — agent must really sit and type
    s["fields_filled"]   = min(1.0, n_filled / 50.0)
    s["buttons_checked"] = min(1.0, n_buttons_checked / 5.0)
    s["page4_radio"]     = float(page4_radio_set)
    s["data_value_hits"] = min(1.0, n_data_hits / max(1,min(10,len(tenant))))
    s["page_count"]      = pages_ok * 1.0
    s["acroform_kept"]   = acroform_ok * 1.0
    # Stricter: 1 signature + 4 initials = 5 image overlays
    s["images_embedded"] = min(1.0, n_images / 5.0)
    # screenshots — require 5 unique, non-trivial PNGs (anti-cheat: md5 dedup + size floor)
    import hashlib
    steps_all = sorted(Path("/tmp_workspace").glob("step_*.png"))
    seen_md5 = set(); good_steps = []
    for p in steps_all:
        try:
            data = p.read_bytes()
            if len(data) < 5120:  # < 5KB → almost certainly a placeholder
                continue
            h = hashlib.md5(data).hexdigest()
            if h in seen_md5:
                continue
            seen_md5.add(h); good_steps.append(p)
        except Exception:
            pass
    steps = good_steps
    s["screenshots"] = min(1.0, len(steps) / 5.0)
    s["screenshots_unique"] = 1.0 if len(seen_md5) >= 5 else (len(seen_md5) / 5.0)
    panel_screen = False
    ocr_available = False
    try:
        import pytesseract
        from PIL import Image
        ocr_available = True
        for p in steps:
            tx = pytesseract.image_to_string(Image.open(p))
            if any(k in tx for k in ["Field","属性","Properties","Form Fields","Annotation",
                                      "Master PDF","Okular","Edit","Tools","Document"]):
                panel_screen = True; break
    except Exception:
        # OCR unavailable — do NOT auto-credit (Warmup installs tesseract+pytesseract)
        panel_screen = False
    s["field_panel_visible"] = 1.0 if panel_screen else 0.0
    # No-cheat: forbid pdftk fill_form / pypdf update_page_form_field_values usage
    log = Path("/tmp_workspace/actions.log")
    forbidden = False
    if log.exists():
        t = log.read_text(errors="ignore")
        if any(b in t for b in ["pdftk fill_form","update_page_form_field_values","cli_fill"]): forbidden = True
    s["no_cli_fill"] = 0.0 if forbidden else 1.0
    # Hard GUI gate: at least one screenshot must OCR to a real PDF editor name
    # (Master PDF Editor / Okular form panel / LibreOffice Draw form fields).
    pdf_ui_ocr = 0.0
    try:
        import pytesseract as _pt
        from PIL import Image as _PI
        for p in steps:
            try:
                tx = _pt.image_to_string(_PI.open(p))
                if any(k in tx for k in ["Master PDF","Okular","Form Fields",
                                          "Edit Form","Annotation","LibreOffice Draw",
                                          "Insert Image","Stamp"]):
                    pdf_ui_ocr = 1.0; break
            except Exception: pass
    except ImportError:
        pdf_ui_ocr = 0.0  # OCR unavailable — no credit (Warmup 已要求安装 tesseract+pytesseract)
    s["pdf_editor_ocr"] = pdf_ui_ocr
    nums = [s[k] for k in s if isinstance(s[k],(int,float))]
    # Weighted aggregate — core deliverable 60%, GUI evidence 30%, aux 10%
    core_keys = ["pdf_exists","fields_filled","buttons_checked","page4_radio",
                 "data_value_hits","acroform_kept","images_embedded"]
    gui_keys  = ["screenshots","screenshots_unique","field_panel_visible",
                 "pdf_editor_ocr","no_cli_fill"]
    aux_keys  = ["page_count"]
    def _avg(keys):
        vs = [s[k] for k in keys if k in s and isinstance(s[k],(int,float))]
        return sum(vs)/len(vs) if vs else 0.0
    base = 0.6*_avg(core_keys) + 0.3*_avg(gui_keys) + 0.1*_avg(aux_keys)
    # Hard gates — agent must really do the work, not just produce shells
    if s.get("pdf_exists",0) < 1.0:                base = min(base, 0.10)
    if s.get("fields_filled",0) < 0.6:             base = min(base, 0.40)   # was 0.45
    if s.get("buttons_checked",0) < 0.6:           base = min(base, 0.45)   # was 0.6
    if s.get("page4_radio",0) < 1.0:               base = min(base, 0.55)
    if s.get("images_embedded",0) < 0.6:           base = min(base, 0.45)
    if s.get("acroform_kept",0) < 1.0:             base = min(base, 0.40)   # flatten = fail core
    if s.get("field_panel_visible",0) < 1.0:       base = min(base, 0.50)   # was 0.55
    if s.get("no_cli_fill",0) < 1.0:               base = min(base, 0.30)   # was 0.4
    if s.get("pdf_editor_ocr",0) < 0.5:            base = min(base, 0.40)   # was 0.55
    if s.get("screenshots_unique",0) < 1.0:        base = min(base, 0.55)   # md5 dedup gate
    # If OCR pipeline unavailable, cap overall at 0.6 (don't let infra gap = full marks)
    if not ocr_available:                          base = min(base, 0.60)
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
