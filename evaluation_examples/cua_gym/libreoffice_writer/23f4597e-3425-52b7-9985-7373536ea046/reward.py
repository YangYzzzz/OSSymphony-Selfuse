"""
Reward Script: Insert three footnotes in the Introduction paragraph
Task ID: writer_bs_017
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.3): Three footnotes exist in the document
  - Component 2 (0.3): Footnote texts match expected content
  - Component 3 (0.2): Footnote references are in the Introduction paragraph
  - Component 4 (0.2): Footnotes are in correct order (machine learning, LeCun, Goodfellow)
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_017'


def persist_app_state(domain):
    """Save any open LibreOffice document before verification."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_footnotes_from_zip(file_path):
    """Extract footnote data from docx zip structure using recover parser."""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    footnotes = []

    with zipfile.ZipFile(file_path, 'r') as z:
        if 'word/footnotes.xml' not in z.namelist():
            return footnotes

        content = z.read('word/footnotes.xml')
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(content, parser=parser)

        for fn in root.findall('w:footnote', ns):
            fn_id = fn.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
            fn_type = fn.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type', 'normal')
            if fn_type != 'normal':
                continue
            text_parts = []
            for t in fn.findall('.//w:t', ns):
                text_parts.append(t.text or '')
            full_text = ''.join(text_parts).strip()
            footnotes.append({'id': fn_id, 'text': full_text})

    return footnotes


