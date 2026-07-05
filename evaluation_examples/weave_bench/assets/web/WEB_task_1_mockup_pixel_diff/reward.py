# Auto-generated from WeaveBench task WEB_task_1_mockup_pixel_diff.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    import json, hashlib
    from pathlib import Path
    try:
        from PIL import Image, ImageChops
    except Exception:
        Image = None
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/tmp_workspace/gt")
    design_dir = Path("/tmp_workspace/design")
    scores = {}

    # ---- 1+2. diffs.json existence + schema -----------------------------
    diffs_path = rd / "diffs.json"
    diffs = []
    if diffs_path.exists():
        try:
            diffs = json.loads(diffs_path.read_text(encoding="utf-8"))
        except Exception:
            diffs = []
    scores["diffs_json"] = 1.0 if isinstance(diffs, list) and diffs else 0.0
    REQ = {"page", "element", "property", "expected", "actual"}
    schema_ok = sum(1 for d in diffs
                    if isinstance(d, dict) and REQ.issubset(d.keys())) if diffs else 0
    scores["diffs_schema"] = (schema_ok / len(diffs)) if diffs else 0.0
    scores["diffs_count_ok"] = 1.0 if len(diffs) >= 10 else len(diffs) / 10.0
    scores["diffs_count_raw"] = len(diffs)

    # ---- 3. diff F1 against GT on (page, property) ----------------------
    # Plus tighter: count how many predicted diffs include the EXACT expected
    # hex / px value as a substring of `expected` or `actual`. This forces the
    # agent to look at the actual rendered/mockup colors, not just guess.
    expected_path = gt_dir / "expected_diffs.json"
    f1 = 0.0
    exact_value_hits = 0
    if expected_path.exists() and diffs:
        try:
            gt = json.loads(expected_path.read_text(encoding="utf-8"))
            gt_pairs = {(g["page"].lower(), g["property"].lower()) for g in gt}
            pred_pairs = {(str(d.get("page","")).lower(),
                           str(d.get("property","")).lower())
                          for d in diffs if isinstance(d, dict)}
            tp = len(gt_pairs & pred_pairs)
            prec = tp / len(pred_pairs) if pred_pairs else 0.0
            rec  = tp / len(gt_pairs) if gt_pairs else 0.0
            f1 = (2*prec*rec/(prec+rec)) if (prec+rec) else 0.0

            # Exact-value match: for each GT row, see if any pred row with same
            # (page, property) contains the GT value inside expected/actual.
            for g in gt:
                key = (g["page"].lower(), g["property"].lower())
                gv_exp = str(g["expected"]).lower()
                gv_act = str(g["actual"]).lower()
                for d in diffs:
                    if not isinstance(d, dict): continue
                    if (str(d.get("page","")).lower(),
                        str(d.get("property","")).lower()) != key:
                        continue
                    blob = (str(d.get("expected","")) + " " +
                            str(d.get("actual",""))).lower()
                    if gv_exp in blob and gv_act in blob:
                        exact_value_hits += 1
                        break
        except Exception:
            pass
    scores["diff_f1"] = round(f1, 3)
    scores["diff_f1_pass"] = 1.0 if f1 >= 0.6 else 0.0
    scores["exact_value_hits"] = exact_value_hits
    # v2: tightened — require ≥8 of 12 exact-value matches for full credit
    scores["exact_value_pass"] = min(1.0, exact_value_hits / 8.0)

    # ---- 4+5. after PNGs exist + STRICT pixel match against mockups -----
    PAGES = ["home", "pricing", "about", "contact"]
    after_dir = rd / "after"
    after_ok = 0
    pixel_ok = 0
    pix_ratios = {}
    for pg in PAGES:
        ap = after_dir / f"{pg}.png"
        mp = design_dir / f"{pg}.png"
        if not ap.exists():
            continue
        after_ok += 1
        if Image is None or not mp.exists():
            continue
        try:
            a = Image.open(ap).convert("RGB")
            m = Image.open(mp).convert("RGB")
            if a.size != m.size:
                a = a.resize(m.size)
            diff = ImageChops.difference(a, m)
            data = list(diff.getdata())
            differing = sum(1 for px in data if any(c > 8 for c in px))
            ratio = differing / len(data)
            pix_ratios[pg] = round(ratio, 4)
            # tighter than before (was 1.5%, now 0.8%)
            if ratio < 0.008:
                pixel_ok += 1
        except Exception:
            pix_ratios[pg] = -1
    scores["after_png_count"] = after_ok / len(PAGES)
    scores["after_pixel_match"] = pixel_ok / len(PAGES)
    scores["pixel_ratios"] = pix_ratios

    # ---- 6. styles.css actually changed --------------------------------
    css = Path("/tmp_workspace/app/styles.css")
    init_hash = Path("/tmp_workspace/.app_styles.sha256")
    css_changed = 0.0
    if css.exists() and init_hash.exists():
        cur = hashlib.sha256(css.read_bytes()).hexdigest()
        css_changed = 0.0 if cur == init_hash.read_text().strip() else 1.0
    scores["css_modified"] = css_changed

    # ---- aggregate (deterministic part) --------------------------------
    # v2: weighted as core (60%) / GUI evidence (30%) / aux (10%)
    core = (
        0.30 * scores["after_pixel_match"] +   # 真正修对的证据
        0.20 * scores["exact_value_pass"] +    # 必须看到真实数值
        0.10 * scores["diff_f1_pass"]          # GT pair 命中
    ) / 0.60
    gui = (
        0.20 * scores["after_png_count"] +     # 截图齐
        0.10 * scores["css_modified"]          # CSS 真改了
    ) / 0.30
    aux = (
        0.04 * scores["diffs_json"] +
        0.03 * scores["diffs_schema"] +
        0.03 * scores["diffs_count_ok"]
    ) / 0.10
    base = 0.6*core + 0.3*gui + 0.1*aux

    # v2: 多层 hard gate
    # gate-1: CSS 没真改 -> cap 0.30 (退化路径)
    if scores["css_modified"] < 1.0:
        base = min(base, 0.30)
    # gate-2: after 截图不齐 (<3/4) -> cap 0.40
    if scores["after_png_count"] < 0.75:
        base = min(base, 0.40)
    # gate-3: 像素匹配差 -> cap 0.45 (v2 比首轮 0.5 更严)
    if scores["after_pixel_match"] < 0.5:
        base = min(base, 0.45)
    # gate-4: 关键诊断维度 (F1+exact_value) 双低 -> cap 0.50
    if scores["diff_f1_pass"] < 1.0 and scores["exact_value_pass"] < 0.5:
        base = min(base, 0.50)
    scores["overall_score"] = round(base, 3)

    # ---- 7. VLM rubric (optional bonus) --------------------------------
    if vlm_score_rubric:
        imgs = []
        for pg in PAGES:
            ap = after_dir / f"{pg}.png"
            mp = design_dir / f"{pg}.png"
            if ap.exists() and mp.exists():
                imgs.extend([str(ap), str(mp)])
        if imgs:
            rubric = {
                "vlm_after_matches_mockup": "after 截图整体与 mockup 视觉一致（颜色/布局/字号/阴影 接近）",
                "vlm_no_obvious_regression": "after 截图本身没有明显排版破损（如重叠、错位、空白）",
            }
            try:
                vlm = vlm_score_rubric(imgs, rubric,
                    instruction="判断修复后的实现截图与设计 mockup 是否视觉一致。")
                for k in rubric: scores[k] = vlm.get(k, 0.0)
                scores["judge_method"] = vlm.get("judge_method", "failed")
                vlm_avg = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
                scores["overall_score"] = round(0.5*base + 0.5*vlm_avg, 3)
                # v2 HARD GATE: VLM judges the visual rubric.
                if scores.get("vlm_after_matches_mockup", 0.0) < 0.6:
                    scores["overall_score"] = min(scores["overall_score"], 0.40)
                if scores.get("vlm_after_matches_mockup", 0.0) < 0.4:
                    scores["overall_score"] = min(scores["overall_score"], 0.25)
            except Exception:
                pass
    else:
        # v2: VLM 不可用时退化分上限封顶 0.6 (防"无 VLM 也能满分"路径)
        scores["judge_method"] = "vlm_unavailable"
        scores["overall_score"] = round(min(scores["overall_score"], 0.60), 3)
    return scores


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
