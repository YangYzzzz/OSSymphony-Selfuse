"""
Reward Script: Apply strikethrough and gray color to last paragraph of document
Task ID: osworld_writer_strikethrough_last_para_008
Domain: libreoffice_writer
Scoring:
  - Component 1: All text runs in last paragraph have strikethrough formatting (0.5 pts)
  - Component 2: All text runs in last paragraph have gray font color (0.5 pts)
  Total: 1.0
"""

import os
from math import sqrt

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_strikethrough_last_para_008'


def color_distance(c1, c2):
    """Euclidean distance between two RGB color tuples."""
    return sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Apply strikethrough AND gray font color to all text in the last paragraph.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document — if it fails, no points possible
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition check: document must have at least one paragraph with text
    paragraphs = doc.paragraphs
    non_empty_paras = [p for p in paragraphs if p.text.strip()]
    if not non_empty_paras:
        print("CRITICAL: Document has no non-empty paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # Identify the last paragraph (last with non-empty text)
    last_para = non_empty_paras[-1]
    print(f"INFO: Last paragraph text (first 120 chars): {repr(last_para.text[:120])}")

    # Get runs with actual text content
    text_runs = [run for run in last_para.runs if run.text.strip()]
    if not text_runs:
        print("FAIL: Last paragraph has no text runs")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Last paragraph has {len(text_runs)} text run(s)")

    # Component 1: All text runs in the last paragraph have strikethrough formatting (0.5 points)
    try:
        all_strike = all(run.font.strike is True for run in text_runs)
        if all_strike:
            print(f"PASS: Component 1 — All {len(text_runs)} run(s) in last paragraph have strikethrough (0.5 pts)")
            total_score += 0.5
        else:
            strike_statuses = [(repr(run.text[:40]), run.font.strike) for run in text_runs]
            print(f"FAIL: Component 1 — Not all runs have strikethrough. Details: {strike_statuses}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check strikethrough: {e}")

    # Component 2: All text runs in the last paragraph have gray font color (0.5 points)
    # Gray is defined as a color close to RGB(128, 128, 128) (#808080).
    # We accept any gray-like color: R≈G≈B and distance from target gray < 80.
    # The exact golden value is RGB(128, 128, 128).
    try:
        # Target gray: RGB(128, 128, 128)
        gray_target = (128, 128, 128)

        def run_is_gray(run):
            """Return (ok, msg) for whether run has gray color."""
            color = run.font.color.rgb
            label = repr(run.text[:40])
            if color is None:
                return False, f"Run {label} has no explicit color (color=None)"
            r, g, b = color[0], color[1], color[2]
            dist = color_distance((r, g, b), gray_target)
            channel_spread = max(r, g, b) - min(r, g, b)
            if dist > 80:
                return False, f"Run {label} color RGB({r},{g},{b}) not gray (dist={dist:.1f})"
            if channel_spread > 60:
                return False, f"Run {label} color RGB({r},{g},{b}) has spread={channel_spread}, not gray"
            return True, f"Run {label} color RGB({r},{g},{b}) is gray (dist={dist:.1f}, spread={channel_spread})"

        gray_results = [run_is_gray(run) for run in text_runs]
        failed_gray = [(ok, msg) for ok, msg in gray_results if not ok]

        for ok, msg in gray_results:
            prefix = "INFO" if ok else "FAIL: Component 2 —"
            print(f"{prefix} {msg}")

        if not failed_gray:
            print(f"PASS: Component 2 — All {len(text_runs)} run(s) in last paragraph have gray font color (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 2 — Not all runs in last paragraph have gray font color")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check font color: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
