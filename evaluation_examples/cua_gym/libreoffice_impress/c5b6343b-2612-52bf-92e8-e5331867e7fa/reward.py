"""
Reward Script: Export slides 2-5 as PDF to Desktop
Task ID: impstruct_039
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): PDF file exists at correct path with valid PDF header
  Component 2 (0.35): PDF has exactly 4 pages (slides 2-5)
  Component 3 (0.40): PDF text content matches slides 2-5 from the presentation
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'impstruct_039'
PDF_PATH = os.path.join(WORKDIR, 'Desktop', 'slides_2to5.pdf')
PPTX_PATH = os.path.join(WORKDIR, 'full_presentation.pptx')


def get_pdf_page_count(pdf_path):
    """Parse PDF page count using pdfinfo CLI tool (available on VM)."""
    stream = os.popen(f'pdfinfo "{pdf_path}" 2>/dev/null')
    output = stream.read()
    stream.close()
    match = re.search(r'Pages:\s+(\d+)', output)
    if match:
        return int(match.group(1))
    return None


def get_pdf_text(pdf_path):
    """Extract text from entire PDF using pdftotext CLI tool."""
    stream = os.popen(f'pdftotext "{pdf_path}" - 2>/dev/null')
    text = stream.read()
    stream.close()
    return text


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: source PPTX must exist
    if not os.path.exists(PPTX_PATH):
        print(f"CRITICAL: Source PPTX not found at {PPTX_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF exists at correct path with valid PDF header (0.25 points)
    try:
        if os.path.exists(PDF_PATH):
            with open(PDF_PATH, 'rb') as f:
                header = f.read(5)
            if header == b'%PDF-':
                file_size = os.path.getsize(PDF_PATH)
                if file_size > 1000:  # A valid PDF with 4 slides should be > 1KB
                    print(f"PASS: Component 1 — PDF exists at {PDF_PATH}, valid header, size={file_size} bytes (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 1 — PDF exists but too small ({file_size} bytes), likely corrupt")
            else:
                print(f"FAIL: Component 1 — File exists but not a valid PDF (header: {header})")
        else:
            print(f"FAIL: Component 1 — PDF not found at {PDF_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: PDF has exactly 4 pages (slides 2-5 inclusive) (0.35 points)
    try:
        page_count = get_pdf_page_count(PDF_PATH)
        if page_count is not None:
            if page_count == 4:
                print(f"PASS: Component 2 — PDF has exactly 4 pages (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — PDF has {page_count} pages, expected 4")
        else:
            print(f"FAIL: Component 2 — Could not determine PDF page count")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDF text content matches slides 2-5 (0.40 points)
    # Verify by checking that text from slides 2-5 IS present and text unique
    # to other slides (1, 6-12) is NOT present.
    try:
        pdf_text = get_pdf_text(PDF_PATH)
        if not pdf_text or len(pdf_text.strip()) < 50:
            print(f"FAIL: Component 3 — Could not extract meaningful text from PDF")
        else:
            # Key phrases expected in slides 2-5 (from PPTX exploration)
            expected_phrases = [
                "Executive Summary",        # Slide 2
                "Revenue Breakdown",        # Slide 3
                "Customer Metrics",         # Slide 4
                "Product Development",      # Slide 5
            ]

            # Phrases that should NOT be in the PDF (unique to slides 1, 6-12)
            excluded_phrases = [
                "Q1 2025 Business Review",  # Slide 1 title
                "Thank You",               # Slide 12
                "Team Performance",         # Slide 6
                "Competitive Landscape",    # Slide 8
            ]

            # Check expected phrases present
            expected_found = 0
            for phrase in expected_phrases:
                if phrase.lower() in pdf_text.lower():
                    expected_found += 1
                    print(f"  Found expected phrase: '{phrase}'")
                else:
                    print(f"  Missing expected phrase: '{phrase}'")

            # Check excluded phrases absent
            excluded_absent = 0
            for phrase in excluded_phrases:
                if phrase.lower() not in pdf_text.lower():
                    excluded_absent += 1
                    print(f"  Correctly absent: '{phrase}'")
                else:
                    print(f"  Incorrectly present: '{phrase}'")

            # Score: half for expected found, half for excluded absent
            expected_ratio = expected_found / len(expected_phrases)
            excluded_ratio = excluded_absent / len(excluded_phrases)
            content_score = 0.40 * (0.5 * expected_ratio + 0.5 * excluded_ratio)

            if content_score > 0:
                print(f"PASS: Component 3 — Content verification ({expected_found}/{len(expected_phrases)} expected, "
                      f"{excluded_absent}/{len(excluded_phrases)} correctly excluded) ({content_score:.2f} pts)")
                total_score += content_score
            else:
                print(f"FAIL: Component 3 — Content does not match slides 2-5")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
