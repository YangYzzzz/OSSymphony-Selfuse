# Auto-generated from WeaveBench task DSK_task_1_file_conflict_resolve.
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
    gt_path = (workspace.parent / "gt" / "expected.json")
    if not gt_path.exists():
        gt_path = workspace / "gt" / "expected.json"
    gt = json.loads(gt_path.read_text()) if gt_path.exists() else {}
    skip_truth = set(gt.get("skip_files",[])); replace_truth = set(gt.get("replace_files",[]))
    s = {}
    dest = workspace/"dest"
    files = list(dest.glob("*")) if dest.exists() else []
    s["dest_count"] = 1.0 if len(files) >= gt.get("expected_dst_min_count",100) else len(files)/max(gt.get("expected_dst_min_count",100),1)
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
        s["log_lines"] = min(1.0, len(rows)/30)
        s["log_dual_decisions"] = 1.0 if {r.get("decision","") for r in rows} >= {"skip","replace"} else 0.0
        # decision-vs-truth alignment
        ok=0
        for r in rows:
            d=r.get("decision",""); fn=r.get("filename","")
            if (d=="skip" and fn in skip_truth) or (d=="replace" and fn in replace_truth): ok+=1
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
    min_shots = gt.get("min_conflict_screens",10)
    # Anti-cheat: require non-trivial PNGs (>=5KB) and md5 uniqueness across shots.
    valid_pngs = [p for p in pngs if p.stat().st_size >= 5*1024]
    md5s = set()
    for p in valid_pngs:
        try: md5s.add(hashlib.md5(p.read_bytes()).hexdigest())
        except: pass
    s["conflict_screenshots"] = min(1.0, len(valid_pngs)/min_shots)
    s["conflict_unique_md5"] = min(1.0, len(md5s)/max(min_shots-2,1))
    if valid_pngs and pytesseract:
        ok = 0
        for p in valid_pngs[:8]:
            try:
                tx = pytesseract.image_to_string(Image.open(p))
                if any(k in tx for k in ["Conflict","已存在","Replace","Replace All","跳过","Skip"]): ok+=1
            except: pass
        s["conflict_ocr"] = min(1.0, ok/4)
        vlm_available = True
    else:
        s["conflict_ocr"] = 0.0
        vlm_available = False
    bak = sum(1 for p in files if re.search(r"\.bak\.\d+", p.name))
    s["bak_files"] = min(1.0, bak/gt.get("min_bak_files",5))
    log = workspace/"actions.log"
    if log.exists():
        txt = log.read_text(errors="ignore")
        s["no_cli_copy"] = 0.0 if re.search(r"\b(cp|rsync|mv)\s+-", txt) else 1.0
    else: s["no_cli_copy"] = 1.0

    # ---- Weighted aggregation: core 60% / gui 30% / aux 10% ----
    def avg(keys):
        vals=[s.get(k,0.0) for k in keys]
        return sum(vals)/len(vals) if vals else 0.0
    core_keys = ["dest_count","keep_intact","decision_truth_alignment","bak_files"]
    gui_keys  = ["conflict_screenshots","conflict_unique_md5","conflict_ocr"]
    aux_keys  = ["log_lines","log_dual_decisions","inventory_match","inventory_schema","no_cli_copy"]
    core, gui, aux = avg(core_keys), avg(gui_keys), avg(aux_keys)
    base = 0.6*core + 0.3*gui + 0.1*aux

    # ---- Hard gates (stricter than v1) ----
    # Core delivery gate: per-file decision must reflect a real GUI workflow,
    # not a guess. Without truth alignment the run is essentially blind.
    if s.get("decision_truth_alignment",0) < 0.6:
        base = min(base, 0.40)
    if s.get("decision_truth_alignment",0) < 0.3:
        base = min(base, 0.25)
    # GUI evidence gate: enough non-trivial shots AND md5 diversity (block static-fake).
    if s.get("conflict_screenshots",0) < 0.7 or s.get("conflict_unique_md5",0) < 0.7:
        base = min(base, 0.40)
    # Forbidden CLI: zero tolerance.
    if s.get("no_cli_copy",1) < 1.0:
        base = min(base, 0.35)
    # Keep-list integrity: if important originals are dropped, severe penalty.
    if s.get("keep_intact",0) < 0.9:
        base = min(base, 0.50)
    # Bak rename evidence: Replace path must be exercised.
    if s.get("bak_files",0) < 1.0:
        base = min(base, 0.55)
    # Dest count must hit threshold.
    if s.get("dest_count",0) < 1.0:
        base = min(base, 0.50)
    # OCR is soft. But if OCR (and thus VLM-style verification) is entirely
    # unavailable, a fully unverified run cannot exceed 0.6.
    if not vlm_available:
        base = min(base, 0.60)

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
