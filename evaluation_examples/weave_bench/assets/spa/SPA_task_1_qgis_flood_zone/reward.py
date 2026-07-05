# Auto-generated from WeaveBench task SPA_task_1_qgis_flood_zone.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """QGIS flood-zone grader: schema/numeric/file/OCR/VLM, all empty -> 0.000."""
    import json, re, subprocess
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

    # 1. ogrinfo schema
    p = rd / "ogrinfo_schema.txt"
    if p.exists():
        txt = p.read_text(errors="ignore")
        has_fields = any(k in txt for k in ["owner", "area_m2", "land_use"])
        has_crs = "4326" in txt or "WGS 84" in txt
        s["ogrinfo_schema"] = 1.0 if (has_fields and has_crs) else 0.5
    else:
        s["ogrinfo_schema"] = 0.0

    # 3. dem_stats.txt
    p = rd / "dem_stats.txt"
    if p.exists():
        txt = p.read_text(errors="ignore")
        has_stats = sum(1 for k in ["Min", "Max", "Mean", "STATISTICS"] if k in txt) >= 2
        s["dem_stats"] = 1.0 if has_stats else 0.4
    else:
        s["dem_stats"] = 0.0

    # 5. parcels_sample.txt
    p = rd / "parcels_sample.txt"
    if p.exists() and len(p.read_text(errors="ignore").strip().splitlines()) >= 5:
        s["parcels_sample"] = 1.0
    else:
        s["parcels_sample"] = 0.0

    # 7. zonal_verify.txt
    p = rd / "zonal_verify.txt"
    if p.exists() and re.search(r"\d", p.read_text(errors="ignore")):
        s["zonal_verify"] = 1.0
    else:
        s["zonal_verify"] = 0.0

    # 9. field_distinct.txt — HIGH/MEDIUM/LOW
    p = rd / "field_distinct.txt"
    if p.exists():
        txt = p.read_text(errors="ignore").upper()
        hits = sum(1 for k in ["HIGH", "MEDIUM", "LOW"] if k in txt)
        s["field_distinct"] = hits / 3.0
    else:
        s["field_distinct"] = 0.0

    # 2,4,6,8,10,12. GUI screenshots + OCR
    shots = {
        "view_01_layers.png":      ["QGIS", "Layers", "Layer", "Browser"],
        "view_02_dem_styled.png":  ["Pseudocolor", "RdYlGn", "Symbology", "Band", "Layer"],
        "view_03_zonal_dialog.png":["Zonal", "Statistics", "Mean", "Min", "Max"],
        "view_04_field_calc.png":  ["Field Calculator", "Expression", "Output", "Field"],
        "view_05_categorized.png": ["HIGH", "MEDIUM", "LOW", "Categorized", "Label"],
        "view_06_print_layout.png":["Layout", "Legend", "Scale", "Map", "Title"],
        "view_07_attribute_table_selection.png": ["Attribute Table", "elev_mean", "flood_risk", "Selected"],
        "view_08_qgis_and_terminal.png":         ["QGIS", "elev_mean", "zonal_verify", "Terminal"],
        "view_09_print_layout_dragging.png":     ["Layout", "Properties", "Item", "Atlas", "Page"],
    }
    gui_present = 0
    gui_ocr_hits = 0
    for fname, kws in shots.items():
        fp = rd / fname
        # v2: 5KB lower bound — files < 5KB treated as placeholders
        if fp.exists() and fp.stat().st_size > 5120:
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

    # 11. GeoPackage + flood_risk field
    gpkg = rd / "flood_parcels.gpkg"
    if gpkg.exists():
        try:
            out = subprocess.run(
                ["ogrinfo", "-sql", "SELECT DISTINCT flood_risk FROM parcels", str(gpkg)],
                capture_output=True, text=True, timeout=30)
            vals = set(re.findall(r"flood_risk\s*\([^)]*\)\s*=\s*(\w+)", out.stdout))
            s["gpkg_field_valid"] = 1.0 if vals == {"HIGH", "MEDIUM", "LOW"} else (
                0.5 if vals else 0.2)
        except Exception:
            s["gpkg_field_valid"] = 0.2
    else:
        s["gpkg_field_valid"] = 0.0

    # 12. risk_summary.txt — three counts present
    p = rd / "risk_summary.txt"
    if p.exists():
        txt = p.read_text(errors="ignore")
        nums = [int(x) for x in re.findall(r"\b(\d+)\b", txt)]
        cats = sum(1 for k in ["HIGH","MEDIUM","LOW"] if k in txt.upper())
        s["risk_summary"] = 1.0 if (cats == 3 and len(nums) >= 3) else 0.4
    else:
        s["risk_summary"] = 0.0

    # 13. PDF exists + A4 + pdf_check.txt
    pdf = rd / "flood_map_layout.pdf"
    s["pdf_exists"] = 1.0 if (pdf.exists() and pdf.stat().st_size > 1024) else 0.0
    if pdf.exists():
        try:
            out = subprocess.run(["pdfinfo", str(pdf)],
                                 capture_output=True, text=True, timeout=15)
            m = re.search(r"Page size:\s+([\d.]+)\s+x\s+([\d.]+)", out.stdout)
            if m:
                w, h = float(m.group(1)), float(m.group(2))
                a4_p = (abs(w - 595) < 15 and abs(h - 842) < 15)
                a4_l = (abs(w - 842) < 15 and abs(h - 595) < 15)
                s["pdf_a4"] = 1.0 if (a4_p or a4_l) else 0.3
            else:
                s["pdf_a4"] = 0.0
        except Exception:
            s["pdf_a4"] = 0.0
    else:
        s["pdf_a4"] = 0.0
    s["pdf_cli_check"] = 1.0 if (rd / "pdf_check.txt").exists() else 0.0

    # 14. validation.json structure
    vj = rd / "validation.json"
    if vj.exists():
        try:
            vd = json.loads(vj.read_text())
            checks = [
                isinstance(vd.get("total_parcels"), int) and vd["total_parcels"] > 0,
                vd.get("all_risk_valid") is True,
                str(vd.get("crs", "")).upper().startswith("EPSG:4326"),
                isinstance(vd.get("high_count"), int),
                isinstance(vd.get("medium_count"), int),
                isinstance(vd.get("low_count"), int),
                isinstance(vd.get("high_total_area_m2"), (int, float)),
            ]
            s["validation_json"] = sum(checks) / len(checks)
            if all(isinstance(vd.get(k), int) for k in ("high_count","medium_count","low_count","total_parcels")):
                tot = vd["high_count"] + vd["medium_count"] + vd["low_count"]
                s["validation_counts_match"] = 1.0 if tot == vd["total_parcels"] else 0.0
            else:
                s["validation_counts_match"] = 0.0
        except Exception:
            s["validation_json"] = 0.0
            s["validation_counts_match"] = 0.0
    else:
        s["validation_json"] = 0.0
        s["validation_counts_match"] = 0.0

    # 15. Shapefile suite
    shp_dir = rd / "flood_parcels_shp"
    exts = [".shp", ".shx", ".dbf", ".prj"]
    if shp_dir.exists():
        found = sum(1 for e in exts if list(shp_dir.glob(f"*{e}")))
        s["shapefile_suite"] = found / len(exts)
    else:
        s["shapefile_suite"] = 0.0

    # 15b. shp_verify.txt — must show 10-char field-name truncation behavior
    p = rd / "shp_verify.txt"
    if p.exists():
        txt = p.read_text(errors="ignore")
        has_field = ("flood_risk" in txt) or ("elev_mean" in txt) or ("area_m2" in txt)
        s["shp_verify"] = 1.0 if has_field else 0.4
    else:
        s["shp_verify"] = 0.0

    # 16. VLM rubric (≥4 items)
    vlm_keys = ["vlm_qgis_real", "vlm_dem_colormap", "vlm_categorized", "vlm_layout_complete"]
    if vlm_score_rubric:
        sample = [str(rd / n) for n in shots if (rd / n).exists()][:4]
        if sample:
            rubric = {
                "vlm_qgis_real":       "截图清晰显示 QGIS 桌面界面（菜单栏 / Layers 面板 / 地图画布）",
                "vlm_dem_colormap":    "DEM 图层使用了红黄绿伪彩色（RdYlGn）渲染",
                "vlm_categorized":     "Parcels 图层有分类着色（红/橙/绿）+ 文字标注",
                "vlm_layout_complete": "Print Layout 含地图框、图例、标题、比例尺、北箭头",
            }
            try:
                vlm = vlm_score_rubric(sample, rubric,
                                       instruction="评估 QGIS 洪水风险标注任务的 GUI 截图。")
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
    existing_shots = [p for p in shot_paths if p.exists() and p.stat().st_size > 5120]
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

    # gui_chrome_ocr: each screenshot must hit ≥ 2 distinct QGIS app-chrome keywords
    chrome_kws = ["QGIS", "Layers", "Symbology", "Print Layout", "Project",
                  "Browser", "Processing", "Toolbox"]
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

    # ---- Aggregate (v2: weighted core/gui/aux + tightened hard gates) ----
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    nonzero = [v for v in nums if v > 0]
    if not nonzero:
        s["overall_score"] = 0.000
        return s

    def _avg(keys):
        vals = [float(s.get(k, 0.0) or 0.0) for k in keys]
        return sum(vals) / max(1, len(vals))

    core_keys = [
        "ogrinfo_schema", "dem_stats", "parcels_sample", "zonal_verify",
        "field_distinct", "risk_summary", "gpkg_field_valid",
        "validation_json", "validation_counts_match",
        "shapefile_suite", "shp_verify",
        "pdf_exists", "pdf_a4",
    ]
    gui_keys = [
        "gui_screenshots_count", "gui_screenshots_ocr",
        "gui_real_interaction", "gui_chrome_ocr", "gui_window_geometry",
        "vlm_qgis_real", "vlm_dem_colormap", "vlm_categorized", "vlm_layout_complete",
    ]
    aux_keys = ["pdf_cli_check"]

    base = 0.6 * _avg(core_keys) + 0.3 * _avg(gui_keys) + 0.1 * _avg(aux_keys)

    # Hard gates — v2 tightened
    if s.get("gui_screenshots_count", 0) < 0.5:
        base = min(base, 0.35)
    if s.get("gpkg_field_valid", 0) < 1.0:
        base = min(base, 0.45)
    if s.get("gpkg_field_valid", 0) == 0:
        base = min(base, 0.30)
    if s.get("validation_json", 0) < 0.6:
        base = min(base, 0.45)
    if s.get("validation_counts_match", 0) == 0:
        base = min(base, 0.50)
    if s.get("pdf_exists", 0) == 0 or s.get("pdf_a4", 0) == 0:
        base = min(base, 0.50)
    if s.get("shapefile_suite", 0) < 1.0:
        base = min(base, 0.55)
    # GUI hard gates: CLI-only / fake-screenshot solutions are heavily capped
    if s.get("gui_real_interaction", 0) < 0.7:
        base = min(base, 0.40)
    if s.get("gui_real_interaction", 0) < 0.5:
        base = min(base, 0.30)
    if s.get("gui_chrome_ocr", 0) < 0.5:
        base = min(base, 0.40)
    if s.get("gui_chrome_ocr", 0) < 0.3:
        base = min(base, 0.30)
    if s.get("gui_window_geometry", 0) < 0.5:
        base = min(base, 0.45)
    # VLM-unavailable cap: without VLM rubric you cannot exceed 0.6
    vlm_sum = sum(float(s.get(k, 0.0) or 0.0) for k in
                  ("vlm_qgis_real","vlm_dem_colormap","vlm_categorized","vlm_layout_complete"))
    if vlm_sum <= 0:
        base = min(base, 0.60)
    elif (vlm_sum / 4.0) < 0.5:
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
