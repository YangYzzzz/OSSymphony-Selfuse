# Auto-generated from WeaveBench task DSK_task_3_system_settings_automation.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

from pathlib import Path
import re, json, hashlib
from PIL import Image

def grade(workspace_path=None, **kwargs):
    """Weighted GNOME schema + GUI-evidence scoring with multi-tier hard gates and anti-cheat."""
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    try: import pytesseract
    except: pytesseract=None
    gt_path = workspace/"gt"/"expected.json"
    try:
        gt = json.loads(gt_path.read_text()) if gt_path.exists() else {}
    except Exception:
        gt = {}
    s = {}

    # --- core: gsettings dump ---
    gd = workspace/"gsettings_dump.txt"
    cfg = gd.read_text(errors="ignore") if gd.exists() else ""
    s["dump_exists"] = 1.0 if cfg else 0.0
    settings = gt.get("settings",[])
    hits = 0
    for spec in settings:
        key_tokens = spec["key"].split()
        ok = False
        for line in cfg.splitlines():
            low = line.lower()
            if all(tok.lower() in low for tok in key_tokens):
                if any(str(v).lower() in low for v in spec["expect"]):
                    ok = True; break
        if ok: hits+=1
    s["settings_matched"] = hits/max(len(settings),1)

    # --- gui: about/background screenshots ---
    extra_shots = ["about.png", "background.png"]
    extra_present = sum(1 for n in extra_shots if (workspace/n).exists() and (workspace/n).stat().st_size >= 8*1024)
    s["gui_only_screenshots"] = extra_present / len(extra_shots)
    extra_ocr_hits = 0
    if pytesseract:
        ocr_keywords = {
            "about.png": ["About","System","GNOME","Ubuntu","关于","系统"],
            "background.png": ["Background","Wallpaper","背景","壁纸","Pictures"],
        }
        for n, kws in ocr_keywords.items():
            p = workspace/n
            if p.exists() and p.stat().st_size >= 8*1024:
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k in tx for k in kws):
                        extra_ocr_hits += 1
                except Exception: pass
    s["gui_only_screenshots_ocr"] = extra_ocr_hits / len(extra_shots)

    # --- gui: setting_*.png (8 expected, anti-cheat: size + md5 + resolution) ---
    required_count = gt.get("screenshots_required_count", 8)
    pngs = sorted(workspace.glob("setting_*.png"))
    valid_pngs, md5s, res_ok_count = [], set(), 0
    min_w, min_h = gt.get("min_resolution", [1024, 600])
    for p in pngs:
        try:
            if p.stat().st_size < 8*1024:
                continue
            md5 = hashlib.md5(p.read_bytes()).hexdigest()
            if md5 in md5s:
                continue
            md5s.add(md5)
            w, h = Image.open(p).size
            if w >= min_w and h >= min_h:
                res_ok_count += 1
            valid_pngs.append(p)
        except Exception:
            pass
    s["screenshots_count"] = min(1.0, len(valid_pngs)/required_count)
    s["screenshots_distinct"] = min(1.0, len(md5s)/required_count) if md5s else 0.0
    s["screenshots_resolution_ok"] = min(1.0, res_ok_count/required_count) if required_count else 0.0

    # --- aux: about OCR keyword (separate from gui_only_screenshots_ocr for granularity) ---
    ap = workspace/"about.png"
    if ap.exists() and pytesseract and ap.stat().st_size >= 8*1024:
        try:
            tx = pytesseract.image_to_string(Image.open(ap))
            s["about_ocr"] = 1.0 if any(k in tx for k in gt.get("about_keywords",["GNOME"])) else 0.0
        except: s["about_ocr"]=0.0
    else:
        s["about_ocr"]=0.0

    # --- aux: no CLI shortcut ---
    log = workspace/"actions.log"
    pat = gt.get("forbidden_actions_log_pattern", r"(gsettings\s+set\b|dconf\s+write\b|xdg-mime\s+default\b)")
    if log.exists():
        s["no_cli_set"] = 0.0 if re.search(pat, log.read_text(errors="ignore")) else 1.0
    else:
        s["no_cli_set"] = 1.0

    # --- weighted scoring: core 60% / gui 30% / aux 10% ---
    core = 0.5*s["dump_exists"] + 0.5*s["settings_matched"]
    gui = (s["gui_only_screenshots"] + s["gui_only_screenshots_ocr"] +
           s["screenshots_count"] + s["screenshots_distinct"] + s["screenshots_resolution_ok"]) / 5.0
    aux = 0.5*s["about_ocr"] + 0.5*s["no_cli_set"]
    base = 0.60*core + 0.30*gui + 0.10*aux

    # --- multi-tier hard gates ---
    if s["no_cli_set"] == 0:
        base = min(base, 0.40)
    if s["dump_exists"] == 0:
        base = min(base, 0.30)
    if s["settings_matched"] < 0.3:
        base = min(base, 0.35)
    elif s["settings_matched"] < 0.6:
        base = min(base, 0.55)
    if s["gui_only_screenshots_ocr"] < 0.5:
        base = min(base, 0.55)
    if s["screenshots_count"] < 0.75:
        base = min(base, 0.55)
    if s["screenshots_distinct"] < 0.75:
        base = min(base, 0.50)
    if pytesseract is None:
        base = min(base, 0.60)

    s["core_score"] = round(float(core), 3)
    s["gui_score"] = round(float(gui), 3)
    s["aux_score"] = round(float(aux), 3)
    s["overall_score"] = round(float(base), 3)
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
