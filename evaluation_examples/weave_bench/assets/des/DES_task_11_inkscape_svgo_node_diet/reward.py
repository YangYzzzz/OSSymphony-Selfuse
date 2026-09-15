# Auto-generated from WeaveBench task DES_task_11_inkscape_svgo_node_diet.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Grader: SVG node-count diet + visual PSNR + Inkscape GUI evidence."""
    import csv, json, subprocess, re
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    src = Path("/tmp_workspace/svg/brand_traced.svg")
    s = {}

    # --- 1. node_counts_before.csv ---
    nb_csv = rd / "node_counts_before.csv"
    nb_ok = 0; nb_rows = 0
    expect_cols = {"path_id","node_count","d_length_chars"}
    if nb_csv.exists():
        try:
            rows = list(csv.DictReader(nb_csv.open()))
            if rows and expect_cols.issubset(set(rows[0].keys())): nb_ok = 1
            nb_rows = len(rows)
        except Exception: pass
    s["nodes_before_csv"] = float(nb_ok)
    s["nodes_before_rows"] = 1.0 if nb_rows >= 5 else 0.0  # 4 main + 1 decoy

    # --- 2. worst_path.txt ---
    wp = rd / "worst_path.txt"
    wp_ok = 0; worst_id = None
    if wp.exists():
        try:
            txt = wp.read_text().strip()
            m = re.match(r"id\s*=\s*(\S+)", txt)
            if m: worst_id = m.group(1); wp_ok = 1
        except Exception: pass
    s["worst_path_recorded"] = float(wp_ok)

    # --- 3 + 4. simplified + optimized SVG sizes ---
    src_size = src.stat().st_size if src.exists() else 0
    simp = rd / "brand_simplified.svg"
    opt = rd / "brand_optimized.svg"
    simp_ok = 1 if (simp.exists() and src_size and simp.stat().st_size < src_size) else 0
    opt_ok = 0; size_red = 0.0
    if opt.exists() and src_size:
        size_red = (src_size - opt.stat().st_size) / src_size
        if size_red >= 0.70: opt_ok = 1
    simp_red = (src_size - simp.stat().st_size)/src_size if simp.exists() and src_size else 0
    s["simplified_smaller"] = 1.0 if (simp_ok and 0.05 <= simp_red <= 0.65) else 0.0
    s["optimized_70pct_smaller"] = float(opt_ok)
    s["size_reduction_partial"] = 1.0 if size_red >= 0.65 else (0.4 if size_red >= 0.45 else 0.0)

    # --- 5. node_counts_after.csv (>=80% reduction) ---
    na_csv = rd / "node_counts_after.csv"
    na_red_ok = 0
    if nb_csv.exists() and na_csv.exists():
        try:
            tot_b = sum(int(r["node_count"]) for r in csv.DictReader(nb_csv.open()))
            tot_a = sum(int(r["node_count"]) for r in csv.DictReader(na_csv.open()))
            if tot_b and (tot_b - tot_a)/tot_b >= 0.80: na_red_ok = 1
        except Exception: pass
    s["nodes_after_80pct_reduction"] = float(na_red_ok)

    # --- 6. raster files exist + size ---
    raster_ok = 0
    for n in ["raster_before.png","raster_after.png"]:
        p = rd / n
        if p.exists() and p.stat().st_size > 5000:
            try:
                from PIL import Image
                w,h = Image.open(p).size
                if min(w,h) >= 800: raster_ok += 1
            except Exception: pass
    s["raster_files_ok"] = raster_ok / 2.0

    # --- 7. visual_diff.json psnr_db >= 38 + ssim >= 0.985 ---
    vd = rd / "visual_diff.json"
    psnr_ok = 0; psnr_val = 0.0; ssim_ok = 0
    if vd.exists():
        try:
            j = json.loads(vd.read_text())
            psnr_val = float(j.get("psnr_db", 0))
            if psnr_val >= 38: psnr_ok = 1
            if float(j.get("ssim", 0)) >= 0.985: ssim_ok = 1
        except Exception: pass
    s["psnr_above_38"] = float(psnr_ok)
    s["psnr_partial"] = 1.0 if psnr_val >= 36 else (0.5 if psnr_val >= 32 else 0.0)
    s["ssim_above_985"] = float(ssim_ok)

    # --- 8 + 9. screenshots present + OCR ---
    shots = ["view_inkscape_xml_editor.png","view_inkscape_node_tool.png","view_inkscape_overlay.png"]
    shot_present = sum(1 for n in shots if (rd/n).exists() and (rd/n).stat().st_size > 5000)
    s["screenshots_present"] = shot_present / 3.0
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_inkscape_xml_editor.png": ["Inkscape","XML","Editor","path","attribute"],
            "view_inkscape_node_tool.png":  ["Node","Insert","Delete","Smooth","Path","Inkscape"],
            "view_inkscape_overlay.png":    ["Inkscape","File","Edit","Path","Object"],
        }
        for n, ks in kws.items():
            p = rd/n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    hits = sum(1 for k in ks if k.lower() in tx.lower())
                    if hits >= max(3, len(ks)-1): ocr_hits += 1
                except Exception: pass
        s["screenshots_ocr"] = ocr_hits / 3.0
    except ImportError:
        s["screenshots_ocr"] = 0.0

    # --- 10. manifest fields ---
    mf = rd / "manifest.json"
    mf_struct = 0; notes_ok = 0; mf_decoy = 0
    if mf.exists():
        try:
            j = json.loads(mf.read_text())
            req = {"worst_path_id","decoy_path_id","nodes_before_total","nodes_after_total",
                   "node_reduction_pct","psnr_db","ssim","size_reduction_pct","agent_notes"}
            if req.issubset(set(j.keys())): mf_struct = 1
            if isinstance(j.get("agent_notes",""), str) and len(j["agent_notes"]) >= 120:
                notes_ok = 1
            if str(j.get("decoy_path_id","")).strip() and str(j.get("decoy_path_id","")).strip().startswith("p_dx_"):
                mf_decoy = 1
        except Exception: pass
    s["manifest_struct"] = float(mf_struct)
    s["manifest_notes"] = float(notes_ok)
    s["manifest_decoy_id"] = float(mf_decoy)

    # --- 12. multi_dpi PSNR ---
    md_dir = rd / "multi_dpi"
    md_json = md_dir / "multi_psnr.json"
    md_ok = 0; md_partial = 0.0
    if md_json.exists():
        try:
            j = json.loads(md_json.read_text())
            vals = [float(j.get(k, 0)) for k in ("r64","r512","r2048")]
            if all(v >= 35 for v in vals): md_ok = 1
            md_partial = sum(min(1.0, v/35.0) for v in vals) / 3.0
        except Exception: pass
    s["multi_dpi_psnr_ok"] = float(md_ok)
    s["multi_dpi_psnr_partial"] = md_partial

    # --- 13. fft_diff.json hf_ratio in [0.5, 1.10] ---
    fft = rd / "fft_diff.json"
    fft_ok = 0
    if fft.exists():
        try:
            j = json.loads(fft.read_text())
            hr = float(j.get("hf_ratio", 0))
            if 0.5 <= hr <= 1.10: fft_ok = 1
        except Exception: pass
    s["fft_hf_ratio_ok"] = float(fft_ok)

    # --- 14. bbox_check.csv per-path delta <= 1.0 ---
    bbc = rd / "bbox_check.csv"
    bbc_ok = 0
    if bbc.exists():
        try:
            rows = list(csv.DictReader(bbc.open()))
            if rows and all(float(r.get("delta_max", 99)) <= 1.0 for r in rows):
                bbc_ok = 1
        except Exception: pass
    s["bbox_preserved"] = float(bbc_ok)

    # --- 15. phash_distance.json hamming <= 4 ---
    ph = rd / "phash_distance.json"
    ph_ok = 0
    if ph.exists():
        try:
            j = json.loads(ph.read_text())
            if int(j.get("hamming_distance", 99)) <= 4: ph_ok = 1
        except Exception: pass
    s["phash_close"] = float(ph_ok)

    # --- 16. decoy_check.json + worst_path is NOT decoy ---
    dc = rd / "decoy_check.json"
    dc_ok = 0
    try:
        _decoy_id_expected = Path("/tmp_workspace/svg/.decoy_id").read_text().strip()
    except Exception:
        _decoy_id_expected = ""
    if dc.exists():
        try:
            j = json.loads(dc.read_text())
            if (_decoy_id_expected
                and str(j.get("detected_decoy_id","")).strip() == _decoy_id_expected
                and int(j.get("node_count", 99)) <= 1
                and isinstance(j.get("rationale",""), str) and len(j["rationale"]) >= 30):
                dc_ok = 1
        except Exception: pass
    # additionally, worst_path must not be the decoy
    worst_not_decoy = 1
    if worst_id and "decoy" in worst_id.lower(): worst_not_decoy = 0
    s["decoy_detected"] = float(dc_ok and worst_not_decoy)

    # --- VLM rubric ---
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_avg = 0.0  # missing helper => assume failed, force evidence
    if vlm_score_rubric:
        rubric = {
            "vlm_inkscape_chrome": "截图明显是 Inkscape 主界面（Tools/Snap/Status bar 都在）",
            "vlm_node_tool_active": "Node tool 截图能看到 path 上稀疏的菱形/方形节点点",
            "vlm_xml_editor_open": "XML editor 截图含左侧节点树 + 右侧属性表",
            "vlm_overlay_compare": "overlay 截图能直观比较 traced vs optimized 两份 logo",
        }
        imgs = [str(rd/n) for n in shots if (rd/n).exists()]
        if imgs:
            try:
                v = vlm_score_rubric(imgs[:3], rubric, instruction="评估 Inkscape 节点瘦身的 GUI 取证截图。")
                for k in rubric: s[k] = v.get(k, 0.0)
                vlm_avg = sum(s[k] for k in rubric)/len(rubric)
            except Exception:
                for k in rubric: s[k] = 0.5

    # --- Hard gates ---
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums)
    has_cli = (nb_csv.exists() and na_csv.exists() and (rd/"visual_diff.json").exists())
    if not has_cli:                              base = min(base, 0.4)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the gui_screenshots_count / vlm_* sub_scores.
    if vlm_score_rubric is not None and vlm_avg < 0.6:
        base = min(base, 0.6)
    if s.get("optimized_70pct_smaller",0)==0:    base = min(base, 0.30)
    if s.get("psnr_above_38",0)==0:              base = min(base, 0.30)
    if s.get("nodes_after_80pct_reduction",0)==0:base = min(base, 0.30)
    if s.get("multi_dpi_psnr_ok",0)==0:          base = min(base, 0.6)
    if s.get("decoy_detected",0)==0:             base = min(base, 0.35)
    if s.get("phash_close",0)==0:                base = min(base, 0.65)
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
