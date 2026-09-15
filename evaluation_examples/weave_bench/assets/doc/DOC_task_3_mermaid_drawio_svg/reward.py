# Auto-generated from WeaveBench task DOC_task_3_mermaid_drawio_svg.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Mermaid → Draw.io → SVG multi-round CLI/GUI grader.
    Empty results → overall_score == 0.000.
    """
    import json, subprocess, re, hashlib
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
    gt = workspace / "gt"

    sub_keys = [
        "original_svg", "mmdc_log",
        "svg_structure_schema",
        "structural_issues_schema",
        "drawio_initial_shots",
        "overlap_initial",
        "drawio_struct_shots", "struct_fixed_svg", "struct_fixed_valid",
        "xmllint_struct_log", "overlap_struct", "struct_check",
        "drawio_style_shots", "styled_svg", "styled_valid",
        "svgo_optimized", "svgo_log", "optimized_valid", "xmllint_optimized_log",
        "size_smaller", "size_compare_schema",
        "style_compliance",
        "drawio_compare_shots",
        "diff_report_schema", "edges_removed_ok",
        "evidence_index", "channel_switches_count",
        "report_length", "report_table",
        "screenshots_count", "screenshot_ocr",
        "cross_channel",
        "vlm_drawio_ui", "vlm_diagram_real",
        "vlm_overlap_visible", "vlm_styled_clean",
    ]
    s = {k: 0.0 for k in sub_keys}

    if not rd.exists() or not any(rd.iterdir()):
        s["overall_score"] = 0.000
        return s

    def well_formed(p):
        if not p.exists():
            return False
        try:
            r = subprocess.run(["xmllint", "--noout", str(p)], capture_output=True, timeout=10)
            return r.returncode == 0
        except Exception:
            return False

    # 1
    osvg = rd / "original_render.svg"
    s["original_svg"] = 1.0 if well_formed(osvg) and osvg.stat().st_size > 100 else (0.4 if osvg.exists() else 0.0)
    if (rd / "mmdc_warnings.log").exists():
        s["mmdc_log"] = 1.0

    # 2
    ss = rd / "svg_structure.json"
    if ss.exists():
        try:
            d = json.loads(ss.read_text())
            need = {"node_count", "edge_count", "labels", "viewBox"}
            s["svg_structure_schema"] = 1.0 if need.issubset(d.keys()) else 0.4
        except Exception:
            pass

    # 3
    si = rd / "structural_issues.json"
    if si.exists():
        try:
            d = json.loads(si.read_text())
            need = {"duplicate_edges", "orphan_nodes", "total_edges", "total_nodes"}
            ok_types = isinstance(d.get("duplicate_edges"), list) and isinstance(d.get("orphan_nodes"), list)
            s["structural_issues_schema"] = 1.0 if (need.issubset(d.keys()) and ok_types) else 0.4
        except Exception:
            pass

    # ---- screenshot validator (anti-cheat: size>=10KB, resolution>=1024x768, md5 unique) ----
    _seen_md5 = set()
    def _valid_shot(p):
        try:
            if p.stat().st_size < 10000:
                return False
            md5 = hashlib.md5(p.read_bytes()).hexdigest()
            if md5 in _seen_md5:
                return False
            if Image is not None:
                try:
                    w, h = Image.open(p).size
                    if w < 1024 or h < 768:
                        return False
                except Exception:
                    return False
            _seen_md5.add(md5)
            return True
        except Exception:
            return False

    # 4 GUI initial
    init_shots = ["view_01_drawio_full", "view_02_drawio_overlap", "view_03_drawio_format_panel"]
    init_present = []
    for n in init_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and _valid_shot(f[0]):
            init_present.append(f[0])
    s["drawio_initial_shots"] = len(init_present) / len(init_shots)

    # 5 overlap initial
    op = rd / "overlap_pairs_initial.json"
    if op.exists():
        try:
            d = json.loads(op.read_text())
            s["overlap_initial"] = 1.0 if all(k in d for k in ["pairs", "total_pairs_checked", "overlapping_count"]) else 0.3
        except Exception:
            pass

    # 6 GUI struct fix shots + struct_fixed.svg
    struct_shots = ["view_04_drawio_struct_fixing", "view_05_drawio_struct_done"]
    struct_present = []
    for n in struct_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and _valid_shot(f[0]):
            struct_present.append(f[0])
    s["drawio_struct_shots"] = len(struct_present) / len(struct_shots)

    sf = rd / "struct_fixed.svg"
    if sf.exists() and sf.stat().st_size > 100:
        s["struct_fixed_svg"] = 1.0
    s["struct_fixed_valid"] = 1.0 if well_formed(sf) else 0.0

    # 7 mid checks
    if (rd / "xmllint_struct.log").exists():
        s["xmllint_struct_log"] = 1.0
    op2 = rd / "overlap_pairs_struct.json"
    if op2.exists():
        try:
            d = json.loads(op2.read_text())
            ok = all(k in d for k in ["pairs", "total_pairs_checked", "overlapping_count"])
            # bonus: overlap should reduce
            initial_overlap = None
            if op.exists():
                try:
                    initial_overlap = int(json.loads(op.read_text()).get("overlapping_count", 0))
                except Exception:
                    pass
            now = int(d.get("overlapping_count", 99))
            if initial_overlap is None or initial_overlap == 0:
                improved = True
            else:
                improved = now < initial_overlap
            s["overlap_struct"] = 1.0 if (ok and improved) else (0.4 if ok else 0.0)
        except Exception:
            pass
    sc = rd / "struct_check.json"
    if sc.exists():
        try:
            d = json.loads(sc.read_text())
            need = {"total_edges", "total_nodes", "edges_removed_vs_original", "nodes_now_connected"}
            s["struct_check"] = 1.0 if need.issubset(d.keys()) else 0.3
        except Exception:
            pass

    # 8 GUI styling
    style_shots = ["view_06_drawio_style_panel", "view_07_drawio_styled"]
    style_present = []
    for n in style_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and _valid_shot(f[0]):
            style_present.append(f[0])
    s["drawio_style_shots"] = len(style_present) / len(style_shots)

    styled = rd / "styled.svg"
    if styled.exists() and styled.stat().st_size > 100:
        s["styled_svg"] = 1.0
    s["styled_valid"] = 1.0 if well_formed(styled) else 0.0

    # 9 svgo
    opt = rd / "optimized.svg"
    if opt.exists() and opt.stat().st_size > 50:
        s["svgo_optimized"] = 1.0
    if (rd / "svgo.log").exists():
        s["svgo_log"] = 1.0
    s["optimized_valid"] = 1.0 if well_formed(opt) else 0.0
    if (rd / "xmllint_optimized.log").exists():
        s["xmllint_optimized_log"] = 1.0
    if opt.exists() and styled.exists():
        s["size_smaller"] = 1.0 if opt.stat().st_size < styled.stat().st_size else 0.0
    sz = rd / "size_compare.json"
    if sz.exists():
        try:
            d = json.loads(sz.read_text())
            s["size_compare_schema"] = 1.0 if all(k in d for k in ["styled_bytes", "optimized_bytes", "ratio"]) else 0.3
        except Exception:
            pass

    # 10 style compliance
    sc_json = rd / "style_compliance.json"
    if sc_json.exists():
        try:
            d = json.loads(sc_json.read_text())
            v = d.get("violations", [])
            if d.get("compliant") is True:
                s["style_compliance"] = 1.0
            elif isinstance(v, list) and len(v) <= 1:
                s["style_compliance"] = 0.4
            else:
                s["style_compliance"] = 0.0
        except Exception:
            pass

    # 11 GUI compare
    cmp_shots = ["view_08_drawio_compare", "view_09_drawio_optimized_zoom"]
    cmp_present = []
    for n in cmp_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and _valid_shot(f[0]):
            cmp_present.append(f[0])
    s["drawio_compare_shots"] = len(cmp_present) / len(cmp_shots)

    # 12 diff report
    dr = rd / "diff_report.json"
    if dr.exists():
        try:
            d = json.loads(dr.read_text())
            need = {"nodes_added", "nodes_removed", "edges_added", "edges_removed"}
            s["diff_report_schema"] = 1.0 if need.issubset(d.keys()) else 0.3
            s["edges_removed_ok"] = 1.0 if int(d.get("edges_removed", 0) or 0) >= 2 else 0.0
        except Exception:
            pass

    # 13 evidence index
    ei = rd / "evidence_index.json"
    if ei.exists():
        try:
            d = json.loads(ei.read_text())
            ok = all(k in d for k in ["screenshots", "svgs", "cli_logs", "channel_switches"])
            s["evidence_index"] = 1.0 if ok else 0.3
            s["channel_switches_count"] = 1.0 if int(d.get("channel_switches", 0) or 0) >= 7 else 0.0
        except Exception:
            pass

    # 14 report
    rr = rd / "repair_report.md"
    if rr.exists():
        txt = rr.read_text(errors="ignore")
        s["report_length"] = 1.0 if len(txt) >= 350 else len(txt) / 350.0
        s["report_table"] = 1.0 if ("|" in txt and re.search(r"\|\s*[-:]+\s*\|", txt)) else 0.0

    # screenshots aggregate (only unique, validated shots count)
    all_shots = init_present + struct_present + style_present + cmp_present
    s["screenshots_count"] = 1.0 if len(all_shots) >= 7 else len(all_shots) / 7.0

    ocr_ratio = 0.0
    if pytesseract and Image and all_shots:
        kws = ["draw.io", "Drawio", "Edit", "Format", "Arrange", "Style",
               "Diagram", "Outline", "Geometry", "Fill"]
        hits = 0
        for sp in all_shots:
            try:
                tx = pytesseract.image_to_string(Image.open(sp))
                if any(k.lower() in tx.lower() for k in kws):
                    hits += 1
            except Exception:
                pass
        ocr_ratio = hits / max(1, len(all_shots))
        s["screenshot_ocr"] = min(1.0, ocr_ratio / 0.5)

    has_cli = (s["mmdc_log"] > 0 and s["svg_structure_schema"] > 0
               and s["overlap_initial"] > 0 and s["svgo_optimized"] > 0)
    has_gui = len(all_shots) >= 7  # tightened from >=5
    s["cross_channel"] = 1.0 if (has_cli and has_gui) else (0.4 if (has_cli or has_gui) else 0.0)

    # VLM rubric
    vlm_used = False
    if vlm_score_rubric and all_shots:
        rubric = {
            "vlm_drawio_ui": "截图中可见 Draw.io 桌面版菜单栏 / 工具栏 / 右侧 Format 面板",
            "vlm_diagram_real": "截图中可见多个带文字标签的方框 / 圆形节点和箭头连线",
            "vlm_overlap_visible": "overlap 截图中能直观看到节点文字遮盖或箭头交叉成乱麻",
            "vlm_styled_clean": "styled / optimized 截图中节点排列整齐、颜色已应用且无重叠",
        }
        try:
            vlm = vlm_score_rubric([str(p) for p in all_shots[:4]], rubric,
                                   instruction="评估 Draw.io 架构图修复任务的截图。")
            for k in rubric:
                s[k] = float(vlm.get(k, 0.0) or 0.0)
            vlm_used = any(s[k] > 0 for k in rubric)
        except Exception:
            pass

    # ---- weighted bucket scoring ----
    def _avg(keys):
        vals = [s[k] for k in keys if k in s]
        return sum(vals) / len(vals) if vals else 0.0

    core_keys = [
        "original_svg", "struct_fixed_svg", "struct_fixed_valid",
        "styled_svg", "styled_valid", "svgo_optimized", "optimized_valid",
        "size_smaller", "style_compliance", "edges_removed_ok",
        "overlap_struct", "struct_check",
    ]
    gui_keys = [
        "drawio_initial_shots", "drawio_struct_shots", "drawio_style_shots",
        "drawio_compare_shots", "screenshots_count", "screenshot_ocr",
        "cross_channel", "vlm_drawio_ui", "vlm_diagram_real",
        "vlm_overlap_visible", "vlm_styled_clean",
    ]
    aux_keys = [
        "mmdc_log", "svg_structure_schema", "structural_issues_schema",
        "overlap_initial", "xmllint_struct_log", "svgo_log",
        "xmllint_optimized_log", "size_compare_schema", "diff_report_schema",
        "evidence_index", "channel_switches_count",
        "report_length", "report_table",
    ]
    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys)
    base = 0.5 * core + 0.3 * gui + 0.2 * aux

    # ---- multi-layer hard gates (tightened) ----
    if not has_cli:
        base = min(base, 0.40)
    if not has_gui:
        base = min(base, 0.40)
    if s["screenshots_count"] < 0.6:
        base = min(base, 0.45)
    if s["struct_fixed_valid"] == 0 or s["styled_valid"] == 0 or s["optimized_valid"] == 0:
        base = min(base, 0.50)
    if s["edges_removed_ok"] == 0:
        base = min(base, 0.55)
    if s["style_compliance"] < 0.5:
        base = min(base, 0.55)
    if ocr_ratio < 0.4 and (pytesseract is not None):
        base = min(base, 0.55)
    if not vlm_used:
        base = min(base, 0.60)

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
