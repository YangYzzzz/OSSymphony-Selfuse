"""
Reward Script: Set shape on slide 4 to tiled picture fill from headshot.jpg at 50% scale
Task ID: impress_design_071
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): Fill type is picture (blipFill), not solid
  Component 2 (0.3): Tile element is present (tiling mode enabled)
  Component 3 (0.2): Tile scale is 50% horizontal and 50% vertical (sx=50000, sy=50000)
  Component 4 (0.2): Embedded image matches headshot.jpg from Desktop
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_design_071'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Namespaces used in OOXML
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
    }

    # Precondition: file must exist and be a valid zip/pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open as zip: {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: slide4.xml must exist
    try:
        slide4_xml = zf.open('ppt/slides/slide4.xml').read().decode('utf-8')
        slide4_root = ET.fromstring(slide4_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot read slide4.xml: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Find the Rectangle 3 shape (the target shape on slide 4)
    # It's the shape with name "Rectangle 3" — look for sp elements
    target_spPr = None
    for sp in slide4_root.findall('.//p:sp', ns):
        cNvPr = sp.find('.//p:nvSpPr/p:cNvPr', ns)
        if cNvPr is not None and 'Rectangle' in (cNvPr.get('name') or ''):
            target_spPr = sp.find('p:spPr', ns)
            print(f"INFO: Found target shape: {cNvPr.get('name')}")
            break

    if target_spPr is None:
        print("CRITICAL: Could not find Rectangle shape on slide 4")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Fill type is picture (blipFill), not solid (0.3 points)
    try:
        blip_fill = target_spPr.find('a:blipFill', ns)
        solid_fill = target_spPr.find('a:solidFill', ns)
        if blip_fill is not None and solid_fill is None:
            print(f"PASS: Component 1 — Shape has picture fill (blipFill) (0.3 pts)")
            total_score += 0.3
        elif blip_fill is not None and solid_fill is not None:
            print(f"PARTIAL: Component 1 — blipFill present but solidFill also present")
            total_score += 0.15
        else:
            fill_type = "solidFill" if solid_fill is not None else "unknown/none"
            print(f"FAIL: Component 1 — Expected picture fill (blipFill), found: {fill_type}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Tile element is present (tiling mode enabled) (0.3 points)
    try:
        tile_elem = None
        if blip_fill is not None:
            tile_elem = blip_fill.find('a:tile', ns)
        if tile_elem is not None:
            print(f"PASS: Component 2 — Tile element present (tiling mode) (0.3 pts)")
            total_score += 0.3
        else:
            # Check if stretch is used instead (not tile mode)
            stretch = blip_fill.find('a:stretch', ns) if blip_fill is not None else None
            if stretch is not None:
                print(f"FAIL: Component 2 — Fill uses stretch mode, not tile mode")
            else:
                print(f"FAIL: Component 2 — No tile element found in fill")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Tile scale is 50% horizontal (sx=50000) and 50% vertical (sy=50000) (0.2 points)
    try:
        if tile_elem is not None:
            sx = tile_elem.get('sx')
            sy = tile_elem.get('sy')
            sx_val = int(sx) if sx else None
            sy_val = int(sy) if sy else None
            print(f"INFO: Tile scale sx={sx_val}, sy={sy_val}")

            sx_ok = sx_val is not None and sx_val == 50000
            sy_ok = sy_val is not None and sy_val == 50000

            if sx_ok and sy_ok:
                print(f"PASS: Component 3 — Tile scale 50% H and 50% V (sx=50000, sy=50000) (0.2 pts)")
                total_score += 0.2
            elif sx_ok or sy_ok:
                which = "horizontal" if sx_ok else "vertical"
                print(f"PARTIAL: Component 3 — Only {which} scale is 50% (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 3 — Expected sx=50000, sy=50000, got sx={sx_val}, sy={sy_val}")
        else:
            print(f"FAIL: Component 3 — No tile element to check scale on")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Embedded image matches headshot.jpg from Desktop (0.2 points)
    try:
        if blip_fill is not None:
            blip = blip_fill.find('a:blip', ns)
            if blip is not None:
                r_embed = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                print(f"INFO: blip r:embed={r_embed}")

                # Read the relationship to find the image path
                rels_xml = zf.open('ppt/slides/_rels/slide4.xml.rels').read().decode('utf-8')
                rels_root = ET.fromstring(rels_xml)
                img_path = None
                for rel in rels_root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
                    if rel.get('Id') == r_embed:
                        target = rel.get('Target')
                        # target is relative, e.g. "../media/image1.jpg"
                        img_path = 'ppt/' + target.replace('../', '')
                        break

                if img_path:
                    print(f"INFO: Image path in zip: {img_path}")
                    embedded_blob = zf.open(img_path).read()
                    # Compare with headshot.jpg on Desktop
                    headshot_path = '/home/user/Desktop/headshot.jpg'
                    if os.path.exists(headshot_path):
                        with open(headshot_path, 'rb') as hf:
                            headshot_blob = hf.read()
                        if embedded_blob == headshot_blob:
                            print(f"PASS: Component 4 — Embedded image matches headshot.jpg ({len(embedded_blob)} bytes) (0.2 pts)")
                            total_score += 0.2
                        else:
                            print(f"FAIL: Component 4 — Embedded image differs from headshot.jpg (embedded={len(embedded_blob)}B, headshot={len(headshot_blob)}B)")
                    else:
                        print(f"FAIL: Component 4 — headshot.jpg not found on Desktop for comparison")
                else:
                    print(f"FAIL: Component 4 — Could not resolve image relationship for {r_embed}")
            else:
                print(f"FAIL: Component 4 — No blip element in blipFill")
        else:
            print(f"FAIL: Component 4 — No blipFill, cannot check image")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
