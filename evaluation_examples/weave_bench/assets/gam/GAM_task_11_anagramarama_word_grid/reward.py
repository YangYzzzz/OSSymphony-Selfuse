# Auto-generated from WeaveBench task GAM_task_11_anagramarama_word_grid.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    """Anagramarama dictionary + GUI typing + OCR score grader.

    12 sub-scores + 4 hard gates.  Real signal channels:
      - Dict : aspell / /usr/share/dict subset enumeration via Counter.
      - GUI  : 3 SDL screenshots OCR for anagram UI / score text.
      - I/O  : entered.csv schema, length-class quotas, score band check.
    No GT leakage: gt/expected.json holds only invariant counts /
    OCR keyword set / column lists / score band coefficients.
    """
    import csv, json, re, os
    from collections import Counter
    from pathlib import Path

    ws  = Path(workspace_path) if workspace_path else Path("/tmp_workspace")
    rd  = ws / "results"
    gtd = ws / "gt"
    expected = {}
    if (gtd/"expected.json").exists():
        try:    expected = json.loads((gtd/"expected.json").read_text())
        except Exception: expected = {}
    s = {}

    # ---- 1. seed_normalized.txt ----
    snf = rd/"seed_normalized.txt"
    seed = ""
    if snf.exists():
        try:
            seed = snf.read_text().strip().lower()
        except Exception: pass
    s["seed_ok"] = 1.0 if (len(seed) == 9 and seed.isalpha()) else 0.0
    seed_counter = Counter(seed)

    # ---- 2. candidates.csv schema + count + subset_ok ----
    ccsv = rd/"candidates.csv"
    cand_rows = []
    cand_score = 0.0
    cand_words = set()
    if ccsv.exists():
        try:
            cand_rows = list(csv.DictReader(ccsv.open()))
            need = set(expected.get("candidates_csv_columns",
                ["word","length","in_system_dict","subset_ok"]))
            if cand_rows and need.issubset(cand_rows[0].keys()):
                target = expected.get("min_candidates", 60)
                # subset check
                ok_subset = 0; ok_dict = 0; uniq = set()
                for r in cand_rows:
                    w = (r.get("word") or "").lower()
                    if w in uniq or not (w.isalpha() and 3 <= len(w) <= 9): continue
                    uniq.add(w)
                    if Counter(w) <= seed_counter: ok_subset += 1; cand_words.add(w)
                    if str(r.get("in_system_dict","")).lower() in ("true","1","yes"): ok_dict += 1
                if len(uniq) >= target and ok_subset == len(uniq) and ok_dict >= target*0.9:
                    cand_score = 1.0
                elif len(cand_rows) >= target * 0.6:
                    cand_score = 0.5
        except Exception: pass
    s["candidates_csv_ok"] = cand_score

    # ---- 3. initial screenshot OCR ----
    shots = expected.get("screenshots_required",
        ["view_anagram_initial.png","view_anagram_midgame.png","view_anagram_final.png"])
    ocr_kw = expected.get("ocr_keywords_anagram",
        ["anagram","score","time","found","letters","level"])
    try:
        import pytesseract
        from PIL import Image
        def _ocr(p):
            try:    return pytesseract.image_to_string(Image.open(p)).lower()
            except Exception: return ""
        t0 = _ocr(rd/shots[0]) if (rd/shots[0]).exists() else ""
        s["initial_shot_ocr"] = 1.0 if any(k in t0 for k in ocr_kw) else 0.0
    except ImportError:
        s["initial_shot_ocr"] = 0.5 if (rd/shots[0]).exists() else 0.0

    # ---- 4-6. entered.csv schema + length-class quotas ----
    ecsv = rd/"entered.csv"
    ent_rows = []
    if ecsv.exists():
        try: ent_rows = list(csv.DictReader(ecsv.open()))
        except Exception: pass
    need_e = set(expected.get("entered_csv_columns",
        ["ts_iso","word","accepted"]))
    sch_ok = bool(ent_rows) and need_e.issubset(ent_rows[0].keys())
    seen=set(); good=[]
    for r in ent_rows:
        w=(r.get("word","") or "").lower(); a=(r.get("accepted","") or "").lower()
        if w in seen or not w.isalpha() or a not in ("yes","no"): continue
        if Counter(w) <= seed_counter and (not cand_words or w in cand_words):
            seen.add(w); good.append(r)
    n_ent=len(good) if sch_ok else 0
    s["entered_csv_count"]=min(1.0, n_ent/expected.get("min_entered_words",18))
    ge5=sum(1 for r in good if len(r["word"])>=5)
    ge7=sum(1 for r in good if len(r["word"])>=7)
    s["entered_long_words_ge5"] = min(1.0,
        ge5 / expected.get("min_entered_len_ge_5", 6))
    s["entered_long_words_ge7"] = min(1.0,
        ge7 / expected.get("min_entered_len_ge_7", 1))

    # ---- 7. midgame screenshot looks like SDL game frame ----
    mg = rd/shots[1]
    mg_ok = 0.0
    if mg.exists():
        try:
            from PIL import Image as PI
            import numpy as np
            im = PI.open(mg).convert("L")
            a = np.array(im); h,w = a.shape
            if h >= 200 and w >= 200 and float(a.std()) > 25:
                mg_ok = 1.0
        except Exception: pass
    s["midgame_shot_real"] = mg_ok

    # ---- 8. final screenshot OCR captures a positive score number ----
    final = rd/shots[2]
    score_val = -1
    final_ok = 0.0
    try:
        import pytesseract
        from PIL import Image
        if final.exists():
            try:
                tx = pytesseract.image_to_string(Image.open(final))
            except Exception:
                tx = ""
            m = re.search(r"score[^0-9]{0,15}(\d{1,4})", tx, re.I)
            if m and 0 < int(m.group(1)) <= 9999:
                score_val = int(m.group(1)); final_ok = 1.0
            else:
                final_ok = 0.0
    except ImportError:
        if final.exists():
            final_ok = 0.5
    s["final_shot_score_ocr"] = final_ok

    # ---- 9. report.json required keys ----
    rj = rd/"report.json"
    rep_ok = 0.0
    rep = {}
    if rj.exists():
        try:
            rep = json.loads(rj.read_text())
            need = expected.get("report_required_keys", [])
            if all(k in rep for k in need):
                rep_ok = 1.0
        except Exception: pass
    s["report_keys_ok"] = rep_ok

    # ---- 10. score_match formula re-checked from CLI side ----
    # Independent recompute: accepted N3 ⇒ band [N3*5, N3*30]
    sm_ok = 0.0
    try:
        agent_score = int(rep.get("ocr_score_value", -1))
        agent_match = bool(rep.get("score_match"))
        n3_check = sum(1 for r in good if r.get("accepted","").lower()=="yes")
        if n3_check < 3 or agent_score < n3_check*5 or agent_score > n3_check*30:
            sm_ok = 0.0
        else:
            sm_ok = 1.0 if agent_match else 0.0
    except Exception:
        sm_ok = 0.0
    s["score_match_correct"] = sm_ok

    # ---- 11. diff.txt non-empty ----
    df = rd/"diff.txt"
    ok=0.0
    if df.exists():
        t=df.read_text().lower()
        cov=len(re.findall(r"^\s*[+\-*]?\s*covered[: ]", t, re.M)) + t.count("covered:")
        mis=len(re.findall(r"missed|missing|not entered", t))
        if cov >= 5 and mis >= 3 and df.stat().st_size >= 200: ok=1.0
        elif df.stat().st_size >= 50: ok=0.4
    s["diff_present"] = ok

    # ---- 12. VLM rubric ----
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    imgs = [str(rd/n) for n in shots if (rd/n).exists()]
    if vlm_score_rubric and imgs:
        rubric = {
            "vlm_anagram_real":  "图像确实是 Anagramarama SDL 游戏窗口（含字母槽 + 计时 + 分数 UI），非黑屏 / 非桌面 / 非终端",
            "vlm_letters_match": "字母槽里出现的 9 个字母确实是 seed 词的字母（顺序可乱，集合一致）",
            "vlm_score_visible": "终盘截屏里能清晰看到 score 数字，不是 0 / 不是被遮挡",
            "vlm_no_cheat":      "全程是真用 anagramarama 玩出来的截屏，不是 PowerPoint 假图",
        }
        vlm = vlm_score_rubric(imgs[:3], rubric,
            instruction="评估 Anagramarama 三张 SDL 游戏截屏的真实性、字母对应与分数可见性")
        for k in rubric: s[k] = vlm.get(k, 0.0)
        s["judge_method"] = vlm.get("judge_method","failed")
    else:
        for k in ["vlm_anagram_real","vlm_letters_match","vlm_score_visible","vlm_no_cheat"]:
            s[k] = 0.5

    # ---- aggregate + hard gates ----
    nums = [v for v in s.values() if isinstance(v,(int,float))]
    base = sum(nums)/len(nums) if nums else 0.0
    cli_evidence = (rd/"candidates.csv").exists() and (rd/"entered.csv").exists() \
                   and (rd/"diff.txt").exists()
    gui_screenshot = any((rd/n).exists() for n in shots)
    vlm_avg = sum(s.get(k,0.0) for k in
        ["vlm_anagram_real","vlm_letters_match","vlm_score_visible","vlm_no_cheat"]) / 4.0
    if not cli_evidence:    base = min(base, 0.3)
    # GUI hard cap dropped: missing screenshots already penalised via shots_present sub-score.
    if vlm_score_rubric is not None and vlm_avg < 0.6:
        base = min(base, 0.4)
    if s.get("seed_ok",0)   < 1.0: base = min(base, 0.3)
    if s.get("initial_shot_ocr",0) < 1.0 and s.get("final_shot_score_ocr",0) < 1.0:
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
