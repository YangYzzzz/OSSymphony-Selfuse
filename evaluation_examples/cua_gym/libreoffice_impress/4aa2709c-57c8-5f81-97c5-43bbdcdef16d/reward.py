"""
Reward Script: Add Morph transition to slide 4 with 1.5s duration
Task ID: impress_sales_026
Domain: libreoffice_impress
Scoring:
  Component 1 — Slide 4 has a Morph transition type (0.60 pts)
  Component 2 — Slide 4 transition duration is 1500ms / 1.5 seconds (0.40 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_sales_026'

# Namespace map for OOXML PowerPoint
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_P14 = 'http://schemas.microsoft.com/office/powerpoint/2010/main'
# Morph transition lives in the 2018/8 namespace
NS_P188 = 'http://schemas.microsoft.com/office/powerpoint/2018/8/main'


def persist_app_state(domain: str):
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


def verify_task(file_path):
    """
    Verify that slide 4 has a Morph transition with 1.5s duration.
    Only scores task-introduced changes (Morph type and 1500ms duration).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid zip (pptx)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open pptx as zip: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse slide 4 XML
    slide_xml_name = 'ppt/slides/slide4.xml'
    try:
        with zf.open(slide_xml_name) as f:
            root = ET.parse(f).getroot()
    except KeyError:
        print(f"CRITICAL: {slide_xml_name} not found in archive")
        zf.close()
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse {slide_xml_name}: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Find transition element on slide 4 (precondition gate, not scored)
    transition_el = root.find(f'.//{{{NS_P}}}transition')
    if transition_el is None:
        print("FAIL: No transition element found on slide 4")
        zf.close()
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Transition element found on slide 4 (attribs: {transition_el.attrib})")

    # Component 1: Slide 4 has a Morph transition type (0.60 points)
    # This is the key task-introduced change: initial has no Morph child, golden does
    try:
        morph_el = transition_el.find(f'{{{NS_P188}}}morph')
        # Also check alternate morph namespaces
        if morph_el is None:
            for child in transition_el:
                if 'morph' in child.tag.lower():
                    morph_el = child
                    break

        if morph_el is not None:
            print(f"PASS: Component 1 — Morph transition type found (tag: {morph_el.tag}) (0.60 pts)")
            total_score += 0.60
        else:
            child_tags = [child.tag for child in transition_el]
            print(f"FAIL: Component 1 — No Morph child in transition. Found children: {child_tags}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Transition duration is exactly 1500ms (1.5 seconds) (0.40 points)
    # Initial has 2000ms (or different), golden has 1500ms
    try:
        # p14:dur is in milliseconds
        dur_str = transition_el.get(f'{{{NS_P14}}}dur')
        if dur_str is None:
            # Fall back to 'dur' without namespace
            dur_str = transition_el.get('dur')

        if dur_str is not None:
            try:
                dur_ms = int(dur_str)
                if dur_ms == 1500:
                    print(f"PASS: Component 2 — Duration is 1500ms (1.5s) (0.40 pts)")
                    total_score += 0.40
                else:
                    print(f"FAIL: Component 2 — Duration is {dur_ms}ms, expected 1500ms")
            except ValueError:
                print(f"FAIL: Component 2 — dur value '{dur_str}' is not a valid integer")
        else:
            spd_attr = transition_el.get('spd')
            print(f"FAIL: Component 2 — No duration attribute found (spd={spd_attr})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    zf.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    # Also check for Smooth_Pitch.pptx as mentioned in context
    alt_path = f'{WORKDIR}/Smooth_Pitch.pptx'
    if os.path.exists(alt_path):
        file_path = alt_path
    else:
        print(f"File not found: {file_path}")
        print("REWARD: 0.0")
        exit(0)

verify_task(file_path)
