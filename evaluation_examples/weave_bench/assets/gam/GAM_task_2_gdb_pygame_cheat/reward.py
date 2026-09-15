# Auto-generated from WeaveBench task GAM_task_2_gdb_pygame_cheat.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import json, re
from pathlib import Path

def grade(workspace_path=None, **kwargs) -> dict:
    """GAM_task_2: GDB pygame cheat grader."""
    ws = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = ws / "results"
    gt_dir = Path("/tmp_workspace/gt")
    gt = {}
    if (gt_dir / "expected.json").exists():
        gt = json.loads((gt_dir / "expected.json").read_text())
    s = {}

    # 1. initial screenshot
    s["view_initial"] = 1.0 if (rd / "view_game_initial.png").exists() else 0.0

    # 2. gdb score session
    gs = rd / "gdb_session_score.txt"
    if gs.exists():
        gtxt = gs.read_text(errors="ignore")
        s["gdb_score_file"] = 1.0
        s["gdb_score_pyrun"] = 1.0 if "PyRun_SimpleString" in gtxt else 0.0
        s["gdb_score_attach"] = 1.0 if re.search(
            r"Attaching to", gtxt) else 0.0
    else:
        s["gdb_score_file"] = 0.0
        s["gdb_score_pyrun"] = 0.0
        s["gdb_score_attach"] = 0.0

    # 3. score changed screenshot
    s["view_score_changed"] = 1.0 if (
        rd / "view_score_changed.png").exists() else 0.0

    # 4. gdb speed session
    gsp = rd / "gdb_session_speed.txt"
    if gsp.exists():
        stxt = gsp.read_text(errors="ignore")
        s["gdb_speed_file"] = 1.0
        s["gdb_speed_keyword"] = 1.0 if "game_speed" in stxt else 0.0
    else:
        s["gdb_speed_file"] = 0.0
        s["gdb_speed_keyword"] = 0.0

    # 5. speed changed screenshots (need both for FPS comparison)
    s["view_speed_changed"] = 1.0 if (
        rd / "view_speed_changed.png").exists() else 0.0
    s["view_speed_changed_2"] = 1.0 if (
        rd / "view_speed_changed_2.png").exists() else 0.0

    # 6. proc maps
    pm = rd / "proc_maps.txt"
    if pm.exists():
        ptxt = pm.read_text(errors="ignore").lower()
        s["proc_maps_exists"] = 1.0
        s["proc_maps_python"] = 1.0 if "python" in ptxt else 0.0
    else:
        s["proc_maps_exists"] = 0.0
        s["proc_maps_python"] = 0.0

    # 7. cheat report
    cr = rd / "cheat_report.md"
    if cr.exists():
        ctxt = cr.read_text(errors="ignore").lower()
        has_pid = bool(re.search(r"pid\s*[:=]?\s*\d+", ctxt))
        has_gdb = "gdb" in ctxt
        has_score = "score" in ctxt or "9999" in ctxt
        has_speed = "speed" in ctxt or "game_speed" in ctxt
        s["report_exists"] = 1.0
        s["report_pid"] = 1.0 if has_pid else 0.0
        s["report_gdb"] = 1.0 if has_gdb else 0.0
        s["report_details"] = 1.0 if (has_score and has_speed) else 0.5
    else:
        s["report_exists"] = 0.0
        s["report_pid"] = 0.0
        s["report_gdb"] = 0.0
        s["report_details"] = 0.0

    # VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    if vlm_score_rubric:
        imgs = [str(p) for p in [
            rd / "view_game_initial.png",
            rd / "view_score_changed.png",
            rd / "view_speed_changed.png",
        ] if p.exists()]
        if imgs:
            rubric = {
                "vlm_game_visible":
                    "截屏中能看到贪吃蛇游戏窗口(蛇/食物/得分)",
                "vlm_score_9999":
                    "修改后的截屏中能看到分数显示为 9999",
                "vlm_window_title":
                    "截屏中能看到窗口标题栏 Snake Game",
            }
            vlm = vlm_score_rubric(imgs, rubric,
                instruction="Evaluate pygame snake game screenshots")
            for k in rubric:
                s[k] = vlm.get(k, 0.0)

    # --- Content-authenticity sub-scores ---
    # 9999 must visibly appear in score-changed screenshot (OCR or fallback)
    s["score_ocr_9999"] = 0.0
    score_img = rd / "view_score_changed.png"
    if score_img.exists():
        ocr_hit = False
        try:
            import pytesseract
            from PIL import Image as _Im
            txt_ocr = pytesseract.image_to_string(_Im.open(score_img))
            ocr_hit = "9999" in txt_ocr
        except Exception:
            ocr_hit = False
        if not ocr_hit:
            # fallback: report explicitly mentions 9999 AND screenshot non-trivial
            try:
                from PIL import Image as _Im
                import numpy as _np
                arr = _np.array(_Im.open(score_img).convert("RGB"))
                rep = rd / "cheat_report.md"
                rep_has_9999 = (rep.exists()
                                and "9999" in rep.read_text(errors="ignore"))
                ocr_hit = bool(rep_has_9999 and arr.std() > 20)
            except Exception:
                pass
        s["score_ocr_9999"] = 1.0 if ocr_hit else 0.0

    # speed screenshot must differ from baseline AND show higher FPS via
    # comparing inter-frame delta of two speed shots vs initial→score shots
    s["speed_pixel_delta"] = 0.0
    s["speed_fps_evidence"] = 0.0
    init_img = rd / "view_game_initial.png"
    sp_img = rd / "view_speed_changed.png"
    sp2_img = rd / "view_speed_changed_2.png"
    score_img2 = rd / "view_score_changed.png"
    try:
        from PIL import Image as _Im
        import numpy as _np

        def _delta(p1, p2):
            a = _Im.open(p1).convert("RGB")
            b = _Im.open(p2).convert("RGB").resize(a.size)
            return float(_np.abs(_np.array(a, dtype=int)
                                 - _np.array(b, dtype=int)).mean())

        if init_img.exists() and sp_img.exists():
            d1 = _delta(init_img, sp_img)
            # raised threshold (was >5); require d > 15 for full
            s["speed_pixel_delta"] = 1.0 if d1 > 15 else max(0.0, d1 / 15)

        # FPS evidence: delta between the two speed-shots should be larger
        # than delta between initial and score-changed (which is taken at
        # the original lower FPS). Helps catch reused/static screenshots.
        if sp_img.exists() and sp2_img.exists() and init_img.exists():
            d_speed = _delta(sp_img, sp2_img)
            d_base = _delta(init_img, score_img2) if score_img2.exists() else 1.0
            ratio = d_speed / max(d_base, 1.0)
            # snake at 3x FPS should produce ~3x position delta
            if ratio >= 1.8 and d_speed > 8:
                s["speed_fps_evidence"] = 1.0
            elif ratio >= 1.3 and d_speed > 5:
                s["speed_fps_evidence"] = 0.5
    except Exception:
        pass

    # --- Anti-cheat: screenshot authenticity ---
    import hashlib
    shots = [rd / n for n in [
        "view_game_initial.png", "view_score_changed.png",
        "view_speed_changed.png", "view_speed_changed_2.png",
    ]]
    existing = [p for p in shots if p.exists()]
    md5s, sizes_ok, res_ok = set(), True, True
    try:
        from PIL import Image as _Im
        for p in existing:
            data = p.read_bytes()
            md5s.add(hashlib.md5(data).hexdigest())
            if len(data) < 5 * 1024:
                sizes_ok = False
            try:
                w, h = _Im.open(p).size
                if w < 640 or h < 480:
                    res_ok = False
            except Exception:
                res_ok = False
    except Exception:
        pass
    s["shot_md5_unique"] = 1.0 if (existing and len(md5s) == len(existing)) else 0.0
    s["shot_size_ok"] = 1.0 if (existing and sizes_ok) else 0.0
    s["shot_resolution_ok"] = 1.0 if (existing and res_ok) else 0.0

    # forbidden imports: pre-built cheat-engine wrappers
    forbidden = ["cheat_engine", "pygame_cheat_engine", "pycheat"]
    bad_import = False
    for src in ws.rglob("*.py"):
        try:
            t = src.read_text(errors="ignore")
            if any(re.search(rf"\bimport\s+{f}|from\s+{f}\b", t) for f in forbidden):
                bad_import = True
                break
        except Exception:
            pass
    # forbidden-import check is a hard gate, not part of the average
    no_cheat_lib = 0.0 if bad_import else 1.0

    # Hard gates
    has_cli = (s.get("gdb_score_file", 0) > 0 and
               s.get("proc_maps_exists", 0) > 0)
    has_gui = (s.get("view_initial", 0) > 0 and
               s.get("view_score_changed", 0) > 0)

    # Weighted overall: core delivery 60% / GUI evidence 30% / aux 10%
    def _avg(keys):
        vs = [s.get(k, 0.0) for k in keys]
        return sum(vs) / len(vs) if vs else 0.0

    core_keys = [
        "gdb_score_file", "gdb_score_pyrun", "gdb_score_attach",
        "gdb_speed_file", "gdb_speed_keyword",
        "proc_maps_exists", "proc_maps_python",
        "score_ocr_9999", "speed_pixel_delta", "speed_fps_evidence",
    ]
    gui_keys = [
        "view_initial", "view_score_changed",
        "view_speed_changed", "view_speed_changed_2",
        "vlm_game_visible", "vlm_score_9999", "vlm_window_title",
        "shot_md5_unique", "shot_size_ok", "shot_resolution_ok",
    ]
    aux_keys = [
        "report_exists", "report_pid", "report_gdb", "report_details",
    ]
    base = 0.6 * _avg(core_keys) + 0.3 * _avg(gui_keys) + 0.1 * _avg(aux_keys)

    # Hard gates (raised vs v1)
    if not has_cli:
        base = min(base, 0.35)
    if not has_gui:
        base = min(base, 0.35)
    # Content-authenticity stair-step caps (tightened)
    if s.get("score_ocr_9999", 0) < 1.0:
        base = min(base, 0.45)
    if s.get("speed_pixel_delta", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("speed_fps_evidence", 0) < 0.5:
        base = min(base, 0.55)
    if s.get("gdb_score_pyrun", 0) < 1.0:
        base = min(base, 0.4)
    if s.get("gdb_score_attach", 0) < 1.0:
        base = min(base, 0.55)
    # Anti-cheat caps
    if s.get("shot_md5_unique", 0) < 1.0:
        base = min(base, 0.4)
    if s.get("shot_size_ok", 0) < 1.0:
        base = min(base, 0.45)
    if s.get("shot_resolution_ok", 0) < 1.0:
        base = min(base, 0.5)
    # forbidden-library gate
    if no_cheat_lib < 1.0:
        base = min(base, 0.35)
    # VLM unavailable → cap at 0.6 (no free pass when VLM cannot verify)
    if not any(k in s for k in ("vlm_game_visible", "vlm_score_9999",
                                 "vlm_window_title")):
        base = min(base, 0.6)
    s["no_cheat_lib_imports"] = no_cheat_lib  # report only
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
