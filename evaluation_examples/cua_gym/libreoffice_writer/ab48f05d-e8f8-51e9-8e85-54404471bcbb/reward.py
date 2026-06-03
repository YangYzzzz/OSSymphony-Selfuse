"""
Reward Script: Accept tracked insertions, leave tracked deletions
Task ID: writer_rm_043
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): No tracked insertions remain (all 6 accepted)
  Component 2 (0.2): All insertions accepted AND exactly 4 deletions remain (compound)
  Component 3 (0.3): Accepted insertion texts are now normal text in document
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_043'

# Known deletion text snippets that should remain as tracked changes
EXPECTED_DELETION_SNIPPETS = [
    'Legacy compatibility mode has been deprecated',
    'The legacy migration tool should be executed',
    'The deprecated SHA-1 certificate validation has been removed',
    'The automatic failover mechanism may trigger false positives',
]

# Known insertion text snippets that should now be normal (accepted) text
EXPECTED_INSERTION_SNIPPETS = [
    'enhanced monitoring capabilities',
    'TLS 1.3 support is now mandatory',
    'Docker Engine 24.0 or later',
    'max_concurrent_sessions',
    'Memory consumption during batch operations',
    'Cache invalidation now uses a probabilistic algorithm',
]

WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WML_NS}


def persist_app_state(domain):
    """Attempt to save any unsaved document state via GUI."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for " + domain)
        except Exception as e:
            print("PERSIST_WARN: save hook failed: " + str(e))


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file " + file_path + ": " + str(e))
        print("REWARD: 0.0")
        return 0.0

    body = doc.element.body

    # Count tracked changes
    insertions = body.findall('.//w:ins', NS)
    num_insertions = len(insertions)

    deletions = body.findall('.//w:del', NS)
    num_deletions = len(deletions)

    # Component 1: No tracked insertions remain — all 6 should be accepted (0.5 points)
    # INITIAL: has 6 tracked insertions -> FAIL
    # GOLDEN: has 0 tracked insertions -> PASS
    try:
        if num_insertions == 0:
            print("PASS: Component 1 — No tracked insertions remain; all accepted (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 — Found " + str(num_insertions) + " tracked insertions still present, expected 0")
    except Exception as e:
        print("ERROR: Component 1 — " + str(e))

    # Component 2: All insertions accepted AND exactly 4 deletions remain with correct content (0.2 points)
    # This is a compound check anchored to the task change (no insertions).
    # INITIAL: fails because insertions still exist
    # GOLDEN: passes because insertions=0 and deletions=4 with correct content
    try:
        if num_insertions == 0 and num_deletions == 4:
            # Verify deletion content matches expected
            deletion_texts = []
            for dl in deletions:
                text_runs = dl.findall('.//w:r/w:delText', NS)
                text = ''.join(t.text or '' for t in text_runs)
                deletion_texts.append(text)

            matched_count = 0
            for snippet in EXPECTED_DELETION_SNIPPETS:
                if any(snippet in dt for dt in deletion_texts):
                    matched_count += 1

            if matched_count == 4:
                print("PASS: Component 2 — Insertions accepted + 4 correct deletions remain (0.2 pts)")
                total_score += 0.2
            else:
                print("FAIL: Component 2 — Deletions present but only " + str(matched_count) + "/4 match expected content")
        else:
            print("FAIL: Component 2 — insertions=" + str(num_insertions) + " (expect 0), deletions=" + str(num_deletions) + " (expect 4)")
    except Exception as e:
        print("ERROR: Component 2 — " + str(e))

    # Component 3: Accepted insertion texts are now normal paragraph text (0.3 points)
    # para.text does NOT include text inside <w:ins> tracked changes,
    # so this only passes when insertions have been accepted (became normal text).
    # INITIAL: insertion text is inside <w:ins> tags, para.text won't find it -> FAIL
    # GOLDEN: insertion text is normal text, para.text finds it -> PASS
    try:
        all_para_text = ' '.join(p.text for p in doc.paragraphs)

        found_count = 0
        for snippet in EXPECTED_INSERTION_SNIPPETS:
            if snippet in all_para_text:
                found_count += 1
                print("  Found accepted insertion text: " + snippet[:50])
            else:
                print("  Missing accepted insertion text: " + snippet[:50])

        if found_count == len(EXPECTED_INSERTION_SNIPPETS):
            print("PASS: Component 3 — All 6 insertion texts present as normal text (0.3 pts)")
            total_score += 0.3
        elif found_count >= 4:
            partial = round(0.3 * found_count / len(EXPECTED_INSERTION_SNIPPETS), 2)
            print("PARTIAL: Component 3 — " + str(found_count) + "/6 insertion texts found (" + str(partial) + " pts)")
            total_score += partial
        else:
            print("FAIL: Component 3 — Only " + str(found_count) + "/6 insertion texts found as normal text")
    except Exception as e:
        print("ERROR: Component 3 — " + str(e))

    final_score = min(round(total_score, 2), 1.0)
    print("")
    print("Score: " + str(total_score) + "/1.0")
    print("REWARD: " + str(final_score))
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = WORKDIR + '/' + TASK_ID + '.docx'
if not os.path.exists(file_path):
    print("File not found: " + file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
