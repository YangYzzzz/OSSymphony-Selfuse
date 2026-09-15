# Auto-generated from WeaveBench task DSK_task_12_dbus_service_introspect_repair.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-axis grader for the D-Bus service repair task."""
    import json, re, subprocess
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt = Path("/opt/dsk12_gt") if Path("/opt/dsk12_gt/expected.json").exists() \
         else (Path("/tmp_workspace/gt") if Path("/tmp_workspace/gt").exists() \
               else Path("/tmp_workspace/setup/gt"))
    expected = {}
    try:
        expected = json.loads((gt / "expected.json").read_text())
    except Exception:
        pass
    s = {}

    # 1) introspect.xml present + mentions Counter iface
    ix = rd / "introspect.xml"; iface_ok = False
    if ix.exists():
        try:
            txt = ix.read_text(errors="replace")
            iface_ok = "org.eyeson.MetricsBox.Counter" in txt and "Echo" in txt
        except Exception: pass
    s["cli_introspect"] = 1.0 if iface_ok else (0.4 if ix.exists() else 0.0)

    # 2) dbus_monitor.log >=30 lines + at least one error frame
    dm = rd / "dbus_monitor.log"; dm_lines, dm_err, dm_real = 0, False, False
    try:
        unique = subprocess.run(["busctl","--user","--no-pager","status","org.eyeson.MetricsBox"],
                                capture_output=True, text=True, timeout=10).stdout
    except Exception:
        unique = ""
    uniq_match = re.search(r":\d+\.\d+", unique)
    if dm.exists():
        try:
            t = dm.read_text(errors="replace")
            dm_lines = sum(1 for ln in t.splitlines() if ln.strip())
            dm_err = bool(re.search(r"error_name=org\.freedesktop\.DBus\.Error\.InvalidArgs", t))
            dm_real = bool(re.search(r"path=/org/eyeson/MetricsBox", t)) and \
                      (uniq_match is None or uniq_match.group(0) in t)
        except Exception: pass
    min_lines = expected.get("min_dbus_monitor_lines", 30)
    s["cli_monitor_lines"] = 1.0 if (dm_lines >= min_lines and dm_err and dm_real) else \
                              (0.5 if dm_lines >= min_lines and dm_real else 0.2 if dm_lines >= min_lines else 0.0)

    # 3) signal_trace.log non-empty + topical
    st = rd / "signal_trace.log"; st_ok = False
    if st.exists():
        try:
            t = st.read_text(errors="replace")
            st_ok = ("MetricUpdated" in t) and bool(re.search(r"path=/org/eyeson/MetricsBox(/Legacy)?", t)) and len(t) > 400
        except Exception: pass
    s["cli_signal_trace"] = 1.0 if st_ok else (0.4 if st.exists() else 0.0)

    # 4) findings.json: >=3 entries spanning 3 root-cause categories
    fj = rd / "findings.json"; entries = []
    if fj.exists():
        try:
            entries = json.loads(fj.read_text())
            if isinstance(entries, dict): entries = [entries]
        except Exception: entries = []
    s["findings_count"] = 1.0 if len(entries) >= 3 else len(entries)/3.0
    cat_keys = {
        "signature": [("invalidargs","typeerror"), ("isinstance","list"), ("echo","signature")],
        "signal":    [("metricupdated","legacy"), ("publish_object","path"), ("wrong path","signal")],
        "policy":    [("allow_secret","getsecret"), ("accessdenied","os.environ"), ("permission","env")],
    }
    def _hits(blob, pairs):
        return any(all(tok in blob for tok in pair) for pair in pairs)
    cats_hit = set()
    for e in entries:
        blob = json.dumps(e, ensure_ascii=False).lower()
        for c, pairs in cat_keys.items():
            if _hits(blob, pairs): cats_hit.add(c)
    s["findings_categories"] = len(cats_hit)/3.0
    ev_ok = sum(1 for e in entries
                if isinstance(e, dict)
                and e.get("evidence_cli") and e.get("evidence_gui")
                and e.get("root_cause") and e.get("fix"))
    s["findings_evidence_links"] = 1.0 if ev_ok >= 3 else ev_ok/3.0

    # 5) GUI screenshots: 5 expected, OCR for keywords
    gui_shots = expected.get("expected_screens", [
        "view_dfeet_introspection_tree.png",
        "view_dfeet_method_call_dialog.png",
        "view_dbus_monitor_terminal.png",
        "view_systemd_unit_status.png",
        "view_postrepair_probe.png",
    ])
    present = [n for n in gui_shots if (rd/n).exists()]
    s["gui_screens_count"] = len(present)/float(len(gui_shots))
    ocr_kws = {
        "view_dfeet_introspection_tree.png": ["MetricsBox", "Counter", "Echo", "Tick"],
        "view_dfeet_method_call_dialog.png": ["Execute", "Method", "Echo", "msg"],
        "view_dbus_monitor_terminal.png":    ["method", "signal", "sender", "path"],
        "view_systemd_unit_status.png":      ["metricsbox", "python", "CPU", "MEM", "PID"],
        "view_postrepair_probe.png":         ["Echo", "Result", "reply", "hi"],
    }
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        for n in present:
            try:
                tx = pytesseract.image_to_string(Image.open(rd/n))
                if any(k.lower() in tx.lower() for k in ocr_kws.get(n, [])):
                    ocr_hits += 1
            except Exception: pass
        s["gui_screens_ocr"] = ocr_hits/float(len(gui_shots))
    except Exception:
        s["gui_screens_ocr"] = 0.5 * (len(present)/float(len(gui_shots)))

    # 6) repair.patch unified diff present + touches all 3 themes
    rp = rd / "repair.patch"; touch3 = 0; patch_applies = False
    src = Path("/tmp_workspace/metricsbox/metricsbox_service.py")
    if rp.exists():
        try:
            txt = rp.read_text(errors="replace")
            patch_present = txt.lstrip().startswith(("---","diff ","@@"))
            if src.exists():
                chk = subprocess.run(["patch","--dry-run","-p0","-f","-d","/", "-i", str(rp)],
                                     capture_output=True, text=True, timeout=15)
                patch_applies = (chk.returncode == 0)
            s["repair_patch_present"] = 1.0 if (patch_present and patch_applies) else (0.3 if patch_present else 0.0)
            if any(k in txt for k in ["Echo", "isinstance", "list", "msg"]):
                touch3 += 1
            if any(k in txt for k in ["publish_object", "MetricUpdated",
                                      "Legacy", "/org/eyeson/MetricsBox"]):
                touch3 += 1
            if any(k in txt for k in ["ALLOW_SECRET", "GetSecret",
                                      "PermissionError", "AccessDenied",
                                      "os.environ"]):
                touch3 += 1
        except Exception:
            s["repair_patch_present"] = 0.2
    else:
        s["repair_patch_present"] = 0.0
    s["repair_patch_touches_3"] = touch3/3.0

    # 7) systemd unit status active
    try:
        live = subprocess.run(["systemctl","--user","is-active","metricsbox.service"],
                              capture_output=True, text=True, timeout=10)
        on_bus = subprocess.run(["busctl","--user","--no-pager","list"],
                                capture_output=True, text=True, timeout=10)
        active = (live.stdout.strip()=="active") and ("org.eyeson.MetricsBox" in on_bus.stdout)
        (rd / "unit_status_after.txt").write_text(live.stdout + on_bus.stdout)
    except Exception:
        active = False
    s["unit_active"] = 1.0 if active else 0.0

    # 8) probe_after: all three steps ok=True + signal received
    pa = rd / "client_probe_after.log"
    try:
        subprocess.run(["python3","/tmp_workspace/metricsbox/client_probe.py",
                        "--echo","hi","--tick","3","--get-secret","--listen-secs","4"],
                       capture_output=True, timeout=30)
        src_log = Path("/tmp_workspace/results/client_probe.log")
        if src_log.exists(): pa.write_text(src_log.read_text())
    except Exception: pass
    echo_ok = tick_ok = secret_ok = False; sig_recv = False
    if pa.exists():
        try:
            for ln in pa.read_text(errors="replace").splitlines():
                if not ln.strip(): continue
                rec = json.loads(ln)
                if rec.get("step") == "echo" and rec.get("ok"): echo_ok = True
                if rec.get("step") == "tick" and rec.get("ok") and rec.get("new_total")==3: tick_ok = True
                if rec.get("step") == "get_secret" and rec.get("ok"): secret_ok = True
                if rec.get("step") == "signal_listen" and rec.get("received"):
                    sig_recv = True
        except Exception: pass
    probe_score = sum([echo_ok, tick_ok, secret_ok])/3.0
    s["probe_after_all_ok"] = probe_score
    s["signal_after_received"] = 1.0 if sig_recv else 0.0

    # 9) report.md ≥60 lines + 4 sections
    rm = rd / "report.md"; n_lines = 0; sec_hits = 0
    if rm.exists():
        try:
            txt = rm.read_text(errors="replace")
            n_lines = len([1 for ln in txt.splitlines() if ln.strip()])
            for kw in ["症状", "取证", "根因", "修复",
                       "symptom", "evidence", "root cause", "fix"]:
                if kw.lower() in txt.lower(): sec_hits += 1
        except Exception: pass
    s["report_present"] = 1.0 if n_lines >= 60 else n_lines/60.0
    s["report_sections"] = 1.0 if sec_hits >= 4 else sec_hits/4.0

    # 10) cross-channel evidence: at least one CLI artifact AND one GUI shot
    cli_evidence = bool(ix.exists() or dm.exists() or st.exists() or rp.exists())
    gui_evidence = len(present) >= 1
    s["cross_channel_evidence"] = 1.0 if (cli_evidence and gui_evidence) else 0.0

    # 11) VLM rubric on the post-repair screenshot
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd/n) for n in [
        "view_postrepair_probe.png",
        "view_dfeet_method_call_dialog.png",
        "view_dfeet_introspection_tree.png",
    ] if (rd/n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_dfeet_tree_visible": "截图含 D-Bus 调试器左侧 service tree 或方法 / 信号节点",
            "vlm_method_call_result": "截图含一次 D-Bus Execute Method 的结果或错误条",
            "vlm_no_red_error_after_repair": "post-repair 截图未显示明显红色 error / Exception",
            "vlm_terminal_or_gui_consistent": "GUI 截图整洁、文字可读、无明显裁切",
        }
        try:
            strict_instr = ("Score 1.0 ONLY if the image is a real screenshot of a Linux desktop "
                            "showing a D-Bus debugger / dbus-monitor / systemd UI with native window chrome and "
                            "anti-aliased fonts. Score 0.0 for hand-drawn / Pillow / GTK-canvas mockups, "
                            "ASCII art, or solid-colour rectangles with pasted text.")
            vlm = vlm_score_rubric(vlm_imgs[:3], rubric, instruction=strict_instr)
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        s["vlm_dfeet_tree_visible"] = 0.5
        s["vlm_method_call_result"] = 0.5
        s["vlm_no_red_error_after_repair"] = 0.5
        s["vlm_terminal_or_gui_consistent"] = 0.5

    # base score
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums)/len(nums) if nums else 0.0

    # Hard gates
    if not (ix.exists() or dm.exists()):       base = min(base, 0.4)
    # GUI hard-cap removed: rely on per-shot VLM/OCR sub-scores instead.
    vlm_avg = (s["vlm_dfeet_tree_visible"] + s["vlm_method_call_result"] +
               s["vlm_no_red_error_after_repair"] +
               s["vlm_terminal_or_gui_consistent"]) / 4.0
    if vlm_score_rubric is not None and vlm_imgs and vlm_avg < 0.6:
        base = min(base, 0.45)
    if ocr_hits < 3:                           base = min(base, 0.55)
    if probe_score < 1.0:                      base = min(base, 0.55)
    if not sig_recv:                           base = min(base, 0.6)
    try:
        live_xml = subprocess.run(["busctl","--user","--xml-interface","introspect",
                                   "org.eyeson.MetricsBox","/org/eyeson/MetricsBox"],
                                  capture_output=True, text=True, timeout=10).stdout
    except Exception:
        live_xml = ""
    contract_live = ("org.eyeson.MetricsBox.Counter" in live_xml and
                     'name="Echo"' in live_xml and 'name="MetricUpdated"' in live_xml)
    s["contract_live"] = 1.0 if contract_live else 0.0
    if not contract_live: base = min(base, 0.45)

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
