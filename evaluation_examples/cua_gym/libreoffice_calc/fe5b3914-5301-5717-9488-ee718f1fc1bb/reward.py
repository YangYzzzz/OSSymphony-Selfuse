"""
Reward Script: Create instructor test booklet from grammar quiz files
Task ID: osworld_multi_apps_grammar_test_compile_011
Domain: libreoffice_writer (ODT format)
Scoring:
  Component 1: Document has 20 heading sections (10 student + 10 instructor) — 0.25 pts
  Component 2: Questions numbered 1-100 in student sections (no answers) — 0.30 pts
  Component 3: Instructor sections have answer tables (Q#, Answer, Points, LO Tag) — 0.30 pts
  Component 4: Student sections do not contain answer key content — 0.15 pts
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_grammar_test_compile_011'
FILE_PATH = f'{WORKDIR}/instructor_test_booklet.odt'

# Table namespace constant
TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'


def get_element_text(elem):
    """Extract all text from an XML element, concatenating all text nodes."""
    texts = []
    for node in elem.iter():
        if node.text:
            texts.append(node.text)
        if node.tail:
            texts.append(node.tail)
    return ''.join(texts).strip()


def load_odt_elements(file_path):
    """Load ODT file and return list of (tag, text) for all paragraphs/headings."""
    with zipfile.ZipFile(file_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')
    root = ET.fromstring(content)
    all_elems = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag in ['p', 'h']:
            txt = get_element_text(elem)
            if txt and txt.strip():
                all_elems.append((tag, txt))
    return root, all_elems


def load_odt_tables(root):
    """Return list of tables, each as list of row lists (cell texts)."""
    tables = []
    for tbl in root.findall(f'.//{{{TABLE_NS}}}table'):
        rows_data = []
        rows = tbl.findall(f'.//{{{TABLE_NS}}}table-row')
        for row in rows:
            cells = row.findall(f'.//{{{TABLE_NS}}}table-cell')
            row_data = []
            for cell in cells:
                texts = []
                for node in cell.iter():
                    if node.text:
                        texts.append(node.text)
                row_data.append(''.join(texts).strip())
            rows_data.append(row_data)
        tables.append(rows_data)
    return tables


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be a valid ODT ZIP
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        root, all_elems = load_odt_elements(file_path)
        tables = load_odt_tables(root)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Document has 20 content sections — 10 student "Grammar Quiz — Section N"
    #              headings and 10 instructor "Instructor Guide — Section N" headings (0.25 pts)
    try:
        headings = [txt for (tag, txt) in all_elems if tag == 'h']

        student_headings = [h for h in headings if re.search(r'Grammar Quiz\s*[—-]\s*Section\s+\d+', h, re.IGNORECASE)]
        instructor_headings = [h for h in headings if re.search(r'Instructor Guide\s*[—-]\s*Section\s+\d+', h, re.IGNORECASE)]

        num_student = len(student_headings)
        num_instructor = len(instructor_headings)

        if num_student == 10 and num_instructor == 10:
            print(f"PASS: Component 1 — 20 headings found (10 student + 10 instructor sections) (0.25 pts)")
            total_score += 0.25
        elif num_student >= 5 or num_instructor >= 5:
            partial = 0.1
            print(f"PARTIAL: Component 1 — Found {num_student} student headings, {num_instructor} instructor headings (partial {partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Expected 10 student + 10 instructor headings, found {num_student} student + {num_instructor} instructor")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Questions numbered 1-100 appear in student sections (no answers visible) (0.30 pts)
    # Check that questions 1, 10, 50, 100 all exist as numbered items in the document
    try:
        # Find all numbered question lines: e.g., "1. Question text" up to "100."
        numbered_questions = []
        for (tag, txt) in all_elems:
            m = re.match(r'^(\d{1,3})\. ', txt)
            if m:
                qnum = int(m.group(1))
                if 1 <= qnum <= 100:
                    numbered_questions.append(qnum)

        numbered_questions_set = set(numbered_questions)

        # All 100 questions should be present
        missing = [n for n in range(1, 101) if n not in numbered_questions_set]
        present_count = len(numbered_questions_set.intersection(range(1, 101)))

        # Check that student sections don't have answers embedded inline
        # (i.e., question paragraphs should not contain answer patterns like "Answer: X")
        inline_answer_paragraphs = []
        for (tag, txt) in all_elems:
            m = re.match(r'^(\d{1,3})\. ', txt)
            if m:
                # Check if this question paragraph includes an embedded answer
                if re.search(r'\bAnswer:\s*\S', txt, re.IGNORECASE):
                    inline_answer_paragraphs.append(txt[:80])
                    print(f"WARNING: Question paragraph appears to contain embedded answer: {txt[:80]}")

        answers_clean = len(inline_answer_paragraphs) == 0

        if present_count == 100 and answers_clean:
            print(f"PASS: Component 2 — All 100 questions (1-100) found in student sections, no embedded answers (0.30 pts)")
            total_score += 0.30
        elif present_count >= 80 and answers_clean:
            print(f"PARTIAL: Component 2 — {present_count}/100 questions found, no embedded answers (partial 0.15 pts)")
            total_score += 0.15
        elif present_count == 100 and not answers_clean:
            # Questions present but answers also appear inline — partial credit
            print(f"PARTIAL: Component 2 — All 100 questions present but some contain inline answers (partial 0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Only {present_count}/100 questions found. Missing: {missing[:10]}...")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Instructor sections have answer tables with headers Q#, Question, Correct Answer, Points, LO Tag (0.30 pts)
    try:
        expected_headers = {'q#', 'question', 'correct answer', 'points', 'lo tag'}
        tables_with_correct_headers = 0
        tables_with_lo_tags = 0

        for tbl in tables:
            if not tbl:
                continue
            header_row = tbl[0]
            header_lower = {h.strip().lower() for h in header_row if h.strip()}
            # Check if table has the expected headers (at minimum Q#, Correct Answer, Points, LO Tag)
            required = {'q#', 'correct answer', 'points', 'lo tag'}
            if required.issubset(header_lower):
                tables_with_correct_headers += 1

                # Also verify LO tags appear in data rows
                for row in tbl[1:]:
                    for cell in row:
                        if re.match(r'^LO-\d+$', cell.strip()):
                            tables_with_lo_tags += 1
                            break

        if tables_with_correct_headers == 10:
            print(f"PASS: Component 3 — All 10 instructor tables have correct headers (Q#, Question, Correct Answer, Points, LO Tag) (0.30 pts)")
            total_score += 0.30
        elif tables_with_correct_headers >= 5:
            partial = 0.15
            print(f"PARTIAL: Component 3 — {tables_with_correct_headers}/10 instructor tables have correct headers (partial {partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Only {tables_with_correct_headers}/10 tables have correct headers (Q#, Correct Answer, Points, LO Tag). Total tables: {len(tables)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Student sections are clean — answers not present in student (non-table) paragraphs (0.15 pts)
    # In the golden structure, student sections have questions-only, instructor sections have tables.
    # We verify that answer key markers ("### Answer Key ###", "Q1:", "Points:", etc.) are NOT
    # present in non-table paragraphs.
    try:
        # Collect non-table paragraph text
        answer_key_markers_found = []
        for (tag, txt) in all_elems:
            # Check for answer key section markers
            if re.search(r'###\s*Answer Key\s*###', txt, re.IGNORECASE):
                answer_key_markers_found.append(txt[:60])
            # Check for "Q1: answer | Points: N" style patterns (raw answer key lines)
            elif re.match(r'^Q\d+:\s+\S+\s*\|\s*Points:\s*\d', txt):
                answer_key_markers_found.append(txt[:60])
            # Check for "Instructions: Answer all questions" type boilerplate (should not be in student section)
            # Actually this is acceptable in student section, skip

        if not answer_key_markers_found:
            print(f"PASS: Component 4 — No raw answer key content found in document paragraphs (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Answer key markers found in non-table paragraphs: {answer_key_markers_found[:3]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
