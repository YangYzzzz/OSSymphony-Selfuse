"""
Reward Script: Redact dates and monetary values from legal PDF, add watermark
Task ID: pdf_pw_031
Domain: pdf
Scoring:
  C1 (0.15) — Output file exists with correct page count (12)
  C2 (0.25) — No YYYY-MM-DD dates remain in text
  C3 (0.25) — No dollar amounts remain in text
  C4 (0.10) — [DATE REDACTED] markers present (>= 10)
  C5 (0.10) — [AMOUNT REDACTED] markers present (>= 8)
  C6 (0.15) — REDACTED COPY watermark on every page
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_031'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'settlement_agreement_redacted.pdf')
EXPECTED_PAGES = 12


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has correct page count (0.15 points)
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Page count is {page_count} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Extract all text from all pages for subsequent checks
    all_text = ""
    page_texts = []
    try:
        for page in doc:
            text = page.get_text()
            page_texts.append(text)
            all_text += text + "\n"
    except Exception as e:
        print(f"ERROR: Could not extract text: {e}")
        doc.close()
        print(f"REWARD: {min(total_score, 1.0)}")
        return min(total_score, 1.0)

    # Component 2: No YYYY-MM-DD dates remain (0.25 points)
    try:
        date_pat = re.compile(r'\d{4}-\d{2}-\d{2}')
        remaining_dates = date_pat.findall(all_text)
        if len(remaining_dates) == 0:
            print(f"PASS: Component 2 — No YYYY-MM-DD dates remain in text (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — {len(remaining_dates)} dates still present: {remaining_dates[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No dollar amounts remain (0.25 points)
    try:
        dollar_pat = re.compile(r'\$[\d,]+\.\d{2}')
        remaining_dollars = dollar_pat.findall(all_text)
        if len(remaining_dollars) == 0:
            print(f"PASS: Component 3 — No dollar amounts remain in text (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — {len(remaining_dollars)} dollar amounts still present: {remaining_dollars[:5]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: [DATE REDACTED] markers present >= 10 (0.10 points)
    try:
        date_redacted_pat = re.compile(r'\[DATE REDACTED\]')
        date_redacted_count = len(date_redacted_pat.findall(all_text))
        if date_redacted_count >= 10:
            print(f"PASS: Component 4 — {date_redacted_count} [DATE REDACTED] markers found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Expected >= 10 [DATE REDACTED] markers, found {date_redacted_count}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: [AMOUNT REDACTED] markers present >= 8 (0.10 points)
    try:
        amount_redacted_pat = re.compile(r'\[AMOUNT REDACTED\]')
        amount_redacted_count = len(amount_redacted_pat.findall(all_text))
        if amount_redacted_count >= 8:
            print(f"PASS: Component 5 — {amount_redacted_count} [AMOUNT REDACTED] markers found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Expected >= 8 [AMOUNT REDACTED] markers, found {amount_redacted_count}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: REDACTED COPY watermark on every page (0.15 points)
    try:
        watermark_pat = re.compile(r'REDACTED COPY', re.IGNORECASE)
        pages_with_watermark = 0
        for i, text in enumerate(page_texts):
            if watermark_pat.search(text):
                pages_with_watermark += 1
        if pages_with_watermark == EXPECTED_PAGES:
            print(f"PASS: Component 6 — Watermark found on all {pages_with_watermark}/{EXPECTED_PAGES} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Watermark found on {pages_with_watermark}/{EXPECTED_PAGES} pages")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
