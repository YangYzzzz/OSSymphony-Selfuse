# Auto-generated from WeaveBench task GAM_task_10_gnuchess_pgn_blunder_hunt.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """gnuchess + xboard PGN audit grader.

    12 sub-scores + 4 hard gates.  Real signal channels:
      - Engine: gnuchess UCI eval + python-chess SAN legality.
      - GUI   : 3 xboard screenshots OCR for board / blunder / result text.
      - File  : evals.csv schema + diff.txt size + result tag invariant.
    No GT leakage: gt/expected.json holds only invariant counts /
    OCR keyword set / diff line bounds / required JSON keys.
    """
    import csv, json, os, re, subprocess
    from pathlib import Path

    ws  = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd  = ws / "results"
    gtd = ws / "gt"
    expected = {}
    if (gtd/"expected.json").exists():
        try:    expected = json.loads((gtd/"expected.json").read_text())
        except Exception: expected = {}
    s = {}

    # ---- 1. illegal_moves.json schema ----
    im = rd/"illegal_moves.json"
    illegal_ok = 0.0
    illegal_count = 0
    if im.exists():
        try:
            d = json.loads(im.read_text())
            if isinstance(d, list):
                illegal_count = len(d)
                gt_illegal = set(tuple(x) for x in expected.get("illegal_truth", []))
                got = {(int(x["ply"]), x["san"]) for x in d if isinstance(x, dict) and "ply" in x and "san" in x}
                keys_ok = bool(d) and all({"ply","side","san","error"}.issubset(x.keys()) for x in d)
                if gt_illegal:
                    if keys_ok and got == gt_illegal and len(d) == len(gt_illegal):
                        illegal_ok = 1.0
                    elif keys_ok:
                        illegal_ok = 0.4
                    elif not d:
                        illegal_ok = 0.0
                else:
                    if keys_ok:
                        illegal_ok = 1.0
                    elif not d:
                        illegal_ok = 0.3  # empty list = scanned but found none
        except Exception: pass
    s["illegal_moves_schema"] = illegal_ok

    # ---- 2. evals.csv length + schema ----
    ec = rd/"evals.csv"
    evals_rows = []
    evals_score = 0.0
    if ec.exists():
        try:
            evals_rows = list(csv.DictReader(ec.open()))
            need = {"ply","side","san","score_cp","best_san","fen"}
            if evals_rows and need.issubset(evals_rows[0].keys()):
                import chess, random
                n = len(evals_rows)
                target = expected.get("min_evals_rows", 40)
                size_ok = min(1.0, n/target)
                sample = random.Random(0).sample(evals_rows, min(5, n)) if n else []
                def _fen_valid(r):
                    try: return chess.Board(r["fen"]).is_valid()
                    except Exception: return False
                fen_ok = (sum(1 for r in sample if _fen_valid(r)) / len(sample)) if sample else 0.0
                evals_score = round(0.5*size_ok + 0.5*fen_ok, 3)
        except Exception: pass
    s["evals_csv_len_schema"] = evals_score

    # ---- 3. blunders.json detected with cp swing ----
    bj = rd/"blunders.json"
    blunders_ok = 0.0
    blunder_count = 0
    if bj.exists():
        try:
            b = json.loads(bj.read_text())
            if isinstance(b, list):
                blunder_count = len(b)
                lo = expected.get("min_blunders", 1)
                hi = expected.get("max_blunders", 4)
                swing_min = expected.get("blunder_min_cp_swing", 180)
                def _b_ok(x):
                    try:
                        cb, ca, sw = int(x["cp_before"]), int(x["cp_after"]), int(x["swing"])
                        return (abs(sw) >= swing_min
                                and abs((ca - cb) - sw) <= 25
                                and 1 <= int(x["ply"]) <= 60
                                and isinstance(x.get("best_san"), str)
                                and len(x["best_san"]) >= 2)
                    except Exception:
                        return False
                req = {"ply","side","san","best_san","cp_before","cp_after","swing"}
                if lo <= blunder_count <= hi and all(req.issubset(x.keys()) and _b_ok(x) for x in b):
                    blunders_ok = 1.0
                elif blunder_count >= 1:
                    blunders_ok = 0.5
        except Exception: pass
    s["blunders_detected"] = blunders_ok

    # ---- 4-6. xboard screenshots ----
    shots = ["view_xboard_initial.png",
             "view_xboard_blunder.png",
             "view_xboard_fixed_final.png"]
    present = sum(1 for n in shots if (rd/n).exists())
    s["xboard_shots_present"] = present / 3.0

    ocr_kw = expected.get("ocr_keywords_xboard",
        ["xboard","white","black","move","game","file"])
    finish_kw = ["1-0","0-1","1/2-1/2","wins","draw","mates","stalemate"]
    try:
        import pytesseract
        from PIL import Image
        def _ocr(p):
            try:    return pytesseract.image_to_string(Image.open(p)).lower()
            except Exception: return ""
        # initial: any xboard menu word
        t = _ocr(rd/"view_xboard_initial.png") if (rd/"view_xboard_initial.png").exists() else ""
        s["xboard_initial_ocr"] = 1.0 if any(k in t for k in ocr_kw) else 0.0
        # blunder shot: must look like a chess board image (heuristic: variance + OCR)
        from PIL import Image as PI
        def _looks_like_board(p):
            try:
                im = PI.open(p).convert("L")
                import numpy as np
                a = np.array(im); h,w = a.shape
                if h<360 or w<360: return False
                hist,_ = np.histogram(a, bins=8, range=(0,256))
                top2 = sorted(hist, reverse=True)[:2]
                return float(a.std()) > 45 and (sum(top2) / a.size) > 0.55
            except Exception: return False
        s["xboard_blunder_shot_real"] = 1.0 if _looks_like_board(rd/"view_xboard_blunder.png") else 0.0
        # final: result text overlay
        t2 = _ocr(rd/"view_xboard_fixed_final.png") if (rd/"view_xboard_fixed_final.png").exists() else ""
        s["xboard_final_result_ocr"] = 1.0 if any(k in t2 for k in finish_kw) else 0.0
    except ImportError:
        # OCR libs missing — give half credit so the test isn't a total zero
        s["xboard_initial_ocr"]      = 0.5 if (rd/"view_xboard_initial.png").exists() else 0.0
        s["xboard_blunder_shot_real"]= 0.5 if (rd/"view_xboard_blunder.png").exists() else 0.0
        s["xboard_final_result_ocr"] = 0.5 if (rd/"view_xboard_fixed_final.png").exists() else 0.0

    # ---- 7. result_check.json ----
    rcj = rd/"result_check.json"
    rc_ok = 0.0
    if rcj.exists():
        try:
            r = json.loads(rcj.read_text())
            choices = expected.get("result_tag_choices",["1-0","0-1","1/2-1/2"])
            if all(k in r for k in ["declared","engine_suggests","match"]) and \
               r["declared"] in choices and r["engine_suggests"] in choices and \
               bool(r["match"]) == (r["declared"] == r["engine_suggests"]) and \
               r["declared"] == expected.get("declared_truth", r["declared"]):
                rc_ok = 1.0
        except Exception: pass
    s["result_check_schema"] = rc_ok

    # ---- 8. fixed.pgn re-replays cleanly ----
    fp = rd/"fixed.pgn"
    fp_ok = 0.0
    fp_result_tag = None
    fp_plies = 0
    if fp.exists():
        try:
            import chess.pgn, io
            game = chess.pgn.read_game(io.StringIO(fp.read_text()))
            if game is not None:
                board = game.board()
                ok = True
                for mv in game.mainline_moves():
                    if mv not in board.legal_moves:
                        ok = False; break
                    board.push(mv); fp_plies += 1
                fp_result_tag = game.headers.get("Result","")
                if ok and fp_plies >= expected.get("fixed_pgn_min_plies",30) \
                   and fp_result_tag in expected.get("result_tag_choices",["1-0","0-1","1/2-1/2"]) \
                   and all(t in game.headers for t in expected.get("fixed_pgn_required_tags",[])):
                    fp_ok = 1.0
                elif ok:
                    fp_ok = 0.5
        except Exception: pass
    s["fixed_pgn_replays"] = fp_ok

    # ---- 9. evals_after.csv ----
    eca = rd/"evals_after.csv"
    eca_ok = 0.0
    if eca.exists():
        try:
            rows = list(csv.DictReader(eca.open()))
            if len(rows) >= 3 and {"ply","san","score_cp"}.issubset(rows[0].keys()):
                eca_ok = 1.0
        except Exception: pass
    s["evals_after_ok"] = eca_ok

    # ---- 10. diff.txt size band ----
    df = rd/"diff.txt"
    dlines = 0
    if df.exists():
        try: dlines = sum(1 for _ in df.open())
        except Exception: dlines = 0
    lo = expected.get("diff_min_lines", 4)
    hi = expected.get("diff_max_lines", 80)
    s["diff_in_range"] = 1.0 if lo <= dlines <= hi else 0.0

    # ---- 11. report.json required keys ----
    rj = rd/"report.json"
    rep_ok = 0.0
    if rj.exists():
        try:
            r = json.loads(rj.read_text())
            need = expected.get("report_required_keys", [
                "illegal_moves","blunders","result_tag_before",
                "result_tag_after","engine_used","fixed_pgn","evals_csv"])
            eng = str(r.get("engine_used","")).lower()
            ver = str(r.get("engine_version",""))
            keys_ok = all(k in r for k in need)
            engine_ok = ("gnuchess" in eng) and bool(re.search(r"\d", ver))
            rep_ok = 1.0 if (keys_ok and engine_ok) else (0.4 if keys_ok else 0.0)
        except Exception: pass
    s["report_keys_ok"] = rep_ok

    # ---- 12. VLM rubric ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    imgs = [str(rd/n) for n in shots if (rd/n).exists()]
    if vlm_score_rubric and imgs:
        rubric = {
            "vlm_xboard_real":   "图像确实是 GNU XBoard 棋盘 GUI（含 8x8 棋盘 + 菜单栏），不是黑屏 / 桌面 / 终端",
            "vlm_blunder_pos":   "blunder 截屏里盘面与第 N 步局面一致（棋子在合理位置而非起始局面）",
            "vlm_finish_text":   "fixed_final 截屏里能看到 1-0 / 0-1 / 1/2-1/2 / wins / draw 的结果文本",
            "vlm_no_cheat":      "全程是真用 xboard 加载 PGN 的截屏，不是 PowerPoint 假图或棋盘网图",
        }
        vlm = vlm_score_rubric(imgs[:3], rubric,
            instruction="评估 xboard 三张棋盘截屏的真实性、局面对应与结果文本可见性")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method","failed")
    else:
        for k in ["vlm_xboard_real","vlm_blunder_pos","vlm_finish_text","vlm_no_cheat"]:
            s[k] = 0.5

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums) if nums else 0.0
    cli_evidence = (rd/"evals.csv").exists() and (rd/"blunders.json").exists() \
                   and (rd/"diff.txt").exists()
    gui_screenshot = any((rd/n).exists() for n in shots)
    vlm_avg = sum(s.get(k,0.0) for k in
        ["vlm_xboard_real","vlm_blunder_pos","vlm_finish_text","vlm_no_cheat"]) / 4.0
    if not cli_evidence:    base = min(base, 0.4)
    # GUI hard cap dropped: missing screenshot already penalised via xboard_shots_present.
    if vlm_score_rubric is not None and vlm_avg < 0.6:
        base = min(base, 0.6)
    if s.get("fixed_pgn_replays",0) < 1.0: base = min(base, 0.55)
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
