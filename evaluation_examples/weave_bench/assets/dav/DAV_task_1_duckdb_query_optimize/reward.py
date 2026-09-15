# Auto-generated from WeaveBench task DAV_task_1_duckdb_query_optimize.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DAV_task_1 grader. Empty workspace → 0.000. Hard gates: GUI + CLI evidence both required."""
    import json, csv, re
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    gt_dir = workspace / "gt"
    gt = {}
    if (gt_dir / "expected.json").exists():
        try: gt = json.loads((gt_dir / "expected.json").read_text())
        except Exception: pass
    s = {}

    # 1. CLI artifacts presence
    explain_files = ["schema.txt"] + [f"explain_q{i}_before.txt" for i in (1,2,3,4)] + [f"explain_q{i}_after.txt" for i in (1,2,3,4)]
    cli_present = sum(1 for f in explain_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(explain_files)
    has_cli_evidence = cli_present >= 5

    # 2. bottleneck_analysis.json structure + content
    ba_score = 0.0
    ba_path = rd / "bottleneck_analysis.json"
    if ba_path.exists():
        try:
            ba = json.loads(ba_path.read_text())
            valid_ops = {"SEQ_SCAN","HASH_JOIN","HASH_GROUP_BY","WINDOW","NESTED_LOOP_JOIN","FILTER","PROJECTION","SORT"}
            ok_n = 0
            for k in ("q1","q2","q3","q4"):
                if isinstance(ba.get(k), dict):
                    if str(ba[k].get("bottleneck_op","")).upper() in valid_ops and \
                       isinstance(ba[k].get("wall_time_ms"), (int,float)) and \
                       len(str(ba[k].get("description",""))) >= 10:
                        ok_n += 1
            ba_score = ok_n / 4
            # 若 gt 提供 bottleneck_op,做一次成员校验加分项
            if gt:
                match_n = 0; total_n = 0
                for k in ("q1","q2","q3","q4"):
                    gt_op = str((gt.get(k) or {}).get("bottleneck_op","")).upper() if isinstance(gt.get(k), dict) else ""
                    if gt_op:
                        total_n += 1
                        if isinstance(ba.get(k), dict) and str(ba[k].get("bottleneck_op","")).upper() == gt_op:
                            match_n += 1
                if total_n:
                    s["bottleneck_op_match"] = match_n / total_n
        except Exception: pass
    s["bottleneck_analysis"] = ba_score

    # 3. optimized_sql files
    opt_dir = rd / "optimized_sql"
    sql_present = 0
    if opt_dir.exists():
        for n in (1,2,3,4):
            f = opt_dir / f"q{n}.sql"
            if f.exists() and len(f.read_text().strip()) >= 30:
                sql_present += 1
    s["optimized_sql"] = sql_present / 4

    # 4. perf_comparison.csv
    perf_score = 0.0; speedup_score = 0.0
    pf = rd / "perf_comparison.csv"
    if pf.exists():
        try:
            rows = list(csv.DictReader(pf.open()))
            need_cols = {"query_id","wall_time_before_ms","wall_time_after_ms","speedup_x","bottleneck_before","bottleneck_after"}
            if rows and need_cols.issubset(set(rows[0].keys())):
                perf_score = 1.0
                speedups = []
                for r in rows:
                    try: speedups.append(float(str(r["speedup_x"]).rstrip("x")))
                    except: pass
                if speedups:
                    good = sum(1 for x in speedups if x >= 5.0)
                    speedup_score = good / max(4, len(speedups))
        except Exception: pass
    s["perf_csv_schema"] = perf_score
    s["speedup_targets"] = speedup_score

    # 5. GUI screenshots — count + size floor (>=5KB) + md5 uniqueness (anti-cheat)
    import hashlib
    gui_shots = ["view_sqllab_q1_running.png","view_query_history_tooltip.png",
                 "view_explore_chart.png","view_dashboard_full.png","view_sqllab_after_optimization.png"]
    gui_paths = [(n, rd / n) for n in gui_shots]
    gui_present = sum(1 for _, p in gui_paths if p.exists())
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui = gui_present >= 3
    md5s = []
    sized_ok = 0
    for _, p in gui_paths:
        if p.exists():
            try:
                b = p.read_bytes()
                if len(b) >= 5 * 1024:
                    sized_ok += 1
                    md5s.append(hashlib.md5(b).hexdigest())
            except Exception: pass
    s["gui_screenshots_size_floor"] = sized_ok / len(gui_shots)
    s["gui_screenshots_md5_unique"] = (len(set(md5s)) / len(gui_shots)) if md5s else 0.0

    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_sqllab_q1_running.png": ["SQL","Lab","Run","Result"],
            "view_query_history_tooltip.png": ["Query","History","duration","wall"],
            "view_explore_chart.png": ["Explore","Chart","Customize","X-axis"],
            "view_dashboard_full.png": ["Dashboard","Markdown","insight"],
            "view_sqllab_after_optimization.png": ["SQL","Lab","Query","History"],
        }
        ocr_hits = 0
        for n, ks in kws.items():
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k in tx for k in ks): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
    except Exception:
        s["gui_screenshots_ocr"] = 0.5 if gui_present > 0 else 0.0

    # 6. tooltip_samples.json
    ts = rd / "tooltip_samples.json"
    ts_score = 0.0
    if ts.exists():
        try:
            d = json.loads(ts.read_text())
            arr = d.get("explore_chart_hover", [])
            if isinstance(arr, list) and len(arr) >= 3 and \
               all(isinstance(x, dict) and "hour" in x and "trip_count" in x for x in arr):
                ts_score = 1.0
        except Exception: pass
    s["tooltip_samples"] = ts_score

    # 7. perf_report.md
    rp = rd / "perf_report.md"
    rp_score = 0.0
    if rp.exists():
        try:
            txt = rp.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            rp_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["perf_report"] = rp_score

    # 8. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    dashboard_png_exists = (rd / "view_dashboard_full.png").exists()
    if vlm_score_rubric and dashboard_png_exists:
        rubric = {
            "vlm_dashboard_has_chart": "截图里有可见的时序 chart(横轴 hour,纵轴 trip_count)",
            "vlm_dashboard_has_markdown": "截图里有 markdown 文本块,内容是优化总结/insight",
            "vlm_layout_clean": "整体 dashboard 布局整齐没有空白/重叠",
            "vlm_superset_branding": "顶部能看到 Superset navbar 和导航",
        }
        try:
            vlm = vlm_score_rubric([str(rd / "view_dashboard_full.png")], rubric, instruction="评估 Superset dashboard 截图的可视化质量。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            for k in rubric: s[k] = 0.0
        vlm_unavailable = False
    else:
        # 无 VLM 时给一个保守的结构性 fallback（不能让无 VLM 也满分）
        vlm_unavailable = True
        fallback_v = 0.3 if dashboard_png_exists else 0.0
        for k in ["vlm_dashboard_has_chart","vlm_dashboard_has_markdown","vlm_layout_clean","vlm_superset_branding"]:
            s[k] = fallback_v

    # ---- 加权聚合：core 60% / gui 30% / aux 10% ----
    def _avg(keys):
        vs = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vs) / len(vs) if vs else 0.0
    core_keys = ["cli_artifacts","bottleneck_analysis","optimized_sql",
                 "perf_csv_schema","speedup_targets"]
    if "bottleneck_op_match" in s:
        core_keys.append("bottleneck_op_match")
    gui_keys  = ["gui_screenshots_count","gui_screenshots_ocr",
                 "gui_screenshots_size_floor","gui_screenshots_md5_unique","tooltip_samples"]
    aux_keys  = ["perf_report","vlm_dashboard_has_chart","vlm_dashboard_has_markdown",
                 "vlm_layout_clean","vlm_superset_branding"]
    base = 0.6 * _avg(core_keys) + 0.3 * _avg(gui_keys) + 0.1 * _avg(aux_keys)

    # ---- hard gates（上拉） ----
    if not has_cli_evidence: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.25)
    if s["bottleneck_analysis"] < 0.5: base = min(base, 0.40)
    if s["bottleneck_analysis"] < 0.25: base = min(base, 0.25)
    if s["speedup_targets"] < 0.5: base = min(base, 0.45)
    if s["speedup_targets"] < 0.25: base = min(base, 0.30)
    if s["optimized_sql"] < 0.5: base = min(base, 0.40)
    if s["perf_csv_schema"] < 1.0: base = min(base, 0.60)
    if s.get("gui_screenshots_ocr", 0) < 0.5: base = min(base, 0.55)
    if s.get("gui_screenshots_md5_unique", 0) < 0.6: base = min(base, 0.50)
    if s.get("gui_screenshots_size_floor", 0) < 0.6: base = min(base, 0.50)
    if s.get("tooltip_samples", 0) < 1.0: base = min(base, 0.65)
    # 无 VLM 退化分上限封顶 0.6（防止无 VLM 也能拿满分）
    if vlm_unavailable: base = min(base, 0.60)

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
