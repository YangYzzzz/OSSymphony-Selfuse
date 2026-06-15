"""
Reward Script: Bates Numbering on Defense Exhibits PDF
Task ID: pdf_legal_029
Domain: pdf
Scoring:
  Component 1 (0.20) — Output file exists and is a valid PDF with 75 pages
  Component 2 (0.40) — All 75 pages contain correct sequential Bates numbers DEF-EX-000001..000075
  Component 3 (0.20) — Bates numbers use Courier font at 9pt
  Component 4 (0.20) — Bates numbers are positioned at bottom-left of each page
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_029'

OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'defense_exhibits_bates.pdf')


def verify_task(file_path):
    """
    Verify Bates numbering task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF
    try:
        import fitz
    except ImportError:
        try:
            import pymupdf as fitz
        except ImportError:
            print("CRITICAL: Neither fitz nor pymupdf available")
            print("REWARD: 0.0")
            return 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file is a valid 75-page PDF (0.20 points)
    # This checks that the output file was created with the right page count.
    # The initial_env has no output file, so this will fail there.
    try:
        page_count = len(doc)
        if page_count == 75:
            print(f"PASS: Component 1 — Output PDF has 75 pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 75 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All pages have correct sequential Bates numbers (0.40 points)
    # Check that each page contains the text DEF-EX-NNNNNN with correct sequence.
    # Award partial credit proportional to how many pages have correct numbers.
    try:
        correct_count = 0
        for i in range(min(page_count, 75)):
            expected_bates = f"DEF-EX-{i+1:06d}"
            page_text = doc[i].get_text()
            if expected_bates in page_text:
                correct_count += 1
            else:
                if correct_count < 3 or i >= 73:
                    # Log first few and last few mismatches
                    print(f"  Page {i+1}: expected '{expected_bates}', not found in text")

        if correct_count == 75:
            print(f"PASS: Component 2 — All 75 pages have correct Bates numbers (0.40 pts)")
            total_score += 0.40
        elif correct_count > 0:
            partial = 0.40 * (correct_count / 75)
            print(f"PARTIAL: Component 2 — {correct_count}/75 pages have correct Bates numbers ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have correct Bates numbers")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bates numbers use Courier font at 9pt (0.20 points)
    # Sample pages 0, 37, 74 to check font properties.
    try:
        sample_pages = [0, 37, 74]
        font_correct = 0
        for pi in sample_pages:
            page = doc[pi]
            expected_bates = f"DEF-EX-{pi+1:06d}"
            blocks = page.get_text('dict')['blocks']
            found = False
            for b in blocks:
                if 'lines' not in b:
                    continue
                for line in b['lines']:
                    for span in line['spans']:
                        if expected_bates in span['text']:
                            font_name = span['font']
                            font_size = span['size']
                            is_courier = 'courier' in font_name.lower()
                            is_9pt = abs(font_size - 9.0) < 0.5
                            if is_courier and is_9pt:
                                font_correct += 1
                                found = True
                            else:
                                print(f"  Page {pi+1}: font='{font_name}' size={font_size} (expected Courier 9pt)")
                                found = True
                            break
                    if found:
                        break
                if found:
                    break
            if not found:
                print(f"  Page {pi+1}: Bates number span not found in text dict")

        if font_correct == len(sample_pages):
            print(f"PASS: Component 3 — Bates numbers use Courier 9pt font (0.20 pts)")
            total_score += 0.20
        elif font_correct > 0:
            partial = 0.20 * (font_correct / len(sample_pages))
            print(f"PARTIAL: Component 3 — {font_correct}/{len(sample_pages)} sampled pages have correct font ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Bates numbers do not use Courier 9pt font")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Bates numbers positioned at bottom-left (0.20 points)
    # Check that the y-position of the Bates text is in the lower portion of the page
    # and x-position is on the left side. Sample pages 0, 37, 74.
    try:
        position_correct = 0
        for pi in sample_pages:
            page = doc[pi]
            page_height = page.rect.height
            page_width = page.rect.width
            expected_bates = f"DEF-EX-{pi+1:06d}"
            blocks = page.get_text('dict')['blocks']
            found = False
            for b in blocks:
                if 'lines' not in b:
                    continue
                for line in b['lines']:
                    for span in line['spans']:
                        if expected_bates in span['text']:
                            bbox = span['bbox']
                            # bbox = (x0, y0, x1, y1)
                            x0, y0, x1, y1 = bbox
                            # Bottom-left means: x0 should be in left half, y1 should be in bottom 15%
                            is_left = x0 < page_width * 0.5
                            is_bottom = y1 > page_height * 0.85
                            if is_left and is_bottom:
                                position_correct += 1
                            else:
                                print(f"  Page {pi+1}: Bates at bbox={bbox}, page={page_width}x{page_height} "
                                      f"(left={is_left}, bottom={is_bottom})")
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
            if not found:
                print(f"  Page {pi+1}: Bates number span not found for position check")

        if position_correct == len(sample_pages):
            print(f"PASS: Component 4 — Bates numbers at bottom-left position (0.20 pts)")
            total_score += 0.20
        elif position_correct > 0:
            partial = 0.20 * (position_correct / len(sample_pages))
            print(f"PARTIAL: Component 4 — {position_correct}/{len(sample_pages)} sampled pages correctly positioned ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Bates numbers not positioned at bottom-left")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
