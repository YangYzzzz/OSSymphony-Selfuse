# Auto-generated from WeaveBench task GAM_task_5_sokoban_solver.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import ast, csv, json, re
from pathlib import Path
from PIL import Image
import numpy as np


def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    gt_path = Path("/tmp_workspace/gt/expected.json")
    gt = json.loads(gt_path.read_text()) if gt_path.exists() else {}
    s = {}

    # 1. solver.py existence + size + parse
    solver = rd / "solver.py"
    s["solver_exists"] = 1.0 if solver.exists() else 0.0
    s["solver_lines"] = 0.0
    s["solver_parses"] = 0.0
    if solver.exists():
        try:
            txt = solver.read_text(errors="ignore")
            n_lines = sum(1 for ln in txt.splitlines()
                          if ln.strip() and not ln.strip().startswith("#"))
            s["solver_lines"] = min(1.0, n_lines / gt.get("min_solver_lines", 30))
            ast.parse(txt)
            s["solver_parses"] = 1.0
        except Exception:
            pass

    # 2. forbidden imports anywhere under workspace
    forbidden = gt.get("forbidden_imports",
                       ["sokoban_solver", "pysokoban", "sokenizer"])
    bad = False
    for src in workspace.rglob("*.py"):
        if "exec/sokoban_game.py" in str(src):
            continue
        try:
            t = src.read_text(errors="ignore")
            if any(re.search(rf"\b(import|from)\s+{f}\b", t) for f in forbidden):
                bad = True
                break
        except Exception:
            pass
    s["no_solver_imports"] = 0.0 if bad else 1.0

    # 3. solution.txt files (at least 2, only LURD chars on first line)
    sol_files = sorted(rd.glob("level_*_solution.txt"))
    valid_sol = 0
    for f in sol_files:
        try:
            first = f.read_text(errors="ignore").splitlines()[0].strip().upper()
            if first and re.fullmatch(r"[LURD]+", first):
                valid_sol += 1
        except Exception:
            pass
    min_sol = gt.get("min_solution_files", 2)
    s["solution_files"] = min(1.0, valid_sol / min_sol)

    # 4. result.json with solved=true (≥ 2)
    res_files = sorted(rd.glob("level_*_result.json"))
    solved = 0
    attempted = 0
    for f in res_files:
        attempted += 1
        try:
            d = json.loads(f.read_text(errors="ignore"))
            if d.get("solved") is True and \
               d.get("boxes_on_goal") == d.get("total_goals"):
                solved += 1
        except Exception:
            pass
    s["levels_attempted"] = min(
        1.0, attempted / gt.get("min_levels_attempted", 2))
    s["levels_solved"] = min(
        1.0, solved / gt.get("min_levels_solved", 2))

    # 5. moves.csv length consistent with solution length
    csv_consistency = 0
    csv_count = 0
    for sf in sol_files:
        m = re.match(r"level_(\d+)_solution\.txt", sf.name)
        if not m:
            continue
        K = m.group(1)
        cf = rd / f"level_{K}_moves.csv"
        if not cf.exists():
            continue
        csv_count += 1
        try:
            sol_len = len(sf.read_text().splitlines()[0].strip())
            with cf.open() as fh:
                n_rows = sum(1 for _ in csv.DictReader(fh))
            if n_rows >= sol_len:
                csv_consistency += 1
        except Exception:
            pass
    s["moves_csv_present"] = min(1.0, csv_count / gt.get("min_solution_files", 2))
    s["moves_csv_consistent"] = (csv_consistency / max(1, csv_count))

    # 6. window_ids.log: at least 2 lines
    wlog = rd / "window_ids.log"
    s["window_ids_log"] = 0.0
    if wlog.exists():
        n = sum(1 for ln in wlog.read_text().splitlines() if ln.strip())
        s["window_ids_log"] = min(1.0, n / 2)

    # 7. step screenshots ≥ 4
    step_pngs = list(rd.glob("level_*_step_*.png"))
    s["step_screenshots"] = min(
        1.0, len(step_pngs) / gt.get("min_step_screenshots", 4))

    # 8. initial / final screenshots ≥ 2 each
    init_pngs = list(rd.glob("level_*_initial.png"))
    final_pngs = list(rd.glob("level_*_final.png"))
    s["initial_screenshots"] = min(1.0, len(init_pngs) / 2)
    s["final_screenshots"] = min(1.0, len(final_pngs) / 2)

    # 9. final screenshot non-trivial (size + std + min resolution)
    s["final_nontrivial"] = 0.0
    sample_final = final_pngs[0] if final_pngs else None
    if sample_final:
        try:
            sz = sample_final.stat().st_size
            if sz < 5 * 1024:
                s["final_nontrivial"] = 0.0
            else:
                im = Image.open(sample_final).convert("RGB")
                a = np.array(im)
                w, h = im.size
                resolution_ok = (w >= 320 and h >= 240)
                std_score = 1.0 if a.std() > 25 else a.std() / 25
                s["final_nontrivial"] = std_score if resolution_ok else min(std_score, 0.4)
        except Exception:
            pass

    # 9b. screenshot md5 uniqueness across all PNG evidence
    import hashlib
    all_pngs = list(rd.glob("level_*.png"))
    s["screenshot_diversity"] = 0.0
    if all_pngs:
        md5s = set()
        small_count = 0
        for p in all_pngs:
            try:
                if p.stat().st_size < 5 * 1024:
                    small_count += 1
                    continue
                md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception:
                pass
        if small_count == len(all_pngs):
            s["screenshot_diversity"] = 0.0
        else:
            valid = len(all_pngs) - small_count
            s["screenshot_diversity"] = min(1.0, len(md5s) / max(1, valid))

    # 10. summary.md keywords
    sm = rd / "summary.md"
    s["summary_complete"] = 0.0
    if sm.exists():
        c = sm.read_text(errors="ignore").lower()
        zh = all(k in c for k in gt.get("summary_keywords_zh",
                                        ["关卡", "求解", "推箱"]))
        en = all(k in c for k in gt.get("summary_keywords_en",
                                        ["level", "solve", "sokoban"]))
        if zh or en:
            s["summary_complete"] = 1.0

    # 11. verify.json present (cross-check between solver + game)
    verify_files = list(rd.glob("level_*_verify.json"))
    s["verify_files"] = min(1.0, len(verify_files) / 2)

    # 12. VLM rubric (3 items)
    vlm_used = False
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    if vlm_score_rubric and sample_final:
        rubric = {
            "vlm_board_visible": "截图中能看到一个由墙(灰色矩形)围成的网格棋盘",
            "vlm_boxes_present": "棋盘中有方块状的箱子(棕色或绿色矩形)",
            "vlm_solved_indicator": "大多数箱子位置和目标点(红色圆点)重合,或显示 SOLVED 字样",
        }
        try:
            vlm = vlm_score_rubric([str(sample_final)], rubric,
                                   instruction="Evaluate the Sokoban game final screenshot.")
            for k in rubric:
                s[k] = float(vlm.get(k, 0.0))
            vlm_used = True
        except Exception:
            for k in rubric:
                s[k] = 0.0

    # --- Content-authenticity sub-scores ---
    # initial vs final pixel diff (paired by level number)
    s["initial_final_pixel_diff"] = 0.0
    if init_pngs and final_pngs:
        try:
            diffs = []
            for ip in init_pngs:
                m = re.match(r"level_(\d+)_initial\.png", ip.name)
                if not m:
                    continue
                K = m.group(1)
                fp = rd / f"level_{K}_final.png"
                if not fp.exists():
                    continue
                ima = Image.open(ip).convert("RGB")
                imb = Image.open(fp).convert("RGB").resize(ima.size)
                d = float(np.abs(np.array(ima, dtype=int)
                                 - np.array(imb, dtype=int)).mean())
                diffs.append(d)
            if diffs:
                avg_d = sum(diffs) / len(diffs)
                s["initial_final_pixel_diff"] = (1.0 if avg_d > 5
                                                 else avg_d / 5)
        except Exception:
            pass

    # levels actually solved (verified)
    s["levels_actually_solved"] = min(
        1.0, solved / gt.get("min_levels_solved", 2))

    # Hard gates (tightened)
    has_cli = (s.get("solver_exists", 0) >= 1.0
               and s.get("solution_files", 0) >= 1.0
               and s.get("solver_parses", 0) >= 1.0)
    has_gui = (s.get("step_screenshots", 0) >= 1.0
               and s.get("final_screenshots", 0) >= 1.0
               and s.get("initial_screenshots", 0) >= 1.0)

    # Weighted average: core delivery 60% / GUI evidence 30% / aux 10%
    def _avg(keys):
        vals = [s.get(k, 0.0) for k in keys if isinstance(s.get(k, 0.0), (int, float))]
        return sum(vals) / len(vals) if vals else 0.0

    core_keys = ["solver_exists", "solver_parses", "no_solver_imports",
                 "solution_files", "levels_attempted", "levels_solved",
                 "levels_actually_solved", "moves_csv_present",
                 "moves_csv_consistent", "verify_files"]
    gui_keys = ["step_screenshots", "initial_screenshots", "final_screenshots",
                "final_nontrivial", "initial_final_pixel_diff",
                "screenshot_diversity",
                "vlm_board_visible", "vlm_boxes_present", "vlm_solved_indicator"]
    aux_keys = ["solver_lines", "window_ids_log", "summary_complete"]

    core = _avg(core_keys)
    gui = _avg([k for k in gui_keys if k in s])
    aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Empty-grader floor: nothing produced at all → ≤ 0.05
    nothing_at_all = (
        s.get("solver_exists", 0) == 0
        and s.get("solution_files", 0) == 0
        and s.get("levels_attempted", 0) == 0
        and s.get("step_screenshots", 0) == 0
        and s.get("final_screenshots", 0) == 0
    )
    if nothing_at_all:
        base = min(base, 0.05)

    # Multi-tier hard gates (tightened from v1)
    if not has_cli:
        base = min(base, 0.35)
    if not has_gui:
        base = min(base, 0.35)
    if s.get("no_solver_imports", 0) < 1.0:
        base = min(base, 0.30)
    if s.get("levels_actually_solved", 0) < 0.5:
        base = min(base, 0.35)
    if s.get("levels_actually_solved", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("moves_csv_consistent", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("verify_files", 0) < 0.5:
        base = min(base, 0.50)
    if s.get("solution_files", 0) < 1.0:
        base = min(base, 0.45)
    if s.get("initial_final_pixel_diff", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("final_nontrivial", 0) < 0.5:
        base = min(base, 0.50)
    if s.get("screenshot_diversity", 0) < 0.6:
        base = min(base, 0.55)
    # VLM unavailable → cap 0.6 (can't get full marks without visual evidence judge)
    if not vlm_used:
        base = min(base, 0.60)

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
