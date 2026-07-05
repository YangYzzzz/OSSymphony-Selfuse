# Auto-generated from WeaveBench task DSK_task_0_multimonitor_layout.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

from pathlib import Path
import json, re, hashlib
from PIL import Image

def grade(workspace_path=None, **kwargs):
    """DSK_0 multi-monitor layout grader.
    Weighted scoring: core deliverables 60% / GUI evidence 30% / aux 10%.
    Multi-tier hard gates + anti-cheat (md5 uniqueness, min file size, min resolution,
    xrandr-structure sanity)."""
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    try:
        import pytesseract
        _tess_ok = True
    except Exception:
        pytesseract = None
        _tess_ok = False
    gt_path = workspace.parent / "gt" / "expected.json"
    if not gt_path.exists():
        gt_path = Path("/tmp_workspace/gt/expected.json")
    gt = json.loads(gt_path.read_text()) if gt_path.exists() else {}
    s = {}

    # --- Core: display_config.txt ---
    dc = workspace/"display_config.txt"
    cfg = dc.read_text(errors="ignore") if dc.exists() else ""
    s["display_config_exists"] = 1.0 if cfg else 0.0
    # Anti-cheat: must look like real xrandr output (has 'Screen 0:' header AND mm sizes)
    s["display_config_xrandr_shape"] = 1.0 if (
        re.search(r"Screen\s+\d+:\s*minimum", cfg) and re.search(r"\d+mm\s*x\s*\d+mm", cfg)
    ) else 0.0

    monitors = gt.get("monitors", {})
    mon_subscores = []
    for name, spec in monitors.items():
        present = name in cfg
        s[f"mon_{name}_present"] = 1.0 if present else 0.0
        sub = [s[f"mon_{name}_present"]]
        if present:
            m = re.search(rf"{re.escape(name)}.*?(?=\n\S+ (?:connected|disconnected)|\Z)", cfg, re.DOTALL)
            blk = m.group(0) if m else ""
            res = spec.get("resolution")
            v = 1.0 if (res and res in blk) else 0.0
            s[f"mon_{name}_resolution"] = v; sub.append(v)
            if "refresh_hz" in spec:
                v = 1.0 if str(spec["refresh_hz"]) in blk else 0.0
                s[f"mon_{name}_refresh"] = v; sub.append(v)
            rot = spec.get("rotation", "normal")
            allowed = rot if isinstance(rot, list) else [rot]
            v = 1.0 if any(r in blk for r in allowed) else 0.0
            s[f"mon_{name}_rotation"] = v; sub.append(v)
            if spec.get("primary"):
                v = 1.0 if "primary" in blk else 0.0
                s[f"mon_{name}_primary"] = v; sub.append(v)
        mon_subscores.append(sum(sub)/len(sub) if sub else 0.0)
    monitors_score = sum(mon_subscores)/len(mon_subscores) if mon_subscores else 0.0

    # --- Core: screenshots present + anti-cheat (size, md5 uniqueness, resolution) ---
    needed = gt.get("screenshots_required", [])
    png_needed = [n for n in needed if n.endswith(".png")]
    pres_count = sum(1 for n in needed if (workspace/n).exists())
    s["screenshots_present"] = (pres_count/len(needed)) if needed else 0.0

    md5s, big_enough, res_ok = [], 0, 0
    for n in png_needed:
        p = workspace/n
        if not p.exists():
            continue
        try:
            data = p.read_bytes()
            if len(data) >= 5*1024:
                big_enough += 1
            md5s.append(hashlib.md5(data).hexdigest())
            try:
                with Image.open(p) as im:
                    w, h = im.size
                if w >= 1024 and h >= 600:
                    res_ok += 1
            except Exception:
                pass
        except Exception:
            pass
    n_png = len(png_needed) if png_needed else 1
    s["screenshots_size_ok"] = big_enough / n_png
    s["screenshots_resolution_ok"] = res_ok / n_png
    s["screenshots_md5_unique"] = (len(set(md5s)) / len(md5s)) if md5s else 0.0

    # --- GUI evidence: OCR ---
    kc = workspace/"keep_changes.png"
    if kc.exists() and _tess_ok:
        try:
            tx = pytesseract.image_to_string(Image.open(kc))
            s["keep_modal_ocr"] = 1.0 if any(k in tx for k in gt.get("keep_ocr_keywords", ["Keep"])) else 0.0
        except Exception:
            s["keep_modal_ocr"] = 0.0
    else:
        s["keep_modal_ocr"] = 0.0

    ov = workspace/"overview.png"
    if ov.exists() and _tess_ok:
        try:
            tx = pytesseract.image_to_string(Image.open(ov))
            apps = list(gt.get("apps_per_screen", {}).values())
            hits = sum(1 for k in apps+["文件","Nautilus"] if k in tx)
            s["overview_apps"] = min(1.0, hits/2)
        except Exception:
            s["overview_apps"] = 0.0
    else:
        s["overview_apps"] = 0.0

    # --- Weighted aggregation ---
    core = (
        0.30 * s["display_config_exists"] +
        0.15 * s["display_config_xrandr_shape"] +
        0.30 * monitors_score +
        0.25 * s["screenshots_present"]
    )
    gui = (
        0.45 * s["keep_modal_ocr"] +
        0.45 * s["overview_apps"] +
        0.10 * s["screenshots_resolution_ok"]
    )
    aux = (
        0.5 * s["screenshots_size_ok"] +
        0.5 * s["screenshots_md5_unique"]
    )
    s["core_score"] = float(core)
    s["gui_score"] = float(gui)
    s["aux_score"] = float(aux)
    base = 0.6*core + 0.3*gui + 0.1*aux

    # --- Multi-tier hard gates (越严越好) ---
    # Gate 1: 核心交付物（display_config + 关键截图）缺失 → 重罚
    if s["display_config_exists"] < 1 or s["screenshots_present"] < 0.8:
        base = min(base, 0.4)
    # Gate 2: display_config 不像真实 xrandr 输出（手写答案）→ 重罚
    if s["display_config_xrandr_shape"] < 1 and s["display_config_exists"] >= 1:
        base = min(base, 0.45)
    # Gate 3: GUI 真实交互证据双 0（既没 keep modal 又没 overview）→ 重罚
    if s["keep_modal_ocr"] < 1 and s["overview_apps"] < 1:
        base = min(base, 0.4)
    # Gate 4: 截图 md5 重复（伪造、复制同一张）→ 重罚
    if md5s and s["screenshots_md5_unique"] < 0.8:
        base = min(base, 0.45)
    # Gate 5: 截图体积 / 分辨率 < 60% 达标（占位/截屏失败）→ 中罚
    if s["screenshots_size_ok"] < 0.6 or s["screenshots_resolution_ok"] < 0.6:
        base = min(base, 0.55)
    # Gate 6: VLM/OCR 不可用 → 上限封顶 0.6（防止无 OCR 也满分）
    if not _tess_ok:
        base = min(base, 0.6)

    s["overall_score"] = float(max(0.0, min(1.0, base)))
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
