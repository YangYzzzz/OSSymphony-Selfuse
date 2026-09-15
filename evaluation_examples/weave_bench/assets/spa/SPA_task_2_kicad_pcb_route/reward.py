# Auto-generated from WeaveBench task SPA_task_2_kicad_pcb_route.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """KiCad PCB routing/DRC/3D/gerber grader; empty workspace -> 0.000."""
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

    # 1. drc_before.json (any valid JSON with unconnected hint)
    p = rd / "drc_before.json"
    if p.exists():
        try:
            json.loads(p.read_text())
            s["drc_before"] = 1.0
        except Exception:
            s["drc_before"] = 0.3
    else:
        s["drc_before"] = 0.0

    # 2. ratsnest_count.txt
    p = rd / "ratsnest_count.txt"
    if p.exists():
        m = re.search(r"\d+", p.read_text(errors="ignore"))
        s["ratsnest_count"] = 1.0 if (m and int(m.group()) > 0) else 0.3
    else:
        s["ratsnest_count"] = 0.0

    # 4. bom.csv
    p = rd / "bom.csv"
    if p.exists() and len(p.read_text(errors="ignore").strip().splitlines()) >= 2:
        s["bom_csv"] = 1.0
    else:
        s["bom_csv"] = 0.0

    # 6. drc_before_summary.txt
    p = rd / "drc_before_summary.txt"
    s["drc_summary"] = 1.0 if (p.exists() and len(p.read_text(errors="ignore").strip()) > 5) else 0.0

    # 8. drc_after.json: unconnected = 0
    p = rd / "drc_after.json"
    if p.exists():
        try:
            d = json.loads(p.read_text())
            uncon_zero = (
                d.get("unconnected") == 0 or
                (isinstance(d.get("unconnected_items"), list)
                 and len(d["unconnected_items"]) == 0)
            )
            s["drc_after_clean"] = 1.0 if uncon_zero else 0.4
        except Exception:
            s["drc_after_clean"] = 0.2
    else:
        s["drc_after_clean"] = 0.0

    # 3,5,7,9,11(top+bot),14. GUI screenshots + OCR
    shots = {
        "view_01_ratsnest.png":     ["KiCad", "Layer", "Pcb", "Board"],
        "view_02_board_setup.png":  ["Design Rules", "Clearance", "Track", "Width", "Via"],
        "view_03_routing.png":      ["KiCad", "Track", "Route", "Layer", "Net"],
        "view_04_drc_dialog.png":   ["DRC", "Violation", "Unconnected", "Error", "Warning"],
        "view_05_3d_top.png":       ["3D", "Viewer", "KiCad", "Top", "Board"],
        "view_06_3d_bottom.png":    ["3D", "Viewer", "Bottom", "Board", "KiCad"],
        "view_07_net_inspector.png":["Net", "Length", "Inspector", "Pad", "Class"],
        "view_08_3d_orbit_animation.png":     ["3D", "Viewer", "View", "Render", "Preferences"],
        "view_09_pcbnew_and_eeschema.png":    ["pcbnew", "Schematic", "eeschema", "+3V3", "GND", "KiCad"],
        "view_10_drc_dialog_running.png":     ["DRC", "Checking", "Refilling", "Run", "Violation"],
        "view_11_layer_visibility_toggled.png":["F.Cu", "Layer", "B.Cu", "In1.Cu", "Manager"],
    }
    gui_present = 0
    gui_ocr_hits = 0
    for fname, kws in shots.items():
        fp = rd / fname
        # tighter min size: <5KB treated as placeholder
        if fp.exists() and fp.stat().st_size > 5 * 1024:
            gui_present += 1
            if pytesseract and Image:
                try:
                    tx = pytesseract.image_to_string(Image.open(fp))
                    if any(k.lower() in tx.lower() for k in kws):
                        gui_ocr_hits += 1
                except Exception:
                    pass
    s["gui_screenshots_count"] = gui_present / len(shots)
    s["gui_screenshots_ocr"] = (gui_ocr_hits / len(shots)) if (pytesseract and Image) else 0.0

    # 10. Gerber + drill
    gdir = rd / "gerbers"
    if gdir.exists():
        gbr = list(gdir.glob("*.gbr")) + list(gdir.glob("*.g[lt][s12]")) + list(gdir.glob("*.gm1"))
        drl = list(gdir.glob("*.drl")) + list(gdir.glob("*.xln"))
        s["gerber_count"] = 1.0 if len(gbr) >= 5 else len(gbr) / 5.0
        s["drill_exists"] = 1.0 if len(drl) >= 1 else 0.0
    else:
        s["gerber_count"] = 0.0
        s["drill_exists"] = 0.0

    # 12. SVG exports
    svg_top = rd / "pcb_top.svg"
    svg_bot = rd / "pcb_bottom.svg"
    ok = sum(1 for sv in (svg_top, svg_bot) if sv.exists() and sv.stat().st_size > 500)
    s["svg_exports"] = ok / 2.0

    # 13. drc_comparison.json
    p = rd / "drc_comparison.json"
    if p.exists():
        try:
            d = json.loads(p.read_text())
            checks = [
                isinstance(d.get("before"), dict),
                isinstance(d.get("after"), dict),
                isinstance(d.get("improvement"), dict),
                isinstance(d.get("gerber_files"), list),
                isinstance(d.get("drill_files"), list),
                isinstance(d.get("after", {}).get("unconnected"), int),
            ]
            s["drc_comparison"] = sum(checks) / len(checks)
        except Exception:
            s["drc_comparison"] = 0.0
    else:
        s["drc_comparison"] = 0.0

    # 15. export_count.txt
    s["export_count"] = 1.0 if (rd / "export_count.txt").exists() else 0.0

    # 16. VLM rubric (4 items)
    vlm_keys = ["vlm_kicad_real", "vlm_traces_visible", "vlm_3d_render", "vlm_drc_dialog"]
    if vlm_score_rubric:
        sample = [str(rd / n) for n in shots if (rd / n).exists()][:4]
        if sample:
            rubric = {
                "vlm_kicad_real":     "截图清晰显示 KiCad PCB Editor / 3D Viewer 界面",
                "vlm_traces_visible": "PCB 上可见铜走线（明显的彩色线段连接焊盘）",
                "vlm_3d_render":      "3D Viewer 显示了 PCB 板卡的三维渲染（含元件、焊盘、丝印）",
                "vlm_drc_dialog":     "DRC 对话框显示检查结果（Violations / Unconnected items 等）",
            }
            try:
                vlm = vlm_score_rubric(sample, rubric,
                                       instruction="评估 KiCad PCB 走线与 DRC 验证任务的 GUI 截图。")
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

    # === GUI hard-gate sub-scores (real GUI interaction vs CLI-only) ===
    import hashlib
    shot_paths = [rd / n for n in shots.keys()]
    existing_shots = [p for p in shot_paths if p.exists() and p.stat().st_size > 5 * 1024]
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
    s["gui_diversity"] = gui_diversity

    # gui_chrome_ocr: each screenshot must hit ≥ 2 distinct KiCad app-chrome keywords
    chrome_kws = ["KiCad", "PCB Editor", "Layers", "Tracks", "Footprint",
                  "DRC", "Pcbnew", "3D Viewer"]
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

    # === gui_real_interaction: combined diversity + geometry + chrome_ocr ===
    # md5-only diversity is cheatable; require ALL three signals.
    div = s.get("gui_diversity", 0.0)
    geo = s.get("gui_window_geometry", 0.0)
    chrome = s.get("gui_chrome_ocr", 0.0)
    if div >= 0.85 and geo >= 0.6 and chrome >= 0.5:
        s["gui_real_interaction"] = 1.0
    elif div >= 0.7 and geo >= 0.4 and chrome >= 0.3:
        s["gui_real_interaction"] = 0.6
    elif div >= 0.5:
        s["gui_real_interaction"] = 0.3
    else:
        s["gui_real_interaction"] = 0.0

    # ---- Aggregate (weighted: core 60% / gui 30% / aux 10%) ----
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    if not any(v > 0 for v in nums):
        s["overall_score"] = 0.000
        return s

    def _avg(keys):
        vs = [s.get(k, 0.0) for k in keys if isinstance(s.get(k, 0.0), (int, float))]
        return sum(vs) / max(1, len(vs))

    core_keys = ["drc_before", "ratsnest_count", "bom_csv", "drc_summary",
                 "drc_after_clean", "gerber_count", "drill_exists",
                 "svg_exports", "drc_comparison", "export_count"]
    gui_keys = ["gui_screenshots_count", "gui_screenshots_ocr",
                "gui_real_interaction", "gui_chrome_ocr", "gui_window_geometry"]
    aux_keys = vlm_keys
    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # ---- Hard gates (tightened) ----
    if s.get("gui_screenshots_count", 0) < 0.5:
        base = min(base, 0.4)
    if s.get("drc_before", 0) == 0:
        base = min(base, 0.4)
    if s.get("drc_after_clean", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("drc_after_clean", 0) == 0:
        base = min(base, 0.4)
    if s.get("gerber_count", 0) < 0.6:
        base = min(base, 0.5)
    if s.get("drill_exists", 0) == 0:
        base = min(base, 0.5)
    if s.get("drc_comparison", 0) < 0.5:
        base = min(base, 0.5)
    # GUI hard gates: tightened thresholds; CLI-only solutions capped low.
    if s.get("gui_real_interaction", 0) < 0.6:
        base = min(base, 0.4)
    if s.get("gui_chrome_ocr", 0) < 0.5:
        base = min(base, 0.4)
    if s.get("gui_window_geometry", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("gui_screenshots_ocr", 0) < 0.4:
        base = min(base, 0.5)
    # VLM unavailable: cap at 0.6 so headless / no-VLM cannot full-score.
    if not vlm_score_rubric or all(s.get(k, 0.0) == 0.0 for k in vlm_keys):
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
