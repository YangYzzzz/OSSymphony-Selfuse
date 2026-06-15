"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve got a two-page introduction finished, and I want the next chapter to kick off on a fresh sheet. In LibreOffice Writer, what’s the quickest way to force a manual page break immediately after page 2 so the new section starts on page 3?
Generated: 2025-09-10 20:42:31
Status: success
Model: azure-o3
Total Steps: 7
"""

import os
import re
import zipfile
from lxml import etree


def _get_para_text(para, ns):
    """Return the concatenated text of a paragraph element."""
    texts = para.xpath('.//w:t', namespaces=ns)
    return ''.join([(t.text or '') for t in texts]).strip()


def _find_page_break_indices(paragraphs, ns):
    """Return a list of paragraph indices that contain a manual page-break element."""
    return [idx for idx, p in enumerate(paragraphs)
            if p.xpath('.//w:br[@w:type="page"]', namespaces=ns)]


def _find_chapter_index(paragraphs, ns):
    """Locate the first paragraph whose visible text begins with the word ‘Chapter’."""
    for idx, p in enumerate(paragraphs):
        text = _get_para_text(p, ns)
        if re.match(r'chapter\s+\d+', text, flags=re.IGNORECASE):
            return idx, text
    return None, None


def verify_manual_page_break_new_chapter(file_path):
    """Verify that a manual page break forces the next chapter to start on a new page.

    Scoring (progressive):
        +0.3  – at least one manual page break exists in the document
        +0.4  – a paragraph starting with the word “Chapter” is found (first chapter)
        +0.3  – the closest page break before that chapter is immediately followed by
                 only empty paragraphs (i.e., the chapter really starts right after
                 the break with no extra content in between)
        Maximum = 1.0
    """

    max_score = 1.0
    score = 0.0

    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    # --------------------------------------------------
    # 1. Load document.xml from the DOCX package
    # --------------------------------------------------
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            doc_xml = z.read('word/document.xml')
    except Exception as exc:
        print(f"✗ Unable to open DOCX or read document.xml: {exc}")
        return 0.0

    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        root = etree.fromstring(doc_xml)
    except Exception as exc:
        print(f"✗ Failed to parse document XML: {exc}")
        return 0.0

    paragraphs = root.xpath('//w:body/w:p', namespaces=ns)
    print(f"Total paragraphs detected: {len(paragraphs)}")

    # --------------------------------------------------
    # 2. Detect manual page breaks
    # --------------------------------------------------
    pb_indices = _find_page_break_indices(paragraphs, ns)
    if pb_indices:
        print(f"✓ Manual page breaks found at indices: {pb_indices} (0.3 points)")
        score += 0.3
    else:
        print("✗ No manual page breaks detected – cannot satisfy requirement")
        return score  # early exit – nothing more to check

    # --------------------------------------------------
    # 3. Locate the first chapter heading
    # --------------------------------------------------
    chapter_idx, chapter_text = _find_chapter_index(paragraphs, ns)
    if chapter_idx is not None:
        print(f"✓ Chapter heading detected at paragraph {chapter_idx}: '{chapter_text}' (0.4 points)")
        score += 0.4
    else:
        print("✗ No chapter heading beginning with the word 'Chapter' found")
        return score  # cannot continue without a chapter heading

    # --------------------------------------------------
    # 4. Ensure the chapter starts immediately after a page break
    # --------------------------------------------------
    pb_before_chapter = [idx for idx in pb_indices if idx < chapter_idx]
    if not pb_before_chapter:
        print("✗ No page break appears before the chapter heading – chapter does not start on new page")
        return score

    last_pb_idx = max(pb_before_chapter)
    intervening_paras = paragraphs[last_pb_idx + 1: chapter_idx]
    if all(_get_para_text(p, ns) == '' for p in intervening_paras):
        print("✓ Chapter heading follows immediately after a manual page break (0.3 points)")
        score += 0.3
    else:
        print("✗ Content exists between the last page break and the chapter heading – not an immediate start")

    final_score = min(score, max_score)
    print(f"Total score: {final_score}")
    return final_score


if __name__ == "__main__":
    # Path to the golden answer file provided in the VM
    FILE_PATH = "/home/user/ive_got_a_two_page_introduction_finished_and_i_want_the_next_chapter_to_kick_off_on_a_fresh_sheet_in.docx"

    reward = verify_manual_page_break_new_chapter(FILE_PATH)
    print(f"REWARD: {reward}")
