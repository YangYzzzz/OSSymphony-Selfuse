"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer, how can I get the file’s Title field to show up automatically in the header area and have it sit flush against the right margin? I’d rather not type the title manually on every page.
Generated: 2025-09-10 12:49:07
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET


def verify_title_in_header(file_path: str) -> float:
    """Verify that the DOCX file has the Title document property field
    automatically inserted in a header paragraph and that the paragraph
    is right-aligned (flush against the right margin).

    Scoring (progressive):
        - 0.6 points  – Title field found in any header
        - 0.4 points  – The paragraph that contains the Title field is
                        explicitly right-aligned (w:jc val="right")
        - 1.0 points  – Both conditions satisfied

    Returns
    -------
    float
        Reward between 0.0 and 1.0 (inclusive).
    """

    max_score = 1.0
    score = 0.0

    print(f"Verifying document: {file_path}")

    # ---------- Preliminary checks (no points) ----------
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    # ---------- Open DOCX as a zip archive ----------
    try:
        docx_zip = zipfile.ZipFile(file_path, 'r')
    except zipfile.BadZipFile:
        print("✗ Not a valid DOCX (ZIP) file")
        return 0.0

    # ---------- Locate header XML files ----------
    header_files = [f for f in docx_zip.namelist()
                    if f.startswith('word/header') and f.endswith('.xml')]
    if not header_files:
        print("✗ No header XML files present – no header defined")
        docx_zip.close()
        return 0.0

    # Namespaces used in WordprocessingML
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }

    title_found = False      # Whether Title field appears in any header
    right_aligned = False    # Whether that paragraph has right alignment

    # ---------- Inspect each header ----------
    for hdr_path in header_files:
        try:
            xml_bytes = docx_zip.read(hdr_path)
            root = ET.fromstring(xml_bytes)
        except Exception as e:
            print(f"Warning: Could not parse {hdr_path}: {e}")
            continue

        # Iterate through paragraphs in the header
        for p in root.findall('.//w:p', ns):
            # --- Detect a DOCPROPERTY Title field in the paragraph ---
            has_title_field = False

            # Method 1:  <w:fldSimple w:instr="DOCPROPERTY  Title  \* MERGEFORMAT"/>
            fld_simple = p.find('.//w:fldSimple', ns)
            if fld_simple is not None:
                instr = fld_simple.get(f'{{{ns["w"]}}}instr', '')
                if re.search(r'DOCPROPERTY\s+Title', instr, re.IGNORECASE):
                    has_title_field = True

            # Method 2: Complex field codes with <w:instrText>
            if not has_title_field:
                for instr_text in p.findall('.//w:instrText', ns):
                    if instr_text.text and re.search(r'DOCPROPERTY\s+Title', instr_text.text, re.IGNORECASE):
                        has_title_field = True
                        break

            # If a Title field is present, evaluate alignment
            if has_title_field:
                title_found = True

                # Check paragraph alignment property <w:jc w:val="right"/>
                jc = p.find('./w:pPr/w:jc', ns)
                align_val = jc.get(f'{{{ns["w"]}}}val') if jc is not None else None
                print(f"✓ Found Title field in {hdr_path} with alignment '{align_val}'.")
                if align_val and align_val.lower() == 'right':
                    right_aligned = True
                else:
                    print("  ↳ Paragraph is not right-aligned.")

    docx_zip.close()

    # ---------- Progressive scoring ----------
    if title_found:
        score += 0.6
        print("✓ Title field present in header (0.6 points)")
    else:
        print("✗ Title field not found in any header (0 points)")

    if title_found and right_aligned:
        score += 0.4
        print("✓ Title paragraph right-aligned (0.4 points)")
    elif title_found:
        print("✗ Title paragraph not right-aligned (0 points)")

    final_score = min(score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    return final_score


# -------------------------
# Execute verification
# -------------------------
if __name__ == "__main__":
    TEST_FILE = "/home/user/in_libreoffice_writer_how_can_i_get_the_files_title_field_to_show_up_automatically_in_the_header_are.docx"
    reward = verify_title_in_header(TEST_FILE)
    print(f"REWARD: {reward}")
