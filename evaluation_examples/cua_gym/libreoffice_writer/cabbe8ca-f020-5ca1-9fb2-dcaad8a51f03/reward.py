"""
Reward Script: Insert endnotes for three cited references in a Writer document
Task ID: writer_rd_055
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30) — Three endnoteReference elements in body
  Component 2 (0.30) — Endnotes part has 3 real endnotes
  Component 3 (0.20) — Endnote content contains correct bibliographic text
  Component 4 (0.20) — Inline '(see reference X)' markers removed/replaced
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_055'

# Expected bibliographic keywords per endnote
EXPECTED_REFS = {
    1: "Wickham",
    2: "Heather",
    3: "Ward-Perkins",
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Component 1: Three endnoteReference elements exist in document body (0.30 points)
    try:
        body = doc.element
        endnote_refs = body.findall('.//w:endnoteReference', ns)
        ref_count = len(endnote_refs)
        if ref_count >= 3:
            print(f"PASS: Component 1 — Found {ref_count} endnoteReference elements in body (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected 3 endnoteReference elements, found {ref_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Endnotes part exists with 3 real endnotes (0.30 points)
    # System endnotes (id=-1, id=0) are always present; real endnotes have id >= 1
    try:
        endnote_rel_count = 0
        real_endnotes = []
        endnotes_xml = None
        for rel_key, rel in doc.part.rels.items():
            if 'endnote' in str(rel.reltype).lower():
                endnote_rel_count += 1
                blob = rel.target_part.blob
                root = etree.fromstring(blob)
                all_endnotes = root.findall('.//w:endnote', ns)
                for en in all_endnotes:
                    en_id = en.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
                    if en_id is not None and int(en_id) >= 1:
                        # Extract text
                        text = ''
                        for p in en.findall('.//w:p', ns):
                            for t in p.findall('.//w:t', ns):
                                text += (t.text or '')
                        real_endnotes.append((int(en_id), text.strip()))
                endnotes_xml = root
                break

        if endnote_rel_count == 0:
            print("FAIL: Component 2 — No endnotes relationship found in document")
        elif len(real_endnotes) >= 3:
            print(f"PASS: Component 2 — Found {len(real_endnotes)} real endnotes (ids: {[e[0] for e in real_endnotes]}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Expected 3 real endnotes, found {len(real_endnotes)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Endnote content contains correct bibliographic references (0.20 points)
    # Each endnote should reference the correct author
    try:
        if len(real_endnotes) >= 3:
            matched = 0
            for en_id, en_text in real_endnotes:
                if en_id in EXPECTED_REFS:
                    expected_author = EXPECTED_REFS[en_id]
                    if expected_author.lower() in en_text.lower():
                        matched += 1
                        print(f"  Endnote {en_id}: contains '{expected_author}' — OK")
                    else:
                        print(f"  Endnote {en_id}: expected '{expected_author}' but found: {en_text[:100]}")

            if matched >= 3:
                print(f"PASS: Component 3 — All 3 endnotes have correct bibliographic content (0.20 pts)")
                total_score += 0.20
            elif matched >= 2:
                partial = round(0.20 * matched / 3, 2)
                print(f"PARTIAL: Component 3 — {matched}/3 endnotes matched ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {matched}/3 endnotes matched")
        else:
            print("FAIL: Component 3 — Not enough endnotes to verify content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Inline '(see reference X)' markers removed/replaced (0.20 points)
    # In the golden doc, these should be gone (replaced by endnote superscripts)
    try:
        see_ref_count = 0
        for para in doc.paragraphs:
            if '(see reference' in para.text.lower():
                see_ref_count += 1

        if see_ref_count == 0:
            print(f"PASS: Component 4 — No '(see reference X)' markers remain in body text (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Found {see_ref_count} paragraphs still containing '(see reference X)'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
