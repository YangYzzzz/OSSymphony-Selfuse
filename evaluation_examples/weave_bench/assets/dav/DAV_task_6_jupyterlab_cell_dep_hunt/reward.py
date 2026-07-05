# Auto-generated from WeaveBench task DAV_task_6_jupyterlab_cell_dep_hunt.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import csv, json, re
from pathlib import Path

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-dim grader for JupyterLab cell dependency hunt task."""
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    nb_dir = workspace / "notebook"
    gt_dir = workspace / "gt"
    s = {}

    gt = {}
    if (gt_dir / "expected.json").exists():
        try:
            gt = json.loads((gt_dir / "expected.json").read_text())
        except Exception:
            gt = {}

    # 1. nbconvert_failure.log
    fl = rd / "nbconvert_failure.log"
    if fl.exists():
        t = fl.read_text(errors="ignore").lower()
        hits = sum(1 for kw in ["error", "traceback", "nameerror"] if kw in t)
        s["nbconvert_failure"] = min(1.0, hits / 2.0)
    else:
        s["nbconvert_failure"] = 0.0

    # 2. cell_meta.tsv
    cm = rd / "cell_meta.tsv"
    if cm.exists():
        try:
            txt = cm.read_text(errors="ignore")
            lines = [l for l in txt.splitlines() if l.strip()]
            need = {"cell_index", "execution_count", "source_first_line", "has_output"}
            header = lines[0].split("\t") if lines else []
            schema_ok = need.issubset(set(header))
            s["cell_meta_present"] = 1.0
            s["cell_meta_schema"] = 1.0 if schema_ok else 0.0
            s["cell_meta_rows"] = min(1.0, max(0, len(lines) - 1) / 5.0)
        except Exception:
            s["cell_meta_present"] = 0.0
            s["cell_meta_schema"] = 0.0
            s["cell_meta_rows"] = 0.0
    else:
        s["cell_meta_present"] = 0.0
        s["cell_meta_schema"] = 0.0
        s["cell_meta_rows"] = 0.0

    # 3. orphan_candidates.json
    oc = rd / "orphan_candidates.json"
    orphan_list = []
    if oc.exists():
        try:
            d = json.loads(oc.read_text())
            orphan_list = d.get("orphans", [])
            non_empty = isinstance(orphan_list, list) and orphan_list and all(
                isinstance(x, str) and x.strip() for x in orphan_list
            )
            s["orphan_candidates"] = 1.0 if non_empty else 0.0
            # NEW: ≥ 3 distinct orphans (multi-orphan finding)
            distinct = len({x.strip() for x in orphan_list if isinstance(x, str)})
            s["orphan_count_ge3"] = 1.0 if distinct >= 3 else 0.0
        except Exception:
            s["orphan_candidates"] = 0.0
            s["orphan_count_ge3"] = 0.0
    else:
        s["orphan_candidates"] = 0.0
        s["orphan_count_ge3"] = 0.0

    # 3b. hidden_state.json (NEW): global mutations beyond orphan symbols
    hs = rd / "hidden_state.json"
    if hs.exists():
        try:
            d = json.loads(hs.read_text())
            muts = d.get("global_mutations", [])
            ok_struct = isinstance(muts, list) and len(muts) >= 1 and all(
                isinstance(m, dict) and m.get("target", "").strip()
                and m.get("evidence", "").strip()
                and m.get("fix_action", "").strip()
                for m in muts
            )
            s["hidden_state_present"] = 1.0 if ok_struct else 0.0
            # Target should reference a real global (pd./plt./np./matplotlib/rcParams/options/seed/etc),
            # and must NOT just repeat an orphan symbol.
            orph_set = {x.strip() for x in orphan_list if isinstance(x, str)}
            global_kw = ("pd.", "plt.", "np.", "matplotlib", "rcparams", "options", "random.seed", "set_option")
            target_quality = 0.0
            if ok_struct:
                tgt = muts[0].get("target", "").lower()
                if any(k in tgt for k in global_kw) and muts[0].get("target") not in orph_set:
                    target_quality = 1.0
            s["hidden_state_target_real"] = target_quality
        except Exception:
            s["hidden_state_present"] = 0.0
            s["hidden_state_target_real"] = 0.0
    else:
        s["hidden_state_present"] = 0.0
        s["hidden_state_target_real"] = 0.0

    # 4-6, 11-12. GUI screenshots — anti-cheat: size>=5KB, md5 uniqueness, OCR keyword hit
    import hashlib
    gui_shots = {
        "view_lab_open.png": ["analysis", "ipynb", "lab"],
        "view_exec_gutter.png": ["[", "]", "1", "2"],
        "view_var_inspector.png": ["variable", "inspector", "name", "type"],
        "view_var_after_fix.png": ["variable", "inspector", "discount", "table"],
        "view_run_all.png": ["1", "2", "3"],
        "view_hover_tooltip.png": [],
    }
    gui_present = 0
    gui_ocr_hits = 0
    ocr_total = 0
    md5_set = set()
    for fname, kws in gui_shots.items():
        p = rd / fname
        # Anti-cheat: require >= 5KB to count as a real screenshot (placeholder ~ <2KB)
        if p.exists() and p.stat().st_size >= 5000:
            gui_present += 1
            try:
                md5_set.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception:
                pass
        if kws:
            ocr_total += 1
            if p.exists():
                try:
                    import pytesseract
                    from PIL import Image
                    tx = pytesseract.image_to_string(Image.open(p)).lower()
                    if any(k.lower() in tx for k in kws):
                        gui_ocr_hits += 1
                except Exception:
                    gui_ocr_hits += 0.5
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    s["gui_screenshots_ocr"] = gui_ocr_hits / ocr_total if ocr_total else 0.0
    # Anti-cheat: distinct md5 / present count, penalize duplicate screenshots
    s["gui_screenshots_md5_unique"] = (len(md5_set) / gui_present) if gui_present else 0.0

    # 7. kernel_probe.json
    kp = rd / "kernel_probe.json"
    if kp.exists():
        try:
            d = json.loads(kp.read_text())
            mr = d.get("missing_referenced", [])
            valid = isinstance(mr, list) and mr and all(
                isinstance(x, str) and x.strip() for x in mr
            )
            overlap = bool(set(mr) & set(orphan_list)) if orphan_list else False
            s["kernel_probe_present"] = 1.0 if valid else 0.0
            s["kernel_probe_overlap"] = 1.0 if overlap else 0.0
        except Exception:
            s["kernel_probe_present"] = 0.0
            s["kernel_probe_overlap"] = 0.0
    else:
        s["kernel_probe_present"] = 0.0
        s["kernel_probe_overlap"] = 0.0

    # 8. analysis_fixed.ipynb
    orig_nb = nb_dir / "analysis.ipynb"
    fixed_nb = nb_dir / "analysis_fixed.ipynb"
    if fixed_nb.exists():
        try:
            f = json.loads(fixed_nb.read_text())
            o = json.loads(orig_nb.read_text()) if orig_nb.exists() else {"cells": []}
            f_cells = f.get("cells", [])
            o_cells = o.get("cells", [])
            s["fixed_nb_present"] = 1.0
            s["fixed_nb_size"] = 1.0 if len(f_cells) >= len(o_cells) else 0.5
        except Exception:
            s["fixed_nb_present"] = 0.0
            s["fixed_nb_size"] = 0.0
    else:
        s["fixed_nb_present"] = 0.0
        s["fixed_nb_size"] = 0.0

    # 9. nbconvert_success.log
    sl = rd / "nbconvert_success.log"
    if sl.exists():
        t = sl.read_text(errors="ignore")
        clean = ("Traceback" not in t) and ("NameError" not in t)
        s["nbconvert_success"] = 1.0 if clean else 0.0
    else:
        s["nbconvert_success"] = 0.0

    # Also check the produced fixed_run notebook itself for ascending exec counts + image
    fixed_run = nb_dir / "analysis_fixed_run.ipynb"
    s["exec_counts_ascending"] = 0.0
    s["has_image_output"] = 0.0
    if fixed_run.exists():
        try:
            d = json.loads(fixed_run.read_text())
            cells = d.get("cells", [])
            ec = [c.get("execution_count") for c in cells
                  if c.get("cell_type") == "code"
                  and c.get("execution_count") is not None]
            if ec and ec == sorted(ec) and ec[0] == 1 and len(ec) == len(set(ec)):
                s["exec_counts_ascending"] = 1.0
            elif ec and ec == sorted(ec):
                s["exec_counts_ascending"] = 0.5
            for c in cells:
                for out in c.get("outputs", []):
                    data = out.get("data", {})
                    if "image/png" in data or "image/jpeg" in data:
                        s["has_image_output"] = 1.0
                        break
                if s["has_image_output"]:
                    break
        except Exception:
            pass

    # 10. validate.py + validate.log
    vp = rd / "validate.py"
    vl = rd / "validate.log"
    s["validate_script"] = 1.0 if vp.exists() and vp.stat().st_size > 100 else 0.0
    if vl.exists():
        t = vl.read_text(errors="ignore").upper()
        s["validate_pass"] = 1.0 if "PASS" in t and "FAIL" not in t.replace("PASSFAIL", "") else (
            0.5 if "PASS" in t else 0.0
        )
    else:
        s["validate_pass"] = 0.0

    # 10b. analysis_fixed.html (NEW): nbconvert --to html --execute output
    html = rd / "analysis_fixed.html"
    if html.exists():
        try:
            t = html.read_text(errors="ignore", encoding="utf-8")
            size_ok = html.stat().st_size >= 8000
            has_img = "<img" in t.lower()
            has_kw = "per-region" in t.lower() or "monthly" in t.lower()
            s["html_export_present"] = 1.0 if size_ok else 0.5
            s["html_has_figure"] = 1.0 if has_img else 0.0
            s["html_has_content_kw"] = 1.0 if has_kw else 0.0
        except Exception:
            s["html_export_present"] = 0.0
            s["html_has_figure"] = 0.0
            s["html_has_content_kw"] = 0.0
    else:
        s["html_export_present"] = 0.0
        s["html_has_figure"] = 0.0
        s["html_has_content_kw"] = 0.0

    # 10c. test_fixed_notebook.py + pytest_outputs.json (NEW)
    tpy = rd / "test_fixed_notebook.py"
    tjs = rd / "pytest_outputs.json"
    if tpy.exists():
        try:
            txt = tpy.read_text(errors="ignore")
            n_def = len(re.findall(r"^\s*def\s+test_\w+", txt, re.M))
            s["pytest_script_present"] = 1.0 if tpy.stat().st_size > 200 else 0.5
            s["pytest_has_4plus_tests"] = 1.0 if n_def >= 4 else (0.5 if n_def >= 2 else 0.0)
        except Exception:
            s["pytest_script_present"] = 0.0
            s["pytest_has_4plus_tests"] = 0.0
    else:
        s["pytest_script_present"] = 0.0
        s["pytest_has_4plus_tests"] = 0.0
    if tjs.exists():
        try:
            d = json.loads(tjs.read_text())
            passed = int(d.get("passed", 0))
            failed = int(d.get("failed", 0))
            s["pytest_results_pass"] = 1.0 if (passed >= 4 and failed == 0) else (
                0.5 if (passed >= 2 and failed == 0) else 0.0
            )
        except Exception:
            s["pytest_results_pass"] = 0.0
    else:
        s["pytest_results_pass"] = 0.0

    # 12. tooltip_samples.json
    ts = rd / "tooltip_samples.json"
    if ts.exists():
        try:
            d = json.loads(ts.read_text())
            items = d.get("hover_samples", [])
            valid = (
                isinstance(items, list) and len(items) >= 1
                and all(
                    isinstance(i, dict)
                    and isinstance(i.get("symbol"), str) and i["symbol"].strip()
                    and isinstance(i.get("hint_text"), str) and i["hint_text"].strip()
                    for i in items
                )
            )
            s["tooltip_structure"] = 1.0 if valid else 0.0
        except Exception:
            s["tooltip_structure"] = 0.0
    else:
        s["tooltip_structure"] = 0.0

    # 13. dependency_report.json
    dr = rd / "dependency_report.json"
    if dr.exists():
        try:
            d = json.loads(dr.read_text())
            ooo = d.get("out_of_order_cells", [])
            orph = d.get("orphan_symbols", [])
            fix = d.get("fix_summary", "")
            s["dep_report_ooo"] = 1.0 if isinstance(ooo, list) and len(ooo) >= 3 else (
                0.5 if isinstance(ooo, list) and len(ooo) >= 1 else 0.0
            )
            s["dep_report_orphan"] = 1.0 if isinstance(orph, list) and orph else 0.0
            s["dep_report_fix"] = 1.0 if isinstance(fix, str) and len(fix) >= 50 else 0.0
        except Exception:
            s["dep_report_ooo"] = 0.0
            s["dep_report_orphan"] = 0.0
            s["dep_report_fix"] = 0.0
    else:
        s["dep_report_ooo"] = 0.0
        s["dep_report_orphan"] = 0.0
        s["dep_report_fix"] = 0.0

    # 14. summary.md
    sm = rd / "summary.md"
    if sm.exists():
        c = sm.read_text(errors="ignore")
        kw = bool(re.search(r"execution\s+order|hidden\s+state", c, re.I))
        has_table = c.count("|") >= 6
        suggestion_lines = [l for l in c.splitlines() if len(l.strip()) >= 30]
        s["summary_keyword"] = 1.0 if kw else 0.0
        s["summary_table"] = 1.0 if has_table else 0.0
        s["summary_suggestions"] = min(1.0, len(suggestion_lines) / 5.0)
    else:
        s["summary_keyword"] = 0.0
        s["summary_table"] = 0.0
        s["summary_suggestions"] = 0.0

    # VLM rubric
    vlm_used = False
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    if vlm_score_rubric:
        imgs = [str(rd / n) for n in gui_shots if (rd / n).exists()]
        if imgs:
            rubric = {
                "vlm_lab_real": "看起来是真的 JupyterLab UI 而不是空白页",
                "vlm_exec_numbers": "截图里能看到 cell 左侧的执行序号 [N]:",
                "vlm_var_inspector": "Variable Inspector 面板可见且不是空白",
                "vlm_layout_clean": "截图布局整齐没有截断或重叠",
            }
            try:
                vlm = vlm_score_rubric(
                    imgs[:4], rubric,
                    instruction="评估 JupyterLab cell-dependency 调试任务截图质量。"
                )
                for k in rubric:
                    s[k] = float(vlm.get(k, 0.0))
                vlm_used = True
            except Exception:
                for k in rubric:
                    s[k] = 0.0

    # Overall — weighted aggregation: core deliverables 60%, GUI evidence 30%, aux 10%
    core_keys = [
        "nbconvert_failure", "cell_meta_present", "cell_meta_schema", "cell_meta_rows",
        "orphan_candidates", "orphan_count_ge3", "hidden_state_present", "hidden_state_target_real",
        "kernel_probe_present", "kernel_probe_overlap",
        "fixed_nb_present", "fixed_nb_size", "nbconvert_success",
        "exec_counts_ascending", "has_image_output",
        "validate_script", "validate_pass",
        "html_export_present", "html_has_figure", "html_has_content_kw",
        "pytest_script_present", "pytest_has_4plus_tests", "pytest_results_pass",
        "dep_report_ooo", "dep_report_orphan", "dep_report_fix",
    ]
    gui_keys = [
        "gui_screenshots_count", "gui_screenshots_ocr", "gui_screenshots_md5_unique",
        "tooltip_structure",
        "vlm_lab_real", "vlm_exec_numbers", "vlm_var_inspector", "vlm_layout_clean",
    ]
    aux_keys = ["summary_keyword", "summary_table", "summary_suggestions"]

    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vals) / len(vals) if vals else 0.0

    base = 0.6 * _avg(core_keys) + 0.3 * _avg(gui_keys) + 0.1 * _avg(aux_keys)

    # Hard gates — tightened in v2
    if s.get("gui_screenshots_count", 0) < 0.7:
        base = min(base, 0.4)
    if s.get("gui_screenshots_md5_unique", 0) < 0.8:
        base = min(base, 0.5)
    if s.get("nbconvert_failure", 0) == 0:
        base = min(base, 0.4)
    if s.get("fixed_nb_present", 0) == 0:
        base = min(base, 0.45)
    if s.get("nbconvert_success", 0) == 0:
        base = min(base, 0.5)
    if s.get("orphan_candidates", 0) == 0:
        base = min(base, 0.5)
    if s.get("kernel_probe_overlap", 0) == 0:
        base = min(base, 0.6)
    if s.get("tooltip_structure", 0) == 0:
        base = min(base, 0.6)
    if s.get("orphan_count_ge3", 0) == 0:
        base = min(base, 0.6)
    if s.get("hidden_state_present", 0) == 0:
        base = min(base, 0.6)
    if s.get("hidden_state_target_real", 0) == 0:
        base = min(base, 0.7)
    if s.get("dep_report_ooo", 0) < 1.0:
        base = min(base, 0.75)
    if s.get("pytest_results_pass", 0) == 0:
        base = min(base, 0.7)
    if s.get("html_export_present", 0) == 0:
        base = min(base, 0.8)
    if s.get("exec_counts_ascending", 0) < 1.0:
        base = min(base, 0.8)
    # When VLM not available, cap at 0.65 to avoid free pass
    if not vlm_used:
        base = min(base, 0.65)

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
