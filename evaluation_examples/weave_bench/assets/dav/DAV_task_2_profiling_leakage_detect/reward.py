# Auto-generated from WeaveBench task DAV_task_2_profiling_leakage_detect.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DAV_task_2 grader. Empty workspace → 0.000. Hard gates: GUI + CLI + sklearn quantification.
    v2: weighted scoring (core 60% / gui 30% / aux 10%), multi-tier hard gates,
    anti-cheat (md5 uniqueness, min size/resolution), VLM-unavailable cap 0.55.
    """
    import json, csv, re, hashlib
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. CLI artifacts
    cli_files = ["describe.txt", "profile.html", "correlation.csv", "profile_clean.html"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 2

    # 2. correlation.csv schema
    cscore = 0.0
    cf = rd / "correlation.csv"
    if cf.exists():
        try:
            rows = list(csv.DictReader(cf.open()))
            need = {"feature", "pearson_r", "abs_r"}
            if rows and need.issubset(set(rows[0].keys())) and len(rows) >= 20:
                cscore = 1.0
        except Exception: pass
    s["correlation_schema"] = cscore

    # 3. suspected_leakage.json structure
    sl_score = 0.0
    sl = rd / "suspected_leakage.json"
    if sl.exists():
        try:
            d = json.loads(sl.read_text())
            cands = d.get("candidates", [])
            if 1 <= len(cands) <= 5 and all(
                isinstance(c, dict) and "feature" in c and "pearson_r" in c and "reason" in c and len(str(c["reason"])) >= 10
                for c in cands
            ):
                sl_score = 1.0
        except Exception: pass
    s["suspected_leakage_json"] = sl_score

    # 4. leakage_test.py output (parse expected output if logged)
    lt_score = 0.0
    out_log = rd / "leakage_test_output.txt"
    if out_log.exists():
        try:
            txt = out_log.read_text()
            # Look for "R² A" and "R² B" patterns
            ra = re.search(r"(?:R²|R2|R_squared)\s*A[:= ]+([\d.]+)", txt)
            rb = re.search(r"(?:R²|R2|R_squared)\s*B[:= ]+([\d.]+)", txt)
            if ra and rb:
                gap = float(ra.group(1)) - float(rb.group(1))
                if gap > 0.05: lt_score = 1.0
                elif gap > 0.02: lt_score = 0.6
        except Exception: pass
    s["leakage_quantified"] = lt_score

    # 5. housing_clean.csv
    cc_score = 0.0
    cc = workspace / "data" / "housing_clean.csv"
    if cc.exists():
        try:
            with cc.open() as f:
                header = next(csv.reader(f))
                if 20 <= len(header) <= 24:
                    cc_score = 1.0
        except Exception: pass
    s["clean_csv_exists"] = cc_score

    # 6. GUI screenshots — anti-cheat: existence + min size (>=20KB) + min resolution (>=1024x600) + md5 uniqueness
    gui_shots = ["view_bokeh_full.png","view_bokeh_box_select.png","view_bokeh_heatmap_hover.png","view_bokeh_clean_axis.png","view_bokeh_after_clean.png"]
    gui_present = sum(1 for n in gui_shots if (rd / n).exists())
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui = gui_present >= 3

    md5_set = set()
    valid_imgs = 0
    try:
        from PIL import Image as _Img
        for n in gui_shots:
            p = rd / n
            if not p.exists(): continue
            try:
                if p.stat().st_size < 20000: continue
                md5_set.add(hashlib.md5(p.read_bytes()).hexdigest())
                w, h = _Img.open(p).size
                if w >= 1024 and h >= 600:
                    valid_imgs += 1
            except Exception: pass
    except Exception:
        valid_imgs = gui_present
        md5_set = {str(i) for i in range(gui_present)}
    s["gui_screenshots_quality"] = valid_imgs / len(gui_shots)
    s["gui_screenshots_unique"] = (len(md5_set) / len(gui_shots)) if gui_present else 0.0
    has_gui_quality = valid_imgs >= 3 and len(md5_set) >= max(3, gui_present)

    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_bokeh_full.png": ["sale_price","Distribution","correlation","Box","Select"],
            "view_bokeh_box_select.png": ["Box","Select","scatter","selected"],
            "view_bokeh_heatmap_hover.png": ["heatmap","correlation","r="],
            "view_bokeh_clean_axis.png": ["overall_quality","scatter","Y-axis"],
            "view_bokeh_after_clean.png": ["sale_price","correlation"],
        }
        ocr_hits = 0
        for n, ks in kws.items():
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in ks): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
        ocr_available = True
    except Exception:
        s["gui_screenshots_ocr"] = 0.3 if gui_present > 0 else 0.0
        ocr_available = False

    # 7. tooltip_samples.json
    ts_score = 0.0
    ts = rd / "tooltip_samples.json"
    if ts.exists():
        try:
            d = json.loads(ts.read_text())
            samples = d if isinstance(d, list) else d.get("heatmap_hover", [])
            if isinstance(samples, list) and len(samples) >= 5:
                def _ok(item):
                    if not isinstance(item, dict):
                        return False
                    pair = item.get("col_pair") or item.get("pair") or item.get("columns")
                    rv = item.get("r") if "r" in item else item.get("pearson_r")
                    pair_ok = (
                        (isinstance(pair, (list, tuple)) and len(pair) == 2)
                        or (isinstance(pair, str) and ("," in pair or "/" in pair or "-" in pair))
                    )
                    return pair_ok and isinstance(rv, (int, float))
                good = sum(1 for it in samples if _ok(it))
                if good >= 5:
                    ts_score = 1.0
                elif good >= 3:
                    ts_score = 0.6
                else:
                    ts_score = 0.3
        except Exception: pass
    s["tooltip_samples"] = ts_score

    # 8. leakage_report.md
    rp_score = 0.0
    rp = rd / "leakage_report.md"
    if rp.exists():
        try:
            txt = rp.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            rp_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["leakage_report"] = rp_score

    # 9. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_available = vlm_score_rubric is not None
    vlm_keys = ["vlm_bokeh_layout","vlm_bokeh_axes_labeled","vlm_bokeh_interactive","vlm_bokeh_data_visible","vlm_bokeh_box_select","vlm_bokeh_heatmap_hover"]
    if vlm_score_rubric and (rd / "view_bokeh_full.png").exists():
        rubric_full = {
            "vlm_bokeh_layout": "截图含多个 Bokeh subplot (scatter/heatmap/histogram)",
            "vlm_bokeh_axes_labeled": "scatter / heatmap 都有清晰的轴标签",
            "vlm_bokeh_interactive": "可见 Box Select / Hover 等交互工具",
            "vlm_bokeh_data_visible": "图表上有真实数据点 / 颜色 / 区分",
        }
        try:
            vlm = vlm_score_rubric([str(rd / "view_bokeh_full.png")], rubric_full, instruction="评估 Bokeh cross-filter dashboard 截图。")
            for k in rubric_full: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            for k in rubric_full: s[k] = 0.0

        bs = rd / "view_bokeh_box_select.png"
        if bs.exists():
            try:
                vlm_bs = vlm_score_rubric([str(bs)], {"vlm_bokeh_box_select": "可见框选区域且其它子图被联动 highlight (高亮 / 半透明对比)"}, instruction="评估 Bokeh box-select 联动截图。")
                s["vlm_bokeh_box_select"] = float(vlm_bs.get("vlm_bokeh_box_select", 0.0))
            except Exception:
                s["vlm_bokeh_box_select"] = 0.0
        else:
            s["vlm_bokeh_box_select"] = 0.0

        hh = rd / "view_bokeh_heatmap_hover.png"
        if hh.exists():
            try:
                vlm_hh = vlm_score_rubric([str(hh)], {"vlm_bokeh_heatmap_hover": "heatmap cell 上浮出含数值的 tooltip (例如 r=0.xx)"}, instruction="评估 Bokeh heatmap hover tooltip 截图。")
                s["vlm_bokeh_heatmap_hover"] = float(vlm_hh.get("vlm_bokeh_heatmap_hover", 0.0))
            except Exception:
                s["vlm_bokeh_heatmap_hover"] = 0.0
        else:
            s["vlm_bokeh_heatmap_hover"] = 0.0
    else:
        for k in vlm_keys:
            s[k] = 0.0

    # weighted aggregate: core delivery 60% / GUI evidence 30% / aux 10%
    core_keys = ["cli_artifacts","correlation_schema","suspected_leakage_json","leakage_quantified","clean_csv_exists","leakage_report"]
    gui_keys_w = ["gui_screenshots_count","gui_screenshots_quality","gui_screenshots_unique","gui_screenshots_ocr"] + vlm_keys
    aux_keys = ["tooltip_samples"]
    def _avg(ks):
        vs = [s.get(k, 0.0) for k in ks if isinstance(s.get(k, 0.0), (int, float))]
        return sum(vs) / len(vs) if vs else 0.0
    core = _avg(core_keys)
    gui = _avg(gui_keys_w)
    aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # multi-tier hard gates (v2: stricter)
    if not has_cli: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.25)
    if not has_gui_quality: base = min(base, 0.40)  # screenshots must be real (size/resolution/unique)
    if s["correlation_schema"] < 1.0: base = min(base, 0.40)
    if s["suspected_leakage_json"] < 1.0: base = min(base, 0.45)
    if s["leakage_quantified"] < 1.0: base = min(base, 0.50)
    if s["leakage_quantified"] < 0.6: base = min(base, 0.35)
    if s["clean_csv_exists"] < 1.0: base = min(base, 0.55)
    if s.get("gui_screenshots_ocr", 0.0) < 0.4: base = min(base, 0.55)
    # VLM unavailable → cap so no-VLM run cannot get full marks
    if not vlm_available: base = min(base, 0.55)

    s["overall_score"] = round(base, 4)
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
