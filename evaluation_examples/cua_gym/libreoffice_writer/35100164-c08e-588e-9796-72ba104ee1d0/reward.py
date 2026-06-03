"""
Reward Script: Apply consistent heading hierarchy to training manual document
Task ID: osworld_writer_heading_styles_004
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Document title paragraph uses Heading 1 style
  Component 2 (0.30): All 4 chapter title paragraphs use Heading 2 style
  Component 3 (0.30): All 8 sub-topic paragraphs use Heading 3 style
  Component 4 (0.10): Heading 2 style font size is 14pt
Total: 1.0
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_heading_styles_004'

# Known paragraph identifiers from task structure analysis
# These are the exact texts from initial exploration
TITLE_TEXT = 'Employee Onboarding Training Manual'
CHAPTER_TEXTS = [
    'Chapter 1: Company Overview',
    'Chapter 2: Workplace Policies',
    'Chapter 3: Benefits and Compensation',
    'Chapter 4: Professional Development',
]
SUBTOPIC_TEXTS = [
    'Company History and Mission',
    'Organizational Structure',
    'Code of Conduct',
    'Attendance and Leave Policy',
    'Health and Wellness Benefits',
    'Salary Review Process',
    'Training and Certification Programs',
    'Performance Evaluation Framework',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    - 1 title paragraph styled as Heading 1
    - 4 chapter title paragraphs styled as Heading 2
    - 8 sub-topic paragraphs styled as Heading 3
    - Heading 2 style updated to 14pt font size

    Initial state: all paragraphs are Normal style with run-level bold/size overrides
    Golden state: heading hierarchy applied + Heading 2 style set to 14pt
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print('CRITICAL: Cannot load file ' + file_path + ': ' + str(e))
        print('REWARD: 0.0')
        return 0.0

    # Build a lookup: paragraph text -> style name
    para_styles = {}
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            para_styles[text] = para.style.name

    # Component 1: Document title has Heading 1 style (0.30 points)
    try:
        title_style = para_styles.get(TITLE_TEXT, None)
        if title_style == 'Heading 1':
            print('PASS: Component 1 — Title paragraph uses Heading 1 style (0.30 pts)')
            total_score += 0.30
        else:
            print('FAIL: Component 1 — Title style expected "Heading 1", found ' + repr(title_style))
    except Exception as e:
        print('ERROR: Component 1 — ' + str(e))

    # Component 2: All 4 chapter titles have Heading 2 style (0.30 points)
    try:
        chapters_with_h2 = 0
        chapter_results = []
        for chapter_text in CHAPTER_TEXTS:
            found_style = para_styles.get(chapter_text, None)
            if found_style == 'Heading 2':
                chapters_with_h2 += 1
                chapter_results.append('PASS: ' + repr(chapter_text) + ' -> Heading 2')
            else:
                chapter_results.append('FAIL: ' + repr(chapter_text) + ' -> ' + repr(found_style))

        if chapters_with_h2 == 4:
            total_score += 0.30
            print('PASS: Component 2 — All 4 chapter titles use Heading 2 style (0.30 pts)')
            for r in chapter_results:
                print('  ' + r)
        elif chapters_with_h2 > 0:
            print('PARTIAL FAIL: Component 2 — Only ' + str(chapters_with_h2) + '/4 chapter titles use Heading 2 style')
            for r in chapter_results:
                print('  ' + r)
        else:
            print('FAIL: Component 2 — No chapter titles use Heading 2 style')
            for r in chapter_results:
                print('  ' + r)
    except Exception as e:
        print('ERROR: Component 2 — ' + str(e))

    # Component 3: All 8 sub-topics have Heading 3 style (0.30 points)
    try:
        subtopics_with_h3 = 0
        subtopic_results = []
        for subtopic_text in SUBTOPIC_TEXTS:
            found_style = para_styles.get(subtopic_text, None)
            if found_style == 'Heading 3':
                subtopics_with_h3 += 1
                subtopic_results.append('PASS: ' + repr(subtopic_text) + ' -> Heading 3')
            else:
                subtopic_results.append('FAIL: ' + repr(subtopic_text) + ' -> ' + repr(found_style))

        if subtopics_with_h3 == 8:
            total_score += 0.30
            print('PASS: Component 3 — All 8 sub-topics use Heading 3 style (0.30 pts)')
            for r in subtopic_results:
                print('  ' + r)
        elif subtopics_with_h3 > 0:
            print('PARTIAL FAIL: Component 3 — Only ' + str(subtopics_with_h3) + '/8 sub-topics use Heading 3 style')
            for r in subtopic_results:
                print('  ' + r)
        else:
            print('FAIL: Component 3 — No sub-topics use Heading 3 style')
            for r in subtopic_results:
                print('  ' + r)
    except Exception as e:
        print('ERROR: Component 3 — ' + str(e))

    # Component 4: Heading 2 style font size is 14pt (0.10 points)
    # The initial document has Heading 2 style at 13pt; the task requires updating it to 14pt
    try:
        h2_style = doc.styles['Heading 2']
        h2_font_size = h2_style.font.size
        h2_font_size_pt = h2_font_size.pt if h2_font_size else None

        if h2_font_size_pt == 14.0:
            print('PASS: Component 4 — Heading 2 style font size is 14pt (0.10 pts)')
            total_score += 0.10
        else:
            print('FAIL: Component 4 — Heading 2 style font size expected 14pt, found ' + str(h2_font_size_pt) + 'pt')
    except Exception as e:
        print('ERROR: Component 4 — ' + str(e))

    final_score = min(total_score, 1.0)
    print('')
    print('Score: ' + str(round(total_score, 2)) + '/1.0')
    print('REWARD: ' + str(round(final_score, 1)))
    return final_score


file_path = WORKDIR + '/' + TASK_ID + '.docx'
if not os.path.exists(file_path):
    print('File not found: ' + file_path)
    print('REWARD: 0.0')
else:
    verify_task(file_path)
