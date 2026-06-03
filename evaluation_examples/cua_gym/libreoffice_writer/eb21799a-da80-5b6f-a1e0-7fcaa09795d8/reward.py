"""
Reward Script: Create envelope with delivery address from letter
Task ID: writer_lec_056
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Envelope section exists with correct dimensions
  Component 2 (0.4): Delivery address (Ms. Linda Park) present in envelope section
  Component 3 (0.3): Return address present in envelope section
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_056'


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes."""
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


def get_envelope_section_paras(doc):
    """
    Return (section_props, list_of_paragraph_texts) for the first section
    if it looks like an envelope (has a section break).
    We detect the envelope by looking for the first sectPr inside a paragraph's pPr.
    All paragraphs before (and including) that break belong to the envelope section.
    """
    body = doc.element.body
    envelope_para_elements = []
    envelope_sectPr = None

    for child in body:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag == 'p':
            envelope_para_elements.append(child)
            pPr = child.find(qn('w:pPr'))
            if pPr is not None:
                sectPr = pPr.find(qn('w:sectPr'))
                if sectPr is not None:
                    envelope_sectPr = sectPr
                    break
        else:
            # Non-paragraph element before any section break - just skip
            pass

    if envelope_sectPr is None:
        return None, []

    # Extract texts from envelope paragraphs
    texts = []
    for p_elem in envelope_para_elements:
        t_nodes = [node.text for node in p_elem.iter(qn('w:t')) if node.text]
        texts.append("".join(t_nodes).strip())

    return envelope_sectPr, texts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document must have at least 2 sections (envelope + letter)
    num_sections = len(doc.sections)
    if num_sections < 2:
        print(f"FAIL: Document has {num_sections} section(s), need at least 2 (envelope + letter)")
        print("REWARD: 0.0")
        return 0.0

    envelope_sectPr, envelope_texts = get_envelope_section_paras(doc)
    if envelope_sectPr is None:
        print("FAIL: No envelope section break found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Envelope section has correct envelope-like dimensions (0.3 points)
    # Standard #10 envelope: ~9.5 x 4.125 inches; other common sizes exist too
    # Key indicator: landscape orientation, width > height, height roughly 3.5-5 inches
    try:
        sec0 = doc.sections[0]
        w_in = sec0.page_width / 914400
        h_in = sec0.page_height / 914400

        # Envelope should be landscape-ish (wider than tall) and small height
        is_envelope_size = (w_in > h_in) and (h_in < 6.0) and (w_in > 6.0)

        if is_envelope_size:
            print(f"PASS: Component 1 -- Envelope section dimensions: {w_in:.2f}x{h_in:.2f} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- Section 0 dimensions {w_in:.2f}x{h_in:.2f} don't look like envelope")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Delivery address (Ms. Linda Park) present in envelope section (0.4 points)
    # The task requires the delivery address to be auto-populated from the letter's address block
    try:
        envelope_text_joined = "\n".join(envelope_texts).lower()

        required_delivery = [
            "linda park",
            "brightstar media",
            "456 sunset blvd",
            "los angeles",
            "90028",
        ]

        matches = sum(1 for item in required_delivery if item.lower() in envelope_text_joined)
        # Award partial: need at least 3 of 5 for any credit, all 5 for full
        if matches >= 5:
            print(f"PASS: Component 2 -- All 5 delivery address parts found in envelope (0.4 pts)")
            total_score += 0.4
        elif matches >= 3:
            partial = round(0.4 * (matches / 5), 2)
            print(f"PARTIAL: Component 2 -- {matches}/5 delivery address parts found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Only {matches}/5 delivery address parts found in envelope")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Return address present in envelope section (0.3 points)
    # The return address should come from sender/company info
    try:
        required_return = [
            "horizon creative",
            "1200 innovation",
            "san francisco",
        ]

        return_matches = sum(1 for item in required_return if item.lower() in envelope_text_joined)

        if return_matches >= 3:
            print(f"PASS: Component 3 -- Return address found in envelope (0.3 pts)")
            total_score += 0.3
        elif return_matches >= 1:
            partial = round(0.3 * (return_matches / 3), 2)
            print(f"PARTIAL: Component 3 -- {return_matches}/3 return address parts found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- Return address not found in envelope section")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
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
