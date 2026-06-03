"""
Reward Script: Add letterhead background to plain letter PDF using pdftk
Task ID: pdf_fm_073
Domain: pdf
Scoring:
  Component 1 (0.25): branded_letter.pdf exists
  Component 2 (0.25): branded_letter.pdf has exactly 3 pages
  Component 3 (0.25): Each page retains original letter text content
  Component 4 (0.25): Each page contains letterhead background text
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_073'

# Paths on the VM
BRANDED_PATH = os.path.join(WORKDIR, 'Documents', 'branded_letter.pdf')
PLAIN_PATH = os.path.join(WORKDIR, 'Documents', 'plain_letter.pdf')
LETTERHEAD_PATH = os.path.join(WORKDIR, 'Documents', 'templates', 'letterhead.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: branded_letter.pdf exists (0.25 points)
    # This is the primary output file — its existence is a task-introduced change
    # (it does NOT exist in initial_env)
    try:
        if os.path.exists(BRANDED_PATH):
            file_size = os.path.getsize(BRANDED_PATH)
            if file_size > 0:
                print(f"PASS: Component 1 — branded_letter.pdf exists ({file_size} bytes) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — branded_letter.pdf exists but is empty")
        else:
            print(f"FAIL: Component 1 — branded_letter.pdf not found at {BRANDED_PATH}")
            # If the file doesn't exist, no further checks are possible
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the branded PDF for remaining checks
    try:
        branded_doc = pymupdf.open(BRANDED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open branded_letter.pdf: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: branded_letter.pdf has exactly 3 pages (0.25 points)
    # The original plain_letter.pdf has 3 pages; the branded version should too
    try:
        page_count = branded_doc.page_count
        if page_count == 3:
            print(f"PASS: Component 2 — branded_letter.pdf has 3 pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected 3 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Load reference texts for comparison
    try:
        plain_doc = pymupdf.open(PLAIN_PATH)
        plain_texts = []
        for i in range(plain_doc.page_count):
            plain_texts.append(plain_doc[i].get_text())
        plain_doc.close()
    except Exception as e:
        print(f"ERROR: Cannot read plain_letter.pdf for reference: {e}")
        plain_texts = []

    try:
        lh_doc = pymupdf.open(LETTERHEAD_PATH)
        letterhead_text = lh_doc[0].get_text()
        lh_doc.close()
    except Exception as e:
        print(f"ERROR: Cannot read letterhead.pdf for reference: {e}")
        letterhead_text = ""

    # Component 3: Each page retains original letter text (0.25 points)
    # The branded PDF should contain the original letter content on each page
    # We check key phrases from each page of the original letter
    try:
        if plain_texts and branded_doc.page_count >= 3:
            pages_with_original = 0
            # Key phrases from each page of the original letter
            key_phrases = [
                ["Ms. Elena Rodriguez", "Digital Transformation"],  # Page 0
                ["Cloud-Native Application", "microservices"],       # Page 1
                ["Dr. James Whitfield", "engagement manager"],       # Page 2
            ]
            for i in range(3):
                branded_text = branded_doc[i].get_text()
                found_all = True
                for phrase in key_phrases[i]:
                    if phrase not in branded_text:
                        found_all = False
                        print(f"  DETAIL: Page {i} missing phrase: '{phrase}'")
                        break
                if found_all:
                    pages_with_original += 1

            if pages_with_original == 3:
                print(f"PASS: Component 3 — all 3 pages retain original letter text (0.25 pts)")
                total_score += 0.25
            elif pages_with_original > 0:
                partial = 0.25 * (pages_with_original / 3.0)
                print(f"PARTIAL: Component 3 — {pages_with_original}/3 pages retain original text ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — no pages retain original letter text")
        else:
            print(f"FAIL: Component 3 — cannot verify (missing reference or wrong page count)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Each page contains letterhead background text (0.25 points)
    # The letterhead contains "Meridian Global Solutions" and contact info
    # This text should appear on EVERY page of the branded PDF
    try:
        if letterhead_text and branded_doc.page_count >= 3:
            # Key phrases from the letterhead
            lh_phrases = [
                "Meridian Global Solutions",
                "1200 Commerce Blvd",
            ]
            pages_with_letterhead = 0
            for i in range(3):
                branded_text = branded_doc[i].get_text()
                found_lh = True
                for phrase in lh_phrases:
                    if phrase not in branded_text:
                        found_lh = False
                        print(f"  DETAIL: Page {i} missing letterhead phrase: '{phrase}'")
                        break
                if found_lh:
                    pages_with_letterhead += 1

            if pages_with_letterhead == 3:
                print(f"PASS: Component 4 — all 3 pages contain letterhead background (0.25 pts)")
                total_score += 0.25
            elif pages_with_letterhead > 0:
                partial = 0.25 * (pages_with_letterhead / 3.0)
                print(f"PARTIAL: Component 4 — {pages_with_letterhead}/3 pages have letterhead ({partial:.3f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — no pages contain letterhead text")
        else:
            print(f"FAIL: Component 4 — cannot verify (missing letterhead reference or wrong page count)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    branded_doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(BRANDED_PATH):
    print(f"File not found: {BRANDED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
