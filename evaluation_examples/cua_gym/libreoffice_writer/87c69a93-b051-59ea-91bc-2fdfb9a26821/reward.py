"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m wrapping up a seminar handout and need the actual Title field (the one stored under File ▸ Properties) to sit dead-center in the page header. What’s the quickest way to set that up in LibreOffice Writer so it updates automatically if the title changes?
Generated: 2025-09-10 16:58:55
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import zipfile
from lxml import etree


def verify_title_field_in_header(file_path: str) -> float:
    """Verify that a LibreOffice/Word document has the Title document property field
    placed in the header and that the paragraph is center-aligned.

    Scoring (progressive):
    • 0.5 – Title document property field exists in *any* header part
    • 0.5 – That paragraph is explicitly centre-aligned (w:jc w:val="center")
    Returns a score between 0.0 and 1.0.
    """

    print(f"Verifying document: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return 0.0  # Nothing to verify

    score = 0.0

    try:
        with zipfile.ZipFile(file_path, "r") as docx_zip:
            # Collect header XML parts
            header_files = [f for f in docx_zip.namelist()
                            if f.startswith("word/header") and f.endswith(".xml")]
            if not header_files:
                print("✗ No header parts present – cannot verify header content")
                return 0.0

            print(f"Found {len(header_files)} header part(s): {header_files}")

            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

            title_field_found = False
            title_field_centered = False

            # Examine each header part for a Title field
            for hdr in header_files:
                root = etree.fromstring(docx_zip.read(hdr))

                for p in root.findall(".//w:p", ns):
                    # Detect simple field (w:fldSimple) or complex field (w:instrText)
                    fld_found = False

                    # 1) Simple field pattern
                    for fld in p.findall(".//w:fldSimple", ns):
                        instr = fld.get(f"{{{ns['w']}}}instr")
                        if instr and "DOCPROPERTY" in instr.upper() and "TITLE" in instr.upper():
                            fld_found = True
                            break

                    # 2) Complex field pattern (runs containing w:instrText)
                    if not fld_found:
                        combined_instr = " ".join(
                            t.text for t in p.findall(".//w:instrText", ns) if t.text
                        )
                        if combined_instr and "DOCPROPERTY" in combined_instr.upper() and "TITLE" in combined_instr.upper():
                            fld_found = True

                    if fld_found:
                        title_field_found = True
                        # Check paragraph alignment – centred?
                        jc = p.find("./w:pPr/w:jc", ns)
                        if jc is not None and jc.get(f"{{{ns['w']}}}val") == "center":
                            title_field_centered = True
                        # We can break early if both conditions satisfied
                        if title_field_centered:
                            break

                if title_field_found and title_field_centered:
                    break  # No need to check further headers

            # Progressive scoring
            if title_field_found:
                score += 0.5
                print("✓ Title field referencing document property found in header (0.5)")
            else:
                print("✗ No Title field referencing document property found in header")

            if title_field_centered:
                score += 0.5
                print("✓ Title field paragraph is centered (0.5)")
            elif title_field_found:
                print("✗ Title field exists but paragraph is not centered")

    except Exception as e:
        print(f"✗ Error while inspecting document: {e}")
        return 0.0

    print(f"Total score awarded: {score}")
    return min(score, 1.0)


def main():
    # Path provided by the task context
    file_path = (
        "/home/user/"
        "im_wrapping_up_a_seminar_handout_and_need_the_actual_title_field_"
        "the_one_stored_under_file_propertie.docx"
    )

    reward = verify_title_field_in_header(file_path)
    print(f"REWARD: {reward}")


if __name__ == "__main__":
    main()
