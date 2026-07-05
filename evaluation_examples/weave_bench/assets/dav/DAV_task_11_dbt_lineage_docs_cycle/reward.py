# Auto-generated from WeaveBench task DAV_task_11_dbt_lineage_docs_cycle.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """dbt cycle/type-mismatch grader. Sub-scores cover: CLI artefacts, fixed model has cast,
    duckdb schema actually changed, GUI screenshots present + OCR hits, VLM rubric."""
    import json, re, subprocess
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    # Read GT from the root-only path the warmup moved expected.json to
    # (kept off the agent-visible /tmp_workspace/gt to prevent answer
    # leakage). Fall back to /tmp_workspace/gt for legacy compatibility.
    gt_dir = Path("/opt/dav11_gt") if Path("/opt/dav11_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    proj = Path("/tmp_workspace/jaffle_shop")
    s = {}

    # ---- 1. run / test / build logs ----
    rb = rd / "run_before.log"
    tb = rd / "test_before.log"
    ba = rd / "build_after.log"
    s["run_before_log"] = 1.0 if rb.exists() and rb.stat().st_size > 50 else 0.0
    s["test_before_log_fail"] = 0.0
    if tb.exists():
        try:
            t = tb.read_text(errors="ignore")
            if re.search(r"\b(FAIL|ERROR|Failure)\b", t):
                s["test_before_log_fail"] = 1.0
        except Exception: pass
    s["build_after_log_pass"] = 0.0
    if ba.exists():
        try:
            t = ba.read_text(errors="ignore")
            # Require dbt's actual completion + per-test PASS marker, not
            # any literal "PASS" in the log. dbt prints lines like
            #   "Completed successfully" / "Done. PASS=N WARN=0 ERROR=0 SKIP=0 TOTAL=N"
            # and per-test "PASS=" rows. We require both an explicit
            # completion marker AND at least one structured PASS counter
            # AND no FAIL/ERROR token.
            has_done = bool(re.search(r"Completed successfully|Done\.", t))
            has_pass_counter = bool(re.search(r"\bPASS\s*=\s*\d+", t))
            has_fail = bool(re.search(r"\bFAIL\b|\bERROR\b|\bFAIL=\s*[1-9]|\bERROR=\s*[1-9]", t))
            s["build_after_log_pass"] = 1.0 if (has_done and has_pass_counter and not has_fail) else 0.0
        except Exception: pass

    # ---- 2. manifest_deps.json (must be jq-extracted subset, not the whole file) ----
    md = rd / "manifest_deps.json"
    s["manifest_deps_jq_extract"] = 0.0
    if md.exists():
        try:
            data = json.loads(md.read_text())
            sz = md.stat().st_size
            flat = json.dumps(data)
            # Tighten the "is jq-subset?" heuristic: a real jq-extracted
            # subset of fct_customer_orders' depends_on is small (≪ 5 KB),
            # has a flat shape, and does not include the dbt-docs node
            # graph keys ("nodes","sources","macros","exposures","metrics")
            # at the top level. Reject the full manifest dump regardless
            # of size if the top-level shape looks like the whole file.
            top_keys = set(data.keys()) if isinstance(data, dict) else set()
            looks_like_full_manifest = bool(
                {"nodes", "sources", "macros"} & top_keys
            ) and len(top_keys) >= 4
            if (sz < 8_000 and not looks_like_full_manifest
                and "fct_customer_orders" in flat
                and "stg_orders" in flat and "stg_payments" in flat
                and "depends_on" in flat):
                s["manifest_deps_jq_extract"] = 1.0
        except Exception:
            pass

    # ---- 3. column_types.json ----
    ct = rd / "column_types.json"
    ct_ok = 0.0
    ct_data = {}
    if ct.exists():
        try:
            ct_data = json.loads(ct.read_text())
            VALID = ("VARCHAR","TEXT","STRING","CHAR","DOUBLE","NUMERIC","DECIMAL","FLOAT","INTEGER","BIGINT")
            def _is_valid_type(v):
                vu = str(v).upper().strip()
                # Accept the canonical type word with optional precision
                # (e.g. DECIMAL(18,2)) but reject suffix-spam such as
                # VARCHARxxx by requiring the rest to be empty, '(', or
                # whitespace.
                for t in VALID:
                    if vu == t:
                        return True
                    if vu.startswith(t) and vu[len(t):len(t)+1] in ("", "(", " "):
                        return True
                return False
            good = [k for k, v in ct_data.items()
                    if "amount" in k.lower() and _is_valid_type(v)]
            if any("stg_orders" in k for k in good) and any("stg_payments" in k for k in good):
                ct_ok = 1.0
        except Exception: pass
    s["column_types_present"] = ct_ok

    # Type discovery: stg_orders.amount should originally be VARCHAR-ish
    stg_orders_was_text = 0.0
    for k, v in ct_data.items():
        if "stg_orders" in k and "amount" in k.lower():
            if str(v).upper().startswith(("VARCHAR","TEXT","STRING","CHAR")):
                stg_orders_was_text = 1.0
    s["column_types_diagnosis"] = stg_orders_was_text

    # ---- 4. fixed_models/ contains a .sql with a cast on amount ----
    fixed_dir = rd / "fixed_models"
    s["fixed_models_dir"] = 1.0 if fixed_dir.exists() and any(fixed_dir.rglob("*.sql")) else 0.0
    s["fixed_models_has_cast"] = 0.0
    if fixed_dir.exists():
        try:
            for f in fixed_dir.rglob("*.sql"):
                raw = f.read_text(errors="ignore")
                txt = re.sub(r"--[^\n]*", "", raw).lower()
                if re.search(r"(cast\s*\(\s*amount\b|amount\s*::\s*(double|numeric|float|decimal))", txt):
                    s["fixed_models_has_cast"] = 1.0
                    break
        except Exception: pass

    # ---- 5. Actual duckdb schema after fix ----
    s["duckdb_schema_fixed"] = 0.0
    duckdb_files = list(proj.rglob("*.duckdb")) if proj.exists() else []
    if duckdb_files:
        try:
            import duckdb as dd
            con = dd.connect(str(duckdb_files[0]), read_only=True)
            try:
                rows = con.execute(
                    "SELECT data_type FROM information_schema.columns "
                    "WHERE lower(column_name)='amount' AND lower(table_name)='stg_orders'"
                ).fetchall()
                if rows:
                    dt = str(rows[0][0]).upper()
                    if any(t in dt for t in ["DOUBLE","NUMERIC","DECIMAL","FLOAT","INTEGER","BIGINT"]):
                        s["duckdb_schema_fixed"] = 1.0
            finally:
                con.close()
        except Exception: pass

    # ---- 6. findings.json ----
    fnd = rd / "findings.json"
    fnd_data = {}
    if fnd.exists():
        try: fnd_data = json.loads(fnd.read_text())
        except Exception: pass
    needed = ["failing_test","failing_model","conflicting_column","upstream_models",
              "upstream_types_before","fix_summary","fixed_files","evidence_screenshots"]
    s["findings_schema"] = 1.0 if (all(k in fnd_data for k in needed)
        and str(fnd_data.get("failing_model","")).strip().lower() in ("fct_customer_orders","customer_orders")
        and len(str(fnd_data.get("fix_summary","")).strip()) >= 20
        and any("stg_orders" in str(f) for f in fnd_data.get("fixed_files",[]))) else 0.0
    s["findings_column_correct"] = 1.0 if str(fnd_data.get("conflicting_column","")).lower() == "amount" else 0.0
    upstream = fnd_data.get("upstream_models", []) or []
    s["findings_upstream_correct"] = 1.0 if (
        isinstance(upstream, list)
        and any("stg_orders" in str(x) for x in upstream)
        and any("stg_payments" in str(x) for x in upstream)
    ) else 0.0

    # ---- 7. GUI screenshots ----
    gui_shots = ["view_dbt_dag_overview.png","view_dbt_lineage_expanded.png",
                 "view_dbt_column_lineage.png","view_dbt_column_lineage_after.png"]
    gui_present = sum(1 for n in gui_shots if (rd/n).exists() and (rd/n).stat().st_size > 4000)
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    gui_ocr = 0.0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_dbt_dag_overview.png": ["dbt","model","stg_","jaffle"],
            "view_dbt_lineage_expanded.png": ["Lineage","stg_orders","stg_payments","customer"],
            "view_dbt_column_lineage.png": ["Columns","amount","Lineage"],
            "view_dbt_column_lineage_after.png": ["Columns","amount"],
        }
        hits = 0
        for n, ks in kws.items():
            p = rd/n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    matched = sum(1 for k in ks if k.lower() in tx.lower())
                    if matched >= max(2, len(ks)//2):
                        hits += 1
                except Exception: pass
        gui_ocr = hits / len(kws)
    except ImportError:
        pass
    s["gui_screenshots_ocr"] = gui_ocr

    # ---- 8. VLM rubric ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd/n) for n in ["view_dbt_lineage_expanded.png","view_dbt_column_lineage.png",
                                    "view_dbt_dag_overview.png"] if (rd/n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_dag_visible": "图中能看到 dbt-docs 的 DAG 节点和连边（≥2 个 model 节点）",
            "vlm_target_node_selected": "fct_customer_orders 或 customer_orders 节点被选中/高亮",
            "vlm_column_panel": "右侧或浮层中能看到 columns 列表，至少含 amount 字段",
            "vlm_lineage_arrows_distinct": "上游模型用不同颜色或不同标识的边连接（不是单一同色）",
        }
        try:
            vlm = vlm_score_rubric(vlm_imgs[:3], rubric, instruction="评估 dbt-docs 列血缘 GUI 取证截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
            s["judge_method"] = vlm.get("judge_method","ok")
        except Exception:
            pass

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums) if nums else 0.0
    has_cli_evidence = (s["run_before_log"] + s["test_before_log_fail"]
                        + s["build_after_log_pass"] + s["manifest_deps_jq_extract"]
                        + s["column_types_present"]) >= 4.0
    if not has_cli_evidence: base = min(base, 0.4)
    # NOTE: We deliberately do NOT cap on missing GUI screenshots.
    # Whether the agent invokes GUI tooling is not a scoring axis.
    # Missing PNGs already cost the corresponding sub_scores
    # (gui_screenshots_count / gui_screenshots_ocr / 4 vlm_*); no
    # additional hard cap is applied here.
    # VLM cap uses the rubric mean (consistent with batch3) and is only
    # enforced when the helper actually ran.
    if vlm_score_rubric is not None and vlm_imgs:
        vlm_avg = sum(s.get(k, 0.0) for k in
            ["vlm_dag_visible","vlm_target_node_selected",
             "vlm_column_panel","vlm_lineage_arrows_distinct"]) / 4.0
        if vlm_avg < 0.5:
            base = min(base, 0.6)
    if s["build_after_log_pass"] < 1.0 or s["duckdb_schema_fixed"] < 1.0:
        base = min(base, 0.45)
    if s["fixed_models_has_cast"] < 1.0:
        base = min(base, 0.45)
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
