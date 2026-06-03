"""
Reward Script: Add copyright footer to first page of PDF
Task ID: pdf_res_057
Domain: pdf
Scoring:
  Component 1: Output file exists at correct path (0.15 pts)
  Component 2: PDF has 10 pages preserved (0.15 pts)
  Component 3: Page 0 contains exact copyright text (0.35 pts)
  Component 4: Copyright text is 7pt italic font (0.20 pts)
  Component 5: Pages 1-9 do NOT contain copyright text (0.15 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_057'

OUTPUT_PATH = os.path.join(WORKDIR, 'papers', 'published_paper_copyright.pdf')
COPYRIGHT_TEXT = '\u00a9 2026 IEEE. Personal use permitted.'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.15 points)
    try:
        if os.path.isfile(OUTPUT_PATH):
            print(f"PASS: Component 1 — Output file exists at {OUTPUT_PATH} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Output file not found at {OUTPUT_PATH}")
            # No file means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the PDF
    try:
        import fitz
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {OUTPUT_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: PDF has 10 pages (0.15 points)
    try:
        page_count = len(doc)
        if page_count == 10:
            print(f"PASS: Component 2 — PDF has 10 pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 10 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page 0 contains the exact copyright text (0.35 points)
    try:
        page0 = doc[0]
        page0_text = page0.get_text()
        if COPYRIGHT_TEXT in page0_text:
            print(f"PASS: Component 3 — Page 0 contains copyright text '{COPYRIGHT_TEXT}' (0.35 pts)")
            total_score += 0.35
        else:
            # Check for partial match
            if '2026 IEEE' in page0_text:
                print(f"FAIL: Component 3 — Found partial copyright text on page 0 but not exact match")
            else:
                print(f"FAIL: Component 3 — Copyright text not found on page 0")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Copyright text is 7pt italic font (0.20 points)
    try:
        page0 = doc[0]
        blocks = page0.get_text('dict')['blocks']
        # Search for copyright span and extract font properties
        copyright_span = None
        for b in blocks:
            if 'lines' not in b:
                continue
            for line in b['lines']:
                for span in line['spans']:
                    if COPYRIGHT_TEXT in span['text'] or '2026 IEEE' in span['text']:
                        copyright_span = span
                        break
                if copyright_span:
                    break
            if copyright_span:
                break

        if copyright_span is not None:
            actual_size = copyright_span['size']
            actual_font = copyright_span['font']
            actual_flags = copyright_span['flags']
            print(f"  Found copyright span: font='{actual_font}', size={actual_size}, flags={actual_flags}")

            # Validate font size is ~7pt and font is italic
            size_ok = abs(actual_size - 7.0) < 0.5
            italic_ok = (actual_flags & 2) != 0 or 'italic' in actual_font.lower() or 'oblique' in actual_font.lower()

            if size_ok and italic_ok:
                print(f"PASS: Component 4 — Copyright text is 7pt italic (0.20 pts)")
                total_score += 0.20
            else:
                details = []
                if not size_ok:
                    details.append(f"size={actual_size}, expected ~7.0")
                if not italic_ok:
                    details.append(f"not italic (font={actual_font}, flags={actual_flags})")
                print(f"FAIL: Component 4 — Font issues: {', '.join(details)}")
        else:
            print(f"FAIL: Component 4 — Copyright span not found in text dict")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Pages 1-9 do NOT contain the copyright text (0.15 points)
    try:
        copyright_on_other_pages = []
        for i in range(1, len(doc)):
            page_text = doc[i].get_text()
            if COPYRIGHT_TEXT in page_text or '2026 IEEE' in page_text:
                copyright_on_other_pages.append(i)

        if len(copyright_on_other_pages) == 0:
            print(f"PASS: Component 5 — Pages 1-9 do not contain copyright text (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Copyright text found on pages: {copyright_on_other_pages}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
