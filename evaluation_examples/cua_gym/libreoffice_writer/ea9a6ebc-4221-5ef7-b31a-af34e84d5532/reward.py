"""
Reward Script: Change font color of all section headings to dark blue (#003366)
Task ID: writer_txtfmt_018
Domain: libreoffice_writer
Scoring:
  Component 1: 'Introduction' heading color == #003366 (0.25 pts)
  Component 2: 'Background' heading color == #003366 (0.25 pts)
  Component 3: 'Analysis' heading color == #003366 (0.25 pts)
  Component 4: 'Conclusion' heading color == #003366 (0.25 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import RGBColor

WORKDIR = '/home/user'
TASK_ID = 'writer_txtfmt_018'

# Target headings and their expected properties
HEADING_TEXTS = ['Introduction', 'Background', 'Analysis', 'Conclusion']
TARGET_COLOR = RGBColor(0x00, 0x33, 0x66)  # #003366 dark blue


def color_distance(c1, c2):
    """Compute Euclidean RGB distance between two RGBColor objects.
    RGBColor is a tuple subclass: c[0]=R, c[1]=G, c[2]=B.
    """
    from math import sqrt
    return sqrt(sum((a - b) ** 2 for a, b in zip(
        (c1[0], c1[1], c1[2]),
        (c2[0], c2[1], c2[2])
    )))


def verify_task(file_path):
    """
    Verify that each of the four section headings has its font color changed to
    dark blue (#003366).

    Strategy:
    - Identify paragraphs whose text exactly matches one of the four heading strings.
    - For each such paragraph, check that all non-empty runs have font color == #003366.
    - Each heading that passes earns 0.25 points (total = 1.0).
    - Body text color is not scored (not a task-introduced change).

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a lookup: heading_text -> list of paragraph objects that match
    heading_paragraphs = {h: [] for h in HEADING_TEXTS}
    for para in doc.paragraphs:
        text = para.text.strip()
        if text in heading_paragraphs:
            heading_paragraphs[text].append(para)

    for heading in HEADING_TEXTS:
        paragraphs = heading_paragraphs[heading]

        # Component: '<heading>' heading color == #003366 (0.25 pts)
        try:
            if not paragraphs:
                print(f"FAIL: Component '{heading}' — paragraph not found in document")
                continue

            # Take the first matching paragraph (there should be exactly one)
            para = paragraphs[0]
            runs = [r for r in para.runs if r.text.strip()]

            if not runs:
                print(f"FAIL: Component '{heading}' — no non-empty runs found")
                continue

            # Check all runs in the heading paragraph have color #003366
            # Count runs that fail the color check; pass only when failed_count == 0
            failed_count = 0
            for run in runs:
                try:
                    run_color = run.font.color.rgb if (run.font.color and run.font.color.type) else None
                except Exception:
                    run_color = None

                if run_color is None:
                    print(f"FAIL: Component '{heading}' — run '{run.text}' has no explicit color (inherited)")
                    failed_count += 1
                    break

                dist = color_distance(run_color, TARGET_COLOR)
                if dist > 10:
                    print(f"FAIL: Component '{heading}' — run '{run.text}' color={run_color!r}, expected #003366 (distance={dist:.1f})")
                    failed_count += 1
                    break
                else:
                    print(f"PASS: Component '{heading}' — run '{run.text}' color={run_color!r} matches #003366 (distance={dist:.1f})")

            if failed_count == 0:
                total_score += 0.25

        except Exception as e:
            print(f"ERROR: Component '{heading}' — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/policy_brief.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
