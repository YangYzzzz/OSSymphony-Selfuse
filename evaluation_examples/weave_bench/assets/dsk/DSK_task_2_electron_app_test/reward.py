# Auto-generated from WeaveBench task DSK_task_2_electron_app_test.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

from pathlib import Path
import hashlib
try:
    import pytesseract
except ImportError:
    pytesseract = None
from PIL import Image
import numpy as np

SCREENS = ["preview.png","notebook_list.png","tags.png","checked.png","bug_emoji.png","help_view.png"]
MIN_BYTES = 8000
MIN_W, MIN_H = 1024, 600

def _valid_screenshot(p):
    try:
        if not p.exists() or p.stat().st_size < MIN_BYTES: return False
        with Image.open(p) as im:
            w,h = im.size
        return w >= MIN_W and h >= MIN_H
    except Exception:
        return False

def _md5(p):
    try: return hashlib.md5(p.read_bytes()).hexdigest()
    except Exception: return None

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    r = {"checks": {}, "overall_score": 0.0}

    # ---- screenshot validity (size + resolution) ----
    valid = {n: _valid_screenshot(workspace/n) for n in SCREENS}
    n_valid = sum(valid.values())
    r["checks"]["screens_valid"] = f"{n_valid}/6"

    # ---- md5 uniqueness (anti-cheat: same screenshot renamed) ----
    md5s = [_md5(workspace/n) for n in SCREENS if valid[n]]
    md5s = [m for m in md5s if m]
    n_unique = len(set(md5s))
    md5_ok = (n_valid == 0) or (n_unique >= max(2, n_valid - 1))
    r["checks"]["screens_unique"] = f"{n_unique}/{len(md5s)}"

    # ---- core: bug_report + no_backdoor ----
    core = 0.0
    br = workspace/"bug_report.md"
    if br.exists():
        c = br.read_text(errors="ignore").lower()
        if all(k in c for k in ["reproduction","expected","actual"]) and ("view" in c or "affected" in c) and len(c) >= 200:
            r["checks"]["bug_report"] = True; core += 0.6
        elif len(c) >= 120 and any(k in c for k in ["reproduction","expected","actual"]):
            r["checks"]["bug_report_partial"] = True; core += 0.25
    log = workspace/"actions.log"
    backdoor_terms = ["sqlite3.connect","ipcMain","joplin.data.get","./database.sqlite","direct sql"]
    if log.exists() and any(k in log.read_text(errors="ignore") for k in backdoor_terms):
        r["checks"]["backdoor_detected"] = True   # used as hard gate below
    else:
        r["checks"]["no_backdoor"] = True; core += 0.4

    # ---- gui: 6-screen presence + OCR signals + emoji-diff ----
    gui = 0.0
    gui += 0.25 * (n_valid / 6.0)            # screen completeness (resolution-checked)

    pp = workspace/"preview.png"; bp = workspace/"bug_emoji.png"; tp = workspace/"tags.png"
    preview_ocr = tags_ocr = False
    if valid["preview.png"] and pytesseract:
        try:
            tx = pytesseract.image_to_string(Image.open(pp))
            if "Bug Repro" in tx and ("|" in tx or "Action" in tx or "Expected" in tx):
                preview_ocr = True
        except Exception: pass
    if valid["tags.png"] and pytesseract:
        try:
            tx = pytesseract.image_to_string(Image.open(tp))
            if "test-bug" in tx.lower() or ("tag" in tx.lower() and ("notebook" in tx.lower() or "note" in tx.lower())):
                tags_ocr = True
        except Exception: pass
    if preview_ocr: r["checks"]["preview_ocr"] = True; gui += 0.25
    if tags_ocr:    r["checks"]["tags_ocr"]    = True; gui += 0.20

    # emoji rendering diff: compare title strip of preview vs bug_emoji
    if valid["preview.png"] and valid["bug_emoji.png"]:
        try:
            a = np.array(Image.open(pp).convert("L").resize((400,60)))
            b = np.array(Image.open(bp).convert("L").resize((400,60)))
            diff = float(np.mean(np.abs(a.astype(int) - b.astype(int)))) / 255.0
            r["checks"][f"emoji_diff={diff:.3f}"] = True
            if diff > 0.08: gui += 0.30
            elif diff > 0.04: gui += 0.15
        except Exception: pass

    gui = min(gui, 1.0)

    # ---- aux: VLM rubric ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    imgs = [str(workspace/n) for n in SCREENS if valid[n]]
    aux = 0.0
    real_vlm = 0
    if vlm_score_rubric and imgs:
        rubric = {
            "vlm_app_running": "截图清晰显示 Joplin Electron 桌面应用界面（左侧 Notebook 栏 / Markdown 预览 / 编辑器三联布局）",
            "vlm_table_rendered": "preview 中含 Markdown 表格（多行多列结构可见，非纯文本管道符）",
            "vlm_checkboxes_present": "可见任务列表的 5 个 checkbox 且至少部分被勾选",
            "vlm_emoji_or_bug_text": "图中能正确渲染 🐛 或类似 emoji（非乱码 □/?），与 Bug Repro 文本同框",
            "vlm_tag_visible": "tags 截图中可见 Joplin 的 Tag 面板/标签 chip（出现 test-bug 或 Tags 标签）",
        }
        vlm = vlm_score_rubric(imgs[:6], rubric, instruction="评估 Joplin Electron 桌面应用 GUI 回归测试截图。")
        for k in rubric: r["checks"][k] = vlm.get(k, 0.0)
        r["judge_method"] = vlm.get("judge_method", "failed")
        aux = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
        real_vlm = sum(1 for k in rubric if r["checks"].get(k, 0) >= 0.5)

    # ---- weighted overall: core 40% / gui 40% / aux 20% ----
    overall = 0.40 * core + 0.40 * gui + 0.20 * aux
    r["checks"]["_w"] = f"core={core:.2f} gui={gui:.2f} aux={aux:.2f}"

    # ---- multi-tier hard gates ----
    has_ocr = preview_ocr or tags_ocr
    if r["checks"].get("backdoor_detected"):
        overall = min(overall, 0.20)
    if n_valid < 3:
        overall = min(overall, 0.25)
    if not md5_ok:
        overall = min(overall, 0.40)         # screenshots are duplicates → cheat
    if n_valid < 5:
        overall = min(overall, 0.45)
    if not has_ocr:
        overall = min(overall, 0.45)         # no real Joplin text was OCR'd
    if vlm_score_rubric and imgs:
        if real_vlm < 2: overall = min(overall, 0.30)
        elif real_vlm < 4: overall = min(overall, 0.55)
    else:
        overall = min(overall, 0.65)         # VLM unavailable → fallback cap

    r["overall_score"] = round(max(0.0, overall), 3)
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
