"""
Reward Script: Insert a new section named 'Executive Summary' at the beginning of a report document.
Task ID: writer_fs_051
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): A section named 'Executive Summary' exists in the document
  Component 2 (0.3): The 'Executive Summary' section appears before the 'Introduction' heading
  Component 3 (0.3): The section contains text content (not empty)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_051'


def persist_app_state(domain):
    """Send Ctrl+S to save any unsaved changes in LibreOffice."""
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
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from odf.opendocument import load
        from odf.text import Section, H, P
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: A section named 'Executive Summary' exists (0.4 points)
    try:
        sections = doc.getElementsByType(Section)
        exec_summary_section = None
        for s in sections:
            section_name = s.attributes.get(
                ('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'name'), ''
            )
            if section_name and 'executive summary' in section_name.lower():
                exec_summary_section = s
                break

        if exec_summary_section is not None:
            print(f"PASS: Component 1 — Section named 'Executive Summary' found (0.4 pts)")
            total_score += 0.4
        else:
            section_names = []
            for s in sections:
                nm = s.attributes.get(
                    ('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'name'), '<unnamed>'
                )
                section_names.append(nm)
            print(f"FAIL: Component 1 — No section named 'Executive Summary' found. Sections: {section_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The section appears before the 'Introduction' heading (0.3 points)
    try:
        body = doc.body
        text_elem = body.childNodes[0]  # office:text

        section_pos = None
        intro_pos = None

        for i, child in enumerate(text_elem.childNodes):
            tag = child.qname if hasattr(child, 'qname') else None

            # Check if this is a section element
            if tag == ('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'section'):
                sec_name = child.attributes.get(
                    ('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'name'), ''
                )
                if sec_name and 'executive summary' in sec_name.lower():
                    if section_pos is None:
                        section_pos = i

            # Check if this is a heading with 'Introduction'
            if tag == ('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'h'):
                heading_text = _extract_text(child)
                if 'introduction' in heading_text.lower():
                    if intro_pos is None:
                        intro_pos = i

        if section_pos is not None and intro_pos is not None and section_pos < intro_pos:
            print(f"PASS: Component 2 — Section at position {section_pos}, Introduction at {intro_pos} (0.3 pts)")
            total_score += 0.3
        elif section_pos is None:
            print(f"FAIL: Component 2 — Executive Summary section not found in document body")
        elif intro_pos is None:
            print(f"FAIL: Component 2 — Introduction heading not found in document body")
        else:
            print(f"FAIL: Component 2 — Section at position {section_pos}, Introduction at {intro_pos} (section not before Introduction)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The section contains text content (0.3 points)
    try:
        if exec_summary_section is not None:
            section_text = _extract_text_recursive(exec_summary_section)
            # Strip the heading text "Executive Summary" itself to check for additional content
            # The section should have SOME content beyond just the heading name
            if len(section_text.strip()) > 0:
                print(f"PASS: Component 3 — Section contains text: '{section_text[:80]}...' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Section is empty (no text content)")
        else:
            print(f"FAIL: Component 3 — Cannot check content, section not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


def _extract_text(element):
    """Extract text from an ODF element (single level)."""
    text = ''
    if hasattr(element, 'childNodes'):
        for node in element.childNodes:
            if hasattr(node, 'data'):
                text += node.data
            elif hasattr(node, 'childNodes'):
                for child in node.childNodes:
                    if hasattr(child, 'data'):
                        text += child.data
    return text


def _extract_text_recursive(element):
    """Extract all text from an ODF element recursively."""
    text = ''
    if hasattr(element, 'data'):
        return element.data
    if hasattr(element, 'childNodes'):
        for child in element.childNodes:
            text += _extract_text_recursive(child)
    return text


# Entry point
persist_app_state('libreoffice_writer')

file_path = f'{WORKDIR}/{TASK_ID}.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
