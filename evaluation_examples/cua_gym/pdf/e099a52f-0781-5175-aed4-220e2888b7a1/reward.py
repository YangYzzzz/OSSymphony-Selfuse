"""
Reward Script: Redact credit card numbers in PDF and add certification text
Task ID: pdf_gf2_028
Domain: pdf
Scoring:
  - Component 1: No credit card numbers remain in text (0.35 pts)
  - Component 2: [CARD REDACTED] replacement text present (0.25 pts)
  - Component 3: Black redaction rectangles present (0.15 pts)
  - Component 4: Certification text on last page (0.15 pts)
  - Component 5: All 7 pages preserved (0.10 pts)
"""

import os
import re
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_028'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Credit card pattern: 4 groups of 4 digits, optionally separated by hyphens or spaces
    cc_pattern = r'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}'

    # Component 1: No credit card numbers remain in extracted text (0.35 points)
    # This FAILS on initial (18 card numbers present) and PASSES on golden (0 card numbers)
    try:
        total_cc_matches = 0
        for i in range(page_count):
            text = doc[i].get_text("text")
            matches = re.findall(cc_pattern, text)
            total_cc_matches += len(matches)

        if total_cc_matches == 0:
            print(f"PASS: Component 1 — No credit card numbers found in text (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — {total_cc_matches} credit card numbers still present in text")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: [CARD REDACTED] replacement text present (0.25 points)
    # This FAILS on initial (no such text) and PASSES on golden (18 occurrences)
    try:
        total_redacted_text = 0
        for i in range(page_count):
            text = doc[i].get_text("text")
            count = text.count("[CARD REDACTED]")
            total_redacted_text += count

        if total_redacted_text >= 15:
            # Full credit: most/all card numbers replaced with [CARD REDACTED]
            print(f"PASS: Component 2 — {total_redacted_text} [CARD REDACTED] markers found (0.25 pts)")
            total_score += 0.25
        elif total_redacted_text >= 5:
            # Partial credit: some replacements done
            partial = 0.15
            print(f"PARTIAL: Component 2 — {total_redacted_text} [CARD REDACTED] markers (expected ~18), awarding {partial} pts")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {total_redacted_text} [CARD REDACTED] markers found (expected ~18)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Black redaction rectangles present on pages 0-5 (0.15 points)
    # This FAILS on initial (no black rectangles) and PASSES on golden (black rects on pages 0-5)
    try:
        pages_with_black_rects = 0
        total_black_rects = 0
        for i in range(min(page_count, 6)):  # pages 0-5 should have redactions
            drawings = doc[i].get_drawings()
            black_rects = [
                d for d in drawings
                if d.get("fill") is not None and all(c < 0.05 for c in d["fill"])
            ]
            if len(black_rects) > 0:
                pages_with_black_rects += 1
                total_black_rects += len(black_rects)

        if pages_with_black_rects >= 5:
            print(f"PASS: Component 3 — {total_black_rects} black rectangles across {pages_with_black_rects} pages (0.15 pts)")
            total_score += 0.15
        elif pages_with_black_rects >= 2:
            partial = 0.08
            print(f"PARTIAL: Component 3 — Black rectangles on {pages_with_black_rects}/6 pages, awarding {partial} pts")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Black rectangles on only {pages_with_black_rects} pages (expected 6)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Certification text on last page (0.15 points)
    # This FAILS on initial (no such text) and PASSES on golden
    try:
        last_page_text = doc[-1].get_text("text")
        cert_text = "Redacted by compliance team on 2026-04-01"
        if cert_text in last_page_text:
            print(f"PASS: Component 4 — Certification text found on last page (0.15 pts)")
            total_score += 0.15
        else:
            # Check for partial match
            if "Redacted by compliance team" in last_page_text:
                print(f"PARTIAL: Component 4 — Partial certification text found (0.08 pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 4 — Certification text not found on last page")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: All 7 pages preserved AND no card numbers (compound check) (0.10 points)
    # This FAILS on initial because the compound condition requires no card numbers
    # and initial has card numbers
    try:
        if page_count == 7 and total_cc_matches == 0:
            print(f"PASS: Component 5 — All 7 pages preserved with redactions applied (0.10 pts)")
            total_score += 0.10
        elif page_count == 7:
            print(f"FAIL: Component 5 — 7 pages present but card numbers still exist")
        else:
            print(f"FAIL: Component 5 — Expected 7 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/finance/payment_records_redacted.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
