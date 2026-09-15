# Auto-generated from WeaveBench task DSK_task_17_fontconfig_glyph_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Grader for font audit task: schema check + GUI shots + correct
    classification of 4 broken fonts vs 2 controls + blacklist applied."""
    import csv, json, subprocess, re
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    s = {}
    mf_p = Path("/opt/dsk17_gt/manifest.json")
    manifest = {}
    if mf_p.exists():
        try: manifest = json.loads(mf_p.read_text())
        except Exception: pass
    gt_defects  = manifest.get("defects", {})
    gt_broken   = set(manifest.get("broken_files", []))
    gt_controls = set(manifest.get("controls", []))
    expected_kinds = {fn: d["kind"] for fn, d in gt_defects.items()}

    # 1. fc-list raw
    fl = rd / "fc_list_raw.txt"; fl_ok = 0.0
    if fl.exists():
        try:
            txt = fl.read_text()
            n = sum(1 for ln in txt.splitlines() if ".ttf" in ln.lower())
            fl_ok = 1.0 if n >= 6 else n/6.0
        except Exception: pass
    s["fc_list_raw"] = fl_ok

    # 2. font_metadata.tsv schema
    fm = rd / "font_metadata.tsv"; fm_ok = 0.0; fm_rows = 0
    need_cols = {"file","family","subfamily","weight_class","num_glyphs",
                 "cmap_has_digits","name_says_italic","italic_angle"}
    if fm.exists():
        try:
            rdr = csv.DictReader(fm.open(), delimiter="\t")
            cols = set(rdr.fieldnames or [])
            rows = list(rdr)
            fm_rows = len(rows)
            ok_rows = 0
            for r in rows:
                if (r.get("cmap_has_digits","") in {"True","False"} and
                    str(r.get("weight_class","")).isdigit() and
                    r.get("italic_angle","").lstrip("-").replace(".","",1).isdigit()):
                    ok_rows += 1
            if need_cols.issubset(cols) and fm_rows==6 and ok_rows==6: fm_ok = 1.0
            elif need_cols.issubset(cols) and ok_rows>=4: fm_ok = 0.5
            else: fm_ok = 0.0
        except Exception: pass
    s["metadata_tsv"] = fm_ok

    # 3. per-font GUI shots present + OCR
    bases = ["AuroraSans-Regular","AuroraSans-Bold","NimbusOffice-Regular",
             "NimbusOffice-Bold","EmberMono-Regular","EmberMono-Italic"]
    shots = [f"view_{b}.ttf.png" for b in bases]
    present = sum(1 for n in shots if (rd/n).exists())
    s["per_font_shots"] = present / len(shots)
    ocr_hits = 0
    try:
        import pytesseract; from PIL import Image
        for n in shots:
            p = rd/n
            if not p.exists(): continue
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(kw in tx for kw in ["Aa","ABC","abc","0123","quick"]):
                    ocr_hits += 1
            except Exception: pass
    except ImportError:
        ocr_hits = 0
    s["per_font_shots_ocr"] = ocr_hits / len(shots)

    # also gnome fonts app group screenshot
    s["fonts_app_shot"] = 1.0 if (rd/"view_gnome_fonts_app.png").exists() else 0.0

    # 4. glyph grid
    gg = rd / "view_glyph_grid.png"; gg_ok = 0.0
    if gg.exists():
        try:
            from PIL import Image
            w,h = Image.open(gg).size
            if w >= 1200 and h >= 500: gg_ok = 1.0
            elif w >= 800 and h >= 300: gg_ok = 0.5
        except Exception: gg_ok = 0.4
    s["glyph_grid"] = gg_ok

    # 5+6. classification correctness
    fa = rd / "font_audit.json"
    set_ok = 0.0; kind_match = 0; total_kinds = max(1, len(expected_kinds))
    must_kinds_ok = 0.0
    try:
        d = json.loads(fa.read_text()) if fa.exists() else {}
        broken_items = d.get("broken", []) or []
        agent_files = {it.get("file","").split("/")[-1] for it in broken_items}
        if agent_files == gt_broken: set_ok = 1.0
        elif gt_broken and len(agent_files & gt_broken) >= len(gt_broken)-1:
            set_ok = 0.7
        # kind per file
        agent_kind = {it.get("file","").split("/")[-1]: it.get("kind","")
                      for it in broken_items}
        # accept fake_bold for NimbusOffice-Bold even though base says missing_glyphs
        relax = {"NimbusOffice-Bold.ttf": {"missing_glyphs","fake_bold"}}
        for fn, gtk in expected_kinds.items():
            ag = agent_kind.get(fn, "")
            allowed = relax.get(fn, {gtk})
            if ag in allowed: kind_match += 1
        must = {"missing_glyphs","spoofed_glyph","spoofed_italic"}
        correct_pairs = {fn for fn,gtk in expected_kinds.items()
                         if agent_kind.get(fn,"") in (relax.get(fn,{gtk}))}
        seen_kinds = {expected_kinds[fn] for fn in correct_pairs}
        if must.issubset(seen_kinds): must_kinds_ok = 1.0
    except Exception: pass
    s["broken_set"]      = set_ok
    s["kind_per_file"]   = kind_match / total_kinds
    s["must_kinds_seen"] = must_kinds_ok

    # 7. blacklist conf
    bl = rd / "70-aurora-blacklist.conf"; bl_ok = 0.0
    if bl.exists():
        try:
            tx = bl.read_text()
            n_reject = tx.count("<rejectfont>")
            fams_hit = sum(1 for fam in ("NimbusOffice","EmberMono")
                           if re.search(r'<patelt[^>]*name="family"[^>]*>\s*<string>'+fam+'</string>', tx))
            sub_hit  = sum(1 for sf in ("Bold","Italic","Regular") if f"<string>{sf}</string>" in tx)
            if n_reject >= 4 and fams_hit == 2 and sub_hit >= 3: bl_ok = 1.0
            elif n_reject >= 2 and fams_hit >= 1: bl_ok = 0.4
            else: bl_ok = 0.0
        except Exception: pass
    s["blacklist_conf"] = bl_ok

    # 8. fc-match after
    fm2 = rd / "fc_match_after.txt"; fm2_ok = 0.0
    if fm2.exists():
        try:
            t = fm2.read_text().lower()
            if "nimbusoffice" not in t: fm2_ok = 1.0
            elif "nimbusoffice-regular.ttf" not in t and "nimbusoffice-bold.ttf" not in t:
                fm2_ok = 0.5
        except Exception: pass
    s["fc_match_after"] = fm2_ok

    # 9. PDF
    pdf = rd / "font_audit_report.pdf"; pages = 0; chars = 0
    if pdf.exists():
        try:
            info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                                  text=True, timeout=15).stdout
            for ln in info.splitlines():
                if ln.startswith("Pages:"): pages = int(ln.split()[1])
            out = subprocess.run(["pdftotext","-f","1","-l","1",str(pdf),"-"],
                                 capture_output=True, text=True, timeout=20).stdout
            chars = len(out.strip())
        except Exception: pass
    s["pdf_pages"]   = 1.0 if pages >= 3 else pages/3.0
    s["pdf_p1_text"] = 1.0 if chars >= 350 else chars/350.0

    # 10. ocr summary text
    og = rd / "glyph_grid_ocr.txt"; og_ok = 0.0
    if og.exists():
        try:
            tx = og.read_text()
            low = tx.lower()
            must_kw = sum(1 for k in ("nimbus","ember","digit","tofu") if k in low) \
                    + sum(1 for k in ("豆腐","方框",".notdef") if k in tx)
            human = "\n".join(ln for ln in tx.splitlines() if any(
                k in ln.lower() for k in ("nimbus","ember","digit","tofu","missing","spoof")))
            if len(human) >= 80 and must_kw >= 3: og_ok = 1.0
            elif len(human) >= 40 and must_kw >= 2: og_ok = 0.5
            else: og_ok = 0.0
        except Exception: pass
    s["ocr_summary"] = og_ok

    # VLM rubric (optional)
    try: from _judge_helper import vlm_score_rubric
    except Exception: vlm_score_rubric = None
    vlm_imgs = [str(rd/n) for n in
                ["view_glyph_grid.png",
                 "view_NimbusOffice-Regular.ttf.png",
                 "view_EmberMono-Regular.ttf.png"] if (rd/n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_grid_legible":  "对照网格里 6 列字体并排，可读出每列家族差异",
            "vlm_tofu_visible":  "至少一格里能看到 .notdef 方框（豆腐）",
            "vlm_glyph_swap":    "至少一格里 'g' 字符形状明显是 '$' 而非 'g'",
            "vlm_clean_layout":  "图像整齐无重叠，字体名称标签可读",
        }
        vlm = vlm_score_rubric(vlm_imgs[:3], rubric,
                               instruction="评估字体审计对照图与字体预览截图。")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")

    # aggregate + hard gates
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums) if nums else 0.0
    has_cli = s.get("fc_list_raw",0) >= 1.0 and s.get("metadata_tsv",0) >= 0.5
    has_gui = s.get("per_font_shots",0) >= 0.5 or s.get("glyph_grid",0) >= 1.0
    vlm_avg = sum(s.get(k,0) for k in ["vlm_grid_legible","vlm_tofu_visible",
                                       "vlm_glyph_swap","vlm_clean_layout"])/4.0
    if not has_cli: base = min(base, 0.40)
    # GUI hard-cap removed: rely on per-shot VLM/OCR sub-scores instead.
    # Only enforce VLM cap when the helper actually ran. Otherwise the
    # 0.5 fallback can trigger the cap on an environment defect.
    if vlm_score_rubric is not None and vlm_imgs and vlm_avg < 0.6:
        base = min(base, 0.60)
    if s.get("broken_set",0) < 1.0:    base = min(base, 0.45)
    if s.get("kind_per_file",0) < 0.75: base = min(base, 0.50)
    if s.get("must_kinds_seen",0) < 1.0: base = min(base, 0.55)
    if s.get("blacklist_conf",0) < 1.0: base = min(base, 0.60)
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
