"""
Reward Script: Update TOC to include 'Appendix: Supplementary Data'
Task ID: writer_struct_048
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): TOC contains an entry with text 'Appendix: Supplementary Data'
  Component 2 (0.3): Appendix TOC entry appears after '7. Safety and Adverse Events' entry
  Component 3 (0.2): Total TOC paragraph count is 8 (increased from 7)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_048'
FILE_PATH = f'{WORKDIR}/Desktop/clinical_trial.docx'


def verify_task(file_path):
    """
    Verify that the TOC was updated to include 'Appendix: Supplementary Data'
    as the 8th entry in the Table of Contents.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the TOC section by finding 'Table of Contents' label
    # Then collect TOC entries (paragraphs with tab-separated text/page number format)
    toc_start_idx = None
    paragraphs = list(doc.paragraphs)

    for i, para in enumerate(paragraphs):
        if 'Table of Contents' in para.text:
            toc_start_idx = i
            break

    if toc_start_idx is None:
        print("FAIL: Could not find 'Table of Contents' label in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found 'Table of Contents' at paragraph index {toc_start_idx}")

    # Collect TOC entries — paragraphs after 'Table of Contents' that contain
    # a tab character (format: "Title\tPageNum") or look like TOC entries
    toc_entries = []
    for para in paragraphs[toc_start_idx + 1:]:
        text = para.text.strip()
        # TOC entries contain a tab (title + page number)
        if '\t' in text and text:
            toc_entries.append(text)
        elif text == '':
            # Empty paragraph signals end of TOC block
            if len(toc_entries) > 0:
                break
        else:
            # Non-tab, non-empty: could be next section heading — stop
            break

    print(f"INFO: Found {len(toc_entries)} TOC entries:")
    for entry in toc_entries:
        print(f"  - {repr(entry)}")

    # Component 1: TOC contains an entry referencing 'Appendix: Supplementary Data' (0.5 pts)
    # This FAILS on initial (entry not there) and PASSES on golden (entry added)
    try:
        appendix_entries = [
            e for e in toc_entries
            if 'Appendix' in e.split('\t')[0] and 'Supplementary Data' in e.split('\t')[0]
        ]

        if len(appendix_entries) > 0:
            print(f"PASS: Component 1 — Appendix entry found in TOC: {repr(appendix_entries[0])} (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 — 'Appendix: Supplementary Data' entry NOT found in TOC")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Appendix TOC entry appears AFTER '7. Safety and Adverse Events' entry (0.3 pts)
    # Verifies correct ordering — appendix should be last
    try:
        safety_indices = [idx for idx, e in enumerate(toc_entries) if 'Safety and Adverse Events' in e.split('\t')[0]]
        appendix_indices = [idx for idx, e in enumerate(toc_entries) if 'Appendix' in e.split('\t')[0] and 'Supplementary Data' in e.split('\t')[0]]
        safety_idx = safety_indices[0] if safety_indices else None
        appendix_idx = appendix_indices[0] if appendix_indices else None

        if safety_idx is not None and appendix_idx is not None and appendix_idx > safety_idx:
            print(f"PASS: Component 2 — Appendix entry (index {appendix_idx}) correctly appears after "
                  f"'Safety and Adverse Events' entry (index {safety_idx}) (0.3 pts)")
            total_score += 0.3
        elif safety_idx is None:
            print("FAIL: Component 2 — '7. Safety and Adverse Events' entry not found in TOC")
        elif appendix_idx is None:
            print("FAIL: Component 2 — Appendix entry not present to check ordering")
        else:
            print(f"FAIL: Component 2 — Appendix entry (index {appendix_idx}) appears before "
                  f"'Safety and Adverse Events' entry (index {safety_idx})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Total TOC entry count is 8 (increased from original 7) (0.2 pts)
    # This verifies that no existing entries were removed and the new one was added
    try:
        expected_count = 8
        actual_count = len(toc_entries)
        if actual_count == expected_count:
            print(f"PASS: Component 3 — TOC has {actual_count} entries (expected {expected_count}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — TOC has {actual_count} entries, expected {expected_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
