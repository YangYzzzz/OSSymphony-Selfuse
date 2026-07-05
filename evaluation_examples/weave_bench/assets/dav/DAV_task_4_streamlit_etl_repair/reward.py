# Auto-generated from WeaveBench task DAV_task_4_streamlit_etl_repair.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DAV_task_4 grader. Empty → 0.000. Hard gates: GUI + CLI + verify pass."""
    import json, csv, re
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    out_dir = workspace / "etl_out"
    s = {}

    # 1. CLI artifacts
    cli_files = ["etl_run.log","anomaly_negative_months.txt","region_total_mismatch.txt"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 2

    aux_files = ["anomaly_month_offset.txt","cache_misconfig_evidence.md","verify.py"]
    aux_present = sum(1 for f in aux_files if (rd / f).exists())
    s["aux_artifacts"] = aux_present / len(aux_files)

    # 2. bug_report.md — 5 段,每段 ≥ 80 字 + file:line;且必须跨 ETL 与 dashboard 两源
    br_score = 0.0
    br_cross = False
    br = rd / "bug_report.md"
    if br.exists():
        try:
            txt = br.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80 and re.search(r"\.py:\d+", p)]
            br_score = min(1.0, len(parags) / 5)
            has_etl = any("etl_pipeline.py:" in p for p in parags)
            has_dash = any("sales_dashboard.py:" in p for p in parags)
            br_cross = has_etl and has_dash
            if not br_cross:
                br_score = min(br_score, 0.5)
        except Exception: pass
    s["bug_report"] = br_score
    s["bug_report_cross_layer"] = 1.0 if br_cross else 0.0

    # 3. backup file
    s["backup_present"] = 1.0 if (rd / "etl_pipeline_backup.py").exists() else 0.0

    # 4. GUI screenshots — 6 standard before/after + 4 GUI-required (hover tooltip / sidebar / multi-window / cache invalidation)
    gui_shots = ["view_streamlit_monthly.png","view_streamlit_categories.png","view_streamlit_region.png",
                 "view_streamlit_monthly_fixed.png","view_streamlit_categories_fixed.png","view_streamlit_region_fixed.png"]
    gui_present = sum(1 for n in gui_shots if (rd / n).exists())
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui = gui_present >= 4

    # 4a. anti-cheat: md5 uniqueness + min filesize for the 6 standard shots
    import hashlib
    md5s, valid_size = set(), 0
    for n in gui_shots:
        p = rd / n
        if p.exists() and p.stat().st_size >= 8000:
            valid_size += 1
            try: md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception: pass
    s["gui_screenshots_unique_md5"] = (len(md5s) / len(gui_shots)) if gui_shots else 0.0
    s["gui_screenshots_min_size"]   = valid_size / len(gui_shots)
    md5_ok = len(md5s) >= max(4, gui_present)  # 同 md5 = 同图复制 cheat

    # 4b. GUI-design-driven shots (each rewards independently; agents pick how to capture)
    extra_shots = {
        "view_dashboard_with_tooltip.png": ["tooltip","-$","negative","revenue","month","-"],
        "view_sidebar_secondhalf.png":     ["second half","aggregation","2024-07","2024-08","2024-09"],
        "view_dashboard_and_editor.png":   ["etl_pipeline","def ","gedit","code","streamlit","sales_dashboard"],
        "view_cache_invalidated.png":      ["streamlit","monthly","revenue"],
    }
    try:
        import pytesseract
        from PIL import Image
        for fname, kws in extra_shots.items():
            p = rd / fname
            sub_key = "extra_" + fname.replace("view_", "").replace(".png","")
            if not p.exists() or p.stat().st_size < 8000:
                s[sub_key] = 0.0
                continue
            try:
                tx = pytesseract.image_to_string(Image.open(p)).lower()
                hit = sum(1 for k in kws if k.lower() in tx)
                s[sub_key] = min(1.0, hit / max(2.0, len(kws) * 0.4))
            except Exception:
                s[sub_key] = 0.3  # file present but OCR failed — capped
    except Exception:
        for fname in extra_shots:
            sub_key = "extra_" + fname.replace("view_", "").replace(".png","")
            p = rd / fname
            s[sub_key] = 0.3 if (p.exists() and p.stat().st_size > 8000) else 0.0

    try:
        import pytesseract
        from PIL import Image
        kws_any = ["streamlit","monthly","revenue","category","region","Total","sum","share"]
        ocr_hits = 0
        for n in gui_shots:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in kws_any): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
        vlm_available = True
    except Exception:
        s["gui_screenshots_ocr"] = 0.3 if gui_present > 0 else 0.0
        vlm_available = False

    # 5. monthly_revenue all >= 0 after fix
    mr_score = 0.0
    mr = out_dir / "monthly_revenue.csv"
    if mr.exists():
        try:
            rows = list(csv.DictReader(mr.open()))
            rev_col = None
            for c in ("revenue","monthly_revenue","total_revenue"):
                if rows and c in rows[0]: rev_col = c; break
            if rev_col:
                neg = sum(1 for r in rows if float(r[rev_col]) < 0)
                mr_score = 1.0 if neg == 0 else 0.0
        except Exception: pass
    s["no_negative_months"] = mr_score

    # 6. category_share has 6 categories
    cs_score = 0.0
    cs = out_dir / "category_share.csv"
    if cs.exists():
        try:
            rows = list(csv.DictReader(cs.open()))
            if len(rows) == 6: cs_score = 1.0
            elif 4 <= len(rows) < 6: cs_score = 0.5
        except Exception: pass
    s["six_categories"] = cs_score

    # 7. region_summary SUM == Total
    rt_score = 0.0
    rt = out_dir / "region_summary.csv"
    if rt.exists():
        try:
            rows = list(csv.DictReader(rt.open()))
            val_col = None
            for c in ("revenue","total","value","sum","amount","total_amount","sales","total_sales","revenue_total"):
                if rows and c in rows[0]: val_col = c; break
            if val_col:
                regions = [r for r in rows if str(r.get("region","")).lower() != "total"]
                total_rows = [r for r in rows if str(r.get("region","")).lower() == "total"]
                if regions and total_rows:
                    s_sum = sum(float(r[val_col]) for r in regions)
                    t_val = float(total_rows[0][val_col])
                    if abs(s_sum - t_val) / max(abs(t_val), 1) < 0.01:
                        rt_score = 1.0
        except Exception: pass
    s["region_total_match"] = rt_score

    # 8. verify_output.txt
    vo_score = 0.0
    vo = rd / "verify_output.txt"
    if vo.exists():
        try:
            txt = vo.read_text()
            if "ALL PASS" in txt or "all pass" in txt.lower(): vo_score = 1.0
            elif "PASS" in txt: vo_score = 0.5
        except Exception: pass
    s["verify_pass"] = vo_score

    # 9. etl_insight.md
    ei_score = 0.0
    ei = rd / "etl_insight.md"
    if ei.exists():
        try:
            txt = ei.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            ei_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["insight_report"] = ei_score

    # 10. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_keys = ["vlm_streamlit_layout","vlm_no_negative_visible","vlm_six_categories_visible","vlm_total_consistent"]
    vlm_used = False
    if vlm_score_rubric and (rd / "view_streamlit_monthly_fixed.png").exists():
        rubric = {
            "vlm_streamlit_layout": "Streamlit dashboard 截图布局清晰,含表格 / chart 元素",
            "vlm_no_negative_visible": "fixed 截图里看不到负数 revenue 条",
            "vlm_six_categories_visible": "category 饼图截图看到 6 个分片(或 6 行)",
            "vlm_total_consistent": "region table 里 Total 行数值看起来等于 SUM",
        }
        try:
            imgs = [str(rd / n) for n in ["view_streamlit_monthly_fixed.png","view_streamlit_categories_fixed.png","view_streamlit_region_fixed.png"] if (rd / n).exists()]
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 streamlit fixed dashboard 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
            vlm_used = any(s[k] > 0 for k in vlm_keys)
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in vlm_keys: s[k] = 0.0

    # ---------- weighted overall ----------
    def _avg(keys):
        vals = [s.get(k, 0.0) for k in keys if isinstance(s.get(k, 0.0), (int, float))]
        return sum(vals) / len(vals) if vals else 0.0

    core_keys = ["no_negative_months","six_categories","region_total_match","verify_pass","bug_report","bug_report_cross_layer"]
    gui_keys  = ["gui_screenshots_count","gui_screenshots_ocr","gui_screenshots_unique_md5","gui_screenshots_min_size",
                 "extra_dashboard_with_tooltip","extra_sidebar_secondhalf","extra_dashboard_and_editor","extra_cache_invalidated"] + vlm_keys
    aux_keys  = ["cli_artifacts","backup_present","insight_report","aux_artifacts"]

    core = _avg(core_keys)
    gui  = _avg(gui_keys)
    aux  = _avg(aux_keys)
    base = 0.60 * core + 0.30 * gui + 0.10 * aux

    # hard gates (tighter)
    if not has_cli: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.25)
    if not md5_ok:  base = min(base, 0.40)             # 同 md5 复制 cheat
    if s["bug_report"] < 0.6: base = min(base, 0.40)
    if s["bug_report_cross_layer"] < 1.0: base = min(base, 0.55)
    if s["verify_pass"] < 1.0: base = min(base, 0.50)
    if (s["no_negative_months"] < 1.0 or s["six_categories"] < 1.0 or s["region_total_match"] < 1.0):
        base = min(base, 0.55)
    extra_avg = _avg(["extra_dashboard_with_tooltip","extra_sidebar_secondhalf","extra_dashboard_and_editor","extra_cache_invalidated"])
    if extra_avg < 0.5: base = min(base, 0.55)
    if not vlm_used: base = min(base, 0.60)            # 无 VLM 退化封顶

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
