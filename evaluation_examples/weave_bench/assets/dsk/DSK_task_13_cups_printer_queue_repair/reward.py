# Auto-generated from WeaveBench task DSK_task_13_cups_printer_queue_repair.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi-axis grader for the CUPS printer-queue repair task."""
    import json, re, subprocess, glob
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt = Path("/opt/dsk13_gt") if Path("/opt/dsk13_gt/expected.json").exists() \
         else (Path("/tmp_workspace/gt") if Path("/tmp_workspace/gt").exists() \
               else Path("/tmp_workspace/setup/gt"))
    expected = {}
    try:
        expected = json.loads((gt / "expected.json").read_text())
    except Exception:
        pass
    s = {}

    # 1) lpstat snapshots: before + after
    snaps = sorted(glob.glob(str(rd / "lpstat_*.txt")))
    s["lpstat_snapshots"] = 1.0 if len(snaps) >= 2 \
        else (0.5 if len(snaps) == 1 else 0.0)

    # 2) ppd_excerpt covers both queues
    pe = rd / "ppd_excerpt.txt"; pe_ok = False
    if pe.exists():
        try:
            t = pe.read_text(errors="replace")
            pe_ok = ("EyesonRaw" in t) and ("EyesonPDF" in t) and len(t) > 200
        except Exception: pass
    s["ppd_excerpt"] = 1.0 if pe_ok else (0.4 if pe.exists() else 0.0)

    # 3) cups error log non-empty + topical
    cel = rd / "cups_error_log.txt"; cel_ok = False
    if cel.exists():
        try:
            t = cel.read_text(errors="replace")
            cel_ok = (len(t.strip()) > 300
                      and ("EyesonRaw" in t and "EyesonPDF" in t)
                      and sum(k in t for k in ["E ", "W ", "filter", "Duplex",
                          "media", "stopped"]) >= 3
                      and re.search(r"\[\d{2}/[A-Za-z]{3}/\d{4}", t) is not None)
        except Exception: pass
    s["cups_error_log"] = 1.0 if cel_ok else (0.4 if cel.exists() else 0.0)

    # 4) cupsfilter before err mentions duplex / filter / supported
    cb = rd / "cupsfilter_before.err"; cb_ok = False
    if cb.exists():
        try:
            t = cb.read_text(errors="replace").lower()
            cb_ok = ("duplex" in t
                     and any(k in t for k in ["unsupported","not supported","reject"])
                     and any(k in t for k in ["cupsfilter","eyeson_wrap","filter failed"]))
        except Exception: pass
    s["cupsfilter_before"] = 1.0 if cb_ok else (0.3 if cb.exists() else 0.0)

    # 5) cupsfilter after: ps non-empty + err clean
    ca_ps = rd / "cupsfilter_after.ps"; ca_err = rd / "cupsfilter_after.err"
    after_ok = False
    if ca_ps.exists() and ca_ps.stat().st_size > 200:
        try:
            t = ca_err.read_text(errors="replace").lower() if ca_err.exists() else ""
            after_ok = "error" not in t and "fail" not in t
        except Exception: pass
    s["cupsfilter_after"] = 1.0 if after_ok else 0.0

    # 6) diagnosis.json: 2 entries covering EyesonRaw + EyesonPDF
    dj = rd / "diagnosis.json"; entries = []
    if dj.exists():
        try:
            entries = json.loads(dj.read_text())
            if isinstance(entries, dict): entries = [entries]
        except Exception: entries = []
    queues = {e.get("queue") for e in entries if isinstance(e, dict)}
    exp_cat = {x["queue"]: x for x in expected.get("expected_root_causes", [])}
    good = 0
    for e in entries:
        if not isinstance(e, dict): continue
        ref = exp_cat.get(e.get("queue"), {})
        cat_ok = e.get("category") == ref.get("category")
        blob = (str(e.get("root_cause","")) + " "
                + " ".join(e.get("evidence_cli", []) or [])).lower()
        kw_ok = sum(k.lower() in blob for k in ref.get("keywords", [])) >= 2
        fix_ok = any(c in str(e.get("fix_command","")).lower()
                     for c in ["lpadmin","lpoptions","sed "])
        if cat_ok and kw_ok and fix_ok: good += 1
    s["diagnosis_count"] = 1.0 if len(entries) >= 2 else len(entries)/2.0
    s["diagnosis_coverage"] = 1.0 if {"EyesonRaw", "EyesonPDF"} <= queues \
        else (len(queues & {"EyesonRaw", "EyesonPDF"})/2.0)
    s["diagnosis_categories"] = good/2.0

    # 7) GUI screenshots + OCR
    gui_shots = expected.get("expected_screens", [
        "view_cups_jobs_red_banner.png",
        "view_cups_set_default_options.png",
        "view_system_config_printer_panel.png",
        "view_lpstat_terminal_before.png",
        "view_postrepair_completed_jobs.png",
    ])
    import hashlib
    present, _seen = [], set()
    for n in gui_shots:
        p = rd/n
        if not p.exists(): continue
        h = hashlib.md5(p.read_bytes()).hexdigest()
        if h in _seen: continue
        _seen.add(h); present.append(n)
    s["gui_screens_count"] = len(present)/float(len(gui_shots))
    ocr_kws = {
        "view_cups_jobs_red_banner.png":        [["EyesonRaw"], ["Stopped","Paused","disabled"]],
        "view_cups_set_default_options.png":    [["EyesonRaw"], ["Duplex"], ["PageSize","Media"]],
        "view_system_config_printer_panel.png": [["EyesonPDF"], ["Properties","Settings","Options"]],
        "view_lpstat_terminal_before.png":      [["lpstat"], ["disabled","stopped"], ["Eyeson"]],
        "view_postrepair_completed_jobs.png":   [["completed","Completed"], ["EyesonRaw","EyesonPDF"]],
    }
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        for n in present:
            try:
                tx = pytesseract.image_to_string(Image.open(rd/n))
                if all(any(k.lower() in tx.lower() for k in grp) for grp in ocr_kws.get(n, [])):
                    ocr_hits += 1
            except Exception: pass
        s["gui_screens_ocr"] = ocr_hits/float(len(gui_shots))
    except Exception:
        s["gui_screens_ocr"] = 0.5 * (len(present)/float(len(gui_shots)))

    # 8) lpstat_after has completed jobs and no stopped
    laf = rd / "lpstat_after.txt"
    if not laf.exists() and snaps:
        laf = Path(snaps[-1])
    completed_ok = stopped_clean = False
    if laf.exists():
        try:
            t = laf.read_text(errors="replace")
            has_struct = ("lpstat" in t.lower()
                          or re.search(r"^\s*\S+-\d+\s+\S+\s+\d+", t, re.M) is not None)
            has_both   = "EyesonRaw" in t and "EyesonPDF" in t
            n_completed = len(re.findall(r"\bcompleted\b", t, re.I))
            n_stopped   = len(re.findall(r"\b(?:stopped|disabled|paused)\b", t, re.I))
            completed_ok  = has_struct and has_both and n_completed >= 2
            stopped_clean = has_struct and n_stopped == 0
        except Exception: pass
    s["jobs_completed"] = 1.0 if completed_ok else 0.0
    s["jobs_no_stopped"] = 1.0 if stopped_clean else 0.0

    # 9) report.md
    rm = rd / "report.md"; n_lines = 0; sec_hits = 0
    if rm.exists():
        try:
            txt = rm.read_text(errors="replace")
            n_lines = len([1 for ln in txt.splitlines() if ln.strip()])
            for kw in ["拓扑", "症状", "取证", "根因", "修复", "复验",
                       "topology", "symptom", "evidence", "root cause",
                       "fix", "regression"]:
                if kw.lower() in txt.lower(): sec_hits += 1
        except Exception: pass
    s["report_present"] = 1.0 if n_lines >= 60 else n_lines/60.0
    s["report_sections"] = 1.0 if sec_hits >= 6 else sec_hits/6.0

    # 10) cross-channel: at least 2 CLI artifacts + 2 GUI screenshots
    cli_artifacts = sum(1 for p in [pe, cel, cb, ca_ps, dj, rm] if p.exists())
    s["cross_channel_evidence"] = 1.0 if (cli_artifacts >= 4 and len(present) >= 2) \
        else 0.0

    # 11) VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd/n) for n in [
        "view_cups_jobs_red_banner.png",
        "view_cups_set_default_options.png",
        "view_postrepair_completed_jobs.png",
    ] if (rd/n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_cups_banner_visible": "截图清楚显示 CUPS Web UI 的 stopped/paused 状态条",
            "vlm_options_panel": "截图显示 Set Default Options 中的 Duplex / PageSize 下拉选择器",
            "vlm_completed_state": "post-repair 截图显示至少 2 条 completed 记录、不再有 stopped",
            "vlm_layout_clean": "整体截图布局整齐、文字可读、无明显裁切",
        }
        try:
            vlm = vlm_score_rubric(vlm_imgs[:3], rubric,
                                   instruction="评估 CUPS 队列修复前后的 GUI 截图质量")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            for k in rubric: s[k] = 0.5
    else:
        s["vlm_cups_banner_visible"] = 0.5
        s["vlm_options_panel"] = 0.5
        s["vlm_completed_state"] = 0.5
        s["vlm_layout_clean"] = 0.5

    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums)/len(nums) if nums else 0.0

    # Hard gates
    if not (cel.exists() or cb.exists() or pe.exists()):  base = min(base, 0.4)
    # GUI hard-cap removed: rely on per-shot VLM/OCR sub-scores instead.
    vlm_avg = (s["vlm_cups_banner_visible"] + s["vlm_options_panel"] +
               s["vlm_completed_state"] + s["vlm_layout_clean"])/4.0
    if vlm_score_rubric is not None and vlm_imgs and vlm_avg < 0.6:
        base = min(base, 0.6)
    if not (completed_ok and stopped_clean):              base = min(base, 0.55)
    if not after_ok:                                      base = min(base, 0.6)

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
