# Auto-generated from WeaveBench task OPS_task_2_postgres_explain_pgadmin.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Postgres EXPLAIN + pgAdmin Graphical Plan + Dashboard 微循环 grader."""
    import json, re, csv, io
    from pathlib import Path
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    try:
        import pytesseract
        from PIL import Image
    except Exception:
        pytesseract = None
        Image = None

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    def ocr_hits(path, kws, min_hits=1):
        if not (pytesseract and Image and path.exists()):
            return 0
        try:
            tx = pytesseract.image_to_string(Image.open(path)).lower()
        except Exception:
            return 0
        return sum(1 for k in kws if k.lower() in tx)

    def shot_real(path, min_size=20000, min_w=1024, min_h=600):
        # 防 cheat：截图必须 ≥ min_size 字节、分辨率达标
        try:
            if not path.exists() or path.stat().st_size < min_size:
                return False
            if Image:
                with Image.open(path) as im:
                    if im.size[0] < min_w or im.size[1] < min_h:
                        return False
            return True
        except Exception:
            return False

    def md5_of(path):
        import hashlib
        try:
            return hashlib.md5(path.read_bytes()).hexdigest()
        except Exception:
            return None

    # 1. compose / ready / schema load
    arts = ["compose_up.log", "ready_ts.txt", "schema_load.log"]
    s["compose_artifacts"] = sum(1 for n in arts if (rd/n).exists()) / len(arts)

    # 2. baseline_plans/q1..q5.json
    bp_dir = rd / "baseline_plans"
    valid_bp = 0
    for i in range(1, 6):
        p = bp_dir / f"q{i}.json"
        if p.exists():
            try:
                d = json.loads(p.read_text())
                if isinstance(d, list) and d:
                    valid_bp += 1
            except Exception:
                pass
    s["baseline_plans"] = valid_bp / 5.0

    # 3. baseline_times.csv
    bt = rd / "baseline_times.csv"
    if bt.exists():
        try:
            r = csv.DictReader(io.StringIO(bt.read_text()))
            rows = list(r)
            cols_ok = bool(r.fieldnames) and all(c in r.fieldnames for c in
                ["query_id","execution_time_ms","planning_time_ms"])
            s["baseline_times"] = 1.0 if (cols_ok and len(rows) >= 5) else (0.5 if rows else 0.0)
        except Exception:
            s["baseline_times"] = 0.0
    else:
        s["baseline_times"] = 0.0

    # 4. pgAdmin Graphical Plan + Object Explorer screenshots (5)
    plan_shots = [
        "view_01_pgadmin_indexes_before.png",
        "view_02_pgadmin_plan_tree_q1.png",
        "view_03_pgadmin_node_detail.png",
        "view_04_pgadmin_q1_statistics.png",
        "view_05_pgadmin_plan_tree_q3.png",
    ]
    plan_real = sum(1 for n in plan_shots if shot_real(rd/n))
    s["plan_shots_present"] = plan_real / len(plan_shots)
    plan_kw = ["pgadmin","query tool","explain","graphical","seq scan","hash join",
               "sort","aggregate","object explorer","statistics","planning time",
               "execution time","actual rows","properties","indexes"]
    if pytesseract and Image:
        # 每张需命中 ≥ 2 个关键词才算 OCR 通过
        s["plan_shots_ocr"] = sum(1 for n in plan_shots if ocr_hits(rd/n, plan_kw) >= 2) / len(plan_shots)
    else:
        s["plan_shots_ocr"] = 0.4 if plan_real else 0.0
    # 截图 md5 多样性（不能 5 张全同一截图）
    plan_md5s = {md5_of(rd/n) for n in plan_shots if (rd/n).exists()}
    plan_md5s.discard(None)
    s["plan_shots_diversity"] = len(plan_md5s) / max(1, plan_real) if plan_real else 0.0

    # 5. Dashboard screenshots (2) - GUI-only signal
    dash_shots = ["view_06_pgadmin_dashboard_activity.png",
                  "view_07_pgadmin_dashboard_locks.png"]
    dash_real = sum(1 for n in dash_shots if shot_real(rd/n))
    s["dashboard_shots_present"] = dash_real / len(dash_shots)
    dash_kw = ["dashboard","sessions","transactions","tuples","block i/o",
               "server activity","locks","wait_event","application_name","state"]
    if pytesseract and Image:
        s["dashboard_shots_ocr"] = sum(1 for n in dash_shots if ocr_hits(rd/n, dash_kw) >= 2) / len(dash_shots)
    else:
        s["dashboard_shots_ocr"] = 0.4 if dash_real else 0.0

    # 6. table_stats / index_stats
    ts = rd / "table_stats.txt"
    s["table_stats"] = 1.0 if (ts.exists() and "seq_scan" in ts.read_text(errors="ignore")) else (0.3 if ts.exists() else 0.0)
    isf = rd / "index_stats.txt"
    s["index_stats"] = 1.0 if (isf.exists() and "idx_scan" in isf.read_text(errors="ignore")) else (0.3 if isf.exists() else 0.0)

    # 7. optimization_plan.json schema
    op = rd / "optimization_plan.json"
    op_score = 0.0
    if op.exists():
        try:
            d = json.loads(op.read_text())
            qs = d.get("queries", [])
            req = {"query_id","bottleneck_node_type","bottleneck_table",
                   "actual_rows_observed","evidence_screenshot",
                   "evidence_explain_json","proposed_index_ddl","expected_node_after"}
            valid = [q for q in qs if isinstance(q, dict) and req <= set(q.keys())]
            op_score = 1.0 if len(valid) >= 5 else len(valid)/5.0
        except Exception:
            pass
    s["optimization_plan"] = op_score

    # 8. create_indexes.sql
    ci = rd / "create_indexes.sql"
    if ci.exists():
        n = len(re.findall(r"CREATE\s+INDEX", ci.read_text(errors="ignore"), re.I))
        s["create_indexes"] = 1.0 if n >= 3 else (0.5 if n >= 1 else 0.0)
    else:
        s["create_indexes"] = 0.0

    # 9. optimized_plans contain Index Scan
    op_dir = rd / "optimized_plans"
    idx_scan_n = 0
    for i in range(1, 6):
        p = op_dir / f"q{i}.json"
        if p.exists():
            try:
                t = p.read_text()
                if any(k in t for k in ["Index Scan", "Index Only Scan", "Bitmap Heap Scan", "Bitmap Index Scan"]):
                    idx_scan_n += 1
            except Exception:
                pass
    s["optimized_index_scan"] = idx_scan_n / 5.0

    # 10. single-query verification screenshots (2)
    after_shots = ["view_08_pgadmin_plan_tree_qN_after.png",
                   "view_09_pgadmin_indexes_after.png"]
    after_real = sum(1 for n in after_shots if shot_real(rd/n))
    s["after_shots_present"] = after_real / len(after_shots)
    if pytesseract and Image:
        s["after_shots_ocr"] = sum(1 for n in after_shots if ocr_hits(rd/n,
            ["index scan","bitmap","indexes","properties"]) >= 1) / len(after_shots)
    else:
        s["after_shots_ocr"] = 0.4 if after_real else 0.0

    # 11. speedup
    ot = rd / "optimized_times.csv"
    speedup_score = 0.0
    if ot.exists() and bt.exists():
        try:
            br = list(csv.DictReader(io.StringIO(bt.read_text())))
            orw = list(csv.DictReader(io.StringIO(ot.read_text())))
            if br and orw:
                b_avg = sum(float(r["execution_time_ms"]) for r in br) / len(br)
                o_avg = sum(float(r["execution_time_ms"]) for r in orw) / len(orw)
                speedup = (b_avg - o_avg) / max(1.0, b_avg)
                speedup_score = 1.0 if speedup >= 0.5 else (0.4 if speedup >= 0.3 else (0.15 if speedup >= 0.1 else 0.0))
        except Exception:
            pass
    s["speedup"] = speedup_score

    # 12. dashboard after (须为真截图)
    p10 = rd / "view_10_pgadmin_dashboard_after.png"
    s["dashboard_after_shot"] = 1.0 if shot_real(p10) else 0.0
    # Dashboard 前后对比：md5 必须不同（若同一截图 → 没真去做复验）
    p06 = rd / "view_06_pgadmin_dashboard_activity.png"
    if shot_real(p10) and shot_real(p06) and md5_of(p10) and md5_of(p06):
        s["dashboard_before_after_diff"] = 1.0 if md5_of(p10) != md5_of(p06) else 0.0
    else:
        s["dashboard_before_after_diff"] = 0.0

    # 13. comparison_report.md
    cr = rd / "comparison_report.md"
    if cr.exists():
        t = cr.read_text(errors="ignore")
        has_table = "|" in t and t.count("|") >= 8
        ref_n = len(re.findall(r"view_\d+", t))
        kw_hit = ("before" in t.lower() and "after" in t.lower()) or ("提速" in t)
        s["comparison_report"] = 1.0 if (len(t) >= 350 and has_table and ref_n >= 3 and kw_hit) else (0.5 if len(t) >= 200 else 0.2)
    else:
        s["comparison_report"] = 0.0

    # cross-channel co-presence
    has_cli_ev = (s["baseline_plans"] > 0) and (s["table_stats"] > 0)
    has_gui_ev = (s["plan_shots_present"] >= 0.4) and (s["dashboard_shots_present"] >= 0.5)
    s["cross_channel_evidence"] = 1.0 if (has_cli_ev and has_gui_ev) else 0.0

    # VLM rubric (4)
    if vlm_score_rubric:
        all_shots = plan_shots + dash_shots + after_shots + ["view_10_pgadmin_dashboard_after.png"]
        sample = [str(rd/n) for n in all_shots if (rd/n).exists()][:4]
        if sample:
            rubric = {
                "vlm_graphical_plan_real": "至少一张截图清晰显示 pgAdmin Graphical EXPLAIN plan tree（节点 + 颜色编码 + 节点连线）",
                "vlm_dashboard_curves": "view_06 / view_10 中能看到 Server activity 真实折线图（多条曲线 + 时间轴），不是空白页",
                "vlm_index_scan_after": "view_08 中能看到 Index Scan / Bitmap 节点替代了原 Seq Scan",
                "vlm_object_explorer_indexes": "view_01 / view_09 至少一张能看到 Object Explorer 中 orders 表的 Indexes 子节点 + 右侧 Properties 显示索引 Definition",
            }
            vlm = vlm_score_rubric(sample, rubric,
                instruction="评估 pgAdmin 4 慢查询诊断 + 索引优化 GUI 截图。")
            for k in rubric:
                s[k] = vlm.get(k, 0.0)
            s["judge_method"] = vlm.get("judge_method", "failed")

    # ---- 加权聚合：核心交付 60% / GUI 证据 30% / 辅助 10% ----
    core_keys = ["baseline_plans","baseline_times","optimization_plan",
                 "create_indexes","optimized_index_scan","speedup",
                 "comparison_report"]
    gui_keys = ["plan_shots_present","plan_shots_ocr","plan_shots_diversity",
                "dashboard_shots_present","dashboard_shots_ocr",
                "after_shots_present","after_shots_ocr",
                "dashboard_after_shot","dashboard_before_after_diff"]
    aux_keys = ["compose_artifacts","table_stats","index_stats",
                "cross_channel_evidence"]
    def _avg(keys):
        vs = [float(s[k]) for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vs)/len(vs) if vs else 0.0
    core = _avg(core_keys)
    gui  = _avg(gui_keys)
    aux  = _avg(aux_keys)
    base = 0.6*core + 0.3*gui + 0.1*aux

    # VLM 子分单独纳入（如有），与上面 base 平均
    vlm_keys = [k for k in s if k.startswith("vlm_")]
    vlm_avg = None
    if vlm_keys:
        vlm_avg = sum(float(s[k]) for k in vlm_keys) / len(vlm_keys)
        base = 0.7*base + 0.3*vlm_avg
    else:
        # 无 VLM 时上限 0.6（不能让无 VLM 也满分）
        base = min(base, 0.6)

    # ---- Hard gates（多层）----
    # 核心：CLI / GUI 证据缺一即重创
    if not has_cli_ev:
        base = min(base, 0.35)
    if not has_gui_ev:
        base = min(base, 0.35)
    # optimization_plan 不达 5 条 → cap 0.45
    if s.get("optimization_plan", 0) < 1.0:
        base = min(base, 0.5 if s.get("optimization_plan", 0) >= 0.6 else 0.45)
    # 索引复验：5/5 才能拿满；< 0.6 直接重罚
    if s.get("optimized_index_scan", 0) < 0.6:
        base = min(base, 0.45)
    if s.get("optimized_index_scan", 0) < 0.4:
        base = min(base, 0.35)
    # 提速 < 50% → cap 0.55；< 30% → cap 0.45
    if s.get("speedup", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("speedup", 0) < 0.4:
        base = min(base, 0.45)
    # CREATE INDEX < 3 条 → cap 0.5
    if s.get("create_indexes", 0) < 1.0:
        base = min(base, 0.5)
    # GUI 截图严苛 gate：5+2+2+1=10 张关键截图，真截图比例 < 70% → cap 0.45
    real_present_avg = (s.get("plan_shots_present",0)*5
                        + s.get("dashboard_shots_present",0)*2
                        + s.get("after_shots_present",0)*2
                        + s.get("dashboard_after_shot",0)) / 10.0
    if real_present_avg < 0.7:
        base = min(base, 0.45)
    # 截图 OCR：plan + dashboard 任一全失败 → cap 0.5
    if s.get("plan_shots_ocr", 0) < 0.4 or s.get("dashboard_shots_ocr", 0) < 0.4:
        base = min(base, 0.5)
    # 截图多样性：5 张 plan 至少 4 个不同 md5
    if s.get("plan_shots_diversity", 0) < 0.8:
        base = min(base, 0.5)
    # Dashboard 前后必须不同
    if s.get("dashboard_after_shot", 0) > 0 and s.get("dashboard_before_after_diff", 0) == 0:
        base = min(base, 0.5)
    # comparison_report 不达标 → cap 0.55
    if s.get("comparison_report", 0) < 1.0:
        base = min(base, 0.6 if s.get("comparison_report", 0) >= 0.5 else 0.5)
    # VLM 多层 cap
    if vlm_avg is not None:
        if vlm_avg < 0.7:
            base = min(base, 0.65)
        if vlm_avg < 0.5:
            base = min(base, 0.5)
        if vlm_avg < 0.3:
            base = min(base, 0.35)

    s["core_subscore"] = float(core)
    s["gui_subscore"] = float(gui)
    s["aux_subscore"] = float(aux)
    s["overall_score"] = float(max(0.0, min(1.0, base)))
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
