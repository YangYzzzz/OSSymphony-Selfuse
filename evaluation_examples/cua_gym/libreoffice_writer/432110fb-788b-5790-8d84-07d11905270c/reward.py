"""
Reward Script: Change image text wrapping from inline to Parallel (square) wrap
Task ID: writer_frd_069
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Image is anchored (not inline)
  Component 2 (0.4): Wrap type is wrapSquare with wrapText=bothSides
  Component 3 (0.3): Spacing from text is ~0.2cm (72000 EMU) on all sides
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_069'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_writer")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    # Namespace map for XML parsing
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    }

    # Find all drawing elements
    body = doc.element.body
    drawings = body.findall('.//w:drawing', ns)

    if len(drawings) == 0:
        print("FAIL: No drawing/image elements found in document")
        print("REWARD: 0.0")
        return 0.0

    # We expect exactly one image; analyze the first drawing
    drawing = drawings[0]
    inlines = drawing.findall('.//wp:inline', ns)
    anchors = drawing.findall('.//wp:anchor', ns)

    # Component 1: Image is anchored (not inline) (0.3 points)
    # Initial state has inline; golden state has anchor.
    try:
        if len(anchors) > 0 and len(inlines) == 0:
            print(f"PASS: Component 1 -- Image is anchored (not inline) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- Image is still inline (inline={len(inlines)}, anchor={len(anchors)})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Wrap type is wrapSquare with wrapText=bothSides (0.4 points)
    # "Parallel" wrap in LibreOffice Writer = wrapSquare in OOXML, with text on both sides
    try:
        if len(anchors) > 0:
            anchor = anchors[0]
            wrap_square = anchor.findall('.//wp:wrapSquare', ns)
            if len(wrap_square) > 0:
                wrap_text = wrap_square[0].get('wrapText')
                if wrap_text == 'bothSides':
                    print(f"PASS: Component 2 -- wrapSquare with wrapText=bothSides (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 2 -- wrapSquare found but wrapText={wrap_text}, expected bothSides")
            else:
                # Check for other wrap types
                wrap_tight = anchor.findall('.//wp:wrapTight', ns)
                wrap_through = anchor.findall('.//wp:wrapThrough', ns)
                wrap_top_bottom = anchor.findall('.//wp:wrapTopAndBottom', ns)
                wrap_none = anchor.findall('.//wp:wrapNone', ns)
                found = 'tight' if wrap_tight else 'through' if wrap_through else 'topAndBottom' if wrap_top_bottom else 'none' if wrap_none else 'unknown'
                print(f"FAIL: Component 2 -- Expected wrapSquare, found wrap type: {found}")
        else:
            print(f"FAIL: Component 2 -- No anchor element; image is inline")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Spacing from text is ~0.2cm (72000 EMU) on all four sides (0.3 points)
    # Task context specifies 0.2cm on all sides. 0.2cm = 72000 EMU.
    # Tolerance: +/- 10000 EMU (~0.028cm) to allow slight rounding differences.
    try:
        if len(anchors) > 0:
            anchor = anchors[0]
            dist_t = int(anchor.get('distT', '0'))
            dist_b = int(anchor.get('distB', '0'))
            dist_l = int(anchor.get('distL', '0'))
            dist_r = int(anchor.get('distR', '0'))

            expected = 72000
            tolerance = 10000
            all_match = (
                abs(dist_t - expected) <= tolerance and
                abs(dist_b - expected) <= tolerance and
                abs(dist_l - expected) <= tolerance and
                abs(dist_r - expected) <= tolerance
            )

            if all_match:
                print(f"PASS: Component 3 -- Spacing ~0.2cm on all sides (T={dist_t}, B={dist_b}, L={dist_l}, R={dist_r}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- Spacing mismatch (expected ~72000 EMU). T={dist_t}, B={dist_b}, L={dist_l}, R={dist_r}")
        else:
            print(f"FAIL: Component 3 -- No anchor element; cannot check spacing")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'

persist_app_state('libreoffice_writer')

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
