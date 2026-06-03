"""
Reward Script: OCR scanned police report to searchable PDF
Task ID: pdf_legal_069
Domain: pdf
Scoring:
  Component 1 (0.20): Output file exists at correct path
  Component 2 (0.20): PDF has exactly 3 pages
  Component 3 (0.30): All 3 pages have non-empty text layers (OCR was performed)
  Component 4 (0.30): Key searchable content present (names, dates, locations)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_069'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'personal_injury', 'police_report_searchable.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file is a valid PDF (0.20 points)
    # This checks that the file exists AND is a valid, openable PDF
    try:
        if doc.page_count > 0:
            print(f"PASS: Component 1 — Valid PDF with {doc.page_count} pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: PDF has exactly 3 pages (preserving original layout) (0.20 points)
    try:
        if doc.page_count == 3:
            print(f"PASS: Component 2 — PDF has exactly 3 pages as expected (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected 3 pages, found {doc.page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 3 pages have text layers (OCR text extraction works) (0.30 points)
    # Each page with text contributes 0.10 points
    try:
        pages_with_text = 0
        for i in range(min(doc.page_count, 3)):
            page = doc[i]
            text = page.get_text("text").strip()
            if len(text) > 50:  # Meaningful text, not just whitespace/artifacts
                pages_with_text += 1
                print(f"  Page {i}: text layer present ({len(text)} chars)")
            else:
                print(f"  Page {i}: NO text layer or insufficient text ({len(text)} chars)")

        if pages_with_text == 3:
            print(f"PASS: Component 3 — All 3 pages have text layers (0.30 pts)")
            total_score += 0.30
        elif pages_with_text > 0:
            partial = round(pages_with_text * 0.10, 2)
            print(f"PARTIAL: Component 3 — {pages_with_text}/3 pages have text ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have text layers")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Key searchable content present (0.30 points)
    # The OCR should capture key information from the police report:
    #   - Officer name: "Whitfield" (0.06 pts)
    #   - Driver 1 name: "Martinez" (0.06 pts)
    #   - Driver 2 name: "Thompson" (0.06 pts)
    #   - Incident date: "03/13/2025" or "March 13" (0.06 pts)
    #   - Location keyword: "Millbrook" or "Oak Ridge" (0.06 pts)
    try:
        all_text = ""
        for page in doc:
            all_text += page.get_text("text")

        key_terms = [
            ("Whitfield", "Officer name"),
            ("Martinez", "Driver 1 name"),
            ("Thompson", "Driver 2 name"),
            ("2025", "Incident year"),
            ("Millbrook", "Location"),
        ]

        comp4_score = 0.0
        for term, desc in key_terms:
            if term.lower() in all_text.lower():
                comp4_score += 0.06
                print(f"  PASS: '{term}' ({desc}) found in text")
            else:
                print(f"  FAIL: '{term}' ({desc}) NOT found in text")

        comp4_score = round(comp4_score, 2)
        if comp4_score > 0:
            print(f"PASS: Component 4 — Key content searchable ({comp4_score} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 — No key content found in text")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
