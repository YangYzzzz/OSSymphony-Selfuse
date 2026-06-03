"""
Reward Script: Export PDF with build-up animation steps as multiple pages
Task ID: impress_el_039
Domain: libreoffice_impress
Scoring:
  - Component 1: PDF page count > 5 (0.15 pts)
  - Component 2: PDF page count == 8 (0.15 pts)
  - Component 3: Slide 2 "Key Achievements" build-up across 3 pages (0.30 pts)
  - Component 4: Slide 4 "Strategic Priorities" build-up across 2 pages (0.25 pts)
  - Component 5: Non-animated slides appear as single pages (0.15 pts)
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'impress_el_039'


def count_bullets_on_page(page):
    """Count bullet points (lines starting with bullet char) on a PDF page."""
    text = page.get_text().strip()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return sum(1 for l in lines if l.startswith('\u2022'))


def get_page_title(page):
    """Extract the first non-empty line as the page title."""
    text = page.get_text().strip()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return lines[0] if lines else ""


def verify_task(pdf_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF file must exist (gate, not scored)
    if not os.path.exists(pdf_path):
        print(f"PRECONDITION FAIL: PDF not found at {pdf_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
    except ImportError:
        try:
            import pymupdf as fitz
        except ImportError:
            print("CRITICAL: PyMuPDF (fitz) not available")
            print("REWARD: 0.0")
            return 0.0

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {pdf_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    num_pages = len(doc)
    print(f"INFO: PDF has {num_pages} pages")

    # Component 1: PDF has more than 5 pages (0.15 pts)
    # The presentation has 5 slides; build-up export must produce >5 pages
    try:
        if num_pages > 5:
            print(f"PASS: Component 1 — PDF has {num_pages} pages, which is > 5 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF has {num_pages} pages, expected > 5")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: PDF has exactly 8 pages (0.15 pts)
    # 5 slides: slide1(1 page) + slide2(3 pages, 3 animation steps) + slide3(1 page)
    # + slide4(2 pages, 2 animation steps) + slide5(1 page) = 8 pages
    try:
        if num_pages == 8:
            print(f"PASS: Component 2 — PDF has exactly 8 pages as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — PDF has {num_pages} pages, expected exactly 8")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Slide 2 "Key Achievements" build-up across 3 consecutive pages (0.30 pts)
    # Pages 2-4 should all have "Key Achievements" title with progressively
    # increasing bullet counts: 1, 2, 3
    try:
        failures = 0
        expected_bullets = [1, 2, 3]
        details = []

        if num_pages < 4:
            failures += 1
            details.append(f"Not enough pages ({num_pages}) to contain 3-page build-up")
        else:
            for idx, expected_b in enumerate(expected_bullets):
                page_idx = 1 + idx  # pages 2, 3, 4 (0-indexed: 1, 2, 3)
                title = get_page_title(doc[page_idx])
                actual_bullets = count_bullets_on_page(doc[page_idx])

                if "Key Achievements" not in title:
                    failures += 1
                    details.append(f"Page {page_idx+1}: expected 'Key Achievements' title, got '{title}'")
                elif actual_bullets != expected_b:
                    failures += 1
                    details.append(f"Page {page_idx+1}: expected {expected_b} bullet(s), found {actual_bullets}")
                else:
                    details.append(f"Page {page_idx+1}: 'Key Achievements' with {actual_bullets} bullet(s) OK")

        if failures == 0:
            print(f"PASS: Component 3 — Slide 2 build-up correct: {'; '.join(details)} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Slide 2 build-up issues: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Slide 4 "Strategic Priorities" build-up across 2 consecutive pages (0.25 pts)
    # Pages 6-7 should have "Strategic Priorities" title with progressively
    # increasing bullet counts: 1, 2
    try:
        failures = 0
        expected_bullets = [1, 2]
        details = []

        if num_pages < 7:
            failures += 1
            details.append(f"Not enough pages ({num_pages}) to contain slide 4 build-up at pages 6-7")
        else:
            for idx, expected_b in enumerate(expected_bullets):
                page_idx = 5 + idx  # pages 6, 7 (0-indexed: 5, 6)
                title = get_page_title(doc[page_idx])
                actual_bullets = count_bullets_on_page(doc[page_idx])

                if "Strategic Priorities" not in title:
                    failures += 1
                    details.append(f"Page {page_idx+1}: expected 'Strategic Priorities' title, got '{title}'")
                elif actual_bullets != expected_b:
                    failures += 1
                    details.append(f"Page {page_idx+1}: expected {expected_b} bullet(s), found {actual_bullets}")
                else:
                    details.append(f"Page {page_idx+1}: 'Strategic Priorities' with {actual_bullets} bullet(s) OK")

        if failures == 0:
            print(f"PASS: Component 4 — Slide 4 build-up correct: {'; '.join(details)} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Slide 4 build-up issues: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Non-animated slides appear as single pages (0.15 pts)
    # Slide 1 ("Quarterly Business Review") = page 1 only
    # Slide 3 ("Market Analysis") = page 5 only
    # Slide 5 ("Next Steps & Timeline") = page 8 only
    # Check that these titles appear exactly once in the PDF
    try:
        failures = 0
        details = []

        for title_check, expected_page_idx in [
            ("Quarterly Business Review", 0),
            ("Market Analysis", 4),
            ("Next Steps", 7),
        ]:
            # Count how many pages have this title
            title_pages = []
            for p_idx in range(num_pages):
                t = get_page_title(doc[p_idx])
                if title_check in t:
                    title_pages.append(p_idx + 1)

            if len(title_pages) == 1 and title_pages[0] == expected_page_idx + 1:
                details.append(f"'{title_check}' appears only on page {title_pages[0]} OK")
            else:
                failures += 1
                details.append(f"'{title_check}' expected only on page {expected_page_idx+1}, found on pages {title_pages}")

        if failures == 0:
            print(f"PASS: Component 5 — Non-animated slides single-page: {'; '.join(details)} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Non-animated slides issues: {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
pdf_path = f'{WORKDIR}/{TASK_ID}.pdf'
verify_task(pdf_path)
