# Auto-generated from WeaveBench task DAV_task_5_clickhouse_slow_query_grafana.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import csv, json, re, statistics
from pathlib import Path

# --- Private oracle (NOT exposed to agent; do not move to gt/expected.json) ---
# These signatures correspond to the intentionally slow queries baked into
# /tmp_workspace/queries.sql and the canonical root-cause vocabulary the
# diagnostic report should reference. Used here for anti-cheat / tightened
# grading only. Keep in sync with exec/queries.sql when the workload changes.
_PRIVATE_TOP_QUERY_SIGNATURES = [
    "select * from ads.ad_events where country = 'us' and event_type = 'click' order by event_time desc",
    "where todate(event_time) between",
    "where campaign_id = 17 or campaign_id = 23 or campaign_id = 41",
]
_PRIVATE_ROOT_CAUSE_KEYWORDS = [
    "prewhere", "function on indexed column", "or to in", "select *",
    "primary key", "todate",
]


def _norm_sql(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "").strip().lower())


def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-dim grader for ClickHouse slow-query + Grafana task."""
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    gt_dir = workspace / "gt"
    s = {}

    gt = {}
    if (gt_dir / "expected.json").exists():
        try:
            gt = json.loads((gt_dir / "expected.json").read_text())
        except Exception:
            gt = {}

    # 1. load_run.log
    lr = rd / "load_run.log"
    s["load_run_log"] = 1.0 if lr.exists() and lr.stat().st_size > 50 else 0.0

    # 2. slow_top10.tsv
    st = rd / "slow_top10.tsv"
    if st.exists():
        try:
            txt = st.read_text(errors="ignore")
            lines = [l for l in txt.splitlines() if l.strip()]
            header_ok = any(
                "query_duration_ms" in l and "read_rows" in l and "query" in l
                for l in lines[:3]
            )
            row_count = max(0, len(lines) - 1)
            s["slow_top10_present"] = 1.0 if lines else 0.0
            s["slow_top10_schema"] = 1.0 if header_ok else 0.0
            s["slow_top10_rows"] = min(1.0, row_count / 5.0)
        except Exception:
            s["slow_top10_present"] = 0.0
            s["slow_top10_schema"] = 0.0
            s["slow_top10_rows"] = 0.0
    else:
        s["slow_top10_present"] = 0.0
        s["slow_top10_schema"] = 0.0
        s["slow_top10_rows"] = 0.0

    # 3. EXPLAIN files
    explain_files = ["explain_top1.txt", "explain_top2.txt",
                     "pipeline_top1.txt", "pipeline_top2.txt"]
    explain_hits = 0
    for f in explain_files:
        p = rd / f
        if p.exists() and len(p.read_text(errors="ignore").splitlines()) >= 5:
            explain_hits += 1
    s["explain_files"] = explain_hits / len(explain_files)

    # 4. slow_top SQL files
    slow_sqls = {}
    for tag in ["slow_top1.sql", "slow_top2.sql"]:
        p = rd / tag
        if p.exists():
            t = p.read_text(errors="ignore").strip().lower()
            slow_sqls[tag] = t
            ok = t.startswith("select") or "select" in t.split("\n", 1)[0]
            s[tag.replace(".sql", "_valid")] = 1.0 if ok else 0.0
        else:
            s[tag.replace(".sql", "_valid")] = 0.0

    # 4b. Anti-cheat: at least one of slow_top1/2 must match a known slow-query
    # signature from the private oracle (proves agent actually inspected
    # query_log, not just dumped any random SELECT).
    sig_hits = 0
    norm_top_sqls = [_norm_sql(slow_sqls.get(k, "")) for k in ("slow_top1.sql", "slow_top2.sql")]
    for sig in _PRIVATE_TOP_QUERY_SIGNATURES:
        sig_n = _norm_sql(sig)
        if any(sig_n in nt for nt in norm_top_sqls if nt):
            sig_hits += 1
    s["slow_top_signature_match"] = min(1.0, sig_hits / 2.0)

    # 5-7,12. GUI screenshots (anti-cheat: size >= 5KB, md5 diversity, OCR keyword hit)
    import hashlib
    gui_shots = {
        "view_datasource.png": ["clickhouse", "working", "connected", "data source"],
        "view_dashboard_before.png": ["adevents", "events", "dashboard"],
        "view_p95_panel.png": ["p95", "latency", "query_log"],
        "view_p95_after.png": ["p95", "latency", "query_log"],
        "view_explore_validate.png": ["explore", "select", "run query"],
    }
    gui_present = 0
    gui_ocr_hits = 0
    gui_md5s = set()
    gui_resolution_ok = 0
    vlm_unavailable = False
    for fname, kws in gui_shots.items():
        p = rd / fname
        if p.exists() and p.stat().st_size >= 5000:
            gui_present += 1
            try:
                gui_md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception:
                pass
            try:
                from PIL import Image
                im = Image.open(p)
                w, h = im.size
                if w >= 1024 and h >= 600:
                    gui_resolution_ok += 1
            except Exception:
                pass
            try:
                import pytesseract
                from PIL import Image
                tx = pytesseract.image_to_string(Image.open(p)).lower()
                if any(k in tx for k in kws):
                    gui_ocr_hits += 1
            except Exception:
                vlm_unavailable = True
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    s["gui_screenshots_ocr"] = gui_ocr_hits / len(gui_shots)
    s["gui_screenshots_md5_diversity"] = (len(gui_md5s) / gui_present) if gui_present else 0.0
    s["gui_screenshots_resolution"] = gui_resolution_ok / len(gui_shots)

    # 8. tooltip_samples.json (anti-cheat: ISO timestamps, distinct values)
    ts = rd / "tooltip_samples.json"
    if ts.exists():
        try:
            d = json.loads(ts.read_text())
            items = d.get("p95_samples", [])
            valid = (
                isinstance(items, list)
                and len(items) >= 3
                and all(
                    isinstance(i, dict)
                    and "timestamp" in i
                    and isinstance(i.get("p95_ms"), (int, float))
                    for i in items
                )
            )
            s["tooltip_structure"] = 1.0 if valid else 0.0
            if valid:
                ts_re = re.compile(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}")
                iso_ok = sum(1 for i in items if ts_re.match(str(i.get("timestamp", ""))))
                vals = [float(i["p95_ms"]) for i in items]
                distinct_vals = len(set(round(v, 3) for v in vals))
                positive = all(v > 0 for v in vals)
                quality = 0.0
                if iso_ok >= 3:
                    quality += 0.4
                if distinct_vals >= 2 and positive:
                    quality += 0.3
                if distinct_vals >= 3:
                    quality += 0.3
                s["tooltip_quality"] = round(quality, 3)
            else:
                s["tooltip_quality"] = 0.0
        except Exception:
            s["tooltip_structure"] = 0.0
            s["tooltip_quality"] = 0.0
    else:
        s["tooltip_structure"] = 0.0
        s["tooltip_quality"] = 0.0

    # 9. optimized SQL files: must differ from slow + must have changed: comment
    for orig, opt in [("slow_top1.sql", "optimized_top1.sql"),
                      ("slow_top2.sql", "optimized_top2.sql")]:
        po = rd / opt
        key = opt.replace(".sql", "")
        if po.exists():
            t = po.read_text(errors="ignore").lower()
            differs = slow_sqls.get(orig, "") and t.strip() != slow_sqls.get(orig, "").strip()
            has_comment = "-- changed" in t or "--changed" in t
            score = 0.0
            if t.strip().startswith("select") or "select" in t.split("\n", 1)[0]:
                score += 0.4
            if differs:
                score += 0.3
            if has_comment:
                score += 0.3
            s[key] = round(score, 3)
        else:
            s[key] = 0.0

    # 10. perf_compare.csv
    pc = rd / "perf_compare.csv"
    perf_rows = []
    if pc.exists():
        try:
            perf_rows = list(csv.DictReader(pc.open()))
            need_cols = {"query_id", "version", "run_idx", "duration_ms", "read_rows"}
            schema_ok = perf_rows and need_cols.issubset(set(perf_rows[0].keys()))
            s["perf_compare_schema"] = 1.0 if schema_ok else 0.0
            buckets = {}
            for r in perf_rows:
                k = (r.get("query_id"), r.get("version"))
                buckets.setdefault(k, 0)
                buckets[k] += 1
            need = [("q_top1", "before"), ("q_top1", "after"),
                    ("q_top2", "before"), ("q_top2", "after")]
            full = sum(1 for k in need if buckets.get(k, 0) >= 3)
            s["perf_compare_coverage"] = full / len(need)
        except Exception:
            s["perf_compare_schema"] = 0.0
            s["perf_compare_coverage"] = 0.0
    else:
        s["perf_compare_schema"] = 0.0
        s["perf_compare_coverage"] = 0.0

    # 11. speedup.json
    sp = rd / "speedup.json"
    if sp.exists():
        try:
            d = json.loads(sp.read_text())
            speedups = []
            for q in ["q_top1", "q_top2"]:
                v = d.get(q, {}).get("speedup")
                try:
                    fv = float(v)
                    speedups.append(fv)
                except Exception:
                    pass
            s["speedup_present"] = 1.0 if len(speedups) == 2 else 0.0
            s["speedup_achieved"] = 1.0 if (len(speedups) == 2 and all(x >= 2.0 for x in speedups)) else (0.5 if speedups else 0.0)
        except Exception:
            s["speedup_present"] = 0.0
            s["speedup_achieved"] = 0.0
    else:
        s["speedup_present"] = 0.0
        s["speedup_achieved"] = 0.0

    # 13. report.md
    rp = rd / "report.md"
    if rp.exists():
        c = rp.read_text(errors="ignore")
        c_low = c.lower()
        has_table = c.count("|") >= 6
        suggestion_lines = [l for l in c.splitlines() if len(l.strip()) >= 30]
        has_root_cause = bool(re.search(r"prewhere|index|primary|order by|function|or →|or->|or to in", c, re.I))
        # Tightened: require ≥2 distinct root-cause keywords from private oracle.
        rc_hits = sum(1 for kw in _PRIVATE_ROOT_CAUSE_KEYWORDS if kw.lower() in c_low)
        s["report_table"] = 1.0 if has_table else 0.0
        s["report_root_cause"] = 1.0 if has_root_cause else 0.0
        s["report_root_cause_depth"] = min(1.0, rc_hits / 2.0)
        s["report_suggestions"] = min(1.0, len(suggestion_lines) / 5.0)
    else:
        s["report_table"] = 0.0
        s["report_root_cause"] = 0.0
        s["report_root_cause_depth"] = 0.0
        s["report_suggestions"] = 0.0

    # VLM rubric
    vlm_ran = False
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    rubric_keys = ["vlm_p95_curve", "vlm_panel_title", "vlm_layout_clean", "vlm_dashboard_real"]
    if vlm_score_rubric:
        imgs = [str(rd / n) for n in gui_shots if (rd / n).exists()]
        if imgs:
            rubric = {
                "vlm_p95_curve": "截图里能看到 p95 时序折线图",
                "vlm_panel_title": "panel 标题清晰可读，包含 latency / p95 字样",
                "vlm_layout_clean": "Grafana 截图布局整齐没有截断或重叠",
                "vlm_dashboard_real": "看起来是真的 Grafana UI 而不是空白页 / 报错页",
            }
            try:
                vlm = vlm_score_rubric(
                    imgs[:4], rubric,
                    instruction="评估 ClickHouse + Grafana 慢查询监控 panel 截图质量。"
                )
                for k in rubric:
                    s[k] = float(vlm.get(k, 0.0))
                vlm_ran = True
            except Exception:
                for k in rubric:
                    s[k] = 0.0

    # Weighted overall: core 55% / gui 25% / aux 10% / vlm 10%
    def _avg(keys):
        vals = [s.get(k, 0.0) for k in keys if k in s]
        return sum(vals) / len(vals) if vals else 0.0

    core_keys = [
        "load_run_log", "slow_top10_present", "slow_top10_schema", "slow_top10_rows",
        "explain_files", "slow_top1_valid", "slow_top2_valid",
        "slow_top_signature_match",
        "optimized_top1", "optimized_top2",
        "perf_compare_schema", "perf_compare_coverage",
        "speedup_present", "speedup_achieved",
    ]
    gui_keys = [
        "gui_screenshots_count", "gui_screenshots_ocr",
        "gui_screenshots_md5_diversity", "gui_screenshots_resolution",
        "tooltip_structure", "tooltip_quality",
    ]
    aux_keys = ["report_table", "report_root_cause", "report_root_cause_depth", "report_suggestions"]

    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys)
    if vlm_ran:
        vlm = _avg(rubric_keys)
        base = 0.55 * core + 0.25 * gui + 0.10 * aux + 0.10 * vlm
    else:
        # No VLM available → re-distribute weight, but cap below
        base = 0.60 * core + 0.28 * gui + 0.12 * aux

    # Hard gates (multi-tier, tightened)
    if s.get("gui_screenshots_count", 0) < 0.6:
        base = min(base, 0.35)
    if s.get("gui_screenshots_ocr", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("gui_screenshots_md5_diversity", 0) < 0.8:
        base = min(base, 0.5)
    if s.get("slow_top10_present", 0) == 0:
        base = min(base, 0.3)
    if s.get("explain_files", 0) < 0.75:
        base = min(base, 0.5)
    if s.get("perf_compare_coverage", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("speedup_achieved", 0) < 1.0:
        base = min(base, 0.5)
    if s.get("tooltip_structure", 0) == 0:
        base = min(base, 0.55)
    if s.get("tooltip_quality", 0) < 0.6:
        base = min(base, 0.65)
    # Tightened gates from private oracle (anti-leak):
    if s.get("slow_top_signature_match", 0) < 0.5:
        base = min(base, 0.5)
    if s.get("report_root_cause_depth", 0) < 0.5:
        base = min(base, 0.6)
    if not vlm_ran:
        base = min(base, 0.6)

    s["overall_score"] = round(base, 3)
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
