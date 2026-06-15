"""
Reward Script: Select the entire second paragraph and delete it from the document.
Task ID: writer_edit_053
Domain: libreoffice_writer
Scoring:
  Component 1: Document has exactly 3 paragraphs (0.4 pts)
  Component 2: The second paragraph (Springfield University) is absent (0.3 pts)
  Component 3: Remaining paragraphs match expected order/content (0.3 pts)
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_edit_053'
FILE_NAME = 'cover_letter.docx'

# Known second paragraph text that should be deleted
DELETED_PARA_SNIPPET = 'I recently graduated from Springfield University'

# Expected paragraph prefixes (first ~50 chars) after deletion
EXPECTED_PARAS = [
    'Dear Hiring Manager, I am writing to express',       # original para 0
    'During my academic career and internships',          # original para 2 (now para 1)
    "I would welcome the opportunity to discuss",         # original para 3 (now para 2)
]


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

    paragraphs = [p for p in doc.paragraphs]
    para_texts = [p.text for p in paragraphs]

    # Component 1: Document has exactly 3 paragraphs (0.4 points)
    # Initial env has 4 paragraphs; golden env has 3 after deletion
    try:
        num_paras = len(para_texts)
        if num_paras == 3:
            print(f"PASS: Component 1 — Document has exactly 3 paragraphs (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected 3 paragraphs, found {num_paras}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The deleted paragraph (Springfield University) is absent (0.3 points)
    # This text was the second paragraph in the initial env; it must be gone in golden env
    try:
        deleted_present = any(DELETED_PARA_SNIPPET in p for p in para_texts)
        if not deleted_present:
            print(f"PASS: Component 2 — Deleted paragraph (Springfield University) is absent (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Deleted paragraph still present: found '{DELETED_PARA_SNIPPET}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Remaining paragraphs match the expected order and content (0.3 points)
    # After deletion, the document should contain original para 0, para 2, para 3 in sequence
    try:
        if len(para_texts) == 3:
            order_ok = all(
                para_texts[i].startswith(EXPECTED_PARAS[i])
                for i in range(3)
            )
            if order_ok:
                print(f"PASS: Component 3 — Remaining 3 paragraphs match expected order and content (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Paragraph order/content mismatch.")
                for i in range(min(3, len(para_texts))):
                    print(f"  Para {i}: {para_texts[i][:60]!r}")
                    print(f"  Expected prefix: {EXPECTED_PARAS[i]!r}")
        else:
            print(f"FAIL: Component 3 — Cannot check order/content because paragraph count is not 3 (found {len(para_texts)})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = f'{WORKDIR}/{FILE_NAME}'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
