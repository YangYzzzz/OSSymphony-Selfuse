"""
Reward Script: Convert 3-digit hex color codes to 6-digit equivalents in styles.css
Task ID: vscode_gs_066
Domain: vscode
Scoring:
  - Component 1 (0.30): #fff -> #ffffff (background-color in body)
  - Component 2 (0.30): #fff -> #ffffff (color in header h1)
  - Component 3 (0.25): #000 -> #000000 (--text-dark custom property)
  - Component 4 (0.15): #f0f -> #ff00ff (--accent-magenta custom property)
  - Precondition gate: #336699 remains unchanged (no false conversion)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_066'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'webapp', 'styles.css')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: #336699 must remain unchanged (no false expansion)
    # This is true in both initial and golden, so it's a gate, not a scoring component
    try:
        gate_match = re.search(r'--primary-color:\s*#([0-9a-fA-F]+)\s*;', content)
        if gate_match:
            gate_val = gate_match.group(1).lower()
            if gate_val != '336699':
                print(f"GATE FAIL: --primary-color is #{gate_val}, expected #336699 (was corrupted)")
                print("REWARD: 0.0")
                return 0.0
            else:
                print(f"GATE PASS: --primary-color is still #336699 (not corrupted)")
        else:
            print("GATE WARN: --primary-color property not found, continuing")
    except Exception as e:
        print(f"GATE ERROR: {e}")

    # Component 1: body background-color changed from #fff to #ffffff (0.30 points)
    # In initial: "background-color: #fff;"
    # In golden:  "background-color: #ffffff;"
    try:
        match = re.search(r'background-color:\s*#([0-9a-fA-F]+)\s*;', content)
        if match:
            hex_val = match.group(1).lower()
            if hex_val == 'ffffff':
                print(f"PASS: Component 1 — body background-color is #ffffff (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 — body background-color is #{hex_val}, expected #ffffff")
        else:
            print("FAIL: Component 1 — background-color property not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: header h1 color changed from #fff to #ffffff (0.30 points)
    # The header h1 rule has "color: #fff;" -> "color: #ffffff;"
    # We need to locate the header h1 block specifically
    try:
        # Find the header h1 block and extract its color value
        # Look for "header h1" followed by color property
        h1_block = re.search(r'header\s+h1\s*\{([^}]+)\}', content, re.DOTALL)
        if h1_block:
            block_content = h1_block.group(1)
            color_match = re.search(r'color:\s*#([0-9a-fA-F]+)\s*;', block_content)
            if color_match:
                hex_val = color_match.group(1).lower()
                if hex_val == 'ffffff':
                    print(f"PASS: Component 2 — header h1 color is #ffffff (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 2 — header h1 color is #{hex_val}, expected #ffffff")
            else:
                print("FAIL: Component 2 — color property not found in header h1 block")
        else:
            print("FAIL: Component 2 — header h1 block not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: --text-dark changed from #000 to #000000 (0.25 points)
    try:
        match = re.search(r'--text-dark:\s*#([0-9a-fA-F]+)\s*;', content)
        if match:
            hex_val = match.group(1).lower()
            if hex_val == '000000':
                print(f"PASS: Component 3 — --text-dark is #000000 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — --text-dark is #{hex_val}, expected #000000")
        else:
            print("FAIL: Component 3 — --text-dark property not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: --accent-magenta changed from #f0f to #ff00ff (0.15 points)
    try:
        match = re.search(r'--accent-magenta:\s*#([0-9a-fA-F]+)\s*;', content)
        if match:
            hex_val = match.group(1).lower()
            if hex_val == 'ff00ff':
                print(f"PASS: Component 4 — --accent-magenta is #ff00ff (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — --accent-magenta is #{hex_val}, expected #ff00ff")
        else:
            print("FAIL: Component 4 — --accent-magenta property not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
