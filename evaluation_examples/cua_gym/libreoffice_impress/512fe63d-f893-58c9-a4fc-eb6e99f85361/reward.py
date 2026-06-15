"""
Reward Script: Verify custom tab stops on slide 2 text box
Task ID: impress_gf1_042
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35): Tab stop at 5 cm left-aligned on all paragraphs
  Component 2 (0.35): Tab stop at 12 cm left-aligned on all paragraphs
  Component 3 (0.30): Tab stop at 22 cm right-aligned on all paragraphs
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_gf1_042'

# Expected tab stops: (position_emu, alignment)
# 1 cm = 360000 EMU
EXPECTED_TABS = [
    (1800000, 'l'),   # 5 cm, left-aligned
    (4320000, 'l'),   # 12 cm, left-aligned
    (7920000, 'r'),   # 22 cm, right-aligned
]

# Tolerance for position matching: 2% relative or 36000 EMU (0.1 cm) absolute
POS_TOLERANCE_EMU = 36000


def get_tab_stops_per_paragraph(pptx_path, slide_idx):
    """Extract tab stop lists from each paragraph in slide XML.
    Returns list of lists: each inner list contains (pos_emu, algn) tuples.
    Only considers paragraphs within the target text box (TextBox 3).
    """
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }

    results = []
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        with zf.open(f'ppt/slides/slide{slide_idx + 1}.xml') as f:
            root = ET.parse(f).getroot()

            # Find all shape trees (sp elements) on the slide
            # We need the text box with tab-separated content (TextBox 3)
            sp_elements = root.findall('.//p:cSld/p:spTree/p:sp', ns)

            for sp in sp_elements:
                # Check if this shape has text with tabs
                txBody = sp.find('.//p:txBody', ns)
                if txBody is None:
                    continue

                # Collect all paragraph texts to identify the right text box
                paragraphs = txBody.findall('a:p', ns)
                texts = []
                for para in paragraphs:
                    t_parts = para.findall('.//a:t', ns)
                    text = ''.join((t.text or '') for t in t_parts)
                    texts.append(text)

                # Identify the text box with tab-separated content
                tab_count = sum(1 for t in texts if '\t' in t)
                if tab_count < 5:
                    continue

                # This is our target text box - extract tab stops per paragraph
                for para in paragraphs:
                    tab_list = para.find('.//a:pPr/a:tabLst', ns)
                    if tab_list is None:
                        # Also check direct child
                        pPr = para.find('a:pPr', ns)
                        if pPr is not None:
                            tab_list = pPr.find('a:tabLst', ns)

                    para_tabs = []
                    if tab_list is not None:
                        for tab in tab_list.findall('a:tab', ns):
                            pos = tab.get('pos')
                            algn = tab.get('algn', 'l')
                            if pos is not None:
                                para_tabs.append((int(pos), algn))
                    results.append(para_tabs)

                break  # Found the target text box

    return results


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

    # Get tab stops from slide 2 (index 1)
    try:
        para_tabs = get_tab_stops_per_paragraph(file_path, slide_idx=1)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not para_tabs:
        print("FAIL: No text box with tab-separated content found on slide 2")
        print("REWARD: 0.0")
        return 0.0

    num_paras = len(para_tabs)
    print(f"INFO: Found {num_paras} paragraphs in the tab-separated text box")

    # Component 1: Tab stop at 5 cm (1800000 EMU), left-aligned (0.35 points)
    try:
        expected_pos, expected_algn = EXPECTED_TABS[0]
        paras_with_tab1 = 0
        for i, tabs in enumerate(para_tabs):
            found = False
            for pos, algn in tabs:
                if abs(pos - expected_pos) <= POS_TOLERANCE_EMU and algn == expected_algn:
                    found = True
                    break
            if found:
                paras_with_tab1 += 1

        if paras_with_tab1 == num_paras and num_paras > 0:
            print(f"PASS: Component 1 — Tab at 5cm left-aligned on all {num_paras} paragraphs (0.35 pts)")
            total_score += 0.35
        elif paras_with_tab1 > 0:
            partial = 0.35 * (paras_with_tab1 / num_paras)
            print(f"PARTIAL: Component 1 — Tab at 5cm left on {paras_with_tab1}/{num_paras} paragraphs ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No paragraphs have tab at 5cm left-aligned")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Tab stop at 12 cm (4320000 EMU), left-aligned (0.35 points)
    try:
        expected_pos, expected_algn = EXPECTED_TABS[1]
        paras_with_tab2 = 0
        for i, tabs in enumerate(para_tabs):
            found = False
            for pos, algn in tabs:
                if abs(pos - expected_pos) <= POS_TOLERANCE_EMU and algn == expected_algn:
                    found = True
                    break
            if found:
                paras_with_tab2 += 1

        if paras_with_tab2 == num_paras and num_paras > 0:
            print(f"PASS: Component 2 — Tab at 12cm left-aligned on all {num_paras} paragraphs (0.35 pts)")
            total_score += 0.35
        elif paras_with_tab2 > 0:
            partial = 0.35 * (paras_with_tab2 / num_paras)
            print(f"PARTIAL: Component 2 — Tab at 12cm left on {paras_with_tab2}/{num_paras} paragraphs ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No paragraphs have tab at 12cm left-aligned")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Tab stop at 22 cm (7920000 EMU), right-aligned (0.30 points)
    try:
        expected_pos, expected_algn = EXPECTED_TABS[2]
        paras_with_tab3 = 0
        for i, tabs in enumerate(para_tabs):
            found = False
            for pos, algn in tabs:
                if abs(pos - expected_pos) <= POS_TOLERANCE_EMU and algn == expected_algn:
                    found = True
                    break
            if found:
                paras_with_tab3 += 1

        if paras_with_tab3 == num_paras and num_paras > 0:
            print(f"PASS: Component 3 — Tab at 22cm right-aligned on all {num_paras} paragraphs (0.30 pts)")
            total_score += 0.30
        elif paras_with_tab3 > 0:
            partial = 0.30 * (paras_with_tab3 / num_paras)
            print(f"PARTIAL: Component 3 — Tab at 22cm right on {paras_with_tab3}/{num_paras} paragraphs ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No paragraphs have tab at 22cm right-aligned")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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
