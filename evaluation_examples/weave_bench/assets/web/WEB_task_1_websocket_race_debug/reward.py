# Auto-generated from WeaveBench task WEB_task_1_websocket_race_debug.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """WebSocket race condition debug grader: file checks + schema + OCR + VLM."""
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

    # Hard gate: empty workspace → 0
    if not rd.exists() or not any(rd.iterdir()):
        s["overall_score"] = 0.000
        return s

    # --- helper ---
    def ocr_check(fpath, keywords):
        if not fpath.exists():
            return 0.0, False
        present = 1.0
        ocr_hit = False
        if pytesseract:
            try:
                tx = pytesseract.image_to_string(Image.open(fpath))
                if any(k.lower() in tx.lower() for k in keywords):
                    ocr_hit = True
            except Exception:
                pass
        return present, ocr_hit

    # 1. Chat connected screenshot
    p1, o1 = ocr_check(rd / "view_chat_connected.png",
                        ["Connected", "WS Chat", "Chat", "Send"])
    s["chat_connected_present"] = p1
    s["chat_connected_ocr"] = 1.0 if o1 else 0.0

    # 2. DevTools WS headers screenshot
    p2, o2 = ocr_check(rd / "view_devtools_ws_headers.png",
                        ["Upgrade", "websocket", "101", "Sec-WebSocket"])
    s["ws_headers_present"] = p2
    s["ws_headers_ocr"] = 1.0 if o2 else 0.0

    # 3. DevTools WS frames (before fix)
    p3, o3 = ocr_check(rd / "view_devtools_ws_frames.png",
                        ["msg_", "from", "text", "id"])
    s["ws_frames_present"] = p3
    s["ws_frames_ocr"] = 1.0 if o3 else 0.0

    # 4. Replay logs
    log_a = rd / "replay_client_a.log"
    log_b = rd / "replay_client_b.log"
    la_text = log_a.read_text(errors="ignore") if log_a.exists() else ""
    lb_text = log_b.read_text(errors="ignore") if log_b.exists() else ""
    la_lines = [l for l in la_text.strip().splitlines() if l.strip()]
    lb_lines = [l for l in lb_text.strip().splitlines() if l.strip()]
    s["replay_logs"] = 1.0 if (len(la_lines) >= 5 and len(lb_lines) >= 5) else (
        0.5 if (la_text and lb_text) else 0.0)

    # 5. message_order_analysis.json
    moa = rd / "message_order_analysis.json"
    moa_data = {}
    if moa.exists():
        try:
            moa_data = json.loads(moa.read_text())
        except Exception:
            pass
    has_total = moa_data.get("total_sent") == 10
    has_missing = "missing" in str(moa_data).lower() or "client_a_missing" in moa_data
    has_order = "out_of_order" in str(moa_data).lower() or "client_a_out_of_order" in moa_data
    s["order_analysis"] = 1.0 if (has_total and has_missing and has_order) else (
        0.5 if moa_data else 0.0)

    # 6. server_race_evidence.txt
    sre = rd / "server_race_evidence.txt"
    sre_text = sre.read_text(errors="ignore") if sre.exists() else ""
    s["race_evidence"] = 1.0 if (
        len(sre_text) > 20 and any(k in sre_text.lower() for k in [
            "race", "send failed", "error", "condition"])
    ) else 0.0

    # 7. server_fixed.js
    fixed = workspace / "ws_chat/server_fixed.js"
    s["fixed_exists"] = 1.0 if fixed.exists() else 0.0
    if fixed.exists():
        code = fixed.read_text(errors="ignore")
        has_snapshot = any(k in code for k in [
            "Array.from", "[...clients]", "spread", "slice"])
        has_ready = "readyState" in code or "OPEN" in code
        no_random_delay = "Math.random()" not in code
        s["fix_quality"] = 1.0 if (has_snapshot and has_ready and no_random_delay) else (
            0.5 if (has_snapshot or has_ready) else 0.0)
    else:
        s["fix_quality"] = 0.0

    # 8. before_after_comparison.json
    bac = rd / "before_after_comparison.json"
    bac_data = {}
    if bac.exists():
        try:
            bac_data = json.loads(bac.read_text())
        except Exception:
            pass
    after = bac_data.get("after", {})
    before = bac_data.get("before", {})
    after_ok = after.get("missing") == 0 and after.get("out_of_order") == 0
    before_has = "total_sent" in str(before)
    s["before_after"] = 1.0 if (after_ok and before_has) else (
        0.5 if bac_data else 0.0)

    # 9. Fixed frames screenshot
    p9, _ = ocr_check(rd / "view_devtools_ws_frames_fixed.png", ["msg_", "id", "from"])
    s["fixed_frames_present"] = p9

    # 10. Console perf screenshot
    p10, o10 = ocr_check(rd / "view_devtools_console_ws_perf.png",
                          ["performance", "measure", "duration", "mark"])
    s["perf_console_present"] = p10
    s["perf_console_ocr"] = 1.0 if o10 else 0.0

    # 11. VLM judge
    all_shots = [str(rd / n) for n in [
        "view_chat_connected.png",
        "view_devtools_ws_headers.png",
        "view_devtools_ws_frames.png",
        "view_devtools_ws_frames_fixed.png",
    ] if (rd / n).exists()]
    if vlm_score_rubric and all_shots:
        rubric = {
            "vlm_ws_frames_real": "截图显示真实的 Chrome DevTools WebSocket Messages 面板，含帧列表",
            "vlm_chat_ui_real": "截图显示真实的 WebSocket 聊天页面，含消息列表和输入框",
            "vlm_order_evidence": "截图中能看到消息 id 乱序或修复后有序的证据",
        }
        vlm = vlm_score_rubric(all_shots[:4], rubric,
            instruction="评估 WebSocket 竞态调试截图的真实性和完整性。")
        for k in rubric:
            s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")

    # --- GUI hard-gate sub-score: 真实浏览器交互信号 ---
    import hashlib
    trajectory_shots = [
        "view_chat_connected.png",
        "view_devtools_ws_headers.png",
        "view_devtools_ws_frames.png",
        "view_devtools_ws_frames_fixed.png",
        "view_devtools_console_ws_perf.png",
    ]
    shot_paths = [rd / n for n in trajectory_shots if (rd / n).exists()]
    gui_signal = 0.0
    if len(shot_paths) >= 3:
        # (a) 多帧像素不重复
        hashes = {hashlib.md5(p.read_bytes()).hexdigest() for p in shot_paths}
        uniq_ratio = len(hashes) / len(shot_paths)
        uniq_score = 1.0 if uniq_ratio >= 0.8 else uniq_ratio
        # (b) 分辨率符合真实屏幕（headless 截图通常是固定的小尺寸或元素 crop）
        common_res = {(1920, 1080), (1366, 768), (1440, 900), (1536, 864),
                      (1680, 1050), (1280, 800), (1280, 720), (2560, 1440),
                      (1600, 900), (1920, 1200)}
        res_hits = 0
        try:
            for p in shot_paths:
                with Image.open(p) as im:
                    w, h = im.size
                if (w, h) in common_res or (w >= 1200 and h >= 700 and 1.2 <= w / h <= 2.4):
                    res_hits += 1
        except Exception:
            pass
        res_score = res_hits / len(shot_paths)
        # (c) 浏览器 chrome 元素 OCR（DevTools tab 名 / 地址栏 URL / 协议）
        chrome_kw = [
            "DevTools", "Elements", "Console", "Network", "Sources",
            "Application", "Performance", "Memory", "Headers", "Messages",
            "Frames", "Preview", "Response", "Initiator", "Timing",
            "http://", "https://", "localhost", "ws://", "127.0.0.1",
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
            chrome_score = 0.5
        gui_signal = uniq_score * 0.4 + res_score * 0.3 + chrome_score * 0.3
    s["gui_real_interaction"] = round(gui_signal, 3)

    # Overall with hard gates
    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums) / max(1, len(nums))
    # Hard gate: 没有真实 GUI 信号则封顶（防止纯 CLI + headless 截图通关）
    if s.get("gui_real_interaction", 0) < 0.6:
        base = min(base, 0.35)
    if s.get("gui_real_interaction", 0) < 0.4:
        base = min(base, 0.25)
    if s.get("chat_connected_present", 0) < 0.5 or s.get("chat_connected_ocr", 0) < 0.5:
        base = min(base, 0.4)
    if s.get("fixed_exists", 0) == 0 or s.get("fix_quality", 0) < 0.5:
        base = min(base, 0.4)
    if s.get("replay_logs", 0) < 1.0:
        base = min(base, 0.45)
    if s.get("order_analysis", 0) < 1.0:
        base = min(base, 0.5)
    if s.get("before_after", 0) < 1.0:
        base = min(base, 0.5)
    # VLM 不可用退化封顶
    if s.get("judge_method", "") == "failed":
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
