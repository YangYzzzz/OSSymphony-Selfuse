"""
Reward Script: Set a tiled background image on the master slide using texture_bg.jpg
Task ID: impress_ma_016
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): Master slide background uses blipFill (image fill, not solid)
  Component 2 (0.3): The fill uses a tile element (tiled/bitmap pattern)
  Component 3 (0.2): Embedded image matches texture_bg.jpg from Desktop
  Component 4 (0.2): Presentation retains all 7 slides
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_016'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
}


def persist_app_state(domain):
    """Attempt to save any unsaved LibreOffice changes."""
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

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Master slide background uses blipFill (0.3 points)
    # Initial has solidFill; golden should have blipFill with an image reference
    try:
        master_xml = zf.open('ppt/slideMasters/slideMaster1.xml').read().decode('utf-8')
        master_root = ET.fromstring(master_xml)
        bg = master_root.find('.//p:cSld/p:bg', NS)
        if bg is None:
            print("FAIL: Component 1 -- No background element found on master slide")
        else:
            blip_fill = bg.find('.//a:blipFill', NS)
            solid_fill = bg.find('.//a:solidFill', NS)
            if blip_fill is not None:
                print(f"PASS: Component 1 -- Master slide has blipFill background (0.3 pts)")
                total_score += 0.3
            elif solid_fill is not None:
                print("FAIL: Component 1 -- Master slide still has solidFill (no image)")
            else:
                print("FAIL: Component 1 -- Master slide background is neither blipFill nor solidFill")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: The blipFill uses a tile element (0.3 points)
    # This means the image is tiled, not stretched. We look for a:tile inside a:blipFill.
    try:
        if blip_fill is not None:
            tile_elem = blip_fill.find('a:tile', NS)
            if tile_elem is not None:
                print(f"PASS: Component 2 -- Tile element present in blipFill (0.3 pts)")
                total_score += 0.3
            else:
                # Check for stretch as an alternative (wrong approach)
                stretch = blip_fill.find('a:stretch', NS)
                if stretch is not None:
                    print("FAIL: Component 2 -- Image is stretched, not tiled")
                else:
                    print("FAIL: Component 2 -- No tile or stretch element found in blipFill")
        else:
            print("FAIL: Component 2 -- No blipFill to check for tiling (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: The embedded image is texture_bg.jpg (0.2 points)
    # Verify that the blip references an image, and that image exists in the archive
    # and matches the source file on disk
    try:
        if blip_fill is not None:
            blip = blip_fill.find('a:blip', NS)
            if blip is not None:
                embed_id = blip.attrib.get(f'{{{NS["r"]}}}embed', '')
                if embed_id:
                    # Resolve the relationship to find the image path
                    rels_xml = zf.open('ppt/slideMasters/_rels/slideMaster1.xml.rels').read().decode('utf-8')
                    rels_root = ET.fromstring(rels_xml)
                    image_target = None
                    for rel in rels_root:
                        if rel.attrib.get('Id') == embed_id:
                            image_target = rel.attrib.get('Target', '')
                            break

                    if image_target:
                        # Normalize the path (target is relative like ../media/texture_bg.jpg)
                        # Resolve relative to ppt/slideMasters/
                        if image_target.startswith('..'):
                            image_zip_path = 'ppt/' + image_target.lstrip('.').lstrip('/')
                        else:
                            image_zip_path = 'ppt/slideMasters/' + image_target

                        # Normalize
                        parts = image_zip_path.replace('\\', '/').split('/')
                        normalized = []
                        for p in parts:
                            if p == '..':
                                if normalized:
                                    normalized.pop()
                            elif p != '.':
                                normalized.append(p)
                        image_zip_path = '/'.join(normalized)

                        if image_zip_path in zf.namelist():
                            embedded_data = zf.open(image_zip_path).read()
                            # Compare with the source texture_bg.jpg on Desktop
                            source_path = os.path.join(WORKDIR, 'Desktop', 'texture_bg.jpg')
                            if os.path.exists(source_path):
                                source_data = open(source_path, 'rb').read()
                                if embedded_data == source_data:
                                    print(f"PASS: Component 3 -- Embedded image matches texture_bg.jpg ({len(embedded_data)} bytes) (0.2 pts)")
                                    total_score += 0.2
                                else:
                                    print(f"FAIL: Component 3 -- Embedded image ({len(embedded_data)} bytes) differs from source ({len(source_data)} bytes)")
                            else:
                                # Source file missing; check filename at least
                                if 'texture_bg' in image_zip_path.lower():
                                    print(f"PASS: Component 3 -- Image path contains 'texture_bg' and is embedded (0.2 pts)")
                                    total_score += 0.2
                                else:
                                    print(f"FAIL: Component 3 -- Cannot verify image identity; source not found and name doesn't match")
                        else:
                            print(f"FAIL: Component 3 -- Image target '{image_zip_path}' not found in archive")
                    else:
                        print(f"FAIL: Component 3 -- Could not resolve relationship for embed ID '{embed_id}'")
                else:
                    print("FAIL: Component 3 -- No embed ID found in blip element")
            else:
                print("FAIL: Component 3 -- No blip element found in blipFill")
        else:
            print("FAIL: Component 3 -- No blipFill to check image (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Presentation retains all 7 slides (0.2 points)
    # This is a compound check: the task should not have broken the slide count
    try:
        slide_files = [n for n in zf.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
        num_slides = len(slide_files)
        if num_slides == 7:
            # Only award points if the background was actually changed (Components 1 passed)
            # This prevents awarding points on initial_env where slides=7 but no image bg
            if total_score > 0:
                print(f"PASS: Component 4 -- Presentation has {num_slides} slides as expected (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 -- 7 slides present but no background change detected (precondition gate)")
        else:
            print(f"FAIL: Component 4 -- Expected 7 slides, found {num_slides}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    zf.close()

    final_score = round(min(total_score, 1.0), 2)
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
