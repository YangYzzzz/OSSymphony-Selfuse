"""
Reward Script: Set header logo image wrap to 'Behind Text'
Task ID: writer_frd_070
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.5): Image uses wp:anchor (not wp:inline) — i.e., it is floating
  - Component 2 (0.3): behindDoc="1" attribute set on the anchor — behind text mode
  - Component 3 (0.2): wp:wrapNone element present inside anchor — correct wrap style
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_070'

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
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


def verify_task(file_path):
    """
    Verify that the logo image in the document has 'Behind Text' wrapping.

    Initial state: image is wp:inline (no wrap / 'None' wrap).
    Golden state: image is wp:anchor with behindDoc="1" and wp:wrapNone.

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

    # Find all drawing elements in the document body
    body = doc.element.body
    drawings = body.findall('.//w:drawing', NS)

    if len(drawings) == 0:
        print("FAIL: No drawing elements found in document")
        print("REWARD: 0.0")
        return 0.0

    # We expect exactly one drawing (the logo image)
    drawing = drawings[0]

    # Component 1: Image uses wp:anchor (not wp:inline) — floating image (0.5 points)
    # In initial state, image is wp:inline. In golden state, it should be wp:anchor.
    try:
        anchors = drawing.findall('wp:anchor', NS)
        inlines = drawing.findall('wp:inline', NS)
        if len(anchors) > 0:
            print(f"PASS: Component 1 — Image is wp:anchor (floating), not inline (0.5 pts)")
            total_score += 0.5
        elif len(inlines) > 0:
            print(f"FAIL: Component 1 — Image is still wp:inline (not floating)")
        else:
            print(f"FAIL: Component 1 — Image has neither anchor nor inline element")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: behindDoc="1" attribute on the anchor (0.3 points)
    # This is the key attribute that makes it "Behind Text" wrapping
    try:
        if len(anchors) > 0:
            anchor = anchors[0]
            behind_doc = anchor.get('behindDoc')
            if behind_doc == '1':
                print(f"PASS: Component 2 — behindDoc='1' set on anchor (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — behindDoc='{behind_doc}', expected '1'")
        else:
            print(f"FAIL: Component 2 — No anchor element to check behindDoc on")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: wp:wrapNone element present (0.2 points)
    # "Behind Text" uses wrapNone (no text wrapping around the image)
    try:
        if len(anchors) > 0:
            anchor = anchors[0]
            wrap_none = anchor.findall('wp:wrapNone', NS)
            if len(wrap_none) > 0:
                print(f"PASS: Component 3 — wp:wrapNone present in anchor (0.2 pts)")
                total_score += 0.2
            else:
                # Check for other wrap types
                wrap_types = ['wp:wrapSquare', 'wp:wrapTight', 'wp:wrapThrough', 'wp:wrapTopAndBottom']
                found_wrap = None
                for wt in wrap_types:
                    if anchor.findall(wt, NS):
                        found_wrap = wt
                        break
                if found_wrap:
                    print(f"FAIL: Component 3 — Found {found_wrap} instead of wp:wrapNone")
                else:
                    print(f"FAIL: Component 3 — No wrap element found in anchor")
        else:
            print(f"FAIL: Component 3 — No anchor element to check wrap on")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before checking
persist_app_state("libreoffice_writer")

# Test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
