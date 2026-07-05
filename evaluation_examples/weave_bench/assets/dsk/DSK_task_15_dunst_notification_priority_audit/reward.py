# Auto-generated from WeaveBench task DSK_task_15_dunst_notification_priority_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """dunst notification audit grader. Cross-channel: CLI dbus-monitor +
    dunstrc patch + GUI rendered stack screenshots + GUI button click via
    D-Bus ActionInvoked. 13 sub-scores + 4 hard gates."""
    import json, re
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/opt/dsk15_gt")
    s = {}

    def _read(p, default=""):
        try: return p.read_text(errors="ignore")
        except Exception: return default

    def _ocr(p):
        try:
            from PIL import Image
            import pytesseract
            return pytesseract.image_to_string(Image.open(p))
        except Exception:
            return ""

    gt = {}
    if (gt_dir / "manifest.json").exists():
        try: gt = json.loads((gt_dir / "manifest.json").read_text())
        except Exception: pass
    expected_section = gt.get("broken_section", "urgency_critical")
    expected_keys    = set(gt.get("broken_keys", ["timeout"]))
    expected_visible = gt.get("expected_visible_after",
                              {"low": 0, "normal": 5, "critical": 3})
    min_visible_critical = int(expected_visible.get("critical", 1))

    # 1. before backup + status
    s["before_backup"] = 1.0 if ((rd/"dunstrc_before.conf").exists()
        and (rd/"dunst_status_before.txt").exists()) else 0.0

    # 2. dbus-monitor log
    dlog = _read(rd/"dbus_monitor.log")
    import re as _re
    notify_lines = len(_re.findall(r"^method call .*interface=org\.freedesktop\.Notifications.*member=Notify\b", dlog, _re.M))
    has_serial = bool(_re.search(r"\bserial=\d+\b", dlog)) and bool(_re.search(r"\bsender=:[0-9.]+\b", dlog))
    s["dbus_monitor_notify"] = 1.0 if (notify_lines >= 12 and has_serial) else min(1.0, notify_lines/24.0)

    # 3. burst_before_manifest
    bmb = []
    try: bmb = json.loads((rd/"burst_before_manifest.json").read_text())
    except Exception: pass
    s["burst_before"] = 1.0 if (isinstance(bmb, list) and len(bmb) >= 12) \
                        else (len(bmb)/12.0 if isinstance(bmb, list) else 0.0)

    # 4. before screenshot OCR
    p_b = rd / "view_dunst_stack_before.png"
    ocr_b = _ocr(p_b) if p_b.exists() else ""
    appname_kw = ["Slack", "PagerDuty", "icinga", "Backup", "slack",
                  "pagerduty", "Icinga"]
    hits_b = sum(1 for k in ["Slack","PagerDuty","icinga","Backup"] if k.lower() in ocr_b.lower())
    s["screenshot_before"] = 1.0 if (p_b.exists() and hits_b >= 2) else \
                             (0.5 if (p_b.exists() and hits_b == 1) else 0.0)

    # 5. dunst history before
    dhb = _read(rd/"dunst_history_before.json")
    s["history_before"] = 1.0 if (dhb and len(dhb) > 50) else 0.0

    # 6. diagnosis.json
    diag = {}
    try: diag = json.loads((rd/"diagnosis.json").read_text())
    except Exception: pass
    diag_score = 0.0
    if diag:
        if diag.get("broken_section") == expected_section: diag_score += 0.3
        bk = set(map(str.lower, diag.get("broken_keys", []) or []))
        exp_low = {k.lower() for k in expected_keys}
        if exp_low.issubset(bk): diag_score += 0.4
        elif exp_low & bk:       diag_score += 0.15
        if str(diag.get("symptom","")).lower().count("ignore") and "timeout" in str(diag.get("symptom","")).lower(): diag_score += 0.1
        ea = diag.get("expected_after", {}) or {}
        if all(k in ea for k in ["low","normal","critical"]): diag_score += 0.2
    s["diagnosis"] = round(min(1.0, diag_score), 3)

    # 7. dunstrc.fixed
    fx = _read(rd/"dunstrc.fixed")
    fx_ok = bool(fx)
    if fx_ok:
        # heuristic: critical timeout != 1 ; has a red-ish background under
        # urgency_critical ; doesn't keep low at timeout=0
        critical_block = re.search(
            r"\[urgency_critical\]([^\[]*)", fx, re.IGNORECASE)
        cb = critical_block.group(1) if critical_block else ""
        crit_timeout_ok = not re.search(r"^\s*timeout\s*=\s*1\s*$", cb, re.M)
        crit_red = bool(re.search(r"background\s*=\s*\"#[89a-fA-F][0-9a-fA-F]{2}",
                                   cb)) or "#900" in cb or "#a00" in cb.lower() \
                                       or "#b00" in cb.lower() or "#f00" in cb
        low_block = re.search(r"\[urgency_low\]([^\[]*)", fx, re.IGNORECASE)
        lb = low_block.group(1) if low_block else ""
        low_timeout_ok = not re.search(r"^\s*timeout\s*=\s*0\s*$", lb, re.M)
        # ignore_* filter sections should be removed or empty
        no_bad_ignore = "[ignore_" not in fx.lower()
        crit_no_ignore_kv = not re.search(r"^\s*ignore\s*=\s*(true|yes|1)\s*$", cb, re.M|re.I)
        crit_timeout_pos = bool(re.search(r"^\s*timeout\s*=\s*([2-9]|\d{2,})\s*$", cb, re.M))
        fx_ok = crit_timeout_ok and crit_timeout_pos and crit_red and low_timeout_ok and no_bad_ignore and crit_no_ignore_kv
    s["dunstrc_fixed"] = 1.0 if fx_ok else 0.0

    # 8. burst_after manifest
    bma = []
    try: bma = json.loads((rd/"burst_after_manifest.json").read_text())
    except Exception: pass
    s["burst_after"] = 1.0 if (isinstance(bma, list) and len(bma) >= 12) \
                        else (len(bma)/12.0 if isinstance(bma, list) else 0.0)

    # 9. after screenshot OCR for critical-ish words
    p_a = rd / "view_dunst_stack_after.png"
    ocr_a = _ocr(p_a) if p_a.exists() else ""
    crit_kw = ["PagerDuty", "icinga", "Icinga", "CRITICAL", "Critical",
               "critical", "ALERT", "Alert"]
    crit_hits_a = sum(1 for k in ["PagerDuty","icinga","CRITICAL","ALERT"] if k.lower() in ocr_a.lower())
    app_hits_a = sum(1 for k in ["Slack","PagerDuty","icinga","Backup"] if k.lower() in ocr_a.lower())
    s["screenshot_after"] = 1.0 if (p_a.exists() and crit_hits_a >= 1 and app_hits_a >= 1) else \
                             (0.5 if (p_a.exists() and (crit_hits_a >= 1 or app_hits_a >= 1)) else 0.0)

    # 10. action_invoked.json
    ai = {}
    try: ai = json.loads((rd/"action_invoked.json").read_text())
    except Exception: pass
    s["action_invoked"] = 1.0 if (isinstance(ai, dict)
        and "notification_id" in ai and "action_key" in ai
        and ai.get("action_key")) else 0.0

    # 11. history_after critical count
    crit_after = 0
    dha = _read(rd/"dunst_history_after.json")
    if dha:
        try:
            d = json.loads(dha)
            # dunstctl history returns {"data":[[ {...}, {...}, ... ]]}
            entries = []
            if isinstance(d, dict) and "data" in d:
                for chunk in d["data"]:
                    if isinstance(chunk, list): entries.extend(chunk)
            elif isinstance(d, list):
                entries = d
            for e in entries:
                u = e.get("urgency", {})
                # dunstctl format: {"data": "Critical"} or just str
                if isinstance(u, dict): u = u.get("data", "")
                if isinstance(u, str) and u.lower().startswith("crit"):
                    crit_after += 1
        except Exception:
            crit_after = 0  # require a parseable dunstctl history JSON, no string fallback
    s["history_after_critical"] = 1.0 if crit_after >= min_visible_critical \
        else (crit_after / max(1, min_visible_critical))

    # 12. summary.md
    sm = _read(rd/"summary.md")
    s["summary_md"] = 1.0 if (sm and len(sm) >= 200
        and "before" in sm.lower() and "after" in sm.lower()) else \
        (0.5 if sm and len(sm) >= 100 else 0.0)

    # cross-channel evidence
    ids_b  = {str(e.get("id")) for e in (bmb if isinstance(bmb,list) else []) if isinstance(e,dict)}
    hist_ids = set(re.findall(r'"id"\s*:\s*\{?\s*"?data"?\s*:?\s*(\d+)', dhb or "")) | set(re.findall(r'"id"\s*:\s*(\d+)', dhb or ""))
    linked = bool(ids_b) and len(ids_b & hist_ids) >= 6
    cli_ev = (rd/"dbus_monitor.log").exists() and (rd/"dunstrc.fixed").exists() and linked
    gui_ev = p_b.exists() and p_a.exists()
    s["cross_channel_evidence"] = 1.0 if (cli_ev and gui_ev) else 0.0

    # VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    shots = [str(p) for p in [p_b, p_a] if p.exists()]
    if vlm_score_rubric and shots:
        rubric = {
            "vlm_real_stack": "图像里能看到真实桌面上叠层渲染的若干通知（不是终端文字）",
            "vlm_color_visible": "after 截图里的 critical 通知背景明显偏红/偏暖色",
            "vlm_app_names_legible": "通知里 app_name / summary 文本可读",
            "vlm_no_overlap_truncate": "叠层布局清晰、未被裁切或过度遮挡",
        }
        try:
            v = vlm_score_rubric(shots[:2], rubric,
                                 instruction="评估 dunst 通知叠层渲染质量。")
            for k in rubric: s[k] = float(v.get(k, 0.0))
            s["judge_method"] = v.get("judge_method", "ok")
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_real_stack", "vlm_color_visible",
                  "vlm_app_names_legible", "vlm_no_overlap_truncate"]:
            s[k] = 0.5

    nums = [v for k, v in s.items()
            if isinstance(v, (int, float)) and k != "judge_method"]
    base = sum(nums) / len(nums) if nums else 0.0

    # Hard gates
    if not cli_ev:                                base = min(base, 0.40)
    # GUI hard-cap removed: rely on per-shot VLM/OCR sub-scores instead.
    vlm_avg = sum(s.get(k, 0.0) for k in ["vlm_real_stack",
                                          "vlm_color_visible",
                                          "vlm_app_names_legible",
                                          "vlm_no_overlap_truncate"]) / 4.0
    if vlm_score_rubric is not None and shots and vlm_avg < 0.6:
        base = min(base, 0.60)
    if s["diagnosis"] < 0.5:                      base = min(base, 0.55)
    if s["dunstrc_fixed"] < 1.0:                  base = min(base, 0.55)
    if s["action_invoked"] < 1.0:                 base = min(base, 0.65)
    if s["history_after_critical"] < 1.0:         base = min(base, 0.60)

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
