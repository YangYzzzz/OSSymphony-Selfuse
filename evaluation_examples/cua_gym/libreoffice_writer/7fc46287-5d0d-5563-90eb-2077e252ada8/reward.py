"""
Reward Script: Insert bookmarks at the beginning of each article in a legal agreement
Task ID: writer_legal_026
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): All 6 required bookmarks exist (0.1 each)
  Component 2 (0.4): Bookmarks are placed in the correct article heading paragraphs (0.067 each)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_026'

# Expected bookmarks and their associated article heading text fragments
EXPECTED_BOOKMARKS = {
    'Art_Definitions': 'Article 1',
    'Art_Scope': 'Article 2',
    'Art_Payment': 'Article 3',
    'Art_Termination': 'Article 4',
    'Art_Confidentiality': 'Article 5',
    'Art_Miscellaneous': 'Article 6',
}


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not installed")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    WNS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    body = doc.element.body

    # Extract all bookmarks from the document
    bookmark_starts = body.findall(f'.//{WNS}bookmarkStart')

    # Build a dict: bookmark_name -> parent paragraph text
    bookmark_map = {}
    for bm in bookmark_starts:
        name = bm.get(f'{WNS}name')
        if name and not name.startswith('_'):  # skip internal bookmarks like _GoBack
            parent = bm.getparent()
            # Get text content of the parent paragraph
            texts = parent.findall(f'.//{WNS}t')
            para_text = ''.join(t.text or '' for t in texts)
            bookmark_map[name] = para_text

    print(f"Found {len(bookmark_map)} user bookmarks: {list(bookmark_map.keys())}")

    # Component 1: All 6 required bookmark names exist (0.6 points, 0.1 each)
    comp1_score = 0.0
    for bm_name, article_fragment in EXPECTED_BOOKMARKS.items():
        try:
            if bm_name in bookmark_map:
                print(f"PASS: Bookmark '{bm_name}' exists (0.1 pts)")
                comp1_score += 0.1
            else:
                print(f"FAIL: Bookmark '{bm_name}' not found")
        except Exception as e:
            print(f"ERROR: Checking bookmark '{bm_name}': {e}")

    total_score += comp1_score
    print(f"Component 1 subtotal: {comp1_score:.2f}/0.60")

    # Component 2: Bookmarks placed in correct article heading paragraphs (0.4 points)
    # Only check bookmarks that exist (Component 1 already penalizes missing ones)
    comp2_score = 0.0
    points_per_bookmark = round(0.4 / 6, 4)  # ~0.0667 each

    for bm_name, article_fragment in EXPECTED_BOOKMARKS.items():
        try:
            if bm_name in bookmark_map:
                para_text = bookmark_map[bm_name]
                if article_fragment in para_text:
                    print(f"PASS: Bookmark '{bm_name}' correctly placed in '{para_text[:60]}' ({points_per_bookmark:.4f} pts)")
                    comp2_score += points_per_bookmark
                else:
                    print(f"FAIL: Bookmark '{bm_name}' in wrong paragraph: '{para_text[:60]}' (expected '{article_fragment}')")
            else:
                print(f"SKIP: Bookmark '{bm_name}' missing — cannot check placement")
        except Exception as e:
            print(f"ERROR: Checking placement of '{bm_name}': {e}")

    total_score += comp2_score
    print(f"Component 2 subtotal: {comp2_score:.4f}/0.40")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state('libreoffice_writer')

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
