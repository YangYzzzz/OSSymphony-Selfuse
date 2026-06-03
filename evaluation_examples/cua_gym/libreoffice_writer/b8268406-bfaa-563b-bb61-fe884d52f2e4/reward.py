"""
Reward Script: Insert a date field at the top of the document before 'Meeting Agenda'
Task ID: writer_struct_008
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): A DATE field paragraph exists before the 'Meeting Agenda' heading
  Component 2 (0.3): The field has correct Word field structure (fldChar begin/instrText/end)
  Component 3 (0.2): Remaining document structure is intact (Heading 1 + 5 bullet points)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_008'
FILE_PATH = '/home/user/Desktop/team_meeting.docx'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError as e:
        print(f"CRITICAL: Cannot import python-docx: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    print(f"Total paragraphs: {len(paragraphs)}")
    for i, p in enumerate(paragraphs):
        print(f"  Para[{i}]: style={p.style.name!r}, text={p.text!r}")

    # Component 1: A DATE field paragraph exists as first paragraph before 'Meeting Agenda' (0.5 points)
    # This verifies that:
    # (a) the first paragraph contains a field (instrText with DATE)
    # (b) the second paragraph is the 'Meeting Agenda' heading
    # On initial_env: no field at top -> FAIL. On golden_env: field present -> PASS.
    try:
        first_para = paragraphs[0] if paragraphs else None
        has_date_field = False
        if first_para is not None:
            xml = first_para._element.xml
            # Check for DATE field instruction text
            if 'instrText' in xml and 'DATE' in xml:
                has_date_field = True

        # Also verify the heading is the second paragraph (position changed)
        heading_is_second = (
            len(paragraphs) >= 2
            and paragraphs[1].style.name == 'Heading 1'
            and 'Meeting Agenda' in paragraphs[1].text
        )

        if has_date_field and heading_is_second:
            print(f"PASS: Component 1 — DATE field found in first paragraph, 'Meeting Agenda' heading is second paragraph (0.5 pts)")
            total_score += 0.5
        elif has_date_field and not heading_is_second:
            print(f"FAIL: Component 1 — DATE field found but 'Meeting Agenda' heading is not the second paragraph")
        elif not has_date_field and heading_is_second:
            first_para_text = first_para.text if first_para else 'N/A'
            print(f"FAIL: Component 1 — No DATE field in first paragraph; first para text={first_para_text!r}")
        else:
            print(f"FAIL: Component 1 — No DATE field and heading not in expected position")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The date field has correct Word field structure (fldChar begin/end + instrText) (0.3 points)
    # This verifies proper field insertion (not just plain text "March 5, 2026").
    # On initial_env: no field -> FAIL. On golden_env: proper field structure -> PASS.
    try:
        first_para = paragraphs[0] if paragraphs else None
        has_fld_begin = False
        has_fld_end = False
        has_instr_text = False
        if first_para is not None:
            xml = first_para._element.xml
            has_fld_begin = 'fldCharType="begin"' in xml or "fldCharType='begin'" in xml
            has_fld_end = 'fldCharType="end"' in xml or "fldCharType='end'" in xml
            has_instr_text = 'instrText' in xml

        if has_fld_begin and has_fld_end and has_instr_text:
            print(f"PASS: Component 2 — Field has correct structure: fldChar begin, instrText, fldChar end (0.3 pts)")
            total_score += 0.3
        else:
            details = []
            if not has_fld_begin:
                details.append("missing fldChar begin")
            if not has_fld_end:
                details.append("missing fldChar end")
            if not has_instr_text:
                details.append("missing instrText")
            print(f"FAIL: Component 2 — Field structure incomplete: {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Remaining document structure is intact (0.2 points)
    # Verifies that the addition of the date field did not corrupt or alter the rest of the document.
    # Checks: total 7 paragraphs, heading at para[1], 5 bullet points at para[2]-para[6].
    # On initial_env: document has 6 paragraphs (no prepended para) -> FAIL.
    # On golden_env: 7 paragraphs with intact structure -> PASS.
    try:
        expected_bullets = [
            'Q2 Budget Review and Financial Projections',
            'Product Roadmap Updates and Milestone Discussion',
            'Team Performance Metrics and KPI Assessment',
            'Client Partnership Opportunities and Onboarding Status',
            'Action Items, Deadlines, and Next Steps',
        ]
        structure_ok = True

        # After the date field, total paragraphs should be 7
        if len(paragraphs) != 7:
            print(f"FAIL: Component 3 — Expected 7 paragraphs, found {len(paragraphs)}")
            structure_ok = False

        # Para[1] = Heading 1 'Meeting Agenda'
        if structure_ok:
            h = paragraphs[1]
            if h.style.name != 'Heading 1' or 'Meeting Agenda' not in h.text:
                print(f"FAIL: Component 3 — Para[1] expected Heading 1 'Meeting Agenda', found style={h.style.name!r}, text={h.text!r}")
                structure_ok = False

        # Para[2]-Para[6] = 5 bullet points
        if structure_ok:
            for idx, expected_text in enumerate(expected_bullets):
                p = paragraphs[idx + 2]
                if 'List Bullet' not in p.style.name or expected_text not in p.text:
                    print(f"FAIL: Component 3 — Para[{idx+2}] expected bullet '{expected_text}', found style={p.style.name!r}, text={p.text!r}")
                    structure_ok = False
                    break

        if structure_ok:
            print(f"PASS: Component 3 — Document structure intact: 7 paragraphs, correct heading at [1], 5 bullets at [2-6] (0.2 pts)")
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
