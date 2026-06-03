"""
Reward Script: Insert chapter number and page number in header (format: '2-5')
Task ID: writer_fs_063
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Header contains a CHAPTER field code
  Component 2 (0.3): Header contains a PAGE field code
  Component 3 (0.3): Dash separator between CHAPTER and PAGE fields in correct order
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_063'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
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

    # Collect all header instrText fields across all sections
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # We check all sections - the task applies to the document header
    has_chapter_field = False
    has_page_field = False
    has_correct_structure = False

    for sec_idx, section in enumerate(doc.sections):
        header = section.header

        # Extract all instrText values from header
        instr_elems = header._element.findall('.//w:instrText', ns)
        instr_texts = [e.text.strip().upper() for e in instr_elems if e.text]

        # Check for CHAPTER field
        chapter_found = any('CHAPTER' in t for t in instr_texts)
        # Check for PAGE field
        page_found = any('PAGE' in t for t in instr_texts)

        if chapter_found:
            has_chapter_field = True
        if page_found:
            has_page_field = True

        # Check structure: CHAPTER field, then dash, then PAGE field
        # Walk through runs in header paragraphs to verify order
        if chapter_found and page_found:
            for para in header.paragraphs:
                runs = para._element.findall('.//w:r', ns)
                # Build a sequence of tokens: 'CHAPTER_BEGIN', 'CHAPTER_END', 'PAGE_BEGIN', 'PAGE_END', text content
                tokens = []
                in_field = False
                current_field_type = None

                for run in runs:
                    fld_chars = run.findall('.//w:fldChar', ns)
                    for fc in fld_chars:
                        fld_type = fc.get(qn('w:fldCharType'))
                        if fld_type == 'begin':
                            in_field = True
                        elif fld_type == 'separate':
                            pass
                        elif fld_type == 'end':
                            if current_field_type:
                                tokens.append(current_field_type)
                                current_field_type = None
                            in_field = False

                    instrs = run.findall('.//w:instrText', ns)
                    for instr in instrs:
                        if instr.text and 'CHAPTER' in instr.text.upper():
                            current_field_type = 'CHAPTER'
                        elif instr.text and 'PAGE' in instr.text.upper():
                            current_field_type = 'PAGE'

                    # Check for text content (dash)
                    t_elems = run.findall('.//w:t', ns)
                    for t_elem in t_elems:
                        if t_elem.text and '-' in t_elem.text and not in_field:
                            tokens.append('DASH')

                # Check order: CHAPTER before DASH before PAGE
                chapter_pos = None
                dash_pos = None
                page_pos = None
                for idx, tok in enumerate(tokens):
                    if tok == 'CHAPTER' and chapter_pos is None:
                        chapter_pos = idx
                    elif tok == 'DASH' and dash_pos is None:
                        dash_pos = idx
                    elif tok == 'PAGE' and page_pos is None:
                        page_pos = idx

                if (chapter_pos is not None and dash_pos is not None and page_pos is not None
                        and chapter_pos < dash_pos < page_pos):
                    has_correct_structure = True

    # Component 1: Header contains a CHAPTER field code (0.4 points)
    try:
        if has_chapter_field:
            print(f"PASS: Component 1 - CHAPTER field found in header (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - No CHAPTER field found in any header")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Header contains a PAGE field code (0.3 points)
    try:
        if has_page_field:
            print(f"PASS: Component 2 - PAGE field found in header (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - No PAGE field found in any header")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Correct structure CHAPTER-dash-PAGE (0.3 points)
    try:
        if has_correct_structure:
            print(f"PASS: Component 3 - Correct CHAPTER-dash-PAGE structure (0.3 pts)")
            total_score += 0.3
        else:
            if has_chapter_field and has_page_field:
                print(f"FAIL: Component 3 - CHAPTER and PAGE fields found but not in correct order with dash separator")
            else:
                print(f"FAIL: Component 3 - Missing fields, cannot verify structure")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
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
