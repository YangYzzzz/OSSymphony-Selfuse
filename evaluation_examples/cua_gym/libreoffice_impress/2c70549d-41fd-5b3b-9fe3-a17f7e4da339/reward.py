"""
Reward Script: Apply Push Left transition to slide 2
Task ID: impress_tm_003
Domain: libreoffice_impress
Scoring:
  Component 1: Slide 2 has a transition element (0.3 pts)
  Component 2: Transition type is 'push' (0.3 pts)
  Component 3: Push direction is 'l' (from left) (0.4 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tm_003'

P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS = {'p': P_NS}


def verify_task(file_path):
    """
    Verify that slide 2 has a Push Left transition applied.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Parse slide 2 XML from the pptx zip
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zf.open('ppt/slides/slide2.xml') as f:
            root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide2.xml: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    zf.close()

    # Find transition element on slide 2
    transition_elem = root.find('.//p:transition', NS)

    # Component 1: Slide 2 has a transition element (0.3 points)
    try:
        if transition_elem is not None:
            print(f"PASS: Component 1 — Slide 2 has a transition element (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Slide 2 has no transition element")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Transition type is 'push' (0.3 points)
    try:
        if transition_elem is not None:
            push_elem = transition_elem.find(f'p:push', NS)
            if push_elem is not None:
                print(f"PASS: Component 2 — Transition type is 'push' (0.3 pts)")
                total_score += 0.3
            else:
                # List what child elements exist
                children = [c.tag.split('}')[-1] if '}' in c.tag else c.tag for c in transition_elem]
                print(f"FAIL: Component 2 — Expected 'push' transition, found children: {children}")
        else:
            print(f"FAIL: Component 2 — No transition element to check type")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Push direction is 'l' (from left) (0.4 points)
    try:
        if transition_elem is not None:
            push_elem = transition_elem.find(f'p:push', NS)
            if push_elem is not None:
                direction = push_elem.get('dir', '')
                if direction == 'l':
                    print(f"PASS: Component 3 — Push direction is 'l' (from left) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 3 — Expected dir='l', found dir='{direction}'")
            else:
                print(f"FAIL: Component 3 — No push element to check direction")
        else:
            print(f"FAIL: Component 3 — No transition element")
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
