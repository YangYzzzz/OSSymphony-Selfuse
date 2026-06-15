"""
Reward Script: Export bookmarks from legal_code.pdf to legal_bookmarks.txt using pdftk format
Task ID: pdf_mbc_043
Domain: pdf
Scoring:
  Component 1 (0.25): File contains pdftk-format BookmarkBegin entries
  Component 2 (0.35): All 3 Title-level (level 1) bookmarks with correct titles and page numbers
  Component 3 (0.25): All 10 Chapter-level (level 2) bookmarks with correct titles and page numbers
  Component 4 (0.15): Correct total bookmark count (13 bookmarks)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_043'
BOOKMARKS_FILE = os.path.join(WORKDIR, 'Documents', 'legal_bookmarks.txt')

# Expected bookmarks from the PDF (pdftk dump_data format)
EXPECTED_TITLE_BOOKMARKS = [
    {"title": "Title I - General Provisions", "level": 1, "page": 1},
    {"title": "Title II - Regulatory Framework", "level": 1, "page": 30},
    {"title": "Title III - Judicial Proceedings", "level": 1, "page": 55},
]

EXPECTED_CHAPTER_BOOKMARKS = [
    {"title": "Chapter 1 - Definitions", "level": 2, "page": 1},
    {"title": "Chapter 2 - Scope of Application", "level": 2, "page": 8},
    {"title": "Chapter 3 - Enforcement Authority", "level": 2, "page": 15},
    {"title": "Chapter 4 - Penalties and Remedies", "level": 2, "page": 22},
    {"title": "Chapter 5 - Licensing Requirements", "level": 2, "page": 30},
    {"title": "Chapter 6 - Compliance Standards", "level": 2, "page": 37},
    {"title": "Chapter 7 - Reporting Obligations", "level": 2, "page": 44},
    {"title": "Chapter 8 - Jurisdiction and Venue", "level": 2, "page": 55},
    {"title": "Chapter 9 - Evidentiary Standards", "level": 2, "page": 60},
    {"title": "Chapter 10 - Appellate Review", "level": 2, "page": 63},
]


def parse_pdftk_bookmarks(content):
    """Parse pdftk-format bookmark data into a list of dicts."""
    bookmarks = []
    current = {}
    for line in content.splitlines():
        line = line.strip()
        if line == "BookmarkBegin":
            if current:
                bookmarks.append(current)
            current = {}
        elif line.startswith("BookmarkTitle:"):
            current["title"] = line[len("BookmarkTitle:"):].strip()
        elif line.startswith("BookmarkLevel:"):
            try:
                current["level"] = int(line[len("BookmarkLevel:"):].strip())
            except ValueError:
                current["level"] = None
        elif line.startswith("BookmarkPageNumber:"):
            try:
                current["page"] = int(line[len("BookmarkPageNumber:"):].strip())
            except ValueError:
                current["page"] = None
    if current:
        bookmarks.append(current)
    return bookmarks


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    if not os.path.exists(BOOKMARKS_FILE):
        print(f"CRITICAL: Bookmarks file not found: {BOOKMARKS_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(BOOKMARKS_FILE, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {BOOKMARKS_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(content.strip()) == 0:
        print("CRITICAL: Bookmarks file is empty")
        print("REWARD: 0.0")
        return 0.0

    # Parse bookmarks from the file
    bookmarks = parse_pdftk_bookmarks(content)

    # Component 1: File contains pdftk-format BookmarkBegin entries (0.25 points)
    # This checks that the output is in pdftk format, not some other format
    try:
        bookmark_begin_count = content.count("BookmarkBegin")
        has_title_field = "BookmarkTitle:" in content
        has_level_field = "BookmarkLevel:" in content
        has_page_field = "BookmarkPageNumber:" in content

        if bookmark_begin_count > 0 and has_title_field and has_level_field and has_page_field:
            print(f"PASS: Component 1 -- pdftk format detected with {bookmark_begin_count} BookmarkBegin entries (0.25 pts)")
            total_score += 0.25
        else:
            missing = []
            if bookmark_begin_count == 0:
                missing.append("BookmarkBegin")
            if not has_title_field:
                missing.append("BookmarkTitle")
            if not has_level_field:
                missing.append("BookmarkLevel")
            if not has_page_field:
                missing.append("BookmarkPageNumber")
            print(f"FAIL: Component 1 -- missing pdftk format fields: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All 3 Title-level (level 1) bookmarks present with correct data (0.35 points)
    try:
        found_titles = 0
        for expected in EXPECTED_TITLE_BOOKMARKS:
            matched = False
            for bm in bookmarks:
                if (bm.get("title") == expected["title"] and
                        bm.get("level") == expected["level"] and
                        bm.get("page") == expected["page"]):
                    matched = True
                    break
            if matched:
                found_titles += 1
                print(f"  FOUND: Title bookmark '{expected['title']}' (level {expected['level']}, page {expected['page']})")
            else:
                print(f"  MISSING: Title bookmark '{expected['title']}' (level {expected['level']}, page {expected['page']})")

        if found_titles == len(EXPECTED_TITLE_BOOKMARKS):
            print(f"PASS: Component 2 -- all {found_titles}/{len(EXPECTED_TITLE_BOOKMARKS)} title-level bookmarks found (0.35 pts)")
            total_score += 0.35
        elif found_titles > 0:
            partial = round(0.35 * found_titles / len(EXPECTED_TITLE_BOOKMARKS), 2)
            print(f"PARTIAL: Component 2 -- {found_titles}/{len(EXPECTED_TITLE_BOOKMARKS)} title-level bookmarks found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- no title-level bookmarks found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All 10 Chapter-level (level 2) bookmarks present with correct data (0.25 points)
    try:
        found_chapters = 0
        for expected in EXPECTED_CHAPTER_BOOKMARKS:
            matched = False
            for bm in bookmarks:
                if (bm.get("title") == expected["title"] and
                        bm.get("level") == expected["level"] and
                        bm.get("page") == expected["page"]):
                    matched = True
                    break
            if matched:
                found_chapters += 1
                print(f"  FOUND: Chapter bookmark '{expected['title']}' (level {expected['level']}, page {expected['page']})")
            else:
                print(f"  MISSING: Chapter bookmark '{expected['title']}' (level {expected['level']}, page {expected['page']})")

        if found_chapters == len(EXPECTED_CHAPTER_BOOKMARKS):
            print(f"PASS: Component 3 -- all {found_chapters}/{len(EXPECTED_CHAPTER_BOOKMARKS)} chapter-level bookmarks found (0.25 pts)")
            total_score += 0.25
        elif found_chapters > 0:
            partial = round(0.25 * found_chapters / len(EXPECTED_CHAPTER_BOOKMARKS), 2)
            print(f"PARTIAL: Component 3 -- {found_chapters}/{len(EXPECTED_CHAPTER_BOOKMARKS)} chapter-level bookmarks found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- no chapter-level bookmarks found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Correct total bookmark count (0.15 points)
    # The PDF has exactly 13 bookmarks (3 titles + 10 chapters)
    try:
        expected_count = 13
        actual_count = len(bookmarks)
        if actual_count == expected_count:
            print(f"PASS: Component 4 -- correct bookmark count: {actual_count} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- expected {expected_count} bookmarks, found {actual_count}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
