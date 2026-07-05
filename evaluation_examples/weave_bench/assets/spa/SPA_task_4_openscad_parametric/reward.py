# Auto-generated from WeaveBench task SPA_task_4_openscad_parametric.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """OpenSCAD parametric CAD constraint-fix grader; empty workspace -> 0.000."""
    import json, re
    from pathlib import Path
    try:
        from PIL import Image
    except ImportError:
        Image = None
    try:
        import pytesseract
    except ImportError:
        pytesseract = None
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    def _load_json(p):
        try:
            return json.loads(p.read_text())
        except Exception:
            return None

    # 1. v1 outputs
    s["v1_stl"] = 1.0 if (rd / "bracket_v1.stl").exists() else 0.0
    s["v1_png"] = 1.0 if (rd / "bracket_v1.png").exists() else 0.0
    s["render_log_v1"] = 1.0 if (rd / "render_log_v1.txt").exists() else 0.0

    # 2. stl_check_v1.json
    p = rd / "stl_check_v1.json"
    ck1 = _load_json(p) if p.exists() else None
    if isinstance(ck1, dict):
        needed = ["num_facets", "volume", "is_manifold"]
        s["stl_v1_schema"] = 1.0 if all(k in ck1 for k in needed) else 0.5
    else:
        s["stl_v1_schema"] = 0.0

    # 6. scad_params.txt
    p = rd / "scad_params.txt"
    if p.exists() and len(p.read_text(errors="ignore").strip().splitlines()) >= 3:
        s["scad_params"] = 1.0
    else:
        s["scad_params"] = 0.0

    # 7. bracket_fixed.scad — dims unchanged
    fixed_scad = workspace / "bracket_fixed.scad"
    if not fixed_scad.exists():
        fixed_scad = rd / "bracket_fixed.scad"
    if fixed_scad.exists():
        s["fixed_scad_exists"] = 1.0
        orig = workspace / "bracket.scad"
        if orig.exists():
            ot = orig.read_text(errors="ignore")
            ft = fixed_scad.read_text(errors="ignore")
            dims_ok = True
            for dim in ["width", "depth", "height"]:
                om = re.search(rf"^\s*{dim}\s*=\s*([\d.]+)", ot, re.M)
                fm = re.search(rf"^\s*{dim}\s*=\s*([\d.]+)", ft, re.M)
                if om and fm and om.group(1) != fm.group(1):
                    dims_ok = False
            s["dims_unchanged"] = 1.0 if dims_ok else 0.0
        else:
            s["dims_unchanged"] = 0.5
        s["fixed_scad_changed"] = 1.0 if (orig.exists() and orig.read_text(errors="ignore") != fixed_scad.read_text(errors="ignore")) else 0.0
    else:
        s["fixed_scad_exists"] = 0.0
        s["dims_unchanged"] = 0.0
        s["fixed_scad_changed"] = 0.0

    # 8. param_changes.json
    p = rd / "param_changes.json"
    pc = _load_json(p) if p.exists() else None
    if isinstance(pc, dict):
        ch = pc.get("changes", [])
        if isinstance(ch, list) and len(ch) >= 1:
            fields_ok = all(
                isinstance(c, dict)
                and all(k in c for k in ("param", "old", "new", "reason"))
                for c in ch
            )
            s["param_changes"] = 1.0 if fields_ok else 0.5
            # cross-check changed params against gt/expected.json known_issues set
            gt_exp = _load_json(workspace.parent / "gt" / "expected.json")
            if not isinstance(gt_exp, dict):
                gt_exp = _load_json(workspace / "gt" / "expected.json")
            if isinstance(gt_exp, dict):
                ki = {x.get("param") for x in gt_exp.get("known_issues", []) if isinstance(x, dict)}
                if ki:
                    changed_params = {c.get("param") for c in ch if isinstance(c, dict)}
                    hit = len(changed_params & ki)
                    if hit == len(ki):
                        s["param_changes_match_gt"] = 1.0
                    elif hit > 0:
                        s["param_changes_match_gt"] = 0.5 * (hit / len(ki))
                    else:
                        s["param_changes_match_gt"] = 0.0
                else:
                    s["param_changes_match_gt"] = 0.0
            else:
                s["param_changes_match_gt"] = 0.0
        else:
            s["param_changes"] = 0.0
            s["param_changes_match_gt"] = 0.0
    else:
        s["param_changes"] = 0.0
        s["param_changes_match_gt"] = 0.0

    # 10. v2 outputs + no warnings
    s["v2_stl"] = 1.0 if (rd / "bracket_v2.stl").exists() else 0.0
    s["v2_png"] = 1.0 if (rd / "bracket_v2.png").exists() else 0.0
    s["admesh_v1_txt"] = 1.0 if (rd / "admesh_v1.txt").exists() else 0.0
    s["admesh_v2_txt"] = 1.0 if (rd / "admesh_v2.txt").exists() else 0.0
    p = rd / "render_log_v2.txt"
    if p.exists():
        log = p.read_text(errors="ignore").lower()
        s["v2_no_warnings"] = 1.0 if "warning" not in log else 0.3
    else:
        s["v2_no_warnings"] = 0.0

    # 12. stl_check_v2.json — degenerate=0 + manifold=true
    p = rd / "stl_check_v2.json"
    ck2 = _load_json(p) if p.exists() else None
    if isinstance(ck2, dict):
        deg_ok = (ck2.get("num_degenerate", 1) == 0)
        mani_ok = (ck2.get("is_manifold", False) is True)
        s["v2_quality"] = 1.0 if (deg_ok and mani_ok) else 0.5
    else:
        s["v2_quality"] = 0.0

    # 13. comparison_report.md
    p = rd / "comparison_report.md"
    if p.exists():
        txt = p.read_text(errors="ignore")
        s["comparison_report"] = min(1.0, len(txt) / 100.0)
    else:
        s["comparison_report"] = 0.0

    # 14. cross_section.png
    s["cross_section"] = 1.0 if (rd / "cross_section.png").exists() else 0.0

    # 3,4,5,9,11(x2). GUI screenshots + OCR
    shots = {
        "view_01_initial_preview.png":["OpenSCAD", "Preview", "Render", "Editor", "Console"],
        "view_02_side.png":           ["OpenSCAD", "View", "Editor", "Console", "Customizer"],
        "view_03_thrown_together.png":["OpenSCAD", "Thrown", "View", "Render", "Editor"],
        "view_04_quick_check.png":    ["OpenSCAD", "Preview", "Render", "Editor", "Console"],
        "view_05_fixed_side.png":     ["OpenSCAD", "View", "Editor", "Console", "Customizer"],
        "view_06_fixed_thrown.png":   ["OpenSCAD", "Thrown", "View", "Render", "Editor"],
        "view_07_full_render.png":    ["OpenSCAD", "Render", "Console", "facets", "Top level"],
    }
    gui_present = 0
    gui_ocr_hits = 0
    MIN_SHOT_BYTES = 5 * 1024
    for fname, kws in shots.items():
        fp = rd / fname
        if fp.exists() and fp.stat().st_size > MIN_SHOT_BYTES:
            gui_present += 1
            if pytesseract and Image:
                try:
                    tx = pytesseract.image_to_string(Image.open(fp))
                    if any(k.lower() in tx.lower() for k in kws):
                        gui_ocr_hits += 1
                except Exception:
                    pass
    s["gui_screenshots_count"] = gui_present / len(shots)
    s["gui_ocr_openscad"] = (gui_ocr_hits / len(shots)) if (pytesseract and Image) else 0.0

    # 15. VLM rubric (4 items)
    vlm_keys = ["vlm_openscad_ui", "vlm_3d_model", "vlm_thrown_together", "vlm_fix_evidence"]
    if vlm_score_rubric:
        sample = [str(rd / n) for n in shots if (rd / n).exists()][:4]
        if sample:
            rubric = {
                "vlm_openscad_ui":      "截图清晰显示 OpenSCAD 界面（3D 视口 + 代码编辑器面板）",
                "vlm_3d_model":         "截图中可见三维实体模型（壁架 / 支架结构）",
                "vlm_thrown_together":  "至少一张截图为 Thrown Together 模式（多色半透明面片可见）",
                "vlm_fix_evidence":     "view_03 与 view_06 / view_02 与 view_05 之间存在可见差异（修复方向正确）",
            }
            try:
                vlm = vlm_score_rubric(sample, rubric,
                                       instruction="评估 OpenSCAD 参数化 CAD 设计迭代截图。")
            except Exception:
                vlm = {}
            for k in vlm_keys:
                s[k] = float(vlm.get(k, 0.0) or 0.0)
        else:
            for k in vlm_keys:
                s[k] = 0.0
    else:
        for k in vlm_keys:
            s[k] = 0.0

    # === GUI hard-gate sub-scores (real GUI interaction vs CLI-only headless) ===
    import hashlib
    shot_paths = [rd / n for n in shots.keys()]
    existing_shots = [p for p in shot_paths if p.exists() and p.stat().st_size > MIN_SHOT_BYTES]
    if existing_shots:
        hashes = set()
        for p in existing_shots:
            try:
                hashes.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception:
                pass
        gui_diversity = len(hashes) / max(1, len(shot_paths))
    else:
        gui_diversity = 0.0
    s["gui_real_interaction"] = 1.0 if gui_diversity >= 0.8 else (0.5 if gui_diversity >= 0.5 else 0.0)

    # gui_chrome_ocr: each screenshot must hit ≥ 2 distinct OpenSCAD app-chrome keywords
    chrome_kws = ["OpenSCAD", "Customizer", "Console", "Preview", "Render",
                  "Editor", "Thrown Together", "View"]
    chrome_hits = 0
    if pytesseract and Image:
        for p in existing_shots:
            try:
                tx = pytesseract.image_to_string(Image.open(p)).lower()
                if sum(1 for k in chrome_kws if k.lower() in tx) >= 2:
                    chrome_hits += 1
            except Exception:
                pass
        s["gui_chrome_ocr"] = chrome_hits / max(1, len(shot_paths))
    else:
        s["gui_chrome_ocr"] = 0.0

    # gui_window_geometry: screenshots match real desktop resolution (≥ 1920×1000)
    geo_ok = 0
    if Image:
        for p in existing_shots:
            try:
                with Image.open(p) as im:
                    w, h = im.size
                    if w >= 1920 and h >= 1000:
                        geo_ok += 1
            except Exception:
                pass
        s["gui_window_geometry"] = geo_ok / max(1, len(shot_paths))
    else:
        s["gui_window_geometry"] = 0.0

    # ---- Aggregate (weighted: core 60% / gui 30% / aux 10%) ----
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    if not any(v > 0 for v in nums):
        s["overall_score"] = 0.000
        return s

    core_keys = ["v1_stl", "v2_stl", "v2_quality", "stl_v1_schema",
                 "fixed_scad_exists", "fixed_scad_changed", "dims_unchanged",
                 "param_changes", "param_changes_match_gt", "v2_no_warnings",
                 "comparison_report"]
    gui_keys  = ["gui_screenshots_count", "gui_ocr_openscad",
                 "gui_real_interaction", "gui_chrome_ocr", "gui_window_geometry",
                 "vlm_openscad_ui", "vlm_3d_model", "vlm_thrown_together",
                 "vlm_fix_evidence"]
    aux_keys  = ["v1_png", "v2_png", "render_log_v1", "scad_params",
                 "admesh_v1_txt", "admesh_v2_txt", "cross_section"]
    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return (sum(vals) / len(vals)) if vals else 0.0
    core = _avg(core_keys)
    gui  = _avg(gui_keys)
    aux  = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    has_cli = (s.get("v1_stl", 0) > 0) and (s.get("stl_v1_schema", 0) > 0)
    has_gui = s.get("gui_screenshots_count", 0) >= 0.4
    if not has_cli:
        base = min(base, 0.4)
    if not has_gui:
        base = min(base, 0.35)
    if s.get("v2_stl", 0) == 0:
        base = min(base, 0.5)
    if s.get("v2_quality", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("param_changes", 0) == 0:
        base = min(base, 0.5)
    if s.get("param_changes_match_gt", 0) < 1.0:
        base = min(base, 0.6)
    # GUI hard gates: tightened — CLI-only / headless openscad solutions capped low
    if s.get("gui_real_interaction", 0) < 0.6:
        base = min(base, 0.4)
    if s.get("gui_chrome_ocr", 0) < 0.5:
        base = min(base, 0.4)
    if s.get("gui_window_geometry", 0) < 0.5:
        base = min(base, 0.45)
    # VLM unavailable degradation cap (cannot be full-score without VLM rubric pass)
    vlm_avg = sum(s.get(k, 0.0) for k in vlm_keys) / max(1, len(vlm_keys))
    if vlm_avg <= 0.0:
        base = min(base, 0.6)
    elif vlm_avg < 0.5:
        base = min(base, 0.7)
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
