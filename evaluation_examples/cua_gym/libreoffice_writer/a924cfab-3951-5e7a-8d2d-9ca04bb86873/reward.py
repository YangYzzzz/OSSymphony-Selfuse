"""
FINAL REWARD SCRIPT - SUCCESS
Task: Could you switch the default font family in Writer to Noto Serif?
Generated: 2025-10-14 12:21:06
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import zipfile
import traceback
from lxml import etree as ET


def verify_default_font_task(file_path: str, expected_font: str = 'Noto Serif') -> float:
    """Verify that the default Writer font (Normal style and/or docDefaults) is set to the
    expected font family. Returns a progressive score between 0.0 and 1.0.
    
    Scoring
    -------
    1.0 : Normal style font is set correctly (most common & authoritative place)
    0.8 : Normal NOT set, but docDefaults set correctly (still changes default)
    0.0 : Neither location set correctly
    """

    print(f"Starting verification for default font change in Writer → looking for '{expected_font}' …")

    # ---------- Basic validations (no points for these) ----------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0
    if not file_path.lower().endswith('.docx'):
        print("✗ Unsupported file format – expected a .docx produced by Writer")
        return 0.0

    # ---------- Helper definitions ----------
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    expected_lower = expected_font.lower()

    def is_font_correct(rfonts_elem):
        """Return True if any of the major font attributes equals expected_font."""
        if rfonts_elem is None:
            return False
        for att in ['ascii', 'hAnsi', 'cs', 'eastAsia']:
            val = rfonts_elem.get(f'{{{ns["w"]}}}{att}')
            if val and val.lower() == expected_lower:
                return True
        return False

    try:
        # ---------- Extract styles.xml from DOCX ----------
        with zipfile.ZipFile(file_path, 'r') as docx_zip:
            if 'word/styles.xml' not in docx_zip.namelist():
                print("✗ styles.xml missing – cannot verify styles")
                return 0.0
            styles_xml = docx_zip.read('word/styles.xml')
        root = ET.fromstring(styles_xml)

        # ---------- 1. Check Normal style ----------
        normal_font_correct = False
        normal_nodes = root.xpath('.//w:style[@w:styleId="Normal"]', namespaces=ns)
        if normal_nodes:
            rPr = normal_nodes[0].find('w:rPr', ns)
            if rPr is not None:
                rfonts = rPr.find('w:rFonts', ns)
                ascii_val = rfonts.get(f'{{{ns["w"]}}}ascii') if rfonts is not None else None
                print(f"Normal style font (ascii): {ascii_val}")
                normal_font_correct = is_font_correct(rfonts)
        else:
            print("✗ Normal style not found – unusual for Writer export")

        # ---------- 2. Check docDefaults ----------
        docdefaults_font_correct = False
        rprdef = root.find('.//w:docDefaults//w:rPrDefault//w:rPr', ns)
        if rprdef is not None:
            rfonts_def = rprdef.find('w:rFonts', ns)
            ascii_val = rfonts_def.get(f'{{{ns["w"]}}}ascii') if rfonts_def is not None else None
            print(f"docDefaults font (ascii): {ascii_val}")
            docdefaults_font_correct = is_font_correct(rfonts_def)

        # ---------- Scoring ----------
        if normal_font_correct:
            print("✓ Default font successfully set via Normal style (full score)")
            score = 1.0
        elif docdefaults_font_correct:
            print("✓ Default font set via docDefaults but Normal style unchanged (partial score)")
            score = 0.8
        else:
            print("✗ Expected font not found in Normal or docDefaults styles")
            score = 0.0

        # Ensure score within bounds
        score = max(0.0, min(score, 1.0))
        print(f"REWARD: {score}")
        return score

    except Exception as e:
        print("✗ Exception during verification:")
        traceback.print_exc()
        return 0.0


# ---------- MAIN EXECUTION (called when script is run) ----------
if __name__ == '__main__':
    # Path to the file produced by the agent/user
    USER_FILE_PATH = '/home/user/could_you_switch_the_default_font_family_in_writer_to_noto_serif.docx'

    reward_score = verify_default_font_task(USER_FILE_PATH)
    # Important: final print for automated graders
    print(f"REWARD: {reward_score}")

