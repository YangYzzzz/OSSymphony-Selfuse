# Auto-generated from WeaveBench task OPS_task_5_bpftrace_pcp_syscallstorm.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """OPS_task_5 grader. Empty → 0.000."""
    import re
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. CLI artifacts
    cli_files = ["culprit_pid.txt","bpftrace_top_comm.txt","bpftrace_syscall_id.txt","top_syscalls.txt","bpftrace_after_fix.txt"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 3

    # 2. top comm含 hot_clock/python3
    tc_score = 0.0
    tc = rd / "bpftrace_top_comm.txt"
    if tc.exists():
        try:
            txt = tc.read_text()
            if "hot_clock" in txt or "python3" in txt: tc_score = 1.0
        except Exception: pass
    s["culprit_identified"] = tc_score

    # 3. qps drop — compare against baseline if present, plus absolute floor
    qps_score = 0.0
    baseline_max = 0
    bl = rd / "bpftrace_syscall_id.txt"
    if bl.exists():
        try:
            bl_txt = bl.read_text()
            bl_counts = [int(m) for m in re.findall(r"\b\d{4,}\b", bl_txt)]
            if bl_counts:
                baseline_max = max(bl_counts)
        except Exception: pass
    af = rd / "bpftrace_after_fix.txt"
    if af.exists():
        try:
            txt = af.read_text()
            counts = [int(m) for m in re.findall(r"\b\d{4,}\b", txt)]
            if counts:
                m = max(counts)
                # absolute tier
                abs_score = 0.0
                if m < 2000: abs_score = 1.0
                elif m < 5000: abs_score = 0.7
                elif m < 15000: abs_score = 0.3
                # ratio tier (require ≥80% drop only if baseline available)
                ratio_score = 0.0
                if baseline_max > 0:
                    drop = 1.0 - (m / baseline_max)
                    if drop >= 0.95: ratio_score = 1.0
                    elif drop >= 0.80: ratio_score = 0.8
                    elif drop >= 0.50: ratio_score = 0.4
                    qps_score = max(abs_score, ratio_score)
                else:
                    # no baseline → cap at 0.7 (cannot prove drop, but absolute floor still meaningful)
                    qps_score = min(abs_score, 0.7)
        except Exception: pass
    s["qps_dropped"] = qps_score

    # 4. fix_strategy.md — require both a quota/limit choice AND a justification term
    fs_score = 0.0
    fs = rd / "fix_strategy.md"
    if fs.exists():
        try:
            txt = fs.read_text()
            tl = txt.lower()
            choice_kws = ["cpuquota", "rate-limit", "rate_limit", "ratelimit", "monotonic"]
            reason_kws = ["vdso", "syscall", "kernel", "sys%", "sys ", "bpftrace", "pmchart"]
            has_choice = any(k in tl for k in choice_kws)
            has_reason = any(k in tl for k in reason_kws)
            if has_choice and has_reason and len(txt) >= 120:
                fs_score = 1.0
            elif has_choice and len(txt) >= 80:
                fs_score = 0.5
        except Exception: pass
    s["fix_strategy"] = fs_score

    # 5. GUI screenshots — must be real (≥ 5KB), not stub placeholders
    gui_shots = ["view_pmchart_metric_browse.png","view_pmchart_spike.png","view_pmchart_cpu.png","view_pmchart_after_fix.png"]
    def _real_shot(p):
        try:
            return p.exists() and p.stat().st_size >= 5 * 1024
        except Exception:
            return False
    gui_present = sum(1 for n in gui_shots if _real_shot(rd / n))
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui = gui_present >= 3

    try:
        import pytesseract
        from PIL import Image
        kws_any = ["pmchart","Performance","Co-Pilot","syscall","kernel","metric","CPU"]
        ocr_hits = 0
        for n in gui_shots:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in kws_any): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
    except Exception:
        s["gui_screenshots_ocr"] = 0.5 if gui_present > 0 else 0.0

    # 6. perf_report.md
    rp_score = 0.0
    rp = rd / "perf_report.md"
    if rp.exists():
        try:
            txt = rp.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            rp_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["perf_report"] = rp_score

    # 7. VLM rubric
    vlm_available = False
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    if vlm_score_rubric and (rd / "view_pmchart_spike.png").exists():
        rubric = {
            "vlm_pmchart_window": "pmchart Qt GUI 窗口可见,有 chart axes",
            "vlm_spike_visible": "spike 截图能看到曲线高峰",
            "vlm_after_flat": "after_fix 截图曲线明显比 spike 平",
            "vlm_metric_label_visible": "Y 轴或 legend 显示了 syscall / CPU 相关 metric 名",
        }
        try:
            imgs = [str(rd / n) for n in ["view_pmchart_spike.png","view_pmchart_after_fix.png","view_pmchart_cpu.png"] if (rd / n).exists()]
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 pmchart Qt GUI 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
            vlm_available = True
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_pmchart_window","vlm_spike_visible","vlm_after_flat","vlm_metric_label_visible"]:
            s[k] = 0.0

    # 8. GUI real interaction (md5 diversity of trajectory frames, only count real-sized shots)
    import hashlib as _hashlib
    traj_paths = [rd / n for n in gui_shots]
    present_paths = [p for p in traj_paths if _real_shot(p)]
    if len(present_paths) >= 3:
        _hashes = set(_hashlib.md5(p.read_bytes()).hexdigest() for p in present_paths)
        gui_diversity = (len(_hashes) / max(1, len(present_paths))) * (len(present_paths) / len(traj_paths))
    else:
        gui_diversity = 0.0
    s["gui_real_interaction"] = 1.0 if gui_diversity >= 0.9 else (0.6 if gui_diversity >= 0.7 else (0.3 if gui_diversity >= 0.5 else 0.0))

    # 9. GUI chrome OCR: app-specific UI elements not present in CLI text dumps
    chrome_kws_pmchart = ["pmchart","Performance Co-Pilot","PCP","System Monitor",
                          "Resources","Processes","CPU History","Memory and Swap",
                          "kernel.all","kernel.percpu","Metric Selection","Chart"]
    chrome_hits = 0
    try:
        import pytesseract as _pt
        from PIL import Image as _Img
        for p in traj_paths:
            if p.exists():
                try:
                    tx = _pt.image_to_string(_Img.open(p))
                    if any(k.lower() in tx.lower() for k in chrome_kws_pmchart):
                        chrome_hits += 1
                except Exception:
                    pass
        s["gui_chrome_ocr"] = chrome_hits / len(traj_paths)
    except Exception:
        s["gui_chrome_ocr"] = 0.0

    # 10. Window geometry: GUI screenshots should reflect real desktop resolution
    geo_hits = 0
    try:
        from PIL import Image as _Img2
        for p in traj_paths:
            if p.exists():
                try:
                    w, h = _Img2.open(p).size
                    if w >= 1280 and h >= 720:
                        geo_hits += 1
                except Exception:
                    pass
        s["gui_window_geometry"] = geo_hits / len(traj_paths)
    except Exception:
        s["gui_window_geometry"] = 0.0

    # Weighted overall: core 60% / GUI 30% / VLM 10%
    core_keys = ["cli_artifacts","culprit_identified","qps_dropped","fix_strategy","perf_report"]
    gui_keys  = ["gui_screenshots_count","gui_screenshots_ocr","gui_real_interaction","gui_chrome_ocr","gui_window_geometry"]
    vlm_keys  = ["vlm_pmchart_window","vlm_spike_visible","vlm_after_flat","vlm_metric_label_visible"]
    def _avg(keys):
        vals = [float(s[k]) for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vals) / len(vals) if vals else 0.0
    core = _avg(core_keys); gui = _avg(gui_keys); vlm_v = _avg(vlm_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * vlm_v

    # Aggregated capping: pick the single tightest cap rather than stacking
    # multiple caps for what is often the same underlying failure.
    caps = []
    if not has_cli: caps.append(0.25)
    if not has_gui: caps.append(0.30)
    if s["culprit_identified"] < 1.0: caps.append(0.40)
    # qps_dropped tier (single cap, take the tightest applicable)
    if s["qps_dropped"] < 0.3:
        caps.append(0.40)
    elif s["qps_dropped"] < 0.7:
        caps.append(0.60)
    # GUI hard gates (single cap among GUI-related failures)
    gui_caps = []
    if s.get("gui_real_interaction", 0.0) < 0.6:
        gui_caps.append(0.40)
    if s.get("gui_chrome_ocr", 0.0) < 0.5 and s.get("gui_window_geometry", 0.0) < 0.5:
        gui_caps.append(0.35)
    if s.get("gui_chrome_ocr", 0.0) < 0.75:
        gui_caps.append(0.65)
    if gui_caps:
        caps.append(min(gui_caps))
    # VLM unavailable → cap at 0.6 (cannot let zero-VLM fully pass)
    if not vlm_available:
        caps.append(0.60)
    if caps:
        base = min(base, min(caps))

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
