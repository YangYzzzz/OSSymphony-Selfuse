"""
Reward Script: Insert separator pages with centered chapter titles in master document
Task ID: writer_rm_090
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All 5 separator titles exist as centered paragraphs before their chapter headings
  Component 2 (0.3): Document has significantly more sections (separator pages are on new pages)
  Component 3 (0.3): Separator page regions are blank except for the centered title
"""

import os
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_090'

# The 5 expected chapter titles (short form on separator pages)
EXPECTED_SEPARATORS = [
    'The Beginning',
    'Rising Action',
    'The Climax',
    'Falling Action',
    'Resolution',
]

# Corresponding full heading text
EXPECTED_HEADINGS = [
    'Chapter 1: The Beginning',
    'Chapter 2: Rising Action',
    'Chapter 3: The Climax',
    'Chapter 4: Falling Action',
    'Chapter 5: Resolution',
]


def persist_app_state(domain):
    """Attempt to save any unsaved LibreOffice state."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
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

    paragraphs = doc.paragraphs

    # Build index: for each paragraph, record text, style, alignment
    para_info = []
    for p in paragraphs:
        para_info.append({
            'text': p.text.strip(),
            'style': p.style.name if p.style else None,
            'alignment': p.paragraph_format.alignment,
        })

    # Find positions of Heading 1 paragraphs (chapter headings)
    heading_positions = {}
    for i, info in enumerate(para_info):
        if info['style'] == 'Heading 1':
            heading_positions[info['text']] = i

    # Component 1: All 5 separator titles exist as centered paragraphs BEFORE their chapter headings (0.4 pts)
    # Each separator title is worth 0.08 pts
    try:
        separator_found_count = 0
        separator_positions = {}

        for sep_idx, (sep_title, heading_text) in enumerate(zip(EXPECTED_SEPARATORS, EXPECTED_HEADINGS)):
            heading_pos = heading_positions.get(heading_text)
            if heading_pos is None:
                print(f"FAIL: Component 1.{sep_idx+1} — Chapter heading '{heading_text}' not found")
                continue

            # Look for the separator title BEFORE the heading position
            found = False
            for i in range(heading_pos):
                if para_info[i]['text'] == sep_title:
                    # Check it's centered
                    is_centered = (para_info[i]['alignment'] == WD_PARAGRAPH_ALIGNMENT.CENTER)
                    if is_centered:
                        separator_found_count += 1
                        separator_positions[sep_title] = i
                        found = True
                        print(f"PASS: Component 1.{sep_idx+1} — Separator '{sep_title}' found at para {i}, centered, before heading at para {heading_pos}")
                        break
                    else:
                        print(f"FAIL: Component 1.{sep_idx+1} — Separator '{sep_title}' found at para {i} but NOT centered (align={para_info[i]['alignment']})")
                        found = True
                        break

            if not found:
                print(f"FAIL: Component 1.{sep_idx+1} — Separator title '{sep_title}' not found before heading '{heading_text}'")

        comp1_score = (separator_found_count / 5) * 0.4
        total_score += comp1_score
        print(f"Component 1 subtotal: {separator_found_count}/5 separators found and centered ({comp1_score:.2f} pts)")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Document has more sections than initial (separator pages on new pages) (0.3 pts)
    # Initial has 2 sections. Golden has 11. We expect at least 7 (original 2 + 5 separator breaks).
    try:
        num_sections = len(doc.sections)
        # The initial document has 2 sections. Adding 5 separator pages should add at least 5 more sections.
        # We give partial credit: 0.06 per additional section beyond 2, up to 5 additional.
        additional_sections = max(0, num_sections - 2)
        if additional_sections >= 5:
            comp2_score = 0.3
            print(f"PASS: Component 2 — {num_sections} sections (>= 7 required), {additional_sections} added ({comp2_score} pts)")
        elif additional_sections > 0:
            comp2_score = (additional_sections / 5) * 0.3
            print(f"PARTIAL: Component 2 — {num_sections} sections, only {additional_sections} additional (expected 5+) ({comp2_score:.2f} pts)")
        else:
            comp2_score = 0.0
            print(f"FAIL: Component 2 — Only {num_sections} sections, same as initial (no separator pages added)")
        total_score += comp2_score

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Separator page regions are blank except for the centered title (0.3 pts)
    # For each separator we found, check that the region between the previous content and
    # the heading is mostly empty paragraphs + the title. This ensures the separator is a
    # "blank page with only the chapter title".
    try:
        separator_blank_count = 0

        for sep_title in EXPECTED_SEPARATORS:
            if sep_title not in separator_positions:
                print(f"FAIL: Component 3 — Cannot check blanks for '{sep_title}' (separator not found)")
                continue

            sep_pos = separator_positions[sep_title]
            heading_text = EXPECTED_HEADINGS[EXPECTED_SEPARATORS.index(sep_title)]
            heading_pos = heading_positions.get(heading_text)

            if heading_pos is None:
                continue

            # The separator page region: from the paragraph after previous chapter's last content
            # to the paragraph before the heading. We look at the range [sep_pos-10, heading_pos)
            # and check that only the separator title has non-empty text.
            # Use a window: from max(0, sep_pos - 15) to heading_pos
            region_start = max(0, sep_pos - 15)
            region_end = heading_pos

            non_empty_in_region = []
            for j in range(region_start, region_end):
                txt = para_info[j]['text']
                if txt and txt != sep_title:
                    # Check if this is content from the previous chapter (before separator page break)
                    # We only care about paragraphs that are on the same page as the separator
                    # A simple heuristic: if it's close to the separator title, it shouldn't have text
                    # But content from previous chapter could be in this range
                    # So we check: between separator title and heading, nothing else
                    if j > sep_pos and j < region_end:
                        non_empty_in_region.append((j, txt[:40]))

            if not non_empty_in_region:
                separator_blank_count += 1
                print(f"PASS: Component 3 — Separator page for '{sep_title}' is blank except for title")
            else:
                print(f"FAIL: Component 3 — Separator page for '{sep_title}' has extra text between title and heading: {non_empty_in_region}")

        if len(separator_positions) > 0:
            comp3_score = (separator_blank_count / 5) * 0.3
        else:
            comp3_score = 0.0
        total_score += comp3_score
        print(f"Component 3 subtotal: {separator_blank_count}/5 separator pages are blank ({comp3_score:.2f} pts)")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
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
