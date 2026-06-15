"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m putting together a 40-page training manual, and I want each chapter title (the text tagged as Heading 1) to kick off on its own page automatically—no more hitting Ctrl + Enter over and over. In LibreOffice Writer, how do I adjust the Heading 1 paragraph style so it always inserts a page break right before the heading?
Generated: 2025-09-10 17:34:08
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
from lxml import etree

"""
Reward script for LibreOffice Writer task:
Verify that the Heading 1 paragraph style is configured to automatically
insert a page break before each Heading 1 paragraph.  
If this style-level setting is present the task is considered 100 % complete
and a reward of 1.0 is returned.  
If the style setting is missing, the script falls back to counting manual
page-breaks (\u000c or explicit <w:br w:type="page"/>) placed immediately before
Heading 1 paragraphs and awards proportional partial credit.

Scoring rules
-------------
1. Heading 1 style contains <w:pageBreakBefore/>  -> 1.0  (full credit)
2. Otherwise:  manual page breaks before headings -> (#withBreak / #headings)
   (progressive score from 0.0-<1.0 depending on how many headings have
    an explicit preceding page break.)

The script prints diagnostic information and the final reward in the format
"REWARD: X.X" as required.
"""

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def _load_xml(docx_path: str, internal_path: str):
    """Extract and parse a specific XML part from the DOCX file."""
    with zipfile.ZipFile(docx_path, "r") as z:
        xml_bytes = z.read(internal_path)
    return etree.fromstring(xml_bytes)

def _heading1_style_has_page_break(styles_root) -> bool:
    """Return True if Heading 1 style has the <w:pageBreakBefore/> element."""
    for style in styles_root.findall('.//w:style[@w:type="paragraph"]', NS):
        style_id = style.get(f'{{{NS["w"]}}}styleId', '').lower()
        name_el = style.find('w:name', NS)
        name_val = name_el.get(f'{{{NS["w"]}}}val', '').lower() if name_el is not None else ''

        if style_id == 'heading1' or name_val == 'heading 1':
            ppr = style.find('w:pPr', NS)
            if ppr is not None and ppr.find('w:pageBreakBefore', NS) is not None:
                return True
    return False

def _count_headings_with_manual_break(doc_root):
    """Count Heading 1 paragraphs and how many are preceded by manual page breaks."""
    paragraphs = doc_root.findall('.//w:body/w:p', NS)
    total_headings = 0
    headings_with_break = 0

    for idx, p in enumerate(paragraphs):
        ppr = p.find('w:pPr', NS)
        if ppr is None:
            continue

        pstyle = ppr.find('w:pStyle', NS)
        if pstyle is None or pstyle.get(f'{{{NS["w"]}}}val', '').lower() != 'heading1':
            continue  # not a Heading 1 paragraph

        total_headings += 1
        manual_break = False

        # Case 1: a page-break <w:br w:type="page"/> inside the same paragraph (before text)
        for br in p.findall('.//w:br', NS):
            if br.get(f'{{{NS["w"]}}}type') == 'page':
                manual_break = True
                break

        # Case 2: a page-break inside the immediately preceding paragraph
        if not manual_break and idx > 0:
            prev_p = paragraphs[idx - 1]
            for br in prev_p.findall('.//w:br', NS):
                if br.get(f'{{{NS["w"]}}}type') == 'page':
                    manual_break = True
                    break

        if manual_break:
            headings_with_break += 1

    return total_headings, headings_with_break

def verify_task(docx_path: str) -> float:
    """Main verification routine. Returns progressive score between 0.0 and 1.0."""
    if not os.path.exists(docx_path):
        print(f"✗ File not found: {docx_path}")
        return 0.0

    try:
        # 1) Check the Heading 1 style definition in styles.xml
        styles_root = _load_xml(docx_path, 'word/styles.xml')
        style_has_break = _heading1_style_has_page_break(styles_root)

        if style_has_break:
            print("✓ Heading 1 style has pageBreakBefore set – full credit")
            print("REWARD: 1.0")
            return 1.0

        # 2) Fallback – evaluate manual page breaks before Heading 1 paragraphs
        print("✗ Heading 1 style missing pageBreakBefore – analysing manual breaks …")
        doc_root = _load_xml(docx_path, 'word/document.xml')
        total, with_break = _count_headings_with_manual_break(doc_root)
        print(f"Found {total} Heading 1 paragraphs; {with_break} preceded by manual page break")

        if total == 0:
            print("✗ No Heading 1 paragraphs found – score 0.0")
            score = 0.0
        else:
            score = with_break / total  # proportional credit
            print(f"✓ Manual-break coverage: {with_break}/{total} → score {score:.2f}")

        final_score = round(min(score, 1.0), 2)
        print(f"REWARD: {final_score}")
        return final_score

    except Exception as exc:
        print(f"✗ Error during verification: {exc}")
        return 0.0

# ---------------------------------------------------------------------------
# Execute verification when run as a script
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    DOCX_PATH = (
        '/home/user/'
        'im_putting_together_a_40_page_training_manual_and_i_want_each_chapter_title_the_text_tagged_as_headi.docx'
    )
    verify_task(DOCX_PATH)

