"""
Reward Script: Verify continuous line numbering every 5 lines in left margin
Task ID: writer_legal_073
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): lnNumType element exists (line numbering enabled)
  Component 2 (0.3): countBy == 5 (interval of 5 lines)
  Component 3 (0.2): restart == continuous (continuous across pages)
  Component 4 (0.2): distance > 0 (numbers positioned in left margin)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_073'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract lnNumType attributes from all sections
    ns = {'w': W_NS}
    count_by_val = None
    restart_val = None
    distance_val = None
    ln_num_count = 0

    for i, section in enumerate(doc.sections):
        sect_pr = section._sectPr
        ln_elems = sect_pr.findall('.//w:lnNumType', ns)
        ln_num_count += len(ln_elems)

        if ln_elems:
            elem = ln_elems[0]
            attribs = elem.attrib
            count_by_val = attribs.get(f'{{{W_NS}}}countBy', None)
            restart_val = attribs.get(f'{{{W_NS}}}restart', None)
            distance_val = attribs.get(f'{{{W_NS}}}distance', None)
            print(f"Section {i}: lnNumType found — countBy={count_by_val}, restart={restart_val}, distance={distance_val}")

    # Component 1: lnNumType element exists (0.3 points)
    # Line numbering is enabled at all
    try:
        if ln_num_count > 0:
            print(f"PASS: Component 1 — lnNumType element exists (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No lnNumType element found in any section")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: countBy == 5 (0.3 points)
    # Numbers displayed every 5 lines
    try:
        if count_by_val == '5':
            print(f"PASS: Component 2 — countBy=5 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — countBy is '{count_by_val}', expected '5'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: restart == continuous (0.2 points)
    # Numbering is continuous across pages
    try:
        if restart_val == 'continuous':
            print(f"PASS: Component 3 — restart=continuous (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — restart is '{restart_val}', expected 'continuous'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: distance > 0 (0.2 points)
    # Numbers appear in the left margin (distance from text)
    try:
        if distance_val is not None and int(distance_val) > 0:
            print(f"PASS: Component 4 — distance={distance_val} > 0, numbers in left margin (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — distance is '{distance_val}', expected positive value")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
