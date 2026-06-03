"""
Reward Script: Window envelope layout for delivery address
Task ID: writer_lec_062
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Address paragraphs have w:framePr elements
  Component 2 (0.25): Frame position ~5cm from left, ~4.5cm from top (page-anchored)
  Component 3 (0.25): Frame dimensions ~9cm wide, ~3cm tall
  Component 4 (0.20): All 5 address lines present in frame + page anchoring
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_062'

# Tolerance for position/size checks: 0.5 cm in EMU
CM_TO_EMU = 360000
TOLERANCE = int(0.5 * CM_TO_EMU)  # 0.5 cm tolerance

# Expected values from task
EXPECTED_X = int(5.0 * CM_TO_EMU)    # 5 cm from left
EXPECTED_Y = int(4.5 * CM_TO_EMU)    # 4.5 cm from top
EXPECTED_W = int(9.0 * CM_TO_EMU)    # 9 cm wide
EXPECTED_H = int(3.0 * CM_TO_EMU)    # 3 cm tall

# Known address lines from the letter
ADDRESS_KEYWORDS = ["vasquez", "director", "northfield", "commerce", "seattle"]


def find_framed_paragraphs(doc):
    """Find all paragraphs that have w:framePr and return their text + frame attributes."""
    body = doc.element.body
    framed = []
    for para_elem in body.findall(qn('w:p')):
        pPr = para_elem.find(qn('w:pPr'))
        if pPr is None:
            continue
        framePr = pPr.find(qn('w:framePr'))
        if framePr is None:
            continue
        # Extract text
        texts = [t.text or '' for t in para_elem.findall('.//' + qn('w:t'))]
        text = ''.join(texts)
        # Extract framePr attributes (strip namespace)
        attrs = {}
        for k, v in framePr.attrib.items():
            key = k.split('}')[-1] if '}' in k else k
            attrs[key] = v
        framed.append({'text': text, 'attrs': attrs})
    return framed


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

    framed = find_framed_paragraphs(doc)
    print(f"INFO: Found {len(framed)} framed paragraphs")
    for fp in framed:
        print(f"  Framed text: {fp['text']!r}, attrs: {fp['attrs']}")

    # Component 1: Address paragraphs have framePr elements (0.30 points)
    # The delivery address lines must be in a text frame, not at default position.
    try:
        # Check that at least 3 of the 5 address keywords appear in framed paragraphs
        framed_texts_lower = [fp['text'].lower() for fp in framed]
        matched_keywords = 0
        for kw in ADDRESS_KEYWORDS:
            if any(kw in t for t in framed_texts_lower):
                matched_keywords += 1
        print(f"INFO: Matched {matched_keywords}/{len(ADDRESS_KEYWORDS)} address keywords in frames")

        if matched_keywords >= 3:
            print(f"PASS: Component 1 — {matched_keywords} address lines in text frame (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Only {matched_keywords} address lines in frame, need >= 3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Components 2-4 require framed address paragraphs to exist
    if matched_keywords < 3:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Get frame attributes from the first framed address paragraph
    # Find the first framed paragraph that matches an address keyword
    frame_attrs = None
    for fp in framed:
        if any(kw in fp['text'].lower() for kw in ADDRESS_KEYWORDS):
            frame_attrs = fp['attrs']
            break

    if frame_attrs is None:
        print("FAIL: Could not find frame attributes for address block")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: Using frame attrs: {frame_attrs}")

    # Component 2: Frame position ~5cm from left, ~4.5cm from top (0.25 points)
    try:
        x_val = int(frame_attrs.get('x', '0'))
        y_val = int(frame_attrs.get('y', '0'))

        x_ok = abs(x_val - EXPECTED_X) <= TOLERANCE
        y_ok = abs(y_val - EXPECTED_Y) <= TOLERANCE

        x_cm = x_val / CM_TO_EMU
        y_cm = y_val / CM_TO_EMU

        if x_ok and y_ok:
            print(f"PASS: Component 2 — Frame position x={x_cm:.1f}cm, y={y_cm:.1f}cm (0.25 pts)")
            total_score += 0.25
        elif x_ok or y_ok:
            # Partial: one dimension correct
            print(f"PARTIAL: Component 2 — x={x_cm:.1f}cm ({'OK' if x_ok else 'WRONG'}), y={y_cm:.1f}cm ({'OK' if y_ok else 'WRONG'}) (0.125 pts)")
            total_score += 0.125
        else:
            print(f"FAIL: Component 2 — Frame position x={x_cm:.1f}cm (expected ~5.0cm), y={y_cm:.1f}cm (expected ~4.5cm)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Frame dimensions ~9cm wide, ~3cm tall (0.25 points)
    try:
        w_val = int(frame_attrs.get('w', '0'))
        h_val = int(frame_attrs.get('h', '0'))

        w_ok = abs(w_val - EXPECTED_W) <= TOLERANCE
        h_ok = abs(h_val - EXPECTED_H) <= TOLERANCE

        w_cm = w_val / CM_TO_EMU
        h_cm = h_val / CM_TO_EMU

        if w_ok and h_ok:
            print(f"PASS: Component 3 — Frame size w={w_cm:.1f}cm, h={h_cm:.1f}cm (0.25 pts)")
            total_score += 0.25
        elif w_ok or h_ok:
            print(f"PARTIAL: Component 3 — w={w_cm:.1f}cm ({'OK' if w_ok else 'WRONG'}), h={h_cm:.1f}cm ({'OK' if h_ok else 'WRONG'}) (0.125 pts)")
            total_score += 0.125
        else:
            print(f"FAIL: Component 3 — Frame size w={w_cm:.1f}cm (expected ~9.0cm), h={h_cm:.1f}cm (expected ~3.0cm)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All 5 address lines in frame + page anchoring (0.20 points)
    try:
        h_anchor = frame_attrs.get('hAnchor', '')
        v_anchor = frame_attrs.get('vAnchor', '')
        page_anchored = (h_anchor == 'page' and v_anchor == 'page')

        all_lines = matched_keywords == len(ADDRESS_KEYWORDS)

        if page_anchored and all_lines:
            print(f"PASS: Component 4 — All 5 address lines + page anchoring (0.20 pts)")
            total_score += 0.20
        elif page_anchored or all_lines:
            detail = f"page_anchored={page_anchored} (h={h_anchor},v={v_anchor}), all_lines={all_lines} ({matched_keywords}/5)"
            print(f"PARTIAL: Component 4 — {detail} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Not page-anchored (h={h_anchor},v={v_anchor}) and only {matched_keywords}/5 lines")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
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
