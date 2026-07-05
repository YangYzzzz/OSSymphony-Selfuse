# Auto-generated from WeaveBench task DOC_task_3_xmind_brainstorm.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

from pathlib import Path
import zipfile, json, re, hashlib
try:
    import pytesseract
except Exception:
    pytesseract = None
from PIL import Image

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    r = {"checks": {}, "overall_score": 0.0}
    core = {}   # 核心交付：xmind 结构 / 产物文件
    gui = {}    # GUI 真实证据：截图 OCR / 唯一性 / 分辨率 / 大小
    aux = {}    # 辅助：md 大纲 / png 大图

    xm = workspace / "mindmap.xmind"
    nodes_total = 0; l1_count = 0; rel_entries = 0; link_entries = 0
    has_attach = False; notes_total_len = 0; notes_count = 0
    icons_hit = 0; styling_hits = 0
    if xm.exists() and xm.stat().st_size >= 2048:
        try:
            with zipfile.ZipFile(xm) as z:
                cj = json.loads(z.read("content.json").decode())
                names = z.namelist()
                has_attach = any(n.startswith("attachments/") and not n.endswith("/") for n in names)
            def walk(n, d=0, acc=None):
                if acc is None: acc = []
                acc.append((n.get("title", ""), d))
                for c in (n.get("children", {}).get("attached") or []):
                    walk(c, d + 1, acc)
                return acc
            nodes = walk(cj[0]["rootTopic"])
            nodes_total = len(nodes)
            l1_count = sum(1 for _, d in nodes if d == 1)
            max_depth = max((d for _, d in nodes), default=0)
            txt = json.dumps(cj, ensure_ascii=False)
            core["nodes>=50"] = 1.0 if nodes_total >= 50 else nodes_total / 50.0
            core["l1>=6"] = 1.0 if l1_count >= 6 else l1_count / 6.0
            core["depth>=4"] = 1.0 if max_depth >= 3 else max_depth / 3.0  # depth index 0..3 == 4 layers
            for grp in (["warning", "lightbulb", "check"], ["⚠", "💡", "✅"]):
                if all(em in txt for em in grp):
                    icons_hit = 1; break
            core["icons_3_kinds"] = float(icons_hit)
            notes = re.findall(r'"notes":\s*\{[^}]*?"plain":\s*\{[^}]*?"content":\s*"([^"]+)"', txt)
            notes_count = len(notes)
            notes_total_len = sum(len(n) for n in notes)
            # Stricter: need both length AND count
            core["notes_quality"] = 1.0 if (notes_total_len >= 240 and notes_count >= 8) else \
                min(notes_total_len / 240.0, notes_count / 8.0)
            rel_entries = len(re.findall(r'"end1Id"\s*:\s*"[^"]+"\s*,\s*"end2Id"\s*:\s*"[^"]+"', txt))
            if rel_entries == 0:
                rel_entries = len(re.findall(r'"id"\s*:\s*"[A-Za-z0-9_\-]+"[^}]*"end1Id"', txt))
            core["relationships>=5"] = 1.0 if rel_entries >= 5 else rel_entries / 5.0
            link_entries = len(re.findall(r'"(?:xlink:)?href"\s*:\s*"[^"]*inputs/[^"]*\.md"', txt))
            if link_entries == 0:
                link_entries = len(re.findall(r'"(?:xlink:)?href"\s*:\s*"[^"]+"', txt))
            core["hyperlinks>=4"] = 1.0 if link_entries >= 4 else link_entries / 4.0
            core["attachments>=1"] = 1.0 if has_attach else 0.0
            for kw in ('"boundary"', '"branch"', '"customSvgPath"', '"shape-class"', '"fill"'):
                if kw in txt: styling_hits += 1
            core["custom_styling"] = 1.0 if styling_hits >= 2 else styling_hits / 2.0
        except Exception as e:
            r["checks"]["xmind_err"] = str(e)[:200]
            core["xmind_parse"] = 0.0
    else:
        core["xmind_present"] = 0.0

    # mindmap.png 分辨率
    png = workspace / "mindmap.png"
    if png.exists() and png.stat().st_size >= 20 * 1024:
        try:
            w, h = Image.open(png).size
            aux["png_res>=2400x1600"] = 1.0 if (w >= 2400 and h >= 1600) else \
                min(w / 2400.0, h / 1600.0)
        except Exception:
            aux["png_res>=2400x1600"] = 0.0
    else:
        aux["png_res>=2400x1600"] = 0.0

    # mindmap.md 大纲缩进深度
    md = workspace / "mindmap.md"
    if md.exists() and md.stat().st_size >= 256:
        try:
            c = md.read_text(errors="ignore")
            depths = set()
            for line in c.splitlines():
                m = re.match(r"^( *)[-*]", line)
                if m: depths.add(len(m.group(1)) // 2)
            max_md_depth = max(depths, default=0)
            aux["md_depth>=4"] = 1.0 if max_md_depth >= 3 else max_md_depth / 3.0
        except Exception:
            aux["md_depth>=4"] = 0.0
    else:
        aux["md_depth>=4"] = 0.0

    # GUI 截图：OCR + md5 唯一 + 分辨率 + 文件大小（防 cheat）
    screen_names = ["view_01_main.png", "view_02_notes.png", "view_03_icons.png",
                    "view_04_format.png", "view_05_relationship.png"]
    ocr_ok = 0; res_ok = 0; size_ok = 0
    md5s = []
    for n in screen_names:
        p = workspace / n
        if not p.exists(): continue
        sz = p.stat().st_size
        if sz < 5 * 1024: continue  # < 5KB 视为占位
        size_ok += 1
        try:
            md5s.append(hashlib.md5(p.read_bytes()).hexdigest())
        except Exception:
            pass
        try:
            im = Image.open(p)
            w, h = im.size
            if w >= 1280 and h >= 720: res_ok += 1
            tx = pytesseract.image_to_string(im) if pytesseract else ""
            if any(k in tx for k in ("Xmind", "XMind")) or "xmind" in tx.lower():
                ocr_ok += 1
        except Exception:
            pass
    uniq = len(set(md5s))
    gui["screens_ocr"] = ocr_ok / 5.0
    gui["screens_size_ok"] = size_ok / 5.0
    gui["screens_res>=720p"] = res_ok / 5.0
    gui["screens_md5_unique"] = uniq / 5.0

    # 写回 checks
    r["checks"].update({f"core.{k}": v for k, v in core.items()})
    r["checks"].update({f"gui.{k}": v for k, v in gui.items()})
    r["checks"].update({f"aux.{k}": v for k, v in aux.items()})
    r["checks"]["_meta"] = {
        "nodes": nodes_total, "l1": l1_count, "rels": rel_entries,
        "links": link_entries, "attach": has_attach,
        "notes_len": notes_total_len, "notes_n": notes_count,
        "screens_md5_unique": uniq, "screens_ocr_ok": ocr_ok,
    }

    # 加权聚合：core 60% / gui 30% / aux 10%
    def avg(d): return sum(d.values()) / len(d) if d else 0.0
    core_avg = avg(core); gui_avg = avg(gui); aux_avg = avg(aux)
    base = 0.6 * core_avg + 0.3 * gui_avg + 0.1 * aux_avg

    # VLM 评分
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_avg = None
    if vlm_score_rubric and png.exists() and png.stat().st_size >= 20 * 1024:
        rubric = {
            "vlm_radial_layout": "图像呈中心节点向外辐射的思维导图布局，非线性列表",
            "vlm_branch_count": "中心至少向外伸展 6 条主分支",
            "vlm_subtopic_depth": "至少有部分分支展开到 ≥3 层子主题（非全部止于一级）",
            "vlm_icon_decorations": "节点上含图标装饰（⚠/💡/✅ 等），用以表示属性",
            "vlm_visual_clarity": "整体连线清晰、文字不重叠、可一眼读懂结构",
            "vlm_no_placeholder": "图片不是 1×1 占位、不是纯白/纯黑、不是无内容截屏",
        }
        try:
            vlm = vlm_score_rubric([str(png)], rubric,
                                   instruction="严格评估 XMind 思维导图的结构质量；占位/空白图给 0。")
        except Exception:
            vlm = {}
        for k in rubric: r["checks"][f"vlm.{k}"] = vlm.get(k, 0.0)
        r["judge_method"] = vlm.get("judge_method", "failed")
        if r["judge_method"] != "failed":
            vlm_avg = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)

    if vlm_avg is not None:
        score = 0.65 * base + 0.35 * vlm_avg
    else:
        # VLM 不可用：上限封顶 0.6（不能让无 VLM 也满分）
        score = min(base, 0.60)
        r["checks"]["vlm_unavailable_cap"] = 0.60

    # —— 多层 hard gate（越严越好）——
    # 1. 核心 xmind 文件不存在或解析失败 → cap 0.30
    if not xm.exists() or core.get("xmind_parse", 1.0) == 0.0 or core.get("xmind_present") == 0.0:
        score = min(score, 0.30)
    # 2. 节点数严重不足 → cap 0.40
    if core.get("nodes>=50", 0) < 0.6:
        score = min(score, 0.40)
    # 3. relationships 严重不足 → cap 0.45
    if core.get("relationships>=5", 0) < 0.6:
        score = min(score, 0.45)
    # 4. hyperlinks 不达标 → cap 0.50
    if core.get("hyperlinks>=4", 0) < 0.5:
        score = min(score, 0.50)
    # 5. attachments 不达标 → cap 0.55
    if core.get("attachments>=1", 0) < 1.0:
        score = min(score, 0.55)
    # 6. GUI 截图 OCR 严重缺失 → cap 0.35（agent 没真用 Xmind GUI）
    if gui.get("screens_ocr", 0) < 0.4:
        score = min(score, 0.35)
    # 7. 截图 md5 重复（同一张图复用）→ cap 0.45
    if gui.get("screens_md5_unique", 0) < 0.6:
        score = min(score, 0.45)
    # 8. 截图分辨率全是缩略图（占位）→ cap 0.50
    if gui.get("screens_res>=720p", 0) < 0.4:
        score = min(score, 0.50)
    # 9. mindmap.png 分辨率不达标 → cap 0.60
    if aux.get("png_res>=2400x1600", 0) < 1.0:
        score = min(score, 0.60)
    # 10. VLM 视觉评分极低 → cap 0.45（即使有截图也判画面不像 mindmap）
    if vlm_avg is not None and vlm_avg < 0.4:
        score = min(score, 0.45)

    r["overall_score"] = round(max(0.0, min(1.0, score)), 3)
    r["weights"] = {"core": 0.6, "gui": 0.3, "aux": 0.1, "vlm_blend": 0.35 if vlm_avg is not None else None}
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
