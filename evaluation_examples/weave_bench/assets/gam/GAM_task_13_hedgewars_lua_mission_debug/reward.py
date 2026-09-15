# Auto-generated from WeaveBench task GAM_task_13_hedgewars_lua_mission_debug.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Hedgewars Lua training-mission repair + GUI playthrough verifier.

    Sub-scores (12) + 3 hard gates.  Real signal channels:
      - File: regex parse of the Lua script for AddTeam / AddAmmo /
              SpawnHealthCrate; numeric checks on team color hex,
              ammo counts, crate y coord.
      - GUI : 4 screenshots OCR for frontend / engine / finish overlay.
      - Run : engine.log captures stderr from hwengine.
    No GT leakage: gt/expected.json holds invariant counts only
    (e.g. number of bugs, OCR keyword set, map_max_y, diff bounds).
    """
    import json, os, re, subprocess
    from pathlib import Path

    ws  = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd  = ws / "results"
    work = ws / "work"
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
            need = {"map","theme","team","hogs","ammo","crates"}
            if (need.issubset(d.keys())
                and isinstance(d.get("crates"), list)
                and len(d["crates"]) == 3):
                schema_ok = 1
        except Exception: pass
    s["parse_before_schema"] = float(schema_ok)

    # ---- 2. bugs.json all 3 bugs detected with evidence ----
    bj = rd / "bugs.json"
    bugs_hit = 0
    if bj.exists():
        try:
            b = json.loads(bj.read_text())
            color_hex_gt    = str(expected.get("broken_team_color_hex", "FFFFFF")).upper()
            crate_idx_set   = expected.get("broken_crate_index_set", [1, 2])
            try: crate_idx_set = list(crate_idx_set)
            except Exception: crate_idx_set = [1, 2]
            offscreen_y_min = int(expected.get("map_max_landscape_y", 2048)) + 1
            for k, must in [
                ("bug_team_color_invisible", ["color_hex"]),
                ("bug_player_no_ammo",       ["weapons_with_zero"]),
                ("bug_crate_offscreen",      ["crate_index","y"]),
            ]:
                v = b.get(k, {})
                ok = bool(v.get("detected")) and all(m in v for m in must)
                if ok and k == "bug_team_color_invisible":
                    ok = color_hex_gt in str(v.get("color_hex","")).upper()
                if ok and k == "bug_player_no_ammo":
                    wz = [str(x).lower() for x in (v.get("weapons_with_zero") or [])]
                    ok = ("ambazooka" in wz) and ("amgrenade" in wz)
                if ok and k == "bug_crate_offscreen":
                    ok = (int(v.get("crate_index",-1)) in crate_idx_set) and \
                         int(v.get("y",0)) >= offscreen_y_min
                if ok: bugs_hit += 1
        except Exception: pass
    s["bugs_detected_with_evidence"] = bugs_hit / 3.0

    # ---- 3-6. fixed lua parses & invariants ----
    fixed_paths = [work/"scripts/CrateCrash_fixed.lua",
                   ws/"exec/scripts/CrateCrash_fixed.lua"]
    fixed = next((p for p in fixed_paths if p.exists()), None)
    luac_ok = color_ok = ammo_ok = crate_ok = 0.0
    txt = ""
    if fixed:
        try: txt = fixed.read_text(errors="ignore")
        except Exception: txt = ""
        try:
            r = subprocess.run(["luac","-p",str(fixed)],
                               capture_output=True, timeout=10)
            luac_ok = 1.0 if r.returncode == 0 else 0.0
        except Exception:
            # fallback: structural sanity
            if "function onGameInit" in txt and "AddTeam" in txt:
                luac_ok = 0.7
    s["fixed_lua_parses"] = luac_ok

    if txt:
        # Team color: AddTeam(<name>, 0xRRGGBB, ...)
        m = re.search(
            r"AddTeam\s*\(\s*[^,]+,\s*0x([0-9A-Fa-f]{6})\b", txt)
        if m:
            hx = int(m.group(1), 16)
            white = 0xFFFFFF
            # crude colour distance: how far each channel from 0xFF
            dr = abs(((hx>>16)&0xFF) - 0xFF)
            dg = abs(((hx>>8 )&0xFF) - 0xFF)
            db = abs(((hx    )&0xFF) - 0xFF)
            if (dr + dg + db) >= 0x180:  # ≥ ~half-white in L1
                near_white  = (dr + dg + db) < 0x240
                chan_dark   = max((hx>>16)&0xFF,(hx>>8)&0xFF,hx&0xFF) < 0xC0
                if (not near_white) and chan_dark:
                    color_ok = 1.0
        # Ammo counts for amBazooka and amGrenade
        baz = re.search(
            r"AddAmmo\s*\(\s*\w+\s*,\s*amBazooka\s*,\s*(\d+)\s*\)", txt)
        gre = re.search(
            r"AddAmmo\s*\(\s*\w+\s*,\s*amGrenade\s*,\s*(\d+)\s*\)", txt)
        if baz and gre and int(baz.group(1)) >= 5 and int(gre.group(1)) >= 5:
            ammo_ok = 1.0
        # Crates: collect all SpawnHealthCrate(x, y) in order
        crates = [(int(a), int(b)) for a,b in re.findall(
            r"SpawnHealthCrate\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", txt)]
        max_y = expected.get("map_max_landscape_y", 2048)
        if (len(crates) >= 3
            and 0 <= crates[1][1] <= max_y
            and 0 <= crates[0][1] <= max_y
            and 0 <= crates[2][1] <= max_y):
            crate_ok = 1.0
    s["fixed_team_color"]    = color_ok
    s["fixed_ammo_counts"]   = ammo_ok
    s["fixed_crates_in_map"] = crate_ok

    # ---- 7. frontend screenshots present + OCR ----
    def _is_real_capture(p):
        # Content-based realness check: any non-trivial PNG ≥ 800×600 with
        # enough colour diversity counts as real. Drops the previous narrow
        # resolution whitelist that rejected legitimate KasmVNC screenshots
        # at non-standard sizes (e.g. 1024×768, 1366×768).
        try:
            from PIL import Image
            im = Image.open(p); w, h = im.size
            if w < 800 or h < 600:
                return False
            try:
                import collections
                px = list(im.convert("RGB").resize((64, 64)).getdata())
                return len(collections.Counter(px)) >= 200
            except Exception:
                return True
        except Exception:
            return False
    shots_fe = ["view_frontend.png","view_frontend_after.png"]
    fe_present = sum(1 for n in shots_fe if (rd/n).exists() and _is_real_capture(rd/n))
    s["frontend_shots_present"] = fe_present / 2.0
    fe_kw = expected.get("frontend_keywords",
        ["training","mission","crash","course","crate","play","single"])
    try:
        import pytesseract
        from PIL import Image
        fe_ocr_hits = 0
        for n in shots_fe:
            p = rd/n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p)).lower()
                    if any(k in tx for k in fe_kw):
                        fe_ocr_hits += 1
                except Exception: pass
        s["frontend_shots_ocr"] = fe_ocr_hits / 2.0
    except ImportError:
        s["frontend_shots_ocr"] = 0.5

    # ---- 8. play bug screenshot present + OCR ----
    pb_shot = rd/"view_play_bug.png"
    s["play_bug_shot_present"] = 1.0 if (pb_shot.exists() and _is_real_capture(pb_shot)) else 0.0
    eng_kw = expected.get("engine_keywords",
        ["trainee","rookie","crates","bazooka","ammo"])
    try:
        import pytesseract
        from PIL import Image
        if pb_shot.exists():
            try:
                tx = pytesseract.image_to_string(Image.open(pb_shot)).lower()
            except Exception:
                tx = ""
            hits = sum(1 for k in eng_kw if k in tx)
            s["play_bug_shot_hud_ocr"] = 1.0 if hits >= 1 else 0.0
        else:
            s["play_bug_shot_hud_ocr"] = 0.0
    except ImportError:
        s["play_bug_shot_hud_ocr"] = 0.5 if pb_shot.exists() else 0.0

    # ---- 9. play finish screenshot present + OCR ----
    pf_shot = rd/"view_play_finish.png"
    s["play_finish_shot_present"] = 1.0 if (pf_shot.exists() and _is_real_capture(pf_shot)) else 0.0
    fin_kw = expected.get("complete_keywords",
        ["mission complete","all crates collected","you won"])
    try:
        import pytesseract
        from PIL import Image
        if pf_shot.exists():
            try:
                tx = pytesseract.image_to_string(Image.open(pf_shot)).lower()
            except Exception:
                tx = ""
            s["play_finish_shot_ocr"] = 1.0 if any(k in tx for k in fin_kw) else 0.0
        else:
            s["play_finish_shot_ocr"] = 0.0
    except ImportError:
        s["play_finish_shot_ocr"] = 0.5 if pf_shot.exists() else 0.0

    # ---- 10. engine.log non-empty + has team / ammo markers ----
    el = rd/"engine.log"
    el_ok = 0.0
    if el.exists() and el.stat().st_size > 8:
        try:
            t = el.read_text(errors="ignore").lower()
            hits = sum(1 for k in ["trainee","rookie","ammo","bazooka"] if k in t)
            real_markers = sum(1 for k in
                ["hwengine","sdl","opengl","loading script","gameflags","seed ","fps:"]
                if k in t)
            el_ok = 1.0 if (hits>=2 and real_markers>=2 and el.stat().st_size>=512) else 0.0
        except Exception: pass
    s["engine_log_ok"] = el_ok

    # ---- 11. diff.txt sanity ----
    df = rd/"diff.txt"
    dlines = 0
    if df.exists():
        try: dlines = sum(1 for _ in df.open())
        except Exception: dlines = 0
    lo = expected.get("diff_min_lines", 6)
    hi = expected.get("diff_max_lines", 200)
    s["diff_in_range"] = 1.0 if lo <= dlines <= hi else 0.0

    # ---- 11b. report.json structural validation (Prompt deliverable #12) ----
    rp = rd / "report.json"; rep_ok = 0.0
    if rp.exists():
        try:
            r = json.loads(rp.read_text())
            need = ["bugs_found", "fixes_applied", "team_color_after",
                    "ammo_after", "crates_after", "playthrough_finished",
                    "screenshots", "engine_log_lines"]
            present = sum(1 for k in need if k in r)
            if (present == len(need)
                and r.get("playthrough_finished")
                and isinstance(r.get("screenshots"), list)
                and len(r.get("screenshots", [])) >= 4):
                rep_ok = 1.0
            elif present >= max(4, len(need) - 2):
                rep_ok = 0.5
        except Exception:
            pass
    s["report_json_ok"] = rep_ok

    # ---- 12. VLM rubric on the screenshots ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    play_imgs = [str(rd/n) for n in
        ["view_play_bug.png","view_play_finish.png","view_frontend_after.png"]
        if (rd/n).exists()]
    if vlm_score_rubric and play_imgs:
        rubric = {
            "vlm_hedgewars_real": "图像确实是 Hedgewars 前端或战斗画面（含菜单 / 小刺猬 / HUD 弹药面板），不是黑屏或主菜单 placeholder",
            "vlm_team_visible":   "fixed 后小刺猬名牌 / 帽子 在 Bamboo 雪地背景下是可见的 (颜色对比明显)",
            "vlm_finish_overlay": "通关截屏里能看到 Mission complete / All crates collected / You won 之类提示",
            "vlm_no_cheat":       "看上去是真实通过前端+引擎通关的，不是把 Demo 文件伪造或叠图",
        }
        vlm = vlm_score_rubric(play_imgs[:3], rubric,
                instruction="评估 Hedgewars 训练任务修复 + 通关截图的真实性与可视一致性")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method","failed")
    else:
        for k in ["vlm_hedgewars_real","vlm_team_visible",
                  "vlm_finish_overlay","vlm_no_cheat"]:
            s[k] = 0.5

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums) if nums else 0.0
    cli_evidence = ((rd/"parse_before.json").exists()
                    and (rd/"bugs.json").exists()
                    and (rd/"diff.txt").exists())
    gui_screenshot = any((rd/n).exists() for n in
        ["view_frontend.png","view_frontend_after.png",
         "view_play_bug.png","view_play_finish.png"])
    vlm_avg = sum(s.get(k,0.0) for k in
        ["vlm_hedgewars_real","vlm_team_visible",
         "vlm_finish_overlay","vlm_no_cheat"]) / 4.0
    if not cli_evidence:    base = min(base, 0.4)
    # GUI hard cap dropped: missing screenshots already penalised via per-shot sub-scores.
    # Only enforce VLM caps when the helper actually ran (otherwise the
    # 0.5 fallback would cap at 0.4 even though no rubric was applied).
    if vlm_score_rubric is not None and vlm_avg < 0.6:
        base = min(base, 0.4)
    if vlm_score_rubric is not None and s.get("vlm_no_cheat",0.0) < 0.5:
        base = min(base, 0.35)
    if s.get("fixed_lua_parses",0) < 1.0: base = min(base, 0.5)
    if s.get("play_finish_shot_ocr",0)<1.0: base = min(base, 0.45)
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
