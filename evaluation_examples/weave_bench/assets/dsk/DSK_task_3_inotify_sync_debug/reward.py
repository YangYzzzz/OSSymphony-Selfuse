# Auto-generated from WeaveBench task DSK_task_3_inotify_sync_debug.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DSK_task_3 grader. Empty → 0.000. Hard gates: GUI + CLI + verify pass."""
    import re
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. CLI artifacts
    cli_files = ["inotify_events.txt","sync.log","sync_backup.py","test1_partial_copy.txt","test2_path_flatten.txt","test3_moved_to_missing.txt"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 3

    # 2. inotify_events.txt has multiple events
    ev_score = 0.0
    ef = rd / "inotify_events.txt"
    if ef.exists():
        try:
            txt = ef.read_text()
            ev_types = set(re.findall(r"\b(CREATE|MODIFY|CLOSE_WRITE|MOVED_TO|MOVED_FROM|DELETE|OPEN)\b", txt))
            if len(ev_types) >= 4: ev_score = 1.0
            elif len(ev_types) >= 2: ev_score = 0.5
        except Exception: pass
    s["inotify_event_diversity"] = ev_score

    # 3. bug_findings.md
    bf_score = 0.0
    bf = rd / "bug_findings.md"
    if bf.exists():
        try:
            txt = bf.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80 and re.search(r"\.py:\d+", p)]
            bf_score = min(1.0, len(parags) / 3)
        except Exception: pass
    s["bug_findings"] = bf_score

    # 4. GUI screenshots
    gui_shots = ["view_nautilus_create.png","view_nautilus_subdir.png","view_nautilus_move.png","view_nautilus_after_fix.png"]
    gui_present = sum(1 for n in gui_shots if (rd / n).exists())
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui = gui_present >= 2

    try:
        import pytesseract
        from PIL import Image
        kws_any = ["Files","Nautilus","watched","subdir","Folder","Documents","Home","b.txt","a.txt"]
        ocr_hits = 0
        for n in gui_shots:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k in tx for k in kws_any): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
        ocr_available = True
    except Exception:
        s["gui_screenshots_ocr"] = 0.5 if gui_present > 0 else 0.0
        ocr_available = False

    # 4b. Anti-cheat: screenshot md5 uniqueness + minimum size (>=5KB) + minimum resolution
    import hashlib
    md5s, big_enough, res_ok = set(), 0, 0
    for n in gui_shots:
        p = rd / n
        if p.exists() and p.stat().st_size >= 5 * 1024:
            big_enough += 1
            try:
                md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception: pass
            try:
                from PIL import Image as _Im
                w, h = _Im.open(p).size
                if w >= 800 and h >= 600: res_ok += 1
            except Exception:
                res_ok += 1  # PIL 不可用时不卡
    denom = max(gui_present, 1)
    s["gui_screenshots_unique"] = len(md5s) / denom if gui_present else 0.0
    s["gui_screenshots_size_ok"] = big_enough / len(gui_shots)
    s["gui_screenshots_res_ok"] = res_ok / len(gui_shots)

    # 5. verify_output.txt (合并了原 mirror_md5 子项: 同时要求 ALL SYNC OK + md5 证据)
    vo_score = 0.0
    vo = rd / "verify_output.txt"
    if vo.exists():
        try:
            txt = vo.read_text()
            has_ok = "ALL SYNC OK" in txt
            has_md5 = bool(re.search(r"\bmd5(sum)?\b", txt, re.I))
            has_md5_match = bool(re.search(r"md5.*(ok|match|equal)|ALL\s+MATCH|md5sum.*OK", txt, re.I))
            if has_ok and has_md5_match: vo_score = 1.0
            elif has_ok and has_md5:     vo_score = 0.8
            elif has_ok:                 vo_score = 0.55
            elif re.search(r"100%|all\s+ok|all\s+match", txt, re.I): vo_score = 0.4
        except Exception: pass
    s["verify_pass"] = vo_score

    # 6. sync_report.md
    sr_score = 0.0
    sr = rd / "sync_report.md"
    if sr.exists():
        try:
            txt = sr.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            sr_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["sync_report"] = sr_score

    # 7. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    if vlm_score_rubric and (rd / "view_nautilus_create.png").exists():
        rubric = {
            "vlm_nautilus_window": "截图能看到 Nautilus 文件管理器窗口和侧边栏",
            "vlm_files_visible": "文件列表区域显示了 a.txt / subdir / b.txt 等",
            "vlm_path_breadcrumb": "顶部能看到路径面包屑(Home > tmp_workspace > watched)",
            "vlm_action_evidence": "截图能看到拖放/新建/复制等动作的证据(高亮 / context menu)",
        }
        try:
            imgs = [str(rd / n) for n in ["view_nautilus_create.png","view_nautilus_subdir.png","view_nautilus_move.png"] if (rd / n).exists()]
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 Nautilus 文件管理器截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_nautilus_window","vlm_files_visible","vlm_path_breadcrumb","vlm_action_evidence"]:
            s[k] = 0.0

    # 8. Content-reality sub-scores
    # 8a. all 3 test_*.txt artifacts present and non-empty
    test_files = ["test1_partial_copy.txt", "test2_path_flatten.txt", "test3_moved_to_missing.txt"]
    ok_t = 0
    for n in test_files:
        p = rd / n
        if p.exists() and p.stat().st_size > 0:
            ok_t += 1
    s["test_artifacts_complete"] = round(ok_t / len(test_files), 3)

    # 8b. fix artifact (sync_backup.py / fixed_sync.py / patch.diff) is real
    fix_score = 0.0
    for cand in ("sync_backup.py", "fixed_sync.py", "patch.diff", "sync_fixed.py"):
        p = rd / cand
        if p.exists() and p.stat().st_size > 200:
            fix_score = 1.0
            break
        elif p.exists() and p.stat().st_size > 0:
            fix_score = max(fix_score, 0.5)
    s["fix_artifact_present"] = fix_score

    # 8c. (removed) mirror_md5_verified — merged into verify_pass to eliminate score-dim overlap

    # 8d. forbidden: bug_findings.md must NOT be empty boilerplate (specific path:line refs already enforced in #3)

    # ---- weighted scoring (核心交付 60% / GUI 证据 30% / 辅助 10%) ----
    core_keys = ["cli_artifacts","bug_findings","verify_pass","test_artifacts_complete","fix_artifact_present"]
    gui_keys  = ["gui_screenshots_count","gui_screenshots_ocr","gui_screenshots_unique","gui_screenshots_size_ok",
                 "gui_screenshots_res_ok","vlm_nautilus_window","vlm_files_visible","vlm_path_breadcrumb","vlm_action_evidence"]
    aux_keys  = ["inotify_event_diversity","sync_report"]
    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vals) / len(vals) if vals else 0.0
    core_avg, gui_avg, aux_avg = _avg(core_keys), _avg(gui_keys), _avg(aux_keys)
    base = 0.6 * core_avg + 0.3 * gui_avg + 0.1 * aux_avg

    # hard gates (v2: 收紧)
    if not has_cli: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.25)
    if s["bug_findings"] < 0.67:                base = min(base, 0.40)
    if s["verify_pass"] < 0.55:                 base = min(base, 0.45)
    if s["inotify_event_diversity"] < 0.5:      base = min(base, 0.60)
    if s["test_artifacts_complete"] < 1.0:      base = min(base, 0.55)
    if s["fix_artifact_present"] < 1.0:         base = min(base, 0.55)
    # 反伪截图: md5 唯一性 + 最小尺寸
    if s["gui_screenshots_unique"] < 0.75:      base = min(base, 0.55)
    if s["gui_screenshots_size_ok"] < 0.75:     base = min(base, 0.55)
    if s["gui_screenshots_ocr"] < 0.5:          base = min(base, 0.55)
    # VLM/OCR 不可用 → 上限封顶 0.6,不许无 VLM 也满分
    vlm_sum = sum(s.get(k, 0.0) for k in ["vlm_nautilus_window","vlm_files_visible","vlm_path_breadcrumb","vlm_action_evidence"])
    if vlm_sum == 0.0 or not ocr_available:     base = min(base, 0.60)

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
