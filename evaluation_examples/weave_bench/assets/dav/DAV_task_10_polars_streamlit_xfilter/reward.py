# Auto-generated from WeaveBench task DAV_task_10_polars_streamlit_xfilter.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-dim grader: plans + profile + speedup + skew JSON + GUI shots + VLM rubric.
    Hard gates: missing CLI evidence -> 0.4, missing GUI shots -> 0.4, VLM<0.6 -> 0.6."""
    import json, re, ast
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    # Read GT from root-only path (warmup moves it off /tmp_workspace/gt
    # to prevent agent from grepping skew_carriers / notes solution map).
    gt_dir = Path("/opt/dav10_gt") if Path("/opt/dav10_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    s = {}

    # ---- 1. plan / profile artefacts ----
    plan_b = rd / "plan_before.txt"
    plan_a = rd / "plan_after.txt"
    prof_b = rd / "profile_before.txt"
    prof_a = rd / "profile_after.txt"
    s["plan_before_exists"]    = 1.0 if plan_b.exists() and plan_b.stat().st_size > 30 else 0.0
    s["plan_after_exists"]     = 1.0 if plan_a.exists() and plan_a.stat().st_size > 30 else 0.0
    # Prompt 第 1 项 + bullet 2: profile_before.txt 必须 ≥ 8 行节点记录
    # (用于事件时序推理). 计算非空行数；少于 8 行视为占位文件，不给分.
    def _profile_lines(p):
        if not p.exists(): return 0
        try:
            return sum(1 for ln in p.read_text(errors="ignore").splitlines() if ln.strip())
        except Exception:
            return 0
    pb_lines = _profile_lines(prof_b)
    s["profile_before_exists"] = 1.0 if (prof_b.exists() and prof_b.stat().st_size > 30 and pb_lines >= 8) else \
                                 (0.5 if (prof_b.exists() and prof_b.stat().st_size > 30) else 0.0)
    s["profile_after_exists"]  = 1.0 if prof_a.exists() and prof_a.stat().st_size > 30 else 0.0

    plan_keywords = ["JOIN", "FILTER", "AGGREGATE", "SCAN", "SELECTION"]
    def has_plan_kw(p):
        if not p.exists(): return 0.0
        try:
            t = p.read_text(errors="ignore").upper()
            return 1.0 if sum(1 for k in plan_keywords if k in t) >= 2 else 0.0
        except Exception:
            return 0.0
    s["plan_before_has_keywords"] = has_plan_kw(plan_b)
    s["plan_after_has_keywords"]  = has_plan_kw(plan_a)

    # ---- 2. predicate pushed down before join in optimized_query.py ----
    opt = rd / "optimized_query.py"
    s["optimized_exists"] = 1.0 if opt.exists() else 0.0
    pushdown_ok = 0.0
    src_text = ""
    if opt.exists():
        try:
            src_text = opt.read_text(errors="ignore")
            ast.parse(src_text)
            s["optimized_parses"] = 1.0
            # bullet #3: file head must contain a `# COUNTER-EXAMPLES`
            # comment block listing ≥ 2 rejected attempts. Look in the
            # first ~80 lines for the marker plus at least 2 bullet items.
            head = "\n".join(src_text.splitlines()[:80])
            if "# COUNTER-EXAMPLES" in head:
                # count bullet-style `# - …` or `# * …` lines after marker
                tail = head.split("# COUNTER-EXAMPLES", 1)[1]
                bullets = sum(
                    1 for ln in tail.splitlines()
                    if re.match(r"\s*#\s*[-*0-9]", ln)
                )
                s["optimized_counter_examples"] = 1.0 if bullets >= 2 else (0.5 if bullets >= 1 else 0.0)
            else:
                s["optimized_counter_examples"] = 0.0
            # Heuristic: filter() call appearing before join() call in source order
            tree = ast.parse(src_text)
            chains = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    chains.append((node.func.attr, node.lineno, node.col_offset))
            f_pos = [(l,c) for (a,l,c) in chains if a == "filter"]
            j_pos = [(l,c) for (a,l,c) in chains if a == "join"]
            joined_before_filter = any((jl,jc) < (fl,fc) for (fl,fc) in f_pos for (jl,jc) in j_pos)
            if f_pos and j_pos and not joined_before_filter and "scan_parquet" in src_text:
                pushdown_ok = 1.0
        except Exception:
            s["optimized_parses"] = 0.0
    else:
        s["optimized_parses"] = 0.0
    s["predicate_pushdown_ordering"] = pushdown_ok

    # ---- 3. skew_partitions.json ----
    sp = rd / "skew_partitions.json"
    sp_rows = []
    if sp.exists():
        try:
            sp_rows = json.loads(sp.read_text())
        except Exception:
            sp_rows = []
    sp_schema_ok = (
        isinstance(sp_rows, list) and len(sp_rows) >= 7
        and all(isinstance(r, dict)
                and {"origin","carrier","p95_delay_min","n_rows","layer_evidence"} <= set(r.keys())
                and isinstance(r.get("n_rows"), int)
                and isinstance(r.get("layer_evidence"), list) and len(r["layer_evidence"]) >= 2
                for r in sp_rows)
    )
    s["skew_partitions_schema"] = 1.0 if sp_schema_ok else 0.0

    expected = {}
    if (gt_dir/"expected.json").exists():
        try: expected = json.loads((gt_dir/"expected.json").read_text())
        except Exception: pass

    skew_carrier_hit = 0.0
    if sp_schema_ok and "skew_carriers" in expected:
        cs = {r.get("carrier") for r in sp_rows}
        gold = set(expected["skew_carriers"])
        if cs & gold:
            skew_carrier_hit = 1.0
    s["skew_partition_value_match"] = skew_carrier_hit

    # ---- 4. findings.json ----
    fnd = rd / "findings.json"
    fnd_data = {}
    if fnd.exists():
        try: fnd_data = json.loads(fnd.read_text())
        except Exception: pass
    needed = ["total_runtime_before_s","total_runtime_after_s","speedup",
              "skew_dimension","skew_values","tail_share_pct",
              "predicate_pushed_down","evidence_screenshots",
              # bullet #12 — surface the four schema fields that were
              # silently unenforced in earlier batch3 builds.
              "bottleneck_count","false_positive_id",
              "cross_source_chain_ids","equivalence_hash"]
    s["findings_schema"] = 1.0 if all(k in fnd_data for k in needed) else \
                           (sum(1 for k in needed if k in fnd_data) / len(needed))

    speedup_ok = 0.0
    try:
        sp_val = float(fnd_data.get("speedup", 0))
        rb = float(fnd_data.get("total_runtime_before_s", 0))
        ra = float(fnd_data.get("total_runtime_after_s", 0))
        if rb >= 5.0 and ra > 0 and (rb/ra) >= 4.5 and sp_val >= 4.5:
            speedup_ok = 1.0
        elif rb >= 3.0 and ra > 0 and (rb/ra) >= 3.0:
            speedup_ok = 0.5
        elif rb > 0 and ra > 0 and (rb/ra) >= 2.0:
            speedup_ok = 0.25
    except Exception:
        pass
    s["speedup_ge_2x"] = speedup_ok

    # predicate text actually appears in optimized_query.py
    pred_text = str(fnd_data.get("predicate_pushed_down","")).strip()
    s["predicate_text_in_source"] = 1.0 if (
        pred_text and len(pred_text) >= 20 and src_text and pred_text in src_text
        and "carrier" in pred_text.lower()
    ) else 0.0

    def _jload(name):
        p = rd/name
        try: return json.loads(p.read_text()) if p.exists() else None
        except Exception: return None
    bn = _jload("bottlenecks.json") or []
    fp = _jload("false_positives.json") or []
    eq = _jload("equivalence.json") or {}
    cs = _jload("cross_source_evidence.json") or {}
    ml = _jload("multilayer_evidence.json") or {}
    et = _jload("event_timeline.json") or []
    types = {b.get("type") for b in bn if isinstance(b, dict)}
    s["bottlenecks_5_distinct_types"] = 1.0 if len(types) >= 5 else 0.0
    s["bottlenecks_causal_chain_ok"]  = 1.0 if bn and all(
        isinstance(b,dict) and len(b.get("causal_chain",[]))>=4
        and len(b.get("abstraction_layers",[]))>=2 for b in bn) else 0.0
    s["equivalence_hash_match"] = 1.0 if eq.get("equal") is True and eq.get("hash_before") and eq.get("hash_before")==eq.get("hash_after") else 0.0
    plan_after_txt = plan_a.read_text(errors="ignore") if plan_a.exists() else ""
    links = cs.get("links",[]) if isinstance(cs,dict) else []
    s["cross_source_links_ok"] = 1.0 if len(links)>=5 and all(
        isinstance(l,dict) and l.get("plan_node_id") and str(l["plan_node_id"]) in plan_after_txt
        for l in links) else 0.0
    s["multilayer_three_layers"] = 1.0 if isinstance(ml,dict) and len(ml)>=3 and all(
        {"logical_plan","physical_exec","storage"} <= set(v.keys()) for v in list(ml.values())[:3]) else 0.0
    s["event_timeline_ordered"] = 0.0
    if isinstance(et,list) and len(et)>=8:
        ts = [e.get("t_start_ms",0) for e in et]
        ids = {e.get("node_id") for e in et}
        order_ok = ts == sorted(ts) and all((e.get("parent") in ids) or e.get("parent") in (None,"null") for e in et)
        f_t = min((e["t_start_ms"] for e in et if "filter" in str(e.get("node_id","")).lower()), default=None)
        j_t = min((e["t_start_ms"] for e in et if "join"   in str(e.get("node_id","")).lower()), default=None)
        if order_ok and f_t is not None and j_t is not None and f_t < j_t:
            s["event_timeline_ordered"] = 1.0
    fp_artifact_metrics = {str(x.get("metric","")).lower() for x in fp if isinstance(x,dict) and x.get("is_artifact")}
    leak = any(m and any(m in " ".join(b.get("causal_chain",[])).lower() for b in bn) for m in fp_artifact_metrics)
    s["false_positive_isolated"] = 1.0 if fp_artifact_metrics and not leak else 0.0

    # ---- 5. GUI screenshots ----
    gui_shots = ["view_streamlit_overview.png","view_brush_tooltip.png",
                 "view_brush_table.png","view_brush_after.png"]
    gui_present = sum(1 for n in gui_shots if (rd/n).exists() and (rd/n).stat().st_size > 4000)
    s["gui_screenshots_count"] = gui_present / len(gui_shots)

    gui_ocr = 0.5
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_streamlit_overview.png": ["Departures","Hour","p95","delay","origin"],
            "view_brush_tooltip.png":      ["n=","carrier","p95","delay"],
            "view_brush_table.png":        ["origin","carrier","p95","n_rows"],
            "view_brush_after.png":        ["carrier","p95","origin"],
        }
        hits = 0
        for n, ks in kws.items():
            p = rd/n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in ks):
                        hits += 1
                except Exception:
                    pass
        gui_ocr = hits / len(kws)
    except ImportError:
        pass
    s["gui_screenshots_ocr"] = gui_ocr

    # ---- 6. VLM rubric (optional) ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd/n) for n in
                ["view_brush_tooltip.png","view_brush_table.png","view_streamlit_overview.png"]
                if (rd/n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
          "vlm_brush_rect_visible": "散点图上必须同时看到一个半透明矩形 brush 选区，且选区内圆点保留原色、选区外的点变为浅灰",
          "vlm_tooltip_with_n":     "矩形 brush 之上叠加一个 hover tooltip 浮层，浮层文字明确包含 'n=' 后跟整数 (≥3 位数)",
          "vlm_filtered_table":     "页面下方 datatable 行数明显少于默认 20，且首列严格按 p95_delay_min 降序排列，包含数据中实际出现的 carrier 代码（agent 通过运行 etl 推断）",
          "vlm_layout_clean":       "整张截图同框完整呈现 4 个 KPI 卡 + Departures by Hour 直方图 + 散点 + datatable，无截断、无滚动条",
        }
        try:
            vlm = vlm_score_rubric(vlm_imgs[:3], rubric, instruction="评估 Polars 长尾分区调试 GUI 取证截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
            s["judge_method"] = vlm.get("judge_method","ok")
        except Exception:
            pass

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums) if nums else 0.0

    has_cli_evidence = (s["plan_before_exists"] + s["profile_before_exists"]
                        + s["plan_after_exists"] + s["profile_after_exists"]) >= 3.0
    if not has_cli_evidence: base = min(base, 0.4)
    # NOTE: We deliberately do NOT cap on missing GUI screenshots —
    # whether the agent invokes GUI tooling is not a scoring axis.
    # Missing PNGs already cost the corresponding sub_scores
    # (gui_screenshots_count / gui_screenshots_ocr / vlm_*); no
    # additional hard cap is applied here.
    # VLM cap uses the rubric mean (consistent with other batch3 tasks)
    # and is only enforced when the helper actually ran.
    if vlm_score_rubric is not None and vlm_imgs:
        vlm_avg = sum(s.get(k, 0.0) for k in
            ["vlm_brush_rect_visible","vlm_tooltip_with_n",
             "vlm_filtered_table","vlm_layout_clean"]) / 4.0
        if vlm_avg < 0.5:
            base = min(base, 0.6)
    if s["speedup_ge_2x"] < 1.0 and s["predicate_pushdown_ordering"] < 1.0:
        base = min(base, 0.55)

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
