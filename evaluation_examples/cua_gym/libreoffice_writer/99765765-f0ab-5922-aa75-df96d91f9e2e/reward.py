"""
Reward Script: Set wrap spacing for text box on page 2
Task ID: writer_obj_044
Domain: libreoffice_writer
Scoring:
  - Component 1: Top wrap spacing == 0 EMU (0 cm)       — 0.3 pts
  - Component 2: Bottom wrap spacing == 0 EMU (0 cm)    — 0.3 pts
  - Component 3: Left wrap spacing == 180000 EMU (0.5cm) — 0.2 pts
  - Component 4: Right wrap spacing == 180000 EMU (0.5cm) — 0.2 pts
  Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_obj_044'

# Target spacing values in EMU (English Metric Units)
# 1 cm = 360000 EMU
# 0 cm = 0 EMU
# 0.5 cm = 180000 EMU
TARGET_TOP = 0         # 0 cm
TARGET_BOTTOM = 0      # 0 cm
TARGET_LEFT = 180000   # 0.5 cm
TARGET_RIGHT = 180000  # 0.5 cm

# Allow a small tolerance for floating-point/rounding differences (~0.01 cm = 3600 EMU)
TOLERANCE = 3600


def get_anchor_distances(file_path):
    """
    Extract the wrap spacing (distT, distB, distL, distR) from the first
    wp:anchor element in the document.
    Returns a dict with keys 'distT', 'distB', 'distL', 'distR' as integers,
    or raises an exception if no anchor is found.
    """
    doc = Document(file_path)
    body_xml = doc.element.body
    wp_ns = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
    anchors = body_xml.findall('.//{%s}anchor' % wp_ns)
    if not anchors:
        raise ValueError("No wp:anchor elements found in document")
    anchor = anchors[0]
    dist_t = int(anchor.get('distT', '0'))
    dist_b = int(anchor.get('distB', '0'))
    dist_l = int(anchor.get('distL', '0'))
    dist_r = int(anchor.get('distR', '0'))
    return {'distT': dist_t, 'distB': dist_b, 'distL': dist_l, 'distR': dist_r}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Set wrap spacing for text box on page 2:
      Top=0cm, Bottom=0cm, Left=0.5cm, Right=0.5cm
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document — precondition gate
    try:
        distances = get_anchor_distances(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load/parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    dist_t = distances['distT']
    dist_b = distances['distB']
    dist_l = distances['distL']
    dist_r = distances['distR']

    print(f"Found wrap spacing: distT={dist_t}, distB={dist_b}, distL={dist_l}, distR={dist_r}")
    print(f"Expected:           distT={TARGET_TOP}, distB={TARGET_BOTTOM}, distL={TARGET_LEFT}, distR={TARGET_RIGHT}")

    # Component 1: Top wrap spacing == 0 cm (0.3 points)
    # The task requires top spacing to change from 115200 EMU to 0 EMU
    try:
        if abs(dist_t - TARGET_TOP) <= TOLERANCE:
            print(f"PASS: Component 1 — Top spacing is 0 cm (distT={dist_t}) (0.3 pts)")
            total_score += 0.3
        else:
            top_cm = dist_t / 360000.0
            print(f"FAIL: Component 1 — Expected top spacing 0 cm, found {top_cm:.4f} cm (distT={dist_t})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bottom wrap spacing == 0 cm (0.3 points)
    # The task requires bottom spacing to change from 115200 EMU to 0 EMU
    try:
        if abs(dist_b - TARGET_BOTTOM) <= TOLERANCE:
            print(f"PASS: Component 2 — Bottom spacing is 0 cm (distB={dist_b}) (0.3 pts)")
            total_score += 0.3
        else:
            bottom_cm = dist_b / 360000.0
            print(f"FAIL: Component 2 — Expected bottom spacing 0 cm, found {bottom_cm:.4f} cm (distB={dist_b})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Left wrap spacing == 0.5 cm (0.2 points)
    # The task requires left spacing to change from 115200 EMU to 180000 EMU
    try:
        if abs(dist_l - TARGET_LEFT) <= TOLERANCE:
            left_cm = dist_l / 360000.0
            print(f"PASS: Component 3 — Left spacing is ~0.5 cm (distL={dist_l}, {left_cm:.4f} cm) (0.2 pts)")
            total_score += 0.2
        else:
            left_cm = dist_l / 360000.0
            print(f"FAIL: Component 3 — Expected left spacing 0.5 cm, found {left_cm:.4f} cm (distL={dist_l})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Right wrap spacing == 0.5 cm (0.2 points)
    # The task requires right spacing to change from 115200 EMU to 180000 EMU
    try:
        if abs(dist_r - TARGET_RIGHT) <= TOLERANCE:
            right_cm = dist_r / 360000.0
            print(f"PASS: Component 4 — Right spacing is ~0.5 cm (distR={dist_r}, {right_cm:.4f} cm) (0.2 pts)")
            total_score += 0.2
        else:
            right_cm = dist_r / 360000.0
            print(f"FAIL: Component 4 — Expected right spacing 0.5 cm, found {right_cm:.4f} cm (distR={dist_r})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/Desktop/tight_layout.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
