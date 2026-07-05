# Auto-generated from WeaveBench task WEB_task_15_sourcemap_stack_decode.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Sourcemap stack decode grader (12 sub-scores + 3 hard gates)."""
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

    # 1. decoded_before.json structure
    db = {}
    try:
        db = json.loads(_read(rd / "decoded_before.json"))
    except Exception:
        db = {}
    if isinstance(db, list) and len(db) >= 3:
        s["decoded_before_count"] = 1.0
    elif isinstance(db, list) and db:
        s["decoded_before_count"] = 0.5
    else:
        s["decoded_before_count"] = 0.0

    # 2. BEFORE: at least one frame must show a stale signal (decoded
    # source line text disagrees with the current src file at decoded
    # line — proof the agent identified a real mismatch).
    stale_evidence = 0.0
    if isinstance(db, list):
        for ent in db:
            if not isinstance(ent, dict):
                continue
            d = ent.get("decoded") or {}
            src_name = (d.get("source") or "").split("/")[-1]
            line = d.get("line")
            text = (d.get("source_line_text") or "").strip()
            if not src_name or not line or not text:
                continue
            cur_src = exec_root / "src" / src_name
            if not cur_src.exists():
                continue
            try:
                cur_lines = cur_src.read_text().splitlines()
            except Exception:
                continue
            if 1 <= line <= len(cur_lines):
                cur_text = cur_lines[line - 1].strip()
                if cur_text and text and cur_text != text:
                    stale_evidence = 1.0
                    break
    s["before_shows_stale"] = stale_evidence

    # 3. stale_bundle.txt names a real bundle that exists in dist/
    stale_txt = _read(rd / "stale_bundle.txt").strip().lower()
    bundle_basenames = []
    dist = exec_root / "dist"
    if dist.exists():
        bundle_basenames = [p.name.lower() for p in dist.glob("*.bundle.js")]
    first_tok = (stale_txt.splitlines() or [""])[0].strip().strip('"').strip("'")
    named_real = first_tok in {b for b in bundle_basenames} \
                 or first_tok in {b.split(".")[0] for b in bundle_basenames}
    # Cross-check: the named bundle should also be the one whose
    # sourcesContent length disagrees with current src.
    truly_stale = None
    for bj in bundle_basenames:
        base = bj.split(".")[0]
        mp = dist / f"{base}.bundle.js.map"
        sp = exec_root / "src" / f"{base}.js"
        if mp.exists() and sp.exists():
            try:
                mj = json.loads(mp.read_text())
                sc = (mj.get("sourcesContent") or [""])[0] or ""
                if abs(len(sc.splitlines())
                       - len(sp.read_text().splitlines())) > 4:
                    truly_stale = base
                    break
            except Exception:
                pass
    matches_truth = (truly_stale is not None
                     and first_tok in (truly_stale, f"{truly_stale}.bundle.js"))
    if matches_truth:
        s["stale_bundle_named"] = 1.0
    elif named_real:
        s["stale_bundle_named"] = 0.5
    else:
        s["stale_bundle_named"] = 0.0

    # 4. map_validation.json: any frame must be marked match=false
    mv = {}
    try:
        mv = json.loads(_read(rd / "map_validation.json"))
    except Exception:
        mv = {}
    falsy = [k for k, v in (mv.items() if isinstance(mv, dict) else [])
             if isinstance(v, dict) and v.get("match") is False]
    exactly_one = (len(falsy) == 1)
    points_to_truth = (truly_stale is not None
                       and exactly_one and falsy[0].lower().startswith(truly_stale))
    s["map_validation"] = (1.0 if points_to_truth
                           else 0.5 if exactly_one
                           else 0.2 if falsy else 0.0)

    # 5. diagnosis.md depth
    diag = _read(rd / "diagnosis.md")
    diag_lines = len([ln for ln in diag.splitlines() if ln.strip()])
    diag_subs = len(re.findall(r"(?m)^###\s+\S", diag))
    diag_lower = diag.lower()
    needed = ["sourcescontent", "line", "stale", "rebuild", truly_stale or "feature"]
    hits = sum(1 for w in needed if w in diag_lower)
    s["diagnosis_depth"] = (
        1.0 if (diag_lines >= 25 and diag_subs >= 3 and hits >= 4)
        else 0.5 if (diag_lines >= 18 and diag_subs >= 2 and hits >= 3)
        else 0.0
    )

    # 6. GUI screenshots
    shots = [
        "view_01_console_stack.png",
        "view_02_sources_stale_frame.png",
        "view_03_sources_correct_frame.png",
        "view_04_after_fix_stack.png",
    ]
    present = sum(1 for n in shots if (rd / n).exists())
    s["gui_screens_present"] = present / len(shots)

    ocr_re = re.compile(r"(TypeError|sourcesContent|DevTools|Sources panel|at\s+\w+\s*\()", re.I)
    per_shot = {"view_01_console_stack.png": re.compile(r"TypeError", re.I),
                "view_02_sources_stale_frame.png": re.compile(r"sourcesContent|Sources", re.I),
                "view_04_after_fix_stack.png": re.compile(r"TypeError", re.I)}
    ocr_hits = 0
    if pytesseract and Image:
        for n in shots:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    needed_re = per_shot.get(n)
                    if needed_re is not None:
                        if needed_re.search(tx):
                            ocr_hits += 1
                    elif ocr_re.search(tx):
                        ocr_hits += 1
                except Exception:
                    pass
        s["gui_screens_ocr"] = ocr_hits / len(shots)
    else:
        s["gui_screens_ocr"] = 0.0

    # 7. After-fix: the bundle the agent named should now have its map's
    # sourcesContent[0] line count match the current src file.
    diff = None
    target_base = None
    for bj in bundle_basenames:
        base = bj.split(".")[0]
        if base in stale_txt:
            target_base = base
            break
    if target_base is None and truly_stale:
        target_base = truly_stale
    if target_base:
        sp = exec_root / "src" / f"{target_base}.js"
        mp = exec_root / "dist" / f"{target_base}.bundle.js.map"
        if sp.exists() and mp.exists():
            try:
                cur_lines = len(sp.read_text().splitlines())
                mj = json.loads(mp.read_text())
                sc = (mj.get("sourcesContent") or [""])[0] or ""
                diff = abs(cur_lines - len(sc.splitlines()))
            except Exception:
                diff = None
    if diff is None:
        s["map_regenerated"] = 0.0
    else:
        s["map_regenerated"] = 1.0 if diff <= 2 else 0.4 if diff <= 8 else 0.0

    # 8. decoded_after.json: the previously-stale frame now decodes to
    # a source line whose text matches the current src/<name>.js at the
    # decoded line number.
    da = {}
    try:
        da = json.loads(_read(rd / "decoded_after.json"))
    except Exception:
        da = {}
    after_ok = 0.0
    if isinstance(da, list) and target_base:
        for ent in da:
            if not isinstance(ent, dict):
                continue
            if target_base not in str(ent.get("input", "")):
                continue
            d = ent.get("decoded") or {}
            src = (d.get("source") or "").split("/")[-1]
            line = d.get("line")
            text = (d.get("source_line_text") or "").strip()
            if src == f"{target_base}.js" and line and text:
                cur_src = exec_root / "src" / src
                if cur_src.exists():
                    cur_lines = cur_src.read_text().splitlines()
                    if 1 <= line <= len(cur_lines):
                        gt_token = "crashHere"
                        if cur_lines[line - 1].strip() == text and gt_token in text:
                            after_ok = max(after_ok, 1.0)
                        elif gt_token in text and text in cur_lines[line - 1]:
                            after_ok = max(after_ok, 0.6)
                        else:
                            after_ok = max(after_ok, 0.0)
    s["after_decodes_correct"] = after_ok

    # 9. VLM rubric
    sample = [str(rd / n) for n in shots if (rd / n).exists()][:4]
    if vlm_score_rubric and sample:
        rubric = {
            "vlm_devtools_real": "至少一张截图清晰显示 Chrome DevTools 真实 UI（左 Files / 右 Sources 编辑器，或顶部 Console 面板）",
            "vlm_stack_visible": "至少一张截图能看到 TypeError 或 stack trace（红色错误链接）",
            "vlm_before_after": "view_04 与 view_01 能体现修复前后差异（行号或源文件指向变化）",
        }
        try:
            vlm = vlm_score_rubric(sample, rubric,
                                   instruction="评估 sourcemap mismatch 调试的 DevTools 截图证据。")
        except Exception:
            vlm = {}
        for k in rubric:
            s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
        vlm_avg = sum(vlm.get(k, 0) for k in rubric) / len(rubric) if vlm else 0.0
    else:
        vlm_avg = 0.3

    # base
    numerics = [v for k, v in s.items()
                if isinstance(v, (int, float)) and k != "judge_method"]
    base = sum(numerics) / max(1, len(numerics))
    overall = round((base + vlm_avg) / 2.0, 3) if vlm_score_rubric else round(base, 3)

    # hard gates
    has_cli_evidence = (
        (rd / "decoded_before.json").exists()
        and (rd / "decoded_after.json").exists()
        and (rd / "diagnosis.md").exists()
    )
    has_gui_screenshot = present >= 2
    if not has_cli_evidence:
        overall = round(min(overall, 0.4), 3)
    # GUI-path scoring axis removed: missing screenshots already cost
    # the screenshots / OCR / vlm_* sub-scores.
    if vlm_score_rubric and vlm_avg < 0.6:
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
