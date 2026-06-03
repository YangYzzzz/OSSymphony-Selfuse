"""
Reward Script: Add interactive table of contents to user_guide.pdf
Task ID: pdf_gf2_030
Domain: pdf
Scoring:
  - Component 1 (0.20): Output file exists and has 23 pages
  - Component 2 (0.15): TOC page has "Table of Contents" title
  - Component 3 (0.15): TOC page lists all 4 chapter names
  - Component 4 (0.30): 4 clickable internal links to correct pages
  - Component 5 (0.20): PDF bookmark outline has 4 correct entries
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_030'

# Expected chapters: name -> 0-indexed target page in the 23-page doc
CHAPTERS = {
    'Getting Started': 1,   # page 2 (1-indexed) = page 1 (0-indexed)
    'Core Features': 6,     # page 7 (1-indexed) = page 6 (0-indexed)
    'Advanced Settings': 12, # page 13 (1-indexed) = page 12 (0-indexed)
    'FAQs': 18,             # page 19 (1-indexed) = page 18 (0-indexed)
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File has 23 pages (0.20 pts)
    # Initial PDF has 22 pages; golden adds 1 TOC page = 23
    try:
        pc = doc.page_count
        if pc == 23:
            print(f"PASS: Component 1 — Page count is 23 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 23 pages, found {pc}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: First page contains "Table of Contents" title (0.15 pts)
    try:
        page0_text = doc[0].get_text("text")
        if "Table of Contents" in page0_text:
            print(f"PASS: Component 2 — 'Table of Contents' title found on page 1 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — 'Table of Contents' not found on page 1. Text: {page0_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: First page lists all 4 chapter names (0.15 pts)
    try:
        page0_text = doc[0].get_text("text")
        found_chapters = []
        missing_chapters = []
        for ch_name in CHAPTERS.keys():
            if ch_name in page0_text:
                found_chapters.append(ch_name)
            else:
                missing_chapters.append(ch_name)

        if len(found_chapters) == 4:
            print(f"PASS: Component 3 — All 4 chapter names found on TOC page (0.15 pts)")
            total_score += 0.15
        elif len(found_chapters) >= 2:
            partial = round(0.15 * len(found_chapters) / 4, 3)
            print(f"PARTIAL: Component 3 — {len(found_chapters)}/4 chapters found ({partial} pts). Missing: {missing_chapters}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {len(found_chapters)}/4 chapters found. Missing: {missing_chapters}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Internal links on page 0 pointing to correct pages (0.30 pts)
    # Each correct link = 0.075 pts
    try:
        links = doc[0].get_links()
        # Filter to internal GOTO links
        goto_links = [l for l in links if l.get('kind') == 1]  # kind=1 is LINK_GOTO

        matched_links = 0
        for ch_name, expected_page in CHAPTERS.items():
            link_found = False
            for link in goto_links:
                target_page = link.get('page', -1)
                if target_page == expected_page:
                    link_found = True
                    break
            if link_found:
                matched_links += 1
                print(f"  LINK OK: '{ch_name}' -> page {expected_page} (0-indexed)")
            else:
                print(f"  LINK MISSING: '{ch_name}' should link to page {expected_page} (0-indexed)")

        if matched_links == 4:
            print(f"PASS: Component 4 — All 4 links correct (0.30 pts)")
            total_score += 0.30
        elif matched_links > 0:
            partial = round(0.30 * matched_links / 4, 3)
            print(f"PARTIAL: Component 4 — {matched_links}/4 links correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No correct links found. GOTO links: {goto_links}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: PDF bookmark outline has 4 correct entries (0.20 pts)
    try:
        toc = doc.get_toc()  # [[level, title, page_1indexed], ...]
        expected_toc = {
            'Getting Started': 2,
            'Core Features': 7,
            'Advanced Settings': 13,
            'FAQs': 19,
        }

        matched_bookmarks = 0
        for entry in toc:
            level, title, page_num = entry[0], entry[1].strip(), entry[2]
            if title in expected_toc and expected_toc[title] == page_num:
                matched_bookmarks += 1
                print(f"  BOOKMARK OK: '{title}' -> page {page_num}")

        if matched_bookmarks == 4:
            print(f"PASS: Component 5 — All 4 bookmarks correct (0.20 pts)")
            total_score += 0.20
        elif matched_bookmarks > 0:
            partial = round(0.20 * matched_bookmarks / 4, 3)
            print(f"PARTIAL: Component 5 — {matched_bookmarks}/4 bookmarks correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No correct bookmarks. TOC entries: {toc}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/{TASK_ID[:-4]}_toc.pdf'
# The task says save as user_guide_toc.pdf
file_path = f'{WORKDIR}/Documents/user_guide_toc.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
