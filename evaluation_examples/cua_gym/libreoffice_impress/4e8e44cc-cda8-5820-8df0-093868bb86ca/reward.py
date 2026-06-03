"""
Reward Script: Create Fontwork 'GRAND OPENING' on slide 2 with Follow Path style and gradient fill
Task ID: impress_ndo_045
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.30): Dedicated Fontwork shape with text exactly 'GRAND OPENING' on slide 2
  - Component 2 (0.20): Text warp uses a curved/path preset (Follow Path style)
  - Component 3 (0.20): Shape spans approximately full slide width (>=90%)
  - Component 4 (0.30): Gradient fill from #FF6B6B to #4ECDC4 (shape or text run)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ndo_045'


def tag_local(el):
    """Get the local tag name without namespace."""
    t = el.tag
    return t.split('}')[-1] if '}' in t else t


def find_fontwork_shape(pptx_path):
    """
    Find a dedicated Fontwork/WordArt shape on slide 2 whose entire text
    is exactly 'GRAND OPENING'. This excludes text boxes that merely
    mention 'grand opening' in a longer sentence.
    """
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        try:
            with zf.open('ppt/slides/slide2.xml') as f:
                root = ET.fromstring(f.read())
        except KeyError:
            print("FAIL: slide2.xml not found in pptx")
            return None

        # Iterate over all <sp> elements (shapes)
        candidates = []
        for sp in root.iter():
            if not tag_local(sp) == 'sp':
                continue

            # Collect all <t> text in this shape
            texts = []
            for el in sp.iter():
                if tag_local(el) == 't' and el.text:
                    texts.append(el.text)
            full_text = ''.join(texts).strip()

            # Must be exactly 'GRAND OPENING' (case-insensitive), not embedded in longer text
            if full_text.upper() == 'GRAND OPENING':
                candidates.append(sp)

        if not candidates:
            return None

        # If multiple matches, prefer one with prstTxWarp or gradFill (more Fontwork-like)
        for sp in candidates:
            for el in sp.iter():
                if tag_local(el) in ('prstTxWarp', 'gradFill'):
                    return sp
        # Fallback: return the first match
        return candidates[0]

    return None


def check_text_warp(sp):
    """Check if the shape uses a curved/path text warp preset."""
    for el in sp.iter():
        if tag_local(el) == 'prstTxWarp':
            prst = el.get('prst', '')
            # Follow Path / curved styles in OOXML
            path_presets = {
                'textArchUp', 'textArchDown', 'textArchUpPour', 'textArchDownPour',
                'textCircle', 'textCirclePour', 'textCurveUp', 'textCurveDown',
                'textCanUp', 'textCanDown', 'textWave1', 'textWave2', 'textWave4',
                'textInflate', 'textDeflate', 'textInflateBottom', 'textInflateTop',
                'textDeflateBottom', 'textDeflateTop', 'textFadeRight', 'textFadeLeft',
                'textFadeUp', 'textFadeDown', 'textSlantUp', 'textSlantDown',
                'textCascadeUp', 'textCascadeDown',
            }
            if prst in path_presets:
                return True, f"Text warp preset: {prst}"
            else:
                return False, f"Text warp preset '{prst}' is not a recognized curved/path style"
    return False, "No prstTxWarp element found in shape"


def check_width(sp, pptx_path):
    """Check if shape spans approximately full slide width (>=90%)."""
    shape_cx = None
    for el in sp.iter():
        if tag_local(el) == 'spPr':
            for child in el:
                if tag_local(child) == 'xfrm':
                    for sub in child:
                        if tag_local(sub) == 'ext':
                            shape_cx = int(sub.get('cx', '0'))
                            break
                    break
            break

    if shape_cx is None:
        return False, "Could not find shape width (xfrm/ext)"

    # Get slide width from presentation.xml
    slide_width = 12191695  # default
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            with zf.open('ppt/presentation.xml') as f:
                pres_root = ET.fromstring(f.read())
                for el in pres_root.iter():
                    if tag_local(el) == 'sldSz':
                        slide_width = int(el.get('cx', str(slide_width)))
                        break
    except Exception:
        pass

    ratio = shape_cx / slide_width if slide_width > 0 else 0
    if ratio >= 0.90:
        return True, f"Shape width {shape_cx} EMU = {ratio*100:.1f}% of slide width {slide_width} EMU"
    else:
        return False, f"Shape width {shape_cx} EMU = {ratio*100:.1f}% of slide width — below 90% threshold"


def check_gradient_fill(sp):
    """Check for gradient fill with #FF6B6B and #4ECDC4 on shape fill or text run fill."""
    target_colors = {'FF6B6B', '4ECDC4'}

    # Walk through all gradFill elements in the shape
    for grad in sp.iter():
        if tag_local(grad) != 'gradFill':
            continue
        colors = set()
        for gs in grad.iter():
            if tag_local(gs) == 'srgbClr':
                colors.add(gs.get('val', '').upper())
        if target_colors.issubset(colors):
            return True, f"Gradient fill found with colors: {colors}"

    return False, "No gradient fill with #FF6B6B and #4ECDC4 found on shape or text"


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

    # Component 1: Dedicated Fontwork shape with text 'GRAND OPENING' on slide 2 (0.30 pts)
    try:
        sp = find_fontwork_shape(file_path)
        if sp is not None:
            print(f"PASS: Component 1 — Shape with exact text 'GRAND OPENING' found on slide 2 (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No dedicated shape with exact text 'GRAND OPENING' found on slide 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        sp = None

    if sp is None:
        # Cannot check further without the shape
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Text warp uses curved/path preset — Follow Path style (0.20 pts)
    try:
        passed, details = check_text_warp(sp)
        if passed:
            print(f"PASS: Component 2 — {details} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — {details}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Shape spans >= 90% of slide width (0.20 pts)
    try:
        passed, details = check_width(sp, file_path)
        if passed:
            print(f"PASS: Component 3 — {details} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — {details}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Gradient fill from #FF6B6B to #4ECDC4 (0.30 pts)
    try:
        passed, details = check_gradient_fill(sp)
        if passed:
            print(f"PASS: Component 4 — {details} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 4 — {details}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
