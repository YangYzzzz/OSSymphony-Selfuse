"""
FINAL REWARD SCRIPT - SUCCESS
Task: Right before paragraph 3 I need to pop in a small table—exactly 3 columns by 4 rows, with the top row set as a header. How do I drop that in using LibreOffice Writer?
Generated: 2025-09-10 16:49:10
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import glob
from docx import Document
from docx.oxml.ns import qn

"""
Reward Script for LibreOffice Writer Task:

Task Recap:
  "Right before paragraph 3 I need to pop in a small table—exactly 3 columns by 4 rows, with the top row set as a header."

This script verifies, with progressive scoring, that the user inserted:
 1. A table positioned between paragraph 2 and paragraph 3 (i.e., immediately *before* paragraph 3)
 2. The table has exactly 4 rows × 3 columns
 3. The first row is flagged as a header row

Scoring:
  • 0.4 – Table correctly positioned before the 3rd paragraph
  • 0.3 – Table dimensions exactly 4 × 3
  • 0.3 – First row is marked as a header row
Total possible: 1.0
"""

def _row_is_header(row):
    """Return True if the given python-docx row element is marked as a header row"""
    trPr = row._tr.trPr
    if trPr is None:
        return False
    hdr = trPr.find(qn('w:tblHeader'))
    if hdr is None:
        return False
    val = hdr.get(qn('w:val'))
    return val in (None, '1', 'true', 'True')


def _locate_target_docx():
    """Find the DOCX file in /home/user that matches task keywords"""
    patterns = [
        '/home/user/**/*.docx',
        '/home/user/*.docx',
    ]
    files = []
    for pat in patterns:
        files.extend(glob.glob(pat, recursive=True))
    if not files:
        return None
    # Prefer filenames containing key phrases
    keywords = ['paragraph_3', 'small_table', 'table']
    for f in files:
        name = os.path.basename(f).lower()
        if any(k in name for k in keywords):
            return f
    return files[0]  # fall back to first found


def verify_writer_table_task(file_path: str) -> float:
    """Verify task completion and return progressive score (0.0-1.0)"""

    max_score = 1.0
    score = 0.0
    print(f"Checking document: {file_path}")

    # ---------- Load document ----------
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Failed to load DOCX: {e}")
        return 0.0  # Cannot proceed

    # ---------- Locate the table BEFORE paragraph 3 ----------
    body = doc.element.body
    para_counter = 0  # counts paragraphs encountered so far
    tbl_element_between_p2_p3 = None

    for child in body.iterchildren():
        # child.tag ends with ...}p for paragraph, ...}tbl for table
        if child.tag.endswith('}p'):
            para_counter += 1
            if para_counter == 3:
                # We have reached paragraph 3; stop scanning further
                break
        elif child.tag.endswith('}tbl'):
            # Table found. If we are *after* paragraph 2 (i.e., para_counter == 2)
            if para_counter == 2 and tbl_element_between_p2_p3 is None:
                tbl_element_between_p2_p3 = child

    if tbl_element_between_p2_p3 is None:
        print("✗ No table found right before paragraph 3")
    else:
        print("✓ Table correctly positioned before paragraph 3 (0.4 points)")
        score += 0.4

    # ---------- Map located element to python-docx Table object ----------
    target_table = None
    if tbl_element_between_p2_p3 is not None:
        for tbl in doc.tables:
            if tbl._tbl is tbl_element_between_p2_p3:
                target_table = tbl
                break
        if target_table is None:
            print("✗ Located XML table could not be matched to a python-docx Table object")

    # ---------- Verify rows/columns ----------
    if target_table is not None:
        row_count = len(target_table.rows)
        col_count = len(target_table.columns)
        if row_count == 4 and col_count == 3:
            print("✓ Table dimensions 4×3 verified (0.3 points)")
            score += 0.3
        else:
            print(f"✗ Incorrect table size. Found {row_count}×{col_count}, expected 4×3")

        # ---------- Verify header row ----------
        try:
            if _row_is_header(target_table.rows[0]):
                print("✓ First row marked as header (0.3 points)")
                score += 0.3
            else:
                print("✗ First row is NOT marked as a header row")
        except Exception as e:
            print(f"✗ Error while checking header row: {e}")

    final_score = min(score, max_score)
    print(f"Total score: {final_score}")
    return final_score


# --------------------- MAIN EXECUTION ---------------------
if __name__ == "__main__":
    path = _locate_target_docx()
    if path is None:
        print("No DOCX file found to verify in /home/user")
        reward_value = 0.0
    else:
        reward_value = verify_writer_table_task(path)
    print(f"REWARD: {reward_value}")

