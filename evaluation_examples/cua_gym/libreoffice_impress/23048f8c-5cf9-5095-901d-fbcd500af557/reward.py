"""
Reward Script: Verify Swivel entrance + Grow & Shrink emphasis animations on slide 5 image
Task ID: impress_ma_084
Domain: libreoffice_impress
Scoring:
  Component 1 (0.30): Timing element exists with animations targeting the product image
  Component 2 (0.30): First animation is Swivel entrance (presetID=56, entr, clickEffect)
  Component 3 (0.25): Second animation is Grow & Shrink emphasis (presetID=6, emph, afterEffect)
  Component 4 (0.15): Grow & Shrink scales to 120% (x=120000, y=120000)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_084'
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def find_image_spid(root):
    """Find the shape ID of the product image on slide 5."""
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'cNvPr' and 'product' in (elem.get('name', '') or '').lower():
            return elem.get('id')
    # Fallback: find any picture shape (pic element) and get its cNvPr id
    pic_ns = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'pic':
            for sub in elem.iter():
                sub_tag = sub.tag.split('}')[-1] if '}' in sub.tag else sub.tag
                if sub_tag == 'cNvPr':
                    return sub.get('id')
    return None


def get_animation_nodes(timing_elem):
    """Extract animation preset nodes from timing XML."""
    animations = []
    for elem in timing_elem.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'cTn' and elem.get('presetID'):
            animations.append(elem)
    return animations


def get_target_spid(anim_node):
    """Get the target shape ID from an animation node."""
    for elem in anim_node.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'spTgt':
            return elem.get('spid')
    return None


def get_scale_values(anim_node):
    """Get scale x/y from animScale element within an animation node."""
    for elem in anim_node.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'by' or tag == 'to':
            x = elem.get('x')
            y = elem.get('y')
            if x and y:
                return x, y
    return None, None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Parse slide 5 XML from the pptx ZIP
    try:
        zf = zipfile.ZipFile(file_path, 'r')
        root = ET.parse(zf.open('ppt/slides/slide5.xml')).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot load slide 5 from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the image shape ID
    image_spid = find_image_spid(root)
    if not image_spid:
        print("WARN: Could not identify product image shape ID, will check animations generically")

    # Find timing element
    timing = root.find('.//p:timing', NS)

    # Component 1: Timing element exists with animations targeting the image (0.30 points)
    try:
        if timing is None:
            print("FAIL: Component 1 -- No timing/animation element found on slide 5")
        else:
            anims = get_animation_nodes(timing)
            # Check that at least one animation targets the image
            targeting_image = any(
                (image_spid and get_target_spid(anim) == image_spid) or
                (not image_spid and get_target_spid(anim))
                for anim in anims
            )

            if len(anims) >= 2 and targeting_image:
                print(f"PASS: Component 1 -- Found {len(anims)} animations targeting image spid={image_spid} (0.30 pts)")
                total_score += 0.30
            elif len(anims) >= 2:
                print(f"FAIL: Component 1 -- Found {len(anims)} animations but none target image spid={image_spid}")
            elif len(anims) >= 1 and targeting_image:
                print(f"PARTIAL: Component 1 -- Found {len(anims)} animation(s) targeting image, need 2 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- Found {len(anims)} animations, need at least 2 targeting image")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Get animation nodes for detailed checks
    anims = get_animation_nodes(timing) if timing is not None else []
    # Filter to animations targeting the image
    image_anims = []
    for anim in anims:
        spid = get_target_spid(anim)
        if image_spid and spid == image_spid:
            image_anims.append(anim)
        elif not image_spid and spid:
            image_anims.append(anim)

    # Component 2: First animation is Swivel entrance (presetID=56, entr, clickEffect) (0.30 points)
    try:
        if len(image_anims) < 1:
            print("FAIL: Component 2 -- No animations found targeting image")
        else:
            first = image_anims[0]
            preset_id = first.get('presetID', '')
            preset_class = first.get('presetClass', '')
            node_type = first.get('nodeType', '')

            is_entrance = preset_class == 'entr'
            is_swivel = preset_id == '56'
            is_click = node_type == 'clickEffect'

            if is_entrance and is_swivel and is_click:
                print(f"PASS: Component 2 -- Swivel entrance (presetID=56, entr, clickEffect) (0.30 pts)")
                total_score += 0.30
            elif is_entrance and is_swivel:
                print(f"PARTIAL: Component 2 -- Swivel entrance found but nodeType={node_type} (expected clickEffect) (0.20 pts)")
                total_score += 0.20
            elif is_entrance:
                print(f"FAIL: Component 2 -- Entrance animation found but presetID={preset_id} (expected 56=Swivel), class={preset_class}")
            else:
                print(f"FAIL: Component 2 -- First animation: presetID={preset_id}, class={preset_class}, nodeType={node_type}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Second animation is Grow & Shrink emphasis (presetID=6, emph, afterEffect) (0.25 points)
    try:
        if len(image_anims) < 2:
            print("FAIL: Component 3 -- Less than 2 animations found targeting image")
        else:
            second = image_anims[1]
            preset_id = second.get('presetID', '')
            preset_class = second.get('presetClass', '')
            node_type = second.get('nodeType', '')

            is_emphasis = preset_class == 'emph'
            is_grow_shrink = preset_id == '6'
            is_after = node_type == 'afterEffect'

            if is_emphasis and is_grow_shrink and is_after:
                print(f"PASS: Component 3 -- Grow & Shrink emphasis (presetID=6, emph, afterEffect) (0.25 pts)")
                total_score += 0.25
            elif is_emphasis and is_grow_shrink:
                print(f"PARTIAL: Component 3 -- Grow & Shrink emphasis found but nodeType={node_type} (expected afterEffect) (0.15 pts)")
                total_score += 0.15
            elif is_emphasis:
                print(f"FAIL: Component 3 -- Emphasis animation found but presetID={preset_id} (expected 6=Grow&Shrink)")
            else:
                print(f"FAIL: Component 3 -- Second animation: presetID={preset_id}, class={preset_class}, nodeType={node_type}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Grow & Shrink scales to 120% (x=120000, y=120000) (0.15 points)
    try:
        if len(image_anims) < 2:
            print("FAIL: Component 4 -- No second animation to check scale values")
        else:
            second = image_anims[1]
            sx, sy = get_scale_values(second)

            if sx == '120000' and sy == '120000':
                print(f"PASS: Component 4 -- Scale 120% (x={sx}, y={sy}) (0.15 pts)")
                total_score += 0.15
            elif sx and sy:
                print(f"FAIL: Component 4 -- Scale x={sx}, y={sy} (expected 120000, 120000)")
            else:
                print(f"FAIL: Component 4 -- No scale values found in second animation")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    try:
        zf.close()
    except:
        pass

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
