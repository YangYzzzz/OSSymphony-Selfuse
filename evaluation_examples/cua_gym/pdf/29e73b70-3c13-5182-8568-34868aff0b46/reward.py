"""
Reward Script: Bates numbering on legal production document
Task ID: pdf_legal_036
Domain: pdf
Scoring:
  Component 1 (0.2): Output file exists and has 150 pages
  Component 2 (0.3): First and last pages have correct Bates numbers (ABC-005001, ABC-005150)
  Component 3 (0.3): Sequential numbering is correct across sampled pages
  Component 4 (0.2): Date '03/20/2024' present on sampled pages and font ~10pt at bottom-center
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_036'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'production', 'batch_5_bates.pdf')


def extract_bates_info(page):
    """
    Extract Bates number and date from the bottom region of a page.
    Returns (bates_number_str, date_str, font_size, bbox) or (None, None, None, None).
    """
    blocks = page.get_text('dict')['blocks']
    for block in blocks:
        if block.get('type') != 0:
            continue
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                text = span['text'].strip()
                if 'ABC-' in text:
                    bbox = span['bbox']
                    size = span['size']
                    # Extract bates number and date
                    parts = text.split()
                    bates_num = None
                    date_str = None
                    for p in parts:
                        if p.startswith('ABC-'):
                            bates_num = p
                        if '/' in p and len(p) == 10:
                            date_str = p
                    return bates_num, date_str, size, bbox
    return None, None, None, None


def verify_task(file_path):
    """
    Verify Bates numbering task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import fitz

    total_score = 0.0

    # Load the file
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file exists and has 150 pages (0.2 points)
    try:
        page_count = doc.page_count
        if page_count == 150:
            print(f"PASS: Component 1 -- File has {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Expected 150 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: First and last pages have correct Bates numbers (0.3 points)
    try:
        # Check page 1 for ABC-005001
        bates_1, date_1, _, _ = extract_bates_info(doc[0])
        # Check page 150 for ABC-005150
        bates_150, date_150, _, _ = extract_bates_info(doc[149])

        first_ok = (bates_1 == 'ABC-005001')
        last_ok = (bates_150 == 'ABC-005150')

        if first_ok and last_ok:
            print(f"PASS: Component 2 -- First page has {bates_1}, last page has {bates_150} (0.3 pts)")
            total_score += 0.3
        elif first_ok or last_ok:
            print(f"PARTIAL: Component 2 -- First: {bates_1} ({'OK' if first_ok else 'WRONG'}), "
                  f"Last: {bates_150} ({'OK' if last_ok else 'WRONG'}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- First: {bates_1}, Last: {bates_150}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Sequential numbering correct across sampled pages (0.3 points)
    # Sample pages at various positions to verify sequential numbering
    try:
        sample_indices = [0, 1, 9, 24, 49, 74, 99, 124, 148, 149]
        correct_count = 0
        total_samples = len(sample_indices)

        for idx in sample_indices:
            if idx >= doc.page_count:
                continue
            expected_num = f"ABC-{5001 + idx:06d}"
            bates, _, _, _ = extract_bates_info(doc[idx])
            if bates == expected_num:
                correct_count += 1
            else:
                print(f"  Page {idx+1}: expected {expected_num}, found {bates}")

        ratio = correct_count / total_samples
        component_score = round(0.3 * ratio, 2)
        if ratio == 1.0:
            print(f"PASS: Component 3 -- All {total_samples} sampled pages have correct sequential Bates numbers (0.3 pts)")
            total_score += 0.3
        elif ratio > 0:
            print(f"PARTIAL: Component 3 -- {correct_count}/{total_samples} sampled pages correct ({component_score} pts)")
            total_score += component_score
        else:
            print(f"FAIL: Component 3 -- 0/{total_samples} sampled pages have correct Bates numbers")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Date and positioning (0.2 points)
    # Verify '03/20/2024' is present and text is ~10pt at bottom-center
    try:
        check_pages = [0, 49, 99, 149]
        date_ok_count = 0
        position_ok_count = 0
        total_checks = len(check_pages)

        for idx in check_pages:
            if idx >= doc.page_count:
                continue
            _, date_str, font_size, bbox = extract_bates_info(doc[idx])

            # Check date
            if date_str == '03/20/2024':
                date_ok_count += 1
            else:
                print(f"  Page {idx+1}: date expected '03/20/2024', found {date_str}")

            # Check positioning: bottom of page (y > 700 for 792pt page) and roughly centered
            if bbox is not None:
                page_rect = doc[idx].rect
                y_bottom = bbox[3]
                x_center = (bbox[0] + bbox[2]) / 2
                page_center = page_rect.width / 2
                # Text should be in bottom 15% of page and within 100pt of center
                is_bottom = y_bottom > page_rect.height * 0.85
                is_centered = abs(x_center - page_center) < 100
                # Font size should be approximately 10pt (allow 8-12 range)
                is_right_size = font_size is not None and 8 <= font_size <= 12
                if is_bottom and is_centered and is_right_size:
                    position_ok_count += 1
                else:
                    print(f"  Page {idx+1}: position issue - bottom={is_bottom}, centered={is_centered}, "
                          f"size={font_size} (right_size={is_right_size})")

        date_ratio = date_ok_count / total_checks
        pos_ratio = position_ok_count / total_checks
        # Split 0.2 points: 0.1 for date, 0.1 for positioning
        date_score = round(0.1 * date_ratio, 2)
        pos_score = round(0.1 * pos_ratio, 2)
        component_score = date_score + pos_score

        if component_score >= 0.2:
            print(f"PASS: Component 4 -- Date correct on {date_ok_count}/{total_checks} pages, "
                  f"positioning correct on {position_ok_count}/{total_checks} pages (0.2 pts)")
            total_score += component_score
        elif component_score > 0:
            print(f"PARTIAL: Component 4 -- Date: {date_ok_count}/{total_checks}, "
                  f"Position: {position_ok_count}/{total_checks} ({component_score} pts)")
            total_score += component_score
        else:
            print(f"FAIL: Component 4 -- Date: {date_ok_count}/{total_checks}, "
                  f"Position: {position_ok_count}/{total_checks}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
