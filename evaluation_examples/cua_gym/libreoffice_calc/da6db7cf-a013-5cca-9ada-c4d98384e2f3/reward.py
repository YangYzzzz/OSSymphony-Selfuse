"""
Reward Script: Create flask_install.odt with installation instructions as numbered list
Task ID: osworld_multi_apps_multi_simple_004
Domain: libreoffice_writer (ODT format)
Scoring:
  Component 1: /home/user/notes/flask_install.odt exists and is non-trivial (0.4 pts)
  Component 2: Document contains a numbered list with numeric format               (0.35 pts)
  Component 3: Numbered list contains Flask installation content                   (0.25 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_multi_simple_004'
FILE_PATH = '/home/user/notes/flask_install.odt'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File flask_install.odt exists at expected path with substantive content (0.4 points)
    # This distinguishes initial_env (file absent) from golden_env (file present).
    try:
        file_size = os.path.getsize(file_path)
        if file_size >= 100:
            print(f"PASS: Component 1 — file exists at {file_path} ({file_size} bytes) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — file is too small ({file_size} bytes), likely empty/corrupted")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the ODT document for further checks
    try:
        from odf.opendocument import load
        from odf.text import P, List, ListItem
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODT file {file_path}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Document contains a numbered list (0.35 points)
    # The task requires using Format > Bullets and Numbering with a numbered (not bulleted) list.
    # In ODF, a numbered list uses a list-style with num-format='1' (Arabic numerals).
    try:
        lists = doc.getElementsByType(List)

        # Collect numeric list style names from automatic styles
        numeric_style_names = set()
        for auto_style in doc.automaticstyles.childNodes:
            style_name = auto_style.getAttribute('name') if hasattr(auto_style, 'getAttribute') else None
            if style_name and hasattr(auto_style, 'childNodes'):
                for child in auto_style.childNodes:
                    if hasattr(child, 'attributes') and child.attributes:
                        attrs = {str(k): str(v) for k, v in child.attributes.items()}
                        # Look for numeric numbering format (Arabic numerals = '1')
                        num_format_key = "('urn:oasis:names:tc:opendocument:xmlns:style:1.0', 'num-format')"
                        if num_format_key in attrs and attrs[num_format_key] == '1':
                            numeric_style_names.add(style_name)

        # Find the first list that uses a numeric style
        matched_list = None
        num_list_items = 0
        for lst in lists:
            lst_style = lst.getAttribute('stylename')
            if lst_style in numeric_style_names:
                matched_list = lst
                num_list_items = len(lst.getElementsByType(ListItem))
                break

        if matched_list is not None and num_list_items >= 1:
            print(f"PASS: Component 2 — numbered list found with {num_list_items} item(s) (0.35 pts)")
            total_score += 0.35
        elif lists:
            print(f"FAIL: Component 2 — {len(lists)} list(s) found but none confirmed as numbered/numeric format")
        else:
            print(f"FAIL: Component 2 — no lists found in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Numbered list contains Flask installation content (0.25 points)
    # The task instructs copying Flask installation instructions — must mention
    # installation-related keywords (pip, venv, flask, install).
    try:
        flask_keywords = ['flask', 'pip', 'venv', 'install', 'virtual']

        def get_node_text(node):
            """Recursively extract text from an ODF node."""
            result = ''
            if node.nodeType == node.TEXT_NODE:
                result += node.data
            for child in node.childNodes:
                result += get_node_text(child)
            return result

        # Collect text from all list items across all lists
        all_text_parts = []
        for lst in doc.getElementsByType(List):
            for item in lst.getElementsByType(ListItem):
                for para in item.getElementsByType(P):
                    all_text_parts.append(get_node_text(para).lower())

        combined_text = ' '.join(all_text_parts)
        matched_keywords = [kw for kw in flask_keywords if kw in combined_text]

        if len(matched_keywords) >= 3:
            print(f"PASS: Component 3 — Flask installation content found: {matched_keywords} (0.25 pts)")
            total_score += 0.25
        elif len(matched_keywords) >= 1:
            print(f"FAIL: Component 3 — only {len(matched_keywords)} keyword(s) found ({matched_keywords}), need >= 3")
        else:
            print(f"FAIL: Component 3 — no Flask installation keywords found in list items")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
