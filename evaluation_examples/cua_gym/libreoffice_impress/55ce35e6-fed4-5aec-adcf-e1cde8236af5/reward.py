"""
Reward Script: Configure master slide font scheme
Task ID: impress_gf2_043
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35): Title placeholder in slide master uses 'Georgia'
  Component 2 (0.35): Body/content placeholder in slide master uses 'Calibri'
  Component 3 (0.30): Footer/Date/SlideNumber placeholders use 'Courier New' at 10pt
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf2_043'

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}


def get_master_placeholder_fonts(pptx_path):
    """
    Parse slideMaster1.xml and extract font/size info for each placeholder type.
    Returns dict: {ph_type: {'fonts': set_of_fonts, 'defRPr_fonts': [(font, size)], 'rPr_fonts': [(font, size)]}}
    """
    result = {}
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open('ppt/slideMasters/slideMaster1.xml') as f:
            root = ET.parse(f).getroot()

        for sp in root.findall('.//p:cSld/p:spTree/p:sp', NS):
            nvSpPr = sp.find('.//p:nvSpPr', NS)
            ph = nvSpPr.find('.//p:ph', NS) if nvSpPr is not None else None
            if ph is None:
                continue
            ph_type = ph.get('type', 'body')

            rPr_fonts = []
            defRPr_fonts = []

            for rPr in sp.findall('.//a:rPr', NS):
                latin = rPr.find('a:latin', NS)
                font = latin.get('typeface') if latin is not None else None
                sz = rPr.get('sz')
                if font:
                    rPr_fonts.append((font, sz))

            for defRPr in sp.findall('.//a:defRPr', NS):
                latin = defRPr.find('a:latin', NS)
                font = latin.get('typeface') if latin is not None else None
                sz = defRPr.get('sz')
                if font:
                    defRPr_fonts.append((font, sz))

            result[ph_type] = {
                'rPr_fonts': rPr_fonts,
                'defRPr_fonts': defRPr_fonts,
            }

    return result


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        ph_data = get_master_placeholder_fonts(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide master XML from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Detected placeholder types in master: {list(ph_data.keys())}")

    # Component 1: Title placeholder uses Georgia (0.35 points)
    # In initial_env: Liberation Sans. In golden_env: Georgia.
    try:
        title_data = ph_data.get('title')
        if title_data is None:
            print("FAIL: Component 1 — No title placeholder found in slide master")
        else:
            # Collect all fonts set on the title placeholder (rPr and defRPr)
            all_fonts = [f for f, sz in title_data['rPr_fonts']] + [f for f, sz in title_data['defRPr_fonts']]
            print(f"  Title fonts found: {all_fonts}")
            # Check that at least one font entry is Georgia and none contradict
            georgia_found = any(f == 'Georgia' for f in all_fonts)
            non_georgia = [f for f in all_fonts if f != 'Georgia']
            if georgia_found and len(non_georgia) == 0:
                print(f"PASS: Component 1 — Title placeholder font is 'Georgia' (0.35 pts)")
                total_score += 0.35
            elif georgia_found:
                # Georgia present but mixed with others — partial
                print(f"PARTIAL: Component 1 — Georgia found but mixed with {non_georgia} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Expected 'Georgia' for title, found: {all_fonts}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Body/content placeholder uses Calibri (0.35 points)
    # In initial_env: Liberation Sans. In golden_env: Calibri.
    try:
        body_data = ph_data.get('body')
        if body_data is None:
            print("FAIL: Component 2 — No body placeholder found in slide master")
        else:
            all_fonts = [f for f, sz in body_data['rPr_fonts']] + [f for f, sz in body_data['defRPr_fonts']]
            print(f"  Body fonts found: {all_fonts}")
            calibri_found = any(f == 'Calibri' for f in all_fonts)
            non_calibri = [f for f in all_fonts if f != 'Calibri']
            if calibri_found and len(non_calibri) == 0:
                print(f"PASS: Component 2 — Body placeholder font is 'Calibri' (0.35 pts)")
                total_score += 0.35
            elif calibri_found:
                print(f"PARTIAL: Component 2 — Calibri found but mixed with {non_calibri} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Expected 'Calibri' for body, found: {all_fonts}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footer, Date, SlideNumber placeholders use Courier New at 10pt (0.30 points)
    # In initial_env: Liberation Sans with no 10pt. In golden_env: Courier New at sz=1000 (10pt).
    # 10pt in OOXML = 1000 hundredths of a point
    try:
        target_types = ['dt', 'ftr', 'sldNum']
        matching_count = 0
        total_checked = 0

        for ph_type in target_types:
            data = ph_data.get(ph_type)
            if data is None:
                print(f"  {ph_type}: not found in master")
                continue

            total_checked += 1
            # Check defRPr entries for Courier New at 10pt
            courier_at_10pt = any(
                f == 'Courier New' and sz == '1000'
                for f, sz in data['defRPr_fonts']
            )
            # Also check rPr entries
            courier_at_10pt_rPr = any(
                f == 'Courier New' and sz == '1000'
                for f, sz in data['rPr_fonts']
            )

            if courier_at_10pt or courier_at_10pt_rPr:
                print(f"  {ph_type}: Courier New at 10pt found")
                matching_count += 1
            else:
                all_entries = data['defRPr_fonts'] + data['rPr_fonts']
                print(f"  {ph_type}: Expected Courier New at 10pt, found: {all_entries}")

        if total_checked == 0:
            print("FAIL: Component 3 — No footer/date/sldNum placeholders found")
        elif matching_count == total_checked:
            print(f"PASS: Component 3 — All {matching_count}/{total_checked} footer placeholders use Courier New at 10pt (0.30 pts)")
            total_score += 0.30
        elif matching_count > 0:
            partial = round(0.30 * matching_count / total_checked, 2)
            print(f"PARTIAL: Component 3 — {matching_count}/{total_checked} placeholders correct ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — 0/{total_checked} footer placeholders use Courier New at 10pt")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
