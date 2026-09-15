# Auto-generated from WeaveBench task GAM_task_16_kmahjongg_pair_solver.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """KMahjongg layout repair + screenshot tile-face clustering +
    KConfig forensics verifier.

    8–15 sub-scores + 3 hard gates.  Channels:
      - File   : KConfig `.layout` parse + 2×2 corner integrity check.
      - Pixel  : screenshot + per-tile patch phash clustering, OCR HUD.
      - Plan   : pair plan vs face_cluster consistency.
      - Config : kmahjonggrc grep for Layout / GameNumber + savegame.
    No GT leakage: gt/expected.json carries only invariant counts &
    keyword sets; never the patched grid.
    """
    import json, os, re, subprocess, glob
    from pathlib import Path

    ws = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = ws / "results"
    lay_dir = ws / "layouts"
    gt_dir = ws / "gt"
    expected = {}
    if (gt_dir / "expected.json").exists():
        try:    expected = json.loads((gt_dir/"expected.json").read_text())
        except Exception: expected = {}
    s = {}

    # ---- 1. parse_before schema + anomalies non-empty ----
    pb = rd / "parse_before.json"
    pb_ok = 0.0
    if pb.exists():
        try:
            d = json.loads(pb.read_text())
            need = {"header","tiles","tile_count","anomalies"}
            an = d.get("anomalies", {})
            non_empty = (an.get("orphan_corners") and
                         an.get("stacked_collisions") and
                         an.get("tile_count_odd") is True)
            if need.issubset(d.keys()) and non_empty:
                pb_ok = 1.0
            elif need.issubset(d.keys()):
                pb_ok = 0.4
        except Exception: pass
    s["parse_before_complete"] = pb_ok

    # ---- 2. bugs.json three bugs ----
    bj = rd / "bugs.json"
    bugs_hit = 0
    if bj.exists():
        try:
            b = json.loads(bj.read_text())
            for k, must in [
                ("bug_orphan_corner",     ["examples"]),
                ("bug_odd_tile_count",    ["tile_count"]),
                ("bug_stacked_collision", ["positions"]),
            ]:
                v = b.get(k, {})
                if v.get("detected") and v.get(must[0]):
                    if isinstance(v.get(must[0]), list):
                        if len(v.get(must[0])) >= 1: bugs_hit += 1
                    else:
                        bugs_hit += 1
        except Exception: pass
    s["bugs_three_with_evidence"] = bugs_hit / 3.0

    # ---- 3 + 4. fixed_dragon.layout structural invariants ----
    fixed = lay_dir / "fixed_dragon.layout"
    tile_count = 0
    orphan_n = collide_n = -1
    head_ok = 0.0
    if fixed.exists():
        try:
            txt = fixed.read_text(errors="ignore")
            if txt.lstrip().startswith("[KMahjonggLayout]"):
                head_ok = 1.0
            # quick parser: extract E1..EN blocks
            depth = int(re.search(r"^Depth\s*=\s*(\d+)", txt, re.M).group(1)) \
                    if re.search(r"^Depth\s*=\s*(\d+)", txt, re.M) else 5
            tiles = {}     # (z,x,y) of upper-left corner
            orphan_local = []
            for z in range(1, depth+1):
                m = re.search(rf"^E{z}\d*\s*=\s*(.+(?:\n[^=\[]+)*)",
                              txt, re.M)
                if not m: continue
                rows = [r for r in m.group(1).splitlines() if r.strip()]
                for y,row in enumerate(rows):
                    for x,ch in enumerate(row):
                        if ch in "1234":
                            tiles.setdefault((z,x,y), ch)
            # check 2x2 integrity for every '1'
            for (z,x,y),ch in list(tiles.items()):
                if ch == "1":
                    need = [(z,x+1,y,"2"),(z,x,y+1,"3"),(z,x+1,y+1,"4")]
                    if not all(tiles.get((zz,xx,yy)) == cc
                               for zz,xx,yy,cc in need):
                        orphan_local.append((z,x,y))
            orphan_n = len(orphan_local)
            tile_count = sum(1 for v in tiles.values() if v == "1")
            # stacked collision: same (x,y) corner '1' in two adjacent z
            zs_by_xy = {}
            for (z,x,y),ch in tiles.items():
                if ch == "1": zs_by_xy.setdefault((x,y), []).append(z)
            collide_n = sum(1 for zs in zs_by_xy.values()
                            if len(zs) >= 2 and any(
                                abs(zs[i]-zs[j]) == 1
                                for i in range(len(zs))
                                for j in range(i+1, len(zs))))
        except Exception:
            pass
    s["fixed_layout_header_ok"]    = head_ok
    s["fixed_tile_count_even"]     = 1.0 if (tile_count > 0 and
                                              tile_count % 2 == 0) else 0.0
    s["fixed_no_orphan_corner"]    = 1.0 if orphan_n == 0 else 0.0
    s["fixed_no_stacked_collision"] = 1.0 if collide_n == 0 else 0.0

    # ---- 5. menu screenshot OCR ----
    menu = rd / "view_kmahjongg_menu.png"
    menu_kw = expected.get("menu_keywords",
        ["game","move","view","settings","kmahjongg","new","help"])
    s["menu_shot_present"] = 1.0 if menu.exists() else 0.0
    try:
        import pytesseract; from PIL import Image
        if menu.exists():
            tx = pytesseract.image_to_string(Image.open(menu)).lower()
            s["menu_shot_ocr"] = 1.0 if any(k in tx for k in menu_kw) else 0.0
        else:
            s["menu_shot_ocr"] = 0.0
    except Exception:
        s["menu_shot_ocr"] = 0.0

    # ---- 6 + 7. broken / fixed deal screenshots ----
    bd = rd / "view_broken_deal.png"
    fd = rd / "view_fixed_deal.png"
    s["broken_deal_shot"] = 1.0 if bd.exists() else 0.0
    s["fixed_deal_shot"]  = 1.0 if fd.exists() else 0.0
    deal_kw = expected.get("deal_keywords",
        ["tiles","time","matches","layout","kmahjongg","00:"])
    try:
        import pytesseract; from PIL import Image
        if fd.exists():
            tx = pytesseract.image_to_string(Image.open(fd)).lower()
            s["fixed_deal_ocr"] = 1.0 if any(k in tx for k in deal_kw) else 0.0
        else:
            s["fixed_deal_ocr"] = 0.0
    except Exception:
        s["fixed_deal_ocr"] = 0.0

    # ---- 8. tile_faces.json clusters / face_up_count ----
    tf = rd / "tile_faces.json"
    if tf.exists():
        try:
            d = json.loads(tf.read_text())
            cn = int(d.get("clusters_total", 0))
            fu = int(d.get("face_up_count", 0))
            s["face_clusters_in_range"] = 1.0 if 18 <= cn <= 50 else \
                (0.5 if 10 <= cn <= 80 else 0.0)
            s["face_up_count_ok"] = 1.0 if fu >= 60 else fu/60.0
            # spot-check: phash strings present
            phash_ok = sum(1 for t in d.get("tiles", [])
                           if isinstance(t.get("phash"), str)
                              and len(t["phash"]) >= 16
                              and (t.get("x"), t.get("y"), t.get("z")) in
                                  {(x,y,z) for (z,x,y),c in tiles.items() if c=="1"})
            s["tile_face_phash_present"] = 1.0 if phash_ok >= 60 else phash_ok/60.0
            hashes = {t["phash"] for t in d.get("tiles", []) if t.get("phash")}
            s["tile_face_phash_diverse"] = 1.0 if len(hashes) >= 18 else len(hashes)/18.0
        except Exception:
            s["face_clusters_in_range"] = 0.0
            s["face_up_count_ok"] = 0.0
            s["tile_face_phash_present"] = 0.0
    else:
        s["face_clusters_in_range"] = 0.0
        s["face_up_count_ok"] = 0.0
        s["tile_face_phash_present"] = 0.0

    # ---- 9. plan.json pairs_planned >= 12 + cluster consistency ----
    pj = rd / "plan.json"
    pairs_planned = 0
    pair_cluster_ok = 0.0
    if pj.exists() and tf.exists():
        try:
            p = json.loads(pj.read_text())
            tdata = json.loads(tf.read_text())
            cmap = {t["id"]: t.get("face_cluster") for t in tdata.get("tiles", [])}
            pairs = p.get("pairs", [])
            pairs_planned = len(pairs)
            good = 0
            for pr in pairs:
                lc = cmap.get(pr.get("left_id"))
                rc = cmap.get(pr.get("right_id"))
                if lc is not None and lc == rc: good += 1
            pair_cluster_ok = good / max(1, len(pairs))
        except Exception: pass
    s["plan_pairs_count"] = min(1.0, pairs_planned / 12.0)
    s["plan_pairs_cluster_consistent"] = pair_cluster_ok

    # ---- 10. progress / after-play screenshots ----
    progress = [rd / f"view_progress_{i}.png" for i in (1,2,3)]
    n_prog = sum(1 for p in progress if p.exists())
    s["progress_shots_count"] = n_prog / 3.0
    after = rd / "view_after_play.png"
    s["after_play_shot"] = 1.0 if after.exists() else 0.0

    # ---- 11. KConfig forensics ----
    kj = rd / "kconfig_state.json"
    kconfig_ok = 0.0
    if kj.exists():
        try:
            d = json.loads(kj.read_text())
            gen = d.get("general", {})
            lay = str(gen.get("Layout", "")).lower()
            gn  = int(gen.get("GameNumber", 0)) if str(gen.get("GameNumber","0")).isdigit() else 0
            live = ""
            for cand in [os.path.expanduser("~/.config/kmahjonggrc"),
                         "/root/.config/kmahjonggrc"]:
                if os.path.exists(cand): live = open(cand).read().lower(); break
            if "fixed_dragon" in lay and gn == 424242 and \
               "fixed_dragon" in live and "424242" in live:
                kconfig_ok = 1.0
            elif "fixed_dragon" in lay and gn == 424242:
                kconfig_ok = 0.4
        except Exception: pass
    # cross-check live config file as best-effort fallback
    if kconfig_ok < 1.0:
        for cand in [os.path.expanduser("~/.config/kmahjonggrc"),
                     "/root/.config/kmahjonggrc"]:
            try:
                if os.path.exists(cand):
                    t = open(cand).read().lower()
                    if "fixed_dragon" in t and "424242" in t:
                        kconfig_ok = max(kconfig_ok, 0.85)
            except Exception: pass
    s["kconfig_state_ok"] = kconfig_ok

    # ---- 12. diff lines ----
    df = rd / "diff.txt"
    dlines = 0
    if df.exists():
        try: dlines = sum(1 for _ in df.open())
        except Exception: dlines = 0
    lo = expected.get("diff_min_lines", 6)
    hi = expected.get("diff_max_lines", 200)
    s["diff_in_range"] = 1.0 if lo <= dlines <= hi else 0.0

    # ---- 13. summary.md keywords ----
    sm = rd / "summary.md"
    sm_ok = 0.0
    if sm.exists():
        t = sm.read_text(errors="ignore")
        kws = expected.get("summary_keywords",
            ["布局解析","截屏识别花色","鼠标点击消对","KConfig 取证"])
        if all(k in t for k in kws) and len(t.splitlines()) >= 8:
            sm_ok = 1.0
        elif sum(1 for k in kws if k in t) >= 3:
            sm_ok = 0.6
    s["summary_md_complete"] = sm_ok

    # ---- 14. VLM rubric ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    imgs = [str(rd/n) for n in
            ["view_fixed_deal.png","view_progress_1.png","view_after_play.png"]
            if (rd/n).exists()]
    if vlm_score_rubric and imgs:
        rubric = {
            "vlm_kmahjongg_real":   "图像确实是 KMahjongg 主窗口或对局画面，含立体牌山和 HUD",
            "vlm_layout_clean":     "fixed 布局看起来形状完整、没有孤立角，整体牌山立体感正确",
            "vlm_progress_change":  "progress 截屏与 fixed_deal 之间能看出明显的牌数减少",
            "vlm_no_cheat":         "看上去是真实点击消对，不是把存档或截屏拼接出来的",
        }
        vlm = vlm_score_rubric(imgs[:3], rubric,
                instruction="评估 KMahjongg 布局修复 + 实战消对截图的真实性")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
    else:
        for k in ["vlm_kmahjongg_real","vlm_layout_clean",
                  "vlm_progress_change","vlm_no_cheat"]:
            s[k] = 0.5

    # ---- aggregate + hard gates ----
    W = {"fixed_no_orphan_corner":3,"fixed_no_stacked_collision":3,
         "tile_face_phash_present":2,"plan_pairs_cluster_consistent":2,
         "kconfig_state_ok":2,"vlm_layout_clean":2,"vlm_no_cheat":2}
    nums=[(W.get(k,1),v) for k,v in s.items() if isinstance(v,(int,float))]
    base = sum(w*v for w,v in nums)/sum(w for w,_ in nums) if nums else 0.0
    cli_evidence = (rd/"parse_before.json").exists() and \
                   (rd/"bugs.json").exists() and \
                   (rd/"kconfig_state.json").exists() and \
                   (rd/"diff.txt").exists()
    gui_screenshot = sum((rd/n).exists() for n in
        ["view_kmahjongg_menu.png","view_broken_deal.png",
         "view_fixed_deal.png","view_after_play.png",
         "view_progress_1.png","view_progress_2.png","view_progress_3.png"]) >= 6 \
        and s.get("fixed_deal_ocr",0) >= 1.0
    vlm_avg = sum(s.get(k, 0.0) for k in
        ["vlm_kmahjongg_real","vlm_layout_clean",
         "vlm_progress_change","vlm_no_cheat"]) / 4.0
    if not cli_evidence:    base = min(base, 0.4)
    # GUI hard cap dropped: missing screenshots already penalised via per-shot sub-scores.
    if vlm_score_rubric is not None and vlm_avg < 0.6:
        base = min(base, 0.6)
    if s.get("fixed_no_orphan_corner", 0) < 1.0: base = min(base, 0.55)
    if s.get("plan_pairs_count", 0) < 1.0:       base = min(base, 0.7)
    if s.get("kconfig_state_ok", 0) < 0.5:       base = min(base, 0.65)
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
