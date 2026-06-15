"""
Reward Script: Insert cross-reference to Bookmark 'sec_results' as clickable hyperlink
Task ID: writer_tm_072
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Hyperlink with anchor='sec_results' exists in document
  Component 2 (0.35): Hyperlink display text contains 'Results and Discussion'
  Component 3 (0.30): Hyperlink has visual link styling (underline/blue color)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_072'


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that a cross-reference hyperlink to bookmark 'sec_results'
    has been inserted, displaying 'Results and Discussion' as a clickable link.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all hyperlinks in the document that reference anchor='sec_results'
    ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    target_anchor = 'sec_results'

    found_hyperlinks = []
    for para in doc.paragraphs:
        for child in para._element:
            if child.tag == qn('w:hyperlink'):
                anchor = child.get(qn('w:anchor'))
                if anchor == target_anchor:
                    # Extract text from all runs inside the hyperlink
                    h_text = ''.join(
                        t.text for t in child.findall('.//' + qn('w:t'))
                        if t.text
                    )
                    # Extract styling info from runs
                    runs = child.findall('.//' + qn('w:r'))
                    has_underline = False
                    has_blue_color = False
                    for r in runs:
                        rpr = r.find(qn('w:rPr'))
                        if rpr is not None:
                            u_elem = rpr.find(qn('w:u'))
                            if u_elem is not None:
                                u_val = u_elem.get(qn('w:val'))
                                if u_val and u_val != 'none':
                                    has_underline = True
                            color_elem = rpr.find(qn('w:color'))
                            if color_elem is not None:
                                c_val = color_elem.get(qn('w:val'))
                                if c_val:
                                    # Check for blue-ish colors
                                    c_val_lower = c_val.lower()
                                    # Common hyperlink blues
                                    if c_val_lower in ('0563c1', '0000ff', '4472c4', '5b9bd5', '2e74b5', '1f4e79'):
                                        has_blue_color = True
                                    # General blue check: high blue component
                                    elif len(c_val_lower) == 6:
                                        try:
                                            r_val = int(c_val_lower[0:2], 16)
                                            g_val = int(c_val_lower[2:4], 16)
                                            b_val = int(c_val_lower[4:6], 16)
                                            if b_val > 128 and b_val > r_val and b_val > g_val:
                                                has_blue_color = True
                                        except ValueError:
                                            pass
                            # Check for Hyperlink rStyle
                            rstyle = rpr.find(qn('w:rStyle'))
                            if rstyle is not None:
                                style_val = rstyle.get(qn('w:val'))
                                if style_val and 'hyperlink' in style_val.lower():
                                    has_blue_color = True  # Hyperlink style implies link appearance

                    found_hyperlinks.append({
                        'text': h_text,
                        'has_underline': has_underline,
                        'has_blue_color': has_blue_color,
                    })

    if not found_hyperlinks:
        print(f"FAIL: No hyperlink with anchor='{target_anchor}' found in the document")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Use the first matching hyperlink
    hl = found_hyperlinks[0]

    # Component 1: Hyperlink with anchor='sec_results' exists (0.35 points)
    try:
        if len(found_hyperlinks) > 0:
            print(f"PASS: Component 1 — Hyperlink with anchor='{target_anchor}' found (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — No hyperlink with anchor='{target_anchor}' found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Hyperlink display text contains 'Results and Discussion' (0.35 points)
    try:
        h_text = hl['text'].strip()
        if 'Results and Discussion' in h_text:
            print(f"PASS: Component 2 — Hyperlink text contains 'Results and Discussion' (text: '{h_text}') (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Expected text containing 'Results and Discussion', found: '{h_text}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Hyperlink has visual link styling (0.30 points)
    # A proper hyperlink should have underline and/or blue color or Hyperlink style
    try:
        has_styling = hl['has_underline'] or hl['has_blue_color']
        if has_styling:
            details = []
            if hl['has_underline']:
                details.append('underline')
            if hl['has_blue_color']:
                details.append('blue/hyperlink color')
            print(f"PASS: Component 3 — Hyperlink has link styling ({', '.join(details)}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Hyperlink lacks visual styling (no underline or blue color)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
