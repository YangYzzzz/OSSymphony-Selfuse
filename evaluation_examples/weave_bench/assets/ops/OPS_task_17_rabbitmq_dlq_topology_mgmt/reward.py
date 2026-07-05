# Auto-generated from WeaveBench task OPS_task_17_rabbitmq_dlq_topology_mgmt.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """OPS_task_17 grader: RabbitMQ DLQ routing-key mismatch triage via
    broker management HTTP API structured evidence and Management UI
    visual screenshots. Sub-scores cover topology dump quality, rate-gap
    quantification, screenshot presence + OCR + VLM, the binding
    fix evidence, post-fix DLQ growth, diagnosis JSON, postmortem
    quality, and cross-channel switch count."""
    import json, re
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/opt/ops17_gt") if Path("/opt/ops17_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    s = {}
    expected = {}
    if (gt_dir / "expected.json").exists():
        try: expected = json.loads((gt_dir / "expected.json").read_text())
        except Exception: expected = {}
    main_q = expected.get("main_queue", "orders.q")
    dlq = expected.get("dlq_queue", "orders.dlq")
    dlx = expected.get("dlx_exchange", "orders.dlx")
    expect_rk = expected.get("expected_dead_letter_routing_key_on_queue",
                             "dead.unrouted")
    broken_rk = expected.get("broken_dlx_binding_routing_key",
                             "dead.routed.#")
    req_keys = expected.get("report_required_keys", [])
    min_dlq_growth = int(expected.get("min_dlq_growth_after_fix", 20))

    def _read(name):
        p = rd / name
        return p.read_text(errors="ignore") if p.exists() else ""

    # 1. status
    st = _read("01_rmq_status.txt")
    s["rmq_status_present"] = 1.0 if st and "RabbitMQ" in st else (0.4 if st else 0.0)

    # 2. queues snapshot — three queues + dlq ~0
    qs = _read("02_queues.txt")
    has_three = (main_q in qs and dlq in qs and "orders.audit" in qs)
    dlq_zero = False
    for ln in qs.splitlines():
        if dlq in ln:
            nums = re.findall(r"\b\d+\b", ln)
            if nums:
                try:
                    if int(nums[0]) <= 5:
                        dlq_zero = True
                except Exception:
                    pass
    if has_three and dlq_zero:
        s["queues_initial_anomaly"] = 1.0
    elif has_three:
        s["queues_initial_anomaly"] = 0.6
    elif qs:
        s["queues_initial_anomaly"] = 0.3
    else:
        s["queues_initial_anomaly"] = 0.0

    # 3. bindings show broken routing key
    bnd = _read("03_bindings.txt")
    has_broken = (dlx in bnd and dlq in bnd
                  and re.search(r"dead\.routed", bnd) is not None)
    s["bindings_broken_visible"] = 1.0 if has_broken else (0.5 if (dlx in bnd and dlq in bnd) else 0.0)

    # 4. queue arguments expose x-dead-letter-*
    qa = _read("04_queue_args.txt")
    if qa and "x-dead-letter-routing-key" in qa and expect_rk in qa:
        s["queue_args_expected_rk"] = 1.0
    elif qa and "x-dead-letter" in qa:
        s["queue_args_expected_rk"] = 0.5
    else:
        s["queue_args_expected_rk"] = 0.0

    # 5. rate gap quantified
    def _rates(name):
        try:
            d = json.loads(_read(name) or "{}")
        except Exception:
            return None, None
        ms = d.get("message_stats", {}) or {}
        pub = ms.get("publish_details", {}).get("rate")
        deliv = ms.get("deliver_get_details", {}).get("rate")
        if deliv is None:
            deliv = ms.get("deliver_details", {}).get("rate")
        return pub, deliv
    p0, d0 = _rates("05_rates_t0.json")
    p1, d1 = _rates("05_rates_t1.json")
    gap_ok = False
    try:
        gaps = []
        for p, d in [(p0, d0), (p1, d1)]:
            if p is not None and d is not None:
                gaps.append(float(p) - float(d))
        if gaps and max(gaps) >= 4.0:
            gap_ok = True
        elif gaps and max(gaps) >= 1.5:
            s["rate_gap_observed"] = 0.6
    except Exception:
        pass
    if gap_ok:
        s["rate_gap_observed"] = 1.0
    elif "rate_gap_observed" not in s:
        s["rate_gap_observed"] = 0.3 if (p0 is not None or p1 is not None) else 0.0

    # 6. screenshots existence + size
    shots = ["view_01_mgmt_overview.png",
             "view_02_mgmt_rates_tooltip.png",
             "view_03_mgmt_queues.png",
             "view_04_dlq_bindings.png",
             "view_05_dlx_detail.png",
             "view_06_mgmt_overview_after.png",
             "view_07_dlq_after.png"]
    def _real_shot(p):
        if not p.exists() or p.stat().st_size < 30000:
            return False
        try:
            from PIL import Image
            im = Image.open(p)
            w, h = im.size
            if w < 1024 or h < 700:
                return False
            ex = im.convert("RGB").getextrema()
            return max(hi - lo for lo, hi in ex) > 60
        except Exception:
            return False
    present = sum(1 for n in shots if _real_shot(rd / n))
    s["gui_screenshots_count"] = present / len(shots)

    # 7. OCR
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_01_mgmt_overview.png":
                ["RabbitMQ", "Overview", "Queued messages", "Message rates",
                 "Connections"],
            "view_02_mgmt_rates_tooltip.png":
                ["msg/s", "publish", "deliver", "redeliver", "ack"],
            "view_03_mgmt_queues.png":
                ["orders.dlq", "orders.audit", "Ready"],
            "view_04_dlq_bindings.png":
                ["orders.dlx", "dead.routed", "Routing key"],
            "view_05_dlx_detail.png":
                ["Exchange", "orders.dlx", "Bindings", "Message rate"],
            "view_06_mgmt_overview_after.png":
                ["RabbitMQ", "Overview", "Queued messages", "Message rates"],
            "view_07_dlq_after.png":
                ["orders.dlq", "Ready"],
        }
        for n, ks in kws.items():
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k in tx for k in ks): ocr_hits += 1
                except Exception:
                    pass
        s["gui_screenshots_ocr"] = ocr_hits / len(shots)
    except ImportError:
        s["gui_screenshots_ocr"] = 0.5

    # 8. diagnosis JSON
    diag = rd / "diagnosis.json"
    diag_keys_score = 0.0; diag_rk = 0.0; diag_rem = 0.0
    if diag.exists():
        try:
            d = json.loads(diag.read_text())
            def _numok(v, lo, hi=None):
                try:
                    x = float(v)
                    return x >= lo and (hi is None or x <= hi)
                except Exception:
                    return False
            num_ok = (_numok(d.get("dlq_depth_before_fix"), 0, 5)
                      and _numok(d.get("dlq_depth_after_fix"), min_dlq_growth)
                      and _numok(d.get("publish_rate_msgps"), 5)
                      and _numok(d.get("deliver_rate_msgps"), 0))
            present_keys = sum(1 for k in req_keys if k in d and d.get(k) not in (None, "", 0))
            diag_keys_score = (present_keys / max(1, len(req_keys))) * (1.0 if num_ok else 0.4)
            if str(d.get("expected_routing_key", "")).strip() == expect_rk:
                diag_rk = 1.0
            elif expect_rk in str(d.get("expected_routing_key", "")):
                diag_rk = 0.7
            rem = str(d.get("remediation", ""))
            if expect_rk in rem and ("bind" in rem.lower() or "binding" in rem.lower()):
                diag_rem = 1.0
            elif expect_rk in rem:
                diag_rem = 0.6
        except Exception:
            pass
    s["diagnosis_keys"] = diag_keys_score
    s["diagnosis_routing_key_match"] = diag_rk
    s["diagnosis_remediation_match"] = diag_rem

    # 9. remediation script
    rem = _read("06_remediation.sh")
    rem_ok = False
    if rem and expect_rk in rem and re.search(
        r"declare\s+binding|Add\s+binding|queue_bind|x-dead-letter-routing-key",
            rem, re.I):
        rem_ok = True
    s["remediation_script_ok"] = 1.0 if rem_ok else (0.5 if rem else 0.0)

    # 10. bindings after — new row visible
    ba = _read("07_bindings_after.txt")
    # Tolerate any whitespace/column-separator (tab, multi-space, JSON commas)
    # between dlx, dlq, and expect_rk on the same logical row.
    _row_re = rf"{re.escape(dlx)}[^\n]*{re.escape(dlq)}[^\n]*{re.escape(expect_rk)}"
    if ba and dlx in ba and dlq in ba and expect_rk in ba and re.search(_row_re, ba):
        s["bindings_after_ok"] = 1.0
    elif ba and dlx in ba and dlq in ba and expect_rk in ba:
        s["bindings_after_ok"] = 0.6
    elif ba and dlx in ba:
        s["bindings_after_ok"] = 0.4
    else:
        s["bindings_after_ok"] = 0.0

    # 11. DLQ growth
    qa2 = _read("08_queues_after.txt")
    dlq_count = 0
    for ln in qa2.splitlines():
        if dlq in ln:
            nums = re.findall(r"\b\d+\b", ln)
            if nums:
                try:
                    dlq_count = max(dlq_count, int(nums[0]))
                except Exception:
                    pass
    if dlq_count >= min_dlq_growth:
        s["dlq_growth_after_fix"] = 1.0
    elif dlq_count >= max(5, min_dlq_growth // 2):
        s["dlq_growth_after_fix"] = 0.6
    else:
        s["dlq_growth_after_fix"] = 0.2 if qa2 else 0.0

    # 12. postmortem
    pm = _read("postmortem.md")
    pm_chars = len(pm)
    s["postmortem_length"] = 1.0 if pm_chars >= 600 else pm_chars / 600.0
    pm_kws = expected.get("expected_postmortem_keywords",
                          ["dead-letter", "binding", "routing key",
                           "broker", "management", "dlx", "topic"])
    hits = sum(1 for k in pm_kws if k.lower() in pm.lower())
    s["postmortem_keywords"] = hits / max(1, len(pm_kws))
    sects = expected.get("expected_postmortem_sections",
                         ["## 时间线", "## 根因", "## 修复",
                          "## 跨通道证据链"])
    sect_hits = sum(1 for h in sects if h in pm)
    s["postmortem_sections"] = sect_hits / max(1, len(sects))

    # 13. cross-channel switches
    cc = rd / "cross_channel.json"
    cc_ok = 0.0
    if cc.exists():
        try:
            d = json.loads(cc.read_text())
            sw = int(d.get("switches", 0))
            tr = d.get("trace", [])
            required_struct = {"03_bindings.txt", "04_queue_args.txt", "07_bindings_after.txt", "08_queues_after.txt"}
            required_visual = {"view_02_mgmt_rates_tooltip.png", "view_04_dlq_bindings.png", "view_06_mgmt_overview_after.png", "view_07_dlq_after.png"}
            struct_refs = sum(1 for x in tr if isinstance(x, str) and x.startswith("STRUCT:") and any((rd / f).exists() for f in required_struct if x.split(":", 1)[1] in f or f.startswith(x.split(":", 1)[1])))
            visual_refs = sum(1 for x in tr if isinstance(x, str) and x.startswith("VISUAL:") and any((rd / f).exists() for f in required_visual if x.split(":", 1)[1] in f or f.startswith(x.split(":", 1)[1])))
            cc_ok = 1.0 if (sw >= 5 and len(tr) >= 5 and struct_refs >= 2 and visual_refs >= 2) else (0.4 if sw >= 3 else 0.0)
        except Exception:
            pass
    s["cross_channel_switches"] = cc_ok

    # 14. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd / n) for n in shots if (rd / n).exists()]
    vlm_judge = 0.0
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_mgmt_ui_real":
                "至少一张截图清晰显示 RabbitMQ Management UI 主窗口（顶部 Overview/Connections/Channels/Exchanges/Queues 导航栏 + Queued messages / Message rates 图）",
            "vlm_rates_tooltip":
                "view_02 显示 Message rates 折线图上有 hover tooltip 浮窗，且 publish 与 deliver 的数字可读",
            "vlm_bindings_panel":
                "view_04 显示某队列详情页的 Bindings 子面板，包含 source exchange + routing key 列",
            "vlm_after_fix_chart":
                "view_06 / view_07 显示修复后 publish 与 deliver 收敛 或 DLQ messages 计数 ≥ 20",
        }
        vlm = vlm_score_rubric(vlm_imgs[:7], rubric,
            instruction="评估 SRE 用 RabbitMQ Management UI 排查 DLQ 路由黑洞的截图。")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
        vlm_judge = sum(s.get(k, 0.0) for k in rubric) / max(1, len(rubric))
    else:
        for k in ("vlm_mgmt_ui_real", "vlm_rates_tooltip",
                  "vlm_bindings_panel", "vlm_after_fix_chart"):
            s[k] = 0.5
        vlm_judge = 0.5

    # Aggregate
    nums = [v for k, v in s.items()
            if isinstance(v, (int, float)) and k != "judge_method"]
    base = sum(nums) / max(1, len(nums))

    # Hard gates
    has_struct = (s["bindings_broken_visible"] >= 0.5
                  and s["queue_args_expected_rk"] >= 0.4
                  and s["bindings_after_ok"] >= 0.4)
    has_visual = s["gui_screenshots_count"] >= 0.5
    if not has_struct: base = min(base, 0.4)
    if not has_visual: base = min(base, 0.4)
    # Only apply the VLM cap when the VLM judge actually ran. When the
    # helper is unavailable (vlm_score_rubric is None), the 0.5 fallback
    # would otherwise penalise a perfect run for an environment defect.
    if vlm_score_rubric is not None and vlm_judge < 0.6:
        base = min(base, 0.55)
    if s["dlq_growth_after_fix"] < 1.0 or s.get("vlm_after_fix_chart", 0) < 0.5:
        base = min(base, 0.55)
    if s["rate_gap_observed"] < 0.6 or s["cross_channel_switches"] < 1.0:
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
