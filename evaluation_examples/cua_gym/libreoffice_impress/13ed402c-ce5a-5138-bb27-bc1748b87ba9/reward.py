"""
Reward Script: Add hyperlink in notes of slide 5
Task ID: impress_ndo_018
Domain: libreoffice_impress
Scoring:
  Component 1 (0.40): Display text 'See reference material' exists in slide 5 notes
  Component 2 (0.40): Hyperlink URL 'https://example.com/reference' attached to that text
  Component 3 (0.20): Original text preserved AND hyperlink text present (compound check)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ndo_018'

def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
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


def get_notes_slide_index_for_slide(pptx_path, slide_num):
    """
    Find which notesSlide XML file corresponds to a given slide number.
    slide_num is 1-based (slide 5 -> slide5.xml).
    Returns the notesSlide filename (e.g., 'notesSlide4') or None.
    """
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            rels_path = f'ppt/slides/_rels/slide{slide_num}.xml.rels'
            with zf.open(rels_path) as f:
                content = f.read().decode()
                root = ET.fromstring(content)
                ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
                for rel in root.findall('r:Relationship', ns):
                    target = rel.get('Target', '')
                    if 'notesSlide' in target:
                        basename = target.split('/')[-1].replace('.xml', '')
                        return basename
    except Exception as e:
        print(f"ERROR: Could not find notes slide mapping for slide {slide_num}: {e}")
    return None


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

    # Find which notesSlide XML corresponds to slide 5
    notes_slide_name = get_notes_slide_index_for_slide(file_path, 5)
    if notes_slide_name is None:
        print("CRITICAL: Slide 5 has no notes slide")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Slide 5 maps to {notes_slide_name}.xml")

    # Parse the notes slide XML and its rels
    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    ns_pkg = 'http://schemas.openxmlformats.org/package/2006/relationships'

    notes_xml_path = f'ppt/notesSlides/{notes_slide_name}.xml'
    rels_xml_path = f'ppt/notesSlides/_rels/{notes_slide_name}.xml.rels'

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open(notes_xml_path) as f:
                notes_root = ET.parse(f).getroot()

            hyperlink_map = {}
            try:
                with zf.open(rels_xml_path) as f:
                    rels_root = ET.fromstring(f.read().decode())
                    for rel in rels_root.findall(f'{{{ns_pkg}}}Relationship'):
                        rel_type = rel.get('Type', '')
                        if 'hyperlink' in rel_type:
                            rid = rel.get('Id', '')
                            target = rel.get('Target', '')
                            hyperlink_map[rid] = target
            except KeyError:
                print("WARN: No rels file found for notes slide")
    except Exception as e:
        print(f"CRITICAL: Cannot parse pptx: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(hyperlink_map)} hyperlink(s) in notes rels: {hyperlink_map}")

    # Find the notes body placeholder (type="body")
    body_shape = None
    for sp in notes_root.findall(f'.//{{{ns_p}}}sp'):
        ph = sp.find(f'.//{{{ns_p}}}ph')
        if ph is not None and ph.get('type') == 'body':
            body_shape = sp
            break

    if body_shape is None:
        print("CRITICAL: No notes body placeholder found in slide 5")
        print("REWARD: 0.0")
        return 0.0

    # Extract all paragraphs with their text and hyperlink info
    paragraphs = []
    for para in body_shape.findall(f'.//{{{ns_a}}}p'):
        runs = []
        for run in para.findall(f'{{{ns_a}}}r'):
            text_el = run.find(f'{{{ns_a}}}t')
            text = text_el.text if text_el is not None else ''
            rpr = run.find(f'{{{ns_a}}}rPr')
            hlink_rid = None
            if rpr is not None:
                hlink = rpr.find(f'{{{ns_a}}}hlinkClick')
                if hlink is not None:
                    hlink_rid = hlink.get(f'{{{ns_r}}}id')
            runs.append({
                'text': text or '',
                'hlink_rid': hlink_rid,
                'hlink_url': hyperlink_map.get(hlink_rid) if hlink_rid else None,
            })
        para_text = ''.join(r['text'] for r in runs)
        paragraphs.append({'text': para_text, 'runs': runs})

    print(f"INFO: Notes paragraphs: {[p['text'] for p in paragraphs]}")

    # Precondition gate: original notes text must still exist (not a scoring component)
    original_text = 'Cite the following source during this section.'
    original_preserved = any(original_text in p['text'] for p in paragraphs)
    if not original_preserved:
        print(f"PRECONDITION FAIL: Original notes text was overwritten/deleted. Returning 0.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Display text 'See reference material' exists in slide 5 notes (0.40 points)
    # This is a task-introduced change: initial has no such text.
    display_text_found = False
    try:
        for para in paragraphs:
            for run in para['runs']:
                if 'See reference material' in run['text']:
                    display_text_found = True
                    break
            if not display_text_found and 'See reference material' in para['text']:
                display_text_found = True
            if display_text_found:
                break

        if display_text_found:
            print(f"PASS: Component 1 - Display text 'See reference material' found in slide 5 notes (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 - Display text 'See reference material' NOT found in slide 5 notes")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Hyperlink URL 'https://example.com/reference' attached to 'See reference material' (0.40 points)
    # This is a task-introduced change: initial has no hyperlinks in notes.
    hyperlink_correct = False
    try:
        for para in paragraphs:
            for run in para['runs']:
                if 'See reference material' in run['text'] and run['hlink_url'] is not None:
                    actual_url = run['hlink_url']
                    if actual_url == 'https://example.com/reference':
                        hyperlink_correct = True
                        print(f"INFO: Hyperlink URL matches: {actual_url}")
                    else:
                        print(f"INFO: Hyperlink URL mismatch: expected 'https://example.com/reference', found '{actual_url}'")

        if hyperlink_correct:
            print(f"PASS: Component 2 - Hyperlink 'https://example.com/reference' correctly linked (0.40 pts)")
            total_score += 0.40
        else:
            any_correct_url = any(url == 'https://example.com/reference' for url in hyperlink_map.values())
            if any_correct_url:
                print(f"FAIL: Component 2 - URL exists in rels but not attached to 'See reference material' text")
            else:
                print(f"FAIL: Component 2 - No hyperlink to 'https://example.com/reference' found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Original text preserved AND hyperlink display text present (0.20 points)
    # Compound check: both conditions must hold. The original text alone is a precondition (true in both).
    # This component is anchored to the task change because it requires BOTH the original text AND the new display text.
    try:
        if original_preserved and display_text_found:
            print(f"PASS: Component 3 - Original notes preserved AND hyperlink display text present (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - original_preserved={original_preserved}, display_text_found={display_text_found}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
