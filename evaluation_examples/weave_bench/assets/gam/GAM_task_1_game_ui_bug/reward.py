# Auto-generated from WeaveBench task GAM_task_1_game_ui_bug.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

from pathlib import Path
from PIL import Image
import re
try:
    import numpy as np
except Exception:
    np = None
try:
    import pytesseract
except Exception:
    pytesseract = None

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    r={"checks":{},"overall_score":0.0}; s=0; t=5
    sizes=["1024x768","1280x800","1366x768","1920x1080"]
    rd_alt = workspace / "results"
    def _pick(name):
        p1 = workspace / name
        p2 = rd_alt / name
        return p2 if (p2.exists() and not p1.exists()) else p1
    menus=[_pick(f"menu_{w}.png") for w in sizes]
    huds=[_pick(f"hud_{w}.png") for w in sizes]
    if all(p.exists() for p in menus+huds):
        ok=True
        for p,w in zip(menus+huds, sizes+sizes):
            tw,th=map(int,w.split("x"))
            iw,ih=Image.open(p).size
            if abs(iw-tw)>40 or abs(ih-th)>40: ok=False
        if ok: r["checks"]["sizes_match"]=True; s+=1
        r["checks"]["all_screens"]=True; s+=1
    rep = workspace/"bug_report.md"
    if not rep.exists(): rep = rd_alt/"bug_report.md"
    if rep.exists():
        c=rep.read_text(errors="ignore")
        rows=[l for l in c.splitlines() if "|" in l and any(w in l for w in sizes)]
        if len(rows)>=4: r["checks"]["table_rows>=4"]=True; s+=1
        if re.search(r"\|\s*(是|Yes)\s*\|", c): r["checks"]["bug_flagged"]=True; s+=1
    annots=list(workspace.glob("annotated_*.png")) + list(rd_alt.glob("annotated_*.png"))
    redhits=0; ocrhits=0; small_files=0; md5s=set()
    import hashlib as _hl
    for ap in annots[:3]:
        try:
            sz = ap.stat().st_size
            if sz < 5_000: small_files += 1
            md5s.add(_hl.md5(ap.read_bytes()).hexdigest())
        except Exception: pass
        a=np.array(Image.open(ap).convert("RGB"))
        red=((a[...,0]>180)&(a[...,1]<80)&(a[...,2]<80)).mean()
        if red>0.02: redhits+=1
        try:
            tx=pytesseract.image_to_string(Image.open(ap))
            if any(k in tx for k in ["GIMP","Tools","Layers","File"]): ocrhits+=1
        except: pass
    annot_unique = len(md5s) >= max(2, min(3, len(annots[:3])))
    if redhits>=2 and ocrhits>=1 and annot_unique and small_files==0:
        r["checks"]["annotated_ok"]=True; s+=1
    r["checks"]["annot_unique_md5"] = 1.0 if annot_unique else 0.0
    r["checks"]["annot_no_tiny"] = 1.0 if small_files==0 else 0.0

    # New: window_metrics.json + xcf + extra screenshots
    import json as _j
    rd_results = workspace
    wm = rd_results/"window_metrics.json"
    if not wm.exists(): wm = rd_alt/"window_metrics.json"
    wm_data = {}
    if wm.exists():
        try: wm_data = _j.loads(wm.read_text())
        except Exception: pass
    samples = wm_data.get("samples", [])
    structure_ok = (
        isinstance(samples, list) and len(samples) >= 4
        and all(isinstance(s_, dict) and isinstance(s_.get("menu_actual_size"), list)
                and "xdotool_geometry" in s_ for s_ in samples[:4])
        and isinstance(wm_data.get("wm_decoration_height"), int)
    )
    r["checks"]["window_metrics"] = 1.0 if structure_ok else 0.0; s += r["checks"]["window_metrics"]; t += 1

    # XCF for annotated — check both root and results/
    annot_xcfs = list(rd_results.glob("annotated_*.xcf")) + list(rd_alt.glob("annotated_*.xcf"))
    r["checks"]["annot_xcf"] = min(1.0, len(annot_xcfs)/3.0); s += r["checks"]["annot_xcf"]; t += 1
    xcf_layered = 0
    for x in annot_xcfs[:3]:
        try:
            head = x.read_bytes()[:14]
            if head.startswith(b"gimp xcf") and x.stat().st_size > 50_000:
                xcf_layered += 1
        except Exception: pass
    r["checks"]["annot_xcf_layered"] = xcf_layered / max(1, len(annot_xcfs[:3])); s += r["checks"]["annot_xcf_layered"]; t += 1

    # Extra evidence screenshots
    extra = ["view_godot_resized_native.png","view_xdotool_terminal.png","view_gimp_annotation_workflow.png"]
    extra_present = sum(1 for n in extra
                        if (rd_results/n).exists() or (rd_alt/n).exists())
    r["checks"]["evidence_screens"] = extra_present / len(extra); s += r["checks"]["evidence_screens"]; t += 1

    # ----- v2 weighted aggregation: core 60% / gui 30% / aux 10% -----
    def _g(k, default=0.0):
        v = r["checks"].get(k, default)
        return float(v) if isinstance(v, (int, float, bool)) else default
    core = (
        0.30 * (1.0 if r["checks"].get("sizes_match") else 0.0)
        + 0.20 * (1.0 if r["checks"].get("all_screens") else 0.0)
        + 0.20 * (1.0 if r["checks"].get("table_rows>=4") else 0.0)
        + 0.15 * (1.0 if r["checks"].get("bug_flagged") else 0.0)
        + 0.15 * _g("window_metrics")
    )
    gui = (
        0.40 * (1.0 if r["checks"].get("annotated_ok") else 0.0)
        + 0.30 * _g("annot_xcf")
        + 0.30 * _g("annot_xcf_layered")
    )
    aux = _g("evidence_screens")
    base = 0.60 * core + 0.30 * gui + 0.10 * aux

    # ----- v2 multi-tier hard gates (越严越好) -----
    if _g("window_metrics") < 1.0:
        base = min(base, 0.45)        # 关键取证缺失
    if _g("annot_xcf_layered") < 0.5:
        base = min(base, 0.55)
    if _g("annot_xcf") < 0.66:
        base = min(base, 0.55)
    if not r["checks"].get("annotated_ok"):
        base = min(base, 0.55)        # GUI 真实交互缺失
    if not r["checks"].get("sizes_match") or not r["checks"].get("all_screens"):
        base = min(base, 0.40)        # 核心交付物失败
    if _g("evidence_screens") < 1.0/3:
        base = min(base, 0.60)
    if _g("annot_unique_md5") == 0.0 or _g("annot_no_tiny") == 0.0:
        base = min(base, 0.40)        # 防伪截图作弊
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    sample = [str(p) for p in (annots[:3] or menus[:2]) if p.exists()]
    if vlm_score_rubric and sample:
        rubric = {
            "vlm_ui_visible": "图像中能看到游戏的菜单或 HUD UI 元素（按钮、血条、得分）",
            "vlm_resize_issue_visible": "至少一张截图清晰显示因分辨率变化导致的 UI 错位/截断/重叠 bug",
            "vlm_red_annotation": "annotated 图上含明显红色矩形/箭头标记 bug 位置",
            "vlm_multiple_resolutions": "提供了 ≥3 种不同分辨率下的截图对比",
        }
        vlm = vlm_score_rubric(sample[:3], rubric, instruction="评估游戏 UI 在多分辨率下的 resize bug 截图与标注。")
        for k in rubric: r["checks"][k] = vlm.get(k, 0.0)
        r["judge_method"] = vlm.get("judge_method", "failed")
        vlm_avg = sum(vlm.get(k, 0.0) for k in rubric)/len(rubric)
        # v2: 多级 VLM 阈值
        if vlm_avg < 0.4:
            base = min(base, 0.30)
        elif vlm_avg < 0.6:
            base = min(base, 0.45)
        r["overall_score"] = round((base + vlm_avg)/2, 3)
    else:
        # v2: VLM 不可用时退化分上限封顶 0.60
        r["overall_score"] = round(min(base, 0.60), 3)

    # ----- BEGIN CHEAT/VLM HARD-GATE (auto-injected) -----
    try:
        from _judge_helper import audit_chat_jsonl_for_banned as _audit
    except Exception:
        _audit = None
    _BANS = ['--headless', 'godot4 --check', 'project.godot']
    if _audit is not None:
        try:
            _a = _audit(_BANS)
            r["audit_total_tool_calls"] = _a.get("total_tool_calls", 0)
            r["audit_screenshots"] = _a.get("computer_screenshots", 0)
            r["audit_any_banned"] = 1.0 if _a.get("any_banned") else 0.0
            r["audit_matches"] = ",".join(_a.get("matches", [])[:5])
            if _a.get("any_banned") and _a.get("computer_screenshots", 0) == 0:
                r["overall_score"] = min(float(r.get("overall_score", 1.0)), 0.30)
            if _a.get("total_tool_calls", 0) >= 5 and _a.get("computer_screenshots", 0) == 0:
                r["overall_score"] = min(float(r.get("overall_score", 1.0)), 0.45)
        except Exception as _e:
            r["audit_error"] = str(_e)[:120]
    # ----- END CHEAT/VLM HARD-GATE -----
    return r


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
