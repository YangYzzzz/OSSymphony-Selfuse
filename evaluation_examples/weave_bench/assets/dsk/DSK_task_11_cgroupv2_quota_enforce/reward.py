# Auto-generated from WeaveBench task DSK_task_11_cgroupv2_quota_enforce.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """cgroup v2 quota tuning + OOM attribution grader.

    Sub-scores:
      - cgroup_inspect content (cgroup2 mount, controllers list)
      - lab.slice / trainjob.service evidence (file existence or systemctl_show)
      - memory.events oom_kill counters (first must be >=1, tuned delta == 0)
      - journalctl OOM line presence
      - quota_report.json schema + numeric/boolean correctness
      - report.md length + keyword coverage
      - 3 GUI screenshots present + OCR keyword hits
      - VLM rubric on the cgtop / system-monitor screenshots
    Hard gates: missing CLI cap 0.4; missing GUI cap 0.4; VLM<0.6 cap 0.6;
    no OOM in first run cap 0.65; report schema invalid cap 0.7.
    """
    import json, re, os
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/opt/dsk11_gt")
    if not gt_dir.exists():
        gt_dir = Path(workspace_path or "/tmp_workspace") / "gt"
    if not gt_dir.exists():
        gt_dir = Path("/tmp_workspace/gt")
    s = {}

    expected = {}
    ej = gt_dir / "expected.json"
    if ej.exists():
        try: expected = json.loads(ej.read_text())
        except Exception: expected = {}

    def read(p):
        try: return p.read_text(errors="ignore")
        except Exception: return ""

    # 1. cgroup_inspect content
    ci = read(rd / "cgroup_inspect.txt")
    has_v2_mount = bool(re.search(r"cgroup2\s+on\s+/sys/fs/cgroup", ci))
    ctrl_line = next((l for l in ci.splitlines() if re.fullmatch(r"\s*[a-z0-9_ ]+\s*", l) and "memory" in l and "cpu" in l), "")
    has_controllers = all(c in ctrl_line.split() for c in ("cpu","memory","io"))
    s["cgroup_inspect_v2"] = 1.0 if has_v2_mount else 0.0
    s["cgroup_inspect_controllers"] = 1.0 if has_controllers else 0.0

    # 2. systemctl_show files reference correct slice + unit
    sf1 = read(rd / "systemctl_show_first.txt")
    sft = read(rd / "systemctl_show_tuned.txt")
    def _mm_bytes(t):
        m = re.search(r"MemoryMax=(\d+)", t); return int(m.group(1)) if m else 0
    def _cq(t):
        m = re.search(r"CPUQuotaPerSecUSec=(\d+)ms", t); return int(m.group(1)) if m else -1
    ok1 = ("Slice=lab.slice" in sf1 and 250*1024*1024 <= _mm_bytes(sf1) <= 270*1024*1024 and 400 <= _cq(sf1) <= 600)
    okT = ("Slice=lab.slice" in sft and _mm_bytes(sft) >= 384*1024*1024 and _cq(sft) >= 750)
    s["systemctl_show_first"] = 1.0 if ok1 else (0.3 if sf1 else 0.0)
    s["systemctl_show_tuned"] = 1.0 if okT else (0.3 if sft else 0.0)

    # 3. memory.events oom_kill counters
    me1 = read(rd / "memory_events_first.txt")
    me_t = read(rd / "memory_events_tuned.txt")
    def parse_events(text):
        out = {}
        for line in text.splitlines():
            parts = line.strip().split()
            if len(parts) == 2:
                try: out[parts[0]] = int(parts[1])
                except ValueError: pass
        return out
    ev1 = parse_events(me1)
    evt = parse_events(me_t)
    oom_kill_first = ev1.get("oom_kill", 0); oom_kill_tuned = evt.get("oom_kill", 0)
    s["mem_events_first_oom"] = 1.0 if oom_kill_first >= 1 else 0.0
    s["mem_events_tuned_no_new_oom"] = 1.0 if (oom_kill_tuned >= oom_kill_first
                                                and oom_kill_tuned - oom_kill_first == 0
                                                and oom_kill_first >= 1) else 0.0

    # 4. journalctl OOM line content
    jo = read(rd / "journalctl_oom.txt")
    must = ("invoked oom-killer", "memory cgroup out of memory", "killed as a result of limit of")
    hard_hits = sum(1 for k in must if k in jo.lower())
    s["journalctl_oom_content"] = 1.0 if (len(jo) > 200 and hard_hits >= 2 and "trainjob" in jo.lower()) else (0.4 if hard_hits >= 1 else 0.0)

    return _finalise_cgroup(s, rd, expected, oom_kill_first, oom_kill_tuned)


def _finalise_cgroup(s, rd, expected, oom_kill_first, oom_kill_tuned):
    import json, re
    from pathlib import Path

    # 5. quota_report.json schema + values
    qr_path = rd / "quota_report.json"
    qr = {}
    if qr_path.exists():
        try: qr = json.loads(qr_path.read_text())
        except Exception: qr = {}
    schema_keys = {"slice","unit","first_run","tuned_run","evidence"}
    schema_ok = schema_keys.issubset(set(qr.keys()))
    s["report_schema"] = 1.0 if schema_ok else (len(schema_keys & set(qr.keys()))/len(schema_keys))

    fr = qr.get("first_run", {}) if isinstance(qr.get("first_run"), dict) else {}
    tr = qr.get("tuned_run", {}) if isinstance(qr.get("tuned_run"), dict) else {}

    s["report_slice"] = 1.0 if qr.get("slice") == expected.get("expected_slice","lab.slice") else 0.0
    s["report_unit"]  = 1.0 if qr.get("unit")  == expected.get("expected_unit","trainjob.service") else 0.0
    s["report_first_oom_true"] = 1.0 if fr.get("oom_killed") is True else 0.0
    s["report_tuned_oom_false"] = 1.0 if tr.get("oom_killed") is False else 0.0
    # tuned MemoryMax must be >= 384 MiB (allow either "512M" or numeric)
    def parse_mb(v):
        if isinstance(v,(int,float)): return v/1024/1024 if v > 1024*1024 else v
        if isinstance(v,str):
            m = re.match(r"^\s*(\d+(?:\.\d+)?)\s*([KMGTkmgt])?", v)
            if not m: return 0
            n = float(m.group(1)); u = (m.group(2) or "").upper()
            return n * {"":1/1024/1024,"K":1/1024,"M":1,"G":1024,"T":1024*1024}.get(u,1)
        return 0
    tuned_mb = parse_mb(tr.get("memory_max",""))
    s["report_tuned_memmax_ok"] = 1.0 if tuned_mb >= expected.get("memory_max_tuned_min_mb",384) else 0.0
    ts = read_safe(rd/"tuned_run.stdout")
    done_ok = bool(re.search(r"allocated=384MiB", ts)) and bool(re.search(r"\bdone\b", ts))
    s["report_tuned_exit_zero"] = 1.0 if (tr.get("exit_code") == 0 and done_ok and len(ts) > 200) else 0.0
    s["tuned_stdout_real"]      = 1.0 if done_ok else 0.0
    # numeric counters consistency
    s["report_oom_counter_match"] = 1.0 if (
        isinstance(fr.get("memory_events_oom_kill"),(int,float)) and
        fr.get("memory_events_oom_kill",0) >= 1 and
        tr.get("memory_events_oom_kill_delta", -1) == 0
    ) else 0.0

    # 6. report.md length + keywords
    rm = rd/"report.md"
    rt = rm.read_text(errors="ignore") if rm.exists() else ""
    s["report_md_length"]   = 1.0 if len(rt) >= 800 else len(rt)/800.0
    kw_needed = expected.get("expected_keys_in_report", [])
    if kw_needed:
        hits = sum(1 for k in kw_needed if k.lower() in rt.lower())
        need = max(6, len(kw_needed))
        s["report_md_keywords"] = 1.0 if hits >= need else hits/need
    else:
        s["report_md_keywords"] = 1.0 if len(rt) >= 400 else 0.0

    # 7. GUI screenshots present + OCR
    gui_shots = ["view_cgtop.png","view_system_monitor.png","view_journal_oom.png"]
    present = sum(1 for n in gui_shots if (rd/n).exists())
    s["gui_shots_present"] = present / len(gui_shots)
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_cgtop.png":         ["lab.slice","trainjob","Tasks","CPU","Memory"],
            "view_system_monitor.png":["Process","train","CPU","Memory","python"],
            "view_journal_oom.png":   ["oom","killed","Memory","cgroup"],
        }
        ocr_hits = 0
        for n, ks in kws.items():
            p = rd/n
            if not p.exists(): continue
            try:
                tx = pytesseract.image_to_string(Image.open(p))
            except Exception:
                tx = ""
            if any(k.lower() in tx.lower() for k in ks):
                ocr_hits += 1
        s["gui_shots_ocr"] = ocr_hits / len(gui_shots)
    except ImportError:
        s["gui_shots_ocr"] = 0.5

    # 8. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_judge = None
    imgs = [str(rd/n) for n in ("view_cgtop.png","view_system_monitor.png","view_journal_oom.png")
            if (rd/n).exists()]
    if vlm_score_rubric and imgs:
        rubric = {
            "vlm_cgtop_visible":      "截图里能看到 systemd-cgtop TUI 表格,包含 lab.slice 行",
            "vlm_sysmon_window":      "截图里能看到 GNOME 系统监视器进程页,含 train/python 进程",
            "vlm_journal_oom_text":   "截图里能看到 journalctl 的 OOM/killed 内核日志行",
            "vlm_evidence_authentic": "截图明显是真实桌面会话(窗口装饰、光标、终端边框)",
        }
        try:
            vlm = vlm_score_rubric(imgs[:3], rubric,
                instruction="评估 cgroup v2 配额排障任务的 GUI 取证截图。")
            for k in rubric: s[k] = vlm.get(k, 0.0)
            vlm_judge = sum(s.get(k,0.0) for k in rubric) / len(rubric)
        except Exception:
            for k in rubric: s[k] = 0.0
            vlm_judge = 0.0

    # Aggregate
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums) / max(len(nums),1)

    has_cli_evidence = (rd/"memory_events_first.txt").exists() and \
                       (rd/"systemctl_show_first.txt").exists() and \
                       (rd/"journalctl_oom.txt").exists() and \
                       len(read_safe(rd/"memory_events_first.txt")) > 10
    has_gui_screenshot = any((rd/n).exists() for n in
        ("view_cgtop.png","view_system_monitor.png","view_journal_oom.png"))

    if not has_cli_evidence:    base = min(base, 0.4)
    # GUI hard-cap removed: rely on per-shot VLM/OCR sub-scores instead.
    if vlm_score_rubric is not None and vlm_judge is not None and vlm_judge < 0.6:
        base = min(base, 0.6)
    if oom_kill_first < 1:                 base = min(base, 0.35)
    if s.get("report_schema",0) < 1.0:     base = min(base, 0.45)
    if s.get("tuned_stdout_real",0) < 1.0: base = min(base, 0.55)
    if s.get("systemctl_show_first",0) < 1.0 or s.get("systemctl_show_tuned",0) < 1.0: base = min(base, 0.6)
    if s.get("report_tuned_oom_false",0) == 0.0: base = min(base, 0.7)

    s["overall_score"] = round(base, 3)
    return s


def read_safe(p):
    try: return p.read_text(errors="ignore")
    except Exception: return ""


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
