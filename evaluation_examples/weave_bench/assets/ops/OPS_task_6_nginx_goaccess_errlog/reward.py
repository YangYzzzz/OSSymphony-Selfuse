# Auto-generated from WeaveBench task OPS_task_6_nginx_goaccess_errlog.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """OPS_task_6 grader. Reads private expectations from gt/expected.json."""
    import re, json, hashlib
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"

    # Locate gt/expected.json (private oracle: keywords / thresholds not in Prompt)
    # NOTE: grader is exec()'d, no __file__ available; rely on workspace_path side-paths.
    gt = {}
    for cand in [
        workspace / "gt" / "expected.json",
        workspace.parent / "gt" / "expected.json",
        workspace.parent / "OPS" / "task_6_nginx_goaccess_errlog" / "gt" / "expected.json",
    ]:
        try:
            if cand.exists():
                gt = json.loads(cand.read_text()); break
        except Exception:
            pass
    anomalous = gt.get("expected_anomalous_codes_before", ["413", "504"])
    fix_kws = gt.get("fix_must_include_keywords",
                     ["worker_connections", "client_max_body_size", "proxy_read_timeout"])
    fix_min_hits = int(gt.get("fix_min_keyword_hits", 3))
    max_413 = int(gt.get("expected_after_fix_max_413", 0))
    max_504 = int(gt.get("expected_after_fix_max_504", 2))
    min_413_before = int(gt.get("expected_413_count_min_before", 30))
    min_504_before = int(gt.get("expected_504_count_min_before", 15))
    min_shot_bytes = int(gt.get("min_screenshot_bytes", 5120))
    min_w, min_h = gt.get("min_screenshot_resolution", [1280, 720])
    min_diversity = float(gt.get("min_md5_diversity", 0.8))
    vlm_cap = float(gt.get("vlm_unavailable_cap", 0.6))

    s = {}

    # 1. CLI artifacts
    cli_files = ["load_test.log","http_codes_before.txt","http_codes_after.txt",
                 "error_log_before.txt","nginx.conf.backup","load_test_after.log"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 4

    # 2. http_codes_before: must contain all anomalous codes AND counts >= private min
    bp_score = 0.0
    bp = rd / "http_codes_before.txt"
    cnt_413_before = cnt_504_before = 0
    if bp.exists():
        try:
            txt = bp.read_text()
            present_codes = sum(1 for c in anomalous if c in txt)
            for line in txt.splitlines():
                m = re.search(r"(\d+)\D+(\d{3})", line.strip())
                if m:
                    cnt, code = int(m.group(1)), m.group(2)
                    if code == "413": cnt_413_before += cnt
                    if code == "504": cnt_504_before += cnt
            cov = present_codes / max(1, len(anomalous))
            volume_ok = (cnt_413_before >= min_413_before and cnt_504_before >= min_504_before)
            bp_score = cov if not volume_ok else max(cov, 1.0)
            if cov < 1.0: bp_score = min(bp_score, 0.5)
        except Exception: pass
    s["before_has_errors"] = bp_score

    # 3. http_codes_after: every anomalous code from gt must drop to threshold
    ap_score = 0.0
    ap = rd / "http_codes_after.txt"
    cnt_413_after = cnt_504_after = -1
    if ap.exists():
        try:
            txt = ap.read_text()
            cnt_413_after = cnt_504_after = 0
            for line in txt.splitlines():
                m = re.search(r"(\d+)\D+(\d{3})", line.strip())
                if m:
                    cnt, code = int(m.group(1)), m.group(2)
                    if code == "413": cnt_413_after += cnt
                    if code == "504": cnt_504_after += cnt
            if cnt_413_after <= max_413 and cnt_504_after <= max_504:
                ap_score = 1.0
            elif cnt_413_after <= max_413 + 2 and cnt_504_after <= max_504 + 3:
                ap_score = 0.5
        except Exception: pass
    s["after_clean"] = ap_score

    # 4. fix_plan.md must reference >= fix_min_hits private nginx directives
    fp_score = 0.0
    fp_hits = 0
    fp = rd / "fix_plan.md"
    if fp.exists():
        try:
            txt = fp.read_text()
            fp_hits = sum(1 for k in fix_kws if k in txt)
            fp_score = min(1.0, fp_hits / max(1, fix_min_hits))
        except Exception: pass
    s["fix_plan_keywords"] = fp_score

    # 5. HTML reports
    s["goaccess_html_before"] = 1.0 if (rd / "access_report_before.html").exists() else 0.0
    s["goaccess_html_after"] = 1.0 if (rd / "access_report_after.html").exists() else 0.0

    # 6. GUI screenshots — existence + size lower bound (filter out placeholders)
    gui_shots = ["view_goaccess_overview.png","view_goaccess_http_codes.png",
                 "view_goaccess_404_404.png","view_goaccess_time_series.png",
                 "view_goaccess_after_fix.png"]
    valid_shots = []
    for n in gui_shots:
        p = rd / n
        if p.exists():
            try:
                if p.stat().st_size >= min_shot_bytes:
                    valid_shots.append(p)
            except Exception: pass
    s["gui_screenshots_count"] = len(valid_shots) / len(gui_shots)
    has_gui = len(valid_shots) >= 4

    # 6b. OCR over goaccess UI keywords
    ocr_available = True
    try:
        import pytesseract
        from PIL import Image
        kws_any = ["GoAccess","Hits","Visitors","HTTP","Status","Codes","Requests","Time","Bandwidth"]
        ocr_hits = 0
        for p in valid_shots:
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k.lower() in tx.lower() for k in kws_any): ocr_hits += 1
            except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
    except Exception:
        ocr_available = False
        s["gui_screenshots_ocr"] = 0.0

    # 7. nginx_report.md
    rp_score = 0.0
    rp = rd / "nginx_report.md"
    if rp.exists():
        try:
            txt = rp.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            rp_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["nginx_report"] = rp_score

    # 8. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_available = bool(vlm_score_rubric) and (rd / "view_goaccess_overview.png").exists()
    rubric = {
        "vlm_goaccess_panels": "GoAccess HTML 报告含多个 panel(Hits / HTTP Codes / Time)",
        "vlm_http_codes_chart": "HTTP Status Codes panel 显示明显的异常状态码占比",
        "vlm_time_series": "时间序列图能看到错误 spike",
        "vlm_after_clean": "after_fix 截图明显比 before 错误条少",
    }
    if vlm_available:
        try:
            imgs = [str(rd / n) for n in ["view_goaccess_overview.png","view_goaccess_http_codes.png","view_goaccess_after_fix.png"] if (rd / n).exists()]
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 GoAccess HTML dashboard 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            vlm_available = False
            for k in rubric: s[k] = 0.0
    else:
        for k in rubric: s[k] = 0.0

    # 9. GUI real interaction — md5 diversity of trajectory frames
    traj_paths = [rd / n for n in gui_shots]
    present_paths = [p for p in traj_paths if p.exists()]
    if len(present_paths) >= 2:
        _hashes = set(hashlib.md5(p.read_bytes()).hexdigest() for p in present_paths)
        gui_diversity = (len(_hashes) / max(1, len(present_paths))) * (len(present_paths) / len(traj_paths))
    else:
        gui_diversity = 0.0
    s["gui_real_interaction"] = 1.0 if gui_diversity >= min_diversity else (0.5 if gui_diversity >= 0.6 else 0.0)

    # 10. Browser / GoAccess chrome OCR
    chrome_kws = ["GoAccess","Visitors","Top URLs","Requested Files","Static Requests",
                  "Not Found","HTTP Status Codes","Time Distribution","Hosts",
                  "DevTools","Inspector","localhost","file://","Firefox","Chromium"]
    chrome_hits = 0
    if ocr_available:
        try:
            import pytesseract as _pt
            from PIL import Image as _Img
            for p in traj_paths:
                if p.exists():
                    try:
                        tx = _pt.image_to_string(_Img.open(p))
                        if any(k.lower() in tx.lower() for k in chrome_kws):
                            chrome_hits += 1
                    except Exception: pass
            s["gui_chrome_ocr"] = chrome_hits / len(traj_paths)
        except Exception:
            s["gui_chrome_ocr"] = 0.0
    else:
        s["gui_chrome_ocr"] = 0.0

    # 11. Window geometry: real GUI screenshots ≥ private min resolution
    geo_hits = 0
    try:
        from PIL import Image as _Img2
        for p in traj_paths:
            if p.exists():
                try:
                    w, h = _Img2.open(p).size
                    if w >= min_w and h >= min_h:
                        geo_hits += 1
                except Exception: pass
        s["gui_window_geometry"] = geo_hits / len(traj_paths)
    except Exception:
        s["gui_window_geometry"] = 0.0

    # ===== Weighted scoring: core 60% / gui 30% / aux 10% =====
    core_keys = ["cli_artifacts","before_has_errors","after_clean",
                 "fix_plan_keywords","goaccess_html_before","goaccess_html_after",
                 "nginx_report"]
    gui_keys  = ["gui_screenshots_count","gui_screenshots_ocr","gui_real_interaction",
                 "gui_chrome_ocr","gui_window_geometry"]
    aux_keys  = list(rubric.keys())  # VLM rubric

    def _avg(keys):
        vals = [float(s.get(k, 0.0)) for k in keys]
        return sum(vals) / len(vals) if vals else 0.0

    core_score = _avg(core_keys)
    gui_score  = _avg(gui_keys)
    aux_score  = _avg(aux_keys)
    s["_core_score"] = round(core_score, 4)
    s["_gui_score"]  = round(gui_score, 4)
    s["_aux_score"]  = round(aux_score, 4)

    base = 0.6 * core_score + 0.3 * gui_score + 0.1 * aux_score

    # ===== Hard gates (multi-layer, prevent "all-zero → 0.55") =====
    # H0: anti-all-zero — if core deliverables totally missing, hard cap 0.10
    hard_signals = sum(1 for k in ("cli_artifacts","before_has_errors","after_clean",
                                    "fix_plan_keywords","nginx_report")
                       if float(s.get(k, 0.0)) > 0.0)
    if hard_signals == 0:
        base = min(base, 0.10)
    elif hard_signals <= 2:
        base = min(base, 0.30)

    if not has_cli:                   base = min(base, 0.25)
    if not has_gui:                   base = min(base, 0.30)

    # Core deliverable gates
    if s["fix_plan_keywords"]   < 1.0:  base = min(base, 0.55)
    if s["fix_plan_keywords"]   < 0.66: base = min(base, 0.40)
    if s["after_clean"]         < 1.0:  base = min(base, 0.55)
    if s["after_clean"]         < 0.5:  base = min(base, 0.40)
    if s["before_has_errors"]   < 1.0:  base = min(base, 0.60)
    if s["before_has_errors"]   < 0.5:  base = min(base, 0.45)
    if s["nginx_report"]        < 0.75: base = min(base, 0.55)

    # GUI real-interaction gates (multi-layer)
    if s.get("gui_real_interaction", 0.0) < 0.5:  base = min(base, 0.40)
    if s.get("gui_chrome_ocr", 0.0) < 0.5 and s.get("gui_window_geometry", 0.0) < 0.6:
        base = min(base, 0.40)
    if s.get("gui_screenshots_count", 0.0) < 0.6: base = min(base, 0.45)

    # VLM unavailable / failed → cap (prevents no-VLM full marks)
    if not vlm_available or aux_score == 0.0:
        base = min(base, vlm_cap)
    elif aux_score < 0.4:
        base = min(base, 0.55)

    s["overall_score"] = round(base, 4)
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
