# Auto-generated from WeaveBench task DAV_task_3_tensorboard_hparam_hunt.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DAV_task_3 grader. Empty → 0.000. Hard gates: GUI + CLI + sweep + rerun."""
    import json, csv, re, os, yaml
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. sweep_plan.json
    sp_score = 0.0
    sp = rd / "sweep_plan.json"
    if sp.exists():
        try:
            d = json.loads(sp.read_text())
            if isinstance(d, dict): d = d.get("runs", d.get("sweep", list(d.values())))
            if isinstance(d, list) and len(d) >= 5 and all("lr" in c and "batch_size" in c and "weight_decay" in c for c in d[:5] if isinstance(c, dict)):
                sp_score = 1.0
        except Exception: pass
    s["sweep_plan"] = sp_score

    # 2. tb_logs runs (must include explicit run_1..run_5 dirs, not just any 5 dirs)
    tb_dir = workspace / "tb_logs"
    runs_present = 0
    sweep_run_dirs = 0
    if tb_dir.exists():
        for d in tb_dir.iterdir():
            if d.is_dir() and any(f.name.startswith("events.out.tfevents") for f in d.iterdir()):
                runs_present += 1
        for i in range(1, 6):
            d = tb_dir / f"run_{i}"
            if d.exists() and d.is_dir() and any(f.name.startswith("events.out.tfevents") for f in d.iterdir()):
                sweep_run_dirs += 1
    s["tb_runs"] = min(1.0, sweep_run_dirs / 5)
    has_runs = sweep_run_dirs >= 4

    # 3. CSV exports
    def csv_ok(path, need_cols, min_rows_per_run=50):
        if not path.exists(): return 0.0
        try:
            rows = list(csv.DictReader(path.open()))
            if not rows or not need_cols.issubset(set(rows[0].keys())): return 0.0
            from collections import Counter
            run_counts = Counter(r["run"] for r in rows)
            good_runs = sum(1 for c in run_counts.values() if c >= min_rows_per_run)
            return min(1.0, good_runs / 5)
        except Exception: return 0.0
    s["loss_csv"] = csv_ok(rd / "loss_curves.csv", {"run","step","train_loss"})
    s["acc_csv"]  = csv_ok(rd / "acc_curves.csv",  {"run","step","val_acc"})

    # 4. best_run.json
    br_score = 0.0
    br = rd / "best_run.json"
    if br.exists():
        try:
            d = json.loads(br.read_text())
            if d.get("best_run") and isinstance(d.get("best_final_val_acc"), (int,float)) \
               and isinstance(d.get("best_hparams"), dict) and isinstance(d.get("ranking"), list):
                br_score = 1.0
        except Exception: pass
    s["best_run_json"] = br_score

    # 5. config_backup + new config
    cfg_score = 0.0
    backup = rd / "config_backup.yaml"
    cur_cfg = workspace / "exec" / "config.yaml"
    if backup.exists() and cur_cfg.exists():
        try:
            old = yaml.safe_load(backup.read_text())
            new = yaml.safe_load(cur_cfg.read_text())
            if old != new and new["training"]["epochs"] >= 80:
                cfg_score = 1.0
            elif old != new:
                cfg_score = 0.5
        except Exception: pass
    s["config_modified"] = cfg_score

    # 6. rerun_best_extended exists; try reading TFEvent val/acc tail and compare against best_run.json's best_final_val_acc
    rerun_score = 0.0
    rerun_acc_ok = 0.0
    rerun_dir = tb_dir / "rerun_best_extended"
    rerun_events = []
    if rerun_dir.exists():
        rerun_events = [f for f in rerun_dir.iterdir() if f.name.startswith("events.out.tfevents")]
    if rerun_events:
        rerun_score = 1.0
        try:
            from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
            ea = EventAccumulator(str(rerun_dir))
            ea.Reload()
            tags = ea.Tags().get("scalars", [])
            acc_tag = "val/acc" if "val/acc" in tags else next((t for t in tags if "acc" in t.lower()), None)
            if acc_tag:
                vals = [e.value for e in ea.Scalars(acc_tag)]
                if len(vals) >= 50:
                    final_rerun = sum(vals[-5:]) / min(5, len(vals))
                    prev_best = None
                    if br.exists():
                        try:
                            prev_best = float(json.loads(br.read_text()).get("best_final_val_acc"))
                        except Exception: prev_best = None
                    if prev_best is not None and final_rerun >= prev_best - 0.01:
                        rerun_acc_ok = 1.0
                    elif prev_best is None and final_rerun >= 0.80:
                        rerun_acc_ok = 0.5
        except Exception: pass
    s["rerun_present"] = rerun_score
    s["rerun_acc_ge_best"] = rerun_acc_ok

    # 7. GUI screenshots — require ≥5 KB, unique md5, ≥1024×600 resolution
    gui_shots = ["view_tb_scalars_loss.png","view_tb_scalars_acc.png","view_tb_smoothing.png","view_tb_hparams_parallel.png","view_tb_rerun_verification.png"]
    import hashlib
    gui_present = 0
    md5_set = set()
    res_ok = 0
    for n in gui_shots:
        p = rd / n
        if p.exists() and p.stat().st_size >= 5 * 1024:
            gui_present += 1
            try:
                md5_set.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception: pass
            try:
                from PIL import Image as _PI
                with _PI.open(p) as im:
                    if im.size[0] >= 1024 and im.size[1] >= 600:
                        res_ok += 1
            except Exception: pass
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    s["gui_screenshots_unique"] = len(md5_set) / len(gui_shots) if gui_present else 0.0
    s["gui_screenshots_resolution"] = res_ok / len(gui_shots)
    has_gui = gui_present >= 4 and len(md5_set) >= 4

    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_tb_scalars_loss.png": ["Scalars","train","loss","run"],
            "view_tb_scalars_acc.png": ["val","acc","Scalars","Smoothing"],
            "view_tb_smoothing.png": ["Smoothing","0.6","Scalars"],
            "view_tb_hparams_parallel.png": ["HParams","lr","batch_size","val_acc","Parallel"],
            "view_tb_rerun_verification.png": ["rerun","val","acc"],
        }
        ocr_hits = 0
        for n, ks in kws.items():
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in ks): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
    except Exception:
        s["gui_screenshots_ocr"] = 0.5 if gui_present > 0 else 0.0

    # 8. tooltip_samples.json
    ts_score = 0.0
    ts = rd / "tooltip_samples.json"
    if ts.exists():
        try:
            d = json.loads(ts.read_text())
            samples = d if isinstance(d, list) else d.get("scalars_hover", [])
            if isinstance(samples, list) and len(samples) >= 5:
                ts_score = 1.0
        except Exception: pass
    s["tooltip_samples"] = ts_score

    # 9. sweep_summary.md
    sm_score = 0.0
    sm = rd / "sweep_summary.md"
    if sm.exists():
        try:
            txt = sm.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            sm_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["sweep_summary"] = sm_score

    # 10. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    if vlm_score_rubric and (rd / "view_tb_scalars_acc.png").exists():
        rubric = {
            "vlm_scalars_multiple_runs": "Scalars 截图含多条 run 曲线(图例 ≥ 3 个 run)",
            "vlm_scalars_axes_clear": "X 轴 step / Y 轴 acc 都有清晰刻度",
            "vlm_hparams_parallel_visible": "HParams 截图能看到 Parallel Coordinates 的多维连线",
            "vlm_smoothing_effect": "smoothing 截图曲线明显比未 smooth 平滑",
        }
        try:
            imgs = [str(rd / "view_tb_scalars_acc.png")]
            if (rd / "view_tb_hparams_parallel.png").exists():
                imgs.append(str(rd / "view_tb_hparams_parallel.png"))
            if (rd / "view_tb_smoothing.png").exists():
                imgs.append(str(rd / "view_tb_smoothing.png"))
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 TensorBoard scalars 和 HParams 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        # VLM unavailable → 用结构性 fallback (按 GUI 截图齐备度给 0.5×count)
        fallback = 0.5 * (gui_present / len(gui_shots))
        for k in ["vlm_scalars_multiple_runs","vlm_scalars_axes_clear","vlm_hparams_parallel_visible","vlm_smoothing_effect"]:
            s[k] = fallback

    # weighted aggregation: core delivery 60% / GUI evidence 30% / aux 10%
    core_keys = ["sweep_plan","tb_runs","loss_csv","acc_csv","best_run_json","config_modified","rerun_present","rerun_acc_ge_best"]
    gui_keys  = ["gui_screenshots_count","gui_screenshots_unique","gui_screenshots_resolution","gui_screenshots_ocr",
                 "vlm_scalars_multiple_runs","vlm_scalars_axes_clear","vlm_hparams_parallel_visible","vlm_smoothing_effect"]
    aux_keys  = ["tooltip_samples","sweep_summary"]
    def _avg(keys):
        vs = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vs) / len(vs) if vs else 0.0
    core = _avg(core_keys); gui = _avg(gui_keys); aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Hard gates (stricter)
    if not has_runs: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.30)
    if s["sweep_plan"] < 1.0: base = min(base, 0.40)
    if s["best_run_json"] < 1.0: base = min(base, 0.45)
    if s["rerun_present"] < 1.0: base = min(base, 0.45)
    if s["rerun_acc_ge_best"] < 1.0: base = min(base, 0.55)
    if s["config_modified"] < 1.0: base = min(base, 0.55)
    if s["gui_screenshots_ocr"] < 0.4: base = min(base, 0.50)
    # VLM-unavailable cap: when all four vlm_* equal the structural fallback (≤0.5), cap at 0.6
    vlm_vals = [s.get(k, 0.0) for k in ["vlm_scalars_multiple_runs","vlm_scalars_axes_clear","vlm_hparams_parallel_visible","vlm_smoothing_effect"]]
    if vlm_vals and max(vlm_vals) <= 0.5: base = min(base, 0.60)

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
