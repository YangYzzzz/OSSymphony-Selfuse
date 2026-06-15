"""
Reward Script: Add three footnotes to history_essay (writer_creative_046.docx)
Task ID: writer_creative_046
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4 pts): footnotes.xml exists and contains exactly 3 user footnotes (IDs 1-3)
  Component 2 (0.3 pts): All 3 footnote texts exactly match required citations
  Component 3 (0.3 pts): All 3 footnote reference markers appear immediately after the correct phrases in body text
  Total: 1.0
"""

import os
import zipfile
import re
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_creative_046'

# Required footnote content (exact strings expected in the XML)
REQUIRED_FOOTNOTES = {
    1: 'John Smith, The Age of Revolution, Oxford University Press, 2019, p.45.',
    2: 'Sarah Davis, Colonial Perspectives, Harvard Press, 2021, p.112.',
    3: 'Robert Thompson et al., Maritime Trade Patterns, Cambridge, 2020, p.78.',
}

# Anchor phrases that should immediately precede each footnote marker in body text
ANCHOR_PHRASES = {
    1: 'according to Smith (2019)',
    2: 'Davis argues',
    3: 'the Thompson study',
}

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid zip/docx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open docx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    with zf:
        namelist = zf.namelist()

        # ---------------------------------------------------------------
        # Component 1: footnotes.xml exists and has exactly 3 user footnotes
        # (IDs 1, 2, 3 — excludes separator stubs with id=-1 and id=0)
        # (0.4 points)
        # ---------------------------------------------------------------
        try:
            if 'word/footnotes.xml' not in namelist:
                print("FAIL: Component 1 — word/footnotes.xml not present in docx (no footnotes added)")
            else:
                fn_xml = zf.read('word/footnotes.xml').decode('utf-8')
                # Count footnote elements with positive integer ids (user footnotes)
                fn_ids = re.findall(r'<w:footnote\b[^>]*\bw:id="(\d+)"', fn_xml)
                fn_ids = [int(x) for x in fn_ids if int(x) > 0]
                if len(fn_ids) == 3 and sorted(fn_ids) == [1, 2, 3]:
                    print(f"PASS: Component 1 — footnotes.xml present with 3 user footnotes (IDs: {sorted(fn_ids)}) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 1 — expected 3 footnotes with IDs [1,2,3], found IDs: {sorted(fn_ids)}")
        except Exception as e:
            print(f"ERROR: Component 1 — {e}")

        # ---------------------------------------------------------------
        # Component 2: All 3 footnote texts match required citations
        # (0.3 points)
        # ---------------------------------------------------------------
        try:
            if 'word/footnotes.xml' not in namelist:
                print("FAIL: Component 2 — footnotes.xml missing, cannot check text")
            else:
                fn_xml = zf.read('word/footnotes.xml').decode('utf-8')
                root = ET.fromstring(fn_xml)
                ns = {'w': W_NS}

                # Build a map from footnote id to concatenated text
                fn_text_map = {}
                for fn_elem in root.findall('w:footnote', ns):
                    fn_id_str = fn_elem.get(f'{{{W_NS}}}id')
                    if fn_id_str is None:
                        continue
                    fn_id = int(fn_id_str)
                    if fn_id <= 0:
                        continue
                    # Gather all text runs inside this footnote, excluding <w:footnoteRef/>
                    texts = []
                    for t_elem in fn_elem.iter(f'{{{W_NS}}}t'):
                        texts.append(t_elem.text or '')
                    fn_text_map[fn_id] = ''.join(texts).strip()

                passed_texts = 0
                for fn_id, expected_text in REQUIRED_FOOTNOTES.items():
                    actual_text = fn_text_map.get(fn_id, '')
                    # Normalize spaces for comparison
                    if actual_text.strip() == expected_text.strip():
                        print(f"PASS: Component 2 — Footnote {fn_id} text correct: '{actual_text[:60]}...'")
                        passed_texts += 1
                    else:
                        print(f"FAIL: Component 2 — Footnote {fn_id} text mismatch:")
                        print(f"  Expected: '{expected_text}'")
                        print(f"  Actual:   '{actual_text}'")

                if passed_texts == 3:
                    print(f"PASS: Component 2 — All 3 footnote texts match (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Only {passed_texts}/3 footnote texts matched")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")

        # ---------------------------------------------------------------
        # Component 3: Footnote reference markers appear immediately after
        # the correct anchor phrases in the document body
        # (0.3 points)
        # ---------------------------------------------------------------
        try:
            if 'word/document.xml' not in namelist:
                print("FAIL: Component 3 — word/document.xml not present")
            else:
                doc_xml = zf.read('word/document.xml').decode('utf-8')

                # Strategy: extract ordered runs of text, tracking footnote refs.
                # For each <w:footnoteReference w:id="N"/>, find the preceding text
                # in the XML and verify the anchor phrase is there.
                # We scan for pattern: anchor_text ... <w:footnoteReference w:id="N"/>

                passed_refs = 0
                for fn_id, anchor in ANCHOR_PHRASES.items():
                    # Build a pattern: anchor text (possibly split across runs) appears
                    # before the footnoteReference with this id.
                    # We search in a window of text before the ref tag.
                    ref_pattern = fr'<w:footnoteReference w:id="{fn_id}"/>'
                    ref_pos = doc_xml.find(ref_pattern)
                    if ref_pos == -1:
                        print(f"FAIL: Component 3 — No footnote reference marker with id={fn_id} found in body")
                        continue

                    # Extract preceding XML context (up to 2000 chars)
                    context_before = doc_xml[max(0, ref_pos - 2000): ref_pos]

                    # Strip XML tags to get plain text and check for anchor phrase
                    plain_before = re.sub(r'<[^>]+>', '', context_before)
                    # Normalize whitespace
                    plain_before = re.sub(r'\s+', ' ', plain_before)

                    if anchor.lower() in plain_before.lower():
                        print(f"PASS: Component 3 — Footnote {fn_id} ref marker follows anchor phrase '{anchor}' (ok)")
                        passed_refs += 1
                    else:
                        print(f"FAIL: Component 3 — Footnote {fn_id} ref marker exists but anchor phrase '{anchor}' not found immediately before it")
                        print(f"  Context (stripped): ...{plain_before[-200:]}")

                if passed_refs == 3:
                    print(f"PASS: Component 3 — All 3 footnote markers placed correctly after anchor phrases (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Only {passed_refs}/3 footnote markers correctly placed")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
