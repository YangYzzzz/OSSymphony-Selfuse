# Auto-generated from WeaveBench task DES_task_2_colorblind_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-dimensional grader for colorblind accessibility audit task."""
    import json, csv, hashlib
    from pathlib import Path

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    if not rd.exists() or not any(rd.iterdir()):
        return {"overall_score": 0.0}

    # Load GT thresholds (fall back to defaults if missing)
    gt_path = workspace / "gt" / "expected.json"
    if not gt_path.exists():
        gt_path = Path(__file__).parent / "gt" / "expected.json" if "__file__" in dir() else gt_path
    gt = {}
    try:
        if gt_path.exists():
            gt = json.loads(gt_path.read_text())
    except Exception:
        gt = {}
    MIN_FIXED_DELTA_E = float(gt.get("min_fixed_delta_e", 10.0))
    WCAG_MIN_RATIO = float(gt.get("wcag_aa_min_ratio", 4.5))
    EXPECTED_SIM = int(gt.get("expected_sim_count", 9))
    EXPECTED_FIXED = int(gt.get("expected_fixed_count", 3))

    # 1. sim images (9 total: 3 banners × 3 types)
    sim_dir = rd / "sim"
    sim_files = list(sim_dir.glob("*.png")) if sim_dir.exists() else []
    s["sim_image_count"] = min(1.0, len(sim_files) / float(EXPECTED_SIM))
    banners = ["banner_promo", "banner_sale", "banner_event"]
    types = ["protanopia", "deuteranopia", "tritanopia"]
    correct_names = sum(1 for b in banners for t in types
                        if sim_dir.exists() and (sim_dir / f"{b}_{t}.png").exists())
    s["sim_naming_correct"] = correct_names / 9.0

    # 2. GUI color picker screenshot
    s["gui_colorpick_screenshot"] = 1.0 if (rd / "view_gimp_colorpick_promo.png").exists() else 0.0

    # 3. contrast_audit.csv
    audit_csv = rd / "contrast_audit.csv"
    audit_rows = []
    if audit_csv.exists():
        try:
            audit_rows = list(csv.DictReader(audit_csv.open()))
            req_cols = {"banner", "fg_hex", "bg_hex", "delta_e", "wcag_ratio", "wcag_aa_pass"}
            cols_ok = req_cols.issubset({c.lower().strip() for c in (audit_rows[0].keys() if audit_rows else [])})
            s["contrast_audit_exists"] = 1.0 if cols_ok and len(audit_rows) >= 3 else 0.3
        except Exception:
            s["contrast_audit_exists"] = 0.0
    else:
        s["contrast_audit_exists"] = 0.0

    # 4. issues_found.json
    iss_f = rd / "issues_found.json"
    if iss_f.exists():
        try:
            data = json.loads(iss_f.read_text())
            req_k = {"banner", "issue", "original_delta_e", "simulated_delta_e", "severity"}
            ok = isinstance(data, list) and len(data) >= 1 and req_k.issubset(set(data[0].keys()))
            s["issues_found_exists"] = 1.0 if ok else 0.3
        except Exception:
            s["issues_found_exists"] = 0.0
    else:
        s["issues_found_exists"] = 0.0

    # 5. GUI simulation comparison screenshots (3)
    sim_shots = ["view_gimp_sim_promo.png", "view_gimp_sim_sale.png", "view_gimp_sim_event.png"]
    s["gui_sim_screenshots"] = sum(1 for n in sim_shots if (rd / n).exists()) / 3.0

    # 6. sim_diff images
    sd_dir = rd / "sim_diff"
    sd_files = list(sd_dir.glob("*.png")) if sd_dir.exists() else []
    s["sim_diff_images"] = min(1.0, len(sd_files) / 3.0)

    # 7. fixed banners exist (3)
    fixed_dir = rd / "fixed"
    fixed_files = list(fixed_dir.glob("*.png")) if fixed_dir.exists() else []
    s["fixed_banners_count"] = min(1.0, len(fixed_files) / float(EXPECTED_FIXED))

    # 8. GUI fix screenshots (3, with dialog)
    fix_shots = ["view_gimp_fix_promo.png", "view_gimp_fix_sale.png", "view_gimp_fix_event.png"]
    s["gui_fix_screenshots"] = sum(1 for n in fix_shots if (rd / n).exists()) / 3.0

    # 9. sim_fixed images (9)
    sf_dir = rd / "sim_fixed"
    sf_files = list(sf_dir.glob("*.png")) if sf_dir.exists() else []
    s["sim_fixed_images"] = min(1.0, len(sf_files) / float(EXPECTED_SIM))

    # 10. before_after screenshots (3)
    ba_shots = ["view_gimp_before_after_promo.png", "view_gimp_before_after_sale.png",
                "view_gimp_before_after_event.png"]
    s["gui_before_after_screenshots"] = sum(1 for n in ba_shots if (rd / n).exists()) / 3.0

    # 11. contrast_fixed.csv — strict: after >= before + ε AND after >= MIN_FIXED_DELTA_E
    cf_csv = rd / "contrast_fixed.csv"
    delta_improved = 0
    delta_total = 0
    delta_meets_threshold = 0
    if cf_csv.exists() and audit_rows:
        try:
            fixed_rows = {r["banner"]: r for r in csv.DictReader(cf_csv.open())}
            for r in audit_rows:
                bn = r.get("banner", "")
                if bn in fixed_rows:
                    delta_total += 1
                    before = float(r.get("delta_e", 0) or 0)
                    after = float(fixed_rows[bn].get("delta_e", 0) or 0)
                    if after >= before + 1.0:
                        delta_improved += 1
                    if after >= MIN_FIXED_DELTA_E:
                        delta_meets_threshold += 1
        except Exception:
            pass
    s["contrast_fixed_exists"] = 1.0 if cf_csv.exists() else 0.0
    s["delta_e_improved"] = (delta_improved / delta_total) if delta_total else 0.0
    s["delta_e_meets_threshold"] = (delta_meets_threshold / delta_total) if delta_total else 0.0

    # 12. wcag_verification.json — also check the ratios actually meet WCAG_MIN_RATIO
    wv_f = rd / "wcag_verification.json"
    if wv_f.exists():
        try:
            data = json.loads(wv_f.read_text())
            req_k = {"banner", "wcag_ratio", "pass"}
            ok = isinstance(data, list) and len(data) >= 1 and req_k.issubset(set(data[0].keys()))
            s["wcag_verification_exists"] = 1.0 if ok else 0.3
            # Strict: pass only if claimed pass AND wcag_ratio actually >= WCAG_MIN_RATIO
            real_pass = 0
            for e in data if isinstance(data, list) else []:
                try:
                    if e.get("pass") and float(e.get("wcag_ratio", 0)) >= WCAG_MIN_RATIO:
                        real_pass += 1
                except Exception:
                    pass
            s["wcag_aa_pass"] = real_pass / max(1, len(data) if isinstance(data, list) else 1)
        except Exception:
            s["wcag_verification_exists"] = 0.0
            s["wcag_aa_pass"] = 0.0
    else:
        s["wcag_verification_exists"] = 0.0
        s["wcag_aa_pass"] = 0.0

    # 13. GUI final check screenshot
    s["gui_final_check"] = 1.0 if (rd / "view_gimp_final_check.png").exists() else 0.0

    # 14. audit_report.json
    ar_f = rd / "audit_report.json"
    if ar_f.exists():
        try:
            d = json.loads(ar_f.read_text())
            req = {"total_banners", "issues_found", "issues_fixed",
                   "avg_delta_e_before", "avg_delta_e_after", "all_wcag_aa_pass"}
            s["audit_report_exists"] = 1.0 if req.issubset(set(d.keys())) else 0.5
        except Exception:
            s["audit_report_exists"] = 0.0
    else:
        s["audit_report_exists"] = 0.0

    # GUI screenshot anti-cheat: md5 unique, min size, min resolution
    gui_shot_names = [
        "view_gimp_colorpick_promo.png",
        "view_gimp_sim_promo.png", "view_gimp_sim_sale.png", "view_gimp_sim_event.png",
        "view_gimp_fix_promo.png", "view_gimp_fix_sale.png", "view_gimp_fix_event.png",
        "view_gimp_histogram_fix.png",
        "view_gimp_before_after_promo.png", "view_gimp_before_after_sale.png",
        "view_gimp_before_after_event.png",
        "view_gimp_final_check.png",
    ]
    md5s = set()
    valid_shot_count = 0
    total_shots_present = 0
    for name in gui_shot_names:
        p = rd / name
        if not p.exists():
            continue
        total_shots_present += 1
        try:
            sz = p.stat().st_size
            if sz < 5 * 1024:
                continue
            h = hashlib.md5(p.read_bytes()).hexdigest()
            if h in md5s:
                continue
            md5s.add(h)
            try:
                from PIL import Image as _PILI
                with _PILI.open(p) as im:
                    w, hh = im.size
                if w < 1024 or hh < 600:
                    continue
            except Exception:
                pass
            valid_shot_count += 1
        except Exception:
            pass
    s["gui_screenshot_validity"] = (valid_shot_count / float(len(gui_shot_names)))
    s["gui_screenshot_uniqueness"] = (len(md5s) / float(total_shots_present)) if total_shots_present else 0.0

    # GUI OCR checks
    try:
        import pytesseract
        from PIL import Image as PILImage
        ocr_cfg = {
            "view_gimp_colorpick_promo.png": ["GIMP", "Color", "Pick", "RGB"],
            "view_gimp_sim_promo.png": ["GIMP", "banner", "promo"],
            "view_gimp_fix_promo.png": ["GIMP", "Hue", "Saturation", "Color"],
            "view_gimp_final_check.png": ["GIMP", "Color", "Deficiency", "Filter"],
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

    vlm_keys = ["vlm_gimp_ui_visible", "vlm_two_images_compared",
                "vlm_color_dialog_open", "vlm_before_after_diff"]
    vlm_imgs = [str(rd / n) for n in
                ["view_gimp_sim_promo.png", "view_gimp_fix_promo.png",
                 "view_gimp_before_after_promo.png", "view_gimp_final_check.png"]
                if (rd / n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_gimp_ui_visible": "截图中可见 GIMP 标题栏、工具栏等 UI 元素",
            "vlm_two_images_compared": "截图中可见两张图像的并排对比（原图和模拟/修复图）",
            "vlm_color_dialog_open": "截图中可见 GIMP 颜色调整对话框（Hue-Saturation、Color Balance 等）",
            "vlm_before_after_diff": "修复前后对比截图中两张模拟图存在明显视觉差异",
        }
        vlm = vlm_score_rubric(vlm_imgs, rubric,
                               instruction="评估色盲无障碍审核 GIMP 截图质量")
        for k in vlm_keys:
            s[k] = vlm.get(k, 0.0)
    else:
        for k in vlm_keys:
            s[k] = 0.0

    # Weighted overall: core delivery (60%) + GUI evidence (30%) + aux (10%)
    core_keys = [
        "sim_image_count", "sim_naming_correct", "contrast_audit_exists",
        "issues_found_exists", "sim_diff_images", "fixed_banners_count",
        "sim_fixed_images", "contrast_fixed_exists", "delta_e_improved",
        "delta_e_meets_threshold", "wcag_verification_exists", "wcag_aa_pass",
        "audit_report_exists",
    ]
    gui_keys = [
        "gui_colorpick_screenshot", "gui_sim_screenshots", "gui_fix_screenshots",
        "gui_before_after_screenshots", "gui_final_check",
        "gui_screenshot_validity", "gui_screenshot_uniqueness", "gui_ocr_quality",
    ] + vlm_keys
    aux_keys = []  # remainder bucket; currently empty

    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return (sum(vals) / len(vals)) if vals else 0.0

    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys) if aux_keys else 0.0
    if aux_keys:
        base = 0.6 * core + 0.3 * gui + 0.1 * aux
    else:
        base = (0.6 * core + 0.3 * gui) / 0.9  # renormalize when aux empty

    # Multi-layer hard gates
    has_cli = s.get("sim_image_count", 0) >= 0.9 and s.get("contrast_audit_exists", 0) > 0
    has_fixed_pipeline = (s.get("fixed_banners_count", 0) >= 0.9
                         and s.get("sim_fixed_images", 0) >= 0.9
                         and s.get("contrast_fixed_exists", 0) > 0)
    has_gui = s.get("gui_sim_screenshots", 0) >= 0.5 or s.get("gui_fix_screenshots", 0) >= 0.5
    gui_shots_real = (s.get("gui_screenshot_validity", 0) >= 0.5
                      and s.get("gui_screenshot_uniqueness", 0) >= 0.7)

    if not has_cli:
        base = min(base, 0.40)
    if not has_fixed_pipeline:
        base = min(base, 0.45)
    if not has_gui:
        base = min(base, 0.40)
    if not gui_shots_real:
        base = min(base, 0.50)
    if s.get("gui_ocr_quality", 0) < 0.5:
        base = min(base, 0.55)
    if s.get("wcag_aa_pass", 0) < 0.6:
        base = min(base, 0.60)
    if s.get("delta_e_improved", 0) < 0.6 or s.get("delta_e_meets_threshold", 0) < 0.6:
        base = min(base, 0.55)
    # VLM unavailable cap: prevent full marks without rubric judging
    if not any(s.get(k, 0) > 0 for k in vlm_keys):
        base = min(base, 0.65)

    s["overall_score"] = round(max(0.0, min(1.0, base)), 3)
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
