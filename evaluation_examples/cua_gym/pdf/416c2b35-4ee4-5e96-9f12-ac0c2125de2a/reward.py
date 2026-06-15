"""
Reward Script: Add Bates numbers and confidentiality designation to legal document
Task ID: pdf_legal_071
Domain: pdf
Scoring:
  Component 1: Output file exists with correct page count (0.15)
  Component 2: Bates numbers JONES-002001 through JONES-002085 on all pages (0.35)
  Component 3: Confidentiality legend on all pages (0.30)
  Component 4: Confidentiality text is red and 7pt font (0.20)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_071'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'production', 'set_2_stamped.pdf')

EXPECTED_PAGE_COUNT = 85
BATES_PREFIX = 'JONES-002'
CONFIDENTIAL_TEXT = 'CONFIDENTIAL - SUBJECT TO PROTECTIVE ORDER'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
    except ImportError:
        try:
            import pymupdf as fitz
        except ImportError:
            print("CRITICAL: Cannot import fitz or pymupdf")
            print("REWARD: 0.0")
            return 0.0

    # Precondition: file must exist and be loadable
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

    # Component 1: Output file has correct page count (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 - Page count is {page_count} as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Expected {EXPECTED_PAGE_COUNT} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Bates numbers JONES-002001 through JONES-002085 on all pages (0.35 points)
    try:
        bates_correct = 0
        bates_total = doc.page_count
        bates_pattern = re.compile(r'JONES-002\d{3}')

        for i in range(doc.page_count):
            page = doc[i]
            rect = page.rect
            # Check bottom strip of page (last 50 points)
            bottom_rect = fitz.Rect(0, rect.height - 50, rect.width, rect.height)
            text = page.get_text('text', clip=bottom_rect)

            expected_bates = f"JONES-{2001 + i:06d}"
            if expected_bates in text:
                bates_correct += 1
            else:
                # Also check with the pattern in case of minor formatting
                matches = bates_pattern.findall(text)
                if matches:
                    print(f"  Page {i}: Found Bates '{matches[0]}' but expected '{expected_bates}'")
                else:
                    if i < 3 or i == doc.page_count - 1:
                        print(f"  Page {i}: No Bates number found in bottom region")

        if bates_total > 0:
            bates_ratio = bates_correct / bates_total
            bates_score = round(0.35 * bates_ratio, 4)
            if bates_ratio == 1.0:
                print(f"PASS: Component 2 - All {bates_total} pages have correct Bates numbers (0.35 pts)")
            else:
                print(f"PARTIAL: Component 2 - {bates_correct}/{bates_total} pages have correct Bates numbers ({bates_score} pts)")
            total_score += bates_score
        else:
            print("FAIL: Component 2 - No pages to check")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Confidentiality legend on all pages (0.30 points)
    try:
        conf_correct = 0
        conf_total = doc.page_count

        for i in range(doc.page_count):
            page = doc[i]
            rect = page.rect
            bottom_rect = fitz.Rect(0, rect.height - 50, rect.width, rect.height)
            text = page.get_text('text', clip=bottom_rect)

            if CONFIDENTIAL_TEXT in text:
                conf_correct += 1
            else:
                # Case-insensitive fallback
                if CONFIDENTIAL_TEXT.lower() in text.lower():
                    conf_correct += 1
                elif i < 3 or i == doc.page_count - 1:
                    print(f"  Page {i}: Confidentiality legend not found")

        if conf_total > 0:
            conf_ratio = conf_correct / conf_total
            conf_score = round(0.30 * conf_ratio, 4)
            if conf_ratio == 1.0:
                print(f"PASS: Component 3 - All {conf_total} pages have confidentiality legend (0.30 pts)")
            else:
                print(f"PARTIAL: Component 3 - {conf_correct}/{conf_total} pages have confidentiality legend ({conf_score} pts)")
            total_score += conf_score
        else:
            print("FAIL: Component 3 - No pages to check")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Confidentiality text is red and 7pt (0.20 points)
    # Check a sample of pages (first, middle, last) for font properties
    try:
        sample_pages = [0, doc.page_count // 2, doc.page_count - 1]
        red_and_7pt_count = 0
        sample_total = len(sample_pages)

        for i in sample_pages:
            page = doc[i]
            rect = page.rect
            bottom_rect = fitz.Rect(0, rect.height - 50, rect.width, rect.height)
            blocks = page.get_text('dict', clip=bottom_rect)

            found_conf_span = False
            for b in blocks.get('blocks', []):
                if 'lines' not in b:
                    continue
                for line in b['lines']:
                    for span in line['spans']:
                        span_text = span.get('text', '')
                        if 'CONFIDENTIAL' in span_text or 'PROTECTIVE ORDER' in span_text:
                            found_conf_span = True
                            color_int = span.get('color', 0)
                            font_size = span.get('size', 0)

                            # Red = 0xFF0000 (16711680) in integer form
                            is_red = (color_int == 0xFF0000)
                            is_7pt = (abs(font_size - 7.0) < 0.5)

                            if is_red and is_7pt:
                                red_and_7pt_count += 1
                            else:
                                if i < 3 or i == doc.page_count - 1:
                                    print(f"  Page {i}: Confidentiality font color=0x{color_int:06X} size={font_size} (expected red 0xFF0000, 7pt)")
                            break
                    if found_conf_span:
                        break
                if found_conf_span:
                    break

            if not found_conf_span and (i < 3 or i == doc.page_count - 1):
                print(f"  Page {i}: No confidentiality span found for font check")

        if sample_total > 0:
            fmt_ratio = red_and_7pt_count / sample_total
            fmt_score = round(0.20 * fmt_ratio, 4)
            if fmt_ratio == 1.0:
                print(f"PASS: Component 4 - Confidentiality text is red 7pt on sampled pages (0.20 pts)")
            else:
                print(f"PARTIAL: Component 4 - {red_and_7pt_count}/{sample_total} sampled pages have red 7pt ({fmt_score} pts)")
            total_score += fmt_score
        else:
            print("FAIL: Component 4 - No sample pages to check")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
