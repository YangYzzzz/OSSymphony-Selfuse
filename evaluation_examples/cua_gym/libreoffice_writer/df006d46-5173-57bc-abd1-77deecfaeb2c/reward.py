"""
Reward Script: Create 'Defined Term' character style (bold+italic) and apply to five terms in Definitions section
Task ID: writer_legal_034
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): 'Defined Term' character style exists with bold=True, italic=True
  Component 2 (0.14 each, 0.7 total): Each of the 5 defined terms in the Definitions section
      has the 'Defined Term' style applied to its run(s)
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_034'

# The five defined terms that must have the 'Defined Term' style applied
DEFINED_TERMS = [
    'Agreement',
    'Confidential Information',
    'Effective Date',
    'Intellectual Property',
    'Services',
]


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

    # Component 1: 'Defined Term' character style exists with bold and italic (0.3 points)
    try:
        defined_term_style = None
        for style in doc.styles:
            if style.name == 'Defined Term' and style.type is not None and style.type.name == 'CHARACTER':
                defined_term_style = style
                break

        if defined_term_style is not None:
            style_bold = defined_term_style.font.bold
            style_italic = defined_term_style.font.italic
            if style_bold and style_italic:
                print(f"PASS: Component 1 — 'Defined Term' character style exists with bold={style_bold}, italic={style_italic} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — 'Defined Term' style exists but bold={style_bold}, italic={style_italic} (expected both True)")
        else:
            print("FAIL: Component 1 — 'Defined Term' character style not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each defined term in the Definitions section has 'Defined Term' style applied (0.14 pts each, 0.7 total)
    # The definitions section is identified by paragraphs between "ARTICLE 1" heading and the next heading
    try:
        # Find paragraphs in the Definitions section (between ARTICLE 1 heading and next ARTICLE heading)
        in_definitions = False
        definition_paras = []
        for para in doc.paragraphs:
            if para.style.name == 'Heading 1' and 'DEFINITIONS' in para.text.upper():
                in_definitions = True
                continue
            if in_definitions and para.style.name == 'Heading 1':
                # Next article heading, stop
                break
            if in_definitions:
                definition_paras.append(para)

        if not definition_paras:
            print("FAIL: Component 2 — Could not find Definitions section paragraphs")
        else:
            per_term_score = 0.14
            for term in DEFINED_TERMS:
                term_found_with_style = False
                for para in definition_paras:
                    # Check if any run in this paragraph has the term text and the 'Defined Term' style
                    for run in para.runs:
                        run_text = run.text.strip()
                        run_style_name = run.style.name if run.style else None
                        # The term should be in a run with 'Defined Term' style
                        if run_text == term and run_style_name == 'Defined Term':
                            term_found_with_style = True
                            break
                    if term_found_with_style:
                        break

                if term_found_with_style:
                    print(f"PASS: Component 2 — '{term}' has 'Defined Term' style applied ({per_term_score} pts)")
                    total_score += per_term_score
                else:
                    print(f"FAIL: Component 2 — '{term}' does not have 'Defined Term' style applied in Definitions section")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
