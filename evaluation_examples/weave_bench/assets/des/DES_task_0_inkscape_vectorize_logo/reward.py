# Auto-generated from WeaveBench task DES_task_0_inkscape_vectorize_logo.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    import re
    from pathlib import Path
    from PIL import Image
    try: from _judge_helper import vlm_score_rubric
    except Exception: vlm_score_rubric = None
    try: import pytesseract
    except ImportError: pytesseract = None
    rd = Path("/tmp_workspace/results")
    rd_alt = Path("/tmp_workspace")
    def _R(name):
        p = rd / name
        return p if p.exists() else rd_alt / name
    scores = {}

    files = ["logo.svg","logo_dark.svg","logo_64.png","logo_256.png","logo_512.png",
             "logo_1024.png","logo_print_cmyk.pdf","logo_sprite.svg"]
    scores["files_count"] = sum(1 for f in files if _R(f).exists()) / len(files)

    svg_p = _R("logo.svg")
    svg = svg_p.read_text(errors="ignore") if svg_p.exists() else ""

    # node count: count d="..." command letters
    cmd_letters = re.findall(r"[MmLlHhVvCcSsQqTtAaZz]", " ".join(re.findall(r'd="([^"]*)"', svg)))
    n_nodes = len(cmd_letters)
    scores["nodes_in_range"] = 1.0 if 50 <= n_nodes <= 300 else (0.5 if (n_nodes > 0 and n_nodes < 600) else 0.0)

    # fill color count ≤4
    fills = set(re.findall(r'fill\s*=\s*"(#[0-9a-fA-F]{6})"', svg))
    fills |= set(m.lower() for m in re.findall(r'fill:\s*(#[0-9a-fA-F]{6})', svg))
    scores["fill_color_count"] = 1.0 if (1 <= len(fills) <= 4) else 0.5 if len(fills) <= 6 else 0.0

    # no embedded raster
    scores["no_image_tag"] = 1.0 if "<image " not in svg else 0.0

    # has text element
    scores["has_text"] = 1.0 if "<text" in svg else 0.0

    # has #reg id
    scores["has_reg_mark"] = 1.0 if (re.search(r'id\s*=\s*"reg"', svg) or 'id="reg"' in svg) else 0.0

    # title + desc (safe against <desc/> self-close)
    desc_m = re.search(r"<desc[^>]*>(.*?)</desc>", svg, re.S) if svg else None
    desc_len = len(desc_m.group(1).strip()) if desc_m else 0
    if "<title>" in svg and "<desc" in svg and desc_len >= 80:
        scores["has_title_desc"] = 1.0
    elif "<title>" in svg:
        scores["has_title_desc"] = 0.5
    else:
        scores["has_title_desc"] = 0.0

    # Inter Bold font in <text>
    has_inter = bool(re.search(r'font-family\s*[:=]\s*["\']?[^"\';>]*Inter', svg, re.I))
    has_bold = bool(re.search(r'font-weight\s*[:=]\s*["\']?\s*(bold|[6-9]00)', svg, re.I))
    scores["text_inter_bold"] = 1.0 if (has_inter and has_bold) else (0.5 if has_inter else 0.0)

    # >=2 inkscape layers
    n_layers = len(re.findall(r'inkscape:groupmode\s*=\s*"layer"', svg))
    scores["layers_count"] = 1.0 if n_layers >= 2 else (0.5 if n_layers == 1 else 0.0)

    # brand color match (ΔE2000 <= 8 each fill vs brand_colors.txt)
    bc_p = Path("/tmp_workspace/brand_colors.txt")
    brand_hex = []
    if bc_p.exists():
        for line in bc_p.read_text(errors="ignore").splitlines():
            m = re.search(r"#([0-9a-fA-F]{6})", line)
            if m: brand_hex.append("#" + m.group(1).lower())
    def _hex_to_lab(h):
        r = int(h[1:3],16)/255.0; g = int(h[3:5],16)/255.0; b = int(h[5:7],16)/255.0
        def f(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
        r,g,b = f(r),f(g),f(b)
        x = (r*0.4124+g*0.3576+b*0.1805)/0.95047
        y = (r*0.2126+g*0.7152+b*0.0722)/1.0
        z = (r*0.0193+g*0.1192+b*0.9505)/1.08883
        def fl(t): return t**(1/3) if t>0.008856 else 7.787*t+16/116
        L = 116*fl(y)-16; A = 500*(fl(x)-fl(y)); B = 200*(fl(y)-fl(z))
        return (L,A,B)
    def _de76(c1,c2):
        return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2) ** 0.5
    if fills and brand_hex:
        brand_labs = [_hex_to_lab(h) for h in brand_hex]
        ok = 0
        for f in fills:
            try:
                lab = _hex_to_lab(f.lower())
                if min(_de76(lab,bl) for bl in brand_labs) <= 10:  # tighter ΔE proxy
                    ok += 1
            except Exception: pass
        scores["brand_color_match"] = ok / len(fills)
    else:
        scores["brand_color_match"] = 0.0

    # dark variant white fill
    dark_svg_p = _R("logo_dark.svg")
    dark_svg = dark_svg_p.read_text(errors="ignore") if dark_svg_p.exists() else ""
    scores["dark_white"] = 1.0 if re.search(r'fill\s*=\s*"#?[fF]{3,6}"|fill:\s*#?[fF]{3,6}', dark_svg) else 0.0

    # PNG sizes
    for n, sz in [("logo_64.png",64),("logo_256.png",256),("logo_512.png",512),("logo_1024.png",1024)]:
        f = _R(n)
        ok = 0.0
        if f.exists():
            try:
                if Image.open(f).size == (sz, sz): ok = 1.0
            except Exception: pass
        scores[f"png_{sz}"] = ok

    # CMYK PDF: %PDF header + DeviceCMYK / CMYK colorspace marker
    pdf = _R("logo_print_cmyk.pdf")
    if pdf.exists():
        try:
            data = pdf.read_bytes()
            head_ok = data[:4] == b"%PDF"
            cmyk_ok = (b"/DeviceCMYK" in data) or (b"/CMYK" in data) or (b"DefaultCMYK" in data)
            if head_ok and cmyk_ok:
                scores["pdf_valid"] = 1.0
            elif head_ok:
                scores["pdf_valid"] = 0.5
            else:
                scores["pdf_valid"] = 0.0
        except Exception: scores["pdf_valid"] = 0.0
    else: scores["pdf_valid"] = 0.0

    # sprite contains 2 symbols
    sprite_p = _R("logo_sprite.svg")
    sprite_svg = sprite_p.read_text(errors="ignore") if sprite_p.exists() else ""
    scores["sprite_two_symbols"] = 1.0 if (sprite_svg.count("<symbol") >= 2) else (0.5 if "<symbol" in sprite_svg else 0.0)

    # 4 Inkscape screenshots + OCR + anti-cheat (md5 unique, size>=5KB, resolution sane)
    import hashlib
    shots = ["view_01_trace_dialog.png","view_02_node_edit.png","view_03_xml_editor.png","view_04_layers_panel.png"]
    valid_shots = []
    md5s = set()
    for n in shots:
        p = _R(n)
        if not p.exists():
            continue
        try:
            b = p.read_bytes()
            if len(b) < 5 * 1024:
                continue
            h = hashlib.md5(b).hexdigest()
            if h in md5s:
                continue
            md5s.add(h)
            try:
                w, hpx = Image.open(p).size
                if w < 1024 or hpx < 600:
                    continue
            except Exception:
                continue
            valid_shots.append((n, p))
        except Exception:
            continue
    scores["inkscape_shots_count"] = len(valid_shots) / len(shots)
    ui_hits = 0
    if pytesseract:
        for n, p in valid_shots:
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k in tx for k in ["Inkscape","Trace","Node","XML","Layer","Path","X:","Y:"]):
                    ui_hits += 1
            except Exception: pass
    scores["inkscape_ui_ocr"] = ui_hits / len(shots)

    # weighted overall: core deliverables 60% / GUI evidence 30% / aux 10%
    core_keys = ["files_count","nodes_in_range","fill_color_count","no_image_tag",
                 "has_text","has_reg_mark","has_title_desc","text_inter_bold",
                 "layers_count","brand_color_match","pdf_valid","sprite_two_symbols"]
    gui_keys  = ["inkscape_shots_count","inkscape_ui_ocr"]
    aux_keys  = ["dark_white","png_64","png_256","png_512","png_1024"]
    def _avg(keys):
        vals = [scores[k] for k in keys if k in scores and isinstance(scores[k],(int,float))]
        return sum(vals)/len(vals) if vals else 0.0
    base = 0.6*_avg(core_keys) + 0.3*_avg(gui_keys) + 0.1*_avg(aux_keys)

    vlm_available = False
    if vlm_score_rubric and _R("logo_512.png").exists():
        rubric = {
            "vlm_logo_recognizable": "图像呈现一个干净、可识别的 logo 形状",
            "vlm_clean_vector": "线条干净无锯齿，符合矢量产物特征",
            "vlm_text_readable": "文字部分清晰可读、字体一致",
        }
        vlm = vlm_score_rubric([str(_R("logo_512.png"))], rubric, instruction="评估矢量化 logo 视觉质量。")
        for k in rubric: scores[k] = vlm.get(k, 0.0)
        scores["judge_method"] = vlm.get("judge_method", "failed")
        if scores["judge_method"] != "failed":
            vlm_available = True
            vlm_avg = sum(vlm.get(k,0) for k in rubric)/len(rubric)
            scores["overall_score"] = round(0.7*base + 0.3*vlm_avg, 3)
        else:
            scores["overall_score"] = round(base, 3)
    else:
        scores["overall_score"] = round(base, 3)

    # multi-layer hard gates (越严越好)
    if scores.get("nodes_in_range", 0) < 1.0:
        scores["overall_score"] = round(min(scores["overall_score"], 0.45), 3)
    if scores.get("has_reg_mark", 0) < 1.0:
        scores["overall_score"] = round(min(scores["overall_score"], 0.45), 3)
    if scores.get("has_text", 0) < 1.0:
        scores["overall_score"] = round(min(scores["overall_score"], 0.45), 3)
    if scores.get("brand_color_match", 0) < 0.75:
        scores["overall_score"] = round(min(scores["overall_score"], 0.55), 3)
    if scores.get("pdf_valid", 0) < 1.0:
        scores["overall_score"] = round(min(scores["overall_score"], 0.55), 3)
    if scores.get("inkscape_shots_count", 0) < 1.0:
        scores["overall_score"] = round(min(scores["overall_score"], 0.50), 3)
    if scores.get("inkscape_ui_ocr", 0) < 0.5:
        scores["overall_score"] = round(min(scores["overall_score"], 0.55), 3)
    if scores.get("files_count", 0) < 1.0:
        scores["overall_score"] = round(min(scores["overall_score"], 0.55), 3)
    if not vlm_available:
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
