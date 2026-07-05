# Auto-generated from WeaveBench task WEB_task_5_sw_cache_poison_purge.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """SW cache poisoning forensics + fix grader."""
    import json, re, subprocess
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

    # 1. headers triple
    h_files = ["headers_v1.txt", "headers_v2.txt", "headers_v1_revalidate.txt"]
    h_present = sum(1 for n in h_files if (rd/n).exists())
    h_with_etag = 0
    for n in h_files:
        p = rd/n
        if p.exists() and re.search(r"(?i)etag\s*:", p.read_text(errors="ignore")):
            h_with_etag += 1
    s["headers_triple"] = h_present / 3.0
    s["headers_have_etag"] = h_with_etag / 3.0

    # 2. network_truth.md
    nt = rd / "network_truth.md"
    if nt.exists():
        txt = nt.read_text(errors="ignore")
        s["network_truth"] = 1.0 if (len(txt) >= 150 and "etag" in txt.lower()) else 0.4
    else:
        s["network_truth"] = 0.0

    # 3. Application panel screenshots
    app_shots = {
        "view_01_sw_registered.png":      ["service worker", "scope", "activated", "running"],
        "view_02_cache_storage_v1.png":   ["cache storage", "products", "request", "response"],
        "view_03_network_from_sw.png":    ["serviceworker", "network", "initiator", "size"],
    }
    present = sum(1 for n in app_shots if (rd/n).exists())
    hits = sum(1 for n,kw in app_shots.items() if ocr_hits(rd/n, kw))
    s["application_shots_present"] = present / len(app_shots)
    s["application_shots_ocr"] = hits / len(app_shots) if pytesseract else 0.5

    # 4. pollution evidence
    p4 = rd / "view_04_v2_polluted.png"
    p5 = rd / "view_05_console_diff.png"
    s["pollution_view_present"] = (int(p4.exists()) + int(p5.exists())) / 2.0
    s["pollution_view_ocr"] = (int(ocr_hits(p4, ["v1","mug","hoodie","cap"])) +
                               int(ocr_hits(p5, ["products","url","method"]))) / 2.0 if pytesseract else 0.5

    # 5. CLI disk inspection
    si = rd / "sw_disk_index.txt"
    se = rd / "sw_storage_explained.md"
    si_lines = len(si.read_text(errors="ignore").splitlines()) if si.exists() else 0
    s["sw_disk_index"] = 1.0 if si_lines >= 5 else si_lines / 5.0
    if se.exists():
        t = se.read_text(errors="ignore")
        s["sw_storage_explain"] = 1.0 if (len(t) >= 80 and ("hash" in t.lower() or "index" in t.lower())) else 0.4
    else:
        s["sw_storage_explain"] = 0.0

    # 6. sw_audit.json
    sa = rd / "sw_audit.json"
    audit_ok = 0.0
    audit_ids = []
    if sa.exists():
        try:
            arr = json.loads(sa.read_text())
            if isinstance(arr, list):
                req = {"id","category","code_anchor","evidence","user_visible_symptom"}
                valid = [e for e in arr if isinstance(e, dict) and req <= set(e.keys())]
                audit_ids = [e.get("id","") for e in valid]
                audit_ok = 1.0 if len(valid) >= 4 else len(valid)/4.0
        except Exception:
            pass
    s["sw_audit_schema"] = audit_ok

    # 7. network sw intercept screenshot
    p6 = rd / "view_06_network_sw_intercept.png"
    s["network_intercept_shot"] = 1.0 if p6.exists() else 0.0
    s["network_intercept_ocr"] = 1.0 if ocr_hits(p6, ["serviceworker","disable cache"]) else (0.5 if not pytesseract else 0.0)

    # 8. fixed sw.js
    fixed_sw = workspace / "cache_app_fixed/public/sw.js"
    orig_sw  = workspace / "cache_app/public/sw.js"
    fix_signals = {"version_in_cache_name": False, "activate_cleanup": False,
                   "swr_or_network_first": False, "query_preserved": False}
    if fixed_sw.exists():
        ftxt = fixed_sw.read_text(errors="ignore")
        if re.search(r"cache[-_]app[-_]store[-_]v\d|CACHE\s*=\s*['\"][^'\"]*v\d", ftxt):
            fix_signals["version_in_cache_name"] = True
        if "caches.keys" in ftxt and "delete" in ftxt:
            fix_signals["activate_cleanup"] = True
        if re.search(r"network[\s_-]?first|stale[\s_-]?while[\s_-]?revalidate|fetch\(.*\).*then|await\s+fetch", ftxt, re.I):
            # crude: see fetch as primary path
            if "fromCacheFirst" not in ftxt or "networkFirst" in ftxt or "staleWhileRevalidate" in ftxt:
                fix_signals["swr_or_network_first"] = True
        # query preserved = no manual stripping of search
        if "keyUrl.search = \"\"" not in ftxt and "url.search = \"\"" not in ftxt:
            fix_signals["query_preserved"] = True
    s["fix_signals_count"] = sum(1 for v in fix_signals.values() if v) / 4.0
    if fixed_sw.exists() and orig_sw.exists():
        try:
            d = subprocess.run(["diff","-u",str(orig_sw),str(fixed_sw)],
                               capture_output=True, text=True, timeout=10)
            dl = sum(1 for l in d.stdout.splitlines() if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++","---")))
            s["fix_diff_size"] = 1.0 if dl >= 12 else dl/12.0
        except Exception:
            s["fix_diff_size"] = 0.5
    else:
        s["fix_diff_size"] = 0.0

    # 9. v2 verification screenshots
    p7 = rd / "view_07_v2_visible.png"
    p8 = rd / "view_08_old_cache_purged.png"
    s["fix_shots_present"] = (int(p7.exists()) + int(p8.exists())) / 2.0
    s["fix_shots_ocr"] = (int(ocr_hits(p7, ["tote","v2"])) +
                          int(ocr_hits(p8, ["cache","storage"]))) / 2.0 if pytesseract else 0.5

    # 10. fix_verification.json
    fv = rd / "fix_verification.json"
    fv_score = 0.0
    if fv.exists():
        try:
            d = json.loads(fv.read_text())
            req = {"before_fix_items_count","after_fix_items_count","before_fix_has_tote",
                   "after_fix_has_tote","old_cache_name_present_after_activate","new_cache_name"}
            if req <= set(d.keys()):
                fv_score = 0.5
                if d.get("after_fix_has_tote") is True and d.get("before_fix_has_tote") is False:
                    fv_score += 0.25
                if d.get("old_cache_name_present_after_activate") is False:
                    fv_score += 0.25
        except Exception:
            pass
    s["fix_verification"] = fv_score

    # 11. patch + report
    pf = rd / "sw_fix.patch"
    s["sw_fix_patch"] = 1.0 if (pf.exists() and len(pf.read_text(errors="ignore")) >= 80) else 0.0
    ir = rd / "incident_report.md"
    if ir.exists():
        t = ir.read_text(errors="ignore")
        kw_hit = any(k in t.lower() for k in ["network-first","network first","stale-while-revalidate","swr"])
        if audit_ids:
            id_hit = sum(1 for i in audit_ids if i and i in t) >= max(2, len(audit_ids)//2)
        else:
            id_hit = True
        s["incident_report"] = 1.0 if (len(t) >= 250 and kw_hit and id_hit) else (0.5 if len(t) >= 150 else 0.2)
    else:
        s["incident_report"] = 0.0

    # 11b. before/after v2 json (Prompt mandates these files)
    bv2 = rd / "before_fix_v2.json"
    av2 = rd / "after_fix_v2.json"
    v2_score = 0.0
    if bv2.exists():
        v2_score += 0.25
        try:
            json.loads(bv2.read_text(errors="ignore"))
            v2_score += 0.25
        except Exception:
            pass
    if av2.exists():
        v2_score += 0.25
        try:
            json.loads(av2.read_text(errors="ignore"))
            v2_score += 0.25
        except Exception:
            pass
    s["v2_payload_files"] = v2_score

    # 12. combined evidence
    p9 = rd / "view_09_combined_evidence.png"
    s["combined_evidence_shot"] = 1.0 if p9.exists() else 0.0

    # numeric agreement with gt
    expj = gt / "expected.json"
    if expj.exists():
        try:
            exp = json.loads(expj.read_text())
            hits_, total_ = 0, 0
            if "min_initial_violations" in exp:
                total_ += 1
                if audit_ok >= (exp["min_initial_violations"]/4.0):
                    hits_ += 1
            if "expected_v2_visible_after_fix" in exp:
                total_ += 1
                try:
                    d = json.loads(fv.read_text()) if fv.exists() else {}
                    if d.get("after_fix_has_tote") is exp["expected_v2_visible_after_fix"]:
                        hits_ += 1
                except Exception:
                    pass
            s["numeric_agreement"] = hits_/total_ if total_ else 0.5
        except Exception:
            s["numeric_agreement"] = 0.0
    else:
        s["numeric_agreement"] = 0.5

    # VLM rubric (4 items)
    if vlm_score_rubric:
        imgs = [str(rd/n) for n in
                ["view_02_cache_storage_v1.png","view_04_v2_polluted.png",
                 "view_07_v2_visible.png","view_08_old_cache_purged.png",
                 "view_09_combined_evidence.png"] if (rd/n).exists()][:4]
        if imgs:
            rubric = {
                "vlm_application_panel_real": "至少一张截图清晰显示 Chrome DevTools Application 面板的 Cache Storage 树或 Service Workers 面板(左侧导航 + 右侧详情)",
                "vlm_pollution_visible": "至少一张截图能看到污染现象——v2 url 但表格仍显示 v1 数据,或 console.table 输出中 url 没有 ?v= 查询串",
                "vlm_fix_v2_visible": "view_07 中表格能看到 v2 独有数据(Tote 或 4 行商品)且 build badge 显示 v2",
                "vlm_old_cache_purged": "view_08 中 Cache Storage 左侧不再有无版本号的旧 cache 名,只剩版本化的新 cache 名",
            }
            vlm = vlm_score_rubric(imgs, rubric,
                instruction="评估 Service Worker 缓存污染取证 + 修复验证截图的真实性与说服力。")
            for k in rubric:
                s[k] = vlm.get(k, 0.0)
            s["judge_method"] = vlm.get("judge_method", "failed")

    # Anti-cheat: screenshot md5 uniqueness + min file size
    import hashlib
    shot_names = ["view_01_sw_registered.png","view_02_cache_storage_v1.png",
                  "view_03_network_from_sw.png","view_04_v2_polluted.png",
                  "view_05_console_diff.png","view_06_network_sw_intercept.png",
                  "view_07_v2_visible.png","view_08_old_cache_purged.png",
                  "view_09_combined_evidence.png"]
    shot_md5s, shot_sizes = [], []
    for n in shot_names:
        p = rd / n
        if p.exists():
            try:
                b = p.read_bytes()
                shot_md5s.append(hashlib.md5(b).hexdigest())
                shot_sizes.append(len(b))
            except Exception:
                pass
    uniq = len(set(shot_md5s))
    nshots = len(shot_md5s)
    s["shot_md5_uniqueness"] = (uniq / nshots) if nshots else 0.0
    s["shot_min_size_ok"] = (sum(1 for sz in shot_sizes if sz >= 5120) / nshots) if nshots else 0.0

    # Weighted aggregate: core delivery 60% / GUI evidence 30% / aux 10%
    def _g(k, d=0.0):
        v = s.get(k, d)
        return float(v) if isinstance(v, (int, float)) else d

    core_keys = ["headers_triple","headers_have_etag","sw_audit_schema",
                 "fix_signals_count","fix_diff_size","fix_verification",
                 "sw_fix_patch","incident_report","v2_payload_files",
                 "numeric_agreement"]
    gui_keys  = ["application_shots_present","application_shots_ocr",
                 "pollution_view_present","pollution_view_ocr",
                 "network_intercept_shot","network_intercept_ocr",
                 "fix_shots_present","fix_shots_ocr",
                 "combined_evidence_shot",
                 "shot_md5_uniqueness","shot_min_size_ok"]
    aux_keys  = ["network_truth","sw_disk_index","sw_storage_explain"]
    vlm_keys  = ["vlm_application_panel_real","vlm_pollution_visible",
                 "vlm_fix_v2_visible","vlm_old_cache_purged"]

    def _avg(keys):
        vals = [_g(k) for k in keys if k in s]
        return sum(vals)/len(vals) if vals else 0.0

    core = _avg(core_keys)
    gui_only = _avg(gui_keys)
    vlm_present = any(k in s for k in vlm_keys)
    vlm_avg = _avg(vlm_keys) if vlm_present else 0.0
    gui = (0.6 * gui_only + 0.4 * vlm_avg) if vlm_present else gui_only
    aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Hard gates (tightened, multi-layer)
    if s.get("application_shots_present", 0) < 0.67:
        base = min(base, 0.4)
    if s.get("sw_audit_schema", 0) < 0.75:
        base = min(base, 0.4)
    if s.get("fix_signals_count", 0) < 0.75:
        base = min(base, 0.4)
    if s.get("fix_verification", 0) < 0.75:
        base = min(base, 0.45)
    if s.get("fix_shots_present", 0) < 1.0:
        base = min(base, 0.45)
    if s.get("fix_diff_size", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("sw_fix_patch", 0) == 0:
        base = min(base, 0.45)
    if s.get("v2_payload_files", 0) < 0.5:
        base = min(base, 0.5)
    if s.get("headers_have_etag", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("incident_report", 0) < 0.5:
        base = min(base, 0.5)
    if s.get("numeric_agreement", 0) < 0.5:
        base = min(base, 0.55)
    # OCR evidence layer (only when pytesseract is available)
    if pytesseract:
        ocr_avg = (s.get("application_shots_ocr",0) + s.get("pollution_view_ocr",0)
                   + s.get("fix_shots_ocr",0)) / 3.0
        if ocr_avg < 0.5:
            base = min(base, 0.5)
    # Anti-cheat caps
    if nshots and s["shot_md5_uniqueness"] < 0.9:
        base = min(base, 0.4)
    if nshots and s["shot_min_size_ok"] < 0.8:
        base = min(base, 0.45)
    if nshots < 7:
        base = min(base, 0.5)
    # VLM unavailable cap
    if not vlm_present or s.get("judge_method") in (None, "failed"):
        base = min(base, 0.6)
    elif vlm_avg < 0.5:
        base = min(base, 0.5)

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
