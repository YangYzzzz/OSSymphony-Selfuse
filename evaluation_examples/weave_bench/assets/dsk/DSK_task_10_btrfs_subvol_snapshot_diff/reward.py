# Auto-generated from WeaveBench task DSK_task_10_btrfs_subvol_snapshot_diff.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Btrfs reflink-aware snapshot diff grader.

    Sub-scores:
      - subvol_list / subvol_show / fs_usage / fs_du presence + content
      - send_dump structure (must contain clone + write ops)
      - changes.json schema + content alignment vs gt/expected.json
      - reflink pair detection (must include payload_alpha_clone.bin)
      - apparent > exclusive invariant (numeric)
      - 3 GUI screenshots present + OCR keyword hits
      - report.md length + keyword coverage
      - VLM rubric on file-manager Properties screenshot
    Hard gates: missing CLI artifacts cap at 0.4; missing GUI screenshots
    cap at 0.4; VLM judge < 0.6 caps at 0.6.
    """
    import json, re, os
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/opt/dsk10_gt")
    if not gt_dir.exists():
        gt_dir = Path(workspace_path or "/tmp_workspace") / "gt"
    if not gt_dir.exists():
        gt_dir = Path("/tmp_workspace/gt")
    s = {}

    expected = {}
    ej = gt_dir / "expected.json"
    if ej.exists():
        try: expected = json.loads(ej.read_text())
        except Exception: expected = {}

    def read(p):
        try: return p.read_text(errors="ignore")
        except Exception: return ""

    # 1. subvolume_list.txt — 5 subvolumes
    sl = read(rd / "subvolume_list.txt")
    sv_hits = sum(1 for x in ("data_a","data_b","data_c","snap1","snap2") if x in sl)
    s["subvol_list"] = sv_hits / 5.0

    # 2. subvolume_show — Generation, UUID lines visible
    show1 = read(rd / "subvolume_show_snap1.txt")
    show2 = read(rd / "subvolume_show_snap2.txt")
    s["subvol_show"] = (
        (1.0 if ("UUID" in show1 and "Generation" in show1) else 0.0) +
        (1.0 if ("UUID" in show2 and "Generation" in show2) else 0.0)
    ) / 2.0

    # 3. fs_usage / fs_du with three-column header
    fu = read(rd / "fs_usage.txt")
    s["fs_usage"] = 1.0 if ("Device size" in fu and "Data,single" in fu) else (0.5 if fu else 0.0)
    fd = read(rd / "fs_du_snap2.txt")
    has_three_col = bool(re.search(r"Total\s+Exclusive\s+Set shared", fd))
    has_clone_row = ("payload_alpha_clone.bin" in fd)
    s["fs_du_header"] = 1.0 if has_three_col else 0.0
    s["fs_du_clone_visible"] = 1.0 if has_clone_row else 0.0

    # 4. send_dump structure
    sd = read(rd / "send_dump.txt")
    has_clone_op  = len(re.findall(r"^clone\s.+len=\d+", sd, re.M)) >= 1
    has_write_op  = len(re.findall(r"^(write|update_extent)\s.+len=\d+", sd, re.M)) >= 2
    has_mkfile_op = bool(re.search(r"^mkfile\s+.*payload_alpha_clone", sd))
    clone_bytes   = sum(int(m.group(1)) for m in re.finditer(r"^clone\s.+len=(\d+)", sd, re.M))
    has_mkfile = bool(re.search(r"^(mkfile|link)\s", sd, re.M))
    s["send_dump_clone"] = 1.0 if (has_clone_op and clone_bytes >= 20_000_000 and has_mkfile_op) else 0.0
    s["send_dump_write"] = 1.0 if has_write_op else 0.0
    s["send_dump_size"]  = 1.0 if len(sd) >= 4000 else len(sd)/4000.0

    # 5. changes.json schema + content alignment
    cj_path = rd / "changes.json"
    cj = {}
    if cj_path.exists():
        try: cj = json.loads(cj_path.read_text())
        except Exception: cj = {}
    required_keys = {"subvolumes","added","modified","removed",
                     "reflink_pairs","snap2_apparent_bytes",
                     "snap2_exclusive_bytes","snap2_shared_bytes","evidence"}
    s["changes_schema"] = 1.0 if required_keys.issubset(cj.keys()) else \
                          (len(required_keys & set(cj.keys())) / len(required_keys))

    def setify(xs):
        return set(os.path.basename(str(x)).strip() for x in (xs or []) if x)

    exp_changes = expected.get("changes_snap1_to_snap2", {})
    add_score = mod_score = rm_score = 0.0
    for key, score_key in [("added","added"),("modified","modified"),("removed","removed")]:
        ag = setify(cj.get(key, []))
        gt = setify(exp_changes.get(key, []))
        if not gt: continue
        inter = ag & gt
        precision = len(inter) / max(len(ag), 1)
        recall = len(inter) / len(gt)
        f1 = 0.0 if (precision + recall) == 0 else 2*precision*recall/(precision+recall)
        if key == "added":    add_score = f1
        if key == "modified": mod_score = f1
        if key == "removed":  rm_score = f1
    s["changes_added"]    = add_score
    s["changes_modified"] = mod_score
    s["changes_removed"]  = rm_score

    # 6. reflink_pairs hit
    reflink_hit = 0.0
    for pair in cj.get("reflink_pairs", []) or []:
        try:
            a, b = (os.path.basename(str(pair[0])), os.path.basename(str(pair[1])))
            names = {a, b}
            if "payload_alpha.bin" in names and "payload_alpha_clone.bin" in names:
                reflink_hit = 1.0; break
        except Exception: pass
    s["reflink_pair_detected"] = reflink_hit

    # 7. numeric invariant: exclusive < apparent (the whole point of the task)
    try:
        ap = int(cj.get("snap2_apparent_bytes", 0))
        ex = int(cj.get("snap2_exclusive_bytes", 0))
        sh = int(cj.get("snap2_shared_bytes", 0))
        sh_min = int(expected.get("expected_shared_bytes_snap2_min", 30_000_000))
        invariant = (ap > ex > 0) and (sh >= sh_min) and (ap - ex) >= 25_000_000 and (ap == ex + sh or abs(ap-(ex+sh)) <= ap*0.15)
        magnitude_ok = (1.1e8 <= ap <= 2.5e8) and (ex <= 8e7) and (sh >= sh_min)
        s["numeric_invariant"] = 1.0 if invariant else 0.0
        s["numeric_magnitude"] = 1.0 if magnitude_ok else 0.5 if invariant else 0.0
    except Exception:
        s["numeric_invariant"] = 0.0
        s["numeric_magnitude"] = 0.0

    return _finalise_btrfs(s, rd, cj, expected)


def _finalise_btrfs(s, rd, cj, expected):
    import re
    from pathlib import Path
    # 8. GUI screenshots present + OCR
    gui_shots = [
        "view_nautilus_snap1.png",
        "view_nautilus_snap2.png",
        "view_terminal_du.png",
    ]
    present = sum(1 for n in gui_shots if (rd/n).exists())
    s["gui_shots_present"] = present / len(gui_shots)
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_nautilus_snap1.png": [["Properties","属性"], ["snap1","payload_alpha","payload_beta"]],
            "view_nautilus_snap2.png": [["Properties","属性"], ["payload_alpha_clone"]],
            "view_terminal_du.png":    [["Total"], ["Exclusive"], ["Set shared"], ["alpha_clone"]],
        }
        ocr_hits = 0
        for n, groups in kws.items():
            p = rd/n
            if not p.exists(): continue
            try: tx = pytesseract.image_to_string(Image.open(p)).lower()
            except Exception: tx = ""
            if all(any(k.lower() in tx for k in grp) for grp in groups): ocr_hits += 1
        s["gui_shots_ocr"] = ocr_hits / len(gui_shots)
    except ImportError:
        s["gui_shots_ocr"] = 0.5

    # 9. report.md length + keywords
    rm = (rd/"report.md")
    rt = rm.read_text(errors="ignore") if rm.exists() else ""
    s["report_length"] = 1.0 if len(rt) >= 400 else len(rt)/400.0
    kw_needed = ["reflink","extent","exclusive","shared","apparent","snapshot","payload_alpha_clone"]
    kw_hits = sum(1 for k in kw_needed if k.lower() in rt.lower())
    has_num = bool(re.search(r"\b\d{2,}\s*(MiB|MB|bytes|B)\b", rt))
    s["report_keywords"] = (kw_hits/len(kw_needed)) * (1.0 if has_num else 0.5)

    # 10. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_judge = None
    imgs = [str(rd/n) for n in (
        "view_nautilus_snap1.png","view_nautilus_snap2.png","view_terminal_du.png"
    ) if (rd/n).exists()]
    if vlm_score_rubric and imgs:
        rubric = {
            "vlm_nautilus_window":  "截图里能看到文件管理器窗口与文件列表",
            "vlm_properties_dlg":   "至少一张截图里出现 Properties / 属性 对话框且含 Size 字段",
            "vlm_terminal_three_col": "终端截图里能看到 Total / Exclusive / Set shared 三列",
            "vlm_evidence_authentic": "截图明显是真实桌面会话(有窗口装饰、光标、状态栏),不是拼接图",
        }
        try:
            vlm = vlm_score_rubric(imgs[:3], rubric,
                instruction="评估 Btrfs reflink 快照差异审计任务的 GUI 取证截图。")
            for k in rubric: s[k] = vlm.get(k, 0.0)
            vlm_judge = sum(s.get(k,0.0) for k in rubric) / len(rubric)
        except Exception:
            for k in rubric: s[k] = 0.0
            vlm_judge = 0.0

    # Aggregate
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums) / max(len(nums), 1)

    has_cli_evidence = (rd/"send_dump.txt").exists() and (rd/"fs_du_snap2.txt").exists() \
                       and len((rd/"fs_du_snap2.txt").read_text(errors="ignore")) > 50
    has_gui_screenshot = any((rd/n).exists() for n in
        ("view_nautilus_snap1.png","view_nautilus_snap2.png","view_terminal_du.png"))

    if not has_cli_evidence:    base = min(base, 0.4)
    # GUI hard-cap removed: rely on per-shot VLM/OCR sub-scores instead.
    if vlm_score_rubric is not None and vlm_judge is not None and vlm_judge < 0.6:
        base = min(base, 0.6)
    if s.get("vlm_properties_dlg",1.0) < 0.6 or s.get("vlm_terminal_three_col",1.0) < 0.6:
        base = min(base, 0.55)
    if s.get("gui_shots_ocr",0.0) < 0.34:  base = min(base, 0.6)
    try:
        _sl_txt = (rd/"subvolume_list.txt").read_text(errors="ignore") if (rd/"subvolume_list.txt").exists() else ""
    except Exception:
        _sl_txt = ""
    if not re.search(r"ID\s+\d+\s+gen\s+\d+", _sl_txt or ""): base = min(base, 0.6)
    if s.get("changes_schema",0) < 1.0: base = min(base, 0.7)
    if s.get("numeric_invariant",0) == 0.0: base = min(base, 0.65)
    if s.get("reflink_pair_detected",0) == 0.0: base = min(base, 0.7)

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
