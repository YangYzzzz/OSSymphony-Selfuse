# Auto-generated from WeaveBench task DES_task_13_cmyk_softproof_gamut.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Grader: ICC paths + oog before/after + Krita GUI evidence + ΔE."""
    import csv, json, subprocess, re
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/tmp_workspace/gt")
    s = {}
    expected = {}
    if (gt_dir/"expected.json").exists():
        try: expected = json.loads((gt_dir/"expected.json").read_text())
        except Exception: pass

    # --- 1. icc_paths.json ---
    icc = rd / "icc_paths.json"
    icc_ok = 0; cmyk_kw_ok = 0
    rgb_p = ""; cmyk_p = ""
    if icc.exists():
        try:
            j = json.loads(icc.read_text())
            rgb_p  = j.get("rgb_icc","")
            cmyk_p = j.get("cmyk_icc","")
            if rgb_p and cmyk_p and Path(rgb_p).exists() and Path(cmyk_p).exists():
                icc_ok = 1
            kws = expected.get("cmyk_profile_substrings", ["FOGRA","Coated","ISOcoated","PSO"])
            if any(k.lower() in cmyk_p.lower() for k in kws):
                cmyk_kw_ok = 1
            else:
                # Try profile description fallback
                try:
                    from PIL import ImageCms
                    desc = ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(cmyk_p))
                    if any(k.lower() in (desc or "").lower() for k in kws):
                        cmyk_kw_ok = 1
                except Exception: pass
        except Exception: pass
    s["icc_paths_resolve"]   = float(icc_ok)
    s["icc_cmyk_keyword"]    = float(cmyk_kw_ok)

    # --- 2 + 8. oog_before / oog_after ---
    def load_oog(path):
        if not path.exists(): return None
        try: return json.loads(path.read_text())
        except Exception: return None
    ob = load_oog(rd/"oog_before.json")
    oa = load_oog(rd/"oog_after.json")
    req_oog = {"oog_pixel_pct","method","intent","src_size"}
    s["oog_before_struct"] = 1.0 if (ob and req_oog.issubset(set(ob.keys()))) else 0.0
    s["oog_after_struct"]  = 1.0 if (oa and req_oog.issubset(set(oa.keys()))) else 0.0
    min_before = float(expected.get("min_oog_pixel_pct_before", 12.0))
    max_after  = float(expected.get("max_oog_pixel_pct_after", 1.5))
    before_pct = float(ob.get("oog_pixel_pct",0)) if ob else 0.0
    after_pct  = float(oa.get("oog_pixel_pct",100)) if oa else 100.0
    s["oog_before_high"]   = 1.0 if before_pct >= min_before else max(0.0, before_pct/min_before)
    s["oog_after_low"]     = 1.0 if after_pct  <= max_after else max(0.0, max(0.0, (max_after*4 - after_pct))/(max_after*4))
    s["oog_drop"]          = 1.0 if (before_pct - after_pct) >= 5.0 else max(0.0, (before_pct - after_pct)/5.0)
    intent_req = expected.get("icc_intent_required","RelativeColorimetric")
    intent_ok = 1.0 if (oa and oa.get("intent","").replace(" ","").lower() == intent_req.lower()) else 0.0
    s["oog_intent_ok"]     = intent_ok
    try:
        from PIL import Image, ImageCms
        src = ImageCms.profileToProfile(Image.open("/tmp_workspace/img/source_rgb.jpg").convert("RGB"),
                rgb_p, cmyk_p, renderingIntent=1, outputMode="CMYK")
        fin = Image.open(rd/"final_cmyk.tif").convert("CMYK")
        import numpy as np
        a = np.array(src.resize(fin.size)); b = np.array(fin)
        real_after = float(((np.abs(a.astype(int)-b.astype(int)).sum(-1) > 60).mean())*100)
        if abs(real_after - after_pct) > 3.0: s["oog_after_low"] = 0.0
    except Exception: pass

    # --- 5. oog_zones.csv ---
    zc = rd / "oog_zones.csv"
    zc_ok = 0; zc_rows = 0
    cols = {"zone_id","x","y","w","h","reason"}
    if zc.exists():
        try:
            rows = list(csv.DictReader(zc.open()))
            if rows and cols.issubset(set(rows[0].keys())):
                zc_ok = 1
                zc_rows = sum(1 for r in rows if r.get("reason") and len(r["reason"].strip()) >= 4)
        except Exception: pass
    min_zones = int(expected.get("patch_zones_csv_min_rows", 3))
    s["oog_zones_schema"] = float(zc_ok)
    s["oog_zones_rows"] = 1.0 if zc_rows >= min_zones else max(0.0, zc_rows/float(min_zones))

    # --- 6. patched_rgb.png ---
    pr = rd / "patched_rgb.png"
    pr_ok = 0
    if pr.exists() and pr.stat().st_size > 10000:
        try:
            from PIL import Image
            w,h = Image.open(pr).size
            if min(w,h) >= 800: pr_ok = 1
        except Exception: pass
    s["patched_png_ok"] = float(pr_ok)

    # --- 7. final_cmyk.tif colorspace ---
    fc = rd / "final_cmyk.tif"
    cs_ok = 0
    if fc.exists():
        try:
            out = subprocess.run(["identify","-format","%[colorspace]",str(fc)],
                                 capture_output=True, text=True, timeout=20).stdout.strip()
            if out.upper() == "CMYK": cs_ok = 1
        except Exception:
            try:
                from PIL import Image
                im = Image.open(fc)
                if im.mode == "CMYK": cs_ok = 1
            except Exception: pass
    s["final_cmyk_tif_cs"] = float(cs_ok)

    # --- 9. delta_e.json ---
    de = rd / "delta_e.json"
    de_struct = 0; de_ok = 0; p95_val = 100.0; p99_ok = 0; p50_ok = 0
    if de.exists():
        try:
            j = json.loads(de.read_text())
            req = {"delta_e_p50","delta_e_p95","delta_e_p99","delta_e_max","method"}
            if req.issubset(set(j.keys())): de_struct = 1
            p50_val = float(j.get("delta_e_p50", 100))
            p95_val = float(j.get("delta_e_p95", 100))
            p99_val = float(j.get("delta_e_p99", 100))
            if p95_val <= float(expected.get("delta_e_max_p95_after", 4.0)): de_ok = 1
            if p50_val <= 1.5: p50_ok = 1
            if p99_val <= 8.0: p99_ok = 1
        except Exception: pass
    s["delta_e_struct"] = float(de_struct)
    s["delta_e_p95_ok"] = float(de_ok)
    s["delta_e_p50_ok"] = float(p50_ok)
    s["delta_e_p99_ok"] = float(p99_ok)
    s["delta_e_p95_partial"] = max(0.0, min(1.0, 4.0 / max(p95_val, 0.1)))

    # --- 10. gs_log.txt ---
    gl = rd / "gs_log.txt"
    gl_ok = 0
    if gl.exists() and gl.stat().st_size > 400:
        try:
            txt = gl.read_text(errors="ignore")
            need = [r"GPL Ghostscript", r"\bICC\b", r"final_cmyk\.tif", r"(RelativeColorimetric|Intent\s*[:=]\s*1)"]
            if all(re.search(p, txt, re.IGNORECASE) for p in need): gl_ok = 1
        except Exception: pass
    s["gs_log_icc"] = float(gl_ok)

    # --- 11. manifest ---
    mf = rd / "manifest.json"
    mf_struct = 0; notes_ok = 0
    if mf.exists():
        try:
            j = json.loads(mf.read_text())
            req = {"rgb_icc","cmyk_icc","oog_before_pct","oog_after_pct",
                   "delta_e_p50","delta_e_p95","delta_e_p99","patched_zones",
                   "intent","tac_pct_max","ink_density_summary","agent_notes"}
            if req.issubset(set(j.keys())): mf_struct = 1
            min_chars = int(expected.get("report_min_chars", 300))
            if isinstance(j.get("agent_notes",""), str) and len(j["agent_notes"]) >= min_chars:
                notes_ok = 1
        except Exception: pass
    s["manifest_struct"] = float(mf_struct)
    s["manifest_notes"]  = float(notes_ok)

    # --- 12 + 13. screenshots + OCR + VLM ---
    shots = expected.get("krita_views_required", [
        "view_krita_softproof_on.png",
        "view_krita_gamut_warning.png",
        "view_krita_brush_correction.png",
    ])
    shot_present = sum(1 for n in shots if (rd/n).exists() and (rd/n).stat().st_size > 5000)
    s["screenshots_present"] = shot_present / float(len(shots))
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_krita_softproof_on.png":     ["Krita","Soft","Proof","FOGRA","Coated","CMYK"],
            "view_krita_gamut_warning.png":    ["Gamut","Warning","Krita","Out","Check"],
            "view_krita_brush_correction.png": ["Brush","Krita","Opacity","Flow","Saturation","Color"],
        }
        for n, ks in kws.items():
            p = rd/n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in ks):
                        ocr_hits += 1
                except Exception: pass
        s["screenshots_ocr"] = ocr_hits / float(len(shots))
    except ImportError:
        s["screenshots_ocr"] = 0.0

    # --- VLM rubric ---
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_avg = 0.5
    if vlm_score_rubric:
        rubric = {
            "vlm_krita_chrome": "截图明显是 Krita 主界面（File/Edit/View 菜单 + dockers）",
            "vlm_softproof_active": "Soft Proof 截图能看到画面和原图相比有色彩偏移",
            "vlm_gamut_warning_overlay": "Gamut Warning 截图能看到大片连续覆盖色块（warning 颜色）",
            "vlm_brush_in_use": "Brush correction 截图能看到笔刷光圈或最近 stroke + brush options 面板",
        }
        imgs = [str(rd/n) for n in shots if (rd/n).exists()]
        if imgs:
            try:
                v = vlm_score_rubric(imgs[:3], rubric, instruction="评估 Krita 软打样 + gamut warning + 笔刷修色的 GUI 取证截图。")
                for k in rubric: s[k] = v.get(k, 0.0)
                vlm_avg = sum(s[k] for k in rubric)/len(rubric)
            except Exception:
                for k in rubric: s[k] = 0.5

    # --- 14. process_compare.csv (3 rows + recommended + oog<=4) ---
    pc = rd / "process_compare.csv"
    pc_ok = 0
    if pc.exists():
        try:
            rows = list(csv.DictReader(pc.open()))
            cols = {"process","profile_path","oog_before_pct","oog_after_pct",
                    "delta_e_p95","delta_e_p99","recommended"}
            if (rows and len(rows) >= 3 and cols.issubset(set(rows[0].keys()))):
                ok_rows = sum(1 for r in rows[:3] if float(r.get("oog_after_pct",99)) <= 4.0)
                rec = sum(1 for r in rows[:3]
                          if str(r.get("recommended","")).strip().lower() in ("true","1","yes"))
                if ok_rows == 3 and rec >= 1:
                    pc_ok = 1
        except Exception: pass
    s["process_compare_ok"] = float(pc_ok)

    # --- 15. halftone_ink_density.json ---
    hi = rd / "halftone_ink_density.json"
    hi_ok = 0
    if hi.exists():
        try:
            j = json.loads(hi.read_text())
            lpi = int(j.get("screen_lpi", 0))
            angles = j.get("screen_angles", {})
            tac_max = float(j.get("tac_pct_max", 999))
            tac_viol = float(j.get("tac_violations_pct", 100))
            ang_vals = [float(angles.get(c, -999)) for c in ("C","M","Y","K")]
            if ang_vals != [-999,-999,-999,-999]:
                pairwise_ok = True
                for i in range(len(ang_vals)):
                    for j2 in range(i+1, len(ang_vals)):
                        diff = abs((ang_vals[i] - ang_vals[j2]) % 90)
                        diff = min(diff, 90 - diff)
                        if diff < 15: pairwise_ok = False
                if (120 <= lpi <= 175 and pairwise_ok
                    and tac_max <= 320 and tac_viol <= 3):
                    hi_ok = 1
        except Exception: pass
    s["halftone_density_ok"] = float(hi_ok)

    # --- 16. registration_tolerance.json ---
    rt = rd / "registration_tolerance.json"
    rt_ok = 0
    if rt.exists():
        try:
            j = json.loads(rt.read_text())
            sp = Path(str(j.get("shifted_render_path","")))
            if (bool(j.get("pass")) and float(j.get("delta_e_p95_after_shift",99)) <= 8.0
                and sp.exists() and (rd/"final_cmyk.tif").exists()):
                from PIL import Image, ImageChops
                d = ImageChops.difference(Image.open(sp).convert("CMYK").split()[3],
                                          Image.open(rd/"final_cmyk.tif").convert("CMYK").split()[3])
                if d.getbbox() is not None and 0.05 < (sum(d.getdata())/255.0) / (d.size[0]*d.size[1]) < 0.5:
                    rt_ok = 1
        except Exception: pass
    s["registration_pass"] = float(rt_ok)

    # --- 17. separations sep_{C,M,Y,K}.tif ---
    sep_dir = rd / "separations"
    sep_present = 0
    try:
        from PIL import Image
        import numpy as np
        fc_img = Image.open(rd/"final_cmyk.tif").convert("CMYK") if (rd/"final_cmyk.tif").exists() else None
        for i,ch in enumerate(("C","M","Y","K")):
            p = sep_dir / f"sep_{ch}.tif"
            if not (p.exists() and p.stat().st_size >= 80_000 and fc_img): continue
            a = np.array(Image.open(p).convert("L").resize((128,128)))
            b = np.array(fc_img.split()[i].resize((128,128)))
            if a.std() > 2 and float(np.corrcoef(a.flatten(), b.flatten())[0,1]) > 0.85: sep_present += 1
    except Exception: pass
    s["separations_4x"] = sep_present / 4.0

    # --- 18. perceptual_decoy.json ---
    pd = rd / "perceptual_decoy.json"
    pd_ok = 0
    if pd.exists():
        try:
            j = json.loads(pd.read_text())
            req = {"perceptual_oog_pct","perceptual_delta_e_p95",
                   "relcol_oog_pct","relcol_delta_e_p95","winner","rationale"}
            if (req.issubset(set(j.keys()))
                and str(j.get("winner","")).replace(" ","").lower() == "relativecolorimetric"
                and isinstance(j.get("rationale",""), str) and len(j["rationale"]) >= 60):
                pd_ok = 1
        except Exception: pass
    s["perceptual_decoy_ok"] = float(pd_ok)

    # --- Hard gates ---
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums) if nums else 0.0
    has_cli = ((rd/"oog_before.json").exists() and (rd/"oog_after.json").exists()
               and (rd/"final_cmyk.tif").exists() and (rd/"delta_e.json").exists())
    if not has_cli:                              base = min(base, 0.35)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the gui_screenshots / vlm_* sub_scores.
    # Only apply the VLM cap when the helper actually ran.
    if vlm_score_rubric is not None and vlm_avg < 0.6:
        base = min(base, 0.45)
    if s.get("oog_after_low",0) < 1.0:           base = min(base, 0.40)
    if s.get("delta_e_p95_ok",0) == 0:           base = min(base, 0.40)
    if s.get("final_cmyk_tif_cs",0) == 0:        base = min(base, 0.40)
    if s.get("process_compare_ok",0) == 0:       base = min(base, 0.45)
    if s.get("halftone_density_ok",0) == 0:      base = min(base, 0.45)
    if s.get("registration_pass",0) == 0:        base = min(base, 0.50)
    if s.get("separations_4x",0) < 1.0:          base = min(base, 0.45)
    if s.get("perceptual_decoy_ok",0) == 0:      base = min(base, 0.45)
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
