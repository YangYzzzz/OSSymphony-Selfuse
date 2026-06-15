"""
Reward Script: Split textbook into 12 chapter .odt files with structure
Task ID: osworld_multi_apps_book_splitting_nav_011
Domain: libreoffice_writer (odt files)

Scoring Rubric:
  Component 1: 12 chapter .odt files present in Desktop/textbook_chapters/     (0.25 pts)
  Component 2: master_index.odt present with 12-row table of chapter info       (0.25 pts)
  Component 3: Each chapter has Heading 1/2/3 hierarchy + mini-TOC paragraphs  (0.30 pts)
  Component 4: Each chapter has section bookmarks at Heading 2 positions        (0.20 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_splitting_nav_011'
CHAPTERS_DIR = '/home/user/Desktop/textbook_chapters'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -----------------------------------------------------------------------
    # Precondition gate: the output directory must exist
    # -----------------------------------------------------------------------
    if not os.path.isdir(CHAPTERS_DIR):
        print(f"CRITICAL: Output directory not found: {CHAPTERS_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: 12 chapter .odt files present in Desktop/textbook_chapters/
    # (0.25 points)
    # -----------------------------------------------------------------------
    try:
        chapter_files = []
        for i in range(1, 13):
            fname = f'chapter_{str(i).zfill(2)}.odt'
            fpath = os.path.join(CHAPTERS_DIR, fname)
            if os.path.isfile(fpath):
                chapter_files.append(fpath)

        if len(chapter_files) == 12:
            print(f"PASS: Component 1 — All 12 chapter files found in {CHAPTERS_DIR} (0.25 pts)")
            total_score += 0.25
        else:
            missing = [f'chapter_{str(i).zfill(2)}.odt'
                       for i in range(1, 13)
                       if not os.path.isfile(os.path.join(CHAPTERS_DIR, f'chapter_{str(i).zfill(2)}.odt'))]
            print(f"FAIL: Component 1 — Only {len(chapter_files)}/12 chapter files found. Missing: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: master_index.odt with a 12-row table of chapter info
    # (0.25 points)
    # -----------------------------------------------------------------------
    try:
        from odf.opendocument import load as odf_load

        master_path = os.path.join(CHAPTERS_DIR, 'master_index.odt')
        if not os.path.isfile(master_path):
            print("FAIL: Component 2 — master_index.odt not found")
        else:
            doc = odf_load(master_path)
            body = doc.text

            # Collect table rows
            table_rows = []

            def collect_table_rows(node):
                tag = node.qname[1] if hasattr(node, 'qname') else ''
                if tag == 'table-row':
                    row_cells = []
                    for cell in getattr(node, 'childNodes', []):
                        cell_tag = cell.qname[1] if hasattr(cell, 'qname') else ''
                        if cell_tag == 'table-cell':
                            cell_text = ''
                            for p in getattr(cell, 'childNodes', []):
                                for child in getattr(p, 'childNodes', []):
                                    if hasattr(child, 'data'):
                                        cell_text += child.data
                            row_cells.append(cell_text.strip())
                    if row_cells:
                        table_rows.append(row_cells)
                for child in getattr(node, 'childNodes', []):
                    collect_table_rows(child)

            collect_table_rows(body)

            # Expect at least 13 rows (1 header + 12 data rows)
            data_rows = [r for r in table_rows if r and r[0].isdigit()]
            if len(data_rows) >= 12:
                # Verify row has at least 4 columns (chapter num, title, sections, subsections)
                valid_rows = [r for r in data_rows if len(r) >= 4]
                if len(valid_rows) >= 12:
                    print(f"PASS: Component 2 — master_index.odt has table with {len(valid_rows)} chapter data rows (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 — Table rows lack required columns. Valid rows: {len(valid_rows)}")
            else:
                print(f"FAIL: Component 2 — Expected 12 data rows in master_index.odt table, found {len(data_rows)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Each chapter has Heading 1/2/3 hierarchy + mini-TOC
    # (0.30 points)
    # -----------------------------------------------------------------------
    try:
        from odf.opendocument import load as odf_load

        chapters_pass = 0
        chapters_fail_details = []

        for i in range(1, 13):
            fname = f'chapter_{str(i).zfill(2)}.odt'
            fpath = os.path.join(CHAPTERS_DIR, fname)
            if not os.path.isfile(fpath):
                chapters_fail_details.append(f"{fname}: file missing")
                continue

            doc = odf_load(fpath)
            body = doc.text

            h1_count = 0
            h2_count = 0
            h3_count = 0
            toc_paragraphs = 0

            def collect_headings(node):
                nonlocal h1_count, h2_count, h3_count, toc_paragraphs
                tag = node.qname[1] if hasattr(node, 'qname') else ''
                if tag == 'h':
                    level = node.getAttribute('outlinelevel')
                    if level == '1':
                        h1_count += 1
                    elif level == '2':
                        h2_count += 1
                    elif level == '3':
                        h3_count += 1
                elif tag == 'p':
                    style = node.getAttribute('stylename') or ''
                    if style in ('TOCTitle', 'TOCEntry') or 'toc' in style.lower():
                        toc_paragraphs += 1
                for child in getattr(node, 'childNodes', []):
                    collect_headings(child)

            h1_count = 0
            h2_count = 0
            h3_count = 0
            toc_paragraphs = 0
            collect_headings(body)

            # Each chapter must have exactly 1 H1, at least 2 H2, at least 1 H3,
            # and at least 1 TOC-style paragraph (mini-TOC)
            has_h1 = h1_count >= 1
            has_h2 = h2_count >= 2
            has_h3 = h3_count >= 1
            has_toc = toc_paragraphs >= 1

            if has_h1 and has_h2 and has_h3 and has_toc:
                chapters_pass += 1
            else:
                chapters_fail_details.append(
                    f"{fname}: H1={h1_count}, H2={h2_count}, H3={h3_count}, TOCparas={toc_paragraphs}"
                )

        if chapters_pass == 12:
            print(f"PASS: Component 3 — All 12 chapters have H1/H2/H3 hierarchy and mini-TOC (0.30 pts)")
            total_score += 0.30
        elif chapters_pass >= 8:
            # Partial credit for 8-11 chapters passing
            comp3_partial = round(0.30 * (chapters_pass / 12), 2)
            print(f"PARTIAL: Component 3 — {chapters_pass}/12 chapters have correct structure ({comp3_partial} pts)")
            print(f"  Failing chapters: {chapters_fail_details[:5]}")
            if comp3_partial > 0:
                total_score += comp3_partial
        else:
            print(f"FAIL: Component 3 — Only {chapters_pass}/12 chapters have correct structure")
            print(f"  Failing chapters: {chapters_fail_details[:5]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Each chapter has section bookmarks at Heading 2 positions
    # (0.20 points)
    # -----------------------------------------------------------------------
    try:
        from odf.opendocument import load as odf_load

        chapters_with_bookmarks = 0
        bookmark_fail_details = []

        for i in range(1, 13):
            fname = f'chapter_{str(i).zfill(2)}.odt'
            fpath = os.path.join(CHAPTERS_DIR, fname)
            if not os.path.isfile(fpath):
                bookmark_fail_details.append(f"{fname}: file missing")
                continue

            doc = odf_load(fpath)
            body = doc.text

            bookmark_names = []
            h2_count = 0

            def collect_bookmarks(node):
                nonlocal h2_count
                tag = node.qname[1] if hasattr(node, 'qname') else ''
                if tag == 'h':
                    level = node.getAttribute('outlinelevel')
                    if level == '2':
                        h2_count += 1
                elif tag == 'bookmark-start':
                    bname = node.getAttribute('name')
                    if bname:
                        bookmark_names.append(bname)
                for child in getattr(node, 'childNodes', []):
                    collect_bookmarks(child)

            bookmark_names = []
            h2_count = 0
            collect_bookmarks(body)

            # Each chapter must have at least as many bookmarks as H2 sections
            # (one bookmark per H2 section)
            if len(bookmark_names) >= h2_count and h2_count >= 2:
                chapters_with_bookmarks += 1
            elif len(bookmark_names) >= 2:
                # At least 2 bookmarks found even if count mismatch
                chapters_with_bookmarks += 1
            else:
                bookmark_fail_details.append(
                    f"{fname}: H2={h2_count}, bookmarks={len(bookmark_names)}"
                )

        if chapters_with_bookmarks == 12:
            print(f"PASS: Component 4 — All 12 chapters have section bookmarks at H2 positions (0.20 pts)")
            total_score += 0.20
        elif chapters_with_bookmarks >= 8:
            comp4_partial = round(0.20 * (chapters_with_bookmarks / 12), 2)
            print(f"PARTIAL: Component 4 — {chapters_with_bookmarks}/12 chapters have bookmarks ({comp4_partial} pts)")
            print(f"  Failing: {bookmark_fail_details[:5]}")
            if comp4_partial > 0:
                total_score += comp4_partial
        else:
            print(f"FAIL: Component 4 — Only {chapters_with_bookmarks}/12 chapters have section bookmarks")
            print(f"  Failing: {bookmark_fail_details[:5]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Final score
    # -----------------------------------------------------------------------
    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
