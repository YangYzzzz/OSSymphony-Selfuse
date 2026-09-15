# Auto-generated from WeaveBench task SPA_task_12_verilator_gtkwave_uart_bug.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    import json, re, hashlib
    from pathlib import Path
    try:
        from PIL import Image
    except Exception:
        Image = None
    try:
        import pytesseract
    except Exception:
        pytesseract = None
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None

    rd = Path("/tmp_workspace/results")
    gt = Path("/tmp_workspace/gt")
    s = {}

    def jload(p):
        try: return json.loads(Path(p).read_text())
        except Exception: return {}

    truth = jload(gt / "expected.json")
    cli_evidence = False
    gui_evidence = False

    # 1. sim_build.log
    sb = rd / "sim_build.log"
    if sb.exists():
        txt = sb.read_text(errors="ignore")
        sim_done = txt.count("[sim] done")
        verilated = ("verilator" in txt.lower()) or ("Vuart_tx" in txt)
        s["sim_build_log"] = 1.0 if (sim_done >= 2 and verilated) else (0.5 if sim_done >= 1 else 0.0)
        if sim_done >= 1: cli_evidence = True
    else:
        s["sim_build_log"] = 0.0

    # 2. vcd_signals.txt
    vs = rd / "vcd_signals.txt"
    if vs.exists():
        t = vs.read_text(errors="ignore")
        hits = sum(1 for k in ["tx", "bit_idx", "state", "clk"] if re.search(r"\b" + k + r"\b", t))
        s["vcd_signals"] = hits / 4.0
        if hits >= 1: cli_evidence = True
    else:
        s["vcd_signals"] = 0.0

    # 3. observed_bits_buggy.json — gated on a real VCD with tx wire & ≥200 changes
    def _vcd_decode(p):
        try:
            txt = Path(p).read_text(errors="ignore")
            if "$timescale" not in txt or "$var" not in txt: return None
            if re.search(r"\$var\s+\w+\s+1\s+\S+\s+tx\b", txt) is None: return None
            if sum(1 for ln in txt.splitlines() if ln[:1] in "01") < 200: return None
            return True
        except Exception: return None
    vcd_b_ok = _vcd_decode(rd / "dump_buggy.vcd") is True
    vcd_f_ok = _vcd_decode(rd / "dump_fixed.vcd") is True
    ob_b = jload(rd / "observed_bits_buggy.json")
    sub = 0; tot = 4
    if isinstance(ob_b.get("byte_hex"), str) and ob_b["byte_hex"].lower().replace(" ", "") in ("0xaa", "aa", "0xAA".lower()):
        sub += 1
    if isinstance(ob_b.get("bits_lsb_first"), list) and ob_b["bits_lsb_first"] == [0,1,0,1,0,1,0,1]:
        sub += 1
    if isinstance(ob_b.get("stop_width_ns"), (int, float)) and 60 <= ob_b["stop_width_ns"] <= 100:
        sub += 1
    if isinstance(ob_b.get("frame_total_ns"), (int, float)) and 1480 <= ob_b["frame_total_ns"] <= 1560:
        sub += 1
    if not vcd_b_ok: sub = 0
    s["observed_bits_buggy"] = sub / tot
    if sub > 0: cli_evidence = True

    # 4-6 & 10-11 & 13. screenshots
    shots = [
        ("view_01_gtkwave_full.png", ["GTKWave", "Wave", "Signals", "uart"]),
        ("view_02_gtkwave_marker_pair.png", ["Marker", "A", "B"]),
        ("view_03_gtkwave_fixed.png", ["GTKWave", "Wave", "tx"]),
        ("view_04_gtkwave_zoom_stop.png", ["GTKWave", "ns", "Wave"]),
    ]
    present = sum(1 for n, _ in shots if (rd / n).exists())
    s["screenshots_present"] = present / len(shots)
    if present > 0: gui_evidence = True
    ocr_hits = 0
    if pytesseract and Image:
        for n, kws in shots:
            p = rd / n
            if p.exists():
                try:
                    tx_txt = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx_txt.lower() for k in kws):
                        ocr_hits += 1
                except Exception:
                    pass
        s["screenshots_ocr"] = ocr_hits / len(shots)
    else:
        s["screenshots_ocr"] = 0.5 if present > 0 else 0.0

    # 7. marker_readout.json
    mr = jload(rd / "marker_readout.json")
    ok_mr = 0
    if isinstance(mr.get("marker_A_ns"), (int, float)) and isinstance(mr.get("marker_B_ns"), (int, float)):
        if mr["marker_B_ns"] - mr["marker_A_ns"] >= 1000:  # ≥ ~6 bit-times spread
            ok_mr += 1
    centers = mr.get("data_bit_centers_ns", [])
    levels  = mr.get("data_bit_levels", [])
    if isinstance(centers, list) and isinstance(levels, list) and len(centers) == 8 and len(levels) == 8:
        ok_mr += 1
        # marker_readout MUST reflect the FIXED capture (0x55 → 1,0,1,0,1,0,1,0)
        if all(int(x) in (0, 1) for x in levels) and levels == [1,0,1,0,1,0,1,0]:
            ok_mr += 1
        # centers must be monotonically increasing and ~160 ns apart
        try:
            if all(140 <= centers[i+1] - centers[i] <= 180 for i in range(7)):
                ok_mr += 1
        except Exception:
            pass
    s["marker_readout"] = ok_mr / 4.0

    # 8-9. fix.diff
    fd = rd / "fix.diff"
    diff_ok = 0; diff_total = 5
    if fd.exists():
        ftxt = fd.read_text(errors="ignore")
        # only 2 hunk markers (@@) lines
        hunks = ftxt.count("\n@@")
        if 1 <= hunks <= 3: diff_ok += 1
        for tok in ["data_r[bit_idx]", "CLKS_PER_BIT-1"]:
            if tok.replace(" ", "") in ftxt.replace(" ", ""):
                diff_ok += 1
        for tok in ["data_r[7 - bit_idx]", "(CLKS_PER_BIT/2)-1"]:
            # must be on a removed line ('-' prefix)
            for line in ftxt.splitlines():
                if line.startswith("-") and tok.replace(" ", "") in line.replace(" ", ""):
                    diff_ok += 1; break
        if cli_evidence is False and ftxt.strip(): cli_evidence = True
    s["fix_diff"] = diff_ok / diff_total

    # 9 alt. observed_bits_fixed.json
    ob_f = jload(rd / "observed_bits_fixed.json")
    sub = 0; tot = 4
    if isinstance(ob_f.get("byte_hex"), str) and ob_f["byte_hex"].lower().replace(" ", "") in ("0x55", "55"):
        sub += 1
    if isinstance(ob_f.get("bits_lsb_first"), list) and ob_f["bits_lsb_first"] == [1,0,1,0,1,0,1,0]:
        sub += 1
    if isinstance(ob_f.get("stop_width_ns"), (int, float)) and 140 <= ob_f["stop_width_ns"] <= 180:
        sub += 1
    if isinstance(ob_f.get("frame_total_ns"), (int, float)) and 1560 <= ob_f["frame_total_ns"] <= 1640:
        sub += 1
    if not vcd_f_ok: sub = 0
    s["observed_bits_fixed"] = sub / tot

    # 12. report.md
    rep_p = rd / "report.md"
    rep = rep_p.read_text(errors="ignore") if rep_p.exists() else ""
    kws = ["LSB", "stop", "0x55", "0xAA", "160", "marker A", "marker B"]
    kw_hits = sum(1 for k in kws if k.lower() in rep.lower())
    refs = sum(1 for n in ["view_01", "view_03", "view_04"] if n in rep)
    extra = ["1520", "1600", "framing", "bit_idx"]
    extra_hits = sum(1 for k in extra if k.lower() in rep.lower())
    if len(rep) >= 400 and kw_hits == len(kws) and refs >= 3 and extra_hits >= 3:
        s["report_quality"] = 1.0
    elif len(rep) >= 200 and (kw_hits >= 5 or refs >= 2):
        s["report_quality"] = 0.4
    else:
        s["report_quality"] = 0.0

    # 13. marker_alignment.json — must be non-zero and consistent with marker pair span
    ma = jload(rd / "marker_alignment.json")
    diff = ma.get("diff_ns")
    mA, mB = mr.get("marker_A_ns"), mr.get("marker_B_ns")
    ok_align = (isinstance(diff, (int, float)) and 0 < abs(diff) <= 12
                and isinstance(mA, (int, float)) and isinstance(mB, (int, float))
                and abs((mB - mA) - 1440) <= 80)
    if ok_align:
        s["marker_alignment"] = 1.0
    elif isinstance(diff, (int, float)) and abs(diff) <= 40:
        s["marker_alignment"] = 0.3
    else:
        s["marker_alignment"] = 0.0

    # decode_wire.py present + non-trivial
    dw = rd / "decode_wire.py"
    if dw.exists():
        dt = dw.read_text(errors="ignore")
        needed = ["$dumpvars" in dt or "VCD" in dt.upper(),
                  "tx" in dt, "bit" in dt.lower(),
                  any(t in dt for t in ["open(", "Path(", "read("]),
                  any(t in dt for t in ["timescale", "$var", "#"]),
                  len(dt) > 600 and len(dt.splitlines()) >= 25]
        s["decode_script"] = sum(needed) / len(needed)
    else:
        s["decode_script"] = 0.0

    # uart_tx_fixed.v sanity
    uf = rd / "uart_tx_fixed.v"
    if uf.exists():
        t = uf.read_text(errors="ignore")
        good = "data_r[bit_idx]" in t and "CLKS_PER_BIT-1" in t.replace(" ", "")
        bad  = ("data_r[7 - bit_idx]" in t) or ("CLKS_PER_BIT/2)-1" in t.replace(" ", ""))
        s["fixed_rtl_clean"] = 1.0 if (good and not bad) else (0.4 if good else 0.0)
    else:
        s["fixed_rtl_clean"] = 0.0

    numeric = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(numeric) / max(1, len(numeric))

    # VLM rubric
    if vlm_score_rubric:
        sample = [str(rd / n) for n, _ in shots if (rd / n).exists()][:4]
        if sample:
            rubric = {
                "vlm_gtkwave_real": "截图来自 GTKWave GUI（可见 SST 树 / Wave panel / 时间轴）",
                "vlm_marker_named": "view_02 显示带名字 (A,B) 的 named marker 与时戳",
                "vlm_buggy_vs_fixed_diff": "view_01 与 view_03 在 tx 信号上的位模式视觉上明显不同",
                "vlm_stop_zoom_clear": "view_04 的 STOP 区高电平宽度与前面 8 个 data bit 的宽度可读对比",
            }
            vlm = vlm_score_rubric(sample, rubric, instruction="评估 GTKWave UART 波形排错截图。")
            for k in rubric: s[k] = vlm.get(k, 0.0)
            s["judge_method"] = vlm.get("judge_method", "failed")
            vlm_avg = sum(vlm.get(k, 0) for k in rubric) / len(rubric)
            s["overall_score"] = round((base + vlm_avg) / 2, 3)
            # Only enforce VLM cap when the helper actually ran. Whether
            # the agent invokes GUI tooling is not a scoring axis.
            if vlm_avg < 0.6:
                s["overall_score"] = round(min(s["overall_score"], 0.6), 3)
        else:
            s["overall_score"] = round(base, 3)
    else:
        s["overall_score"] = round(base, 3)

    if not cli_evidence:
        s["overall_score"] = round(min(s["overall_score"], 0.4), 3)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the gui_screenshots / vlm_* sub_scores.
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
