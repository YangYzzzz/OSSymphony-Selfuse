# Auto-generated from WeaveBench task GAM_task_0_gnome_mines_solve.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import csv, re, json, hashlib
from pathlib import Path
from PIL import Image
import numpy as np

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    """Stricter GAM_0 v2: weighted scoring + multi-layer hard gates + anti-cheat."""
    gt_path = workspace.parent / "gt" / "expected.json"
    if not gt_path.exists():
        gt_path = Path("/tmp_workspace/gt/expected.json")
    try:
        gt = json.loads(gt_path.read_text()) if gt_path.exists() else {}
    except Exception:
        gt = {}
    s = {}
    cf = workspace/"clicks.csv"
    rows = []
    if cf.exists():
        try:
            rows = list(csv.DictReader(cf.open()))
        except Exception:
            rows = []
    s["clicks_count"] = min(1.0, len(rows)/gt.get("min_clicks",240))
    s["clicks_schema"] = 1.0 if rows and all(k in rows[0] for k in ["step","action","x","y","reason"]) else 0.0
    flags = sum(1 for x in rows if x.get("action")=="right")
    s["flags_right_click"] = min(1.0, flags/gt.get("min_flags_right_click",80))
    reasoned = sum(1 for x in rows if re.search(r"(safe|flag)-by-?\w*", x.get("reason","")))
    s["reasoned_actions"] = min(1.0, reasoned/gt.get("min_reasoned_actions",120))
    # diversity of reasons (must mention >=3 distinct rule prefixes)
    distinct_reasons = len(set(x.get("reason","").split("-")[0] for x in rows if x.get("reason","")))
    s["reason_diversity"] = min(1.0, distinct_reasons/3)
    # coordinate variability — flat coords = synthetic CSV
    try:
        xs = sorted({int(float(x.get("x","0"))) for x in rows if x.get("x","").strip()})
        ys = sorted({int(float(x.get("y","0"))) for x in rows if x.get("y","").strip()})
        s["coord_diversity"] = 1.0 if (len(xs) >= 12 and len(ys) >= 8) else (
            min(len(xs)/12, len(ys)/8) if (xs and ys) else 0.0)
    except Exception:
        s["coord_diversity"] = 0.0
    # monotonic step ordering — fakers often hand-fill
    try:
        steps = [int(x.get("step","0")) for x in rows if x.get("step","").strip().lstrip("-").isdigit()]
        s["step_monotonic"] = 1.0 if (len(steps) >= len(rows)*0.95 and steps == sorted(steps)) else 0.0
    except Exception:
        s["step_monotonic"] = 0.0
    fb = workspace/"final_board.png"
    fb_size = fb.stat().st_size if fb.exists() else 0
    # placeholder image (<20KB) doesn't count
    s["final_board_exists"] = 1.0 if (fb.exists() and fb_size >= 20000) else 0.0
    if fb.exists() and fb_size >= 20000:
        try:
            im_rgb = Image.open(fb).convert("RGB")
            w0, h0 = im_rgb.size
            # Big board screenshot must be >= 720x480 and roughly landscape (board is 30x16)
            min_w, min_h = gt.get("final_board_min_w",720), gt.get("final_board_min_h",480)
            s["board_resolution"] = 1.0 if (w0 >= min_w and h0 >= min_h and w0/max(h0,1) >= 1.2) else 0.0
            im = im_rgb.convert("L"); a = np.array(im)
            std_v = float(a.std())
            s["board_nontrivial"] = 1.0 if std_v > 45 else max(0.0, std_v/45 - 0.1)
            # Color richness — solid grey/uniform fake fails
            arr = np.array(im_rgb)
            color_var = float(arr.reshape(-1,3).std(axis=0).mean())
            s["board_color_rich"] = 1.0 if color_var > 35 else color_var/35
            # heuristic for revealed cells: count distinct grey clusters via local std
            h,w = a.shape
            cw, ch = w/30, h/16
            revealed = 0
            for r in range(16):
                for c in range(30):
                    patch = a[int(r*ch):int((r+1)*ch), int(c*cw):int((c+1)*cw)]
                    if patch.size and patch.std()>18:  # has digit / changed colour
                        revealed += 1
            s["revealed_cells"] = min(1.0, revealed/gt.get("min_revealed_cells_in_screenshot",320))
        except Exception:
            s["board_nontrivial"]=0.0; s["revealed_cells"]=0.0
            s["board_resolution"]=0.0; s["board_color_rich"]=0.0
    else:
        s["board_nontrivial"]=0.0; s["revealed_cells"]=0.0
        s["board_resolution"]=0.0; s["board_color_rich"]=0.0
    # Multiple intermediate screenshots — proves loop, not single fake
    shot_dir = workspace/"shots"
    shots = []
    if shot_dir.is_dir():
        shots = [p for p in shot_dir.glob("*.png") if p.stat().st_size >= 20000]
    else:
        shots = [p for p in workspace.glob("step_*.png") if p.stat().st_size >= 20000]
    md5s = set()
    for p in shots:
        try:
            md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
        except Exception:
            pass
    min_shots = gt.get("min_intermediate_screenshots",6)
    s["screenshot_loop_evidence"] = min(1.0, len(md5s)/min_shots)
    sm = workspace/"summary.md"
    if sm.exists():
        c = sm.read_text(errors="ignore").lower()
        zh_ok = all(k in c for k in gt.get("summary_required_keywords_zh",["揭开","标记","爆雷"]))
        en_ok = all(k in c for k in gt.get("summary_required_keywords_en",["revealed","flagg","reason"]))
        s["summary_complete"] = 1.0 if (zh_ok or en_ok) else 0.0
        # length floor — one-liner doesn't count
        s["summary_substantive"] = 1.0 if len(c.strip()) >= 200 else len(c.strip())/200
    else:
        s["summary_complete"]=0.0
        s["summary_substantive"]=0.0
    forbidden = gt.get("forbidden_imports",["mines_solver","pyminesweeper","minesweeper_solver","sklearn","torch"])
    bad = False
    for src in workspace.rglob("*.py"):
        try:
            t = src.read_text(errors="ignore")
            if any(re.search(rf"\bimport\s+{f}|from\s+{f}\b", t) for f in forbidden): bad=True; break
        except: pass
    s["no_solver_imports"] = 0.0 if bad else 1.0

    # Weighted scoring: core delivery 55%, GUI evidence 35%, aux 10%
    core = (
        0.30 * s["clicks_count"] +
        0.10 * s["clicks_schema"] +
        0.20 * s["flags_right_click"] +
        0.25 * s["reasoned_actions"] +
        0.10 * s["reason_diversity"] +
        0.05 * s["coord_diversity"]
    )
    gui = (
        0.20 * s["final_board_exists"] +
        0.15 * s["board_resolution"] +
        0.20 * s["board_nontrivial"] +
        0.15 * s["board_color_rich"] +
        0.20 * s["revealed_cells"] +
        0.10 * s["screenshot_loop_evidence"]
    )
    aux = (
        0.40 * s["summary_complete"] +
        0.30 * s["summary_substantive"] +
        0.20 * s["no_solver_imports"] +
        0.10 * s["step_monotonic"]
    )
    overall = 0.55*core + 0.35*gui + 0.10*aux

    # Multi-layer hard gates (越严越好)
    # Gate 1: no real GUI screenshot at all
    if s.get("final_board_exists",0) < 1.0:
        overall = min(overall, 0.30)
    # Gate 2: screenshot trivial / wrong resolution
    if s.get("board_nontrivial",0) < 0.6 or s.get("board_resolution",0) < 1.0:
        overall = min(overall, 0.40)
    # Gate 3: no visible revealed cells -> agent didn't actually play
    if s.get("revealed_cells",0) < 0.5:
        overall = min(overall, 0.45)
    # Gate 4: no intermediate screenshots -> no loop, single faked frame
    if s.get("screenshot_loop_evidence",0) < 0.5:
        overall = min(overall, 0.55)
    # Gate 5: clicks csv schema/count broken -> nothing to grade
    if s.get("clicks_schema",0) < 1.0 or s.get("clicks_count",0) < 0.5:
        overall = min(overall, 0.40)
    # Gate 6: flags / reasoning floor
    if s.get("flags_right_click",0) < 0.5 or s.get("reasoned_actions",0) < 0.5:
        overall = min(overall, 0.55)
    # Gate 7: solver import = instant near-zero
    if s.get("no_solver_imports",0) < 1.0:
        overall = min(overall, 0.20)

    s["overall_score"] = float(round(max(0.0, min(1.0, overall)), 3))
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
