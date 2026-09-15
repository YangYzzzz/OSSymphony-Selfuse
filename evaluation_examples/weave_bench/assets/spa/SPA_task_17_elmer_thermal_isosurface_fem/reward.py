# Auto-generated from WeaveBench task SPA_task_17_elmer_thermal_isosurface_fem.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """SPA_task_17 grader: Elmer thermal FEM + ParaView iso-surface verify."""
    import json, re, subprocess
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt_dir = Path(workspace_path or "/tmp_workspace") / "gt"
    if not gt_dir.exists(): gt_dir = Path("/tmp_workspace/gt")
    expected = {}
    if (gt_dir / "expected.json").exists():
        try: expected = json.loads((gt_dir / "expected.json").read_text())
        except Exception: pass
    s = {}

    # 1. gmsh outputs
    gmsh_log = rd/"gmsh_buggy.log"; mshb = rd/"heatsink_buggy.msh"
    s["gmsh_log_present"] = 1.0 if gmsh_log.exists() and gmsh_log.stat().st_size > 50 else 0.0
    s["msh_buggy_present"] = 1.0 if mshb.exists() and mshb.stat().st_size > 1000 else 0.0

    # 2. ElmerGrid mesh
    mb_dir = rd/"mesh_buggy"
    s["elmergrid_buggy"] = 1.0 if (mb_dir/"mesh.nodes").exists() else 0.0

    # 3. case_buggy/case.vtu
    cb_vtu = rd/"case_buggy"/"case.vtu"
    s["vtu_buggy_present"] = 1.0 if cb_vtu.exists() and cb_vtu.stat().st_size > 50_000 else 0.0
    s["elmer_buggy_log"] = 1.0 if (rd/"elmer_buggy.log").exists() else 0.0

    # 4. stats_buggy.json
    sb = {}
    sb_p = rd/"stats_buggy.json"
    if sb_p.exists():
        try: sb = json.loads(sb_p.read_text())
        except Exception: pass
    Tmax_b = sb.get("Tmax_C")
    s["stats_buggy_present"] = 1.0 if sb else 0.0
    s["stats_buggy_tmax_range"] = 1.0 if (
        isinstance(Tmax_b,(int,float)) and 120.0 <= Tmax_b <= 230.0) else 0.0
    # hotspot near (30,20)
    hsxyz = sb.get("hotspot_xyz_mm") or []
    near_centre = False
    if isinstance(hsxyz, list) and len(hsxyz) >= 2:
        try:
            near_centre = abs(float(hsxyz[0])-30.0) <= 8.0 and abs(float(hsxyz[1])-20.0) <= 8.0
        except Exception: pass
    s["stats_buggy_hotspot_loc"] = 1.0 if near_centre else 0.0

    # 5-8. ParaView screenshots
    pv_shots = ["view_paraview_top_buggy.png", "view_paraview_iso80_buggy.png",
                "view_paraview_probe_buggy.png", "view_paraview_iso80_fixed.png",
                "view_paraview_side_by_side.png"]
    pv_present = sum(1 for n in pv_shots if (rd/n).exists() and (rd/n).stat().st_size > 2000)
    s["paraview_shots_count"] = pv_present / len(pv_shots)
    # OCR
    ocr_hits = ocr_total = 0
    try:
        from PIL import Image
        import pytesseract
        kw_map = {
            "view_paraview_top_buggy.png": ["ParaView","RenderView","Pipeline"],
            "view_paraview_iso80_buggy.png": ["Contour","Isosurface","353","80"],
            "view_paraview_probe_buggy.png": ["Probe","Spreadsheet","Information"],
            "view_paraview_iso80_fixed.png": ["Contour","Isosurface","353","80"],
            "view_paraview_side_by_side.png": ["buggy","fixed","Compare","ParaView"],
        }
        for fn, kws in kw_map.items():
            p = rd/fn
            if p.exists():
                ocr_total += 1
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in kws): ocr_hits += 1
                except Exception: pass
        s["paraview_ocr"] = (ocr_hits / ocr_total) if ocr_total else 0.0
    except Exception:
        s["paraview_ocr"] = 0.5

    # 7. probe_buggy.json
    pj = rd/"probe_buggy.json"; probe_T = None
    if pj.exists():
        try:
            d = json.loads(pj.read_text())
            probe_T = d.get("probe_temp_C")
        except Exception: pass
    s["probe_buggy_present"] = 1.0 if probe_T is not None else 0.0
    if isinstance(probe_T,(int,float)) and isinstance(Tmax_b,(int,float)):
        s["probe_vs_tmax_close"] = 1.0 if abs(float(probe_T) - float(Tmax_b)) <= 25.0 else (0.5 if abs(float(probe_T) - float(Tmax_b)) <= 35.0 else 0.0)
    else:
        s["probe_vs_tmax_close"] = 0.0

    # 9. case_fixed/case.sif – check h in [200,300] and other materials unchanged
    cf_sif = rd/"case_fixed"/"case.sif"
    sif_ok = sif_unchanged = False
    if cf_sif.exists():
        txt = cf_sif.read_text()
        # find first BC's HTC value
        m = re.search(r"Boundary Condition\s+1\b.*?Heat Transfer Coefficient\s*=\s*([0-9.eE+\-]+)",
                      txt, re.DOTALL)
        if m:
            try:
                h = float(m.group(1))
                sif_ok = (200.0 <= h <= 300.0)
            except Exception: pass
        # heuristic: original Aluminium values must remain
        buggy_sif = (rd/"case_buggy"/"case.sif").read_text() if (rd/"case_buggy"/"case.sif").exists() else ""
        def _norm(t):
            import re
            return [re.sub(r"\s+"," ",l.strip()) for l in t.splitlines()
                    if l.strip() and "Heat Transfer Coefficient" not in l]
        diff_lines = set(_norm(txt)) ^ set(_norm(buggy_sif))
        sif_unchanged = bool(buggy_sif) and len(diff_lines) <= 2 and ("167" in txt) and ("2700" in txt) and ("Heat Source" in txt)
    s["fixed_sif_h_in_range"] = 1.0 if sif_ok else 0.0
    s["fixed_sif_minimal_diff"] = 1.0 if sif_unchanged else 0.0
    diff_path = rd/"sif_diff.txt"
    s["sif_diff_artefact"] = 1.0 if (diff_path.exists() and diff_path.stat().st_size > 30
                                     and "Heat Transfer Coefficient" in diff_path.read_text()) else 0.0
    geo_b = (rd/"heatsink_buggy.geo"); geo_f = (rd/"heatsink_fixed.geo")
    s["geo_only_lc_changed"] = 1.0 if (geo_b.exists() and geo_f.exists()
         and abs(len(geo_b.read_text().splitlines()) - len(geo_f.read_text().splitlines())) <= 2) else 0.0

    # 10. case_fixed/case.vtu + stats_fixed
    cf_vtu = rd/"case_fixed"/"case.vtu"
    s["vtu_fixed_present"] = 1.0 if cf_vtu.exists() and cf_vtu.stat().st_size > 50_000 else 0.0
    sf = {}
    sf_p = rd/"stats_fixed.json"
    if sf_p.exists():
        try: sf = json.loads(sf_p.read_text())
        except Exception: pass
    Tmax_f = sf.get("Tmax_C")
    n_nodes_f = sf.get("n_nodes")
    s["fixed_tmax_under_100"] = 1.0 if (
        isinstance(Tmax_f,(int,float)) and 30.0 <= Tmax_f <= 100.0) else 0.0
    s["fixed_mesh_refined"]   = 1.0 if (
        isinstance(n_nodes_f,(int, float)) and n_nodes_f >= 25000) else 0.0
    # Cross-check: fixed Tmax must be lower than buggy by ≥30 °C
    drop = (Tmax_b - Tmax_f) if isinstance(Tmax_b,(int,float)) and isinstance(Tmax_f,(int,float)) else 0
    s["temp_drop_meaningful"] = 1.0 if drop >= 30.0 else (0.5 if drop >= 18.0 else 0.0)

    # 13. report
    rmd = rd/"report.md"; rpdf = rd/"report.pdf"
    rmd_chars = len(rmd.read_text()) if rmd.exists() else 0
    s["report_md"] = 1.0 if rmd_chars >= 250 else rmd_chars / 250.0
    pages = 0
    if rpdf.exists():
        try:
            out = subprocess.run(["pdfinfo", str(rpdf)], capture_output=True, text=True, timeout=15).stdout
            for ln in out.splitlines():
                if ln.startswith("Pages:"): pages = int(ln.split()[1])
        except Exception: pass
    s["report_pdf_pages"] = 1.0 if pages >= 2 else (pages / 2.0 if pages else 0.0)
    # report content must mention key metrics
    rep_text = rmd.read_text() if rmd.exists() else ""
    import re as _re
    patterns = [r"h[_ ]?bottom\s*[:=]?\s*(?:1?\d{1,2}\.?\d*)\s*W",
                r"lc[_ ]?centre\s*[:=]?\s*\d+\.?\d*\s*mm",
                r"n[_ ]?nodes\s*[:=]?\s*[2-9]\d{4,}",
                r"Tmax[^\n]{0,40}?\d{2,3}\.?\d*\s*°?\s*C",
                r"100\s*°?\s*C"]
    s["report_content_keywords"] = sum(bool(_re.search(p, rep_text, _re.I)) for p in patterns) / len(patterns)

    # 14. Cross-channel evidence count
    cli_outputs = sum(1 for f in [gmsh_log, mshb, sb_p, sf_p, cf_sif, cf_vtu, cb_vtu,
                                   rd/"elmer_buggy.log", rd/"elmer_fixed.log"] if f.exists())
    s["cross_channel"] = 1.0 if (cli_outputs >= 6 and pv_present >= 4) else (
                          0.5 if (cli_outputs >= 4 and pv_present >= 2) else 0.0)

    # VLM rubric on iso-surface screenshots
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd/n) for n in ["view_paraview_iso80_buggy.png",
                                    "view_paraview_iso80_fixed.png",
                                    "view_paraview_side_by_side.png"] if (rd/n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_iso_visible_buggy": "buggy 图中能看到 80°C 等温面的体积形状(像气泡/团块包住电阻)",
            "vlm_iso_shrunk_fixed": "fixed 图中 80°C 等温面明显变小或消失(冷却充分)",
            "vlm_legend_present": "图中显示 ParaView 的颜色条/legend(温度刻度)",
            "vlm_compare_clear": "side-by-side 图中能直接对比两组结果差异",
        }
        try:
            vlm = vlm_score_rubric(vlm_imgs[:3], rubric,
                instruction="评估 ParaView 等温面截图是否能直观区分 buggy 与 fixed 的散热差异。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
            s["judge_method"] = vlm.get("judge_method", "ok")
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_iso_visible_buggy","vlm_iso_shrunk_fixed",
                   "vlm_legend_present","vlm_compare_clear"]:
            s.setdefault(k, 0.0)

    vlm_avg = sum(s.get(k, 0.0) for k in
        ["vlm_iso_visible_buggy","vlm_iso_shrunk_fixed",
         "vlm_legend_present","vlm_compare_clear"]) / 4.0

    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums) / len(nums) if nums else 0.0
    has_cli_evidence = cli_outputs >= 4
    if not has_cli_evidence:    base = min(base, 0.4)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the paraview_shots / vlm_* sub_scores.
    if vlm_score_rubric is not None and vlm_imgs and vlm_avg < 0.4:           base = min(base, 0.40)
    elif vlm_score_rubric is not None and vlm_imgs and vlm_avg < 0.6:         base = min(base, 0.50)
    if vlm_score_rubric is not None and vlm_imgs and s.get("vlm_iso_shrunk_fixed",0.0) < 0.5: base = min(base, 0.55)
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
