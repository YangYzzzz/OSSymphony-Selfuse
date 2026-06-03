"""
Reward Script: Convert multi-level numbered list from '1/a/i' to 'Article/Section/Clause' format
Task ID: wrpara_049
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Level 1 items use 'Article N.' format
  Component 2 (0.35): Level 2 items use 'Section N.M.' format
  Component 3 (0.30): Level 3 items use 'Clause N.M.K.' format
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'wrpara_049'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
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


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task converts a multi-level numbered list:
      Initial:  1. / a. / i.  (numeric / alpha / roman)
      Golden:   Article N. / Section N.M. / Clause N.M.K.

    We identify paragraphs by their hierarchy level from the initial doc
    (the hierarchy is known from the task context) and verify the golden
    prefix format. Content after the prefix must remain intact.

    Expected structure (from task context):
      5 Level-1 items  (Article 1 .. Article 5)
      Variable Level-2 items (Section X.Y)
      Variable Level-3 items (Clause X.Y.Z)
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all non-empty paragraphs after the title/date/blank preamble
    # Preamble: P0=Title, P1=date, P2=blank  => content starts at P3
    content_paras = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            content_paras.append(text)

    # Skip title and date line
    # Title: "Bylaws of the Greenfield Community Association"
    # Date: "Adopted March 15, 2025"
    body_paras = []
    for t in content_paras:
        if t.startswith("Bylaws of") or t.startswith("Adopted "):
            continue
        body_paras.append(t)

    if not body_paras:
        print("FAIL: No body paragraphs found in the document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(body_paras)} body paragraphs")

    # Regex patterns for the golden format
    article_re = re.compile(r'^Article\s+(\d+)\.\s+')
    section_re = re.compile(r'^Section\s+(\d+)\.(\d+)\.\s+')
    clause_re = re.compile(r'^Clause\s+(\d+)\.(\d+)\.(\d+)\.\s+')

    # Regex patterns for the initial (old) format
    old_level1_re = re.compile(r'^(\d+)\.\s+')  # "1. Name and Purpose"
    old_level2_re = re.compile(r'^([a-z])\.\s+')  # "a. The name of ..."
    old_level3_re = re.compile(r'^(i{1,3}|iv|v|vi{0,3})\.\s+')  # "i. The Association ..."

    # Classify each paragraph by what format it currently has
    articles_found = []
    sections_found = []
    clauses_found = []
    old_format_found = False

    for text in body_paras:
        if article_re.match(text):
            m = article_re.match(text)
            articles_found.append(int(m.group(1)))
        elif section_re.match(text):
            m = section_re.match(text)
            sections_found.append((int(m.group(1)), int(m.group(2))))
        elif clause_re.match(text):
            m = clause_re.match(text)
            clauses_found.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
        else:
            # Check if it still uses old format
            if old_level1_re.match(text) or old_level2_re.match(text) or old_level3_re.match(text):
                old_format_found = len(body_paras) > 0  # derive from actual state

    print(f"INFO: Articles found: {len(articles_found)}, Sections found: {len(sections_found)}, Clauses found: {len(clauses_found)}")
    if old_format_found:
        print(f"INFO: Some paragraphs still use old numbering format")

    # ========================================================
    # Component 1: Level 1 items use "Article N." format (0.35 points)
    # Expected: Article 1 through Article 5 (5 items)
    # ========================================================
    try:
        expected_articles = {1, 2, 3, 4, 5}
        found_articles = set(articles_found)
        matched_count = len(found_articles & expected_articles)
        if matched_count == 5:
            print(f"PASS: Component 1 — All 5 Article-level items found with correct format (0.35 pts)")
            total_score += 0.35
        elif matched_count > 0:
            if matched_count > 0:
                partial = round(0.35 * matched_count / 5, 2)
                print(f"PARTIAL: Component 1 — {matched_count}/5 Article items found ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 1 — No 'Article N.' formatted paragraphs found (expected 5)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ========================================================
    # Component 2: Level 2 items use "Section N.M." format (0.35 points)
    # Expected: Multiple Section items with proper parent numbering
    # ========================================================
    try:
        from collections import defaultdict
        num_sections = len(sections_found)
        if num_sections >= 10:
            valid_parents = all(1 <= s[0] <= 5 for s in sections_found)
            by_article = defaultdict(list)
            for art, sec in sections_found:
                by_article[art].append(sec)
            sequential = valid_parents and all(
                sorted(secs) == list(range(1, len(secs) + 1))
                for secs in by_article.values()
            )
            if valid_parents and sequential:
                print(f"PASS: Component 2 — {num_sections} Section items with correct N.M format (0.35 pts)")
                total_score += 0.35
            elif valid_parents:
                print(f"PARTIAL: Component 2 — Sections found but numbering not sequential (0.25 pts)")
                total_score += 0.25
            elif not valid_parents:
                print(f"PARTIAL: Component 2 — Sections found but parent numbers invalid (0.2 pts)")
                total_score += 0.2
        elif num_sections > 0:
            if num_sections > 0:
                partial = round(0.35 * min(num_sections / 10.0, 1.0), 2)
                print(f"PARTIAL: Component 2 — Only {num_sections} Section items found ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 2 — No 'Section N.M.' formatted paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ========================================================
    # Component 3: Level 3 items use "Clause N.M.K." format (0.30 points)
    # Expected: Multiple Clause items with proper parent numbering
    # ========================================================
    try:
        num_clauses = len(clauses_found)
        if num_clauses >= 8:
            valid_parents = all(1 <= c[0] <= 5 for c in clauses_found)
            clause_parents = set((c[0], c[1]) for c in clauses_found)
            section_set = set(sections_found)
            parents_match = valid_parents and clause_parents.issubset(section_set)
            if parents_match:
                print(f"PASS: Component 3 — {num_clauses} Clause items with correct N.M.K format (0.30 pts)")
                total_score += 0.30
            elif valid_parents:
                print(f"PARTIAL: Component 3 — Clauses found but parent sections missing (0.2 pts)")
                total_score += 0.2
            elif not valid_parents:
                print(f"PARTIAL: Component 3 — Clauses found but parent numbers invalid (0.15 pts)")
                total_score += 0.15
        elif num_clauses > 0:
            if num_clauses > 0:
                partial = round(0.30 * min(num_clauses / 8.0, 1.0), 2)
                print(f"PARTIAL: Component 3 — Only {num_clauses} Clause items found ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 3 — No 'Clause N.M.K.' formatted paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
