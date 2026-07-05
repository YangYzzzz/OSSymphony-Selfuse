# Auto-generated from WeaveBench task DSK_task_6_flameshot_annotate_ocr.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DSK_task_6 grader (v2: weighted + cheat-resistant)."""
    import json, csv, re, hashlib
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    def _md5(p):
        try: return hashlib.md5(p.read_bytes()).hexdigest()
        except Exception: return None

    # 1. CLI artifacts
    cli_files = ["instructions_pretty.txt","keyword_hit_rate.csv","per_image_summary.json"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 1

    # 2. annotated/*.png
    ann_dir = rd / "annotated"
    ann_count = 0
    if ann_dir.exists():
        ann_count = len(list(ann_dir.glob("annotated_*.png")))
    s["annotated_count"] = min(1.0, ann_count / 6)

    # 3. ocr_outputs/*.txt
    ocr_dir = rd / "ocr_outputs"
    ocr_count = 0
    if ocr_dir.exists():
        for f in ocr_dir.glob("ocr_*.txt"):
            if f.stat().st_size > 5: ocr_count += 1
    s["ocr_count"] = min(1.0, ocr_count / 6)

    # 4. hit rate
    hr_score = 0.0
    hf = rd / "keyword_hit_rate.csv"
    if hf.exists():
        try:
            rows = list(csv.DictReader(hf.open()))
            need = {"screenshot_id","total_keywords","hits","hit_rate"}
            if rows and need.issubset(set(rows[0].keys())):
                good = sum(1 for r in rows if float(r["hit_rate"]) >= 0.60)
                hr_score = good / max(6, len(rows))
        except Exception: pass
    s["keyword_hit_rate"] = hr_score

    # 5. GUI screenshots
    gui_shots = ["view_flameshot_step1.png","view_flameshot_step3.png","view_flameshot_step5.png","view_flameshot_complete.png"]
    gui_present = sum(1 for n in gui_shots if (rd / n).exists())
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui = gui_present >= 2

    # 5b. GUI screenshots integrity: md5 unique + size >= 8KB + resolution >= 800x600
    gui_md5s, gui_size_ok, gui_res_ok = set(), 0, 0
    try:
        from PIL import Image as _Img2
        for n in gui_shots:
            p = rd / n
            if not p.exists(): continue
            try:
                if p.stat().st_size >= 8 * 1024: gui_size_ok += 1
                m = _md5(p)
                if m: gui_md5s.add(m)
                im = _Img2.open(p)
                w, h = im.size
                if w >= 800 and h >= 600: gui_res_ok += 1
            except Exception: pass
    except Exception: pass
    n_total = max(1, gui_present)
    md5_unique_ratio = len(gui_md5s) / n_total
    size_ratio = gui_size_ok / n_total
    res_ratio = gui_res_ok / n_total
    s["gui_screenshots_integrity"] = round(min(md5_unique_ratio, size_ratio, res_ratio), 3)
    gui_authentic = (gui_present >= 3 and md5_unique_ratio >= 0.75 and size_ratio >= 0.75 and res_ratio >= 0.75)

    try:
        import pytesseract
        from PIL import Image
        kws_any = ["flameshot","Tools","Pencil","Rectangle","Arrow","Text","Color","Save"]
        ocr_hits = 0
        for n in gui_shots:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in kws_any): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
    except Exception:
        s["gui_screenshots_ocr"] = 0.5 if gui_present > 0 else 0.0

    # 6. ocr_summary.md
    rp_score = 0.0
    rp = rd / "ocr_summary.md"
    if rp.exists():
        try:
            txt = rp.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            rp_score = min(1.0, len(parags) / 4)
        except Exception: pass
    s["ocr_summary"] = rp_score

    # 7. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_available = bool(vlm_score_rubric)
    if vlm_score_rubric and ann_count > 0:
        rubric = {
            "vlm_annotation_visible": "annotated 截图能看到 rect / 箭头 / text 标注",
            "vlm_annotation_color_correct": "标注颜色按 instructions(rect=red, arrow=green 等)",
            "vlm_text_not_obscured": "标注没有完全盖住下面的文本",
            "vlm_flameshot_toolbar": "flameshot 截图含工具栏 / 标注按钮",
        }
        try:
            imgs = []
            for n in ("annotated_1.png","annotated_3.png","annotated_5.png"):
                p = ann_dir / n
                if p.exists(): imgs.append(str(p))
            if (rd / "view_flameshot_step1.png").exists():
                imgs.append(str(rd / "view_flameshot_step1.png"))
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 flameshot 标注 + OCR pipeline 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_annotation_visible","vlm_annotation_color_correct","vlm_text_not_obscured","vlm_flameshot_toolbar"]:
            s[k] = 0.0

    # 8. Content-reality sub-scores
    # 8a. annotated PNGs contain real annotation color pixels (red / yellow / green)
    ann_color_ok = 0
    ann_total = 0
    ann_md5s = set()
    ann_size_ok = 0
    try:
        from PIL import Image as _Img
        if ann_dir.exists():
            for f in sorted(ann_dir.glob("annotated_*.png"))[:6]:
                ann_total += 1
                try:
                    if f.stat().st_size >= 5 * 1024: ann_size_ok += 1
                    m = _md5(f)
                    if m: ann_md5s.add(m)
                    im = _Img.open(f).convert("RGB")
                    w, h = im.size
                    pixels = list(im.getdata())
                    step = max(1, len(pixels) // 5000)
                    hits = 0
                    for i in range(0, len(pixels), step):
                        r, g, b = pixels[i]
                        if (r > 180 and g < 90 and b < 90) or \
                           (r > 200 and g > 180 and b < 90) or \
                           (r < 90 and g > 180 and b < 90):
                            hits += 1
                            if hits >= 8:
                                break
                    if hits >= 8:
                        ann_color_ok += 1
                except Exception:
                    pass
    except Exception:
        pass
    if ann_total == 0:
        s["annotation_color_present"] = 0.0
        s["annotated_integrity"] = 0.0
    else:
        s["annotation_color_present"] = round(ann_color_ok / ann_total, 3)
        s["annotated_integrity"] = round(min(len(ann_md5s) / ann_total, ann_size_ok / ann_total), 3)

    # 8b. ocr_outputs hit >= 3 plausible English keywords across all files
    ocr_kw = ["the", "and", "is", "in", "of", "to", "for", "with", "this", "that",
              "button", "click", "window", "menu", "file", "save", "open", "close", "help"]
    total_hits = 0
    if ocr_dir.exists():
        for f in ocr_dir.glob("ocr_*.txt"):
            try:
                t = f.read_text(errors="ignore").lower()
                for k in ocr_kw:
                    if re.search(r"\b" + re.escape(k) + r"\b", t):
                        total_hits += 1
            except Exception:
                pass
    if total_hits >= 9:
        s["ocr_keyword_hits"] = 1.0
    elif total_hits >= 3:
        s["ocr_keyword_hits"] = round(total_hits / 9.0, 3)
    else:
        s["ocr_keyword_hits"] = 0.0

    # Weighted aggregation: core delivery 60% + GUI evidence 30% + auxiliary 10%
    core_keys = ["cli_artifacts","annotated_count","ocr_count","keyword_hit_rate","annotation_color_present","annotated_integrity","ocr_keyword_hits"]
    gui_keys  = ["gui_screenshots_count","gui_screenshots_ocr","gui_screenshots_integrity"]
    aux_keys  = ["ocr_summary","vlm_annotation_visible","vlm_annotation_color_correct","vlm_text_not_obscured","vlm_flameshot_toolbar"]
    def _avg(keys):
        vs = [float(s[k]) for k in keys if k in s and isinstance(s[k],(int,float))]
        return sum(vs)/len(vs) if vs else 0.0
    core = _avg(core_keys); gui = _avg(gui_keys); aux = _avg(aux_keys)
    base = 0.60 * core + 0.30 * gui + 0.10 * aux

    # Hard gates (tightened)
    if not has_cli: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.25)
    if s["annotated_count"] < 0.67: base = min(base, 0.40)        # need >=4/6 annotated
    if s["ocr_count"] < 0.67:       base = min(base, 0.45)        # need >=4/6 ocr
    if s["keyword_hit_rate"] < 0.5: base = min(base, 0.55)
    if s["annotation_color_present"] < 0.5: base = min(base, 0.45)
    if s["ocr_keyword_hits"] < 0.34:        base = min(base, 0.50)
    if s["annotated_count"] < 0.34:         base = min(base, 0.35)
    # GUI authenticity gates
    if not gui_authentic:                           base = min(base, 0.55)
    if s["gui_screenshots_integrity"] < 0.5:        base = min(base, 0.50)
    if s["annotated_integrity"] < 0.5:              base = min(base, 0.55)
    if s.get("gui_screenshots_ocr", 0.0) < 0.5:     base = min(base, 0.60)
    # VLM unavailable -> cap (cannot fully verify visual quality)
    if not vlm_available:                           base = min(base, 0.65)

    s["overall_score"] = round(max(0.0, base), 4)
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
