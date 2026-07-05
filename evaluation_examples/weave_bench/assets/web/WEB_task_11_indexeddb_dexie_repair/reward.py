# Auto-generated from WeaveBench task WEB_task_11_indexeddb_dexie_repair.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-dim grader for WEB_task_11_indexeddb_dexie_repair.

    Sub-scores cover: SSR-vs-IDB sanity, before/after IDB dump shape,
    corruption_report schema, repair script legality, post-fix invariants,
    GUI screenshots + OCR, source-immutability gate, VLM rubric.
    Hard gates: missing CLI evidence -> 0.4, missing GUI -> 0.4,
    VLM<0.6 -> 0.6, fixture sources tampered -> 0.5.
    """
    import json, hashlib, re, ast
    from pathlib import Path

    rd = Path("/tmp_workspace/results")
    # GT lives at root-only /opt/web11_gt; warmup moves it off
    # /tmp_workspace/gt to prevent answer leakage. Falls back for legacy mounts.
    gt_dir = Path("/opt/web11_gt") if Path("/opt/web11_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    app_dir = Path("/tmp_workspace/app")
    setup_dir = Path("/tmp_workspace/setup")
    s = {}

    def load_json(p):
        try: return json.loads(Path(p).read_text())
        except Exception: return None

    expected = load_json(gt_dir / "expected.json") or {}

    # ---- 1. SSR sanity ----
    page = rd / "page_static.html"
    if page.exists():
        try:
            txt = page.read_text(errors="ignore")
            ssr_clean = (
                "Invalid Date" not in txt and
                "corrupt" not in txt.lower() and
                "Infinity" not in txt and
                len(txt) > 200
            )
            s["ssr_html_clean"] = 1.0 if ssr_clean else 0.0
            s["ssr_html_present"] = 1.0
        except Exception:
            s["ssr_html_clean"] = 0.0; s["ssr_html_present"] = 0.0
    else:
        s["ssr_html_clean"] = 0.0; s["ssr_html_present"] = 0.0

    # ---- 2. idb_dump_before ----
    db_b = load_json(rd / "idb_dump_before.json") or {}
    before_todos    = db_b.get("todos") if isinstance(db_b, dict) else None
    before_projects = db_b.get("projects") if isinstance(db_b, dict) else None
    has_dump = isinstance(before_todos, list) and isinstance(before_projects, list)
    s["dump_before_shape"] = 1.0 if has_dump else 0.0
    s["dump_before_rows"]  = 1.0 if (has_dump and len(before_todos) == 12 and len(before_projects) >= 4) else 0.0

    has_str_pri = has_dangling = has_inf = False
    if has_dump:
        proj_ids = {p.get("id") for p in before_projects}
        for r in before_todos:
            if isinstance(r.get("priority"), str): has_str_pri = True
            if r.get("projectId") not in proj_ids: has_dangling = True
            if isinstance(r.get("dueAt"), str): has_inf = True
    s["dump_before_has_corruptions"] = (
        sum([has_str_pri, has_dangling, has_inf]) /
        max(expected.get("expected_kind_min_hits", 2), 1)
    )
    if s["dump_before_has_corruptions"] > 1.0:
        s["dump_before_has_corruptions"] = 1.0

    # ---- 3. corruption_report.json ----
    cr = load_json(rd / "corruption_report.json") or {}
    cr_list = cr.get("corrupted_rows") if isinstance(cr, dict) else None
    cr_rows_ok = isinstance(cr_list, list) and len(cr_list) >= 3 and all(
        isinstance(x, dict) and {"id","kind"} <= set(x.keys()) for x in cr_list)
    s["corruption_report_schema"] = 1.0 if cr_rows_ok else 0.0
    kinds_ok_set = set(expected.get("expected_kinds", []))
    kinds_seen = {x.get("kind") for x in (cr_list or []) if isinstance(x, dict)}
    s["corruption_report_kinds"] = 1.0 if (
        len(kinds_seen & kinds_ok_set) >= expected.get("expected_kind_min_hits", 2)) else 0.0
    expected_ids = set(expected.get("expected_corrupt_ids", []))
    seen_ids = {x.get("id") for x in (cr_list or []) if isinstance(x, dict)}
    s["corruption_report_ids"] = 1.0 if (
        len(seen_ids & expected_ids) >= expected.get("expected_corrupt_min_hits", 3)) else (
        len(seen_ids & expected_ids) / 3.0)

    # ---- 4. repair.js legality ----
    rj = rd / "repair.js"
    repair_ok = 0.0
    if rj.exists() and rj.stat().st_size > 200:
        try:
            text = rj.read_text(errors="ignore")
            forbidden = any(x in text for x in
                ["rm -rf", "deleteDatabase", "indexedDB.deleteDatabase",
                 "child_process.exec", "spawn(\"rm", "execSync(\"rm"])
            uses_eval = any(k in text for k in ["page.evaluate", "evaluateHandle", "Dexie"])
            if not forbidden and uses_eval:
                repair_ok = 1.0
            elif not forbidden:
                repair_ok = 0.5
        except Exception:
            pass
    s["repair_script_legal"] = repair_ok

    # ---- 5. repair.log marker ----
    rl = rd / "repair.log"
    s["repair_log_ok"] = 1.0 if (rl.exists() and "REPAIR_OK" in rl.read_text(errors="ignore")) else 0.0

    # ---- 6. dump_after invariants ----
    db_a = load_json(rd / "idb_dump_after.json") or {}
    after_todos    = db_a.get("todos") if isinstance(db_a, dict) else None
    after_projects = db_a.get("projects") if isinstance(db_a, dict) else None
    has_after = isinstance(after_todos, list) and isinstance(after_projects, list)
    s["dump_after_shape"] = 1.0 if has_after else 0.0
    s["dump_after_rowcount"] = 1.0 if (
        has_after and len(after_todos) == expected.get("expected_total_todos_after", 12)) else 0.0

    pri_int = pid_ok = due_ok = True
    if has_after:
        proj_ids = {p.get("id") for p in after_projects}
        for r in after_todos:
            if not isinstance(r.get("priority"), (int, float)) or isinstance(r.get("priority"), bool):
                pri_int = False
            if r.get("projectId") not in proj_ids:
                pid_ok = False
            if not isinstance(r.get("dueAt"), (int, float)) or isinstance(r.get("dueAt"), bool):
                due_ok = False
    else:
        pri_int = pid_ok = due_ok = False
    s["after_priorities_int"]      = 1.0 if pri_int else 0.0
    s["after_no_dangling_project"] = 1.0 if pid_ok else 0.0
    s["after_due_at_numeric"]      = 1.0 if due_ok else 0.0

    # ---- 7. GUI screenshots + OCR ----
    gui_shots = ["view_app_glitch.png", "view_idb_todos_store.png",
                 "view_idb_compound_index.png", "view_idb_projects_store.png",
                 "view_app_after.png", "view_idb_index_after.png"]
    gui_present = sum(1 for n in gui_shots if (rd/n).exists() and (rd/n).stat().st_size > 4000)
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    gui_ocr = 0.5
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_app_glitch.png":            ["Acme","todos","Invalid","Project","Priority","?"],
            "view_idb_todos_store.png":       ["IndexedDB","AcmeTodoDB","todos","priority","Value"],
            "view_idb_compound_index.png":    ["projectId","priority","Key","Index"],
            "view_idb_projects_store.png":    ["projects","Value","Key","name"],
            "view_app_after.png":             ["Acme","todos","Health","hot","projects"],
            "view_idb_index_after.png":       ["projectId","priority","Index","Key"],
        }
        hits = 0
        for n, ks in kws.items():
            p = rd / n
            if not p.exists(): continue
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

    # ---- 8. findings.json ----
    fnd = load_json(rd / "findings.json") or {}
    needed = ["rows_before","rows_after","corrupted_count_before","corrupted_count_after",
              "hot_via_index_before","hot_via_index_after","kinds_seen","fix_strategy",
              "evidence_screenshots"]
    s["findings_schema"] = 1.0 if all(k in fnd for k in needed) else 0.0
    try:
        s["findings_hot_after_5"] = 1.0 if int(fnd.get("hot_via_index_after", -1)) == \
            expected.get("expected_hot_count_after", 5) else 0.0
    except Exception:
        s["findings_hot_after_5"] = 0.0
    try:
        s["findings_corrupted_after_zero"] = 1.0 if int(fnd.get("corrupted_count_after", -1)) == 0 else 0.0
    except Exception:
        s["findings_corrupted_after_zero"] = 0.0

    # ---- 9. fixture immutability gate ----
    src_unchanged = 1.0
    for rel in ["public/js/seed.js", "public/js/app.js"]:
        live = app_dir / rel
        orig = setup_dir / rel
        if not (live.exists() and orig.exists()):
            continue
        try:
            if hashlib.sha256(live.read_bytes()).hexdigest() != \
               hashlib.sha256(orig.read_bytes()).hexdigest():
                src_unchanged = 0.0
        except Exception:
            pass
    s["fixture_sources_unchanged"] = src_unchanged

    # ---- 10. VLM rubric ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_min = 1.0
    if vlm_score_rubric:
        imgs = [str(rd/n) for n in gui_shots if (rd/n).exists()]
        if imgs:
            rubric = {
                "vlm_idb_tree_visible":   "图中可见 DevTools Application 面板的 IndexedDB 数据库 tree（含 AcmeTodoDB 节点）",
                "vlm_kv_table_visible":   "右侧出现 key/value 表格（id 列 + Value 展开）",
                "vlm_corruption_evident": "至少一张图能看到 priority 是字符串引号或 dueAt 是 'Infinity' 字符串等异常值",
                "vlm_after_glitch_gone":  "after 截图里 hot 列表 5 行、表格无粉底色、无 'Invalid Date' 文本",
            }
            try:
                vlm = vlm_score_rubric(imgs[:4], rubric, instruction="评估 IndexedDB 损坏诊断与修复 GUI 取证截图。")
                for k in rubric: s[k] = float(vlm.get(k, 0.0))
                vlm_min = min(s[k] for k in rubric)
                s["judge_method"] = vlm.get("judge_method", "ok")
            except Exception:
                pass

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums) / len(nums) if nums else 0.0

    has_cli_evidence = (s["dump_before_shape"] + s["dump_after_shape"] +
                        s["repair_log_ok"] + s["corruption_report_schema"]) >= 2.5
    has_gui_shot = s["gui_screenshots_count"] >= 0.5
    if not has_cli_evidence:           base = min(base, 0.4)
    # GUI-path scoring axis removed: missing screenshots already cost
    # gui_screenshots_count / gui_screenshots_ocr / 4 vlm_* sub-scores.
    if vlm_score_rubric and vlm_min < 0.6: base = min(base, 0.6)
    if s["fixture_sources_unchanged"] < 1.0: base = min(base, 0.5)
    if (s["after_priorities_int"] + s["after_no_dangling_project"] +
        s["after_due_at_numeric"]) < 2.0:
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
