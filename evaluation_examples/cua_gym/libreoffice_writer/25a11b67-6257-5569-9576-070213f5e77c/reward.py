"""
Reward Script: Promote third and fourth outline items from level 2 to level 1
Task ID: writer_lec_013
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): 'Budget Analysis' promoted to level 1 (ilvl=0)
  Component 2 (0.40): 'Risk Assessment' promoted to level 1 (ilvl=0)
  Component 3 (0.20): Both promotions done AND 'Team Roles' not over-promoted AND exactly 4 level-1 items
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_013'


def get_numbered_items(doc):
    """Extract all numbered list items with their ilvl from the document."""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    items = []
    for para in doc.paragraphs:
        pPr = para._element.find('{%s}pPr' % ns)
        if pPr is None:
            continue
        numPr = pPr.find('{%s}numPr' % ns)
        if numPr is None:
            continue
        ilvlE = numPr.find('{%s}ilvl' % ns)
        if ilvlE is None:
            continue
        ilvl = int(ilvlE.get('{%s}val' % ns))
        items.append({'text': para.text.strip(), 'ilvl': ilvl})
    return items


def persist_app_state(domain):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in ("libreoffice_calc", "libreoffice_writer", "libreoffice_impress"):
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print("PERSIST: ctrl+s sent for %s" % domain)
        except Exception as e:
            print("PERSIST_WARN: save hook failed: %s" % e)


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
        print("CRITICAL: Cannot load file %s: %s" % (file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Extract all numbered list items
    items = get_numbered_items(doc)
    print("Found %d numbered items:" % len(items))
    for item in items:
        print("  ilvl=%d  text='%s'" % (item['ilvl'], item['text']))

    if len(items) == 0:
        print("FAIL: No numbered list items found in document")
        print("REWARD: 0.0")
        return 0.0

    # Build lookup by text
    item_by_text = {}
    for item in items:
        item_by_text[item['text']] = item['ilvl']

    # Component 1: 'Budget Analysis' promoted to level 1 (ilvl=0) — 0.40 points
    try:
        if 'Budget Analysis' in item_by_text:
            ba_ilvl = item_by_text['Budget Analysis']
            if ba_ilvl == 0:
                print("PASS: Component 1 — 'Budget Analysis' is at level 1 (ilvl=0) (0.40 pts)")
                total_score += 0.40
            else:
                print("FAIL: Component 1 — 'Budget Analysis' ilvl=%d, expected 0" % ba_ilvl)
        else:
            print("FAIL: Component 1 — 'Budget Analysis' not found in numbered items")
    except Exception as e:
        print("ERROR: Component 1 — %s" % e)

    # Component 2: 'Risk Assessment' promoted to level 1 (ilvl=0) — 0.40 points
    try:
        if 'Risk Assessment' in item_by_text:
            ra_ilvl = item_by_text['Risk Assessment']
            if ra_ilvl == 0:
                print("PASS: Component 2 — 'Risk Assessment' is at level 1 (ilvl=0) (0.40 pts)")
                total_score += 0.40
            else:
                print("FAIL: Component 2 — 'Risk Assessment' ilvl=%d, expected 0" % ra_ilvl)
        else:
            print("FAIL: Component 2 — 'Risk Assessment' not found in numbered items")
    except Exception as e:
        print("ERROR: Component 2 — %s" % e)

    # Component 3: Outline structure integrity — 0.20 points
    # Compound check anchored to task changes: both promotions done AND Team Roles not
    # over-promoted AND exactly 4 level-1 items. This component only passes when the
    # task changes are in place, so it returns 0 on the initial env.
    try:
        ba_promoted = item_by_text.get('Budget Analysis') == 0
        ra_promoted = item_by_text.get('Risk Assessment') == 0
        tr_correct = item_by_text.get('Team Roles') == 1
        level1_items = [item for item in items if item['ilvl'] == 0]
        level1_count_ok = len(level1_items) == 4

        if ba_promoted and ra_promoted and tr_correct and level1_count_ok:
            level1_texts = [item['text'] for item in level1_items]
            print("PASS: Component 3 — Outline structure correct: 4 level-1 items %s, Team Roles at level 2 (0.20 pts)" % level1_texts)
            total_score += 0.20
        else:
            reasons = []
            if not ba_promoted:
                reasons.append("Budget Analysis not at level 1")
            if not ra_promoted:
                reasons.append("Risk Assessment not at level 1")
            if not tr_correct:
                reasons.append("Team Roles not at level 2 (ilvl=%s)" % item_by_text.get('Team Roles', 'missing'))
            if not level1_count_ok:
                reasons.append("level-1 count=%d (expected 4)" % len(level1_items))
            print("FAIL: Component 3 — %s" % '; '.join(reasons))
    except Exception as e:
        print("ERROR: Component 3 — %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.2f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = '%s/%s.docx' % (WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: %s" % file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
