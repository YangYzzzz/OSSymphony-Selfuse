# Auto-generated from WeaveBench task SPA_task_14_cloudcompare_scan_vs_cad.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

import json, re, os
from pathlib import Path


def _safe_load_json(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return {}


def grade(workspace_path=None, **kwargs) -> dict:
    """CloudCompare scan-vs-CAD deviation QC grader."""
    rd = Path(workspace_path or "/tmp_workspace") / "results"
    gt_dir = Path("/tmp_workspace/gt")
    truth = _safe_load_json(gt_dir / "expected.json")
    s = {}
    cli_evidence = False
    gui_evidence = False

    try:
        from PIL import Image
    except Exception:
        Image = None
    try:
        import pytesseract
    except Exception:
        pytesseract = None
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    # 1. pdal_info.txt
    pi = rd / "pdal_info.txt"
    if pi.exists():
        txt = pi.read_text(errors="ignore")
        has_np = "num_points" in txt.lower() or "count" in txt.lower()
        has_bbox = "bounds" in txt.lower() or "minx" in txt.lower()
        s["pdal_info"] = 1.0 if (has_np and has_bbox) else 0.5
        cli_evidence = True
    else:
        s["pdal_info"] = 0.0

    # 2. stats_raw.json
    sr = _safe_load_json(rd / "stats_raw.json")
    sr_keys = ["num_points", "filter_ratio", "icp_rmse_mm"]
    s["stats_raw_schema"] = sum(1 for k in sr_keys if k in sr) / len(sr_keys)
    if sr:
        cli_evidence = True

    # 3. transform_icp.json
    ti = _safe_load_json(rd / "transform_icp.json")
    if isinstance(ti, list) and len(ti) == 4 and all(len(r) == 4 for r in ti):
        s["transform_icp"] = 1.0
    else:
        s["transform_icp"] = 0.0

    # 4. aligned ply exists
    ap = rd / "bracket_scan_aligned.ply"
    s["aligned_ply_exists"] = 1.0 if ap.exists() and ap.stat().st_size > 1000 else 0.0
    c2m = rd / "bracket_scan_c2m.ply"
    s["c2m_ply_present"] = 1.0 if c2m.exists() and c2m.stat().st_size > 1024 else 0.0

    # 5-10. GUI screenshots
    gui_shots = [
        "view_cc_loaded.png",
        "view_cc_c2m_colormap.png",
        "view_cc_histogram.png",
        "view_cc_max_deviation.png",
        "view_cc_cross_section.png",
        "view_cc_top_ortho.png",
        "view_cc_front_ortho.png",
    ]
    def _is_cc_ui(p):
        if not (Image and pytesseract and p.exists()): return False
        try:
            t = pytesseract.image_to_string(Image.open(p)).lower()
        except Exception: return False
        return sum(k in t for k in ["cloudcompare","db tree","properties","scalar","console"]) >= 2
    ok = [sh for sh in gui_shots if _is_cc_ui(rd / sh)]
    s["gui_screenshots"] = len(ok) / len(gui_shots)
    gui_evidence = len(ok) >= 5

    # OCR check on histogram screenshot
    hist_shot = rd / "view_cc_histogram.png"
    s["histogram_ocr"] = 0.0
    if hist_shot.exists() and pytesseract and Image:
        try:
            img = Image.open(hist_shot)
            txt = pytesseract.image_to_string(img).lower()
            if any(kw in txt for kw in ["mean", "max", "std", "histogram", "deviation"]):
                s["histogram_ocr"] = 1.0
        except Exception:
            pass

    # 11. deviation_stats.json
    ds = _safe_load_json(rd / "deviation_stats.json")
    exp = truth.get("expected_stats", {})
    tol = {"dev_max_mm":(0.6,1.1),"dev_mean_mm":(0.05,0.25),"pct_over_0.5mm":(0.5,8.0)}
    hit = sum(1 for k,(lo,hi) in tol.items()
              if isinstance(ds.get(k.replace("_mm","")), (int,float))
              and lo <= ds[k.replace("_mm","")] <= hi)
    schema = sum(1 for k in ["dev_mean","dev_std","dev_max","dev_min","pct_over_0.5mm"] if k in ds)/5
    s["deviation_stats_schema"] = 0.4*schema + 0.6*(hit/len(tol))

    # 12. over_tolerance_regions.json
    otr = _safe_load_json(rd / "over_tolerance_regions.json")
    if isinstance(otr, list) and 1 <= len(otr) <= 5:
        schema = sum(1 for r in otr if "centroid_xyz" in r and "max_dev_mm" in r and "point_count" in r)/len(otr)
        maxes = sorted([float(r.get("max_dev_mm",0)) for r in otr], reverse=True)
        big_ok = len(maxes)>=1 and 0.6 <= maxes[0] <= 1.1
        if len(maxes) >= 2:
            mid_ok = 0.25 <= maxes[1] <= 0.55
            s["over_tolerance_regions"] = 0.4*schema + 0.3*big_ok + 0.3*mid_ok
        else:
            s["over_tolerance_regions"] = 0.4*schema + 0.6*big_ok
    else:
        s["over_tolerance_regions"] = 0.0

    # 13. root_cause.md
    rc = rd / "root_cause.md"
    if rc.exists():
        txt = rc.read_text(errors="ignore")
        word_count = len(txt.split())
        has_suggestions = sum(1 for kw in ["建议", "suggest", "recommend", "improv"] if kw in txt.lower())
        cc = len(txt); kw = sum(k in txt for k in ["热变形","夹具","颤振","进给","M5","翼板","翘曲"])
        s["root_cause_md"] = min(1.0, cc/400) * (0.4 + 0.3*min(1.0,has_suggestions/2) + 0.3*min(1.0,kw/3))
    else:
        s["root_cause_md"] = 0.0

    # 14. report.md
    rp = rd / "report.md"
    if rp.exists():
        txt = rp.read_text(errors="ignore")
        word_count = len(txt.split())
        img_refs = len(re.findall(r"!\[.*?\]\(view_cc_.*?\.png\)", txt))
        has_verdict = "pass" in txt.lower() or "fail" in txt.lower()
        s["report_md_length"] = 1.0 if len(txt) >= 300 else min(1.0, len(txt)/300.0)
        s["report_md_images"] = min(1.0, img_refs / 6)
        s["report_md_verdict"] = 1.0 if has_verdict else 0.0
    else:
        s["report_md_length"] = 0.0
        s["report_md_images"] = 0.0
        s["report_md_verdict"] = 0.0

    # 15. report.pdf
    pdf = rd / "report.pdf"
    if pdf.exists():
        size_kb = pdf.stat().st_size / 1024
        s["report_pdf"] = 1.0 if size_kb > 50 else size_kb / 50
    else:
        s["report_pdf"] = 0.0

    # VLM rubric
    if vlm_score_rubric:
        colormap_shot = rd / "view_cc_c2m_colormap.png"
        if colormap_shot.exists():
            rubric = {
                "vlm_colormap_visible": "偏差热图显示清晰，能看到红/蓝/绿颜色渐变",
                "vlm_ui_elements": "CloudCompare UI 元素完整，含 DB Tree 和 3D 视图",
            }
            try:
                vlm = vlm_score_rubric([str(colormap_shot)], rubric, instruction="评估 CloudCompare 偏差热图截图质量")
                for k in rubric:
                    s[k] = vlm.get(k, 0.0)
            except Exception:
                pass

    # Hard gates
    base = sum(v for v in s.values() if isinstance(v, (int, float))) / max(1, len(s))
    if not cli_evidence:
        base = min(base, 0.4)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the gui_screenshots / vlm_* sub_scores.
    if s.get("histogram_ocr",0) < 1.0: base = min(base, 0.65)
    if vlm_score_rubric is not None and s.get("vlm_colormap_visible",0) < 0.6: base = min(base, 0.7)

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
