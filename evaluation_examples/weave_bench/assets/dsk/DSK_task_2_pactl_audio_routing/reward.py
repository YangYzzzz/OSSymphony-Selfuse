# Auto-generated from WeaveBench task DSK_task_2_pactl_audio_routing.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """DSK_task_2 grader v2. Empty → 0.000.
    Weighted: core 0.6 / gui 0.3 / aux 0.1. Multi-tier hard gates + anti-cheat.
    """
    import json, re, os, struct, hashlib
    from pathlib import Path
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd = workspace / "results"
    s = {}

    # 1. CLI artifacts
    cli_files = ["baseline.txt","verify_topology.txt","cleanup_verify.txt","loaded_modules.txt","freq_analysis.txt"]
    cli_present = sum(1 for f in cli_files if (rd / f).exists())
    s["cli_artifacts"] = cli_present / len(cli_files)
    has_cli = cli_present >= 3

    # 2. loaded_modules.txt has >= 8 module-ids
    mods_score = 0.0
    mf = rd / "loaded_modules.txt"
    if mf.exists():
        try:
            txt = mf.read_text()
            ids = re.findall(r"\b\d+\b", txt)
            if len(ids) >= 8: mods_score = 1.0
            elif len(ids) >= 4: mods_score = 0.5
        except Exception: pass
    s["loaded_modules"] = mods_score

    # 3. GUI screenshots — must exist + non-trivial size + md5 uniqueness
    gui_shots = ["view_pavucontrol_output.png","view_pavucontrol_input.png","view_pavucontrol_recording.png",
                 "view_pavucontrol_playback.png","view_pavucontrol_config.png","view_pavucontrol_meter.png"]
    gui_present = sum(1 for n in gui_shots if (rd / n).exists())
    s["gui_screenshots_count"] = gui_present / len(gui_shots)
    has_gui = gui_present >= 4

    # 3a. anti-cheat: each shot >= 20KB and not trivially small placeholder
    big_shots = 0
    md5s = set()
    for n in gui_shots:
        p = rd / n
        if p.exists() and p.stat().st_size >= 20 * 1024:
            big_shots += 1
            try:
                md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
            except Exception: pass
    s["gui_screenshots_size"] = big_shots / len(gui_shots)
    # 3b. md5 uniqueness — penalise duplicate / copy-paste screenshots
    s["gui_screenshots_unique"] = (len(md5s) / len(gui_shots)) if gui_present else 0.0

    try:
        import pytesseract
        from PIL import Image
        kws_any = ["Output","Input","Recording","Playback","Devices","virtual","monitor","Volume","Mute","Configuration"]
        ocr_hits = 0
        ocr_available = True
        for n in gui_shots:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k in tx for k in kws_any): ocr_hits += 1
                except Exception: pass
        s["gui_screenshots_ocr"] = ocr_hits / len(gui_shots)
    except Exception:
        ocr_available = False
        s["gui_screenshots_ocr"] = 0.3 if gui_present > 0 else 0.0

    # 4. wav files
    wav_score = 0.0
    wav_files = ["captured_monitor.wav","captured_recording.wav"]
    ok_wav = 0
    for n in wav_files:
        p = rd / n
        if p.exists() and p.stat().st_size > 1024:
            ok_wav += 1
    wav_score = ok_wav / len(wav_files)
    s["wav_recorded"] = wav_score

    # 5. freq_analysis 440Hz peak — must show measured peak near 440Hz
    freq_score = 0.0
    fa = rd / "freq_analysis.txt"
    if fa.exists():
        try:
            txt = fa.read_text()
            # Strong: an explicit measured peak in 420-460 paired with "peak"/"Hz" wording
            strong = False
            for m in re.finditer(r"(\d{3}(?:\.\d+)?)\s*[Hh]z", txt):
                try:
                    v = float(m.group(1))
                    if 420.0 <= v <= 460.0:
                        strong = True; break
                except Exception: pass
            has_peak_word = bool(re.search(r"peak|maximum|fundamental", txt, re.I))
            both_files = bool(re.search(r"captured_monitor", txt)) and bool(re.search(r"captured_recording", txt))
            if strong and has_peak_word and both_files:
                freq_score = 1.0
            elif strong and has_peak_word:
                freq_score = 0.7
            elif strong or re.search(r"4[34]\d.*[Hh]z|peak.*4\d\d|440\s*[±+\-]?\s*\d+", txt):
                freq_score = 0.5
            elif "440" in txt:
                freq_score = 0.25
        except Exception: pass
    s["freq_440_peak"] = freq_score

    # 6. cleanup verify (positive match: evidence of removal/unload)
    cv_score = 0.0
    cv = rd / "cleanup_verify.txt"
    if cv.exists():
        try:
            txt = cv.read_text()
            low = txt.lower()
            strong = bool(
                re.search(r"\b0\s+(virtual\s+)?sinks?\b", low)
                or re.search(r"all\s+virtual\s+sinks?\s+(unloaded|removed|cleaned)", low)
                or re.search(r"virtual\s+sinks?\s*[:=]\s*0\b", low)
                or re.search(r"no\s+(remaining\s+)?(virtual|null-sink)", low)
            )
            weak = bool(re.search(r"\b(unload|remov|cleaned|cleanup)", low))
            if strong:
                cv_score = 1.0
            elif weak:
                cv_score = 0.5
        except Exception: pass
    s["cleanup_complete"] = cv_score

    # 7. routing_report.md — 4 paragraphs each ≥80 chars + must mention required topics
    rp_score = 0.0
    rp = rd / "routing_report.md"
    if rp.exists():
        try:
            txt = rp.read_text()
            parags = [p for p in re.split(r"\n\s*\n", txt) if len(p.strip()) >= 80]
            base_rp = min(1.0, len(parags) / 4)
            low = txt.lower()
            topics = sum(1 for kw in ("topology","440","clean","loopback","latency","sample","monitor") if kw in low)
            topic_factor = min(1.0, topics / 5)
            rp_score = round(0.6 * base_rp + 0.4 * topic_factor, 4)
        except Exception: pass
    s["routing_report"] = rp_score

    # 8. VLM rubric
    vlm_available = False
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    if vlm_score_rubric and (rd / "view_pavucontrol_output.png").exists():
        vlm_available = True
        rubric = {
            "vlm_pavucontrol_layout": "pavucontrol GUI 界面整齐,顶部有标签栏",
            "vlm_virtual_sinks_visible": "Output Devices 标签里能看到 virtual sink",
            "vlm_volume_sliders": "音量滑块可见且不在最低位",
            "vlm_meter_active": "playback meter 截图能看到信号活动",
        }
        try:
            imgs = [str(rd / "view_pavucontrol_output.png")]
            for n in ("view_pavucontrol_playback.png","view_pavucontrol_meter.png"):
                if (rd / n).exists(): imgs.append(str(rd / n))
            vlm = vlm_score_rubric(imgs, rubric, instruction="评估 pavucontrol GUI 截图。")
            for k in rubric: s[k] = float(vlm.get(k, 0.0))
        except Exception:
            for k in rubric: s[k] = 0.0
    else:
        for k in ["vlm_pavucontrol_layout","vlm_virtual_sinks_visible","vlm_volume_sliders","vlm_meter_active"]:
            s[k] = 0.0

    # 9. Content-reality sub-scores
    # 9a. baseline.txt lists >= 2 sinks (real pactl baseline)
    bp = rd / "baseline.txt"
    if bp.exists():
        try:
            btxt = bp.read_text()
            sinks = re.findall(r"(?m)^\s*Sink\s+#\d+|name:\s*<", btxt)
            if len(sinks) >= 2:
                s["baseline_sinks"] = 1.0
            elif len(sinks) >= 1:
                s["baseline_sinks"] = 0.5
            else:
                s["baseline_sinks"] = 0.0
        except Exception:
            s["baseline_sinks"] = 0.0
    else:
        s["baseline_sinks"] = 0.0

    # 9b. (removed) default_sink_set — Prompt 未要求 set-default-sink，避免误伤

    # 9c. captured wav substantial (> 16KB each) and proper RIFF/WAVE header
    big_wav = 0
    valid_wav = 0
    for n in wav_files:
        p = rd / n
        if p.exists() and p.stat().st_size > 16 * 1024:
            big_wav += 1
            try:
                with open(p, "rb") as fh:
                    head = fh.read(12)
                if head[:4] == b"RIFF" and head[8:12] == b"WAVE":
                    valid_wav += 1
            except Exception: pass
    s["wav_substantial"] = big_wav / len(wav_files)
    s["wav_valid_riff"] = valid_wav / len(wav_files)

    # ---- weighted aggregation ----
    core_keys = ("cli_artifacts","loaded_modules","wav_recorded","wav_substantial",
                 "wav_valid_riff","freq_440_peak","cleanup_complete","baseline_sinks")
    gui_keys  = ("gui_screenshots_count","gui_screenshots_size","gui_screenshots_unique",
                 "gui_screenshots_ocr","vlm_pavucontrol_layout","vlm_virtual_sinks_visible",
                 "vlm_volume_sliders","vlm_meter_active")
    aux_keys  = ("routing_report",)
    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k], (int, float))]
        return (sum(vals) / len(vals)) if vals else 0.0
    core = _avg(core_keys); gui = _avg(gui_keys); aux = _avg(aux_keys)
    base = 0.6 * core + 0.3 * gui + 0.1 * aux
    s["_core"] = round(core, 4); s["_gui"] = round(gui, 4); s["_aux"] = round(aux, 4)

    # hard gates — multi-tier
    if not has_cli: base = min(base, 0.25)
    if not has_gui: base = min(base, 0.25)
    if s["loaded_modules"] < 0.5: base = min(base, 0.40)
    if s["wav_recorded"] < 0.5: base = min(base, 0.45)
    if s["wav_valid_riff"] < 0.5: base = min(base, 0.50)
    if s["freq_440_peak"] < 0.5: base = min(base, 0.55)
    if s["freq_440_peak"] < 0.25: base = min(base, 0.40)
    if s["cleanup_complete"] < 0.5: base = min(base, 0.55)
    if s["baseline_sinks"] < 0.5: base = min(base, 0.40)
    if s["wav_substantial"] < 0.5: base = min(base, 0.50)
    if s["gui_screenshots_size"] < 0.5: base = min(base, 0.50)
    if s["gui_screenshots_unique"] < 0.7: base = min(base, 0.55)
    if s["gui_screenshots_ocr"] < 0.4: base = min(base, 0.60)
    # When VLM unavailable, cap at 0.6 so headless runs cannot achieve top score
    if not vlm_available: base = min(base, 0.60)

    s["overall_score"] = round(base, 4)
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
