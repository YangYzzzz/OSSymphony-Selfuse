"""
Reward Script: Create a 'Meeting Minutes' list style with em-dash bullet and 0.8cm indent
Task ID: writer_lec_022
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.25): 'Meeting Minutes' paragraph style exists
  - Component 2 (0.30): Numbering uses em-dash (U+2014) as level-0 bullet
  - Component 3 (0.20): Level-0 left indent is ~0.8 cm (453 twips)
  - Component 4 (0.25): Style applied to meeting-note paragraphs (paras 8-14)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_022'

# Em-dash character (U+2014)
EM_DASH = '\u2014'
# 0.8 cm in twips: 1 cm = 567 twips, 0.8 cm = 453.6 twips
TARGET_INDENT_TWIPS = 454
INDENT_TOLERANCE_TWIPS = 30  # allow some tolerance


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

    # Component 1: 'Meeting Minutes' paragraph style exists (0.25 points)
    meeting_minutes_style = None
    try:
        for s in doc.styles:
            if s.name == 'Meeting Minutes' and s.type == 1:  # PARAGRAPH type
                meeting_minutes_style = s
                break

        if meeting_minutes_style is not None:
            print(f"PASS: Component 1 — 'Meeting Minutes' paragraph style found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — 'Meeting Minutes' paragraph style not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If style doesn't exist, remaining checks will fail — still try them for diagnostics
    # but they should naturally fail.

    # Component 2: Em-dash bullet character at level 0 (0.30 points)
    try:
        if meeting_minutes_style is not None:
            # Get the numId from the style's pPr
            pPr = meeting_minutes_style.element.find(qn('w:pPr'))
            numPr = pPr.find(qn('w:numPr')) if pPr is not None else None
            numId_el = numPr.find(qn('w:numId')) if numPr is not None else None
            num_id_val = numId_el.get(qn('w:val')) if numId_el is not None else None

            if num_id_val is not None:
                # Find the abstractNumId from the num element
                numbering_part = doc.part.numbering_part
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                abstract_num_id = None

                for num_el in numbering_part.element.findall('.//w:num', ns):
                    if num_el.get(qn('w:numId')) == num_id_val:
                        abs_ref = num_el.find('w:abstractNumId', ns)
                        if abs_ref is not None:
                            abstract_num_id = abs_ref.get(qn('w:val'))
                        break

                if abstract_num_id is not None:
                    # Find the abstractNum and check level 0 bullet text
                    for abs_num in numbering_part.element.findall('.//w:abstractNum', ns):
                        if abs_num.get(qn('w:abstractNumId')) == abstract_num_id:
                            lvl0 = None
                            for lvl in abs_num.findall('w:lvl', ns):
                                if lvl.get(qn('w:ilvl')) == '0':
                                    lvl0 = lvl
                                    break

                            if lvl0 is not None:
                                # Check numFmt is bullet
                                num_fmt = lvl0.find('w:numFmt', ns)
                                is_bullet = (num_fmt is not None and
                                             num_fmt.get(qn('w:val')) == 'bullet')

                                # Check lvlText for em-dash
                                lvl_text = lvl0.find('w:lvlText', ns)
                                bullet_char = lvl_text.get(qn('w:val')) if lvl_text is not None else None

                                if is_bullet and bullet_char == EM_DASH:
                                    print(f"PASS: Component 2 — Em-dash bullet character at level 0 (0.30 pts)")
                                    total_score += 0.30
                                else:
                                    print(f"FAIL: Component 2 — Expected em-dash bullet, "
                                          f"found: bullet={is_bullet}, char={repr(bullet_char)}")
                            else:
                                print(f"FAIL: Component 2 — Level 0 not found in abstractNum")
                            break
                    else:
                        print(f"FAIL: Component 2 — abstractNum {abstract_num_id} not found")
                else:
                    print(f"FAIL: Component 2 — Could not resolve abstractNumId from numId={num_id_val}")
            else:
                print(f"FAIL: Component 2 — Style has no numId reference")
        else:
            print(f"FAIL: Component 2 — No 'Meeting Minutes' style to check numbering")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Level 0 left indent ~0.8 cm / ~453 twips (0.20 points)
    try:
        if meeting_minutes_style is not None:
            pPr = meeting_minutes_style.element.find(qn('w:pPr'))
            numPr = pPr.find(qn('w:numPr')) if pPr is not None else None
            numId_el = numPr.find(qn('w:numId')) if numPr is not None else None
            num_id_val = numId_el.get(qn('w:val')) if numId_el is not None else None

            if num_id_val is not None:
                numbering_part = doc.part.numbering_part
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                abstract_num_id = None

                for num_el in numbering_part.element.findall('.//w:num', ns):
                    if num_el.get(qn('w:numId')) == num_id_val:
                        abs_ref = num_el.find('w:abstractNumId', ns)
                        if abs_ref is not None:
                            abstract_num_id = abs_ref.get(qn('w:val'))
                        break

                if abstract_num_id is not None:
                    for abs_num in numbering_part.element.findall('.//w:abstractNum', ns):
                        if abs_num.get(qn('w:abstractNumId')) == abstract_num_id:
                            for lvl in abs_num.findall('w:lvl', ns):
                                if lvl.get(qn('w:ilvl')) == '0':
                                    ind_el = lvl.find('w:pPr/w:ind', ns)
                                    if ind_el is not None:
                                        left_val = ind_el.get(qn('w:left'))
                                        if left_val is not None:
                                            left_twips = int(left_val)
                                            diff = abs(left_twips - TARGET_INDENT_TWIPS)
                                            if diff <= INDENT_TOLERANCE_TWIPS:
                                                print(f"PASS: Component 3 — Level 0 indent={left_twips} twips "
                                                      f"(target ~{TARGET_INDENT_TWIPS}, diff={diff}) (0.20 pts)")
                                                total_score += 0.20
                                            else:
                                                print(f"FAIL: Component 3 — Level 0 indent={left_twips} twips, "
                                                      f"expected ~{TARGET_INDENT_TWIPS} (0.8 cm), diff={diff}")
                                        else:
                                            print(f"FAIL: Component 3 — No w:left attribute on indent")
                                    else:
                                        print(f"FAIL: Component 3 — No indent element in level 0")
                                    break
                            break
                else:
                    print(f"FAIL: Component 3 — Could not resolve abstractNumId")
            else:
                print(f"FAIL: Component 3 — Style has no numId reference")
        else:
            print(f"FAIL: Component 3 — No 'Meeting Minutes' style to check indent")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Style applied to meeting-note paragraphs (0.25 points)
    # The meeting notes are paragraphs under "Key Discussion Points" heading (paras 8-14 in both initial/golden).
    # We check that at least some paragraphs use the 'Meeting Minutes' style.
    try:
        applied_count = 0
        total_meeting_paras = 0

        # Find paragraphs between "Key Discussion Points" and "Action Items" headings
        in_section = False
        for p in doc.paragraphs:
            if p.style and p.style.name.startswith('Heading') and 'Key Discussion' in p.text:
                in_section = True
                continue
            if p.style and p.style.name.startswith('Heading') and in_section:
                break
            if in_section and p.text.strip():
                total_meeting_paras += 1
                if p.style and p.style.name == 'Meeting Minutes':
                    applied_count += 1

        if total_meeting_paras > 0 and applied_count == total_meeting_paras:
            print(f"PASS: Component 4 — 'Meeting Minutes' style applied to all {applied_count} "
                  f"meeting-note paragraphs (0.25 pts)")
            total_score += 0.25
        elif applied_count > 0:
            # Partial credit: proportional
            partial = 0.25 * (applied_count / total_meeting_paras)
            print(f"PARTIAL: Component 4 — Style applied to {applied_count}/{total_meeting_paras} "
                  f"paragraphs ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — 'Meeting Minutes' style not applied to any meeting-note paragraphs "
                  f"(found {total_meeting_paras} candidate paragraphs)")
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
