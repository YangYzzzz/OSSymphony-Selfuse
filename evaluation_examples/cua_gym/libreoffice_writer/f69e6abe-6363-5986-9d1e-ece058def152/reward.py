"""
Reward Script: Open a saved version of a Writer document in a new read-only window
Task ID: writer_lec_092
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Two or more LibreOffice Writer windows exist
  Component 2 (0.3): One window has "(read-only)" in its title (version opened)
  Component 3 (0.3): Both windows coexist — editable original AND read-only version (side-by-side)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_092'


def persist_app_state(domain: str):
    """Best-effort save to flush any unsaved GUI state."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            import time
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def get_writer_windows():
    """
    Use wmctrl to list all open windows and return those matching LibreOffice Writer.
    Returns a list of window title strings.
    """
    os.environ["DISPLAY"] = ":0"
    try:
        output = os.popen("wmctrl -l").read().strip()
        lines = output.split('\n') if output else []
    except Exception as e:
        print(f"ERROR: wmctrl failed: {e}")
        return []

    writer_windows = []
    for line in lines:
        # wmctrl -l format: <hex_id> <desktop> <hostname> <title...>
        # Title is everything after the third whitespace-separated token
        parts = line.split(None, 3)
        if len(parts) >= 4:
            title = parts[3]
            if 'LibreOffice Writer' in title:
                writer_windows.append(title)
    return writer_windows


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    writer_windows = get_writer_windows()
    print(f"INFO: Found {len(writer_windows)} LibreOffice Writer window(s):")
    for w in writer_windows:
        print(f"  - {w}")

    # Component 1: Two or more Writer windows exist (0.4 points)
    # In initial state there is only 1 window; golden state has 2.
    try:
        if len(writer_windows) >= 2:
            print(f"PASS: Component 1 — {len(writer_windows)} Writer windows found (>= 2) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected >= 2 Writer windows, found {len(writer_windows)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: One window has "(read-only)" in its title (0.3 points)
    # This indicates that a version was opened in read-only mode.
    try:
        readonly_windows = [w for w in writer_windows if '(read-only)' in w.lower() or '(read only)' in w.lower()]
        if len(readonly_windows) >= 1:
            print(f"PASS: Component 2 — Found read-only window: '{readonly_windows[0]}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No window with '(read-only)' in title found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Both windows coexist — editable AND read-only (0.3 points)
    # The task requires side-by-side: the original stays open AND the version is opened.
    # This compound check only passes when BOTH exist, so it fails on initial_env
    # (which has only the editable window).
    try:
        editable_windows = [w for w in writer_windows
                            if TASK_ID in w
                            and '(read-only)' not in w.lower()
                            and '(read only)' not in w.lower()]
        readonly_windows = [w for w in writer_windows
                            if '(read-only)' in w.lower() or '(read only)' in w.lower()]
        if len(editable_windows) >= 1 and len(readonly_windows) >= 1:
            print(f"PASS: Component 3 — Both editable ('{editable_windows[0]}') and read-only ('{readonly_windows[0]}') windows coexist (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Need both editable and read-only windows; editable={len(editable_windows)}, readonly={len(readonly_windows)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")
verify_task()
