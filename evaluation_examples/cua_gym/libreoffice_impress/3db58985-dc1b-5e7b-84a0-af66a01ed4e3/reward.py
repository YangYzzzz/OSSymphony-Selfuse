"""
Reward Script: Verify professional transition scheme on 8-slide presentation
Task ID: impress_tm_042
Domain: libreoffice_impress
Scoring:
  - Slide 1: Fade transition at 0.8s (0.25 pts)
  - Slides 2-7: Wipe Right transition at 0.5s (0.55 pts)
  - Slide 8: Fade transition at 1.2s (0.20 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_042'

P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
P14_NS = 'http://schemas.microsoft.com/office/powerpoint/2010/main'


def get_transition_info(zf, slide_num):
    """
    Extract transition type, direction, and duration from a slide XML.
    Returns dict with keys: type (str|None), dir (str|None), dur_ms (int|None)
    """
    ns = {'p': P_NS}
    fname = f'ppt/slides/slide{slide_num}.xml'
    try:
        with zf.open(fname) as f:
            root = ET.parse(f).getroot()
    except KeyError:
        return {'type': None, 'dir': None, 'dur_ms': None}

    tr = root.find('.//p:transition', ns)
    if tr is None:
        return {'type': None, 'dir': None, 'dur_ms': None}

    # Extract duration from p14:dur attribute (milliseconds)
    dur_ms = None
    dur_val = tr.attrib.get(f'{{{P14_NS}}}dur')
    if dur_val is not None:
        try:
            dur_ms = int(dur_val)
        except ValueError:
            pass
    # Also check standard 'spd' attribute as fallback
    if dur_ms is None:
        spd = tr.attrib.get('spd')
        if spd is not None:
            # spd is 'slow'(1000), 'med'(500), 'fast'(250) or milliseconds
            spd_map = {'slow': 1000, 'med': 500, 'fast': 250}
            dur_ms = spd_map.get(spd)
            if dur_ms is None:
                try:
                    dur_ms = int(spd)
                except ValueError:
                    pass

    # Extract transition type from child element
    trans_type = None
    trans_dir = None
    for child in tr:
        tag = child.tag
        # Strip namespace to get local name
        if '}' in tag:
            local = tag.split('}')[1]
        else:
            local = tag
        trans_type = local
        trans_dir = child.attrib.get('dir')
        break  # Only first child is the transition type

    return {'type': trans_type, 'dir': trans_dir, 'dur_ms': dur_ms}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ----------------------------------------------------------------
    # Component 1: Slide 1 has Fade transition (0.15 pts)
    # ----------------------------------------------------------------
    try:
        info = get_transition_info(zf, 1)
        if info['type'] == 'fade':
            print(f"PASS: Component 1 — Slide 1 has Fade transition (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Slide 1 expected 'fade', found '{info['type']}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: Slide 1 has duration 800ms (0.8s) (0.10 pts)
    # ----------------------------------------------------------------
    try:
        info = get_transition_info(zf, 1)
        if info['dur_ms'] is not None and info['dur_ms'] == 800:
            print(f"PASS: Component 2 — Slide 1 duration is 800ms (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Slide 1 expected duration 800ms, found {info['dur_ms']}ms")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: Slides 2-7 all have Wipe transition (0.30 pts)
    # Each slide contributes 0.05 pts (6 slides)
    # ----------------------------------------------------------------
    try:
        wipe_count = 0
        for slide_num in range(2, 8):
            info = get_transition_info(zf, slide_num)
            if info['type'] == 'wipe':
                wipe_count += 1
            else:
                print(f"  DETAIL: Slide {slide_num} expected 'wipe', found '{info['type']}'")
        pts = round(0.05 * wipe_count, 2)
        if wipe_count == 6:
            print(f"PASS: Component 3 — All slides 2-7 have Wipe transition (0.30 pts)")
            total_score += pts
        elif wipe_count > 0:
            print(f"PARTIAL: Component 3 — {wipe_count}/6 slides have Wipe ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 3 — 0/6 slides have Wipe transition")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: Slides 2-7 Wipe direction is 'r' (right) (0.15 pts)
    # Each slide contributes 0.025 pts (6 slides)
    # ----------------------------------------------------------------
    try:
        dir_count = 0
        for slide_num in range(2, 8):
            info = get_transition_info(zf, slide_num)
            if info['dir'] == 'r':
                dir_count += 1
            else:
                print(f"  DETAIL: Slide {slide_num} wipe dir expected 'r', found '{info['dir']}'")
        pts = round(0.025 * dir_count, 3)
        if dir_count == 6:
            print(f"PASS: Component 4 — All slides 2-7 have Wipe direction 'r' (0.15 pts)")
            total_score += pts
        elif dir_count > 0:
            print(f"PARTIAL: Component 4 — {dir_count}/6 slides have dir='r' ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 4 — 0/6 slides have dir='r'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ----------------------------------------------------------------
    # Component 5: Slides 2-7 all have duration 500ms (0.5s) (0.10 pts)
    # Each slide contributes ~0.0167 pts
    # ----------------------------------------------------------------
    try:
        dur_count = 0
        for slide_num in range(2, 8):
            info = get_transition_info(zf, slide_num)
            if info['dur_ms'] is not None and info['dur_ms'] == 500:
                dur_count += 1
            else:
                print(f"  DETAIL: Slide {slide_num} expected 500ms, found {info['dur_ms']}ms")
        pts = round(0.10 * dur_count / 6.0, 4)
        if dur_count == 6:
            print(f"PASS: Component 5 — All slides 2-7 have 500ms duration (0.10 pts)")
            total_score += pts
        elif dur_count > 0:
            print(f"PARTIAL: Component 5 — {dur_count}/6 slides have 500ms ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 5 — 0/6 slides have 500ms duration")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ----------------------------------------------------------------
    # Component 6: Slide 8 has Fade transition (0.10 pts)
    # ----------------------------------------------------------------
    try:
        info = get_transition_info(zf, 8)
        if info['type'] == 'fade':
            print(f"PASS: Component 6 — Slide 8 has Fade transition (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — Slide 8 expected 'fade', found '{info['type']}'")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # ----------------------------------------------------------------
    # Component 7: Slide 8 has duration 1200ms (1.2s) (0.10 pts)
    # ----------------------------------------------------------------
    try:
        info = get_transition_info(zf, 8)
        if info['dur_ms'] is not None and info['dur_ms'] == 1200:
            print(f"PASS: Component 7 — Slide 8 duration is 1200ms (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — Slide 8 expected duration 1200ms, found {info['dur_ms']}ms")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    zf.close()

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
