# Auto-generated from WeaveBench task SPA_task_3_colmap_mesh_repair.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """COLMAP+MeshLab cross-channel grader; empty workspace -> 0.000."""
    import json, re, hashlib
    from pathlib import Path
    try:
        from PIL import Image
    except ImportError:
        Image = None
    try:
        import pytesseract
    except ImportError:
        pytesseract = None
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    def _load_json(p):
        try:
            return json.loads(p.read_text())
        except Exception:
            return None

    # 1. db_stats.json
    p = rd / "db_stats.json"
    d = _load_json(p) if p.exists() else None
    if isinstance(d, dict):
        needed = ["num_images", "num_keypoints_total", "num_matches_total"]
        s["db_stats_schema"] = 1.0 if all(k in d for k in needed) else 0.5
        s["db_stats_values"] = 1.0 if (d.get("num_images") or 0) > 0 else 0.0
    else:
        s["db_stats_schema"] = 0.0
        s["db_stats_values"] = 0.0

    # 3. sparse_stats.json
    p = rd / "sparse_stats.json"
    d = _load_json(p) if p.exists() else None
    s["sparse_registered"] = 1.0 if (isinstance(d, dict) and (d.get("registered_images") or 0) > 0) else 0.0

    # 5. dense_stats.json
    p = rd / "dense_stats.json"
    d = _load_json(p) if p.exists() else None
    s["dense_points"] = 1.0 if (isinstance(d, dict) and (d.get("num_points") or 0) > 0) else 0.0

    # 7. mesh_before.json
    p = rd / "mesh_before.json"
    mb = _load_json(p) if p.exists() else None
    s["mesh_before"] = 1.0 if (isinstance(mb, dict) and "vertices" in mb and "faces" in mb) else 0.0

    # 10. topology_before.json
    p = rd / "topology_before.json"
    tb = _load_json(p) if p.exists() else None
    s["topology_before"] = 1.0 if (isinstance(tb, dict) and len(tb) >= 3) else 0.0

    # 12. measurements.json
    p = rd / "measurements.json"
    m = _load_json(p) if p.exists() else None
    s["measurements"] = 1.0 if (isinstance(m, dict) and "value_units" in m) else 0.0

    # 13. repaired.obj + mesh_after.json
    obj = rd / "repaired.obj"
    s["repaired_obj"] = 1.0 if (obj.exists() and obj.stat().st_size > 1024) else 0.0
    p = rd / "mesh_after.json"
    ma = _load_json(p) if p.exists() else None
    if isinstance(ma, dict) and "vertices" in ma and "faces" in ma:
        s["mesh_after"] = 1.0
        # 严格：仅 faces 数变化才记 1.0；顶点数也变 → 1.0；完全不变 → 0.0（不再给 0.3 安慰分）
        changed = False
        if isinstance(mb, dict):
            if ma.get("faces") != mb.get("faces") or ma.get("vertices") != mb.get("vertices"):
                changed = True
        s["mesh_changed"] = 1.0 if changed else 0.0
        s["mesh_after_surface_area"] = 1.0 if "surface_area" in ma else 0.0
    else:
        s["mesh_after"] = 0.0
        s["mesh_changed"] = 0.0
        s["mesh_after_surface_area"] = 0.0

    # 14. repair_report.md
    p = rd / "repair_report.md"
    if p.exists():
        txt = p.read_text(errors="ignore")
        s["repair_report"] = min(1.0, len(txt) / 150.0)
    else:
        s["repair_report"] = 0.0

    # 2,4,6,8,9,11,12,14. GUI screenshots + OCR
    shots = {
        "view_01_match_matrix.png":     ["COLMAP", "Database", "Match", "Matrix"],
        "view_02_sparse_cloud.png":     ["COLMAP", "Reconstruction", "Model", "Image"],
        "view_03_dense_pointcloud.png": ["MeshLab", "Layer", "Render", "Vertices"],
        "view_04_initial_mesh.png":     ["MeshLab", "Vertices", "Faces", "Filter"],
        "view_05_nonmanifold.png":      ["MeshLab", "Filter", "Selection", "Manifold"],
        "view_06_repaired.png":         ["MeshLab", "Filter", "Smooth", "Cleaning"],
        "view_07_measurement.png":      ["MeshLab", "Measur", "Edit", "Tool"],
        "view_08_final_render.png":     ["MeshLab", "Render", "Vertices", "Faces"],
    }
    gui_present = 0
    gui_ocr_hits = 0
    gui_md5s = set()
    gui_resolution_ok = 0
    for fname, kws in shots.items():
        fp = rd / fname
        # 防 cheat：截图必须 > 5KB（< 5KB 视为占位）
        if fp.exists() and fp.stat().st_size > 5120:
            gui_present += 1
            try:
                gui_md5s.add(hashlib.md5(fp.read_bytes()).hexdigest())
            except Exception:
                pass
            if Image:
                try:
                    im = Image.open(fp)
                    w, h = im.size
                    if w >= 1024 and h >= 600:
                        gui_resolution_ok += 1
                except Exception:
                    pass
            if pytesseract and Image:
                try:
                    tx = pytesseract.image_to_string(Image.open(fp))
                    if any(k.lower() in tx.lower() for k in kws):
                        gui_ocr_hits += 1
                except Exception:
                    pass
    s["gui_screenshots_count"] = gui_present / len(shots)
    s["gui_ocr_meshlab"] = (gui_ocr_hits / len(shots)) if (pytesseract and Image) else 0.0
    # 防 cheat：md5 多样性（截图必须互不相同）+ 分辨率
    s["gui_md5_diversity"] = (len(gui_md5s) / len(shots)) if gui_present else 0.0
    s["gui_resolution_ok"] = (gui_resolution_ok / len(shots)) if Image else 0.0

    # 15. VLM rubric (4 items) — 不可用时记入 vlm_unavailable，不污染分母
    vlm_keys = ["vlm_3d_mesh_visible", "vlm_meshlab_ui", "vlm_colmap_ui", "vlm_repair_evidence"]
    vlm_available = False
    if vlm_score_rubric:
        sample = [str(rd / n) for n in shots if (rd / n).exists()][:4]
        if sample:
            rubric = {
                "vlm_3d_mesh_visible": "至少一张截图可见 3D 三角网格 / 点云渲染（多边形面片或点云结构清晰）",
                "vlm_meshlab_ui":      "MeshLab 界面元素清晰（工具栏 / 菜单 / Layer 面板）",
                "vlm_colmap_ui":       "至少一张截图清晰显示 COLMAP GUI（Database management 或 3D viewer）",
                "vlm_repair_evidence": "存在网格修复证据（高亮缺陷 / 删除碎片 / 平滑前后差异）",
            }
            try:
                vlm = vlm_score_rubric(sample, rubric,
                                       instruction="评估 COLMAP+MeshLab 摄影测量与网格修复截图。")
                vlm_available = bool(vlm)
            except Exception:
                vlm = {}
            if vlm_available:
                for k in vlm_keys:
                    s[k] = float(vlm.get(k, 0.0) or 0.0)

    # ---- Aggregate (weighted: core 60% / gui 30% / aux 10%) ----
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    if not any(v > 0 for v in nums):
        s["overall_score"] = 0.000
        return s

    def _avg(keys):
        vs = [s.get(k, 0.0) for k in keys if k in s]
        return (sum(vs) / len(vs)) if vs else 0.0

    core_keys = [
        "db_stats_schema", "db_stats_values",
        "sparse_registered", "dense_points",
        "mesh_before", "topology_before", "measurements",
        "repaired_obj", "mesh_after", "mesh_changed",
        "mesh_after_surface_area", "repair_report",
    ]
    gui_keys = [
        "gui_screenshots_count", "gui_ocr_meshlab",
        "gui_md5_diversity", "gui_resolution_ok",
    ]
    aux_keys = [k for k in s.keys() if k.startswith("vlm_")]

    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys) if aux_keys else 0.0

    if aux_keys:
        base = 0.6 * core + 0.3 * gui + 0.1 * aux
    else:
        # VLM 不可用时保留 core/gui 但封顶 0.6（无 VLM 不能满分）
        base = (0.6 * core + 0.3 * gui) / 0.9
        base = min(base, 0.6)

    # 多层 hard gate
    has_cli = (s.get("db_stats_schema", 0) > 0) or (s.get("sparse_registered", 0) > 0)
    if not has_cli:
        base = min(base, 0.35)
    # GUI 真实交互门槛上拉：必须 ≥ 70% 截图存在
    gui_pres = s.get("gui_screenshots_count", 0)
    if gui_pres < 0.7:
        base = min(base, 0.4)
    if gui_pres < 0.4:
        base = min(base, 0.25)
    # OCR 命中率门槛（OCR 可用时）
    if pytesseract and Image:
        if s.get("gui_ocr_meshlab", 0) < 0.5:
            base = min(base, 0.5)
        if s.get("gui_ocr_meshlab", 0) < 0.25:
            base = min(base, 0.35)
    # md5 多样性（防止反复提交同一张图）
    if s.get("gui_md5_diversity", 0) < 0.7:
        base = min(base, 0.45)
    # 核心交付物
    if s.get("repaired_obj", 0) == 0:
        base = min(base, 0.4)
    if s.get("mesh_after", 0) == 0:
        base = min(base, 0.4)
    if s.get("mesh_changed", 0) == 0:
        base = min(base, 0.5)
    # VLM 可用且分数低
    if aux_keys:
        if aux < 0.6:
            base = min(base, 0.55)
        if aux < 0.4:
            base = min(base, 0.4)

    s["overall_score"] = round(max(0.0, base), 3)
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
