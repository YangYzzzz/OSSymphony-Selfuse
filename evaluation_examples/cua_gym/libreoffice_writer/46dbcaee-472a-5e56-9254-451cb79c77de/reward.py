"""
Reward Script: Turn off track changes recording in Q4_Proposal.docx
Task ID: writer_rm_002
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Track changes recording is disabled (no w:trackChanges in settings.xml)
  Component 2 (0.4): Recording is disabled AND all 5 existing tracked insertions are preserved
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_002'

# Persistence hook: save any unsaved LibreOffice state before verifying
# Enabled because the agent toggles a GUI setting (track changes recording)
# that only persists to disk on file save.
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(2.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def check_track_changes_recording(settings_root, ns):
    """Check if track changes recording is enabled.
    Returns True if recording is OFF (w:trackChanges element absent).
    """
    tc_elements = settings_root.findall('.//w:trackChanges', ns)
    return len(tc_elements) == 0


def count_tracked_insertions(doc_root, ns):
    """Count tracked insertion elements (w:ins) in document.xml."""
    ins_elements = doc_root.findall('.//w:ins', ns)
    return len(ins_elements)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # Precondition: file must exist and be a valid docx
    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse settings.xml and document.xml
    try:
        settings_xml = zf.read('word/settings.xml')
        settings_root = ET.fromstring(settings_xml)
        doc_xml = zf.read('word/document.xml')
        doc_root = ET.fromstring(doc_xml)
    except Exception as e:
        print(f"CRITICAL: Cannot parse docx internals: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    zf.close()

    # Component 1: Track changes recording is disabled (0.6 points)
    # The w:trackChanges element in settings.xml controls recording state.
    # Present = recording ON, Absent = recording OFF.
    # This FAILS on initial_env (element present) and PASSES on golden_env (element absent).
    try:
        recording_off = check_track_changes_recording(settings_root, ns)
        if recording_off:
            print(f"PASS: Component 1 -- Track changes recording is OFF (no w:trackChanges element) (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 -- Track changes recording is still ON (w:trackChanges element found)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Recording is OFF AND existing tracked insertions are preserved (0.4 points)
    # The task says: "The 5 existing tracked changes remain visible and unresolved."
    # We check that recording is off AND exactly 5 w:ins elements remain.
    # This FAILS on initial_env (recording is ON) and PASSES on golden_env.
    try:
        if recording_off:
            insertion_count = count_tracked_insertions(doc_root, ns)
            if insertion_count == 5:
                print(f"PASS: Component 2 -- Recording OFF and 5 tracked insertions preserved (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 -- Recording OFF but tracked insertions count is {insertion_count}, expected 5")
        else:
            print(f"FAIL: Component 2 -- Recording is still ON, cannot award preservation points")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
