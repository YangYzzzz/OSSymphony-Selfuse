"""
Reward Script: Split anthology.odt by author into 5 author .odt files and create anthology_index.odt
Task ID: osworld_multi_apps_book_splitting_nav_012
Domain: libreoffice_writer (ODT files)
Scoring:
  Component 1 (0.20): 5 author .odt files present in Desktop/anthology_split/
  Component 2 (0.30): Each author file has Heading 1 for chapter titles
  Component 3 (0.20): Each author file has Heading 2 for section titles
  Component 4 (0.15): Each author file has a Table of Contents (TOC)
  Component 5 (0.15): anthology_index.odt has 5 author H1 entries with bulleted chapter lists
"""

import os

# All verification runs on the VM
WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_splitting_nav_012'
SPLIT_DIR = '/home/user/Desktop/anthology_split'

# Expected authors (by surname, as filenames)
EXPECTED_AUTHORS = ['Delacroix', 'Nakamura', 'Okafor', 'Petrov', 'Rivera']


def get_text_from_element(elem):
    """Recursively extract text from an ODF element."""
    parts = []
    if hasattr(elem, 'data'):
        parts.append(elem.data)
    if hasattr(elem, 'childNodes'):
        for child in elem.childNodes:
            parts.extend(get_text_from_element(child))
    return parts


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Check that the split directory exists (gate condition — not scored)
    if not os.path.exists(SPLIT_DIR):
        print("CRITICAL: anthology_split/ directory not found at " + SPLIT_DIR)
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: 5 author ODT files are present in anthology_split/ (0.20)
    # This FAILS on initial (empty dir) and PASSES on golden (5 files present)
    # -----------------------------------------------------------------------
    try:
        files_in_dir = [f for f in os.listdir(SPLIT_DIR) if f.endswith('.odt')]
        author_files = [f for f in files_in_dir if f != 'anthology_index.odt']

        found_authors = []
        for expected in EXPECTED_AUTHORS:
            # Match by surname (case-insensitive, exact filename match)
            match = next((f for f in author_files if f.lower() == expected.lower() + '.odt'), None)
            if match:
                found_authors.append(match)

        if len(found_authors) == 5:
            print("PASS: Component 1 — All 5 author ODT files present: " + str(found_authors) + " (0.20 pts)")
            total_score += 0.20
        else:
            print("FAIL: Component 1 — Expected 5 author files, found " + str(len(found_authors)) + ": " + str(found_authors))
    except Exception as e:
        print("ERROR: Component 1 — " + str(e))

    # -----------------------------------------------------------------------
    # Component 2: Each author file has H1 headings for chapter titles (0.30)
    # Task requires: "apply Heading 1 for chapter titles"
    # This FAILS on initial (empty dir) and PASSES on golden (H1 chapter titles present)
    # -----------------------------------------------------------------------
    try:
        from odf.opendocument import load
        from odf.text import H

        authors_with_h1 = 0
        for expected in EXPECTED_AUTHORS:
            fpath = os.path.join(SPLIT_DIR, expected + '.odt')
            if not os.path.exists(fpath):
                print("FAIL: Component 2 — File not found: " + fpath)
                continue
            doc = load(fpath)
            headings = doc.getElementsByType(H)
            h1_list = [h for h in headings if h.getAttribute('outlinelevel') == '1']
            # Expect H1 entries that look like chapters (contain "Chapter")
            chapter_h1 = []
            for h in h1_list:
                text = ''.join(get_text_from_element(h))
                if 'Chapter' in text or 'chapter' in text:
                    chapter_h1.append(text[:50])
            if len(chapter_h1) >= 2:
                print("PASS: Component 2 — " + expected + ".odt has " + str(len(chapter_h1)) + " H1 chapter headings, e.g.: " + str(chapter_h1[:2]))
                authors_with_h1 += 1
            else:
                print("FAIL: Component 2 — " + expected + ".odt has only " + str(len(chapter_h1)) + " H1 chapter headings (need >= 2)")

        # Award 0.30 proportionally based on authors passing
        if authors_with_h1 == 5:
            print("PASS: Component 2 — All 5 author files have H1 chapter titles (0.30 pts)")
            total_score += 0.30
        elif authors_with_h1 > 0:
            comp2_score = round(0.30 * authors_with_h1 / 5, 4)
            print("PARTIAL: Component 2 — " + str(authors_with_h1) + "/5 authors have H1 chapter titles (" + str(comp2_score) + " pts)")
            total_score += comp2_score
        else:
            print("FAIL: Component 2 — No author files have H1 chapter titles (0.0 pts)")
    except Exception as e:
        print("ERROR: Component 2 — " + str(e))

    # -----------------------------------------------------------------------
    # Component 3: Each author file has H2 headings for section titles (0.20)
    # Task requires: "apply ... Heading 2 for section titles"
    # This FAILS on initial (empty dir) and PASSES on golden (H2 present)
    # -----------------------------------------------------------------------
    try:
        from odf.opendocument import load
        from odf.text import H

        authors_with_h2 = 0
        for expected in EXPECTED_AUTHORS:
            fpath = os.path.join(SPLIT_DIR, expected + '.odt')
            if not os.path.exists(fpath):
                continue
            doc = load(fpath)
            headings = doc.getElementsByType(H)
            h2_list = [h for h in headings if h.getAttribute('outlinelevel') == '2']
            if len(h2_list) >= 2:
                print("PASS: Component 3 — " + expected + ".odt has " + str(len(h2_list)) + " H2 section headings")
                authors_with_h2 += 1
            else:
                print("FAIL: Component 3 — " + expected + ".odt has only " + str(len(h2_list)) + " H2 section headings (need >= 2)")

        if authors_with_h2 == 5:
            print("PASS: Component 3 — All 5 author files have H2 section titles (0.20 pts)")
            total_score += 0.20
        elif authors_with_h2 > 0:
            comp3_score = round(0.20 * authors_with_h2 / 5, 4)
            print("PARTIAL: Component 3 — " + str(authors_with_h2) + "/5 authors have H2 section titles (" + str(comp3_score) + " pts)")
            total_score += comp3_score
        else:
            print("FAIL: Component 3 — No author files have H2 section titles (0.0 pts)")
    except Exception as e:
        print("ERROR: Component 3 — " + str(e))

    # -----------------------------------------------------------------------
    # Component 4: Each author file has a Table of Contents (TOC) (0.15)
    # Task requires: "insert a TOC"
    # This FAILS on initial (empty dir) and PASSES on golden (TOC present)
    # -----------------------------------------------------------------------
    try:
        from odf.opendocument import load
        from odf import text as odf_text

        authors_with_toc = 0
        for expected in EXPECTED_AUTHORS:
            fpath = os.path.join(SPLIT_DIR, expected + '.odt')
            if not os.path.exists(fpath):
                continue
            doc = load(fpath)
            toc_elements = doc.getElementsByType(odf_text.TableOfContent)
            if len(toc_elements) >= 1:
                print("PASS: Component 4 — " + expected + ".odt has TOC element")
                authors_with_toc += 1
            else:
                print("FAIL: Component 4 — " + expected + ".odt has no TOC element")

        if authors_with_toc == 5:
            print("PASS: Component 4 — All 5 author files have TOC (0.15 pts)")
            total_score += 0.15
        elif authors_with_toc > 0:
            comp4_score = round(0.15 * authors_with_toc / 5, 4)
            print("PARTIAL: Component 4 — " + str(authors_with_toc) + "/5 authors have TOC (" + str(comp4_score) + " pts)")
            total_score += comp4_score
        else:
            print("FAIL: Component 4 — No author files have TOC (0.0 pts)")
    except Exception as e:
        print("ERROR: Component 4 — " + str(e))

    # -----------------------------------------------------------------------
    # Component 5: anthology_index.odt has 5 author H1 entries + bulleted lists (0.15)
    # Task requires: "Create a master anthology_index.odt with a two-level listing:
    #   author name as Heading 1, chapter titles as a bulleted list below each author"
    # This FAILS on initial (no file) and PASSES on golden (correct structure)
    # -----------------------------------------------------------------------
    try:
        from odf.opendocument import load
        from odf.text import H, ListItem

        index_path = os.path.join(SPLIT_DIR, 'anthology_index.odt')
        if not os.path.exists(index_path):
            print("FAIL: Component 5 — anthology_index.odt not found at " + index_path)
        else:
            doc = load(index_path)
            headings = doc.getElementsByType(H)

            # Count H1 entries matching author surnames
            author_surnames = ['Rivera', 'Nakamura', 'Okafor', 'Petrov', 'Delacroix']
            h1_author_matches = 0
            for h in headings:
                if h.getAttribute('outlinelevel') == '1':
                    h_text = ''.join(get_text_from_element(h))
                    for surname in author_surnames:
                        if surname.lower() in h_text.lower():
                            h1_author_matches += 1
                            break

            # Count bulleted list items (chapter titles)
            list_items = doc.getElementsByType(ListItem)
            list_item_count = len(list_items)

            print("INFO: anthology_index.odt — H1 author matches: " + str(h1_author_matches) + ", list items: " + str(list_item_count))

            if h1_author_matches >= 5 and list_item_count >= 15:
                print("PASS: Component 5 — anthology_index.odt has all 5 author H1 entries and " + str(list_item_count) + " bulleted chapter entries (0.15 pts)")
                total_score += 0.15
            elif h1_author_matches >= 3 and list_item_count >= 8:
                partial = round(0.15 * h1_author_matches / 5, 4)
                print("PARTIAL: Component 5 — anthology_index.odt has " + str(h1_author_matches) + "/5 author H1 entries and " + str(list_item_count) + " list items (" + str(partial) + " pts)")
                total_score += partial
            else:
                print("FAIL: Component 5 — anthology_index.odt insufficient: " + str(h1_author_matches) + " author H1 headings, " + str(list_item_count) + " list items (need >= 5 H1s and >= 15 items)")
    except Exception as e:
        print("ERROR: Component 5 — " + str(e))

    final_score = min(total_score, 1.0)
    print("\nScore: " + str(round(total_score, 4)) + "/1.0")
    print("REWARD: " + str(round(final_score, 2)))
    return final_score


if __name__ == '__main__':
    verify_task()
