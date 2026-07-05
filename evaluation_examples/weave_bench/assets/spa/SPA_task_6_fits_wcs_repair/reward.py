# Auto-generated from WeaveBench task SPA_task_6_fits_wcs_repair.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """SPA_task_6 grader (v2, harder). Weighted: core 60% / gui 30% / aux 10%."""
    import csv, re, hashlib
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. CLI artifacts
    cli_files = ["header_broken.txt","header_correct.txt","projected_pixels_broken.csv","fix_wcs.py"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 3

    # 2. residual_broken.csv: 至少 4/5 残差 > 50″
    rb_score = 0.0
    rb = rd / "residual_broken.csv"
    if rb.exists():
        try:
            rows = list(csv.DictReader(rb.open()))
            if len(rows) >= 5:
                bad_count = sum(1 for r in rows if float(r.get("residual_arcsec", 0)) > 50)
                if bad_count >= 5: rb_score = 1.0
                elif bad_count >= 4: rb_score = 0.7
                elif bad_count >= 2: rb_score = 0.3
        except Exception: pass
    s["residual_broken_large"] = rb_score

    # 3. fix_wcs.py touches ≥4 of the 6 expected keywords AND mentions assigned values
    fw_score = 0.0
    fw_touches = 0
    fw = rd / "fix_wcs.py"
    if fw.exists() and fw.stat().st_size >= 200:
        try:
            txt = fw.read_text()
            kws = ("CRPIX1","CRPIX2","CD2_1","CD2_2","CTYPE1","RADESYS")
            fw_touches = sum(1 for kw in kws if kw in txt)
            has_assign = bool(re.search(r"(header\[|hdr\[|update_header|set_keyword|writeto|\.update\()", txt))
            base_fw = min(1.0, fw_touches / 5)  # 需要命中 5 个才满
            fw_score = base_fw if has_assign else base_fw * 0.5
        except Exception: pass
    s["fix_script_completeness"] = fw_score

    # 4. fixed.fits + ancillary
    s["fixed_fits_exists"] = 1.0 if (workspace / "fixed.fits").exists() and (workspace / "fixed.fits").stat().st_size > 4096 else 0.0
    s["broken_fits_exists"] = 1.0 if (workspace / "broken.fits").exists() else 0.0
    s["correct_fits_exists"] = 1.0 if (workspace / "correct.fits").exists() else 0.0
    s["catalogue_overlay_reg"] = 0.0
    reg_p = workspace / "exec" / "catalogue_overlay.reg"
    if reg_p.exists():
        try:
            rt = reg_p.read_text()
            n_circ = len(re.findall(r"circle", rt, re.I))
            s["catalogue_overlay_reg"] = 1.0 if n_circ >= 5 else (0.5 if n_circ >= 1 else 0.0)
        except Exception: pass

    # 5. residual_fixed.csv all < 1.5"
    rf_score = 0.0; rf_pass_ratio = 0.0
    rf = rd / "residual_fixed.csv"
    if rf.exists():
        try:
            rows = list(csv.DictReader(rf.open()))
            if len(rows) >= 5:
                good = sum(1 for r in rows if float(r.get("residual_arcsec", 99)) < 1.5)
                rf_pass_ratio = good / len(rows)
                rf_score = rf_pass_ratio if rf_pass_ratio >= 1.0 else rf_pass_ratio * 0.6
        except Exception: pass
    s["residual_fixed_small"] = rf_score

    # 6. GUI screenshots — 必须存在 + 大小下限 + md5 多样
    gui_shots = ["view_ds9_broken.png","view_ds9_overlay_broken.png","view_ds9_fixed.png",
                 "view_ds9_overlay_fixed.png","view_ds9_info_panel.png","view_ds9_zoom_star.png"]
    valid_paths = []
    md5s = set()
    for n in gui_shots:
        p = rd / n
        if p.exists() and p.stat().st_size >= 5120:  # >5KB 才算非占位
            try:
                md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
                valid_paths.append(p)
            except Exception: pass
    gui_valid = len(valid_paths)
    s["gui_screenshots_count"] = gui_valid / len(gui_shots)
    s["gui_screenshots_unique"] = len(md5s) / len(gui_shots)
    has_gui = gui_valid >= 5 and len(md5s) >= 5

    # 截图分辨率检查
    res_ok = 0
    try:
        from PIL import Image
        for p in valid_paths:
            try:
                w, h = Image.open(p).size
                if w >= 800 and h >= 600: res_ok += 1
            except Exception: pass
    except Exception:
        res_ok = gui_valid  # 无 PIL 时不扣
    s["gui_screenshots_resolution"] = res_ok / len(gui_shots)

    # OCR
    ocr_available = False
    try:
        import pytesseract
        from PIL import Image
        ocr_available = True
        kws_any = ["DS9","SAOImage","File","Edit","View","Zoom","Frame","Region","WCS","RA","DEC","CRPIX","CTYPE"]
        ocr_hits = 0
        for p in valid_paths:
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k in tx for k in kws_any): ocr_hits += 1
            except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
    except Exception:
        s["gui_screenshots_ocr"] = 0.0
    ocr_pass = s["gui_screenshots_ocr"] >= 0.5

    # 7. wcs_fix_report.md
    rp_score = 0.0
    rp = rd / "wcs_fix_report.md"
    if rp.exists():
        try:
            txt = rp.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            rp_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["wcs_fix_report"] = rp_score

    # 8. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_keys = ["vlm_ds9_window","vlm_region_overlay","vlm_overlay_aligned_in_fixed","vlm_overlay_misaligned_in_broken"]
    vlm_used = False
    if vlm_score_rubric and (rd / "view_ds9_overlay_fixed.png").exists():
        rubric = {
            "vlm_ds9_window": "DS9 主窗口可见,有图像内容(stars / noise)",
            "vlm_region_overlay": "截图能看到 region overlay 圆圈",
            "vlm_overlay_aligned_in_fixed": "fixed 截图里 region 圆套住 star (中心对齐)",
            "vlm_overlay_misaligned_in_broken": "broken 截图里 region 圆明显偏离 star",
        }
        try:
            imgs = [str(rd / n) for n in ["view_ds9_overlay_fixed.png","view_ds9_overlay_broken.png"] if (rd / n).exists()]
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 DS9 broken vs fixed overlay 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
            vlm_used = True
        except Exception:
            for k in vlm_keys: s[k] = 0.0
    else:
        for k in vlm_keys: s[k] = 0.0
    vlm_avg = sum(s[k] for k in vlm_keys) / len(vlm_keys)

    # ===== 加权汇总：core 60% / gui 30% / aux 10% =====
    core = (
        0.30 * s["fixed_fits_exists"] +
        0.30 * s["residual_fixed_small"] +
        0.20 * s["fix_script_completeness"] +
        0.10 * s["residual_broken_large"] +
        0.10 * s["cli_artifacts"]
    )
    gui = (
        0.25 * s["gui_screenshots_count"] +
        0.20 * s["gui_screenshots_unique"] +
        0.15 * s["gui_screenshots_resolution"] +
        0.20 * s["gui_screenshots_ocr"] +
        0.20 * vlm_avg
    )
    aux = (
        0.40 * s["wcs_fix_report"] +
        0.20 * s["broken_fits_exists"] +
        0.20 * s["correct_fits_exists"] +
        0.20 * s["catalogue_overlay_reg"]
    )
    base = 0.60 * core + 0.30 * gui + 0.10 * aux

    # ===== Hard gates（多层、上拉阈值） =====
    if not has_cli: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.30)
    if s["fixed_fits_exists"] < 1.0: base = min(base, 0.35)
    if s["fix_script_completeness"] < 0.8: base = min(base, 0.45)
    if s["residual_fixed_small"] < 1.0: base = min(base, 0.55)
    if not ocr_pass: base = min(base, 0.55)
    if s["gui_screenshots_unique"] < 5/6: base = min(base, 0.50)  # 防同图多复制
    # 防答案泄漏：fix_wcs.py 必须真的命中所有 6 个关键字段中的至少 5 个
    if fw_touches < 5: base = min(base, 0.55)
    # VLM 不可用退化封顶
    if not vlm_used: base = min(base, 0.60)

    s["core_subtotal"] = round(core, 4)
    s["gui_subtotal"] = round(gui, 4)
    s["aux_subtotal"] = round(aux, 4)
    s["overall_score"] = round(max(0.0, min(1.0, base)), 4)
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
