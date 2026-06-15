"""
Reward Script: Edit master slide body text style to Open Sans 20pt with 1.5 line spacing
Task ID: impress_ma_014
Domain: libreoffice_impress
Scoring:
  Component 1: Font name is 'Open Sans' on master body placeholder (0.35)
  Component 2: Font size is 20pt (2000 hundredths) on master body placeholder (0.35)
  Component 3: Line spacing is 1.5 lines (150% / 150000 spcPct) in bodyStyle (0.30)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_014'

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice before verifying."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_body_placeholder_fonts(pptx_path):
    """
    Extract font name and size from the body placeholder (idx=1) shape runs
    in slideMaster1.xml. Returns list of (typeface, sz) tuples.
    """
    fonts = []
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            with zf.open('ppt/slideMasters/slideMaster1.xml') as f:
                root = ET.parse(f).getroot()
                for sp in root.findall('.//p:sp', NS):
                    ph = sp.find('.//p:nvSpPr/p:nvPr/p:ph', NS)
                    if ph is not None and ph.get('idx') == '1':
                        for r in sp.findall('.//a:r', NS):
                            rPr = r.find('a:rPr', NS)
                            if rPr is not None:
                                sz = rPr.get('sz')
                                latin = rPr.find('a:latin', NS)
                                tf = latin.get('typeface') if latin is not None else None
                                fonts.append((tf, sz))
                        break
    except Exception as e:
        print(f"ERROR: Could not parse body placeholder fonts: {e}")
    return fonts


def get_body_style_properties(pptx_path):
    """
    Extract font, size, and line spacing from bodyStyle/lvl1pPr in txStyles
    of slideMaster1.xml.
    Returns dict with keys: typeface, sz, lnSpc_pct
    """
    result = {'typeface': None, 'sz': None, 'lnSpc_pct': None}
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            with zf.open('ppt/slideMasters/slideMaster1.xml') as f:
                root = ET.parse(f).getroot()
                txStyles = root.find('.//p:txStyles', NS)
                if txStyles is not None:
                    bodyStyle = txStyles.find('p:bodyStyle', NS)
                    if bodyStyle is not None:
                        lvl1 = bodyStyle.find('a:lvl1pPr', NS)
                        if lvl1 is not None:
                            # Line spacing
                            lnSpc = lvl1.find('a:lnSpc', NS)
                            if lnSpc is not None:
                                spcPct = lnSpc.find('a:spcPct', NS)
                                if spcPct is not None:
                                    result['lnSpc_pct'] = spcPct.get('val')
                            # Font from defRPr
                            defRPr = lvl1.find('a:defRPr', NS)
                            if defRPr is not None:
                                result['sz'] = defRPr.get('sz')
                                latin = defRPr.find('a:latin', NS)
                                if latin is not None:
                                    result['typeface'] = latin.get('typeface')
    except Exception as e:
        print(f"ERROR: Could not parse bodyStyle properties: {e}")
    return result


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

    # Get data from both the body placeholder shape and the bodyStyle
    ph_fonts = get_body_placeholder_fonts(file_path)
    body_style = get_body_style_properties(file_path)

    # Component 1: Font name is 'Open Sans' (0.35 points)
    # Check both the placeholder shape runs and the bodyStyle defRPr
    try:
        # Check placeholder shape runs — all should be Open Sans
        ph_font_names = [tf for tf, sz in ph_fonts if tf is not None]
        all_ph_open_sans = len(ph_font_names) > 0 and all(
            tf == 'Open Sans' for tf in ph_font_names
        )
        # Check bodyStyle lvl1pPr
        style_font_open_sans = body_style.get('typeface') == 'Open Sans'

        # Accept if either location shows Open Sans (different edit methods)
        if all_ph_open_sans or style_font_open_sans:
            details = []
            if all_ph_open_sans:
                details.append(f"placeholder runs: {ph_font_names}")
            if style_font_open_sans:
                details.append(f"bodyStyle: {body_style.get('typeface')}")
            print(f"PASS: Component 1 — Font is 'Open Sans' ({', '.join(details)}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Expected 'Open Sans', found placeholder={ph_font_names}, bodyStyle={body_style.get('typeface')}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Font size is 20pt = 2000 hundredths of a point (0.35 points)
    try:
        # Check placeholder shape runs
        ph_sizes = [sz for tf, sz in ph_fonts if sz is not None]
        all_ph_20pt = len(ph_sizes) > 0 and all(
            str(sz) == '2000' for sz in ph_sizes
        )
        # Check bodyStyle lvl1pPr
        style_20pt = str(body_style.get('sz')) == '2000'

        if all_ph_20pt or style_20pt:
            details = []
            if all_ph_20pt:
                details.append(f"placeholder runs: {ph_sizes}")
            if style_20pt:
                details.append(f"bodyStyle: {body_style.get('sz')}")
            print(f"PASS: Component 2 — Font size is 20pt ({', '.join(details)}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Expected sz=2000 (20pt), found placeholder={ph_sizes}, bodyStyle={body_style.get('sz')}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Line spacing is 1.5 lines = 150000 spcPct (0.30 points)
    # Line spacing can be set in bodyStyle lvl1pPr OR in the placeholder shape paragraphs
    try:
        # Check bodyStyle
        style_lnSpc = body_style.get('lnSpc_pct')
        if style_lnSpc is not None and str(style_lnSpc) == '150000':
            print(f"PASS: Component 3 — Line spacing is 1.5 lines (bodyStyle spcPct={style_lnSpc}) (0.30 pts)")
            total_score += 0.30
        else:
            # Also check the placeholder shape paragraphs directly
            ph_lnSpc = get_placeholder_line_spacing(file_path)
            if ph_lnSpc and all(str(v) == '150000' for v in ph_lnSpc):
                print(f"PASS: Component 3 — Line spacing is 1.5 lines (placeholder pPr spcPct={ph_lnSpc}) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — Expected lnSpc spcPct=150000 (1.5 lines), found bodyStyle={style_lnSpc}, placeholder={ph_lnSpc}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


def get_placeholder_line_spacing(pptx_path):
    """
    Extract line spacing spcPct values from the body placeholder (idx=1)
    paragraph-level properties in slideMaster1.xml.
    """
    values = []
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            with zf.open('ppt/slideMasters/slideMaster1.xml') as f:
                root = ET.parse(f).getroot()
                for sp in root.findall('.//p:sp', NS):
                    ph = sp.find('.//p:nvSpPr/p:nvPr/p:ph', NS)
                    if ph is not None and ph.get('idx') == '1':
                        for p_el in sp.findall('.//a:p', NS):
                            pPr = p_el.find('a:pPr', NS)
                            if pPr is not None:
                                lnSpc = pPr.find('a:lnSpc', NS)
                                if lnSpc is not None:
                                    spcPct = lnSpc.find('a:spcPct', NS)
                                    if spcPct is not None:
                                        values.append(spcPct.get('val'))
                        break
    except Exception as e:
        print(f"ERROR: Could not parse placeholder line spacing: {e}")
    return values


# Entry point
persist_app_state('libreoffice_impress')

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
