# Auto-generated from WeaveBench task OPS_task_0_vscode_debugger_offbyone.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """OPS_0 v2: weighted scoring + multi-tier hard gates + anti-cheat (md5/size/resolution)."""
    import json, hashlib, importlib.util
    from pathlib import Path
    try: import pytesseract; from PIL import Image
    except: pytesseract=None; Image=None
    gt = json.loads(Path("/tmp_workspace/gt/expected.json").read_text()) if Path("/tmp_workspace/gt/expected.json").exists() else {}
    rd = Path("/tmp_workspace/results")
    s = {}
    # ---- screenshots: existence + size + md5 uniqueness + min resolution ----
    req = gt.get("screenshots_required",[])
    md5s = {}; sizes = {}; resolutions = {}
    for n in req:
        p = rd/n
        if p.exists():
            try:
                b = p.read_bytes()
                md5s[n] = hashlib.md5(b).hexdigest()
                sizes[n] = len(b)
                if Image:
                    try:
                        with Image.open(p) as im: resolutions[n] = im.size
                    except: resolutions[n] = (0,0)
            except: pass
    for n in req:
        ok = (n in md5s) and sizes.get(n,0) >= 5*1024
        if Image and n in resolutions:
            w,h = resolutions[n]
            ok = ok and (w >= 1024 and h >= 600)
        s[f"img_{n}"] = 1.0 if ok else (0.5 if n in md5s else 0.0)
    unique = len(set(md5s.values()))
    s["img_unique"] = (unique/len(req)) if req else 0.0
    # ---- OCR keyword evidence (require >=2 distinct keywords across all imgs OR >=50% imgs hit) ----
    ocr_hit_imgs = 0; ocr_kw_set = set()
    if pytesseract and Image:
        for n in req:
            p = rd/n
            if not p.exists(): continue
            try:
                tx = pytesseract.image_to_string(Image.open(p)).upper()
                hits = [k for k in gt.get("ocr_keywords_debug_panel",[]) if k in tx]
                if hits:
                    ocr_hit_imgs += 1
                    ocr_kw_set.update(hits)
            except: pass
        s["debug_panel_ocr"] = (ocr_hit_imgs/len(req)) if req else 0.0
        s["debug_panel_ocr_kw_diversity"] = min(1.0, len(ocr_kw_set)/2.0)
    else:
        s["debug_panel_ocr"] = 0.0; s["debug_panel_ocr_kw_diversity"] = 0.0
    # ---- analysis ----
    a_path = rd/"analysis.md"
    a = a_path.read_text() if a_path.exists() else ""
    mn = gt.get("min_analysis_chars",100); mx = gt.get("max_analysis_chars",500)
    s["analysis_length"] = 1.0 if mn <= len(a) <= mx else (0.5 if a else 0.0)
    s["analysis_keywords"] = 1.0 if sum(1 for k in ["off-by-one","floor","ceil","边界","余数","mod"] if k in a.lower()) >= 2 else (0.5 if a else 0.0)
    # ---- patch: must touch only core.py, contain unified-diff hallmarks ----
    patch_path = rd/"fix.patch"
    patch = patch_path.read_text() if patch_path.exists() else ""
    plus_headers = [ln for ln in patch.splitlines() if ln.startswith("+++ ")]
    minus_headers = [ln for ln in patch.splitlines() if ln.startswith("--- ")]
    only_core = (len(plus_headers) == 1 and "core.py" in plus_headers[0] and len(minus_headers) == 1)
    s["valid_patch"] = 1.0 if (gt.get("buggy_file","core.py") in patch and "@@" in patch and only_core) else (0.5 if patch else 0.0)
    s["patch_uses_ceil"] = 1.0 if gt.get("expected_fix_pattern","math.ceil") in patch else 0.0
    # ---- pytest output ----
    pytest_path = rd/"pytest.txt"
    pt = pytest_path.read_text() if pytest_path.exists() else ""
    s["pytest_pass"] = 1.0 if ("passed" in pt and "failed" not in pt and "error" not in pt.lower()) else (0.3 if pt else 0.0)
    # ---- run 6 truth test cases against current core.py ----
    core_path = Path("/tmp_workspace/pager/core.py")
    if core_path.exists():
        try:
            spec = importlib.util.spec_from_file_location("pager_core", str(core_path))
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            ok=0; total=0
            for tc in gt.get("test_cases",[]):
                total+=1
                try:
                    if mod.total_pages(*tc["args"]) == tc["expect"]: ok+=1
                except: pass
            s["test_cases_pass"] = ok/max(total,1)
        except Exception:
            s["test_cases_pass"] = 0.0
    else:
        s["test_cases_pass"] = 0.0
    # ---- weighted aggregation: core delivery 60% / GUI evidence 30% / aux 10% ----
    img_keys = [f"img_{n}" for n in req]
    imgs_avg = sum(s.get(k,0) for k in img_keys)/max(len(img_keys),1)
    core_score = (
        0.45 * s.get("test_cases_pass",0) +
        0.25 * s.get("valid_patch",0) +
        0.15 * s.get("patch_uses_ceil",0) +
        0.15 * s.get("pytest_pass",0)
    )
    gui_score = (
        0.40 * imgs_avg +
        0.20 * s.get("img_unique",0) +
        0.25 * s.get("debug_panel_ocr",0) +
        0.15 * s.get("debug_panel_ocr_kw_diversity",0)
    )
    aux_score = 0.5*s.get("analysis_length",0) + 0.5*s.get("analysis_keywords",0)
    base = 0.6*core_score + 0.3*gui_score + 0.1*aux_score
    # ---- multi-tier hard gates ----
    imgs_present = sum(1 for n in req if n in md5s)
    if s.get("test_cases_pass",0) < 1.0:
        base = min(base, 0.45)
    if s.get("valid_patch",0) < 1.0:
        base = min(base, 0.5)
    if imgs_present < 3:
        base = min(base, 0.35)
    if s.get("img_unique",0) < 0.75:  # too many duplicate screenshots = cheat
        base = min(base, 0.4)
    if pytesseract and s.get("debug_panel_ocr",0) < 0.5:
        base = min(base, 0.55)
    if not pytesseract:  # no VLM/OCR → cap so blind runs can't max out
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
