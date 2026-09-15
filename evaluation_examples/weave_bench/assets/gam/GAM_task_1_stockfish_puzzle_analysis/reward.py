# Auto-generated from WeaveBench task GAM_task_1_stockfish_puzzle_analysis.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import csv, json, re
from pathlib import Path

def grade(workspace_path=None, **kwargs) -> dict:
    """GAM_task_1: Stockfish puzzle analysis grader."""
    ws = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = ws / "results"
    gt_dir = ws / "gt" if (ws / "gt").exists() else Path("/tmp_workspace/gt")
    gt = {}
    if (gt_dir / "expected.json").exists():
        gt = json.loads((gt_dir / "expected.json").read_text())
    s = {}

    # 1. moves.txt
    mt = rd / "moves.txt"
    if mt.exists():
        lines = [l.strip() for l in mt.read_text().splitlines() if l.strip()]
        s["moves_file"] = min(1.0, len(lines) / gt.get("min_moves", 40))
    else:
        s["moves_file"] = 0.0

    # 2. eval_log.csv schema + row count
    ef = rd / "eval_log.csv"
    eval_rows = []
    if ef.exists():
        eval_rows = list(csv.DictReader(ef.open()))
        need = ["ply", "move", "cp_before", "cp_after", "best_move"]
        s["eval_schema"] = 1.0 if eval_rows and all(
            k in eval_rows[0] for k in need) else 0.0
        s["eval_count"] = min(1.0, len(eval_rows) / gt.get("min_eval_rows", 40))
    else:
        s["eval_schema"] = 0.0
        s["eval_count"] = 0.0

    # 3. blunders.json
    bf = rd / "blunders.json"
    if bf.exists():
        try:
            blunders = json.loads(bf.read_text())
            gt_plies = gt.get("blunder_plies", [])
            s["blunders_count"] = min(1.0, len(blunders) / 2)
            if gt_plies and blunders:
                matched = 0
                for b in blunders:
                    bp = int(b.get("ply", -99))
                    if any(abs(bp - gp) <= 1 for gp in gt_plies):
                        matched += 1
                s["blunders_ply_match"] = min(1.0, matched / len(gt_plies))
            else:
                s["blunders_ply_match"] = 0.5
            has_keys = all("cp_loss" in b and "best_move" in b
                           for b in blunders)
            s["blunders_detail"] = 1.0 if has_keys else 0.0
        except Exception:
            s["blunders_count"] = 0.0
            s["blunders_ply_match"] = 0.0
            s["blunders_detail"] = 0.0
    else:
        s["blunders_count"] = 0.0
        s["blunders_ply_match"] = 0.0
        s["blunders_detail"] = 0.0

    # 4-5. board images
    s["board_initial"] = 1.0 if (rd / "board_initial.png").exists() else 0.0
    s["view_initial"] = 1.0 if (rd / "view_initial.png").exists() else 0.0

    # 6. blunder view screenshots
    blunder_views = list(rd.glob("view_blunder_*.png"))
    s["view_blunders"] = min(1.0, len(blunder_views) / 2)

    # 7. annotated PGN
    ap = rd / "annotated.pgn"
    if ap.exists():
        pgn_text = ap.read_text(errors="ignore")
        blunder_comments = len(re.findall(
            r"\{[^}]*[Bb]lunder[^}]*\}", pgn_text))
        s["annotated_pgn"] = min(1.0, blunder_comments / 2)
    else:
        s["annotated_pgn"] = 0.0

    # 8. final view
    s["view_final"] = 1.0 if (rd / "view_final.png").exists() else 0.0

    # 9. analysis report
    ar = rd / "analysis_report.md"
    if ar.exists():
        txt = ar.read_text(errors="ignore").lower()
        has_opening = any(k in txt for k in
                         gt.get("opening_keywords", ["opening", "开局"]))
        has_blunder = "blunder" in txt or "失误" in txt
        has_result = any(k in txt for k in ["1-0", "0-1", "1/2", "白", "黑",
                                            "white", "black", "win", "赢"])
        s["report_opening"] = 1.0 if has_opening else 0.0
        s["report_blunder"] = 1.0 if has_blunder else 0.0
        s["report_result"] = 1.0 if has_result else 0.0
    else:
        s["report_opening"] = 0.0
        s["report_blunder"] = 0.0
        s["report_result"] = 0.0

    # VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    if vlm_score_rubric:
        imgs = [str(p) for p in [
            rd / "view_initial.png",
            *blunder_views,
            rd / "view_final.png"
        ] if p.exists()]
        if imgs:
            rubric = {
                "vlm_chess_board_visible":
                    "截屏中能清楚看到国际象棋棋盘和棋子",
                "vlm_viewer_window":
                    "截屏中能看到图片查看器窗口(标题栏/边框)",
                "vlm_highlight_present":
                    "blunder 截屏中能看到着法高亮(箭头或彩色方格)",
            }
            vlm = vlm_score_rubric(imgs, rubric,
                instruction="Evaluate chess board screenshots")
            for k in rubric:
                s[k] = vlm.get(k, 0.0)

    # --- Content-authenticity sub-scores ---
    s["blunders_min2"] = 0.0
    s["blunders_cp_loss_present"] = 0.0
    bf2 = rd / "blunders.json"
    if bf2.exists():
        try:
            bb = json.loads(bf2.read_text())
            if isinstance(bb, list):
                s["blunders_min2"] = 1.0 if len(bb) >= 2 else 0.0
                if bb and all(
                    isinstance(x, dict)
                    and isinstance(x.get("cp_loss"), (int, float))
                    for x in bb
                ):
                    s["blunders_cp_loss_present"] = 1.0
        except Exception:
            pass

    s["pgn_nag_present"] = 0.0
    ap2 = rd / "annotated.pgn"
    if ap2.exists():
        pt = ap2.read_text(errors="ignore")
        if re.search(r"\$\d+", pt) or re.search(r"\{[^}]*[?!]+[^}]*\}", pt):
            s["pgn_nag_present"] = 1.0

    s["boards_unique"] = 0.0
    try:
        import hashlib
        bd_imgs = list(rd.glob("board_*.png")) + list(rd.glob("view_*.png"))
        hashes = set()
        for p in bd_imgs:
            try:
                hashes.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception:
                pass
        if bd_imgs:
            s["boards_unique"] = min(1.0, len(hashes) / 3)
    except Exception:
        pass

    # --- Forbidden imports check ---
    forbidden = ["chess_solver", "stockfish_wrapper_solver"]
    bad_import = False
    for src in ws.rglob("*.py"):
        try:
            t = src.read_text(errors="ignore")
            if any(re.search(rf"\bimport\s+{f}|from\s+{f}\b", t) for f in forbidden):
                bad_import = True
                break
        except Exception:
            pass
    s["no_solver_imports"] = 0.0 if bad_import else 1.0

    # --- Screenshot authenticity: size + resolution ---
    s["screens_size_ok"] = 0.0
    s["screens_resolution_ok"] = 0.0
    try:
        min_bytes = int(gt.get("min_screenshot_bytes", 5120))
        min_w = int(gt.get("min_screenshot_width", 800))
        view_imgs = list(rd.glob("view_*.png"))
        if view_imgs:
            big_enough = [p for p in view_imgs
                          if p.stat().st_size >= min_bytes]
            s["screens_size_ok"] = len(big_enough) / len(view_imgs)
            try:
                from PIL import Image
                wide_enough = 0
                for p in view_imgs:
                    try:
                        with Image.open(p) as im:
                            if im.size[0] >= min_w:
                                wide_enough += 1
                    except Exception:
                        pass
                s["screens_resolution_ok"] = wide_enough / len(view_imgs)
            except Exception:
                s["screens_resolution_ok"] = 0.5
    except Exception:
        pass

    # VLM availability flag (cap if missing)
    vlm_available = vlm_score_rubric is not None and any(
        k.startswith("vlm_") for k in s
    )

    # Hard gates
    has_cli = (s.get("moves_file", 0) > 0 and s.get("eval_count", 0) > 0)
    has_gui = (s.get("view_initial", 0) > 0 or
               s.get("view_blunders", 0) > 0)

    # --- Weighted aggregate (core 60% / gui 30% / aux 10%) ---
    core_keys = ["moves_file", "eval_schema", "eval_count",
                 "blunders_count", "blunders_ply_match", "blunders_detail",
                 "blunders_min2", "blunders_cp_loss_present",
                 "annotated_pgn", "pgn_nag_present"]
    gui_keys = ["board_initial", "view_initial", "view_blunders",
                "view_final", "boards_unique",
                "screens_size_ok", "screens_resolution_ok",
                "vlm_chess_board_visible", "vlm_viewer_window",
                "vlm_highlight_present"]
    aux_keys = ["report_opening", "report_blunder", "report_result",
                "no_solver_imports"]

    def _mean(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vals) / len(vals) if vals else 0.0

    core = _mean(core_keys)
    gui = _mean(gui_keys)
    aux = _mean(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Hard gates (tightened)
    if not has_cli:
        base = min(base, 0.35)
    if not has_gui:
        base = min(base, 0.35)
    if s.get("blunders_ply_match", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("blunders_min2", 0) < 1.0:
        base = min(base, 0.4)
    if s.get("blunders_cp_loss_present", 0) < 1.0:
        base = min(base, 0.45)
    if s.get("pgn_nag_present", 0) < 1.0:
        base = min(base, 0.5)
    if s.get("boards_unique", 0) < 1.0:
        base = min(base, 0.5)
    if s.get("screens_size_ok", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("screens_resolution_ok", 0) < 0.7:
        base = min(base, 0.5)
    if s.get("no_solver_imports", 0) < 1.0:
        base = min(base, 0.35)
    # VLM unavailable → cap 0.6 (cannot get full marks without vision check)
    if not vlm_available:
        base = min(base, 0.6)

    s["overall_score"] = float(base)
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
