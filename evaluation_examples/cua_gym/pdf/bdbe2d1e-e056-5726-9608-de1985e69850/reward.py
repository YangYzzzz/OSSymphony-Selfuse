"""
Reward Script: OCR extraction from scanned PDF
Task ID: pdf_res_013
Domain: pdf
Scoring:
  - Component 1 (0.20): ocr_output.txt exists and is non-empty
  - Component 2 (0.25): Substantial text content (>= 1000 chars, >= 50 lines)
  - Component 3 (0.25): Contains reasonable English text (academic keywords)
  - Component 4 (0.30): Content covers all 6 pages (section markers from different parts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_013'
OCR_FILE = os.path.join(WORKDIR, 'papers', 'ocr_output.txt')


def verify_task():
    """
    Verify OCR task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist (task asks agent to create it)
    if not os.path.exists(OCR_FILE):
        print(f"FAIL: OCR output file not found at {OCR_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Read the file content
    try:
        with open(OCR_FILE, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {OCR_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File exists and is non-empty (0.20 points)
    # Litmus: initial_env has no ocr_output.txt, so this FAILS on initial
    try:
        if len(content.strip()) > 0:
            print(f"PASS: Component 1 -- ocr_output.txt exists and is non-empty ({len(content)} chars) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- ocr_output.txt is empty")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Substantial text content (0.25 points)
    # A 6-page OCR should produce significant text. Golden has ~10K chars, ~260 lines.
    # We check >= 1000 chars and >= 50 lines as a reasonable lower bound.
    try:
        line_count = content.count('\n')
        char_count = len(content)
        if char_count >= 1000 and line_count >= 50:
            print(f"PASS: Component 2 -- Substantial content: {char_count} chars, {line_count} lines (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- Insufficient content: {char_count} chars (need >= 1000), {line_count} lines (need >= 50)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Contains reasonable English text (0.25 points)
    # The paper is about distributed computing. Check for academic/technical terms
    # that would appear in a real OCR of this paper.
    try:
        content_lower = content.lower()
        # These terms should appear in any reasonable OCR of a 1987 CS paper
        # about distributed computing
        expected_terms = [
            'distributed',      # core topic
            'computing',        # core topic
            'processor',        # technical term throughout
            'algorithm',        # CS paper standard term
            'performance',      # common in systems papers
        ]
        found_terms = [t for t in expected_terms if t in content_lower]
        # Need at least 3 out of 5 terms to account for OCR imperfections
        if len(found_terms) >= 3:
            print(f"PASS: Component 3 -- Found {len(found_terms)}/5 key terms: {found_terms} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- Only found {len(found_terms)}/5 key terms: {found_terms} (need >= 3)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Content covers all 6 pages (0.30 points)
    # A 6-page academic paper has distinct sections across pages.
    # Check for section-like markers that indicate text from multiple pages.
    # The golden file has: Abstract (page 1), Introduction (page 1-2),
    # body sections (pages 2-5), Conclusion (page 5-6), References (page 6).
    try:
        content_lower = content.lower()
        # Section markers that span different pages of the paper
        page_indicators = [
            'abstract',         # typically page 1
            'introduction',     # page 1-2
            'conclusion',       # near end (page 5-6)
            'references',       # last page (page 6)
        ]
        found_sections = [s for s in page_indicators if s in content_lower]

        # Also check content volume suggests multi-page extraction
        # A single page of OCR would produce roughly 1000-2000 chars
        # 6 pages should produce at least 4000 chars
        multi_page_volume = len(content) >= 4000

        if len(found_sections) >= 3 and multi_page_volume:
            print(f"PASS: Component 4 -- Multi-page coverage: found sections {found_sections}, volume={len(content)} chars (0.30 pts)")
            total_score += 0.30
        elif len(found_sections) >= 2 and multi_page_volume:
            partial = 0.15
            print(f"PARTIAL: Component 4 -- Some page coverage: found sections {found_sections}, volume={len(content)} chars ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Insufficient page coverage: found sections {found_sections}, volume={len(content)} chars")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
