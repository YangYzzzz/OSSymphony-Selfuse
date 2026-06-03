"""
Reward Script: Import styles from thesis_styles.odt into writer_bs_083.odt
Task ID: writer_bs_083
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Thesis Heading style exists in document
  Component 2 (0.25): Thesis Body style exists in document
  Component 3 (0.25): Heading 1 style overwritten with thesis_styles.odt properties
  Component 4 (0.25): My Note and My Quote styles preserved unchanged
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_083'

STYLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'
FO_NS = 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'


def get_style_name(elem):
    """Get the style:name attribute from an element using the attributes dict."""
    if hasattr(elem, 'attributes') and elem.attributes:
        return elem.attributes.get((STYLE_NS, 'name'))
    return None


def get_style_attrs(style_elem):
    """Extract key attributes from a style element's child nodes."""
    attrs = {}
    for child in style_elem.childNodes:
        if hasattr(child, 'attributes') and child.attributes:
            for key, val in child.attributes.items():
                attrs[key] = val
    return attrs


def find_style_by_name(doc, target_name):
    """Find a named style in the document's styles using attributes dict."""
    for child in doc.styles.childNodes:
        name = get_style_name(child)
        if name == target_name:
            return child
    return None


def persist_app_state(domain):
    """Send Ctrl+S to save any unsaved changes in LibreOffice."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
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
        from odf.opendocument import load
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a set of all style names present
    style_names = set()
    for child in doc.styles.childNodes:
        name = get_style_name(child)
        if name:
            style_names.add(name)

    # Component 1: Thesis Heading style exists (0.25 points)
    # This style should be newly imported from thesis_styles.odt
    try:
        thesis_heading = find_style_by_name(doc, 'Thesis_20_Heading')
        if thesis_heading is not None:
            # Verify it has expected properties: 18pt, bold, centered, dark red color
            attrs = get_style_attrs(thesis_heading)
            font_size_ok = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'font-size')) == '18pt'
            font_weight_ok = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'font-weight')) == 'bold'
            if font_size_ok and font_weight_ok:
                print(f"PASS: Component 1 -- Thesis Heading style exists with correct properties (0.25 pts)")
                total_score += 0.25
            else:
                print(f"PARTIAL: Component 1 -- Thesis Heading exists but properties differ (font_size={font_size_ok}, weight={font_weight_ok})")
                total_score += 0.1
        else:
            print(f"FAIL: Component 1 -- Thesis Heading style not found. Available: {style_names}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Thesis Body style exists (0.25 points)
    # This style should be newly imported from thesis_styles.odt
    try:
        thesis_body = find_style_by_name(doc, 'Thesis_20_Body')
        if thesis_body is not None:
            # Verify it has expected properties: 12pt, justified, Times New Roman
            attrs = get_style_attrs(thesis_body)
            font_size_ok = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'font-size')) == '12pt'
            text_align_ok = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'text-align')) == 'justify'
            if font_size_ok and text_align_ok:
                print(f"PASS: Component 2 -- Thesis Body style exists with correct properties (0.25 pts)")
                total_score += 0.25
            else:
                print(f"PARTIAL: Component 2 -- Thesis Body exists but properties differ (font_size={font_size_ok}, align={text_align_ok})")
                total_score += 0.1
        else:
            print(f"FAIL: Component 2 -- Thesis Body style not found. Available: {style_names}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Heading 1 style overwritten with thesis_styles.odt properties (0.25 points)
    # The modified Heading 1 from thesis_styles.odt should have: 20pt, bold, Times New Roman,
    # dark green color (#006400), underline
    try:
        heading1 = find_style_by_name(doc, 'Heading_20_1')
        if heading1 is not None:
            attrs = get_style_attrs(heading1)
            # Check key distinguishing properties from the thesis_styles version
            font_size = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'font-size'))
            font_name = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:style:1.0', 'font-name'))
            color = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'color'))
            underline = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:style:1.0', 'text-underline-style'))

            checks = {
                'font_size_20pt': font_size == '20pt',
                'font_times_new_roman': font_name == 'Times New Roman',
                'color_dark_green': color == '#006400',
                'underline_solid': underline == 'solid',
            }
            passed = sum(1 for v in checks.values() if v)
            print(f"  Heading 1 checks: {checks}")

            if passed >= 3:
                print(f"PASS: Component 3 -- Heading 1 overwritten with thesis_styles properties ({passed}/4 checks) (0.25 pts)")
                total_score += 0.25
            elif passed >= 1:
                partial = round(0.25 * passed / 4, 2)
                print(f"PARTIAL: Component 3 -- Heading 1 partially overwritten ({passed}/4 checks) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- Heading 1 not overwritten (0/4 checks passed)")
        else:
            print(f"FAIL: Component 3 -- Heading 1 style not found in document")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: My Note and My Quote styles preserved unchanged (0.25 points)
    # These styles should remain identical to the initial state
    try:
        my_note = find_style_by_name(doc, 'My_20_Note')
        my_quote = find_style_by_name(doc, 'My_20_Quote')

        note_ok = False
        quote_ok = False

        if my_note is not None:
            attrs = get_style_attrs(my_note)
            # My Note: 10pt, italic, color #666666
            note_size = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'font-size')) == '10pt'
            note_italic = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'font-style')) == 'italic'
            note_color = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'color')) == '#666666'
            note_ok = note_size and note_italic and note_color
            print(f"  My Note: size={note_size}, italic={note_italic}, color={note_color}")
        else:
            print(f"  My Note: NOT FOUND")

        if my_quote is not None:
            attrs = get_style_attrs(my_quote)
            # My Quote: 12pt, center-aligned, Times New Roman, color #1a3c6e
            quote_size = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'font-size')) == '12pt'
            quote_align = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'text-align')) == 'center'
            quote_color = attrs.get(('urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0', 'color')) == '#1a3c6e'
            quote_ok = quote_size and quote_align and quote_color
            print(f"  My Quote: size={quote_size}, align={quote_align}, color={quote_color}")
        else:
            print(f"  My Quote: NOT FOUND")

        # This component checks preservation - but we only award points if the
        # imported styles also exist (otherwise the task wasn't done at all)
        # We combine preservation check with existence of at least one imported style
        has_imported = ('Thesis_20_Heading' in style_names or 'Thesis_20_Body' in style_names)

        if note_ok and quote_ok and has_imported:
            print(f"PASS: Component 4 -- My Note and My Quote preserved unchanged (0.25 pts)")
            total_score += 0.25
        elif note_ok and quote_ok and not has_imported:
            # Styles preserved but nothing imported - this is initial state, award 0
            print(f"FAIL: Component 4 -- Styles preserved but no imported styles found (initial state)")
        elif note_ok or quote_ok:
            partial = 0.125 if has_imported else 0.0
            print(f"PARTIAL: Component 4 -- Only one style preserved (note={note_ok}, quote={quote_ok}) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Both My Note and My Quote are missing or corrupted")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
