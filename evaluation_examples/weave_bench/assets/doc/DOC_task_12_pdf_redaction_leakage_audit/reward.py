# Auto-generated from WeaveBench task DOC_task_12_pdf_redaction_leakage_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """PDF redaction-leakage audit grader.

    Sub-scores cover: pdfinfo + meta.json + 3 independent text-extraction
    channels on the leaky PDF, leak_findings.json schema/PII coverage,
    pdfgrep cross-channel, GUI screenshots (initial render + zoom + Draw
    edit before/after + safe Okular view) with OCR + diversity checks,
    safe PDF re-export plus 3 channels of post-fix re-verification, the
    redaction_report.md narrative, a cross-channel CLI/GUI gate, and a
    VLM rubric judging that the GUI screenshots were truly captured from
    a PDF reader and a vector document editor. Empty results dir →
    overall_score == 0.000.
    """
    import json, re, hashlib, subprocess
    from pathlib import Path
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

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    # Prefer root-only /opt/doc12_gt to prevent answer leakage; fall back
    # to /tmp_workspace/gt for legacy mounts.
    gt = Path("/opt/doc12_gt") if Path("/opt/doc12_gt/expected.json").exists() else workspace / "gt"

    sub_keys = [
        "pdfinfo_present", "meta_schema",
        "leak_pdftotext_present", "leak_mutool_present", "leak_qdf_present",
        "extractors_agree",
        "leak_findings_schema", "leak_findings_token_classes",
        "leak_findings_strings", "leak_findings_per_employee",
        "pdfgrep_hits_present",
        "screenshots_count", "screenshots_diversity",
        "screenshots_chrome_ocr",
        "safe_pdf_present", "safe_pdftotext_clean",
        "safe_pdftotext_keeps_names", "safe_mutool_clean",
        "safe_pdfgrep_clean", "safe_render_present",
        "report_sections", "report_length",
        "cross_channel",
        "vlm_reader_chrome", "vlm_zoom_state",
        "vlm_draw_edit_layer", "vlm_safe_redacted_visible",
    ]
    s = {k: 0.0 for k in sub_keys}

    if not rd.exists() or not any(rd.iterdir()):
        s["overall_score"] = 0.000
        return s

    expected = {}
    ej = gt / "expected.json"
    if ej.exists():
        try:
            expected = json.loads(ej.read_text())
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 1. pdfinfo.txt + meta.json
    # ------------------------------------------------------------------
    pdfinfo = rd / "pdfinfo.txt"
    if pdfinfo.exists() and pdfinfo.stat().st_size > 50:
        s["pdfinfo_present"] = 1.0

    meta = {}
    mj = rd / "meta.json"
    if mj.exists():
        try:
            meta = json.loads(mj.read_text())
            need = {"pages", "producer", "creator", "title"}
            if need.issubset(set(meta.keys())) and isinstance(meta.get("pages"), int):
                s["meta_schema"] = 1.0
            elif meta:
                s["meta_schema"] = 0.5
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 2. three independent leak-extraction channels
    # ------------------------------------------------------------------
    lp = rd / "leak_pdftotext.txt"
    lp_text = lp.read_text(errors="ignore") if lp.exists() else ""
    pii_probe = ["412-77-9183", "583-21-4406", "297-08-6620",
                 "148,500", "221,750", "109,200"]
    pii_hits = sum(1 for t in pii_probe if t in lp_text)
    if lp_text and "Personnel Compensation Roster" in lp_text and pii_hits >= 5:
        s["leak_pdftotext_present"] = 1.0
    elif lp_text and pii_hits >= 2:
        s["leak_pdftotext_present"] = 0.5

    lm = rd / "leak_mutool.txt"
    lm_text = lm.read_text(errors="ignore") if lm.exists() else ""
    if lm_text and len(lm_text) > 80:
        s["leak_mutool_present"] = 1.0
    elif lm_text:
        s["leak_mutool_present"] = 0.5

    lq = rd / "leak_qdf.pdf"
    if lq.exists() and lq.stat().st_size > 1024:
        s["leak_qdf_present"] = 1.0

    if lp_text and lm_text:
        sample_pii = ["412-77-9183", "583-21-4406", "297-08-6620",
                      "148,500", "221,750", "109,200",
                      "0094-558217", "0188-330945", "0271-441089"]
        agree = sum(1 for tok in sample_pii if tok in lp_text and tok in lm_text)
        s["extractors_agree"] = agree / len(sample_pii)

    # ------------------------------------------------------------------
    # 3. leak_findings.json: schema, token classes, leaked strings, employee map
    # ------------------------------------------------------------------
    lf = rd / "leak_findings.json"
    lf_data = {}
    if lf.exists():
        try:
            lf_data = json.loads(lf.read_text())
        except Exception:
            lf_data = {}
    if lf_data:
        need = {"extractors_agree", "leak_token_classes",
                "leaked_strings", "per_employee"}
        if need.issubset(set(lf_data.keys())):
            s["leak_findings_schema"] = 1.0
        else:
            s["leak_findings_schema"] = 0.5

        classes = lf_data.get("leak_token_classes") or []
        gt_classes = expected.get("leak_token_classes",
                                  ["SSN", "Salary", "Account"])
        if isinstance(classes, list) and set(gt_classes) <= set(classes):
            s["leak_findings_token_classes"] = 1.0
        elif isinstance(classes, list) and classes:
            s["leak_findings_token_classes"] = len(set(classes) & set(gt_classes)) / len(gt_classes)

        strings = lf_data.get("leaked_strings") or []
        min_strings = int(expected.get("leaked_string_count_min", 12))
        if isinstance(strings, list) and len(set(strings)) >= min_strings:
            s["leak_findings_strings"] = 1.0
        elif isinstance(strings, list) and strings:
            s["leak_findings_strings"] = min(1.0, len(set(strings)) / float(min_strings))

        per_emp = lf_data.get("per_employee") or []
        gt_emps = expected.get("employees", [])
        if isinstance(per_emp, list) and gt_emps:
            hits = 0
            for gt_emp in gt_emps:
                gt_name = gt_emp.get("name", "")
                gt_fields = gt_emp.get("leaked_fields", [])
                for ent in per_emp:
                    if not isinstance(ent, dict):
                        continue
                    if ent.get("name") == gt_name:
                        agent_leaked = ent.get("leaked") or []
                        if isinstance(agent_leaked, list):
                            matched = sum(1 for fld in gt_fields
                                          if any(fld in a for a in agent_leaked))
                            if matched == len(gt_fields):
                                hits += 1
                        break
            s["leak_findings_per_employee"] = hits / max(1, len(gt_emps))

    # ------------------------------------------------------------------
    # 4. pdfgrep_hits.txt
    # ------------------------------------------------------------------
    pg = rd / "pdfgrep_hits.txt"
    if pg.exists() and pg.stat().st_size > 30:
        s["pdfgrep_hits_present"] = 1.0

    # ------------------------------------------------------------------
    # 5. screenshots: count, diversity, OCR for editor / reader chrome
    # ------------------------------------------------------------------
    shot_names = [
        "view_01_initial_render", "view_02_zoom_bar",
        "view_03_draw_loaded", "view_04_draw_after_edit",
        "view_05_safe_in_okular",
    ]
    shots = []
    for n in shot_names:
        cands = list(rd.glob(f"{n}*.png"))
        if cands and cands[0].stat().st_size > 3000:
            shots.append(cands[0])
    s["screenshots_count"] = min(1.0, len(shots) / 5.0)

    if shots:
        hashes = {hashlib.md5(p.read_bytes()).hexdigest() for p in shots}
        ratio = len(hashes) / len(shots)
        s["screenshots_diversity"] = 1.0 if ratio >= 0.8 else (0.5 if ratio >= 0.5 else 0.0)

    if pytesseract and Image and shots:
        chrome_kws = ["Okular", "Draw", "LibreOffice", "File", "Edit",
                      "View", "Tools", "Insert", "Format",
                      "Personnel", "REDACTED"]
        chrome_hits = 0
        for p in shots:
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if sum(1 for k in chrome_kws if k.lower() in tx.lower()) >= 2:
                    chrome_hits += 1
            except Exception:
                pass
        s["screenshots_chrome_ocr"] = min(1.0, chrome_hits / 3.0)

    # ------------------------------------------------------------------
    # 6. personnel_safe.pdf and post-fix re-verification channels
    # ------------------------------------------------------------------
    safe_pdf = workspace / "exec" / "redaction_project" / "personnel_safe.pdf"
    if safe_pdf.exists() and safe_pdf.stat().st_size > 1024:
        s["safe_pdf_present"] = 1.0

    must_absent = expected.get("post_fix_pdftotext_must_not_contain",
                               ["412-77-9183", "583-21-4406", "297-08-6620",
                                "148,500", "221,750", "109,200",
                                "0094-558217", "0188-330945", "0271-441089"])
    must_keep = expected.get("post_fix_pdftotext_should_still_contain",
                             ["Eleanor Whittaker", "Marcus Holloway",
                              "Priya Ranganathan",
                              "Personnel Compensation Roster"])

    sp = rd / "safe_pdftotext.txt"
    sp_text = sp.read_text(errors="ignore") if sp.exists() else ""
    if sp_text:
        absent = sum(1 for t in must_absent if t not in sp_text)
        s["safe_pdftotext_clean"] = absent / max(1, len(must_absent))
        kept = sum(1 for t in must_keep if t in sp_text)
        s["safe_pdftotext_keeps_names"] = kept / max(1, len(must_keep))

    sm = rd / "safe_mutool.txt"
    sm_text = sm.read_text(errors="ignore") if sm.exists() else ""
    if sm_text.strip():
        absent = sum(1 for t in must_absent if t not in sm_text)
        has_redacted = "[REDACTED]" in sm_text
        s["safe_mutool_clean"] = (absent / max(1, len(must_absent))) * (1.0 if has_redacted else 0.4)

    spg = rd / "safe_pdfgrep.txt"
    spg_text = spg.read_text(errors="ignore") if spg.exists() else ""
    if spg.exists() and spg_text.strip():
        absent = sum(1 for t in must_absent if t not in spg_text)
        has_redacted = "[REDACTED]" in spg_text
        s["safe_pdfgrep_clean"] = (absent / max(1, len(must_absent))) * (1.0 if has_redacted else 0.4)

    sr = list(rd.glob("safe_render-1.png")) or list(rd.glob("safe_render*.png"))
    if sr and sr[0].stat().st_size > 5000:
        s["safe_render_present"] = 1.0

    # ------------------------------------------------------------------
    # 7. redaction_report.md sections + length
    # ------------------------------------------------------------------
    rep = rd / "redaction_report.md"
    rep_text = rep.read_text(errors="ignore") if rep.exists() else ""
    if rep_text:
        sects = ["Summary", "Root cause", "Evidence", "Fix",
                 "Verification", "Recommendation"]
        header_re = [re.compile(rf"(?im)^\s*#{{1,6}}\s*{re.escape(h)}\b") for h in sects]
        sect_hits = sum(1 for rgx in header_re if rgx.search(rep_text))
        s["report_sections"] = sect_hits / len(sects)
        nlines = len([ln for ln in rep_text.splitlines() if ln.strip()])
        s["report_length"] = 1.0 if nlines >= 25 else nlines / 25.0

    # ------------------------------------------------------------------
    # 8. cross-channel CLI / GUI presence
    # ------------------------------------------------------------------
    cli_artifacts = sum(1 for n in ["leak_pdftotext.txt", "leak_mutool.txt",
                                    "leak_qdf.pdf", "pdfgrep_hits.txt",
                                    "leak_findings.json", "safe_pdftotext.txt"]
                        if (rd / n).exists())
    has_cli = cli_artifacts >= 4
    has_gui = len(shots) >= 4
    s["cross_channel"] = 1.0 if (has_cli and has_gui) else (0.5 if (has_cli or has_gui) else 0.0)

    # ------------------------------------------------------------------
    # 9. VLM rubric judging the GUI screenshots
    # ------------------------------------------------------------------
    vlm_avg = None
    if vlm_score_rubric and shots:
        rubric = {
            "vlm_reader_chrome":
                "view_01 / view_05 截图含 PDF 阅读器主窗口外框（标题栏 / 工具栏 / 侧边栏），不是裸渲染图像",
            "vlm_zoom_state":
                "view_02 截图能从窗体缩放比例或状态栏看出已显著放大，并聚焦到至少一条黑色条带",
            "vlm_draw_edit_layer":
                "view_03 / view_04 截图显示矢量文档编辑器的可逐对象编辑界面（左右侧边栏 + 中央画布），且 view_04 中可读到 [REDACTED] 字串而非黑色条带",
            "vlm_safe_redacted_visible":
                "view_05 修复后 PDF 在阅读器中可读，画面中能读到 [REDACTED] 占位文字或员工姓名",
        }
        try:
            vlm = vlm_score_rubric([str(p) for p in shots[:5]], rubric,
                                   instruction="评估 PDF 假性涂黑泄露审计任务的 GUI 截图真实性。")
            for k in rubric:
                s[k] = float(vlm.get(k, 0.0) or 0.0)
            s["judge_method"] = vlm.get("judge_method", "vlm")
            vlm_avg = sum(s[k] for k in rubric) / len(rubric)
        except Exception:
            vlm_avg = None

    # ------------------------------------------------------------------
    # Aggregate + hard gates
    # ------------------------------------------------------------------
    nums = [v for k, v in s.items()
            if isinstance(v, (int, float)) and k != "judge_method"]
    base = sum(nums) / max(1, len(nums))

    if not has_cli:
        base = min(base, 0.4)
    # NOTE: We deliberately do NOT cap on missing GUI screenshots —
    # whether the agent invokes a PDF reader / vector editor UI is not
    # a scoring axis. Missing PNGs already cost the screenshots_count /
    # screenshots_diversity / screenshots_chrome_ocr / 4 vlm_* sub_scores;
    # no additional hard cap is applied here.
    if cli_artifacts < 6:
        base = min(base, 0.55)
    if len(shots) < 5:
        base = min(base, 0.55)
    if s.get("safe_pdftotext_keeps_names", 0) < 1.0:
        base = min(base, 0.6)
    if s.get("leak_findings_per_employee", 0) < 1.0:
        base = min(base, 0.65)
    if s.get("extractors_agree", 0) < 0.7:
        base = min(base, 0.6)
    if vlm_score_rubric is not None and vlm_avg is not None and vlm_avg < 0.6:
        base = min(base, 0.6)
    if s.get("safe_pdftotext_clean", 0) < 0.7 and s.get("safe_pdf_present", 0) > 0:
        base = min(base, 0.55)
    if s.get("leak_findings_per_employee", 0) < 0.5 and lf_data:
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
