"""
Reward Script: Survey data analysis pipeline task
Task ID: osworld_multi_apps_code_script_output_010
Domain: multi_apps (libreoffice_calc + os + python scripting)

Scoring rubric:
  Component 1: CSV export exists at /home/user/data/survey_results.csv              (0.15 pts)
  Component 2: Python pipeline script exists at /home/user/scripts/survey_pipeline.py (0.15 pts)
  Component 3: Correlation heatmap PNG exists at /home/user/Desktop/correlation_heatmap.png (0.15 pts)
  Component 4: JSON report exists with all 3 required keys                           (0.35 pts)
  Component 5: improvement_areas in JSON contains correct questions (mean < 3.0)    (0.20 pts)
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_script_output_010'

CSV_PATH = f'{WORKDIR}/data/survey_results.csv'
PIPELINE_PATH = f'{WORKDIR}/scripts/survey_pipeline.py'
HEATMAP_PATH = f'{WORKDIR}/Desktop/correlation_heatmap.png'
JSON_REPORT_PATH = f'{WORKDIR}/data/survey_analysis.json'

REQUIRED_JSON_KEYS = {'descriptive_stats', 'improvement_areas', 'total_responses'}
# Ground truth from the golden artifact: questions with mean < 3.0
EXPECTED_IMPROVEMENT_AREAS = {'Q2', 'Q3', 'Q5'}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: CSV export exists (0.15 points)
    # The task requires exporting survey_results.ods to CSV via terminal.
    # Initial state only has the .ods file; the .csv is a task-introduced artifact.
    try:
        if os.path.isfile(CSV_PATH):
            # Validate it looks like a valid CSV with at least some content
            with open(CSV_PATH, 'r') as f:
                first_line = f.readline().strip()
            if first_line:
                print(f"PASS: Component 1 — CSV exported at {CSV_PATH} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — CSV file exists but is empty at {CSV_PATH}")
        else:
            print(f"FAIL: Component 1 — CSV not found at {CSV_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Python pipeline script exists (0.15 points)
    # The task requires writing a full analysis pipeline at /home/user/scripts/survey_pipeline.py.
    # Initial state has no scripts directory; this is entirely a task-introduced artifact.
    try:
        if os.path.isfile(PIPELINE_PATH):
            # Validate it's non-trivially a Python script
            with open(PIPELINE_PATH, 'r') as f:
                content = f.read()
            if len(content) > 100 and ('import' in content or 'def ' in content):
                print(f"PASS: Component 2 — Pipeline script found at {PIPELINE_PATH} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Pipeline script exists but appears too minimal at {PIPELINE_PATH}")
        else:
            print(f"FAIL: Component 2 — Pipeline script not found at {PIPELINE_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correlation heatmap PNG exists on Desktop (0.15 points)
    # The task requires generating a heatmap saved as /home/user/Desktop/correlation_heatmap.png.
    # Initial state Desktop is empty; this is a task-introduced artifact.
    try:
        if os.path.isfile(HEATMAP_PATH):
            heatmap_size = os.path.getsize(HEATMAP_PATH)
            if heatmap_size > 1000:
                print(f"PASS: Component 3 — Heatmap PNG found at {HEATMAP_PATH} (size={heatmap_size} bytes, 0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Heatmap PNG exists but is suspiciously small ({heatmap_size} bytes)")
        else:
            print(f"FAIL: Component 3 — Heatmap PNG not found at {HEATMAP_PATH}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: JSON report exists with all 3 required keys (0.35 points)
    # The task requires writing survey_analysis.json with keys:
    #   descriptive_stats, improvement_areas, total_responses
    # Initial state has no such JSON file; this is a task-introduced artifact.
    json_report = None
    try:
        if os.path.isfile(JSON_REPORT_PATH):
            with open(JSON_REPORT_PATH, 'r') as f:
                json_report = json.load(f)
            missing_keys = REQUIRED_JSON_KEYS - set(json_report.keys())
            if not missing_keys:
                print(f"PASS: Component 4 — JSON report has all required keys {REQUIRED_JSON_KEYS} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 4 — JSON report missing keys: {missing_keys}. Found keys: {set(json_report.keys())}")
        else:
            print(f"FAIL: Component 4 — JSON report not found at {JSON_REPORT_PATH}")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 4 — JSON report is malformed: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: improvement_areas contains correct questions with mean < 3.0 (0.20 points)
    # The task defines improvement areas as questions with mean score below 3.0.
    # Based on the ground truth, Q2 (mean=2.8), Q3 (mean=2.95), Q5 (mean=2.575) are below 3.0.
    # This check is meaningful only if Component 4 passed (json_report loaded).
    try:
        if json_report is not None and 'improvement_areas' in json_report:
            actual_areas = set(json_report['improvement_areas'])
            if actual_areas == EXPECTED_IMPROVEMENT_AREAS:
                print(f"PASS: Component 5 — improvement_areas correct: {sorted(actual_areas)} (0.20 pts)")
                total_score += 0.20
            else:
                # Check partial overlap (some areas identified correctly)
                overlap = actual_areas & EXPECTED_IMPROVEMENT_AREAS
                if overlap and len(overlap) >= 2:
                    print(f"FAIL: Component 5 — improvement_areas partially correct. "
                          f"Expected {sorted(EXPECTED_IMPROVEMENT_AREAS)}, got {sorted(actual_areas)}")
                else:
                    print(f"FAIL: Component 5 — improvement_areas incorrect. "
                          f"Expected {sorted(EXPECTED_IMPROVEMENT_AREAS)}, got {sorted(actual_areas)}")
        elif json_report is None:
            print("FAIL: Component 5 — JSON report not loaded, cannot verify improvement_areas")
        else:
            print("FAIL: Component 5 — 'improvement_areas' key missing from JSON report")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
