# Auto-generated from WeaveBench task GAM_task_12_godot_scene_node_debug.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Godot 3 .tscn scene-graph repair + GUI playthrough verifier.

    Sub-scores (12) + 3 hard gates.  Real signal channels:
      - File: in-house regex parse of .tscn ext_resource / sub_resource /
              node sections; numeric checks for ExtResource id, Label
              margins, RectangleShape2D extents.
      - GUI : 4 screenshots OCR for editor / play / finish overlay.
      - Run : runtime.log captures stdout from godot3 --path.
    No GT leakage: gt/expected.json holds invariant counts only
    (e.g. number of bugs, OCR keyword set, viewport size, diff bounds).
    """
    import json, os, re
    from pathlib import Path

    ws  = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd  = ws / "results"
    proj = ws / "proj"
    gt_dir = ws / "gt"
    expected = {}
    if (gt_dir / "expected.json").exists():
        try:    expected = json.loads((gt_dir/"expected.json").read_text())
        except Exception: expected = {}
    s = {}

    # ---- 1. parse_before.json schema ----
    pb = rd / "parse_before.json"
    schema_ok = 0
    if pb.exists():
        try:
            d = json.loads(pb.read_text())
            need = {"ext_resources","sub_resources","nodes"}
            if need.issubset(d.keys()) and len(d.get("nodes", [])) >= 6:
                schema_ok = 1
        except Exception: pass
    s["parse_before_schema"] = float(schema_ok)

    # ---- 2. bugs.json all 3 bugs detected with evidence ----
    bj = rd / "bugs.json"
    bugs_hit = 0
    if bj.exists():
        try:
            b = json.loads(bj.read_text())
            # Numeric "ground-truth" values are read from gt/expected.json so
            # changing the broken fixture only requires editing the JSON, and
            # so the answers are not silently leaked in grader source.
            ext_ref_gt   = int(expected.get("broken_extresource_id_referenced", 2))
            ext_def_gt   = int(expected.get("broken_extresource_id_defined", 1))
            label_lo     = float(expected.get("broken_label_margin_left", 1000.0))
            label_lo_top = float(expected.get("broken_label_margin_top",  1000.0))
            sub_id_gt    = int(expected.get("broken_floor_shape_subresource_id", 1))
            zero_ext_gt  = list(expected.get("broken_floor_extents", [0.0, 0.0]))
            vw_gt, vh_gt = expected.get("viewport_size", [640, 480])
            for k, must in [
                ("bug_dangling_extresource",
                    ["referenced_id","defined_ids"]),
                ("bug_label_offscreen",
                    ["margin_left","margin_top","viewport"]),
                ("bug_collision_zero_extents",
                    ["subresource_id","extents"]),
            ]:
                v = b.get(k, {})
                exp_match = True
                if k == "bug_dangling_extresource":
                    exp_match = (int(v.get("referenced_id",-1)) == ext_ref_gt and
                                 ext_def_gt in [int(x) for x in v.get("defined_ids",[])])
                if k == "bug_label_offscreen":
                    # Allow either margin to surpass the (relaxed) lower bound;
                    # avoids penalising agents that clamped one axis to 0.
                    exp_match = ((float(v.get("margin_left",0)) >= label_lo or
                                  float(v.get("margin_top",0))  >= label_lo_top) and
                                 list(v.get("viewport",[]))[:2] == [vw_gt, vh_gt])
                if k == "bug_collision_zero_extents":
                    ext = v.get("extents",[1,1])
                    exp_match = (int(v.get("subresource_id",-1)) == sub_id_gt and
                                 float(ext[0]) == float(zero_ext_gt[0]) and
                                 float(ext[1]) == float(zero_ext_gt[1]))
                if v.get("detected") and all(m in v for m in must) and exp_match:
                    bugs_hit += 1
        except Exception: pass
    s["bugs_detected_with_evidence"] = bugs_hit / 3.0

    # ---- 3-6. fixed.tscn parses & invariants ----
    fixed_paths = [proj/"scenes/main_fixed.tscn",
                   ws/"exec/scenes/main_fixed.tscn"]
    fixed = next((p for p in fixed_paths if p.exists()), None)
    parses = ext_id_ok = label_ok = floor_ok = 0.0
    txt = ""
    if fixed:
        try:
            txt = fixed.read_text(errors="ignore")
            if "[gd_scene" in txt and "[node name=" in txt:
                parses = 1.0
        except Exception: parses = 0.0
    s["fixed_tscn_parses"] = parses

    if parses:
        # Collect ext_resource ids
        ext_ids = set()
        for m in re.finditer(r"\[ext_resource[^\]]*\bid=(\d+)", txt):
            ext_ids.add(int(m.group(1)))
        sub_ids = set()
        for m in re.finditer(r"\[sub_resource[^\]]*\bid=(\d+)", txt):
            sub_ids.add(int(m.group(1)))
        # Find PlayerSprite block + its texture line
        ps_blk = re.search(
            r'\[node name="PlayerSprite"[^\]]*\](.*?)(?=\n\[node|\Z)',
            txt, re.S)
        if ps_blk:
            tm = re.search(r"texture\s*=\s*ExtResource\(\s*(\d+)\s*\)",
                           ps_blk.group(1))
            if tm and int(tm.group(1)) in ext_ids:
                ext_id_ok = 1.0
        # GoalLabel margins inside viewport
        gl_blk = re.search(
            r'\[node name="GoalLabel"[^\]]*\](.*?)(?=\n\[node|\Z)',
            txt, re.S)
        if gl_blk:
            ml = re.search(r"margin_left\s*=\s*(-?[0-9.]+)",  gl_blk.group(1))
            mt = re.search(r"margin_top\s*=\s*(-?[0-9.]+)",   gl_blk.group(1))
            mr = re.search(r"margin_right\s*=\s*(-?[0-9.]+)", gl_blk.group(1))
            mb = re.search(r"margin_bottom\s*=\s*(-?[0-9.]+)",gl_blk.group(1))
            vw, vh = expected.get("viewport_size",[640,480])
            if ml and mt and mr and mb:
                vals = [float(x.group(1)) for x in (ml,mt,mr,mb)]
                if (-50 <= vals[0] <= vw and -50 <= vals[1] <= vh
                    and 0 <= vals[2] <= vw+50 and 0 <= vals[3] <= vh+50):
                    label_ok = 1.0
        # Floor RectangleShape2D extents
        fs_blk = re.search(
            r'\[node name="FloorShape"[^\]]*\](.*?)(?=\n\[node|\Z)',
            txt, re.S)
        if fs_blk:
            sm = re.search(r"shape\s*=\s*SubResource\(\s*(\d+)\s*\)",
                           fs_blk.group(1))
            if sm:
                sid = int(sm.group(1))
                # find that sub_resource block's extents
                sb = re.search(
                    r'\[sub_resource[^\]]*\bid=' + str(sid) +
                    r'[^\]]*\](.*?)(?=\n\[sub_resource|\n\[node|\Z)',
                    txt, re.S)
                if sb:
                    em = re.search(
                        r"extents\s*=\s*Vector2\(\s*(-?[0-9.]+)\s*,"
                        r"\s*(-?[0-9.]+)\s*\)",
                        sb.group(1))
                    if em:
                        ex, ey = float(em.group(1)), float(em.group(2))
                        if ex > 0 and ey > 0:
                            floor_ok = 1.0
    s["fixed_extresource_id"]   = ext_id_ok
    s["fixed_label_in_viewport"]= label_ok
    s["fixed_floor_extents"]    = floor_ok

    # ---- 7. editor screenshots present + OCR ----
    shots_editor = ["view_editor_before.png","view_editor_after.png"]
    editor_present = sum(1 for n in shots_editor if (rd/n).exists())
    s["editor_shots_present"] = editor_present / 2.0
    ed_kw = expected.get("editor_keywords",
        ["scene","node","inspector","filesystem","godot"])
    try:
        import pytesseract
        from PIL import Image
        editor_ocr_hits = 0
        for n in shots_editor:
            p = rd/n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p)).lower()
                    hit_kw = {k for k in ed_kw if k in tx}
                    if len(hit_kw) >= 3:
                        editor_ocr_hits += 1
                except Exception: pass
        s["editor_shots_ocr"] = editor_ocr_hits / 2.0
    except ImportError:
        s["editor_shots_ocr"] = 0.5

    # ---- 8. play bug screenshot present + OCR ----
    pb_shot = rd/"view_play_bug.png"
    s["play_bug_shot_present"] = 1.0 if pb_shot.exists() else 0.0
    pl_kw = expected.get("play_keywords",
        ["sceneplay","scenplay","goal","arrows","reach","left/right"])
    try:
        import pytesseract
        from PIL import Image
        if pb_shot.exists():
            try:
                tx = pytesseract.image_to_string(Image.open(pb_shot)).lower()
            except Exception:
                tx = ""
            hits = sum(1 for k in pl_kw if k in tx)
            s["play_bug_shot_hud_ocr"] = 1.0 if hits >= 1 else 0.0
        else:
            s["play_bug_shot_hud_ocr"] = 0.0
    except ImportError:
        s["play_bug_shot_hud_ocr"] = 0.5 if pb_shot.exists() else 0.0

    # ---- 9. play finish screenshot present + OCR GOAL ----
    pf_shot = rd/"view_play_finish.png"
    s["play_finish_shot_present"] = 1.0 if pf_shot.exists() else 0.0
    try:
        import pytesseract
        from PIL import Image
        if pf_shot.exists():
            try:
                tx = pytesseract.image_to_string(Image.open(pf_shot)).lower()
            except Exception:
                tx = ""
            s["play_finish_shot_ocr"] = 1.0 if "goal" in tx else 0.0
        else:
            s["play_finish_shot_ocr"] = 0.0
    except ImportError:
        s["play_finish_shot_ocr"] = 0.5 if pf_shot.exists() else 0.0

    # ---- 9b. play screenshots must differ ----
    diff_ok = 0.0
    try:
        from PIL import Image, ImageChops
        if pb_shot.exists() and pf_shot.exists():
            a = Image.open(pb_shot).convert("RGB").resize((128,96))
            b = Image.open(pf_shot).convert("RGB").resize((128,96))
            import numpy as np
            d = np.abs(np.asarray(a, dtype=int)-np.asarray(b, dtype=int)).mean()
            diff_ok = 1.0 if d >= 12.0 else 0.0
    except Exception: pass
    s["play_shots_distinct"] = diff_ok

    # ---- 10. runtime.log non-empty + has player/scene markers ----
    rl = rd/"runtime.log"
    rt_ok = 0.0
    if rl.exists() and rl.stat().st_size > 8:
        try:
            t = rl.read_text(errors="ignore").lower()
            needles = ["[player] ready", "[main] scene ready",
                       "godot engine v3.", "opengl es 2.0 renderer"]
            hits = sum(1 for k in needles if k in t)
            rt_ok = 1.0 if hits >= 3 else (0.5 if hits == 2 else 0.0)
        except Exception: pass
    s["runtime_log_ok"] = rt_ok

    # ---- 11. diff.txt sanity ----
    df = rd/"diff.txt"
    dlines = 0
    if df.exists():
        try: dlines = sum(1 for _ in df.open())
        except Exception: dlines = 0
    lo = expected.get("diff_min_lines", 6)
    hi = expected.get("diff_max_lines", 200)
    s["diff_in_range"] = 1.0 if lo <= dlines <= hi else 0.0

    # ---- 12. VLM rubric on the screenshots ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    play_imgs = [str(rd/n) for n in
        ["view_play_bug.png","view_play_finish.png","view_editor_after.png"]
        if (rd/n).exists()]
    if vlm_score_rubric and play_imgs:
        rubric = {
            "vlm_godot_real":     "图像确实是 Godot 3 编辑器或运行时窗口（含场景树/2D viewport/HUD），不是黑屏或主菜单",
            "vlm_geometry_clean": "fixed 场景的 PlayerSprite 有真实贴图（不是粉红 missing），GoalLabel 在窗口内可见",
            "vlm_finish_overlay": "通关截屏里能同时看到玩家贴图、地板和 GOAL 文字",
            "vlm_no_cheat":       "看上去是真实通过编辑器+运行通关的，不是把截图伪造或叠图",
        }
        vlm = vlm_score_rubric(play_imgs[:3], rubric,
                instruction="评估 Godot 3 场景修复 + 通关截图的真实性与可视一致性")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method","failed")
    else:
        for k in ["vlm_godot_real","vlm_geometry_clean",
                  "vlm_finish_overlay","vlm_no_cheat"]:
            s[k] = 0.5

    # ---- 12b. report.json structural + numeric ----
    rp = rd / "report.json"; rep_ok = 0.0
    if rp.exists():
        try:
            r = json.loads(rp.read_text())
            need = ["bugs_found","fixes_applied","extresource_id_after",
                    "label_margin_after","floor_extents_after",
                    "playthrough_finished","screenshots","runtime_log_lines"]
            if (all(k in r for k in need) and r.get("playthrough_finished")
                and int(r.get("extresource_id_after",-1)) in (1,3,4,5)
                and len(r.get("screenshots",[])) == 4):
                rep_ok = 1.0
        except Exception: pass
    s["report_json_ok"] = rep_ok

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums) if nums else 0.0
    cli_evidence = ((rd/"parse_before.json").exists()
                    and (rd/"bugs.json").exists()
                    and (rd/"diff.txt").exists())
    gui_screenshot = any((rd/n).exists() for n in
        ["view_editor_before.png","view_editor_after.png",
         "view_play_bug.png","view_play_finish.png"])
    vlm_avg = sum(s.get(k,0.0) for k in
        ["vlm_godot_real","vlm_geometry_clean",
         "vlm_finish_overlay","vlm_no_cheat"]) / 4.0
    if not cli_evidence:    base = min(base, 0.4)
    # GUI hard cap dropped: missing screenshots already penalised via per-shot sub-scores.
    # Match Prompt bullet "VLM 4 项 ≥ 0.6"; only enforce when the helper
    # actually ran, so missing _judge_helper does not silently penalise.
    if vlm_score_rubric is not None and vlm_avg < 0.6:
        base = min(base, 0.45)
    if s.get("fixed_tscn_parses",0) < 1.0: base = min(base, 0.5)
    if s.get("play_finish_shot_ocr",0) < 1.0: base = min(base, 0.7)
    if s.get("runtime_log_ok",0) < 1.0:        base = min(base, 0.55)
    if s.get("play_shots_distinct",0) < 1.0:   base = min(base, 0.6)
    if s.get("report_json_ok",0) < 1.0:        base = min(base, 0.6)
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
