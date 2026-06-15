"""
Reward Script: Scale A4 PDF to US Letter size
Task ID: pdf_gf2_032
Domain: pdf
Scoring:
  Component 1: Page count matches original (10 pages) — 0.2 pts
  Component 2: All pages are US Letter size (612x792 pts) — 0.4 pts
  Component 3: Content preserved — key text from original present — 0.25 pts
  Component 4: No content clipped — section headers from all pages present — 0.15 pts
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_032'

# Expected section headers from each page (derived from task description + VM exploration)
EXPECTED_HEADERS = [
    "Meridian Analytics",
    "1. Executive Summary",
    "2. Revenue Breakdown",
    "3. Operating Expenses",
    "4. Client Portfolio Analysis",
    "5. Product Development",
    "6. Human Resources",
    "7. Risk Assessment",
    "8. Strategic Outlook for FY2025",
    "Appendix: Financial Summary Tables",
]

LETTER_WIDTH = 612.0
LETTER_HEIGHT = 792.0
TOLERANCE = 2.0  # points tolerance for page dimensions


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count is 10 (0.2 points)
    try:
        page_count = doc.page_count
        if page_count == 10:
            print(f"PASS: Component 1 — Page count is 10 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 10 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All pages are US Letter size 612x792 (0.4 points)
    try:
        letter_pages = 0
        total_pages = doc.page_count
        for i in range(total_pages):
            p = doc[i]
            w, h = p.rect.width, p.rect.height
            if abs(w - LETTER_WIDTH) <= TOLERANCE and abs(h - LETTER_HEIGHT) <= TOLERANCE:
                letter_pages += 1
            else:
                print(f"  Page {i}: dimensions {w}x{h}, expected ~{LETTER_WIDTH}x{LETTER_HEIGHT}")

        if total_pages > 0 and letter_pages == total_pages:
            print(f"PASS: Component 2 — All {total_pages} pages are US Letter size (0.4 pts)")
            total_score += 0.4
        elif total_pages > 0:
            # Partial credit: proportion of pages that are correct
            partial = 0.4 * (letter_pages / total_pages)
            print(f"PARTIAL: Component 2 — {letter_pages}/{total_pages} pages are US Letter ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content preserved — key text strings present (0.25 points)
    try:
        all_text = ""
        for i in range(doc.page_count):
            all_text += doc[i].get_text("text")

        # Check for critical content phrases (not just headers)
        content_checks = [
            "Meridian Analytics",
            "Annual Performance Report 2024",
            "fiscal year 2024",
            "$37.3M",
            "218 active enterprise clients",
        ]
        found_count = 0
        for phrase in content_checks:
            if phrase in all_text:
                found_count += 1

        if found_count == len(content_checks):
            print(f"PASS: Component 3 — All {len(content_checks)} content phrases found (0.25 pts)")
            total_score += 0.25
        elif found_count > 0:
            partial = 0.25 * (found_count / len(content_checks))
            print(f"PARTIAL: Component 3 — {found_count}/{len(content_checks)} content phrases found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No content phrases found in output PDF")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: No content clipped — section headers from all 10 pages present (0.15 points)
    try:
        all_text = ""
        for i in range(doc.page_count):
            all_text += doc[i].get_text("text")

        headers_found = 0
        for header in EXPECTED_HEADERS:
            if header in all_text:
                headers_found += 1
            else:
                print(f"  Missing header: '{header}'")

        if headers_found == len(EXPECTED_HEADERS):
            print(f"PASS: Component 4 — All {len(EXPECTED_HEADERS)} section headers present (0.15 pts)")
            total_score += 0.15
        elif headers_found > 0:
            partial = 0.15 * (headers_found / len(EXPECTED_HEADERS))
            print(f"PARTIAL: Component 4 — {headers_found}/{len(EXPECTED_HEADERS)} headers found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No section headers found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/a4_document_letter.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
