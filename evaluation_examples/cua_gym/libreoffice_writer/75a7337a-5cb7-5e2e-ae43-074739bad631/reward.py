"""
Reward Script: Verify footnote paragraph style modifications in Writer document
Task ID: writer_bs_041
Domain: libreoffice_writer
Scoring:
  Component 1: Font name = Liberation Serif in FootnoteText style (0.20 pts)
  Component 2: Font size = 8pt in FootnoteText style (0.20 pts)
  Component 3: Left indent ~0.3cm in FootnoteText style (0.20 pts)
  Component 4: Tab stop at ~0.5cm in FootnoteText style (0.15 pts)
  Component 5: Period after footnote reference number (0.15 pts)
  Component 6: Tab character after period in footnote content (0.10 pts)
"""

import os
import time
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_041'


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Style-level checks ---
    # Find the FootnoteText style (may be 'FootnoteText' or 'Footnote' after LO re-save)
    fn_style = None
    for style in doc.styles:
        if style.style_id in ('FootnoteText', 'Footnote'):
            fn_style = style
            break
        if style.name and 'footnote' in style.name.lower() and 'text' in style.name.lower():
            fn_style = style
            break

    if fn_style is None:
        # Also try by name pattern (Footnote Text, footnote text)
        for style in doc.styles:
            if style.name and 'footnote' in style.name.lower() and style.type is not None:
                from docx.enum.style import WD_STYLE_TYPE
                if style.type == WD_STYLE_TYPE.PARAGRAPH:
                    fn_style = style
                    break

    if fn_style is None:
        print("CRITICAL: FootnoteText/Footnote paragraph style not found in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found footnote style: name='{fn_style.name}', id='{fn_style.style_id}'")

    # Also parse the raw XML of the style for precise checks
    style_xml = ET.tostring(fn_style.element, encoding='unicode')
    style_root = fn_style.element
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Component 1: Font name = Liberation Serif (0.20 points)
    try:
        rpr = style_root.find('.//w:rPr', ns)
        font_name = None
        if rpr is not None:
            rfonts = rpr.find('w:rFonts', ns)
            if rfonts is not None:
                font_name = rfonts.attrib.get(qn('w:ascii'))
        # Also check via python-docx API
        api_font_name = fn_style.font.name

        if font_name == 'Liberation Serif' or api_font_name == 'Liberation Serif':
            print(f"PASS: Component 1 -- Font name is Liberation Serif (xml={font_name}, api={api_font_name}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- Expected font 'Liberation Serif', found xml={font_name}, api={api_font_name}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Font size = 8pt (16 half-points in XML, or 101600 EMU) (0.20 points)
    try:
        sz_val = None
        if rpr is not None:
            sz = rpr.find('w:sz', ns)
            if sz is not None:
                sz_val = sz.attrib.get(qn('w:val'))
        # Also check via API
        api_size = fn_style.font.size
        api_size_pt = api_size.pt if api_size else None

        # 8pt = 16 half-points in XML
        size_ok = False
        if sz_val is not None and int(sz_val) == 16:
            size_ok = True
        elif api_size_pt is not None and abs(api_size_pt - 8.0) < 0.5:
            size_ok = True

        if size_ok:
            print(f"PASS: Component 2 -- Font size is 8pt (xml_half_pt={sz_val}, api_pt={api_size_pt}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- Expected 8pt (16 half-pt), found xml_half_pt={sz_val}, api_pt={api_size_pt}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Left indent ~0.3cm (approx 170 twips) (0.20 points)
    # 0.3cm = 170.1 twips (1 twip = 1/567 cm, so 0.3*567 = 170.1)
    # Allow tolerance of +/- 10 twips
    try:
        ppr = style_root.find('.//w:pPr', ns)
        ind_left = None
        if ppr is not None:
            ind = ppr.find('w:ind', ns)
            if ind is not None:
                ind_left_str = ind.attrib.get(qn('w:left'))
                if ind_left_str is not None:
                    ind_left = int(ind_left_str)

        # Also check via API (returns EMU)
        api_indent = fn_style.paragraph_format.left_indent
        api_indent_twips = None
        if api_indent is not None:
            # 1 twip = 635 EMU (1 inch = 914400 EMU, 1 inch = 1440 twips)
            api_indent_twips = api_indent / 635.0

        target_twips = 170  # 0.3cm
        tolerance = 15  # twips

        indent_ok = False
        if ind_left is not None and abs(ind_left - target_twips) <= tolerance:
            indent_ok = True
        elif api_indent_twips is not None and abs(api_indent_twips - target_twips) <= tolerance:
            indent_ok = True

        if indent_ok:
            api_twips_str = f"{api_indent_twips:.1f}" if api_indent_twips is not None else "None"
            print(f"PASS: Component 3 -- Left indent ~0.3cm (xml_twips={ind_left}, api_twips={api_twips_str}) (0.20 pts)")
            total_score += 0.20
        else:
            api_twips_str = f"{api_indent_twips:.1f}" if api_indent_twips is not None else "None"
            print(f"FAIL: Component 3 -- Expected left indent ~170 twips (0.3cm), found xml_twips={ind_left}, api_twips={api_twips_str}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Tab stop at ~0.5cm (approx 283 twips) (0.15 points)
    # 0.5cm = 283.5 twips
    try:
        tab_found = False
        target_tab = 283  # twips
        tab_tolerance = 15

        if ppr is not None:
            tabs_elem = ppr.find('w:tabs', ns)
            if tabs_elem is not None:
                for tab in tabs_elem.findall('w:tab', ns):
                    pos_str = tab.attrib.get(qn('w:pos'))
                    if pos_str is not None:
                        pos = int(pos_str)
                        if abs(pos - target_tab) <= tab_tolerance:
                            tab_found = True
                            print(f"PASS: Component 4 -- Tab stop at ~0.5cm (pos={pos} twips) (0.15 pts)")
                            total_score += 0.15
                            break

        if not tab_found:
            # Try via API
            try:
                for ts in fn_style.paragraph_format.tab_stops:
                    # ts.position is in EMU
                    ts_twips = ts.position / 635.0
                    if abs(ts_twips - target_tab) <= tab_tolerance:
                        tab_found = True
                        print(f"PASS: Component 4 -- Tab stop at ~0.5cm (api_twips={ts_twips:.1f}) (0.15 pts)")
                        total_score += 0.15
                        break
            except Exception:
                pass

        if not tab_found:
            print(f"FAIL: Component 4 -- No tab stop found at ~283 twips (0.5cm)")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # --- Footnote content checks ---
    # Get the footnotes XML part
    footnotes_part = None
    try:
        for rel in doc.part.rels.values():
            if 'footnotes' in rel.reltype:
                footnotes_part = rel.target_part
                break
    except Exception as e:
        print(f"ERROR: Cannot access footnotes part: {e}")

    if footnotes_part is None:
        print("FAIL: Components 5-6 -- No footnotes part found")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    try:
        fn_root = ET.fromstring(footnotes_part.blob)
    except Exception as e:
        print(f"ERROR: Cannot parse footnotes XML: {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Collect real footnotes (id >= 2, skip separator footnotes 0 and 1)
    real_footnotes = []
    for fn in fn_root.findall('.//w:footnote', ns):
        fn_id = fn.attrib.get(qn('w:id'), '0')
        if int(fn_id) >= 2:
            real_footnotes.append(fn)

    if len(real_footnotes) == 0:
        print("FAIL: Components 5-6 -- No real footnotes found (expected 6)")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 5: Period after footnote reference number (0.15 points)
    # In golden: after <w:footnoteRef/>, the next run contains "."
    # In initial: after <w:footnoteRef/>, the next run contains " " (space)
    try:
        period_count = 0
        for fn in real_footnotes:
            paras = fn.findall('.//w:p', ns)
            for p in paras:
                runs = p.findall('w:r', ns)
                found_ref = False
                for i, r in enumerate(runs):
                    if r.find('.//w:footnoteRef', ns) is not None:
                        found_ref = True
                        # Check next run for period
                        if i + 1 < len(runs):
                            next_run = runs[i + 1]
                            t_elems = next_run.findall('.//w:t', ns)
                            next_text = ''.join(t.text or '' for t in t_elems)
                            if '.' in next_text:
                                period_count += 1
                        break

        total_fn = len(real_footnotes)
        if period_count >= total_fn and total_fn > 0:
            print(f"PASS: Component 5 -- Period found after footnote ref in all {period_count}/{total_fn} footnotes (0.15 pts)")
            total_score += 0.15
        elif period_count > 0:
            partial = 0.15 * (period_count / total_fn)
            print(f"PARTIAL: Component 5 -- Period found in {period_count}/{total_fn} footnotes ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 -- No periods found after footnote references (0/{total_fn})")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Tab character after period in footnote content (0.10 points)
    # In golden: <w:tab/> element in a run after the period run
    try:
        tab_count = 0
        for fn in real_footnotes:
            paras = fn.findall('.//w:p', ns)
            for p in paras:
                runs = p.findall('w:r', ns)
                found_ref = False
                for i, r in enumerate(runs):
                    if r.find('.//w:footnoteRef', ns) is not None:
                        found_ref = True
                        # Look for a <w:tab/> element in subsequent runs (within next 3 runs)
                        for j in range(i + 1, min(i + 4, len(runs))):
                            if runs[j].find('.//w:tab', ns) is not None:
                                tab_count += 1
                                break
                        break

        total_fn = len(real_footnotes)
        if tab_count >= total_fn and total_fn > 0:
            print(f"PASS: Component 6 -- Tab character found in all {tab_count}/{total_fn} footnotes (0.10 pts)")
            total_score += 0.10
        elif tab_count > 0:
            partial = 0.10 * (tab_count / total_fn)
            print(f"PARTIAL: Component 6 -- Tab found in {tab_count}/{total_fn} footnotes ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 -- No tab characters found in footnotes (0/{total_fn})")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
