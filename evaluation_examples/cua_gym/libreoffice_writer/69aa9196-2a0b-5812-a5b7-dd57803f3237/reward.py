"""
Reward Script: Select all text and paste as unformatted text at end of document
Task ID: writer_edit_009
Domain: libreoffice_writer
Scoring:
  Component 1: Document paragraph count increased (original 4 + separator + 4 plain = 9 total)   — 0.20 pts
  Component 2: Separator paragraph '---' exists after the original content                        — 0.20 pts
  Component 3: Plain text section contains the correct text content (same as original)            — 0.20 pts
  Component 4: Plain text section has no bold formatting (original title was bold)                — 0.20 pts
  Component 5: Plain text section has no italic formatting (original date was italic)             — 0.10 pts
  Component 6: Plain text section has no underline formatting (original phrases were underlined)  — 0.10 pts
Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_edit_009'

# Expected content from the original memo (for text verification)
EXPECTED_TEXTS = [
    'Internal Memo',
    'Date: March 3, 2025',
    'Subject: Office Relocation',
    'We are pleased to announce that our office will relocate to 123 Main Street effective April 1, 2025. Please contact HR for details.',
]

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task asks the agent to:
    1. Copy all text from the document
    2. Paste it as unformatted (plain) text at the end
    3. Include a separator paragraph '---' before the pasted text

    Golden state: 9 paragraphs total
      - Para 0-3: original formatted content
      - Para 4: separator '---'
      - Para 5-8: same text as para 0-3 but with NO bold/italic/underline
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    num_paras = len(paragraphs)
    print(f"INFO: Document has {num_paras} paragraphs")

    # Component 1: Document has more paragraphs than initial (task-introduced change: added 5 more paras)
    # Initial: 4 paragraphs. Golden: 9 paragraphs (4 original + 1 separator + 4 plain copies)
    try:
        if num_paras >= 9:
            print(f"PASS: Component 1 — Document has {num_paras} paragraphs (expected >= 9) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected >= 9 paragraphs, found {num_paras}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Separator paragraph '---' exists at position 4 (0-indexed)
    # This is a clear task-introduced change — no separator in initial doc
    try:
        separator_found = False
        separator_idx = -1
        for i, para in enumerate(paragraphs):
            if para.text.strip() == '---':
                separator_found = True
                separator_idx = i
                break
        if separator_found:
            print(f"PASS: Component 2 — Separator '---' found at paragraph index {separator_idx} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — No separator paragraph '---' found in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # For components 3-6, we need to find the plain text section
    # It should be the paragraphs AFTER the separator
    plain_section = []
    if separator_idx >= 0 and separator_idx + 1 < num_paras:
        plain_section = paragraphs[separator_idx + 1:]

    # Component 3: Plain text section contains all expected text content
    # Verifies that the pasted text has the correct content
    try:
        if len(plain_section) == 0:
            print(f"FAIL: Component 3 — No plain text section found after separator")
        else:
            plain_texts = [para.text.strip() for para in plain_section if para.text.strip()]
            # Check that all 4 expected memo lines appear in the plain section
            matched = 0
            for expected in EXPECTED_TEXTS:
                # Check if any paragraph contains the expected text (allow exact or subset match)
                found_match = any(expected in pt or pt in expected for pt in plain_texts)
                if found_match:
                    matched += 1
            if matched == len(EXPECTED_TEXTS):
                print(f"PASS: Component 3 — Plain text section contains all {matched}/{len(EXPECTED_TEXTS)} expected text lines (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Plain text section matched {matched}/{len(EXPECTED_TEXTS)} expected lines")
                print(f"  Plain texts found: {plain_texts}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Plain text section has NO bold formatting
    # The title 'Internal Memo' was bold in the original — it must be plain in the copy.
    # GATE: plain_section must be non-empty (i.e., task was actually performed)
    try:
        if len(plain_section) == 0:
            print(f"FAIL: Component 4 — No plain text section found (task not performed)")
        else:
            bold_found = False
            for para in plain_section:
                for run in para.runs:
                    if run.text.strip() and run.bold is True:
                        bold_found = True
                        print(f"  DETAIL: Bold text found in plain section: '{run.text}'")
                        break
                if bold_found:
                    break
            # Also verify that the plain_section actually has runs (not just empty paragraphs)
            has_text_runs = any(run.text.strip() for para in plain_section for run in para.runs)
            if not bold_found and has_text_runs:
                print(f"PASS: Component 4 — No bold formatting in plain text section (0.20 pts)")
                total_score += 0.20
            elif bold_found:
                print(f"FAIL: Component 4 — Bold formatting detected in plain text section (should be plain)")
            else:
                print(f"FAIL: Component 4 — Plain section has no text runs to verify")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Plain text section has NO italic formatting
    # The date 'Date: March 3, 2025' was italic in the original — it must be plain in the copy.
    # GATE: plain_section must be non-empty
    try:
        if len(plain_section) == 0:
            print(f"FAIL: Component 5 — No plain text section found (task not performed)")
        else:
            italic_found = False
            for para in plain_section:
                for run in para.runs:
                    if run.text.strip() and run.italic is True:
                        italic_found = True
                        print(f"  DETAIL: Italic text found in plain section: '{run.text}'")
                        break
                if italic_found:
                    break
            has_text_runs = any(run.text.strip() for para in plain_section for run in para.runs)
            if not italic_found and has_text_runs:
                print(f"PASS: Component 5 — No italic formatting in plain text section (0.10 pts)")
                total_score += 0.10
            elif italic_found:
                print(f"FAIL: Component 5 — Italic formatting detected in plain text section (should be plain)")
            else:
                print(f"FAIL: Component 5 — Plain section has no text runs to verify")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Plain text section has NO underline formatting
    # '123 Main Street' and 'April 1, 2025' were underlined in the original — must be plain in the copy.
    # GATE: plain_section must be non-empty
    try:
        if len(plain_section) == 0:
            print(f"FAIL: Component 6 — No plain text section found (task not performed)")
        else:
            underline_found = False
            for para in plain_section:
                for run in para.runs:
                    if run.text.strip() and run.underline is True:
                        underline_found = True
                        print(f"  DETAIL: Underlined text found in plain section: '{run.text}'")
                        break
                if underline_found:
                    break
            has_text_runs = any(run.text.strip() for para in plain_section for run in para.runs)
            if not underline_found and has_text_runs:
                print(f"PASS: Component 6 — No underline formatting in plain text section (0.10 pts)")
                total_score += 0.10
            elif underline_found:
                print(f"FAIL: Component 6 — Underline formatting detected in plain text section (should be plain)")
            else:
                print(f"FAIL: Component 6 — Plain section has no text runs to verify")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/Desktop/formatted_memo.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
