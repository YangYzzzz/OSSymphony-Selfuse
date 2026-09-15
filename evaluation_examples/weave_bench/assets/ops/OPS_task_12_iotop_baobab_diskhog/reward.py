# Auto-generated from WeaveBench task OPS_task_12_iotop_baobab_diskhog.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """OPS_task_12 grader: storage I/O attribution via iotop CLI + baobab GUI.
    Sub-scores cover CLI evidence (df / iostat / iotop / lsof / ps), GUI
    screenshots (overview, treemap hover, files highlighted, after-fix),
    OCR + VLM verification, post-remediation iostat ratio, postmortem
    quality, and cross-channel switch count."""
    import json, os, re, subprocess
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/opt/ops12_gt") if Path("/opt/ops12_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    s = {}
    expected = {}
    if (gt_dir / "expected.json").exists():
        try: expected = json.loads((gt_dir / "expected.json").read_text())
        except Exception: expected = {}
    hog_sub = expected.get("hog_process_cmdline_substring", "log_burst.py")
    hog_file_suffix = expected.get("hog_log_filename_suffix", ".frames.log")
    hog_dir_basename = expected.get("expected_treemap_largest_subdir_basename", "report_renderer")
    drop_factor = float(expected.get("min_post_remediation_drop_factor", 5.0))

    def _read(name):
        p = rd / name
        return p.read_text(errors="ignore") if p.exists() else ""

    # 1. df + iostat before
    df_before = _read("df_before.txt")
    s["df_before_present"] = 1.0 if df_before and ("/tmp_workspace/varlog" in df_before or "%" in df_before) else 0.0
    iostat_before = _read("iostat_before.txt")
    s["iostat_before_present"] = 1.0 if iostat_before and re.search(r"wMB/s|w/s|kB_wrtn", iostat_before) else (0.4 if iostat_before else 0.0)

    # 2. iotop_top.txt — must mention DISK WRITE or pidstat fallback
    iotop_txt = _read("iotop_top.txt")
    if iotop_txt:
        has_hdr = bool(re.search(r"Total DISK WRITE|DISK\s+WRITE\s+", iotop_txt))
        has_pidstat = bool(re.search(r"\bkB_wr/s\b", iotop_txt) and re.search(r"\bCommand\b", iotop_txt))
        has_rate = bool(re.search(r"\b([3-9]|\d{2,})(\.\d+)?\s*(M|MB|MiB)/s\b|\b\d{4,}(\.\d+)?\s*K", iotop_txt))
        s["iotop_evidence"] = 1.0 if (has_hdr or has_pidstat) and has_rate and hog_sub in iotop_txt else (0.4 if iotop_txt else 0.0)
    else:
        s["iotop_evidence"] = 0.0

    # 3. lsof + ps + proc fd evidence
    lsof_txt = _read("lsof_hog.txt")
    s["lsof_present"] = 1.0 if lsof_txt and "PID" in lsof_txt and hog_file_suffix in lsof_txt else (0.5 if lsof_txt else 0.0)
    ps_txt = _read("ps_hog.txt")
    s["ps_cmdline_match"] = 1.0 if ps_txt and hog_sub in ps_txt else (0.4 if ps_txt else 0.0)
    proc_fd = _read("proc_fd.txt")
    s["proc_fd_match"] = 1.0 if proc_fd and hog_file_suffix in proc_fd else (0.3 if proc_fd else 0.0)

    # 4. diagnosis.json: required keys + cmdline match + path match
    diag_path = rd / "diagnosis.json"
    diag_keys = 0.0; diag_cmd = 0.0; diag_path_ok = 0.0; diag_mibps = 0.0
    if diag_path.exists():
        try:
            d = json.loads(diag_path.read_text())
            req = expected.get("report_required_keys", [])
            present = sum(1 for k in req if k in d)
            diag_keys = present / max(1, len(req))
            cmdline = str(d.get("top_io_cmd", ""))
            if hog_sub in cmdline: diag_cmd = 1.0
            lf = str(d.get("largest_file_path", ""))
            if hog_file_suffix in lf and hog_dir_basename in lf:
                diag_path_ok = 1.0
            try:
                w = float(d.get("write_mibps_observed", 0))
                iot_nums = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*(?:M|MB|MiB)/s", iotop_txt)]
                iot_max = max(iot_nums) if iot_nums else 0.0
                if w >= 3.0 and iot_max >= 3.0 and abs(w - iot_max) <= max(1.5, 0.4 * iot_max):
                    diag_mibps = 1.0
                elif w >= 3.0 and iot_max >= 3.0:
                    diag_mibps = 0.5
                else:
                    diag_mibps = 0.0
            except Exception:
                pass
        except Exception:
            pass
    s["diagnosis_keys"] = diag_keys
    s["diagnosis_cmdline_match"] = diag_cmd
    s["diagnosis_path_match"] = diag_path_ok
    s["diagnosis_writerate_plausible"] = diag_mibps

    # 5. post-remediation iostat ratio
    iostat_after = _read("iostat_after.txt")
    s["iostat_after_present"] = 1.0 if iostat_after else 0.0
    def _peak_w(text):
        vals = []
        for ln in text.splitlines():
            # heuristic: numeric column near "wMB/s" rows under device names
            m = re.findall(r"\b\d+\.\d+\b", ln)
            if m and not ln.startswith("Linux") and "Device" not in ln and "avg" not in ln:
                vals.extend(float(x) for x in m)
        return max(vals) if vals else 0.0
    pre_peak = _peak_w(iostat_before)
    post_peak = _peak_w(iostat_after)
    if pre_peak > 0 and post_peak >= 0:
        ratio = (pre_peak + 0.01) / (post_peak + 0.01)
        s["remediation_iostat_drop"] = 1.0 if ratio >= drop_factor else max(0.0, min(1.0, ratio / drop_factor))
    else:
        s["remediation_iostat_drop"] = 0.4 if iostat_after else 0.0

    # 6. GUI screenshots present + size
    shots = ["view_baobab_overview.png", "view_baobab_treemap_hover.png",
             "view_files_highlighted.png", "view_baobab_after.png"]
    def _real_img(p):
        try:
            from PIL import Image
            if not p.exists() or p.stat().st_size < 40000: return False
            with Image.open(p) as im: return im.size[0] >= 800 and im.size[1] >= 600
        except Exception: return False
    present = sum(1 for n in shots if _real_img(rd / n))
    s["gui_screenshots_count"] = present / len(shots)

    # 7. OCR keyword hits
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_baobab_overview.png": ["Disk Usage", "Folder", "Size", "Contents", "Analyzer", "baobab"],
            "view_baobab_treemap_hover.png": ["MB", "MiB", "GB", hog_dir_basename, hog_file_suffix, "Treemap"],
            "view_files_highlighted.png": [hog_file_suffix, hog_dir_basename, "Files"],
            "view_baobab_after.png": ["Disk Usage", "Folder", "Size", "Analyzer", "baobab"],
        }
        for n, ks in kws.items():
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k in tx for k in ks): ocr_hits += 1
                except Exception:
                    pass
        s["gui_screenshots_ocr"] = ocr_hits / len(shots)
    except ImportError:
        s["gui_screenshots_ocr"] = 0.5

    # 8. postmortem
    pm = _read("postmortem.md")
    pm_chars = len(pm)
    s["postmortem_length"] = 1.0 if pm_chars >= 600 else pm_chars / 600.0
    pm_kws = expected.get("expected_postmortem_keywords",
                          ["rotation", "frames", "renderer", "iotop", "baobab", "lsof"])
    hits = sum(1 for k in pm_kws if k.lower() in pm.lower())
    s["postmortem_keywords"] = 1.0 if hits >= 6 else (0.6 if hits >= 5 else 0.3 if hits >= 4 else 0.0)
    required_h = ("## 时间线", "## 根因", "## 止血与彻底修复建议", "## 跨通道证据链")
    sect_hits = sum(1 for h in required_h if h in pm)
    s["postmortem_sections"] = 1.0 if sect_hits == 4 else sect_hits / 8.0

    # 9. cross-channel switches
    cc = rd / "cross_channel.json"
    cc_ok = 0.0
    if cc.exists():
        try:
            d = json.loads(cc.read_text())
            sw = int(d.get("switches", 0))
            tr = d.get("trace", [])
            need = {"STRUCT:iostat":"iostat_before.txt","STRUCT:lsof":"lsof_hog.txt",
                    "STRUCT:ps":"ps_hog.txt","STRUCT:kill":"remediation.sh",
                    "VISUAL:overview":"view_baobab_overview.png","VISUAL:treemap_hover":"view_baobab_treemap_hover.png",
                    "VISUAL:after":"view_baobab_after.png"}
            backed = sum(1 for x in tr if x in need and (rd / need[x]).exists() and (rd / need[x]).stat().st_size > 200)
            if sw >= 5 and len(tr) >= 5 and backed >= 5:
                cc_ok = 1.0
            elif backed >= 3:
                cc_ok = 0.5
        except Exception:
            pass
    s["cross_channel_switches"] = cc_ok

    # 10. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd / n) for n in shots if (rd / n).exists()]
    vlm_judge = 0.0
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_baobab_real": "至少一张截图清晰显示 GNOME Disk Usage Analyzer (baobab) 的主窗口，含左侧 folder 列表 + 中央 ring chart 或 tree-map",
            "vlm_treemap_dominant_rect": "treemap 截图里有一个矩形面积明显比其他都大（超过 60% 屏幕面积），且有 tooltip / hover 状态可见",
            "vlm_after_state_clean": "view_baobab_after.png 显示 tree-map 已经没有那块吃满全图的巨型矩形",
        }
        vlm = vlm_score_rubric(vlm_imgs[:3], rubric, instruction="评估值班 SRE 用 baobab 排查磁盘 hog 的截图。")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
        vlm_judge = sum(s.get(k, 0.0) for k in rubric) / max(1, len(rubric))
    else:
        for k in ("vlm_baobab_real", "vlm_treemap_dominant_rect", "vlm_after_state_clean"):
            s[k] = 0.5
        vlm_judge = 0.5

    nums = [v for k, v in s.items() if isinstance(v, (int, float)) and k != "judge_method"]
    base = sum(nums) / max(1, len(nums))

    # Hard gates
    has_cli = (s["iotop_evidence"] >= 0.5 and s["lsof_present"] >= 0.5
               and s["ps_cmdline_match"] >= 0.4)
    if not has_cli: base = min(base, 0.4)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the gui_screenshots_count / vlm_* sub_scores.
    # Only apply the VLM cap when the helper actually ran. Otherwise the
    # 0.5 fallback would penalise environments without _judge_helper.
    if vlm_score_rubric is not None and vlm_judge < 0.6:
        base = min(base, 0.55)
    if s.get("gui_screenshots_ocr", 0.0) < 0.5: base = min(base, 0.5)
    if s["diagnosis_path_match"] == 0 and s["diagnosis_cmdline_match"] == 0:
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
