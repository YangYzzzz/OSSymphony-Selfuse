"""
Reward Script: Insert a blank line after each paragraph in the 'Terms and Conditions' section
Task ID: osworld_writer_blank_line_insertion_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Blank paragraphs inserted between consecutive T&C content paragraphs (4.1-4.4),
                     i.e., the 4 NEW blank lines that were NOT present in the initial document.
  Component 2 (0.4): The full T&C section has ALL 5 content paragraphs each followed by a blank,
                     confirming the complete alternating pattern including after 4.5.

Initial state: T&C section has 5 content paragraphs (4.1-4.5) with no blank lines between them.
Golden state:  Each of the 5 T&C content paragraphs is followed by a blank (empty) paragraph.
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_blank_line_insertion_003'

# Known content prefixes for the 5 Terms and Conditions paragraphs
TC_PARA_PREFIXES = [
    '4.1 Confidentiality.',
    '4.2 Intellectual Property.',
    '4.3 Limitation of Liability.',
    '4.4 Dispute Resolution.',
    '4.5 Governing Law.',
]


def find_tc_section_start(paragraphs):
    """Find the index of the '4. TERMS AND CONDITIONS' heading."""
    for i, para in enumerate(paragraphs):
        text = para.text.strip()
        if '4.' in text and 'TERMS AND CONDITIONS' in text.upper():
            return i
    return -1


def find_tc_section_end(paragraphs, start_idx):
    """Find the index just past the last paragraph in the T&C section (before section 5 or SIGNATURES)."""
    for i in range(start_idx + 1, len(paragraphs)):
        text = paragraphs[i].text.strip()
        # Stop at section 5 heading or SIGNATURES
        if text.startswith('5.') or text == 'SIGNATURES':
            return i
    return len(paragraphs)


def verify_task(file_path):
    """
    Verify task completion: blank line inserted after each paragraph in the T&C section.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document — precondition gate (not scored)
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    total_paras = len(paragraphs)
    print(f"INFO: Document has {total_paras} paragraphs total")

    # Locate the Terms and Conditions section — precondition gate (not scored)
    tc_start = find_tc_section_start(paragraphs)
    if tc_start == -1:
        print("CRITICAL: '4. TERMS AND CONDITIONS' heading not found in document")
        print("REWARD: 0.0")
        return 0.0

    tc_end = find_tc_section_end(paragraphs, tc_start)
    tc_section = paragraphs[tc_start:tc_end]
    print(f"INFO: T&C section spans paragraph indices {tc_start} to {tc_end - 1} "
          f"(total {len(tc_section)} paragraphs)")
    for i, p in enumerate(tc_section):
        preview = p.text[:80] if p.text else '[EMPTY]'
        print(f"  TC para {i}: {preview!r}")

    # Verify all 5 T&C content paragraphs exist — precondition gate (not scored)
    tc_texts = [p.text.strip() for p in tc_section]
    found_prefixes = [prefix for prefix in TC_PARA_PREFIXES
                      if any(t.startswith(prefix) for t in tc_texts)]
    if len(found_prefixes) < 5:
        print(f"WARN: Only {len(found_prefixes)}/5 T&C content paragraphs found. "
              f"Missing: {[p for p in TC_PARA_PREFIXES if p not in found_prefixes]}")

    # Component 1: Blank paragraphs inserted BETWEEN consecutive T&C content paragraphs (0.6 points)
    # Specifically checks that 4.1, 4.2, 4.3, 4.4 each have a blank paragraph immediately after them
    # and BEFORE the next T&C content paragraph.
    # In the INITIAL document, these blank lines DO NOT EXIST (4.1-4.4 are consecutive with no blanks).
    # In the GOLDEN document, these blank lines ARE INSERTED.
    try:
        # For each of the first 4 T&C paragraphs (4.1-4.4), verify that the paragraph immediately
        # after it within the T&C section is blank (empty).
        inter_blank_count = 0
        inter_checked = 0

        for idx in range(len(tc_section) - 1):
            text = tc_section[idx].text.strip()
            # Check if this is one of 4.1-4.4 (not 4.5)
            is_tc_content_not_last = any(text.startswith(prefix)
                                          for prefix in TC_PARA_PREFIXES[:4])
            if is_tc_content_not_last:
                inter_checked += 1
                next_text = tc_section[idx + 1].text.strip()
                if next_text == '':
                    inter_blank_count += 1
                    print(f"PASS: Blank line found after paragraph starting with {text[:50]!r}")
                else:
                    print(f"FAIL: No blank line after {text[:50]!r}; "
                          f"next paragraph is {next_text[:50]!r}")

        print(f"INFO: Found blank lines after {inter_blank_count}/{inter_checked} "
              f"inter-paragraph positions (4.1-4.4)")

        if inter_blank_count == 4:
            print(f"PASS: Component 1 — blank paragraph after all 4 inter-T&C positions (0.6 pts)")
            total_score += 0.6
        elif inter_blank_count > 0:
            partial_c1 = round(0.6 * inter_blank_count / 4, 2)
            print(f"PARTIAL: Component 1 — {inter_blank_count}/4 inter-paragraph blanks found, score {partial_c1}")
            total_score += partial_c1
        else:
            print(f"FAIL: Component 1 — no blank lines found between T&C paragraphs")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 T&C content paragraphs have a blank paragraph immediately after them (0.4 points)
    # This is a superset of Component 1 — it also checks the blank after 4.5.
    # In INITIAL: the blank after 4.5 exists (paragraph 21), but blanks after 4.1-4.4 do NOT.
    # In GOLDEN: ALL 5 T&C paragraphs are followed by blank paragraphs.
    # This component FAILS on initial because, while 4.5 has a trailing blank, the overall
    # alternating pattern (all 5 followed by blanks) is NOT present in the initial document.
    try:
        # Check the FULL alternating pattern: the T&C section should have exactly the pattern:
        # [heading, 4.1-content, blank, 4.2-content, blank, 4.3-content, blank,
        #  4.4-content, blank, 4.5-content, blank]
        # which means the section should have length 11 with alternating content/blank.

        # Find indices of all 5 T&C content paragraphs within tc_section
        tc_content_indices = []
        for idx, para in enumerate(tc_section):
            text = para.text.strip()
            if any(text.startswith(prefix) for prefix in TC_PARA_PREFIXES):
                tc_content_indices.append(idx)

        blank_after_all_count = 0

        for content_idx in tc_content_indices:
            content_text = tc_section[content_idx].text.strip()
            # Check if there is a blank paragraph immediately after within tc_section
            next_in_section = content_idx + 1
            if next_in_section < len(tc_section):
                next_text = tc_section[next_in_section].text.strip()
                if next_text == '':
                    blank_after_all_count += 1
                else:
                    print(f"FAIL (C2): No blank after {content_text[:50]!r} "
                          f"in section; next is {next_text[:50]!r}")
            else:
                # Last item in the section — check next paragraph in full document
                abs_next = tc_start + content_idx + 1
                if abs_next < len(paragraphs) and paragraphs[abs_next].text.strip() == '':
                    blank_after_all_count += 1
                else:
                    print(f"FAIL (C2): No blank after final T&C paragraph {content_text[:50]!r}")

        print(f"INFO: Blank after count for all T&C paragraphs: {blank_after_all_count}/5")

        # Binary scoring: only award when ALL 5 T&C paragraphs have blank after them.
        # Reason: The blank after 4.5 already existed in the initial document as a section
        # separator; partial credit here would reward a precondition, not a task change.
        # The full 0.4 is only earned when the complete task is done (all 5 blanks present).
        if blank_after_all_count == 5:
            print(f"PASS: Component 2 — all 5 T&C paragraphs followed by blank (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — only {blank_after_all_count}/5 T&C paragraphs have blank "
                  f"paragraphs after them (0 pts; requires all 5)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {round(total_score, 4)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
