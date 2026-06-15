"""
Reward Script: Insert decorative page border around all pages
Task ID: writer_rd_026
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.25): pgBorders element exists in section properties
  - Component 2 (0.25): All four sides have double-line border style
  - Component 3 (0.25): Border color is dark red (#8B0000) on all sides
  - Component 4 (0.25): Border size ~3pt and spacing ~1.0cm on all sides
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_026'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that the document has a 3pt double-line page border in dark red (#8B0000)
    with ~1.0 cm padding from page edges on all four sides.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    sides = ['top', 'left', 'bottom', 'right']

    # Get section properties
    try:
        sect_pr = doc.sections[0]._sectPr
        pg_borders_list = sect_pr.findall('.//w:pgBorders', ns)
    except Exception as e:
        print(f"ERROR: Cannot access section properties: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: pgBorders element exists with all four sides (0.25 points)
    try:
        if pg_borders_list:
            pg_borders = pg_borders_list[0]
            side_elements = {}
            all_sides_present = True
            for side in sides:
                el = pg_borders.find(f'w:{side}', ns)
                if el is not None:
                    side_elements[side] = el
                else:
                    all_sides_present = False

            if all_sides_present and len(side_elements) == 4:
                print(f"PASS: Component 1 -- pgBorders exists with all 4 sides (0.25 pts)")
                total_score += 0.25
            else:
                missing = [s for s in sides if s not in side_elements]
                print(f"FAIL: Component 1 -- pgBorders exists but missing sides: {missing}")
        else:
            print(f"FAIL: Component 1 -- No pgBorders element found in section properties")
            # No borders at all, nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All four sides have double-line border style (0.25 points)
    try:
        all_double = True
        for side in sides:
            el = side_elements.get(side)
            if el is not None:
                val = el.get(f'{{{ns["w"]}}}val')
                if val != 'double':
                    all_double = False
                    print(f"  INFO: {side} border style = '{val}', expected 'double'")

        if all_double:
            print(f"PASS: Component 2 -- All four sides have double-line border style (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- Not all sides have double-line border style")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Border color is dark red #8B0000 on all sides (0.25 points)
    try:
        all_correct_color = True
        for side in sides:
            el = side_elements.get(side)
            if el is not None:
                color = el.get(f'{{{ns["w"]}}}color')
                if color is None or color.upper() != '8B0000':
                    all_correct_color = False
                    print(f"  INFO: {side} border color = '{color}', expected '8B0000'")

        if all_correct_color:
            print(f"PASS: Component 3 -- All four sides have dark red #8B0000 color (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- Not all sides have correct dark red color")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Border size ~3pt (sz=24 in eighth-points) and spacing ~1.0cm (~28pt) (0.25 points)
    try:
        size_ok = True
        spacing_ok = True
        for side in sides:
            el = side_elements.get(side)
            if el is not None:
                sz = el.get(f'{{{ns["w"]}}}sz')
                space = el.get(f'{{{ns["w"]}}}space')

                # sz is in eighth-points: 3pt = 24
                if sz is not None:
                    sz_val = int(sz)
                    # Allow small tolerance: 18-30 (2.25pt to 3.75pt)
                    if sz_val < 18 or sz_val > 30:
                        size_ok = False
                        print(f"  INFO: {side} sz={sz_val} (expected ~24 for 3pt)")
                else:
                    size_ok = False

                # space is in points: 1.0cm ~ 28.35pt, allow 24-32
                if space is not None:
                    space_val = int(space)
                    if space_val < 20 or space_val > 36:
                        spacing_ok = False
                        print(f"  INFO: {side} space={space_val} (expected ~28 for 1.0cm)")
                else:
                    spacing_ok = False

        if size_ok and spacing_ok:
            print(f"PASS: Component 4 -- Border size ~3pt and spacing ~1.0cm on all sides (0.25 pts)")
            total_score += 0.25
        elif size_ok:
            print(f"PARTIAL: Component 4 -- Border size correct but spacing off (0.125 pts)")
            total_score += 0.125
        elif spacing_ok:
            print(f"PARTIAL: Component 4 -- Spacing correct but border size off (0.125 pts)")
            total_score += 0.125
        else:
            print(f"FAIL: Component 4 -- Both border size and spacing incorrect")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
