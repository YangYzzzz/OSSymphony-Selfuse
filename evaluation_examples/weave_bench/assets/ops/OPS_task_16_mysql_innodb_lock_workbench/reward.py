# Auto-generated from WeaveBench task OPS_task_16_mysql_innodb_lock_workbench.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """OPS_task_16 grader: MySQL InnoDB lock contention triage via
    mysql CLI + perf_schema + slowlog (CLI channel) and MySQL Workbench
    Client Connections + Visual Explain (GUI channel). Sub-scores cover
    CLI evidence depth, GUI screenshot presence + OCR, the remediation
    DDL choice, the post-fix lock-wait drop ratio, the diagnosis JSON,
    the postmortem, and cross-channel switch count."""
    import json, os, re
    from pathlib import Path
    rd = Path("/tmp_workspace/results")
    gt_dir = Path("/opt/ops16_gt") if Path("/opt/ops16_gt/expected.json").exists() else Path("/tmp_workspace/gt")
    s = {}
    expected = {}
    if (gt_dir / "expected.json").exists():
        try: expected = json.loads((gt_dir / "expected.json").read_text())
        except Exception: expected = {}
    bad_subs = expected.get("bad_query_substrings",
                            ["UPDATE invoices", "tenant_id", "status"])
    fix_must = expected.get("expected_fix_index_must_include",
                            ["tenant_id", "status"])
    min_waits = int(expected.get("min_lock_wait_events_observed", 5))
    min_slow = int(expected.get("min_slowlog_rows", 5))
    req_keys = expected.get("report_required_keys", [])

    def _read(name):
        p = rd / name
        return p.read_text(errors="ignore") if p.exists() else ""

    # 1. version + global counters
    s["mysql_version_present"] = 1.0 if _read("01_mysql_version.txt").strip() else 0.0
    cnt_txt = _read("02_innodb_status_counters.txt")
    pre_avg = 0.0
    m = re.search(r"Innodb_row_lock_time_avg\s+(\d+(?:\.\d+)?)", cnt_txt)
    if m:
        try: pre_avg = float(m.group(1))
        except Exception: pre_avg = 0.0
    s["innodb_counters_present"] = 1.0 if (cnt_txt and pre_avg > 50) else (0.5 if cnt_txt else 0.0)

    # 2. SHOW ENGINE INNODB STATUS
    eng = _read("03_innodb_status.txt")
    if eng and re.search(r"LATEST DETECTED DEADLOCK|LOCK WAIT|lock_mode", eng):
        s["innodb_engine_status"] = 1.0
    elif eng:
        s["innodb_engine_status"] = 0.5
    else:
        s["innodb_engine_status"] = 0.0

    # 3. lock-wait sampling rows
    lw = _read("04_lock_waits.txt")
    waiter_rows = len(re.findall(r"\bwaiting_trx\b|\bblocking_trx\b", lw))
    # Each sample writes at most 2 occurrences of those headers; count
    # non-header lines that look like trx data instead:
    data_lines = [ln for ln in lw.splitlines()
                  if ln.strip() and not ln.lower().startswith("waiting")
                  and "+--" not in ln and "|" in ln]
    n_samples = len(data_lines)
    if n_samples >= min_waits:
        s["lock_wait_samples"] = 1.0
    elif n_samples >= 2:
        s["lock_wait_samples"] = n_samples / float(min_waits)
    else:
        s["lock_wait_samples"] = 0.2 if waiter_rows else 0.0

    # 4. slowlog + digest
    slog = _read("05_slow_query.log")
    n_slow_lines = len([ln for ln in slog.splitlines()
                        if ln.strip() and not ln.startswith("#")])
    s["slow_log_present"] = 1.0 if n_slow_lines >= min_slow else (n_slow_lines / float(min_slow) if n_slow_lines else 0.0)
    digest = _read("05_slow_digest.txt")
    s["slow_digest_match"] = 1.0 if (digest and all(b in digest for b in bad_subs[:3])) else (0.5 if digest else 0.0)

    # 5. GUI screenshots existence + size
    shots = ["view_01_workbench_dashboard.png",
             "view_02_client_connections.png",
             "view_03_connection_rightclick.png",
             "view_04_perf_report.png",
             "view_05_visual_explain_before.png",
             "view_06_visual_explain_after.png",
             "view_07_connections_after.png"]
    present = sum(1 for n in shots
                  if (rd / n).exists() and (rd / n).stat().st_size > 5000)
    s["gui_screenshots_count"] = present / len(shots)

    # 6. OCR keyword hits
    ocr_hits = 0
    try:
        import pytesseract
        from PIL import Image
        kws = {
            "view_01_workbench_dashboard.png":
                ["MySQL", "Workbench", "Server Status", "InnoDB", "Connections"],
            "view_02_client_connections.png":
                ["Client Connections", "Thread", "State", "Info", "Time"],
            "view_03_connection_rightclick.png":
                ["Kill", "View", "Thread", "Query", "Connection"],
            "view_04_perf_report.png":
                ["Performance", "Top", "Resource", "Query", "Statement"],
            "view_05_visual_explain_before.png":
                ["EXPLAIN", "invoices", "Visual", "Cost", "rows"],
            "view_06_visual_explain_after.png":
                ["EXPLAIN", "invoices", "Visual", "Cost", "rows", "ix_"],
            "view_07_connections_after.png":
                ["Client Connections", "Thread", "State", "Info"],
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

    # 7. remediation DDL parsed
    ddl = _read("06_remediation.sql")
    has_ddl = bool(re.search(r"CREATE\s+(?:UNIQUE\s+)?INDEX|ALTER\s+TABLE\s+invoices\s+ADD\s+(?:INDEX|KEY)",
                             ddl, re.I))
    has_cols = all(re.search(rf"\b{c}\b", ddl, re.I) for c in fix_must)
    if has_ddl and has_cols:
        s["remediation_ddl_ok"] = 1.0
    elif has_ddl:
        s["remediation_ddl_ok"] = 0.5
    else:
        s["remediation_ddl_ok"] = 0.0

    # 8. SHOW INDEX after — agent-applied fix landed
    idx_after = _read("07_indexes_after.txt")
    s["index_after_present"] = 1.0 if (idx_after and "tenant_id" in idx_after and "status" in idx_after) else (0.4 if idx_after else 0.0)

    # 9. post-fix lock_time_avg drop
    after_txt = _read("08_innodb_status_after.txt")
    post_avg = None
    m2 = re.search(r"Innodb_row_lock_time_avg\s+(\d+(?:\.\d+)?)", after_txt)
    if m2:
        try: post_avg = float(m2.group(1))
        except Exception: post_avg = None
    if pre_avg and post_avg is not None:
        if post_avg <= pre_avg / 3.0:
            s["lock_wait_drop"] = 1.0
        elif post_avg <= pre_avg / 1.5:
            s["lock_wait_drop"] = 0.6
        else:
            s["lock_wait_drop"] = 0.2
    else:
        s["lock_wait_drop"] = 0.4 if after_txt else 0.0

    # 10. diagnosis JSON: required keys + missing_index check
    diag = rd / "diagnosis.json"
    diag_keys_score = 0.0; diag_idx = 0.0; diag_q = 0.0
    if diag.exists():
        try:
            d = json.loads(diag.read_text())
            present_keys = sum(1 for k in req_keys if k in d)
            diag_keys_score = present_keys / max(1, len(req_keys))
            mi = d.get("missing_index", [])
            if isinstance(mi, list):
                low = [str(x).lower() for x in mi]
                if all(c.lower() in low for c in fix_must):
                    diag_idx = 1.0
                elif any(c.lower() in low for c in fix_must):
                    diag_idx = 0.5
            tbq = str(d.get("top_blocking_query", ""))
            if all(b in tbq for b in bad_subs[:3]):
                diag_q = 1.0
            elif "UPDATE" in tbq.upper() and "invoices" in tbq:
                diag_q = 0.5
        except Exception:
            pass
    s["diagnosis_keys"] = diag_keys_score
    s["diagnosis_missing_index_match"] = diag_idx
    s["diagnosis_top_query_match"] = diag_q

    # 11. postmortem
    pm = _read("postmortem.md")
    pm_chars = len(pm)
    s["postmortem_length"] = 1.0 if pm_chars >= 600 else pm_chars / 600.0
    pm_kws = expected.get("expected_postmortem_keywords",
                          ["deadlock", "innodb", "index", "explain",
                           "workbench", "perf_schema", "slowlog"])
    hits = sum(1 for k in pm_kws if k.lower() in pm.lower())
    s["postmortem_keywords"] = hits / max(1, len(pm_kws))
    sects = expected.get("expected_postmortem_sections",
                         ["## 时间线", "## 根因", "## 修复",
                          "## 跨通道证据链"])
    sect_hits = sum(1 for h in sects if h in pm)
    s["postmortem_sections"] = sect_hits / max(1, len(sects))

    # 12. cross-channel switches
    cc = rd / "cross_channel.json"
    cc_ok = 0.0
    if cc.exists():
        try:
            d = json.loads(cc.read_text())
            sw = int(d.get("switches", 0))
            tr = d.get("trace", [])
            if sw >= 5 and isinstance(tr, list) and len(tr) >= 5:
                struct_n = sum(1 for x in tr if isinstance(x, str) and x.startswith("STRUCT:"))
                visual_n = sum(1 for x in tr if isinstance(x, str) and x.startswith("VISUAL:"))
                cc_ok = 1.0 if (struct_n >= 2 and visual_n >= 2) else 0.6
            elif sw >= 3:
                cc_ok = 0.4
        except Exception:
            pass
    s["cross_channel_switches"] = cc_ok

    # 13. VLM rubric
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    vlm_imgs = [str(rd / n) for n in shots if (rd / n).exists()]
    vlm_judge = 0.0
    if vlm_score_rubric and vlm_imgs:
        rubric = {
            "vlm_workbench_real":
                "至少一张截图清晰显示 MySQL Workbench 主窗口，含左侧 Navigator (Management/Performance/Schemas) + 中央活体面板",
            "vlm_visual_explain_tree":
                "view_05 / view_06 至少一张能看到 Workbench Visual Explain 的节点树（带颜色编码的表 / 索引节点 + cost label）",
            "vlm_plan_color_change":
                "对比 view_05 与 view_06，可以看出 plan 节点颜色明显从偏红/橙变为偏绿/黄（即从 range/ALL 变为 ref/eq_ref）",
            "vlm_connections_grid":
                "view_02 显示 Client Connections grid 至少 6 行 process，且 State / Info 列可读",
        }
        vlm = vlm_score_rubric(vlm_imgs[:7], rubric,
            instruction="评估 DBA 在 MySQL Workbench 中排查 InnoDB 锁竞争的截图。")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method", "failed")
        vlm_judge = sum(s.get(k, 0.0) for k in rubric) / max(1, len(rubric))
    else:
        for k in ("vlm_workbench_real", "vlm_visual_explain_tree",
                  "vlm_plan_color_change", "vlm_connections_grid"):
            s[k] = 0.5
        vlm_judge = 0.5

    # Aggregate
    nums = [v for k, v in s.items()
            if isinstance(v, (int, float)) and k != "judge_method"]
    base = sum(nums) / max(1, len(nums))

    # Hard gates
    has_cli = (s["innodb_engine_status"] >= 0.5
               and s["lock_wait_samples"] >= 0.4
               and s["slow_log_present"] >= 0.4)
    if not has_cli: base = min(base, 0.4)
    # NOTE: GUI invocation is not a scoring axis; missing PNGs already
    # cost the gui_screenshots_count / vlm_* sub_scores.
    # Only enforce VLM cap when the helper actually ran.
    if vlm_score_rubric is not None and vlm_judge < 0.6:
        base = min(base, 0.6)
    if (s["remediation_ddl_ok"] == 0
            and s["index_after_present"] == 0):
        base = min(base, 0.45)
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
