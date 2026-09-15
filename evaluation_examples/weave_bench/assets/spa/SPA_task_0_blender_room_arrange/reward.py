# Auto-generated from WeaveBench task SPA_task_0_blender_room_arrange.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

from pathlib import Path
import csv, re, json, subprocess
from PIL import Image
import numpy as np

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    """Stricter SPA_5 grader: bounding-box rule conformance against gt/expected.json."""
    gt_path = (workspace.parent / "gt" / "expected.json")
    if not gt_path.exists():
        gt_path = Path("/tmp_workspace/gt/expected.json")
    gt = json.loads(gt_path.read_text()) if gt_path.exists() else {}
    s = {}
    bl = workspace/"room.blend"
    s["blend_exists"] = 1.0 if bl.exists() else 0.0
    objs = []
    blender_ok = False
    if bl.exists():
        try:
            sc=subprocess.run(["blender","-b",str(bl),"--python-expr",
                "import bpy,json;objs=[(o.name,list(o.location),list(o.dimensions),list(o.rotation_euler)) for o in bpy.data.objects if o.type=='MESH'];print('JSON_OUT',json.dumps(objs))"],
                capture_output=True,timeout=180,text=True)
            m=re.search(r"JSON_OUT (.+)", sc.stdout)
            if m: objs=json.loads(m.group(1)); blender_ok = True
        except Exception as e: s["blender_err"]=str(e)[:80]
    # Fallback: parse layout.csv if blender CLI not available / parse failed
    if not objs:
        lc = workspace/"layout.csv"
        if lc.exists():
            try:
                import csv as _csv
                with lc.open() as fh:
                    for row in _csv.DictReader(fh):
                        try:
                            x = float(row.get("x", 0) or 0)
                            y = float(row.get("y", 0) or 0)
                            z = float(row.get("z", 0) or 0)
                            rz = float(row.get("rotation_z", 0) or 0)
                            objs.append((row.get("object","obj"),
                                         [x, y, z],
                                         [0.5, 0.5, 0.5],  # default bbox dims
                                         [0, 0, rz]))
                        except Exception: pass
            except Exception: pass
    s["mesh_count"] = min(1.0, len(objs)/max(gt.get("min_meshes",6),6))
    # keys -> 同义词集合（覆盖 Polyhaven 真实对象名 ClassicConsole / WoodenTable /
    # ClassicNightstand / ArmChair / WoodenChair 等，以及常见英文别名 couch/desk/stand/light）
    key_synonyms = {
        "sofa":   ["sofa", "couch", "settee"],
        "coffee": ["coffee", "coffeetable", "cocktail"],
        "tv":     ["tv", "television", "console", "classicconsole", "tvstand", "stand", "media", "cabinet"],
        "dining": ["dining", "diningtable", "woodentable", "table"],
        "chair":  ["chair", "armchair", "woodenchair", "stool", "seat"],
        "nightstand": ["nightstand", "classicnightstand", "bedside", "sidetable", "endtable", "lamp", "light", "floorlamp", "torchiere"],
    }
    def _norm(n): return re.sub(r"[^a-z0-9]", "", n.lower())
    norm_names = [_norm(n) for n,_,_,_ in objs] if objs else []
    name_blob = " ".join(norm_names)
    matched_keys = set()
    for k, syns in key_synonyms.items():
        if any(s in name_blob for s in syns): matched_keys.add(k)
    s["furniture_named"] = len(matched_keys)/6
    def _obj_key(name):
        nn = _norm(name)
        for k, syns in key_synonyms.items():
            if any(s in nn for s in syns): return k
        return None
    # bbox xy non-overlap
    boxes=[]
    for n,loc,dim,_ in objs:
        if _obj_key(n) is not None:
            boxes.append((loc[0]-dim[0]/2,loc[1]-dim[1]/2,loc[0]+dim[0]/2,loc[1]+dim[1]/2))
    no_overlap = True; pairs=0; ok_pairs=0
    for i in range(len(boxes)):
        for j in range(i+1,len(boxes)):
            pairs+=1; a,b=boxes[i],boxes[j]
            if max(a[0],b[0])>=min(a[2],b[2]) or max(a[1],b[1])>=min(a[3],b[3]): ok_pairs+=1
            else: no_overlap=False
    s["no_overlap"] = (ok_pairs/pairs) if pairs else 0.0
    # rule conformance vs gt
    R = gt.get("room_dims_m",{}); tol = gt.get("tolerance_m",0.05)
    Y = R.get("y",6.0); X = R.get("x",5.0)
    rule_hits=0; rule_total=0
    obj_map = {}
    for n,loc,dim,_ in objs:
        k = _obj_key(n)
        if k is not None: obj_map.setdefault(k, (loc,dim))
    for rule in gt.get("rules",[]):
        rule_total+=1
        target = next((k for k in key_synonyms if k in rule.get("object","")), None)
        if not target or target not in obj_map: continue
        loc,dim = obj_map[target]
        if rule.get("wall")=="north":
            d = abs(Y - (loc[1]+dim[1]/2))
            if abs(d - rule.get("distance_m",0))<=tol+0.05: rule_hits+=1
        elif rule.get("wall")=="south":
            d = loc[1]-dim[1]/2
            if d<=tol+0.05: rule_hits+=1
        elif rule.get("wall")=="east":
            d = abs(X - (loc[0]+dim[0]/2))
            if abs(d - rule.get("distance_m",0))<=tol+0.1: rule_hits+=1
        if "x_center_m" in rule and abs(loc[0]-rule["x_center_m"])<=0.2: rule_hits+=0.5
    s["rule_conformance"] = min(1.0, rule_hits/max(rule_total,1))
    # render & top_view
    rp=workspace/"render.png"
    render_md5 = None
    if rp.exists():
        im=Image.open(rp); arr=np.array(im.convert("L"))
        s["render_size"] = 1.0 if im.size==(1920,1080) else 0.0
        s["render_nontrivial"] = 1.0 if arr.std()>35 else max(0.0, (arr.std()-10)/25)
        try:
            import hashlib
            render_md5 = hashlib.md5(rp.read_bytes()).hexdigest()
            s["render_filesize_ok"] = 1.0 if rp.stat().st_size >= 30*1024 else 0.0
        except Exception:
            s["render_filesize_ok"] = 0.0
    else:
        s["render_size"]=0.0; s["render_nontrivial"]=0.0; s["render_filesize_ok"]=0.0
    tv=workspace/"top_view.png"
    tv_md5 = None
    if tv.exists():
        _tvsz = Image.open(tv).size
        s["top_view_ok"] = 1.0 if (_tvsz[0]>=1280 and _tvsz[1]>=720) else 0.0
        try:
            import hashlib
            tv_md5 = hashlib.md5(tv.read_bytes()).hexdigest()
            s["top_view_filesize_ok"] = 1.0 if tv.stat().st_size >= 15*1024 else 0.0
        except Exception:
            s["top_view_filesize_ok"] = 0.0
    else:
        s["top_view_ok"] = 0.0; s["top_view_filesize_ok"] = 0.0
    s["screenshots_distinct"] = 1.0 if (render_md5 and tv_md5 and render_md5 != tv_md5) else 0.0
    lc=workspace/"layout.csv"
    if lc.exists():
        rows=list(csv.DictReader(lc.open()))
        if len(rows)>=6 and all(k in rows[0] for k in ["object","x","y","z","rotation_z","distance_to_nearest_wall_mm"]):
            s["layout_csv_schema"] = 1.0
            try:
                ok = sum(1 for row in rows if 0<=float(row["distance_to_nearest_wall_mm"])<=200)
                s["layout_csv_distance"] = 1.0 if ok>=1 else 0.0
            except: s["layout_csv_distance"]=0.0
            names = [r.get("object","").strip().lower() for r in rows[:6]]
            s["layout_csv_unique"] = 1.0 if len(set(names))==6 and all(names) else 0.0
        else:
            s["layout_csv_schema"]=0.5 if rows else 0.0; s["layout_csv_distance"]=0.0; s["layout_csv_unique"]=0.0
    else:
        s["layout_csv_schema"]=0.0; s["layout_csv_distance"]=0.0; s["layout_csv_unique"]=0.0
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    imgs = [str(p) for p in [workspace/"render.png", workspace/"top_view.png"] if p.exists()]
    if vlm_score_rubric and imgs:
        rubric = {
            "vlm_room_complete": "渲染图呈现一个完整的室内房间场景，含 ≥6 件家具（沙发/桌椅/柜灯等）",
            "vlm_no_overlap": "家具之间无明显穿模或重叠，摆放空间合理",
            "vlm_against_wall": "至少 3 件大件家具贴墙摆放（沙发靠墙、柜靠墙等）",
            "vlm_walkable_aisle": "中央或主要通道留有可行走的空间，未被家具完全占满",
            "vlm_lighting_ok": "渲染图光照正常（非全黑、非过曝），材质可辨",
        }
        vlm = vlm_score_rubric(imgs[:2], rubric, instruction="评估 Blender 室内家具布置的合理性。第一张为透视渲染，第二张为顶视图（如有）。")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
    nums=[v for v in s.values() if isinstance(v,(int,float))]
    flat = sum(nums)/len(nums) if nums else 0.0
    # 加权：核心交付 60% / GUI 证据 30% / 辅助 10%
    core_keys = ["blend_exists","mesh_count","furniture_named","no_overlap","rule_conformance","layout_csv_schema","layout_csv_distance","layout_csv_unique"]
    gui_keys  = ["render_size","render_nontrivial","render_filesize_ok","top_view_ok","top_view_filesize_ok","screenshots_distinct"]
    aux_keys  = [k for k in s if k.startswith("vlm_")]
    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k],(int,float))]
        return sum(vals)/len(vals) if vals else 0.0
    core = _avg(core_keys); gui = _avg(gui_keys); aux = _avg(aux_keys) if aux_keys else flat
    base = 0.6*core + 0.3*gui + 0.1*aux
    # 多层 hard gate（均上调）
    if s.get("blend_exists",0) < 1.0: base = min(base, 0.30)
    if s.get("no_overlap",0) < 0.85: base = min(base, 0.40)
    if s.get("rule_conformance",0) < 0.6: base = min(base, 0.45)
    if s.get("mesh_count",0) < 1.0: base = min(base, 0.50)
    if s.get("render_size",0) < 1.0 or s.get("render_nontrivial",0) < 0.8: base = min(base, 0.45)
    if s.get("top_view_ok",0) < 1.0: base = min(base, 0.50)
    if s.get("screenshots_distinct",0) < 1.0: base = min(base, 0.45)
    if s.get("layout_csv_schema",0) < 1.0 or s.get("layout_csv_unique",0) < 1.0: base = min(base, 0.50)
    vlm_keys = [k for k in s if k.startswith("vlm_")]
    if vlm_keys:
        vlm_avg = sum(s.get(k,0) for k in vlm_keys)/len(vlm_keys)
        if vlm_avg < 0.6: base = min(base, 0.50)
        if vlm_avg < 0.4: base = min(base, 0.35)
    else:
        # VLM 不可用时退化分上限封顶 0.6
        base = min(base, 0.60)
    s["overall_score"] = round(base, 3)
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
