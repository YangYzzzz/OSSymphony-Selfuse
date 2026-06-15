"""
Reward Script: Create 'Warning' character style and apply to DANGER/CAUTION/NOTICE
Task ID: writer_txtfmt_062
Domain: libreoffice_writer
Scoring:
  - Component 1: 'Warning' character style exists with bold=True and font color #FF0000 (0.30 pts)
  - Component 2: 'DANGER' run has Warning style + bold + red color + yellow background (0.25 pts)
  - Component 3: 'CAUTION' run has Warning style + bold + red color + yellow background (0.25 pts)
  - Component 4: 'NOTICE' run has Warning style + bold + red color + yellow background (0.20 pts)
Total: 1.0
"""

import os
from docx import Document
from docx.shared import RGBColor
import lxml.etree as etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_txtfmt_062'
FILE_NAME = 'safety_procedures.docx'

# Namespace for XML queries
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def get_shd_fill(run_element):
    """Extract the shd fill color from a run's rPr element."""
    rpr = run_element.find(f'{{{W_NS}}}rPr')
    if rpr is None:
        return None
    shd = rpr.find(f'{{{W_NS}}}shd')
    if shd is None:
        return None
    fill = shd.get(f'{{{W_NS}}}fill')
    return fill  # e.g. 'FFFF00'


def get_run_style_name(run_element):
    """Extract the rStyle val from a run's rPr element."""
    rpr = run_element.find(f'{{{W_NS}}}rPr')
    if rpr is None:
        return None
    rstyle = rpr.find(f'{{{W_NS}}}rStyle')
    if rstyle is None:
        return None
    return rstyle.get(f'{{{W_NS}}}val')


def verify_word_formatting(doc, word, para_index_hint=None):
    """
    Find a run whose text matches `word` exactly, and verify:
      - rStyle val == 'Warning'
      - bold == True
      - font color == #FF0000
      - shd fill == #FFFF00
    Returns (found: bool, details: str)
    """
    for i, para in enumerate(doc.paragraphs):
        # Optionally skip if we have a hint and are far off
        for run in para.runs:
            if run.text.strip() == word:
                details = []
                passed = True

                # Check style
                style_val = get_run_style_name(run._element)
                if style_val == 'Warning':
                    details.append(f'rStyle=Warning OK')
                else:
                    details.append(f'rStyle={style_val!r} (expected Warning)')
                    passed = False

                # Check bold
                if run.font.bold is True:
                    details.append('bold=True OK')
                else:
                    details.append(f'bold={run.font.bold} (expected True)')
                    passed = False

                # Check font color
                try:
                    rgb = run.font.color.rgb
                    if str(rgb).upper() == 'FF0000':
                        details.append('color=#FF0000 OK')
                    else:
                        details.append(f'color=#{rgb} (expected #FF0000)')
                        passed = False
                except Exception as ce:
                    details.append(f'color check error: {ce}')
                    passed = False

                # Check yellow background via shd fill
                fill = get_shd_fill(run._element)
                if fill and fill.upper() == 'FFFF00':
                    details.append('shd_fill=#FFFF00 OK')
                else:
                    details.append(f'shd_fill={fill!r} (expected FFFF00)')
                    passed = False

                return passed, f"Para {i}: {'; '.join(details)}"
    return False, f'Run with text {word!r} not found in document'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — failure here is fatal
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'Warning' character style exists with bold=True and font color #FF0000 (0.30 pts)
    try:
        warning_style = None
        for style in doc.styles:
            if style.type.name == 'CHARACTER' and style.name == 'Warning':
                warning_style = style
                break

        if warning_style is not None:
            style_bold = warning_style.font.bold
            try:
                style_color = str(warning_style.font.color.rgb).upper() if warning_style.font.color.rgb else None
            except Exception:
                style_color = None

            if style_bold is True and style_color == 'FF0000':
                print(f"PASS: Component 1 — 'Warning' char style found, bold={style_bold}, color=#FF0000 (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 — 'Warning' char style found but bold={style_bold}, color={style_color} (expected bold=True, color=FF0000)")
        else:
            print("FAIL: Component 1 — 'Warning' character style not found in document styles")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'DANGER' run has Warning style + bold + red color + yellow background (0.25 pts)
    try:
        passed, details = verify_word_formatting(doc, 'DANGER')
        if passed:
            print(f"PASS: Component 2 — DANGER formatting verified ({details}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — DANGER formatting incorrect: {details}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'CAUTION' run has Warning style + bold + red color + yellow background (0.25 pts)
    try:
        passed, details = verify_word_formatting(doc, 'CAUTION')
        if passed:
            print(f"PASS: Component 3 — CAUTION formatting verified ({details}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — CAUTION formatting incorrect: {details}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'NOTICE' run has Warning style + bold + red color + yellow background (0.20 pts)
    try:
        passed, details = verify_word_formatting(doc, 'NOTICE')
        if passed:
            print(f"PASS: Component 4 — NOTICE formatting verified ({details}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — NOTICE formatting incorrect: {details}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the canonical task file on the VM
file_path = os.path.join(WORKDIR, FILE_NAME)
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
