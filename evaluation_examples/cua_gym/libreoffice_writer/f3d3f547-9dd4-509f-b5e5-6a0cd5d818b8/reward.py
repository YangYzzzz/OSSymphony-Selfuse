"""
Reward Script: Insert footnote at the end of a specific sentence
Task ID: writer_acad_006
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): A footnote exists in the document (footnotes.xml has user footnote)
  Component 2 (0.35): Footnote text matches expected content about Journal of Applied Psychology
  Component 3 (0.25): Footnote reference is placed near the target sentence ("This theory was first proposed in 1987.")
"""

import os
import zipfile
import re
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_006'

# Namespace for OOXML word processing
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}

# Expected footnote text (from task context)
EXPECTED_FOOTNOTE_TEXT = "The original paper was published in the Journal of Applied Psychology, Vol. 72, pp. 212-220."
# Target sentence where footnote should be placed
TARGET_SENTENCE = "This theory was first proposed in 1987."


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_footnotes_from_zip(file_path):
    """Extract footnote data from the docx zip archive."""
    footnotes = []
    with zipfile.ZipFile(file_path) as z:
        if 'word/footnotes.xml' not in z.namelist():
            return footnotes
        fn_xml = z.read('word/footnotes.xml')
        root = etree.fromstring(fn_xml)
        for fn in root.findall('w:footnote', NS):
            fn_type = fn.get(f'{{{WNS}}}type')
            fn_id = fn.get(f'{{{WNS}}}id')
            # Skip separator and continuationSeparator (system footnotes)
            if fn_type in ('separator', 'continuationSeparator'):
                continue
            # Extract all text from the footnote
            texts = []
            for t_elem in fn.findall('.//w:t', NS):
                if t_elem.text:
                    texts.append(t_elem.text)
            footnote_text = ''.join(texts).strip()
            footnotes.append({'id': fn_id, 'text': footnote_text})
    return footnotes


def get_footnote_ref_context(file_path):
    """Find the text context surrounding footnote references in document.xml."""
    contexts = []
    with zipfile.ZipFile(file_path) as z:
        body_xml = z.read('word/document.xml')
        root = etree.fromstring(body_xml)
        # Find all paragraphs containing footnoteReference
        for para in root.findall('.//w:p', NS):
            refs = para.findall('.//w:footnoteReference', NS)
            if refs:
                # Get full paragraph text
                para_texts = []
                for t_elem in para.findall('.//w:t', NS):
                    if t_elem.text:
                        para_texts.append(t_elem.text)
                para_text = ''.join(para_texts)
                ref_ids = [r.get(f'{{{WNS}}}id') for r in refs]
                contexts.append({'para_text': para_text, 'ref_ids': ref_ids})
    return contexts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: A user-defined footnote exists in the document (0.40 points)
    try:
        footnotes = get_footnotes_from_zip(file_path)
        if len(footnotes) > 0:
            print(f"PASS: Component 1 — Found {len(footnotes)} user footnote(s) (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — No user footnotes found in document")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Footnote text matches expected content (0.35 points)
    try:
        footnotes = get_footnotes_from_zip(file_path)
        found_match = False
        for fn in footnotes:
            fn_text = fn['text']
            # Normalize whitespace for comparison
            fn_text_norm = re.sub(r'\s+', ' ', fn_text).strip()
            expected_norm = re.sub(r'\s+', ' ', EXPECTED_FOOTNOTE_TEXT).strip()
            if expected_norm.lower() in fn_text_norm.lower() or fn_text_norm.lower() in expected_norm.lower():
                found_match = True
                print(f"PASS: Component 2 — Footnote text matches: '{fn_text_norm[:80]}...' (0.35 pts)")
                total_score += 0.35
                break
            # Also check for partial match: key terms present
            elif ('journal of applied psychology' in fn_text_norm.lower()
                  and 'vol. 72' in fn_text_norm.lower()
                  and '212' in fn_text_norm):
                found_match = True
                print(f"PASS: Component 2 — Footnote text contains key terms (partial match): '{fn_text_norm[:80]}' (0.35 pts)")
                total_score += 0.35
                break
        if not found_match:
            fn_texts = [fn['text'] for fn in footnotes]
            print(f"FAIL: Component 2 — No footnote matches expected text. Found: {fn_texts}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footnote reference is placed near the target sentence (0.25 points)
    try:
        contexts = get_footnote_ref_context(file_path)
        found_in_context = False
        for ctx in contexts:
            para_text = ctx['para_text']
            # Check if the target sentence appears in the paragraph containing the footnote ref
            if TARGET_SENTENCE.lower().rstrip('.') in para_text.lower():
                found_in_context = True
                print(f"PASS: Component 3 — Footnote ref found in paragraph containing '{TARGET_SENTENCE[:50]}' (0.25 pts)")
                total_score += 0.25
                break
        if not found_in_context:
            para_texts = [ctx['para_text'][:80] for ctx in contexts]
            print(f"FAIL: Component 3 — Footnote ref not in paragraph with target sentence. Ref paragraphs: {para_texts}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_writer")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
