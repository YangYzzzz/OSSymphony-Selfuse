# Auto-generated from WeaveBench task WEB_task_10_lighthouse_devtools_perf_drill.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-dim grader for WEB_task_10_lighthouse_devtools_perf_drill.

    Sub-scores cover: lighthouse JSON validity, summary attribution,
    root-cause schema, fix-source diff, temp-server reachability,
    speed-up ratio, coverage artefact, GUI screenshots + OCR, VLM rubric.
    Hard gates: missing CLI evidence -> 0.4, missing GUI -> 0.4,
    VLM<0.6 -> 0.6, no real ratio improvement -> 0.55.
    """
    import json, re, hashlib, urllib.request, subprocess
    from pathlib import Path

    rd = Path("/tmp_workspace/results")
    # GT lives at root-only /opt/web10_gt (warmup moves it off the
    # agent-visible /tmp_workspace/gt to prevent answer leakage).
    # Fall back to /tmp_workspace/gt for legacy mounts.
    gt_dir = Path("/opt/web10_gt") if Path("/opt/web10_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    app_dir = Path("/tmp_workspace/app")
    s = {}

    def load_json(p):
        try: return json.loads(Path(p).read_text())
        except Exception: return None

    expected = load_json(gt_dir / "expected.json") or {}

    # ---- 1. Lighthouse JSON artefacts ----
    lh_b = load_json(rd / "lh_before.json")
    lh_a = load_json(rd / "lh_after.json")
    s["lh_before_valid"] = 1.0 if isinstance(lh_b, dict) and "audits" in lh_b else 0.0
    s["lh_after_valid"]  = 1.0 if isinstance(lh_a, dict) and "audits" in lh_a else 0.0

    sum_b = load_json(rd / "lh_summary_before.json") or {}
    sum_a = load_json(rd / "lh_summary_after.json")  or {}
    s["summary_before_valid"] = 1.0 if isinstance(sum_b, dict) and sum_b else 0.0
    s["summary_after_valid"]  = 1.0 if isinstance(sum_a, dict) and sum_a else 0.0

    # ---- 2. Render-blocking attribution ----
    def collect_files(j):
        if not isinstance(j, dict): return set()
        out = set()
        def walk(x):
            if isinstance(x, str):
                for tag in expected.get("expected_culprits", []):
                    if tag in x: out.add(tag)
            elif isinstance(x, dict):
                for v in x.values(): walk(v)
            elif isinstance(x, list):
                for v in x: walk(v)
        walk(j)
        return out
    rb_hits = collect_files(sum_b) | collect_files(lh_b)
    needed = expected.get("expected_culprit_min_hits", 2)
    s["render_blocking_attribution"] = 1.0 if len(rb_hits) >= needed else (len(rb_hits) / max(needed, 1))

    # ---- 3. root_causes.json ----
    rc = load_json(rd / "root_causes.json") or {}
    rc_list = rc.get("culprits") if isinstance(rc, dict) else None
    rc_ok = isinstance(rc_list, list) and len(rc_list) >= 2 and all(
        isinstance(x, dict) and {"file","kind","screenshot"} <= set(x.keys())
        and (x.get("evidence_ms") or x.get("evidence_kb"))
        and (rd / str(x.get("screenshot",""))).exists()
        for x in rc_list)
    s["root_causes_schema"] = 1.0 if rc_ok else 0.0
    rc_files_real = 0
    if rc_ok:
        for x in rc_list:
            if any(c in str(x.get("file","")) for c in expected.get("expected_culprits", [])):
                rc_files_real += 1
    s["root_causes_files_real"] = 1.0 if rc_files_real >= 2 else (rc_files_real / 2.0)

    # ---- 4. Optimized HTML diff vs smoke + script tag fix ----
    opt = rd / "index.optimized.html"
    smoke = app_dir / "public" / "index.ok.html"
    s["optimized_html_exists"] = 1.0 if opt.exists() and opt.stat().st_size > 200 else 0.0
    diff_ok = 0.0
    if opt.exists() and smoke.exists():
        h1 = hashlib.sha256(opt.read_bytes()).hexdigest()
        h2 = hashlib.sha256(smoke.read_bytes()).hexdigest()
        diff_ok = 1.0 if h1 != h2 else 0.0
    s["optimized_not_smoke_copy"] = diff_ok

    fix_score = 0.0
    if opt.exists():
        try:
            html = opt.read_text(errors="ignore")
            # 2-pass attribute check: HTML allows attrs in any order
            # (e.g. `<script src="x" defer></script>`). The earlier
            # single regex required async/defer/type to come BEFORE src,
            # which falsely failed defer-after-src — the most common
            # human-written form.
            def _script_tags_for(basename):
                pat = rf"<script[^>]*\bsrc=[\"'][^\"']*{re.escape(basename)}[\"'][^>]*>"
                return list(re.finditer(pat, html))
            def _has_async_defer(tag_text):
                return any(k in tag_text for k in ("async", "defer", "type=\"module\"", "type='module'"))
            def _all_tags_deferred(basename):
                tags = _script_tags_for(basename)
                return bool(tags) and all(_has_async_defer(m.group(0)) for m in tags)
            def _present_or_deferred(basename):
                tags = _script_tags_for(basename)
                if not tags:
                    return True
                return all(_has_async_defer(m.group(0)) for m in tags)
            removed_blocker = "blockerA.js" not in html or not _script_tags_for("blockerA.js")
            legacy_safe = "legacy-bundle.js" not in html or _all_tags_deferred("legacy-bundle.js")
            tracker_tags = _script_tags_for("tracker.js")
            tracker_ok = (not tracker_tags) or all(_has_async_defer(m.group(0)) for m in tracker_tags)
            must_remove = expected.get("removed_or_deferred_tags", [])
            must_defer  = expected.get("must_use_async_or_defer_for", [])
            removed_ok = all(_present_or_deferred(t) for t in must_remove)
            defer_ok   = all(_all_tags_deferred(t) for t in must_defer if t in html)
            score_parts = [removed_blocker, legacy_safe, tracker_ok, removed_ok, defer_ok]
            fix_score = 1.0 if all(score_parts) else (sum(map(bool, score_parts)) / (len(score_parts)+1))
        except Exception:
            fix_score = 0.0
    s["optimized_html_fixes"] = fix_score

    # ---- 5. Temp :7101 server reachable + serves the optimized html ----
    serve_ok = 0.0
    try:
        with urllib.request.urlopen("http://127.0.0.1:7101/", timeout=5) as r:
            body = r.read().decode("utf-8", errors="ignore")
            if r.status == 200 and len(body) > 200:
                serve_ok = 1.0
                # bonus check: served body should not still reference blockerA src tag
                if re.search(r"<script[^>]*src=[\"'][^\"']*blockerA\.js", body):
                    serve_ok = 0.5
    except Exception:
        serve_ok = 0.0
    s["temp_server_serves_optimized"] = serve_ok

    # ---- 6. Speed-up + perf score after ----
    def lh_num(j, key):
        try: return float(j["audits"][key]["numericValue"])
        except Exception: return None
    def lh_score(j):
        try: return float(j["categories"]["performance"]["score"])
        except Exception: return None
    tbt_b = lh_num(lh_b, "total-blocking-time")
    tbt_a = lh_num(lh_a, "total-blocking-time")
    lcp_b = lh_num(lh_b, "largest-contentful-paint")
    lcp_a = lh_num(lh_a, "largest-contentful-paint")
    perf_a = lh_score(lh_a)
    min_before = expected.get("tbt_before_min_ms", 1500)
    max_after  = expected.get("tbt_after_max_ms", 600)
    valid_pair = (tbt_b is not None and tbt_b >= min_before
                  and tbt_a is not None and tbt_a <= max_after)
    ratio = ((tbt_b - tbt_a) / tbt_b) if valid_pair else None

    s["tbt_improvement_ratio"] = (
        1.0 if (ratio is not None and ratio >= expected.get("tbt_improvement_min_ratio", 0.4))
        else (max(0.0, ratio) if ratio is not None else 0.0)
    )
    s["perf_score_after_pass"] = (
        1.0 if (perf_a is not None and perf_a >= expected.get("perf_score_after_min", 0.7))
        else (perf_a if perf_a is not None else 0.0)
    )
    s["lcp_after_pass"] = (
        1.0 if (lcp_a is not None and lcp_a <= expected.get("lcp_after_max_ms", 3500)) else 0.0
    )

    # ---- 7. Coverage artefact ----
    cov = rd / "coverage_before.json"
    cov_ok = 0.0
    if cov.exists() and cov.stat().st_size > 1500:
        try:
            cj = json.loads(cov.read_text(errors="ignore"))
            entries = cj if isinstance(cj, list) else cj.get("entries") or cj.get("results") or []
            min_kb = expected.get("unused_bytes_min_kb", 400) * 1024
            culprits = expected.get("expected_culprits", [])
            hit = any(any(c in str(e.get("url","")+e.get("file","")) for c in culprits)
                      and float(e.get("unusedBytes", e.get("unused_bytes", 0))) >= min_kb
                      for e in entries if isinstance(e, dict))
            cov_ok = 1.0 if hit else 0.3
        except Exception:
            cov_ok = 0.3
    s["coverage_export_present"] = cov_ok

    # ---- 8. GUI screenshots + OCR ----
    gui_shots = ["view_perf_flamechart_long_task.png",
                 "view_perf_bottom_up.png",
                 "view_coverage_panel.png",
                 "view_perf_after.png"]
    gui_present = sum(1 for n in gui_shots if (rd/n).exists() and (rd/n).stat().st_size > 4000)
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    gui_ocr = 0.5
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_perf_flamechart_long_task.png": ["Performance","Evaluate","Script","Self","Total","Task"],
            "view_perf_bottom_up.png":            ["Bottom-Up","Bottom","Self Time","Total Time","%"],
            "view_coverage_panel.png":            ["Coverage","Unused","Bytes","Usage","URL"],
            "view_perf_after.png":                ["Performance","Network","Frames","FCP","LCP","Main"],
        }
        hits = 0
        for n, ks in kws.items():
            p = rd / n
            if not p.exists(): continue
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if sum(1 for k in ks if k.lower() in tx.lower()) >= 3:
                    hits += 1
            except Exception:
                pass
        gui_ocr = hits / len(kws)
    except ImportError:
        gui_ocr = 0.0
    s["gui_screenshots_ocr"] = gui_ocr

    # ---- 9. VLM rubric ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_min = 1.0
    if vlm_score_rubric:
        imgs = [str(rd/n) for n in gui_shots if (rd/n).exists()]
        if imgs:
            rubric = {
                "vlm_flamechart_visible":   "图片是 Chrome DevTools Performance 面板，能看到火焰图带颜色的多层 task 条带",
                "vlm_long_task_tooltip":    "其中至少一张图能看到 hover tooltip 浮层（含 ms 数字或文件名）",
                "vlm_coverage_table":       "Coverage 截图含表格 + Unused Bytes 列 + 红蓝 Usage Visualization 条",
                "vlm_after_no_long_task":   "after 截图火焰图明显比 before 窄，没有 ≥1s 的连续 Evaluate Script 块",
            }
            try:
                vlm = vlm_score_rubric(imgs[:4], rubric, instruction="评估 Lighthouse + DevTools 性能调试取证截图。")
                for k in rubric: s[k] = float(vlm.get(k, 0.0))
                vlm_min = min(s[k] for k in rubric)
                s["judge_method"] = vlm.get("judge_method", "ok")
            except Exception:
                pass

    # ---- 10. findings.json schema ----
    fnd = load_json(rd / "findings.json") or {}
    needed_keys = ["tbt_before_ms","tbt_after_ms","lcp_before_ms","lcp_after_ms",
                   "perf_score_before","perf_score_after","tbt_improvement_ratio",
                   "fixes_applied","evidence_screenshots"]
    s["findings_schema"] = 1.0 if all(k in fnd for k in needed_keys) else 0.0

    # cross-check findings against lh JSONs (within 15% tolerance)
    def close(a, b, tol=0.15):
        try:
            a = float(a); b = float(b)
            return abs(a - b) <= max(1.0, abs(b) * tol)
        except Exception:
            return False
    cross = 0
    if tbt_b is not None and close(fnd.get("tbt_before_ms"), tbt_b): cross += 1
    if tbt_a is not None and close(fnd.get("tbt_after_ms"),  tbt_a): cross += 1
    if perf_a is not None and close(fnd.get("perf_score_after"), perf_a, 0.10): cross += 1
    s["findings_consistent_with_lh"] = cross / 3.0

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums) / len(nums) if nums else 0.0

    has_cli_evidence = (s["lh_before_valid"] + s["lh_after_valid"] +
                        s["summary_before_valid"] + s["coverage_export_present"]) >= 2.5
    has_gui_shot = s["gui_screenshots_count"] >= 0.5
    if not has_cli_evidence: base = min(base, 0.4)
    # GUI-path scoring axis removed: missing screenshots already cost
    # gui_screenshots_count / gui_screenshots_ocr / 4 vlm_* sub-scores;
    # whether the agent invoked DevTools UI is not its own scoring axis.
    if vlm_score_rubric and vlm_min < 0.6: base = min(base, 0.55)
    if s["optimized_not_smoke_copy"] < 1.0: base = min(base, 0.45)
    if s["optimized_html_fixes"]    < 1.0: base = min(base, 0.5)
    if s["tbt_improvement_ratio"] < 1.0 and s["perf_score_after_pass"] < 1.0:
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
