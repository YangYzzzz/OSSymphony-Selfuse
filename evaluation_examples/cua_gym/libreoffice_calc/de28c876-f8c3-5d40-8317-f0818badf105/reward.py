"""
Reward Script: Build a Writer exam document from quiz files
Task ID: osworld_multi_apps_grammar_test_compile_009
Domain: libreoffice_writer (ODT format)
Scoring:
  Component 1 (0.20): tiered_exam.odt file exists at /home/user/tiered_exam.odt
  Component 2 (0.30): Document structural elements - title page, TOC heading,
                       Part I / Part II / Appendix A headings
  Component 3 (0.20): 10 section headings (Sections 1-10) across both parts
  Component 4 (0.15): 2 scoring rubric tables (one per part)
  Component 5 (0.15): Answer key appendix with 100 question-answer rows
  Total: 1.00
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_grammar_test_compile_009'
FILE_PATH = os.path.join(WORKDIR, 'tiered_exam.odt')

TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
OFFICE_NS = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'

H_TAG = f'{{{TEXT_NS}}}h'
P_TAG = f'{{{TEXT_NS}}}p'
TABLE_TAG = f'{{{TABLE_NS}}}table'
TABLE_ROW_TAG = f'{{{TABLE_NS}}}table-row'
TABLE_CELL_TAG = f'{{{TABLE_NS}}}table-cell'
OUTLINE_ATTR = f'{{{TEXT_NS}}}outline-level'


def find_all_elements(elem, tag):
    """Recursively find all elements with the given tag."""
    result = []
    if elem.tag == tag:
        result.append(elem)
    for child in elem:
        result.extend(find_all_elements(child, tag))
    return result


def get_element_text(elem):
    """Get concatenated text content of an element."""
    return ''.join(elem.itertext()).strip()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tiered_exam.odt file exists (0.20 points)
    # This is the primary output artifact — must exist to score anything
    try:
        if not os.path.isfile(file_path):
            print(f"FAIL: Component 1 — file not found: {file_path}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
        print(f"PASS: Component 1 — tiered_exam.odt exists (0.20 pts)")
        total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the ODT as a ZIP archive and parse content.xml
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'content.xml' not in z.namelist():
                print("CRITICAL: content.xml not found in ODT archive")
                print(f"\nScore: {total_score}/1.0")
                print(f"REWARD: {total_score}")
                return total_score
            content_xml = z.read('content.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot open ODT file: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    try:
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse content.xml: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    body = root.find(f'{{{OFFICE_NS}}}body')
    if body is None:
        print("CRITICAL: No office:body found in content.xml")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    text_elem = body.find(f'{{{OFFICE_NS}}}text')
    if text_elem is None:
        print("CRITICAL: No office:text found in body")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Extract all text content from paragraphs for full-text checks
    all_text_items = []
    for child in find_all_elements(text_elem, P_TAG) + find_all_elements(text_elem, H_TAG):
        t = get_element_text(child)
        if t:
            all_text_items.append(t)
    full_text = '\n'.join(all_text_items).lower()

    # Component 2: Document structure — title page, TOC heading, Part I/II/Appendix headings (0.30 points)
    # These are structural elements introduced by the task; the initial env has no such document
    try:
        # Check headings
        all_headings = find_all_elements(text_elem, H_TAG)
        heading_texts = [get_element_text(h) for h in all_headings]

        h1_texts = [get_element_text(h) for h in all_headings
                    if h.get(OUTLINE_ATTR) == '1']

        has_toc_heading = any('table of contents' in h.lower() for h in heading_texts)
        has_part1_heading = any('part i' in h.lower() and ('easy' in h.lower() or 'questions' in h.lower())
                                for h in h1_texts)
        has_part2_heading = any('part ii' in h.lower() and ('hard' in h.lower() or 'questions' in h.lower())
                                for h in h1_texts)
        has_appendix_heading = any('appendix' in h.lower() and 'answer' in h.lower()
                                   for h in h1_texts)

        # Check title page content (should have exam title text in paragraphs)
        has_title_page = ('grammar' in full_text and 'examination' in full_text)

        # Check TOC content (list of sections in TOC area)
        has_toc_content = ('section 1' in full_text and 'section 6' in full_text)

        comp2_checks = [has_toc_heading, has_part1_heading, has_part2_heading,
                        has_appendix_heading, has_title_page, has_toc_content]
        comp2_passed = sum(comp2_checks)
        comp2_total = len(comp2_checks)

        if comp2_passed == comp2_total:
            print(f"PASS: Component 2 — all {comp2_total} structural elements present "
                  f"(TOC heading, Part I/II headings, Appendix heading, title page, TOC content) (0.30 pts)")
            total_score += 0.30
        elif comp2_passed >= 4:
            print(f"PARTIAL: Component 2 — {comp2_passed}/{comp2_total} structural elements present (0.15 pts)")
            print(f"  TOC heading: {has_toc_heading}, Part I: {has_part1_heading}, "
                  f"Part II: {has_part2_heading}, Appendix: {has_appendix_heading}, "
                  f"Title page: {has_title_page}, TOC content: {has_toc_content}")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — only {comp2_passed}/{comp2_total} structural elements present")
            print(f"  TOC heading: {has_toc_heading}, Part I: {has_part1_heading}, "
                  f"Part II: {has_part2_heading}, Appendix: {has_appendix_heading}, "
                  f"Title page: {has_title_page}, TOC content: {has_toc_content}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 10 section headings (Sections 1-10) across both parts (0.20 points)
    # Easy Sections 1-5 (Q1-50) under Part I, Hard Sections 6-10 (Q51-100) under Part II
    try:
        h2_texts = [get_element_text(h) for h in all_headings
                    if h.get(OUTLINE_ATTR) == '2']

        # Check for each expected section heading
        expected_sections = [
            ('section 1', '1', '10'),
            ('section 2', '11', '20'),
            ('section 3', '21', '30'),
            ('section 4', '31', '40'),
            ('section 5', '41', '50'),
            ('section 6', '51', '60'),
            ('section 7', '61', '70'),
            ('section 8', '71', '80'),
            ('section 9', '81', '90'),
            ('section 10', '91', '100'),
        ]

        sections_found = 0
        for sec_name, q_start, q_end in expected_sections:
            found = any(sec_name in h.lower() for h in h2_texts)
            if found:
                sections_found += 1

        # Also check question numbering - verify questions 1-50 and 51-100 exist in document
        has_q1 = '1.' in full_text or 'question 1' in full_text
        has_q51 = '51.' in full_text
        has_q100 = '100.' in full_text

        if sections_found == 10 and has_q1 and has_q51 and has_q100:
            print(f"PASS: Component 3 — all 10 section headings present, questions 1-100 found (0.20 pts)")
            total_score += 0.20
        elif sections_found >= 8:
            print(f"PARTIAL: Component 3 — {sections_found}/10 section headings present (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — only {sections_found}/10 section headings found")
            print(f"  H2 headings: {h2_texts}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 2 scoring rubric tables (one per part) (0.15 points)
    # Both tables should have 3-column structure: Score Range | Performance Level | Description
    try:
        all_tables = find_all_elements(text_elem, TABLE_TAG)
        rubric_tables = []

        for table in all_tables:
            rows = find_all_elements(table, TABLE_ROW_TAG)
            if len(rows) < 2:
                continue
            # Check header row for scoring rubric columns
            first_row_cells = find_all_elements(rows[0], TABLE_CELL_TAG)
            first_row_texts = [get_element_text(c).lower() for c in first_row_cells]
            is_rubric = (
                any('score' in t for t in first_row_texts) and
                any('performance' in t or 'level' in t for t in first_row_texts)
            )
            if is_rubric:
                rubric_tables.append(table)

        rubric_count = len(rubric_tables)

        if rubric_count >= 2:
            print(f"PASS: Component 4 — {rubric_count} scoring rubric tables found "
                  f"(Score Range/Performance Level/Description columns) (0.15 pts)")
            total_score += 0.15
        elif rubric_count == 1:
            print(f"PARTIAL: Component 4 — only 1 scoring rubric table found, expected 2 (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 4 — no scoring rubric tables found (expected 2)")
            print(f"  Total tables in document: {len(all_tables)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Answer key appendix with 100 question-answer rows (0.15 points)
    # Table should have rows for Q1-Q100 with corresponding answers
    try:
        all_tables = find_all_elements(text_elem, TABLE_TAG)
        answer_key_table = None

        for table in all_tables:
            rows = find_all_elements(table, TABLE_ROW_TAG)
            if len(rows) < 10:
                continue
            # Check if this looks like the answer key: first column has question numbers
            # Answer key should have ~101 rows (header + 100 questions)
            if len(rows) >= 50:
                # Verify it's the answer key by checking the header and some content
                first_row_cells = find_all_elements(rows[0], TABLE_CELL_TAG)
                first_row_text = ' '.join(get_element_text(c).lower() for c in first_row_cells)
                if 'question' in first_row_text or 'answer' in first_row_text or 'number' in first_row_text:
                    answer_key_table = table
                    break
                # Also check if row values look like numbers 1-100
                second_row_cells = find_all_elements(rows[1], TABLE_CELL_TAG)
                if second_row_cells:
                    first_cell_text = get_element_text(second_row_cells[0]).strip()
                    if first_cell_text == '1':
                        answer_key_table = table
                        break

        if answer_key_table is not None:
            rows = find_all_elements(answer_key_table, TABLE_ROW_TAG)
            # Count data rows (subtract header row)
            data_rows = len(rows) - 1  # header row + data rows

            # Verify Q1 and Q100 are in the answer key
            q1_found = False
            q100_found = False
            for row in rows[1:]:  # skip header
                cells = find_all_elements(row, TABLE_CELL_TAG)
                if cells:
                    qnum = get_element_text(cells[0]).strip()
                    if qnum == '1':
                        q1_found = True
                    elif qnum == '100':
                        q100_found = True

            if data_rows >= 100 and q1_found and q100_found:
                print(f"PASS: Component 5 — answer key table found with {data_rows} rows, "
                      f"Q1 and Q100 verified (0.15 pts)")
                total_score += 0.15
            elif data_rows >= 90:
                print(f"PARTIAL: Component 5 — answer key table has {data_rows} rows "
                      f"(expected 100) (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 5 — answer key table has only {data_rows} data rows")
        else:
            print(f"FAIL: Component 5 — no answer key table found with 100+ rows")
            print(f"  Tables found: {len(all_tables)}, row counts: "
                  f"{[len(find_all_elements(t, TABLE_ROW_TAG)) for t in all_tables]}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM env
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
