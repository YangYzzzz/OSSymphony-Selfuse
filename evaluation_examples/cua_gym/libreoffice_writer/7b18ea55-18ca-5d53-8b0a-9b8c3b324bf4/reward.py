"""
FINAL REWARD SCRIPT - SUCCESS
Task: LibreOffice Writer keeps peppering paragraph 11 (it’s a block of SQL code) with red squiggles. How do I select that one paragraph and set its language to “None” so spell-check leaves it alone while the rest of the document still gets checked?
Generated: 2025-09-10 13:47:13
Status: success
Model: azure-o3
Total Steps: 10
"""

import os
import re
import zipfile
from lxml import etree as ET


def verify_writer_language_setting(file_path: str) -> float:
    """Verify that only the SQL paragraph has its language set to *None* (zxx)
    while every other paragraph retains a normal spell-checkable language.

    Scoring (progressive):
        0.6 – Every run in the SQL paragraph is correctly marked zxx
        0.3 – Some (but not all) runs in that paragraph are marked zxx
        +0.4 – No other paragraph in the document is marked zxx
        +0.2 – If only some runs were zxx but no other paragraph is zxx
        (capped to 1.0)
    """

    max_score = 1.0
    score = 0.0

    # ---------- 1) Basic file checks ----------
    if not os.path.exists(file_path):
        print("✗ File does not exist:", file_path)
        return 0.0  # Nothing to check

    try:
        with zipfile.ZipFile(file_path) as zf:
            if "word/document.xml" not in zf.namelist():
                print("✗ document.xml missing – not a valid DOCX")
                return 0.0
            xml_bytes = zf.read("word/document.xml")
    except Exception as exc:
        print("✗ Cannot open DOCX:", exc)
        return 0.0  # Critical failure – no points

    # ---------- 2) Parse XML ----------
    try:
        root = ET.fromstring(xml_bytes)
    except ET.XMLSyntaxError as exc:
        print("✗ XML parsing error:", exc)
        return 0.0

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs = root.xpath("//w:body/w:p", namespaces=ns)

    # ---------- 3) Locate the SQL paragraph ----------
    sql_regex = re.compile(r"\bselect\b.*\bfrom\b", re.I | re.S)
    sql_paragraph = None
    sql_index = None

    for idx, p in enumerate(paragraphs):
        texts = [t.text for t in p.xpath(".//w:t", namespaces=ns) if t.text]
        if sql_regex.search(" ".join(texts)):
            sql_paragraph = p
            sql_index = idx
            break

    if sql_paragraph is None:
        print("✗ SQL paragraph containing 'SELECT … FROM' not found – cannot verify task")
        return 0.0

    print(f"✓ Located SQL paragraph at index {sql_index} (1-based {sql_index + 1})")

    # ---------- 4) Check language (w:lang) on runs inside SQL paragraph ----------
    run_langs = []
    for rPr in sql_paragraph.xpath(".//w:rPr", namespaces=ns):
        lang_el = rPr.find("w:lang", namespaces=ns)
        run_langs.append(
            lang_el.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val") if lang_el is not None else None
        )

    full_sql_correct = bool(run_langs) and all(l == "zxx" for l in run_langs)
    partial_sql_correct = any(l == "zxx" for l in run_langs) and not full_sql_correct

    if full_sql_correct:
        score += 0.6
        print("✓ All runs in SQL paragraph are language 'None' (zxx) (+0.6)")
    elif partial_sql_correct:
        score += 0.3
        print("• Some runs in SQL paragraph are language 'None' (zxx) (+0.3)")
    else:
        print("✗ SQL paragraph is not marked language 'None'")

    # ---------- 5) Ensure no OTHER paragraph is set to zxx ----------
    other_zxx_found = False
    for idx, para in enumerate(paragraphs):
        if para is sql_paragraph:
            continue  # Skip SQL paragraph itself
        for lang_el in para.xpath(".//w:lang", namespaces=ns):
            if lang_el.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val") == "zxx":
                other_zxx_found = True
                print(f"✗ Paragraph {idx} incorrectly has language 'None' (zxx)")
                break
        if other_zxx_found:
            break

    if not other_zxx_found and (full_sql_correct or partial_sql_correct):
        # Award bonus only if SQL paragraph is at least partially correct
        bonus = 0.4 if full_sql_correct else 0.2
        score += bonus
        print(f"✓ No other paragraph uses language 'None' (+{bonus})")

    # ---------- 6) Finalise score ----------
    final_score = min(score, max_score)
    print(f"Total score: {final_score}")
    return final_score


if __name__ == "__main__":
    DOC_PATH = "/home/user/libreoffice_writer_keeps_peppering_paragraph_11_its_a_block_of_sql_code_with_red_squiggles_how_do_i_.docx"
    reward = verify_writer_language_setting(DOC_PATH)
    print("REWARD:", reward)

