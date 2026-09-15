# Auto-generated from WeaveBench task GAM_task_17_pysol_freecell_fcsolve.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """PySolFC + fc-solve dual-engine FreeCell verifier.

    8–15 sub-scores + 3 hard gates.  Channels:
      - CLI a : make_pysol_freecell_board.py 生成 board.txt
      - CLI b : fc-solve 求解
      - GUI a : PySolFC menu/deal screenshot OCR
      - GUI b : per-cascade OCR 识牌 cross-check
      - GUI c : board snapshots after applying first 25 moves to a copy
      - CLI c : pickle 解 statistics.dat 验证 won 计数增长
    No GT leakage: gt/expected.json carries only invariants
    (deal seed, expected_min_moves, keyword sets).
    """
    import json, os, re, csv, glob, math
    from pathlib import Path

    ws = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = ws / "results"
    gt_dir = ws / "gt"
    expected = {}
    if (gt_dir / "expected.json").exists():
        try: expected = json.loads((gt_dir/"expected.json").read_text())
        except Exception: expected = {}
    seed_expected = int(expected.get("ms_deal_number", 617))
    s = {}

    # ---- 1. deal_seed.json ----
    ds = rd / "deal_seed.json"
    s["deal_seed_correct"] = 0.0
    if ds.exists():
        try:
            d = json.loads(ds.read_text())
            if int(d.get("ms_deal_number", -1)) == seed_expected:
                s["deal_seed_correct"] = 1.0
        except Exception: pass

    # ---- 2. board.txt full deck ----
    bt = rd / "board.txt"
    bv = rd / "board_verify.json"
    rows = 0; tokens = []
    if bt.exists():
        try:
            lines = [ln.strip() for ln in bt.read_text().splitlines() if ln.strip()]
            rows = len(lines)
            for ln in lines:
                tokens.extend(ln.split())
        except Exception: pass
    deck_ok = (rows == 8 and len(tokens) == 52
               and len(set(tokens)) == 52
               and all(re.fullmatch(r"(?:A|[2-9]|T|J|Q|K)[CDHS]", t)
                       for t in tokens))
    s["board_full_deck"] = 1.0 if deck_ok else 0.0
    s["board_verify_present"] = 1.0 if bv.exists() else 0.0

    # ---- 3. initial PySol screenshot OCR ----
    vi = rd / "view_pysol_initial.png"
    s["initial_shot_present"] = 1.0 if vi.exists() else 0.0
    initial_kw = expected.get("initial_keywords",
        ["freecell","617","#617","numbered","game"])
    try:
        import pytesseract; from PIL import Image
        if vi.exists():
            tx = pytesseract.image_to_string(Image.open(vi)).lower()
            hit_fc  = "freecell" in tx
            hit_num = ("617" in tx) or ("# 617" in tx) or ("#617" in tx)
            hit_menu = any(k in tx for k in ["file","game","help","statistics","select"])
            n_cards  = len(re.findall(r"\b(?:[A2-9TJQK])[CDHScdhs]\b", tx))
            w,h = Image.open(vi).size; big = (w*h) >= 600*450
            s["initial_shot_ocr"] = 1.0 if (hit_fc and hit_num and hit_menu and n_cards>=12 and big) \
                                    else (0.4 if (hit_fc and hit_num and big) else 0.0)
        else:
            s["initial_shot_ocr"] = 0.0
    except Exception:
        s["initial_shot_ocr"] = 0.4 if vi.exists() else 0.0

    # ---- 4. pysol_options ----
    po = rd / "pysol_options.json"
    s["pysol_options_ok"] = 0.0
    if po.exists():
        try:
            d = json.loads(po.read_text())
            if int(d.get("last_game_number", -1)) == seed_expected:
                s["pysol_options_ok"] = 1.0
            elif d.get("last_gameid") or d.get("options_path"):
                s["pysol_options_ok"] = 0.4
        except Exception: pass

    # ---- 5. board_seen.json schema ----
    bs = rd / "board_seen.json"
    s["board_seen_schema"] = 0.0
    seen_tokens = []
    if bs.exists():
        try:
            d = json.loads(bs.read_text())
            casc = d.get("cascades", [])
            if isinstance(casc, list) and len(casc) == 8:
                ok = all(isinstance(c, list) and 6 <= len(c) <= 8
                         for c in casc)
                if ok:
                    s["board_seen_schema"] = 1.0
                    for c in casc: seen_tokens.extend(c)
        except Exception: pass

    # ---- 6. board_match ratio ----
    bm = rd / "board_match.json"
    match_ratio = 0.0
    if bm.exists():
        try:
            d = json.loads(bm.read_text())
            tot = max(1, int(d.get("total", 52)))
            mat = int(d.get("matched", 0))
            match_ratio = mat / tot
        except Exception: pass
    # cross-verify with seen_tokens vs board.txt token multisets
    if seen_tokens and tokens and match_ratio == 0.0:
        from collections import Counter
        a = Counter(t.upper() for t in tokens)
        b = Counter(t.upper() for t in seen_tokens)
        common = sum((a & b).values())
        match_ratio = common / 52.0
    # cross-verify with canonical seed deal (positional)
    import subprocess, shutil
    mk = shutil.which("make_pysol_freecell_board.py") or "/usr/share/freecell-solver/make_pysol_freecell_board.py"
    canon=[]
    try:
        canon=[ln.split() for ln in subprocess.check_output(
                    ["python3", mk, str(seed_expected), "freecell"],
                    timeout=15).decode().splitlines()
                if ln.strip() and not ln.startswith(":")]
    except Exception: pass
    flat = [c for r in canon for c in r] if len(canon)==8 else []
    pos_ok = sum(1 for a,b in zip(flat, seen_tokens) if a.upper()==b.upper()) if flat and seen_tokens else 0
    if pos_ok>=44:
        s["board_match_85pct"] = 1.0
    elif pos_ok>0:
        s["board_match_85pct"] = pos_ok/44.0
    else:
        s["board_match_85pct"] = 1.0 if match_ratio >= 0.85 else \
                                  (match_ratio / 0.85)

    # ---- 7. solution.json schema + moves_total ----
    sj = rd / "solution.json"
    moves_total = 0
    move_kinds = set()
    s["solution_schema"] = 0.0
    if sj.exists():
        try:
            d = json.loads(sj.read_text())
            moves = d.get("moves", [])
            moves_total = int(d.get("moves_total", len(moves)))
            schema_ok = isinstance(moves, list) and all(
                isinstance(m, dict) and "kind" in m and "from" in m
                and "to" in m for m in moves[:5])
            if schema_ok and moves_total >= 60:
                s["solution_schema"] = 1.0
            elif schema_ok:
                s["solution_schema"] = 0.5
            for m in moves:
                if m.get("kind"): move_kinds.add(m["kind"])
        except Exception: pass
    s["solution_moves_total_60"] = 1.0 if moves_total >= 60 else \
                                    (moves_total / 60.0 if moves_total else 0.0)

    # ---- 8. fcsolve_raw.log ----
    fr = rd / "fcsolve_raw.log"
    fr_ok = 0.0
    if fr.exists():
        try:
            t = fr.read_text(errors="ignore")
            n_lines = t.count("\n")
            has_total = ("Total number of moves" in t) or \
                        ("Move a card" in t) or ("This game is solveable" in t)
            if n_lines >= 100 and has_total:
                fr_ok = 1.0
            elif n_lines >= 30 and has_total:
                fr_ok = 0.6
            elif fr.stat().st_size > 0:
                fr_ok = 0.3
        except Exception: pass
    s["fcsolve_raw_log_ok"] = fr_ok

    # ---- 9. play screenshots + play_log.csv ----
    play_shots = [rd / f"view_play_{i}.png" for i in (5,10,15,20,25)]
    n_play = sum(1 for p in play_shots if p.exists())
    s["play_progress_shots"] = n_play / 5.0
    pl = rd / "play_log.csv"
    pl_rows = 0
    if pl.exists():
        try:
            with pl.open() as f:
                rdr = csv.DictReader(f)
                hdrs = rdr.fieldnames or []
                if all(h in hdrs for h in
                       ["step","from","to","card","pre_top","post_top",
                        "screenshot"]):
                    pl_rows = sum(1 for _ in rdr)
        except Exception: pass
    s["play_log_25rows"] = 1.0 if pl_rows >= 25 else (pl_rows / 25.0)

    # ---- 10. play_verify.json foundation_match ----
    pv = rd / "play_verify.json"
    s["foundation_match"] = 0.0
    if pv.exists():
        try:
            d = json.loads(pv.read_text())
            if d.get("foundation_match") is True:
                s["foundation_match"] = 1.0
            elif d.get("expected_foundations") and d.get("observed_foundations"):
                exp = d["expected_foundations"]; obs = d["observed_foundations"]
                diff = sum(abs(int(exp.get(k,0)) - int(obs.get(k,0)))
                           for k in "HDSC")
                if diff <= 4: s["foundation_match"] = 0.6
        except Exception: pass

    # ---- 11. won screenshot OCR ----
    vw = rd / "view_pysol_won.png"
    s["won_shot_present"] = 1.0 if vw.exists() else 0.0
    won_kw = expected.get("won_keywords",
        ["won","congrat","king","foundation","game won","you win"])
    try:
        import pytesseract; from PIL import Image
        if vw.exists():
            tx = pytesseract.image_to_string(Image.open(vw)).lower()
            banner   = any(k in tx for k in ["game won","you win","congrat","congratulations"])
            n_kings  = len(re.findall(r"\bK[CDHScdhs]\b", tx))
            s["won_shot_ocr"] = 1.0 if (banner and ("foundation" in tx or n_kings>=2)) \
                                else (0.4 if banner else 0.0)
        else:
            s["won_shot_ocr"] = 0.0
    except Exception:
        s["won_shot_ocr"] = 0.4 if vw.exists() else 0.0

    # ---- 12. pysol stats delta ----
    ps = rd / "pysol_stats.json"
    s["stats_delta_won"] = 0.0
    if ps.exists():
        try:
            import pickle
            d = json.loads(ps.read_text())
            delta = int(d.get("delta_won_after_run", 0))
            sp = d.get("stats_path") or os.path.expanduser("~/.PySolFC/statistics.dat")
            won_now = 0
            try:
                obj = pickle.load(open(sp, "rb"))
                gs  = getattr(obj, "games_stats", {}) or {}
                won_now = sum(int(getattr(v.get(8), "won", 0) or 0)
                              for v in gs.values() if v.get(8))
            except Exception:
                won_now = 0
            if delta >= 1 and won_now >= 1:
                s["stats_delta_won"] = 1.0
            elif won_now >= 1:
                s["stats_delta_won"] = 0.4
        except Exception: pass

    # ---- 13. move_kind_histogram ----
    mh = rd / "move_kind_histogram.json"
    s["move_kind_diversity"] = 0.0
    if mh.exists():
        try:
            d = json.loads(mh.read_text())
            allowed = ["stack_to_foundation","stack_to_freecell",
                       "freecell_to_foundation","stack_to_stack",
                       "freecell_to_stack"]
            nonzero = sum(1 for k in allowed if int(d.get(k, 0)) > 0)
            s["move_kind_diversity"] = 1.0 if nonzero >= 3 else \
                                        (nonzero / 3.0)
        except Exception: pass

    # ---- 14. channels.json switch_count ----
    cj = rd / "channels.json"
    s["channel_switches_5"] = 0.0
    if cj.exists():
        try:
            d = json.loads(cj.read_text())
            sc = int(d.get("switch_count", 0))
            sw = d.get("switches", [])
            channels = set(x.get("channel","") for x in sw)
            allowed_tools = {"make_pysol_freecell_board.py","fc-solve",
                             "tesseract","pytesseract","pickle","gnome-screenshot","pyautogui"}
            real_tool = sum(1 for x in sw if x.get("tool") in allowed_tools)
            shot_refs = sum(1 for x in sw
                            if isinstance(x.get("step"), int)
                            and (rd/f"view_play_{x['step']}.png").exists())
            if sc >= 5 and len(channels) >= 3 and real_tool >= 4 and shot_refs >= 2:
                s["channel_switches_5"] = 1.0
            elif sc >= 3 and real_tool >= 2:
                s["channel_switches_5"] = 0.5
        except Exception: pass

    # ---- 15. summary.md keywords ----
    sm = rd / "summary.md"
    s["summary_keywords"] = 0.0
    if sm.exists():
        t = sm.read_text(errors="ignore")
        kws = expected.get("summary_keywords",
            ["deal 一致性校验","求解器输出","拖拽执行","统计取证"])
        hit = sum(1 for k in kws if k in t)
        if hit == 4 and len(t.splitlines()) >= 10:
            s["summary_keywords"] = 1.0
        elif hit >= 3:
            s["summary_keywords"] = 0.6

    # ---- VLM rubric ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    imgs = [str(rd/n) for n in
            ["view_pysol_initial.png","view_play_15.png",
             "view_pysol_won.png"] if (rd/n).exists()]
    if vlm_score_rubric and imgs:
        rubric = {
            "vlm_pysol_real":     "图像确实是 PySolFC 的 FreeCell 对局窗口（4 freecell + 4 foundation + 8 cascade）",
            "vlm_deal_consistent":"初始截图里 cascade 上的牌看起来是 52 张完整 deck，与 fc-solve board.txt 的 token 大致吻合",
            "vlm_progress_real":  "中间过程截图能看到明显牌动（cascade 顶端卡在变 / freecell 槽被占用）",
            "vlm_won_state":      "通关截图能看到 4 个 foundation 都被 K 牌占满 或弹出 won 提示文字",
        }
        vlm = vlm_score_rubric(imgs[:3], rubric,
                instruction="评估 PySolFC + fc-solve 双引擎通关截图的真实性")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
    else:
        import hashlib
        hs = {p: hashlib.md5(open(p,"rb").read()).hexdigest() for p in imgs if os.path.exists(p)}
        sizes = [os.path.getsize(p) for p in imgs if os.path.exists(p)]
        distinct = len(set(hs.values())); rich = sum(1 for sz in sizes if sz>=40000)
        base_v = 0.6 if (imgs and distinct==len(imgs) and rich>=2) else 0.2
        for k in ["vlm_pysol_real","vlm_deal_consistent",
                  "vlm_progress_real","vlm_won_state"]:
            s[k] = base_v
        s["judge_method"] = "fallback_heuristic"

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v, (int,float))]
    base = sum(nums)/len(nums) if nums else 0.0
    cli_evidence = (rd/"board.txt").exists() and (rd/"solution.json").exists() \
                   and (rd/"fcsolve_raw.log").exists() \
                   and (rd/"pysol_stats.json").exists()
    gui_screenshot = any((rd/n).exists() for n in
        ["view_pysol_initial.png","view_play_5.png","view_play_10.png",
         "view_play_15.png","view_play_20.png","view_play_25.png",
         "view_pysol_won.png"])
    vlm_avg = sum(s.get(k, 0.0) for k in
        ["vlm_pysol_real","vlm_deal_consistent",
         "vlm_progress_real","vlm_won_state"]) / 4.0
    if not cli_evidence:    base = min(base, 0.4)
    # GUI hard cap dropped: missing screenshots already penalised via per-shot sub-scores.
    if vlm_score_rubric is not None and vlm_avg < 0.6:
        base = min(base, 0.6)
    if s.get("board_match_85pct", 0) < 1.0: base = min(base, 0.7)
    if s.get("solution_moves_total_60", 0) < 1.0: base = min(base, 0.7)
    if s.get("stats_delta_won", 0) < 1.0: base = min(base, 0.65)
    if s.get("channel_switches_5", 0) < 1.0: base = min(base, 0.65)
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
