# Auto-generated from WeaveBench task DAV_task_12_airflow_dag_sla_gantt.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi sub-score grader for DAV_task_12_airflow_dag_sla_gantt.
    Combines CLI artefact checks, GUI screenshot existence + OCR keyword
    hits, DAG-file fix verification, verify-run state, and a VLM rubric on
    the Gantt screenshots. Hard gates: missing CLI artefacts -> 0.4,
    missing GUI shots -> 0.4, vlm < 0.6 -> 0.6."""
    import json, os, re, subprocess, time
    from pathlib import Path

    rd = Path("/tmp_workspace/results")
    # Read GT from the root-only path the warmup moved expected.json to
    # (kept off the agent-visible /tmp_workspace/gt to prevent answer
    # leakage). Fall back to workspace_path/gt for legacy compatibility.
    if Path("/opt/dav12_gt/expected.json").exists():
        gt = Path("/opt/dav12_gt")
    else:
        gt = Path(workspace_path or ".") / "gt"
    expected = {}
    if (gt / "expected.json").exists():
        try:
            expected = json.loads((gt / "expected.json").read_text())
        except Exception:
            expected = {}

    s = {}

    def file_nonempty(p):
        return p.exists() and p.stat().st_size > 0

    cli_files = [
        "dag_runs.txt",
        "states_for_dag_run.txt",
        "states_for_dag_run_odd.txt",
        "extract_orders_attempt_grep.txt",
        "dag_show_static.txt",
        "dag_fix.diff",
    ]
    cli_present = sum(1 for n in cli_files if file_nonempty(rd / n))
    s["cli_artefacts_present"] = cli_present / len(cli_files)

    # CLI evidence keywords — Prompt requires ≥2 keyword hits, casing
    # preserved (`Retry`, `try_number=`, `duration=` are the canonical
    # Airflow log markers; lowercasing made the check too permissive).
    grep_hit = 0
    grep_terms = ["Retry", "try_number=", "duration="]
    p = rd / "extract_orders_attempt_grep.txt"
    if p.exists():
        t = p.read_text(errors="ignore")
        for kw in grep_terms:
            if kw in t:
                grep_hit += 1
    s["cli_grep_keywords"] = 1.0 if grep_hit >= 2 else (grep_hit / 2.0)

    p = rd / "dag_show_static.txt"
    s["cli_dag_show_topology"] = 1.0 if (
        p.exists() and "transform_revenue" in p.read_text(errors="ignore")
    ) else 0.0

    # GUI screenshots
    gui_shots = expected.get("expected_gui_screenshots", [
        "view_airflow_gantt.png",
        "view_airflow_gantt_hover_tooltip.png",
        "view_airflow_task_instance_details.png",
        "view_airflow_graph_view.png",
        "view_airflow_log_drawer.png",
    ])
    extra = ["view_airflow_gantt_after_fix.png"]
    gui_present = sum(1 for n in gui_shots if (rd / n).exists())
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    s["gui_after_fix_shot"] = 1.0 if (rd / extra[0]).exists() else 0.0

    # OCR
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_airflow_gantt.png": ["Gantt", "extract_orders", "load_warehouse"],
            "view_airflow_gantt_hover_tooltip.png": ["duration", "start", "end"],
            "view_airflow_task_instance_details.png": ["try_number", "Task Instance", "Log"],
            "view_airflow_graph_view.png": ["transform_revenue", "clean_orders", "Graph"],
            "view_airflow_log_drawer.png": ["INFO", "Log", "extract_orders"],
        }
        ocr_hit = 0
        for name, ks in kws.items():
            f = rd / name
            if not f.exists():
                continue
            try:
                txt = pytesseract.image_to_string(Image.open(f))
            except Exception:
                continue
            if any(k in txt for k in ks):
                ocr_hit += 1
        s["gui_screenshots_ocr"] = ocr_hit / len(kws)
    except ImportError:
        s["gui_screenshots_ocr"] = 0.5

    # DAG fix verification
    dag_path = Path("/tmp_workspace/airflow_home/dags/etl_orders_v3.py")
    fix_ok = 0.0
    if dag_path.exists():
        src = dag_path.read_text(errors="ignore")
        # transform_revenue must depend on clean_orders
        m = re.search(r"\[([^\]]*)\]\s*>>\s*transform_revenue", src)
        if m and "clean_orders" in m.group(1):
            fix_ok = 1.0
        elif "clean_orders >> transform_revenue" in src:
            fix_ok = 1.0
    s["dag_fix_correct"] = fix_ok

    # diff contains clean_orders on a + line — require BOTH `clean_orders`
    # and `transform_revenue` in the same `+` (added) hunk line, after
    # stripping `#` / `//` comments. The previous boolean precedence was
    # `(A and B and C) or (A and B and D)` which was satisfied by any
    # `+` line containing `clean_orders` even when `transform_revenue`
    # was nowhere on it.
    diff_p = rd / "dag_fix.diff"
    s["dag_diff_has_fix"] = 0.0
    if diff_p.exists():
        for ln in diff_p.read_text(errors="ignore").splitlines():
            if not (ln.startswith("+") and not ln.startswith("+++")):
                continue
            code = ln.split("#", 1)[0].split("//", 1)[0]
            if "clean_orders" in code and "transform_revenue" in code:
                s["dag_diff_has_fix"] = 1.0
                break

    # verify run state via airflow CLI — poll up to 60 s because Airflow's
    # scheduler/executor is asynchronous: the agent can correctly trigger
    # `verify_fix` (and exit) seconds before the DAG's last task ticks over
    # to `success`. Without this poll the grader caught many runs in the
    # `running`/`queued` window and scored 0 even when the fix was correct
    # and the run did reach success a few seconds later.
    verify_state = ""
    deadline = time.time() + 60.0
    poll_attempt = 0
    while time.time() < deadline:
        try:
            out = subprocess.run(
                ["airflow", "dags", "state", "etl_orders_v3", "verify_fix"],
                capture_output=True, text=True, timeout=20,
            )
            verify_state = (out.stdout or "").strip().splitlines()[-1] if out.stdout else ""
        except Exception:
            verify_state = ""
        if "success" in verify_state.lower():
            break
        # transient states we keep polling through; if we hit a definitive
        # failure (failed/upstream_failed) bail out early so we don't waste
        # the full 60 s window.
        if any(t in verify_state.lower() for t in ("failed", "upstream_failed")):
            break
        poll_attempt += 1
        time.sleep(min(5.0, 1.0 + poll_attempt * 0.5))
    if "success" in verify_state.lower():
        s["verify_run_success"] = 1.0
    elif "running" in verify_state.lower() or "queued" in verify_state.lower() \
            or "scheduled" in verify_state.lower():
        # Run was triggered + reached an executable state but didn't finish
        # within the poll window — partial credit so async-timing alone
        # doesn't tank the score.
        s["verify_run_success"] = 0.5
    else:
        s["verify_run_success"] = 0.0

    # rca.md sections
    rca = rd / "rca.md"
    sections = ["symptom", "evidence_cli", "evidence_gui",
                "root_cause", "fix", "verification"]
    sec_hit = 0
    long_enough = 0
    if rca.exists():
        body = rca.read_text(errors="ignore")
        for sec in sections:
            m = re.search(rf"##\s+{sec}\b(.*?)(?=\n##\s|\Z)", body,
                          flags=re.IGNORECASE | re.DOTALL)
            if m:
                sec_hit += 1
                if len(m.group(1).strip()) >= 50:
                    long_enough += 1
    s["rca_sections_present"] = sec_hit / len(sections)
    s["rca_sections_long"] = long_enough / len(sections)

    # summary.json structure
    sj = rd / "summary.json"
    sj_ok = 0.0
    cross_n = 0
    if sj.exists():
        try:
            d = json.loads(sj.read_text())
            need = {"failed_or_sla_missed_tasks", "root_cause",
                    "fix_lines_changed", "cross_channel_switches"}
            if need.issubset(set(d.keys())):
                sj_ok = 1.0
            cross_n = int(d.get("cross_channel_switches", 0))
            # bonus correctness on tasks list
            tasks = set(d.get("failed_or_sla_missed_tasks") or [])
            exp_tasks = set(expected.get("expected_failed_or_sla_missed_tasks", []))
            s["summary_tasks_correct"] = (
                len(tasks & exp_tasks) / max(1, len(exp_tasks))
            )
        except Exception:
            s["summary_tasks_correct"] = 0.0
    else:
        s["summary_tasks_correct"] = 0.0
    s["summary_schema"] = sj_ok
    s["cross_channel_min5"] = 1.0 if cross_n >= 5 else cross_n / 5.0

    # VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_avg = 0.5
    if vlm_score_rubric:
        imgs = [str(rd / n) for n in [
            "view_airflow_gantt.png",
            "view_airflow_gantt_hover_tooltip.png",
            "view_airflow_gantt_after_fix.png",
        ] if (rd / n).exists()]
        if imgs:
            rubric = {
                "vlm_gantt_visible": "图像里能清楚看见 Gantt 时间轴和多个 task bar",
                "vlm_color_state": "可以分辨成功 / SLA-missed / retry 的颜色差异",
                "vlm_tooltip_data": "至少一张截图里能读出 tooltip 中的精确时长 / start / end",
                "vlm_after_fix_order": "after-fix 截图里 transform_revenue bar 在 clean_orders bar 之后",
            }
            v = vlm_score_rubric(imgs[:3], rubric,
                                 instruction="评估 Airflow Gantt 取证证据的清晰度。")
            for k in rubric:
                s[k] = v.get(k, 0.0)
            vals = [v.get(k, 0.0) for k in rubric]
            vlm_avg = sum(vals) / max(1, len(vals))
            s["judge_method"] = v.get("judge_method", "rubric")

    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums) / len(nums) if nums else 0.0

    # Hard gates
    if s["cli_artefacts_present"] < 0.5:
        base = min(base, 0.4)
    # NOTE: We deliberately do NOT cap on missing GUI screenshots —
    # whether the agent invokes GUI tooling is not a scoring axis.
    # Missing PNGs already cost the corresponding sub_scores
    # (gui_screenshots_count / gui_after_fix_shot / gui_screenshots_ocr
    # / 4 vlm_*); no additional hard cap is applied here.
    if vlm_score_rubric is not None and vlm_avg < 0.6:
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
