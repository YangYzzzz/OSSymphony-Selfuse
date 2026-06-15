"""
Reward Script: Configure document page numbering — Roman for front matter, Arabic for chapters
Task ID: writer_tech_071
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Front matter section uses lowerRoman page numbering format
  Component 2 (0.35): Chapter section uses decimal (Arabic) page numbering format with restart at 1
  Component 3 (0.15): Document has at least 2 sections (section break between front matter and chapters)
  Component 4 (0.15): Both sections have PAGE field codes in footers (page numbers displayed)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_071'


def footer_has_page_field(section):
    """Check if a section's footer contains a PAGE field code."""
    footer = section.footer
    for fp in footer.paragraphs:
        for run in fp.runs:
            for instr in run._element.findall(qn('w:instrText')):
                if 'PAGE' in (instr.text or ''):
                    return True
    return False


def verify_task(file_path):
    """
    Verify that the document has:
    - Front matter section with lowercase Roman numeral page numbering
    - Chapter section with Arabic (decimal) numbering restarted at 1
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    sections = doc.sections
    num_sections = len(sections)
    print(f"INFO: Document has {num_sections} section(s)")

    # Component 3: Document has at least 2 sections (0.15 points)
    # This is a structural precondition that must be met for the numbering to work,
    # but in the initial_env the doc also has 2 sections — so we gate on it
    # but only award points if combined with a numbering change (handled below).
    # Actually, both initial and golden have 2 sections, so we cannot score this alone.
    # Instead, we use it as a gate.
    if num_sections < 2:
        print("FAIL: Document has fewer than 2 sections — cannot have split numbering")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Front matter section (section 0) uses lowerRoman format (0.40 points)
    # In initial_env: section 0 has fmt=decimal → FAIL
    # In golden_env: section 0 has fmt=lowerRoman → PASS
    try:
        sect0 = sections[0]._sectPr
        pgNumType0 = sect0.find(qn('w:pgNumType'))
        if pgNumType0 is not None:
            fmt0 = pgNumType0.get(qn('w:fmt'))
            print(f"INFO: Section 0 pgNumType fmt={fmt0}")
            if fmt0 == 'lowerRoman':
                print(f"PASS: Component 1 — Front matter uses lowerRoman numbering (0.40 pts)")
                total_score += 0.40
            else:
                print(f"FAIL: Component 1 — Expected lowerRoman for front matter, found: {fmt0}")
        else:
            print("FAIL: Component 1 — No pgNumType element in section 0")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Chapter section (section 1) uses decimal format with start=1 (0.35 points)
    # In initial_env: section 1 has fmt=decimal but no start attribute → FAIL
    # In golden_env: section 1 has fmt=decimal AND start=1 → PASS
    try:
        sect1 = sections[-1]._sectPr  # last section = chapters
        pgNumType1 = sect1.find(qn('w:pgNumType'))
        if pgNumType1 is not None:
            fmt1 = pgNumType1.get(qn('w:fmt'))
            start1 = pgNumType1.get(qn('w:start'))
            print(f"INFO: Section 1 pgNumType fmt={fmt1}, start={start1}")

            # Must be decimal AND restarted at 1
            if fmt1 == 'decimal' and start1 == '1':
                print(f"PASS: Component 2 — Chapter section uses decimal numbering restarted at 1 (0.35 pts)")
                total_score += 0.35
            elif fmt1 == 'decimal' and start1 is None:
                print(f"FAIL: Component 2 — Chapter section is decimal but not restarted at 1 (start is missing)")
            else:
                print(f"FAIL: Component 2 — Expected decimal+start=1 for chapters, found fmt={fmt1}, start={start1}")
        else:
            print("FAIL: Component 2 — No pgNumType element in chapter section")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Front matter section has PAGE field in footer (0.10 points)
    # Both sections should display page numbers. We check footers have PAGE fields.
    # In initial_env, footer also has PAGE field — but this check is only scored
    # when combined with the numbering format check above. We use a compound check:
    # section 0 footer has PAGE field AND fmt is lowerRoman.
    # Actually, let's check that the footer is not linked to previous (independent footer)
    # and has a PAGE field — this ensures the page number is actually displayed.
    # Both initial and golden have unlinked footers with PAGE fields, so this alone
    # would pass on both. Let's make it compound with lowerRoman.
    try:
        # Compound: footer has PAGE field AND section uses lowerRoman
        page_field_0 = footer_has_page_field(sections[0])
        sect0_pr = sections[0]._sectPr
        pgn0 = sect0_pr.find(qn('w:pgNumType'))
        fmt0_val = pgn0.get(qn('w:fmt')) if pgn0 is not None else None

        if page_field_0 and fmt0_val == 'lowerRoman':
            print(f"PASS: Component 3 — Front matter footer displays Roman page numbers (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Front matter footer: PAGE field={page_field_0}, fmt={fmt0_val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Chapter section footer has PAGE field and uses decimal+restart (0.15 points)
    # Compound check: footer has PAGE field AND section uses decimal with start=1
    try:
        page_field_1 = footer_has_page_field(sections[-1])
        sect1_pr = sections[-1]._sectPr
        pgn1 = sect1_pr.find(qn('w:pgNumType'))
        fmt1_val = pgn1.get(qn('w:fmt')) if pgn1 is not None else None
        start1_val = pgn1.get(qn('w:start')) if pgn1 is not None else None

        if page_field_1 and fmt1_val == 'decimal' and start1_val == '1':
            print(f"PASS: Component 4 — Chapter footer displays Arabic page numbers restarted at 1 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Chapter footer: PAGE field={page_field_1}, fmt={fmt1_val}, start={start1_val}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
