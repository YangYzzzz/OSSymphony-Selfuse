# Auto-generated from WeaveBench task GAM_task_15_xmoto_level_xml_repair_ride.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """X-Moto level XML repair + GUI ride + SQLite forensics verifier.

    Sub-scores (12) + 3 hard gates.  Channels:
      - File: lxml parse + shoelace winding + entity inventory.
      - GUI : 4 screenshots OCR for menu / ride-bug / ride-finish.
      - DB  : sqlite3 query of stats_levels for nbCompleted >= 1.
    No GT leakage: gt/expected.json carries only invariant counts &
    keyword sets, never specific patched coordinates.
    """
    import json, sqlite3, subprocess, glob, os, re
    from pathlib import Path

    ws = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = ws / "results"
    lvl_dir = ws / "Levels"
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
            need = {"level_size","blocks","entities"}
            blk_need = {"id","background","vertices","winding_signed_area"}
            ent_need = {"id","type_id","x","y","inside_block_id"}
            if need.issubset(d.keys()) and isinstance(d["blocks"], list) \
               and len(d["blocks"]) == expected.get("broken_block_count", 5) \
               and all(blk_need.issubset(b) for b in d["blocks"]) \
               and isinstance(d["entities"], list) and d["entities"] \
               and all(ent_need.issubset(e) for e in d["entities"]):
                schema_ok = 1
        except Exception: pass
    s["parse_before_schema"] = float(schema_ok)

    # ---- 2. bugs.json all 3 bugs detected with evidence ----
    # Semantic checks only — we verify the SHAPE of the bug evidence
    # (correct sign / correct missing entity / correct point-in-poly)
    # rather than requiring the agent to match a literal block id from
    # gt/expected.json. The exact id is still useful as a tie-breaker
    # when present, but absence of the id field no longer zeros the bug.
    bj = rd / "bugs.json"
    bugs_hit = 0
    if bj.exists():
        try:
            b = json.loads(bj.read_text())
            v = b.get("bug_block_winding", {})
            gt_winding_id = expected.get("broken_winding_negative_block_id")
            if (v.get("detected") and "block_id" in v
                and isinstance(v.get("signed_area"), (int, float))
                and v["signed_area"] < 0
                and (gt_winding_id is None or v.get("block_id") == gt_winding_id
                     or "block_id" in v)):
                bugs_hit += 1
            v = b.get("bug_no_end_of_level", {})
            if v.get("detected") and isinstance(v.get("entity_types_present"), list) \
               and "EndOfLevel" not in v["entity_types_present"]: bugs_hit += 1
            v = b.get("bug_strawberry_in_block", {})
            gt_host_block = expected.get("broken_strawberry_host_block")
            if (v.get("detected") and "host_block_id" in v
                and (gt_host_block is None or v.get("host_block_id") == gt_host_block
                     or "host_block_id" in v)):
                bugs_hit += 1
        except Exception: pass
    s["bugs_detected_with_evidence"] = bugs_hit / 3.0

    # ---- 3 + 4 + 5 + 6. fixed.lvl invariants ----
    fixed = lvl_dir / "fixed.lvl"
    xmllint_ok = winding_ok = end_count_ok = strawberry_ok = 0.0
    fixed_blocks = []
    fixed_entities = []
    if fixed.exists():
        # xmllint
        try:
            r = subprocess.run(["xmllint","--noout",str(fixed)],
                               capture_output=True, timeout=10)
            xmllint_ok = 1.0 if r.returncode == 0 else 0.0
        except Exception: pass
        # parse with lxml
        try:
            from lxml import etree
            tree = etree.parse(str(fixed))
            root = tree.getroot()
            for blk in root.iter("block"):
                bg = (blk.get("background","false") == "true")
                pts = []
                for v in blk.iter("vertex"):
                    try: pts.append((float(v.get("x","0")), float(v.get("y","0"))))
                    except Exception: pass
                # shoelace
                area = 0.0
                for i in range(len(pts)):
                    x1,y1 = pts[i]; x2,y2 = pts[(i+1)%len(pts)]
                    area += x1*y2 - x2*y1
                area /= 2.0
                fixed_blocks.append({"id": blk.get("id",""),
                                     "background": bg,
                                     "vertices": pts,
                                     "area": area})
            for ent in root.iter("entity"):
                tid = ent.get("typeid","")
                pos = ent.find("position")
                x = float(pos.get("x","0")) if pos is not None else 0.0
                y = float(pos.get("y","0")) if pos is not None else 0.0
                fixed_entities.append({"id": ent.get("id",""),
                                       "typeid": tid, "x": x, "y": y})
        except Exception: pass
    # winding: all non-background blocks have area >= 0
    nbg = [b for b in fixed_blocks if not b["background"]]
    if nbg:
        winding_ok = 1.0 if all(b["area"] >= 0 for b in nbg) else 0.0
    s["fixed_xmllint_ok"]            = xmllint_ok
    s["fixed_blocks_winding_ok"]     = winding_ok
    # exactly 1 EndOfLevel
    end_n = sum(1 for e in fixed_entities if e["typeid"] == "EndOfLevel")
    end_count_ok = 1.0 if end_n == 1 else 0.0
    s["fixed_endoflevel_count_ok"] = end_count_ok
    # strawberry not in any block (point-in-polygon test)
    def _point_in_poly(px, py, poly):
        n = len(poly); inside = False
        if n < 3: return False
        j = n - 1
        for i in range(n):
            xi, yi = poly[i]; xj, yj = poly[j]
            if ((yi > py) != (yj > py)) and \
               (px < (xj - xi)*(py - yi)/((yj - yi) or 1e-9) + xi):
                inside = not inside
            j = i
        return inside
    straws = [e for e in fixed_entities if e["typeid"] == "Strawberry"]
    if straws:
        good = 0
        for e in straws:
            in_any = False
            for b in nbg:
                if _point_in_poly(e["x"], e["y"], b["vertices"]):
                    in_any = True; break
            if not in_any: good += 1
        strawberry_ok = good / len(straws)
    s["fixed_strawberry_outside"] = strawberry_ok

    # ---- 7. menu screenshots present + OCR ----
    menu_shots = ["view_xmoto_menu.png","view_xmoto_menu_fixed.png"]
    menu_present = sum(1 for n in menu_shots if (rd/n).exists())
    s["menu_shots_present"] = menu_present / 2.0
    menu_kw = expected.get("menu_keywords",
        ["levels","play","x-moto","xmoto","custom","external","best"])
    try:
        import pytesseract
        from PIL import Image
        hits = 0
        for n in menu_shots:
            p = rd/n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p)).lower()
                    if any(k in tx for k in menu_kw): hits += 1
                except Exception: pass
        s["menu_shots_ocr"] = hits / 2.0
    except ImportError:
        s["menu_shots_ocr"] = 0.0

    # ---- 8. ride-bug screenshot present ----
    # 50 KB floor (Prompt 第 6 项: "真实游戏画面"). PNG of an X-Moto window
    # at typical 800×600+ ride view comfortably exceeds 50 KB; smaller
    # files are flagged as likely placeholder/blank.
    rb = rd / "view_ride_bug.png"
    s["ride_bug_shot_present"] = 1.0 if rb.exists() and rb.stat().st_size > 50_000 else 0.0
    try:
        import pytesseract
        from PIL import Image
        if rb.exists():
            try:
                tx = pytesseract.image_to_string(Image.open(rb)).lower()
            except Exception:
                tx = ""
            hud = expected.get("ride_hud_keywords",
                ["time","strawberries","wrecker","fps","x-moto","00:"])
            s["ride_bug_shot_hud_ocr"] = 1.0 if any(k in tx for k in hud) else 0.0
        else:
            s["ride_bug_shot_hud_ocr"] = 0.0
    except ImportError:
        s["ride_bug_shot_hud_ocr"] = 0.0

    # ---- 9. ride-finish screenshot OCR ----
    rf = rd / "view_ride_finish.png"
    s["ride_finish_shot_present"] = 1.0 if rf.exists() else 0.0
    finish_kw = expected.get("finish_keywords",
        ["finished","best time","replay","time:","level","completed"])
    try:
        import pytesseract
        from PIL import Image
        if rf.exists():
            try:
                tx = pytesseract.image_to_string(Image.open(rf)).lower()
            except Exception:
                tx = ""
            s["ride_finish_shot_ocr"] = 1.0 if any(k in tx for k in finish_kw) else 0.0
        else:
            s["ride_finish_shot_ocr"] = 0.0
    except ImportError:
        s["ride_finish_shot_ocr"] = 0.0

    # ---- 10. SQLite stats: fixed_level_completed >= 1 ----
    sj = rd / "sqlite_stats.json"
    sql_ok = 0.0
    sql_completed = 0
    if sj.exists():
        try:
            d = json.loads(sj.read_text())
            sql_completed = int(d.get("fixed_level_completed", 0))
            if sql_completed >= 1 and isinstance(d.get("tables"), list):
                sql_ok = 1.0
            elif d.get("tables"):
                sql_ok = 0.4
        except Exception: pass
    # also try the live DB if accessible (best-effort, no failure)
    if sql_ok < 1.0:
        cands = []
        for pat in ["~/.local/share/xmoto/*.db", "~/.xmoto/*.db",
                    "/root/.local/share/xmoto/*.db"]:
            cands += glob.glob(os.path.expanduser(pat))
        for db in cands:
            try:
                con = sqlite3.connect(db); cur = con.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tabs = [r[0] for r in cur.fetchall()]
                if "stats_levels" in tabs:
                    cur.execute("SELECT SUM(nbCompleted) FROM stats_levels")
                    n = cur.fetchone()[0] or 0
                    if n >= 1: sql_ok = max(sql_ok, 0.8)
                con.close()
            except Exception: pass
    s["sqlite_completed_evidence"] = sql_ok

    # ---- 11. diff.txt sanity ----
    df = rd / "diff.txt"
    lo = expected.get("diff_min_lines", 8)
    hi = expected.get("diff_max_lines", 250)
    txt = df.read_text(errors="ignore") if df.exists() else ""
    dlines = txt.count("\n")
    has_unified = ("---" in txt and "+++" in txt and "@@" in txt)
    # Unified-diff markers boost to full credit, but a plain in-range diff
    # still counts (Prompt only mandates the line range).
    if lo <= dlines <= hi:
        s["diff_in_range"] = 1.0 if has_unified else 0.7
    else:
        s["diff_in_range"] = 0.0

    # ---- 11b. report.json structural validation (Prompt deliverable #12) ----
    rp = rd / "report.json"; rep_ok = 0.0
    if rp.exists():
        try:
            r = json.loads(rp.read_text())
            need = ["bugs_found", "fixes_applied", "blocks_after",
                    "endoflevel_after", "strawberries_after",
                    "playthrough_finished", "screenshots", "sqlite_completed"]
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

    # ---- 12. VLM rubric on the ride screenshots ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    imgs = [str(rd/n) for n in
        ["view_ride_bug.png","view_ride_finish.png","view_xmoto_menu_fixed.png"]
        if (rd/n).exists()]
    if vlm_score_rubric and imgs:
        rubric = {
            "vlm_xmoto_real":      "图像确实是 X-Moto 游戏画面（含摩托车 / 地形 / HUD），不是黑屏或加载页",
            "vlm_geometry_clean":  "fixed 关卡的地形看起来连续平整、没有鬼地面穿透，EndOfLevel 标志可见",
            "vlm_finish_overlay":  "通关截屏含 Finished / Best time / Replay / Time 之类提示",
            "vlm_no_cheat":        "看上去是真实骑车通关，不是把存档或截屏拼接出来的",
        }
        vlm = vlm_score_rubric(imgs[:3], rubric,
                instruction="评估 X-Moto 关卡修复 + 实战通关截图的真实性与几何整齐度")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method","failed")
    else:
        for k in ["vlm_xmoto_real","vlm_geometry_clean",
                  "vlm_finish_overlay","vlm_no_cheat"]:
            s[k] = 0.5
        s["judge_method"] = "unavailable"

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums) if nums else 0.0
    cli_evidence = (rd/"parse_before.json").exists() and (rd/"bugs.json").exists() \
                   and (rd/"sqlite_stats.json").exists() and (rd/"diff.txt").exists()
    gui_screenshot = any((rd/n).exists() for n in
        ["view_xmoto_menu.png","view_xmoto_menu_fixed.png",
         "view_ride_bug.png","view_ride_finish.png"])
    vlm_avg = sum(s.get(k,0.0) for k in
        ["vlm_xmoto_real","vlm_geometry_clean",
         "vlm_finish_overlay","vlm_no_cheat"]) / 4.0
    if not cli_evidence:    base = min(base, 0.4)
    # GUI hard cap dropped: missing screenshots already penalised via per-shot sub-scores.
    # Only enforce VLM cap when the helper actually ran.
    if vlm_score_rubric is not None and vlm_avg < 0.6:
        base = min(base, 0.45)
    if s.get("fixed_xmllint_ok",0) < 1.0: base = min(base, 0.4)
    if s.get("ride_finish_shot_ocr",0) < 1.0: base = min(base, 0.55)
    if s.get("sqlite_completed_evidence",0) < 0.5: base = min(base, 0.50)
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
