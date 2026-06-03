"""
Reward Script: Extract PowerPoint text to Writer document with structured headings and summary
Task ID: osworld_multi_apps_impress_text_to_writer_007
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.35): 10 Heading 2 sections with [Slide N] prefix (slides 1-10)
  - Component 2 (0.20): Content Summary section with correct slide/table counts
  - Component 3 (0.20): Writer table reproducing the comparison table (3 cols, 4 rows)
  - Component 4 (0.25): 3-level bullet hierarchy present in document
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_impress_text_to_writer_007'


def get_text(element):
    """Recursively extract text from an ODF element."""
    texts = []
    for node in element.childNodes:
        if node.nodeType == 3:  # TEXT_NODE
            texts.append(str(node.data))
        elif hasattr(node, 'childNodes'):
            texts.append(get_text(node))
    return ''.join(texts)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODT document using odfpy
    try:
        from odf.opendocument import load
        from odf.text import P, H
        from odf.table import Table, TableRow, TableCell
    except ImportError as e:
        print(f"CRITICAL: odfpy not available: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: 10 Heading 2 sections with [Slide N] prefix (0.35 points)
    # Task requires Heading 2 per slide with '[Slide N]' prefix for slides 1-10
    # This FAILS on initial (file doesn't exist) → PASSES on golden
    # -----------------------------------------------------------------------
    try:
        headings = doc.getElementsByType(H)

        # Collect all Heading level 2 texts
        heading2_texts = []
        for h in headings:
            level = h.getAttribute('outlinelevel')
            text = get_text(h).strip()
            if level == '2':
                heading2_texts.append(text)

        # Check for [Slide 1] through [Slide 10] headings
        slide_headings_found = 0
        for n in range(1, 11):
            prefix = f'[Slide {n}]'
            matches = [t for t in heading2_texts if t.startswith(prefix)]
            if matches:
                slide_headings_found += 1

        if slide_headings_found == 10:
            print(f"PASS: Component 1 — All 10 slide headings found with [Slide N] prefix (0.35 pts)")
            total_score += 0.35
        elif slide_headings_found >= 5:
            partial = 0.15
            print(f"PARTIAL: Component 1 — Only {slide_headings_found}/10 slide headings found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {slide_headings_found}/10 [Slide N] heading 2 sections found")
            print(f"  Found headings: {heading2_texts[:5]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Content Summary section with correct counts (0.20 points)
    # Task requires 'Content Summary' section listing: Slides: 10, Tables: 1
    # This FAILS on initial → PASSES on golden
    # -----------------------------------------------------------------------
    try:
        paras = doc.getElementsByType(P)

        # Check for Content Summary heading
        all_headings = doc.getElementsByType(H)
        has_summary_heading = any(
            'Content Summary' in get_text(h)
            for h in all_headings
        )

        # Look for the required counts in paragraphs
        all_para_texts = [get_text(p).strip() for p in paras]
        has_slides_count = any('Slides: 10' in t or 'Slides:10' in t for t in all_para_texts)
        has_tables_count = any('Tables: 1' in t or 'Tables:1' in t for t in all_para_texts)

        if has_summary_heading and has_slides_count and has_tables_count:
            print(f"PASS: Component 2 — Content Summary section present with Slides: 10 and Tables: 1 (0.20 pts)")
            total_score += 0.20
        elif has_summary_heading and (has_slides_count or has_tables_count):
            partial = 0.10
            print(f"PARTIAL: Component 2 — Content Summary heading found but incomplete counts ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Content Summary section missing or incomplete")
            print(f"  Has summary heading: {has_summary_heading}")
            print(f"  Has 'Slides: 10': {has_slides_count}")
            print(f"  Has 'Tables: 1': {has_tables_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Writer table reproducing comparison table (0.20 points)
    # Task requires recreating the comparison table (3 columns, 4 rows)
    # This FAILS on initial → PASSES on golden
    # -----------------------------------------------------------------------
    try:
        tables = doc.getElementsByType(Table)

        # Collect table details for analysis
        table_details = []
        for table in tables:
            rows = table.getElementsByType(TableRow)
            row_count = len(rows)
            all_cell_texts = []
            for row in rows:
                cells = row.getElementsByType(TableCell)
                for cell in cells:
                    cell_text = get_text(cell).strip()
                    if cell_text:
                        all_cell_texts.append(cell_text.lower())
            table_details.append({'rows': row_count, 'cells': all_cell_texts})

        # Check for comparison table: 3 cols x 4 rows with relevant content
        # Expected headers: Feature, NovaSpark X1, Competitor Average
        comparison_tables = [
            td for td in table_details
            if td['rows'] >= 4
            and any('feature' in t for t in td['cells'])
            and any('novaspark' in t for t in td['cells'])
        ]

        if len(comparison_tables) >= 1:
            print(f"PASS: Component 3 — Comparison table found with correct structure (0.20 pts)")
            total_score += 0.20
        elif len(tables) > 0:
            print(f"PARTIAL: Component 3 — Table found but not matching comparison table structure (0.10 pts)")
            for td in table_details:
                print(f"  Table: {td['rows']} rows, cells: {td['cells'][:6]}")
            if len(table_details) > 0:
                total_score += 0.10
        else:
            print(f"FAIL: Component 3 — No table found in document (expected 1 comparison table)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: 3-level bullet hierarchy present (0.25 points)
    # Task requires preserving 3-level bullet hierarchy from presentation
    # This FAILS on initial → PASSES on golden
    # -----------------------------------------------------------------------
    try:
        paras = doc.getElementsByType(P)

        # Count paragraphs at each bullet level
        # Style names: Bullet_L0, Bullet_L1, Bullet_L2
        # Or detect by bullet characters: •, ◦, ▪
        level0_count = 0
        level1_count = 0
        level2_count = 0

        for p in paras:
            style = p.getAttribute('stylename') or ''
            text = get_text(p).strip()

            if not text:
                continue

            # Check by style name (preferred)
            if 'L0' in style or 'level-1' in style.lower() or 'list1' in style.lower():
                level0_count += 1
            elif 'L1' in style or 'level-2' in style.lower() or 'list2' in style.lower():
                level1_count += 1
            elif 'L2' in style or 'level-3' in style.lower() or 'list3' in style.lower():
                level2_count += 1
            # Also check by bullet characters for plain-text bullet encoding
            elif text.startswith('• '):
                level0_count += 1
            elif text.startswith('◦ '):
                level1_count += 1
            elif text.startswith('▪ '):
                level2_count += 1

        has_level0 = level0_count >= 5
        has_level1 = level1_count >= 5
        has_level2 = level2_count >= 3

        if has_level0 and has_level1 and has_level2:
            print(f"PASS: Component 4 — 3-level bullet hierarchy present (L0:{level0_count}, L1:{level1_count}, L2:{level2_count}) (0.25 pts)")
            total_score += 0.25
        elif has_level0 and has_level1:
            partial = 0.12
            print(f"PARTIAL: Component 4 — Only 2 levels found (L0:{level0_count}, L1:{level1_count}, L2:{level2_count}) ({partial} pts)")
            total_score += partial
        elif has_level0:
            partial = 0.06
            print(f"PARTIAL: Component 4 — Only level 0 bullets found (L0:{level0_count}) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Insufficient bullet hierarchy (L0:{level0_count}, L1:{level1_count}, L2:{level2_count})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/product_launch_text_extract.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
