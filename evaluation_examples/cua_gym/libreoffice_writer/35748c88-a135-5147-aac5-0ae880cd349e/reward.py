"""
Reward Script: Create a custom toolbar with business formatting shortcuts
Task ID: writer_biz_079
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25) - Custom toolbar XML file exists in swriter toolbar dir
  Component 2 (0.25) - Toolbar has a meaningful name (e.g. "Business Formatting")
  Component 3 (0.25) - Toolbar contains all 4 required command items
  Component 4 (0.25) - Each command maps to the correct UNO command
"""

import os
import glob

# LibreOffice custom toolbar config location
SWRITER_TOOLBAR_DIR = (
    "/home/user/.config/libreoffice/4/user/config/"
    "soffice.cfg/modules/swriter/toolbar"
)

TASK_ID = "writer_biz_079"

# Required UNO commands for the 4 toolbar buttons
REQUIRED_COMMANDS = {
    "heading_style": {
        "patterns": [".uno:StyleApply", "Heading"],
        "description": "Apply corporate heading style",
    },
    "insert_date": {
        "patterns": [".uno:InsertDateField", ".uno:InsertDate"],
        "description": "Insert date field",
    },
    "insert_table": {
        "patterns": [".uno:InsertTable"],
        "description": "Insert table",
    },
    "track_changes": {
        "patterns": [".uno:TrackChanges"],
        "description": "Toggle track changes",
    },
}


def find_custom_toolbar_files():
    """Find custom toolbar XML files in the swriter toolbar directory."""
    if not os.path.isdir(SWRITER_TOOLBAR_DIR):
        return []
    xml_files = glob.glob(os.path.join(SWRITER_TOOLBAR_DIR, "*.xml"))
    return xml_files


def parse_toolbar_xml(filepath):
    """Parse a toolbar XML file and extract toolbar name and command hrefs."""
    import xml.etree.ElementTree as ET

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except Exception as e:
        print(f"  ERROR parsing {filepath}: {e}")
        return None, []

    # Extract toolbar uiname
    # Namespace handling
    ns = {
        "toolbar": "http://openoffice.org/2001/toolbar",
        "xlink": "http://www.w3.org/1999/xlink",
    }

    toolbar_name = root.attrib.get(
        "{http://openoffice.org/2001/toolbar}uiname", ""
    )

    # Extract all toolbaritem hrefs
    items = []
    for item in root.findall(".//toolbar:toolbaritem", ns):
        href = item.attrib.get("{http://www.w3.org/1999/xlink}href", "")
        text = item.attrib.get(
            "{http://openoffice.org/2001/toolbar}text", ""
        )
        items.append({"href": href, "text": text})

    return toolbar_name, items


def verify_task():
    """
    Verify that a custom toolbar with business formatting shortcuts exists.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Custom toolbar XML file exists (0.25 points)
    try:
        toolbar_files = find_custom_toolbar_files()
        if len(toolbar_files) > 0:
            print(f"PASS: Component 1 - Found {len(toolbar_files)} custom toolbar file(s) in swriter toolbar dir (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - No custom toolbar XML files found in {SWRITER_TOOLBAR_DIR}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse all toolbar files to find the best matching one
    best_toolbar_name = ""
    best_items = []
    best_file = ""

    for tf in toolbar_files:
        name, items = parse_toolbar_xml(tf)
        if name is not None and len(items) > len(best_items):
            best_toolbar_name = name
            best_items = items
            best_file = tf

    if not best_items:
        # Try the first file even if parsing returned no items
        for tf in toolbar_files:
            name, items = parse_toolbar_xml(tf)
            if name is not None:
                best_toolbar_name = name
                best_items = items
                best_file = tf
                break

    print(f"  Analyzing toolbar: {best_file}")
    print(f"  Toolbar name: '{best_toolbar_name}'")
    print(f"  Items found: {len(best_items)}")
    for item in best_items:
        print(f"    href={item['href']}  text={item['text']}")

    # Component 2: Toolbar has a meaningful business-related name (0.25 points)
    try:
        name_lower = best_toolbar_name.lower()
        # Accept names containing business/formatting/custom keywords
        has_meaningful_name = (
            len(best_toolbar_name.strip()) > 0
            and any(
                kw in name_lower
                for kw in ["business", "format", "custom", "shortcut", "frequent", "biz"]
            )
        )
        if has_meaningful_name:
            print(f"PASS: Component 2 - Toolbar has meaningful name: '{best_toolbar_name}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - Toolbar name '{best_toolbar_name}' doesn't appear business/formatting related")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Toolbar contains at least 4 command items (0.25 points)
    try:
        if len(best_items) >= 4:
            print(f"PASS: Component 3 - Toolbar has {len(best_items)} items (>= 4 required) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Toolbar has only {len(best_items)} items, need at least 4")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: All 4 required UNO commands are present (0.25 points)
    try:
        all_hrefs = " ".join(item["href"] for item in best_items).lower()
        all_texts = " ".join(item["text"] for item in best_items).lower()
        combined = all_hrefs + " " + all_texts

        found_commands = 0
        total_commands = len(REQUIRED_COMMANDS)

        for cmd_key, cmd_info in REQUIRED_COMMANDS.items():
            # Check if any pattern matches in href or text
            if any(p.lower() in combined for p in cmd_info["patterns"]):
                found_commands += 1
                print(f"  FOUND: {cmd_info['description']}")
            else:
                print(f"  MISSING: {cmd_info['description']} (patterns: {cmd_info['patterns']})")

        if found_commands == total_commands:
            print(f"PASS: Component 4 - All {total_commands} required commands found (0.25 pts)")
            total_score += 0.25
        elif found_commands > 0:
            partial = 0.25 * (found_commands / total_commands)
            print(f"FAIL: Component 4 - Only {found_commands}/{total_commands} commands found (partial: {partial:.3f} pts)")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 4 - No required commands found (0/{total_commands})")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
