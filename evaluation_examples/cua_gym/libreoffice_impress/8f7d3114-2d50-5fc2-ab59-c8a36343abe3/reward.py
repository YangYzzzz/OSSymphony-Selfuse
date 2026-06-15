"""
Reward Script: Apply a tiled background image to slide 7 using ~/Pictures/small_pattern.png
Task ID: impress_el_074
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): Slide 7 has a picture/image background (not inherited/blank)
  Component 2 (0.4): Background uses tile fill mode (not stretch)
  Component 3 (0.3): The background image matches small_pattern.png
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_el_074'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid zip (pptx)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: presentation must have at least 7 slides
    try:
        from pptx import Presentation
        prs = Presentation(file_path)
        num_slides = len(prs.slides)
        if num_slides < 7:
            print(f"CRITICAL: Only {num_slides} slides, need at least 7")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load presentation: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse slide 7 XML for background analysis
    bg_element = None
    blipFill = None
    tile_element = None
    blip_rId = None

    try:
        with zf.open('ppt/slides/slide7.xml') as f:
            root = ET.parse(f).getroot()
        bg_element = root.find('.//p:bg', NS)
    except Exception as e:
        print(f"ERROR: Cannot parse slide7.xml: {e}")

    # Component 1: Slide 7 has a picture/image background (0.3 points)
    # This checks that a background element with blipFill exists on slide 7.
    # Initial state has NO bg element (inherits from master), so this FAILS on initial.
    try:
        if bg_element is not None:
            blipFill = bg_element.find('.//a:blipFill', NS)
            if blipFill is not None:
                print("PASS: Component 1 — Slide 7 has a blipFill (image) background (0.3 pts)")
                total_score += 0.3
            else:
                # Check if there's a solid fill or gradient instead of image
                solidFill = bg_element.find('.//a:solidFill', NS)
                gradFill = bg_element.find('.//a:gradFill', NS)
                if solidFill is not None:
                    print("FAIL: Component 1 — Slide 7 has solid fill background, not image")
                elif gradFill is not None:
                    print("FAIL: Component 1 — Slide 7 has gradient fill background, not image")
                else:
                    print("FAIL: Component 1 — Slide 7 background exists but no blipFill found")
        else:
            print("FAIL: Component 1 — Slide 7 has no explicit background element (inherits from master)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Background uses tile fill mode (0.4 points)
    # The task requires tiled/repeated pattern. A tile element must exist within blipFill.
    # Stretch fill would be wrong (single image scaled to fill).
    try:
        if blipFill is not None:
            tile_element = blipFill.find('a:tile', NS)
            stretch_element = blipFill.find('a:stretch', NS)
            if tile_element is not None:
                print("PASS: Component 2 — Background uses tile (repeat) fill mode (0.4 pts)")
                total_score += 0.4
            elif stretch_element is not None:
                print("FAIL: Component 2 — Background uses stretch fill, not tile/repeat")
            else:
                print("FAIL: Component 2 — Background blipFill has neither tile nor stretch")
        else:
            print("FAIL: Component 2 — No blipFill to check for tile mode")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The background image matches small_pattern.png (0.3 points)
    # Verify the embedded image is the same file as ~/Pictures/small_pattern.png
    try:
        if blipFill is not None:
            blip = blipFill.find('a:blip', NS)
            if blip is not None:
                blip_rId = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                if blip_rId:
                    # Resolve the relationship to find the media file path
                    rels_path = 'ppt/slides/_rels/slide7.xml.rels'
                    target = None
                    try:
                        with zf.open(rels_path) as rf:
                            rels_root = ET.parse(rf).getroot()
                        for rel in rels_root:
                            if rel.get('Id') == blip_rId:
                                target = rel.get('Target')
                                break
                    except Exception as e:
                        print(f"ERROR: Component 3 — Cannot read rels: {e}")

                    if target:
                        # Resolve relative path (../media/xxx.png -> ppt/media/xxx.png)
                        media_path = os.path.normpath(os.path.join('ppt/slides', target))
                        try:
                            embedded_blob = zf.read(media_path)
                        except KeyError:
                            # Try without normpath
                            media_path = 'ppt/media/' + os.path.basename(target)
                            embedded_blob = zf.read(media_path)

                        # Read the source pattern file
                        pattern_path = os.path.join(WORKDIR, 'Pictures', 'small_pattern.png')
                        if os.path.exists(pattern_path):
                            with open(pattern_path, 'rb') as pf:
                                pattern_blob = pf.read()
                            if embedded_blob == pattern_blob:
                                print(f"PASS: Component 3 — Embedded image matches small_pattern.png ({len(embedded_blob)} bytes) (0.3 pts)")
                                total_score += 0.3
                            else:
                                print(f"FAIL: Component 3 — Embedded image ({len(embedded_blob)} bytes) does not match small_pattern.png ({len(pattern_blob)} bytes)")
                        else:
                            print(f"FAIL: Component 3 — Reference file {pattern_path} not found on VM")
                    else:
                        print(f"FAIL: Component 3 — Could not resolve relationship {blip_rId}")
                else:
                    print("FAIL: Component 3 — blip element has no embed attribute")
            else:
                print("FAIL: Component 3 — No blip element found in blipFill")
        else:
            print("FAIL: Component 3 — No blipFill to check image")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
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
