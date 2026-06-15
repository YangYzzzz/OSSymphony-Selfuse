"""
Reward Script: Fix audio cross-slide playback in LibreOffice Impress
Task ID: impress_fix_029
Domain: libreoffice_impress
Scoring:
  Component 1 (0.4): numSld attribute > 1 (audio plays across multiple slides)
  Component 2 (0.3): numSld >= total slide count (audio covers all slides)
  Component 3 (0.3): repeatCount="indefinite" on audio cTn (audio loops)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_fix_029'

# Namespace map for OOXML
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def persist_app_state(domain):
    """Save any unsaved GUI state before verification."""
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


def get_total_slides(pptx_path):
    """Count total slides in the presentation."""
    count = 0
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        for name in zf.namelist():
            if name.startswith('ppt/slides/slide') and name.endswith('.xml'):
                count += 1
    return count


def get_audio_config(pptx_path):
    """
    Extract audio configuration from slide1.xml timing section.
    Returns dict with numSld (int or None) and repeatCount (str or None).
    """
    result = {'numSld': None, 'repeatCount': None, 'has_audio': False}

    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            # Check slide1.xml for audio timing
            try:
                with zf.open('ppt/slides/slide1.xml') as f:
                    root = ET.parse(f).getroot()
            except KeyError:
                print("WARN: ppt/slides/slide1.xml not found")
                return result

            # Find p:audio elements in timing
            p_ns = NS['p']
            for audio_elem in root.iter(f'{{{p_ns}}}audio'):
                result['has_audio'] = True
                # Find cMediaNode child
                for cmedia in audio_elem.iter(f'{{{p_ns}}}cMediaNode'):
                    num_sld_str = cmedia.get('numSld')
                    if num_sld_str is not None:
                        try:
                            result['numSld'] = int(num_sld_str)
                        except ValueError:
                            result['numSld'] = None

                    # Find the cTn child of cMediaNode for repeatCount
                    for ctn in cmedia.iter(f'{{{p_ns}}}cTn'):
                        repeat = ctn.get('repeatCount')
                        if repeat is not None:
                            result['repeatCount'] = repeat
                        break  # Only first cTn under cMediaNode

    except Exception as e:
        print(f"ERROR: Failed to parse pptx: {e}")

    return result


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
        total_slides = get_total_slides(file_path)
        print(f"INFO: Presentation has {total_slides} slides")
    except Exception as e:
        print(f"CRITICAL: Cannot read pptx as ZIP: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: audio must exist on slide 1
    audio_config = get_audio_config(file_path)
    if not audio_config['has_audio']:
        print("CRITICAL: No audio element found in slide 1 timing section")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Audio config — numSld={audio_config['numSld']}, repeatCount={audio_config['repeatCount']}")

    # Component 1: numSld > 1 — audio plays across multiple slides (0.4 points)
    # Initial env has numSld=1, golden should have numSld >> 1
    try:
        num_sld = audio_config['numSld']
        if num_sld is not None and num_sld > 1:
            print(f"PASS: Component 1 — numSld={num_sld} > 1, audio plays across multiple slides (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — numSld={num_sld}, audio only plays on 1 slide")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: numSld >= total slide count — audio covers ALL slides (0.3 points)
    # Task requires audio to play through all 15 slides
    try:
        num_sld = audio_config['numSld']
        if num_sld is not None and total_slides > 0 and num_sld >= total_slides:
            print(f"PASS: Component 2 — numSld={num_sld} >= {total_slides} total slides, audio covers entire presentation (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — numSld={num_sld} does not cover all {total_slides} slides")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: repeatCount="indefinite" — audio loops (0.3 points)
    # Task says "looping if the presentation duration exceeds the audio length"
    try:
        repeat = audio_config['repeatCount']
        if repeat is not None and repeat.lower() == 'indefinite':
            print(f"PASS: Component 3 — repeatCount='{repeat}', audio loops indefinitely (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — repeatCount='{repeat}', audio does not loop")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
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
