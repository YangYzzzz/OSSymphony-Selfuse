"""
Reward Script: Verify AutoText entry for warning box template
Task ID: writer_tech_059
Domain: libreoffice_writer
Scoring:
  Component 1 (0.20) — A new .bau AutoText file exists (beyond default mytexts.bau)
  Component 2 (0.20) — BAU contains a block entry with warning-related name/title
  Component 3 (0.20) — AutoText content has yellow background formatting
  Component 4 (0.20) — AutoText content has red left border formatting
  Component 5 (0.20) — AutoText content has bold red "WARNING:" text
"""

import os
import glob
import zipfile
import re

AUTOTEXT_DIR = '/home/user/.config/libreoffice/4/user/autotext'
TASK_ID = 'writer_tech_059'


def find_new_bau_files():
    """Find .bau files in autotext dir that are not the default mytexts.bau."""
    if not os.path.isdir(AUTOTEXT_DIR):
        return []
    bau_files = glob.glob(os.path.join(AUTOTEXT_DIR, '*.bau'))
    # Filter out the default empty mytexts.bau
    new_baus = [f for f in bau_files if os.path.basename(f).lower() != 'mytexts.bau']
    return new_baus


def read_bau_xml(bau_path):
    """Read all XML content from a .bau (zip) file. Returns dict of filename -> content string."""
    result = {}
    try:
        with zipfile.ZipFile(bau_path, 'r') as z:
            for name in z.namelist():
                if name.endswith('.xml'):
                    result[name] = z.read(name).decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  WARN: Could not read BAU {bau_path}: {e}")
    return result


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: A new .bau AutoText file exists (0.20 points)
    try:
        new_baus = find_new_bau_files()
        if len(new_baus) > 0:
            print(f"PASS: Component 1 — Found {len(new_baus)} new BAU file(s): {[os.path.basename(f) for f in new_baus]} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — No new .bau files found beyond mytexts.bau in {AUTOTEXT_DIR}")
            # Also check if mytexts.bau itself now has entries
            mytexts_path = os.path.join(AUTOTEXT_DIR, 'mytexts.bau')
            if os.path.exists(mytexts_path):
                xmls = read_bau_xml(mytexts_path)
                block_xml = xmls.get('BlockList.xml', '')
                if 'abbreviated-name' in block_xml and 'block-list:name=' in block_xml:
                    # mytexts.bau has entries, treat it as the target
                    new_baus = [mytexts_path]
                    print(f"  INFO: mytexts.bau has block entries, using it as target")
                    total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if not new_baus and os.path.exists(os.path.join(AUTOTEXT_DIR, 'mytexts.bau')):
        # Last resort: check mytexts.bau
        new_baus = [os.path.join(AUTOTEXT_DIR, 'mytexts.bau')]

    # Collect all XML content from all candidate BAU files
    all_block_xmls = {}
    all_content_xmls = {}
    for bau_path in new_baus if new_baus else []:
        xmls = read_bau_xml(bau_path)
        bname = os.path.basename(bau_path)
        for fname, content in xmls.items():
            if fname == 'BlockList.xml':
                all_block_xmls[bname] = content
            elif 'content.xml' in fname:
                all_content_xmls[f"{bname}:{fname}"] = content

    # Component 2: BAU contains a block entry with warning-related name (0.20 points)
    try:
        found_warning_block = False
        for bname, block_xml in all_block_xmls.items():
            # Look for block entries; check if any name/abbreviated-name relates to "warn"
            # Pattern: block-list:abbreviated-name="X" block-list:name="Y"
            names = re.findall(r'block-list:(?:abbreviated-)?name="([^"]*)"', block_xml, re.IGNORECASE)
            block_text = block_xml.lower()
            if any('warn' in n.lower() for n in names) or 'warn' in block_text:
                found_warning_block = True
                print(f"PASS: Component 2 — Found warning-related block entry in {bname}: names={names} (0.20 pts)")
                break

        if not found_warning_block:
            # Broader check: any block entry at all (partial — the user might name it differently)
            has_any_entry = False
            for bname, block_xml in all_block_xmls.items():
                if 'abbreviated-name' in block_xml and 'block-list:name=' in block_xml:
                    has_any_entry = True
                    break
            if has_any_entry:
                # Check if the content.xml has warning-related content even if block name doesn't say "warn"
                for key, content_xml in all_content_xmls.items():
                    if 'WARNING' in content_xml or 'warning' in content_xml.lower():
                        found_warning_block = True
                        print(f"PASS: Component 2 — Block entry exists and content contains WARNING text (0.20 pts)")
                        break
            if not found_warning_block:
                print(f"FAIL: Component 2 — No warning-related block entry found in BAU files")
        if found_warning_block:
            total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: AutoText content has yellow background formatting (0.20 points)
    try:
        found_yellow_bg = False
        for key, content_xml in all_content_xmls.items():
            # Check for yellow/gold background color in various formats
            # ODF uses fo:background-color="#ffff00" or similar
            bg_colors = re.findall(r'(?:background-color|background)\s*[:=]\s*["\']?#?([0-9a-fA-F]{6})', content_xml)
            for color in bg_colors:
                r_val = int(color[0:2], 16)
                g_val = int(color[2:4], 16)
                b_val = int(color[4:6], 16)
                # Yellow range: high R, high G, low B
                if r_val >= 200 and g_val >= 200 and b_val <= 100:
                    found_yellow_bg = True
                    print(f"PASS: Component 3 — Yellow background found: #{color} in {key} (0.20 pts)")
                    break
            if found_yellow_bg:
                break
        if not found_yellow_bg:
            print(f"FAIL: Component 3 — No yellow background color found in AutoText content XML")
        else:
            total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: AutoText content has red left border (0.20 points)
    try:
        found_red_border = False
        for key, content_xml in all_content_xmls.items():
            # Check for border-left with red color
            # ODF format: fo:border-left="2.0pt solid #ff0000"
            border_matches = re.findall(r'border-left\s*[:=]\s*["\']?([^"\'>;]+)', content_xml)
            for border_val in border_matches:
                # Check if border specification contains a red-ish color
                color_in_border = re.findall(r'#([0-9a-fA-F]{6})', border_val)
                for color in color_in_border:
                    r_val = int(color[0:2], 16)
                    g_val = int(color[2:4], 16)
                    b_val = int(color[4:6], 16)
                    # Red: high R, low G, low B
                    if r_val >= 200 and g_val <= 80 and b_val <= 80:
                        found_red_border = True
                        print(f"PASS: Component 4 — Red left border found: {border_val.strip()} in {key} (0.20 pts)")
                        break
                if found_red_border:
                    break
            if found_red_border:
                break

        if not found_red_border:
            # Also check for generic border with red color (some implementations use fo:border instead of fo:border-left)
            for key, content_xml in all_content_xmls.items():
                border_matches = re.findall(r'(?:fo:border|border)\s*[:=]\s*["\']?([^"\'>;]+)', content_xml)
                for border_val in border_matches:
                    color_in_border = re.findall(r'#([0-9a-fA-F]{6})', border_val)
                    for color in color_in_border:
                        r_val = int(color[0:2], 16)
                        g_val = int(color[2:4], 16)
                        b_val = int(color[4:6], 16)
                        if r_val >= 200 and g_val <= 80 and b_val <= 80:
                            found_red_border = True
                            print(f"PASS: Component 4 — Red border found (may include left): {border_val.strip()} in {key} (0.20 pts)")
                            break
                    if found_red_border:
                        break
                if found_red_border:
                    break

        if not found_red_border:
            print(f"FAIL: Component 4 — No red left border found in AutoText content XML")
        else:
            total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: AutoText content has bold red "WARNING:" text (0.20 points)
    try:
        found_warning_text = False
        for key, content_xml in all_content_xmls.items():
            content_lower = content_xml.lower()
            # Check for "WARNING" or "WARNING:" text in the content
            has_warning_text = 'warning' in content_lower

            # Check for bold formatting (fo:font-weight="bold")
            has_bold = 'font-weight="bold"' in content_lower or 'font-weight:bold' in content_lower

            # Check for red text color (fo:color="#ff0000" or similar)
            has_red_text = False
            text_colors = re.findall(r'fo:color\s*=\s*"#([0-9a-fA-F]{6})"', content_xml, re.IGNORECASE)
            for color in text_colors:
                r_val = int(color[0:2], 16)
                g_val = int(color[2:4], 16)
                b_val = int(color[4:6], 16)
                if r_val >= 200 and g_val <= 80 and b_val <= 80:
                    has_red_text = True
                    break

            if has_warning_text and has_bold and has_red_text:
                found_warning_text = True
                print(f"PASS: Component 5 — Bold red 'WARNING:' text found in {key} (0.20 pts)")
                break
            elif has_warning_text and (has_bold or has_red_text):
                # Partial: has warning text + at least one formatting attribute
                found_warning_text = True
                missing = []
                if not has_bold:
                    missing.append('bold')
                if not has_red_text:
                    missing.append('red color')
                print(f"PASS: Component 5 — WARNING text found with partial formatting (missing: {missing}) in {key} (0.20 pts)")
                break

        if not found_warning_text:
            print(f"FAIL: Component 5 — No bold red 'WARNING:' text found in AutoText content")
        else:
            total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(AUTOTEXT_DIR):
    print(f"AutoText directory not found: {AUTOTEXT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()
