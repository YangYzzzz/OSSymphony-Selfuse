"""
Reward Script: Extract PDF bookmarks/TOC to indented text file
Task ID: pdf_gf1_032
Domain: pdf
Scoring:
  Component 1 (0.15): toc.txt exists
  Component 2 (0.15): toc.txt has at least 16 lines
  Component 3 (0.25): Top-level (level 1) entries have no leading spaces
  Component 4 (0.25): Level 2 entries start with exactly 2 spaces
  Component 5 (0.10): Level 3 entries start with exactly 4 spaces
  Component 6 (0.10): All bookmark titles from the PDF appear in the file
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_032'

# Known bookmark structure from the PDF (derived from task description + VM exploration)
# Format: (level, title)
EXPECTED_BOOKMARKS = [
    (1, 'Chapter 1: System Architecture Overview'),
    (2, '1.1 Hardware Requirements'),
    (2, '1.2 Software Dependencies'),
    (2, '1.3 Network Configuration'),
    (3, '1.3.1 Firewall Rules'),
    (1, 'Chapter 2: Installation and Deployment'),
    (2, '2.1 Pre-Installation Checklist'),
    (2, '2.2 Step-by-Step Installation'),
    (2, '2.3 Post-Installation Verification'),
    (3, '2.3.1 Health Check Procedures'),
    (1, 'Chapter 3: User Management and Security'),
    (2, '3.1 Role-Based Access Control'),
    (2, '3.2 Authentication Protocols'),
    (3, '3.2.1 Multi-Factor Authentication Setup'),
    (2, '3.3 Audit Logging'),
    (1, 'Chapter 4: Troubleshooting and Maintenance'),
    (2, '4.1 Common Error Codes'),
    (2, '4.2 Performance Tuning'),
    (2, '4.3 Backup and Recovery'),
    (3, '4.3.1 Disaster Recovery Procedures'),
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    toc_path = f'{WORKDIR}/Documents/toc.txt'

    # Component 1: toc.txt exists (0.15 points)
    try:
        if os.path.isfile(toc_path):
            print(f"PASS: Component 1 — toc.txt exists (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — toc.txt does not exist at {toc_path}")
            # If file doesn't exist, nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read the file content
    try:
        with open(toc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.splitlines()
        # Filter out completely empty lines for counting meaningful entries
        non_empty_lines = [l for l in lines if l.strip()]
        print(f"INFO: toc.txt has {len(lines)} total lines, {len(non_empty_lines)} non-empty lines")
    except Exception as e:
        print(f"ERROR: Cannot read toc.txt: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: At least 16 non-empty lines (0.15 points)
    try:
        if len(non_empty_lines) >= 16:
            print(f"PASS: Component 2 — {len(non_empty_lines)} non-empty lines >= 16 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — only {len(non_empty_lines)} non-empty lines, expected >= 16")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Top-level (level 1) entries have no leading spaces (0.25 points)
    # Check that all 4 chapter titles appear as lines with no leading whitespace
    try:
        level1_titles = [t for lv, t in EXPECTED_BOOKMARKS if lv == 1]
        level1_pass = 0
        level1_total = len(level1_titles)
        for title in level1_titles:
            found = False
            for line in non_empty_lines:
                if title in line and not line.startswith(' ') and not line.startswith('\t'):
                    found = True
                    break
            if found:
                level1_pass += 1
            else:
                print(f"  DETAIL: Level-1 title not found without indent: '{title}'")
        if level1_pass == level1_total:
            print(f"PASS: Component 3 — all {level1_total} level-1 entries have no leading spaces (0.25 pts)")
            total_score += 0.25
        elif level1_pass > 0:
            partial = 0.25 * (level1_pass / level1_total)
            print(f"PARTIAL: Component 3 — {level1_pass}/{level1_total} level-1 entries correct ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no level-1 entries found without indentation")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Level 2 entries start with exactly 2 spaces (0.25 points)
    try:
        level2_titles = [t for lv, t in EXPECTED_BOOKMARKS if lv == 2]
        level2_pass = 0
        level2_total = len(level2_titles)
        for title in level2_titles:
            found = False
            for line in non_empty_lines:
                if title in line:
                    # Check line starts with exactly 2 spaces then non-space
                    stripped = line.lstrip(' ')
                    indent = len(line) - len(stripped)
                    if indent == 2:
                        found = True
                        break
            if found:
                level2_pass += 1
            else:
                print(f"  DETAIL: Level-2 title not found with 2-space indent: '{title}'")
        if level2_pass == level2_total:
            print(f"PASS: Component 4 — all {level2_total} level-2 entries have 2-space indent (0.25 pts)")
            total_score += 0.25
        elif level2_pass > 0:
            partial = 0.25 * (level2_pass / level2_total)
            print(f"PARTIAL: Component 4 — {level2_pass}/{level2_total} level-2 entries correct ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — no level-2 entries found with 2-space indent")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Level 3 entries start with exactly 4 spaces (0.10 points)
    try:
        level3_titles = [t for lv, t in EXPECTED_BOOKMARKS if lv == 3]
        level3_pass = 0
        level3_total = len(level3_titles)
        for title in level3_titles:
            found = False
            for line in non_empty_lines:
                if title in line:
                    stripped = line.lstrip(' ')
                    indent = len(line) - len(stripped)
                    if indent == 4:
                        found = True
                        break
            if found:
                level3_pass += 1
            else:
                print(f"  DETAIL: Level-3 title not found with 4-space indent: '{title}'")
        if level3_pass == level3_total:
            print(f"PASS: Component 5 — all {level3_total} level-3 entries have 4-space indent (0.10 pts)")
            total_score += 0.10
        elif level3_pass > 0:
            partial = 0.10 * (level3_pass / level3_total)
            print(f"PARTIAL: Component 5 — {level3_pass}/{level3_total} level-3 entries correct ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — no level-3 entries found with 4-space indent")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: All bookmark titles from the PDF appear in the file (0.10 points)
    try:
        all_titles = [t for _, t in EXPECTED_BOOKMARKS]
        file_text = content  # full text of toc.txt
        titles_found = 0
        for title in all_titles:
            if title in file_text:
                titles_found += 1
            else:
                print(f"  DETAIL: Missing bookmark title: '{title}'")
        if titles_found == len(all_titles):
            print(f"PASS: Component 6 — all {len(all_titles)} bookmark titles present (0.10 pts)")
            total_score += 0.10
        elif titles_found > 0:
            partial = 0.10 * (titles_found / len(all_titles))
            print(f"PARTIAL: Component 6 — {titles_found}/{len(all_titles)} titles found ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — no bookmark titles found in toc.txt")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
