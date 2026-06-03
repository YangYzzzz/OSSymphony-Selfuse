"""
Reward Script: Create 'Emphasis Strong' character style and apply to five key phrases
Task ID: writer_rd_053
Domain: libreoffice_writer
Scoring:
  Component 1: 'Emphasis Strong' style definition exists with correct properties (0.25)
  Component 2: All 5 phrases reference the EmphasisStrong rStyle (0.25)
  Component 3: All 5 phrases have bold + dark red (#8B0000) + expanded spacing (0.30)
  Component 4: Underline removed from all 5 phrases (0.20)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_053'

TARGET_PHRASES = [
    'critical issue',
    'unprecedented growth',
    'immediate action required',
    'fundamental change',
    'long-term strategy',
]


def persist_app_state(domain):
    """Best-effort save for LibreOffice Writer."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for %s" % domain)
    except Exception as e:
        print("PERSIST_WARN: save hook failed: %s" % e)


def find_phrase_runs(doc, phrases):
    """For each phrase, find the run(s) that contain it.
    Returns dict: phrase -> list of (run, paragraph) tuples.
    """
    from docx.oxml.ns import qn
    result = {p: [] for p in phrases}
    for para in doc.paragraphs:
        text_lower = para.text.lower()
        for phrase in phrases:
            if phrase in text_lower:
                for run in para.runs:
                    if phrase in run.text.lower():
                        result[phrase].append((run, para))
                        break
    return result


