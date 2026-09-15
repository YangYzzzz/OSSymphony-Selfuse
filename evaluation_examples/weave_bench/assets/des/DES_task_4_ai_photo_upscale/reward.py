# Auto-generated from WeaveBench task DES_task_4_ai_photo_upscale.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """AI photo upscale QA pipeline grader."""
    import json, subprocess
    from pathlib import Path

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    if not rd.exists() or not any(rd.iterdir()):
        return {"overall_score": 0.0}

    MIN_SHOT_BYTES = 10 * 1024  # 10KB; smaller = placeholder/fake
    def _shot_ok(p):
        try:
            return p.exists() and p.stat().st_size >= MIN_SHOT_BYTES
        except Exception:
            return False

    # 1. baseline_info.txt
    bi = rd / "baseline_info.txt"
    if bi.exists():
        txt = bi.read_text(errors="ignore")
        img_count = txt.lower().count("jpeg") + txt.lower().count("png")
        s["baseline_info"] = 1.0 if img_count >= 3 else max(0.0, img_count / 3.0)
    else:
        s["baseline_info"] = 0.0

    # 2. GUI original levels screenshot (must be ≥ 10KB, not placeholder)
    s["gui_original_levels"] = 1.0 if _shot_ok(rd / "view_gimp_original_levels.png") else 0.0

    # 3. 4x upscaled files exist + resolution check
    names_4x = ["landscape_4x.png", "portrait_4x.png", "macro_4x.png"]
    up_count = 0
    res_ok = 0
    for name in names_4x:
        fp = rd / name
        if fp.exists():
            up_count += 1
            try:
                out = subprocess.run(
                    ["identify", "-format", "%wx%h", str(fp)],
                    capture_output=True, text=True, timeout=10
                )
                if "1920" in out.stdout and "1440" in out.stdout:
                    res_ok += 1
            except Exception:
                pass
    s["upscaled_count"] = up_count / 3.0
    s["upscaled_resolution"] = res_ok / 3.0

    # 4. bicubic reference files
    names_bc = ["landscape_bicubic.png", "portrait_bicubic.png", "macro_bicubic.png"]
    bc_count = sum(1 for n in names_bc if (rd / n).exists())
    s["bicubic_files"] = bc_count / 3.0

    # 5. psnr_comparison.json
    psnr_f = rd / "psnr_comparison.json"
    if psnr_f.exists():
        try:
            d = json.loads(psnr_f.read_text())
            # Tighter: real PSNR for 4x upscale should be > 15 dB; trivial constants score 0
            valid = sum(1 for key in ["landscape", "portrait", "macro"]
                        if key in d and 15.0 < float(d[key].get("bicubic_vs_ai_psnr_db", 0) or 0) < 80.0)
            s["psnr_comparison"] = valid / 3.0
        except Exception:
            s["psnr_comparison"] = 0.0
    else:
        s["psnr_comparison"] = 0.0

    # 6. GUI bicubic vs AI screenshot
    s["gui_bicubic_vs_ai"] = 1.0 if _shot_ok(rd / "view_gimp_bicubic_vs_ai.png") else 0.0

    # 7. upscaled_metadata.txt — check resolution and colorspace
    um = rd / "upscaled_metadata.txt"
    if um.exists():
        txt = um.read_text(errors="ignore").lower()
        has_res = "1920" in txt and "1440" in txt
        has_srgb = "srgb" in txt or "rgb" in txt
        s["upscaled_metadata"] = 1.0 if (has_res and has_srgb) else (0.5 if has_res else 0.0)
    else:
        s["upscaled_metadata"] = 0.0

    # 8. GUI edge detect screenshot
    s["gui_edge_detect"] = 1.0 if _shot_ok(rd / "view_gimp_edge_detect.png") else 0.0

    # 9. GUI curves compare screenshot
    s["gui_curves_compare"] = 1.0 if _shot_ok(rd / "view_gimp_curves_compare.png") else 0.0

    # 10. GUI histogram screenshot
    s["gui_histogram"] = 1.0 if _shot_ok(rd / "view_gimp_histogram.png") else 0.0

    # 11. color_depth_report.txt
    cd = rd / "color_depth_report.txt"
    if cd.exists():
        txt = cd.read_text(errors="ignore").lower()
        s["color_depth_report"] = 1.0 if any(kw in txt for kw in ["colorspace", "srgb", "rgb"]) else 0.3
    else:
        s["color_depth_report"] = 0.0

    # 12. dssim_scores.json
    ds_f = rd / "dssim_scores.json"
    if ds_f.exists():
        try:
            d = json.loads(ds_f.read_text())
            # Tighter: real DSSIM for similar 4x outputs should be < 0.5; 0 also rejected (suspect)
            valid = sum(1 for key in ["landscape", "portrait", "macro"]
                        if key in d and 0.0 < float(d[key].get("dssim", 999) or 999) < 0.5)
            s["dssim_scores"] = valid / 3.0
        except Exception:
            s["dssim_scores"] = 0.0
    else:
        s["dssim_scores"] = 0.0

    # 13. GUI final output screenshot
    s["gui_final_output"] = 1.0 if _shot_ok(rd / "view_gimp_final_output.png") else 0.0

    # 13b. GUI artifact check screenshot
    s["gui_artifact_check"] = 1.0 if _shot_ok(rd / "view_gimp_artifact_check.png") else 0.0

    # 13c. Anti-cheat: screenshots must be md5-unique (no copy-paste of one shot)
    import hashlib
    shot_names = [
        "view_gimp_original_levels.png", "view_gimp_bicubic_vs_ai.png",
        "view_gimp_edge_detect.png", "view_gimp_curves_compare.png",
        "view_gimp_histogram.png", "view_gimp_artifact_check.png",
        "view_gimp_final_output.png",
    ]
    md5s = []
    for n in shot_names:
        p = rd / n
        if _shot_ok(p):
            try:
                md5s.append(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception:
                pass
    s["screenshot_uniqueness"] = (len(set(md5s)) / len(shot_names)) if shot_names else 0.0

    # 14. quality_report.md
    qr = rd / "quality_report.md"
    if qr.exists():
        txt = qr.read_text(errors="ignore")
        s["quality_report"] = 1.0 if len(txt) >= 500 else max(0.0, len(txt) / 500.0)
    else:
        s["quality_report"] = 0.0

    # GUI OCR checks
    try:
        import pytesseract
        from PIL import Image as PILImage
        ocr_cfg = {
            "view_gimp_original_levels.png": ["GIMP", "Levels", "Input"],
            "view_gimp_bicubic_vs_ai.png": ["GIMP", "200", "zoom"],
            "view_gimp_edge_detect.png": ["GIMP", "Edge", "400"],
            "view_gimp_curves_compare.png": ["GIMP", "Curves", "RGB"],
            "view_gimp_histogram.png": ["GIMP", "Histogram"],
            "view_gimp_artifact_check.png": ["GIMP", "Filter"],
        }
        hits = 0
        for fname, kws in ocr_cfg.items():
            p = rd / fname
            if p.exists():
                try:
                    txt = pytesseract.image_to_string(PILImage.open(p))
                    if any(k.lower() in txt.lower() for k in kws):
                        hits += 1
                except Exception:
                    pass
        s["gui_ocr_quality"] = hits / len(ocr_cfg)
    except ImportError:
        s["gui_ocr_quality"] = 0.0

    # VLM rubric (≥4 items)
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    vlm_keys = ["vlm_zoom_detail_visible", "vlm_gimp_ui_present",
                "vlm_curves_panel_open", "vlm_histogram_visible"]
    vlm_imgs = [str(rd / n) for n in
                ["view_gimp_bicubic_vs_ai.png", "view_gimp_edge_detect.png",
                 "view_gimp_curves_compare.png", "view_gimp_histogram.png"]
                if _shot_ok(rd / n)]
    vlm_available = bool(vlm_score_rubric and vlm_imgs)
    if vlm_available:
        rubric = {
            "vlm_zoom_detail_visible": "截图中可见放大图像（200% 或 400%）的纹理细节",
            "vlm_gimp_ui_present": "截图中可见 GIMP 标题栏、菜单栏等 UI 元素",
            "vlm_curves_panel_open": "截图中可见 GIMP Curves 对话框（含曲线/通道面板）",
            "vlm_histogram_visible": "截图中可见 GIMP Histogram 面板（含频谱分布）",
        }
        vlm = vlm_score_rubric(vlm_imgs, rubric,
                               instruction="评估 AI 超分质检 GIMP 截图质量")
        for k in vlm_keys:
            s[k] = vlm.get(k, 0.0)
    else:
        for k in vlm_keys:
            s[k] = 0.0

    # Weighted overall: core delivery 60% / GUI evidence 30% / aux 10%
    def _avg(keys):
        vals = [s.get(k, 0.0) for k in keys]
        return sum(vals) / len(vals) if vals else 0.0

    core_keys = ["upscaled_count", "upscaled_resolution", "bicubic_files",
                 "psnr_comparison", "dssim_scores", "quality_report"]
    gui_keys = ["gui_original_levels", "gui_bicubic_vs_ai", "gui_edge_detect",
                "gui_curves_compare", "gui_histogram", "gui_artifact_check",
                "gui_final_output", "gui_ocr_quality", "screenshot_uniqueness"] + vlm_keys
    aux_keys = ["baseline_info", "upscaled_metadata", "color_depth_report"]

    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Multi-layer hard gates (越严越好)
    has_cli = s.get("baseline_info", 0) > 0 and s.get("upscaled_count", 0) >= 0.6
    has_gui = sum(1 for k in ["gui_bicubic_vs_ai", "gui_edge_detect",
                              "gui_curves_compare", "gui_histogram"]
                  if s.get(k, 0) > 0) >= 2

    if not has_cli:
        base = min(base, 0.4)
    if not has_gui:
        base = min(base, 0.4)
    # Core delivery gate: PSNR or DSSIM 完全失败 → cap 0.4
    if s.get("psnr_comparison", 0) < 0.34 or s.get("dssim_scores", 0) < 0.34:
        base = min(base, 0.4)
    # Upscaled resolution gate: 三张图分辨率全 fail → cap 0.45
    if s.get("upscaled_resolution", 0) < 0.34:
        base = min(base, 0.45)
    # OCR gate (tightened): <0.4 cap 0.5; <0.2 cap 0.4
    if s.get("gui_ocr_quality", 0) < 0.2:
        base = min(base, 0.4)
    elif s.get("gui_ocr_quality", 0) < 0.4:
        base = min(base, 0.5)
    # Screenshot uniqueness gate: 复制粘贴同一张截图 → cap 0.5
    if s.get("screenshot_uniqueness", 0) < 0.6:
        base = min(base, 0.5)
    # VLM unavailable → cap 0.6 (don't allow full score without visual judging)
    if not vlm_available:
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
