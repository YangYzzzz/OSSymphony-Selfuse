"""
Reward Script: Export presentation as PDF handout with 4 slides per page
Task ID: impstruct_043
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): PDF file exists at /home/user/Desktop/handouts.pdf
  Component 2 (0.30): PDF has exactly 3 pages (12 slides / 4 per page)
  Component 3 (0.20): PDF page dimensions are A4 portrait (handout format)
  Component 4 (0.25): PDF content includes text from all 12 slides grouped 4 per page
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'impstruct_043'
PDF_PATH = os.path.join(WORKDIR, 'Desktop', 'handouts.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF file exists at correct path (0.25 points)
    # This is task-introduced: initial_env has no PDF at all
    try:
        if os.path.isfile(PDF_PATH):
            file_size = os.path.getsize(PDF_PATH)
            if file_size > 100:
                print(f"PASS: Component 1 - PDF exists at {PDF_PATH} (size: {file_size} bytes) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 - PDF exists but too small ({file_size} bytes), likely corrupt")
        else:
            print(f"FAIL: Component 1 - PDF not found at {PDF_PATH}")
            # No point checking further if file doesn't exist
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Read PDF raw data for subsequent checks
    try:
        with open(PDF_PATH, 'rb') as f:
            pdf_data = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read PDF: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: PDF has exactly 3 pages (0.30 points)
    # 12 slides / 4 slides per page = 3 pages
    # This is task-introduced: no PDF exists in initial_env
    try:
        count_match = re.search(b'/Count\\s+(\\d+)', pdf_data)
        if count_match:
            page_count = int(count_match.group(1).decode())
            if page_count == 3:
                print(f"PASS: Component 2 - PDF has 3 pages (4 slides/page x 3 = 12 slides) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - PDF has {page_count} pages, expected 3 (12 slides / 4 per page)")
        else:
            print(f"FAIL: Component 2 - Could not determine page count from PDF")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: PDF page dimensions are A4 portrait (0.20 points)
    # Handouts are typically exported in A4 portrait format
    # A4 = 595.28 x 841.89 pts (or close to it)
    # This is task-introduced: no PDF exists in initial_env
    try:
        mediabox_match = re.search(b'/MediaBox\\s*\\[([^\\]]+)\\]', pdf_data)
        if mediabox_match:
            dims = mediabox_match.group(1).decode().strip().split()
            if len(dims) == 4:
                width = float(dims[2])
                height = float(dims[3])
                # A4 portrait: width ~595, height ~842
                # Allow some tolerance for different PDF generators
                is_portrait = height > width
                is_reasonable_size = (500 < width < 700) and (700 < height < 1000)
                if is_portrait and is_reasonable_size:
                    print(f"PASS: Component 3 - PDF is portrait format ({width:.1f} x {height:.1f} pts) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 3 - PDF dimensions {width:.1f} x {height:.1f} pts, "
                          f"expected portrait A4-like (portrait={is_portrait})")
            else:
                print(f"FAIL: Component 3 - Could not parse MediaBox dimensions")
        else:
            print(f"FAIL: Component 3 - No MediaBox found in PDF")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: PDF content shows multiple slides per page (0.25 points)
    # Verify by extracting text and checking that "Slide N" labels or
    # slide content from the original PPTX appears grouped appropriately.
    # We check for content from several slides to confirm they were included.
    # This is task-introduced: no PDF exists in initial_env
    try:
        # Use pdftotext if available to extract text
        text_content = ""
        pdftotext_available = os.path.exists('/usr/bin/pdftotext')
        if pdftotext_available:
            import tempfile
            tmp = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
            tmp.close()
            os.system(f'pdftotext "{PDF_PATH}" "{tmp.name}" 2>/dev/null')
            with open(tmp.name, 'r', errors='ignore') as f:
                text_content = f.read()
            os.unlink(tmp.name)
        else:
            # Fallback: try to decode raw PDF streams (less reliable)
            text_content = pdf_data.decode('latin-1', errors='ignore')

        # Check for content from multiple slides
        # The original presentation has 12 slides with these key phrases
        slide_markers = [
            "Business Review",       # Slide 1
            "Agenda",                # Slide 2
            "Revenue Overview",      # Slide 3
            "Customer Acquisition",  # Slide 4
            "Product Development",   # Slide 5
            "Engineering",           # Slide 6
            "Marketing Performance", # Slide 7
            "Regional Expansion",    # Slide 8
            "Financial Summary",     # Slide 9
            "Strategic Partner",     # Slide 10
            "Strategic Priorities",  # Slide 11
            "Thank You",            # Slide 12
        ]

        found_count = 0
        for marker in slide_markers:
            if marker.lower() in text_content.lower():
                found_count += 1

        # Need at least 8 of 12 slide contents to be present
        # (some tolerance for text extraction imprecision)
        if found_count >= 8:
            print(f"PASS: Component 4 - PDF contains content from {found_count}/12 slides (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - PDF contains content from only {found_count}/12 slides, expected >= 8")
            if found_count > 0:
                print(f"  (partial content detected, but insufficient)")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
