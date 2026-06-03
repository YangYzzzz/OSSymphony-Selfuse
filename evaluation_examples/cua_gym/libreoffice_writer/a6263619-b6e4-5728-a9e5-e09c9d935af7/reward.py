"""
Reward Script: Insert TOC and Table of Figures into Masters_Thesis.docx
Task ID: writer_mt_092
Domain: libreoffice_writer
Scoring:
  Component 1: TOC title present (0.15)
  Component 2: TOC field code present (0.20)
  Component 3: TOC has chapter entries (0.20)
  Component 4: TOF title present (0.15)
  Component 5: TOF field code present (0.15)
  Component 6: TOF has figure entries (0.15)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_092'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def persist_app_state(domain):
    """Save any unsaved changes via Ctrl+S."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


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

    # Gather all paragraph texts for analysis
    all_texts = [(i, p.text.strip(), p.style.name if p.style else 'None') for i, p in enumerate(doc.paragraphs)]

    # Gather all instrText field codes from the XML body
    body = doc.element.body
    instr_texts = [it.text for it in body.findall('.//w:instrText', NS) if it.text]

    # ---------------------------------------------------------------
    # Component 1: TOC title "Table of Contents" present (0.15 pts)
    # This is NOT present in initial (initial has "[This page reserved for Table of Contents]")
    # ---------------------------------------------------------------
    try:
        toc_title_found = False
        for idx, text, style in all_texts:
            if text == 'Table of Contents':
                toc_title_found = True
                break
        if toc_title_found:
            print(f"PASS: Component 1 — 'Table of Contents' title found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — 'Table of Contents' title not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ---------------------------------------------------------------
    # Component 2: TOC field code present in document XML (0.20 pts)
    # Initial has 0 instrText elements; golden has TOC field codes
    # ---------------------------------------------------------------
    try:
        toc_field_found = False
        for it_text in instr_texts:
            # TOC field for headings uses \o switch
            if 'TOC' in it_text and '\\o' in it_text:
                toc_field_found = True
                break
        if toc_field_found:
            print(f"PASS: Component 2 — TOC field code with \\o switch found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — No TOC field code with \\o switch found. instrTexts: {instr_texts}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: TOC has chapter entries - at least 5 of 7 chapters (0.20 pts)
    # Initial has no TOC entries; golden has 32 entries for H1+H2
    # We look for "Chapter X:" pattern in paragraphs after TOC title
    # ---------------------------------------------------------------
    try:
        toc_chapter_count = 0
        in_toc_section = False
        for idx, text, style in all_texts:
            if text == 'Table of Contents':
                in_toc_section = True
                continue
            if in_toc_section and style in ('Heading 1', 'Heading 2'):
                # We've left the TOC area and entered the body
                in_toc_section = False
                break
            if in_toc_section and text.startswith('Chapter '):
                toc_chapter_count += 1

        if toc_chapter_count >= 5:
            print(f"PASS: Component 3 — Found {toc_chapter_count} chapter entries in TOC (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Found only {toc_chapter_count} chapter entries in TOC, expected >= 5")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: "Table of Figures" title present (0.15 pts)
    # Initial has "[This page reserved for Table of Figures]" only
    # ---------------------------------------------------------------
    try:
        tof_title_found = False
        for idx, text, style in all_texts:
            if text == 'Table of Figures':
                tof_title_found = True
                break
        if tof_title_found:
            print(f"PASS: Component 4 — 'Table of Figures' title found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — 'Table of Figures' title not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ---------------------------------------------------------------
    # Component 5: TOF field code present (0.15 pts)
    # Initial has 0 field codes; golden has TOC \c "Figure"
    # ---------------------------------------------------------------
    try:
        tof_field_found = False
        for it_text in instr_texts:
            # Table of Figures uses TOC with \c "Figure" switch
            if 'TOC' in it_text and 'Figure' in it_text:
                tof_field_found = True
                break
        if tof_field_found:
            print(f"PASS: Component 5 — TOF field code (TOC \\c \"Figure\") found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — No TOF field code found. instrTexts: {instr_texts}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ---------------------------------------------------------------
    # Component 6: TOF has figure entries - at least 7 of 10 figures (0.15 pts)
    # Initial has no TOF entries; golden lists 10 figure captions
    # ---------------------------------------------------------------
    try:
        tof_figure_count = 0
        in_tof_section = False
        for idx, text, style in all_texts:
            if text == 'Table of Figures':
                in_tof_section = True
                continue
            if in_tof_section and style in ('Heading 1', 'Heading 2'):
                in_tof_section = False
                break
            if in_tof_section and text.startswith('Figure '):
                tof_figure_count += 1

        if tof_figure_count >= 7:
            print(f"PASS: Component 6 — Found {tof_figure_count} figure entries in TOF (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Found only {tof_figure_count} figure entries in TOF, expected >= 7")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
persist_app_state('libreoffice_writer')

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
