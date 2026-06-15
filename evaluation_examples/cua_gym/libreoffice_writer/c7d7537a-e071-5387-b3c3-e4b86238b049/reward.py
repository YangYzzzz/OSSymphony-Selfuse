"""
FINAL REWARD SCRIPT - SUCCESS
Task: Every time I tweak the layout, my introduction on page 3 jumps up to page 2. How can I lock in a completely blank page right after page 2 so the rest of the document starts on page 3 in LibreOffice Writer?
Generated: 2025-09-10 14:22:13
Status: success
Model: azure-o3
Total Steps: 8
"""

import os
import zipfile
from docx import Document
from lxml import etree

"""
Reward Script
-------------
Verifies the LibreOffice Writer task:
"Lock a completely blank page right after page 2 so the rest of the document starts on page 3." 

Success Criteria (progressively scored):
1. An "Introduction" paragraph exists (0.3)
2. Page/section breaks BEFORE the Introduction:
   • ≥1 break (0.2)
   • ≥2 breaks (adds 0.3 more) – ensuring the blank page (page 2) (total 0.5)
3. Evidence of a title/cover page text before those breaks (heuristic: contains the phrase "title page") (0.2)

Perfect task completion = 1.0
The script parses the DOCX XML to count explicit page/section breaks and checks pre-Introduction text content.
"""

TARGET_FILE = "/home/user/every_time_i_tweak_the_layout_my_introduction_on_page_3_jumps_up_to_page_2_how_can_i_lock_in_a_compl.docx"

# -----------------------------------------------------------------------------
# Helper: count breaks & gather text before the Introduction paragraph
# -----------------------------------------------------------------------------

def _analyze_before_intro(file_path):
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(file_path) as z:
        root = etree.fromstring(z.read("word/document.xml"))

    break_count = 0
    texts_before_intro = []

    for p in root.xpath("//w:p", namespaces=ns):
        # full paragraph text
        p_text = "".join(t.text for t in p.xpath(".//w:t", namespaces=ns) if t.text).strip()

        # Stop once we reach the Introduction paragraph
        if p_text.lower().startswith("introduction"):
            break

        if p_text:
            texts_before_intro.append(p_text)

        # count <w:br w:type="page"/>
        break_count += len(p.xpath(".//w:br[@w:type='page']", namespaces=ns))

        # count section breaks <w:sectPr>/<w:type w:val="nextPage"/>
        for sect in p.xpath(".//w:sectPr", namespaces=ns):
            type_el = sect.find(".//w:type", namespaces=ns)
            if type_el is not None and type_el.get(f"{{{ns['w']}}}val") == "nextPage":
                break_count += 1

    return break_count, texts_before_intro

# -----------------------------------------------------------------------------
# Main verification function
# -----------------------------------------------------------------------------

def verify_task(file_path):
    print(f"--- Verifying task for file: {file_path} ---")
    score = 0.0

    # prerequisite: file exists & loads (no points)
    if not os.path.exists(file_path):
        print("✗ File not found")
        print("REWARD: 0.0")
        return 0.0
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Cannot load DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Requirement 1: Introduction paragraph present --------------------------
    intro_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().lower().startswith("introduction"):
            intro_idx = i
            break

    if intro_idx is not None:
        print(f"✓ Introduction paragraph found (index {intro_idx}) (0.3)")
        score += 0.3
    else:
        print("✗ No Introduction paragraph found")

    # Requirement 2: Count breaks before Introduction ------------------------
    break_count, pre_intro_texts = _analyze_before_intro(file_path)
    print(f"Found {break_count} explicit page/section break(s) before Introduction")

    if break_count >= 1:
        print("✓ ≥1 break separating pages (0.2)")
        score += 0.2
    if break_count >= 2:
        print("✓ ≥2 breaks -> blank page ensured (additional 0.3)")
        score += 0.3
    else:
        print("✗ Fewer than 2 breaks; blank page not ensured")

    # Requirement 3: Detect title/cover page text ----------------------------
    has_title_page_text = any("title page" in t.lower() for t in pre_intro_texts)
    if has_title_page_text:
        print("✓ Detected 'Title Page' text before breaks (0.2)")
        score += 0.2
    else:
        print("✗ No explicit 'Title Page' text found before Introduction")

    # ---------------------------------------------------------------------
    final_score = round(min(score, 1.0), 2)
    print(f"Total Score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task(TARGET_FILE)
