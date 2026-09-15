# Auto-generated from WeaveBench task DSK_task_14_polkit_rule_localauth_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """polkit local auth audit grader: cross-channel evidence (CLI pkcheck
    matrix + GUI auth dialog screenshot + correct broken-rule identification
    + idempotent fix). 12 sub-scores + 3 hard gates."""
    import json, hashlib, subprocess, re
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/opt/dsk14_gt")
    s = {}

    def _ocr(p):
        try:
            from PIL import Image
            import pytesseract
            return pytesseract.image_to_string(Image.open(p))
        except Exception:
            return ""

    def _read(p, default=""):
        try: return p.read_text(errors="ignore")
        except Exception: return default

    gt = {}
    if (gt_dir / "manifest.json").exists():
        try: gt = json.loads((gt_dir / "manifest.json").read_text())
        except Exception: pass
    expected_broken = gt.get("broken_rule_file", "40-eyeson-broad.rules")
    expected_action = gt.get("leaked_action_id", "")
    red_herrings    = gt.get("red_herrings",
                             ["45-eyeson-userlist.rules", "50-eyeson-deny.rules"])

    # 1. pkaction excerpt
    p1 = rd / "pkaction_eyeson.txt"
    txt = _read(p1)
    has_three = sum(1 for a in ["org.eyeson.benchpolicy.read",
                                "org.eyeson.benchpolicy.write",
                                "org.eyeson.benchpolicy.admin"] if a in txt)
    s["pkaction_excerpt"] = has_three / 3.0 if p1.exists() else 0.0

    # 2. rules_before backups
    rb = rd / "rules_before"
    backed = 0
    for n in ["40-eyeson-broad.rules",
              "45-eyeson-userlist.rules",
              "50-eyeson-deny.rules"]:
        if (rb / n).exists() and (rb / n).stat().st_size > 50:
            backed += 1
    s["rules_backed_up"] = backed / 3.0

    # 3. pkcheck_before.tsv
    pcb = rd / "pkcheck_before.tsv"
    before_rows = []
    if pcb.exists():
        for line in pcb.read_text().splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) >= 3: before_rows.append(parts)
    need = {"org.eyeson.benchpolicy.read","org.eyeson.benchpolicy.write","org.eyeson.benchpolicy.admin"}
    allowed_rows = [r for r in before_rows if r[2].strip() == "allowed"]
    s["pkcheck_before_schema"] = 1.0 if (pcb.exists() and len(before_rows) == 3
        and {r[0] for r in before_rows} == need
        and len(allowed_rows) == 1
        and allowed_rows[0][0] == expected_action) else 0.0

    # 4 + 5. GUI screenshots OCR
    auth_kw = ["Authenticate", "Authentication", "认证", "Password",
               "口令", "密码", "授权"]
    p_dlg = rd / "view_polkit_dialog.png"
    ocr_dlg = _ocr(p_dlg).lower() if p_dlg.exists() else ""
    s["gui_dialog_before"] = 1.0 if (p_dlg.exists()
        and any(k.lower() in ocr_dlg for k in auth_kw)
        and ("polkit" in ocr_dlg or "benchpolicy" in ocr_dlg or "privilege" in ocr_dlg
             or "权限" in ocr_dlg or "认证" in ocr_dlg)) else 0.0

    p_dir = rd / "view_rules_dir.png"
    dir_ocr = _ocr(p_dir)
    hits = sum(1 for k in ("40-eyeson-broad", "45-eyeson-userlist", "50-eyeson-deny") if k in dir_ocr)
    s["gui_rules_dir"] = 1.0 if (p_dir.exists() and "rules.d" in dir_ocr and hits >= 2) else \
        (0.3 if (p_dir.exists() and hits >= 1) else 0.0)

    # 6. diagnosis.json
    diag = {}
    try: diag = json.loads((rd / "diagnosis.json").read_text())
    except Exception: pass
    diag_score = 0.0
    if diag:
        if diag.get("broken_rule_file") == expected_broken: diag_score += 0.4
        if expected_action and diag.get("leaked_action_id") == expected_action:
            diag_score += 0.4
        if diag.get("leak_kind") == gt.get("leak_kind", "implicit_yes"):
            diag_score += 0.1
        if isinstance(diag.get("red_herrings"), list) and \
           set(diag["red_herrings"]) == set(red_herrings):
            diag_score += 0.1
    s["diagnosis_correct"] = round(min(1.0, diag_score), 3)

    # 7. fixed rule content — accept any *.fixed file matching the GT broken file
    fx = rd / f"{expected_broken}.fixed"
    fx_text = _read(fx)
    auth_block = re.search(r'action\.id\s*==\s*"' + re.escape(expected_action) +
                           r'"[^}]{0,400}AUTH_ADMIN', fx_text, re.S) if fx_text else None
    fx_ok = (fx.exists() and "addRule" in fx_text
             and "polkit.Result.YES" not in fx_text
             and "NOT_HANDLED" not in fx_text
             and auth_block is not None)
    s["fixed_rule_quality"] = 1.0 if fx_ok else 0.0

    # 8. pkcheck_after.tsv: leaked action now requires auth
    pca = rd / "pkcheck_after.tsv"
    after_rows = []
    if pca.exists():
        for line in pca.read_text().splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) >= 3: after_rows.append(parts)
    after_ok = False
    if pca.exists() and len(after_rows) == 3:
        for r in after_rows:
            aid, ec, verdict = r[0], r[1], r[2]
            if expected_action and aid == expected_action and \
               verdict.strip() in ("auth_required", "not_authorized"):
                after_ok = True
        # no fallback: the leaked action MUST be the one that flipped
    s["pkcheck_after_flipped"] = 1.0 if after_ok else 0.0

    # 9. dialog after
    p_dlg2 = rd / "view_polkit_dialog_after.png"
    ocr_dlg2 = _ocr(p_dlg2).lower() if p_dlg2.exists() else ""
    s["gui_dialog_after"] = 1.0 if (p_dlg2.exists()
        and any(k.lower() in ocr_dlg2 for k in auth_kw)
        and ("polkit" in ocr_dlg2 or "benchpolicy" in ocr_dlg2 or "privilege" in ocr_dlg2
             or "权限" in ocr_dlg2 or "认证" in ocr_dlg2)) else 0.0

    # 10. summary.md
    sm = rd / "summary.md"
    sm_txt = _read(sm)
    sm_low = sm_txt.lower()
    needed = ["before", "after", expected_broken.lower(),
              expected_action.lower(), "auth_admin"]
    hit = sum(1 for k in needed if k in sm_low)
    s["summary_md"] = 1.0 if (sm.exists() and len(sm_txt) >= 350 and hit == 5) else \
        (0.4 if sm.exists() and len(sm_txt) >= 200 and hit >= 3 else 0.0)

    # 11. red herrings untouched
    untouched = 0
    for n in red_herrings:
        live = Path(f"/etc/polkit-1/rules.d/{n}")
        backup = rb / n
        if live.exists() and backup.exists():
            try:
                if hashlib.sha256(live.read_bytes()).hexdigest() == \
                   hashlib.sha256(backup.read_bytes()).hexdigest():
                    untouched += 1
            except Exception: pass
    s["red_herrings_untouched"] = untouched / max(1, len(red_herrings))

    # 12. journal_polkit log existence
    jp = rd / "journal_polkit.txt"
    s["journal_polkit"] = 1.0 if (jp.exists() and jp.stat().st_size > 50) else 0.0

    # cross-channel evidence: CLI artefact + GUI screenshot present
    cli_ev = (pcb.exists() and pca.exists() and (rd/"pkaction_eyeson.txt").exists())
    gui_ev = (p_dlg.exists() or p_dlg2.exists())
    s["cross_channel_evidence"] = 1.0 if (cli_ev and gui_ev) else 0.0

    # VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    shots = [str(p) for p in [p_dlg, p_dlg2, p_dir] if p.exists()]
    if vlm_score_rubric and shots:
        rubric = {
            "vlm_dialog_real": "图像里能看到真实桌面上的 polkit 鉴权对话框（含密码框 / Authenticate 按钮）",
            "vlm_target_action": "对话框文案与某个被 polkit 保护的 action 名相关（不是空白窗）",
            "vlm_no_terminal_fake": "不是终端伪造的文字截图，而是真桌面 GUI 渲染",
            "vlm_layout_clean": "截图布局清晰、未被裁切或遮挡",
        }
        try:
            v = vlm_score_rubric(shots[:3], rubric,
                                 instruction="评估 polkit 认证对话框截图真实性。")
            for k in rubric: s[k] = float(v.get(k, 0.0))
            s["judge_method"] = v.get("judge_method", "ok")
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_dialog_real", "vlm_target_action",
                  "vlm_no_terminal_fake", "vlm_layout_clean"]:
            s[k] = 0.5

    nums = [v for k, v in s.items()
            if isinstance(v, (int, float)) and k != "judge_method"]
    base = sum(nums) / len(nums) if nums else 0.0

    # Hard gates
    if not cli_ev:                                 base = min(base, 0.40)
    # GUI hard-cap removed: rely on per-shot VLM/OCR sub-scores instead.
    vlm_avg = sum(s.get(k, 0.0) for k in ["vlm_dialog_real",
                                          "vlm_target_action",
                                          "vlm_no_terminal_fake",
                                          "vlm_layout_clean"]) / 4.0
    if vlm_score_rubric is not None and shots and vlm_avg < 0.6:
        base = min(base, 0.60)
    if s["diagnosis_correct"] < 0.4:               base = min(base, 0.55)
    if s["pkcheck_after_flipped"] < 1.0:           base = min(base, 0.55)
    if s["red_herrings_untouched"] < 1.0:          base = min(base, 0.50)

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
