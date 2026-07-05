# Auto-generated from WeaveBench task WEB_task_4_a11y_axe_aria_fix.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """A11y axe-cli + Chrome Accessibility tree + ARIA fix grader."""
    import json, re, subprocess
    from pathlib import Path
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        pytesseract = None
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    gt = workspace / "gt"
    s = {}

    # 1. axe_initial.json violations count
    ai = rd / "axe_initial.json"
    initial_violations = 0
    if ai.exists():
        try:
            data = json.loads(ai.read_text())
            vlist = data if isinstance(data, list) else data.get("violations", [])
            initial_violations = len(vlist)
            s["axe_initial_violations"] = 1.0 if initial_violations >= 6 else initial_violations / 6.0
        except Exception:
            s["axe_initial_violations"] = 0.0
    else:
        s["axe_initial_violations"] = 0.0

    # 2. axe_initial_summary.md
    ais = rd / "axe_initial_summary.md"
    if ais.exists():
        txt = ais.read_text(errors="ignore")
        impact_hits = sum(1 for k in ["critical", "serious", "moderate", "minor"] if k in txt.lower())
        has_rule_id = bool(re.search(r"(image-alt|label|color-contrast|link-name|button-name|aria-|region)", txt))
        has_selector = "#" in txt or "." in txt
        if len(txt) >= 200 and impact_hits >= 2 and has_rule_id and has_selector:
            s["initial_summary"] = 1.0
        elif len(txt) >= 100 and impact_hits >= 1:
            s["initial_summary"] = 0.5
        else:
            s["initial_summary"] = 0.2
    else:
        s["initial_summary"] = 0.0

    # 3-5, 10-11. GUI screenshots OCR
    shot_kws = {
        "view_a11y_tree_overview.png": ["Accessibility", "Role", "Name", "Tree"],
        "view_a11y_violation_node.png": ["img", "textbox", "Role", "Name", "Accessibility"],
        "view_a11y_contrast_issue.png": ["Contrast", "ratio", "AA", "color"],
        "view_a11y_tree_fixed.png": ["Accessibility", "Role", "Name", "Tree"],
        "view_a11y_fixed_node.png": ["Role", "Name", "Accessibility", "button", "img"],
        "view_lighthouse_a11y_score.png": ["Accessibility", "Lighthouse", "Performance"],
    }
    shots_present = 0
    ocr_hits = 0
    lighthouse_score_ok = False
    for name, kws_list in shot_kws.items():
        p = rd / name
        # 占位文件 (<5KB) 不算真截图
        if p.exists() and p.stat().st_size >= 5 * 1024:
            shots_present += 1
            if pytesseract:
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in kws_list):
                        ocr_hits += 1
                    if name == "view_lighthouse_a11y_score.png":
                        if re.search(r"\b(8[5-9]|9\d|100)\b", tx):
                            lighthouse_score_ok = True
                except Exception:
                    pass
    s["lighthouse_score_ge_85"] = 1.0 if lighthouse_score_ok else (0.5 if not pytesseract else 0.0)
    s["gui_shots_present"] = shots_present / len(shot_kws)
    s["gui_shots_ocr"] = ocr_hits / len(shot_kws) if pytesseract else 0.5

    # 6. a11y_tree_snapshot.json
    ats = rd / "a11y_tree_snapshot.json"
    if ats.exists():
        try:
            snap = json.loads(ats.read_text())
            required = {"selector", "role", "name", "issue"}
            valid = [e for e in snap if isinstance(e, dict) and required <= set(e.keys())]
            s["tree_snapshot"] = 1.0 if len(valid) >= 5 else len(valid) / 5.0
        except Exception:
            s["tree_snapshot"] = 0.0
    else:
        s["tree_snapshot"] = 0.0

    # 7. a11y_app_fixed/ exists with substantial changes
    fixed_dir = workspace / "a11y_app_fixed"
    fixed_html = fixed_dir / "index.html"
    orig_html = workspace / "a11y_app/index.html"
    if fixed_html.exists() and orig_html.exists():
        try:
            diff_out = subprocess.run(
                ["diff", "-u", str(orig_html), str(fixed_html)],
                capture_output=True, text=True, timeout=10
            )
            diff_lines = len([l for l in diff_out.stdout.splitlines() if l.startswith('+') or l.startswith('-')])
            s["fixed_dir_diff"] = 1.0 if diff_lines >= 10 else diff_lines / 10.0
        except Exception:
            s["fixed_dir_diff"] = 0.5 if fixed_html.exists() else 0.0
    else:
        s["fixed_dir_diff"] = 0.0

    # 8. axe_fixed.json — fewer violations than initial
    af = rd / "axe_fixed.json"
    fixed_violations = 999
    if af.exists():
        try:
            data = json.loads(af.read_text())
            vlist = data if isinstance(data, list) else data.get("violations", [])
            fixed_violations = len(vlist)
        except Exception:
            pass
    reduction = initial_violations - fixed_violations
    s["violation_reduction"] = 1.0 if reduction >= 4 else (reduction / 4.0 if reduction > 0 else 0.0)

    # 9. axe_diff_summary.md
    ads = rd / "axe_diff_summary.md"
    if ads.exists():
        txt = ads.read_text(errors="ignore")
        has_compare = any(k in txt.lower() for k in ["before", "after", "修复前", "修复后", "fixed", "remaining"])
        s["diff_summary"] = 1.0 if (len(txt) >= 50 and has_compare) else 0.3
    else:
        s["diff_summary"] = 0.0

    # 12. a11y_compliance_report.md
    rpt = rd / "a11y_compliance_report.md"
    if rpt.exists():
        txt = rpt.read_text(errors="ignore")
        has_wcag = any(k in txt for k in ["WCAG", "1.1.1", "1.4.3", "4.1.2", "2.1.1"])
        has_table = "|" in txt and "---" in txt
        s["report_quality"] = 1.0 if (len(txt) >= 200 and has_wcag and has_table) else 0.3
    else:
        s["report_quality"] = 0.0

    # 13. fix.patch
    patch = rd / "fix.patch"
    if patch.exists():
        txt = patch.read_text(errors="ignore")
        # 真正的 unified diff 必须含 +/- 行与 hunk header
        has_hunk = "@@" in txt
        plus_lines = sum(1 for l in txt.splitlines() if l.startswith("+") and not l.startswith("+++"))
        minus_lines = sum(1 for l in txt.splitlines() if l.startswith("-") and not l.startswith("---"))
        if len(txt) >= 200 and has_hunk and plus_lines >= 5 and minus_lines >= 5:
            s["patch_exists"] = 1.0
        elif len(txt) >= 50:
            s["patch_exists"] = 0.4
        else:
            s["patch_exists"] = 0.2
    else:
        s["patch_exists"] = 0.0

    # numeric agreement with gt
    if (gt / "expected.json").exists():
        try:
            exp = json.loads((gt / "expected.json").read_text())
            hits = 0
            total = 0
            if "min_initial_violations" in exp:
                total += 1
                if initial_violations >= exp["min_initial_violations"]:
                    hits += 1
            if "expected_fixed_rules" in exp and af.exists():
                total += 1
                data = json.loads(af.read_text())
                vlist = data if isinstance(data, list) else data.get("violations", [])
                remaining_ids = {v.get("id", "") for v in vlist}
                fixed_rules = set(exp["expected_fixed_rules"])
                actually_fixed = fixed_rules - remaining_ids
                if len(actually_fixed) >= len(fixed_rules) * 0.6:
                    hits += 1
            if "expected_post_fix_max_violations" in exp and af.exists():
                total += 1
                if fixed_violations <= exp["expected_post_fix_max_violations"]:
                    hits += 1
            s["numeric_agreement"] = hits / total if total else 0.0
        except Exception:
            s["numeric_agreement"] = 0.0
    else:
        s["numeric_agreement"] = 0.5

    # VLM judge
    if vlm_score_rubric:
        imgs = [str(rd / n) for n in shot_kws if (rd / n).exists()][:4]
        if imgs:
            rubric = {
                "vlm_a11y_tree_real": "至少一张截图清晰显示 Chrome DevTools Accessibility Tree（树形节点列表含 Role/Name 列）",
                "vlm_violation_highlight": "至少一张截图显示选中了一个有无障碍问题的 DOM 元素，且右侧面板显示其属性",
                "vlm_lighthouse_score": "截图显示 Lighthouse Accessibility 审计分数圆环",
                "vlm_before_after": "能看到修复前后 Accessibility Tree 的差异",
            }
            vlm = vlm_score_rubric(imgs, rubric,
                instruction="评估 Chrome DevTools Accessibility 面板和 Lighthouse 审计截图的真实性和信息完整度。")
            for k in rubric:
                s[k] = vlm.get(k, 0.0)
            s["judge_method"] = vlm.get("judge_method", "failed")

    # --- GUI hard-gate sub-score: 真实浏览器交互信号 ---
    import hashlib
    trajectory_shots = [
        "view_a11y_tree_overview.png",
        "view_a11y_violation_node.png",
        "view_a11y_contrast_issue.png",
        "view_a11y_tree_fixed.png",
        "view_a11y_fixed_node.png",
        "view_lighthouse_a11y_score.png",
    ]
    shot_paths = [rd / n for n in trajectory_shots if (rd / n).exists()]
    gui_signal = 0.0
    if len(shot_paths) >= 3:
        hashes = {hashlib.md5(p.read_bytes()).hexdigest() for p in shot_paths}
        uniq_ratio = len(hashes) / len(shot_paths)
        # v2 收紧：要求所有截图 md5 互不相同（uniq_ratio == 1.0）
        uniq_score = 1.0 if uniq_ratio >= 1.0 else (0.6 if uniq_ratio >= 0.8 else uniq_ratio * 0.5)
        common_res = {(1920, 1080), (1366, 768), (1440, 900), (1536, 864),
                      (1680, 1050), (1280, 800), (1280, 720), (2560, 1440),
                      (1600, 900), (1920, 1200)}
        res_hits = 0
        try:
            for p in shot_paths:
                with Image.open(p) as im:
                    w, h = im.size
                if (w, h) in common_res or (w >= 1200 and h >= 700 and 1.2 <= w / h <= 2.4):
                    res_hits += 1
        except Exception:
            pass
        res_score = res_hits / len(shot_paths)
        chrome_kw = [
            "DevTools", "Elements", "Console", "Network", "Sources",
            "Application", "Performance", "Accessibility", "Lighthouse",
            "Issues", "Audits", "Computed", "Styles", "Properties",
            "Contrast", "ARIA", "Role", "Name",
            "http://", "https://", "localhost", "127.0.0.1",
        ]
        chrome_hits = 0
        if pytesseract:
            for p in shot_paths:
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if sum(1 for k in chrome_kw if k.lower() in tx.lower()) >= 2:
                        chrome_hits += 1
                except Exception:
                    pass
            chrome_score = chrome_hits / len(shot_paths)
        else:
            chrome_score = 0.5
        gui_signal = uniq_score * 0.4 + res_score * 0.3 + chrome_score * 0.3
    s["gui_real_interaction"] = round(gui_signal, 3)

    # Aggregate — v2 加权：核心交付 60% / GUI 证据 30% / 辅助 10%
    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vals) / len(vals) if vals else 0.0

    core_keys = [
        "axe_initial_violations", "violation_reduction", "fixed_dir_diff",
        "tree_snapshot", "report_quality", "patch_exists",
        "initial_summary", "diff_summary", "numeric_agreement",
    ]
    gui_keys = [
        "gui_shots_present", "gui_shots_ocr", "gui_real_interaction",
        "lighthouse_score_ge_85",
    ]
    vlm_keys = [k for k in s if k.startswith("vlm_")]
    aux_keys = vlm_keys

    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys) if aux_keys else 0.5

    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Hard gates — v2 收紧
    # 没有真实 GUI 信号：分级封顶
    gui_sig = s.get("gui_real_interaction", 0)
    if gui_sig < 0.4:
        base = min(base, 0.30)
    elif gui_sig < 0.6:
        base = min(base, 0.40)
    if s.get("gui_shots_present", 0) < 0.5:
        base = min(base, 0.40)
    if s.get("axe_initial_violations", 0) == 0:
        base = min(base, 0.35)
    if s.get("fixed_dir_diff", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("tree_snapshot", 0) < 0.5:
        base = min(base, 0.5)
    if s.get("violation_reduction", 0) == 0:
        base = min(base, 0.45)
    if s.get("patch_exists", 0) < 0.5:
        base = min(base, 0.55)
    if s.get("report_quality", 0) < 0.5:
        base = min(base, 0.55)
    # VLM 不可用时 / 退化路径封顶 0.6（避免无 VLM 也满分）
    if s.get("judge_method", "ok") == "failed" or not vlm_keys:
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
