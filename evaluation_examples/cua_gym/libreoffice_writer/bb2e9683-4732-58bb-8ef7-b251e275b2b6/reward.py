"""
Reward Script: Add a blank line after each item in the ordered list in the meeting minutes document
Task ID: osworld_writer_blank_line_insertion_004
Domain: libreoffice_writer
Scoring:
  Component 1: Blank lines between consecutive Action Items list entries (0.1 pts each × 6 = 0.6 pts)
               Counts blank paragraphs sandwiched between consecutive List Number items.
               Initial doc has 0 such blanks; golden doc has 6.
  Component 2: All 7 list items each have a blank paragraph immediately after them (0.4 pts)
               Binary check: did ALL 7 list items get a blank line added after them?
               Initial doc has only 1 (pre-existing trailing blank after last item); golden has 7.
  Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_blank_line_insertion_004'

# Number of Action Items items expected
EXPECTED_ITEM_COUNT = 7


def verify_task(file_path):
    """
    Verify that blank lines (empty paragraphs) were inserted after each
    Action Items list item.
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

    # Locate the Action Items heading
    action_items_idx = None
    for i, para in enumerate(paragraphs):
        if para.style.name.startswith('Heading') and 'Action Items' in para.text:
            action_items_idx = i
            break

    if action_items_idx is None:
        print("FAIL: Could not find 'Action Items' heading in document")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: Found 'Action Items' heading at paragraph index {action_items_idx}")

    # Collect all paragraphs under Action Items heading (stop at next Heading or end)
    section_paras = []
    i = action_items_idx + 1
    while i < len(paragraphs):
        para = paragraphs[i]
        if para.style.name.startswith('Heading'):
            break
        section_paras.append((i, para))
        i += 1

    print(f"INFO: Action Items section contains {len(section_paras)} paragraphs")

    # Component 1: Count inter-item blank lines
    # A blank paragraph is one with empty/whitespace text immediately between two List Number items.
    # In other words: section_paras[j] is List Number, section_paras[j+1] is blank,
    # section_paras[j+2] is List Number.
    # This counts blank lines inserted BETWEEN consecutive list items (not trailing).
    # Expected: 6 (between items 1-2, 2-3, 3-4, 4-5, 5-6, 6-7)
    # Initial doc: 0 such inter-item blanks → scores 0.0 for this component
    # Golden doc: 6 such inter-item blanks → scores 0.6 for this component
    inter_item_blanks = 0
    try:
        for j in range(len(section_paras) - 2):
            curr_para = section_paras[j][1]
            next_para = section_paras[j + 1][1]
            after_next_para = section_paras[j + 2][1]
            if (curr_para.style.name == 'List Number' and
                    next_para.text.strip() == '' and
                    after_next_para.style.name == 'List Number'):
                inter_item_blanks += 1

        if inter_item_blanks >= 6:
            points_c1 = 0.6
            print(f"PASS: Component 1 — All 6 inter-item blank lines present ({points_c1} pts)")
            total_score += points_c1
        elif inter_item_blanks > 0:
            points_c1 = round(min(inter_item_blanks, 6) * 0.1, 2)
            print(f"PARTIAL: Component 1 — {inter_item_blanks}/6 inter-item blank lines found ({points_c1} pts)")
            total_score += points_c1
        else:
            print(f"FAIL: Component 1 — No inter-item blank lines found (0.0 pts)")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ALL 7 list items each have a blank paragraph immediately after them (0.4 pts)
    # Counts how many List Number paragraphs in the section are immediately followed by a blank.
    # Initial: 1 (only the last item has a trailing blank) → does not reach 7 → scores 0.0
    # Golden: 7 (all items followed by blank) → scores 0.4
    try:
        list_item_indices = [
            j for j, (_, para) in enumerate(section_paras)
            if para.style.name == 'List Number'
        ]
        print(f"INFO: Found {len(list_item_indices)} List Number items in Action Items section")

        items_with_blank_after = 0
        for j in list_item_indices:
            # Check if the next paragraph in the section is blank
            if j + 1 < len(section_paras):
                next_para = section_paras[j + 1][1]
                if next_para.text.strip() == '':
                    items_with_blank_after += 1
            else:
                # The last item — check full document for next paragraph after section
                # (handled via the section which continues past the heading)
                pass

        print(f"INFO: {items_with_blank_after}/{len(list_item_indices)} list items have a blank paragraph immediately after them")

        if items_with_blank_after == EXPECTED_ITEM_COUNT:
            print(f"PASS: Component 2 — All {EXPECTED_ITEM_COUNT} list items have blank lines after them (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Only {items_with_blank_after}/{EXPECTED_ITEM_COUNT} list items have blank lines after them (0.0 pts)")

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
