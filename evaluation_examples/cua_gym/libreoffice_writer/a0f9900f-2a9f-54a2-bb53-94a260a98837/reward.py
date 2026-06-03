"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer, how do I turn the words “Contact us” into an email link that opens a new message to support@example.com when someone clicks it?
Generated: 2025-09-10 19:07:02
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

"""
Reward Script: LibreOffice Writer – Verify “Contact us” Email Link
---------------------------------------------------------------
This script validates that within the provided DOCX file the words
“Contact us” have been correctly converted into a hyperlink that opens a
new e-mail message addressed to **support@example.com**.

Scoring (progressive):
 • 0.5 points – Anchor text “Contact us” is present *and* wrapped in a hyperlink
 • 0.5 points – That hyperlink’s target begins with “mailto:” and contains “support@example.com”

A perfect implementation returns REWARD: 1.0.
"""

FILE_PATH = "/home/user/in_libreoffice_writer_how_do_i_turn_the_words_contact_us_into_an_email_link_that_opens_a_new_message.docx"
EXPECTED_ANCHOR = "Contact us"
EXPECTED_EMAIL = "support@example.com"


def _extract_relationships(zipf):
    """Return a dict mapping relationship id → target."""
    rels_path = "word/_rels/document.xml.rels"
    id_to_target = {}

    if rels_path not in zipf.namelist():
        print("✗ Relationships file not found – cannot resolve hyperlink targets")
        return id_to_target

    rel_xml = zipf.read(rels_path)
    rel_root = ET.fromstring(rel_xml)

    # Relationship elements live in the package relationships namespace
    for rel in rel_root:
        rid = rel.attrib.get("Id") or rel.attrib.get("{http://schemas.openxmlformats.org/package/2006/relationships}Id")
        target = rel.attrib.get("Target") or rel.attrib.get("{http://schemas.openxmlformats.org/package/2006/relationships}Target")
        id_to_target[rid] = target
    return id_to_target


def _find_hyperlinks(file_path):
    """Return a list of dicts with keys: anchor, target for every hyperlink."""
    hyperlinks = []

    with zipfile.ZipFile(file_path, "r") as z:
        if "word/document.xml" not in z.namelist():
            print("✗ document.xml not found – invalid DOCX structure")
            return hyperlinks

        doc_xml = z.read("word/document.xml")
        relationships = _extract_relationships(z)

        # Parse main document XML
        root = ET.fromstring(doc_xml)
        w_ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        r_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

        for h in root.iter(f"{w_ns}hyperlink"):
            rid = h.attrib.get(f"{r_ns}id")
            # Collect visible text inside hyperlink
            anchor_parts = [t.text for t in h.iter(f"{w_ns}t") if t.text]
            anchor_text = "".join(anchor_parts).strip()
            target = relationships.get(rid)
            hyperlinks.append({"anchor": anchor_text, "target": target})
    return hyperlinks


def verify_email_link(file_path: str, expected_anchor: str, expected_email: str) -> float:
    """Return a progressive score based on hyperlink correctness."""
    print(f"Verifying email link in: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0  # No points for missing file

    try:
        links = _find_hyperlinks(file_path)
    except Exception as e:
        print(f"✗ Error reading hyperlinks: {e}")
        return 0.0

    if not links:
        print("✗ No hyperlinks found in document")
        return 0.0

    print(f"✓ Found {len(links)} hyperlink(s) in document")

    anchor_match = False
    email_match = False

    expected_anchor_norm = expected_anchor.strip().lower()

    # Examine each hyperlink for matches
    for link in links:
        anchor_norm = re.sub(r"\s+", " ", link["anchor"]).strip().lower()
        if anchor_norm == expected_anchor_norm:
            anchor_match = True
            target = link["target"] or ""
            if target.lower().startswith("mailto:") and expected_email.lower() in target.lower():
                email_match = True
            break  # Found the relevant anchor; no need to keep looping

    score = 0.0

    # 0.5 points – anchor text linked
    if anchor_match:
        print(f"✓ Anchor text '{expected_anchor}' is hyperlinked")
        score += 0.5
    else:
        print(f"✗ Anchor text '{expected_anchor}' not linked")

    # 0.5 points – correct mailto target
    if email_match:
        print(f"✓ Hyperlink target correctly set to mailto:{expected_email}")
        score += 0.5
    elif anchor_match:
        print("✗ Hyperlink does not point to the correct email address")

    final_score = min(score, 1.0)
    print(f"Total score: {final_score}/1.0")
    return final_score


if __name__ == "__main__":
    reward = verify_email_link(FILE_PATH, EXPECTED_ANCHOR, EXPECTED_EMAIL)
    print(f"REWARD: {reward}")

