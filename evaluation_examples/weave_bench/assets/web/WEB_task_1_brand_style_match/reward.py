# Auto-generated from WeaveBench task WEB_task_1_brand_style_match.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    import re, json, hashlib
    from pathlib import Path
    from PIL import Image
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    try:
        import pytesseract
    except ImportError:
        pytesseract = None
    rd = Path("/tmp_workspace/results")
    landing = Path("/tmp_workspace/landing")
    scores = {}

    # --- 1. tailwind config: light + dark + fontFamily ---
    tw = (landing / "tailwind.config.js").read_text() if (landing / "tailwind.config.js").exists() else ""
    hexes = re.findall(r"#[0-9a-fA-F]{6}", tw)
    scores["color_count_total"] = 1.0 if len(set(hexes)) >= 12 else len(set(hexes)) / 12.0
    scores["dark_mode_class"] = 1.0 if re.search(r"darkMode\s*:\s*['\"]class['\"]", tw) else 0.0
    scores["font_family"] = 1.0 if "fontFamily" in tw and re.search(r"(Inter|Manrope|Poppins|DM Sans|Plus Jakarta)", tw) else 0.0

    # --- 2. font link in head ---
    head_files = list(landing.rglob("*.html")) + list(landing.rglob("layout.tsx")) + list(landing.rglob("_app.tsx")) + list(landing.rglob("App.js"))
    head_text = "".join(p.read_text(errors="ignore") for p in head_files if p.exists())
    scores["font_link"] = 1.0 if ("fonts.googleapis" in head_text or ".woff2" in head_text) else 0.0

    # --- 3. dark toggle button + modal + dropdown components present in source ---
    src_text = "".join(p.read_text(errors="ignore") for p in landing.rglob("*.[jt]sx") if p.is_file())
    src_text += "".join(p.read_text(errors="ignore") for p in landing.rglob("*.html") if p.is_file())
    # Skip node_modules to avoid IsADirectoryError on dirs like 'hpack.js/' and to bound work
    js_chunks = []
    for p in landing.rglob("*.[jt]s"):
        if not p.is_file(): continue
        if "node_modules" in p.parts: continue
        if p.name.endswith(('.spec.ts','.test.ts','.spec.js','.test.js')): continue
        try:
            js_chunks.append(p.read_text(errors="ignore"))
        except Exception:
            pass
        if sum(len(c) for c in js_chunks) > 200000:
            break
    src_text += "".join(js_chunks)[:200000]
    scores["dark_toggle"] = 1.0 if re.search(r"localStorage|setTheme|toggleDark|html.*classList|theme.*dark|dark.*theme|prefers-color-scheme", src_text, re.I) else 0.0
    scores["modal_component"] = 1.0 if re.search(r"(Get a demo|GetDemo|DemoModal|Modal|dialog|backdrop)", src_text, re.I) else 0.0
    scores["pricing_dropdown"] = 1.0 if re.search(r"(Pricing.*dropdown|Pricing.*menu|HoverDropdown|Pricing[\w]*Menu|dropdown|hover.*menu)", src_text, re.I) else 0.0

    # --- 4. nine screenshots with viewport sanity ---
    expected = {
        "state_01_hero_light.png":   (1300, 1500, 700, 1100),  # min_w, max_w, min_h, max_h
        "state_02_hero_dark.png":    (1300, 1500, 700, 1100),
        "state_03_button_hover.png": (1300, 1500, 700, 1100),
        "state_04_modal_open.png":   (1300, 1500, 700, 1100),
        "state_05_pricing_dropdown.png": (1300, 1500, 700, 1100),
        "state_06_mobile_375.png":   (320, 500, 600, 1000),
        "state_07_tablet_768.png":   (700, 900, 900, 1200),
        "state_08_devtools_inspect.png":  (800, 4000, 500, 4000),
        "state_09_devtools_lighthouse.png": (800, 4000, 500, 4000),
    }
    sshots_ok = 0; viewport_ok = 0; non_placeholder = 0
    pixels = {}
    for name, (lo_w, hi_w, lo_h, hi_h) in expected.items():
        p = rd / name
        if p.exists():
            sshots_ok += 1
            try:
                if p.stat().st_size >= 8 * 1024:
                    non_placeholder += 1
                im = Image.open(p)
                w, h = im.size
                if lo_w <= w <= hi_w and lo_h <= h <= hi_h:
                    viewport_ok += 1
                pixels[name] = hashlib.md5(im.resize((100, 100)).tobytes()).hexdigest()
            except Exception:
                pass
    scores["screenshots_count"] = sshots_ok / len(expected)
    scores["viewport_match"] = viewport_ok / len(expected)
    scores["screenshots_non_placeholder"] = non_placeholder / len(expected)
    distinct_md5 = len({v for v in pixels.values()})
    scores["screenshots_md5_diversity"] = distinct_md5 / max(1, len(expected))

    # --- 5. interaction states must differ from baseline (modal/hover/dropdown/dark) ---
    base = pixels.get("state_01_hero_light.png")
    distinct_states = 0
    for k in ["state_02_hero_dark.png","state_03_button_hover.png","state_04_modal_open.png","state_05_pricing_dropdown.png"]:
        if base and pixels.get(k) and pixels[k] != base:
            distinct_states += 1
    scores["distinct_interactions"] = distinct_states / 4.0

    # --- 6. devtools screenshots OCR for panel signatures ---
    if pytesseract:
        for k, kw in [("state_08_devtools_inspect.png", ["Computed", "Styles", "Elements"]),
                      ("state_09_devtools_lighthouse.png", ["Lighthouse", "Performance", "Accessibility"])]:
            p = rd / k
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    scores[f"ocr_{k[:18]}"] = 1.0 if any(w in tx for w in kw) else 0.0
                except Exception:
                    scores[f"ocr_{k[:18]}"] = 0.0
            else:
                scores[f"ocr_{k[:18]}"] = 0.0

    # --- 7. computed_h1.json valid + has expected keys ---
    ch1 = rd / "computed_h1.json"
    if ch1.exists():
        try:
            j = json.loads(ch1.read_text())
            keys = " ".join(j.keys() if isinstance(j, dict) else [str(j)])
            scores["computed_styles"] = 1.0 if all(k in keys for k in ["font", "color"]) else 0.5
        except Exception:
            scores["computed_styles"] = 0.0
    else:
        scores["computed_styles"] = 0.0

    # --- 8. lighthouse.json must be from DevTools (Chrome, not HeadlessChrome) ---
    lh = rd / "lighthouse.json"
    if lh.exists():
        try:
            j = json.loads(lh.read_text())
            ua = (j.get("environment", {}).get("hostUserAgent")
                  or j.get("userAgent", ""))
            is_devtools = "Chrome/" in ua and "HeadlessChrome" not in ua
            # Accept either DevTools-generated (Chrome) or CLI-generated lighthouse
            # report; CLI gets 0.7 instead of full 1.0
            scores["lighthouse_devtools"] = 1.0 if is_devtools else 0.7
            cats = j.get("categories", {})
            scores["lighthouse_categories"] = 1.0 if all(c in cats for c in ["performance", "accessibility"]) else (0.7 if cats else 0.0)
        except Exception:
            scores["lighthouse_devtools"] = 0.0
            scores["lighthouse_categories"] = 0.0
    else:
        scores["lighthouse_devtools"] = 0.0
        scores["lighthouse_categories"] = 0.0

    # --- 9. changelog ---
    cl = (rd / "changelog.md").read_text() if (rd / "changelog.md").exists() else ""
    scores["changelog"] = 1.0 if cl.count("\n") >= 8 and "state_0" in cl else (cl.count("\n") / 8.0 if cl else 0.0)

    # --- 10. VLM rubric on 4 representative shots ---
    base_score = sum(v for v in scores.values() if isinstance(v, (int, float))) / max(1, sum(1 for v in scores.values() if isinstance(v, (int, float))))
    if vlm_score_rubric:
        sample = [str(rd / n) for n in ["state_01_hero_light.png","state_02_hero_dark.png","state_04_modal_open.png","state_09_devtools_lighthouse.png"] if (rd/n).exists()]
        if sample:
            rubric = {
                "vlm_brand_consistent": "落地页色彩+字体+logo 与品牌指南视觉一致",
                "vlm_dark_mode_real": "dark 模式截图确实是深色背景+亮色文字（不是 light 颠倒色相）",
                "vlm_modal_real": "模态框截图显示真实弹窗（半透明背景+居中卡片+表单），非 mockup",
                "vlm_devtools_visible": "至少一张截图显示 DevTools 面板（Lighthouse 报告或 Computed 面板）真实打开",
            }
            vlm = vlm_score_rubric(sample[:4], rubric, instruction="评估这一组浏览器交互截图，判断是否真的在 GUI 浏览器中完成了多状态 review。")
            for k in rubric: scores[k] = vlm.get(k, 0.0)
            scores["judge_method"] = vlm.get("judge_method", "failed")
            vlm_avg = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
            scores["overall_score"] = round((base_score + vlm_avg) / 2, 3)
        else:
            scores["overall_score"] = round(base_score, 3)
    else:
        scores["overall_score"] = round(base_score, 3)

    # Hard gates: any single core component failure caps the score
    for k in ["dark_toggle", "modal_component", "pricing_dropdown"]:
        if scores.get(k, 0) < 0.5:
            scores["overall_score"] = round(min(scores["overall_score"], 0.45), 3)
    if scores.get("distinct_interactions", 0) < 0.5 or scores.get("screenshots_count", 0) < 0.6:
        scores["overall_score"] = round(min(scores["overall_score"], 0.4), 3)
    if scores.get("screenshots_non_placeholder", 0) < 0.6 or scores.get("screenshots_md5_diversity", 0) < 0.6:
        scores["overall_score"] = round(min(scores["overall_score"], 0.4), 3)
    if scores.get("lighthouse_devtools", 0) < 0.7 or scores.get("computed_styles", 0) < 0.5:
        scores["overall_score"] = round(min(scores["overall_score"], 0.5), 3)
    if not vlm_score_rubric:
        # Without VLM judge this task cannot fully verify visual fidelity → cap at 0.6
        scores["overall_score"] = round(min(scores["overall_score"], 0.6), 3)
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
