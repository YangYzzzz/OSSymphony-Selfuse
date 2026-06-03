"""
Reward Script: Two-column layout for definitions section in a legal contract
Task ID: writer_legal_054
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Document has 3 sections (section breaks inserted around definitions)
  Component 2 (0.3): The definitions section uses 2-column layout
  Component 3 (0.2): Non-definitions sections remain single-column
  Component 4 (0.2): Column spacing in the 2-column section is ~0.5cm (180000 EMU)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_054'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
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
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    sections = list(doc.sections)
    num_sections = len(sections)

    # ---------------------------------------------------------------
    # Helper: get column count and spacing from a sectPr element
    # ---------------------------------------------------------------
    def get_col_info(sectPr):
        """Return (num_cols, space_emu) from a sectPr element."""
        cols_elem = sectPr.find(f'{{{ns}}}cols')
        if cols_elem is None:
            return 1, None  # default is 1 column
        num_str = cols_elem.get(f'{{{ns}}}num')
        space_str = cols_elem.get(f'{{{ns}}}space')
        num = int(num_str) if num_str else 1
        space = int(space_str) if space_str else None
        return num, space

    # ---------------------------------------------------------------
    # Component 1: Document has 3 sections (0.3 points)
    # Initial: 1 section. Golden: 3 sections (break before and after definitions).
    # ---------------------------------------------------------------
    try:
        if num_sections >= 3:
            print(f"PASS: Component 1 — Document has {num_sections} sections (expected >=3) (0.3 pts)")
            total_score += 0.3
        elif num_sections == 2:
            # Partial credit: at least one section break was inserted
            print(f"PARTIAL: Component 1 — Document has 2 sections (expected >=3) (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Document has {num_sections} section(s), expected >=3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: At least one section uses 2-column layout (0.3 points)
    # The definitions section should have w:cols w:num="2".
    # We check that some section (not the first or last) has 2 columns.
    # ---------------------------------------------------------------
    try:
        found_2col_section = False
        two_col_section_idx = -1

        # Also inspect sectPr embedded in paragraph pPr (inline section breaks)
        body = doc.element.body
        section_col_infos = []

        # Collect all section definitions in order:
        # 1) sectPr inside paragraph pPr elements (inline section breaks)
        # 2) final sectPr as last child of body
        for child in body:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == 'p':
                pPr = child.find(f'{{{ns}}}pPr')
                if pPr is not None:
                    sectPr = pPr.find(f'{{{ns}}}sectPr')
                    if sectPr is not None:
                        num_cols, space = get_col_info(sectPr)
                        section_col_infos.append((num_cols, space))
            elif tag == 'sectPr':
                num_cols, space = get_col_info(child)
                section_col_infos.append((num_cols, space))

        print(f"  DEBUG: Found {len(section_col_infos)} section definitions: {section_col_infos}")

        for idx, (ncols, sp) in enumerate(section_col_infos):
            if ncols == 2:
                found_2col_section = True
                two_col_section_idx = idx
                break

        if found_2col_section:
            print(f"PASS: Component 2 — Found 2-column section at section index {two_col_section_idx} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No section with 2-column layout found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: Non-definitions sections are single-column (0.2 points)
    # All sections except the 2-column one should have num_cols == 1.
    # ---------------------------------------------------------------
    try:
        if found_2col_section and len(section_col_infos) >= 3:
            non_def_single = True
            for idx, (ncols, sp) in enumerate(section_col_infos):
                if idx == two_col_section_idx:
                    continue  # skip the definitions section
                if ncols != 1:
                    non_def_single = False
                    print(f"  FAIL detail: Section {idx} has {ncols} columns, expected 1")

            if non_def_single:
                print(f"PASS: Component 3 — All non-definitions sections are single-column (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Some non-definitions sections are not single-column")
        elif not found_2col_section:
            print(f"FAIL: Component 3 — Cannot verify (no 2-column section found)")
        else:
            print(f"FAIL: Component 3 — Not enough sections to verify ({len(section_col_infos)} found)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: Column spacing in 2-column section is ~0.5cm (0.2 points)
    # 0.5 cm = 180000 EMU. We allow a tolerance of +/-50000 EMU (~0.14cm).
    # Also accept 720 (0.5 inch default) as a reasonable alternative.
    # ---------------------------------------------------------------
    try:
        if found_2col_section:
            _, spacing = section_col_infos[two_col_section_idx]
            if spacing is not None:
                # Accept if spacing is reasonable (between 100000 and 500000 EMU, roughly 0.28cm to 1.4cm)
                # Ideal: 180000 EMU = 0.5cm
                target_emu = 180000
                tolerance = 100000  # generous tolerance
                if abs(spacing - target_emu) <= tolerance:
                    print(f"PASS: Component 4 — Column spacing is {spacing} EMU (~{spacing/360000:.2f} cm), target ~0.5cm (0.2 pts)")
                    total_score += 0.2
                else:
                    # Still give partial credit if spacing exists and is reasonable
                    if 50000 <= spacing <= 1000000:
                        print(f"PARTIAL: Component 4 — Column spacing is {spacing} EMU (~{spacing/360000:.2f} cm), not ideal but present (0.1 pts)")
                        total_score += 0.1
                    else:
                        print(f"FAIL: Component 4 — Column spacing is {spacing} EMU, expected ~180000 EMU (0.5cm)")
            else:
                print(f"FAIL: Component 4 — No column spacing attribute found on 2-column section")
        else:
            print(f"FAIL: Component 4 — Cannot verify spacing (no 2-column section found)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
