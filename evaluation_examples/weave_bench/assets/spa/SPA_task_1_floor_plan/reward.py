# Auto-generated from WeaveBench task SPA_task_1_floor_plan.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

from pathlib import Path
import json
import re
from PIL import Image

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    # gt directory: sibling of workspace (host-side), not visible to agent
    gt_dir = workspace.parent / "gt"
    if not gt_dir.exists():
        # fallback: bench-style layout where gt sits next to workspace via ../gt
        for cand in [workspace / "gt", workspace.parent.parent / "gt"]:
            if cand.exists():
                gt_dir = cand
                break

    r = {"checks": {}, "overall_score": 0.0}
    # v2: weighted scoring buckets
    core_s, core_t = 0.0, 0  # 60% — svg/png/placement core deliverables
    gui_s, gui_t = 0.0, 0    # 30% — Inkscape GUI evidence (ui shots / lpe / measure / layer)
    aux_s, aux_t = 0.0, 0    # 10% — GT coverage / alignment auxiliary
    svg = workspace / "floor_annotated.svg"
    # also try /tmp_workspace/results/ landing
    if not svg.exists() and (workspace / "results" / "floor_annotated.svg").exists():
        svg = workspace / "results" / "floor_annotated.svg"
    if svg.exists():
        try:
            c = svg.read_text(errors="ignore")
        except Exception:
            c = ""
        shapes = len(re.findall(r"<(rect|path)", c))
        core_t += 1
        if shapes >= 22:
            r["checks"][f"shapes={shapes}"] = True; core_s += 1
        elif shapes >= 14:
            r["checks"][f"shapes={shapes}"] = 0.5; core_s += 0.5
        colors = set(re.findall(r"fill:#([0-9a-fA-F]{3,6})", c))
        core_t += 1
        if len(colors) >= 4:
            r["checks"][f"colors={len(colors)}"] = True; core_s += 1
        texts = len(re.findall(r"<text", c))
        core_t += 1
        if texts >= 22:
            r["checks"][f"texts={texts}"] = True; core_s += 1
        elif texts >= 14:
            r["checks"][f"texts={texts}"] = 0.5; core_s += 0.5
        gui_t += 1
        if c.count("mm") >= 5:
            r["checks"]["dim_mm>=5"] = True; gui_s += 1
        elif c.count("mm") >= 3:
            r["checks"]["dim_mm>=5"] = 0.5; gui_s += 0.5
    png = workspace / "floor_annotated.png"
    if not png.exists() and (workspace / "results" / "floor_annotated.png").exists():
        png = workspace / "results" / "floor_annotated.png"
    core_t += 1
    if png.exists():
        try:
            w, h = Image.open(png).size
            png_size = png.stat().st_size
            # v2 anti-cheat: also require min file size to defeat blank/placeholder images
            if w >= 2000 and h >= 1500 and png_size >= 50_000:
                r["checks"]["png_res"] = True; core_s += 1
            elif w >= 2000 and h >= 1500:
                r["checks"]["png_res"] = 0.4; core_s += 0.4
        except Exception:
            pass
    pc = workspace / "placement_check.md"
    if not pc.exists() and (workspace / "results" / "placement_check.md").exists():
        pc = workspace / "results" / "placement_check.md"
    core_t += 1
    if pc.exists():
        try:
            lines = pc.read_text(errors="ignore").splitlines()
            if len(lines) >= 22:
                r["checks"]["check_lines"] = True; core_s += 1
            elif len(lines) >= 14:
                r["checks"]["check_lines"] = 0.5; core_s += 0.5
        except Exception:
            pass

    # Collect named IDs once
    named = []
    c2 = ""
    if svg.exists():
        try:
            c2 = svg.read_text(errors="ignore")
        except Exception:
            c2 = ""
        # furniture layer present
        gui_t += 1
        if re.search(r'inkscape:groupmode\s*=\s*"layer"', c2) and re.search(r'inkscape:label\s*=\s*"furniture"', c2):
            r["checks"]["furniture_layer"] = True; gui_s += 1
        else:
            r["checks"]["furniture_layer"] = False
        # v2: Named IDs threshold raised to 22 (match prompt count)
        all_ids = re.findall(r'\bid\s*=\s*"([^"]+)"', c2)
        named = [i for i in all_ids if re.match(r'^[a-z]+(_[a-z0-9]+)+$', i)]
        r["checks"]["named_ids"] = min(1.0, len(named) / 22.0); core_s += r["checks"]["named_ids"]; core_t += 1
        # LPE
        lpe_count = len(re.findall(r"inkscape:path-effect", c2))
        r["checks"]["lpe_count"] = 1.0 if lpe_count >= 3 else lpe_count / 3.0
        gui_s += r["checks"]["lpe_count"]; gui_t += 1
        # Measure annotations: count text elements with mm
        mm_count = len(re.findall(r"<text[^>]*>[^<]*mm[^<]*</text>", c2))
        r["checks"]["measure_count"] = 1.0 if mm_count >= 5 else mm_count / 5.0
        gui_s += r["checks"]["measure_count"]; gui_t += 1

    # ---------- GT integration (B2 / D1 / B2 alignment) ----------
    gt_furniture = {}
    gt_rooms = {}
    try:
        ef = gt_dir / "expected_furniture.json"
        if ef.exists():
            gt_furniture = json.loads(ef.read_text(errors="ignore")).get("required_furniture", {})
    except Exception:
        gt_furniture = {}
    try:
        rj = gt_dir / "rooms.json"
        if rj.exists():
            gt_rooms = json.loads(rj.read_text(errors="ignore"))
    except Exception:
        gt_rooms = {}

    # D1: how many GT-required furniture names appear in named ID set
    if gt_furniture:
        named_set = set(named)
        hits = sum(1 for k in gt_furniture if any(k == n or n.startswith(k + "_") or n.endswith("_" + k) or k in n for n in named_set))
        # v2: tighter target — require ≥10 hits or ≥50% of GT
        target = max(10, int(0.5 * len(gt_furniture)))
        r["checks"]["gt_furniture_coverage"] = min(1.0, hits / float(target))
        aux_s += r["checks"]["gt_furniture_coverage"]; aux_t += 1

    # D1: how many GT room names referenced in SVG text/labels
    if gt_rooms and c2:
        room_hits = sum(1 for rn in gt_rooms if rn in c2)
        r["checks"]["gt_room_refs"] = min(1.0, room_hits / max(1.0, float(len(gt_rooms))))
        aux_s += r["checks"]["gt_room_refs"]; aux_t += 1

    # B2 alignment: 4 furniture along east wall, x-center variance ≤ 5
    # Heuristic: find rect IDs containing 'east' or use any 4 explicit aligned IDs;
    # parse <rect ... id="..." x="..." width="..." />
    if c2:
        rect_pat = re.compile(
            r'<rect\b[^>]*?\bid\s*=\s*"([^"]+)"[^>]*?\bx\s*=\s*"([\-0-9.]+)"[^>]*?\bwidth\s*=\s*"([\-0-9.]+)"',
            re.DOTALL,
        )
        rects = []
        for m in rect_pat.finditer(c2):
            try:
                rects.append((m.group(1), float(m.group(2)) + float(m.group(3)) / 2.0))
            except Exception:
                continue
        # also try the alternative attribute order: id ... width ... x
        rect_pat2 = re.compile(
            r'<rect\b[^>]*?\bid\s*=\s*"([^"]+)"[^>]*?\bwidth\s*=\s*"([\-0-9.]+)"[^>]*?\bx\s*=\s*"([\-0-9.]+)"',
            re.DOTALL,
        )
        existing = {rid for rid, _ in rects}
        for m in rect_pat2.finditer(c2):
            if m.group(1) in existing:
                continue
            try:
                rects.append((m.group(1), float(m.group(3)) + float(m.group(2)) / 2.0))
            except Exception:
                continue
        east_rects = [(rid, cx) for rid, cx in rects if "east" in rid.lower() or rid.lower().endswith("_e")]
        align_score = 0.0
        if len(east_rects) >= 4:
            xs = [cx for _, cx in east_rects[:4]]
            mean = sum(xs) / 4.0
            var = sum((x - mean) ** 2 for x in xs) / 4.0
            r["checks"]["east_align_variance"] = round(var, 3)
            align_score = 1.0 if var <= 5.0 else (0.5 if var <= 25.0 else 0.0)
        else:
            r["checks"]["east_align_variance"] = None
        r["checks"]["alignment_score"] = align_score
        aux_s += align_score; aux_t += 1
    # ---------- end GT integration ----------

    # 5 UI screenshots — check both workspace/ and workspace/results/
    # v2 anti-cheat: also require each present shot to be ≥5KB and md5-unique
    import hashlib
    rd_results = workspace
    rd_alt = workspace / "results"
    ui_shots = ["view_01_layers_panel.png", "view_02_lpe_dialog.png", "view_03_align_dialog.png",
                "view_04_measure_tool.png", "view_xml_editor.png"]
    ui_paths = []
    for n in ui_shots:
        for d in (rd_results, rd_alt):
            p = d / n
            if p.exists():
                ui_paths.append(p)
                break
    ui_md5s = set()
    ui_valid = 0
    for p in ui_paths:
        try:
            if p.stat().st_size >= 5000:
                h = hashlib.md5(p.read_bytes()).hexdigest()
                if h not in ui_md5s:
                    ui_md5s.add(h); ui_valid += 1
        except Exception:
            continue
    r["checks"]["inkscape_ui_shots"] = ui_valid / len(ui_shots)
    r["checks"]["inkscape_ui_unique_md5"] = len(ui_md5s)
    gui_s += ui_valid / len(ui_shots); gui_t += 1

    # v2: weighted overall — core 60%, gui 30%, aux 10%
    def _avg(s, t): return (s / t) if t > 0 else 0.0
    core_avg = _avg(core_s, core_t)
    gui_avg = _avg(gui_s, gui_t)
    aux_avg = _avg(aux_s, aux_t)
    base = 0.6 * core_avg + 0.3 * gui_avg + 0.1 * aux_avg
    r["checks"]["_core_avg"] = round(core_avg, 3)
    r["checks"]["_gui_avg"] = round(gui_avg, 3)
    r["checks"]["_aux_avg"] = round(aux_avg, 3)
    vlm_ran = False
    # v2: cap base when VLM unavailable so no-VLM path can't reach full score
    base_no_vlm_cap = 0.60
    if vlm_score_rubric and png.exists():
        rubric = {
            "vlm_furniture_present": "户型图上叠加了 ≥18 个家具/物件标注（矩形或图形元素）",
            "vlm_text_legible": "每个标注上有清晰可读的文字编号或名称（不重叠原户型线条）",
            "vlm_color_categorized": "标注按 ≥4 种颜色分类（如不同房间或不同家具类别）",
            "vlm_layout_realistic": "家具摆放符合常理（沙发对电视、床靠墙等），无明显穿墙或占用通道",
        }
        try:
            vlm = vlm_score_rubric([str(png)], rubric, instruction="评估手绘客户家具摆放叠加在户型图上的标注质量。")
        except Exception:
            vlm = {}
        for k in rubric:
            r["checks"][k] = vlm.get(k, 0.0)
        r["judge_method"] = vlm.get("judge_method", "failed")
        vlm_avg = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
        if vlm and r["judge_method"] != "failed":
            vlm_ran = True
            r["overall_score"] = round((base + vlm_avg) / 2, 3)
        else:
            r["overall_score"] = round(base, 3)
    else:
        r["overall_score"] = round(base, 3)

    # v2: when VLM did not run, hard cap overall score (no full marks without judge)
    if not vlm_ran:
        r["overall_score"] = round(min(r["overall_score"], base_no_vlm_cap), 3)
    # v2 hard gates — tighter and multi-layer
    if vlm_ran:
        vlm_keys = ["vlm_furniture_present", "vlm_text_legible", "vlm_color_categorized", "vlm_layout_realistic"]
        vlm_avg = sum(r["checks"].get(k, 0) for k in vlm_keys) / len(vlm_keys)
        if vlm_avg < 0.75:
            r["overall_score"] = round(min(r["overall_score"], 0.50), 3)
        if vlm_avg < 0.5:
            r["overall_score"] = round(min(r["overall_score"], 0.35), 3)
    # core deliverable gate — if core average < 0.5, hard cap 0.40
    if r["checks"].get("_core_avg", 0) < 0.5:
        r["overall_score"] = round(min(r["overall_score"], 0.40), 3)
    # named id gate (raised threshold)
    if r["checks"].get("named_ids", 0) < 0.7:
        r["overall_score"] = round(min(r["overall_score"], 0.50), 3)
    if r["checks"].get("named_ids", 0) < 0.4:
        r["overall_score"] = round(min(r["overall_score"], 0.35), 3)
    # GUI evidence gate (raised threshold + multi-layer)
    if r["checks"].get("inkscape_ui_shots", 0) < 0.6:
        r["overall_score"] = round(min(r["overall_score"], 0.50), 3)
    if r["checks"].get("inkscape_ui_shots", 0) < 0.3:
        r["overall_score"] = round(min(r["overall_score"], 0.35), 3)
    if r["checks"].get("lpe_count", 0) < 1.0:
        r["overall_score"] = round(min(r["overall_score"], 0.60), 3)
    if r["checks"].get("lpe_count", 0) == 0:
        r["overall_score"] = round(min(r["overall_score"], 0.40), 3)
    # furniture layer is mandatory — without it agent didn't really use Inkscape layers
    if r["checks"].get("furniture_layer") is not True:
        r["overall_score"] = round(min(r["overall_score"], 0.50), 3)
    # Structural gate: missing core furniture coverage caps overall
    if "gt_furniture_coverage" in r["checks"] and r["checks"]["gt_furniture_coverage"] < 0.5:
        r["overall_score"] = round(min(r["overall_score"], 0.55), 3)

    # ----- BEGIN CHEAT/VLM HARD-GATE (auto-injected) -----
    try:
        from _judge_helper import audit_chat_jsonl_for_banned as _audit
    except Exception:
        _audit = None
    _BANS = ['"xmllint"', 'xpath', 'svgpathtools.parse']
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
    r["overall_score"] = float(r["overall_score"])
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