def verify_task(file_path):
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    from docx import Document
    from docx.oxml.ns import qn

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 1: 'Emphasis Strong' character style exists with
    #   bold, color #8B0000, spacing 20 (1pt expanded)  — 0.25 pts
    # ---------------------------------------------------------------
    try:
        style_found = False
        style_props_ok = False

        # Search in styles XML for the custom style
        styles_el = doc.styles.element
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

        for style_el in styles_el.findall('.//w:style', ns):
            name_el = style_el.find('w:name', ns)
            stype = style_el.get(qn('w:type'))
            if name_el is not None and name_el.get(qn('w:val')) == 'Emphasis Strong' and stype == 'character':
                style_found = True
                # Verify style run properties
                rpr = style_el.find('w:rPr', ns)
                if rpr is not None:
                    has_bold = rpr.find('w:b', ns) is not None
                    color_el = rpr.find('w:color', ns)
                    has_color = color_el is not None and color_el.get(qn('w:val'), '').upper() == '8B0000'
                    spacing_el = rpr.find('w:spacing', ns)
                    has_spacing = spacing_el is not None and spacing_el.get(qn('w:val')) == '20'
                    style_props_ok = has_bold and has_color and has_spacing
                    print("DETAIL: Style rPr — bold=%s, color=%s, spacing=%s" % (has_bold, has_color, has_spacing))
                break

        if style_found and style_props_ok:
            print("PASS: Component 1 — 'Emphasis Strong' style exists with correct properties (0.25 pts)")
            total_score += 0.25
        elif style_found:
            print("PARTIAL: Component 1 — Style exists but properties incomplete (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 1 — 'Emphasis Strong' character style not found")
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # ---------------------------------------------------------------
    # Component 2: All 5 phrases reference rStyle=EmphasisStrong
    #   — 0.25 pts (0.05 per phrase)
    # ---------------------------------------------------------------
    try:
        phrase_runs = find_phrase_runs(doc, TARGET_PHRASES)
        rstyle_count = 0

        for phrase in TARGET_PHRASES:
            runs = phrase_runs[phrase]
            if runs:
                run, para = runs[0]
                rpr = run._element.find(qn('w:rPr'))
                if rpr is not None:
                    rs = rpr.find(qn('w:rStyle'))
                    if rs is not None and rs.get(qn('w:val')) == 'EmphasisStrong':
                        rstyle_count += 1
                        print("PASS: Component 2 — '%s' has rStyle=EmphasisStrong" % phrase)
                    else:
                        rs_val = rs.get(qn('w:val')) if rs is not None else None
                        print("FAIL: Component 2 — '%s' rStyle=%s (expected EmphasisStrong)" % (phrase, rs_val))
                else:
                    print("FAIL: Component 2 — '%s' has no rPr element" % phrase)
            else:
                print("FAIL: Component 2 — phrase '%s' not found in document" % phrase)

        comp2_score = rstyle_count * 0.05
        if rstyle_count == 5:
            print("PASS: Component 2 — All 5/5 phrases reference EmphasisStrong (0.25 pts)")
        else:
            print("PARTIAL: Component 2 — %d/5 phrases reference EmphasisStrong (%.2f pts)" % (rstyle_count, comp2_score))
        total_score += comp2_score
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # ---------------------------------------------------------------
    # Component 3: All 5 phrases have bold + dark red #8B0000 +
    #   expanded spacing (val=20)  — 0.30 pts (0.06 per phrase)
    # ---------------------------------------------------------------
    try:
        phrase_runs = find_phrase_runs(doc, TARGET_PHRASES)
        format_count = 0

        for phrase in TARGET_PHRASES:
            runs = phrase_runs[phrase]
            if runs:
                run, para = runs[0]
                # Check bold — either direct or inherited from style
                is_bold = run.font.bold is True
                if not is_bold:
                    # Check via XML
                    rpr = run._element.find(qn('w:rPr'))
                    if rpr is not None and rpr.find(qn('w:b')) is not None:
                        is_bold = True

                # Check color
                has_dark_red = False
                try:
                    rgb = run.font.color.rgb
                    if rgb is not None and str(rgb).upper() == '8B0000':
                        has_dark_red = True
                except:
                    pass
                if not has_dark_red:
                    rpr = run._element.find(qn('w:rPr'))
                    if rpr is not None:
                        c = rpr.find(qn('w:color'))
                        if c is not None and c.get(qn('w:val'), '').upper() == '8B0000':
                            has_dark_red = True

                # Check spacing
                has_spacing = False
                rpr = run._element.find(qn('w:rPr'))
                if rpr is not None:
                    sp = rpr.find(qn('w:spacing'))
                    if sp is not None and sp.get(qn('w:val')) == '20':
                        has_spacing = True

                if is_bold and has_dark_red and has_spacing:
                    format_count += 1
                    print("PASS: Component 3 — '%s' has bold+darkred+spacing" % phrase)
                else:
                    print("FAIL: Component 3 — '%s' bold=%s, darkred=%s, spacing=%s" % (phrase, is_bold, has_dark_red, has_spacing))
            else:
                print("FAIL: Component 3 — phrase '%s' not found" % phrase)

        comp3_score = format_count * 0.06
        if format_count == 5:
            print("PASS: Component 3 — All 5/5 phrases correctly formatted (0.30 pts)")
        else:
            print("PARTIAL: Component 3 — %d/5 phrases formatted (%.2f pts)" % (format_count, comp3_score))
        total_score += comp3_score
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    # ---------------------------------------------------------------
    # Component 4: Underline removed from all 5 phrases — 0.20 pts
    #   (0.04 per phrase)
    # ---------------------------------------------------------------
    try:
        phrase_runs = find_phrase_runs(doc, TARGET_PHRASES)
        no_underline_count = 0

        for phrase in TARGET_PHRASES:
            runs = phrase_runs[phrase]
            if runs:
                run, para = runs[0]
                # underline must be explicitly False or absent (None can mean inherit)
                # Check XML directly for w:u element
                rpr = run._element.find(qn('w:rPr'))
                has_underline = False
                if rpr is not None:
                    u_el = rpr.find(qn('w:u'))
                    if u_el is not None:
                        uval = u_el.get(qn('w:val'), 'single')
                        if uval != 'none':
                            has_underline = True

                if run.font.underline is True:
                    has_underline = True

                if not has_underline:
                    no_underline_count += 1
                    print("PASS: Component 4 — '%s' underline removed" % phrase)
                else:
                    print("FAIL: Component 4 — '%s' still underlined" % phrase)
            else:
                print("FAIL: Component 4 — phrase '%s' not found" % phrase)

        comp4_score = no_underline_count * 0.04
        if no_underline_count == 5:
            print("PASS: Component 4 — Underline removed from all 5/5 phrases (0.20 pts)")
        else:
            print("PARTIAL: Component 4 — %d/5 phrases de-underlined (%.2f pts)" % (no_underline_count, comp4_score))
        total_score += comp4_score
    except Exception as e:
        print("ERROR: Component 4 — %s" % e)

    final_score = min(round(total_score, 2), 1.0)
    print("")
    print("Score: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = os.path.join(WORKDIR, TASK_ID + '.docx')
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
