"""
Reward Script: Add company header and footer to all pages of a PDF
Task ID: pdf_pw_017
Domain: pdf
Scoring:
  Component 1 (0.25): Header text present on all 12 pages in top margin
  Component 2 (0.20): Header styling - 14pt bold blue
  Component 3 (0.25): Footer text present on all 12 pages in bottom margin
  Component 4 (0.15): Footer styling - 8pt gray
  Component 5 (0.15): Original content preserved (page count unchanged)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_017'

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

    num_pages = len(doc)

    # Component 1: Header text "Nexus Technologies Inc." on all 12 pages in top margin (0.25 points)
    try:
        header_pages = 0
        for i in range(num_pages):
            page = doc[i]
            data = page.get_text("dict")
            found_header = False
            for block in data["blocks"]:
                if block.get("type", 0) != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        # Header should be in top margin area (y < 50)
                        if span["bbox"][1] < 50 and "Nexus Technologies Inc." in span["text"]:
                            found_header = True
            if found_header:
                header_pages += 1

        if header_pages == num_pages and num_pages >= 12:
            print(f"PASS: Component 1 - Header found on all {header_pages}/{num_pages} pages (0.25 pts)")
            total_score += 0.25
        elif header_pages > 0:
            # Partial credit proportional to pages with header
            partial = 0.25 * (header_pages / num_pages)
            print(f"PARTIAL: Component 1 - Header found on {header_pages}/{num_pages} pages ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - Header not found on any page")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Header styling - 14pt bold blue (0.20 points)
    try:
        style_ok_count = 0
        for i in range(num_pages):
            page = doc[i]
            data = page.get_text("dict")
            for block in data["blocks"]:
                if block.get("type", 0) != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["bbox"][1] < 50 and "Nexus Technologies Inc." in span["text"]:
                            size_ok = abs(span["size"] - 14.0) < 1.0
                            is_bold = bool(span["flags"] & 16)
                            c = span["color"]
                            r = (c >> 16) & 0xFF
                            g = (c >> 8) & 0xFF
                            b = c & 0xFF
                            # Blue: expect low R, low G, high B (context says 0,0,0.8 = 0,0,204)
                            is_blue = r < 30 and g < 30 and b > 150
                            if size_ok and is_bold and is_blue:
                                style_ok_count += 1

        if style_ok_count == num_pages and num_pages >= 12:
            print(f"PASS: Component 2 - Header style correct (14pt, bold, blue) on all pages (0.20 pts)")
            total_score += 0.20
        elif style_ok_count > 0:
            partial = 0.20 * (style_ok_count / num_pages)
            print(f"PARTIAL: Component 2 - Header style correct on {style_ok_count}/{num_pages} pages ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - Header style incorrect on all pages")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Footer text "Confidential - Do Not Distribute" on all pages in bottom margin (0.25 points)
    try:
        footer_pages = 0
        for i in range(num_pages):
            page = doc[i]
            data = page.get_text("dict")
            found_footer = False
            for block in data["blocks"]:
                if block.get("type", 0) != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        # Footer should be in bottom margin area (y > 755)
                        if span["bbox"][1] > 755 and "Confidential - Do Not Distribute" in span["text"]:
                            found_footer = True
            if found_footer:
                footer_pages += 1

        if footer_pages == num_pages and num_pages >= 12:
            print(f"PASS: Component 3 - Footer found on all {footer_pages}/{num_pages} pages (0.25 pts)")
            total_score += 0.25
        elif footer_pages > 0:
            partial = 0.25 * (footer_pages / num_pages)
            print(f"PARTIAL: Component 3 - Footer found on {footer_pages}/{num_pages} pages ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - Footer not found on any page")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Footer styling - 8pt gray (0.15 points)
    try:
        footer_style_ok = 0
        for i in range(num_pages):
            page = doc[i]
            data = page.get_text("dict")
            for block in data["blocks"]:
                if block.get("type", 0) != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["bbox"][1] > 755 and "Confidential - Do Not Distribute" in span["text"]:
                            size_ok = abs(span["size"] - 8.0) < 1.0
                            c = span["color"]
                            r = (c >> 16) & 0xFF
                            g = (c >> 8) & 0xFF
                            b = c & 0xFF
                            # Gray: R, G, B should be similar and in mid-range (context: 128,128,128)
                            is_gray = (abs(r - g) < 30 and abs(g - b) < 30 and r > 80 and r < 200)
                            if size_ok and is_gray:
                                footer_style_ok += 1

        if footer_style_ok == num_pages and num_pages >= 12:
            print(f"PASS: Component 4 - Footer style correct (8pt, gray) on all pages (0.15 pts)")
            total_score += 0.15
        elif footer_style_ok > 0:
            partial = 0.15 * (footer_style_ok / num_pages)
            print(f"PARTIAL: Component 4 - Footer style correct on {footer_style_ok}/{num_pages} pages ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - Footer style incorrect on all pages")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Original content preserved - page count matches original 12 pages (0.15 points)
    # This checks that the branded file didn't lose/add pages compared to the original
    try:
        original_path = os.path.join(WORKDIR, 'Documents', 'whitepaper.pdf')
        if os.path.exists(original_path):
            orig_doc = fitz.open(original_path)
            orig_pages = len(orig_doc)
            orig_doc.close()

            if num_pages == orig_pages and num_pages == 12:
                print(f"PASS: Component 5 - Page count preserved ({num_pages} pages) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 - Page count mismatch: branded={num_pages}, original={orig_pages}")
        else:
            # If original doesn't exist, just check expected page count
            if num_pages == 12:
                print(f"PASS: Component 5 - Page count is 12 as expected (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 - Expected 12 pages, found {num_pages}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/whitepaper_branded.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
