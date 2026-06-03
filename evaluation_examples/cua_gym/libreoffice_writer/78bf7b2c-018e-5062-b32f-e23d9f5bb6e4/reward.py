"""
FINAL REWARD SCRIPT - SUCCESS
Task: Quick refresher, please: in LibreOffice Writer, how do I stick a comment that literally says "Rephrase this." on paragraph 5?
Generated: 2025-09-10 13:20:18
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import zipfile
from lxml import etree

"""
Reward Script for LibreOffice Writer Task
Task:  "Quick refresher, please: in LibreOffice Writer, how do I stick a comment that literally says \"Rephrase this.\" on paragraph 5?"

The script verifies two key requirements:
1. A comment whose text is EXACTLY "Rephrase this." exists in the document.
2. That comment is attached to paragraph 5 (1-based index).

Progressive scoring:
• 0.7 points ‑ Comment with correct text exists.
• +0.3 points ‑ Comment is attached to the correct paragraph (paragraph 5).
The script returns 1.0 only when both conditions are met.
"""

# ----------------------------- Helper Functions ----------------------------- #

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def _load_comments(zip_file):
    """Return a dict mapping comment ID → comment text for a DOCX file."""
    try:
        xml_bytes = zip_file.read("word/comments.xml")
    except KeyError:
        return {}

    root = etree.fromstring(xml_bytes)
    mapping = {}
    for cm in root.xpath("//w:comment", namespaces=NS):
        cid = cm.get(f"{{{NS['w']}}}id")
        text_nodes = cm.xpath(".//w:t", namespaces=NS)
        mapping[cid] = "".join(t.text or "" for t in text_nodes)
    return mapping


def _paragraph_comment_ids(zip_file):
    """Return a list where each index corresponds to a paragraph and holds the first
    comment ID that starts in that paragraph (or None)."""
    doc_xml = zip_file.read("word/document.xml")
    root = etree.fromstring(doc_xml)
    paragraphs = root.xpath("//w:body/w:p", namespaces=NS)

    para_comment_ids = []
    for p in paragraphs:
        start = p.xpath(".//w:commentRangeStart", namespaces=NS)
        if start:
            cid = start[0].get(f"{{{NS['w']}}}id")
            para_comment_ids.append(cid)
        else:
            para_comment_ids.append(None)
    return para_comment_ids

# --------------------------- Verification Function -------------------------- #

def verify_writer_comment(file_path,
                           expected_comment="Rephrase this.",
                           target_paragraph=5):
    print(f"Verifying file: {file_path}")

    # Guard: file must exist
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    # Only DOCX implementation needed for this task
    if not file_path.lower().endswith(".docx"):
        print("✗ Unsupported file format (only .docx verified)")
        return 0.0

    score = 0.0  # progressive score

    with zipfile.ZipFile(file_path) as zf:
        # 1) Check that a comment with exact text exists
        comments = _load_comments(zf)
        matching_ids = [cid for cid, txt in comments.items()
                        if txt.strip().lower() == expected_comment.lower()]
        if matching_ids:
            print(f"✓ Found comment text '{expected_comment}' (id(s): {matching_ids})")
            score += 0.7
        else:
            print(f"✗ Comment text '{expected_comment}' not found")
            print(f"REWARD: {score}")
            return score  # can't earn more without correct comment

        # 2) Check that one of those comments starts in paragraph 5
        para_comment_ids = _paragraph_comment_ids(zf)
        target_idx = target_paragraph - 1  # convert to 0-based index
        if target_idx < len(para_comment_ids):
            cid_at_para = para_comment_ids[target_idx]
            if cid_at_para and cid_at_para in matching_ids:
                print(f"✓ Comment correctly attached to paragraph {target_paragraph}")
                score += 0.3
            else:
                print(f"✗ Expected comment not attached to paragraph {target_paragraph}")
        else:
            print(f"✗ Document has only {len(para_comment_ids)} paragraphs (< {target_paragraph})")

    final_score = min(score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score

# ------------------------------ Auto-execution ------------------------------ #
if __name__ == "__main__":
    # Attempt to locate the file in the user's home directory automatically
    home_dir = "/home/user"
    target_file = None
    for fname in os.listdir(home_dir):
        if fname.startswith("quick_refresher") and fname.endswith(".docx"):
            target_file = os.path.join(home_dir, fname)
            break
    if not target_file:
        # Fallback to explicit path (matches task description)
        target_file = (
            "/home/user/quick_refresher_please_in_libreoffice_writer_how_do_i_"
            "stick_a_comment_that_literally_says_rephrase_t.docx"
        )

    verify_writer_comment(target_file)

