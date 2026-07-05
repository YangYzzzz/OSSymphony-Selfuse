# Auto-generated from WeaveBench task SPA_task_5_dxf_bracket_repair.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-dim grader for the DXF bracket repair task.

    Sub-scores cover: file presence, JSON schema, audit/duplicate numerics,
    dimension count, GUI screenshot count + OCR, render presence, and 3 VLM
    rubric items. Hard gates ensure nothing scores high without GUI evidence,
    cleanup evidence, or final render.
    """
    import json
    import re
    from pathlib import Path

    rd = Path("/tmp_workspace/results")
    rep = rd / "report"
    s = {}

    # ---- 1. entities_initial.json ------------------------------------------------
    p = rep / "entities_initial.json"
    if p.exists():
        try:
            d = json.loads(p.read_text())
            ok = (
                isinstance(d.get("by_layer"), dict)
                and len(d["by_layer"]) >= 1
                and isinstance(d.get("total_entities"), int)
                and d["total_entities"] > 0
                and isinstance(d.get("modelspace_extents"), list)
            )
            s["entities_initial"] = 1.0 if ok else 0.4
        except Exception:
            s["entities_initial"] = 0.2
    else:
        s["entities_initial"] = 0.0

    # ---- 2. audit_initial.txt ----------------------------------------------------
    p = rep / "audit_initial.txt"
    s["audit_initial"] = 1.0 if (p.exists() and p.stat().st_size > 10) else 0.0

    # ---- 3. duplicates.json (initial) -------------------------------------------
    p = rep / "duplicates.json"
    if p.exists():
        try:
            d = json.loads(p.read_text())
            grp = d.get("duplicate_groups", [])
            cnt = d.get("duplicate_count", 0)
            ok = isinstance(grp, list) and isinstance(cnt, int) and cnt >= 1 and len(grp) >= 1
            s["duplicates_initial"] = 1.0 if ok else 0.3
        except Exception:
            s["duplicates_initial"] = 0.2
    else:
        s["duplicates_initial"] = 0.0

    # ---- 4. audit_after_cleanup.txt ---------------------------------------------
    p = rep / "audit_after_cleanup.txt"
    s["audit_after"] = 1.0 if (p.exists() and p.stat().st_size > 10) else 0.0

    # ---- 5. duplicates_after.json must be 0 -------------------------------------
    p = rep / "duplicates_after.json"
    if p.exists():
        try:
            d = json.loads(p.read_text())
            cnt = d.get("duplicate_count", -1)
            s["duplicates_clean"] = 1.0 if cnt == 0 else 0.3
        except Exception:
            s["duplicates_clean"] = 0.2
    else:
        s["duplicates_clean"] = 0.0

    # ---- 6. dimensions.json count >= 3 ------------------------------------------
    p = rep / "dimensions.json"
    if p.exists():
        try:
            d = json.loads(p.read_text())
            n = d.get("dimension_count", 0)
            sub = d.get("by_subtype", {}) or {}
            has_radial = (sub.get("radial", 0) + sub.get("diametric", 0)) >= 1
            has_linear = sub.get("linear", 0) >= 2
            score = 0.0
            if n >= 3:
                score += 0.5
            if has_radial:
                score += 0.25
            if has_linear:
                score += 0.25
            s["dimensions_added"] = round(min(score, 1.0), 3)
        except Exception:
            s["dimensions_added"] = 0.2
    else:
        s["dimensions_added"] = 0.0

    # ---- 7. render_final.png > 5KB ----------------------------------------------
    p = rep / "render_final.png"
    if p.exists():
        sz = p.stat().st_size
        s["render_present"] = 1.0 if sz > 5000 else (sz / 5000.0)
    else:
        s["render_present"] = 0.0

    # ---- 8. validation.json schema + layer-0 reduced ----------------------------
    p = rep / "validation.json"
    if p.exists():
        try:
            d = json.loads(p.read_text())
            keys = ["audit_errors_initial", "audit_errors_after",
                    "duplicate_count_initial", "duplicate_count_after",
                    "dimension_count", "title_layer_text_count",
                    "layer_distribution_after",
                    "modelspace_extents", "render_png_size_bytes"]
            present = sum(1 for k in keys if k in d)
            ld = d.get("layer_distribution_after", {}) or {}
            outline_layer = ld.get("OUTLINE", 0)
            zero_layer_after = ld.get("0", 0)
            # Compare against initial layer-0 geometry to enforce real cleanup.
            init_zero = 0
            init_p = rep / "entities_initial.json"
            if init_p.exists():
                try:
                    init = json.loads(init_p.read_text())
                    by = (init.get("by_layer") or {}).get("0", {}) or {}
                    for k_e in ("LINE", "CIRCLE", "ARC", "LWPOLYLINE", "POLYLINE"):
                        v = by.get(k_e, 0)
                        if isinstance(v, int):
                            init_zero += v
                except Exception:
                    init_zero = 0
            if init_zero > 0:
                reduction = 1.0 - (zero_layer_after / max(1, init_zero))
                cleanup_ok = outline_layer >= 1 and reduction >= 0.5
            else:
                cleanup_ok = outline_layer >= 1 and zero_layer_after <= 2
            score = 0.4 * (present / len(keys)) + 0.6 * (1.0 if cleanup_ok else 0.3)
            s["validation_summary"] = round(min(score, 1.0), 3)
        except Exception:
            s["validation_summary"] = 0.2
    else:
        s["validation_summary"] = 0.0

    # ---- 9-10. GUI screenshots + OCR + anti-cheat -------------------------------
    try:
        from PIL import Image  # noqa: F401
        _has_pil = True
    except Exception:
        _has_pil = False
    try:
        import pytesseract
        _has_tess = True
    except Exception:
        _has_tess = False

    import hashlib

    shots = {
        "view_drawing_initial.png":   ["LibreCAD", "Layer", "Tool", "Cmd"],
        "view_layers_panel.png":      ["Layer", "OUTLINE", "0", "HIDDEN"],
        "view_after_cleanup.png":     ["LibreCAD", "Modify", "Layer"],
        "view_dimensions_added.png":  ["Dim", "Linear", "Radial", "Dimension"],
        "view_print_preview.png":     ["Print", "Preview", "A4", "Title"],
    }
    have, ocr_hit = 0, 0
    md5s = set()
    res_ok = 0
    size_ok = 0
    mtimes = []
    for fname, kws in shots.items():
        p = rd / fname
        if p.exists():
            sz = p.stat().st_size
            # Floor: anything under 5KB is treated as a placeholder, not a screenshot.
            if sz >= 5000:
                size_ok += 1
                have += 1
                try:
                    md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
                except Exception:
                    pass
                mtimes.append(p.stat().st_mtime)
                if _has_pil:
                    try:
                        from PIL import Image as _Img
                        with _Img.open(p) as im:
                            w, h = im.size
                        if w >= 1024 and h >= 600:
                            res_ok += 1
                    except Exception:
                        pass
                if _has_pil and _has_tess:
                    try:
                        from PIL import Image as _Img
                        txt = pytesseract.image_to_string(_Img.open(p))
                        if any(k.lower() in txt.lower() for k in kws):
                            ocr_hit += 1
                    except Exception:
                        pass
    n_shots = len(shots)
    # Count score requires presence + md5 uniqueness + minimum resolution.
    uniq_ratio = (len(md5s) / max(1, have)) if have else 0.0
    res_ratio = res_ok / n_shots
    presence_ratio = have / n_shots
    s["gui_screenshots_count"] = round(
        0.5 * presence_ratio + 0.3 * uniq_ratio + 0.2 * res_ratio, 3
    )
    # OCR: when VLM/OCR available, demand ≥60% hit rate to count as full credit.
    if _has_pil and _has_tess:
        s["gui_screenshots_ocr"] = round(min(1.0, (ocr_hit / n_shots) / 0.6), 3)
    else:
        # Neutral but capped — never a free 1.0.
        s["gui_screenshots_ocr"] = 0.4
    # Timestamp ordering: screenshots should follow workflow order.
    expected_order = list(shots.keys())
    ordered_mtimes = []
    for fn in expected_order:
        p = rd / fn
        if p.exists() and p.stat().st_size >= 5000:
            ordered_mtimes.append(p.stat().st_mtime)
    if len(ordered_mtimes) >= 3:
        s["gui_screenshots_order"] = round(
            sum(1 for i in range(1, len(ordered_mtimes))
                if ordered_mtimes[i] >= ordered_mtimes[i-1]) /
            (len(ordered_mtimes) - 1), 3
        )
    else:
        s["gui_screenshots_order"] = 0.0

    # ---- 11. cleaned DXF landed --------------------------------------------------
    cleaned = Path("/tmp_workspace/dxf_project/bracket_clean.dxf")
    s["cleaned_dxf_present"] = 1.0 if (cleaned.exists() and cleaned.stat().st_size > 500) else 0.0

    # ---- 12. VLM rubric ----------------------------------------------------------
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    vlm_keys = ["vlm_librecad_real", "vlm_dimensions_visible", "vlm_titleblock_visible"]
    _vlm_available = False
    if vlm_score_rubric is not None:
        sample = [str(rd / n) for n in shots if (rd / n).exists()]
        render_p = rep / "render_final.png"
        if render_p.exists():
            sample.append(str(render_p))
        sample = sample[:5]
        if sample:
            rubric = {
                "vlm_librecad_real": "至少 1 张截图明确显示 LibreCAD 主窗口（含菜单栏 / 工具栏 / 命令行面板 / 图层面板等多种 LibreCAD UI 元素），不是裸黑屏或纯渲染图",
                "vlm_dimensions_visible": "在 dimensions_added / render_final 中能看到带数字的尺寸标注线（线性距离 + 半径/直径），且尺寸文本可读",
                "vlm_titleblock_visible": "print_preview 或 render_final 中右下角能看到包含图号/比例/日期等多行文字的标题栏区域",
            }
            try:
                vlm = vlm_score_rubric(
                    sample, rubric,
                    instruction="评估 DXF 机械图清理 + 标注 + 出图任务的截图与渲染。",
                ) or {}
            except Exception:
                vlm = {}
            for k in vlm_keys:
                v = vlm.get(k, 0.0)
                try:
                    s[k] = float(v)
                except Exception:
                    s[k] = 0.0
            _vlm_available = True
        else:
            for k in vlm_keys:
                s[k] = 0.0
    else:
        for k in vlm_keys:
            s[k] = 0.4  # capped neutral when judge helper unavailable

    # ---- aggregate (weighted: core 60% / gui 30% / aux 10%) ---------------------
    core_keys = [
        "duplicates_initial", "duplicates_clean",
        "dimensions_added", "validation_summary", "cleaned_dxf_present",
        "render_present",
    ]
    gui_keys = [
        "gui_screenshots_count", "gui_screenshots_ocr",
        "gui_screenshots_order",
    ] + vlm_keys
    aux_keys = ["entities_initial", "audit_initial", "audit_after"]

    def _avg(keys):
        vals = [s.get(k, 0.0) for k in keys if isinstance(s.get(k, 0.0), (int, float))]
        return sum(vals) / max(1, len(vals))

    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # ---- hard gates (multi-layer, tightened) ------------------------------------
    # Core delivery gates.
    if s.get("cleaned_dxf_present", 0) == 0:
        base = min(base, 0.35)
    if s.get("duplicates_initial", 0) < 0.5:
        base = min(base, 0.40)
    if s.get("duplicates_clean", 0) < 0.5:
        base = min(base, 0.40)
    if s.get("dimensions_added", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("render_present", 0) == 0:
        base = min(base, 0.45)
    if s.get("validation_summary", 0) < 0.5:
        base = min(base, 0.50)
    # GUI evidence gates (anti-cheat: forbids "no real GUI run" path to a high score).
    if s.get("gui_screenshots_count", 0) < 0.7:
        base = min(base, 0.45)
    if s.get("gui_screenshots_count", 0) < 0.4:
        base = min(base, 0.30)
    if _has_pil and _has_tess and s.get("gui_screenshots_ocr", 0) < 0.5:
        base = min(base, 0.55)
    # VLM gates.
    vlm_avg = sum(s.get(k, 0.0) for k in vlm_keys) / len(vlm_keys)
    if _vlm_available:
        if vlm_avg < 0.6:
            base = min(base, 0.55)
        if vlm_avg < 0.4:
            base = min(base, 0.40)
    else:
        # No VLM → never let a run reach satisfactory.
        base = min(base, 0.60)

    s["overall_score"] = round(max(0.0, min(1.0, base)), 3)
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
