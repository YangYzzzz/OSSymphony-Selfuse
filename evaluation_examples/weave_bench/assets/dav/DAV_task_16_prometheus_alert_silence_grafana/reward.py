# Auto-generated from WeaveBench task DAV_task_16_prometheus_alert_silence_grafana.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DAV_task_16 grader: alert silence + rule patch + cross-channel evidence."""
    import json, os, re, subprocess
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    # Read GT from the root-only path the warmup moved expected.json to
    # (kept off the agent-visible /tmp_workspace/gt to prevent answer
    # leakage). Fall back to /tmp_workspace/gt for legacy mounts.
    gt_dir = Path("/opt/dav16_gt") if Path("/opt/dav16_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    s = {}
    expected = {}
    if (gt_dir / "expected.json").exists():
        try: expected = json.loads((gt_dir / "expected.json").read_text())
        except Exception: expected = {}
    noisy = expected.get("noisy_alert_to_silence", "HighErrorRate")
    patch_target = expected.get("rule_to_patch_alertname", "JvmOldGcStorm")
    rate_kw = expected.get("patched_expr_must_contain_any", ["rate(", "irate(", "increase("])

    # 1. firing_alerts.json
    fa = rd / "firing_alerts.json"
    s["firing_alerts_present"] = 1.0 if fa.exists() else 0.0
    firing_ok = 0.0
    if fa.exists():
        try:
            d = json.loads(fa.read_text())
            arr = d.get("firing") if isinstance(d, dict) else d
            if isinstance(arr, list) and len(arr) >= expected.get("expected_firing_alert_count_min", 2):
                names = {(a.get("name") or a.get("alertname") or "") for a in arr if isinstance(a, dict)}
                hits = sum(1 for tgt in (noisy, patch_target) if any(tgt in n for n in names))
                firing_ok = 1.0 if hits == 2 else (0.5 if hits == 1 else 0.0)
        except Exception:
            pass
    s["firing_alerts_schema"] = firing_ok

    # 2. promtool check before/after
    s["promtool_check_before"] = 1.0 if (rd / "promtool_check_before.txt").exists() and (rd / "promtool_check_before.txt").stat().st_size > 0 else 0.0
    test_after = rd / "promtool_test_after.txt"
    test_after_ok = 0.0
    if test_after.exists():
        txt = test_after.read_text(errors="ignore")
        if "SUCCESS" in txt or "PASS" in txt or re.search(r"\b0 failures?\b|Unit Testing.*SUCCESS", txt, re.I):
            test_after_ok = 1.0
        elif len(txt) > 20:
            test_after_ok = 0.4
    s["promtool_test_after"] = test_after_ok

    # 3. silences.json structure + matcher + duration
    sil = rd / "silences.json"
    sil_ok = 0.0
    duration_min = 0.0
    sil_matcher_ok = 0.0
    if sil.exists():
        try:
            d = json.loads(sil.read_text())
            items = d if isinstance(d, list) else (d.get("data") or d.get("silences") or [d])
            for it in items:
                ms = it.get("matchers", [])
                names = {m.get("name", ""): m.get("value", "") for m in ms if isinstance(m, dict)}
                if names.get("alertname") == noisy and not any(m.get("isRegex") for m in ms):
                    sil_matcher_ok = 1.0
                    # parse start/end ISO
                    try:
                        from datetime import datetime
                        def _p(x): return datetime.fromisoformat(x.replace("Z", "+00:00"))
                        dur = (_p(it["endsAt"]) - _p(it["startsAt"])).total_seconds()
                        if expected.get("silence_min_duration_seconds", 6900) <= dur <= expected.get("silence_max_duration_seconds", 8100):
                            duration_min = 1.0
                        elif dur > 1800:
                            duration_min = 0.5
                    except Exception:
                        duration_min = 0.3
                    break
            sil_ok = 1.0
        except Exception:
            pass
    s["silences_present"] = sil_ok
    s["silence_matcher_correct"] = sil_matcher_ok
    s["silence_duration_in_range"] = duration_min

    # 4. amtool silences output
    am = rd / "amtool_silences.txt"
    am_txt = am.read_text(errors="ignore") if am.exists() else ""
    s["amtool_evidence"] = 1.0 if (noisy in am_txt and re.search(r"(ID|Matchers|Expires)", am_txt)) else 0.0

    # 5. tcpdump / webhook tail — silenced alert name should NOT appear
    captured_text = ""
    for n in ("webhook_after_silence.txt", "webhook_tail.log"):
        p = rd / n
        if p.exists():
            captured_text += "\n" + p.read_text(errors="ignore")
    pcap = rd / "webhook_after_silence.pcap"; pcap_strings = ""
    if pcap.exists() and pcap.stat().st_size > 1024:
        try:
            pcap_strings = subprocess.run(["strings", str(pcap)], capture_output=True, text=True, timeout=15).stdout
        except Exception:
            pass
        captured_text += "\n" + pcap_strings
    pcap_ok = bool(re.search(r"(POST\s+/|alertname|alertmanager)", pcap_strings))
    tail_ok = bool(re.search(r"(POST|alertname|status)", captured_text)) and len(captured_text) > 200
    has_capture = pcap_ok or tail_ok
    s["tcpdump_evidence_present"] = 1.0 if has_capture else 0.0
    if captured_text and has_capture:
        s["silence_effect_in_capture"] = 1.0 if (noisy not in captured_text and patch_target in captured_text) else 0.0
    else:
        s["silence_effect_in_capture"] = 0.0

    # 6. fixed_rules.yml — promtool check + expr contains rate( + threshold > 0.0X
    fr = rd / "fixed_rules.yml"
    fr_check = 0.0; fr_rate = 0.0; fr_thr = 0.0
    if fr.exists():
        try:
            r = subprocess.run(["promtool", "check", "rules", str(fr)], capture_output=True, text=True, timeout=20)
            if r.returncode == 0:
                fr_check = 1.0
        except Exception:
            fr_check = 0.0
        body = fr.read_text(errors="ignore")
        # find the patched alert block
        m = re.search(r"alert:\s*" + re.escape(patch_target) + r"\b[\s\S]{0,400}?expr:\s*([^\n]+)", body)
        if m:
            expr = m.group(1)
            if any(k in expr for k in rate_kw) and "jvm_old_gc_pause_seconds_total" in expr and re.search(r"\[\s*\d+[smh]\s*\]", expr):
                fr_rate = 1.0
            thr = re.search(r">\s*([0-9]*\.?[0-9]+)", expr)
            thr_min = expected.get("patched_expr_threshold_min", 0.01)
            if thr and thr_min <= float(thr.group(1)) <= 1.0:
                fr_thr = 1.0
    s["fixed_rules_promtool_ok"] = fr_check
    s["fixed_rules_uses_rate"] = fr_rate
    s["fixed_rules_threshold_ok"] = fr_thr

    # 7. GUI screenshots (5)
    gui_shots = [
        "view_alert_state_history.png",
        "view_silence_create.png",
        "view_annotate_panel.png",
        "view_edit_inspect.png",
        "view_alert_resolved.png",
    ]
    present = sum(1 for n in gui_shots if (rd / n).exists() and (rd / n).stat().st_size > 5000)
    s["gui_screenshots_count"] = present / len(gui_shots)
    # OCR keywords
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_alert_state_history.png": ["State", "history", "Alert", "Normal", "Firing"],
            "view_silence_create.png": ["Silence", "matcher", "Expires", "Active", "alertname"],
            "view_annotate_panel.png": ["Annotation", "annotation", "flap", "error", "ratio"],
            "view_edit_inspect.png": ["Edit", "Inspect", "Query", "Data", "Stats"],
            "view_alert_resolved.png": ["Silenced", "Normal", "Alert", "rules", "Alerting"],
        }
        for n, ks in kws.items():
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k in tx for k in ks): ocr_hits += 1
                except Exception:
                    pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
    except ImportError:
        s["gui_screenshots_ocr"] = 0.5

    # 8. postmortem
    pm = rd / "postmortem.md"
    pm_chars = 0; pm_kw_hits = 0
    if pm.exists():
        body = pm.read_text(errors="ignore")
        pm_chars = len(body)
        for kw in expected.get("expected_postmortem_keywords", []):
            if kw.lower() in body.lower():
                pm_kw_hits += 1
    s["postmortem_length"] = 1.0 if pm_chars >= 800 else (0.5 if pm_chars >= 400 else pm_chars / 800.0)
    s["postmortem_keywords"] = 1.0 if pm_kw_hits >= 4 else (0.5 if pm_kw_hits >= 3 else pm_kw_hits / 12.0)

    # 9. cross-channel evidence count
    cli_artifacts = ["firing_alerts.json", "promtool_check_before.txt", "promtool_test_after.txt",
                     "amtool_silences.txt", "silences.json", "fixed_rules.yml"]
    cli_n = sum(1 for n in cli_artifacts if (rd / n).exists())
    s["cli_artifact_count"] = cli_n / len(cli_artifacts)

    # 10. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd / n) for n in ("view_annotate_panel.png", "view_silence_create.png",
                                      "view_alert_state_history.png") if (rd / n).exists()]
    vlm_judge = 0.0
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_state_history_flap": "截图能看出 alert 状态在 firing 与 normal 之间反复切换（多段红绿条带）",
            "vlm_silence_active": "Silence 详情页显示 Active 状态、含 alertname matcher 和 ~2h 过期时间",
            "vlm_annotation_visible": "时序面板上能看到一段红色或彩色 region annotation 覆盖在 flap 区段",
            "vlm_panel_layout_clean": "面板布局整齐，坐标轴/legend 可读，没有重叠或截断",
        }
        vlm = vlm_score_rubric(vlm_imgs[:3], rubric, instruction="评估 SRE 值班员在 Grafana/Alertmanager 中的取证截图。")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
        vlm_judge = sum(s.get(k, 0.0) for k in rubric) / max(1, len(rubric))
    else:
        s["vlm_state_history_flap"] = 0.0
        s["vlm_silence_active"] = 0.0
        s["vlm_annotation_visible"] = 0.0
        s["vlm_panel_layout_clean"] = 0.0
        vlm_judge = 0.0

    nums = [v for k, v in s.items() if isinstance(v, (int, float)) and k != "judge_method"]
    base = sum(nums) / max(1, len(nums))

    # Hard gates
    has_cli = (s["cli_artifact_count"] >= 0.5) and (s["tcpdump_evidence_present"] >= 1.0 or s["amtool_evidence"] >= 1.0)
    if not has_cli: base = min(base, 0.4)
    # NOTE: We deliberately do NOT cap on missing GUI screenshots —
    # whether the agent invokes Grafana/Alertmanager UI tooling is not
    # a scoring axis. Missing PNGs already cost the corresponding
    # sub_scores (gui_screenshots_count / gui_screenshots_ocr /
    # 4 vlm_*); no additional hard cap is applied here.
    # VLM cap is only enforced when the helper actually ran. The
    # 0.0 fallback (HARDENING-3) intentionally drops the helper-missing
    # baseline, but we must NOT then cap on that 0.0 — the rubric was
    # never evaluated.
    if vlm_score_rubric is not None and vlm_judge < 0.6:
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
