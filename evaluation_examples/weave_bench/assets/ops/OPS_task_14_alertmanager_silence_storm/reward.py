# Auto-generated from WeaveBench task OPS_task_14_alertmanager_silence_storm.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Alertmanager silence-storm grader.

    Sub-scores (12) + 3 hard gates:
      G1: no CLI evidence -> cap 0.4
      G2: no GUI screenshot -> cap 0.4
      G3: VLM judge avg < 0.6 -> cap 0.6
    """
    import json, re, subprocess
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

    # ---- 1. silences_raw.json ----
    sraw = rd / "silences_raw.json"
    silences = []
    if sraw.exists():
        try:
            silences = json.loads(sraw.read_text())
        except Exception:
            silences = []
    if isinstance(silences, dict):
        silences = silences.get("data", []) or silences.get("silences", [])
    blob = json.dumps(silences) if isinstance(silences, list) else ""
    has_regex_star = ('".*"' in blob) or ("'.*'" in blob)
    has_y9999 = "9999" in blob
    s["silences_raw_present"] = 1.0 if (
        isinstance(silences, list) and len(silences) >= 12
        and all(isinstance(x, dict) and "matchers" in x and "endsAt" in x for x in silences)
        and has_regex_star and has_y9999
    ) else (0.5 if isinstance(silences, list) and len(silences) >= 8 else 0.0)

    # ---- 2. alerts_active + alerts_prom ----
    aa = rd / "alerts_active.json"
    ap = rd / "alerts_prom.json"
    s["alerts_active_present"] = 1.0 if (aa.exists() and aa.stat().st_size > 50) else 0.0
    s["alerts_prom_present"] = 1.0 if (ap.exists() and ap.stat().st_size > 50) else 0.0

    # ---- 3. promtool check output ----
    pt = rd / "promtool_check.txt"
    pt_text = pt.read_text(errors="ignore") if pt.exists() else ""
    s["promtool_check"] = 1.0 if (
        ("SUCCESS" in pt_text or "FAILED" in pt_text or "is valid" in pt_text)
        and len(pt_text) > 20
    ) else 0.0

    # ---- 4. silence_diff recall/precision vs gt ----
    diff = rd / "silence_diff.md"
    diff_text = diff.read_text(errors="ignore") if diff.exists() else ""
    truth_path = gt / "swallowed_alerts.txt"
    truth = set()
    if truth_path.exists():
        truth = {ln.strip() for ln in truth_path.read_text().splitlines() if ln.strip() and not ln.startswith("#")}
    # Each alertname must appear together with a silence id (8+ hex/dash) on
    # the same non-empty line — i.e. an actual local join, not a JSON dump.
    joined = []
    for ln in diff_text.splitlines():
        if re.search(r"[0-9a-f]{8}-[0-9a-f-]{4,}", ln) or re.search(r"silence[_ -]?id", ln, re.I):
            joined.append(ln)
    join_blob = "\n".join(joined)
    if truth:
        found = {a for a in truth if re.search(r"\b" + re.escape(a) + r"\b", join_blob)}
        extras = set(re.findall(r"\b[A-Z][A-Za-z0-9]{4,40}\b", join_blob)) - truth - {"BillingDeploy","SearchSpike","ApiLatencyDegraded"}
        fp_extra = max(0, len(extras) - 1)
        s["swallowed_recall"] = min(1.0, len(found) / max(1, len(truth)))
        s["swallowed_precision"] = 1.0 if fp_extra == 0 else max(0.0, 1 - fp_extra/3.0)
    else:
        s["swallowed_recall"] = 1.0 if diff_text.strip() else 0.0
        s["swallowed_precision"] = 1.0 if diff_text.strip() else 0.0

    # ---- 5. eight web UI screenshots ----
    shots = [
        "view_01_silences_overview.png",
        "view_02_offender_silence_expanded.png",
        "view_03_active_alerts_filter.png",
        "view_04_status_routes_tree.png",
        "view_05_silence_form_preview.png",
        "view_06_prom_alerts_page.png",
        "view_07_route_tooltip.png",
        "view_08_after_fix.png",
    ]
    present = sum(1 for n in shots if (rd / n).exists() and (rd / n).stat().st_size > 30000)
    s["screenshots_count"] = present / len(shots)

    ocr_hits = 0
    if pytesseract and Image:
        keywords = ["Silences", "Alerts", "Status", "Matcher", "Receiver",
                    "Active", "Prometheus", "Alertmanager", "Routing",
                    "Affected", "Expire", "New Silence"]
        for n in shots:
            p = rd / n
            if not p.exists():
                continue
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k in tx for k in keywords):
                    ocr_hits += 1
            except Exception:
                pass
        s["screenshots_ocr"] = ocr_hits / len(shots)
    else:
        s["screenshots_ocr"] = 0.5 if present else 0.0

    # ---- 6. routing_walk.json structure + amtool cross-check ----
    rw_path = rd / "routing_walk.json"
    rw_data = {}
    if rw_path.exists():
        try:
            rw_data = json.loads(rw_path.read_text())
        except Exception:
            rw_data = {}
    path = rw_data.get("path", [])
    structural_ok = isinstance(path, list) and len(path) >= 3 and "final_receiver" in rw_data
    s["routing_walk_struct"] = 1.0 if structural_ok else (0.5 if rw_data else 0.0)

    # cross-check final_receiver vs amtool routes test
    cross_ok = False
    cfg = Path("/tmp_workspace/silence_audit/alertmanager.yml")
    if structural_ok and cfg.exists():
        labels = rw_data.get("input_labels", {}) or {}
        args = ["amtool", "config", "routes", "test",
                "--config.file=" + str(cfg)]
        for k, v in labels.items():
            args.append(f"{k}={v}")
        try:
            r = subprocess.run(args, capture_output=True, text=True, timeout=30)
            out = (r.stdout + r.stderr)
            # Prefer the explicit "Receiver:" header that amtool emits; fall
            # back to the historic loose pattern when the output format
            # differs across amtool versions.
            m = re.search(r"\bReceiver:\s*(\S+)", out) or \
                re.search(r"(?:receiver|route)[^\n]*?[:= ]\s*([A-Za-z0-9_\-]+)", out)
            amtool_recv = (m.group(1).strip() if m else "").lower()
            fr = str(rw_data.get("final_receiver", "")).strip().lower()
            if fr and amtool_recv and fr == amtool_recv and fr not in {"default","pagerduty-default"}:
                cross_ok = True
        except Exception:
            pass
    s["routing_walk_consistent"] = 1.0 if cross_ok else (0.5 if structural_ok else 0.0)

    # ---- 7. fix_plan.md ----
    fp = rd / "fix_plan.md"
    fp_text = fp.read_text(errors="ignore") if fp.exists() else ""
    bullets = re.split(r"(?m)^\s*[-*]\s+|^\s*\d+[.)]\s+", fp_text)
    bullets = [b for b in bullets if b.strip()]
    def bullet_ok(b):
        return (re.search(r"=~|\.\*|9999", b) and          # cites the bad pattern
                re.search(r"\bendsAt\b|\bends_at\b", b) and   # names the field
                re.search(r"(service|alertname)\s*=\s*['\"]?[A-Za-z]", b, re.I))  # concrete fix
    good = sum(1 for b in bullets if bullet_ok(b))
    s["fix_plan"] = 1.0 if good >= 3 else (0.5 if good >= 1 else 0.0)

    # ---- 8. before_after.txt has both segments + active count rises ----
    ba = rd / "before_after.txt"
    ba_text = ba.read_text(errors="ignore") if ba.exists() else ""
    has_both = ("BEFORE" in ba_text.upper() and "AFTER" in ba_text.upper())
    rises = False
    if has_both:
        # split on AFTER marker
        try:
            up = ba_text.upper()
            i = up.index("AFTER")
            before = ba_text[:i]
            after = ba_text[i:]
            # heuristic: count alert rows (lines containing common alert markers)
            def cnt(t):
                return len({m for m in re.findall(r"\b[A-Z][A-Za-z0-9]{4,40}\b", t) if m not in {"BEFORE","AFTER","ALERT","ALERTS","STATE"}})
            b, a = cnt(before), cnt(after)
            rises = (a >= b + 2) and b >= 1 and a >= 4
        except Exception:
            rises = False
    s["before_after"] = 1.0 if (has_both and rises) else (0.5 if has_both else 0.0)

    # ---- compute base ----
    numeric = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(numeric) / max(1, len(numeric))

    # ---- VLM rubric ----
    vlm_avg = None
    if vlm_score_rubric:
        # Pass all 8 shots so view_07 (route_tooltip) is included, otherwise
        # the vlm_hover_tooltip rubric rates an unseen image.
        sample = [str(rd / n) for n in shots if (rd / n).exists()][:8]
        if sample:
            rubric = {
                "vlm_silences_ui_real":
                    "至少一张截图清晰显示 Alertmanager Silences 页面 (silence 卡片列表 + 顶部 Silenced/Active/Suppressed tab)",
                "vlm_routing_tree_visible":
                    "view_04 类截图显示 Status > Routing tree 的嵌套树/YAML 视图",
                "vlm_hover_tooltip":
                    "view_07 截图含 hover tooltip 浮层(矩形带尖角的悬浮框)在 routing/receiver 节点上",
                "vlm_silence_form_preview":
                    "view_05 截图显示 New Silence 表单 + Affected alerts 预览数字 ≥ 1",
            }
            try:
                vlm = vlm_score_rubric(
                    sample, rubric,
                    instruction="评估 Alertmanager Web UI 取证截图的真实性"
                )
                for k in rubric:
                    s[k] = float(vlm.get(k, 0.0) or 0.0)
                s["judge_method"] = vlm.get("judge_method", "vlm")
                vlm_avg = sum(s[k] for k in rubric) / len(rubric)
            except Exception:
                vlm_avg = None

    # ---- hard gates ----
    has_cli_evidence = (
        s["silences_raw_present"] >= 0.5
        and (s["alerts_active_present"] + s["alerts_prom_present"]) >= 1.0
        and s["promtool_check"] >= 0.5
    )

    if vlm_avg is not None:
        overall = (base + vlm_avg) / 2.0
    else:
        overall = base

    if not has_cli_evidence:
        overall = min(overall, 0.4)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the screenshots_count / screenshots_ocr / 4 vlm_* sub_scores.
    if vlm_avg is not None and vlm_avg < 0.6:
        overall = min(overall, 0.5)
    if vlm_avg is not None and vlm_avg < 0.4:
        overall = min(overall, 0.35)
    # G4: silence_diff must show real recall, else cap at 0.5
    if s.get("swallowed_recall", 0) < 0.5:
        overall = min(overall, 0.5)

    s["overall_score"] = round(overall, 3)
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
