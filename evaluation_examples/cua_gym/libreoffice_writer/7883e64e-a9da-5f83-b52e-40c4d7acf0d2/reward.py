"""
FINAL REWARD SCRIPT - SUCCESS
Task: Spell-check keeps flagging “colour” and “organise” in paragraph 2 because it’s still set to the US dictionary. In LibreOffice Writer, how can I switch JUST that paragraph to English (UK) so it stops throwing errors?
Generated: 2025-09-10 13:25:51
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
from lxml import etree

# -----------------------------------------------------------
# Helper: extract the language setting for each paragraph
# -----------------------------------------------------------

def extract_paragraph_languages(docx_path):
    """Return a list with the language code (e.g., 'en-US', 'en-GB')
    detected for each paragraph in the DOCX file. It checks paragraph
    formatting (pPr) first, and if not found, it falls back to run-level
    language definitions within the paragraph.
    """
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraph_langs = []

    # Read the main document XML from the DOCX package
    with zipfile.ZipFile(docx_path) as z:
        document_xml = z.read("word/document.xml")

    root = etree.fromstring(document_xml)

    # Iterate over paragraphs in document order
    for p in root.xpath("//w:body/w:p", namespaces=ns):
        lang_code = None

        # 1) Check paragraph properties for language
        pPr = p.find("w:pPr", namespaces=ns)
        if pPr is not None:
            lang_elem = pPr.find(".//w:lang", namespaces=ns)
            if lang_elem is not None:
                lang_code = lang_elem.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")

        # 2) If not found, look at the first run that specifies a language
        if lang_code is None:
            for r in p.findall("w:r", namespaces=ns):
                rPr = r.find("w:rPr", namespaces=ns)
                if rPr is not None:
                    lang_elem = rPr.find("w:lang", namespaces=ns)
                    if lang_elem is not None:
                        lang_code = lang_elem.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")
                        if lang_code:
                            break

        paragraph_langs.append(lang_code)
    return paragraph_langs

# -----------------------------------------------------------
# Main verification routine
# -----------------------------------------------------------

def verify_task(docx_path):
    """Verify that ONLY paragraph 2 is switched to English (UK) (en-GB)
    while at least one other paragraph remains English (US) (en-US).
    Returns a progressive score between 0.0 and 1.0.
    """
    print(f"Verifying file: {docx_path}")

    # Preliminary file check (no points awarded!)
    if not os.path.isfile(docx_path):
        print("✗ File not found – cannot verify task")
        print("REWARD: 0.0")
        return 0.0

    try:
        para_langs = extract_paragraph_languages(docx_path)
        print(f"Detected languages per paragraph: {para_langs}")
    except Exception as e:
        print(f"✗ Failed to parse document XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Progressive scoring variables
    total_score = 0.0
    max_score   = 1.0

    # Requirement 1 (0.7 pts): Paragraph 2 set to English (UK)
    if len(para_langs) >= 2 and para_langs[1] and para_langs[1].lower() == "en-gb":
        print("✓ Paragraph 2 is correctly set to English (UK)")
        total_score += 0.7
    else:
        print("✗ Paragraph 2 is NOT set to English (UK)")

    # Requirement 2 (0.3 pts): At least one OTHER paragraph remains English (US)
    other_para_langs = [lang for idx, lang in enumerate(para_langs) if idx != 1]
    if any(lang and lang.lower() == "en-us" for lang in other_para_langs):
        print("✓ At least one other paragraph remains English (US)")
        total_score += 0.3
    else:
        print("✗ No other paragraph remains English (US)")

    final_score = min(total_score, max_score)
    print(f"Final Score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

# -----------------------------------------------------------
# Execute verification (path provided by the task context)
# -----------------------------------------------------------
if __name__ == "__main__":
    file_path = (
        "/home/user/"
        "spell_check_keeps_flagging_colour_and_organise_in_paragraph_2_because_its_still_set_to_the_"
        "us_dictio.docx"
    )
    verify_task(file_path)

