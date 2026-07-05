# Auto-generated from WeaveBench task GAM_task_2_mines_visual.
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
    """Stricter GAM_2: require min_revealed_cells from board image, no solver libs, reasoned >=100."""
    _gt_path = workspace.parent / "gt" / "expected.json"
    if not _gt_path.exists():
        _gt_path = Path("/tmp_workspace/gt/expected.json")
    gt = json.loads(_gt_path.read_text()) if _gt_path.exists() else {}
    s = {}
    cf = workspace/"clicks.csv"
    rows = []
    if cf.exists():
        rows = list(csv.DictReader(cf.open()))
    s["clicks_count"] = min(1.0, len(rows)/gt.get("min_clicks",200))
    s["clicks_schema"] = 1.0 if rows and all(k in rows[0] for k in ["step","action","x","y","reason"]) else 0.0
    flags = sum(1 for x in rows if x.get("action")=="right")
    s["flags_right_click"] = min(1.0, flags/gt.get("min_flags_right_click",80))
    reasoned = sum(1 for x in rows if re.search(r"(safe|flag)-by-?\w*", x.get("reason","")))
    s["reasoned_actions"] = min(1.0, reasoned/gt.get("min_reasoned_actions",100))
    # diversity of reasons
    distinct_reasons = len(set(x.get("reason","").split("-")[0] for x in rows))
    s["reason_diversity"] = min(1.0, distinct_reasons/3)
    fb = workspace/"final_board.png"
    fb_size = fb.stat().st_size if fb.exists() else 0
    s["final_board_exists"] = 1.0 if (fb.exists() and fb_size >= 5120) else 0.0
    s["final_board_md5"] = hashlib.md5(fb.read_bytes()).hexdigest()[:10] if fb.exists() else ""
    s["final_board_resolution_ok"] = 0.0
    if fb.exists() and fb_size >= 5120:
        try:
            im = Image.open(fb).convert("L"); a = np.array(im)
            h,w = a.shape
            s["final_board_resolution_ok"] = 1.0 if (w >= 1024 and h >= 600) else 0.0
            s["board_nontrivial"] = 1.0 if a.std()>40 else a.std()/40
            cw, ch = w/30, h/16
            revealed = 0
            for r in range(16):
                for c in range(30):
                    patch = a[int(r*ch):int((r+1)*ch), int(c*cw):int((c+1)*cw)]
                    if patch.size and patch.std()>15:
                        revealed += 1
            s["revealed_cells_raw"] = revealed
            s["revealed_cells"] = min(1.0, revealed/gt.get("min_revealed_cells_in_screenshot",380))
        except Exception as e:
            s["board_nontrivial"]=0.0; s["revealed_cells"]=0.0
    else:
        s["board_nontrivial"]=0.0; s["revealed_cells"]=0.0
    sm = workspace/"summary.md"
    if sm.exists():
        c = sm.read_text(errors="ignore").lower()
        zh_ok = all(k in c for k in gt.get("summary_required_keywords_zh",["揭开","标记"]))
        en_ok = all(k in c for k in gt.get("summary_required_keywords_en",["revealed","flagg"]))
        s["summary_complete"] = 1.0 if (zh_ok or en_ok) else 0.0
    else:
        s["summary_complete"]=0.0
    forbidden = gt.get("forbidden_imports",["mines_solver","pyminesweeper"])
    bad = False
    for src in workspace.rglob("*.py"):
        try:
            t = src.read_text(errors="ignore")
            if any(re.search(rf"\bimport\s+{f}|from\s+{f}\b", t) for f in forbidden): bad=True; break
        except: pass
    s["no_solver_imports"] = 0.0 if bad else 1.0
    # Weighted overall: 60% core delivery / 30% GUI evidence / 10% aux
    core_keys = ["clicks_count","flags_right_click","reasoned_actions","revealed_cells",
                 "summary_complete","final_board_exists"]
    gui_keys  = ["board_nontrivial","final_board_resolution_ok","no_solver_imports"]
    aux_keys  = ["clicks_schema","reason_diversity"]
    def _avg(keys):
        vals = [float(s.get(k,0.0)) for k in keys]
        return sum(vals)/len(vals) if vals else 0.0
    core = _avg(core_keys); gui = _avg(gui_keys); aux = _avg(aux_keys)
    s["core_score"], s["gui_score"], s["aux_score"] = core, gui, aux
    s["overall_score"] = 0.6*core + 0.3*gui + 0.1*aux
    # Multi-tier hard gates
    if s.get("final_board_exists",0) < 1 or s.get("summary_complete",0) < 1:
        s["overall_score"] = min(float(s["overall_score"]), 0.40)
    if s.get("revealed_cells",0) < 0.7:
        s["overall_score"] = min(float(s["overall_score"]), 0.45)
    if s.get("revealed_cells",0) < 0.4:
        s["overall_score"] = min(float(s["overall_score"]), 0.30)
    if s.get("reasoned_actions",0) < 0.6:
        s["overall_score"] = min(float(s["overall_score"]), 0.50)
    if s.get("final_board_resolution_ok",0) < 1:
        s["overall_score"] = min(float(s["overall_score"]), 0.55)
    if s.get("no_solver_imports",1) < 1:
        s["overall_score"] = min(float(s["overall_score"]), 0.30)

    # ----- BEGIN CHEAT/VLM HARD-GATE (auto-injected) -----
    try:
        from _judge_helper import audit_chat_jsonl_for_banned as _audit
    except Exception:
        _audit = None
    _BANS = ['gnome-mines --solve', 'dconf read', '/dev/shm/mines']
    if _audit is not None:
        try:
            _a = _audit(_BANS)
            s["audit_total_tool_calls"] = _a.get("total_tool_calls", 0)
            s["audit_screenshots"] = _a.get("computer_screenshots", 0)
            s["audit_any_banned"] = 1.0 if _a.get("any_banned") else 0.0
            s["audit_matches"] = ",".join(_a.get("matches", [])[:5])
            if _a.get("any_banned"):
                s["overall_score"] = min(float(s.get("overall_score", 1.0)), 0.25)
            if _a.get("total_tool_calls", 0) >= 5 and _a.get("computer_screenshots", 0) == 0:
                s["overall_score"] = min(float(s.get("overall_score", 1.0)), 0.40)
            # GUI 真实交互证据：截图数下限（visual loop 至少 ~30 次截图）
            if _a.get("computer_screenshots", 0) < 30:
                s["overall_score"] = min(float(s.get("overall_score", 1.0)), 0.55)
            if _a.get("computer_screenshots", 0) < 10:
                s["overall_score"] = min(float(s.get("overall_score", 1.0)), 0.40)
        except Exception as _e:
            s["audit_error"] = str(_e)[:120]
    else:
        # VLM helper unavailable → cap (no semantic check possible)
        s["overall_score"] = min(float(s.get("overall_score", 1.0)), 0.60)
    # ----- END CHEAT/VLM HARD-GATE -----
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
