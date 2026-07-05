# Auto-generated from WeaveBench task DES_task_15_blender_bpy_lookdev_eyedrop.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Strict grader for Blender lookdev task."""
    import json, subprocess, math, os
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    src = Path("/tmp_workspace/source")
    s = {}

    # 1. build_scene.py
    bs = rd / "build_scene.py"
    bs_ok = 0.0
    if bs.exists():
        try:
            txt = bs.read_text()
            if "import bpy" in txt and ("Suzanne" in txt or "monkey" in txt.lower()):
                bs_ok = 1.0
            elif "import bpy" in txt:
                bs_ok = 0.6
        except Exception:
            pass
    s["build_script"] = bs_ok

    # 2. scene.blend
    sb = rd / "scene.blend"
    s["scene_blend"] = 1.0 if (sb.exists() and sb.stat().st_size > 1024) else 0.0

    # 3. build_log.txt
    bl = rd / "build_log.txt"
    log_ok = 0.0
    if bl.exists():
        try:
            t = bl.read_text(errors="ignore")
            if any(k in t for k in ["Saved", "Blender quit", "BLENDER_QUIT", ".blend"]):
                log_ok = 1.0
            elif len(t) > 10:
                log_ok = 0.4
        except Exception:
            pass
    s["build_log"] = log_ok

    # 4. eyedrop_samples.json
    ej = rd / "eyedrop_samples.json"
    eyedrop_ok = 0.0; targets_cov = 0.0; samples = []
    needed = {"fur", "nose", "pupil", "bg"}
    if ej.exists():
        try:
            d = json.loads(ej.read_text())
            samples = d.get("samples", []) if isinstance(d, dict) else []
            if len(samples) >= 4:
                eyedrop_ok = 1.0
            elif len(samples) >= 2:
                eyedrop_ok = 0.5
            tgts = {str(x.get("target", "")).lower() for x in samples}
            targets_cov = len(needed & tgts) / len(needed)
        except Exception:
            pass
    s["eyedrop_count"] = eyedrop_ok
    s["eyedrop_targets_coverage"] = targets_cov

    # 5. GUI screenshots
    gui_imgs = {
        "view_blender_image_editor.png": ["Image", "Editor", "Sampler", "Color"],
        "view_blender_shader_editor.png": ["Shader", "Principled", "BSDF", "Base Color", "Material"],
        "view_blender_viewport_matpreview.png": ["Verts", "Faces", "Tris", "Material", "Preview"],
    }
    present = sum(1 for n in gui_imgs if (rd / n).exists())
    s["gui_screenshots_count"] = present / len(gui_imgs)
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        for n, kws in gui_imgs.items():
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in kws):
                        ocr_hits += 1
                except Exception:
                    pass
        s["gui_ocr_hits"] = ocr_hits / len(gui_imgs)
    except ImportError:
        s["gui_ocr_hits"] = 0.5

    # 6. render_0001.png
    render = rd / "render_0001.png"
    render_ok = 0.0; resolution_ok = 0.0
    if render.exists():
        render_ok = 1.0
        try:
            from PIL import Image as _I
            im = _I.open(render)
            if im.size == (1024, 1024):
                resolution_ok = 1.0
            elif min(im.size) >= 512:
                resolution_ok = 0.5
        except Exception:
            pass
    s["render_exists"] = render_ok
    s["render_resolution"] = resolution_ok

    # 7. color_compare.json  -> max_deltaE <= 4
    cc = rd / "color_compare.json"
    delta_ok = 0.0; rois_count = 0.0
    if cc.exists():
        try:
            d = json.loads(cc.read_text())
            rois = d.get("rois", [])
            rois_count = 1.0 if len(rois) >= 4 else len(rois) / 4.0
            def _rgb2lab(rgb):
                import colorsys
                r,g,b=[c/255.0 for c in rgb]
                def f(u): return ((u+0.055)/1.055)**2.4 if u>0.04045 else u/12.92
                R,G,B=f(r),f(g),f(b)
                X=R*0.4124+G*0.3576+B*0.1805; Y=R*0.2126+G*0.7152+B*0.0722; Z=R*0.0193+G*0.1192+B*0.9505
                X,Y,Z=X/0.95047,Y/1.0,Z/1.08883
                def fl(t): return t**(1/3) if t>0.008856 else 7.787*t+16/116
                L=116*fl(Y)-16; a=500*(fl(X)-fl(Y)); bb=200*(fl(Y)-fl(Z))
                return (L,a,bb)
            from PIL import Image as _CI
            mx=None
            ref_png_local = rd / "reference.png"
            if not ref_png_local.exists():
                ref_png_local = src / "reference.png"
            if render.exists() and ref_png_local.exists() and rois:
                rim=_CI.open(render).convert("RGB").resize((1024,1024))
                fim=_CI.open(ref_png_local).convert("RGB").resize((1024,1024))
                rois_rect={"fur":(150,150,350,350),"nose":(450,400,580,540),
                           "pupil":(310,310,370,370),"bg":(100,850,900,1000)}
                deltas=[]
                for name,(x0,y0,x1,y1) in rois_rect.items():
                    def _avg(im):
                        px=[im.getpixel((x,y)) for x in range(x0,x1,8) for y in range(y0,y1,8)]
                        n=len(px); return tuple(sum(p[i] for p in px)/n for i in range(3))
                    L1=_rgb2lab(_avg(rim)); L2=_rgb2lab(_avg(fim))
                    deltas.append(math.sqrt(sum((a-b)**2 for a,b in zip(L1,L2))))
                mx=max(deltas)
            if mx is not None and mx <= 4: delta_ok = 1.0
            elif mx is not None and mx <= 9: delta_ok = 0.5
        except Exception:
            pass
    s["color_compare_rois"] = rois_count
    s["color_compare_deltaE"] = delta_ok

    # 8. eyedrop RGB vs reference.png actual pixel sanity
    ref_png = rd / "reference.png"
    if not ref_png.exists():
        ref_png = src / "reference.png"
    sane = 0.0
    if samples and ref_png.exists():
        try:
            from PIL import Image as _I
            im = _I.open(ref_png).convert("RGB")
            W, H = im.size
            ok = 0; total = 0
            for sm in samples[:8]:
                try:
                    x = int(sm["x"]) % W; y = int(sm["y"]) % H
                    pr, pg, pb = im.getpixel((x, y))
                    dr = pr - int(sm["r"]); dg = pg - int(sm["g"]); db = pb - int(sm["b"])
                    dist = math.sqrt(dr*dr + dg*dg + db*db)
                    total += 1
                    if dist <= 12:
                        ok += 1
                except Exception:
                    pass
            sane = ok / total if total else 0.0
        except Exception:
            pass
    s["eyedrop_pixel_sanity"] = sane

    # 9. lookdev.md (>= 10 lines)
    lm = rd / "lookdev.md"
    lm_ok = 0.0
    if lm.exists():
        txt = lm.read_text()
        lines = [l for l in txt.splitlines() if l.strip()]
        need_kw = ["fur","nose","pupil","bg","decoy","ΔE","gamma"]
        hits = sum(1 for k in need_kw if k.lower() in txt.lower())
        if len(lines) >= 12 and hits >= 6: lm_ok = 1.0
        elif len(lines) >= 8 and hits >= 4: lm_ok = 0.5
    s["lookdev_md"] = lm_ok

    # 10. histogram divergence: render not a rename of reference
    hist_ok = 0.0
    if render.exists() and ref_png.exists():
        try:
            from PIL import Image as _I
            r = _I.open(render).convert("RGB").resize((128, 128))
            f = _I.open(ref_png).convert("RGB").resize((128, 128))
            diff = 0
            ra = list(r.getdata()); fa = list(f.getdata())
            for (a, b) in zip(ra, fa):
                diff += abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])
            avg_diff = diff / (len(ra) * 3)
            if 5 <= avg_diff <= 200:
                hist_ok = 1.0
            elif avg_diff > 0:
                hist_ok = 0.5
        except Exception:
            pass
    s["render_not_rename"] = hist_ok

    # --- 11. HDRI consistency ---
    hc = rd / "hdri_consistency.json"
    hc_ok = 0.0
    if hc.exists():
        try:
            j = json.loads(hc.read_text())
            renders = j.get("renders", [])
            present = sum(1 for r in renders
                          if (rd / str(r.get("render_path",""))).exists())
            from PIL import Image as _HI
            def _rgb2lab(rgb):
                r,g,b=[c/255.0 for c in rgb]
                def f(u): return ((u+0.055)/1.055)**2.4 if u>0.04045 else u/12.92
                R,G,B=f(r),f(g),f(b)
                X=R*0.4124+G*0.3576+B*0.1805; Y=R*0.2126+G*0.7152+B*0.0722; Z=R*0.0193+G*0.1192+B*0.9505
                X,Y,Z=X/0.95047,Y/1.0,Z/1.08883
                def fl(t): return t**(1/3) if t>0.008856 else 7.787*t+16/116
                L=116*fl(Y)-16; a=500*(fl(X)-fl(Y)); bb=200*(fl(Y)-fl(Z))
                return (L,a,bb)
            labs=[]
            for r in renders[:3]:
                p=rd/str(r.get("render_path",""))
                if p.exists():
                    im=_HI.open(p).convert("RGB").resize((128,128))
                    px=list(im.getdata()); n=len(px)
                    avg=tuple(sum(c[i] for c in px)/n for i in range(3))
                    labs.append(_rgb2lab(avg))
            mx=0.0
            for i in range(len(labs)):
                for j2 in range(i+1,len(labs)):
                    mx=max(mx,math.sqrt(sum((a-b)**2 for a,b in zip(labs[i],labs[j2]))))
            if (len(renders)>=3 and present>=3 and mx<=6.0): hc_ok=1.0
            elif present>=2 and mx<=12.0: hc_ok=0.5
        except Exception: pass
    s["hdri_consistency_ok"] = hc_ok

    # --- 12. PBR bake channels ---
    bake_ok = 0.0
    try:
        from PIL import Image as _BI
        score = 0
        # roughness
        rp = rd / "bake_roughness.png"
        if rp.exists() and rp.stat().st_size >= 5_000:
            im = _BI.open(rp).convert("L")
            if min(im.size) >= 512:
                px = list(im.resize((128,128)).getdata())
                m = sum(px)/len(px)/255.0
                if 0.2 <= m <= 0.85:
                    score += 1
        # normal
        np_ = rd / "bake_normal.png"
        if np_.exists() and np_.stat().st_size >= 5_000:
            im = _BI.open(np_).convert("RGB")
            if min(im.size) >= 512:
                px = list(im.resize((128,128)).getdata())
                rs = sum(p[0] for p in px)/len(px)
                gs = sum(p[1] for p in px)/len(px)
                bs = sum(p[2] for p in px)/len(px)
                if bs >= 180 and abs(rs - gs) < 80:
                    score += 1
        # ao
        ap = rd / "bake_ao.png"
        if ap.exists() and ap.stat().st_size >= 5_000:
            im = _BI.open(ap).convert("L")
            if min(im.size) >= 512:
                px = sorted(list(im.resize((128,128)).getdata()))
                m = sum(px)/len(px)/255.0
                p1 = px[max(0, len(px)//100)]
                if 0.4 <= m <= 0.95 and p1 <= 80:
                    score += 1
        bake_ok = score / 3.0
    except Exception:
        pass
    s["pbr_bake_ok"] = bake_ok

    # --- 13. UV checker ---
    uv_ok = 0.0
    uvj = rd / "uv_checker.json"
    if uvj.exists():
        try:
            j = json.loads(uvj.read_text())
            ec = float(j.get("edge_continuity_score", 0))
            si = float(j.get("stretched_islands_pct", 100))
            tx = rd / str(j.get("checker_tex_path",""))
            rn = rd / str(j.get("render_path",""))
            if (ec >= 0.6 and si <= 15 and tx.exists() and rn.exists()):
                uv_ok = 1.0
            elif tx.exists() and rn.exists():
                uv_ok = 0.5
        except Exception: pass
    s["uv_checker_ok"] = uv_ok

    # --- 14. exposure ratio ---
    ex_ok = 0.0
    exj = rd / "exposure_ratio.json"
    if exj.exists():
        try:
            j = json.loads(exj.read_text())
            err = float(j.get("ratio_error_pct", 99))
            m = rd / str(j.get("ev_minus2",""))
            p = rd / str(j.get("ev_plus2",""))
            from PIL import Image as _EI
            sizes_ok = 0
            for f in (m, p):
                if f.exists():
                    im = _EI.open(f)
                    if im.size == (1024, 1024):
                        sizes_ok += 1
            if err <= 25 and sizes_ok == 2:
                ex_ok = 1.0
            elif sizes_ok >= 1:
                ex_ok = 0.5
        except Exception: pass
    s["exposure_ratio_ok"] = ex_ok

    # --- 15. decoy check ---
    dc_ok = 0.0
    dcj = rd / "decoy_check.json"
    if dcj.exists():
        try:
            j = json.loads(dcj.read_text())
            in_decoy = sum(1 for sm in samples
                           if 700 <= int(sm.get("x",0)) <= 980
                           and 50 <= int(sm.get("y",0)) <= 280)
            rat = str(j.get("rationale",""))
            if (bool(j.get("skipped_decoy"))
                and int(j.get("samples_within_decoy_distance_le", 99)) == 0
                and len(rat) >= 120 and in_decoy == 0
                and any(k in rat.lower() for k in ["decoy","fluorescent","green","荧光"])
                and ("700" in rat or "decoy_color" in rat.lower())):
                dc_ok = 1.0
        except Exception: pass
    # Also independently scan eyedrop samples vs decoy color (50,240,50)
    if samples:
        bad = 0
        for sm in samples:
            try:
                dr = int(sm.get("r",0)) - 50
                dg = int(sm.get("g",0)) - 240
                db = int(sm.get("b",0)) - 50
                if math.sqrt(dr*dr + dg*dg + db*db) <= 30:
                    bad += 1
            except Exception: pass
        if bad > 0:
            dc_ok = min(dc_ok, 0.0)
    s["decoy_skipped_ok"] = dc_ok

    # VLM
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd / n) for n in
                ["view_blender_shader_editor.png",
                 "view_blender_viewport_matpreview.png",
                 "view_blender_image_editor.png"] if (rd / n).exists()]
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_blender_real_ui": "截图来自真实 Blender 3.x 界面，含顶部菜单 / Properties 面板",
            "vlm_shader_nodes_present": "Shader Editor 内可见 ≥ 2 个节点（如 Principled BSDF）",
            "vlm_viewport_lit": "3D Viewport 显示了着色后的几何体（不是默认灰色）",
            "vlm_no_python_traceback": "界面里没有 Python traceback 弹窗",
        }
        vlm = vlm_score_rubric(vlm_imgs, rubric,
                               instruction="评估 Blender lookdev 截图真实性。")
        for k in rubric:
            s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")

    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums) / len(nums) if nums else 0.0
    has_cli = (s.get("scene_blend", 0) + s.get("build_log", 0) +
               s.get("render_exists", 0)) > 0
    if not has_cli:
        base = min(base, 0.4)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the gui_screenshots_count / vlm_* sub_scores.
    if s.get("eyedrop_pixel_sanity", 0) < 0.5:
        base = min(base, 0.55)
    if s.get("color_compare_deltaE", 0) < 0.5:
        base = min(base, 0.45)
    if vlm_score_rubric is not None and s.get("vlm_blender_real_ui", 1.0) < 0.6:
        base = min(base, 0.5)
    if s.get("hdri_consistency_ok", 0) < 0.5 and s.get("pbr_bake_ok", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("decoy_skipped_ok", 0) < 0.5:
        base = min(base, 0.55)
    if s.get("hdri_consistency_ok", 0) < 0.5:
        base = min(base, 0.6)
    if s.get("pbr_bake_ok", 0) < 0.5:
        base = min(base, 0.6)
    if s.get("exposure_ratio_ok", 0) < 0.5:
        base = min(base, 0.65)
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
