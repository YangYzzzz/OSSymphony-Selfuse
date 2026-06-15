"""
Reward Script: Create block quote indentation for paragraphs 3 and 6
Task ID: writer_para_048
Domain: libreoffice_writer
Scoring:
  Component 1: Paragraph 3 left_indent == ~3cm              (0.35 points)
  Component 2: Paragraph 3 right_indent == ~1cm             (0.15 points)
  Component 3: Paragraph 6 left_indent == ~3cm              (0.35 points)
  Component 4: Paragraph 6 right_indent == ~1cm             (0.15 points)
  Total: 1.0
"""

import os
from docx import Document
from docx.shared import Cm

WORKDIR = '/home/user'
TASK_ID = 'writer_para_048'

# Tolerance: 0.05cm (~1.4pt) to handle floating-point rounding in EMU conversion
TOLERANCE_CM = 0.05


def indent_cm(value):
    """Return indent in cm, or None if value is None."""
    if value is None:
        return None
    return value.cm


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Paragraphs 3 and 6 (excerpt/block-quote paragraphs) must have
          left_indent=3cm and right_indent=1cm.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Retrieve all paragraphs
    paragraphs = doc.paragraphs
    if len(paragraphs) < 6:
        print(f"FAIL: Expected at least 6 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Paragraph indices are 0-based; task paragraphs 3 and 6 are index 2 and 5
    para3 = paragraphs[2]
    para6 = paragraphs[5]

    # Component 1: Paragraph 3 left_indent == ~3cm (0.35 points)
    try:
        left3 = indent_cm(para3.paragraph_format.left_indent)
        if left3 is not None and abs(left3 - 3.0) <= TOLERANCE_CM:
            print(f"PASS: Component 1 — Para 3 left_indent={left3:.4f}cm (expected ~3cm) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Para 3 left_indent={left3}cm, expected ~3cm")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Paragraph 3 right_indent == ~1cm (0.15 points)
    try:
        right3 = indent_cm(para3.paragraph_format.right_indent)
        if right3 is not None and abs(right3 - 1.0) <= TOLERANCE_CM:
            print(f"PASS: Component 2 — Para 3 right_indent={right3:.4f}cm (expected ~1cm) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Para 3 right_indent={right3}cm, expected ~1cm")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Paragraph 6 left_indent == ~3cm (0.35 points)
    try:
        left6 = indent_cm(para6.paragraph_format.left_indent)
        if left6 is not None and abs(left6 - 3.0) <= TOLERANCE_CM:
            print(f"PASS: Component 3 — Para 6 left_indent={left6:.4f}cm (expected ~3cm) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — Para 6 left_indent={left6}cm, expected ~3cm")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Paragraph 6 right_indent == ~1cm (0.15 points)
    try:
        right6 = indent_cm(para6.paragraph_format.right_indent)
        if right6 is not None and abs(right6 - 1.0) <= TOLERANCE_CM:
            print(f"PASS: Component 4 — Para 6 right_indent={right6:.4f}cm (expected ~1cm) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Para 6 right_indent={right6}cm, expected ~1cm")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Verify text content is unchanged (non-scoring integrity gate)
    expected_texts = [
        'Book Review: The Invisible Hand of Data',
        'In her latest work, Professor Sarah Chen',
        'We have entered an era where every click',
        'This provocative thesis is supported',
        'Chen presents compelling evidence',
        'The algorithms do not merely predict',
        'Overall, this is an essential read',
    ]
    try:
        for idx, expected_start in enumerate(expected_texts):
            actual_text = paragraphs[idx].text if idx < len(paragraphs) else ""
            if not actual_text.startswith(expected_start[:30]):
                print(f"WARN: Para {idx + 1} text mismatch — starts with '{actual_text[:40]}'")
    except Exception as e:
        print(f"WARN: Text integrity check failed: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
