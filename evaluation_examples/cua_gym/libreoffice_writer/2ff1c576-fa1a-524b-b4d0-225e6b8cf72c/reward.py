"""
Reward Script: Court opinion style setup verification
Task ID: writer_legal_086
Domain: libreoffice_writer
Scoring: 4 components (0.25 each) for Court Heading, Court Subheading, Court Body, Court Quote styles
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_086'


def persist_app_state(domain: str):
    """Save any unsaved changes in LibreOffice before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that 4 custom paragraph styles exist with the correct properties.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.shared import Pt, Inches
        from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: tolerance for EMU values (0.5in = 457200 EMU, allow ~5% tolerance)
    def emu_close(actual, expected, tolerance=25000):
        if actual is None:
            return False
        return abs(actual - expected) <= tolerance

    def pt_close(actual_size, expected_pt, tolerance=0.5):
        if actual_size is None:
            return False
        return abs(actual_size.pt - expected_pt) <= tolerance

    # Component 1: Court Heading style (0.25 points)
    # Must: exist, based on Heading 1, centered, all caps, bold, 14pt
    try:
        style = doc.styles['Court Heading']
        checks_passed = 0
        total_checks = 5

        # Check base style is Heading 1
        if style.base_style and style.base_style.name == 'Heading 1':
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Heading base_style={style.base_style.name if style.base_style else None}, expected Heading 1")

        # Check centered alignment
        if style.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Heading alignment={style.paragraph_format.alignment}, expected CENTER")

        # Check all caps
        if style.font.all_caps is True:
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Heading all_caps={style.font.all_caps}, expected True")

        # Check bold
        if style.font.bold is True:
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Heading bold={style.font.bold}, expected True")

        # Check 14pt
        if pt_close(style.font.size, 14.0):
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Heading font.size={style.font.size}, expected 14pt")

        component_score = 0.25 * (checks_passed / total_checks)
        if checks_passed == total_checks:
            print(f"PASS: Component 1 — Court Heading style fully correct ({0.25} pts)")
            total_score += component_score
        elif checks_passed > 0:
            print(f"PARTIAL: Component 1 — Court Heading {checks_passed}/{total_checks} properties correct ({component_score:.3f} pts)")
            total_score += component_score
        else:
            print(f"FAIL: Component 1 — Court Heading 0/{total_checks} properties correct")

    except KeyError:
        print("FAIL: Component 1 — 'Court Heading' style does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Court Subheading style (0.25 points)
    # Must: exist, based on Heading 2, left-aligned, bold, small caps, 12pt
    try:
        style = doc.styles['Court Subheading']
        checks_passed = 0
        total_checks = 5

        # Check base style is Heading 2
        if style.base_style and style.base_style.name == 'Heading 2':
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Subheading base_style={style.base_style.name if style.base_style else None}, expected Heading 2")

        # Check left alignment
        if style.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.LEFT:
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Subheading alignment={style.paragraph_format.alignment}, expected LEFT")

        # Check bold
        if style.font.bold is True:
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Subheading bold={style.font.bold}, expected True")

        # Check small caps
        if style.font.small_caps is True:
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Subheading small_caps={style.font.small_caps}, expected True")

        # Check 12pt
        if pt_close(style.font.size, 12.0):
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Subheading font.size={style.font.size}, expected 12pt")

        component_score = 0.25 * (checks_passed / total_checks)
        if checks_passed == total_checks:
            print(f"PASS: Component 2 — Court Subheading style fully correct ({0.25} pts)")
            total_score += component_score
        elif checks_passed > 0:
            print(f"PARTIAL: Component 2 — Court Subheading {checks_passed}/{total_checks} properties correct ({component_score:.3f} pts)")
            total_score += component_score
        else:
            print(f"FAIL: Component 2 — Court Subheading 0/{total_checks} properties correct")

    except KeyError:
        print("FAIL: Component 2 — 'Court Subheading' style does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Court Body style (0.25 points)
    # Must: justified, double-spaced, 12pt Times New Roman, first-line indent 0.5in
    try:
        style = doc.styles['Court Body']
        checks_passed = 0
        total_checks = 5

        # Check justified alignment
        if style.paragraph_format.alignment == WD_PARAGRAPH_ALIGNMENT.JUSTIFY:
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Body alignment={style.paragraph_format.alignment}, expected JUSTIFY")

        # Check double spacing (2.0)
        ls = style.paragraph_format.line_spacing
        if ls is not None and abs(float(ls) - 2.0) < 0.1:
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Body line_spacing={ls}, expected 2.0")

        # Check 12pt
        if pt_close(style.font.size, 12.0):
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Body font.size={style.font.size}, expected 12pt")

        # Check Times New Roman
        if style.font.name and 'times' in style.font.name.lower():
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Body font.name={style.font.name}, expected Times New Roman")

        # Check first-line indent 0.5in (457200 EMU)
        if emu_close(style.paragraph_format.first_line_indent, 457200):
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Body first_line_indent={style.paragraph_format.first_line_indent}, expected ~457200 EMU (0.5in)")

        component_score = 0.25 * (checks_passed / total_checks)
        if checks_passed == total_checks:
            print(f"PASS: Component 3 — Court Body style fully correct ({0.25} pts)")
            total_score += component_score
        elif checks_passed > 0:
            print(f"PARTIAL: Component 3 — Court Body {checks_passed}/{total_checks} properties correct ({component_score:.3f} pts)")
            total_score += component_score
        else:
            print(f"FAIL: Component 3 — Court Body 0/{total_checks} properties correct")

    except KeyError:
        print("FAIL: Component 3 — 'Court Body' style does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Court Quote style (0.25 points)
    # Must: single-spaced, 11pt, left and right indent 0.5in
    try:
        style = doc.styles['Court Quote']
        checks_passed = 0
        total_checks = 4

        # Check single spacing (1.0)
        ls = style.paragraph_format.line_spacing
        if ls is not None and abs(float(ls) - 1.0) < 0.1:
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Quote line_spacing={ls}, expected 1.0")

        # Check 11pt
        if pt_close(style.font.size, 11.0):
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Quote font.size={style.font.size}, expected 11pt")

        # Check left indent 0.5in (457200 EMU)
        if emu_close(style.paragraph_format.left_indent, 457200):
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Quote left_indent={style.paragraph_format.left_indent}, expected ~457200 EMU (0.5in)")

        # Check right indent 0.5in (457200 EMU)
        if emu_close(style.paragraph_format.right_indent, 457200):
            checks_passed += 1
        else:
            print(f"  DETAIL: Court Quote right_indent={style.paragraph_format.right_indent}, expected ~457200 EMU (0.5in)")

        component_score = 0.25 * (checks_passed / total_checks)
        if checks_passed == total_checks:
            print(f"PASS: Component 4 — Court Quote style fully correct ({0.25} pts)")
            total_score += component_score
        elif checks_passed > 0:
            print(f"PARTIAL: Component 4 — Court Quote {checks_passed}/{total_checks} properties correct ({component_score:.3f} pts)")
            total_score += component_score
        else:
            print(f"FAIL: Component 4 — Court Quote 0/{total_checks} properties correct")

    except KeyError:
        print("FAIL: Component 4 — 'Court Quote' style does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
