# Auto-generated from WeaveBench task GAM_task_6_rhythm_autoplay.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """GAM_task_6 grader. Empty → 0.000-0.05. Hard gates: GUI + CLI + hit rate."""
    import json, csv, re, hashlib
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. CSV files
    csv_score_easy = 0.0; csv_score_medium = 0.0
    sched = rd / "schedule_easy.csv"
    if sched.exists():
        try:
            rows = list(csv.DictReader(sched.open()))
            need = {"step","target_ms","lane","key"}
            if rows and need.issubset(set(rows[0].keys())) and len(rows) >= 15:
                csv_score_easy = 1.0
        except Exception: pass
    s["schedule_csv"] = csv_score_easy

    hits_easy_path = rd / "hits_easy.csv"
    hits_easy_rows = []
    if hits_easy_path.exists():
        try:
            hits_easy_rows = list(csv.DictReader(hits_easy_path.open()))
            need = {"step","target_ms","actual_ms","lane","hit_or_miss"}
            if hits_easy_rows and need.issubset(set(hits_easy_rows[0].keys())):
                s["hits_csv_schema"] = 1.0
            else:
                s["hits_csv_schema"] = 0.5
        except Exception:
            s["hits_csv_schema"] = 0.0
    else:
        s["hits_csv_schema"] = 0.0

    # 2. screen_calibration.json
    cal_score = 0.0
    cal = rd / "screen_calibration.json"
    if cal.exists():
        try:
            d = json.loads(cal.read_text())
            lanes = d.get("lanes", [])
            if (isinstance(lanes, list) and len(lanes) >= 4
                and all("x_px" in l for l in lanes[:4])
                and isinstance(d.get("judge_line_y_px"), (int,float))):
                cal_score = 1.0
        except Exception: pass
    s["screen_calibration"] = cal_score

    # Load expected.json (host-side GT) if present, to keep grader & GT in sync.
    expected = {}
    for cand in [workspace / "gt" / "expected.json",
                 workspace.parent / "gt" / "expected.json"]:
        if cand.exists():
            try: expected = json.loads(cand.read_text())
            except Exception: expected = {}
            break
    extra_forbidden = list(expected.get("forbidden_imports", []) or [])
    exp_min_avg_acc = float(expected.get("min_avg_accuracy", 0.55) or 0.55)
    exp_min_total_hits = int(expected.get("min_total_hits_logged", 30) or 30)
    exp_min_step_shots = int(expected.get("min_step_screenshots", 4) or 4)
    exp_judg_keys = list(expected.get("judgment_keywords", []) or [])
    exp_sum_zh = list(expected.get("summary_keywords_zh", []) or [])
    exp_sum_en = list(expected.get("summary_keywords_en", []) or [])

    # 3. inject_loop.py exists + uses real key-injection tool + no forbidden imports
    inj_score = 0.0
    inj = rd / "inject_loop.py"
    if inj.exists():
        try:
            txt = inj.read_text()
            forbidden = ["rhythm_bot","autoplay_bot","beatmap_solver","stepmania_bot"] + extra_forbidden
            uses_xdotool = bool(re.search(r"""(?m)^[^#\n]*xdotool""", txt))
            no_bad = not any(re.search(rf"\bimport\s+{f}\b|from\s+{f}\b", txt) for f in forbidden)
            if uses_xdotool and no_bad:
                inj_score = 1.0
        except Exception: pass
    s["inject_loop"] = inj_score

    # 4. GUI screenshots (≥ 50KB each, md5-unique to prevent duplicate cheating)
    gui_shots = ["view_game_start.png","view_game_step1.png","view_game_step2.png","view_game_step3.png",
                 "view_game_final_easy.png","view_game_final_medium.png"]
    gui_present = 0
    md5s = set()
    for n in gui_shots:
        p = rd / n
        if p.exists() and p.stat().st_size >= 50000:
            try:
                h = hashlib.md5(p.read_bytes()).hexdigest()
                if h in md5s:
                    continue  # duplicate / copied screenshot does not count
                md5s.add(h)
                gui_present += 1
            except Exception:
                pass
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    s["gui_screenshots_unique"] = 1.0 if len(md5s) >= len(gui_shots) else len(md5s) / len(gui_shots)
    has_gui = gui_present >= 3
    # step screenshots specifically
    step_shots = sum(1 for n in ["view_game_step1.png","view_game_step2.png","view_game_step3.png"]
                     if (rd / n).exists() and (rd / n).stat().st_size >= 50000)
    s["step_screenshots_min"] = 1.0 if step_shots >= min(3, exp_min_step_shots) else step_shots / max(1, min(3, exp_min_step_shots))

    # 5. game logs + judgment keywords (real game must emit PERFECT/GREAT/GOOD/MISS)
    has_easy_log = (rd / "game_easy.log").exists() and (rd / "game_easy.log").stat().st_size > 0
    has_medium_log = (rd / "game_medium.log").exists() and (rd / "game_medium.log").stat().st_size > 0
    s["game_logs"] = ((1.0 if has_easy_log else 0.0) + (1.0 if has_medium_log else 0.0)) / 2
    judg_hit = 0
    if exp_judg_keys:
        for ln in ("game_easy.log", "game_medium.log"):
            p = rd / ln
            if p.exists():
                try:
                    t = p.read_text(errors="ignore").upper()
                    judg_hit += sum(1 for k in exp_judg_keys if k.upper() in t)
                except Exception:
                    pass
        # require at least half of judgment keywords to appear across both logs
        need = max(1, len(exp_judg_keys) // 2)
        s["judgment_keywords_in_log"] = 1.0 if judg_hit >= need else judg_hit / max(1, need * 2)
    else:
        s["judgment_keywords_in_log"] = 1.0

    # 6. hit rates
    def hit_rate(rows):
        if not rows: return 0.0
        hits = sum(1 for r in rows if str(r.get("hit_or_miss","")).lower() in ("hit","ok","perfect","good"))
        return hits / len(rows) if rows else 0.0
    er = hit_rate(hits_easy_rows)
    s["easy_hit_rate"] = 1.0 if er >= 0.90 else (er / 0.90)
    hits_med_path = rd / "hits_medium.csv"
    hits_med_rows = []
    if hits_med_path.exists():
        try: hits_med_rows = list(csv.DictReader(hits_med_path.open()))
        except Exception: pass
    mr = hit_rate(hits_med_rows)
    s["medium_hit_rate"] = 1.0 if mr >= 0.75 else (mr / 0.75)

    # 7. summary.md (≥ 4 paragraphs of ≥ 80 chars + bilingual keyword coverage)
    sm_score = 0.0
    sm_keys_score = 0.0
    sm = rd / "summary.md"
    if sm.exists():
        try:
            txt = sm.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            sm_score = min(1.0, len(parags) / 4)
            zh_hit = sum(1 for k in exp_sum_zh if k in txt)
            en_hit = sum(1 for k in (exp_sum_en or []) if k.lower() in txt.lower())
            zh_ratio = zh_hit / max(1, len(exp_sum_zh)) if exp_sum_zh else 1.0
            en_ratio = en_hit / max(1, len(exp_sum_en)) if exp_sum_en else 1.0
            sm_keys_score = (zh_ratio + en_ratio) / 2
        except Exception: pass
    s["summary"] = sm_score
    s["summary_keywords"] = sm_keys_score

    # 8. VLM rubric
    vlm_available = False
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    if vlm_score_rubric and (rd / "view_game_start.png").exists():
        rubric = {
            "vlm_game_window": "截图能看到 4-lane rhythm game window",
            "vlm_lanes_visible": "4 个 lane 颜色 / 边界清晰可辨",
            "vlm_score_visible": "截图能看到 score / combo / hit 数字",
            "vlm_notes_falling": "play 中截图能看到 note 在 lane 里",
        }
        try:
            imgs = [str(rd / n) for n in ["view_game_start.png","view_game_step1.png","view_game_final_easy.png"] if (rd / n).exists()]
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 4-lane rhythm game 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
            vlm_available = True
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_game_window","vlm_lanes_visible","vlm_score_visible","vlm_notes_falling"]:
            s[k] = 0.0

    # --- Content-authenticity sub-scores ---
    s["hits_easy_rate_ge_06"] = 1.0 if er >= 0.6 else 0.0
    s["hits_medium_rate_ge_06"] = 1.0 if mr >= 0.6 else 0.0
    s["hits_csv_full_schema"] = 1.0 if (
        s.get("hits_csv_schema", 0) == 1.0 and len(hits_easy_rows) >= 15
    ) else 0.0
    # Expected-aligned authenticity: total hits across both maps + min average accuracy
    total_logged = len(hits_easy_rows) + len(hits_med_rows)
    s["total_hits_logged"] = 1.0 if total_logged >= exp_min_total_hits else total_logged / max(1, exp_min_total_hits)
    avg_acc = (er + mr) / 2
    s["avg_accuracy_meets_min"] = 1.0 if avg_acc >= exp_min_avg_acc else (avg_acc / max(0.01, exp_min_avg_acc))

    # Stricter forbidden imports check across full workspace
    forbidden_all = list(set(["rhythm_bot", "autoplay_bot", "beatmap_solver",
                              "stepmania_bot", "osu_bot", "rhythm_solver"]
                             + extra_forbidden))
    bad_import = False
    for src in workspace.rglob("*.py"):
        try:
            t = src.read_text(errors="ignore")
            if any(re.search(rf"\bimport\s+{f}\b|from\s+{f}\b", t)
                   for f in forbidden_all):
                bad_import = True
                break
        except Exception:
            pass
    s["no_bot_framework_imports"] = 0.0 if bad_import else 1.0

    nums = [v for v in s.values() if isinstance(v, (int, float))]
    naive_mean = sum(nums) / len(nums) if nums else 0.0

    # Weighted aggregate: core delivery 0.6, GUI evidence 0.3, auxiliary 0.1
    def _avg(keys):
        vs = [float(s.get(k, 0.0)) for k in keys]
        return sum(vs) / len(vs) if vs else 0.0
    core_keys = ["schedule_csv","hits_csv_schema","screen_calibration","inject_loop",
                 "easy_hit_rate","medium_hit_rate","game_logs",
                 "hits_csv_full_schema","hits_easy_rate_ge_06","hits_medium_rate_ge_06",
                 "total_hits_logged","avg_accuracy_meets_min","no_bot_framework_imports",
                 "judgment_keywords_in_log"]
    gui_keys  = ["gui_screenshots_count","gui_screenshots_unique","step_screenshots_min",
                 "vlm_game_window","vlm_lanes_visible","vlm_score_visible","vlm_notes_falling"]
    aux_keys  = ["summary","summary_keywords"]
    base = 0.6 * _avg(core_keys) + 0.3 * _avg(gui_keys) + 0.1 * _avg(aux_keys)

    # hard gates (stricter than v1)
    if not has_gui: base = min(base, 0.05)  # empty workspace must give 0.000-0.05
    if not has_easy_log: base = min(base, 0.25)
    if not has_medium_log: base = min(base, 0.45)
    if s["inject_loop"] < 1.0: base = min(base, 0.40)
    if s["screen_calibration"] < 1.0: base = min(base, 0.50)
    if s["easy_hit_rate"] < 0.6: base = min(base, 0.55)
    # Content-authenticity stair-step caps
    if s.get("hits_csv_full_schema", 0) < 1.0:
        base = min(base, 0.45)
    if s.get("hits_easy_rate_ge_06", 0) < 1.0:
        base = min(base, 0.50)
    if s.get("hits_medium_rate_ge_06", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("no_bot_framework_imports", 0) < 1.0:
        base = min(base, 0.30)
    # Expected.json authenticity gates
    if s.get("total_hits_logged", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("avg_accuracy_meets_min", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("judgment_keywords_in_log", 0) < 0.5:
        base = min(base, 0.50)
    # GUI authenticity: unique screenshots required
    if s.get("gui_screenshots_unique", 0) < 0.7:
        base = min(base, 0.45)
    if s.get("step_screenshots_min", 0) < 1.0:
        base = min(base, 0.55)
    # VLM-unavailable cap (cannot be a free pass when VLM is down)
    if not vlm_available:
        base = min(base, 0.60)
    else:
        vlm_avg = _avg(["vlm_game_window","vlm_lanes_visible","vlm_score_visible","vlm_notes_falling"])
        if vlm_avg < 0.4: base = min(base, 0.30)
        elif vlm_avg < 0.6: base = min(base, 0.45)

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
