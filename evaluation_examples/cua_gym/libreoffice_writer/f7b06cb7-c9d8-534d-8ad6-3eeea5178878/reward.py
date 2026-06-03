"""
Reward Script: Enable track changes recording in Writer document
Task ID: writer_rm_001
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.6): Track changes recording is enabled in document settings
  - Component 2 (0.4): Track changes enabled AND document content integrity preserved
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_001'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def check_track_changes_enabled(doc):
    """
    Check if track changes recording is enabled in the document settings.
    Returns True if enabled, False otherwise.
    """
    from lxml import etree
    settings_elem = doc.settings.element
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Check for <w:trackChanges/> or <w:trackRevisions/> in document settings
    track_changes = settings_elem.findall('.//w:trackChanges', ns)
    track_revisions = settings_elem.findall('.//w:trackRevisions', ns)

    # Also check via raw XML string in case of namespace variations
    settings_xml = etree.tostring(settings_elem).decode()
    has_track_in_xml = ('trackChanges' in settings_xml or 'trackRevisions' in settings_xml)

    if len(track_changes) > 0 or len(track_revisions) > 0 or has_track_in_xml:
        # Verify it's not explicitly set to false (w:val="false" or w:val="0")
        for elem in track_changes + track_revisions:
            val = elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
            if val is not None and val.lower() in ('false', '0', 'off'):
                return False
        return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
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

    # Component 1: Track changes recording is enabled (0.6 points)
    # The task requires enabling "Record Changes" (Edit > Track Changes > Record Changes).
    # In OOXML, this is represented by a <w:trackChanges/> element in the settings part.
    # LibreOffice may also use <w:trackRevisions/> depending on version.
    try:
        track_enabled = check_track_changes_enabled(doc)
        if track_enabled:
            print(f"PASS: Component 1 — Track changes recording is enabled (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — No trackChanges/trackRevisions element found or it is disabled")
    except Exception as e:
        track_enabled = False
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Track changes enabled AND document content integrity (0.4 points)
    # Compound check anchored to the task change: track changes must be enabled
    # AND the document content must be preserved (no accidental modifications).
    # This FAILS on initial_env because track changes is not enabled there.
    try:
        if not track_enabled:
            print(f"FAIL: Component 2 — Track changes not enabled (anchor condition failed)")
        else:
            # Verify content integrity as sub-condition
            paragraphs = doc.paragraphs
            para_count = len(paragraphs)

            if para_count != 68:
                print(f"FAIL: Component 2 — Expected 68 paragraphs, found {para_count}")
            else:
                expected_markers = [
                    (0, 'NON-DISCLOSURE AGREEMENT'),
                    (1, 'Confidential Business Agreement'),
                    (2, 'Effective Date: March 15, 2025'),
                    (4, '1. PARTIES'),
                ]
                mismatches = [
                    (idx, expected_text, paragraphs[idx].text.strip())
                    for idx, expected_text in expected_markers
                    if paragraphs[idx].text.strip() != expected_text
                ]
                if not mismatches:
                    print(f"PASS: Component 2 — Track changes enabled + content intact (0.4 pts)")
                    total_score += 0.4
                else:
                    idx, exp, act = mismatches[0]
                    print(f"FAIL: Component 2 — Para {idx}: expected '{exp}', found '{act}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification (LibreOffice Writer may have unsaved edits)
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
