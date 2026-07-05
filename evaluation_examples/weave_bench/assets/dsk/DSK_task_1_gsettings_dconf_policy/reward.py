# Auto-generated from WeaveBench task DSK_task_1_gsettings_dconf_policy.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-dimensional grader for gsettings + dconf-editor policy audit task."""
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
    gt = workspace / "gt"
    s = {}

    def _safe_text(p):
        try:
            return p.read_text(errors="ignore") if p.exists() else ""
        except Exception:
            return ""

    # 1. baseline_dump.txt: must exist AND >= 200 lines (empty -> 0.000)
    bd = rd / "baseline_dump.txt"
    bd_lines = _safe_text(bd).splitlines()
    if not bd.exists() or len(bd_lines) == 0:
        s["baseline_dump"] = 0.0
    elif len(bd_lines) >= 200:
        s["baseline_dump"] = 1.0
    else:
        s["baseline_dump"] = round(len(bd_lines) / 200.0, 3)

    # 2. audit_before.json schema (items with required fields)
    ab = rd / "audit_before.json"
    ab_data = {}
    if ab.exists():
        try:
            ab_data = json.loads(_safe_text(ab))
        except Exception:
            ab_data = {}
    items_before = ab_data.get("items", []) if isinstance(ab_data, dict) else []
    required_fields = {"schema", "key", "expected", "actual", "status"}
    valid_items = [
        it for it in items_before
        if isinstance(it, dict) and required_fields.issubset(it.keys())
    ]
    target_count = max(1, len(items_before)) if items_before else 1
    if not items_before:
        s["audit_before_schema"] = 0.0
    else:
        s["audit_before_schema"] = round(len(valid_items) / target_count, 3)

    # 3. screenshots present (7 GUI shots) — 必须文件 ≥ 5KB 才算真截图
    shots = [
        "view_01_dconf_interface.png",
        "view_02_dconf_privacy.png",
        "view_03_dconf_edit_before.png",
        "view_04_dconf_edit_after.png",
        "view_05_dconf_lockdown.png",
        "view_06_dconf_watch.png",
        "view_07_dconf_verified.png",
    ]
    present = sum(1 for n in shots if (rd / n).exists() and (rd / n).stat().st_size >= 5120)
    s["screenshots_count"] = round(present / len(shots), 3)

    # 3b. anti-cheat: md5 uniqueness + 分辨率 ≥ 1280x720
    import hashlib
    md5s = set()
    res_ok = 0
    valid_shots = 0
    for n in shots:
        p = rd / n
        if not p.exists() or p.stat().st_size < 5120:
            continue
        valid_shots += 1
        try:
            md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
        except Exception:
            pass
        if Image is not None:
            try:
                w, h = Image.open(p).size
                if w >= 1280 and h >= 720:
                    res_ok += 1
            except Exception:
                pass
    s["screenshots_unique"] = round(len(md5s) / max(1, len(shots)), 3) if valid_shots else 0.0
    s["screenshots_resolution"] = round(res_ok / max(1, len(shots)), 3) if valid_shots else 0.0

    # 4. OCR coverage on screenshots
    ocr_hits = 0
    dconf_kws = ["Key properties", "Summary", "Description",
                 "Default value", "Custom value", "Use default",
                 "dconf", "schema", "Apply"]
    if pytesseract and Image:
        for n in shots:
            p = rd / n
            if not p.exists() or p.stat().st_size == 0:
                continue
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k.lower() in tx.lower() for k in dconf_kws):
                    ocr_hits += 1
            except Exception:
                pass
        s["screenshots_ocr"] = round(ocr_hits / len(shots), 3)
    else:
        s["screenshots_ocr"] = 0.0

    # 5. key_ranges.txt has range/enum metadata
    kr = rd / "key_ranges.txt"
    kr_text = _safe_text(kr)
    if not kr.exists() or not kr_text.strip():
        s["key_ranges"] = 0.0
    else:
        has_meta = bool(re.search(r"(enum|range|type|maximum|minimum)", kr_text, re.IGNORECASE))
        s["key_ranges"] = 1.0 if has_meta else 0.0

    # 6. dconf_signals.log has >= 2 /org/gnome paths
    sl = rd / "dconf_signals.log"
    sig_text = _safe_text(sl)
    if not sl.exists() or not sig_text.strip():
        s["dconf_signals"] = 0.0
    else:
        sig_paths = re.findall(r"/org/gnome/\S+", sig_text)
        if len(sig_paths) >= 2:
            s["dconf_signals"] = 1.0
        else:
            s["dconf_signals"] = round(len(sig_paths) / 2.0, 3)

    # 7. dconf_after_dump.ini non-empty
    dd = rd / "dconf_after_dump.ini"
    if not dd.exists() or dd.stat().st_size <= 50:
        s["dconf_dump"] = 0.0
    else:
        s["dconf_dump"] = 1.0

    # 8. policy_diff.txt has >= 3 changes
    pd = rd / "policy_diff.txt"
    pd_text = _safe_text(pd)
    if not pd.exists() or not pd_text.strip():
        s["policy_diff"] = 0.0
    else:
        change_lines = len(re.findall(r"^[<>+-]", pd_text, re.MULTILINE))
        s["policy_diff"] = 1.0 if change_lines >= 3 else round(change_lines / 3.0, 3)

    # 9. audit_after.json: all COMPLIANT + cross-validate w/ gt
    aa = rd / "audit_after.json"
    aa_data = {}
    if aa.exists():
        try:
            aa_data = json.loads(_safe_text(aa))
        except Exception:
            aa_data = {}
    items_after = aa_data.get("items", []) if isinstance(aa_data, dict) else []
    if not items_after:
        s["audit_after_compliant"] = 0.0
    else:
        compliant = sum(
            1 for it in items_after
            if isinstance(it, dict) and it.get("status") == "COMPLIANT"
        )
        s["audit_after_compliant"] = round(compliant / max(1, len(items_after)), 3)

    gt_file = gt / "expected.json"
    gt_expected = {}
    if gt_file.exists():
        try:
            gt_expected = json.loads(_safe_text(gt_file))
        except Exception:
            gt_expected = {}
    if gt_expected and items_after:
        gt_items = gt_expected.get("items", [])
        gt_map = {(g.get("schema"), g.get("key")): g.get("expected")
                  for g in gt_items if isinstance(g, dict)}
        match = 0
        for it in items_after:
            k = (it.get("schema"), it.get("key"))
            if k in gt_map and str(it.get("actual")) == str(gt_map[k]):
                match += 1
        s["values_match_gt"] = round(match / max(1, len(gt_map)), 3)
    else:
        s["values_match_gt"] = 0.0

    # 10. compliance_report.md
    cr = rd / "compliance_report.md"
    cr_text = _safe_text(cr)
    if not cr.exists() or not cr_text.strip():
        s["compliance_report"] = 0.0
    else:
        score = 0.0
        if re.search(r"^#\s+", cr_text, re.MULTILINE):
            score += 0.3
        table_rows = len(re.findall(r"^\|.*\|.*\|", cr_text, re.MULTILINE))
        if table_rows >= 6:
            score += 0.4
        if re.search(r"\d+(\.\d+)?\s*%", cr_text):
            score += 0.3
        s["compliance_report"] = round(score, 3)

    # 11. audit_summary.json
    ass = rd / "audit_summary.json"
    ass_data = {}
    if ass.exists():
        try:
            ass_data = json.loads(_safe_text(ass))
        except Exception:
            ass_data = {}
    req_keys = {"total_keys", "compliant_before", "compliant_after",
                "compliance_rate_before", "compliance_rate_after",
                "screenshots", "signals_captured"}
    if not ass_data:
        s["audit_summary_schema"] = 0.0
    else:
        present_k = req_keys & set(ass_data.keys())
        s["audit_summary_schema"] = round(len(present_k) / len(req_keys), 3)

    # 12. VLM rubric (4 items)
    sample = [str(rd / n) for n in shots if (rd / n).exists() and (rd / n).stat().st_size > 0][:4]
    if vlm_score_rubric and sample:
        rubric = {
            "vlm_dconf_editor_real": "截图清晰显示 dconf-editor 应用窗口（左侧路径树 + 右侧 Key properties / 编辑面板）",
            "vlm_key_detail_visible": "至少一张截图能看到 Summary / Description / Type / Default value 这些 GUI-only 字段",
            "vlm_edit_evidence": "至少一张截图显示某个键的 Custom value 输入框、'Use default value' 切换条或 ✓ Apply 按钮",
            "vlm_watch_terminal": "view_06 截图含真实终端窗口 + 命令提示符 + dconf watch 输出的实时路径行（不是文字 PS）",
        }
        try:
            vlm = vlm_score_rubric(sample, rubric,
                                   instruction="评估 dconf-editor + 终端 dconf watch 的取证截图真实性。")
            for k in rubric:
                s[k] = vlm.get(k, 0.0) if isinstance(vlm, dict) else 0.0
            if isinstance(vlm, dict):
                s["judge_method"] = vlm.get("judge_method", "failed")
        except Exception:
            for k in rubric:
                s[k] = 0.0
    else:
        for k in ["vlm_dconf_editor_real", "vlm_key_detail_visible",
                  "vlm_edit_evidence", "vlm_watch_terminal"]:
            s[k] = 0.0

    # 13. Content-reality sub-scores (drive content-driven hard gates)
    # 13a. compliance_report.md mentions >= 3 specific schema keys
    if not cr.exists() or not cr_text.strip():
        s["report_key_specificity"] = 0.0
    else:
        keys_mentioned = set(re.findall(r"org\.gnome\.[A-Za-z0-9_\-\.]+", cr_text))
        if len(keys_mentioned) >= 3:
            s["report_key_specificity"] = 1.0
        else:
            s["report_key_specificity"] = round(len(keys_mentioned) / 3.0, 3)

    # 13b. audit_after flips: NON_COMPLIANT(before) -> COMPLIANT(after)
    flip = 0
    if items_before and items_after:
        bad_before = {(i.get("schema"), i.get("key"))
                      for i in items_before
                      if isinstance(i, dict) and i.get("status") == "NON_COMPLIANT"}
        good_after = {(i.get("schema"), i.get("key"))
                      for i in items_after
                      if isinstance(i, dict) and i.get("status") == "COMPLIANT"}
        flip = len(bad_before & good_after)
    if flip >= 3:
        s["compliance_flips"] = 1.0
    elif flip >= 1:
        s["compliance_flips"] = round(flip / 3.0, 3)
    else:
        s["compliance_flips"] = 0.0

    # 13c. dconf after-dump truly differs from baseline (line set diff)
    dd_text = _safe_text(dd)
    base_set = set(l.strip() for l in bd_lines if l.strip())
    after_set = set(l.strip() for l in dd_text.splitlines() if l.strip())
    if not base_set or not after_set:
        s["dump_diff_real"] = 0.0
    else:
        diff_n = len(after_set.symmetric_difference(base_set))
        if diff_n >= 3:
            s["dump_diff_real"] = 1.0
        else:
            s["dump_diff_real"] = round(diff_n / 3.0, 3)

    # Aggregate (weighted): core 60% / gui 30% / aux 10%
    def _g(k, default=0.0):
        v = s.get(k, default)
        return float(v) if isinstance(v, (int, float)) else default

    core_keys = ["audit_after_compliant", "values_match_gt", "compliance_flips",
                 "dconf_dump", "dump_diff_real"]
    gui_keys = ["screenshots_count", "screenshots_ocr", "screenshots_unique",
                "screenshots_resolution",
                "vlm_dconf_editor_real", "vlm_key_detail_visible",
                "vlm_edit_evidence", "vlm_watch_terminal"]
    aux_keys = ["baseline_dump", "audit_before_schema", "key_ranges",
                "dconf_signals", "policy_diff", "compliance_report",
                "audit_summary_schema", "report_key_specificity"]
    core = sum(_g(k) for k in core_keys) / len(core_keys)
    gui = sum(_g(k) for k in gui_keys) / len(gui_keys)
    aux = sum(_g(k) for k in aux_keys) / len(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # VLM 不可用时整体封顶 0.6,不能让无 VLM 也满分
    if vlm_score_rubric is None or s.get("judge_method") == "failed":
        base = min(base, 0.6)
    # OCR 全 0 (pytesseract 不可用或截图全失败) 封顶 0.6
    if s.get("screenshots_ocr", 0) < 0.4:
        base = min(base, 0.6)

    # Hard gates — 关键产物缺失或退化路径直接封顶
    if s.get("screenshots_count", 0) < 0.7:
        base = min(base, 0.40)
    if s.get("screenshots_unique", 0) < 0.7:
        base = min(base, 0.45)  # 截图重复 = 伪截图嫌疑
    if s.get("screenshots_resolution", 0) < 0.5:
        base = min(base, 0.50)
    if s.get("baseline_dump", 0) == 0:
        base = min(base, 0.30)
    if s.get("audit_before_schema", 0) < 0.5:
        base = min(base, 0.40)
    if s.get("dconf_signals", 0) == 0:
        base = min(base, 0.50)
    if s.get("audit_after_compliant", 0) < 0.5:
        base = min(base, 0.40)
    if s.get("compliance_report", 0) < 0.5:
        base = min(base, 0.50)
    # Content-driven stepped hard gates (上拉)
    if s.get("compliance_flips", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("dump_diff_real", 0) < 0.5:
        base = min(base, 0.50)
    if s.get("report_key_specificity", 0) < 0.7:
        base = min(base, 0.55)
    if s.get("values_match_gt", 0) < 0.5:
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
