# Auto-generated from WeaveBench task DSK_task_1_dup_triage.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

from pathlib import Path
import csv, re, json, hashlib
from PIL import Image

def grade(workspace_path=None, **kwargs):
    workspace = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    """Stricter DSK_4: decisions per file must match real diff truth (gt/expected.json)."""
    try: import pytesseract
    except: pytesseract=None
    gt = json.loads(Path("/tmp_workspace/gt/expected.json").read_text()) if Path("/tmp_workspace/gt/expected.json").exists() else {}
    skip_truth = set(gt.get("skip_files",[])) | set(gt.get("skip_older_files",[]))
    replace_truth = set(gt.get("replace_files",[]))
    keep_both_truth = set(gt.get("keep_both_files",[]))
    skip_older_truth = set(gt.get("skip_older_files",[]))
    s = {}
    dest = workspace/"dest"
    files = list(dest.glob("*")) if dest.exists() else []
    s["dest_count"] = 1.0 if len(files) >= gt.get("expected_dst_min_count",150) else len(files)/max(gt.get("expected_dst_min_count",150),1)
    kl = workspace/"keep_list.txt"
    if kl.exists():
        keep = [l.strip() for l in kl.read_text().splitlines() if l.strip()]
        existing = set(p.name for p in files)
        intact = sum(1 for k in keep if any(k==n or n.startswith(k+".bak.") for n in existing))
        s["keep_intact"] = intact/max(len(keep),1)
    else: s["keep_intact"] = 0.0
    cl = workspace/"conflict_log.csv"
    if cl.exists():
        rows = list(csv.DictReader(cl.open()))
        s["log_lines"] = min(1.0, len(rows)/45)
        decisions_seen = {r.get("decision","") for r in rows}
        required = {"skip","replace","keep_both","skip_older"}
        s["log_dual_decisions"] = len(decisions_seen & required) / len(required)
        # decision-vs-truth alignment (4-class)
        ok=0
        for r in rows:
            d=r.get("decision",""); fn=r.get("filename","")
            if d=="skip" and (fn in skip_truth and fn not in skip_older_truth): ok+=1
            elif d=="skip_older" and fn in skip_older_truth: ok+=1
            elif d=="skip" and fn in skip_older_truth: ok+=1  # tolerate skip merged
            elif d=="replace" and fn in replace_truth: ok+=1
            elif d=="keep_both" and fn in keep_both_truth: ok+=1
        s["decision_truth_alignment"] = ok/max(len(rows),1)
    else:
        s["log_lines"]=0.0; s["log_dual_decisions"]=0.0; s["decision_truth_alignment"]=0.0
    fi = workspace/"final_inventory.csv"
    if fi.exists():
        rows = list(csv.DictReader(fi.open()))
        s["inventory_match"] = 1.0 if abs(len(rows)-len(files))<=2 else max(0, 1-abs(len(rows)-len(files))/len(files) if files else 0)
        s["inventory_schema"] = 1.0 if rows and all(k in rows[0] for k in ["filename","size","mtime","sha256"]) else 0.0
    else: s["inventory_match"]=0.0; s["inventory_schema"]=0.0
    pngs = list(workspace.glob("conflict_*.png"))
    # Filter out placeholder/blank screenshots (< 5KB) to defeat trivial fakes
    valid_pngs = [p for p in pngs if p.stat().st_size >= 5120]
    s["conflict_screenshots"] = min(1.0, len(valid_pngs)/gt.get("min_conflict_screens",15))
    # Anti-cheat: md5 uniqueness + min resolution
    uniq_md5 = set(); res_ok = 0
    for p in valid_pngs:
        try:
            uniq_md5.add(hashlib.md5(p.read_bytes()).hexdigest())
            with Image.open(p) as im:
                if im.size[0] >= 800 and im.size[1] >= 600: res_ok += 1
        except: pass
    s["conflict_unique"] = min(1.0, len(uniq_md5)/max(gt.get("min_conflict_screens",15),1))
    s["conflict_resolution"] = min(1.0, res_ok/max(gt.get("min_conflict_screens",15),1))
    if valid_pngs and pytesseract:
        ok = 0
        for p in valid_pngs[:12]:
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k in tx for k in ["Conflict","已存在","Replace","Replace All","跳过","Skip","Keep Both","保留"]): ok+=1
            except: pass
        s["conflict_ocr"] = min(1.0, ok/6)
        vlm_available = True
    else:
        s["conflict_ocr"]=0.0
        vlm_available = False
    bak_pat = re.compile(r"\.bak\.\d{9,10}$")
    bak = sum(1 for p in files if bak_pat.search(p.name))
    s["bak_files"] = min(1.0, bak/gt.get("min_bak_files",10))
    # keep_both: src 拷贝后 Nautilus 会生成 ` (copy)` 或 ` (1)` 后缀文件，与原 dst 同名基础
    if keep_both_truth and files:
        names = [p.name for p in files]
        kb_ok = 0
        for fn in keep_both_truth:
            base = fn.rsplit(".",1)[0]; ext = fn.rsplit(".",1)[1] if "." in fn else ""
            # 原文件存在 + 至少一个变体存在
            has_orig = fn in names
            has_variant = any((fn != n) and (base in n) and (ext == "" or n.endswith("."+ext)) for n in names)
            if has_orig and has_variant: kb_ok += 1
        s["keep_both_kept"] = kb_ok / len(keep_both_truth)
    else:
        s["keep_both_kept"] = 0.0
    # Forbidden CLI commands
    log = workspace/"actions.log"
    if log.exists():
        txt = log.read_text(errors="ignore")
        s["no_cli_copy"] = 0.0 if re.search(r"\b(cp|rsync|mv)\s+-", txt) else 1.0
    else: s["no_cli_copy"] = 1.0
    # v2 加权评分: 核心交付 60% / GUI 证据 30% / 辅助 10%
    core_keys = ["dest_count","keep_intact","log_lines","log_dual_decisions",
                 "decision_truth_alignment","inventory_match","inventory_schema",
                 "bak_files","keep_both_kept"]
    gui_keys  = ["conflict_screenshots","conflict_unique","conflict_resolution","conflict_ocr"]
    aux_keys  = ["no_cli_copy"]
    def _avg(keys):
        vals = [s[k] for k in keys if k in s and isinstance(s[k],(int,float))]
        return sum(vals)/len(vals) if vals else 0.0
    base = 0.6*_avg(core_keys) + 0.3*_avg(gui_keys) + 0.1*_avg(aux_keys)
    # Hard gate 1: GUI 证据 (截图数 + 唯一性 + 分辨率) 必须真实
    if s.get("conflict_screenshots",0) < 0.7: base = min(base, 0.4)
    if s.get("conflict_unique",0) < 0.6:      base = min(base, 0.40)  # 大量重复截图 = 伪造
    if s.get("conflict_resolution",0) < 0.6:  base = min(base, 0.45)  # 缩略图占位 = 退化
    # Hard gate 2: CLI 拷贝禁令
    if s.get("no_cli_copy",1) < 1.0: base = min(base, 0.35)
    # Hard gate 3: 核心交付物 (log + inventory + decision) 任一缺失
    if min(s.get("log_lines",0), s.get("inventory_schema",0), s.get("decision_truth_alignment",0)) < 0.5:
        base = min(base, 0.45)
    # Hard gate 4: decision 对齐严格梯度
    dta = s.get("decision_truth_alignment",0)
    if dta < 0.5: base = min(base, 0.35)
    elif dta < 0.7: base = min(base, 0.55)
    # Hard gate 5: dest_count
    if s.get("dest_count",0) < 0.85: base = min(base, 0.5)
    if s.get("dest_count",0) < 0.6:  base = min(base, 0.35)
    # Hard gate 6: keep_both/skip_older v2 升级专属——agent 不能整片忽略
    if s.get("keep_both_kept",0) < 0.4: base = min(base, 0.55)
    # Hard gate 7: VLM/OCR 不可用时封顶 0.6 (避免无证据满分)
    if not vlm_available: base = min(base, 0.6)
    s["overall_score"] = round(base, 3)

    # ----- BEGIN CHEAT/VLM HARD-GATE (auto-injected) -----
    try:
        from _judge_helper import audit_chat_jsonl_for_banned as _audit
    except Exception:
        _audit = None
    _BANS = ['rsync --ignore-existing', 'rsync -a --ignore', 'cp -an', 'cp -rn', 'cp --no-clobber', 'cp -fr ', 'cp -rf ']
    if _audit is not None:
        try:
            _a = _audit(_BANS)
            s["audit_total_tool_calls"] = _a.get("total_tool_calls", 0)
            s["audit_screenshots"] = _a.get("computer_screenshots", 0)
            s["audit_any_banned"] = 1.0 if _a.get("any_banned") else 0.0
            s["audit_matches"] = ",".join(_a.get("matches", [])[:5])
            if _a.get("any_banned") and _a.get("computer_screenshots", 0) == 0:
                s["overall_score"] = min(float(s.get("overall_score", 1.0)), 0.30)
            if _a.get("total_tool_calls", 0) >= 5 and _a.get("computer_screenshots", 0) == 0:
                s["overall_score"] = min(float(s.get("overall_score", 1.0)), 0.45)
        except Exception as _e:
            s["audit_error"] = str(_e)[:120]
    # ----- END CHEAT/VLM HARD-GATE -----
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
