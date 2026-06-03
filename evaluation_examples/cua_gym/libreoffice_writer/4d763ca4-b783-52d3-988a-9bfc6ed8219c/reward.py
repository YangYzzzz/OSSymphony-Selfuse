"""
Reward Script: Insert a section named 'Executive Summary' around the first two paragraphs
               with section protection (read-only) and a light blue background (#E3F2FD).
Task ID: writer_struct_047
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): A Structured Document Tag (w:sdt) section named "Executive Summary" exists
  Component 2 (0.30): The section has write protection (sdtContentLocked lock)
  Component 3 (0.30): Both paragraphs inside the section have background fill color #E3F2FD
"""

import os
import zipfile
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_047'
FILE_PATH = os.path.join(WORKDIR, 'investment_prospectus.docx')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    LibreOffice Writer sections created via Format > Sections are stored in DOCX as
    Structured Document Tags (w:sdt elements). We verify:
      1. A w:sdt with alias/tag "Executive Summary" exists
      2. The sdtPr contains a w:lock with w:val="sdtContentLocked" (write protection)
      3. Both paragraph-level properties inside sdtContent contain w:shd fill="E3F2FD"

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load raw document XML from the docx archive
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            doc_xml = z.read('word/document.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: w:sdt section named "Executive Summary" exists (0.40 points)
    # The section must have w:alias w:val="Executive Summary" inside its sdtPr
    try:
        # Find the sdtPr block and check for the alias
        alias_match = re.search(
            r'<w:alias\s+w:val="Executive Summary"',
            doc_xml,
            re.IGNORECASE
        )
        tag_match = re.search(
            r'<w:tag\s+w:val="Executive Summary"',
            doc_xml,
            re.IGNORECASE
        )
        # Accept either alias or tag with "Executive Summary" (LO may use either)
        has_sdt = 'w:sdt' in doc_xml
        has_exec_summary_name = (alias_match is not None) or (tag_match is not None)

        if has_sdt and has_exec_summary_name:
            print(f"PASS: Component 1 — w:sdt section named 'Executive Summary' found (0.40 pts)")
            total_score += 0.40
        else:
            if not has_sdt:
                print(f"FAIL: Component 1 — No w:sdt element found in document")
            else:
                print(f"FAIL: Component 1 — w:sdt found but no alias/tag 'Executive Summary'; "
                      f"alias_match={alias_match is not None}, tag_match={tag_match is not None}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Section has write protection (sdtContentLocked) (0.30 points)
    # The sdtPr must contain <w:lock w:val="sdtContentLocked"/>
    try:
        lock_match = re.search(
            r'<w:lock\s+w:val="sdtContentLocked"',
            doc_xml
        )
        if lock_match:
            print(f"PASS: Component 2 — Section write protection (sdtContentLocked) found (0.30 pts)")
            total_score += 0.30
        else:
            # Check for any lock element to report what's present
            any_lock = re.findall(r'<w:lock[^>]*/>', doc_xml)
            print(f"FAIL: Component 2 — sdtContentLocked lock not found; "
                  f"existing lock elements: {any_lock}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Both paragraphs in the section have #E3F2FD background (0.30 points)
    # Each paragraph's pPr should contain w:shd with w:fill="E3F2FD"
    try:
        # Extract the sdtContent block to limit search scope
        sdt_content_match = re.search(
            r'<w:sdtContent>(.*?)</w:sdtContent>',
            doc_xml,
            re.DOTALL
        )
        if sdt_content_match:
            sdt_content = sdt_content_match.group(1)
            # Count paragraphs with E3F2FD fill
            shd_fills = re.findall(
                r'w:fill="E3F2FD"',
                sdt_content,
                re.IGNORECASE
            )
            # We need at least 2 paragraphs with the correct background
            if len(shd_fills) >= 2:
                print(f"PASS: Component 3 — {len(shd_fills)} paragraphs with #E3F2FD background "
                      f"found inside section (0.30 pts)")
                total_score += 0.30
            elif len(shd_fills) == 1:
                print(f"FAIL: Component 3 — Only 1 of 2 paragraphs has #E3F2FD background; "
                      f"both paragraphs must have the light blue fill")
            else:
                # Check if any E3F2FD exists anywhere in doc
                all_fills = re.findall(r'w:fill="E3F2FD"', doc_xml, re.IGNORECASE)
                print(f"FAIL: Component 3 — No #E3F2FD fill found inside sdtContent; "
                      f"total E3F2FD in document: {len(all_fills)}")
        else:
            # sdtContent not found — but check entire doc for fills as fallback
            all_fills = re.findall(r'w:fill="E3F2FD"', doc_xml, re.IGNORECASE)
            if len(all_fills) >= 2:
                print(f"PARTIAL: Component 3 — {len(all_fills)} #E3F2FD fills found but no sdtContent block; "
                      f"cannot confirm they are inside the section")
            else:
                print(f"FAIL: Component 3 — No sdtContent block and no #E3F2FD fill found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
