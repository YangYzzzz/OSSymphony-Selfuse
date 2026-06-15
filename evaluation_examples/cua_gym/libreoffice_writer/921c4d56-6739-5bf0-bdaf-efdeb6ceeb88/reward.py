"""
Reward Script: Change paragraph alignments in data report
Task ID: writer_para_045
Domain: libreoffice_writer

Scoring rubric:
  Component 1: Table header paragraphs (para indices 1, 3, 5) must have CENTER alignment
               0.2 pts each -> 0.6 pts total
  Component 2: Data description paragraphs (para indices 2, 4, 6) must have JUSTIFY alignment
               0.133/0.133/0.134 pts each -> 0.4 pts total
  Total: 1.0

Only task-introduced changes are scored.
Initial file: all non-heading paragraphs are LEFT aligned.
Golden file: headers are CENTER, descriptions are JUSTIFY.
"""

import os
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_para_045'

# Expected paragraph indices and alignments (0-indexed)
# Para 0: Heading 1 — unchanged
# Para 1, 3, 5: Table headers -> CENTER  (0.2 pts each)
# Para 2, 4, 6: Data descriptions -> JUSTIFY  (0.133/0.133/0.134 pts)

HEADER_INDICES = [1, 3, 5]
DESCRIPTION_INDICES = [2, 4, 6]

EXPECTED_HEADER_TEXTS = [
    'Table 1: Regional Sales Performance Q4 2024',
    'Table 2: Product Category Breakdown',
    'Table 3: Customer Acquisition Metrics',
]

EXPECTED_DESCRIPTION_PREFIXES = [
    'The North American region',
    'Enterprise solutions accounted',
    'New customer acquisition cost',
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

    paragraphs = doc.paragraphs

    if len(paragraphs) < 7:
        print(f"CRITICAL: Expected at least 7 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1a: Para 1 (table header 1) must be CENTER (0.2 pts)
    try:
        para = paragraphs[1]
        alignment = para.paragraph_format.alignment
        actual_text = para.text.strip()
        if alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            print(f"PASS: Para 1 ('{actual_text[:45]}') is CENTER (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Para 1 ('{actual_text[:45]}') expected CENTER, got {alignment}")
    except Exception as e:
        print(f"ERROR: Para 1 alignment check: {e}")

    # Component 1b: Para 3 (table header 2) must be CENTER (0.2 pts)
    try:
        para = paragraphs[3]
        alignment = para.paragraph_format.alignment
        actual_text = para.text.strip()
        if alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            print(f"PASS: Para 3 ('{actual_text[:45]}') is CENTER (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Para 3 ('{actual_text[:45]}') expected CENTER, got {alignment}")
    except Exception as e:
        print(f"ERROR: Para 3 alignment check: {e}")

    # Component 1c: Para 5 (table header 3) must be CENTER (0.2 pts)
    try:
        para = paragraphs[5]
        alignment = para.paragraph_format.alignment
        actual_text = para.text.strip()
        if alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            print(f"PASS: Para 5 ('{actual_text[:45]}') is CENTER (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Para 5 ('{actual_text[:45]}') expected CENTER, got {alignment}")
    except Exception as e:
        print(f"ERROR: Para 5 alignment check: {e}")

    # Component 2a: Para 2 (description 1) must be JUSTIFY (0.133 pts)
    try:
        para = paragraphs[2]
        alignment = para.paragraph_format.alignment
        actual_text = para.text.strip()
        if alignment == WD_PARAGRAPH_ALIGNMENT.JUSTIFY:
            print(f"PASS: Para 2 ('{actual_text[:45]}...') is JUSTIFY (0.133 pts)")
            total_score += 0.133
        else:
            print(f"FAIL: Para 2 ('{actual_text[:45]}...') expected JUSTIFY, got {alignment}")
    except Exception as e:
        print(f"ERROR: Para 2 alignment check: {e}")

    # Component 2b: Para 4 (description 2) must be JUSTIFY (0.133 pts)
    try:
        para = paragraphs[4]
        alignment = para.paragraph_format.alignment
        actual_text = para.text.strip()
        if alignment == WD_PARAGRAPH_ALIGNMENT.JUSTIFY:
            print(f"PASS: Para 4 ('{actual_text[:45]}...') is JUSTIFY (0.133 pts)")
            total_score += 0.133
        else:
            print(f"FAIL: Para 4 ('{actual_text[:45]}...') expected JUSTIFY, got {alignment}")
    except Exception as e:
        print(f"ERROR: Para 4 alignment check: {e}")

    # Component 2c: Para 6 (description 3) must be JUSTIFY (0.134 pts)
    try:
        para = paragraphs[6]
        alignment = para.paragraph_format.alignment
        actual_text = para.text.strip()
        if alignment == WD_PARAGRAPH_ALIGNMENT.JUSTIFY:
            print(f"PASS: Para 6 ('{actual_text[:45]}...') is JUSTIFY (0.134 pts)")
            total_score += 0.134
        else:
            print(f"FAIL: Para 6 ('{actual_text[:45]}...') expected JUSTIFY, got {alignment}")
    except Exception as e:
        print(f"ERROR: Para 6 alignment check: {e}")

    # Precondition info (not scored): Para 0 should remain unchanged
    try:
        para0_align = paragraphs[0].paragraph_format.alignment
        para0_text = paragraphs[0].text.strip()
        print(f"INFO: Para 0 ('{para0_text[:40]}') alignment={para0_align} (unchanged heading, not scored)")
    except Exception as e:
        print(f"INFO: Para 0 check skipped: {e}")

    final_score = round(min(total_score, 1.0), 3)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
