# Auto-generated from WeaveBench task WEB_task_2_oauth_pkce_token_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """OAuth PKCE token audit grader: file checks + schema + OCR + VLM."""
    import json, re
    from pathlib import Path
    try:
        from PIL import Image
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

    # 1-2. Consent + logged-in screenshots
    gui_shots = {
        "view_consent_page.png": ["Authorize", "scope", "alice", "Login", "consent"],
        "view_logged_in.png": ["alice", "Logged", "token", "access"],
    }
    gui_present = 0
    gui_ocr = 0
    for fname, keywords in gui_shots.items():
        p = rd / fname
        if p.exists():
            gui_present += 1
            if pytesseract:
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in keywords):
                        gui_ocr += 1
                except Exception:
                    pass
    s["consent_shots_present"] = gui_present / 2.0
    s["consent_shots_ocr"] = gui_ocr / 2.0

    # 3-4. DevTools token request/response screenshots
    dt_shots = {
        "view_devtools_token_request.png": ["authorization_code", "code_verifier", "POST", "token"],
        "view_devtools_token_response.png": ["access_token", "expires_in", "refresh_token"],
    }
    dt_present = 0
    dt_ocr = 0
    for fname, keywords in dt_shots.items():
        p = rd / fname
        if p.exists():
            dt_present += 1
            if pytesseract:
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in keywords):
                        dt_ocr += 1
                except Exception:
                    pass
    s["devtools_token_present"] = dt_present / 2.0
    s["devtools_token_ocr"] = dt_ocr / 2.0

    # 5. token_decoded.json
    td = rd / "token_decoded.json"
    td_data = {}
    if td.exists():
        try:
            td_data = json.loads(td.read_text())
        except Exception:
            pass
    # Accept nested or flat structure
    has_alg = "alg" in str(td_data)
    has_sub = "sub" in str(td_data)
    has_exp = "exp" in str(td_data)
    s["token_decoded"] = 1.0 if (has_alg and has_sub and has_exp) else (
        0.5 if td_data else 0.0)

    # 6. token_audit.json
    ta = rd / "token_audit.json"
    ta_data = {}
    if ta.exists():
        try:
            ta_data = json.loads(ta.read_text())
        except Exception:
            pass
    has_lifetime = isinstance(ta_data.get("token_lifetime_seconds"), (int, float))
    has_issue = isinstance(ta_data.get("lifetime_issue"), str) and len(ta_data.get("lifetime_issue", "")) > 5
    has_missing = isinstance(ta_data.get("missing_claims"), list)
    s["token_audit_schema"] = 1.0 if (has_lifetime and has_issue and has_missing) else (
        0.5 if ta_data else 0.0)
    # Check lifetime is correctly identified as too short
    if has_lifetime:
        lt = ta_data["token_lifetime_seconds"]
        s["lifetime_correct"] = 1.0 if (lt <= 120) else 0.0
    else:
        s["lifetime_correct"] = 0.0

    # 7. cors_test.txt
    ct = rd / "cors_test.txt"
    ct_text = ct.read_text(errors="ignore") if ct.exists() else ""
    has_http = "HTTP" in ct_text or "curl" in ct_text.lower()
    has_ac = "Access-Control" in ct_text or "access-control" in ct_text.lower() or "Origin" in ct_text
    s["cors_test"] = 1.0 if (len(ct_text) > 50 and has_http and has_ac) else (
        0.5 if (len(ct_text) > 50 and has_http) else 0.0)

    # 8. CORS error screenshot
    cors_shot = rd / "view_devtools_cors_error.png"
    s["cors_error_shot"] = 1.0 if cors_shot.exists() else 0.0
    if cors_shot.exists() and pytesseract:
        try:
            tx = pytesseract.image_to_string(Image.open(cors_shot))
            if any(k in tx for k in ["CORS", "Access-Control", "cross-origin", "blocked"]):
                s["cors_error_ocr"] = 1.0
            else:
                s["cors_error_ocr"] = 0.0
        except Exception:
            s["cors_error_ocr"] = 0.0
    else:
        s["cors_error_ocr"] = 0.0

    # 9. auth_server_fixed.js
    fixed = workspace / "oauth_app/auth_server_fixed.js"
    s["fixed_exists"] = 1.0 if fixed.exists() else 0.0
    if fixed.exists():
        code = fixed.read_text(errors="ignore")
        has_cors = any(k in code for k in [
            "Access-Control-Allow-Origin", "cors", "CORS",
        ])
        has_lifetime_fix = "3600" in code or "60 * 60" in code or "3600000" in code
        s["fix_quality"] = 1.0 if (has_cors and has_lifetime_fix) else (
            0.5 if (has_cors or has_lifetime_fix) else 0.0)
    else:
        s["fix_quality"] = 0.0

    # 10. fix_verification.json
    fv = rd / "fix_verification.json"
    fv_data = {}
    if fv.exists():
        try:
            fv_data = json.loads(fv.read_text())
        except Exception:
            pass
    lt_ok = fv_data.get("new_token_lifetime_seconds") == 3600
    cors_ok = fv_data.get("cors_headers_present") is True
    refresh_ok = fv_data.get("refresh_succeeds") is True
    s["verification_json"] = 1.0 if (lt_ok and cors_ok and refresh_ok) else (
        0.5 if fv_data else 0.0)

    # 11. audit_report.md
    ar = rd / "audit_report.md"
    ar_text = ar.read_text(errors="ignore") if ar.exists() else ""
    issue_count = len(re.findall(r"(?i)(问题|issue|bug|vulnerability|misconfigur)", ar_text))
    has_diff = "diff" in ar_text.lower() or "---" in ar_text or "+++" in ar_text
    s["audit_report"] = 1.0 if (issue_count >= 2 and has_diff and len(ar_text) > 200) else (
        0.5 if ar.exists() else 0.0)

    # 12. Fixed token info screenshot
    ft_shot = rd / "view_fixed_token_info.png"
    s["fixed_token_shot"] = 1.0 if ft_shot.exists() else 0.0

    # VLM judge
    all_shots = [str(rd / n) for n in [
        "view_consent_page.png", "view_logged_in.png",
        "view_devtools_token_request.png", "view_devtools_cors_error.png",
    ] if (rd / n).exists()]
    if vlm_score_rubric and all_shots:
        rubric = {
            "vlm_consent_real": "截图显示真实的 OAuth 授权同意页面（含输入框和 Authorize 按钮）",
            "vlm_devtools_real": "截图显示真实的 Chrome DevTools Network/Console 面板",
            "vlm_token_visible": "截图中可见 JWT token 或 OAuth 相关参数",
        }
        vlm = vlm_score_rubric(all_shots[:4], rubric,
            instruction="评估 OAuth PKCE 授权流程截图的真实性和完整性。")
        for k in rubric:
            s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")

    # --- GUI hard-gate sub-score: 真实浏览器交互信号 ---
    import hashlib
    trajectory_shots = [
        "view_consent_page.png",
        "view_logged_in.png",
        "view_devtools_token_request.png",
        "view_devtools_token_response.png",
        "view_devtools_cors_error.png",
        "view_fixed_token_info.png",
    ]
    shot_paths = [rd / n for n in trajectory_shots if (rd / n).exists()]
    # Anti-cheat: drop placeholder files < 5KB
    shot_paths = [p for p in shot_paths if p.stat().st_size >= 5 * 1024]
    gui_signal = 0.0
    if len(shot_paths) >= 3:
        hashes = {hashlib.md5(p.read_bytes()).hexdigest() for p in shot_paths}
        uniq_ratio = len(hashes) / len(shot_paths)
        uniq_score = 1.0 if uniq_ratio >= 0.8 else uniq_ratio * 0.5
        common_res = {(1920, 1080), (1366, 768), (1440, 900), (1536, 864),
                      (1680, 1050), (1280, 800), (1280, 720), (2560, 1440),
                      (1600, 900), (1920, 1200)}
        res_hits = 0
        try:
            for p in shot_paths:
                with Image.open(p) as im:
                    w, h = im.size
                if (w, h) in common_res or (w >= 1280 and h >= 720 and 1.2 <= w / h <= 2.4):
                    res_hits += 1
        except Exception:
            pass
        res_score = res_hits / len(shot_paths)
        chrome_kw = [
            "DevTools", "Elements", "Console", "Network", "Sources",
            "Application", "Storage", "Cookies", "Local Storage", "Session Storage",
            "Headers", "Preview", "Response", "Payload", "Initiator", "Authorization",
            "http://", "https://", "localhost", "127.0.0.1", "code=", "state=",
        ]
        chrome_hits = 0
        if pytesseract:
            for p in shot_paths:
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if sum(1 for k in chrome_kw if k.lower() in tx.lower()) >= 2:
                        chrome_hits += 1
                except Exception:
                    pass
            chrome_score = chrome_hits / len(shot_paths)
        else:
            chrome_score = 0.4
        coverage = min(1.0, len(shot_paths) / 5.0)
        gui_signal = (uniq_score * 0.35 + res_score * 0.30 + chrome_score * 0.35) * coverage
    s["gui_real_interaction"] = round(gui_signal, 3)

    # --- Weighted aggregation: core 60% / gui 30% / aux 10% ---
    def _avg(keys):
        vs = [s.get(k, 0.0) for k in keys if isinstance(s.get(k), (int, float))]
        return sum(vs) / len(vs) if vs else 0.0

    core_keys = ["token_decoded", "token_audit_schema", "lifetime_correct",
                 "fixed_exists", "fix_quality", "verification_json",
                 "audit_report", "cors_test"]
    gui_keys = ["consent_shots_present", "devtools_token_present",
                "cors_error_shot", "fixed_token_shot", "gui_real_interaction"]
    aux_keys = ["consent_shots_ocr", "devtools_token_ocr", "cors_error_ocr",
                "vlm_consent_real", "vlm_devtools_real", "vlm_token_visible"]
    core = _avg(core_keys)
    gui = _avg(gui_keys)
    aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux

    # Multi-tier hard gates
    if s.get("gui_real_interaction", 0) < 0.6:
        base = min(base, 0.4)
    if s.get("gui_real_interaction", 0) < 0.4:
        base = min(base, 0.30)
    if s.get("consent_shots_present", 0) < 0.5:
        base = min(base, 0.4)
    if s.get("token_decoded", 0) == 0:
        base = min(base, 0.35)
    if s.get("fixed_exists", 0) == 0:
        base = min(base, 0.4)
    if s.get("fix_quality", 0) < 1.0:
        base = min(base, 0.55)
    if s.get("cors_test", 0) == 0:
        base = min(base, 0.45)
    if s.get("verification_json", 0) < 1.0:
        base = min(base, 0.6)
    # VLM unavailable cap
    if s.get("judge_method", "failed") == "failed":
        base = min(base, 0.6)
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
