# Auto-generated from WeaveBench task DES_task_1_heic_avif_batch.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-dimensional grader for HEIC→AVIF batch conversion QA task."""
    import json, csv, subprocess, hashlib
    from pathlib import Path

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    if not rd.exists() or not any(rd.iterdir()):
        return {"overall_score": 0.0}

    # Anti-cheat helper: screenshot must be > 5KB AND have a unique md5 across
    # the screenshot batch (rules out copy-pasted placeholder PNGs).
    _shot_md5s = {}
    def _shot_ok(name: str) -> bool:
        p = rd / name
        if not p.exists():
            return False
        try:
            data = p.read_bytes()
        except Exception:
            return False
        if len(data) < 5 * 1024:
            return False
        h = hashlib.md5(data).hexdigest()
        if h in _shot_md5s and _shot_md5s[h] != name:
            return False
        _shot_md5s[h] = name
        return True

    # 1. exif_audit.csv
    exif_csv = rd / "exif_audit.csv"
    if exif_csv.exists():
        try:
            rows = list(csv.DictReader(exif_csv.open()))
            req_cols = {"filename", "width", "height", "color_space", "icc_profile"}
            cols_ok = req_cols.issubset({c.lower().strip() for c in (rows[0].keys() if rows else [])})
            s["exif_audit_csv"] = min(1.0, len(rows) / 8.0) if cols_ok else 0.3
        except Exception:
            s["exif_audit_csv"] = 0.0
    else:
        s["exif_audit_csv"] = 0.0

    # 2. spec_validation.txt
    spec_txt = rd / "spec_validation.txt"
    if spec_txt.exists():
        lines = [l for l in spec_txt.read_text(errors="ignore").splitlines() if l.strip()]
        s["spec_validation"] = min(1.0, len(lines) / 8.0)
    else:
        s["spec_validation"] = 0.0

    # 3. GUI precheck screenshot
    s["gui_precheck_screenshot"] = 1.0 if _shot_ok("view_gimp_precheck_overview.png") else 0.0

    # 4. AVIF files exist (8 total)
    avif_dir = rd / "avif"
    avif_files = list(avif_dir.glob("*.avif")) if avif_dir.exists() else []
    s["avif_file_count"] = min(1.0, len(avif_files) / 8.0)

    # 5. GIMP comparison screenshots (3 required) — anti-cheat: size + md5 unique
    gui_compare = ["view_gimp_compare_03.png", "view_gimp_compare_05.png",
                   "view_gimp_compare_07.png"]
    gui_present = sum(1 for n in gui_compare if _shot_ok(n))
    s["gui_compare_screenshots"] = gui_present / 3.0

    # 6. ssim_report.csv — per-image threshold from quality_spec.json (stricter)
    ssim_csv = rd / "ssim_report.csv"
    ssim_ok = 0
    ssim_total = 0
    spec_thresh = {}
    try:
        spec_path = workspace / "quality_spec.json"
        if not spec_path.exists():
            spec_path = workspace / "exec" / "quality_spec.json"
        if spec_path.exists():
            for e in json.loads(spec_path.read_text()):
                base = str(e.get("filename", "")).rsplit(".", 1)[0]
                if base:
                    spec_thresh[base] = float(e.get("min_ssim", 0.85))
    except Exception:
        spec_thresh = {}
    if ssim_csv.exists():
        try:
            rows = list(csv.DictReader(ssim_csv.open()))
            ssim_total = len(rows)
            for r in rows:
                val = float(r.get("ssim", 0) or 0)
                base = str(r.get("filename", "")).rsplit(".", 1)[0]
                thr = spec_thresh.get(base, 0.85)
                if val >= thr:
                    ssim_ok += 1
        except Exception:
            pass
    s["ssim_report_rows"] = min(1.0, ssim_total / 8.0)
    s["ssim_above_threshold"] = (ssim_ok / ssim_total) if ssim_total else 0.0

    # 7. Diff map screenshot (GUI Curves)
    s["gui_diffmap_screenshot"] = 1.0 if _shot_ok("view_gimp_diffmap_03.png") else 0.0

    # 7b. diff_photo_03.png (raw diff map deliverable)
    s["diff_photo_artifact"] = 1.0 if (rd / "diff_photo_03.png").exists() else 0.0

    # 8. Histogram comparison screenshot
    s["gui_histogram_screenshot"] = 1.0 if _shot_ok("view_gimp_histogram_compare.png") else 0.0

    # 9. icc_check.json
    icc_f = rd / "icc_check.json"
    if icc_f.exists():
        try:
            data = json.loads(icc_f.read_text())
            if isinstance(data, list) and len(data) >= 1 and all("file" in e and "has_icc" in e for e in data):
                s["icc_check_json"] = min(1.0, len(data) / 8.0)
            else:
                s["icc_check_json"] = 0.3
        except Exception:
            s["icc_check_json"] = 0.0
    else:
        s["icc_check_json"] = 0.0

    # 10. metadata_fix_log.json
    mfl = rd / "metadata_fix_log.json"
    if mfl.exists():
        try:
            data = json.loads(mfl.read_text())
            if isinstance(data, list) and len(data) >= 1 and all("file" in e and "xmp_written" in e for e in data):
                s["metadata_fix_log"] = 1.0
            else:
                s["metadata_fix_log"] = 0.3
        except Exception:
            s["metadata_fix_log"] = 0.0
    else:
        s["metadata_fix_log"] = 0.0

    # 11. XMP tag verification via exiftool
    xmp_score = 0.0
    if avif_dir.exists() and avif_files:
        try:
            checked = hit = 0
            for af in avif_files[:3]:
                checked += 1
                out = subprocess.run(
                    ["exiftool", "-XMP-dc:Description", "-s3", str(af)],
                    capture_output=True, text=True, timeout=10
                )
                if "QA-passed" in out.stdout:
                    hit += 1
            xmp_score = (hit / checked) if checked else 0.0
        except Exception:
            xmp_score = 0.0
    s["xmp_tag_written"] = xmp_score

    # 12. GUI metadata viewer screenshot
    s["gui_metadata_screenshot"] = 1.0 if _shot_ok("view_gimp_metadata.png") else 0.0

    # 13. size_report.csv
    size_csv = rd / "size_report.csv"
    if size_csv.exists():
        try:
            rows = list(csv.DictReader(size_csv.open()))
            s["size_report"] = min(1.0, len(rows) / 8.0)
        except Exception:
            s["size_report"] = 0.0
    else:
        s["size_report"] = 0.0

    # 14. conversion_report.json — qa_screenshots must list all 6 specific names
    cr = rd / "conversion_report.json"
    expected_qa = {"view_gimp_compare_03.png", "view_gimp_compare_05.png",
                   "view_gimp_compare_07.png", "view_gimp_diffmap_03.png",
                   "view_gimp_histogram_compare.png", "view_gimp_metadata.png"}
    if cr.exists():
        try:
            d = json.loads(cr.read_text())
            req = {"total_images", "all_ssim_above_threshold", "avg_ssim",
                   "avg_compression_ratio", "metadata_intact_count", "failed_images",
                   "qa_screenshots"}
            ok = req.issubset(set(d.keys()))
            qa = d.get("qa_screenshots")
            qa_set = set(qa) if isinstance(qa, list) else set()
            qa_named_ok = expected_qa.issubset(qa_set)
            if ok and qa_named_ok:
                s["conversion_report"] = 1.0
            elif ok and isinstance(qa, list) and len(qa) >= 6:
                s["conversion_report"] = 0.7
            elif ok:
                s["conversion_report"] = 0.5
            else:
                s["conversion_report"] = 0.3
        except Exception:
            s["conversion_report"] = 0.0
    else:
        s["conversion_report"] = 0.0

    # GUI OCR checks
    try:
        import pytesseract
        from PIL import Image as PILImage
        ocr_checks = {
            "view_gimp_compare_03.png": ["GIMP", "200", "zoom", "photo"],
            "view_gimp_diffmap_03.png": ["Curves", "GIMP"],
            "view_gimp_histogram_compare.png": ["Histogram", "GIMP"],
            "view_gimp_metadata.png": ["Metadata", "EXIF", "XMP", "GIMP"],
            "view_gimp_precheck_overview.png": ["GIMP", "Properties", "Image"],
        }
        ocr_hits = 0
        for fname, kws in ocr_checks.items():
            p = rd / fname
            if p.exists():
                try:
                    txt = pytesseract.image_to_string(PILImage.open(p))
                    if any(k.lower() in txt.lower() for k in kws):
                        ocr_hits += 1
                except Exception:
                    pass
        s["gui_ocr_quality"] = ocr_hits / len(ocr_checks)
    except ImportError:
        s["gui_ocr_quality"] = 0.0

    # VLM rubric (≥4 items)
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    vlm_keys = ["vlm_zoom_visible", "vlm_two_images_side_by_side",
                "vlm_curves_dialog_open", "vlm_histogram_panel_visible"]
    vlm_imgs = [str(rd / n) for n in
                ["view_gimp_compare_03.png", "view_gimp_diffmap_03.png",
                 "view_gimp_histogram_compare.png", "view_gimp_metadata.png"]
                if (rd / n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_zoom_visible": "截图中可见 200% 缩放级别标识（如 200:1 或 zoom 数字）",
            "vlm_two_images_side_by_side": "截图中可见原图和转换后图像的并排或双窗口对比",
            "vlm_curves_dialog_open": "差异图截图中可见 GIMP Curves 对话框（含通道曲线）",
            "vlm_histogram_panel_visible": "直方图截图中可见 GIMP Histogram 面板（含频谱）",
        }
        vlm = vlm_score_rubric(vlm_imgs, rubric,
                               instruction="评估 HEIC→AVIF 转换质量审核 GIMP 截图")
        for k in vlm_keys:
            s[k] = vlm.get(k, 0.0)
    else:
        for k in vlm_keys:
            s[k] = 0.0

    # ---- Weighted overall scoring ----
    # Core deliverables (60%): the actual conversion outputs that the task asks for.
    core_keys = ["avif_file_count", "ssim_above_threshold", "ssim_report_rows",
                 "exif_audit_csv", "icc_check_json", "metadata_fix_log",
                 "xmp_tag_written", "size_report", "conversion_report",
                 "diff_photo_artifact"]
    # GUI evidence (30%): screenshots + OCR/VLM that the agent really used GIMP.
    gui_keys = ["gui_precheck_screenshot", "gui_compare_screenshots",
                "gui_diffmap_screenshot", "gui_histogram_screenshot",
                "gui_metadata_screenshot", "gui_ocr_quality"] + vlm_keys
    # Auxiliary (10%): supporting artefacts.
    aux_keys = ["spec_validation"]

    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return (sum(vals) / len(vals)) if vals else 0.0

    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Hard gates — multi-layer, each caps `base` independently.
    has_cli = s.get("exif_audit_csv", 0) > 0 and s.get("ssim_report_rows", 0) > 0
    has_gui = s.get("gui_compare_screenshots", 0) >= 0.6
    if not has_cli:
        base = min(base, 0.40)
    if not has_gui:
        base = min(base, 0.40)
    # Core deliverable: AVIF batch must exist + most pass per-image SSIM.
    if s.get("avif_file_count", 0) < 0.75 or s.get("ssim_above_threshold", 0) < 0.5:
        base = min(base, 0.45)
    # Metadata closed-loop must actually be done (XMP tag verified by exiftool).
    if s.get("xmp_tag_written", 0) < 0.5:
        base = min(base, 0.55)
    # OCR gate (only when OCR stack is installed).
    try:
        import pytesseract  # noqa: F401
        _ocr_available = True
    except Exception:
        _ocr_available = False
    if _ocr_available and s.get("gui_ocr_quality", 0) < 0.4:
        base = min(base, 0.55)
    # VLM gate: when VLM judge is unavailable, cap to prevent free pass.
    _vlm_used = any(s.get(k, 0) > 0 for k in vlm_keys)
    if not _vlm_used:
        base = min(base, 0.60)
    # Conversion report must list all 6 named QA screenshots (full credit only
    # when conversion_report >= 1.0).
    if s.get("conversion_report", 0) < 1.0:
        base = min(base, 0.70)

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
