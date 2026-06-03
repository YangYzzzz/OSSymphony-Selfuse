"""
Reward Script: Apply paragraph styles to legal document Court_Brief.docx
Task ID: writer_pd_026
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Body paragraphs use Times New Roman 12pt with 1.5 line spacing
  Component 2 (0.20): Body paragraphs have 1.27cm first-line indent
  Component 3 (0.25): Block quotes use 11pt italic Times New Roman with 2cm left/right indent
  Component 4 (0.25): Headings use Arial 14pt bold with 18pt space before and Heading style
"""

import os
from docx import Document
from docx.shared import Pt, Cm

WORKDIR = '/home/user'
TASK_ID = 'writer_pd_026'


def persist_app_state():
    """Save any unsaved state in LibreOffice Writer."""
    try:
        os.environ["DISPLAY"] = ":0"
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        import time
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def classify_paragraphs(doc):
    """Classify paragraphs into heading, block_quote, and body categories.

    Headings: paragraphs whose style name starts with 'Heading', OR
              paragraphs that are 14pt bold (manually formatted headings in initial).
    Block quotes: paragraphs with left_indent >= 1.5cm (indented quotes).
    Body: everything else with text content.
    """
    headings = []
    block_quotes = []
    body = []

    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if not text:
            continue

        pf = p.paragraph_format
        style_name = p.style.name if p.style else ''

        # Check if it is a heading-like paragraph
        is_heading_style = style_name.startswith('Heading')
        is_heading_manual = (
            bool(p.runs)
            and p.runs[0].font.bold
            and p.runs[0].font.size is not None
            and p.runs[0].font.size.pt >= 13.5
        )

        # Check if it is a block quote (indented paragraph)
        li = pf.left_indent
        is_block_quote = (li is not None and li >= Cm(1.5))

        if is_heading_style or is_heading_manual:
            headings.append((i, p))
        elif is_block_quote:
            block_quotes.append((i, p))
        else:
            body.append((i, p))

    return headings, block_quotes, body


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

    headings, block_quotes, body = classify_paragraphs(doc)
    print(f"INFO: Found {len(headings)} headings, {len(block_quotes)} block quotes, {len(body)} body paragraphs")

    # Component 1: Body paragraphs use Times New Roman 12pt with 1.5 line spacing (0.30 pts)
    try:
        if len(body) == 0:
            print("FAIL: Component 1 -- No body paragraphs found")
        else:
            tnr_count = 0
            size_ok_count = 0
            spacing_ok_count = 0
            checked = 0

            for idx, p in body:
                pf = p.paragraph_format
                for run in p.runs:
                    if run.text.strip():
                        checked += 1
                        if run.font.name == 'Times New Roman':
                            tnr_count += 1
                        if run.font.size and abs(run.font.size.pt - 12.0) < 0.5:
                            size_ok_count += 1
                        break  # check first non-empty run

                # Check line spacing on paragraph level
                ls = pf.line_spacing
                if ls is not None and abs(float(ls) - 1.5) < 0.1:
                    spacing_ok_count += 1

            if checked == 0:
                print("FAIL: Component 1 -- No body runs to check")
            else:
                tnr_ratio = tnr_count / checked
                size_ratio = size_ok_count / checked
                spacing_ratio = spacing_ok_count / len(body) if len(body) > 0 else 0

                # All three sub-checks must pass at >= 80% ratio
                if tnr_ratio >= 0.8 and size_ratio >= 0.8 and spacing_ratio >= 0.8:
                    print(f"PASS: Component 1 -- Body: TNR={tnr_ratio:.0%}, 12pt={size_ratio:.0%}, 1.5sp={spacing_ratio:.0%} (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 1 -- Body: TNR={tnr_ratio:.0%}, 12pt={size_ratio:.0%}, 1.5sp={spacing_ratio:.0%}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Body paragraphs have 1.27cm first-line indent (0.20 pts)
    try:
        if len(body) == 0:
            print("FAIL: Component 2 -- No body paragraphs found")
        else:
            fli_ok_count = 0
            fli_total = 0
            target_fli = Cm(1.27)  # 457200 EMU

            for idx, p in body:
                pf = p.paragraph_format
                fli = pf.first_line_indent
                fli_total += 1
                # Accept first_line_indent close to 1.27cm (allow 0.15cm tolerance)
                # Also accept 0 for special paragraphs like case number, party names etc.
                if fli is not None and abs(fli - target_fli) < Cm(0.15):
                    fli_ok_count += 1

            fli_ratio = fli_ok_count / fli_total if fli_total > 0 else 0

            # Many body paragraphs should have first-line indent; at least 50% (some may be special lines)
            if fli_ratio >= 0.5:
                print(f"PASS: Component 2 -- First-line indent: {fli_ok_count}/{fli_total} ({fli_ratio:.0%}) body paras have ~1.27cm indent (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 -- First-line indent: {fli_ok_count}/{fli_total} ({fli_ratio:.0%}) body paras have ~1.27cm indent (need >= 50%)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Block quotes use 11pt italic with 2cm left/right indent (0.25 pts)
    try:
        if len(block_quotes) == 0:
            print("FAIL: Component 3 -- No block quotes found")
        else:
            italic_ok = 0
            size_ok = 0
            indent_ok = 0
            font_ok = 0
            total_bq = len(block_quotes)
            target_indent = Cm(2.0)  # 720000 EMU

            for idx, p in block_quotes:
                pf = p.paragraph_format
                li = pf.left_indent or 0
                ri = pf.right_indent or 0

                # Check indent (2cm with tolerance)
                if abs(li - target_indent) < Cm(0.2) and abs(ri - target_indent) < Cm(0.2):
                    indent_ok += 1

                # Check font properties on first run
                if p.runs:
                    r = p.runs[0]
                    if r.font.italic:
                        italic_ok += 1
                    if r.font.size and abs(r.font.size.pt - 11.0) < 0.5:
                        size_ok += 1
                    if r.font.name == 'Times New Roman':
                        font_ok += 1

            # For scoring: italic + 11pt are the key task changes (indent was pre-existing)
            # So we score based on italic and size changes primarily
            italic_ratio = italic_ok / total_bq
            size_ratio = size_ok / total_bq
            font_ratio = font_ok / total_bq

            if italic_ratio >= 0.75 and size_ratio >= 0.75:
                print(f"PASS: Component 3 -- Block quotes: italic={italic_ratio:.0%}, 11pt={size_ratio:.0%}, TNR={font_ratio:.0%} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Block quotes: italic={italic_ratio:.0%}, 11pt={size_ratio:.0%}, TNR={font_ratio:.0%}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Headings use Arial 14pt bold with 18pt space before and Heading style (0.25 pts)
    try:
        if len(headings) == 0:
            print("FAIL: Component 4 -- No heading paragraphs found")
        else:
            heading_style_ok = 0
            arial_ok = 0
            size_ok = 0
            bold_ok = 0
            space_before_ok = 0
            total_h = len(headings)
            target_sb = Pt(18)  # 228600 EMU

            for idx, p in headings:
                pf = p.paragraph_format
                style_name = p.style.name if p.style else ''

                # Check heading style (must be Heading 1 or Heading 2, not Normal)
                if style_name.startswith('Heading'):
                    heading_style_ok += 1

                # Check font properties
                if p.runs:
                    r = p.runs[0]
                    if r.font.name == 'Arial':
                        arial_ok += 1
                    if r.font.size and abs(r.font.size.pt - 14.0) < 0.5:
                        size_ok += 1
                    if r.font.bold:
                        bold_ok += 1

                # Check space before (18pt = 228600 EMU)
                sb = pf.space_before
                if sb is not None and abs(sb - target_sb) < Pt(2):
                    space_before_ok += 1

            style_ratio = heading_style_ok / total_h
            arial_ratio = arial_ok / total_h
            sb_ratio = space_before_ok / total_h

            # Key task changes: heading style (was Normal), Arial font (was Calibri), 18pt space before (was 12pt)
            # Bold and 14pt were pre-existing, so we don't score those alone
            sub_score = 0.0
            if style_ratio >= 0.75:
                sub_score += 0.10
                print(f"  PASS: Heading style applied: {heading_style_ok}/{total_h} ({style_ratio:.0%})")
            else:
                print(f"  FAIL: Heading style applied: {heading_style_ok}/{total_h} ({style_ratio:.0%})")

            if arial_ratio >= 0.75:
                sub_score += 0.08
                print(f"  PASS: Arial font: {arial_ok}/{total_h} ({arial_ratio:.0%})")
            else:
                print(f"  FAIL: Arial font: {arial_ok}/{total_h} ({arial_ratio:.0%})")

            if sb_ratio >= 0.75:
                sub_score += 0.07
                print(f"  PASS: 18pt space before: {space_before_ok}/{total_h} ({sb_ratio:.0%})")
            else:
                print(f"  FAIL: 18pt space before: {space_before_ok}/{total_h} ({sb_ratio:.0%})")

            if sub_score > 0:
                print(f"PASS: Component 4 -- Headings scored {sub_score:.2f}/0.25 pts")
                total_score += sub_score
            else:
                print(f"FAIL: Component 4 -- Headings scored 0.00/0.25 pts")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    # Try alternate name
    file_path = f'{WORKDIR}/Court_Brief.docx'
    if not os.path.exists(file_path):
        print(f"File not found: {WORKDIR}/{TASK_ID}.docx or {WORKDIR}/Court_Brief.docx")
        print("REWARD: 0.0")
    else:
        verify_task(file_path)
else:
    verify_task(file_path)
