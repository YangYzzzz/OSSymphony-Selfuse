# Auto-generated from WeaveBench task DOC_task_4_calc_vlookup_ods.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """LibreOffice Calc ODS VLOOKUP repair grader: CLI XML analysis + GUI fix + validation.
    Empty results → overall_score == 0.000.
    """
    import json, subprocess, zipfile, re
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
    gt_data = {}
    if (gt / "expected.json").exists():
        try:
            gt_data = json.loads((gt / "expected.json").read_text())
        except Exception:
            pass

    sub_keys = [
        "content_pretty", "unpack_meta_schema",
        "broken_refs_lines", "broken_refs_format", "broken_refs_count",
        "named_ranges_schema", "named_ranges_has_broken",
        "sheet_stats_coverage",
        "calc_initial_shots", "calc_find_shots",
        "vlookup_mapping_schema",
        "calc_named_ranges_shots",
        "fixed_ods_exists", "fixed_ods_valid_zip",
        "postfix_no_ref", "postfix_grep_schema",
        "calc_fixed_shots", "calc_summary_shot",
        "csv_export_exists", "csv_no_ref",
        "validation_report_schema", "vlookup_match_rate", "summary_kpis_present",
        "report_length", "report_table",
        "repack_log_exists",
        "screenshots_count", "screenshot_ocr",
        "cross_channel",
        "vlm_calc_ui", "vlm_ref_errors_visible",
        "vlm_named_ranges_dialog", "vlm_fixed_clean",
    ]
    s = {k: 0.0 for k in sub_keys}

    if not rd.exists() or not any(rd.iterdir()):
        s["overall_score"] = 0.000
        return s

    # 1
    cp = rd / "content_pretty.xml"
    if cp.exists() and cp.stat().st_size > 1000:
        s["content_pretty"] = 1.0
    um = rd / "unpack_meta.json"
    if um.exists():
        try:
            d = json.loads(um.read_text())
            need = {"content_xml_bytes", "content_xml_lines", "manifest_entries"}
            s["unpack_meta_schema"] = 1.0 if need.issubset(d.keys()) else 0.3
        except Exception:
            pass

    # 2 broken refs
    br = rd / "broken_refs.txt"
    if br.exists():
        lines = [l for l in br.read_text(errors="ignore").splitlines() if l.strip()]
        n = len(lines)
        s["broken_refs_lines"] = 1.0 if n >= 50 else (n / 50.0 if n else 0.0)
        ok_fmt = sum(1 for l in lines[:30] if re.match(r"\S+:\S+\s+\S", l))
        s["broken_refs_format"] = ok_fmt / max(1, min(30, n))
    bc = rd / "broken_refs_count.txt"
    if bc.exists():
        try:
            v = int(bc.read_text(errors="ignore").strip().split()[0])
            s["broken_refs_count"] = 1.0 if v > 0 else 0.0
        except Exception:
            pass

    # 3 named ranges
    nr = rd / "named_ranges_audit.json"
    if nr.exists():
        try:
            d = json.loads(nr.read_text())
            ok = isinstance(d.get("valid"), list) and isinstance(d.get("broken"), list) and "total" in d
            s["named_ranges_schema"] = 1.0 if ok else 0.3
            s["named_ranges_has_broken"] = 1.0 if (ok and len(d.get("broken", [])) > 0) else 0.0
        except Exception:
            pass

    # 4 sheet stats
    ss = rd / "sheet_stats.json"
    if ss.exists():
        try:
            d = json.loads(ss.read_text())
            need = {"SalesData", "ProductCatalog", "Summary"}
            found = set(d.keys()) if isinstance(d, dict) else set()
            s["sheet_stats_coverage"] = len(found & need) / 3.0
        except Exception:
            pass

    # 5 GUI initial
    init_shots = ["view_01_calc_errors", "view_02_calc_formula_bar"]
    init_present = []
    for n in init_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and f[0].stat().st_size > 3000:
            init_present.append(f[0])
    s["calc_initial_shots"] = len(init_present) / len(init_shots)

    # 6 Find shots
    find_shots = ["view_03_calc_find_dialog", "view_04_calc_find_results"]
    find_present = []
    for n in find_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and f[0].stat().st_size > 3000:
            find_present.append(f[0])
    s["calc_find_shots"] = len(find_present) / len(find_shots)

    # 7 VLOOKUP mapping (schema + GT cross-check)
    vm = rd / "vlookup_mapping.json"
    mapping_matches_gt = False
    if vm.exists():
        try:
            d = json.loads(vm.read_text())
            need = {"product_catalog_columns", "vlookup_formulas_sampled", "inferred_mapping"}
            ok = need.issubset(d.keys()) and isinstance(d.get("inferred_mapping"), list) and len(d["inferred_mapping"]) >= 1
            s["vlookup_mapping_schema"] = 1.0 if ok else 0.3
            # GT cross-check: inferred_mapping must contain old=6 → new=4 (per gt/expected.json)
            gt_map = (gt_data or {}).get("vlookup_fix_mapping", {}) or {}
            expected_old, expected_new = None, None
            for k, v in gt_map.items():
                m1 = re.search(r"old_col_(\d+)", str(k))
                m2 = re.search(r"new_col_(\d+)", str(v))
                if m1 and m2:
                    expected_old, expected_new = int(m1.group(1)), int(m2.group(1))
                    break
            if ok and expected_old is not None:
                for entry in d.get("inferred_mapping", []):
                    try:
                        if int(entry.get("old")) == expected_old and int(entry.get("new")) == expected_new:
                            mapping_matches_gt = True
                            break
                    except Exception:
                        continue
                if not mapping_matches_gt:
                    # downgrade schema score: agent fabricated a mapping
                    s["vlookup_mapping_schema"] = min(s["vlookup_mapping_schema"], 0.3)
        except Exception:
            pass

    # 8 Named Ranges shots
    nr_shots = ["view_05_calc_named_ranges", "view_06_calc_named_ranges_fixed"]
    nr_present = []
    for n in nr_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and f[0].stat().st_size > 3000:
            nr_present.append(f[0])
    s["calc_named_ranges_shots"] = len(nr_present) / len(nr_shots)

    # 9 fixed ods
    fixed = rd / "sales_report_fixed.ods"
    if fixed.exists() and fixed.stat().st_size > 1000:
        s["fixed_ods_exists"] = 1.0
        try:
            with zipfile.ZipFile(str(fixed), "r") as z:
                names = z.namelist()
                if "content.xml" in names and "META-INF/manifest.xml" in names and "mimetype" in names:
                    s["fixed_ods_valid_zip"] = 1.0
        except Exception:
            pass

    # 10 postfix grep
    pg = rd / "postfix_grep.json"
    if pg.exists():
        try:
            d = json.loads(pg.read_text())
            need = {"ref_count_after_fix", "fixed_ods_size_bytes", "manifest_ok"}
            s["postfix_grep_schema"] = 1.0 if need.issubset(d.keys()) else 0.3
            s["postfix_no_ref"] = 1.0 if int(d.get("ref_count_after_fix", 99) or 99) == 0 else 0.0
        except Exception:
            pass
    # cross-check via direct unzip
    if s["postfix_no_ref"] == 0 and fixed.exists():
        try:
            with zipfile.ZipFile(str(fixed), "r") as z:
                content = z.read("content.xml").decode("utf-8", errors="replace")
                if "#REF" not in content:
                    s["postfix_no_ref"] = 1.0
        except Exception:
            pass

    # 11 fixed shots
    fix_shots = ["view_07_calc_salesdata_fixed", "view_08_calc_formula_bar_fixed"]
    fix_present = []
    for n in fix_shots:
        f = list(rd.glob(f"{n}*.png"))
        if f and f[0].stat().st_size > 3000:
            fix_present.append(f[0])
    s["calc_fixed_shots"] = len(fix_present) / len(fix_shots)

    # 12 summary shot
    sm = list(rd.glob("view_09_calc_summary*.png"))
    sm_present = []
    if sm and sm[0].stat().st_size > 3000:
        s["calc_summary_shot"] = 1.0
        sm_present = [sm[0]]

    # 13 csv export + validation
    csv_file = rd / "salesdata_export.csv"
    if not csv_file.exists():
        # soffice may name output by sheet, try alternatives
        cands = list(rd.glob("*SalesData*.csv")) + list(rd.glob("sales_report_fixed*.csv"))
        if cands:
            csv_file = cands[0]
    if csv_file.exists() and csv_file.stat().st_size > 100:
        s["csv_export_exists"] = 1.0
        text = csv_file.read_text(errors="replace")
        if "#REF" not in text:
            s["csv_no_ref"] = 1.0

    vr = rd / "validation_report.json"
    if vr.exists():
        try:
            d = json.loads(vr.read_text())
            need = {"sampled_rows", "match_rate", "csv_has_ref_error",
                    "total_revenue", "total_orders", "avg_order_value"}
            s["validation_report_schema"] = 1.0 if need.issubset(d.keys()) else 0.4
            mr = float(d.get("match_rate", 0) or 0)
            s["vlookup_match_rate"] = 1.0 if mr >= 0.9 else max(0.0, mr / 0.9)
            kpis = sum(1 for k in ["total_revenue", "total_orders", "avg_order_value"]
                       if isinstance(d.get(k), (int, float)))
            s["summary_kpis_present"] = kpis / 3.0
        except Exception:
            pass

    # 14 report
    rr = rd / "repair_report.md"
    if rr.exists():
        txt = rr.read_text(errors="ignore")
        s["report_length"] = 1.0 if len(txt) >= 350 else len(txt) / 350.0
        s["report_table"] = 1.0 if ("|" in txt and re.search(r"\|\s*[-:]+\s*\|", txt)) else 0.0

    # 14b repack_log.txt 存在性弱校验（Prompt #15 产物）
    rl = rd / "repack_log.txt"
    if rl.exists() and rl.stat().st_size > 0:
        s["repack_log_exists"] = 1.0

    # screenshots aggregate
    all_shots = init_present + find_present + nr_present + fix_present + sm_present
    s["screenshots_count"] = len(all_shots) / 9.0

    if pytesseract and Image and all_shots:
        kws = ["LibreOffice", "Calc", "VLOOKUP", "Named", "Range",
               "#REF", "Find", "Replace", "Sheet", "Summary", "Cell"]
        hits = 0
        for sp in all_shots:
            try:
                tx = pytesseract.image_to_string(Image.open(sp))
                if any(k in tx for k in kws):
                    hits += 1
            except Exception:
                pass
        s["screenshot_ocr"] = min(1.0, hits / 5.0)

    has_cli = (s["broken_refs_lines"] > 0.3 and s["sheet_stats_coverage"] > 0.5
               and s["fixed_ods_exists"] > 0 and s["csv_export_exists"] > 0)
    has_gui = s["screenshots_count"] >= 0.55
    s["cross_channel"] = 1.0 if (has_cli and has_gui) else (0.5 if (has_cli or has_gui) else 0.0)

    # VLM rubric
    if vlm_score_rubric and all_shots:
        rubric = {
            "vlm_calc_ui": "截图中可见 LibreOffice Calc 菜单栏 / 工具栏 / 单元格网格",
            "vlm_ref_errors_visible": "errors 截图中可见红色 #REF! 标记的错误单元格",
            "vlm_named_ranges_dialog": "至少一张截图显示 Manage Named Ranges 对话框",
            "vlm_fixed_clean": "fixed 截图中单元格显示正常数值且无红色错误标记",
        }
        try:
            vlm = vlm_score_rubric([str(p) for p in all_shots[:4]], rubric,
                                   instruction="评估 LibreOffice Calc VLOOKUP 修复任务截图。")
            for k in rubric:
                s[k] = float(vlm.get(k, 0.0) or 0.0)
        except Exception:
            pass

    # GT KPI cross-check (must be within 5% of expected.json values)
    kpi_match = 0
    kpi_total = 0
    if gt_data and vr.exists():
        try:
            d = json.loads(vr.read_text())
            for k in ["total_revenue", "total_orders", "avg_order_value"]:
                if k in gt_data and isinstance(d.get(k), (int, float)):
                    kpi_total += 1
                    exp = float(gt_data[k]); act = float(d[k])
                    if abs(act - exp) <= max(1.0, abs(exp) * 0.05):
                        kpi_match += 1
        except Exception:
            pass
    if kpi_total > 0:
        # If KPIs don't match GT, cap summary_kpis_present accordingly
        s["summary_kpis_present"] = min(s["summary_kpis_present"], kpi_match / kpi_total)

    # Weighted aggregation: core delivery 60% + GUI evidence 30% + auxiliary 10%
    core_keys = [
        "broken_refs_lines", "broken_refs_format", "broken_refs_count",
        "named_ranges_schema", "named_ranges_has_broken",
        "sheet_stats_coverage",
        "vlookup_mapping_schema",
        "fixed_ods_exists", "fixed_ods_valid_zip",
        "postfix_no_ref", "postfix_grep_schema",
        "csv_export_exists", "csv_no_ref",
        "validation_report_schema", "vlookup_match_rate", "summary_kpis_present",
    ]
    gui_keys = [
        "calc_initial_shots", "calc_find_shots", "calc_named_ranges_shots",
        "calc_fixed_shots", "calc_summary_shot",
        "screenshots_count", "screenshot_ocr",
        "vlm_calc_ui", "vlm_ref_errors_visible",
        "vlm_named_ranges_dialog", "vlm_fixed_clean",
    ]
    aux_keys = [
        "content_pretty", "unpack_meta_schema",
        "report_length", "report_table",
        "repack_log_exists", "cross_channel",
    ]
    def _avg(keys):
        vals = [s[k] for k in keys if k in s]
        return sum(vals) / len(vals) if vals else 0.0
    base = 0.6 * _avg(core_keys) + 0.3 * _avg(gui_keys) + 0.1 * _avg(aux_keys)

    # Hard gates (越严越好)
    if not has_cli:
        base = min(base, 0.35)
    if not has_gui:
        base = min(base, 0.35)
    if s["postfix_no_ref"] == 0 and s["fixed_ods_exists"] > 0:
        base = min(base, 0.40)
    if s["csv_no_ref"] == 0 and s["csv_export_exists"] > 0:
        base = min(base, 0.45)
    # Inferred mapping must match GT (old→new column index)
    if not mapping_matches_gt:
        base = min(base, 0.50)
    # Validation report must achieve high match_rate AND KPIs match GT
    if s["vlookup_match_rate"] < 0.7:
        base = min(base, 0.50)
    if kpi_total > 0 and kpi_match < kpi_total:
        base = min(base, 0.55)
    # VLM unavailable / all-zero rubric → cap 0.6 (cannot get full credit without visual evidence judging)
    vlm_keys = ["vlm_calc_ui", "vlm_ref_errors_visible", "vlm_named_ranges_dialog", "vlm_fixed_clean"]
    if (vlm_score_rubric is None) or all(s[k] == 0.0 for k in vlm_keys):
        base = min(base, 0.60)
    # OCR keyword evidence too weak → cap 0.55
    if s["screenshot_ocr"] < 0.5:
        base = min(base, 0.55)
    # Screenshots coverage really low (<5/9) → cap 0.45
    if s["screenshots_count"] < 5/9 - 1e-6:
        base = min(base, 0.45)

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