def get_footnote_refs_in_paragraphs(file_path):
    """Get footnote reference ids and their parent paragraph indices."""
    from docx import Document

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    doc = Document(file_path)
    body = doc.element.body
    all_paras = body.findall('w:p', ns)

    refs_by_para = {}
    for p_idx, para_elem in enumerate(all_paras):
        refs = para_elem.findall('.//w:footnoteReference', ns)
        for ref in refs:
            fid = ref.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
            if fid:
                if p_idx not in refs_by_para:
                    refs_by_para[p_idx] = []
                refs_by_para[p_idx].append(fid)

    # Also get paragraph texts for identification
    para_texts = []
    for p in doc.paragraphs:
        para_texts.append(p.text if p.text else '')

    return refs_by_para, para_texts


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

    # Get footnotes from zip
    try:
        footnotes = get_footnotes_from_zip(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read footnotes from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get footnote references in body
    try:
        refs_by_para, para_texts = get_footnote_refs_in_paragraphs(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot read document structure: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Total footnote refs across all paragraphs
    all_ref_ids = []
    for p_idx in sorted(refs_by_para.keys()):
        all_ref_ids.extend(refs_by_para[p_idx])

    # Component 1: Three footnotes exist in the document (0.3 points)
    try:
        num_footnotes = len(footnotes)
        num_refs = len(all_ref_ids)
        if num_footnotes == 3 and num_refs == 3:
            print(f"PASS: Component 1 - Found 3 footnotes and 3 references (0.3 pts)")
            total_score += 0.3
        elif num_footnotes >= 1 or num_refs >= 1:
            # Partial credit: at least some footnotes exist
            partial = 0.1 * min(num_footnotes, 3)
            print(f"FAIL: Component 1 - Found {num_footnotes} footnotes and {num_refs} refs, expected 3 each (partial: {partial:.1f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No footnotes found in document")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Footnote texts match expected content (0.3 points)
    # Expected texts from task context
    expected_texts = [
        "Machine learning is a subset of artificial intelligence.",
        "See LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998).",
        "See Goodfellow, I., Bengio, Y., & Courville, A. (2016).",
    ]
    # Key phrases that must appear (more flexible matching)
    key_phrases = [
        ["machine learning", "subset", "artificial intelligence"],
        ["lecun", "1998"],
        ["goodfellow", "2016"],
    ]
    try:
        matched_count = 0
        for i, phrases in enumerate(key_phrases):
            found_match = False
            for fn in footnotes:
                fn_lower = fn['text'].lower()
                if all(phrase in fn_lower for phrase in phrases):
                    found_match = True
                    break
            if found_match:
                matched_count += 1
                print(f"PASS: Component 2.{i+1} - Footnote about {phrases[0]} found")
            else:
                print(f"FAIL: Component 2.{i+1} - No footnote matching {phrases}")

        comp2_score = (matched_count / 3) * 0.3
        if matched_count == 3:
            print(f"PASS: Component 2 - All 3 footnote texts match ({comp2_score:.1f} pts)")
        else:
            print(f"FAIL: Component 2 - Only {matched_count}/3 footnote texts match ({comp2_score:.2f} pts)")
        total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Footnote references are in the Introduction paragraph (0.2 points)
    # The Introduction paragraph contains "machine learning", "neural networks", "deep learning"
    try:
        intro_para_idx = None
        for idx, txt in enumerate(para_texts):
            if 'machine learning' in txt.lower():
                # Further confirm it's the Introduction paragraph
                intro_para_idx = idx
                break

        if intro_para_idx is not None and intro_para_idx in refs_by_para:
            refs_in_intro = refs_by_para[intro_para_idx]
            if len(refs_in_intro) == 3:
                print(f"PASS: Component 3 - All 3 footnote refs are in Introduction paragraph (para {intro_para_idx}) (0.2 pts)")
                total_score += 0.2
            elif len(refs_in_intro) >= 1:
                partial = (len(refs_in_intro) / 3) * 0.2
                print(f"FAIL: Component 3 - Only {len(refs_in_intro)}/3 refs in Introduction paragraph ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 - No footnote refs in Introduction paragraph")
        elif intro_para_idx is None:
            print(f"FAIL: Component 3 - Could not identify Introduction paragraph")
        else:
            # Check if refs are in any paragraph
            total_refs = len(all_ref_ids)
            if total_refs > 0:
                print(f"FAIL: Component 3 - {total_refs} refs found but not in Introduction paragraph (para indices with refs: {list(refs_by_para.keys())})")
            else:
                print(f"FAIL: Component 3 - No footnote references found in body")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Footnotes are in correct order (0.2 points)
    # Footnote 1 = machine learning, Footnote 2 = LeCun, Footnote 3 = Goodfellow
    try:
        if len(footnotes) >= 3:
            fn_by_id = {fn['id']: fn['text'] for fn in footnotes}
            order_correct = 0

            # Check footnote id=1 is about machine learning
            if '1' in fn_by_id and 'machine learning' in fn_by_id['1'].lower():
                order_correct += 1
                print(f"PASS: Component 4.1 - Footnote 1 is about machine learning")
            else:
                fn1_text = fn_by_id.get('1', 'N/A')
                print(f"FAIL: Component 4.1 - Footnote 1 text: {repr(fn1_text[:80])}")

            # Check footnote id=2 is about LeCun
            if '2' in fn_by_id and 'lecun' in fn_by_id['2'].lower():
                order_correct += 1
                print(f"PASS: Component 4.2 - Footnote 2 references LeCun")
            else:
                fn2_text = fn_by_id.get('2', 'N/A')
                print(f"FAIL: Component 4.2 - Footnote 2 text: {repr(fn2_text[:80])}")

            # Check footnote id=3 is about Goodfellow
            if '3' in fn_by_id and 'goodfellow' in fn_by_id['3'].lower():
                order_correct += 1
                print(f"PASS: Component 4.3 - Footnote 3 references Goodfellow")
            else:
                fn3_text = fn_by_id.get('3', 'N/A')
                print(f"FAIL: Component 4.3 - Footnote 3 text: {repr(fn3_text[:80])}")

            comp4_score = (order_correct / 3) * 0.2
            if order_correct == 3:
                print(f"PASS: Component 4 - All footnotes in correct order ({comp4_score:.1f} pts)")
            else:
                print(f"FAIL: Component 4 - Only {order_correct}/3 in correct order ({comp4_score:.2f} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 - Not enough footnotes ({len(footnotes)}) to check order")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
