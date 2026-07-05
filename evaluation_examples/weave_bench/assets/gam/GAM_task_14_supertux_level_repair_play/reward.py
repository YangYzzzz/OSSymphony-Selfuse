# Auto-generated from WeaveBench task GAM_task_14_supertux_level_repair_play.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """SuperTux level S-expr repair + GUI playthrough verifier.

    Sub-scores (12) + 3 hard gates.  Real signal channels:
      - File: sexpdata.loads parses fixed.stl + tilemap stride math.
      - GUI : 4 screenshots OCR for editor / play / finish overlay.
      - Save: ~/.local/share/supertux2/profile1/state excerpt.
    No GT leakage: gt/expected.json holds invariant counts only
    (e.g. number of bugs, OCR keyword set, diff line bounds).
    """
    import json, os, re, subprocess
    from pathlib import Path

    ws  = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd  = ws / "results"
    lvl = ws / "levels"
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
            need = {"sector_size","tilemaps","objects","spawnpoints"}
            if need.issubset(d.keys()): schema_ok = 1
        except Exception: pass
    s["parse_before_schema"] = float(schema_ok)

    # ---- 2. bugs.json all 3 bugs detected with evidence ----
    bj = rd / "bugs.json"
    bugs_hit = 0
    if bj.exists():
        try:
            b = json.loads(bj.read_text())
            for k, must in [
                ("bug_tilemap_stride",   ["declared_width","actual_row_stride"]),
                ("bug_firefly_oob",      ["firefly_xy","sector_size"]),
                ("bug_infoblock_buried", ["infoblock_xy","tile_id_under"]),
            ]:
                v = b.get(k, {})
                if v.get("detected") and all(m in v for m in must):
                    bugs_hit += 1
        except Exception: pass
    s["bugs_detected_with_evidence"] = bugs_hit / 3.0

    # ---- 3 + 4 + 5 + 6. fixed.stl must parse & invariants ----
    fixed = lvl / "fixed.stl"
    parses = stride_ok = firefly_ok = info_ok = 0.0
    fxd_data = None
    if fixed.exists():
        try:
            import sexpdata
            txt = fixed.read_text()
            fxd_data = sexpdata.loads(txt)
            parses = 1.0
        except Exception:
            parses = 0.0
    s["fixed_stl_parses"] = parses

    def _walk(node):
        if isinstance(node, list):
            yield node
            for c in node:
                yield from _walk(c)

    def _name(node):
        if isinstance(node, list) and node and hasattr(node[0], "value"):
            try: return node[0].value()
            except Exception: return None
        return None

    if fxd_data is not None:
        sector_w = sector_h = None
        firefly_xy = None
        infoblock_xy = None
        main_tilemap = None
        for n in _walk(fxd_data):
            if _name(n) == "sector":
                for c in n[1:]:
                    if _name(c) == "size" and len(c) >= 3:
                        try: sector_w, sector_h = int(c[1]), int(c[2])
                        except Exception: pass
                    if _name(c) == "tilemap":
                        # treat the largest tilemap as "main"
                        w = h = None; tcount = 0; zpos = 0
                        for cc in c[1:]:
                            if _name(cc)=="width"  and len(cc)>=2: w = int(cc[1])
                            if _name(cc)=="height" and len(cc)>=2: h = int(cc[1])
                            if _name(cc)=="z-pos"  and len(cc)>=2:
                                try: zpos = int(cc[1])
                                except Exception: zpos = 0
                            if _name(cc)=="tiles":
                                tcount = max(tcount, len(cc)-1)
                        if w and h and (main_tilemap is None
                                        or (w*h) > main_tilemap[0]*main_tilemap[1]):
                            main_tilemap = (w, h, tcount, zpos)
                    if _name(c) == "firefly":
                        for cc in c[1:]:
                            if _name(cc)=="x" and len(cc)>=2: fx = float(cc[1])
                            if _name(cc)=="y" and len(cc)>=2: fy = float(cc[1])
                        try: firefly_xy = (fx, fy)
                        except Exception: pass
                    if _name(c) == "infoblock":
                        for cc in c[1:]:
                            if _name(cc)=="x" and len(cc)>=2: ix = float(cc[1])
                            if _name(cc)=="y" and len(cc)>=2: iy = float(cc[1])
                        try: infoblock_xy = (ix, iy)
                        except Exception: pass
        if main_tilemap:
            w, h, tc, _ = main_tilemap
            stride_ok = 1.0 if tc == w * h else 0.0
        if sector_w and sector_h and firefly_xy:
            fx, fy = firefly_xy
            if 0 <= fx < sector_w*32 and 0 <= fy < sector_h*32:
                firefly_ok = 1.0
        if infoblock_xy and main_tilemap:
            ix, iy = infoblock_xy
            w, h, _, _ = main_tilemap
            col, row = int(ix)//32, int(iy)//32
            tiles = next((cc[1:] for n in _walk(fxd_data) if _name(n)=="tilemap"
                          for cc in n[1:] if _name(cc)=="tiles"), [])
            idx = row*w + col
            if 0 <= idx < len(tiles):
                try: info_ok = 1.0 if int(tiles[idx]) == 0 else 0.0
                except Exception: info_ok = 0.0
        # parse_after.json may also assert tile_id_under == 0
        pa = rd / "parse_after.json"
        if pa.exists():
            try:
                pad = json.loads(pa.read_text())
                if any(o.get("kind")=="infoblock"
                       and o.get("tile_id_under", 1) == 0
                       for o in pad.get("objects", [])):
                    info_ok = 1.0
            except Exception: pass
    s["fixed_tilemap_stride"]    = stride_ok
    s["fixed_firefly_in_bounds"] = firefly_ok
    s["fixed_infoblock_air"]     = info_ok

    # ---- 7. editor screenshots present + OCR ----
    shots_editor = ["view_editor_before.png","view_editor_after.png"]
    editor_present = sum(1 for n in shots_editor if (rd/n).exists())
    s["editor_shots_present"] = editor_present / 2.0
    try:
        import pytesseract
        from PIL import Image
        editor_ocr_hits = 0
        for n in shots_editor:
            p = rd/n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p)).lower()
                    edit_kw = expected.get("editor_keywords",["sector: main","tilemap","tileset"])
                    if sum(1 for k in edit_kw if k in tx) >= 2:
                        editor_ocr_hits += 1
                except Exception: pass
        s["editor_shots_ocr"] = editor_ocr_hits / 2.0
    except ImportError:
        s["editor_shots_ocr"] = 0.5

    # ---- 8. play bug screenshot present + OCR HUD ----
    pb_shot = rd/"view_play_bug.png"
    s["play_bug_shot_present"] = 1.0 if pb_shot.exists() else 0.0
    try:
        import pytesseract
        from PIL import Image
        if pb_shot.exists():
            try:
                tx = pytesseract.image_to_string(Image.open(pb_shot)).lower()
            except Exception:
                tx = ""
            hud_kw = expected.get("hud_keywords", ["coins:","time:","score:"])
            hits = sum(1 for k in hud_kw if k in tx)
            s["play_bug_shot_hud_ocr"] = 1.0 if hits >= 1 else 0.0
        else:
            s["play_bug_shot_hud_ocr"] = 0.0
    except ImportError:
        s["play_bug_shot_hud_ocr"] = 0.5 if pb_shot.exists() else 0.0

    # ---- 9. play finish screenshot OCR ----
    pf_shot = rd/"view_play_finish.png"
    s["play_finish_shot_present"] = 1.0 if pf_shot.exists() else 0.0
    finish_kw = expected.get("finish_keywords", ["level finished","you got"])
    try:
        import pytesseract
        from PIL import Image
        if pf_shot.exists():
            try:
                tx = pytesseract.image_to_string(Image.open(pf_shot)).lower()
            except Exception:
                tx = ""
            s["play_finish_shot_ocr"] = 1.0 if any(k in tx for k in finish_kw) else 0.0
        else:
            s["play_finish_shot_ocr"] = 0.0
    except ImportError:
        s["play_finish_shot_ocr"] = 0.5 if pf_shot.exists() else 0.0

    # ---- 10. save_excerpt.sexp parses + non-empty ----
    se = rd/"save_excerpt.sexp"
    save_ok = 0.0
    if se.exists() and se.stat().st_size > 8:
        try:
            import sexpdata
            parsed = sexpdata.loads("(" + se.read_text() + ")")
            raw = se.read_text().lower()
            needs = ["level-progress", "fixed.stl", "(state", "(name"]
            if (isinstance(parsed, list) and len(parsed) >= 1
                and all(t in raw for t in needs)):
                save_ok = 1.0
        except Exception:
            try:
                import sexpdata
                sexpdata.loads(se.read_text())
                save_ok = 0.7
            except Exception: pass
    s["save_state_excerpt_ok"] = save_ok

    # ---- 11. diff.txt sanity ----
    df = rd/"diff.txt"
    dlines = 0
    if df.exists():
        try: dlines = sum(1 for _ in df.open())
        except Exception: dlines = 0
    lo = expected.get("diff_min_lines", 6)
    hi = expected.get("diff_max_lines", 200)
    s["diff_in_range"] = 1.0 if lo <= dlines <= hi else 0.0

    # ---- 12. VLM rubric on the two play screenshots ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    play_imgs = [str(rd/n) for n in ["view_play_bug.png","view_play_finish.png",
                                      "view_editor_after.png"] if (rd/n).exists()]
    if vlm_score_rubric and play_imgs:
        rubric = {
            "vlm_supertux_real":  "图像确实是 SuperTux 游戏画面（含 Tux 角色 / 砖块 / HUD），不是黑屏或主菜单",
            "vlm_geometry_clean": "fixed 关卡的 tilemap 在编辑器视图里平整无错位，firefly 终点可见且贴近地面",
            "vlm_finish_overlay": "通关截屏里能看到 Level Finished / Bonus / 通关弹窗的提示文字",
            "vlm_no_cheat":       "看上去是真实通过编辑器+试玩通关的，不是把存档伪造或贴图覆盖",
        }
        vlm = vlm_score_rubric(play_imgs[:3], rubric,
                instruction="评估 SuperTux 关卡修复 + 通关截图的真实性与几何整齐度")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method","failed")
    else:
        for k in ["vlm_supertux_real","vlm_geometry_clean",
                  "vlm_finish_overlay","vlm_no_cheat"]:
            s[k] = 0.0
        s["judge_method"] = "unavailable"

    # ---- distinct screenshots + report.json cross-check ----
    import hashlib
    shots = ["view_editor_before.png","view_editor_after.png",
             "view_play_bug.png","view_play_finish.png"]
    hs = {hashlib.md5((rd/n).read_bytes()).hexdigest()
          for n in shots if (rd/n).exists()}
    s["shots_distinct"] = 1.0 if len(hs) == 4 else 0.0
    rp = rd/"report.json"
    ok = False
    if rp.exists():
        try:
            r = json.loads(rp.read_text())
            ok = (r.get("playthrough_finished") is True
                  and set(r.get("screenshots",[])) >= set(shots))
        except Exception: pass
    s["report_json_ok"] = 1.0 if ok else 0.0

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums) if nums else 0.0
    cli_evidence = (rd/"parse_before.json").exists() and (rd/"bugs.json").exists() \
                   and (rd/"diff.txt").exists()
    gui_screenshot = any((rd/n).exists() for n in
        ["view_editor_before.png","view_editor_after.png",
         "view_play_bug.png","view_play_finish.png"])
    vlm_avg = sum(s.get(k,0.0) for k in
        ["vlm_supertux_real","vlm_geometry_clean",
         "vlm_finish_overlay","vlm_no_cheat"]) / 4.0
    if not cli_evidence:    base = min(base, 0.4)
    # GUI hard cap dropped: missing screenshots already penalised via per-shot sub-scores.
    if vlm_score_rubric is not None and vlm_avg < 0.6:
        base = min(base, 0.45)
    if s.get("fixed_stl_parses",0) < 1.0: base = min(base, 0.4)
    if s.get("play_finish_shot_ocr",0) < 1.0: base = min(base, 0.5)
    if s.get("save_state_excerpt_ok",0) < 1.0: base = min(base, 0.55)
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
