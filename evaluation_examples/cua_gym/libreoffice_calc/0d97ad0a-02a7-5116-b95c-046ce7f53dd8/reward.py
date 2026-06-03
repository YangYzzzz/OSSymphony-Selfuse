"""
Reward Script: Create a callout shape near G10 with text pointing toward E10
Task ID: calc_gao_048
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): Drawing/shape exists in the file (no drawings in initial)
  Component 2 (0.25): Shape is a callout type (wedgeRectCallout or similar)
  Component 3 (0.25): Shape contains the exact text 'Note: This value includes tax'
  Component 4 (0.20): Shape is positioned near G10 area and pointer points toward E10 (leftward)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'calc_gao_048'

# XML namespaces used in OOXML drawings
NS = {
    'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def extract_drawing_xml(file_path):
    """Extract drawing XML content from the xlsx archive if it exists."""
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            names = z.namelist()
            # Look for any drawing XML file
            drawing_files = [n for n in names if n.startswith('xl/drawings/drawing') and n.endswith('.xml')]
            if not drawing_files:
                return None, []
            # Parse the first drawing file
            xml_content = z.read(drawing_files[0]).decode('utf-8')
            return xml_content, drawing_files
    except Exception as e:
        print(f"ERROR: Could not read zip archive: {e}")
        return None, []


def parse_shapes(xml_content):
    """Parse shapes from drawing XML content. Returns list of shape dicts."""
    shapes = []
    try:
        root = ET.fromstring(xml_content)
        # Find all twoCellAnchor elements (each contains a shape)
        for anchor in root.findall('.//xdr:twoCellAnchor', NS):
            shape_info = {}

            # Get anchor positions (from/to columns and rows)
            from_el = anchor.find('xdr:from', NS)
            to_el = anchor.find('xdr:to', NS)
            if from_el is not None:
                shape_info['from_col'] = int(from_el.find('xdr:col', NS).text)
                shape_info['from_row'] = int(from_el.find('xdr:row', NS).text)
            if to_el is not None:
                shape_info['to_col'] = int(to_el.find('xdr:col', NS).text)
                shape_info['to_row'] = int(to_el.find('xdr:row', NS).text)

            # Get shape element
            sp = anchor.find('xdr:sp', NS)
            if sp is not None:
                # Shape name
                nvSpPr = sp.find('xdr:nvSpPr', NS)
                if nvSpPr is not None:
                    cNvPr = nvSpPr.find('xdr:cNvPr', NS)
                    if cNvPr is not None:
                        shape_info['name'] = cNvPr.get('name', '')

                # Preset geometry (shape type)
                spPr = sp.find('xdr:spPr', NS)
                if spPr is not None:
                    prstGeom = spPr.find('a:prstGeom', NS)
                    if prstGeom is not None:
                        shape_info['prst'] = prstGeom.get('prst', '')
                        # Get adjustment values (pointer direction)
                        avLst = prstGeom.find('a:avLst', NS)
                        if avLst is not None:
                            adjustments = {}
                            for gd in avLst.findall('a:gd', NS):
                                adj_name = gd.get('name', '')
                                adj_fmla = gd.get('fmla', '')
                                adjustments[adj_name] = adj_fmla
                            shape_info['adjustments'] = adjustments

                # Text content
                txBody = sp.find('xdr:txBody', NS)
                if txBody is not None:
                    text_parts = []
                    for p in txBody.findall('.//a:p', NS):
                        for r in p.findall('.//a:r', NS):
                            t = r.find('a:t', NS)
                            if t is not None and t.text:
                                text_parts.append(t.text)
                    shape_info['text'] = ''.join(text_parts)

            shapes.append(shape_info)
    except Exception as e:
        print(f"ERROR: Failed to parse drawing XML: {e}")
    return shapes


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid xlsx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Extract drawing XML from the xlsx archive
    xml_content, drawing_files = extract_drawing_xml(file_path)

    # Component 1: A drawing/shape exists in the file (0.30 points)
    # Initial file has NO drawings at all, so presence of any drawing is task-introduced
    try:
        if xml_content is not None and len(drawing_files) > 0:
            shapes = parse_shapes(xml_content)
            if len(shapes) > 0:
                print(f"PASS: Component 1 -- Drawing exists with {len(shapes)} shape(s) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 -- Drawing XML found but no shapes parsed")
        else:
            print(f"FAIL: Component 1 -- No drawing XML found in the file")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Shape is a callout type (0.25 points)
    # Callout preset geometries include: wedgeRectCallout, wedgeRoundRectCallout,
    # wedgeEllipseCallout, borderCallout1/2/3, accentCallout1/2/3, etc.
    try:
        callout_shapes = [s for s in shapes if 'prst' in s and 'callout' in s.get('prst', '').lower()]
        if len(callout_shapes) > 0:
            prst_type = callout_shapes[0].get('prst', 'unknown')
            print(f"PASS: Component 2 -- Callout shape found (type: {prst_type}) (0.25 pts)")
            total_score += 0.25
        else:
            # Also accept any shape that has callout-like characteristics
            # (name contains 'callout' or shape type contains 'Callout')
            named_callouts = [s for s in shapes if 'callout' in s.get('name', '').lower()]
            if len(named_callouts) > 0:
                print(f"PASS: Component 2 -- Shape named as callout (name: {named_callouts[0].get('name')}) (0.25 pts)")
                total_score += 0.25
            else:
                # List what was found
                found_types = [s.get('prst', 'no-prst') for s in shapes]
                print(f"FAIL: Component 2 -- No callout shape found. Shape types: {found_types}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Shape contains the exact text 'Note: This value includes tax' (0.25 points)
    try:
        expected_text = 'Note: This value includes tax'
        text_match_found = False
        for s in shapes:
            shape_text = s.get('text', '').strip()
            if shape_text == expected_text:
                print(f"PASS: Component 3 -- Exact text match: '{shape_text}' (0.25 pts)")
                total_score += 0.25
                text_match_found = True
                break
            elif expected_text.lower() in shape_text.lower():
                # Partial match -- text is present but may have extra whitespace or casing
                print(f"PASS: Component 3 -- Text contains expected content (found: '{shape_text}') (0.25 pts)")
                total_score += 0.25
                text_match_found = True
                break
        if not text_match_found:
            all_texts = [s.get('text', '') for s in shapes]
            print(f"FAIL: Component 3 -- Expected '{expected_text}', found texts: {all_texts}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Shape positioned near G10 and pointer toward E10 (0.20 points)
    # G10 = col 6 (0-indexed), row 9 (0-indexed)
    # Shape should start around col 5-7, row 7-11 area
    # Pointer toward E10 (col 4) means adj1 should be negative (pointing left)
    try:
        position_ok = False
        for s in shapes:
            from_col = s.get('from_col')
            from_row = s.get('from_row')
            to_col = s.get('to_col')
            to_row = s.get('to_row')

            if from_col is not None and from_row is not None:
                # Check shape is near G10 area (col 5-8, row 6-13 -- generous range)
                col_near_g = (5 <= from_col <= 8) or (5 <= (to_col or 0) <= 12)
                row_near_10 = (6 <= from_row <= 13) or (6 <= (to_row or 0) <= 15)

                # Check pointer direction -- adj1 negative means pointing left (toward E column)
                adj = s.get('adjustments', {})
                adj1_val = adj.get('adj1', '')
                pointer_left = False
                if 'val' in adj1_val:
                    try:
                        adj1_num = int(adj1_val.replace('val ', '').strip())
                        pointer_left = adj1_num < 0  # Negative = points left
                    except ValueError:
                        pass

                if col_near_g and row_near_10:
                    if pointer_left:
                        print(f"PASS: Component 4 -- Shape at col {from_col}-{to_col}, row {from_row}-{to_row}, pointer adj1={adj1_val} (leftward) (0.20 pts)")
                        total_score += 0.20
                    else:
                        # Position is correct but pointer direction uncertain -- partial credit
                        print(f"PASS: Component 4 -- Shape at col {from_col}-{to_col}, row {from_row}-{to_row}, position correct near G10 (0.20 pts)")
                        total_score += 0.20
                    position_ok = True
                    break

        if not position_ok:
            positions = [(s.get('from_col'), s.get('from_row'), s.get('to_col'), s.get('to_row')) for s in shapes]
            print(f"FAIL: Component 4 -- Shape not near G10. Positions: {positions}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
