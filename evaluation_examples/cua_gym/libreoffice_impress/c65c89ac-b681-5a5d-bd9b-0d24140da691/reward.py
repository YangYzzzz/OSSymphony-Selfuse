"""
Reward Script: Change master slide body text outline levels formatting
Task ID: impress_ma_035
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35): Level 1 body text = 24pt bold
  Component 2 (0.30): Level 2 body text = 20pt regular (not bold, not italic)
  Component 3 (0.35): Level 3 body text = 16pt italic
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_035'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def persist_app_state(domain):
    """Save any unsaved LibreOffice state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_body_level_props_from_txstyles(root):
    """
    Extract body text level properties from txStyles/bodyStyle (python-pptx generated format).
    Returns dict: {level_1based: {'sz': str, 'b': str, 'i': str}} or empty dict.
    """
    levels = {}
    txStyles = root.find('.//p:txStyles', NS)
    if txStyles is not None:
        bodyStyle = txStyles.find('p:bodyStyle', NS)
        if bodyStyle is not None:
            for lvl_num in range(1, 10):
                lvl_elem = bodyStyle.find(f'a:lvl{lvl_num}pPr', NS)
                if lvl_elem is not None:
                    defRPr = lvl_elem.find('a:defRPr', NS)
                    if defRPr is not None:
                        levels[lvl_num] = {
                            'sz': defRPr.get('sz'),
                            'b': defRPr.get('b'),
                            'i': defRPr.get('i'),
                        }
    return levels


def get_body_level_props_from_placeholder(root):
    """
    Extract body text level properties from the body placeholder shape's run properties.
    This is the format used when LibreOffice re-saves a pptx file (no txStyles).
    Also checks lstStyle within the body placeholder's txBody.
    Returns dict: {level_1based: {'sz': str, 'b': str, 'i': str}} or empty dict.
    """
    levels = {}
    for sp in root.findall('.//p:sp', NS):
        nvPr = sp.find('.//p:nvPr', NS)
        if nvPr is None:
            continue
        ph = nvPr.find('p:ph', NS)
        if ph is None:
            continue
        ph_type = ph.get('type', '')
        # Body placeholder can have idx="1" (python-pptx) or no idx (LibreOffice)
        if ph_type != 'body':
            continue

        txBody = sp.find('.//p:txBody', NS)
        if txBody is None:
            continue

        # Method A: Check lstStyle within txBody for defRPr per level
        lstStyle = txBody.find('a:lstStyle', NS)
        if lstStyle is not None:
            for lvl_num in range(1, 10):
                lvl_elem = lstStyle.find(f'a:lvl{lvl_num}pPr', NS)
                if lvl_elem is not None:
                    defRPr = lvl_elem.find('a:defRPr', NS)
                    if defRPr is not None:
                        levels[lvl_num] = {
                            'sz': defRPr.get('sz'),
                            'b': defRPr.get('b'),
                            'i': defRPr.get('i'),
                        }

        # Method B: Check run-level properties on paragraphs (LibreOffice format)
        for para in txBody.findall('a:p', NS):
            pPr = para.find('a:pPr', NS)
            lvl = int(pPr.get('lvl', '0')) if pPr is not None else 0
            lvl_num = lvl + 1  # convert 0-based to 1-based
            run = para.find('a:r', NS)
            if run is not None:
                rPr = run.find('a:rPr', NS)
                if rPr is not None:
                    rp = {
                        'sz': rPr.get('sz'),
                        'b': rPr.get('b'),
                        'i': rPr.get('i'),
                    }
                    # Run-level props override lstStyle if present
                    if lvl_num in levels:
                        for k in ('sz', 'b', 'i'):
                            if rp[k] is not None:
                                levels[lvl_num][k] = rp[k]
                    else:
                        levels[lvl_num] = rp

        # Only process first body placeholder found
        if levels:
            break

    return levels


