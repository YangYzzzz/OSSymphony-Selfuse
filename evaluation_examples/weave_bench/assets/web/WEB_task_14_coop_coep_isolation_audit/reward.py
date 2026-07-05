# Auto-generated from WeaveBench task WEB_task_14_coop_coep_isolation_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """COOP/COEP × crossOriginIsolated grader (12 sub-scores + 3 hard gates)."""
    import json, re
    from pathlib import Path
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    try:
        import pytesseract
        from PIL import Image
    except Exception:
        pytesseract = None
        Image = None

    rd = Path("/tmp_workspace/results")
    # GT lives at root-only /opt/web14_gt; warmup moves it off the
    # agent-visible /tmp_workspace/gt to prevent answer leakage.
    gt_path = (Path("/opt/web14_gt/expected.json")
               if Path("/opt/web14_gt/expected.json").exists()
               else Path("/tmp_workspace/gt/expected.json"))
    expected = {}
    if gt_path.exists():
        try:
            expected = json.loads(gt_path.read_text())
        except Exception:
            expected = {}

    s = {}

    def _read(p):
        try:
            return p.read_text(errors="ignore")
        except Exception:
            return ""

    def _has_header(text, name, value_re=None):
        rx = re.compile(rf"(?im)^\s*{re.escape(name)}\s*:\s*(.+)$")
        for m in rx.finditer(text):
            v = m.group(1).strip()
            if value_re is None:
                return True, v
            if re.search(value_re, v, re.I):
                return True, v
        return False, None

    # 1. header_audit.json structure + correctness
    aud_p = rd / "header_audit.json"
    aud = {}
    if aud_p.exists():
        try:
            aud = json.loads(_read(aud_p))
        except Exception:
            aud = {}
    aud_keys = {"main", "widget", "static", "thirdp"}
    has_keys = aud_keys.issubset(set(aud.keys()))
    needs_hits = 0
    if has_keys:
        expect_nc = {"main": {"Cross-Origin-Opener-Policy"},
                     "widget": {"Cross-Origin-Resource-Policy"},
                     "static": {"Cross-Origin-Resource-Policy"},
                     "thirdp": {"Cross-Origin-Resource-Policy"}}
        for k in aud_keys:
            got = {h.split(":")[0].strip() for h in (aud.get(k, {}) or {}).get("needs_change", []) if isinstance(h, str)}
            if expect_nc[k].issubset(got):
                needs_hits += 1
    s["audit_structure"] = 1.0 if has_keys else 0.0
    s["audit_completeness"] = needs_hits / 4.0

    # 2. before-curl files exist and contain header-ish lines
    before_files = [
        "curl_main_before.txt", "curl_3p_before.txt",
        "curl_widget_before.txt", "curl_static_before.txt",
    ]
    bf_present = sum(1 for n in before_files if (rd / n).exists())
    s["curl_before_present"] = bf_present / len(before_files)
    bf_header_hits = 0
    for n in before_files:
        t = _read(rd / n)
        if re.search(r"(?im)^\s*HTTP/", t) and re.search(r"(?im)^\s*Cross-Origin-", t):
            bf_header_hits += 1
    s["curl_before_header_grep"] = bf_header_hits / len(before_files)

    # 3. GUI screenshots before-side
    gui_before = [
        "view_01_banner_before.png",
        "view_02_devtools_app_frames.png",
        "view_03_devtools_console_sab_error.png",
        "view_04_devtools_network_3p.png",
    ]
    gb_present = sum(1 for n in gui_before if (rd / n).exists())
    s["gui_before_present"] = gb_present / len(gui_before)

    ocr_keywords = re.compile(
        r"(crossOriginIsolated|isolated|COEP|COOP|Frames|Application|SharedArray|Network|Console|Cross-Origin)",
        re.I,
    )
    gb_ocr = 0
    if pytesseract and Image:
        for n in gui_before:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if ocr_keywords.search(tx):
                        gb_ocr += 1
                except Exception:
                    pass
    s["gui_before_ocr"] = gb_ocr / len(gui_before) if pytesseract else 0.5

    # 4. patch.diff exists and references the three fixture files
    diff_text = _read(rd / "patch.diff")
    diff_hunks = len(re.findall(r"(?m)^@@ ", diff_text))
    touched = set(re.findall(r"(?m)^\+\+\+ [ab]?/?(\S+)", diff_text))
    needed = {"Caddyfile", "server.py"}
    hit = sum(1 for n in needed if any(n in p for p in touched))
    s["patch_diff"] = (hit / 2.0) if (diff_hunks >= 2 and hit >= 1) else 0.0

    # 5. after-curl correctness
    after_main = _read(rd / "curl_main_after.txt")
    after_widget = _read(rd / "curl_widget_after.txt")
    after_static = _read(rd / "curl_static_after.txt")
    after_3p = _read(rd / "curl_3p_after.txt")

    main_coop_ok, main_coop_v = _has_header(
        after_main, "Cross-Origin-Opener-Policy", r"^same-origin\s*$"
    )
    s["fix_main_coop"] = 1.0 if main_coop_ok else 0.0
    main_coep_ok, _ = _has_header(
        after_main, "Cross-Origin-Embedder-Policy", r"require-corp|credentialless"
    )
    s["fix_main_coep"] = 1.0 if main_coep_ok else 0.0

    widget_corp_ok, _ = _has_header(
        after_widget, "Cross-Origin-Resource-Policy", r"^(same-origin|same-site)\s*$"
    )
    s["fix_widget_corp"] = 1.0 if widget_corp_ok else 0.0

    static_corp_ok, _ = _has_header(
        after_static, "Cross-Origin-Resource-Policy", r"^(same-origin|same-site)\s*$"
    )
    s["fix_static_corp"] = 1.0 if static_corp_ok else 0.0

    tp_corp_ok, tp_corp_v = _has_header(
        after_3p, "Cross-Origin-Resource-Policy", r"cross-origin"
    )
    s["fix_3p_corp"] = 1.0 if tp_corp_ok else 0.0

    # 6. after GUI
    after_banner = rd / "view_05_banner_after.png"
    after_frames = rd / "view_06_devtools_app_frames_after.png"
    s["gui_after_present"] = (
        (1.0 if after_banner.exists() else 0.0)
        + (1.0 if after_frames.exists() else 0.0)
    ) / 2.0

    after_ocr_hits = 0
    after_ocr_total = 0
    if pytesseract and Image:
        for p, want in [
            (after_banner, re.compile(r"isolated|true|STATUS", re.I)),
            (after_frames, re.compile(r"Cross-Origin\s*Isolated|Yes|true", re.I)),
        ]:
            after_ocr_total += 1
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if want.search(tx):
                        after_ocr_hits += 1
                except Exception:
                    pass
        s["gui_after_ocr"] = after_ocr_hits / max(1, after_ocr_total)
    else:
        s["gui_after_ocr"] = 0.5

    # 7. report.md depth
    rep = _read(rd / "report.md")
    rep_lines = len([ln for ln in rep.splitlines() if ln.strip()])
    rep_subhead = len(re.findall(r"(?m)^###\s+\S", rep))
    kw_hits = sum(1 for kw in ("COOP", "COEP", "CORP", "same-origin", "require-corp", "cross-origin") if re.search(kw, rep, re.I))
    origin_hits = sum(1 for kw in ("widget", "static", "9090", "3p", "third") if re.search(kw, rep, re.I))
    s["report_depth"] = 1.0 if (rep_lines >= 30 and rep_subhead >= 3 and kw_hits >= 5 and origin_hits >= 3) else (
        0.5 if rep_lines >= 20 and kw_hits >= 3 else 0.0
    )

    # 8. VLM rubric
    sample_imgs = [str(rd / n) for n in (
        "view_01_banner_before.png",
        "view_02_devtools_app_frames.png",
        "view_05_banner_after.png",
        "view_06_devtools_app_frames_after.png",
    ) if (rd / n).exists()][:4]

    if vlm_score_rubric and sample_imgs:
        rubric = {
            "vlm_real_browser": "至少一张截图清晰展示 Chromium 浏览器渲染的 SAB demo 页面（含 banner 与 dl/dd 表）",
            "vlm_devtools_open": "至少一张截图打开了 DevTools，并能看到 Application 或 Console 面板的真实 UI",
            "vlm_isolated_yes": "after 截图能看到 'isolated' / 'Yes' / 'true' 这类正向状态文字",
        }
        try:
            vlm = vlm_score_rubric(sample_imgs, rubric,
                                   instruction="评估 COOP/COEP cross-origin-isolated 取证截图。")
        except Exception:
            vlm = {}
        for k in rubric:
            s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
        vlm_avg = sum(vlm.get(k, 0) for k in rubric) / len(rubric) if vlm else 0.0
    else:
        vlm_avg = 0.5

    # base
    numerics = [v for k, v in s.items()
                if isinstance(v, (int, float)) and k != "judge_method"]
    base = sum(numerics) / max(1, len(numerics))
    overall = round((base + vlm_avg) / 2.0, 3) if vlm_score_rubric else round(base, 3)

    # hard gates
    has_cli_evidence = (
        bf_present == 4
        and all((rd / f"curl_{x}_after.txt").exists()
                for x in ("main", "widget", "static", "3p"))
        and (rd / "header_audit.json").exists()
        and (rd / "patch.diff").exists()
    )
    has_gui_screenshot = (gb_present == 4 and after_banner.exists() and after_frames.exists())
    if not has_cli_evidence:
        overall = round(min(overall, 0.4), 3)
    # GUI-path scoring axis removed: missing screenshots already cost
    # the screenshots / OCR / vlm_* sub-scores.
    if vlm_score_rubric and vlm_avg < 0.6:
        overall = round(min(overall, 0.6), 3)
    if vlm_score_rubric and s.get("vlm_isolated_yes", 0) < 0.6:
        overall = round(min(overall, 0.5), 3)

    s["overall_score"] = overall
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
