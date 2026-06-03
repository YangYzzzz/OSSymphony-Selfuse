"""
Reward Script: Set tab stops at 1cm and 10cm in Default Paragraph Style
Task ID: writer_tech_023
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Tab stop at ~1cm in Normal style
  Component 2 (0.4): Tab stop at ~10cm in Normal style
  Component 3 (0.2): Exactly 2 custom tab stops, both LEFT alignment
"""

import os
from docx import Document
from docx.oxml.ns import qn
from docx.enum.text import WD_TAB_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_023'

# 1 cm = 360000 EMU, 10 cm = 3600000 EMU
# Allow tolerance of ~0.5mm = 18000 EMU for rounding differences
TARGET_1CM_EMU = 360000
TARGET_10CM_EMU = 3600000
TOLERANCE_EMU = 18000


def persist_app_state(domain):
    """Save any unsaved LibreOffice state before verification."""
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


def get_normal_style_tab_stops(doc):
    """Extract tab stops from the Normal (Default Paragraph) style.

    Returns list of (position_emu, alignment) tuples, filtering out
    CLEAR stops and LEFT@0 defaults.
    """
    tab_stops = []
    for style in doc.styles:
        if style.name == 'Normal':
            # Use XML to get raw tab stop data for reliability
            elem = style.element
            pPr = elem.find(qn('w:pPr'))
            if pPr is not None:
                tabs_elem = pPr.find(qn('w:tabs'))
                if tabs_elem is not None:
                    for tab in tabs_elem.findall(qn('w:tab')):
                        val = tab.get(qn('w:val'))
                        pos_twips = int(tab.get(qn('w:pos'), '0'))
                        # Convert twips to EMU (1 twip = 635 EMU)
                        pos_emu = pos_twips * 635
                        # Filter out 'clear' type tabs and position=0 defaults
                        if val == 'clear':
                            continue
                        if pos_twips == 0:
                            continue
                        tab_stops.append((pos_emu, val))
            # Also try python-docx API as fallback
            if not tab_stops:
                try:
                    for ts in style.paragraph_format.tab_stops:
                        if ts.alignment == WD_TAB_ALIGNMENT.CLEAR:
                            continue
                        if ts.position == 0:
                            continue
                        alignment_str = str(ts.alignment).split('(')[0].strip().lower()
                        tab_stops.append((ts.position, alignment_str))
                except Exception:
                    pass
            break
    return tab_stops


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    tab_stops = get_normal_style_tab_stops(doc)
    print(f"INFO: Found {len(tab_stops)} custom tab stops in Normal style")
    for i, (pos, align) in enumerate(tab_stops):
        print(f"  Tab {i}: position={pos} EMU ({pos/360000:.3f} cm), alignment={align}")

    # Component 1: Tab stop at ~1cm in Normal style (0.4 points)
    try:
        matching_1cm = [pos for pos, align in tab_stops
                        if abs(pos - TARGET_1CM_EMU) <= TOLERANCE_EMU]
        if len(matching_1cm) > 0:
            print(f"PASS: Component 1 - Tab stop at ~1cm found (pos={matching_1cm[0]} EMU, "
                  f"target={TARGET_1CM_EMU}, diff={abs(matching_1cm[0] - TARGET_1CM_EMU)}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - No tab stop near 1cm ({TARGET_1CM_EMU} EMU +/- {TOLERANCE_EMU})")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Tab stop at ~10cm in Normal style (0.4 points)
    try:
        matching_10cm = [pos for pos, align in tab_stops
                         if abs(pos - TARGET_10CM_EMU) <= TOLERANCE_EMU]
        if len(matching_10cm) > 0:
            print(f"PASS: Component 2 - Tab stop at ~10cm found (pos={matching_10cm[0]} EMU, "
                  f"target={TARGET_10CM_EMU}, diff={abs(matching_10cm[0] - TARGET_10CM_EMU)}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 - No tab stop near 10cm ({TARGET_10CM_EMU} EMU +/- {TOLERANCE_EMU})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Exactly 2 custom tab stops, both LEFT alignment (0.2 points)
    try:
        if len(tab_stops) == 2:
            all_left = all(
                align in ('left', 'LEFT (0)')
                for _, align in tab_stops
            )
            if all_left:
                print(f"PASS: Component 3 - Exactly 2 tab stops, both LEFT alignment (0.2 pts)")
                total_score += 0.2
            else:
                alignments = [align for _, align in tab_stops]
                print(f"FAIL: Component 3 - Tab stops exist but not all LEFT: {alignments}")
        else:
            print(f"FAIL: Component 3 - Expected 2 tab stops, found {len(tab_stops)}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state before verification
persist_app_state("libreoffice_writer")

# Test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
