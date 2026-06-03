"""
Reward Script: Create academic PDF with title, author, and three sections
Task ID: pdf_res_007
Domain: pdf
Scoring:
  Component 1 (0.20): PDF exists and has >= 2 pages
  Component 2 (0.20): Title text present
  Component 3 (0.15): Author name present
  Component 4 (0.25): All three section headings present (Introduction, Main Results, Conclusion)
  Component 5 (0.20): Each section contains substantive text (>= 100 chars per section)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_007'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract full text from all pages
    full_text = ""
    try:
        for i in range(doc.page_count):
            full_text += doc[i].get_text()
    except Exception as e:
        print(f"CRITICAL: Cannot extract text from PDF: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has at least 2 pages (0.20 points)
    # Task requires creating a multi-page academic paper; context says >= 2 pages
    try:
        page_count = doc.page_count
        if page_count >= 2:
            print(f"PASS: Component 1 — PDF has {page_count} pages (>= 2 required) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — PDF has {page_count} pages, expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Title "On the Convergence of Gradient Descent" present (0.20 points)
    try:
        title = "On the Convergence of Gradient Descent"
        if title in full_text:
            print(f"PASS: Component 2 — Title '{title}' found in PDF (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Title '{title}' not found in extracted text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Author "Dr. Sarah Chen" present (0.15 points)
    try:
        author = "Dr. Sarah Chen"
        if author in full_text:
            print(f"PASS: Component 3 — Author '{author}' found in PDF (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Author '{author}' not found in extracted text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All three section headings present (0.25 points)
    # Award partial credit: ~0.083 per heading found
    try:
        headings = ["Introduction", "Main Results", "Conclusion"]
        headings_found = 0
        for heading in headings:
            if heading in full_text:
                headings_found += 1
                print(f"  - Heading '{heading}' found")
            else:
                print(f"  - Heading '{heading}' NOT found")

        if headings_found == 3:
            print(f"PASS: Component 4 — All 3 section headings found (0.25 pts)")
            total_score += 0.25
        elif headings_found > 0:
            partial = round(0.25 * headings_found / 3, 2)
            print(f"PARTIAL: Component 4 — {headings_found}/3 headings found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No section headings found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Each section has substantive text (0.20 points)
    # Verify that each section contains at least ~100 characters of body text
    # (indicating placeholder paragraphs were generated, not just headings)
    try:
        sections_with_text = 0
        section_markers = ["Introduction", "Main Results", "Conclusion"]

        for idx, heading in enumerate(section_markers):
            start_pos = full_text.find(heading)
            if start_pos < 0:
                print(f"  - Section '{heading}': heading not found, skipping text check")
                continue

            # Find end of section (next heading or end of text)
            section_start = start_pos + len(heading)
            section_end = len(full_text)
            for next_heading in section_markers[idx + 1:]:
                next_pos = full_text.find(next_heading, section_start)
                if next_pos > 0:
                    section_end = next_pos
                    break

            section_text = full_text[section_start:section_end].strip()
            text_len = len(section_text)

            if text_len >= 100:
                sections_with_text += 1
                print(f"  - Section '{heading}': {text_len} chars of body text (sufficient)")
            else:
                print(f"  - Section '{heading}': only {text_len} chars of body text (insufficient, need >= 100)")

        if sections_with_text == 3:
            print(f"PASS: Component 5 — All 3 sections have substantive text (0.20 pts)")
            total_score += 0.20
        elif sections_with_text > 0:
            partial = round(0.20 * sections_with_text / 3, 2)
            print(f"PARTIAL: Component 5 — {sections_with_text}/3 sections have substantive text ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No sections have substantive text")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
file_path = f'{WORKDIR}/papers/draft_paper.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
