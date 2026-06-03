"""
Reward Script: Mail merge certificate of completion template
Task ID: writer_mt_034
Domain: libreoffice_writer
Scoring:
  Component 1: Landscape orientation (0.20)
  Component 2: 'Certificate of Completion' title - centered, 36pt, bold (0.20)
  Component 3: <StudentName> placeholder - centered, 28pt, bold (0.20)
  Component 4: 'has successfully completed' + <CourseName> in 18pt (0.15)
  Component 5: <CompletionDate> and <InstructorName> present (0.10)
  Component 6: Decorative page border present (0.15)
"""

import os

from docx import Document
from docx.shared import Pt
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_034'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all paragraph texts for searching
    all_paras = [(p.text.strip(), p) for p in doc.paragraphs]
    non_empty = [(text, p) for text, p in all_paras if text]

    # Component 1: Landscape orientation (0.20 points)
    # Initial is portrait; golden is landscape. This checks a task-introduced change.
    try:
        section = doc.sections[0]
        is_landscape = section.orientation == WD_ORIENT.LANDSCAPE
        # Also verify dimensions are swapped (width > height)
        width_gt_height = section.page_width > section.page_height
        if is_landscape and width_gt_height:
            print(f"PASS: Component 1 - Landscape orientation confirmed "
                  f"(width={section.page_width}, height={section.page_height}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - Expected landscape orientation. "
                  f"Got orientation={section.orientation}, width={section.page_width}, height={section.page_height}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: 'Certificate of Completion' title - centered, 36pt, bold (0.20 points)
    # Initial doc is blank; this text does not exist in initial.
    try:
        found_title = False
        for text, para in non_empty:
            if 'certificate of completion' in text.lower():
                is_centered = para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER
                # Check runs for 36pt bold
                has_bold_36 = False
                for run in para.runs:
                    if run.text.strip():
                        is_bold = run.font.bold is True
                        is_36 = run.font.size is not None and abs(run.font.size.pt - 36.0) < 1.0
                        if is_bold and is_36:
                            has_bold_36 = True
                            break

                if is_centered and has_bold_36:
                    print(f"PASS: Component 2 - 'Certificate of Completion' centered, 36pt bold (0.20 pts)")
                    total_score += 0.20
                    found_title = True
                else:
                    print(f"FAIL: Component 2 - Title found but formatting wrong. "
                          f"Centered={is_centered}, Bold+36pt={has_bold_36}")
                    found_title = True
                break
        if not found_title:
            print("FAIL: Component 2 - 'Certificate of Completion' text not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: <StudentName> placeholder - centered, 28pt, bold (0.20 points)
    # Initial doc has no such placeholder; this is a task-introduced element.
    try:
        found_student = False
        for text, para in non_empty:
            if '<studentname>' in text.lower() or 'studentname' in text.lower():
                is_centered = para.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER
                has_bold_28 = False
                for run in para.runs:
                    if run.text.strip() and 'studentname' in run.text.lower():
                        is_bold = run.font.bold is True
                        is_28 = run.font.size is not None and abs(run.font.size.pt - 28.0) < 1.0
                        if is_bold and is_28:
                            has_bold_28 = True
                            break

                if is_centered and has_bold_28:
                    print(f"PASS: Component 3 - '<StudentName>' centered, 28pt bold (0.20 pts)")
                    total_score += 0.20
                    found_student = True
                else:
                    print(f"FAIL: Component 3 - StudentName found but formatting wrong. "
                          f"Centered={is_centered}, Bold+28pt={has_bold_28}")
                    found_student = True
                break
        if not found_student:
            print("FAIL: Component 3 - '<StudentName>' placeholder not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: 'has successfully completed' + <CourseName> in 18pt (0.15 points)
    # Both are task-introduced content.
    try:
        found_completed = False
        found_course = False
        for text, para in non_empty:
            if 'has successfully completed' in text.lower():
                found_completed = True
                # Check for 18pt
                for run in para.runs:
                    if run.text.strip() and run.font.size is not None:
                        if abs(run.font.size.pt - 18.0) < 1.0:
                            found_completed = True

            if '<coursename>' in text.lower() or 'coursename' in text.lower():
                found_course = True
                for run in para.runs:
                    if run.text.strip() and 'coursename' in run.text.lower():
                        if run.font.size is not None and abs(run.font.size.pt - 18.0) < 1.0:
                            found_course = True

        sub_score = 0.0
        if found_completed:
            sub_score += 0.075
            print("PASS: Component 4a - 'has successfully completed' text found")
        else:
            print("FAIL: Component 4a - 'has successfully completed' text not found")

        if found_course:
            sub_score += 0.075
            print("PASS: Component 4b - '<CourseName>' placeholder found")
        else:
            print("FAIL: Component 4b - '<CourseName>' placeholder not found")

        if sub_score > 0:
            total_score += sub_score
            print(f"  Component 4 total: {sub_score:.3f} pts")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: <CompletionDate> and <InstructorName> present (0.10 points)
    # Both are task-introduced content.
    try:
        all_text = ' '.join(text for text, _ in non_empty).lower()
        has_date = 'completiondate' in all_text
        has_instructor = 'instructorname' in all_text

        sub_score = 0.0
        if has_date:
            sub_score += 0.05
            print("PASS: Component 5a - '<CompletionDate>' placeholder found")
        else:
            print("FAIL: Component 5a - '<CompletionDate>' placeholder not found")

        if has_instructor:
            sub_score += 0.05
            print("PASS: Component 5b - '<InstructorName>' placeholder found")
        else:
            print("FAIL: Component 5b - '<InstructorName>' placeholder not found")

        if sub_score > 0:
            total_score += sub_score
            print(f"  Component 5 total: {sub_score:.3f} pts")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Decorative page border present (0.15 points)
    # Initial doc has no page borders; golden has double border on all sides.
    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        sect_pr = doc.sections[0]._sectPr
        pg_borders = sect_pr.findall('.//w:pgBorders', ns)

        if len(pg_borders) > 0:
            border_elem = pg_borders[0]
            sides_found = 0
            for side in ['top', 'left', 'bottom', 'right']:
                side_elem = border_elem.find(f'w:{side}', ns)
                if side_elem is not None:
                    val = side_elem.get(qn('w:val'))
                    if val and val != 'none':
                        sides_found += 1

            if sides_found == 4:
                print(f"PASS: Component 6 - Decorative page border found on all 4 sides (0.15 pts)")
                total_score += 0.15
            elif sides_found > 0:
                partial = 0.15 * (sides_found / 4)
                print(f"PARTIAL: Component 6 - Border found on {sides_found}/4 sides ({partial:.3f} pts)")
                total_score += partial
            else:
                print("FAIL: Component 6 - pgBorders element exists but no valid border sides")
        else:
            print("FAIL: Component 6 - No page borders found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
