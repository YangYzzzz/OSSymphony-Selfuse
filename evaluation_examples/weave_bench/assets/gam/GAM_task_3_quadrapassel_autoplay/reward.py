# Auto-generated from WeaveBench task GAM_task_3_quadrapassel_autoplay.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import csv, re, json, hashlib, glob as globmod
from pathlib import Path
from PIL import Image
import numpy as np

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    gt_path = Path("/tmp_workspace/gt/expected.json")
    gt = json.loads(gt_path.read_text()) if gt_path.exists() else {}
    s = {}

    # 1. game_log.csv existence and row count
    cf = rd / "game_log.csv"
    rows = []
    if cf.exists():
        try:
            with cf.open(encoding="utf-8", errors="ignore") as _fh:
                rows = list(csv.DictReader(_fh))
        except Exception:
            rows = []
    min_rows = gt.get("min_log_rows", 60)
    s["log_row_count"] = min(1.0, len(rows) / min_rows)

    # 2. CSV schema
    required_cols = ["step", "piece_type", "rotation", "target_col",
                     "lines_cleared", "board_height", "holes",
                     "action_keys", "screenshot_file"]
    s["log_schema"] = 1.0 if rows and all(
        k in rows[0] for k in required_cols) else 0.0

    # 3. piece_type validity + diversity
    valid_pieces = set("IOTSZJL")
    min_piece_types = gt.get("min_piece_types", 5)
    if rows:
        piece_vals = set(r.get("piece_type", "").strip() for r in rows)
        s["piece_type_valid"] = 1.0 if piece_vals.issubset(valid_pieces) and len(piece_vals) >= min_piece_types else 0.0
    else:
        s["piece_type_valid"] = 0.0

    # 4. total lines cleared
    total_lines = sum(int(r.get("lines_cleared", 0)) for r in rows if r.get("lines_cleared", "").isdigit())
    min_lines = gt.get("min_lines_cleared", 10)
    s["lines_cleared"] = min(1.0, total_lines / min_lines)

    # 5. board step screenshots (count + size + width)
    step_shots = list(rd.glob("board_step_*.png"))
    min_shots = gt.get("min_step_screenshots", 8)
    min_bytes = gt.get("min_shot_bytes", 5120)
    min_w = gt.get("min_shot_width", 200)
    s["step_screenshots"] = min(1.0, len(step_shots) / min_shots)
    if step_shots:
        ok_sized = 0
        for p in step_shots:
            try:
                if p.stat().st_size < min_bytes:
                    continue
                with Image.open(p) as im:
                    if im.width >= min_w:
                        ok_sized += 1
            except Exception:
                pass
        s["step_shot_quality"] = ok_sized / len(step_shots)
    else:
        s["step_shot_quality"] = 0.0

    # 5b. md5 diversity of step shots (anti-cheat: no repeated placeholders)
    s["step_shot_md5_diversity"] = 0.0
    if step_shots:
        md5s = set()
        for p in step_shots:
            try:
                md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception:
                pass
        s["step_shot_md5_diversity"] = len(md5s) / len(step_shots)

    # 6. final_board.png
    fb = rd / "final_board.png"
    s["final_board_exists"] = 0.0
    s["board_nontrivial"] = 0.0
    std_thr = gt.get("board_std_threshold", 40)
    if fb.exists():
        s["final_board_exists"] = 1.0
        try:
            im = Image.open(fb).convert("RGB")
            a = np.array(im)
            s["board_nontrivial"] = 1.0 if a.std() > std_thr else a.std() / std_thr
        except Exception:
            pass

    # 7. summary.md
    sm = rd / "summary.md"
    if sm.exists():
        c = sm.read_text(errors="ignore").lower()
        zh = all(k in c for k in gt.get("summary_keywords_zh", ["方块", "消行", "得分", "策略"]))
        en = all(k in c for k in gt.get("summary_keywords_en", ["piece", "line", "score", "heuristic"]))
        s["summary_complete"] = 1.0 if (zh or en) else 0.0
    else:
        s["summary_complete"] = 0.0

    # 8. action_keys present (≥70% rows must record real keys)
    keys_present = sum(1 for r in rows if re.search(
        r"(Left|Right|Up|space|Return)", r.get("action_keys", "")))
    if rows:
        ratio = keys_present / len(rows)
        s["action_keys_present"] = 1.0 if ratio >= 0.7 else ratio / 0.7
    else:
        s["action_keys_present"] = 0.0

    # 9. no solver imports
    forbidden = gt.get("forbidden_imports", ["tetris_ai", "pytris", "tetris_solver"])
    bad = False
    for src in workspace.rglob("*.py"):
        try:
            t = src.read_text(errors="ignore")
            if any(re.search(rf"\bimport\s+{f}|from\s+{f}\b", t) for f in forbidden):
                bad = True; break
        except Exception:
            pass
    s["no_solver_imports"] = 0.0 if bad else 1.0

    # 10. VLM rubric (optional)
    vlm_available = False
    try:
        from _judge_helper import vlm_score_rubric
        vlm_available = True
    except Exception:
        vlm_score_rubric = None
    if vlm_score_rubric and fb.exists():
        rubric = {
            "vlm_board_visible": "截图中能看到俄罗斯方块棋盘，有彩色方块",
            "vlm_pieces_placed": "棋盘中已放置多个方块，不是空棋盘",
            "vlm_no_trivial": "棋盘不是全空或全满，有游戏进行中的状态",
        }
        vlm = vlm_score_rubric([str(fb)], rubric,
                               instruction="Evaluate the Tetris game board screenshot.")
        for k in rubric:
            s[k] = vlm.get(k, 0.0)

    # --- Content-authenticity sub-scores ---
    shots_n = len(step_shots)
    rows_n = len(rows)
    s["actions_match_shots"] = 0.0
    if shots_n > 0 and rows_n > 0:
        s["actions_match_shots"] = (min(shots_n, rows_n)
                                    / max(shots_n, rows_n))

    s["step_pixel_diff_nontrivial"] = 0.0
    if len(step_shots) >= 2:
        try:
            sorted_shots = sorted(step_shots)
            diffs = []
            for i in range(min(4, len(sorted_shots) - 1)):
                ima = Image.open(sorted_shots[i]).convert("RGB")
                imb = (Image.open(sorted_shots[i + 1])
                       .convert("RGB").resize(ima.size))
                d = float(np.abs(np.array(ima, dtype=int)
                                 - np.array(imb, dtype=int)).mean())
                diffs.append(d)
            if diffs:
                avg_d = sum(diffs) / len(diffs)
                s["step_pixel_diff_nontrivial"] = (1.0 if avg_d > 5
                                                   else avg_d / 5)
        except Exception:
            pass

    # ---- Weighted aggregation: core 60% / gui 30% / aux 10% ----
    core_keys = ["log_row_count", "log_schema", "piece_type_valid",
                 "lines_cleared", "summary_complete", "action_keys_present"]
    gui_keys = ["step_screenshots", "step_shot_quality", "step_shot_md5_diversity",
                "final_board_exists", "board_nontrivial",
                "actions_match_shots", "step_pixel_diff_nontrivial"]
    aux_keys = ["no_solver_imports"]
    def avg(keys):
        vs = [s[k] for k in keys if isinstance(s.get(k), (int, float))]
        return sum(vs) / len(vs) if vs else 0.0
    core = avg(core_keys); gui = avg(gui_keys); aux = avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    vlm_keys = ["vlm_board_visible", "vlm_pieces_placed", "vlm_no_trivial"]
    vlm_nums = [s[k] for k in vlm_keys if isinstance(s.get(k), (int, float))]
    if vlm_nums:
        vlm_avg = sum(vlm_nums) / len(vlm_nums)
        base = 0.85 * base + 0.15 * vlm_avg
        if vlm_avg < 0.6:
            base = min(base, 0.55)
        if vlm_avg < 0.4:
            base = min(base, 0.35)
    else:
        # No VLM available: cap at 0.6 to avoid free perfect score
        base = min(base, 0.6)

    # Hard gates
    has_cli = s.get("log_row_count", 0) >= 0.5 and s.get("action_keys_present", 0) >= 0.5
    has_gui = s.get("final_board_exists", 0) > 0 and s.get("step_screenshots", 0) >= 0.5
    if not has_cli:
        base = min(base, 0.4)
    if not has_gui:
        base = min(base, 0.4)
    # Evidence gate: no game_log at all → near-zero
    if s.get("log_row_count", 0) == 0 and s.get("log_schema", 0) == 0:
        base = min(base, 0.05)
    # Stair-step content-authenticity caps (stricter than v1)
    if s.get("actions_match_shots", 0) < 0.7:
        base = min(base, 0.5)
    if s.get("step_pixel_diff_nontrivial", 0) < 0.5:
        base = min(base, 0.4)
    if s.get("board_nontrivial", 0) < 0.6:
        base = min(base, 0.5)
    if s.get("step_shot_md5_diversity", 0) < 0.8:
        base = min(base, 0.45)
    if s.get("step_shot_quality", 0) < 0.6:
        base = min(base, 0.5)
    if s.get("piece_type_valid", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("lines_cleared", 0) < 0.5:
        base = min(base, 0.5)
    if s.get("no_solver_imports", 0) < 1.0:
        base = min(base, 0.3)
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
