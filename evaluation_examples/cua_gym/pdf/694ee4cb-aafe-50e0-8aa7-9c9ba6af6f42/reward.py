"""
Reward Script: Create a PDF demonstrating all 14 standard PDF base fonts
Task ID: pdf_cr_040
Domain: pdf
Scoring:
  Component 1 (0.15): PDF exists at correct path with >= 1 page
  Component 2 (0.25): Contains font name labels (Helvetica, Times-Roman, Courier)
  Component 3 (0.30): Uses >= 10 distinct font names across all text spans
  Component 4 (0.30): Contains 'quick brown fox' at least 10 times
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_040'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'multi_font.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has at least 1 page (0.15 points)
    # Initial env has no file at all, so this only passes on golden.
    try:
        page_count = doc.page_count
        if page_count >= 1:
            print(f"PASS: Component 1 — PDF has {page_count} page(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Extract full text and span info for subsequent checks
    try:
        full_text = ''
        all_span_fonts = set()
        for i in range(doc.page_count):
            page = doc[i]
            full_text += page.get_text()
            data = page.get_text("dict")
            for block in data["blocks"]:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["text"].strip():
                            all_span_fonts.add(span["font"])
    except Exception as e:
        print(f"ERROR: Could not extract text/font info: {e}")
        full_text = ''
        all_span_fonts = set()

    # Component 2: Contains key font name labels in text (0.25 points)
    # Task requires displaying each font name. Check at least the 3 main families.
    try:
        required_labels = ['Helvetica', 'Times-Roman', 'Courier']
        found_labels = [label for label in required_labels if label in full_text]
        if len(found_labels) == len(required_labels):
            print(f"PASS: Component 2 — Found all key font labels: {found_labels} (0.25 pts)")
            total_score += 0.25
        else:
            missing = [l for l in required_labels if l not in full_text]
            print(f"FAIL: Component 2 — Found {len(found_labels)}/{len(required_labels)} labels. Missing: {missing}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Uses at least 10 distinct font names in spans (0.30 points)
    # The task requires demonstrating all 14 base fonts. We check >= 10 for robustness.
    try:
        distinct_font_count = len(all_span_fonts)
        if distinct_font_count >= 10:
            print(f"PASS: Component 3 — {distinct_font_count} distinct fonts used: {sorted(all_span_fonts)} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Only {distinct_font_count} distinct fonts (need >= 10). Fonts: {sorted(all_span_fonts)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Contains 'quick brown fox' at least 10 times (0.30 points)
    # Task says to show sample text below each font name. 14 fonts = 14 occurrences expected.
    # We check >= 10 for robustness (Symbol/ZapfDingbats may render differently).
    try:
        fox_count = full_text.lower().count('quick brown fox')
        if fox_count >= 10:
            print(f"PASS: Component 4 — 'quick brown fox' found {fox_count} times (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 4 — 'quick brown fox' found only {fox_count} times (need >= 10)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
