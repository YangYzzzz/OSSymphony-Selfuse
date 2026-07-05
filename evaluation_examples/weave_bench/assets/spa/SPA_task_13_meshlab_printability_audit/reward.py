# Auto-generated from WeaveBench task SPA_task_13_meshlab_printability_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import json, re, ast
from pathlib import Path


def _safe_load_json(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return None


def _ocr(img_path):
    try:
        from PIL import Image
        import pytesseract
        return pytesseract.image_to_string(Image.open(img_path))
    except Exception:
        return ""


def grade(workspace_path=None, **kwargs):
    """SPA_task_13 grader: 13 sub-scores + 3 hard gates.

    workspace_path is the agent's /tmp_workspace (where results/ lives).
    The grader-only gt/expected.json is at /tmp_workspace/gt/expected.json
    (mounted by the harness; never visible to the agent at task time)."""
    ws = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = ws / "results"
    gt_path = ws / "gt" / "expected.json"
    gt = _safe_load_json(gt_path) or {}
    s = {}

    # 1. mesh_stats_before.json
    msb = _safe_load_json(rd / "logs" / "mesh_stats_before.json")
    if isinstance(msb, dict) and {"bracket", "knob"} <= set(msb.keys()):
        s["mesh_stats_before_schema"] = 1.0
    else:
        s["mesh_stats_before_schema"] = 0.0

    # 2. mesh_stats_after.json — bracket nm_edges == 0
    msa = _safe_load_json(rd / "logs" / "mesh_stats_after.json")
    bracket_after_nm = None
    if isinstance(msa, dict) and "bracket" in msa:
        b = msa["bracket"]
        # accept either flat or nested key
        for k in ("non_manifold_edges", "non_two_manifold_edges"):
            if k in b:
                try:
                    bracket_after_nm = int(b[k]); break
                except Exception:
                    pass
    real_nm = None
    try:
        import trimesh
        m = trimesh.load(rd/"fixed"/"bracket_fixed.stl", process=False)
        min_faces = int(gt.get("bracket_min_face_count", 410))
        want_euler = int(gt.get("bracket_expected_euler_number", 2))
        require_winding = bool(gt.get("bracket_require_winding_consistent", True))
        winding_ok = (m.is_winding_consistent if require_winding else True)
        real_nm = 0 if winding_ok and len(m.faces) >= min_faces \
                      and m.euler_number == want_euler else 1
    except Exception:
        pass
    s["bracket_repaired_nm0"] = 1.0 if (bracket_after_nm == 0 and real_nm == 0) else 0.0

    # 3. overhang_fraction.json
    of = _safe_load_json(rd / "logs" / "overhang_fraction.json")
    if isinstance(of, dict) and {"bracket", "knob"} <= set(of.keys()):
        try:
            ok = all(0.0 <= float(of[k]) <= 1.0 for k in ("bracket", "knob"))
            s["overhang_fraction_valid"] = 1.0 if ok else 0.0
        except Exception:
            s["overhang_fraction_valid"] = 0.0
    else:
        s["overhang_fraction_valid"] = 0.0

    # 4. repair.log contains expected filter names
    rl = rd / "logs" / "repair.log"
    if rl.exists():
        txt = rl.read_text(errors="ignore")
        wanted = [
            "meshing_remove_duplicate_vertices",
            "meshing_remove_duplicate_faces",
            "meshing_repair_non_manifold_edges",
            "meshing_close_holes",
        ]
        hits = sum(1 for w in wanted if w in txt) + (
            1 if ("bracket" in txt and "knob" in txt) else 0
        )
        s["repair_log_filters"] = min(1.0, hits / 5.0)
    else:
        s["repair_log_filters"] = 0.0

    # 5. components_after.json — bracket=1, knob=2
    ca = _safe_load_json(rd / "logs" / "components_after.json")
    if isinstance(ca, dict):
        try:
            try:
                import trimesh
                cb = len(trimesh.load(rd/"fixed"/"bracket_fixed.stl", process=False).split(only_watertight=False))
                ck = len(trimesh.load(rd/"fixed"/"knob_fixed.stl",    process=False).split(only_watertight=False))
                claim_ok = int(ca.get("bracket",-1))==cb and int(ca.get("knob",-1))==ck
                truth_ok = (cb == 1) and (ck == 2)
                s["components_after_correct"] = 1.0 if (claim_ok and truth_ok) else 0.0
            except Exception:
                s["components_after_correct"] = 0.0
        except Exception:
            s["components_after_correct"] = 0.0
    else:
        s["components_after_correct"] = 0.0

    # 6. self_intersect.json — knob > 0
    si = _safe_load_json(rd / "logs" / "self_intersect.json")
    if isinstance(si, dict):
        try:
            real_si = -1
            try:
                import trimesh
                km = trimesh.load(rd/"fixed"/"knob_fixed.stl", process=False)
                real_si = sum(1 for c in km.split(only_watertight=False) if not c.is_volume)
                real_si += 1 if (len(km.split(only_watertight=False)) >= 2) else 0
            except Exception:
                pass
            s["knob_self_intersect_detected"] = 1.0 if (int(si.get("knob",0)) > 0 and real_si > 0) else 0.0
        except Exception:
            s["knob_self_intersect_detected"] = 0.0
    else:
        s["knob_self_intersect_detected"] = 0.0

    # 7. fixed STL files exist with non-trivial size
    fx_b = rd / "fixed" / "bracket_fixed.stl"
    fx_k = rd / "fixed" / "knob_fixed.stl"
    s["fixed_stls_exist"] = 1.0 if (
        fx_b.exists() and fx_b.stat().st_size > 1024
        and fx_k.exists() and fx_k.stat().st_size > 1024
    ) else 0.0

    # 8. GUI screenshots — at least N exist
    shot_dir = rd / "shots"
    shots = sorted(shot_dir.glob("*.png")) if shot_dir.exists() else []
    min_shots = int(gt.get("min_screenshots", 4))
    s["screenshots_present"] = min(1.0, len(shots) / max(1, min_shots))

    # 9. OCR — at least one MeshLab screenshot mentions Vertices or Faces
    ocr_hit = 0
    keys = gt.get("ocr_required_substrings_meshlab_panel", ["Vertices", "Faces"])
    for sh in shots[:6]:
        t = _ocr(sh)
        low = t.lower()
        if ("meshlab" in low) and any(k.lower() in low for k in keys):
            ocr_hit += 1
    s["meshlab_panel_ocr"] = 1.0 if ocr_hit >= 2 else (0.5 if ocr_hit == 1 else 0.0)

    # 10. printability_report.json decisions
    pr = _safe_load_json(rd / "printability_report.json")
    decisions_ok = 0
    if isinstance(pr, dict) and isinstance(pr.get("bracket"), dict) and isinstance(pr.get("knob"), dict):
        want = gt.get("report_decision_values", {
            "bracket": "auto_repaired", "knob": "redesign_required"
        })
        if pr["bracket"].get("decision") == want.get("bracket"):
            decisions_ok += 1
        if pr["knob"].get("decision") == want.get("knob"):
            decisions_ok += 1
    s["report_decisions_correct"] = decisions_ok / 2.0

    # 11. report markdown — >=30 lines and mentions both parts
    md = rd / "printability_report.md"
    if md.exists():
        lines = md.read_text(errors="ignore").splitlines()
        text = "\n".join(lines).lower()
        ok = (len(lines) >= 30) and ("bracket" in text) and ("knob" in text)
        s["report_md_complete"] = 1.0 if ok else 0.0
    else:
        s["report_md_complete"] = 0.0

    # 12. PDF exists and >10 KB
    pdf = rd / "printability_report.pdf"
    ok = pdf.exists() and pdf.stat().st_size > 10*1024
    if ok:
        try:
            import subprocess
            txt = subprocess.run(["pdftotext","-q",str(pdf),"-"],capture_output=True,text=True,timeout=15).stdout.lower()
            ok = ("auto_repaired" in txt) and ("redesign_required" in txt) and ("bracket" in txt) and ("knob" in txt)
        except Exception: ok = False
    s["report_pdf_exists"] = 1.0 if ok else 0.0

    # 13. forbidden imports check
    forbidden = gt.get("forbidden_imports", ["bpy"])
    bad = False
    for src in ws.rglob("*.py"):
        try:
            t = src.read_text(errors="ignore")
            for f in forbidden:
                if re.search(rf"^\s*(import\s+{re.escape(f)}|from\s+{re.escape(f)}\b)", t, re.M):
                    bad = True; break
        except Exception:
            pass
        if bad:
            break
    s["no_forbidden_imports"] = 0.0 if bad else 1.0

    # ---- Hard gates ----
    has_cli_evidence = any((rd / "logs" / n).exists() and (rd / "logs" / n).stat().st_size > 0
                           for n in ("mesh_stats_before.json", "mesh_stats_after.json", "repair.log"))
    has_gui_screenshot = len(shots) >= 1

    # VLM rubric (optional)
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    vlm_ok = 1.0
    if vlm_score_rubric and shots:
        rubric = {
            "vlm_meshlab_window_visible":  "screenshot shows the MeshLab title-bar/menu and a 3D viewport with a mesh",
            "vlm_nm_edges_highlighted":    "01_*.png shows non-manifold edges drawn in red/yellow on the bracket",
            "vlm_stats_panel_readable":    "a side panel with numeric Vertices/Faces counts is legible",
            "vlm_knob_two_shells_visible": "03_*/05_*.png shows the knob's central boss as a clearly distinct body inside the disc",
        }
        try:
            picks = [str(p) for p in shots[:3]]
            v = vlm_score_rubric(picks, rubric,
                instruction="Judge if these are real MeshLab GUI screenshots showing 3D mesh QA work.")
            for k in rubric:
                s[k] = float(v.get(k, 0.0))
            vlm_ok = sum(s[k] for k in rubric) / len(rubric)
        except Exception:
            pass

    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums) / max(1, len(nums))

    if not has_cli_evidence:
        base = min(base, 0.4)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the screenshots / vlm_* sub_scores.
    if vlm_score_rubric is not None and vlm_ok < 0.6:
        base = min(base, 0.5)

    s["overall_score"] = base
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
