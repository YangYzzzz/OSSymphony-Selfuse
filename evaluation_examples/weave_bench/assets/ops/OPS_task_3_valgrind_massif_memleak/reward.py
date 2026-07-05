# Auto-generated from WeaveBench task OPS_task_3_valgrind_massif_memleak.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """valgrind massif + memcheck + massif-visualizer 微循环 grader."""
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

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    def ocr_hits(path, kws):
        if not (pytesseract and Image and path.exists()):
            return False
        try:
            tx = pytesseract.image_to_string(Image.open(path)).lower()
        except Exception:
            return False
        return any(k.lower() in tx for k in kws)

    # 1. build + massif_baseline
    bl = rd / "build_baseline.log"
    s["build_baseline"] = 1.0 if bl.exists() else 0.0
    mb = rd / "massif_baseline.out"
    if mb.exists() and mb.stat().st_size >= 1024:
        t = mb.read_text(errors="ignore")
        snap_n = len(re.findall(r"snapshot=\d+", t))
        heap_n = len(re.findall(r"mem_heap_B=\d+", t))
        s["massif_baseline"] = 1.0 if (snap_n >= 5 and heap_n >= 5) else (0.5 if (snap_n >= 1 and heap_n >= 1) else 0.2)
    else:
        s["massif_baseline"] = 0.0

    # 2. ms_print_baseline
    mp = rd / "ms_print_baseline.txt"
    if mp.exists():
        t = mp.read_text(errors="ignore")
        has_graph = bool(re.search(r"[#:@]", t)) and len(t) >= 200
        s["ms_print_baseline"] = 1.0 if has_graph else 0.3
    else:
        s["ms_print_baseline"] = 0.0

    # 3. massif-visualizer screenshots phase 2 (3)
    base_shots = ["view_01_heap_timeline.png",
                  "view_02_peak_snapshot.png",
                  "view_03_top_allocator_expanded.png"]
    # screenshots smaller than 8KB are treated as placeholders/blank frames
    bp = sum(1 for n in base_shots if (rd/n).exists() and (rd/n).stat().st_size >= 8192)
    s["base_shots_present"] = bp / len(base_shots)
    msv_kw = ["massif", "snapshot", "allocation", "tree", "peak", "heap",
              "bytes", "timeline", "function", "detailed", "malloc"]
    if pytesseract and Image:
        s["base_shots_ocr"] = sum(1 for n in base_shots if ocr_hits(rd/n, msv_kw)) / len(base_shots)
    else:
        s["base_shots_ocr"] = 0.5 if bp else 0.0

    # 4. memcheck_baseline.txt
    mcb = rd / "memcheck_baseline.txt"
    if mcb.exists():
        t = mcb.read_text(errors="ignore")
        has_lost = any(k in t for k in ["definitely lost", "indirectly lost", "possibly lost"])
        has_stack = "at 0x" in t
        s["memcheck_baseline"] = 1.0 if (has_lost and has_stack) else (0.5 if has_lost else 0.2)
    else:
        s["memcheck_baseline"] = 0.0

    # 5. memcheck_topfuncs.txt
    mtf = rd / "memcheck_topfuncs.txt"
    if mtf.exists():
        lines = [l.strip() for l in mtf.read_text(errors="ignore").splitlines() if l.strip()]
        s["memcheck_topfuncs"] = 1.0 if len(lines) >= 1 else 0.0
    else:
        s["memcheck_topfuncs"] = 0.0

    # 6. cross-validation
    p4 = rd / "view_04_xref_function_node.png"
    cv = rd / "cross_validation.json"
    cv_score = 0.0
    if cv.exists():
        try:
            d = json.loads(cv.read_text())
            req = {"topfuncs_from_memcheck","matched_in_massif_tree",
                   "match_ratio","confirmed_leak_funcs","confirmed_screenshot"}
            if req <= set(d.keys()):
                cv_score = 0.5
                if isinstance(d.get("match_ratio"), (int, float)) and d["match_ratio"] >= 0.5:
                    cv_score += 0.5
        except Exception:
            pass
    s["cross_validation"] = cv_score
    s["xref_screenshot"] = 1.0 if p4.exists() else 0.0

    # 7. leak_analysis.json
    la = rd / "leak_analysis.json"
    la_score = 0.0
    if la.exists():
        try:
            d = json.loads(la.read_text())
            sites = d.get("leak_sites", [])
            req = {"function","file","line_approx","alloc_bytes_at_peak",
                   "alloc_percentage","leak_type","evidence_screenshot",
                   "evidence_memcheck_line"}
            allowed = {"unbounded_growth","missing_free","realloc_without_shrink","double_alloc_no_free"}
            def _ok(x):
                if not (isinstance(x, dict) and req <= set(x.keys())): return False
                if x.get("leak_type") not in allowed: return False
                # numeric fields must be non-trivial
                if not isinstance(x.get("alloc_bytes_at_peak"), int) or x["alloc_bytes_at_peak"] <= 0: return False
                if not isinstance(x.get("alloc_percentage"), (int, float)) or x["alloc_percentage"] <= 0: return False
                if not isinstance(x.get("line_approx"), int) or not (1 <= x["line_approx"] <= 1000): return False
                if not isinstance(x.get("function"), str) or len(x["function"].strip()) < 2: return False
                if not isinstance(x.get("evidence_memcheck_line"), str) or len(x["evidence_memcheck_line"]) < 5: return False
                return True
            valid = [x for x in sites if _ok(x)]
            # require distinct function names across sites
            distinct_funcs = {x["function"].strip() for x in valid}
            if len(distinct_funcs) >= 3:
                la_score = 1.0
            elif len(distinct_funcs) == 2:
                la_score = 0.6
            elif len(distinct_funcs) == 1:
                la_score = 0.3
        except Exception:
            pass
    s["leak_analysis"] = la_score

    # 8. iter1 build + memcheck
    bi = rd / "build_fixed_iter1.log"
    mi = rd / "memcheck_iter1.txt"
    s["iter1_artifacts"] = (int(bi.exists()) + int(mi.exists())) / 2.0

    # 9. iter1 GUI
    p5 = rd / "view_05_iter1_alloctree.png"
    s["iter1_screenshot"] = 1.0 if p5.exists() else 0.0
    s["iter1_screenshot_ocr"] = 1.0 if ocr_hits(p5, msv_kw) else (0.5 if (p5.exists() and not pytesseract) else 0.0)

    # 10. memcheck_final - definitely lost reduction
    mcf = rd / "memcheck_final.txt"
    final_score = 0.0
    if mcf.exists() and mcb.exists():
        try:
            def_lost = lambda txt: int((re.search(r"definitely lost:\s*([\d,]+)\s*bytes", txt) or [None,'0'])[1].replace(",",""))
            base_lost = def_lost(mcb.read_text(errors="ignore"))
            final_lost = def_lost(mcf.read_text(errors="ignore"))
            if base_lost == 0 and final_lost == 0:
                final_score = 0.7
            elif base_lost > 0:
                ratio = final_lost / base_lost
                final_score = 1.0 if ratio < 0.2 else (0.7 if ratio < 0.5 else (0.4 if ratio < 0.8 else 0.1))
        except Exception:
            final_score = 0.0
    s["memcheck_final_reduction"] = final_score

    # 11. massif_fixed peak reduction
    mf = rd / "massif_fixed.out"
    s["massif_fixed_exists"] = 1.0 if (mf.exists() and mf.stat().st_size >= 1024) else 0.0
    peak_score = 0.0
    if mf.exists() and mb.exists():
        try:
            bp_vals = [int(x) for x in re.findall(r"mem_heap_B=(\d+)", mb.read_text(errors="ignore"))]
            fp_vals = [int(x) for x in re.findall(r"mem_heap_B=(\d+)", mf.read_text(errors="ignore"))]
            if bp_vals and fp_vals:
                ratio = max(fp_vals) / max(max(bp_vals), 1)
                peak_score = 1.0 if ratio < 0.5 else (0.6 if ratio < 0.8 else 0.2)
        except Exception:
            pass
    s["peak_reduction"] = peak_score

    # 12. final timeline shot
    p6 = rd / "view_06_fixed_timeline.png"
    s["final_timeline_shot"] = 1.0 if p6.exists() else 0.0
    s["final_timeline_ocr"] = 1.0 if ocr_hits(p6, msv_kw) else (0.5 if (p6.exists() and not pytesseract) else 0.0)

    # 13. patch + fix_summary
    pt = rd / "server.patch"
    if pt.exists():
        t = pt.read_text(errors="ignore")
        is_diff = ("---" in t and "+++" in t and "@@" in t)
        n = sum(1 for l in t.splitlines() if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++","---")))
        s["server_patch"] = 1.0 if (is_diff and n >= 6) else (0.5 if is_diff else 0.0)
    else:
        s["server_patch"] = 0.0
    fs = rd / "fix_summary.md"
    if fs.exists():
        t = fs.read_text(errors="ignore")
        ref_n = len(re.findall(r"view_\d+", t))
        has_nums = len(re.findall(r"\d{4,}", t)) >= 2
        s["fix_summary"] = 1.0 if (len(t) >= 350 and ref_n >= 3 and has_nums) else (0.5 if len(t) >= 200 else 0.2)
    else:
        s["fix_summary"] = 0.0

    # cross-channel evidence
    has_cli_ev = (s["massif_baseline"] > 0 and s["memcheck_baseline"] > 0)
    has_gui_ev = (s["base_shots_present"] >= 0.5 and s["xref_screenshot"] > 0)
    s["cross_channel_evidence"] = 1.0 if (has_cli_ev and has_gui_ev) else 0.0

    # VLM rubric (4)
    if vlm_score_rubric:
        all_shots = base_shots + ["view_04_xref_function_node.png",
                                  "view_05_iter1_alloctree.png",
                                  "view_06_fixed_timeline.png"]
        sample = [str(rd/n) for n in all_shots if (rd/n).exists()][:4]
        if sample:
            rubric = {
                "vlm_msv_real_window": "至少一张截图清晰显示 massif-visualizer GUI 真窗口（标题栏 + 主图 + 侧栏 snapshot 列表）",
                "vlm_alloctree_expanded": "至少一张截图能看到 Allocation Tree 真展开（带函数名 + 字节数 + 百分比的多层缩进树）",
                "vlm_xref_funcs": "view_04 中能看到 ≥2 个 memcheck topfuncs 列表中的函数名同时出现在 Allocation Tree 节点行",
                "vlm_fixed_flat_or_lower": "view_06 修复后时间线明显比 view_01 平坦或下降，不再持续增长",
            }
            vlm = vlm_score_rubric(sample, rubric,
                instruction="评估 valgrind massif + massif-visualizer 堆缺陷诊断与修复闭环截图。")
            for k in rubric:
                s[k] = vlm.get(k, 0.0)
            s["judge_method"] = vlm.get("judge_method", "failed")

    # GUI hard-gate: real interaction via md5 diversity of trajectory frames
    # Anti-cheat: screenshots < 8KB are treated as blank/placeholder and dropped
    import hashlib as _hashlib
    traj_shots = ["view_01_heap_timeline.png","view_02_peak_snapshot.png",
                  "view_03_top_allocator_expanded.png","view_04_xref_function_node.png",
                  "view_05_iter1_alloctree.png","view_06_fixed_timeline.png"]
    traj_paths = [rd / n for n in traj_shots]
    present_paths = [p for p in traj_paths if p.exists() and p.stat().st_size >= 8192]
    if len(present_paths) >= 2:
        _hashes = set(_hashlib.md5(p.read_bytes()).hexdigest() for p in present_paths)
        gui_diversity = (len(_hashes) / max(1, len(present_paths))) * (len(present_paths) / len(traj_paths))
    else:
        gui_diversity = 0.0
    s["gui_real_interaction"] = 1.0 if gui_diversity >= 0.8 else (0.5 if gui_diversity >= 0.6 else 0.0)

    # GUI chrome OCR: app-specific UI elements that only appear in real GUI apps (not text terminal)
    chrome_kws_msv = ["Massif Visualizer","massif-visualizer","Allocation Tree","Detailed Snapshot",
                      "kcachegrind","Call Graph","Callee","Caller","Flat Profile",
                      "Snapshot #","Heap Profile","gdbgui","Source View"]
    chrome_hits = 0
    if pytesseract and Image:
        for p in traj_paths:
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in chrome_kws_msv):
                        chrome_hits += 1
                except Exception:
                    pass
        s["gui_chrome_ocr"] = chrome_hits / len(traj_paths)
    else:
        s["gui_chrome_ocr"] = 0.0

    # Window geometry: real GUI screenshots should match desktop resolution (≥1280×720) and contain menubar area
    geo_hits = 0
    if Image:
        for p in traj_paths:
            if p.exists():
                try:
                    w, h = Image.open(p).size
                    if w >= 1280 and h >= 720:
                        geo_hits += 1
                except Exception:
                    pass
        s["gui_window_geometry"] = geo_hits / len(traj_paths)
    else:
        s["gui_window_geometry"] = 0.0

    # Weighted aggregation: core delivery 60% / GUI evidence 30% / auxiliary 10%
    def _avg(keys):
        vs = [s[k] for k in keys if isinstance(s.get(k), (int, float))]
        return sum(vs) / len(vs) if vs else 0.0
    core_keys = ["build_baseline", "massif_baseline", "ms_print_baseline",
                 "memcheck_baseline", "leak_analysis", "server_patch",
                 "fix_summary", "memcheck_final_reduction", "peak_reduction",
                 "massif_fixed_exists", "iter1_artifacts"]
    gui_keys_main = ["base_shots_present", "base_shots_ocr", "xref_screenshot",
                     "iter1_screenshot", "iter1_screenshot_ocr",
                     "final_timeline_shot", "final_timeline_ocr",
                     "gui_real_interaction", "gui_chrome_ocr", "gui_window_geometry"]
    vlm_keys = [k for k in s if k.startswith("vlm_")]
    gui_keys = gui_keys_main + vlm_keys
    aux_keys = ["memcheck_topfuncs", "cross_validation", "cross_channel_evidence"]
    base = 0.6 * _avg(core_keys) + 0.3 * _avg(gui_keys) + 0.1 * _avg(aux_keys)

    # Hard gates (v2: more layers + stricter thresholds)
    if not has_cli_ev:
        base = min(base, 0.35)
    if not has_gui_ev:
        base = min(base, 0.35)
    if s.get("leak_analysis", 0) == 0:
        base = min(base, 0.45)
    if s.get("leak_analysis", 0) < 0.6:
        base = min(base, 0.55)
    if s.get("server_patch", 0) == 0:
        base = min(base, 0.45)
    if s.get("memcheck_final_reduction", 0) == 0 and s.get("peak_reduction", 0) == 0:
        base = min(base, 0.45)
    if s.get("fix_summary", 0) < 0.5:
        base = min(base, 0.6)
    # GUI hard gates: no real GUI interaction → cap (CLI-only ceiling)
    if s.get("gui_real_interaction", 0.0) < 0.6:
        base = min(base, 0.4)
    if s.get("gui_real_interaction", 0.0) < 0.4:
        base = min(base, 0.3)
    if s.get("gui_chrome_ocr", 0.0) < 0.5:
        base = min(base, 0.45)
    if s.get("gui_chrome_ocr", 0.0) < 0.34 and s.get("gui_window_geometry", 0.0) < 0.5:
        base = min(base, 0.35)
    if s.get("base_shots_present", 0.0) < 1.0:
        base = min(base, 0.6)
    if vlm_keys:
        vlm_avg = sum(s[k] for k in vlm_keys) / len(vlm_keys)
        if vlm_avg < 0.6:
            base = min(base, 0.5)
        if vlm_avg < 0.4:
            base = min(base, 0.35)
    else:
        # VLM unavailable → cap to prevent free pass
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
