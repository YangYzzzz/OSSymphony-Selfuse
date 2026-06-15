"""
FINAL REWARD SCRIPT - SUCCESS
Task: When I put the header text "Draft — Do Not Distribute" in LibreOffice Writer it shows up on every page, but I only want it on the odd-numbered pages and left-aligned. How do I set that up?
Generated: 2025-09-10 13:04:42
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import re
import zipfile
from lxml import etree as ET

"""
Reward Script: LibreOffice Writer – Odd-Page Left-Aligned Header Verification

Task to verify:
The document should show the header text "Draft — Do Not Distribute" ONLY on odd-numbered pages
and that text must be left-aligned.

Scoring (progressive):
• 0.4  – Required header text appears in the *default / odd-page* header
• 0.4  – The same text is *absent* from every even-page header
• 0.2  – The text in the odd-page header is left-aligned
Total possible = 1.0

This script analyses the DOCX package directly via XML so it works even when the
file was authored in LibreOffice Writer.
"""

FILE_PATH = "/home/user/when_i_put_the_header_text_draft_do_not_distribute_in_libreoffice_writer_it_shows_up_on_every_page_b.docx"

# Regex to match the required header text (case-insensitive, allows either – or —)
TEXT_PATTERN = re.compile(r"Draft\s+[—-]\s+Do Not Distribute", re.IGNORECASE)

# XML namespaces used in DOCX files
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

def extract_header_parts(zip_file):
    """Build a mapping {header-type -> set(xml part names)} from document relationships."""
    rel_root = ET.fromstring(zip_file.read("word/_rels/document.xml.rels"))
    rid_to_target = {el.get("Id"): el.get("Target") for el in rel_root}

    doc_root = ET.fromstring(zip_file.read("word/document.xml"))
    type_to_parts = {}

    for sect in doc_root.xpath(".//w:sectPr", namespaces=NS):
        for hdr in sect.xpath("./w:headerReference", namespaces=NS):
            h_type = hdr.get(f"{{{NS['w']}}}type", "default")  # default if no explicit type
            rid = hdr.get(f"{{{NS['r']}}}id")
            part = rid_to_target.get(rid)
            if not part:
                continue
            if not part.startswith("word/"):
                part = "word/" + part
            type_to_parts.setdefault(h_type, set()).add(part)
    return type_to_parts

def get_header_text_and_alignment(zip_file, part_name):
    """Return (full_text, alignment) for the first paragraph in the given header part."""
    xml = zip_file.read(part_name)
    root = ET.fromstring(xml)

    # Collect concatenated text from all <w:t> elements
    texts = [t.text for t in root.xpath(".//w:t", namespaces=NS) if t.text]
    full_text = " ".join(texts).strip()

    # Determine alignment from the first paragraph (<w:jc val="...">)
    alignment = "left"  # default assumption in Word/Writer if not specified
    first_p = root.find(".//w:p", namespaces=NS)
    if first_p is not None:
        jc = first_p.find(".//w:jc", namespaces=NS)
        if jc is not None:
            alignment = jc.get(f"{{{NS['w']}}}val", "left")
    return full_text, alignment

def verify_task(file_path):
    score = 0.0
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as z:
            # 1. Discover which header parts belong to odd (default) and even pages
            type_parts = extract_header_parts(z)
            print("Header parts by type:", {k: list(v) for k, v in type_parts.items()})

            # --- Requirement 1: text present in odd (default) header(s) ---
            default_text_ok = False
            if "default" in type_parts:
                for part in type_parts["default"]:
                    text, alignment = get_header_text_and_alignment(z, part)
                    print(f"default header {part}: text='{text}' alignment={alignment}")
                    if TEXT_PATTERN.search(text):
                        default_text_ok = True
                        break
            if default_text_ok:
                score += 0.4
                print("✓ Required text present in odd-page header (0.4)")
            else:
                print("✗ Required text NOT found in odd-page header")

            # --- Requirement 2: text absent from all even headers ---
            even_text_absent = True  # remains true only if no match found
            if "even" in type_parts:
                for part in type_parts["even"]:
                    text, _ = get_header_text_and_alignment(z, part)
                    print(f"even header {part}: text='{text}'")
                    if TEXT_PATTERN.search(text):
                        even_text_absent = False
                        break
            if even_text_absent:
                score += 0.4
                print("✓ Text absent from even-page headers (0.4)")
            else:
                print("✗ Text incorrectly appears in an even-page header")

            # --- Requirement 3: left alignment in odd header ---
            alignment_ok = False
            if "default" in type_parts:
                for part in type_parts["default"]:
                    _, alignment = get_header_text_and_alignment(z, part)
                    if alignment in (None, "left"):
                        alignment_ok = True
                    else:
                        alignment_ok = False
                        break  # any non-left alignment fails
            if alignment_ok:
                score += 0.2
                print("✓ Odd-page header text is left-aligned (0.2)")
            else:
                print("✗ Odd-page header text is NOT left-aligned")

    except Exception as e:
        print("✗ Error while verifying document:", e)
        return 0.0

    score = min(score, 1.0)  # safeguard
    print(f"Final score: {score}")
    return score

if __name__ == "__main__":
    reward = verify_task(FILE_PATH)
    print(f"REWARD: {reward}")