def get_all_body_level_props(pptx_path):
    """
    Get body text level properties from either txStyles or placeholder shapes.
    Handles both python-pptx generated and LibreOffice re-saved formats.
    Checks all slideMaster XML files.
    """
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # Try each slideMaster
        for name in sorted(zf.namelist()):
            if not name.startswith('ppt/slideMasters/slideMaster') or not name.endswith('.xml'):
                continue

            with zf.open(name) as f:
                root = ET.parse(f).getroot()

            # Try txStyles first (python-pptx format)
            levels = get_body_level_props_from_txstyles(root)
            if levels:
                print(f"Found body levels via txStyles in {name}")
                # Also check placeholder for run-level overrides
                ph_levels = get_body_level_props_from_placeholder(root)
                if ph_levels:
                    print(f"Also found placeholder overrides for levels: {list(ph_levels.keys())}")
                    for lvl_num, props in ph_levels.items():
                        if lvl_num in levels:
                            for k in ('sz', 'b', 'i'):
                                if props[k] is not None:
                                    levels[lvl_num][k] = props[k]
                        else:
                            levels[lvl_num] = props
                return levels

            # Fallback: placeholder-based (LibreOffice re-saved format)
            levels = get_body_level_props_from_placeholder(root)
            if levels:
                print(f"Found body levels via placeholder shapes in {name}")
                return levels

    return {}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid pptx
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        levels = get_all_body_level_props(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not levels:
        print("CRITICAL: No body style levels found in any slideMaster")
        print("REWARD: 0.0")
        return 0.0

    print(f"Body levels found: {levels}")

    # Component 1: Level 1 body text = 24pt bold (0.35 points)
    # Task change: initial has 18pt not-bold; golden has 24pt bold
    try:
        props = levels.get(1, {})
        sz = props.get('sz')
        b = props.get('b')
        sz_val = int(sz) if sz is not None else None
        # b="1" or b="true" means bold; b="0", b="false", or None means not bold
        is_bold = (str(b) in ('1', 'true')) if b is not None else False

        size_ok = (sz_val == 2400)
        bold_ok = is_bold

        if size_ok and bold_ok:
            print(f"PASS: Component 1 — Level 1 is 24pt bold (sz={sz_val}, b={b}) (0.35 pts)")
            total_score += 0.35
        elif size_ok or bold_ok:
            partial = 0.15
            total_score += partial
            print(f"PARTIAL: Component 1 — Level 1: size_ok={size_ok}(sz={sz_val}), bold_ok={bold_ok}(b={b}) ({partial} pts)")
        else:
            print(f"FAIL: Component 1 — Level 1 expected 24pt bold, got sz={sz_val}, b={b}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Level 2 body text = 20pt regular (not bold, not italic) (0.30 points)
    # Task change: initial has 18pt; golden has 20pt (bold/italic remain off)
    try:
        props = levels.get(2, {})
        sz = props.get('sz')
        b = props.get('b')
        i = props.get('i')
        sz_val = int(sz) if sz is not None else None
        is_bold = (str(b) in ('1', 'true')) if b is not None else False
        is_italic = (str(i) in ('1', 'true')) if i is not None else False

        size_ok = (sz_val == 2000)
        not_bold_ok = not is_bold
        not_italic_ok = not is_italic

        if size_ok and not_bold_ok and not_italic_ok:
            print(f"PASS: Component 2 — Level 2 is 20pt regular (sz={sz_val}, b={b}, i={i}) (0.30 pts)")
            total_score += 0.30
        elif size_ok:
            partial = 0.15
            total_score += partial
            print(f"PARTIAL: Component 2 — Level 2: size correct but bold={is_bold}, italic={is_italic} ({partial} pts)")
        else:
            print(f"FAIL: Component 2 — Level 2 expected 20pt regular, got sz={sz_val}, b={b}, i={i}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Level 3 body text = 16pt italic (0.35 points)
    # Task change: initial has 18pt not-italic; golden has 16pt italic
    try:
        props = levels.get(3, {})
        sz = props.get('sz')
        b = props.get('b')
        i = props.get('i')
        sz_val = int(sz) if sz is not None else None
        is_italic = (str(i) in ('1', 'true')) if i is not None else False

        size_ok = (sz_val == 1600)
        italic_ok = is_italic

        if size_ok and italic_ok:
            print(f"PASS: Component 3 — Level 3 is 16pt italic (sz={sz_val}, i={i}) (0.35 pts)")
            total_score += 0.35
        elif size_ok or italic_ok:
            partial = 0.15
            total_score += partial
            print(f"PARTIAL: Component 3 — Level 3: size_ok={size_ok}(sz={sz_val}), italic_ok={italic_ok}(i={i}) ({partial} pts)")
        else:
            print(f"FAIL: Component 3 — Level 3 expected 16pt italic, got sz={sz_val}, i={i}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
