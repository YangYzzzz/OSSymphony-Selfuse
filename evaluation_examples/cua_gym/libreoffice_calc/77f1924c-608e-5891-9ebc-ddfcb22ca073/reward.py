"""
Reward Script: Merge 5 .txt question files into unit_exam.odt with formatted sections
Task ID: osworld_multi_apps_grammar_test_compile_007
Domain: libreoffice_writer (ODT)
Scoring:
  Component 1: File 'unit_exam.odt' exists in /home/user/Documents/ (0.1 points)
  Component 2: 5 Heading 2 sections with correct section titles (0.3 points)
  Component 3: Each section has an italic instruction paragraph (0.3 points)
  Component 4: Questions are numbered 1-25 sequentially across all sections (0.3 points)
"""

import os

WORKDIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_grammar_test_compile_007'
FILE_PATH = f'{WORKDIR}/unit_exam.odt'

EXPECTED_HEADINGS = [
    'Multiple Choice',
    'Fill in the Blank',
    'Short Answer',
    'True/False',
    'Essay',
]

# Expected instruction text substrings for each section (from task source files)
EXPECTED_INSTRUCTIONS = [
    'Choose the best answer from the options provided',
    'Fill in each blank with the most appropriate word',
    'Answer each question in one to three complete sentences',
    'Write "True" if the statement is grammatically correct',
    'Write a well-organized response of at least three paragraphs',
]

SECTION_QUESTION_RANGES = [
    (1, 5),    # Multiple Choice: questions 1-5
    (6, 10),   # Fill in the Blank: questions 6-10
    (11, 15),  # Short Answer: questions 11-15
    (16, 20),  # True/False: questions 16-20
    (21, 25),  # Essay: questions 21-25
]


def get_elem_text(elem):
    """Recursively extract all text from an ODT element."""
    text = ''
    if hasattr(elem, 'data'):
        return str(elem.data)
    if hasattr(elem, 'childNodes'):
        for child in elem.childNodes:
            text += get_elem_text(child)
    return text


def elem_has_italic_span(elem, italic_styles):
    """Check if any child span uses an italic auto-style."""
    if not hasattr(elem, 'childNodes'):
        return False
    for child in elem.childNodes:
        if hasattr(child, 'qname') and child.qname[1] == 'span':
            style_name = child.getAttribute('stylename')
            if style_name and style_name in italic_styles:
                return True
        # Also check recursively
        if elem_has_italic_span(child, italic_styles):
            return True
    return False


