# Auto-generated from WeaveBench task WEB_task_0_iframe_3layer_form.
import inspect
import json
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "/opt/eval")
sys.path.insert(0, "/tmp_workspace/gt")

def grade(workspace_path=None, **kwargs) -> dict:
    import re
    from pathlib import Path
    try:
        from _judge_helper import vlm_score_rubric
    except Exception:
        vlm_score_rubric = None
    rd = Path("/tmp_workspace/results")
    scores = {}

    png = rd / "quote.png"
    png_size = png.stat().st_size if png.exists() else 0
    scores["quote_png"] = 1.0 if png.exists() and png_size >= 5120 else 0.0
    scores["quote_png_size_ok"] = 1.0 if png_size >= 20480 else (0.5 if png_size >= 5120 else 0.0)

    amt_path = rd / "quote_amount.txt"
    amt = amt_path.read_text().strip() if amt_path.exists() else ""
    scores["amount_format"] = 1.0 if re.fullmatch(r"¥[\d,]+\.\d{2}", amt) else 0.0
    m = re.search(r"¥([\d,]+)\.\d{2}", amt)
    try:
        amt_val = int(m.group(1).replace(",", "")) if m else 0
    except Exception:
        amt_val = 0
    scores["amount_reasonable"] = 1.0 if 100 <= amt_val <= 100000 else 0.0

    log = Path("/tmp_workspace/server.log").read_text() if Path("/tmp_workspace/server.log").exists() else ""
    scores["submitted"] = 1.0 if "POST /submit_quote" in log else 0.0
    scores["name_ok"] = 1.0 if ("张三" in log or "%E5%BC%A0%E4%B8%89" in log) else 0.0
    scores["plate_ok"] = 1.0 if ("京A12345" in log or "%E4%BA%ACA12345" in log) else 0.0
    scores["brand_ok"] = 1.0 if "Toyota" in log else 0.0
    scores["model_ok"] = 1.0 if "Camry" in log else 0.0
    scores["dob_ok"] = 1.0 if "1990-05-15" in log else 0.0
    scores["no_bot_flag"] = 0.0 if "bot_detected" in log else 1.0

    core_keys = ["submitted", "name_ok", "plate_ok", "brand_ok", "model_ok", "dob_ok", "no_bot_flag"]
    aux_keys = ["quote_png", "quote_png_size_ok", "amount_format", "amount_reasonable"]
    core = sum(scores[k] for k in core_keys) / len(core_keys)
    aux = sum(scores[k] for k in aux_keys) / len(aux_keys)
    base = 0.65 * core + 0.35 * aux

    if scores["submitted"] < 1.0:
        base = min(base, 0.40)
    if scores["name_ok"] < 1.0 or scores["plate_ok"] < 1.0:
        base = min(base, 0.45)
    if scores["quote_png"] < 1.0:
        base = min(base, 0.35)
    if scores["amount_format"] < 1.0:
        base = min(base, 0.55)
    if scores["no_bot_flag"] < 1.0:
        base = min(base, 0.50)

    if vlm_score_rubric and png.exists() and png_size >= 5120:
        rubric = {
            "vlm_quote_visible": "截图清晰显示报价金额（含 ¥ 符号或数字），且金额数字可读",
            "vlm_result_page": "页面是 quote_result.html 风格的报价结果页（不是表单中间步骤）",
            "vlm_no_error_overlay": "页面没有错误提示、bot_detected 红条、HTTP 5xx 等异常",
        }
        vlm = vlm_score_rubric([str(png)], rubric, instruction="评估 iframe 多步表单填写完成后跳转到的报价结果截图。")
        for k in rubric: scores[k] = vlm.get(k, 0.0)
        scores["judge_method"] = vlm.get("judge_method", "failed")
        vlm_avg = sum(vlm.get(k, 0.0) for k in rubric) / len(rubric)
        if scores.get("judge_method") == "failed":
            overall = min(base, 0.6)
        else:
            overall = 0.7 * base + 0.3 * vlm_avg
            if vlm_avg < 0.5:
                overall = min(overall, 0.55)
            if vlm_avg < 0.3:
                overall = min(overall, 0.40)
        scores["overall_score"] = round(overall, 3)
    else:
        scores["judge_method"] = "no_vlm"
        scores["overall_score"] = round(min(base, 0.6), 3)
    return scores


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
