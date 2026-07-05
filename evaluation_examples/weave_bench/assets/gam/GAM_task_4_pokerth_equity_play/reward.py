# Auto-generated from WeaveBench task GAM_task_4_pokerth_equity_play.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import csv, re, json
from pathlib import Path
from PIL import Image
import numpy as np

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    gt_path = Path("/tmp_workspace/gt/expected.json")
    gt = json.loads(gt_path.read_text()) if gt_path.exists() else {}
    s = {}

    # 1. hands.csv row count
    cf = rd / "hands.csv"
    rows = []
    if cf.exists():
        rows = list(csv.DictReader(cf.open()))
    min_hands = gt.get("min_hands", 10)
    s["hands_count"] = min(1.0, len(rows) / min_hands)

    # 2. CSV schema
    req = ["hand_num", "hole_cards", "community_cards", "street",
           "equity_pct", "decision", "pot_size", "result"]
    s["csv_schema"] = 1.0 if rows and all(k in rows[0] for k in req) else 0.0

    # 3. hole_cards format (e.g. "Ah Kd")
    card_pat = re.compile(r"^[2-9TJQKA][shdc]\s+[2-9TJQKA][shdc]$")
    valid_hc = sum(1 for r in rows if card_pat.match(r.get("hole_cards", "").strip()))
    s["hole_cards_valid"] = min(1.0, valid_hc / max(1, len(rows)))

    # 4. equity_pct range
    eq_ok = 0
    for r in rows:
        try:
            e = float(r.get("equity_pct", -1))
            if 0 <= e <= 100:
                eq_ok += 1
        except (ValueError, TypeError):
            pass
    s["equity_range_valid"] = min(1.0, eq_ok / max(1, len(rows)))

    # 5. decision validity
    valid_dec = {"Fold", "Call", "Raise", "fold", "call", "raise"}
    dec_ok = sum(1 for r in rows if r.get("decision", "").strip() in valid_dec)
    s["decision_valid"] = min(1.0, dec_ok / max(1, len(rows)))

    # 5b. result column semantic validity (W/L/Fold)
    valid_res = {"W", "L", "Fold", "w", "l", "fold"}
    res_ok = sum(1 for r in rows if r.get("result", "").strip() in valid_res)
    s["result_valid"] = min(1.0, res_ok / max(1, len(rows)))

    # 6. decision rationality: avg equity of Fold < avg equity of Call
    fold_eq, call_eq = [], []
    for r in rows:
        try:
            e = float(r.get("equity_pct", 50))
            d = r.get("decision", "").strip().lower()
            if d == "fold":
                fold_eq.append(e)
            elif d in ("call", "raise"):
                call_eq.append(e)
        except (ValueError, TypeError):
            pass
    if fold_eq and call_eq:
        s["decision_rationality"] = 1.0 if np.mean(fold_eq) < np.mean(call_eq) else 0.0
    else:
        s["decision_rationality"] = 0.0  # not enough data to judge

    # 7. hand screenshots
    hand_shots = list(rd.glob("hand_*.png"))
    min_shots = gt.get("min_hand_screenshots", 10)
    s["hand_screenshots"] = min(1.0, len(hand_shots) / min_shots)

    # 8. equity_log.json
    ej = rd / "equity_log.json"
    s["equity_log_exists"] = 0.0
    if ej.exists():
        try:
            data = json.loads(ej.read_text())
            s["equity_log_exists"] = 1.0 if len(data) >= 5 else len(data) / 5
        except Exception:
            pass

    # 9. final_table.png
    ft = rd / "final_table.png"
    s["final_table_exists"] = 0.0
    s["table_nontrivial"] = 0.0
    if ft.exists():
        s["final_table_exists"] = 1.0
        try:
            im = Image.open(ft).convert("RGB")
            a = np.array(im)
            s["table_nontrivial"] = 1.0 if a.std() > 40 else a.std() / 40
        except Exception:
            pass

    # 10. summary.md
    sm = rd / "summary.md"
    if sm.exists():
        c = sm.read_text(errors="ignore").lower()
        zh = all(k in c for k in gt.get("summary_keywords_zh", ["手数", "胜", "筹码"]))
        en = all(k in c for k in gt.get("summary_keywords_en", ["hand", "win", "chip"]))
        s["summary_complete"] = 1.0 if (zh or en) else 0.0
    else:
        s["summary_complete"] = 0.0

    # 11. no solver imports
    forbidden = gt.get("forbidden_imports", ["poker_solver", "poker_ai_agent"])
    bad = False
    for src in workspace.rglob("*.py"):
        try:
            t = src.read_text(errors="ignore")
            if any(re.search(rf"\bimport\s+{f}|from\s+{f}\b", t) for f in forbidden):
                bad = True; break
        except Exception:
            pass
    s["no_solver_imports"] = 0.0 if bad else 1.0

    # 12. VLM rubric (optional)
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    rubric_keys = ["vlm_table_visible", "vlm_cards_visible", "vlm_buttons_visible"]
    if vlm_score_rubric and ft.exists():
        rubric = {
            "vlm_table_visible": "截图中能看到扑克牌桌，有牌面和筹码",
            "vlm_cards_visible": "截图中能看到手牌和/或公共牌",
            "vlm_buttons_visible": "截图中能看到 Call/Fold/Raise 按钮区域",
        }
        vlm = vlm_score_rubric([str(ft)], rubric,
                               instruction="Evaluate the PokerTH table screenshot.")
        for k in rubric:
            s[k] = vlm.get(k, 0.5)
    else:
        # VLM unavailable → structural fallback: neutral 0.5 to avoid pulling base down
        for k in rubric_keys:
            s[k] = 0.5

    # --- Content-authenticity sub-scores ---
    n_hands = len(rows)
    n_shots = len(hand_shots)
    s["hand_shots_per_hand"] = 0.0
    if n_hands > 0:
        s["hand_shots_per_hand"] = min(1.0, n_shots / n_hands)

    # equity_log row count (accept .csv or .json)
    log_rows_count = 0
    ej_csv = rd / "equity_log.csv"
    if ej_csv.exists():
        try:
            log_rows_count = sum(1 for _ in csv.DictReader(ej_csv.open()))
        except Exception:
            pass
    elif ej.exists():
        try:
            d = json.loads(ej.read_text())
            log_rows_count = len(d) if isinstance(d, list) else 0
        except Exception:
            pass
    s["equity_log_rows_ge10"] = min(1.0, log_rows_count / 12)

    # preflop / postflop decision streets present in hands.csv
    streets = set(r.get("street", "").strip().lower() for r in rows)
    has_pre = any("pre" in st for st in streets)
    has_post = any(st in ("flop", "turn", "river", "post", "postflop")
                   for st in streets)
    if has_pre and has_post:
        s["preflop_postflop_fields"] = 1.0
    elif has_pre or has_post:
        s["preflop_postflop_fields"] = 0.5
    else:
        s["preflop_postflop_fields"] = 0.0

    # --- Weighted aggregation: core 60% / gui 30% / aux 10% ---
    core_keys = [
        "hands_count", "csv_schema", "hole_cards_valid", "equity_range_valid",
        "decision_valid", "result_valid", "decision_rationality",
        "equity_log_exists", "equity_log_rows_ge10",
        "preflop_postflop_fields", "no_solver_imports",
    ]
    gui_keys = [
        "hand_screenshots", "hand_shots_per_hand",
        "final_table_exists", "table_nontrivial",
        "vlm_table_visible", "vlm_cards_visible", "vlm_buttons_visible",
    ]
    aux_keys = ["summary_complete"]

    def _avg(keys):
        vs = [float(s[k]) for k in keys if k in s]
        return sum(vs) / len(vs) if vs else 0.0

    core_score = _avg(core_keys)
    gui_score = _avg(gui_keys)
    aux_score = _avg(aux_keys)
    s["core_score"] = round(core_score, 4)
    s["gui_score"] = round(gui_score, 4)
    s["aux_score"] = round(aux_score, 4)

    base = 0.6 * core_score + 0.3 * gui_score + 0.1 * aux_score

    # --- Hard gates (single layer, no stacked stair-step caps) ---
    # G1: no CSV/log evidence at all → near-zero
    if s.get("hands_count", 0) == 0 and s.get("csv_schema", 0) == 0:
        base = min(base, 0.05)
    # G2: core delivery weak → cap 0.4
    if core_score < 0.6:
        base = min(base, 0.4)
    # G3: GUI evidence weak (no real interaction with PokerTH) → cap 0.4
    if gui_score < 0.5:
        base = min(base, 0.4)
    # G4: forbidden solver imports → hard cap 0.3
    if s.get("no_solver_imports", 0) < 1.0:
        base = min(base, 0.3)
    # G5: decision rationality failed (Fold avg equity ≥ Call avg) → cap 0.5
    if s.get("decision_rationality", 0) < 1.0:
        base = min(base, 0.5)
    # G6: VLM available and clearly fails (real screenshot doesn't show table) → cap 0.45
    vlm_used = vlm_score_rubric is not None and ft.exists()
    if vlm_used:
        vlm_avg = (s.get("vlm_table_visible", 0) + s.get("vlm_cards_visible", 0)
                   + s.get("vlm_buttons_visible", 0)) / 3.0
        if vlm_avg < 0.4:
            base = min(base, 0.45)
    else:
        # VLM unavailable → cannot prove real GUI interaction → cap 0.6
        base = min(base, 0.6)

    s["overall_score"] = round(max(0.0, base), 4)
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
