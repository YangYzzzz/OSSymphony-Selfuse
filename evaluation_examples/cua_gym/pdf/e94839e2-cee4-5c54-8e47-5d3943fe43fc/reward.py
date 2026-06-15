"""
Reward Script: Redact phone numbers and dollar amounts in vendor_contracts.pdf
Task ID: pdf_pw_019
Domain: pdf
Scoring:
  - Component 1 (0.25): No phone number patterns remain in the output PDF
  - Component 2 (0.25): No dollar amount patterns remain in the output PDF
  - Component 3 (0.15): [PHONE REDACTED] replacement markers present
  - Component 4 (0.15): [AMOUNT REDACTED] replacement markers present
  - Component 5 (0.20): All 20 pages preserved
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_019'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from the PDF
    try:
        all_text = ""
        for page in doc:
            all_text += page.get_text("text")
        page_count = doc.page_count
    except Exception as e:
        print(f"CRITICAL: Cannot extract text: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: No phone number patterns remain (0.25 points)
    # Phone pattern: (XXX) XXX-XXXX
    try:
        phone_pattern = r'\(\d{3}\) \d{3}-\d{4}'
        remaining_phones = re.findall(phone_pattern, all_text)
        if len(remaining_phones) == 0:
            print(f"PASS: Component 1 — No phone number patterns remain (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — {len(remaining_phones)} phone numbers still present: {remaining_phones[:3]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No dollar amount patterns remain (0.25 points)
    # Dollar pattern: $X,XXX.XX
    try:
        dollar_pattern = r'\$[\d,]+\.\d{2}'
        remaining_dollars = re.findall(dollar_pattern, all_text)
        if len(remaining_dollars) == 0:
            print(f"PASS: Component 2 — No dollar amount patterns remain (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — {len(remaining_dollars)} dollar amounts still present: {remaining_dollars[:3]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: [PHONE REDACTED] replacement markers present (0.15 points)
    # This verifies the redacted text was actually replaced, not just deleted
    try:
        phone_redacted_count = all_text.count('[PHONE REDACTED]')
        if phone_redacted_count > 0:
            print(f"PASS: Component 3 — Found {phone_redacted_count} '[PHONE REDACTED]' markers (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — No '[PHONE REDACTED]' markers found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: [AMOUNT REDACTED] replacement markers present (0.15 points)
    try:
        amount_redacted_count = all_text.count('[AMOUNT REDACTED]')
        if amount_redacted_count > 0:
            print(f"PASS: Component 4 — Found {amount_redacted_count} '[AMOUNT REDACTED]' markers (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — No '[AMOUNT REDACTED]' markers found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: All 20 pages preserved (0.20 points)
    # This checks that pages were not lost during redaction AND that the document
    # is not the original (which also has 20 pages but no redaction markers).
    # Combined with Components 1-4, this ensures the redacted doc is complete.
    try:
        if page_count == 20:
            # Only award points if at least one redaction marker exists
            # (to avoid scoring the unmodified original file)
            has_any_redaction = (all_text.count('[PHONE REDACTED]') + all_text.count('[AMOUNT REDACTED]')) > 0
            if has_any_redaction:
                print(f"PASS: Component 5 — All 20 pages preserved with redactions applied (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — 20 pages present but no redaction markers found (original file?)")
        else:
            print(f"FAIL: Component 5 — Expected 20 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/finance/vendor_contracts_clean.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
