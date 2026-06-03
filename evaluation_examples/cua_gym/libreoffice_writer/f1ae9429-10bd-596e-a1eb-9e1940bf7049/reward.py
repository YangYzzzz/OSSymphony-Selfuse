"""
Reward Script: Verify footnote and endnote insertion in Writer document
Task ID: writer_bs_044
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.3): Footnote with correct text exists
  - Component 2 (0.3): Endnote with correct text exists
  - Component 3 (0.2): Footnote reference placed near 'p-hacking' in body
  - Component 4 (0.2): Endnote reference placed near '(Simmons et al., 2011)' in body
"""

import os
import re
import zipfile

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_044'

EXPECTED_FOOTNOTE_TEXT = 'P-hacking refers to the misuse of data analysis to find statistically significant patterns.'
EXPECTED_ENDNOTE_TEXT = 'Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-Positive Psychology. Psychological Science, 22(11), 1359-1366.'


def get_note_texts(zf, xml_name, tag_prefix):
    """Extract user notes (skip separator/continuationSeparator notes) from footnotes.xml or endnotes.xml."""
    if xml_name not in zf.namelist():
        return []
    content = zf.read(xml_name).decode('utf-8')
    # Find all note elements that do NOT have type="separator" or type="continuationSeparator"
    # User notes have a positive integer id and no type attribute (or type="normal")
    notes = []
    # Pattern: find each <w:footnote ...>...</w:footnote> or <w:endnote ...>...</w:endnote>
    note_tag = 'footnote' if 'footnote' in xml_name else 'endnote'
    pattern = re.compile(
        rf'<w:{note_tag}\s[^>]*?w:id="(\d+)"[^>]*?>(.*?)</w:{note_tag}>',
        re.DOTALL
    )
    for match in pattern.finditer(content):
        note_id = int(match.group(1))
        note_body = match.group(2)
        # Skip system notes (id -1 and 0 are separator/continuationSeparator)
        if note_id <= 0:
            continue
        # Also skip if type="separator" or type="continuationSeparator"
        type_match = re.search(rf'w:type="(separator|continuationSeparator)"', match.group(0))
        if type_match:
            continue
        # Extract text from <w:t> elements
        text_parts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', note_body)
        full_text = ''.join(text_parts).strip()
        notes.append({'id': note_id, 'text': full_text})
    return notes


def get_note_references_context(zf):
    """Extract footnote and endnote reference positions from document.xml body."""
    content = zf.read('word/document.xml').decode('utf-8')
    result = {'footnote_refs': [], 'endnote_refs': []}

    # For footnote references, find surrounding text context
    for match in re.finditer(r'<w:footnoteReference\s+w:id="(\d+)"/>', content):
        note_id = int(match.group(1))
        # Get surrounding context (300 chars before)
        start = max(0, match.start() - 500)
        context_before = content[start:match.start()]
        # Extract text from <w:t> in context
        texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', context_before)
        text_before = ''.join(texts)
        result['footnote_refs'].append({'id': note_id, 'text_before': text_before})

    for match in re.finditer(r'<w:endnoteReference\s+w:id="(\d+)"/>', content):
        note_id = int(match.group(1))
        start = max(0, match.start() - 500)
        context_before = content[start:match.start()]
        texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', context_before)
        text_before = ''.join(texts)
        result['endnote_refs'].append({'id': note_id, 'text_before': text_before})

    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Footnote with correct text exists (0.3 points)
    try:
        footnotes = get_note_texts(zf, 'word/footnotes.xml', 'footnote')
        footnote_found = False
        for fn in footnotes:
            # Check if text matches (allow minor variations)
            if 'p-hacking' in fn['text'].lower() and 'misuse' in fn['text'].lower() and 'statistically significant' in fn['text'].lower():
                footnote_found = True
                print(f"PASS: Component 1 — Footnote found with correct text: '{fn['text'][:80]}...' (0.3 pts)")
                total_score += 0.3
                break
        if not footnote_found:
            if footnotes:
                print(f"FAIL: Component 1 — Footnotes found but none match expected text. Found: {[fn['text'][:60] for fn in footnotes]}")
            else:
                print("FAIL: Component 1 — No user footnotes found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Endnote with correct text exists (0.3 points)
    try:
        endnotes = get_note_texts(zf, 'word/endnotes.xml', 'endnote')
        endnote_found = False
        for en in endnotes:
            # Check key parts of the reference
            if 'simmons' in en['text'].lower() and 'false-positive' in en['text'].lower() and 'psychological science' in en['text'].lower():
                endnote_found = True
                print(f"PASS: Component 2 — Endnote found with correct text: '{en['text'][:80]}...' (0.3 pts)")
                total_score += 0.3
                break
        if not endnote_found:
            if endnotes:
                print(f"FAIL: Component 2 — Endnotes found but none match expected text. Found: {[en['text'][:60] for en in endnotes]}")
            else:
                print("FAIL: Component 2 — No user endnotes found in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footnote reference placed near 'p-hacking' in body text (0.2 points)
    try:
        refs = get_note_references_context(zf)
        fn_ref_correct = False
        for ref in refs['footnote_refs']:
            text_before = ref['text_before']
            # The footnote should be placed after 'p-hacking' in the paragraph
            if 'p-hacking' in text_before.lower():
                fn_ref_correct = True
                print(f"PASS: Component 3 — Footnote reference placed after 'p-hacking' in body (0.2 pts)")
                total_score += 0.2
                break
        if not fn_ref_correct:
            if refs['footnote_refs']:
                print(f"FAIL: Component 3 — Footnote reference exists but not placed near 'p-hacking'. Context: '{refs['footnote_refs'][0]['text_before'][-60:]}'")
            else:
                print("FAIL: Component 3 — No footnote references found in document body")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Endnote reference placed near '(Simmons et al., 2011)' in body text (0.2 points)
    try:
        en_ref_correct = False
        for ref in refs['endnote_refs']:
            text_before = ref['text_before']
            # The endnote should be placed after 'Simmons et al., 2011' or '(Simmons et al., 2011)'
            if 'simmons' in text_before.lower() and '2011' in text_before:
                en_ref_correct = True
                print(f"PASS: Component 4 — Endnote reference placed after '(Simmons et al., 2011)' in body (0.2 pts)")
                total_score += 0.2
                break
        if not en_ref_correct:
            if refs['endnote_refs']:
                print(f"FAIL: Component 4 — Endnote reference exists but not placed near 'Simmons et al., 2011'. Context: '{refs['endnote_refs'][0]['text_before'][-60:]}'")
            else:
                print("FAIL: Component 4 — No endnote references found in document body")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Main entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
