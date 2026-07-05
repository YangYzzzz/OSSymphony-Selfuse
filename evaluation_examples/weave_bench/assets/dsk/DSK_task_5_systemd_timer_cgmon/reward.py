# Auto-generated from WeaveBench task DSK_task_5_systemd_timer_cgmon.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DSK_task_5 grader (v2: weighted scoring + anti-cheat)."""
    import re, hashlib
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. CLI artifacts
    cli_files = ["list_timers_before.txt","list_timers_after.txt","journal_timer_before.txt","journal_service_before.txt","journal_after.txt","cpuquota_verify.txt"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 3

    # 2. bug_findings.md
    bf_score = 0.0
    bf = rd / "bug_findings.md"
    if bf.exists():
        try:
            txt = bf.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80 and re.search(r"sample\.(service|timer)|sample\.\w+:\d+|\.timer|\.service", p)]
            bf_score = min(1.0, len(parags) / 3)
        except Exception: pass
    s["bug_findings"] = bf_score

    # 3. journal shows trigger
    jt_score = 0.0
    ja = rd / "journal_after.txt"
    if ja.exists():
        try:
            txt = ja.read_text()
            if "workload.py started" in txt or re.search(r"Started\s+Sample.*service", txt): jt_score = 1.0
            elif re.search(r"sample\.service", txt): jt_score = 0.5
        except Exception: pass
    s["timer_triggered"] = jt_score

    # 4. cpuquota_verify
    cv_score = 0.0
    cv = rd / "cpuquota_verify.txt"
    if cv.exists():
        try:
            txt = cv.read_text()
            # cpu.max format: "50000 100000" or "max 100000"
            if re.search(r"\b\d{4,5}\s+\d{5,6}\b", txt) and "max" not in txt.split()[0:1]:
                cv_score = 1.0
            elif "CPUQuota" in txt or "cpu.max" in txt:
                cv_score = 0.5
        except Exception: pass
    s["cpuquota_active"] = cv_score

    # 5. GUI screenshots — anti-cheat: count, size>=5KB, md5 unique, OCR keywords
    gui_shots = ["view_system_monitor_processes.png","view_system_monitor_resources.png","view_systemd_cgtop.png",
                 "view_system_monitor_after_fix.png","view_cgtop_after_fix.png"]
    valid_paths = []
    md5_set = set()
    for n in gui_shots:
        p = rd / n
        if p.exists() and p.stat().st_size >= 5 * 1024:
            try:
                h = hashlib.md5(p.read_bytes()).hexdigest()
                if h not in md5_set:
                    md5_set.add(h)
                    valid_paths.append((n, p))
            except Exception:
                pass
    gui_present = len(valid_paths)
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    s["gui_md5_unique"] = 1.0 if gui_present == len(gui_shots) else (gui_present / len(gui_shots))
    has_gui = gui_present >= 3

    vlm_available_flag = False
    try:
        import pytesseract
        from PIL import Image
        kws_any = ["Processes","Resources","CPU","Memory","cgtop","sample","python3","User"]
        ocr_hits = 0
        res_ok = 0
        for n, p in valid_paths:
            try:
                im = Image.open(p)
                w, h = im.size
                if w >= 1024 and h >= 600:
                    res_ok += 1
                tx = pytesseract.image_to_string(im)
                if any(k in tx for k in kws_any): ocr_hits += 1
            except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
        s["gui_resolution_ok"] = res_ok / len(gui_shots)
    except Exception:
        s["gui_screenshots_ocr"] = 0.3 if gui_present > 0 else 0.0
        s["gui_resolution_ok"] = 0.3 if gui_present > 0 else 0.0

    # 6. systemd_report.md
    rp_score = 0.0
    rp = rd / "systemd_report.md"
    if rp.exists():
        try:
            txt = rp.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            rp_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["systemd_report"] = rp_score

    # 7. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    if vlm_score_rubric and (rd / "view_system_monitor_resources.png").exists():
        rubric = {
            "vlm_system_monitor_window": "gnome-system-monitor 窗口可见 + 标签栏",
            "vlm_cpu_curve": "CPU 资源曲线截图明显能看到时序数据",
            "vlm_cgtop_tree": "systemd-cgtop 截图显示 cgroup 树形 + CPU%",
            "vlm_after_fix_lower_cpu": "after_fix 截图 CPU% 比 before 低",
        }
        try:
            imgs = [str(rd / n) for n in ["view_system_monitor_resources.png","view_systemd_cgtop.png","view_system_monitor_after_fix.png"] if (rd / n).exists()]
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 gnome-system-monitor + systemd-cgtop 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
            vlm_available_flag = True
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_system_monitor_window","vlm_cpu_curve","vlm_cgtop_tree","vlm_after_fix_lower_cpu"]:
            s[k] = 0.0

    # 8. Content-reality sub-scores
    # 8a. unit file backups (sample.service.bak / sample.timer.bak) per Prompt 交付物 #9
    bak_present = sum(1 for n in ("sample.service.bak", "sample.timer.bak") if (rd / n).exists())
    s["unit_backup"] = bak_present / 2

    # 8c. timer fired >= 1 (count occurrences in journal_after.txt)
    tcount = 0
    if ja.exists():
        try:
            t = ja.read_text()
            tcount = len(re.findall(r"Started\s+Sample.*service|workload\.py started|sample\.service:.*entered", t))
        except Exception:
            pass
    s["timer_fire_count"] = 1.0 if tcount >= 1 else 0.0

    # Weighted aggregation: core 60% / gui 30% / aux 10%
    core_keys = ["cli_artifacts", "bug_findings", "timer_triggered",
                 "cpuquota_active", "timer_fire_count"]
    gui_keys  = ["gui_screenshots_count", "gui_screenshots_ocr",
                 "gui_md5_unique", "gui_resolution_ok"]
    aux_keys  = ["systemd_report", "unit_backup",
                 "vlm_system_monitor_window", "vlm_cpu_curve",
                 "vlm_cgtop_tree", "vlm_after_fix_lower_cpu"]
    def avg(keys):
        vs = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vs) / len(vs) if vs else 0.0
    core = avg(core_keys); gui = avg(gui_keys); aux = avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Multi-tier hard gates (v2: stricter, layered)
    if not has_cli: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.30)
    if s["bug_findings"] < 0.7: base = min(base, 0.45)
    if s["bug_findings"] < 0.4: base = min(base, 0.30)
    if s["timer_triggered"] < 0.5: base = min(base, 0.45)
    if s["cpuquota_active"] < 0.5: base = min(base, 0.50)
    if s["timer_fire_count"] < 0.5: base = min(base, 0.40)
    if s["gui_screenshots_count"] < 0.6: base = min(base, 0.45)
    if s["gui_md5_unique"] < 0.8: base = min(base, 0.55)
    if s["gui_screenshots_ocr"] < 0.4: base = min(base, 0.55)
    # When VLM is unavailable, cap the ceiling so all-text agents can't max out
    if not vlm_available_flag: base = min(base, 0.60)

    s["overall_score"] = round(max(0.0, base), 4)
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
