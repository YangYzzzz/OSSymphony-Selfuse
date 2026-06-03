"""
Reward Script: Add 'Back to Table of Contents' navigation links
Task ID: impress_fix_093
Domain: libreoffice_impress
Scoring:
  Precondition gate: Slide 1 must NOT have 'Back to Table of Contents' (else 0.0)
  Component 1 (0.40): Slides 2-16 each contain 'Back to Table of Contents' text
  Component 2 (0.35): Each link has an internal hyperlink action targeting slide 1
  Component 3 (0.25): Link text is positioned at the bottom of each slide
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_093'

# XML namespaces used in OOXML
NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'rels': 'http://schemas.openxmlformats.org/package/2006/relationships',
}


def find_back_link_shapes(root):
    """Find shapes containing 'Back to Table of Contents' text.
    Returns list of (shape_element, full_text, x_off, y_off, cy) tuples."""
    results = []
    for sp in root.findall('.//p:sp', NS):
        txBody = sp.find('.//p:txBody', NS)
        if txBody is None:
            continue
        text = ''.join(t.text or '' for t in txBody.findall('.//a:t', NS))
        if 'back to table of contents' in text.lower():
            # Get position from spPr/xfrm
            xfrm = sp.find('.//p:spPr/a:xfrm', NS)
            y_off = None
            cy = None
            x_off = None
            if xfrm is not None:
                off_el = xfrm.find('a:off', NS)
                ext_el = xfrm.find('a:ext', NS)
                if off_el is not None:
                    y_off = int(off_el.get('y', '0'))
                    x_off = int(off_el.get('x', '0'))
                if ext_el is not None:
                    cy = int(ext_el.get('cy', '0'))
            results.append((sp, text.strip(), x_off, y_off, cy))
    return results


def get_hyperlink_target(zf, slide_num, sp):
    """Check if a shape's text run has an hlinkClick action pointing to slide1.
    Returns the target filename (e.g., 'slide1.xml') or None."""
    # Find hlinkClick elements with ppaction://hlinksldjump action
    hlinks = sp.findall('.//a:hlinkClick', NS)
    for hlink in hlinks:
        action = hlink.get('action', '')
        if 'hlinksldjump' not in action:
            continue
        rid = hlink.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        if rid is None:
            continue
        # Look up the relationship target
        try:
            with zf.open(f'ppt/slides/_rels/slide{slide_num}.xml.rels') as rf:
                rels_root = ET.parse(rf).getroot()
                for rel in rels_root.findall('.//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
                    if rel.get('Id') == rid:
                        return rel.get('Target')
        except (KeyError, ET.ParseError):
            pass
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Determine number of slides
    slide_files = [n for n in zf.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
    num_slides = len(slide_files)
    print(f"INFO: Found {num_slides} slides")

    if num_slides < 2:
        print("FAIL: Need at least 2 slides (1 TOC + content slides)")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Load slide height for position checks
    try:
        with zf.open('ppt/presentation.xml') as pf:
            pres_root = ET.parse(pf).getroot()
            sldSz = pres_root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldSz')
            if sldSz is None:
                sldSz = pres_root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldSz')
            slide_height = int(sldSz.get('cy', '6858000')) if sldSz is not None else 6858000
    except Exception:
        slide_height = 6858000  # default 7.5 inches
    print(f"INFO: Slide height = {slide_height} EMU")

    # Parse all slide XMLs
    slide_roots = {}
    for slide_num in range(1, num_slides + 1):
        try:
            with zf.open(f'ppt/slides/slide{slide_num}.xml') as sf:
                slide_roots[slide_num] = ET.parse(sf).getroot()
        except Exception as e:
            print(f"WARNING: Cannot parse slide {slide_num}: {e}")

    # =========================================================================
    # Precondition gate: Slide 1 must NOT have 'Back to Table of Contents'
    # This is a structural requirement, not a task-introduced change, so it
    # acts as a gate rather than a scoring component.
    # =========================================================================
    try:
        if 1 in slide_roots:
            back_shapes_slide1 = find_back_link_shapes(slide_roots[1])
            if len(back_shapes_slide1) > 0:
                print(f"FAIL: Precondition -- Slide 1 incorrectly has 'Back to Table of Contents'. Returning 0.0.")
                zf.close()
                print("REWARD: 0.0")
                return 0.0
            else:
                print(f"GATE: Slide 1 correctly has no 'Back to Table of Contents'")
    except Exception as e:
        print(f"WARNING: Precondition check error -- {e}")

    # =========================================================================
    # Component 1: Slides 2-N each have 'Back to Table of Contents' text (0.40)
    # =========================================================================
    try:
        slides_with_text = 0
        expected_slides = num_slides - 1  # slides 2 through N
        for slide_num in range(2, num_slides + 1):
            if slide_num not in slide_roots:
                continue
            back_shapes = find_back_link_shapes(slide_roots[slide_num])
            if len(back_shapes) > 0:
                slides_with_text += 1
            else:
                print(f"  MISS: Slide {slide_num} missing 'Back to Table of Contents' text")

        if expected_slides > 0:
            ratio = slides_with_text / expected_slides
            comp1_score = round(0.40 * ratio, 4)
            if ratio >= 1.0:
                print(f"PASS: Component 1 -- All {expected_slides} content slides have 'Back to Table of Contents' text ({comp1_score} pts)")
            else:
                print(f"PARTIAL: Component 1 -- {slides_with_text}/{expected_slides} slides have text ({comp1_score} pts)")
            if comp1_score > 0:
                total_score += comp1_score
        else:
            print(f"FAIL: Component 1 -- No content slides found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # =========================================================================
    # Component 2: Each link has hyperlink action targeting slide 1 (0.35)
    # =========================================================================
    try:
        slides_with_link = 0
        for slide_num in range(2, num_slides + 1):
            if slide_num not in slide_roots:
                continue
            back_shapes = find_back_link_shapes(slide_roots[slide_num])
            for sp, text, x, y, cy in back_shapes:
                target = get_hyperlink_target(zf, slide_num, sp)
                if target is not None and 'slide1.xml' in target:
                    slides_with_link += 1
                    break  # one valid link per slide is enough
                else:
                    print(f"  MISS: Slide {slide_num} 'Back to TOC' has no hyperlink to slide 1 (target={target})")

        if expected_slides > 0:
            ratio = slides_with_link / expected_slides
            comp2_score = round(0.35 * ratio, 4)
            if ratio >= 1.0:
                print(f"PASS: Component 2 -- All {expected_slides} links target slide 1 ({comp2_score} pts)")
            else:
                print(f"PARTIAL: Component 2 -- {slides_with_link}/{expected_slides} links target slide 1 ({comp2_score} pts)")
            if comp2_score > 0:
                total_score += comp2_score
        else:
            print(f"FAIL: Component 2 -- No content slides found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================================
    # Component 3: Link text is positioned at bottom of slide (0.25)
    # Bottom = top of shape > 75% of slide height
    # =========================================================================
    try:
        slides_at_bottom = 0
        bottom_threshold = int(slide_height * 0.75)
        for slide_num in range(2, num_slides + 1):
            if slide_num not in slide_roots:
                continue
            back_shapes = find_back_link_shapes(slide_roots[slide_num])
            for sp, text, x, y, cy in back_shapes:
                if y is not None and y >= bottom_threshold:
                    slides_at_bottom += 1
                    break
                else:
                    print(f"  MISS: Slide {slide_num} link position y={y}, threshold={bottom_threshold}")

        if expected_slides > 0:
            ratio = slides_at_bottom / expected_slides
            comp3_score = round(0.25 * ratio, 4)
            if ratio >= 1.0:
                print(f"PASS: Component 3 -- All {expected_slides} links positioned at bottom ({comp3_score} pts)")
            else:
                print(f"PARTIAL: Component 3 -- {slides_at_bottom}/{expected_slides} links at bottom ({comp3_score} pts)")
            if comp3_score > 0:
                total_score += comp3_score
        else:
            print(f"FAIL: Component 3 -- No content slides found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    zf.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: persist app state then verify
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
