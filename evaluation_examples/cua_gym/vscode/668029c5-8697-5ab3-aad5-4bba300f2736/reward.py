"""
FINAL REWARD SCRIPT - SUCCESS
Task: While working in /home/user/ml_project/models.py, I need a quick way to display my scikit-learn RandomForestClassifier’s feature importances and tree diagram directly in VS Code—how can I set that up?
Generated: 2025-09-12 00:15:36
Status: success
Model: azure-o3
Total Steps: 8
"""

import json
import pathlib
import re


def _strip_json_comments(text: str) -> str:
    """Remove // comments from JSON5-like text while respecting quoted strings."""
    cleaned_lines = []
    for line in text.splitlines():
        new_line = ""
        i, in_str, str_char = 0, False, ""
        while i < len(line):
            ch = line[i]
            if in_str:
                new_line += ch
                # handle escaped characters inside strings
                if ch == "\\" and i + 1 < len(line):
                    new_line += line[i + 1]
                    i += 1
                elif ch == str_char:
                    in_str = False
            else:
                if ch in ("'", '"'):
                    in_str = True
                    str_char = ch
                    new_line += ch
                elif ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
                    break  # start of // comment
                else:
                    new_line += ch
            i += 1
        if new_line.strip():
            cleaned_lines.append(new_line)
    return "\n".join(cleaned_lines)


def _parse_tasks_json(path: pathlib.Path):
    """Return parsed JSON data (dict) or (None, error_msg)."""
    try:
        raw = path.read_text()
    except FileNotFoundError:
        return None, "tasks.json missing"

    cleaned = _strip_json_comments(raw)
    try:
        return json.loads(cleaned), None
    except json.JSONDecodeError as e:
        return None, f"JSON decode error: {e}"


def verify_task() -> float:
    """Verify that the VS Code workflow for RandomForest visualisation is set up properly."""

    workspace = pathlib.Path("/home/user/ml_project")
    score = 0.0  # progressive scoring

    # ------------------------------------------------------------------
    # 1. Check for helper script that performs the visualisation
    # ------------------------------------------------------------------
    script_path = workspace / "scripts" / "visualise_rf.py"
    if script_path.exists():
        print(f"✓ Found visualisation script: {script_path}")
        content = script_path.read_text()

        has_importance_plot = "feature_importances_" in content
        has_tree_plot = "plot_tree" in content
        if has_importance_plot and has_tree_plot:
            print("  ✓ Script plots feature importances AND tree diagram (0.4 points)")
            score += 0.4
        else:
            print("  ✗ Script missing either importance plot or tree diagram (0 points)")
    else:
        print("✗ visualise_rf.py not found (0 points)")

    # ------------------------------------------------------------------
    # 2. Validate VS Code task configuration that runs this script
    # ------------------------------------------------------------------
    tasks_path = workspace / ".vscode" / "tasks.json"
    tasks_data, err = _parse_tasks_json(tasks_path)
    if tasks_data is None:
        print(f"✗ Unable to read tasks.json: {err} (0 points)")
    else:
        found_task = False
        for task in tasks_data.get("tasks", []):
            label = (task.get("label") or task.get("name") or "").lower()
            args = task.get("args", []) if isinstance(task.get("args", []), list) else []
            if "visualise" in label and "randomforest" in label:
                if any("visualise_rf.py" in str(arg) for arg in args):
                    found_task = True
                    break
        if found_task:
            print("✓ VS Code task calls visualise_rf.py (0.4 points)")
            score += 0.4
        else:
            print("✗ No suitable VS Code task configured (0 points)")

    # ------------------------------------------------------------------
    # 3. Bonus: script should save PNGs AND auto-open them via `code -r`
    # ------------------------------------------------------------------
    if script_path.exists():
        saves_png = ".png" in content
        opens_in_vscode = re.search(r"code[\'\"]?\s*,?\s*-r", content) is not None
        if saves_png and opens_in_vscode:
            print("✓ Script saves PNGs and opens them in the current VS Code window (0.2 points)")
            score += 0.2
        else:
            print("✗ Script does not both save PNGs and open them via VS Code CLI (0 points)")

    # ------------------------------------------------------------------
    final_score = min(score, 1.0)
    print(f"Total score: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()
