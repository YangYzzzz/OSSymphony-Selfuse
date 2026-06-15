"""
Reward Script: Create a custom toolbar macro that inserts a formatted 'Note to Self' text box
Task ID: writer_acad_095
Domain: libreoffice_writer
Scoring:
  Component 1: Macro subroutine exists with appropriate name (0.25)
  Component 2: Macro creates a text frame (0.25)
  Component 3: Yellow background and red border configured (0.25)
  Component 4: Placeholder text 'NOTE:' present in macro (0.25)
"""

import os
import re
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_095'

# Path to LibreOffice Basic macro storage
MACRO_DIR = os.path.expanduser('~/.config/libreoffice/4/user/basic/Standard')
MODULE_FILE = os.path.join(MACRO_DIR, 'Module1.xba')


def extract_basic_code(xba_path):
    """Extract the Basic code from a .xba XML file."""
    try:
        tree = ET.parse(xba_path)
        root = tree.getroot()
        # The text content of the root element is the Basic code
        return root.text or ""
    except Exception as e:
        print(f"ERROR: Could not parse {xba_path}: {e}")
        # Fallback: read raw and extract between tags
        try:
            with open(xba_path, 'r') as f:
                content = f.read()
            # Extract text between the script:module tags
            match = re.search(r'<script:module[^>]*>(.*)</script:module>', content, re.DOTALL)
            if match:
                return match.group(1)
        except:
            pass
        return ""


def verify_task():
    """
    Verify that a LibreOffice Basic macro has been created that inserts a
    formatted 'Note to Self' text box with yellow background and red border.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Check if module file exists
    if not os.path.exists(MODULE_FILE):
        print(f"CRITICAL: Macro module file not found: {MODULE_FILE}")
        print("REWARD: 0.0")
        return 0.0

    basic_code = extract_basic_code(MODULE_FILE)
    if not basic_code.strip():
        print("CRITICAL: Module file is empty or could not be parsed")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Extracted Basic code length: {len(basic_code)} chars")

    # Normalize code for case-insensitive matching
    code_lower = basic_code.lower()

    # Component 1: A macro subroutine exists beyond the default empty Main (0.25 points)
    # The initial state has only "Sub Main / End Sub". The golden state should have
    # a new Sub that handles inserting a note/text box.
    try:
        # Find all Sub definitions
        sub_pattern = re.findall(r'sub\s+(\w+)', code_lower)
        # Filter out the default empty "main"
        custom_subs = [s for s in sub_pattern if s != 'main']

        if len(custom_subs) > 0:
            # Check that at least one sub name relates to "note" or "insert"
            has_relevant_name = any(
                ('note' in s or 'insert' in s or 'revision' in s or 'mark' in s)
                for s in custom_subs
            )
            if has_relevant_name:
                print(f"PASS: Component 1 — Found relevant macro sub(s): {custom_subs} (0.25 pts)")
                total_score += 0.25
            else:
                # Still give credit if there's a custom sub (may have different naming)
                # but only partial
                print(f"PARTIAL: Component 1 — Found custom sub(s) {custom_subs} but name doesn't indicate note/insert (0.15 pts)")
                total_score += 0.15
        else:
            print("FAIL: Component 1 — No custom subroutine found beyond default Main")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Macro creates a text frame (0.25 points)
    # Check for TextFrame creation pattern in the code
    try:
        has_textframe = 'textframe' in code_lower or 'text.textframe' in code_lower
        has_createinstance = 'createinstance' in code_lower

        if has_textframe and has_createinstance:
            print(f"PASS: Component 2 — Macro creates a TextFrame via createInstance (0.25 pts)")
            total_score += 0.25
        elif has_textframe:
            print(f"PARTIAL: Component 2 — TextFrame referenced but createInstance not found (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 2 — No TextFrame creation found in macro code")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Yellow background and red border (0.25 points)
    # Yellow background: RGB(255, 255, 0) or hex equivalent
    # Red border: RGB(255, 0, 0) or hex equivalent
    try:
        # Check for yellow background color setting
        has_yellow_bg = False
        # Common patterns: BackColor = RGB(255, 255, 0), BackColor = 16776960, BackColor = &HFFFF00
        if re.search(r'backcolor\s*=\s*rgb\s*\(\s*255\s*,\s*255\s*,\s*0\s*\)', code_lower):
            has_yellow_bg = True
        elif re.search(r'backcolor\s*=\s*16776960', code_lower):
            has_yellow_bg = True
        elif re.search(r'backcolor.*ffff00', code_lower):
            has_yellow_bg = True
        elif 'backcolor' in code_lower and ('yellow' in code_lower or '255, 255, 0' in code_lower.replace(' ', '')):
            has_yellow_bg = True

        # Check for red border color
        has_red_border = False
        # Look for border-related properties with red color
        if re.search(r'border', code_lower) and re.search(r'rgb\s*\(\s*255\s*,\s*0\s*,\s*0\s*\)', code_lower):
            has_red_border = True
        elif re.search(r'border', code_lower) and re.search(r'color\s*=\s*16711680', code_lower):
            has_red_border = True
        elif re.search(r'border', code_lower) and 'ff0000' in code_lower:
            has_red_border = True

        if has_yellow_bg and has_red_border:
            print(f"PASS: Component 3 — Yellow background and red border configured (0.25 pts)")
            total_score += 0.25
        elif has_yellow_bg:
            print(f"PARTIAL: Component 3 — Yellow background found but red border not detected (0.15 pts)")
            total_score += 0.15
        elif has_red_border:
            print(f"PARTIAL: Component 3 — Red border found but yellow background not detected (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 3 — Neither yellow background nor red border found in macro")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Placeholder text containing 'NOTE:' (0.25 points)
    # The macro should insert text like "NOTE: [Add revision note here]"
    try:
        has_note_text = 'note:' in code_lower or 'note to self' in code_lower
        has_placeholder = (
            'revision' in code_lower or
            'add' in code_lower or
            'placeholder' in code_lower or
            '[' in basic_code  # bracket indicates placeholder pattern
        )

        if has_note_text and has_placeholder:
            print(f"PASS: Component 4 — Placeholder text with 'NOTE:' found (0.25 pts)")
            total_score += 0.25
        elif has_note_text:
            print(f"PARTIAL: Component 4 — 'NOTE:' text found but no placeholder pattern (0.20 pts)")
            total_score += 0.20
        elif has_placeholder:
            print(f"PARTIAL: Component 4 — Placeholder pattern found but no 'NOTE:' (0.10 pts)")
            total_score += 0.10
        else:
            print("FAIL: Component 4 — No 'NOTE:' placeholder text found in macro")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