def verify_task(file_path):
    """
    Verify task completion for merging 5 .txt question files into unit_exam.odt.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition Gate: File must exist ---
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load ODF document
    try:
        from odf.opendocument import load
        from odf.text import H, P, Span
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODT file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: File exists and is a valid ODT document (0.1 points) ---
    # We only reach here if the file exists and loads successfully.
    try:
        # Verify it's a proper text document with content
        children = list(doc.text.childNodes)
        if len(children) > 0:
            print(f"PASS: Component 1 — unit_exam.odt exists and is a valid ODT document ({len(children)} elements) (0.1 pts)")
            total_score += 0.1
        else:
            print("FAIL: Component 1 — unit_exam.odt is empty")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Collect italic auto-styles (styles with font-style=italic) ---
    italic_styles = set()
    try:
        for style in doc.automaticstyles.childNodes:
            if not hasattr(style, 'qname'):
                continue
            name = style.getAttribute('name')
            for child in style.childNodes:
                if not hasattr(child, 'qname'):
                    continue
                tag = child.qname[1]
                if tag == 'text-properties':
                    if hasattr(child, 'attributes'):
                        for k, v in child.attributes.items():
                            if 'font-style' in str(k) and v == 'italic':
                                italic_styles.add(name)
    except Exception as e:
        print(f"WARN: Could not determine italic styles: {e}")

    # --- Component 2: 5 Heading 2 sections with correct titles (0.3 points) ---
    try:
        found_headings = []
        for elem in doc.text.childNodes:
            if not hasattr(elem, 'qname'):
                continue
            if elem.qname[1] == 'h':
                level = elem.getAttribute('outlinelevel')
                heading_text = get_elem_text(elem).strip()
                if level == '2':
                    found_headings.append(heading_text)

        headings_correct = []
        for expected in EXPECTED_HEADINGS:
            if any(expected.lower() in h.lower() for h in found_headings):
                headings_correct.append(expected)

        if len(found_headings) == 5 and len(headings_correct) == 5:
            print(f"PASS: Component 2 — 5 Heading 2 sections found with correct titles: {found_headings} (0.3 pts)")
            total_score += 0.3
        elif len(found_headings) >= 3:
            pts = 0.15
            print(f"PARTIAL: Component 2 — Found {len(found_headings)} Heading 2 sections (expected 5): {found_headings} ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 2 — Expected 5 Heading 2 sections, found {len(found_headings)}: {found_headings}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Each section has italic instruction paragraph (0.3 points) ---
    try:
        # Build section map: heading → list of following paragraphs until next heading
        sections = {}
        current_section = None
        for elem in doc.text.childNodes:
            if not hasattr(elem, 'qname'):
                continue
            tag = elem.qname[1]
            if tag == 'h':
                level = elem.getAttribute('outlinelevel')
                if level == '2':
                    current_section = get_elem_text(elem).strip()
                    sections[current_section] = []
            elif tag == 'p' and current_section is not None:
                sections[current_section].append(elem)

        italic_count = 0
        for section_name, paragraphs in sections.items():
            if len(paragraphs) == 0:
                continue
            # The first paragraph should be the instruction paragraph with italic text
            first_para = paragraphs[0]
            para_text = get_elem_text(first_para).strip()
            has_italic = elem_has_italic_span(first_para, italic_styles)

            if has_italic and len(para_text) > 10:
                italic_count += 1
            else:
                print(f"FAIL: Component 3 — Section '{section_name}' missing italic instruction (has_italic={has_italic}, text={repr(para_text[:60])})")

        if italic_count == 5:
            print(f"PASS: Component 3 — All 5 sections have italic instruction paragraphs (0.3 pts)")
            total_score += 0.3
        elif italic_count >= 3:
            pts = 0.15
            print(f"PARTIAL: Component 3 — {italic_count}/5 sections have italic instruction paragraphs ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 3 — Only {italic_count}/5 sections have italic instruction paragraphs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --- Component 4: Questions numbered 1-25 sequentially (0.3 points) ---
    try:
        # Collect all paragraph texts (non-instruction paragraphs)
        all_question_texts = []
        current_section = None
        for elem in doc.text.childNodes:
            if not hasattr(elem, 'qname'):
                continue
            tag = elem.qname[1]
            if tag == 'h':
                level = elem.getAttribute('outlinelevel')
                if level == '2':
                    current_section = get_elem_text(elem).strip()
            elif tag == 'p' and current_section is not None:
                para_text = get_elem_text(elem).strip()
                all_question_texts.append((current_section, para_text))

        # For each section, skip first para (instruction) and check numbering
        section_texts = {}
        section_order = []
        for section_name, para_text in all_question_texts:
            if section_name not in section_texts:
                section_texts[section_name] = []
                section_order.append(section_name)
            section_texts[section_name].append(para_text)

        # Check sequential numbering 1-25
        import re
        numbered_questions = 0
        expected_num = 1
        numbering_correct = True
        numbering_details = []

        for section_idx, section_name in enumerate(section_order):
            paras = section_texts.get(section_name, [])
            # Skip first paragraph (instruction)
            question_paras = paras[1:] if len(paras) > 1 else paras

            for para_text in question_paras:
                # Check if paragraph starts with expected number
                match = re.match(r'^(\d+)[\.\)]\s', para_text)
                if match:
                    actual_num = int(match.group(1))
                    if actual_num == expected_num:
                        numbered_questions += 1
                        expected_num += 1
                    else:
                        numbering_details.append(f"Expected Q{expected_num}, got Q{actual_num} in '{section_name}'")
                        numbering_correct = False

        if numbered_questions == 25 and numbering_correct:
            print(f"PASS: Component 4 — All 25 questions numbered 1-25 sequentially (0.3 pts)")
            total_score += 0.3
        elif numbered_questions >= 20:
            pts = 0.15
            print(f"PARTIAL: Component 4 — {numbered_questions}/25 questions numbered correctly ({pts} pts). Issues: {numbering_details[:3]}")
            total_score += pts
        else:
            print(f"FAIL: Component 4 — Only {numbered_questions}/25 questions numbered correctly. Issues: {numbering_details[:3]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
