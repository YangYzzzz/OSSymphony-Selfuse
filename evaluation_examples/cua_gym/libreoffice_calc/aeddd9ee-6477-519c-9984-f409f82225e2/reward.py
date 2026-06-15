"""
Reward Script: Compile semester tests into comprehensive Writer exam document
Task ID: osworld_multi_apps_grammar_test_compile_008
Domain: libreoffice_writer (ODT)
Scoring:
  Component 1: Cover page with title 'Final Comprehensive Exam', date, and student info fields (0.25 pts)
  Component 2: Table of Contents with 10 section entries + Answer Key entry (0.20 pts)
  Component 3: 10 Sections headed by source filenames (test_01.txt through test_10.txt) (0.25 pts)
  Component 4: Sequential question numbering 1-100 (0.20 pts)
  Component 5: Answer Key section with answers for all 100 questions (0.10 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_grammar_test_compile_008'
FILE_PATH = f'{WORKDIR}/final_exam_complete.odt'


def get_all_text(doc):
    """Extract all text from ODT document in document order."""
    all_text = []
    for elem in doc.text.childNodes:
        tag = getattr(elem, 'tagName', '')
        if tag in ('text:p', 'text:h'):
            text = ''
            for node in elem.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    text += node.data
                elif hasattr(node, 'childNodes'):
                    for child in node.childNodes:
                        if child.nodeType == child.TEXT_NODE:
                            text += child.data
            all_text.append(text.strip())
    return all_text


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

    # Load ODT document
    try:
        from odf.opendocument import load as odf_load
    except ImportError:
        print("CRITICAL: odfpy library not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = odf_load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        all_text = get_all_text(doc)
    except Exception as e:
        print(f"CRITICAL: Cannot extract text from ODT: {e}")
        print("REWARD: 0.0")
        return 0.0

    all_text_joined = '\n'.join(all_text)

    # Component 1: Cover page with required elements (0.25 points)
    # Must contain: 'Final Comprehensive Exam' title, Date field, Student Name/ID/Class fields
    try:
        has_title = any('Final Comprehensive Exam' in t for t in all_text)
        has_date = any(re.search(r'Date:', t) for t in all_text)
        has_student_name = any(re.search(r'Student Name', t) for t in all_text)
        has_student_id = any(re.search(r'Student ID', t) for t in all_text)

        if has_title and has_date and has_student_name and has_student_id:
            print("PASS: Component 1 — Cover page has title 'Final Comprehensive Exam', Date, Student Name, and Student ID fields (0.25 pts)")
            total_score += 0.25
        else:
            missing = []
            if not has_title:
                missing.append("title 'Final Comprehensive Exam'")
            if not has_date:
                missing.append("Date field")
            if not has_student_name:
                missing.append("Student Name field")
            if not has_student_id:
                missing.append("Student ID field")
            print(f"FAIL: Component 1 — Cover page missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Table of Contents with 10 section entries + Answer Key entry (0.20 points)
    # TOC must list all 10 sections (referencing test_01.txt through test_10.txt) and Answer Key
    try:
        has_toc_header = any(t == 'Table of Contents' or t.startswith('Table of Contents') for t in all_text)
        # Check TOC entries reference all 10 test files
        toc_section_hits = set()
        toc_ak_matches = [t for t in all_text if 'Answer Key' in t and re.search(r'\.{3,}', t)]
        for t in all_text:
            for n in range(1, 11):
                fname = f'test_{n:02d}.txt'
                if fname in t and re.search(r'Section\s+\d+', t):
                    toc_section_hits.add(n)

        sections_in_toc = len(toc_section_hits)
        answer_key_in_toc = len(toc_ak_matches) > 0

        if has_toc_header and sections_in_toc == 10 and answer_key_in_toc:
            print(f"PASS: Component 2 — Table of Contents present with all 10 section entries and Answer Key entry (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_toc_header:
                missing.append("'Table of Contents' heading")
            if sections_in_toc < 10:
                missing.append(f"only {sections_in_toc}/10 section entries in TOC")
            if not answer_key_in_toc:
                missing.append("Answer Key entry in TOC")
            print(f"FAIL: Component 2 — TOC missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 10 numbered sections, each headed by source filename (0.25 points)
    # Sections 1-10 each headed by their source filename (test_01.txt through test_10.txt)
    try:
        section_headings_found = set()
        for t in all_text:
            # Match patterns like "Section N: test_NN.txt"
            m = re.match(r'^Section\s+(\d+):\s+test_(\d+)\.txt\b', t)
            if m:
                sec_num = int(m.group(1))
                file_num = int(m.group(2))
                # Section N should reference test_NN.txt
                if 1 <= sec_num <= 10 and file_num == sec_num:
                    section_headings_found.add(sec_num)

        sections_found = len(section_headings_found)

        if sections_found == 10:
            print(f"PASS: Component 3 — All 10 section headings found (Section 1: test_01.txt through Section 10: test_10.txt) (0.25 pts)")
            total_score += 0.25
        else:
            missing_sections = [i for i in range(1, 11) if i not in section_headings_found]
            print(f"FAIL: Component 3 — Only {sections_found}/10 section headings found. Missing sections: {missing_sections}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Sequential question numbering 1-100 (0.20 points)
    # Questions must be numbered sequentially from 1 to 100 (no gaps, no duplicates)
    try:
        question_numbers = []
        for t in all_text:
            m = re.match(r'^(\d+)\.\s+\S', t)
            if m:
                question_numbers.append(int(m.group(1)))

        total_questions = len(question_numbers)
        expected_numbers = list(range(1, 101))

        if question_numbers == expected_numbers:
            print(f"PASS: Component 4 — Questions numbered sequentially 1-100 (found {total_questions} questions) (0.20 pts)")
            total_score += 0.20
        elif total_questions == 100 and sorted(question_numbers) == expected_numbers:
            print(f"PASS: Component 4 — 100 questions present but may be out of order (sorted matches 1-100). Awarding partial. (0.20 pts)")
            total_score += 0.20
        else:
            if total_questions == 100:
                dups = [n for n in question_numbers if question_numbers.count(n) > 1]
                print(f"FAIL: Component 4 — 100 questions found but not sequential 1-100. Duplicates: {set(dups)[:5]}")
            else:
                print(f"FAIL: Component 4 — Expected 100 questions numbered 1-100, found {total_questions} question numbers")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Answer Key section at the end listing correct answers (0.10 points)
    # Must have "Answer Key" heading followed by answers for questions 1-100
    try:
        # Find the last/final Answer Key (not the TOC entry)
        last_ak_idx = -1
        for i, t in enumerate(all_text):
            if t.strip() == 'Answer Key':
                last_ak_idx = i

        if last_ak_idx < 0:
            print("FAIL: Component 5 — No standalone 'Answer Key' section found at the end of the document")
        else:
            # Check that after Answer Key heading, answers for Q1-Q100 are present
            ak_text_block = '\n'.join(all_text[last_ak_idx:last_ak_idx + 20])
            # Look for answer patterns like "Q1: B" or "1. B" etc.
            answer_matches = re.findall(r'Q(\d+):\s*[A-D]', ak_text_block)
            num_answers_visible = len(answer_matches)

            if num_answers_visible >= 10:
                print(f"PASS: Component 5 — Answer Key section found at index {last_ak_idx} with {num_answers_visible}+ answers visible (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — Answer Key section found but only {num_answers_visible} answer entries visible in first 20 lines (expected Q1-Q100 format)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
