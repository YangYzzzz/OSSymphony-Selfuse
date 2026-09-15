# Auto-generated from WeaveBench task WEB_task_3_har_replay_mock.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """HAR analysis + Chrome Network panel + jq/sed mock grader (v2 hardened)."""
    import json, re
    from pathlib import Path
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        pytesseract = None
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    gt = workspace / "gt"
    s = {}

    # 1. all_requests.json — 严格校验 url/method/status/time_ms/size_bytes 类型
    ar = rd / "all_requests.json"
    if ar.exists():
        try:
            data = json.loads(ar.read_text())
            required_keys = {"url", "method", "status", "time_ms", "size_bytes"}
            valid = []
            for e in data:
                if not (isinstance(e, dict) and required_keys <= set(e.keys())):
                    continue
                if not isinstance(e.get("url"), str) or not e["url"].startswith("http"):
                    continue
                if not isinstance(e.get("time_ms"), (int, float)):
                    continue
                if not isinstance(e.get("size_bytes"), (int, float)):
                    continue
                valid.append(e)
            s["all_requests_count"] = 1.0 if len(valid) >= 15 else len(valid) / 15.0
        except Exception:
            s["all_requests_count"] = 0.0
    else:
        s["all_requests_count"] = 0.0

    # 2. bottleneck_top3.json — 必须严格降序 + 第一条 > 4500ms + 含 diagnosis
    bt = rd / "bottleneck_top3.json"
    if bt.exists():
        try:
            top3 = json.loads(bt.read_text())
            sorted_ok = len(top3) == 3 and all(isinstance(e, dict) and "time_ms" in e for e in top3)
            descending = sorted_ok and top3[0]["time_ms"] > top3[1]["time_ms"] > top3[2]["time_ms"]
            first_slow = sorted_ok and top3[0]["time_ms"] > 4500
            has_diag = sorted_ok and all(isinstance(e.get("diagnosis"), str) and len(e.get("diagnosis", "")) >= 5 for e in top3)
            ok = sorted_ok and descending and first_slow and has_diag
            s["bottleneck_structure"] = 1.0 if ok else (0.4 if sorted_ok else 0.0)
        except Exception:
            s["bottleneck_structure"] = 0.0
    else:
        s["bottleneck_structure"] = 0.0

    # 3-4. GUI screenshots OCR
    shot_kws = {
        "view_har_waterfall.png": ["Network", "Waterfall", "Time", "Name", "Status"],
        "view_har_slow_request.png": ["Timing", "Waiting", "TTFB", "Content Download", "Request"],
        "view_fixed_waterfall.png": ["Network", "Waterfall", "Name"],
        "view_comparison_side.png": ["Network", "Waterfall"],
        "view_throttled_waterfall.png": ["Custom", "Throttl", "Network", "Slow"],
    }
    shots_present = 0
    ocr_hits = 0
    MIN_SHOT_BYTES = 5 * 1024  # 占位图过滤
    for name, kws_list in shot_kws.items():
        p = rd / name
        if p.exists() and p.stat().st_size >= MIN_SHOT_BYTES:
            shots_present += 1
            if pytesseract:
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    # 至少命中 2 个关键词才算 OCR hit
                    hits = sum(1 for k in kws_list if k.lower() in tx.lower())
                    if hits >= 2:
                        ocr_hits += 1
                except Exception:
                    pass
    s["gui_shots_present"] = shots_present / len(shot_kws)
    s["gui_shots_ocr"] = ocr_hits / len(shot_kws) if pytesseract else 0.4

    # 5. timing_breakdown.json
    tb = rd / "timing_breakdown.json"
    if tb.exists():
        try:
            tbd = json.loads(tb.read_text())
            has_ttfb = isinstance(tbd.get("ttfb_ms"), (int, float)) and tbd["ttfb_ms"] > 1000
            s["timing_breakdown"] = 1.0 if has_ttfb else 0.3
        except Exception:
            s["timing_breakdown"] = 0.0
    else:
        s["timing_breakdown"] = 0.0

    # 6. fixed_checkout.har validity + bottleneck reduced + wait phase reduced
    fh = rd / "fixed_checkout.har"
    if fh.exists():
        try:
            har_data = json.loads(fh.read_text())
            entries = har_data.get("log", {}).get("entries", [])
            max_time = max((e.get("time", 0) for e in entries), default=0)
            max_wait = 0
            for e in entries:
                t = e.get("timings", {}) or {}
                w = t.get("wait", 0)
                if isinstance(w, (int, float)) and w > max_wait:
                    max_wait = w
            ok = len(entries) >= 15 and max_time < 300 and max_wait < 100
            s["fixed_har_valid"] = 1.0 if ok else (0.4 if len(entries) >= 15 else 0.0)
        except Exception:
            s["fixed_har_valid"] = 0.0
    else:
        s["fixed_har_valid"] = 0.0

    # 7. mock_validation.json — 必须 speedup_ratio > 15 + 字段齐全
    mv = rd / "mock_validation.json"
    if mv.exists():
        try:
            mvd = json.loads(mv.read_text())
            req = {"valid_json", "original_max_time_ms", "fixed_max_time_ms", "speedup_ratio", "total_entries", "modified_entries"}
            schema_ok = req <= set(mvd.keys()) and bool(mvd.get("valid_json"))
            try:
                ratio = float(mvd.get("speedup_ratio", 0))
            except Exception:
                ratio = 0
            if schema_ok and ratio > 15:
                s["mock_validation"] = 1.0
            elif schema_ok and ratio > 10:
                s["mock_validation"] = 0.6
            else:
                s["mock_validation"] = 0.2
        except Exception:
            s["mock_validation"] = 0.0
    else:
        s["mock_validation"] = 0.0

    # 9. live_latency.json — 需含 url/status/time_total_ms/time_ttfb_ms 全字段
    ll = rd / "live_latency.json"
    if ll.exists():
        try:
            lld = json.loads(ll.read_text())
            need = {"url", "status", "time_total_ms", "time_ttfb_ms"}
            valid = [e for e in lld if isinstance(e, dict) and need <= set(e.keys())
                     and isinstance(e.get("time_total_ms"), (int, float))
                     and "localhost" in str(e.get("url", "")) or "127.0.0.1" in str(e.get("url", ""))]
            uniq_urls = len({e.get("url") for e in valid})
            s["live_latency"] = 1.0 if (len(valid) >= 3 and uniq_urls >= 3) else len(valid) / 3.0 * 0.5
        except Exception:
            s["live_latency"] = 0.0
    else:
        s["live_latency"] = 0.0

    # 11. har_analysis_report.md
    rpt = rd / "har_analysis_report.md"
    if rpt.exists():
        txt = rpt.read_text(errors="ignore")
        s["report_length"] = 1.0 if len(txt) >= 200 else len(txt) / 200.0
        has_table = "|" in txt and "---" in txt
        s["report_table"] = 1.0 if has_table else 0.0
    else:
        s["report_length"] = 0.0
        s["report_table"] = 0.0

    # numeric agreement with gt/expected.json — 多项交叉校验
    if (gt / "expected.json").exists():
        try:
            exp = json.loads((gt / "expected.json").read_text())
            hits = 0
            total = 0
            if "bottleneck_url_contains" in exp and bt.exists():
                total += 1
                top3 = json.loads(bt.read_text())
                if top3 and exp["bottleneck_url_contains"] in top3[0].get("url", ""):
                    hits += 1
            if "total_entries" in exp and ar.exists():
                total += 1
                data = json.loads(ar.read_text())
                if abs(len(data) - exp["total_entries"]) <= 1:
                    hits += 1
            if "bottleneck_time_ms" in exp and bt.exists():
                total += 1
                top3 = json.loads(bt.read_text())
                if top3 and abs(top3[0].get("time_ms", 0) - exp["bottleneck_time_ms"]) <= 100:
                    hits += 1
            if "top3_urls" in exp and bt.exists():
                total += 1
                top3 = json.loads(bt.read_text())
                got_urls = [e.get("url", "") for e in top3]
                exp_urls = exp["top3_urls"]
                match = sum(1 for u in exp_urls if any(u in g or g in u for g in got_urls))
                if match >= 2:
                    hits += 1
            if "bottleneck_wait_ms" in exp:
                tb = rd / "timing_breakdown.json"
                if tb.exists():
                    total += 1
                    try:
                        tbd = json.loads(tb.read_text())
                        if abs(tbd.get("ttfb_ms", 0) - exp["bottleneck_wait_ms"]) <= 500:
                            hits += 1
                    except Exception:
                        pass
            s["numeric_agreement"] = hits / total if total else 0.0
        except Exception:
            s["numeric_agreement"] = 0.0
    else:
        s["numeric_agreement"] = 0.3

    # VLM judge
    if vlm_score_rubric:
        imgs = [str(rd / n) for n in shot_kws if (rd / n).exists()][:4]
        if imgs:
            rubric = {
                "vlm_devtools_real": "截图清晰显示 Chrome DevTools Network 面板（含 Waterfall 列彩色时序条）",
                "vlm_timing_panel": "至少一张截图显示请求的 Timing 细分面板（Stalled/DNS/SSL/Waiting）",
                "vlm_comparison": "能看到修复前后的瀑布图对比或节流效果",
            }
            vlm = vlm_score_rubric(imgs, rubric,
                instruction="评估 Chrome DevTools Network 面板 HAR 分析截图的真实性和信息完整度。")
            for k in rubric:
                s[k] = vlm.get(k, 0.0)
            s["judge_method"] = vlm.get("judge_method", "failed")

    # --- GUI hard-gate sub-score: 真实浏览器交互信号 ---
    import hashlib
    trajectory_shots = [
        "view_har_waterfall.png",
        "view_har_slow_request.png",
        "view_fixed_waterfall.png",
        "view_comparison_side.png",
        "view_throttled_waterfall.png",
    ]
    shot_paths = [rd / n for n in trajectory_shots if (rd / n).exists()]
    gui_signal = 0.0
    if len(shot_paths) >= 3:
        hashes = {hashlib.md5(p.read_bytes()).hexdigest() for p in shot_paths}
        uniq_ratio = len(hashes) / len(shot_paths)
        uniq_score = 1.0 if uniq_ratio >= 0.8 else uniq_ratio
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
        chrome_kw = [
            "DevTools", "Elements", "Console", "Network", "Sources",
            "Application", "Performance", "Headers", "Preview", "Response",
            "Initiator", "Timing", "Waterfall", "Throttling", "No throttling",
            "Slow 3G", "Fast 3G", "http://", "https://", "localhost", "127.0.0.1",
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

    # Aggregate — 加权：核心交付 55% / GUI 真实信号 30% / 辅助 15%
    def avg(keys, default=0.0):
        vs = [s[k] for k in keys if isinstance(s.get(k), (int, float))]
        return sum(vs) / len(vs) if vs else default

    core_keys = ["all_requests_count", "bottleneck_structure", "timing_breakdown",
                 "fixed_har_valid", "mock_validation", "numeric_agreement", "live_latency"]
    gui_keys = ["gui_shots_present", "gui_shots_ocr", "gui_real_interaction",
                "vlm_devtools_real", "vlm_timing_panel", "vlm_comparison"]
    aux_keys = ["report_length", "report_table"]

    core = avg(core_keys)
    gui = avg(gui_keys)
    aux = avg(aux_keys)
    base = 0.55 * core + 0.30 * gui + 0.15 * aux

    # Hard gates — 多层封顶，防退化路径
    # GUI 真实交互信号（截图唯一/分辨率/chrome OCR）
    gri = s.get("gui_real_interaction", 0)
    if gri < 0.7:
        base = min(base, 0.45)
    if gri < 0.5:
        base = min(base, 0.35)
    if gri < 0.3:
        base = min(base, 0.25)
    # 截图齐全度
    if s.get("gui_shots_present", 0) < 0.6:
        base = min(base, 0.4)
    if s.get("gui_shots_present", 0) < 0.4:
        base = min(base, 0.3)
    # 核心交付物：HAR 解析 / 瓶颈定位 / mock 修复
    if s.get("all_requests_count", 0) < 0.5:
        base = min(base, 0.4)
    if s.get("bottleneck_structure", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("timing_breakdown", 0) < 0.5:
        base = min(base, 0.5)
    if s.get("fixed_har_valid", 0) < 0.5:
        base = min(base, 0.45)
    if s.get("mock_validation", 0) < 0.5:
        base = min(base, 0.5)
    if s.get("numeric_agreement", 0) < 0.4:
        base = min(base, 0.55)
    # VLM 不可用时整体封顶 0.6（避免无 VLM 无成本通关）
    if s.get("judge_method") in (None, "failed", "fallback"):
        base = min(base, 0.6)

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
