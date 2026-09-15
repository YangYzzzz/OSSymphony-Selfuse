# Auto-generated from WeaveBench task DAV_task_17_jaeger_trace_root_cause_compare.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DAV_task_17 grader: jaeger trace root-cause + compare evidence."""
    import csv, json, re, subprocess
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    # Read GT from the root-only path the warmup moved expected.json to
    # (kept off the agent-visible /tmp_workspace/gt to prevent answer
    # leakage). Fall back to /tmp_workspace/gt for legacy mounts.
    gt_dir = Path("/opt/dav17_gt") if Path("/opt/dav17_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    s = {}
    expected = {}
    if (gt_dir / "expected.json").exists():
        try: expected = json.loads((gt_dir / "expected.json").read_text())
        except Exception: expected = {}
    svc = expected.get("service_name", "checkout-api")
    op = expected.get("slow_root_operation", "POST /checkout")
    slow_name = expected.get("slow_span_name", "payments.gateway.http")
    min_dur_ms = expected.get("slow_span_min_duration_ms", 2400)
    err_code = expected.get("slow_span_error_status_code", 504)

    # 1. services + operations
    s_svc = 0.0; s_op = 0.0
    js = rd / "jaeger_services.json"
    if js.exists():
        try:
            d = json.loads(js.read_text())
            arr = d.get("data") if isinstance(d, dict) else d
            if isinstance(arr, list) and any(svc in str(x) for x in arr):
                s_svc = 1.0
        except Exception: pass
    s["services_present"] = s_svc
    jo = rd / "jaeger_operations.json"
    if jo.exists():
        try:
            d = json.loads(jo.read_text())
            arr = d.get("data") if isinstance(d, dict) else d
            txt = json.dumps(arr)
            if op in txt or "checkout" in txt:
                s_op = 1.0
        except Exception: pass
    s["operations_present"] = s_op

    # 2. raw_traces.json — must be ≥ 60
    rt = rd / "raw_traces.json"
    n_traces = 0; n_spans = 0
    if rt.exists():
        try:
            d = json.loads(rt.read_text())
            arr = d.get("data") if isinstance(d, dict) else d
            if isinstance(arr, list):
                n_traces = len(arr)
                n_spans = sum(len(t.get("spans", [])) for t in arr if isinstance(t, dict))
        except Exception: pass
    min_n = expected.get("min_total_traces", 60)
    s["raw_traces_present"] = 1.0 if n_traces >= min_n else (n_traces / min_n if n_traces else 0.0)

    # 3. trace_durations.csv schema + rows
    td = rd / "trace_durations.csv"
    td_ok = 0.0
    if td.exists():
        try:
            rows = list(csv.DictReader(td.open()))
            if rows and {"traceID", "duration_us", "span_count"}.issubset(set(rows[0].keys())):
                if abs(len(rows) - max(n_traces, 1)) <= max(2, int(0.1 * max(n_traces, 1))):
                    td_ok = 1.0
                else:
                    td_ok = 0.5
        except Exception: pass
    s["trace_durations_csv"] = td_ok

    # 4. duration_summary.json — p95 ≥ 2000 ms
    ds = rd / "duration_summary.json"
    p95_ok = 0.0
    if ds.exists():
        try:
            d = json.loads(ds.read_text())
            p95 = float(d.get("p95_ms", 0))
            if p95 >= expected.get("expected_p95_root_ms_min", 2000):
                p95_ok = 1.0
            elif p95 >= 500:
                p95_ok = 0.5
        except Exception: pass
    s["duration_p95_ok"] = p95_ok

    # 5. slow_trace.json
    st = rd / "slow_trace.json"
    st_ok = 0.0
    if st.exists():
        try:
            d = json.loads(st.read_text())
            spans = (d.get("data", [{}])[0] if isinstance(d.get("data"), list) else d).get("spans", [])
            if isinstance(d, dict) and (d.get("spans") or spans):
                spans = spans or d.get("spans", [])
                if len(spans) >= 5:
                    st_ok = 1.0
                elif len(spans) >= 2:
                    st_ok = 0.5
        except Exception: pass
    s["slow_trace_present"] = st_ok

    # 6. slow_span.json — must identify the true bottleneck leaf span
    ss = rd / "slow_span.json"
    span_name_ok = 0.0; span_dur_ok = 0.0; span_tag_ok = 0.0
    if ss.exists():
        try:
            d = json.loads(ss.read_text())
            name = str(d.get("span_name", ""))
            dur_us = float(d.get("duration_us", 0))
            st_spans = []
            if st.exists():
                try:
                    _d = json.loads(st.read_text()); _t = (_d.get("data",[_d])[0] if isinstance(_d.get("data"),list) else _d)
                    st_spans = _t.get("spans", [])
                except Exception: pass
            matched = next((sp for sp in st_spans if str(d.get("span_name","")) in (sp.get("operationName","") or "")
                            and abs(int(sp.get("duration",0)) - int(d.get("duration_us",0))) <= 50), None)
            span_name_ok = 1.0 if (slow_name == name and matched) else (0.0 if not matched else 0.3)
            span_dur_ok = 1.0 if (matched and dur_us/1000.0 >= min_dur_ms) else 0.0
            tags = d.get("tags", {})
            tag_text = json.dumps(tags) if not isinstance(tags, str) else tags
            has_code = re.search(r'"http\.status_code"\s*:\s*"?%d' % err_code, tag_text) is not None
            has_err  = ("ERROR" in tag_text) and ("peer.service" in tag_text)
            span_tag_ok = 1.0 if (has_code and has_err) else (0.4 if has_code else 0.0)
        except Exception: pass
    s["slow_span_name"] = span_name_ok
    s["slow_span_duration"] = span_dur_ok
    s["slow_span_tags"] = span_tag_ok

    # 7. hypothesis + report
    hy = rd / "hypothesis.md"
    hy_chars = len(hy.read_text(errors="ignore")) if hy.exists() else 0
    hy_root = 0.0
    if hy.exists() and expected.get("expected_hypothesis_root_cause_substring", "payments.gateway.http") in hy.read_text(errors="ignore"):
        hy_root = 1.0
    s["hypothesis_length"] = 1.0 if hy_chars >= 400 else hy_chars / 400.0
    s["hypothesis_identifies_root"] = hy_root

    rp = rd / "root_cause_report.md"
    rp_chars = 0; rp_kw = 0
    if rp.exists():
        body = rp.read_text(errors="ignore")
        rp_chars = len(body)
        # Keyword set inlined here as a grader-only default so gt/expected.json
        # can omit the answer list. Mirrors the postmortem checklist hinted at
        # by the Prompt's "缓解 / 治理 / 回归监控" sections.
        DEFAULT_KW = ["payments.gateway.http","504 Gateway Timeout",
                      "peer.service=payments-gateway","circuit breaker",
                      "fail-fast","SLO regression","p95"]
        for kw in expected.get("expected_postmortem_keywords", DEFAULT_KW):
            if kw.lower() in body.lower():
                rp_kw += 1
    s["report_length"] = 1.0 if rp_chars >= 800 else rp_chars / 800.0
    s["report_keywords"] = 1.0 if rp_kw >= 5 else (rp_kw / 5.0 if rp_kw else 0.0)

    # 8. GUI screenshots (4) + OCR
    gui_shots = ["view_jaeger_search.png", "view_trace_waterfall.png",
                 "view_span_tags.png", "view_trace_compare.png"]
    present = sum(1 for n in gui_shots if (rd / n).exists() and (rd / n).stat().st_size > 5000)
    s["gui_screenshots_count"] = present / len(gui_shots)
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_jaeger_search.png": ["Jaeger", "Find", "Traces", "Service", "Operation"],
            "view_trace_waterfall.png": ["Trace", "Timeline", "Service", "Duration", "Spans", "payments"],
            "view_span_tags.png": ["Tags", "Logs", "status_code", "http", "error", "504"],
            "view_trace_compare.png": ["Compare", "Traces", "diff", "A", "B", "Service"],
        }
        for n, ks in kws.items():
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in ks): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
        s["gui_screenshots_count"] = (present / len(gui_shots)) if ocr_hits >= 3 else 0.0
    except ImportError:
        s["gui_screenshots_ocr"] = 0.5

    # 9. otlp pcap
    pcap = rd / "otlp_capture.pcap"
    pcap_ok = 0.0
    if pcap.exists() and pcap.stat().st_size > 200:
        try:
            out = subprocess.run(["strings", str(pcap)], capture_output=True, text=True, timeout=15)
            if "POST /checkout" in out.stdout or "checkout-api" in out.stdout:
                pcap_ok = 1.0
            elif out.stdout.strip():
                pcap_ok = 0.5
        except Exception:
            pcap_ok = 0.4
    s["otlp_pcap_evidence"] = pcap_ok

    # CLI artifact tally
    cli_artifacts = ["jaeger_services.json", "jaeger_operations.json", "raw_traces.json",
                     "trace_durations.csv", "duration_summary.json",
                     "slow_trace.json", "slow_span.json"]
    cli_n = sum(1 for n in cli_artifacts if (rd / n).exists())
    s["cli_artifact_count"] = cli_n / len(cli_artifacts)

    # VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd / n) for n in ("view_trace_waterfall.png", "view_trace_compare.png",
                                      "view_span_tags.png") if (rd / n).exists()]
    vlm_judge = 0.0
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_waterfall_hotspot": "Trace timeline 中能看到一条明显比同级 sibling 长得多的子 span（占据 trace 大部分宽度）",
            "vlm_compare_diff": "Compare Traces 视图清楚展示两条 trace 之间结构或耗时差异（高亮 / diff 颜色）",
            "vlm_error_chip_visible": "Tags / Logs 抽屉中能看到一个明显的 HTTP error 状态码 chip 与 ERROR 状态高亮",
            "vlm_layout_clean": "整体 Jaeger UI 布局清晰，没有遮挡或截断，关键面板可读",
        }
        vlm = vlm_score_rubric(vlm_imgs[:3], rubric, instruction="评估分布式追踪根因定位 / Compare Traces 截图。")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
        vlm_judge = sum(s.get(k, 0.0) for k in rubric) / max(1, len(rubric))
    else:
        # Helper offline → leave rubric scores at 0.0 (no freebie) and
        # rely on the 'vlm_score_rubric is not None' helper-guard below
        # to skip the VLM cap entirely.
        s["vlm_waterfall_hotspot"] = 0.0
        s["vlm_compare_diff"] = 0.0
        s["vlm_error_chip_visible"] = 0.0
        s["vlm_layout_clean"] = 0.0
        vlm_judge = 0.0

    IGNORE = {"judge_method","cli_artifact_count","vlm_layout_clean","hypothesis_length","report_length"}
    nums = [v for k, v in s.items() if isinstance(v,(int,float)) and k not in IGNORE]
    base = sum(nums) / max(1, len(nums))

    # Hard gates
    has_cli = (s["cli_artifact_count"] >= 0.85) and (s["otlp_pcap_evidence"] >= 1.0) and (s["raw_traces_present"] >= 1.0)
    must_pass = (s["slow_span_name"] >= 1.0 and s["slow_span_tags"] >= 1.0)
    if not has_cli: base = min(base, 0.35)
    # NOTE: We deliberately do NOT cap on missing GUI screenshots —
    # whether the agent invokes Jaeger UI tooling is not a scoring
    # axis. Missing PNGs already cost the corresponding sub_scores
    # (gui_screenshots_count / gui_screenshots_ocr / 4 vlm_*); no
    # additional hard cap is applied here.
    # VLM cap aligned with batch3 (vlm_avg<0.6 cap @0.45) and only
    # enforced when the helper actually ran.
    if vlm_score_rubric is not None and vlm_judge < 0.6:
        base = min(base, 0.45)
    if not must_pass: base = min(base, 0.55)

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
