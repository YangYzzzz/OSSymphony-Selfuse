"""
Reward Script: Multi-chapter PDF report generation
Task ID: pdf_aw_026
Domain: pdf
Scoring:
  Component 1: PDF exists with >= 7 pages (0.10)
  Component 2: Cover page has correct title (0.15)
  Component 3: TOC page lists 4 chapters with page numbers (0.20)
  Component 4: 4 chapters start on correct pages with correct titles (0.20)
  Component 5: Chapter paragraph text matches JSON source (0.20)
  Component 6: Footer 'Page X' on every page (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_026'
PDF_PATH = os.path.join(WORKDIR, 'reports', 'quarterly_analysis.pdf')
JSON_PATH = os.path.join(WORKDIR, 'data', 'chapters.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: PDF must exist
    if not os.path.exists(PDF_PATH):
        print(f"CRITICAL: PDF not found at {PDF_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
        doc = pymupdf.open(PDF_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {PDF_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: Load chapters JSON for content verification
    try:
        with open(JSON_PATH, 'r') as f:
            chapters = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load chapters JSON {JSON_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Extract text from all pages
    page_texts = []
    for i in range(page_count):
        page_texts.append(doc[i].get_text("text"))

    # Component 1: PDF has >= 7 pages (0.10 points)
    # Initial env has no PDF at all, so this only passes on golden
    try:
        if page_count >= 7:
            print(f"PASS: Component 1 -- PDF has {page_count} pages (>= 7) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 -- PDF has {page_count} pages, expected >= 7")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Cover page has 'Quarterly Analysis Q1 2026' (0.15 points)
    try:
        cover_text = page_texts[0] if page_count > 0 else ""
        if "Quarterly Analysis Q1 2026" in cover_text:
            print(f"PASS: Component 2 -- Cover page contains 'Quarterly Analysis Q1 2026' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Cover page missing 'Quarterly Analysis Q1 2026'. Text: {cover_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: TOC page lists 4 chapters with page numbers (0.20 points)
    # The TOC should be on page 2 (index 1) and list all 4 chapter titles
    try:
        toc_page_idx = -1
        toc_text = ""
        # Search for a page containing 'Table of Contents'
        for i in range(min(3, page_count)):
            if "Table of Contents" in page_texts[i]:
                toc_text = page_texts[i]
                toc_page_idx = i
                break

        if toc_page_idx >= 0:
            chapters_in_toc = 0
            has_page_numbers = 0
            for ch in chapters:
                title = ch["title"]
                if title in toc_text:
                    chapters_in_toc += 1
            # Check for numeric page references (at least some digits after chapter names)
            digits_in_toc = re.findall(r'\b\d+\b', toc_text)
            # Filter out the page footer number; look for page refs >= 3
            page_refs = [int(d) for d in digits_in_toc if int(d) >= 3]

            if chapters_in_toc == 4 and len(page_refs) >= 4:
                print(f"PASS: Component 3 -- TOC lists all 4 chapters with page numbers (0.20 pts)")
                total_score += 0.20
            elif chapters_in_toc >= 2:
                partial = 0.10
                print(f"PARTIAL: Component 3 -- TOC lists {chapters_in_toc}/4 chapters, {len(page_refs)} page refs ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- TOC has {chapters_in_toc}/4 chapters, {len(page_refs)} page refs")
        else:
            print(f"FAIL: Component 3 -- No 'Table of Contents' page found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 4 chapters each start on a new page with correct titles (0.20 points)
    # Each chapter title should appear at the start of a page (not in the middle of another chapter's page)
    try:
        chapter_titles = [ch["title"] for ch in chapters]
        chapters_on_new_page = 0

        for title in chapter_titles:
            matched_page = -1
            for i in range(2, page_count):  # Skip cover (0) and TOC (1)
                text = page_texts[i]
                # Check if this chapter title appears near the top of the page
                # Remove the "Page X" footer line at the start if present
                lines = [ln.strip() for ln in text.strip().split('\n') if ln.strip()]
                # Look for the title in the first few lines of the page
                for ln in lines[:5]:
                    if title in ln:
                        matched_page = i
                        break
                if matched_page >= 0:
                    break
            if matched_page >= 0:
                chapters_on_new_page += 1

        if chapters_on_new_page == 4:
            print(f"PASS: Component 4 -- All 4 chapters start on new pages with correct titles (0.20 pts)")
            total_score += 0.20
        elif chapters_on_new_page >= 2:
            partial = round(0.20 * chapters_on_new_page / 4, 2)
            print(f"PARTIAL: Component 4 -- {chapters_on_new_page}/4 chapters on new pages ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Only {chapters_on_new_page}/4 chapters found starting on new pages")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Chapter paragraph content matches JSON source (0.20 points)
    # Check that key phrases from each chapter's paragraphs appear in the PDF
    try:
        all_text = "\n".join(page_texts)
        matched_chapters = 0

        for ch in chapters:
            title = ch["title"]
            paragraphs = ch["paragraphs"]
            # Check a unique phrase from each paragraph (first ~50 chars that are distinctive)
            para_matches = 0
            for para in paragraphs:
                # Take a distinctive snippet from the middle of the paragraph
                words = para.split()
                if len(words) >= 10:
                    snippet = " ".join(words[5:12])  # words 5-11
                else:
                    snippet = " ".join(words[:5])
                # Normalize whitespace for matching
                normalized_text = re.sub(r'\s+', ' ', all_text)
                if snippet in normalized_text:
                    para_matches += 1

            if para_matches >= 2:  # At least 2 of 3 paragraphs matched
                matched_chapters += 1

        if matched_chapters == 4:
            print(f"PASS: Component 5 -- All 4 chapters' paragraph content matches JSON source (0.20 pts)")
            total_score += 0.20
        elif matched_chapters >= 2:
            partial = round(0.20 * matched_chapters / 4, 2)
            print(f"PARTIAL: Component 5 -- {matched_chapters}/4 chapters' content verified ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 -- Only {matched_chapters}/4 chapters' content matches JSON")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Footer 'Page X' on every page (0.15 points)
    try:
        pages_with_footer = 0
        for i in range(page_count):
            text = page_texts[i]
            # Look for "Page <number>" pattern in the text
            if re.search(r'Page\s+\d+', text):
                pages_with_footer += 1

        if pages_with_footer == page_count and page_count >= 7:
            print(f"PASS: Component 6 -- All {page_count} pages have 'Page X' footer (0.15 pts)")
            total_score += 0.15
        elif pages_with_footer >= page_count * 0.7 and page_count >= 7:
            partial = 0.08
            print(f"PARTIAL: Component 6 -- {pages_with_footer}/{page_count} pages have footer ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 -- Only {pages_with_footer}/{page_count} pages have 'Page X' footer")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
