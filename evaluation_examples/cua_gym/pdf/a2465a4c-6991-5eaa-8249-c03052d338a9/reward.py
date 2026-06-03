"""
Reward Script: Markdown-to-PDF Slides Converter
Task ID: pdf_gf3_033
Domain: pdf
Scoring:
  C1 (0.20) - slides.pdf exists with exactly 15 pages
  C2 (0.20) - Dark background (#1a1a2e / RGB 26,26,45) on all slides
  C3 (0.15) - Text is white/light colored (titles white, body light)
  C4 (0.20) - Correct titles from # headings present on each slide
  C5 (0.10) - Slide numbers appear on each page
  C6 (0.15) - md_to_pdf_slides.py exists and is valid Python
"""

import os
import ast

try:
    import fitz
except ImportError:
    os.system('pip3 install PyMuPDF -q 2>/dev/null')
    try:
        import fitz
    except ImportError:
        fitz = None

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_033'

# Expected titles parsed from # headings in slides.md (15 slides)
EXPECTED_TITLES = [
    'Welcome to DevConf 2026',
    'The State of Cloud Native',
    'Rust in Production',
    'AI-Powered Code Review',
    'Observability Beyond Metrics',
    'The WebAssembly Revolution',
    'Sustainable Software Engineering',
    'Zero Trust Architecture',
    'Developer Experience Matters',
    'GraphQL at Scale',
    'The Future of Databases',
    'Open Source Sustainability',
    'Containerization Best Practices',
    'Workshop: Building Your First ML Pipeline',
    'Closing Remarks and Thank You',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    pdf_path = f'{WORKDIR}/output/slides.pdf'
    script_path = f'{WORKDIR}/scripts/md_to_pdf_slides.py'

    # ----------------------------------------------------------------
    # Component 1: slides.pdf exists with exactly 15 pages (0.20 pts)
    # ----------------------------------------------------------------
    doc = None
    try:
        if fitz is None:
            print(f"FAIL: Component 1 — PyMuPDF (fitz) not available, cannot verify PDF")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        if not os.path.exists(pdf_path):
            print(f"FAIL: Component 1 — {pdf_path} does not exist")
            # If the PDF doesn't exist, nothing else can be checked
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        doc = fitz.open(pdf_path)
        page_count = doc.page_count
        if page_count == 15:
            print(f"PASS: Component 1 — slides.pdf has {page_count} pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — expected 15 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if doc is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ----------------------------------------------------------------
    # Component 2: Dark background on all slides (0.20 pts)
    # Expected: #1a1a2e = RGB(26, 26, 45)
    # ----------------------------------------------------------------
    try:
        dark_bg_count = 0
        for i in range(doc.page_count):
            page = doc[i]
            pix = page.get_pixmap()
            # Sample corner pixel (should be background)
            r, g, b = pix.pixel(5, 5)[:3]
            # Allow some tolerance (within 10 of expected)
            if abs(r - 26) <= 10 and abs(g - 26) <= 10 and abs(b - 45) <= 15:
                dark_bg_count += 1
            else:
                print(f"  Page {i+1}: unexpected bg color ({r},{g},{b})")

        if dark_bg_count == doc.page_count:
            print(f"PASS: Component 2 — all {dark_bg_count} slides have dark background (0.20 pts)")
            total_score += 0.20
        elif dark_bg_count > 0:
            partial = round(0.20 * dark_bg_count / doc.page_count, 3)
            print(f"PARTIAL: Component 2 — {dark_bg_count}/{doc.page_count} slides have dark bg ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no slides have dark background")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: Text is white/light colored (0.15 pts)
    # Title should be white (#ffffff), body text light (>= 160 per channel)
    # ----------------------------------------------------------------
    try:
        light_text_pages = 0
        for i in range(doc.page_count):
            page = doc[i]
            text_dict = page.get_text('dict')
            found_light = 0  # count of light-colored spans
            for block in text_dict.get('blocks', []):
                if 'lines' not in block:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        text = span['text'].strip()
                        if not text:
                            continue
                        color_int = span['color']
                        r = (color_int >> 16) & 0xFF
                        g = (color_int >> 8) & 0xFF
                        b_val = color_int & 0xFF
                        # Light text: all channels >= 128
                        if r >= 128 and g >= 128 and b_val >= 128:
                            found_light += 1
                            break
                    if found_light > 0:
                        break
                if found_light > 0:
                    break
            if found_light > 0:
                light_text_pages += 1

        if light_text_pages == doc.page_count:
            print(f"PASS: Component 3 — all slides have light-colored text (0.15 pts)")
            total_score += 0.15
        elif light_text_pages > 0:
            partial = round(0.15 * light_text_pages / doc.page_count, 3)
            print(f"PARTIAL: Component 3 — {light_text_pages}/{doc.page_count} slides have light text ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no slides have light-colored text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: Correct titles on each slide (0.20 pts)
    # First text line on each page should match expected title
    # ----------------------------------------------------------------
    try:
        title_matches = 0
        for i in range(min(doc.page_count, len(EXPECTED_TITLES))):
            page = doc[i]
            text = page.get_text().strip()
            lines = text.split('\n')
            first_line = lines[0].strip() if lines else ''
            expected = EXPECTED_TITLES[i]
            if expected.lower() in first_line.lower() or first_line.lower() in expected.lower():
                title_matches += 1
            else:
                print(f"  Page {i+1}: expected title '{expected}', found '{first_line[:60]}'")

        if title_matches == len(EXPECTED_TITLES):
            print(f"PASS: Component 4 — all 15 slide titles match (0.20 pts)")
            total_score += 0.20
        elif title_matches > 0:
            partial = round(0.20 * title_matches / len(EXPECTED_TITLES), 3)
            print(f"PARTIAL: Component 4 — {title_matches}/{len(EXPECTED_TITLES)} titles match ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — no titles match expected values")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ----------------------------------------------------------------
    # Component 5: Slide numbers on each page (0.10 pts)
    # Last text element on each page should be the page number (1-15)
    # ----------------------------------------------------------------
    try:
        numbered_pages = 0
        for i in range(doc.page_count):
            page = doc[i]
            text = page.get_text().strip()
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            if lines:
                last_line = lines[-1]
                # The slide number should be the page index + 1
                if last_line == str(i + 1):
                    numbered_pages += 1
                else:
                    print(f"  Page {i+1}: expected slide number '{i+1}', last line is '{last_line[:20]}'")

        if numbered_pages == doc.page_count:
            print(f"PASS: Component 5 — all slides have correct slide numbers (0.10 pts)")
            total_score += 0.10
        elif numbered_pages > 0:
            partial = round(0.10 * numbered_pages / doc.page_count, 3)
            print(f"PARTIAL: Component 5 — {numbered_pages}/{doc.page_count} slides have numbers ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — no slides have slide numbers")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    # ----------------------------------------------------------------
    # Component 6: md_to_pdf_slides.py exists and is valid Python (0.15 pts)
    # ----------------------------------------------------------------
    try:
        if not os.path.exists(script_path):
            print(f"FAIL: Component 6 — {script_path} does not exist")
        else:
            with open(script_path, 'r') as f:
                script_content = f.read()

            # Verify it parses as valid Python
            ast.parse(script_content)

            # Check it references key elements (not just any Python file)
            has_md_read = 'slides.md' in script_content or 'markdown' in script_content.lower() or '.md' in script_content
            has_pdf_write = 'slides.pdf' in script_content or 'pdf' in script_content.lower()
            has_reportlab_or_fitz = 'reportlab' in script_content or 'fitz' in script_content or 'pymupdf' in script_content.lower()

            if has_md_read and has_pdf_write and has_reportlab_or_fitz:
                print(f"PASS: Component 6 — valid Python script with MD-to-PDF logic (0.15 pts)")
                total_score += 0.15
            elif has_md_read and has_pdf_write:
                print(f"PARTIAL: Component 6 — valid Python script but missing PDF library import (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — script exists but missing key MD/PDF references")
    except SyntaxError as e:
        print(f"FAIL: Component 6 — script has syntax error: {e}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
