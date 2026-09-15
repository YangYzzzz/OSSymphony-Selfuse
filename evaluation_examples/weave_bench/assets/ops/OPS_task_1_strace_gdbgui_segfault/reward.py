# Auto-generated from WeaveBench task OPS_task_1_strace_gdbgui_segfault.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """gdbgui + strace + addr2line use-after-free 诊断闭环 grader (v2 tightened)."""
    import json, re, hashlib
    from pathlib import Path
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    try:
        import pytesseract
        from PIL import Image
    except Exception:
        pytesseract = None
        Image = None

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    def ocr_hits(path, kws):
        if not (pytesseract and Image and path.exists()):
            return False
        try:
            tx = pytesseract.image_to_string(Image.open(path)).lower()
        except Exception:
            return False
        return any(k.lower() in tx for k in kws)

    # 1. build.log + server_pid.txt
    bl = rd / "build.log"
    pid = rd / "server_pid.txt"
    s["build_artifacts"] = (int(bl.exists()) + int(pid.exists())) / 2.0

    # 2. strace_crash_tail.txt — require ≥100 lines AND ≥3 distinct syscalls from the set
    sc = rd / "strace_crash_tail.txt"
    if sc.exists():
        txt = sc.read_text(errors="ignore")
        lines = txt.strip().split("\n")
        sys_kws = ["mmap", "munmap", "write", "read", "brk", "close"]
        sys_hits = sum(1 for k in sys_kws if k in txt)
        if len(lines) >= 100 and sys_hits >= 3:
            s["strace_crash"] = 1.0
        elif len(lines) >= 50 and sys_hits >= 2:
            s["strace_crash"] = 0.5
        elif lines and sys_hits >= 1:
            s["strace_crash"] = 0.25
        else:
            s["strace_crash"] = 0.0
    else:
        s["strace_crash"] = 0.0

    # 3. dmesg_segfault.txt
    dm = rd / "dmesg_segfault.txt"
    if dm.exists():
        t = dm.read_text(errors="ignore").lower()
        s["dmesg_segfault"] = 1.0 if ("segfault" in t or "sigsegv" in t) else 0.3
    else:
        s["dmesg_segfault"] = 0.0

    # 4. core.bin
    cb = rd / "core.bin"
    s["core_dump"] = 1.0 if (cb.exists() and cb.stat().st_size > 100) else 0.0

    # 5. gdbgui screenshots phase 2 + 4 (6 of them)
    debug_shots = [
        "view_01_gdbgui_coredump_bt.png",
        "view_02_gdbgui_frame_jump.png",
        "view_03_gdbgui_breakpoint_hit.png",
        "view_04_gdbgui_step_to_release.png",
        "view_05_gdbgui_memory_viewer.png",
        "view_06_gdbgui_stack_regs.png",
    ]
    # require non-trivial size (>5KB) to count as present (anti-placeholder)
    def _valid_shot(p):
        return p.exists() and p.stat().st_size >= 5 * 1024
    present = sum(1 for n in debug_shots if _valid_shot(rd / n))
    s["debug_shots_present"] = present / len(debug_shots)
    kw = ["gdbgui", "breakpoint", "variables", "call stack", "registers",
          "source", "gdb", "console", "locals", "step", "continue", "memory"]
    if pytesseract and Image:
        hits = sum(1 for n in debug_shots if ocr_hits(rd / n, kw))
        s["debug_shots_ocr"] = hits / len(debug_shots)
    else:
        s["debug_shots_ocr"] = 0.5 if present else 0.0
    # md5 uniqueness across all 8 gdbgui screenshots (anti-cheat: same image reused)
    all_shots_for_md5 = debug_shots + [
        "view_07_gdbgui_fix_verified.png",
        "view_08_gdbgui_continue_no_crash.png",
    ]
    md5s = []
    for n in all_shots_for_md5:
        p = rd / n
        if _valid_shot(p):
            try:
                md5s.append(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception:
                pass
    if md5s:
        s["shots_md5_uniqueness"] = len(set(md5s)) / len(md5s)
    else:
        s["shots_md5_uniqueness"] = 0.0

    # 6. addr2line + objdump
    al = rd / "addr2line_output.txt"
    if al.exists():
        s["addr2line"] = 1.0 if re.search(r"\w+\.c:\d+", al.read_text(errors="ignore")) else 0.3
    else:
        s["addr2line"] = 0.0
    da = rd / "disasm_handle_request.txt"
    if da.exists():
        t = da.read_text(errors="ignore")
        s["disasm"] = 1.0 if any(k in t for k in ["mov", "call", "lea", "ret", "push", "jmp"]) else 0.3
    else:
        s["disasm"] = 0.0

    # 7. defect_analysis.json — schema + correct defect_class (UAF) + narrative quality
    dj = rd / "defect_analysis.json"
    da_score = 0.0
    defect_class_correct = False
    if dj.exists():
        try:
            d = json.loads(dj.read_text())
            req = {"crash_addr","crash_file","crash_line","suspect_function","defect_class",
                   "evidence_strace_lines","evidence_addr2line","evidence_gdbgui_screenshot","narrative"}
            allowed = {"use_after_free","double_free","oob_write","uninit_read","null_deref"}
            if req <= set(d.keys()):
                da_score = 0.25
                if d.get("defect_class") in allowed:
                    da_score += 0.15
                # bonus: defect_class must actually be use_after_free (true root cause)
                if d.get("defect_class") == "use_after_free":
                    da_score += 0.20
                    defect_class_correct = True
                # narrative ≥80 chars AND must mention three evidence channels
                narr = d.get("narrative", "")
                if isinstance(narr, str) and len(narr) >= 80:
                    da_score += 0.15
                    nl = narr.lower()
                    chan_hits = sum(1 for k in ["strace", "addr2line", "gdbgui"] if k in nl)
                    if chan_hits >= 3:
                        da_score += 0.15
                # suspect_function must be handle_request (per Prompt + crash site)
                if d.get("suspect_function") == "handle_request":
                    da_score += 0.10
                da_score = min(da_score, 1.0)
        except Exception:
            pass
    s["defect_analysis"] = da_score
    s["defect_class_correct"] = 1.0 if defect_class_correct else 0.0

    # 8. fix.patch — must touch g_last_response or free/log_response area (true UAF fix)
    fp = rd / "fix.patch"
    if fp.exists():
        t = fp.read_text(errors="ignore")
        is_diff = ("---" in t and "+++" in t and "@@" in t)
        plus_lines = [l for l in t.splitlines() if l.startswith("+") and not l.startswith("+++")]
        plus = len(plus_lines)
        plus_blob = "\n".join(plus_lines).lower()
        # fix is meaningful if it touches g_last_response, free(response), or moves log_response
        meaningful = any(k in plus_blob for k in [
            "g_last_response", "log_response", "strdup", "memcpy", "= null"
        ])
        if is_diff and plus >= 3 and meaningful:
            s["fix_patch"] = 1.0
        elif is_diff and plus >= 3:
            s["fix_patch"] = 0.6
        elif is_diff:
            s["fix_patch"] = 0.3
        else:
            s["fix_patch"] = 0.0
    else:
        s["fix_patch"] = 0.0

    # 9. fixed build + post strace
    bf = rd / "build_fixed.log"
    s["build_fixed"] = 1.0 if bf.exists() else 0.0
    sp = rd / "strace_post_tail.txt"
    if sp.exists():
        t = sp.read_text(errors="ignore")
        tlow = t.lower()
        nlines = len(t.strip().split("\n"))
        no_crash = ("sigsegv" not in tlow) and ("segfault" not in tlow)
        # Prompt requires ≥200 lines for post-fix strace tail
        if no_crash and nlines >= 200:
            s["strace_post"] = 1.0
        elif no_crash and nlines >= 100:
            s["strace_post"] = 0.6
        elif no_crash:
            s["strace_post"] = 0.3
        else:
            s["strace_post"] = 0.0
    else:
        s["strace_post"] = 0.0

    # 10. fix verification screenshots (2) — same anti-placeholder size gate
    fv_shots = ["view_07_gdbgui_fix_verified.png", "view_08_gdbgui_continue_no_crash.png"]
    fv_present = sum(1 for n in fv_shots if _valid_shot(rd / n))
    s["fix_shots_present"] = fv_present / len(fv_shots)
    if pytesseract and Image:
        s["fix_shots_ocr"] = sum(1 for n in fv_shots if ocr_hits(rd / n, kw)) / len(fv_shots)
    else:
        s["fix_shots_ocr"] = 0.5 if fv_present else 0.0

    # 11. report
    rpt = rd / "diagnosis_report.md"
    if rpt.exists():
        t = rpt.read_text(errors="ignore")
        sections = ["## Root Cause","## strace Evidence","## addr2line Evidence",
                    "## gdbgui Evidence","## Fix & Regression"]
        sec_hits = sum(1 for sec in sections if sec.lower() in t.lower())
        s["report"] = 1.0 if (len(t) >= 350 and sec_hits >= 5) else (0.5 if sec_hits >= 3 else 0.2)
    else:
        s["report"] = 0.0

    # 12. cross-channel evidence (CLI + GUI co-present)
    has_cli_ev = (s["strace_crash"] > 0) and (s["addr2line"] > 0)
    has_gui_ev = (s["debug_shots_present"] >= 0.5)
    s["cross_channel_evidence"] = 1.0 if (has_cli_ev and has_gui_ev) else 0.0

    # VLM rubric (4 items)
    if vlm_score_rubric:
        all_shots = debug_shots + fv_shots
        sample = [str(rd / n) for n in all_shots if (rd / n).exists()][:4]
        if sample:
            rubric = {
                "vlm_gdbgui_real_window": "至少一张截图清晰显示 gdbgui 浏览器窗口(顶栏 gdbgui 字样 + 左侧源码面板带行号 + 底部 GDB Console)",
                "vlm_variables_panel": "至少一张截图能读到 Variables/Locals 面板列出变量名 + 当前值(非空)",
                "vlm_memory_or_stack": "至少一张截图能看到 Memory Viewer 的 hex 输出 或 Call Stack 面板的多帧列表",
                "vlm_fix_verified": "view_07/view_08 中能看出修复后断点能命中且程序未崩溃 Continue",
            }
            vlm = vlm_score_rubric(sample, rubric,
                instruction="评估 gdbgui 浏览器调试器在 use-after-free 诊断与修复验证中的截图真实性。")
            for k in rubric:
                s[k] = vlm.get(k, 0.0)
            s["judge_method"] = vlm.get("judge_method", "failed")

    # ---- Weighted aggregate: core 60% / gui 30% / aux 10% ----
    core_keys = ["defect_analysis", "defect_class_correct", "fix_patch",
                 "build_fixed", "strace_post", "report"]
    gui_keys = ["debug_shots_present", "debug_shots_ocr",
                "fix_shots_present", "fix_shots_ocr", "shots_md5_uniqueness"]
    vlm_keys = [k for k in s if k.startswith("vlm_")]
    gui_keys_full = gui_keys + vlm_keys
    aux_keys = ["build_artifacts", "strace_crash", "dmesg_segfault",
                "core_dump", "addr2line", "disasm", "cross_channel_evidence"]

    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vals) / len(vals) if vals else 0.0

    core = _avg(core_keys)
    gui = _avg(gui_keys_full)
    aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # ---- Hard gates (tightened for v2) ----
    # CLI/GUI evidence channels
    if not has_cli_ev:
        base = min(base, 0.35)
    if not has_gui_ev:
        base = min(base, 0.35)
    # Must have ALL 6 debug screenshots present (>=5KB) — partial cap
    if s.get("debug_shots_present", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("debug_shots_present", 0) < 0.5:
        base = min(base, 0.40)
    # defect analysis correctness
    if s.get("defect_analysis", 0) < 0.5:
        base = min(base, 0.50)
    if s.get("defect_analysis", 0) == 0:
        base = min(base, 0.40)
    # fix patch must be meaningful
    if s.get("fix_patch", 0) < 0.6:
        base = min(base, 0.50)
    if s.get("fix_patch", 0) == 0:
        base = min(base, 0.40)
    # post-fix regression must show no crash
    if s.get("strace_post", 0) < 0.6:
        base = min(base, 0.55)
    # screenshot anti-cheat
    if s.get("shots_md5_uniqueness", 0) < 0.75:
        base = min(base, 0.55)
    # VLM thresholds — tighter, layered
    if vlm_keys:
        vlm_avg = sum(s[k] for k in vlm_keys) / len(vlm_keys)
        s["vlm_avg"] = vlm_avg
        if vlm_avg < 0.6:
            base = min(base, 0.55)
        if vlm_avg < 0.4:
            base = min(base, 0.30)
    else:
        # VLM unavailable → can't reach top tier
        base = min(base, 0.60)

    s["overall_score"] = float(max(0.0, min(1.0, base)))
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
