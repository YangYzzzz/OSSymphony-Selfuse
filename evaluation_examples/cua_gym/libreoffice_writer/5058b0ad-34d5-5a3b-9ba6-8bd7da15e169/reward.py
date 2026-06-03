"""
Reward Script: Insert image with Through wrap and 0.3cm spacing
Task ID: writer_frd_080
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Image inserted as anchored drawing
  Component 2 (0.3): Wrap type is Through (wrapThrough)
  Component 3 (0.4): Spacing 0.3cm on all four sides (108000 EMU each)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_080'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        import time
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for %s" % domain)
    except Exception as e:
        print("PERSIST_WARN: save hook failed: %s" % e)


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
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    }

    body = doc.element.body

    # Component 1: Image inserted as anchored drawing (0.3 points)
    # Initial doc has 0 drawings; golden has 1 anchor drawing with an image
    try:
        drawings = body.findall('.//w:drawing', ns)
        anchor_count = 0
        anchors = []
        for d in drawings:
            anc_list = d.findall('.//wp:anchor', ns)
            anchor_count += len(anc_list)
            anchors.extend(anc_list)

        # Also check that there is at least one image relationship
        image_rels = [r for r in doc.part.rels.values() if 'image' in r.reltype]

        if anchor_count >= 1 and len(image_rels) >= 1:
            print("PASS: Component 1 -- Image inserted as anchored drawing (anchor=%d, image_rels=%d) (0.3 pts)" % (anchor_count, len(image_rels)))
            total_score += 0.3
        else:
            print("FAIL: Component 1 -- Expected anchored image drawing. anchor=%d, image_rels=%d" % (anchor_count, len(image_rels)))
    except Exception as e:
        print("ERROR: Component 1 -- %s" % e)
        anchors = []

    # Component 2: Wrap type is Through (wrapThrough) (0.3 points)
    # Initial doc has no drawings at all, so this will fail on initial
    try:
        wrap_through_found = False
        for anc in anchors:
            wt = anc.findall('wp:wrapThrough', ns)
            if len(wt) > 0:
                wrap_through_found = True
                break

        if wrap_through_found:
            print("PASS: Component 2 -- Wrap type is Through (wrapThrough found) (0.3 pts)")
            total_score += 0.3
        else:
            # Check what wrap type is present for debug info
            wrap_types_found = []
            for anc in anchors:
                for wtype in ['wrapThrough', 'wrapTight', 'wrapSquare', 'wrapNone', 'wrapTopAndBottom']:
                    if anc.findall('wp:' + wtype, ns):
                        wrap_types_found.append(wtype)
            print("FAIL: Component 2 -- Expected wrapThrough, found: %s" % (wrap_types_found if wrap_types_found else 'no anchors/no wrap'))
    except Exception as e:
        print("ERROR: Component 2 -- %s" % e)

    # Component 3: Spacing 0.3cm on all four sides (0.4 points)
    # 0.3cm = 108000 EMU. Allow small tolerance (within 5000 EMU ~ 0.014cm)
    # Initial doc has no anchor at all, so this fails on initial
    EXPECTED_EMU = 108000
    TOLERANCE = 5000
    try:
        spacing_ok = False
        if anchors:
            anc = anchors[0]
            dist_attrs = {
                'distT': anc.get('distT'),
                'distB': anc.get('distB'),
                'distL': anc.get('distL'),
                'distR': anc.get('distR'),
            }

            all_match = True
            details = []
            for attr_name, val_str in dist_attrs.items():
                if val_str is None:
                    all_match = False
                    details.append("%s=None" % attr_name)
                else:
                    val = int(val_str)
                    diff = abs(val - EXPECTED_EMU)
                    if diff <= TOLERANCE:
                        details.append("%s=%d OK" % (attr_name, val))
                    else:
                        all_match = False
                        details.append("%s=%d (expected ~%d)" % (attr_name, val, EXPECTED_EMU))

            if all_match:
                print("PASS: Component 3 -- All spacing 0.3cm (%s) (0.4 pts)" % ', '.join(details))
                total_score += 0.4
                spacing_ok = True
            else:
                # Partial credit: award 0.1 per correct side
                correct_sides = 0
                for attr_name, val_str in dist_attrs.items():
                    if val_str is not None and abs(int(val_str) - EXPECTED_EMU) <= TOLERANCE:
                        correct_sides += 1
                partial = correct_sides * 0.1
                if partial > 0:
                    print("PARTIAL: Component 3 -- %d/4 sides correct (%s) (%.1f pts)" % (correct_sides, ', '.join(details), partial))
                    total_score += partial
                else:
                    print("FAIL: Component 3 -- Spacing incorrect (%s)" % ', '.join(details))
        else:
            print("FAIL: Component 3 -- No anchor element found to check spacing")
    except Exception as e:
        print("ERROR: Component 3 -- %s" % e)

    final_score = round(min(total_score, 1.0), 1)
    print("")
    print("Score: %.1f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = '%s/%s.docx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
