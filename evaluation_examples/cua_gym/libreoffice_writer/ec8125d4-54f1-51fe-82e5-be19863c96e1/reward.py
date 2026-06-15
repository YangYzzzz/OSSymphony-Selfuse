"""
Reward Script: Set up a two-column newsletter layout using linked text boxes.
Task ID: writer_obj_055
Domain: libreoffice_writer
Scoring:
  - Component 1: Two text boxes (VML shapes) exist in the document (0.20 pts)
  - Component 2: Both text boxes have correct size and position (0.40 pts)
  - Component 3: Both text boxes have no border (stroked=f) (0.20 pts)
  - Component 4: Both text boxes have 0.2cm internal padding (0.10 pts)
  - Component 5: Text boxes are linked (left box has o:next pointing to right box) (0.10 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_055'

# Tolerance for position/size comparisons (in cm)
TOLERANCE_CM = 0.05

VML_NS = 'urn:schemas-microsoft-com:vml'
O_NS = 'urn:schemas-microsoft-com:office:office'
W10_NS = 'urn:schemas-microsoft-com:office:word'


def parse_style_pt(style_str):
    """Parse VML style string and return dict of property->value (in pt)."""
    result = {}
    for part in style_str.split(';'):
        part = part.strip()
        if ':' in part:
            key, val = part.split(':', 1)
            key = key.strip()
            val = val.strip()
            m = re.match(r'^(-?[\d.]+)pt$', val)
            if m:
                result[key] = float(m.group(1))
    return result


def pt_to_cm(pt):
    """Convert points to centimetres."""
    return pt / 28.3465


def inch_to_cm(inch):
    """Convert inches to centimetres."""
    return inch * 2.54


def parse_inset_cm(inset_str):
    """Parse v:textbox inset attribute (comma-separated) and return values in cm."""
    values = []
    for part in inset_str.split(','):
        part = part.strip()
        m_in = re.match(r'^(-?[\d.]+)in$', part)
        m_cm = re.match(r'^(-?[\d.]+)cm$', part)
        m_pt = re.match(r'^(-?[\d.]+)pt$', part)
        if m_in:
            values.append(inch_to_cm(float(m_in.group(1))))
        elif m_cm:
            values.append(float(m_cm.group(1)))
        elif m_pt:
            values.append(pt_to_cm(float(m_pt.group(1))))
        else:
            values.append(0.254)  # default
    return values


def approx_equal(a, b, tol=TOLERANCE_CM):
    return abs(a - b) <= tol


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Set up a two-column newsletter layout on page 1 using linked text boxes.
    - Two text boxes side by side (7.5cm wide, 18cm tall each)
    - Left box: X=1.5cm, Y=4cm; Right box: X=10cm, Y=4cm
    - No border on both boxes
    - 0.2cm internal padding on all sides
    - Linked so text flows from left to right
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load document {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body

    # Component 1: Two text boxes (VML shapes) exist (0.20 pts)
    try:
        vml_shapes = body.findall('.//{' + VML_NS + '}shape')
        num_shapes = len(vml_shapes)
        if num_shapes >= 2:
            print(f"PASS: Component 1 — Found {num_shapes} VML text box shapes (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected >= 2 VML shapes (text boxes), found {num_shapes}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Only proceed with detailed checks if we have at least 2 shapes
    if total_score < 0.20:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score:.2f}/1.0")
        print(f"REWARD: {final_score:.1f}")
        return final_score

    # Identify left box (X~1.5cm) and right box (X~10.0cm)
    left_box = None
    right_box = None

    for shape in vml_shapes:
        style_str = shape.get('style', '')
        style = parse_style_pt(style_str)
        x_cm = pt_to_cm(style.get('left', -1))
        if approx_equal(x_cm, 1.5, 0.1) and left_box is None:
            left_box = shape
        elif approx_equal(x_cm, 10.0, 0.1) and right_box is None:
            right_box = shape

    # Component 2: Both text boxes have correct size and position (0.40 pts)
    # 0.20 per box (0.10 for position + 0.10 for size, awarded together if both match)
    try:
        comp2_score = 0.0

        # Left box
        if left_box is not None:
            style = parse_style_pt(left_box.get('style', ''))
            x_cm = pt_to_cm(style.get('left', -999))
            y_cm = pt_to_cm(style.get('top', -999))
            w_cm = pt_to_cm(style.get('width', -999))
            h_cm = pt_to_cm(style.get('height', -999))

            pos_ok = approx_equal(x_cm, 1.5) and approx_equal(y_cm, 4.0)
            size_ok = approx_equal(w_cm, 7.5) and approx_equal(h_cm, 18.0)

            if pos_ok and size_ok:
                print(f"PASS: Component 2a — Left box: X={x_cm:.3f}cm Y={y_cm:.3f}cm W={w_cm:.3f}cm H={h_cm:.3f}cm (0.20 pts)")
                comp2_score += 0.20
            elif pos_ok:
                print(f"PARTIAL: Component 2a — Left box position OK but size wrong W={w_cm:.3f}cm H={h_cm:.3f}cm (expected 7.5x18cm) (0.10 pts)")
                comp2_score += 0.10
            elif size_ok:
                print(f"PARTIAL: Component 2a — Left box size OK but position wrong X={x_cm:.3f}cm (expected 1.5) Y={y_cm:.3f}cm (expected 4.0) (0.10 pts)")
                comp2_score += 0.10
            else:
                print(f"FAIL: Component 2a — Left box X={x_cm:.3f}cm (exp 1.5) Y={y_cm:.3f}cm (exp 4.0) W={w_cm:.3f}cm (exp 7.5) H={h_cm:.3f}cm (exp 18.0)")
        else:
            print("FAIL: Component 2a — No left text box found near X=1.5cm")

        # Right box
        if right_box is not None:
            style = parse_style_pt(right_box.get('style', ''))
            x_cm = pt_to_cm(style.get('left', -999))
            y_cm = pt_to_cm(style.get('top', -999))
            w_cm = pt_to_cm(style.get('width', -999))
            h_cm = pt_to_cm(style.get('height', -999))

            pos_ok = approx_equal(x_cm, 10.0) and approx_equal(y_cm, 4.0)
            size_ok = approx_equal(w_cm, 7.5) and approx_equal(h_cm, 18.0)

            if pos_ok and size_ok:
                print(f"PASS: Component 2b — Right box: X={x_cm:.3f}cm Y={y_cm:.3f}cm W={w_cm:.3f}cm H={h_cm:.3f}cm (0.20 pts)")
                comp2_score += 0.20
            elif pos_ok:
                print(f"PARTIAL: Component 2b — Right box position OK but size wrong W={w_cm:.3f}cm H={h_cm:.3f}cm (expected 7.5x18cm) (0.10 pts)")
                comp2_score += 0.10
            elif size_ok:
                print(f"PARTIAL: Component 2b — Right box size OK but position wrong X={x_cm:.3f}cm (expected 10.0) Y={y_cm:.3f}cm (expected 4.0) (0.10 pts)")
                comp2_score += 0.10
            else:
                print(f"FAIL: Component 2b — Right box X={x_cm:.3f}cm (exp 10.0) Y={y_cm:.3f}cm (exp 4.0) W={w_cm:.3f}cm (exp 7.5) H={h_cm:.3f}cm (exp 18.0)")
        else:
            print("FAIL: Component 2b — No right text box found near X=10.0cm")

        if comp2_score > 0:
            total_score += comp2_score

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Both text boxes have no border (stroked="f") (0.20 pts)
    try:
        comp3_score = 0.0

        if left_box is not None:
            stroked_left = left_box.get('stroked', '').lower()
            if stroked_left in ('f', 'false'):
                print(f"PASS: Component 3a — Left box has no border (stroked='{stroked_left}') (0.10 pts)")
                comp3_score += 0.10
            else:
                print(f"FAIL: Component 3a — Left box stroked='{stroked_left}' (expected 'f' for no border)")
        else:
            print("FAIL: Component 3a — Left box not found, cannot check border")

        if right_box is not None:
            stroked_right = right_box.get('stroked', '').lower()
            if stroked_right in ('f', 'false'):
                print(f"PASS: Component 3b — Right box has no border (stroked='{stroked_right}') (0.10 pts)")
                comp3_score += 0.10
            else:
                print(f"FAIL: Component 3b — Right box stroked='{stroked_right}' (expected 'f' for no border)")
        else:
            print("FAIL: Component 3b — Right box not found, cannot check border")

        if comp3_score > 0:
            total_score += comp3_score

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Both text boxes have 0.2cm internal padding (0.10 pts, 0.05 each)
    try:
        TARGET_INSET_CM = 0.2
        INSET_TOL = 0.02
        comp4_score = 0.0

        for box_name, box in [('Left', left_box), ('Right', right_box)]:
            if box is None:
                print(f"FAIL: Component 4 ({box_name}) — box not found")
                continue
            textbox_elem = box.find('.//{' + VML_NS + '}textbox')
            if textbox_elem is None:
                print(f"FAIL: Component 4 ({box_name}) — no v:textbox child element found")
                continue
            inset_str = textbox_elem.get('inset', '')
            if not inset_str:
                print(f"FAIL: Component 4 ({box_name}) — no inset attribute found (expected ~0.2cm)")
                continue
            inset_values = parse_inset_cm(inset_str)
            if all(abs(v - TARGET_INSET_CM) <= INSET_TOL for v in inset_values):
                print(f"PASS: Component 4 ({box_name}) — internal padding {inset_values[0]:.4f}cm all sides (0.05 pts)")
                comp4_score += 0.05
            else:
                print(f"FAIL: Component 4 ({box_name}) — inset {inset_values} cm (expected 0.2cm all sides)")

        if comp4_score > 0:
            total_score += comp4_score

    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Text boxes are linked (left o:next references right box) (0.10 pts)
    try:
        if left_box is not None and right_box is not None:
            next_attr = left_box.get('{' + O_NS + '}next', '')
            right_id = right_box.get('id', '')

            # next_attr should reference the right box: "#<id>"
            next_refs_right = next_attr and right_id and (next_attr == '#' + right_id)

            if not next_refs_right and next_attr:
                # Fallback: check o:spid
                right_spid = right_box.get('{' + O_NS + '}spid', '')
                next_refs_right = bool(right_spid and next_attr == '#' + right_spid)

            if next_refs_right:
                print(f"PASS: Component 5 — Left box linked to right box via o:next='{next_attr}' (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — Left box o:next='{next_attr}' does not reference right box id='{right_id}'")
        else:
            print("FAIL: Component 5 — Cannot check link: one or both text boxes not found")

    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/monthly_newsletter.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
