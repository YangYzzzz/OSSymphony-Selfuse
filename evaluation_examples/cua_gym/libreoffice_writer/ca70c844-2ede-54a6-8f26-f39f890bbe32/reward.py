"""
Reward Script: HR Department Organizational Chart in LibreOffice Writer
Task ID: writer_hr_059
Domain: libreoffice_writer

Scoring Rubric:
  Component 1 (0.25): Document has >= 7 text boxes with non-empty text (org chart boxes)
  Component 2 (0.25): Key leadership positions present (VP of HR + 3 Directors)
  Component 3 (0.20): Manager positions present (at least 5 of 6 manager text boxes)
  Component 4 (0.15): Connector lines present (at least 5 line shapes for hierarchy)
  Component 5 (0.15): Consistent box formatting (same dimensions and bold text)
"""

import os
import sys

# Persistence hook: save any unsaved LibreOffice state
def persist_app_state():
    try:
        import pyautogui
        import time
        os.environ["DISPLAY"] = ":0"
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


WORKDIR = '/home/user'
TASK_ID = 'writer_hr_059'


def verify_task(file_path):
    """
    Verify HR org chart task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        import lxml.etree as etree
    except ImportError as e:
        print(f"CRITICAL: Missing required library: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'wpc': 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas',
        'v': 'urn:schemas-microsoft-com:vml',
    }

    # --- Component 1: Text boxes with content (0.25 points) ---
    # The org chart requires >= 7 text boxes (1 VP + 3 directors + at least 3 managers)
    try:
        wps_txbxs = body.findall('.//wps:txbx', ns)
        v_txbxs = body.findall('.//v:textbox', {'v': 'urn:schemas-microsoft-com:vml'})
        all_txbxs = wps_txbxs + v_txbxs

        # Get text from each textbox
        txbx_texts = []
        for txbx in all_txbxs:
            t_elems = txbx.findall('.//w:t', ns)
            text = ''.join(t.text or '' for t in t_elems).strip()
            if text:
                txbx_texts.append(text)

        total_txbx = len(txbx_texts)

        if total_txbx >= 10:
            print(f"PASS: Component 1 — Found {total_txbx} text boxes with content (need >= 7) (0.25 pts)")
            total_score += 0.25
        elif total_txbx >= 7:
            # Partial: partial credit if fewer than 10 but >= 7
            print(f"PASS: Component 1 — Found {total_txbx} text boxes with content (need >= 7) (0.25 pts)")
            total_score += 0.25
        elif total_txbx >= 4:
            # Partial: significant shape presence but not enough
            print(f"PARTIAL: Component 1 — Found {total_txbx} text boxes (need >= 7) (0.12 pts)")
            total_score += 0.12
        else:
            print(f"FAIL: Component 1 — Found only {total_txbx} text boxes with content (need >= 7)")

        print(f"  Text boxes found: {txbx_texts}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: Key leadership positions (VP of HR + 3 Directors) (0.25 points) ---
    # Checks for the top-level hierarchy labels as specified in task
    try:
        # Gather all text from document (paragraphs + text boxes)
        all_texts_lower = set()
        for txbx in wps_txbxs + v_txbxs:
            t_elems = txbx.findall('.//w:t', ns)
            text = ''.join(t.text or '' for t in t_elems).strip()
            if text:
                all_texts_lower.add(text.lower())

        # Also check regular paragraphs (some implementations may use those)
        for para in doc.paragraphs:
            if para.text.strip():
                all_texts_lower.add(para.text.strip().lower())

        # Required leadership positions
        vp_found = any('vp of hr' in t or 'vp, hr' in t or 'vice president' in t and 'hr' in t
                        for t in all_texts_lower)
        dir_recruiting = any('director' in t and 'recruit' in t for t in all_texts_lower)
        dir_benefits = any('director' in t and 'benefit' in t for t in all_texts_lower)
        dir_employee = any('director' in t and ('employee' in t or 'relations' in t) for t in all_texts_lower)

        positions_found = [vp_found, dir_recruiting, dir_benefits, dir_employee]
        count_found = sum(positions_found)

        if count_found == 4:
            print(f"PASS: Component 2 — All 4 key positions found: VP of HR + 3 Directors (0.25 pts)")
            total_score += 0.25
        elif count_found == 3:
            print(f"PARTIAL: Component 2 — Found 3/4 key positions (0.18 pts)")
            print(f"  VP={vp_found}, Dir.Recruiting={dir_recruiting}, Dir.Benefits={dir_benefits}, Dir.EmpRel={dir_employee}")
            total_score += 0.18
        elif count_found == 2:
            print(f"PARTIAL: Component 2 — Found 2/4 key positions (0.12 pts)")
            total_score += 0.12
        elif count_found == 1:
            print(f"PARTIAL: Component 2 — Found 1/4 key positions (0.06 pts)")
            total_score += 0.06
        else:
            print(f"FAIL: Component 2 — None of the 4 key leadership positions found")
            print(f"  All text boxes: {list(all_texts_lower)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Manager positions (0.20 points) ---
    # At least 5 of 6 manager text boxes should be present
    try:
        # Look for manager-level text boxes
        manager_texts = [t for t in all_texts_lower if 'manager' in t or 'mgr' in t]
        mgr_count = len(manager_texts)

        # Also check for any recruiting, benefits, employee relations managers
        mgr_recruiting = sum(1 for t in all_texts_lower if 'manager' in t and 'recruit' in t)
        mgr_benefits = sum(1 for t in all_texts_lower if 'manager' in t and 'benefit' in t)
        mgr_emp_rel = sum(1 for t in all_texts_lower if ('manager' in t or 'mgr' in t) and
                          ('employee' in t or 'relations' in t or 'relation' in t))

        total_specific_mgrs = mgr_recruiting + mgr_benefits + mgr_emp_rel

        if mgr_count >= 6:
            print(f"PASS: Component 3 — Found {mgr_count} manager positions (need >= 5) (0.20 pts)")
            total_score += 0.20
        elif mgr_count >= 5:
            print(f"PASS: Component 3 — Found {mgr_count} manager positions (need >= 5) (0.20 pts)")
            total_score += 0.20
        elif mgr_count >= 3:
            print(f"PARTIAL: Component 3 — Found {mgr_count} manager positions (need >= 5) (0.10 pts)")
            total_score += 0.10
        elif mgr_count >= 1:
            print(f"PARTIAL: Component 3 — Found {mgr_count} manager positions (need >= 5) (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — No manager positions found (need >= 5)")
            print(f"  All text box texts: {list(all_texts_lower)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --- Component 4: Connector lines/shapes present (0.15 points) ---
    # Hierarchy must show connections between boxes via line shapes
    try:
        drawings = body.findall('.//w:drawing', ns)
        line_count = 0

        for drawing in drawings:
            xml = etree.tostring(drawing).decode()
            # Line shapes: prst="line" or "straightConnector1" or "bentConnector"
            # and shapes that have no txbx (not text boxes)
            has_txbx = 'txbx' in xml.lower() or 'textbox' in xml.lower()
            has_line = ('prst="line"' in xml or
                        'straightConnector' in xml or
                        'bentConnector' in xml or
                        'curvedConnector' in xml or
                        'cxnSp' in xml)
            if not has_txbx and has_line:
                line_count += 1

        # Also check for line shapes via prstGeom
        all_line_shapes = body.findall('.//a:prstGeom[@prst="line"]', ns)
        all_connector_shapes = body.findall('.//a:prstGeom[@prst="straightConnector1"]', ns)
        total_lines = max(line_count, len(all_line_shapes) + len(all_connector_shapes))

        # Each drawing marked as line
        # From our analysis: 9 line drawings expected
        if total_lines >= 7:
            print(f"PASS: Component 4 — Found {total_lines} connector/line shapes (need >= 5) (0.15 pts)")
            total_score += 0.15
        elif total_lines >= 5:
            print(f"PASS: Component 4 — Found {total_lines} connector/line shapes (need >= 5) (0.15 pts)")
            total_score += 0.15
        elif total_lines >= 3:
            print(f"PARTIAL: Component 4 — Found {total_lines} connector/line shapes (need >= 5) (0.08 pts)")
            total_score += 0.08
        elif total_lines >= 1:
            print(f"PARTIAL: Component 4 — Found {total_lines} connector/line shapes (need >= 5) (0.04 pts)")
            total_score += 0.04
        else:
            print(f"FAIL: Component 4 — No connector/line shapes found (need >= 5)")
            print(f"  Total drawings: {len(drawings)}, line_count: {line_count}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # --- Component 5: Consistent box formatting (0.15 points) ---
    # All text boxes should have consistent dimensions and bold text formatting
    try:
        # Get dimensions for each textbox
        all_cx = []
        all_cy = []
        bold_count = 0
        box_count = 0

        for txbx in wps_txbxs:
            wsp = txbx.getparent()
            if wsp is None:
                continue
            box_count += 1

            # Get shape size
            spPr = wsp.find('wps:spPr', ns)
            xfrm = spPr.find('.//a:xfrm', ns) if spPr is not None else None
            ext = xfrm.find('a:ext', ns) if xfrm is not None else None
            cx = int(ext.get('cx', 0)) if ext is not None else 0
            cy = int(ext.get('cy', 0)) if ext is not None else 0
            if cx > 0:
                all_cx.append(cx)
            if cy > 0:
                all_cy.append(cy)

            # Check bold formatting in runs
            rPr = wsp.find('.//w:rPr', ns)
            if rPr is not None:
                bold_elem = rPr.find('w:b', ns)
                if bold_elem is not None:
                    bold_count += 1

        # Check dimension consistency: all boxes should have same cx and cy
        consistent_dims = False
        if len(all_cx) >= 7:
            # Check if most boxes have the same dimensions
            from collections import Counter
            cx_counter = Counter(all_cx)
            cy_counter = Counter(all_cy)
            most_common_cx = cx_counter.most_common(1)[0][1]
            most_common_cy = cy_counter.most_common(1)[0][1]
            # More than 70% must share the same size
            if most_common_cx >= len(all_cx) * 0.7 and most_common_cy >= len(all_cy) * 0.7:
                consistent_dims = True

        # Check bold formatting consistency
        bold_ratio = bold_count / box_count if box_count > 0 else 0
        consistent_bold = bold_ratio >= 0.7  # at least 70% of boxes are bold

        if consistent_dims and consistent_bold:
            print(f"PASS: Component 5 — Consistent formatting: dims={consistent_dims}, bold_ratio={bold_ratio:.2f} (0.15 pts)")
            total_score += 0.15
        elif consistent_dims or consistent_bold:
            print(f"PARTIAL: Component 5 — Partially consistent: dims={consistent_dims}, bold_ratio={bold_ratio:.2f} (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 5 — Inconsistent formatting: dims={consistent_dims}, bold_ratio={bold_ratio:.2f}")
            print(f"  cx values: {all_cx}")
            print(f"  cy values: {all_cy}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved LibreOffice state before scoring
persist_app_state()

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
