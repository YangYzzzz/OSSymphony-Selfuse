"""
Reward Script: Create 'CommandLine' paragraph style in LibreOffice Writer
Task ID: writer_tech_043
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): CommandLine paragraph style exists
  Component 2 (0.25): Font properties — Liberation Mono 10pt, green #00FF00
  Component 3 (0.2): Background black, left indent ~0.3cm
  Component 4 (0.25): CommandLine style applied to command paragraphs
"""

import os
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_043'


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

    # -------------------------------------------------------
    # Component 1: CommandLine paragraph style exists (0.3 pts)
    # -------------------------------------------------------
    style_found = False
    style_elem = None
    try:
        styles_elem = doc.styles.element
        for s in styles_elem.findall(qn('w:style')):
            name_elem = s.find(qn('w:name'))
            stype = s.get(qn('w:type'))
            if name_elem is not None:
                val = name_elem.get(qn('w:val'))
                if val == 'CommandLine' and stype == 'paragraph':
                    style_found = True
                    style_elem = s
                    break
        if style_found:
            print(f"PASS: Component 1 — 'CommandLine' paragraph style exists (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — 'CommandLine' paragraph style not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------
    # Component 2: Font properties — Liberation Mono 10pt, green text (0.25 pts)
    # Checks: rFonts ascii="Liberation Mono", sz=20 (10pt), color=00FF00
    # -------------------------------------------------------
    if style_found and style_elem is not None:
        try:
            rpr = style_elem.find(qn('w:rPr'))
            sub_score = 0.0
            sub_total = 3  # font name, size, color

            # Font name
            rfonts = rpr.find(qn('w:rFonts')) if rpr is not None else None
            if rfonts is not None:
                ascii_font = rfonts.get(qn('w:ascii'), '')
                if 'Liberation Mono' in ascii_font:
                    sub_score += 1
                    print(f"  PASS: Font name = '{ascii_font}'")
                else:
                    print(f"  FAIL: Font name expected 'Liberation Mono', found '{ascii_font}'")
            else:
                print(f"  FAIL: No rFonts element in CommandLine style")

            # Font size (w:sz value in half-points, 20 = 10pt)
            sz_elem = rpr.find(qn('w:sz')) if rpr is not None else None
            if sz_elem is not None:
                sz_val = sz_elem.get(qn('w:val'), '')
                if sz_val == '20':
                    sub_score += 1
                    print(f"  PASS: Font size = 10pt (sz={sz_val})")
                else:
                    print(f"  FAIL: Font size expected 20 (10pt), found {sz_val}")
            else:
                print(f"  FAIL: No sz element in CommandLine style")

            # Font color (w:color val="00FF00")
            color_elem = rpr.find(qn('w:color')) if rpr is not None else None
            if color_elem is not None:
                color_val = color_elem.get(qn('w:val'), '').upper()
                if color_val == '00FF00':
                    sub_score += 1
                    print(f"  PASS: Text color = #{color_val}")
                else:
                    print(f"  FAIL: Text color expected #00FF00, found #{color_val}")
            else:
                print(f"  FAIL: No color element in CommandLine style")

            comp2_score = 0.25 * (sub_score / sub_total)
            if comp2_score > 0:
                print(f"PASS: Component 2 — Font properties ({sub_score}/{sub_total} checks) ({comp2_score:.3f} pts)")
            else:
                print(f"FAIL: Component 2 — Font properties ({sub_score}/{sub_total} checks)")
            total_score += comp2_score
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")
    else:
        print(f"SKIP: Component 2 — style not found, cannot check font properties")

    # -------------------------------------------------------
    # Component 3: Black background (shading) and left indent ~0.3cm (0.2 pts)
    # Checks: pPr/shd fill="000000", pPr/ind left ~170 twips
    # -------------------------------------------------------
    if style_found and style_elem is not None:
        try:
            ppr = style_elem.find(qn('w:pPr'))
            sub_score = 0.0
            sub_total = 2

            # Background shading
            shd = ppr.find(qn('w:shd')) if ppr is not None else None
            if shd is not None:
                fill_val = shd.get(qn('w:fill'), '').upper()
                if fill_val == '000000':
                    sub_score += 1
                    print(f"  PASS: Background fill = #{fill_val} (black)")
                else:
                    print(f"  FAIL: Background fill expected #000000, found #{fill_val}")
            else:
                print(f"  FAIL: No shading element in CommandLine style")

            # Left indent (~170 twips = 0.3cm; allow range 140-200 for tolerance)
            ind = ppr.find(qn('w:ind')) if ppr is not None else None
            if ind is not None:
                left_val = ind.get(qn('w:left'), '0')
                try:
                    left_int = int(left_val)
                    # 0.3 cm = ~170 twips. Allow 100-250 for tolerance.
                    if 100 <= left_int <= 250:
                        sub_score += 1
                        print(f"  PASS: Left indent = {left_int} twips (~{left_int/567:.2f} cm)")
                    else:
                        print(f"  FAIL: Left indent expected ~170 twips (0.3cm), found {left_int} twips")
                except ValueError:
                    print(f"  FAIL: Left indent not numeric: {left_val}")
            else:
                print(f"  FAIL: No indent element in CommandLine style")

            comp3_score = 0.2 * (sub_score / sub_total)
            if comp3_score > 0:
                print(f"PASS: Component 3 — Background/indent ({sub_score}/{sub_total} checks) ({comp3_score:.3f} pts)")
            else:
                print(f"FAIL: Component 3 — Background/indent ({sub_score}/{sub_total} checks)")
            total_score += comp3_score
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")
    else:
        print(f"SKIP: Component 3 — style not found, cannot check background/indent")

    # -------------------------------------------------------
    # Component 4: CommandLine style applied to command paragraphs (0.25 pts)
    # In the golden doc, command-line paragraphs use the CommandLine style.
    # We check that at least 5 paragraphs use CommandLine style.
    # -------------------------------------------------------
    try:
        cmd_style_count = 0
        for para in doc.paragraphs:
            if para.style and para.style.name == 'CommandLine':
                cmd_style_count += 1

        if cmd_style_count >= 5:
            print(f"PASS: Component 4 — {cmd_style_count} paragraphs use 'CommandLine' style (0.25 pts)")
            total_score += 0.25
        elif cmd_style_count > 0:
            # Partial: some applied but not enough
            partial = 0.25 * min(cmd_style_count / 5.0, 1.0)
            print(f"PARTIAL: Component 4 — {cmd_style_count} paragraphs use 'CommandLine' style ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No paragraphs use 'CommandLine' style")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
