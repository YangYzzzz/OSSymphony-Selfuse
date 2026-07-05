# Auto-generated from WeaveBench task WEB_task_16_webrtc_simulcast_layer_audit.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """WebRTC simulcast layer audit grader.

    8-15 sub-scores + 3 hard gates.
    GT lives at root-only /opt/web16_gt/expected.json (warmup moves it
    off the agent-visible /tmp_workspace/gt to prevent answer leakage).
    """
    import json, os, subprocess
    from pathlib import Path

    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/opt/web16_gt") if Path("/opt/web16_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    s = {}

    expected = {}
    try:
        expected = json.loads((gt_dir / "expected.json").read_text())
    except Exception:
        expected = {}

    # ---------- 1. report file exists & schema ----------
    rep_path = rd / "simulcast_report.json"
    rep = {}
    s["report_exists"] = 1.0 if rep_path.exists() else 0.0
    if rep_path.exists():
        try:
            rep = json.loads(rep_path.read_text())
        except Exception:
            rep = {}
    schema_keys = {"session_duration_sec", "layers", "degrade_window",
                   "effective_video_bitrate_bps_during_degrade",
                   "verdict_one_line"}
    s["report_schema"] = 1.0 if (
        isinstance(rep, dict) and schema_keys.issubset(rep.keys())
        and isinstance(rep.get("layers"), list)
        and len(rep.get("layers", [])) == 3
    ) else 0.0

    # ---------- 2. SSRC values match GT ----------
    gt_ssrcs = expected.get("ssrcs", {})  # {"f": int, "h": int, "q": int}
    got_ssrcs = {}
    for layer in rep.get("layers", []):
        if isinstance(layer, dict) and "rid" in layer and "ssrc" in layer:
            try:
                got_ssrcs[layer["rid"]] = int(layer["ssrc"])
            except Exception:
                pass
    ssrc_hits = sum(
        1 for k in ("f", "h", "q")
        if k in gt_ssrcs and got_ssrcs.get(k) == gt_ssrcs[k]
    )
    s["ssrc_match"] = ssrc_hits / 3.0 if gt_ssrcs else 0.0

    # ---------- 3. ssrc_to_rid.json mapping correct ----------
    map_path = rd / "ssrc_to_rid.json"
    map_ok = 0
    if map_path.exists():
        try:
            mp = json.loads(map_path.read_text())
            for k in ("f", "h", "q"):
                entry = mp.get(k, {})
                if (isinstance(entry, dict)
                        and int(entry.get("ssrc", -1)) == gt_ssrcs.get(k, -2)
                        and int(entry.get("packets", 0)) > 0):
                    map_ok += 1
        except Exception:
            pass
    s["ssrc_rid_mapping"] = map_ok / 3.0

    # ---------- 4. degrade window timing ----------
    dw = rep.get("degrade_window", {}) if isinstance(rep, dict) else {}
    dw_path = rd / "degrade_window.json"
    if dw_path.exists() and not dw:
        try:
            dw = json.loads(dw_path.read_text())
        except Exception:
            dw = {}
    gt_start = expected.get("f_paused_start_sec")
    gt_end = expected.get("f_paused_end_sec")
    timing_hits = 0
    try:
        if gt_start is not None and abs(float(dw.get("f_paused_start_sec", 1e9)) - float(gt_start)) <= 1.5:
            timing_hits += 1
        if gt_end is not None and abs(float(dw.get("f_paused_end_sec", 1e9)) - float(gt_end)) <= 1.5:
            timing_hits += 1
    except Exception:
        pass
    s["degrade_window_timing"] = timing_hits / 2.0

    # ---------- 5. min BWE ----------
    gt_bwe = expected.get("min_bwe_bps")
    bwe_ok = 0.0
    try:
        got_bwe = float(dw.get("min_bwe_bps", 0))
        if gt_bwe and abs(got_bwe - float(gt_bwe)) <= 0.08 * float(gt_bwe):
            bwe_ok = 1.0
    except Exception:
        pass
    s["min_bwe_value"] = bwe_ok

    # ---------- 6. degrade reasons include 'bandwidth' ----------
    reasons = dw.get("reasons", []) if isinstance(dw, dict) else []
    s["degrade_reason_bandwidth"] = 1.0 if (
        isinstance(reasons, list) and "bandwidth" in [str(x).lower() for x in reasons]
    ) else 0.0

    # ---------- 7. CLI evidence: jq + tshark outputs ----------
    jq_path = rd / "jq_outbound_summary.json"
    cli_jq = 0.0
    if jq_path.exists() and jq_path.stat().st_size > 50:
        try:
            arr = json.loads(jq_path.read_text())
            if isinstance(arr, list) and len(arr) == 3 and all(
                isinstance(x, dict) and "ssrc" in x and "rid" in x for x in arr
            ):
                cli_jq = 1.0
        except Exception:
            cli_jq = 0.5
    s["cli_jq_summary"] = cli_jq

    tsh_path = rd / "tshark_ssrc_packets.txt"
    cli_tsh = 0.0
    if tsh_path.exists() and tsh_path.stat().st_size > 20:
        try:
            txt = tsh_path.read_text().lower()
            hit = sum(1 for v in gt_ssrcs.values()
                      if str(v) in txt or hex(v) in txt or hex(v)[2:] in txt)
            cli_tsh = hit / 3.0
        except Exception:
            pass
    s["cli_tshark_packets"] = cli_tsh
    has_cli_evidence = (cli_jq > 0 and cli_tsh > 0)

    # ---------- 8. GUI screenshots existence ----------
    gui_shots = [
        "view_internals_outbound_three_layers.png",
        "view_internals_hover_45s.png",
        "view_wireshark_rtp_streams.png",
        "view_wireshark_stream_analysis.png",
        "view_internals_f_layer_drop.png",
        "view_internals_quality_limitation.png",
        "view_devtools_media_panel.png",
    ]
    gui_present = sum(1 for n in gui_shots if (rd / n).exists()
                      and (rd / n).stat().st_size > 1024)
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui_screenshot = gui_present >= 6

    # ---------- 9. OCR keywords on screenshots ----------
    ocr_score = 0.5
    try:
        import pytesseract
        from PIL import Image
        ocr_kws = {
            "view_internals_outbound_three_layers.png":
                ["bytesSent", "RTCOutbound", "rid", "Outbound"],
            "view_wireshark_rtp_streams.png":
                ["RTP Streams", "Src port", "Packets", "SSRC"],
            "view_wireshark_stream_analysis.png":
                ["Max Delta", "Mean Jitter", "Lost", "Analysis"],
            "view_internals_quality_limitation.png":
                ["qualityLimitation", "bandwidth", "cpu"],
            "view_devtools_media_panel.png":
                ["Properties", "Events", "Messages", "Player"],
        }
        hits = total = 0
        for fname, kws in ocr_kws.items():
            p = rd / fname
            if not p.exists():
                continue
            total += 1
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k.lower() in tx.lower() for k in kws):
                    hits += 1
            except Exception:
                pass
        if total:
            ocr_score = hits / total
    except ImportError:
        ocr_score = 0.0
    s["gui_screenshots_ocr"] = ocr_score

    # ---------- 10. PDF + insights ----------
    pdf = rd / "simulcast_report.pdf"
    s["pdf_exists"] = 1.0 if pdf.exists() and pdf.stat().st_size > 1024 else 0.0
    pages = 0; first_text = ""; full_text = ""
    if pdf.exists():
        try:
            out = subprocess.run(
                ["pdftotext", "-f", "1", "-l", "1", str(pdf), "-"],
                capture_output=True, text=True, timeout=30,
            )
            first_text = out.stdout
            full = subprocess.run(
                ["pdftotext", str(pdf), "-"],
                capture_output=True, text=True, timeout=30,
            )
            full_text = full.stdout
            info = subprocess.run(
                ["pdfinfo", str(pdf)],
                capture_output=True, text=True, timeout=10,
            ).stdout
            for ln in info.splitlines():
                if ln.lower().startswith("pages:"):
                    pages = int(ln.split(":", 1)[1].strip())
        except Exception:
            pass
    s["pdf_pages"] = 1.0 if pages >= 2 else (pages / 2.0 if pages else 0.0)
    KW = ("bandwidth", "720p", "SSRC", "bitrate", "kbps",
          "qualityLimitation", "BWE", "rid", "simulcast")
    bullets = [ln for ln in first_text.splitlines()
               if ln.strip() and len(ln.strip()) >= 25
               and sum(k.lower() in ln.lower() for k in KW) >= 2]
    s["pdf_insights"] = 1.0 if len(bullets) >= 5 else len(bullets) / 5.0
    s["pdf_title_present"] = 1.0 if (
        ("Simulcast" in first_text or "simulcast" in first_text.lower())
        and ("降级" in first_text) and ("取证" in first_text)
    ) else 0.0

    # ---------- 11. Verdict text quality ----------
    import re
    v = str(rep.get("verdict_one_line", ""))
    has_num = bool(re.search(r"\d{2,}", v))
    has_720 = ("720" in v) or ("f" in v.split())
    has_bw  = ("带宽" in v) or ("bandwidth" in v.lower()) or ("BWE" in v)
    s["verdict_one_line"] = 1.0 if (len(v) >= 40 and has_num and has_720 and has_bw) else 0.0

    # ---------- 12. Manifest sanity ----------
    mf = rd / "_manifest.txt"
    s["manifest_present"] = 1.0 if (mf.exists() and mf.stat().st_size > 100) else 0.0

    # ---------- VLM rubric ----------
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_judge = 1.0
    if vlm_score_rubric:
        imgs = [str(rd / n) for n in gui_shots if (rd / n).exists()][:3]
        if imgs:
            rubric = {
                "vlm_three_layers_visible":
                    "截图里能看到 3 条独立的 simulcast layer 时间序列曲线",
                "vlm_drop_window_visible":
                    "截图里能看到 f 层(720p)的 bytesSent 出现明显的平台/暂停段",
                "vlm_wireshark_rtp_panel":
                    "截图里能看到 Wireshark RTP Streams 面板,列出 ≥3 行 SSRC 流",
                "vlm_layout_clean":
                    "整体截图没有遮挡、没有截断、布局可读",
            }
            try:
                vlm = vlm_score_rubric(
                    imgs, rubric,
                    instruction="评估 WebRTC simulcast 取证截图的质量。",
                )
                for k in rubric:
                    s[k] = vlm.get(k, 0.0)
                vlm_judge = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
            except Exception:
                pass

    nums = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(nums) / len(nums) if nums else 0.0

    # ---------- Hard gates ----------
    if not has_cli_evidence:
        base = min(base, 0.40)
    # GUI-path scoring axis removed: missing screenshots already cost
    # gui_screenshots_count / gui_screenshots_ocr / 4 vlm_* sub-scores.
    if vlm_judge < 0.60:
        base = min(base, 0.60)
    if s.get("ssrc_match", 0) < 0.34:
        base = min(base, 0.50)
    if s.get("degrade_window_timing", 0) < 1.0:
        base = min(base, 0.50)
    if s.get("gui_screenshots_ocr", 0) < 0.6:
        base = min(base, 0.50)

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
