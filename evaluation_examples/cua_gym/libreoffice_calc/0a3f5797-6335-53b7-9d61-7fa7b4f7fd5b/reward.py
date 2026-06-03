"""
Reward Script: Merge 6 different-format documents into a single PDF
Task ID: pdf_gf3_018
Domain: pdf
Scoring:
  Component 1 (0.25): final_submission.pdf exists with correct page count (9 pages)
  Component 2 (0.15): Cover letter content from cover.docx on early pages
  Component 3 (0.25): Section A, B, C content present in correct sequential order
  Component 4 (0.15): Python-generated title page with expected content
  Component 5 (0.20): Signature image on the last page
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_018'

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    file_path = f'{WORKDIR}/docs/final_submission.pdf'

    # Precondition: file must exist and be a valid PDF
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Component 1: Page count is 9 (0.25 points)
    # The merged PDF should have: cover.docx (2 pages) + section_a (2) + section_b (1)
    # + section_c (2) + title page (1) + signature page (1) = 9 pages
    # Initial env has NO final_submission.pdf, so this inherently fails on initial.
    try:
        if page_count >= 7 and page_count <= 11:
            # Partial credit for reasonable page count
            if page_count == 9:
                print(f"PASS: Component 1 -- Page count is exactly 9 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"PARTIAL: Component 1 -- Page count is {page_count}, expected 9 (0.15 pts)")
                total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Page count is {page_count}, expected ~9")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Cover letter content from cover.docx on early pages (0.15 points)
    # The cover.docx content should appear in the first 2 pages as "Government Submission Cover Letter"
    # and "Meridian Consulting Group"
    try:
        cover_text = ""
        for i in range(min(3, page_count)):
            cover_text += doc[i].get_text("text")

        cover_markers = [
            "Government Submission Cover Letter",
            "Meridian Consulting Group",
            "Pennsylvania Avenue",
        ]
        found_count = sum(1 for m in cover_markers if m in cover_text)

        if found_count == len(cover_markers):
            print(f"PASS: Component 2 -- All {len(cover_markers)} cover letter markers found (0.15 pts)")
            total_score += 0.15
        elif found_count >= 2:
            print(f"PARTIAL: Component 2 -- {found_count}/{len(cover_markers)} cover markers found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 -- Only {found_count}/{len(cover_markers)} cover markers found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Section A, B, C content present in correct order (0.25 points)
    # Sections must appear after cover content and in order: A then B then C
    try:
        all_text = ""
        section_positions = {}
        for i in range(page_count):
            page_text = doc[i].get_text("text")
            all_text += page_text

            # Find first page where each section heading appears
            if "SECTION A:" in page_text and "A" not in section_positions:
                section_positions["A"] = i
            if "SECTION B:" in page_text and "B" not in section_positions:
                section_positions["B"] = i
            if "SECTION C:" in page_text and "C" not in section_positions:
                section_positions["C"] = i

        sections_found = len(section_positions)
        # Check ordering: A before B before C
        correct_order = False
        if sections_found == 3:
            correct_order = (section_positions["A"] < section_positions["B"] < section_positions["C"])

        if sections_found == 3 and correct_order:
            # Verify some actual content from each section
            has_a_content = "TECHNICAL APPROACH" in all_text
            has_b_content = "PAST PERFORMANCE" in all_text
            has_c_content = "COST PROPOSAL" in all_text
            content_count = sum([has_a_content, has_b_content, has_c_content])

            if content_count == 3:
                print(f"PASS: Component 3 -- All 3 sections found in correct order with content (0.25 pts)")
                total_score += 0.25
            else:
                print(f"PARTIAL: Component 3 -- Sections in order but only {content_count}/3 have expected content (0.20 pts)")
                total_score += 0.20
        elif sections_found >= 2:
            print(f"PARTIAL: Component 3 -- Found {sections_found}/3 sections (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 -- Only {sections_found}/3 section headers found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Python-generated title page with expected content (0.15 points)
    # The title page should contain "ADVANCED ENERGY GRID" or similar title-page text
    # and NOT be part of any section (A, B, C) or cover letter
    try:
        title_page_found = False
        title_page_idx = -1

        for i in range(page_count):
            page_text = doc[i].get_text("text")
            # The title page has "ADVANCED ENERGY GRID" and "DOE-RFP-2025-0347"
            # It should NOT be a section page or cover page
            if ("ADVANCED ENERGY GRID" in page_text and
                "SECTION A:" not in page_text and
                "SECTION B:" not in page_text and
                "SECTION C:" not in page_text and
                "Government Submission Cover Letter" not in page_text):
                title_page_found = True
                title_page_idx = i
                break

        if title_page_found:
            title_text = doc[title_page_idx].get_text("text")
            has_solicitation = "DOE-RFP-2025-0347" in title_text
            if has_solicitation:
                print(f"PASS: Component 4 -- Title page found at page {title_page_idx} with solicitation ref (0.15 pts)")
                total_score += 0.15
            else:
                print(f"PARTIAL: Component 4 -- Title page found but missing solicitation reference (0.10 pts)")
                total_score += 0.10
        else:
            print(f"FAIL: Component 4 -- No Python-generated title page found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Signature image on the last page (0.20 points)
    # The last page should contain the signature.png as an embedded image
    # and certification text
    try:
        last_page = doc[page_count - 1]
        images = last_page.get_images()
        last_text = last_page.get_text("text")

        has_image = len(images) >= 1
        has_cert_text = ("certify" in last_text.lower() or
                        "authorized" in last_text.lower() or
                        "submission" in last_text.lower())

        if has_image and has_cert_text:
            print(f"PASS: Component 5 -- Last page has {len(images)} image(s) and certification text (0.20 pts)")
            total_score += 0.20
        elif has_image:
            print(f"PARTIAL: Component 5 -- Last page has image but missing certification text (0.15 pts)")
            total_score += 0.15
        elif has_cert_text:
            print(f"PARTIAL: Component 5 -- Last page has certification text but no image (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 -- Last page has no image and no certification text")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/docs/final_submission.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task()
