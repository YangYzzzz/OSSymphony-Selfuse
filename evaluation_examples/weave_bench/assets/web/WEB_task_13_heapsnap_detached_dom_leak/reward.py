# Auto-generated from WeaveBench task WEB_task_13_heapsnap_detached_dom_leak.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Detached-DOM heap snapshot grader (12 sub-scores + 3 hard gates)."""
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
    exec_root = Path("/tmp_workspace/exec")
    s = {}

    def _read(p):
        try:
            return p.read_text(errors="ignore")
        except Exception:
            return ""

    def _jload(p):
        try:
            return json.loads(_read(p))
        except Exception:
            return None

    # 1. heap snapshots present + plausible
    base_snap = rd / "heap_baseline.heapsnapshot"
    churn_snap = rd / "heap_after_churn.heapsnapshot"
    fix_snap = rd / "heap_after_fix.heapsnapshot"
    def _detached_count(p):
        d = _jload(p) or {}
        strs = d.get("strings") or []
        need = {"node_count", "edge_count", "meta"}
        if not (isinstance(d, dict) and "snapshot" in d and "nodes" in d
                and need & set(d.get("snapshot", {}))):
            return None
        return sum(1 for x in strs if isinstance(x, str) and x.startswith("Detached "))
    cb, cc = _detached_count(base_snap), _detached_count(churn_snap)
    s["heap_snapshots_present"] = (int(cb is not None) + int(cc is not None)) / 2.0
    s["heap_snapshots_real"] = 1.0 if (cb is not None and cc is not None and cc - cb >= 3) else 0.0

    # 2. detached_count.json structure + delta
    dc = _jload(rd / "detached_count.json") or {}
    delta_ok = 0.0
    top_ok = 0.0
    if isinstance(dc, dict):
        try:
            base_n = int(dc.get("baseline", -1))
            after_n = int(dc.get("after_churn", -1))
            tol = 3
            if (cb is not None and cc is not None
                and abs(base_n - cb) <= tol and abs(after_n - cc) <= tol
                and after_n - base_n >= 5):
                delta_ok = 1.0
            elif base_n >= 0 and after_n - base_n >= 5 and (cb is None or cc is None):
                delta_ok = 0.3
        except Exception:
            pass
        top = str(dc.get("top_detached_constructor", ""))
        if re.match(r"^Detached\s+(HTML\w*Element|InternalNode|Node)\b", top):
            top_ok = 1.0
        elif top.startswith("Detached "):
            top_ok = 0.4
    s["detached_delta"] = delta_ok
    s["top_constructor_named"] = top_ok

    # 3. suspect_listeners.json: ≥4 entries, both kinds covered
    sus = _jload(rd / "suspect_listeners.json") or []
    if isinstance(sus, list):
        kinds = [str(e.get("kind", "")) for e in sus if isinstance(e, dict)]
        n_add = sum(1 for k in kinds if "addEventListener" in k)
        n_int = sum(1 for k in kinds if "setInterval" in k)
        bad = sum(1 for e in sus if isinstance(e, dict)
                  and "clock" in str(e.get("snippet", "")) + str(e.get("line", "")))
        if len(sus) >= 4 and n_add >= 2 and n_int >= 2 and bad == 0:
            s["suspect_listeners"] = 1.0
        elif len(sus) >= 4 and n_add >= 2 and n_int >= 2:
            s["suspect_listeners"] = 0.5
        elif len(sus) >= 2 and (n_add >= 1 or n_int >= 1):
            s["suspect_listeners"] = 0.5
        else:
            s["suspect_listeners"] = 0.0
    else:
        s["suspect_listeners"] = 0.0

    # 4. GUI screenshots
    shots = [
        "view_01_memory_panel_initial.png",
        "view_02_comparison_detached.png",
        "view_03_retainer_chain.png",
        "view_04_sources_breakpoint.png",
        "view_05_post_fix_comparison.png",
    ]
    present = sum(1 for n in shots if (rd / n).exists())
    s["gui_screens_present"] = present / len(shots)

    ocr_re = re.compile(
        r"(Memory|Heap|Snapshot|Constructor|Detached|Retainers|Comparison|"
        r"Sources|app\.js|Paused|breakpoint|Listener|Timer|closure|DevTools)",
        re.I,
    )
    ocr_hits = 0
    if pytesseract and Image:
        for n in shots:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    uniq = len(set(m.group(0).lower() for m in ocr_re.finditer(tx)))
                    if uniq >= 2:
                        ocr_hits += 1
                except Exception:
                    pass
        s["gui_screens_ocr"] = ocr_hits / len(shots)
    else:
        s["gui_screens_ocr"] = 0.0

    # 5. fix.patch contains the two pairing tokens
    patch_txt = _read(rd / "fix.patch")
    has_remove = "removeEventListener" in patch_txt
    has_clear = "clearInterval" in patch_txt
    if has_remove and has_clear:
        s["fix_patch_tokens"] = 1.0
    elif has_remove or has_clear:
        s["fix_patch_tokens"] = 0.2
    else:
        s["fix_patch_tokens"] = 0.0

    # 6. deployed app.js looks structurally fixed
    cur_app = _read(exec_root / "public" / "app.js")
    rem_count = len(re.findall(r"\bremoveEventListener\s*\(", cur_app))
    clr_count = len(re.findall(r"\bclearInterval\s*\(", cur_app))
    has_teardown = "teardown" in cur_app or "cleanup" in cur_app
    if rem_count >= 2 and clr_count >= 2 and has_teardown:
        s["deployed_fix_shape"] = 1.0
    elif rem_count >= 1 and clr_count >= 1:
        s["deployed_fix_shape"] = 0.6
    else:
        s["deployed_fix_shape"] = 0.0

    # 7. after_fix snapshot reduces leak vs churn
    reduction_ok = 0.0
    if isinstance(dc, dict):
        try:
            base_n = int(dc.get("baseline", -1))
            after_n = int(dc.get("after_churn", -1))
            fix_n = int(dc.get("after_fix", -1))
            if base_n >= 0 and after_n >= 0 and fix_n >= 0:
                churn_delta = after_n - base_n
                fix_delta = fix_n - base_n
                if fix_delta <= max(4, base_n + 4) and churn_delta - fix_delta >= 5:
                    reduction_ok = 1.0
                elif churn_delta - fix_delta >= 2:
                    reduction_ok = 0.5
        except Exception:
            pass
    s["leak_reduced_after_fix"] = reduction_ok

    # 8. root_cause.md depth
    rc = _read(rd / "root_cause.md")
    rc_lines = len([ln for ln in rc.splitlines() if ln.strip()])
    rc_subs = len(re.findall(r"(?m)^###\s+\S", rc))
    rc_refs = len(re.findall(r"app\.js:\d+", rc))
    if rc_lines >= 25 and rc_subs >= 3 and rc_refs >= 2:
        s["root_cause_depth"] = 1.0
    elif rc_lines >= 15 and rc_subs >= 2:
        s["root_cause_depth"] = 0.5
    else:
        s["root_cause_depth"] = 0.0

    # 9. summary.json schema
    summ = _jload(rd / "summary.json") or {}
    summ_ok = 0.0
    if isinstance(summ, dict):
        ll = summ.get("leak_lines", [])
        rks = [str(x).lower() for x in (summ.get("retainer_kinds") or [])]
        kinds = []
        if isinstance(ll, list):
            kinds = [str(e.get("kind", "")) for e in ll if isinstance(e, dict)]
        n_add = sum(1 for k in kinds if "addEventListener" in k)
        n_int = sum(1 for k in kinds if "setInterval" in k)
        has_listener = any("listener" in r for r in rks)
        has_timer = any("timer" in r for r in rks)
        if (
            isinstance(ll, list) and len(ll) >= 4 and n_add >= 1 and n_int >= 1
            and has_listener and has_timer
            and "leak_count_before_churn_delta" in summ
            and "leak_count_after_fix_delta" in summ
        ):
            summ_ok = 1.0
        elif isinstance(ll, list) and len(ll) >= 2:
            summ_ok = 0.5
    s["summary_schema"] = summ_ok

    # 10. VLM rubric
    sample = [str(rd / n) for n in shots if (rd / n).exists()][:5]
    vlm_avg = 0.0
    if vlm_score_rubric and sample:
        rubric = {
            "vlm_memory_panel_real": (
                "至少一张截图清晰显示 Chrome DevTools Memory 面板真实 UI"
                "（左侧 Snapshot 列表 + 中央 Constructor 列）"
            ),
            "vlm_comparison_detached": (
                "Comparison 视图里能看到 Detached 类构造器一行 + 非零的 #New/#Delta"
            ),
            "vlm_retainer_chain": (
                "Retainers 面板展开了一条至少 3 层的引用链，"
                "含 closure / Listener / Timer 这类节点"
            ),
            "vlm_before_after_diff": (
                "view_05 与 view_02 能体现修复前后 Detached 数量的明显回落"
            ),
        }
        try:
            vlm = vlm_score_rubric(
                sample, rubric,
                instruction="评估 detached-DOM heap snapshot 取证的 DevTools 截图证据。",
            )
        except Exception:
            vlm = {}
        for k in rubric:
            s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
        if vlm:
            vlm_avg = sum(vlm.get(k, 0) for k in rubric) / len(rubric)

    # base
    numerics = [
        v for k, v in s.items()
        if isinstance(v, (int, float)) and k != "judge_method"
    ]
    base = sum(numerics) / max(1, len(numerics))
    overall = round(
        (base + vlm_avg) / 2.0, 3
    ) if vlm_score_rubric else round(base, 3)

    # hard gates
    has_cli_evidence = (
        base_snap.exists() and churn_snap.exists()
        and (rd / "detached_count.json").exists()
        and (rd / "root_cause.md").exists()
    )
    has_gui_screenshot = present >= 2
    if not has_cli_evidence:
        overall = round(min(overall, 0.4), 3)
    # GUI-path scoring axis removed: missing screenshots already cost
    # the screenshots / OCR / vlm_* sub-scores.
    if vlm_score_rubric and vlm_avg < 0.55:
        overall = round(min(overall, 0.45), 3)

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
