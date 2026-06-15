"""
Reward Script: Apply Heading 3 style to four sub-sub-heading paragraphs
Task ID: writer_struct_030
Domain: libreoffice_writer
Scoring:
  - Component 1: 'Sampling Method' has Heading 3 style        (0.25 pts)
  - Component 2: 'Survey Design' has Heading 3 style          (0.25 pts)
  - Component 3: 'Control Group Selection' has Heading 3 style (0.25 pts)
  - Component 4: 'Data Normalization' has Heading 3 style     (0.25 pts)
  Total: 1.0
"""

import os

try:
    from docx import Document
except ImportError:
    print("CRITICAL: python-docx not installed")
    print("REWARD: 0.0")
    raise SystemExit

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_030'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'experiment_report.docx')

# Target paragraphs that must be changed to Heading 3
TARGET_PARAGRAPHS = [
    'Sampling Method',
    'Survey Design',
    'Control Group Selection',
    'Data Normalization',
]


def verify_task(file_path):
    """
    Verify that the four target paragraphs have been changed to 'Heading 3' style.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition gate: ensure the file can be loaded
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a lookup: {paragraph_text: style_name} for all paragraphs in document
    para_styles = {}
    for para in doc.paragraphs:
        text = para.text.strip()
        if text in TARGET_PARAGRAPHS:
            para_styles[text] = para.style.name

    # Component 1: 'Sampling Method' has Heading 3 style (0.25 points)
    try:
        target = 'Sampling Method'
        actual_style = para_styles.get(target)
        if actual_style == 'Heading 3':
            print(f"PASS: Component 1 — '{target}' has style 'Heading 3' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — '{target}' expected 'Heading 3', found: {actual_style!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Survey Design' has Heading 3 style (0.25 points)
    try:
        target = 'Survey Design'
        actual_style = para_styles.get(target)
        if actual_style == 'Heading 3':
            print(f"PASS: Component 2 — '{target}' has style 'Heading 3' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — '{target}' expected 'Heading 3', found: {actual_style!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Control Group Selection' has Heading 3 style (0.25 points)
    try:
        target = 'Control Group Selection'
        actual_style = para_styles.get(target)
        if actual_style == 'Heading 3':
            print(f"PASS: Component 3 — '{target}' has style 'Heading 3' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — '{target}' expected 'Heading 3', found: {actual_style!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'Data Normalization' has Heading 3 style (0.25 points)
    try:
        target = 'Data Normalization'
        actual_style = para_styles.get(target)
        if actual_style == 'Heading 3':
            print(f"PASS: Component 4 — '{target}' has style 'Heading 3' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — '{target}' expected 'Heading 3', found: {actual_style!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
