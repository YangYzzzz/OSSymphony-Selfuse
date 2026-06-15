"""
Reward Script: Format envelope addresses with specific fonts and sizes
Task ID: writer_lec_040
Domain: libreoffice_writer
Scoring:
  - Component 1: Delivery address font is Arial (0.3)
  - Component 2: Delivery address size is 14pt (0.3)
  - Component 3: Return address font is Arial (0.2)
  - Component 4: Return address size is 10pt (0.2)
  - Gate: Address text content preserved (precondition)
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_040'

# Expected text content for verification
RETURN_ADDR_TEXTS = [
    'Greenfield Technologies Inc.',
    '4200 Lakeshore Boulevard, Suite 300',
    'Chicago, IL 60613',
]
DELIVERY_ADDR_TEXTS = [
    'Ms. Patricia Hawthorne',
    'Regional Director, Western Operations',
    'Cascade Financial Group',
    '8750 Wilshire Boulevard, Floor 22',
    'Los Angeles, CA 90036',
]

# Return address paragraph indices: 0, 1, 2
RETURN_ADDR_INDICES = [0, 1, 2]
# Delivery address paragraph indices: 7, 8, 9, 10, 11
DELIVERY_ADDR_INDICES = [7, 8, 9, 10, 11]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs

    # Precondition: document has at least 12 paragraphs
    if len(paras) < 12:
        print(f"CRITICAL: Expected at least 12 paragraphs, found {len(paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Delivery address font is Arial (0.3 points)
    try:
        delivery_fonts = []
        for idx in DELIVERY_ADDR_INDICES:
            for run in paras[idx].runs:
                if run.text.strip():
                    delivery_fonts.append(run.font.name)
        all_arial = all(f == 'Arial' for f in delivery_fonts) and len(delivery_fonts) > 0
        if all_arial:
            print(f"PASS: Component 1 - Delivery address font is Arial ({delivery_fonts}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - Delivery address fonts: {delivery_fonts}, expected all Arial")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Delivery address size is 14pt (0.3 points)
    try:
        delivery_sizes = []
        for idx in DELIVERY_ADDR_INDICES:
            for run in paras[idx].runs:
                if run.text.strip() and run.font.size:
                    delivery_sizes.append(run.font.size.pt)
        all_14 = all(abs(s - 14.0) < 0.5 for s in delivery_sizes) and len(delivery_sizes) > 0
        if all_14:
            print(f"PASS: Component 2 - Delivery address size is 14pt ({delivery_sizes}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - Delivery address sizes: {delivery_sizes}, expected all 14.0pt")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Return address font is Arial (0.2 points)
    try:
        return_fonts = []
        for idx in RETURN_ADDR_INDICES:
            for run in paras[idx].runs:
                if run.text.strip():
                    return_fonts.append(run.font.name)
        all_arial_ret = all(f == 'Arial' for f in return_fonts) and len(return_fonts) > 0
        if all_arial_ret:
            print(f"PASS: Component 3 - Return address font is Arial ({return_fonts}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 - Return address fonts: {return_fonts}, expected all Arial")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Return address size is 10pt (0.2 points)
    try:
        return_sizes = []
        for idx in RETURN_ADDR_INDICES:
            for run in paras[idx].runs:
                if run.text.strip() and run.font.size:
                    return_sizes.append(run.font.size.pt)
        all_10 = all(abs(s - 10.0) < 0.5 for s in return_sizes) and len(return_sizes) > 0
        if all_10:
            print(f"PASS: Component 4 - Return address size is 10pt ({return_sizes}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 - Return address sizes: {return_sizes}, expected all 10.0pt")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Content preservation is a precondition gate, not a scoring component.
    # Text content exists in both initial and golden, so scoring it would give
    # points to the initial env. Instead, use it as a gate: if content is corrupted,
    # zero out the score.
    try:
        content_ok = all(
            paras[idx].text.strip() == RETURN_ADDR_TEXTS[i]
            for i, idx in enumerate(RETURN_ADDR_INDICES)
        ) and all(
            paras[idx].text.strip() == DELIVERY_ADDR_TEXTS[i]
            for i, idx in enumerate(DELIVERY_ADDR_INDICES)
        )
        if not content_ok:
            print("GATE FAIL: Address text content was corrupted - zeroing score")
            total_score = 0.0
        else:
            print("GATE PASS: Address text content preserved")
    except Exception as e:
        print(f"ERROR: Content gate - {e}")
        total_score = 0.0

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
