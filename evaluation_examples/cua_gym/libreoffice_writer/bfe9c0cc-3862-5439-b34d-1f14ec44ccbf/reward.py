"""
FINAL REWARD SCRIPT - SUCCESS
Task: While reviewing this document in LibreOffice Writer I realized the third paragraph is a bit fuzzy. Could you walk me through how to stick a comment that reads exactly "Clarify scope." onto paragraph 3 so it’s obvious what needs fixing?
Generated: 2025-09-10 15:22:48
Status: success
Model: azure-o3
Total Steps: 1
"""

import zipfile
import os
import traceback
from lxml import etree

"""
Reward Verification Script
Task: Ensure that the DOCX document has a comment reading exactly
       "Clarify scope." attached to the third (non-empty) paragraph.
Scoring (progressive):
  • 0.5  – The required comment text exists in the document’s comment store.
  • 0.5  – That same comment is actually linked to paragraph-3.
Returns 1.0 only when both conditions are satisfied.
"""

def _extract_comments(zipf):
    """Return a dict {comment_id: comment_text}."""
    comments_path = 'word/comments.xml'
    if comments_path not in zipf.namelist():
        print('✗ comments.xml not found in DOCX')
        return {}

    root = etree.fromstring(zipf.read(comments_path))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    comments = {}
    for c in root.findall('w:comment', ns):
        cid = c.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
        texts = c.xpath('.//w:t', namespaces=ns)
        comment_text = ''.join(t.text for t in texts if t.text).strip()
        comments[cid] = comment_text
        print(f"  Found comment id={cid!r} text={comment_text!r}")
    return comments


def _paragraph_comment_ids(paragraph, ns):
    """Return set of comment IDs referenced within a paragraph element."""
    ids = set()
    for node in paragraph.xpath('.//w:commentRangeStart|.//w:commentReference', namespaces=ns):
        cid = node.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
        if cid:
            ids.add(cid)
    return ids


def _paragraph_text(paragraph, ns):
    texts = paragraph.xpath('.//w:t', namespaces=ns)
    return ''.join(t.text for t in texts if t.text)


def verify_comment_on_third_paragraph(docx_path: str, expected_comment: str = "Clarify scope.") -> float:
    """Main verification routine returning a score between 0.0 and 1.0."""
    score = 0.0
    max_score = 1.0

    if not os.path.exists(docx_path):
        print(f'✗ File not found: {docx_path}')
        return 0.0

    try:
        with zipfile.ZipFile(docx_path) as z:
            print('✓ DOCX file opened')

            # 1. ----- Validate the comment text exists -----
            comments = _extract_comments(z)
            matching_ids = [cid for cid, text in comments.items() if text == expected_comment]
            if matching_ids:
                print(f"✓ Found expected comment text {expected_comment!r} with ids {matching_ids}")
                score += 0.5
            else:
                print(f"✗ Expected comment text {expected_comment!r} not found")

            # Stop early if document.xml missing
            if 'word/document.xml' not in z.namelist():
                print('✗ document.xml not found in DOCX')
                return score

            # 2. ----- Determine if that comment is on paragraph-3 -----
            root = etree.fromstring(z.read('word/document.xml'))
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = root.xpath('//w:body/w:p', namespaces=ns)

            # Filter out empty paragraphs
            non_empty = [p for p in paragraphs if _paragraph_text(p, ns).strip() or list(p)]
            if len(non_empty) < 3:
                print('✗ Document has fewer than 3 non-empty paragraphs')
            else:
                third_p = non_empty[2]
                ids_in_third = _paragraph_comment_ids(third_p, ns)
                third_preview = _paragraph_text(third_p, ns)[:100]
                print(f"Third paragraph preview: {third_preview!r}")
                print(f'Comment IDs attached to third paragraph: {ids_in_third}')

                if any(cid in ids_in_third for cid in matching_ids):
                    print('✓ Expected comment is attached to paragraph-3')
                    score += 0.5
                elif matching_ids:
                    print('✗ Expected comment NOT attached to paragraph-3')

            final_score = min(score, max_score)
            print(f'Total score: {final_score}')
            return final_score

    except Exception:
        print('✗ Error during verification')
        traceback.print_exc()
        return 0.0


if __name__ == '__main__':
    DOCX_PATH = '/home/user/while_reviewing_this_document_in_libreoffice_writer_i_realized_the_third_paragraph_is_a_bit_fuzzy_co.docx'
    reward = verify_comment_on_third_paragraph(DOCX_PATH)
    print(f'REWARD: {reward}')
