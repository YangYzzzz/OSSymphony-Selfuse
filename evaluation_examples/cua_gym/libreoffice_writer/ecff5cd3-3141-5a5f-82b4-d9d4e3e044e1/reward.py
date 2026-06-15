"""
Reward Script: Apply 'First Page' style to each chapter section
Task ID: writer_rm_076
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All 10 sections have titlePg enabled (Different First Page)
  Component 2 (0.3): Each section has a first-page header reference
  Component 3 (0.3): Each section has a first-page footer with chapter-specific content
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_076'


def persist_app_state(domain):
    """Best-effort save of any open LibreOffice document."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that each section in the document uses 'Different First Page' style,
    meaning titlePg is enabled and first-page headers/footers exist.
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

    num_sections = len(doc.sections)
    if num_sections < 10:
        print(f"WARN: Expected 10 sections, found {num_sections}")

    # Component 1: All sections have titlePg enabled (0.4 points)
    # titlePg is the XML element that enables "Different First Page" header/footer.
    # In initial_env this is False for all sections; in golden it should be True.
    try:
        sections_with_titlepg = 0
        for i, sec in enumerate(doc.sections):
            sectPr = sec._sectPr
            title_pg = sectPr.find(qn('w:titlePg'))
            if title_pg is not None:
                sections_with_titlepg += 1

        if num_sections > 0 and sections_with_titlepg == num_sections:
            print(f"PASS: Component 1 — All {num_sections} sections have titlePg enabled (0.4 pts)")
            total_score += 0.4
        elif sections_with_titlepg > 0:
            # Partial credit proportional to how many sections have it
            partial = 0.4 * (sections_with_titlepg / max(num_sections, 1))
            print(f"PARTIAL: Component 1 — {sections_with_titlepg}/{num_sections} sections have titlePg ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No sections have titlePg enabled (0 of {num_sections})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each section has a first-page header reference (0.3 points)
    # In initial_env sections only have 'default' header refs. In golden they should
    # also have 'first' type header references.
    try:
        sections_with_first_header = 0
        for i, sec in enumerate(doc.sections):
            sectPr = sec._sectPr
            header_refs = sectPr.findall(qn('w:headerReference'))
            if any(hr.get(qn('w:type')) == 'first' for hr in header_refs):
                sections_with_first_header += 1

        if num_sections > 0 and sections_with_first_header == num_sections:
            print(f"PASS: Component 2 — All {num_sections} sections have first-page header ref (0.3 pts)")
            total_score += 0.3
        elif sections_with_first_header > 0:
            partial = 0.3 * (sections_with_first_header / max(num_sections, 1))
            print(f"PARTIAL: Component 2 — {sections_with_first_header}/{num_sections} sections have first-page header ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No sections have first-page header references")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each section has a first-page footer reference (0.3 points)
    # In initial_env sections only have 'default' footer refs. In golden they should
    # also have 'first' type footer references, containing chapter-specific text.
    try:
        sections_with_first_footer = 0
        for i, sec in enumerate(doc.sections):
            sectPr = sec._sectPr
            footer_refs = sectPr.findall(qn('w:footerReference'))
            if any(fr.get(qn('w:type')) == 'first' for fr in footer_refs):
                sections_with_first_footer += 1

        if num_sections > 0 and sections_with_first_footer == num_sections:
            print(f"PASS: Component 3 — All {num_sections} sections have first-page footer ref (0.3 pts)")
            total_score += 0.3
        elif sections_with_first_footer > 0:
            partial = 0.3 * (sections_with_first_footer / max(num_sections, 1))
            print(f"PARTIAL: Component 3 — {sections_with_first_footer}/{num_sections} sections have first-page footer ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No sections have first-page footer references")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
