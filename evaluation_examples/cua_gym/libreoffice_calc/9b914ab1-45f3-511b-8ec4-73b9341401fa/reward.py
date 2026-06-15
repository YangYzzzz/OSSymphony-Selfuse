"""
Reward Script: Apply Heading 1 styles, insert TOC, and add bookmarks in novel_draft.odt
Task ID: osworld_multi_apps_book_splitting_nav_007
Domain: libreoffice_writer (ODT)
Scoring:
  Component 1 (0.40): 8 Heading 1 paragraphs on chapter titles
  Component 2 (0.30): 1 Table of Contents present
  Component 3 (0.30): 8 bookmarks named chapter_1 through chapter_8
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_splitting_nav_007'
FILE_PATH = f'{WORKDIR}/novel_draft.odt'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — precondition gate
    try:
        from odf.opendocument import load
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Lazy import helpers
    try:
        from odf import text as odftext
    except Exception as e:
        print(f"CRITICAL: Cannot import odfpy: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 8 chapter titles have Heading 1 style (0.40 points)
    # Task requires: "Apply Heading 1 to each chapter title"
    # Initial state: 0 headings (all BodyText). Golden state: 8 headings (level=1).
    try:
        headings = doc.getElementsByType(odftext.H)
        heading1_elements = [h for h in headings if h.getAttribute('outlinelevel') == '1']
        heading1_count = len(heading1_elements)

        # Verify heading texts contain "Chapter X:" pattern
        chapter_headings = []
        for h in heading1_elements:
            text = ''
            for child in h.childNodes:
                if child.nodeType == 3:
                    text += child.data
                elif hasattr(child, 'childNodes'):
                    for grandchild in child.childNodes:
                        if grandchild.nodeType == 3:
                            text += grandchild.data
            if 'Chapter' in text:
                chapter_headings.append(text.strip())

        if heading1_count >= 8 and len(chapter_headings) >= 8:
            print(f"PASS: Component 1 — Found {heading1_count} Heading 1 elements, "
                  f"{len(chapter_headings)} chapter headings (0.40 pts)")
            total_score += 0.40
        elif heading1_count > 0 and len(chapter_headings) > 0:
            # Partial credit for some headings
            partial = round(0.40 * (len(chapter_headings) / 8), 2)
            print(f"PARTIAL: Component 1 — Found {len(chapter_headings)}/8 chapter headings "
                  f"with Heading 1 style ({partial} pts)")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 1 — Expected 8 Heading 1 chapter elements, "
                  f"found {heading1_count} headings, {len(chapter_headings)} chapter headings")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Table of Contents present at document start (0.30 points)
    # Task requires: "insert a TOC at the document start"
    # Initial state: 0 TOCs. Golden state: 1 TOC.
    try:
        toc_elements = doc.getElementsByType(odftext.TableOfContent)
        toc_count = len(toc_elements)

        if toc_count >= 1:
            print(f"PASS: Component 2 — Found {toc_count} Table of Contents (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Expected 1 TOC, found {toc_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 8 bookmarks named chapter_1 through chapter_8 (0.30 points)
    # Task requires: "add bookmarks named 'chapter_1' through 'chapter_8' at the start of each chapter"
    # Initial state: 0 bookmarks. Golden state: 8 bookmarks with exact names.
    try:
        # Try BookmarkStart first, fall back to Bookmark
        bookmark_elements = doc.getElementsByType(odftext.BookmarkStart)
        if not bookmark_elements:
            bookmark_elements = doc.getElementsByType(odftext.Bookmark)

        bookmark_names = set()
        for b in bookmark_elements:
            bname = b.getAttribute('name')
            if bname:
                bookmark_names.add(bname)

        expected_bookmarks = {f'chapter_{i}' for i in range(1, 9)}
        found_expected = bookmark_names & expected_bookmarks
        missing = expected_bookmarks - bookmark_names

        if len(found_expected) == 8:
            print(f"PASS: Component 3 — All 8 chapter bookmarks found: "
                  f"{sorted(found_expected)} (0.30 pts)")
            total_score += 0.30
        elif len(found_expected) > 0:
            partial = round(0.30 * (len(found_expected) / 8), 2)
            print(f"PARTIAL: Component 3 — Found {len(found_expected)}/8 chapter bookmarks "
                  f"({partial} pts). Missing: {sorted(missing)}")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 3 — No chapter bookmarks found. "
                  f"Expected: {sorted(expected_bookmarks)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
