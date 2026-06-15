"""
Reward Script: Add footnotes with Roman numeral numbering to technical terms
Task ID: writer_rd_028
Domain: libreoffice_writer
Scoring:
  Component 1: Exactly 3 footnotes exist (0.30 pts)
  Component 2: Footnotes contain definitions for photosynthesis, mitochondria, ribosome (0.30 pts)
  Component 3: Footnote numbering format is lowerRoman (0.25 pts)
  Component 4: Footnote references attached near correct terms in body (0.15 pts)
"""

import os
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_028'

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def get_footnotes_from_zip(filepath):
    """Extract footnote data from the docx zip."""
    footnotes = []
    with zipfile.ZipFile(filepath, 'r') as z:
        if 'word/footnotes.xml' not in z.namelist():
            return footnotes
        fn_xml = z.read('word/footnotes.xml')
        tree = etree.fromstring(fn_xml)
        for fn in tree.findall('.//w:footnote', NS):
            fid = fn.get(f'{{{WNS}}}id')
            ftype = fn.get(f'{{{WNS}}}type', 'normal')
            if ftype != 'normal':
                continue
            texts = []
            for t in fn.findall('.//w:t', NS):
                if t.text:
                    texts.append(t.text)
            text = ''.join(texts).strip()
            footnotes.append({'id': fid, 'text': text})
    return footnotes


def get_footnote_numfmt(filepath):
    """Check if footnote numbering format is lowerRoman."""
    with zipfile.ZipFile(filepath, 'r') as z:
        # Check section-level footnotePr in document.xml
        if 'word/document.xml' in z.namelist():
            doc_xml = z.read('word/document.xml')
            doc_tree = etree.fromstring(doc_xml)
            for sect_pr in doc_tree.findall('.//w:sectPr', NS):
                for fn_pr in sect_pr.findall('w:footnotePr', NS):
                    num_fmt = fn_pr.find('w:numFmt', NS)
                    if num_fmt is not None:
                        return num_fmt.get(f'{{{WNS}}}val')
        # Check document-level settings
        if 'word/settings.xml' in z.namelist():
            settings_xml = z.read('word/settings.xml')
            settings_tree = etree.fromstring(settings_xml)
            for fn_pr in settings_tree.findall('.//w:footnotePr', NS):
                num_fmt = fn_pr.find('w:numFmt', NS)
                if num_fmt is not None:
                    return num_fmt.get(f'{{{WNS}}}val')
    return None


def get_footnote_ref_contexts(filepath):
    """Get the paragraph text surrounding each footnote reference."""
    contexts = []
    with zipfile.ZipFile(filepath, 'r') as z:
        if 'word/document.xml' not in z.namelist():
            return contexts
        doc_xml = z.read('word/document.xml')
        doc_tree = etree.fromstring(doc_xml)
        refs = doc_tree.findall('.//w:footnoteReference', NS)
        for ref in refs:
            fid = ref.get(f'{{{WNS}}}id')
            # Walk up to paragraph
            parent = ref.getparent()
            while parent is not None and parent.tag != f'{{{WNS}}}p':
                parent = parent.getparent()
            if parent is not None:
                texts = []
                for t in parent.findall('.//w:t', NS):
                    if t.text:
                        texts.append(t.text)
                para_text = ''.join(texts).lower()
                contexts.append({'id': fid, 'para_text': para_text})
    return contexts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must be a valid docx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        # Quick validity check
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'word/document.xml' not in z.namelist():
                print("CRITICAL: Not a valid docx file")
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot open file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 3 normal footnotes exist (0.30 points)
    try:
        footnotes = get_footnotes_from_zip(file_path)
        num_fn = len(footnotes)
        if num_fn == 3:
            print(f"PASS: Component 1 — Found exactly 3 footnotes (0.30 pts)")
            total_score += 0.30
        elif num_fn > 0:
            # Partial credit: at least some footnotes
            partial = min(num_fn / 3.0, 1.0) * 0.30
            print(f"PARTIAL: Component 1 — Found {num_fn} footnotes, expected 3 ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No footnotes found, expected 3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Footnotes contain definitions for the three terms (0.30 points)
    # Each term definition is worth 0.10 points
    try:
        footnotes = get_footnotes_from_zip(file_path)
        all_fn_text = ' '.join([fn['text'].lower() for fn in footnotes])

        terms_found = 0

        # Check for photosynthesis definition
        if 'photosynthesis' in all_fn_text and any(
            kw in all_fn_text for kw in ['light', 'energy', 'plant', 'carbon', 'chemical', 'organic', 'convert']
        ):
            print(f"PASS: Component 2a — Photosynthesis definition found (0.10 pts)")
            total_score += 0.10
            terms_found += 1
        else:
            print(f"FAIL: Component 2a — No adequate photosynthesis definition in footnotes")

        # Check for mitochondria definition
        if 'mitochondria' in all_fn_text and any(
            kw in all_fn_text for kw in ['atp', 'energy', 'organelle', 'cell', 'phosphorylation', 'powerhouse']
        ):
            print(f"PASS: Component 2b — Mitochondria definition found (0.10 pts)")
            total_score += 0.10
            terms_found += 1
        else:
            print(f"FAIL: Component 2b — No adequate mitochondria definition in footnotes")

        # Check for ribosome definition
        if 'ribosome' in all_fn_text and any(
            kw in all_fn_text for kw in ['protein', 'rna', 'translation', 'synthesis', 'mrna', 'polypeptide', 'molecular']
        ):
            print(f"PASS: Component 2c — Ribosome definition found (0.10 pts)")
            total_score += 0.10
            terms_found += 1
        else:
            print(f"FAIL: Component 2c — No adequate ribosome definition in footnotes")

        print(f"  Component 2 summary: {terms_found}/3 term definitions found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footnote numbering format is lowerRoman (0.25 points)
    try:
        num_fmt = get_footnote_numfmt(file_path)
        if num_fmt == 'lowerRoman':
            print(f"PASS: Component 3 — Footnote numbering is lowerRoman (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Footnote numFmt is '{num_fmt}', expected 'lowerRoman'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Footnote references are placed near the correct terms (0.15 points)
    # Each correctly placed ref is worth 0.05
    try:
        ref_contexts = get_footnote_ref_contexts(file_path)
        terms_placed = 0

        # Check if any footnote ref is in a paragraph mentioning photosynthesis
        if any('photosynthesis' in ctx['para_text'] for ctx in ref_contexts):
            print(f"PASS: Component 4a — Footnote ref near 'photosynthesis' (0.05 pts)")
            total_score += 0.05
            terms_placed += 1
        else:
            print(f"FAIL: Component 4a — No footnote ref in paragraph containing 'photosynthesis'")

        # Check mitochondria
        if any('mitochondria' in ctx['para_text'] or 'mitochondrial' in ctx['para_text'] for ctx in ref_contexts):
            print(f"PASS: Component 4b — Footnote ref near 'mitochondria' (0.05 pts)")
            total_score += 0.05
            terms_placed += 1
        else:
            print(f"FAIL: Component 4b — No footnote ref in paragraph containing 'mitochondria'")

        # Check ribosome
        if any('ribosome' in ctx['para_text'] for ctx in ref_contexts):
            print(f"PASS: Component 4c — Footnote ref near 'ribosome' (0.05 pts)")
            total_score += 0.05
            terms_placed += 1
        else:
            print(f"FAIL: Component 4c — No footnote ref in paragraph containing 'ribosome'")

        print(f"  Component 4 summary: {terms_placed}/3 correctly placed references")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
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


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
