"""
Reward Script: Navigation hyperlinks in branching presentation
Task ID: impress_gf2_041
Domain: libreoffice_impress
Scoring:
  - Component 1: Slide 3 'Yes' button -> slide 4 (0.2)
  - Component 2: Slide 3 'No' button -> slide 8 (0.2)
  - Component 3: Slide 7 'Go to Summary' button -> slide 11 (0.2)
  - Component 4: Slide 11 'Start Over' button -> slide 1 (0.2)
  - Component 5: Slide 11 'End Presentation' button -> slide 12 (0.2)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_041'

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}
RELS_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'


def get_slide_rels(zf, slide_num):
    """Parse slide relationships to map rId -> target slide filename."""
    rels_path = 'ppt/slides/_rels/slide%d.xml.rels' % slide_num
    rels = {}
    try:
        with zf.open(rels_path) as f:
            root = ET.fromstring(f.read())
            for rel in root:
                rid = rel.get('Id')
                target = rel.get('Target', '')
                rtype = rel.get('Type', '')
                if 'slide' in rtype.split('/')[-1].lower() and target.startswith('slide'):
                    rels[rid] = target  # e.g. 'slide4.xml'
    except KeyError:
        pass
    return rels


def find_button_with_hyperlink(zf, slide_num, expected_text, expected_target_slide_num):
    """
    Check if a slide contains a shape with the given text and a hyperlink
    action (ppaction://hlinksldjump) that targets the expected slide number.
    Returns True if found and correctly linked.
    """
    # Parse slide XML for shapes with hlinkClick
    slide_path = 'ppt/slides/slide%d.xml' % slide_num
    try:
        with zf.open(slide_path) as f:
            root = ET.parse(f).getroot()
    except KeyError:
        return False

    # Get relationship mappings
    rels = get_slide_rels(zf, slide_num)
    expected_target = 'slide%d.xml' % expected_target_slide_num

    # Find all shapes (sp elements) in the slide
    shapes = root.findall('.//p:cSld/p:spTree/p:sp', NS)
    for shape in shapes:
        # Extract text from the shape
        texts = []
        for t_elem in shape.findall('.//a:t', NS):
            if t_elem.text:
                texts.append(t_elem.text)
        shape_text = ''.join(texts).strip()

        # Check if text matches (case-insensitive)
        if shape_text.lower() != expected_text.lower():
            continue

        # Found the shape with matching text. Now check for hyperlink action.
        # Hyperlinks can be on the shape-level cNvPr or on individual runs
        hlink_elems = shape.findall('.//a:hlinkClick', NS)
        for hlink in hlink_elems:
            action = hlink.get('action', '')
            rid = hlink.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', '')
            if action == 'ppaction://hlinksldjump' and rid in rels:
                if rels[rid] == expected_target:
                    return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print("CRITICAL: Cannot open file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file should have 12 slides
    try:
        slide_count = len([n for n in zf.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')])
        if slide_count < 12:
            print("PRECONDITION FAIL: Expected 12 slides, found %d" % slide_count)
            print("REWARD: 0.0")
            zf.close()
            return 0.0
        print("PRECONDITION: %d slides found (>= 12 required)" % slide_count)
    except Exception as e:
        print("ERROR: Could not count slides: %s" % e)

    # Component 1: Slide 3 has 'Yes' button linking to slide 4 (0.2 points)
    try:
        if find_button_with_hyperlink(zf, 3, 'Yes', 4):
            print("PASS: Component 1 - Slide 3 'Yes' button links to slide 4 (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 - Slide 3 missing 'Yes' button linking to slide 4")
    except Exception as e:
        print("ERROR: Component 1 - %s" % e)

    # Component 2: Slide 3 has 'No' button linking to slide 8 (0.2 points)
    try:
        if find_button_with_hyperlink(zf, 3, 'No', 8):
            print("PASS: Component 2 - Slide 3 'No' button links to slide 8 (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 2 - Slide 3 missing 'No' button linking to slide 8")
    except Exception as e:
        print("ERROR: Component 2 - %s" % e)

    # Component 3: Slide 7 has 'Go to Summary' button linking to slide 11 (0.2 points)
    try:
        if find_button_with_hyperlink(zf, 7, 'Go to Summary', 11):
            print("PASS: Component 3 - Slide 7 'Go to Summary' button links to slide 11 (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 3 - Slide 7 missing 'Go to Summary' button linking to slide 11")
    except Exception as e:
        print("ERROR: Component 3 - %s" % e)

    # Component 4: Slide 11 has 'Start Over' button linking to slide 1 (0.2 points)
    try:
        if find_button_with_hyperlink(zf, 11, 'Start Over', 1):
            print("PASS: Component 4 - Slide 11 'Start Over' button links to slide 1 (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 4 - Slide 11 missing 'Start Over' button linking to slide 1")
    except Exception as e:
        print("ERROR: Component 4 - %s" % e)

    # Component 5: Slide 11 has 'End Presentation' button linking to slide 12 (0.2 points)
    try:
        if find_button_with_hyperlink(zf, 11, 'End Presentation', 12):
            print("PASS: Component 5 - Slide 11 'End Presentation' button links to slide 12 (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 5 - Slide 11 missing 'End Presentation' button linking to slide 12")
    except Exception as e:
        print("ERROR: Component 5 - %s" % e)

    zf.close()

    final_score = min(total_score, 1.0)
    print("\nScore: %.1f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
file_path = '%s/%s.pptx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
