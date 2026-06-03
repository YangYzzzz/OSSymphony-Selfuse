"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve got a couple of cross-references that should jump straight to the start of Appendix A. What’s the quickest way to drop a bookmark named "annex-a" right on the “Appendix A” heading in LibreOffice Writer?
Generated: 2025-09-10 18:58:28
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import re
import zipfile
import traceback
from lxml import etree


def extract_docx_bookmarks(file_path):
    """Extract all bookmarks from a DOCX file along with the paragraph text
    where the bookmark starts.
    Returns a list of dicts with keys: name, paragraph_text"""
    bookmarks = []
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Main document XML
            doc_xml = zf.read('word/document.xml')
            root = etree.fromstring(doc_xml)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            # Iterate over all bookmarkStart elements
            for bkm_start in root.findall('.//w:bookmarkStart', ns):
                name = bkm_start.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}name')

                # Get the nearest ancestor paragraph (<w:p>) to capture heading text
                para = bkm_start.xpath('ancestor::w:p[1]', namespaces=ns)
                para_text = ''
                if para:
                    # Gather visible text within the paragraph
                    for t in para[0].xpath('.//w:t', namespaces=ns):
                        if t.text:
                            para_text += t.text

                bookmarks.append({'name': name, 'paragraph_text': para_text})
    except Exception as e:
        print(f"✗ Error extracting bookmarks: {e}")
        traceback.print_exc()
    return bookmarks


def verify_annex_a_bookmark(file_path):
    """Verify that the document contains a bookmark named 'annex-a' placed on
    a paragraph that includes the text 'Appendix A'. Returns a progressive
    score between 0.0 and 1.0."""
    score = 0.0
    max_score = 1.0

    print(f"Verifying LibreOffice Writer task in file: {file_path}")

    # Preliminary existence check (NO points for this!)
    if not os.path.exists(file_path):
        print("✗ File not found – cannot verify task")
        print("REWARD: 0.0")
        return 0.0

    # Support only DOCX for this verifier
    if not file_path.lower().endswith('.docx'):
        print("✗ Provided document is not a DOCX – unsupported format for this verifier")
        print("REWARD: 0.0")
        return 0.0

    # Extract bookmarks
    bookmarks = extract_docx_bookmarks(file_path)
    print(f"Found {len(bookmarks)} bookmark(s) in document.")
    for bm in bookmarks:
        print(f"  - Bookmark '{bm['name']}' in paragraph: '{bm['paragraph_text'][:60]}'")

    # Requirement 1: Bookmark named 'annex-a' exists (0.5 pts)
    annex_bookmarks = [bm for bm in bookmarks if bm['name'] and bm['name'].lower() == 'annex-a']
    if annex_bookmarks:
        print("✓ Bookmark named 'annex-a' exists (0.5 points)")
        score += 0.5

        # Requirement 2: Bookmark is placed on a paragraph containing 'Appendix A' (0.5 pts)
        correct_position = any(
            bm['paragraph_text'] and re.search(r'appendix\s+a', bm['paragraph_text'], re.IGNORECASE)
            for bm in annex_bookmarks
        )
        if correct_position:
            print("✓ Bookmark is correctly placed at the 'Appendix A' heading (0.5 points)")
            score += 0.5
        else:
            print("✗ 'annex-a' bookmark not at an 'Appendix A' heading (0 points)")
    else:
        print("✗ No bookmark named 'annex-a' found (0 points)")

    # Final score (ensure not above 1.0)
    final_score = min(score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


# ---------------------------
# Execute verification script
# ---------------------------
if __name__ == '__main__':
    target_file = (
        '/home/user/ive_got_a_couple_of_cross_references_that_should_jump_straight_to_the_start_of_appendix_a_whats_the_.docx'
    )
    verify_annex_a_bookmark(target_file)
