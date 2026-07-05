# Auto-generated from WeaveBench task WEB_task_6_mv3_ext_bg_sw_debug.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """MV3 extension background SW debug grader."""
    import json, re, subprocess, zipfile
    from pathlib import Path
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    try:
        import pytesseract
        from PIL import Image
    except Exception:
        pytesseract = None
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    gt = workspace / "gt"
    s = {}

    def ocr_hits(path, kws):
        if not (pytesseract and path.exists()):
            return False
        try:
            tx = pytesseract.image_to_string(Image.open(path)).lower()
        except Exception:
            return False
        return any(k.lower() in tx for k in kws)

    # 1. manifest_audit.json
    ma = rd / "manifest_audit.json"
    audit_ids = []
    if ma.exists():
        try:
            d = json.loads(ma.read_text())
            findings = d.get("findings", [])
            req = {"id","severity","rule","evidence_path","expected","observed"}
            valid = [f for f in findings if isinstance(f, dict) and req <= set(f.keys())]
            audit_ids = [f.get("id","") for f in valid]
            s["manifest_audit_schema"] = 1.0 if len(valid) >= 4 else len(valid)/4.0
            ms_keys = {"manifest_version","permissions_declared","host_permissions_declared",
                       "content_scripts_matches","action_keys","background_type"}
            s["manifest_audit_meta"] = 1.0 if ms_keys <= set(d.keys()) else 0.4
        except Exception:
            s["manifest_audit_schema"] = 0.0
            s["manifest_audit_meta"] = 0.0
    else:
        s["manifest_audit_schema"] = 0.0
        s["manifest_audit_meta"] = 0.0

    # 2. zip + listing
    z = rd / "mv3_extension.zip"
    s["zip_built"] = 1.0 if z.exists() and z.stat().st_size > 500 else 0.0
    zl = rd / "zip_listing.txt"
    needed = ["manifest.json","background.js","popup.html","popup.js","content.js"]
    if zl.exists():
        t = zl.read_text(errors="ignore")
        hits = sum(1 for n in needed if n in t)
        s["zip_listing"] = hits / len(needed)
    else:
        s["zip_listing"] = 0.0

    # 3. extensions page screenshots
    p1 = rd / "view_01_extensions_devmode.png"
    p2 = rd / "view_02_ext_card_errors.png"
    s["ext_page_shots_present"] = (int(p1.exists()) + int(p2.exists())) / 2.0
    s["ext_page_shots_ocr"] = (int(ocr_hits(p1, ["developer mode","load unpacked","extensions"])) +
                               int(ocr_hits(p2, ["error","alarms","permission","service worker"]))) / 2.0 if pytesseract else 0.5

    # 4. popup fail
    p3 = rd / "view_03_popup_fail.png"
    s["popup_fail_shot"] = 1.0 if p3.exists() else 0.0
    s["popup_fail_ocr"] = 1.0 if ocr_hits(p3, ["reading time","reading"]) else (0.5 if not pytesseract else 0.0)

    # 5. bg sw devtools + permissions dump
    p4 = rd / "view_04_bg_sw_devtools.png"
    p5 = rd / "view_05_permissions_dump.png"
    s["bg_sw_shots_present"] = (int(p4.exists()) + int(p5.exists())) / 2.0
    s["bg_sw_shots_ocr"] = (int(ocr_hits(p4, ["chrome-extension","console","alarms","uncaught"])) +
                            int(ocr_hits(p5, ["permissions","tabs","storage","notifications"]))) / 2.0 if pytesseract else 0.5

    # 6. repro_report.md
    rr = rd / "repro_report.md"
    if rr.exists():
        t = rr.read_text(errors="ignore")
        line_refs = len(re.findall(r"background\.js:\s*L?\d+|manifest\.json:\s*L?\d+|background\.js:\d+", t))
        kw_ok = all(k in t.lower() for k in ["service worker","lifecycle"]) and ("alarm" in t.lower())
        s["repro_report"] = 1.0 if (len(t) >= 220 and line_refs >= 3 and kw_ok) else (0.5 if len(t) >= 150 else 0.2)
    else:
        s["repro_report"] = 0.0

    # 7. SW restart state evidence
    p6 = rd / "view_06_state_before.png"
    p7 = rd / "view_07_state_after_restart.png"
    s["sw_restart_evidence"] = (int(p6.exists()) + int(p7.exists())) / 2.0

    # 8. fixed manifest correctness
    fm = workspace / "mv3_extension_fixed/manifest.json"
    fm_signals = {"alarms_perm": False, "default_popup": False, "host_perm_python": False}
    if fm.exists():
        try:
            d = json.loads(fm.read_text())
            perms = d.get("permissions", []) or []
            host_perms = d.get("host_permissions", []) or []
            action = d.get("action", {}) or {}
            if "alarms" in perms: fm_signals["alarms_perm"] = True
            if isinstance(action, dict) and action.get("default_popup"): fm_signals["default_popup"] = True
            if any("docs.python.org" in h for h in host_perms): fm_signals["host_perm_python"] = True
        except Exception:
            pass
    s["fixed_manifest_signals"] = sum(1 for v in fm_signals.values() if v) / 3.0

    # 9. fixed background.js uses chrome.storage
    fb = workspace / "mv3_extension_fixed/background.js"
    bg_persist = False
    if fb.exists():
        bt = fb.read_text(errors="ignore")
        # Must both write and read storage to count as real persistence
        wrote = bool(re.search(r"chrome\.storage\.(local|session)\.set", bt))
        read = bool(re.search(r"chrome\.storage\.(local|session)\.get", bt))
        bg_persist = wrote and read
    s["bg_uses_storage"] = 1.0 if bg_persist else 0.0

    # 10. fix_diff.patch
    fd = rd / "fix_diff.patch"
    if fd.exists():
        t = fd.read_text(errors="ignore")
        covers = ("manifest.json" in t) and ("background.js" in t)
        s["fix_diff_present"] = 1.0 if (len(t) >= 100 and covers) else 0.4
    else:
        s["fix_diff_present"] = 0.0

    # 11. post-fix screenshots
    post_shots = ["view_08_ext_no_errors.png","view_09_popup_works.png",
                  "view_10_popup_with_data.png","view_11_state_persisted.png"]
    pp = sum(1 for n in post_shots if (rd/n).exists())
    s["post_fix_shots_present"] = pp / len(post_shots)
    pp_ocr = 0
    if pytesseract:
        ocr_kws = {
            "view_08_ext_no_errors.png": ["reading","tracker","service worker","details"],
            "view_09_popup_works.png":   ["reading time","reset","no data"],
            "view_10_popup_with_data.png":["s","reading"],
            "view_11_state_persisted.png":["s","reading"],
        }
        for n, kws in ocr_kws.items():
            if ocr_hits(rd/n, kws): pp_ocr += 1
    s["post_fix_shots_ocr"] = pp_ocr / len(post_shots) if pytesseract else 0.5

    # 12. verification.json
    vf = rd / "verification.json"
    vf_score = 0.0
    if vf.exists():
        try:
            d = json.loads(vf.read_text())
            req = {"finding_1_resolved","finding_2_resolved",
                   "finding_3_resolved","finding_4_resolved",
                   "popup_renders_after_sw_restart","errors_panel_clean_after_fix",
                   "fixed_zip_size_bytes"}
            if req <= set(d.keys()):
                vf_score = 0.5
                trues = sum(1 for k in ["finding_1_resolved","finding_2_resolved",
                                        "finding_3_resolved","finding_4_resolved"]
                            if d.get(k) is True)
                vf_score += 0.125 * trues
        except Exception:
            pass
    s["verification_json"] = min(1.0, vf_score)

    # 13. mv3_postmortem.md
    pm = rd / "mv3_postmortem.md"
    if pm.exists():
        t = pm.read_text(errors="ignore")
        kw_ok = all(k in t.lower() for k in ["service worker","chrome.storage"]) and "lifecycle" in t.lower()
        id_ok = sum(1 for i in audit_ids if i and i in t) >= max(2, len(audit_ids)//2) if audit_ids else True
        s["postmortem"] = 1.0 if (len(t) >= 300 and kw_ok and id_ok) else (0.5 if len(t) >= 200 else 0.2)
    else:
        s["postmortem"] = 0.0

    # 14. combined proof
    p12 = rd / "view_12_combined_proof.png"
    s["combined_proof"] = 1.0 if p12.exists() else 0.0

    # 15. extra deliverables required by Prompt
    s["fixed_zip_present"] = 1.0 if (rd / "mv3_extension_fixed.zip").exists() else 0.0
    s["fixed_manifest_keys_present"] = 1.0 if (rd / "fixed_manifest_keys.txt").exists() else 0.0

    # numeric agreement w/ gt
    expj = gt / "expected.json"
    if expj.exists():
        try:
            exp = json.loads(expj.read_text())
            hits_, total_ = 0, 0
            if "expected_audit_findings_min" in exp:
                total_ += 1
                if len(audit_ids) >= exp["expected_audit_findings_min"]: hits_ += 1
            if "expected_zip_required_files" in exp and zl.exists():
                total_ += 1
                t = zl.read_text(errors="ignore")
                if all(n in t for n in exp["expected_zip_required_files"]): hits_ += 1
            if "expected_fix_signals" in exp:
                sig_map = {
                    "default_popup_added": fm_signals.get("default_popup", False),
                    "alarms_permission_added": fm_signals.get("alarms_perm", False),
                    "host_permissions_covers_content_script_matches": fm_signals.get("host_perm_python", False),
                    "state_persisted_to_chrome_storage": bg_persist,
                }
                for sig in exp["expected_fix_signals"]:
                    if sig in sig_map:
                        total_ += 1
                        if sig_map[sig]: hits_ += 1
            s["numeric_agreement"] = hits_/total_ if total_ else 0.5
        except Exception:
            s["numeric_agreement"] = 0.0
    else:
        s["numeric_agreement"] = 0.5

    # VLM rubric (4 items)
    if vlm_score_rubric:
        candidates = ["view_02_ext_card_errors.png","view_04_bg_sw_devtools.png",
                      "view_07_state_after_restart.png","view_09_popup_works.png",
                      "view_11_state_persisted.png","view_12_combined_proof.png"]
        imgs = [str(rd/n) for n in candidates if (rd/n).exists()][:4]
        if imgs:
            rubric = {
                "vlm_devtools_sw_real": "至少一张截图清晰显示扩展 background service worker 的独立 DevTools 窗口(标题或地址条含 chrome-extension://,Console 面板有真实日志)",
                "vlm_errors_panel_real": "至少一张截图显示 chrome://extensions 的扩展卡片 Errors 面板,内有真实红色错误条目(非 PS 文字)",
                "vlm_popup_renders_after_fix": "修复后截图中 popup 真的弹出且能看到表格 / 'Reset' 按钮 / 域名行,而不是只有 tooltip",
                "vlm_state_persisted_after_restart": "view_11 中 popup 表格在 SW terminate+restart 之后仍包含累计数据,不为空",
            }
            try:
                vlm = vlm_score_rubric(imgs, rubric,
                    instruction="评估 MV3 扩展调试与修复的 GUI 证据真实性。")
                for k in rubric:
                    s[k] = vlm.get(k, 0.0)
                s["judge_method"] = vlm.get("judge_method", "failed")
            except Exception:
                for k in rubric:
                    s[k] = 0.0
                s["judge_method"] = "exception"

    # Anti-cheat: screenshot md5 uniqueness + minimum size
    import hashlib
    all_view_pngs = [p for p in rd.glob("view_*.png") if p.exists()]
    md5s, small = set(), 0
    for p in all_view_pngs:
        try:
            b = p.read_bytes()
            if len(b) < 5 * 1024:
                small += 1
            md5s.add(hashlib.md5(b).hexdigest())
        except Exception:
            pass
    if all_view_pngs:
        s["screenshot_md5_diversity"] = len(md5s) / len(all_view_pngs)
        s["screenshot_size_ok"] = 1.0 - (small / len(all_view_pngs))
    else:
        s["screenshot_md5_diversity"] = 0.0
        s["screenshot_size_ok"] = 0.0

    # Weighted aggregate: core deliverables 60% / GUI evidence 30% / aux 10%
    core_keys = ["manifest_audit_schema","manifest_audit_meta","zip_built","zip_listing",
                 "fixed_manifest_signals","bg_uses_storage","fix_diff_present",
                 "verification_json","numeric_agreement","fixed_zip_present",
                 "fixed_manifest_keys_present"]
    gui_keys  = ["ext_page_shots_present","ext_page_shots_ocr","popup_fail_shot","popup_fail_ocr",
                 "bg_sw_shots_present","bg_sw_shots_ocr","sw_restart_evidence",
                 "post_fix_shots_present","post_fix_shots_ocr","combined_proof",
                 "screenshot_md5_diversity","screenshot_size_ok",
                 "vlm_devtools_sw_real","vlm_errors_panel_real",
                 "vlm_popup_renders_after_fix","vlm_state_persisted_after_restart"]
    aux_keys  = ["repro_report","postmortem"]
    def avg(keys):
        vs = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return sum(vs) / len(vs) if vs else 0.0
    base = 0.6 * avg(core_keys) + 0.3 * avg(gui_keys) + 0.1 * avg(aux_keys)

    # Hard gates (strict v2)
    if s.get("ext_page_shots_present", 0) < 0.5:
        base = min(base, 0.35)
    if s.get("manifest_audit_schema", 0) < 0.5:
        base = min(base, 0.40)
    if s.get("fixed_manifest_signals", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("fixed_manifest_signals", 0) < 0.66:
        base = min(base, 0.40)
    if s.get("bg_uses_storage", 0) == 0:
        base = min(base, 0.45)
    if s.get("post_fix_shots_present", 0) < 0.75:
        base = min(base, 0.50)
    if s.get("post_fix_shots_present", 0) < 0.5:
        base = min(base, 0.40)
    if s.get("numeric_agreement", 0) < 0.5:
        base = min(base, 0.50)
    # Anti-cheat hard gates
    if s.get("screenshot_md5_diversity", 0) < 0.8 and len(all_view_pngs) >= 4:
        base = min(base, 0.45)
    if s.get("screenshot_size_ok", 0) < 0.8 and len(all_view_pngs) >= 4:
        base = min(base, 0.40)
    # VLM degradation cap: when VLM unavailable / failed, cap so无 VLM 也满分被禁
    jm = s.get("judge_method", "")
    if vlm_score_rubric is None or jm in ("failed", "exception", ""):
        base = min(base, 0.60)
    vlm_keys = ["vlm_devtools_sw_real","vlm_errors_panel_real",
                "vlm_popup_renders_after_fix","vlm_state_persisted_after_restart"]
    vlm_vs = [s[k] for k in vlm_keys if k in s]
    if vlm_vs:
        vlm_mean = sum(vlm_vs) / len(vlm_vs)
        if vlm_mean < 0.6:
            base = min(base, 0.55)
        if vlm_mean < 0.4:
            base = min(base, 0.40)

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
