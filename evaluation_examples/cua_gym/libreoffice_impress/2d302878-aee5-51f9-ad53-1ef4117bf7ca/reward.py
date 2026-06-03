"""
Reward Script: Interactive quiz slide with answer buttons and navigation
Task ID: impress_gf2_004
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): 'A: London' button on slide 4 links to slide 7 (wrong answer)
  Component 2 (0.25): 'B: Paris' button on slide 4 links to slide 6 (correct answer)
  Component 3 (0.25): 'C: Berlin' button on slide 4 links to slide 7 (wrong answer)
  Component 4 (0.25): 'Next Question' button on slide 6 links to slide 8
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_004'


def get_shape_hyperlink_target(pptx_path, slide_num, shape_text_match):
    """
    Find a shape on a given slide (1-indexed) whose text contains shape_text_match,
    and return the target slide number (1-indexed) if it has a hyperlink action.
    Returns None if no hyperlink found.
    """
    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # Parse the slide XML
        slide_xml_path = f'ppt/slides/slide{slide_num}.xml'
        try:
            with zf.open(slide_xml_path) as f:
                slide_root = ET.parse(f).getroot()
        except KeyError:
            return None

        # Parse the slide relationships
        rels_path = f'ppt/slides/_rels/slide{slide_num}.xml.rels'
        rels_map = {}
        try:
            with zf.open(rels_path) as f:
                rels_root = ET.parse(f).getroot()
                for rel in rels_root:
                    rid = rel.get('Id')
                    target = rel.get('Target')
                    rel_type = rel.get('Type')
                    if rid and target:
                        rels_map[rid] = (target, rel_type)
        except KeyError:
            return None

        # Find all shapes (sp elements) in the slide
        # Namespace for p:sp
        sp_elements = slide_root.findall('.//' + '{' + ns_p + '}sp')
        if not sp_elements:
            # Try without namespace prefix for cSld/spTree
            sp_elements = slide_root.findall('.//{' + ns_p + '}cSld/{' + ns_p + '}spTree/{' + ns_p + '}sp')

        for sp in sp_elements:
            # Get all text in this shape
            texts = sp.findall('.//{' + ns_a + '}t')
            full_text = ''.join((t.text or '') for t in texts).strip()

            if shape_text_match.lower() in full_text.lower():
                # Look for hlinkClick in this shape
                hlinks = sp.findall('.//{' + ns_a + '}hlinkClick')
                for hlink in hlinks:
                    action = hlink.get('action', '')
                    rid = hlink.get('{' + ns_r + '}id', '')
                    if 'hlinksldjump' in action.lower() and rid in rels_map:
                        target, rel_type = rels_map[rid]
                        # Extract slide number from target like 'slide7.xml'
                        if 'slide' in target.lower() and target.endswith('.xml'):
                            slide_name = target.split('/')[-1]  # e.g., 'slide7.xml'
                            try:
                                target_num = int(slide_name.replace('slide', '').replace('.xml', ''))
                                return target_num
                            except ValueError:
                                pass
    return None


def check_shape_exists_with_text(pptx_path, slide_num, text_match):
    """Check if a shape with the given text exists on the slide."""
    ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    ns_p = 'http://schemas.openxmlformats.org/presentationml/2006/main'

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_xml_path = f'ppt/slides/slide{slide_num}.xml'
        try:
            with zf.open(slide_xml_path) as f:
                slide_root = ET.parse(f).getroot()
        except KeyError:
            return False

        sp_elements = slide_root.findall('.//' + '{' + ns_p + '}sp')
        for sp in sp_elements:
            texts = sp.findall('.//{' + ns_a + '}t')
            full_text = ''.join((t.text or '') for t in texts).strip()
            if text_match.lower() in full_text.lower():
                return True
    return False


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

    # Component 1: 'A: London' on slide 4 links to slide 7 (0.25 points)
    try:
        target = get_shape_hyperlink_target(file_path, 4, 'A: London')
        if target == 7:
            print(f"PASS: Component 1 — 'A: London' links to slide 7 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — 'A: London' expected link to slide 7, found: {target}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'B: Paris' on slide 4 links to slide 6 (0.25 points)
    try:
        target = get_shape_hyperlink_target(file_path, 4, 'B: Paris')
        if target == 6:
            print(f"PASS: Component 2 — 'B: Paris' links to slide 6 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — 'B: Paris' expected link to slide 6, found: {target}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'C: Berlin' on slide 4 links to slide 7 (0.25 points)
    try:
        target = get_shape_hyperlink_target(file_path, 4, 'C: Berlin')
        if target == 7:
            print(f"PASS: Component 3 — 'C: Berlin' links to slide 7 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — 'C: Berlin' expected link to slide 7, found: {target}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Slide 6 has 'Next Question' button linking to slide 8 (0.25 points)
    try:
        target = get_shape_hyperlink_target(file_path, 6, 'Next Question')
        if target == 8:
            print(f"PASS: Component 4 — 'Next Question' on slide 6 links to slide 8 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — 'Next Question' expected link to slide 8, found: {target}")
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
