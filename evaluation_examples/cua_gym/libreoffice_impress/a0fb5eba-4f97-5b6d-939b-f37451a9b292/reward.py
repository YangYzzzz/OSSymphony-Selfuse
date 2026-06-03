"""
Reward Script: Export slide master pages as separate PDF pages appended after regular slides
Task ID: impress_el_045
Domain: libreoffice_impress
Scoring:
  Component 1 (0.15): PDF file exists at expected path
  Component 2 (0.25): PDF has >= 13 pages (10 regular + 3 master reference)
  Component 3 (0.25): First 10 pages contain expected regular slide content
  Component 4 (0.35): Last pages contain master/design reference content for 3 themes
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'impress_el_045'


def verify_task(pdf_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF file exists (0.15 points)
    # This is a task-introduced change: initial_env has NO PDF file.
    try:
        if not os.path.exists(pdf_path):
            print(f"FAIL: Component 1 — PDF file not found at {pdf_path}")
            print("REWARD: 0.0")
            return 0.0

        file_size = os.path.getsize(pdf_path)
        if file_size < 1000:
            print(f"FAIL: Component 1 — PDF file too small ({file_size} bytes), likely corrupt")
            print("REWARD: 0.0")
            return 0.0

        if file_size >= 1000:
            print(f"PASS: Component 1 — PDF file exists at {pdf_path} ({file_size} bytes) (0.15 pts)")
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load PDF using pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
    except ImportError:
        print("ERROR: pypdf not available — install with: pip3 install pypdf")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot read PDF {pdf_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: PDF has >= 13 pages (10 regular slides + 3 master reference pages) (0.25 points)
    try:
        if num_pages >= 13:
            print(f"PASS: Component 2 — PDF has {num_pages} pages (>= 13 expected) (0.25 pts)")
            total_score += 0.25
        elif num_pages > 10:
            # Partial credit if some master pages present
            partial = 0.25 * (num_pages - 10) / 3.0
            print(f"PARTIAL: Component 2 — PDF has {num_pages} pages (expected >= 13), partial credit {partial:.2f}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — PDF has only {num_pages} pages (expected >= 13, i.e. 10 regular + 3 master)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Helper: extract text from a PDF page
    def get_page_text(page_idx):
        try:
            return reader.pages[page_idx].extract_text() or ""
        except Exception:
            return ""

    # Component 3: First 10 pages contain expected regular slide content (0.25 points)
    # Check for key text from the known slides
    try:
        expected_slide_markers = [
            "Acme Corporation",            # Slide 1
            "Revenue grew 18%",            # Slide 2
            "Net Revenue",                 # Slide 3
            "Carbon neutral",              # Slide 4
            "Water usage reduced",         # Slide 5
            "STEM education",              # Slide 6
            "Platform v3.0",               # Slide 7
            "API response time",           # Slide 8
            "Berlin, Tokyo",               # Slide 9
            "Finalize 2026 budget",        # Slide 10
        ]

        matches_found = 0
        for i, marker in enumerate(expected_slide_markers):
            if i < num_pages:
                page_text = get_page_text(i)
                if marker in page_text:
                    matches_found += 1
                else:
                    print(f"  INFO: Page {i+1} does not contain expected marker '{marker}'")

        if matches_found >= 8:
            print(f"PASS: Component 3 — {matches_found}/10 regular slide pages contain expected content (0.25 pts)")
            total_score += 0.25
        elif matches_found >= 5:
            partial = 0.25 * matches_found / 10.0
            print(f"PARTIAL: Component 3 — {matches_found}/10 regular slide matches, partial credit {partial:.2f}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {matches_found}/10 regular slide pages match expected content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Master/design reference pages present after regular slides (0.35 points)
    # The last 3 pages (or pages after the 10 regular slides) should contain
    # design reference content for 3 themes: Corporate, Nature, Clean
    try:
        theme_names = ["Corporate", "Nature", "Clean"]
        design_ref_keywords = ["Design Reference", "Master Page", "Background"]

        themes_found = []
        design_ref_pages_found = 0

        # Search pages from index 10 onward (after the 10 regular slides)
        for page_idx in range(10, num_pages):
            page_text = get_page_text(page_idx)

            # Check if this page is a design reference / master page
            is_design_ref = any(kw in page_text for kw in design_ref_keywords)
            if is_design_ref:
                design_ref_pages_found += 1
                for theme in theme_names:
                    if theme in page_text and theme not in themes_found:
                        themes_found.append(theme)
                        print(f"  Found design reference for '{theme}' theme on page {page_idx + 1}")

        themes_score = len(themes_found) / 3.0  # 0.0 to 1.0

        if len(themes_found) == 3 and design_ref_pages_found >= 3:
            print(f"PASS: Component 4 — All 3 master theme reference pages found ({themes_found}) (0.35 pts)")
            total_score += 0.35
        elif len(themes_found) > 0:
            partial = 0.35 * themes_score
            print(f"PARTIAL: Component 4 — Found {len(themes_found)}/3 theme references ({themes_found}), partial credit {partial:.2f}")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No design reference / master theme pages found after slide 10")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
pdf_path = f'{WORKDIR}/{TASK_ID}.pdf'
if not os.path.exists(pdf_path):
    print(f"File not found: {pdf_path}")
    print("REWARD: 0.0")
else:
    verify_task(pdf_path)
