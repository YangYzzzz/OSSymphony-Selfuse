"""
Reward Script: Add Fade transition to all slides with 1.5s duration
Task ID: impress_teach_017
Domain: libreoffice_impress
Scoring:
  Component 1 (0.5): All 10 slides have a 'fade' transition type
  Component 2 (0.5): All fade transitions have 1500ms duration
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_teach_017'

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}


def persist_app_state():
    """Save any unsaved LibreOffice Impress edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Parse all slide XMLs from the pptx ZIP
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            slide_files = sorted(
                [f for f in zf.namelist()
                 if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
            )
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(slide_files) == 0:
        print("CRITICAL: No slides found in presentation")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(slide_files)} slides")

    # Collect transition info for each slide
    # A slide has a "fade" transition if there is a <p:transition> with a <p:fade> child
    # Note: initial file may have <p:transition> without a type child (= no visual transition)
    # We also check inside mc:AlternateContent/mc:Choice and mc:Fallback blocks
    fade_slides = 0
    fade_with_correct_dur = 0

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            for sf in slide_files:
                with zf.open(sf) as f:
                    content = f.read().decode()
                    root = ET.fromstring(content)

                # Search all p:transition elements (including inside mc:AlternateContent)
                all_transitions = root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}transition')

                slide_fade_count = 0
                slide_fade_dur_count = 0

                for tr in all_transitions:
                    # Check if this transition has a fade child
                    fade_children = [
                        child for child in tr
                        if (child.tag.split('}')[-1] if '}' in child.tag else child.tag).lower() == 'fade'
                    ]

                    if len(fade_children) > 0:
                        slide_fade_count += 1
                        # Check duration: look for 'dur' attribute (standard) or p14:dur
                        dur_val = tr.attrib.get('dur', None)
                        # Also check for namespaced dur attributes
                        if dur_val is None:
                            for attr_key, attr_val in tr.attrib.items():
                                if 'dur' in attr_key:
                                    dur_val = attr_val
                                    break
                        if dur_val is not None and str(dur_val) == '1500':
                            slide_fade_dur_count += 1

                if slide_fade_count > 0:
                    fade_slides += 1
                if slide_fade_dur_count > 0:
                    fade_with_correct_dur += 1
    except Exception as e:
        print(f"CRITICAL: Error parsing slide XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    num_slides = len(slide_files)

    # Component 1: All slides have 'fade' transition (0.5 points)
    # This checks for the actual fade transition TYPE, not just a transition element
    try:
        if fade_slides == num_slides and num_slides > 0:
            print(f"PASS: Component 1 - All {num_slides} slides have 'fade' transition (0.5 pts)")
            total_score += 0.5
        elif fade_slides > 0:
            partial = 0.5 * (fade_slides / num_slides)
            print(f"PARTIAL: Component 1 - {fade_slides}/{num_slides} slides have 'fade' transition ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No slides have 'fade' transition (0/{num_slides})")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All fade transitions have 1500ms duration (0.5 points)
    # Only scored if at least some slides have fade transitions
    try:
        if fade_slides == 0:
            print("FAIL: Component 2 - No fade transitions to check duration")
        elif fade_with_correct_dur == num_slides:
            print(f"PASS: Component 2 - All {num_slides} slides have 1500ms fade duration (0.5 pts)")
            total_score += 0.5
        elif fade_with_correct_dur > 0:
            partial = 0.5 * (fade_with_correct_dur / num_slides)
            print(f"PARTIAL: Component 2 - {fade_with_correct_dur}/{num_slides} slides have 1500ms fade ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No slides have correct 1500ms fade duration")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
