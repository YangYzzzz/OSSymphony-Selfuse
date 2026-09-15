# Auto-generated from WeaveBench task DES_task_10_darktable_raw_tonecurve_recover.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Multi sub-score grader for darktable RAW recover + GIMP mask + IM check."""
    import csv, json, subprocess, os
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    raws = Path("/tmp_workspace/raws")
    s = {}

    # --- 1. raw_stats.csv schema + 3 rows ---
    rs_csv = rd / "raw_stats.csv"
    raw_schema_ok = 0; raw_rows = 0
    expect_cols = {"filename","mean","p05","p50","p95","entropy","max_used_bit"}
    if rs_csv.exists():
        try:
            rows = list(csv.DictReader(rs_csv.open()))
            if rows and expect_cols.issubset(set(rows[0].keys())):
                raw_schema_ok = 1
            raw_rows = len(rows)
        except Exception: pass
    s["raw_stats_present"] = 1.0 if rs_csv.exists() else 0.0
    s["raw_stats_schema"]  = float(raw_schema_ok)
    s["raw_stats_rows"]    = 1.0 if raw_rows >= 3 else raw_rows/3.0

    # --- 2. dev_stats.csv mean lifted >= 0.20 vs raw_stats.csv ---
    dv_csv = rd / "dev_stats.csv"
    lift_ok = 0
    if rs_csv.exists() and dv_csv.exists():
        try:
            r = {row["filename"]: float(row["mean"]) for row in csv.DictReader(rs_csv.open())}
            d = {row["filename"].replace("dev_","flat_"): float(row["mean"]) for row in csv.DictReader(dv_csv.open())}
            ok = 0
            for k in r:
                if "flat_d" in k:  # trap: skip
                    continue
                base = k.replace(".tif","").replace(".tiff","")
                for cand in [base, base.replace("flat_","dev_"), base+".png"]:
                    if cand in d and d[cand] - r[k] >= 0.20:
                        ok += 1; break
            lift_ok = 1 if ok >= 2 else 0
        except Exception: pass
    s["dev_stats_lifted"] = float(lift_ok)

    # --- 3. histogram_delta.json keys + delta > 0.22 ---
    hd = rd / "histogram_delta.json"
    hd_ok = 0
    if hd.exists():
        try:
            j = json.loads(hd.read_text())
            keys = ["flat_a","flat_b","flat_c"]
            if all(k in j and float(j[k].get("delta",0)) > 0.22 for k in keys):
                hd_ok = 1
        except Exception: pass
    s["histogram_delta_ok"] = float(hd_ok)

    # --- 4. dev_*.png exist ---
    dev_present = sum(1 for n in ["dev_a.png","dev_b.png","dev_c.png"] if (rd/n).exists())
    s["dev_pngs_present"] = dev_present / 3.0

    # --- 5. xmp_files.txt ---
    xf = rd / "xmp_files.txt"
    xmp_ok = 0
    if xf.exists():
        try:
            lines = [l.strip() for l in xf.read_text().splitlines() if l.strip()]
            if len(lines) >= 3:
                real = 0
                for l in lines[:3]:
                    p = Path(l)
                    if p.exists() and p.stat().st_size > 200:
                        b = p.read_bytes().lower()
                        if b"darktable:history" in b and (b"toneequal" in b or b"tonecurve" in b):
                            real += 1
                if real >= 3: xmp_ok = 1
        except Exception: pass
    s["xmp_sidecars"] = float(xmp_ok)

    # --- 6. dev_b_masked.xcf exists + >=2 layer ---
    xcf = rd / "dev_b_masked.xcf"
    xcf_ok = 0; layer_ct = 0
    if xcf.exists() and xcf.stat().st_size > 1024:
        xcf_ok = 1
        try:
            # Probe via real gimp CLI; if gimp is unavailable we keep
            # layer_ct=0 rather than running a brittle binary regex
            # (which used to count any NUL-padded ASCII as a layer
            # and could trivially be exploited by a fake .xcf blob).
            out = subprocess.run(
                ["gimp","-i","-b",
                 f'(let* ((img (car (gimp-xcf-load 0 "{xcf}" "")))) (gimp-message (number->string (car (gimp-image-get-layers img)))) (gimp-quit 0))'],
                capture_output=True, text=True, timeout=30)
            txt = out.stderr + out.stdout
            import re
            m = re.search(r"(\d+)", txt.split("Message:")[-1] if "Message" in txt else txt)
            if m: layer_ct = int(m.group(1))
        except Exception:
            layer_ct = 0
    s["xcf_present"] = float(xcf_ok)
    s["xcf_multi_layer"] = 1.0 if layer_ct >= 3 else (0.5 if layer_ct >= 2 else 0.0)

    # --- 7. exif_check.txt all 3 contain darktable ---
    ec = rd / "exif_check.txt"
    exif_hits = 0
    if ec.exists():
        try:
            import re as _re
            for line in ec.read_text().lower().splitlines():
                if _re.search(r"darktable\s+[345]\.\d", line) and "simulat" not in line:
                    exif_hits += 1
        except Exception: pass
    xmp_hist = sum(1 for n in ["flat_a","flat_b","flat_c"]
        if (raws/(n+".tif.xmp")).exists()
        and b"darktable:history" in (raws/(n+".tif.xmp")).read_bytes())
    s["exif_software"] = 1.0 if (exif_hits >= 3 and xmp_hist >= 3) else 0.0

    # --- 8 + 9. screenshots present + OCR keywords ---
    shots = ["view_dt_lighttable.png","view_dt_tonecurve.png","view_gimp_layer_mask.png"]
    shot_present = sum(1 for n in shots if (rd/n).exists() and (rd/n).stat().st_size > 5000)
    s["screenshots_present"] = shot_present / 3.0
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_dt_lighttable.png": ["lighttable","import","collect","filmstrip","selected"],
            "view_dt_tonecurve.png":  ["darkroom","tone","curve","equalizer","histogram"],
            "view_gimp_layer_mask.png": ["Layers","Mask","Brush","Tools","Channels"],
        }
        for n, ks in kws.items():
            p = rd/n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    hit = sum(1 for k in ks if k.lower() in tx.lower())
                    if hit >= 3: ocr_hits += 1
                except Exception: pass
        s["screenshots_ocr"] = ocr_hits / 3.0
    except ImportError:
        s["screenshots_ocr"] = 0.0

    # --- 10. manifest.json fields ---
    mf = rd / "manifest.json"
    manifest_struct_ok = 0; tcp_ok = 0; notes_ok = 0; tcp_mono_ok = 0
    if mf.exists():
        try:
            j = json.loads(mf.read_text())
            req = {"raws_inspected","tone_curve_points","exposure_lifted_files","mask_protected_file","agent_notes"}
            if req.issubset(set(j.keys())):
                manifest_struct_ok = 1
            tcp = j.get("tone_curve_points", [])
            non_end = [p for p in tcp if isinstance(p,(list,tuple)) and 0.0 < float(p[0]) < 1.0]
            if isinstance(tcp, list) and len(non_end) >= 5:
                tcp_ok = 1
            # monotonic check
            try:
                pts = sorted([(float(p[0]), float(p[1])) for p in tcp if isinstance(p,(list,tuple))])
                if pts and all(pts[i][1] <= pts[i+1][1] + 1e-6 for i in range(len(pts)-1)):
                    tcp_mono_ok = 1
            except Exception: pass
            if isinstance(j.get("agent_notes",""), str) and len(j["agent_notes"]) >= 120:
                notes_ok = 1
        except Exception: pass
    s["manifest_struct"] = float(manifest_struct_ok)
    s["manifest_tonecurve"] = float(tcp_ok)
    s["manifest_tonecurve_monotonic"] = float(tcp_mono_ok)
    s["manifest_notes"] = float(notes_ok)

    # --- 13. dev_channel_stats.csv: per-channel lift >= 0.10 ---
    chc = rd / "dev_channel_stats.csv"
    chc_ok = 0
    if chc.exists():
        try:
            rows = list(csv.DictReader(chc.open()))
            cols = {"filename","r_mean","g_mean","b_mean","r_lift","g_lift","b_lift"}
            if rows and cols.issubset(set(rows[0].keys())):
                ok_files = 0
                for r in rows:
                    if all(float(r.get(c,0)) >= 0.10 for c in ("r_lift","g_lift","b_lift")):
                        ok_files += 1
                if ok_files >= 3: chc_ok = 1
                elif ok_files >= 2: chc_ok = 0  # require all 3
        except Exception: pass
    s["channel_lift_uniform"] = float(chc_ok)

    # --- 14. noise_floor.json: noise_amp <= 4.5 each ---
    nf = rd / "noise_floor.json"
    nf_ok = 0
    if nf.exists():
        try:
            j = json.loads(nf.read_text())
            keys = ["flat_a","flat_b","flat_c"]
            need = {"raw_dark_std","dev_dark_std","noise_amp","snr_gain_db"}
            if all(k in j and need.issubset(set(j[k].keys())) for k in keys):
                if all(float(j[k]["noise_amp"]) <= 4.5 for k in keys):
                    nf_ok = 1
        except Exception: pass
    s["noise_floor_ok"] = float(nf_ok)

    # --- 15. highlight_rolloff.csv: flat_b frac_above_0_95 <= 0.012 ---
    hr = rd / "highlight_rolloff.csv"
    hr_ok = 0
    if hr.exists():
        try:
            rows = list(csv.DictReader(hr.open()))
            cols = {"filename","frac_above_0_90","frac_above_0_95","frac_above_0_99"}
            if rows and cols.issubset(set(rows[0].keys())):
                bdic = next((r for r in rows if "b" in r.get("filename","").lower()), None)
                if bdic and float(bdic["frac_above_0_95"]) <= 0.012:
                    hr_ok = 1
        except Exception: pass
    s["highlight_rolloff_ok"] = float(hr_ok)

    # --- 16. mask_iou.json: iou >= 0.55 ---
    # Don't trust the agent's self-reported `iou` field — recompute the
    # true IoU between the agent's mask (mask_b.png binary or extracted
    # from dev_b_masked.xcf) and the warmup-generated highlight bbox in
    # /opt/dav10_gt/highlight_bbox.json (root-only). Fall back to the
    # agent-reported value only if no mask file is present.
    mi = rd / "mask_iou.json"
    mi_ok = 0; iou_val = 0.0
    bbox_path_root = Path("/opt/dav10_gt/highlight_bbox.json")
    bbox_path_legacy = Path("/tmp_workspace/gt/highlight_bbox.json")
    bbox_path = bbox_path_root if bbox_path_root.exists() else bbox_path_legacy
    gt_bbox = None
    if bbox_path.exists():
        try:
            gt_bbox = json.loads(bbox_path.read_text()).get("bbox")
        except Exception:
            gt_bbox = None

    # --- GT-leak audit ---
    # Confirmed incident: a stale GUI docker image shipped with a leftover
    # `/tmp_workspace/gt/highlight_bbox.json` (the warmup `rmdir` silently
    # failed because the dir was non-empty). gpt-5.4-pro was observed
    # cat'ing that file in turn 5 and bypassing the visual highlight
    # detection step entirely. The setup script is now fixed to `rm -rf`
    # the dir, but we ALSO audit the agent's chat.jsonl here so any
    # surviving image regression — or any future agent that finds a new
    # GT path — is caught at grading time. On hit: zero out mask_iou_ok
    # AND impose an overall cap at 0.4 (parity with `has_cli=False`).
    audit_banned_hit = False
    audit_info = {}
    try:
        from _judge_helper import audit_chat_jsonl_for_banned
        audit_info = audit_chat_jsonl_for_banned([
            "/tmp_workspace/gt/highlight_bbox",
            "/opt/dav10_gt/",
            "dav10_gt/highlight_bbox",
        ])
        audit_banned_hit = bool(audit_info.get("any_banned"))
    except Exception:
        audit_banned_hit = False
    s["audit_banned"] = 1.0 if audit_banned_hit else 0.0

    def _compute_real_iou(mask_path, bbox):
        try:
            from PIL import Image
            import numpy as _np
            arr = _np.asarray(Image.open(mask_path).convert("L"))
            mask_pixels = arr > 127
            x0, y0, x1, y1 = [int(v) for v in bbox]
            gt_mask = _np.zeros_like(mask_pixels, dtype=bool)
            x0 = max(0, min(arr.shape[1]-1, x0)); x1 = max(0, min(arr.shape[1], x1))
            y0 = max(0, min(arr.shape[0]-1, y0)); y1 = max(0, min(arr.shape[0], y1))
            gt_mask[y0:y1, x0:x1] = True
            inter = int((mask_pixels & gt_mask).sum())
            union = int((mask_pixels | gt_mask).sum())
            return (inter / union) if union else 0.0
        except Exception:
            return None

    real_iou = None
    mask_b_png = rd / "mask_b.png"
    if gt_bbox is not None and mask_b_png.exists():
        real_iou = _compute_real_iou(mask_b_png, gt_bbox)
    if real_iou is not None:
        iou_val = float(real_iou)
    elif mi.exists():
        # No mask_b.png available — fall back to the (untrusted) self-
        # reported value, but cap it at 0.55 so it cannot exceed the
        # threshold without an actual mask file.
        try:
            j = json.loads(mi.read_text())
            iou_val = min(0.55, float(j.get("iou", 0)))
        except Exception:
            iou_val = 0.0
    if iou_val >= 0.55: mi_ok = 1
    # If the agent peeked at the GT bbox file, the IoU is meaningless —
    # the agent could have drawn a perfect mask from the leaked coords.
    if audit_banned_hit:
        mi_ok = 0
        iou_val = 0.0
    s["mask_iou_ok"] = float(mi_ok)
    s["mask_iou_partial"] = max(0.0, min(1.0, iou_val / 0.55))

    # --- 17. trap_check.json: must skip flat_d, mean shift <= 0.05 ---
    tc = rd / "trap_check.json"
    tc_ok = 0
    if tc.exists():
        try:
            j = json.loads(tc.read_text())
            import re as _r2
            rat = str(j.get("rationale",""))
            has_num = bool(_r2.search(r"0\.[4-6]\d", rat)) and "mean" in rat.lower()
            raw_d = float(j.get("raw_mean", 0))
            if (str(j.get("decision","")).lower() == "skip"
                and float(j.get("dev_d_mean_shift", 1.0)) <= 0.05
                and len(rat) >= 60 and has_num and 0.45 <= raw_d <= 0.65):
                tc_ok = 1
        except Exception: pass
    # also check that no aggressive dev_d.png with high mean exists
    trap_violation = 0
    try:
        from PIL import Image
        import numpy as _np
        ddev = rd / "dev_d.png"
        if ddev.exists():
            arr = _np.asarray(Image.open(ddev).convert("L"), dtype=float)/255.0
            if float(arr.mean()) > 0.70:
                trap_violation = 1
    except Exception: pass
    s["trap_skip_ok"] = float(tc_ok and not trap_violation)

    # --- VLM rubric ---
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_dark = 0.5
    if vlm_score_rubric and (rd/"view_dt_tonecurve.png").exists():
        rubric = {
            "vlm_in_darkroom": "截图位于 darktable darkroom 模式（左右两列模块面板，中间预览图）",
            "vlm_curve_visible": "截图里能看到 tone curve / tone equalizer 的曲线图与 ≥3 个控制点",
            "vlm_image_brightened": "中央预览图相比 lighttable 缩略图明显被抬亮",
            "vlm_gimp_mask_visible": "GIMP 截图中 Layers 面板能看到 layer mask 缩略图",
        }
        imgs = [str(rd/"view_dt_tonecurve.png"), str(rd/"view_gimp_layer_mask.png"),
                str(rd/"view_dt_lighttable.png")]
        imgs = [p for p in imgs if Path(p).exists()]
        try:
            v = vlm_score_rubric(imgs[:3], rubric, instruction="评估摄影师 RAW 还原的 GUI 取证截图。")
            for k in rubric: s[k] = v.get(k, 0.0)
            vlm_dark = sum(s[k] for k in rubric)/len(rubric)
        except Exception:
            for k in rubric: s[k] = 0.5

    # --- Hard gates ---
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums)
    has_cli = (rs_csv.exists() and dv_csv.exists() and ec.exists())
    if not has_cli:                     base = min(base, 0.4)
    # GT-leak hard cap: if the chat audit found the agent reading the
    # bbox / GT files (parity with the `/tmp_workspace/gt/` incident),
    # cap the overall at 0.4 — the IoU and any downstream "highlight
    # was correctly identified" claims are uncredible.
    if audit_banned_hit:                base = min(base, 0.4)
    # NOTE: We deliberately do NOT cap on missing GUI screenshots —
    # whether the agent invokes darktable/GIMP UI tooling is not a
    # scoring axis. Missing PNGs already cost screenshots_present /
    # screenshots_ocr / 4 vlm_*; no additional hard cap is applied.
    # VLM caps aligned with batch3 (vlm_avg<0.6 cap @0.5) and only
    # enforced when the helper actually ran.
    if vlm_score_rubric is not None and vlm_dark < 0.6:
        base = min(base, 0.5)
    if vlm_score_rubric is not None and \
       min(s.get(k,0) for k in ("vlm_in_darkroom","vlm_curve_visible","vlm_gimp_mask_visible")) < 0.5:
        base = min(base, 0.45)
    if s.get("xcf_present",0) == 0:     base = min(base, 0.55)
    if s.get("histogram_delta_ok",0)==0:base = min(base, 0.55)
    if s.get("trap_skip_ok",0) == 0:    base = min(base, 0.45)  # trap is critical
    if s.get("noise_floor_ok",0) == 0:  base = min(base, 0.6)
    if s.get("mask_iou_ok",0) == 0:     base = min(base, 0.6)
    if s.get("channel_lift_uniform",0)==0: base = min(base, 0.6)
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
