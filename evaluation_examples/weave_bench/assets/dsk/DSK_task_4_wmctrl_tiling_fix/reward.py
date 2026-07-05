# Auto-generated from WeaveBench task DSK_task_4_wmctrl_tiling_fix.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DSK_task_4 grader v2. Empty → 0.000. Weighted: core 0.6 / gui 0.3 / aux 0.1. Multi-tier hard gates."""
    import json, re, hashlib
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. CLI artifacts
    cli_files = ["screen_geom.txt","tile_run.log","wmctrl_after_tile.txt","wmctrl_after_fix.txt","window_types.txt","tile_backup.sh"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 3

    # 2. layout_violations.json
    lv_score = 0.0
    lv = rd / "layout_violations.json"
    if lv.exists():
        try:
            d = json.loads(lv.read_text())
            v = d.get("violations", d) if isinstance(d, dict) else d
            if isinstance(v, list) and len(v) >= 3: lv_score = 1.0
            elif isinstance(v, list) and len(v) >= 1: lv_score = 0.5
        except Exception: pass
    s["layout_violations"] = lv_score

    # 3. bug_findings.md
    bf_score = 0.0
    bf = rd / "bug_findings.md"
    if bf.exists():
        try:
            txt = bf.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80 and re.search(r"\.sh:\d+", p)]
            bf_score = min(1.0, len(parags) / 3)
        except Exception: pass
    s["bug_findings"] = bf_score

    # 4. GUI screenshots (count + size sanity + md5 uniqueness anti-cheat)
    gui_shots = ["view_screen_broken.png","view_screen_fixed.png","view_terminal_wmctrl.png"]
    gui_present = sum(1 for n in gui_shots if (rd / n).exists())
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui = gui_present >= 2
    # 4b. screenshot anti-cheat: each ≥ 5KB and md5 distinct
    sizes_ok = 0
    md5s = set()
    for n in gui_shots:
        p = rd / n
        if p.exists() and p.stat().st_size >= 5 * 1024:
            sizes_ok += 1
            try:
                md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception:
                pass
    s["gui_screenshots_quality"] = (sizes_ok / len(gui_shots)) * (1.0 if len(md5s) == sizes_ok and sizes_ok > 0 else 0.5 if md5s else 0.0)

    try:
        import pytesseract
        from PIL import Image
        kws_any = ["Terminal","gedit","Firefox","Files","Nautilus","wmctrl","Activities"]
        ocr_hits = 0
        for n in gui_shots:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k in tx for k in kws_any): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
    except Exception:
        s["gui_screenshots_ocr"] = 0.5 if gui_present > 0 else 0.0

    # 5. verify_output.txt
    vo_score = 0.0
    vo = rd / "verify_output.txt"
    if vo.exists():
        try:
            txt = vo.read_text()
            has_overlap = bool(re.search(r"overlap\s*=\s*0", txt))
            has_quad   = bool(re.search(r"windows_in_quadrant\s*=\s*4", txt))
            has_allok  = "ALL OK" in txt
            if has_overlap and has_quad and has_allok: vo_score = 1.0
            elif has_overlap and has_allok: vo_score = 0.8
            elif has_overlap: vo_score = 0.6
        except Exception: pass
    s["verify_pass"] = vo_score

    # 6. tiling_report.md
    rp_score = 0.0
    rp = rd / "tiling_report.md"
    if rp.exists():
        try:
            txt = rp.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            rp_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["tiling_report"] = rp_score

    # 7. VLM rubric — fixed vs broken
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    if vlm_score_rubric and (rd / "view_screen_fixed.png").exists():
        rubric = {
            "vlm_fixed_2x2_grid": "fixed 截图能看到 4 个窗口排成清晰 2x2 网格",
            "vlm_no_offscreen": "fixed 截图里没有窗口跑出屏幕外",
            "vlm_no_overlap": "fixed 截图里 4 窗口之间没有明显重叠",
            "vlm_broken_vs_fixed_diff": "broken 截图明显比 fixed 截图杂乱(窗口位置错乱)",
        }
        try:
            imgs = [str(rd / "view_screen_fixed.png")]
            if (rd / "view_screen_broken.png").exists(): imgs.append(str(rd / "view_screen_broken.png"))
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 4 窗口 2x2 tile 截图,broken vs fixed 对比。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_fixed_2x2_grid","vlm_no_offscreen","vlm_no_overlap","vlm_broken_vs_fixed_diff"]:
            s[k] = 0.0

    # 8. Content-reality sub-scores
    # 8a. wmctrl_after_fix.txt: >= 4 window lines with -G geometry columns
    waf = rd / "wmctrl_after_fix.txt"
    if waf.exists():
        try:
            wtxt = waf.read_text()
            geom_lines = re.findall(r"(?m)^0x[0-9a-fA-F]+\s+\S+\s+\d+\s+\d+\s+\d+\s+\d+", wtxt)
            if len(geom_lines) >= 4:
                s["wmctrl_after_4_windows"] = 1.0
            else:
                s["wmctrl_after_4_windows"] = round(len(geom_lines) / 4.0, 3)
        except Exception:
            s["wmctrl_after_4_windows"] = 0.0
    else:
        s["wmctrl_after_4_windows"] = 0.0

    # 8b. fixed tile script present and non-trivial
    fix_score = 0.0
    for cand in ("fixed_tile.sh", "tile_fixed.sh", "tile.sh.fixed", "patch.diff"):
        p = rd / cand
        if p.exists() and p.stat().st_size > 100:
            fix_score = 1.0
            break
        elif p.exists() and p.stat().st_size > 0:
            fix_score = max(fix_score, 0.5)
    s["fixed_script_present"] = fix_score

    # 8d. check_layout.py present (Prompt deliverable #6)
    cl = rd / "check_layout.py"
    s["check_layout_present"] = 1.0 if (cl.exists() and cl.stat().st_size > 50) else 0.0

    # 8c. quadrant coverage v2: split via median of observed x/y; require 4 distinct quadrants
    # AND check expected window names land in distinct buckets matching layout.json zones.
    quad_score = 0.0
    quad_match_score = 0.0
    if waf.exists():
        try:
            wtxt = waf.read_text()
            # wmctrl -lG line: WID DESK X Y W H HOST TITLE...
            line_re = re.compile(r"^(0x[0-9a-fA-F]+)\s+\S+\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+\S+\s+(.*)$", re.M)
            entries = []
            for m in line_re.finditer(wtxt):
                entries.append((m.group(1), int(m.group(2)), int(m.group(3)),
                                int(m.group(4)), int(m.group(5)), m.group(6).strip()))
            if entries:
                xs = sorted(int(e[1] + e[3] / 2) for e in entries)
                ys = sorted(int(e[2] + e[4] / 2) for e in entries)
                mx = xs[len(xs) // 2] if xs else 0
                my = ys[len(ys) // 2] if ys else 0
                quads = set()
                buckets = {}
                for wid, x, y, w, h, title in entries:
                    cx, cy = x + w / 2, y + h / 2
                    qx = "right" if cx >= mx else "left"
                    qy = "bottom" if cy >= my else "top"
                    quads.add((qx, qy))
                    buckets[(qy, qx)] = title
                if len(quads) >= 4:
                    quad_score = 1.0
                elif len(quads) == 3:
                    quad_score = 0.6
                elif len(quads) == 2:
                    quad_score = 0.3
                # 8c-bis: window-name → expected quadrant matching
                expected = [
                    (("top", "left"),     re.compile(r"terminal", re.I)),
                    (("top", "right"),    re.compile(r"gedit",    re.I)),
                    (("bottom", "left"),  re.compile(r"nautilus|files", re.I)),
                    (("bottom", "right"), re.compile(r"firefox",  re.I)),
                ]
                hits = 0
                for key, pat in expected:
                    title = buckets.get(key, "")
                    if title and pat.search(title):
                        hits += 1
                quad_match_score = hits / 4.0
        except Exception:
            pass
    s["quadrant_coverage"] = quad_score
    s["quadrant_window_match"] = quad_match_score

    # Weighted aggregation: core 0.6 / gui 0.3 / aux 0.1
    core_keys = ["verify_pass", "layout_violations", "bug_findings",
                 "wmctrl_after_4_windows", "quadrant_coverage", "quadrant_window_match",
                 "fixed_script_present"]
    gui_keys = ["gui_screenshots_count", "gui_screenshots_ocr", "gui_screenshots_quality",
                "vlm_fixed_2x2_grid", "vlm_no_offscreen", "vlm_no_overlap", "vlm_broken_vs_fixed_diff"]
    aux_keys = ["cli_artifacts", "check_layout_present", "tiling_report"]
    def _avg(keys):
        vs = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vs) / len(vs) if vs else 0.0
    core = _avg(core_keys); gui = _avg(gui_keys); aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Multi-tier hard gates (tightened in v2)
    if not has_cli: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.25)
    if s["bug_findings"] < 0.5:           base = min(base, 0.40)
    if s["verify_pass"] < 0.5:            base = min(base, 0.45)
    if s["layout_violations"] < 0.5:      base = min(base, 0.55)
    if s["wmctrl_after_4_windows"] < 0.5: base = min(base, 0.45)
    if s["fixed_script_present"] < 0.5:   base = min(base, 0.50)
    if s["quadrant_coverage"] < 0.5:      base = min(base, 0.50)
    if s["quadrant_window_match"] < 0.5:  base = min(base, 0.55)
    if s["gui_screenshots_quality"] < 0.5: base = min(base, 0.55)
    # VLM unavailable → cap 0.6 (prevent passing without VLM verification)
    vlm_sum = sum(s.get(k, 0.0) for k in ["vlm_fixed_2x2_grid","vlm_no_offscreen","vlm_no_overlap","vlm_broken_vs_fixed_diff"])
    if vlm_sum == 0.0: base = min(base, 0.60)

    s["overall_score"] = round(base, 4)
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
