"""
Reward Script: Style hierarchy for documentation with Text Body parent and child styles
Task ID: writer_tech_084
Domain: libreoffice_writer
Scoring:
  Component 1: Body Text style has Liberation Sans 11pt (0.25)
  Component 2: Doc Note style with blue border/background, based on Body Text (0.25)
  Component 3: Doc Warning style with yellow border/background, based on Body Text (0.25)
  Component 4: Doc Tip style with green border/background, based on Body Text (0.25)
"""

import os
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from math import sqrt

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_084'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def hex_to_rgb(hex_str):
    """Convert hex color string to (r, g, b) tuple."""
    hex_str = hex_str.strip('#')
    return (int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))


def color_distance(c1, c2):
    """Euclidean distance between two RGB tuples."""
    return sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def get_style_by_name_or_id(doc, names):
    """Try to find a style by multiple possible names."""
    for name in names:
        try:
            return doc.styles[name]
        except KeyError:
            continue
    return None


def get_left_border_color(style_element):
    """Extract left border color from style XML."""
    ppr = style_element.find(qn('w:pPr'))
    if ppr is None:
        return None
    pbdr = ppr.find(qn('w:pBdr'))
    if pbdr is None:
        return None
    left = pbdr.find(qn('w:left'))
    if left is None:
        return None
    color = left.get(qn('w:color'))
    return color


def get_shading_fill(style_element):
    """Extract paragraph shading fill color from style XML."""
    ppr = style_element.find(qn('w:pPr'))
    if ppr is None:
        return None
    shd = ppr.find(qn('w:shd'))
    if shd is None:
        return None
    fill = shd.get(qn('w:fill'))
    return fill


def has_left_border(style_element):
    """Check if style has a left border defined."""
    ppr = style_element.find(qn('w:pPr'))
    if ppr is None:
        return False
    pbdr = ppr.find(qn('w:pBdr'))
    if pbdr is None:
        return False
    left = pbdr.find(qn('w:left'))
    if left is None:
        return False
    val = left.get(qn('w:val'))
    # 'none' means no border
    if val and val.lower() == 'none':
        return False
    return True


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # The task says "Text Body" but python-docx/OOXML calls it "Body Text".
    # We accept either name.
    PARENT_NAMES = ['Text Body', 'Body Text']

    # Component 1: Body Text/Text Body style has Liberation Sans 11pt (0.25 points)
    try:
        parent_style = get_style_by_name_or_id(doc, PARENT_NAMES)
        if parent_style is None:
            print("FAIL: Component 1 -- Neither 'Text Body' nor 'Body Text' style found")
        else:
            parent_name = parent_style.name
            font_name = parent_style.font.name
            font_size = parent_style.font.size

            font_name_ok = font_name is not None and 'liberation sans' in font_name.lower()
            font_size_ok = font_size is not None and abs(font_size.pt - 11.0) < 0.5

            if font_name_ok and font_size_ok:
                print(f"PASS: Component 1 -- '{parent_name}' has Liberation Sans {font_size.pt}pt (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- '{parent_name}' font: name={font_name}, size={font_size}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Components 2-4: Verify each child style
    CHILD_STYLES = {
        'Doc Note': {
            'border_color_target': (0x44, 0x72, 0xC4),  # blue
            'fill_color_target': (0xD6, 0xE4, 0xF0),    # light blue
            'component_num': 2,
        },
        'Doc Warning': {
            'border_color_target': (0xFF, 0xC0, 0x00),  # yellow
            'fill_color_target': (0xFF, 0xF2, 0xCC),    # light yellow
            'component_num': 3,
        },
        'Doc Tip': {
            'border_color_target': (0x70, 0xAD, 0x47),  # green
            'fill_color_target': (0xE2, 0xEF, 0xDA),    # light green
            'component_num': 4,
        },
    }

    for style_name, config in CHILD_STYLES.items():
        comp_num = config['component_num']
        try:
            style = get_style_by_name_or_id(doc, [style_name])
            if style is None:
                print(f"FAIL: Component {comp_num} -- Style '{style_name}' not found")
                continue

            # Sub-checks for each child style
            checks_passed = 0
            total_checks = 3  # base style, left border color, background fill

            # Check 1: Inherits from Body Text / Text Body
            base = style.base_style
            if base is not None and base.name in PARENT_NAMES:
                checks_passed += 1
            else:
                base_name = base.name if base else 'None'
                print(f"  INFO: Component {comp_num} -- '{style_name}' base is '{base_name}', not Text Body/Body Text")

            # Check 2: Left border with correct color
            border_color_hex = get_left_border_color(style.element)
            if border_color_hex and has_left_border(style.element):
                try:
                    actual_border = hex_to_rgb(border_color_hex)
                    dist = color_distance(actual_border, config['border_color_target'])
                    if dist < 60:  # allow some tolerance
                        checks_passed += 1
                    else:
                        print(f"  INFO: Component {comp_num} -- '{style_name}' border color {border_color_hex} distance={dist:.1f}")
                except Exception:
                    print(f"  INFO: Component {comp_num} -- '{style_name}' border color parse error: {border_color_hex}")
            else:
                print(f"  INFO: Component {comp_num} -- '{style_name}' has no left border")

            # Check 3: Background shading fill with correct color
            fill_hex = get_shading_fill(style.element)
            if fill_hex:
                try:
                    actual_fill = hex_to_rgb(fill_hex)
                    dist = color_distance(actual_fill, config['fill_color_target'])
                    if dist < 60:  # allow some tolerance
                        checks_passed += 1
                    else:
                        print(f"  INFO: Component {comp_num} -- '{style_name}' fill color {fill_hex} distance={dist:.1f}")
                except Exception:
                    print(f"  INFO: Component {comp_num} -- '{style_name}' fill color parse error: {fill_hex}")
            else:
                print(f"  INFO: Component {comp_num} -- '{style_name}' has no background shading")

            # Award points proportionally
            if checks_passed == total_checks:
                print(f"PASS: Component {comp_num} -- '{style_name}' fully correct ({checks_passed}/{total_checks}) (0.25 pts)")
                total_score += 0.25
            elif checks_passed > 0:
                partial = round(0.25 * checks_passed / total_checks, 3)
                print(f"PARTIAL: Component {comp_num} -- '{style_name}' ({checks_passed}/{total_checks}) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component {comp_num} -- '{style_name}' no sub-checks passed")

        except Exception as e:
            print(f"ERROR: Component {comp_num} -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
