"""
Reward script for impress_stu_019:
Verify that all 10 slides in Anthropology_Talk.pptx have a Fade transition
with 1-second duration.

Scoring:
- Precondition: file exists, valid pptx, has 10 slides (0.0 if fails)
- Fade transition on each slide: 0.06 per slide (total 0.6)
- 1-second duration on each slide: 0.04 per slide (total 0.4)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

PPTX_PATH = "/home/user/Anthropology_Talk.pptx"
EXPECTED_SLIDES = 10

def check_transitions(pptx_path):
    """Check each slide for Fade transition and 1-second duration via XML."""
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
    }

    fade_results = []
    duration_results = []

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        for i in range(1, EXPECTED_SLIDES + 1):
            slide_xml = f'ppt/slides/slide{i}.xml'
            has_fade = False
            has_duration = False

            try:
                with zf.open(slide_xml) as f:
                    root = ET.parse(f).getroot()

                    # Find transition element - search with and without namespace
                    transitions = root.findall('.//p:transition', ns)

                    for tr in transitions:
                        # Check for fade child element
                        fade = tr.find('p:fade', ns)
                        if fade is not None:
                            has_fade = True

                        # Check duration via multiple methods:
                        # Method 1: spd attribute ('slow'=2s, 'med'=1s, 'fast'=0.5s)
                        spd = tr.get('spd')
                        if spd == 'med':
                            has_duration = True

                        # Method 2: p14:dur attribute in milliseconds
                        dur_val = tr.get('{http://schemas.microsoft.com/office/powerpoint/2010/main}dur')
                        if dur_val is not None:
                            try:
                                dur_ms = int(dur_val)
                                if dur_ms == 1000:
                                    has_duration = True
                            except ValueError:
                                pass

                        # Method 3: dur attribute directly (some implementations)
                        dur_direct = tr.get('dur')
                        if dur_direct is not None:
                            try:
                                dur_ms = int(dur_direct)
                                if dur_ms == 1000:
                                    has_duration = True
                            except ValueError:
                                pass

                        # Method 4: If spd is absent and no dur attribute,
                        # default speed in OOXML is 'fast' (0.5s), so not 1s.
                        # If spd is explicitly not set and no dur, it's not 1s.

            except KeyError:
                pass

            fade_results.append(has_fade)
            duration_results.append(has_duration)

    return fade_results, duration_results


def main():
    score = 0.0

    # Precondition: file exists
    if not os.path.exists(PPTX_PATH):
        print(f"ERROR: File not found: {PPTX_PATH}")
        print(f"REWARD: 0.0")
        return

    # Precondition: valid pptx (can open as zip)
    try:
        if not zipfile.is_zipfile(PPTX_PATH):
            print(f"ERROR: Not a valid PPTX file: {PPTX_PATH}")
            print(f"REWARD: 0.0")
            return
    except Exception as e:
        print(f"ERROR: Cannot read file: {e}")
        print(f"REWARD: 0.0")
        return

    # Precondition: has 10 slides
    try:
        from pptx import Presentation
        prs = Presentation(PPTX_PATH)
        num_slides = len(prs.slides)
        print(f"Number of slides: {num_slides}")
        if num_slides != EXPECTED_SLIDES:
            print(f"ERROR: Expected {EXPECTED_SLIDES} slides, found {num_slides}")
            print(f"REWARD: 0.0")
            return
    except Exception as e:
        print(f"ERROR: Cannot parse PPTX: {e}")
        print(f"REWARD: 0.0")
        return

    # Check transitions via XML
    try:
        fade_results, duration_results = check_transitions(PPTX_PATH)
    except Exception as e:
        print(f"ERROR: Failed to check transitions: {e}")
        print(f"REWARD: 0.0")
        return

    # Score: Fade transition (0.06 per slide, total 0.6)
    fade_count = sum(fade_results)
    fade_score = fade_count * 0.06
    print(f"Fade transitions: {fade_count}/{EXPECTED_SLIDES} slides")
    for i, has_fade in enumerate(fade_results):
        if not has_fade:
            print(f"  Slide {i+1}: NO Fade transition")

    # Score: Duration (0.04 per slide, total 0.4)
    duration_count = sum(duration_results)
    duration_score = duration_count * 0.04
    print(f"1-second duration: {duration_count}/{EXPECTED_SLIDES} slides")
    for i, has_dur in enumerate(duration_results):
        if not has_dur:
            print(f"  Slide {i+1}: Duration is NOT 1 second")

    score = round(fade_score + duration_score, 2)
    print(f"\nFade score: {fade_score:.2f} / 0.60")
    print(f"Duration score: {duration_score:.2f} / 0.40")
    print(f"REWARD: {score}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        print(f"REWARD: 0.0")
