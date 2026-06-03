"""
Reward Script: Set up different headers for each chapter section
Task ID: writer_rm_089
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.30): Section 0 header contains 'Introduction'
  - Component 2 (0.30): Section 1 header is unlinked AND contains 'Background'
  - Component 3 (0.30): Section 2 header is unlinked AND contains 'Methodology'
  - Component 4 (0.10): All three headers are distinct and non-empty (holistic check)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_089'


def persist_app_state(domain: str):
    """Try to save any unsaved LibreOffice state."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_header_text(section):
    """Extract combined header text from a section."""
    return ''.join(p.text for p in section.header.paragraphs).strip()


def verify_task(file_path):
    """
    Verify that each chapter section has a distinct header with the correct text.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document must have at least 3 sections
    sections = doc.sections
    if len(sections) < 3:
        print(f"FAIL: Document has {len(sections)} sections, need at least 3")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Section 0 (Chapter 1) header contains 'Introduction' (0.30 pts)
    # Initial state: header is empty. Task requires setting it to 'Introduction'.
    try:
        hdr0_text = get_header_text(sections[0])
        if 'Introduction' in hdr0_text:
            print(f"PASS: Component 1 -- Section 0 header contains 'Introduction' (found: '{hdr0_text}') (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- Section 0 header='{hdr0_text}'; expected to contain 'Introduction'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Section 1 (Chapter 2) header is unlinked AND contains 'Background' (0.30 pts)
    # Initial state: linked_to_previous=True, header empty. Task requires unlinking and setting 'Background'.
    try:
        sec1 = sections[1]
        hdr1_text = get_header_text(sec1)
        linked1 = sec1.header.is_linked_to_previous
        if 'Background' in hdr1_text and not linked1:
            print(f"PASS: Component 2 -- Section 1 header='{hdr1_text}', unlinked={not linked1} (0.30 pts)")
            total_score += 0.30
        elif 'Background' in hdr1_text:
            # Partial: text is right but still linked
            print(f"PARTIAL: Component 2 -- Section 1 has 'Background' but is still linked to previous (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Section 1 header='{hdr1_text}', linked={linked1}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Section 2 (Chapter 3) header is unlinked AND contains 'Methodology' (0.30 pts)
    # Initial state: linked_to_previous=True, header empty. Task requires unlinking and setting 'Methodology'.
    try:
        sec2 = sections[2]
        hdr2_text = get_header_text(sec2)
        linked2 = sec2.header.is_linked_to_previous
        if 'Methodology' in hdr2_text and not linked2:
            print(f"PASS: Component 3 -- Section 2 header='{hdr2_text}', unlinked={not linked2} (0.30 pts)")
            total_score += 0.30
        elif 'Methodology' in hdr2_text:
            print(f"PARTIAL: Component 3 -- Section 2 has 'Methodology' but is still linked to previous (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- Section 2 header='{hdr2_text}', linked={linked2}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: All three section headers are distinct and non-empty (0.10 pts)
    # This holistic check ensures headers are truly differentiated.
    # In initial state, all headers are empty so this will FAIL on initial.
    try:
        header_texts = [get_header_text(sections[i]) for i in range(3)]
        all_non_empty = all(len(h) > 0 for h in header_texts)
        all_distinct = len(set(header_texts)) == 3
        if all_non_empty and all_distinct:
            print(f"PASS: Component 4 -- All 3 headers distinct and non-empty: {header_texts} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 -- Headers not all distinct/non-empty: {header_texts}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state before verification
persist_app_state("libreoffice_writer")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
