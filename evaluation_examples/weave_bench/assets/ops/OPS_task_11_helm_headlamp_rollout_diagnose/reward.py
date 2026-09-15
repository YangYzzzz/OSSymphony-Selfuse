# Auto-generated from WeaveBench task OPS_task_11_helm_headlamp_rollout_diagnose.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
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
    gt = Path("/opt/ops11_gt") if Path("/opt/ops11_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    s = {}
    cli_evidence = False
    gui_evidence = False

    def jload(p):
        try:
            return json.loads(Path(p).read_text())
        except Exception:
            return None

    truth = jload(gt / "expected.json") or {}

    hh = jload(rd / "helm_history.json")
    if isinstance(hh, list) and len(hh) >= 2:
        last_status = (hh[-1] or {}).get("status", "").lower()
        ok = last_status in {"failed", "pending-upgrade", "pending_upgrade", "superseded"}
        s["helm_history"] = 1.0 if ok else 0.5
        cli_evidence = True
    else:
        s["helm_history"] = 0.0

    m1 = rd / "manifest_rev1.yaml"
    m2 = rd / "manifest_rev2.yaml"
    s["manifests_present"] = 1.0 if (m1.exists() and m2.exists()
        and len(m1.read_text().splitlines()) >= 20
        and len(m2.read_text().splitlines()) >= 20) else 0.0
    if s["manifests_present"]:
        cli_evidence = True

    df = rd / "manifest_rev1_rev2.diff"
    diff_lines = [l for l in df.read_text().splitlines() if l.strip()] if df.exists() else []
    s["manifest_diff"] = 1.0 if len(diff_lines) >= 6 else 0.0

    immutable_whitelist = {
        "spec.selector.matchLabels",
        "spec.clusterIP",
        "spec.serviceName",
        "spec.volumeClaimTemplates.",
        "spec.template.spec.containers.resources",
    }
    idj = jload(rd / "immutable_diffs.json")
    diffs = (idj or {}).get("diffs", []) if isinstance(idj, dict) else []
    # additionally require at least one diff path mentions matchLabels
    must_have_matchlabels = any("matchLabels" in str(d.get("path", "")) for d in diffs if isinstance(d, dict))
    valid = 0
    invalid = 0
    for d in diffs:
        if not isinstance(d, dict):
            continue
        path = str(d.get("path", ""))
        if any(path.startswith(w) for w in immutable_whitelist):
            valid += 1
        else:
            invalid += 1
    if valid >= 1 and invalid == 0 and must_have_matchlabels:
        s["immutable_diffs"] = 1.0
    elif valid >= 1 and must_have_matchlabels:
        s["immutable_diffs"] = max(0.3, valid / (valid + invalid))
    elif valid >= 1:
        s["immutable_diffs"] = min(0.5, valid / max(1, valid + invalid))
    else:
        s["immutable_diffs"] = 0.0

    ev = jload(rd / "events.json")
    ev_text = json.dumps(ev) if ev else ""
    has_event_kw = any(k in ev_text.lower() for k in ["immutable", "failedcreate", "fieldimmutable", "field is immutable"])
    s["events_keyword"] = 1.0 if (ev and has_event_kw) else (0.4 if ev else 0.0)
    if ev:
        cli_evidence = True

    crit = (rd / "critical_event.txt").read_text(errors="ignore") if (rd / "critical_event.txt").exists() else ""
    cl = crit.lower()
    phrase = ("field is immutable" in cl) and ("selector" in cl) and ("deployment" in cl or "apps/v1" in cl)
    s["critical_event"] = 1.0 if phrase else (0.3 if "immutable" in cl else 0.0)

    shots = [
        ("view_01_headlamp_workloads.png", ["Workloads", "Deployments", "demo", "Headlamp"]),
        ("view_02_headlamp_events.png", ["Events", "FailedCreate", "Failed", "immutable", "Reason"]),
        ("view_03_headlamp_manifest_yaml.png", ["selector", "matchLabels", "spec", "apiVersion"]),
        ("view_04_headlamp_replicaset.png", ["ReplicaSet", "Desired", "Ready", "demo"]),
        ("view_05_headlamp_after_fix.png", ["Workloads", "Deployments", "demo", "Ready"]),
    ]
    present = sum(1 for n, _ in shots if (rd / n).exists())
    real = sum(1 for n, _ in shots if (rd / n).exists() and (rd / n).stat().st_size >= 60_000)
    s["screenshots_present"] = real / len(shots)
    ocr_hits = 0
    if pytesseract and Image:
        for n, kws in shots:
            p = rd / n
            if p.exists():
                try:
                    tx = pytesseract.image_to_string(Image.open(p))
                    if any(k.lower() in tx.lower() for k in kws):
                        ocr_hits += 1
                except Exception:
                    pass
    s["screenshots_ocr"] = ocr_hits / len(shots)
    gui_evidence = (real >= 4) and (ocr_hits >= 3)

    fp = rd / "fix_chart.patch"
    if fp.exists():
        ftext = fp.read_text()
        nonempty = [l for l in ftext.splitlines() if l.strip()]
        header_ok = ("--- " in ftext and "+++ " in ftext)
        hunk_ok = ftext.count("@@") >= 1
        targets_tpl = ("broken-chart/templates/deployment.yaml" in ftext) or ("templates/deployment.yaml" in ftext)
        mentions_sel = ("selector" in ftext) or ("matchLabels" in ftext) or ("helm.sh/resource-policy" in ftext)
        s["fix_patch"] = 1.0 if (len(nonempty) >= 12 and header_ok and hunk_ok and targets_tpl and mentions_sel) else (0.3 if header_ok else 0.0)
    else:
        s["fix_patch"] = 0.0

    pfd = rd / "post_fix_diff.txt"
    pt = pfd.read_text(errors="ignore") if pfd.exists() else ""
    diffish = sum(1 for l in pt.splitlines() if l.startswith(("+", "-", "@@", "<", "> "))) >= 4
    mentions_res = ("Deployment" in pt) or ("selector" in pt) or ("matchLabels" in pt)
    s["post_fix_diff"] = 1.0 if (len(pt) >= 200 and diffish and mentions_res) else (0.3 if pt else 0.0)

    pm = (rd / "postmortem.md").read_text(errors="ignore") if (rd / "postmortem.md").exists() else ""
    refs = {
        "rev": bool(re.search(r"rev(ision)?\s*\d+", pm, re.I)) or "revision" in pm.lower(),
        "field": any(p in pm for p in ["spec.selector", "matchLabels", "selector", "clusterIP"]),
        "msg": "immutable" in pm.lower(),
        "patch": "patch" in pm.lower() or "diff" in pm.lower() or "uninstall" in pm.lower(),
    }
    crossref = sum(refs.values())
    if len(pm) >= 300 and crossref >= 4:
        s["postmortem"] = 1.0
    elif len(pm) >= 150 and crossref >= 2:
        s["postmortem"] = 0.5
    else:
        s["postmortem"] = 0.0

    numeric = [v for v in s.values() if isinstance(v, (int, float))]
    base = sum(numeric) / max(1, len(numeric))

    if vlm_score_rubric:
        sample = [str(rd / n) for n, _ in shots if (rd / n).exists()][:4]
        if sample:
            rubric = {
                "vlm_headlamp_real": "至少一张截图清晰显示 Headlamp 主界面（左侧资源导航 + 右侧资源表格）",
                "vlm_yaml_editor_open": "view_03 是 Headlamp 的 YAML 编辑器视图，能看到 selector / matchLabels 字段",
                "vlm_event_panel": "view_02 显示 Events 列表 + 至少一条 reason 列指明失败原因",
            }
            vlm = vlm_score_rubric(sample, rubric, instruction="评估 Headlamp K8s GUI 截图。")
            for k in rubric:
                s[k] = vlm.get(k, 0.0)
            s["judge_method"] = vlm.get("judge_method", "failed")
            vlm_avg = sum(vlm.get(k, 0) for k in rubric) / len(rubric)
            s["overall_score"] = round((base + vlm_avg) / 2, 3)
            # Only enforce VLM caps when the helper actually ran.
            if vlm.get("vlm_headlamp_real", 0) < 0.6:
                s["overall_score"] = round(min(s["overall_score"], 0.45), 3)
            if vlm_avg < 0.6:
                s["overall_score"] = round(min(s["overall_score"], 0.6), 3)
        else:
            s["overall_score"] = round(base, 3)
    else:
        s["overall_score"] = round(base, 3)

    if not cli_evidence:
        s["overall_score"] = round(min(s["overall_score"], 0.4), 3)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the screenshots / vlm_* sub_scores.
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
