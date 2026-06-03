"""
Reward Script: Verify Emmet wrap with <section class="articles"> tag
Task ID: vscode_web_007
Domain: vscode
Scoring:
  Component 1 (0.4): <section class="articles"> tag exists in the HTML
  Component 2 (0.3): All 6 original <p> elements are nested inside the <section> tag
  Component 3 (0.3): Paragraph content is preserved intact
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_007'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'website', 'index.html')

# The 6 paragraph texts that must be preserved inside the section
EXPECTED_PARAGRAPHS = [
    "Breaking: New AI Model Achieves Record Performance on Benchmark Tests",
    "Review: The Latest Smartphone from Nexora Features a Revolutionary Camera",
    "Analysis: How Cloud Computing is Reshaping Enterprise Infrastructure",
    "Opinion: Open Source Software Continues to Drive Innovation Across Industries",
    "Guide: Getting Started with Rust for Systems Programming",
    "Report: Global Semiconductor Shortage Shows Signs of Recovery",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: <section class="articles"> opening and closing tags exist (0.4 points)
    try:
        has_open = bool(re.search(r'<section\s+class\s*=\s*["\']articles["\']\s*>', content))
        has_close = bool(re.search(r'</section>', content))
        if has_open and has_close:
            print(f"PASS: Component 1 — <section class=\"articles\"> tag found with closing tag (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Missing section tag. open={has_open}, close={has_close}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 6 <p> elements are nested inside the <section> tag (0.3 points)
    try:
        # Extract content between <section class="articles"> and </section>
        section_match = re.search(
            r'<section\s+class\s*=\s*["\']articles["\']\s*>(.*?)</section>',
            content, re.DOTALL
        )
        if section_match:
            section_content = section_match.group(1)
            # Find all <p> tags inside the section
            p_tags_inside = re.findall(r'<p>(.*?)</p>', section_content, re.DOTALL)
            p_texts_inside = [t.strip() for t in p_tags_inside]

            # Check that all 6 expected paragraphs are inside
            all_inside = all(
                any(expected in actual for actual in p_texts_inside)
                for expected in EXPECTED_PARAGRAPHS
            )
            if all_inside and len(p_texts_inside) >= 6:
                print(f"PASS: Component 2 — All 6 <p> elements nested inside <section> (0.3 pts)")
                total_score += 0.3
            else:
                found_count = sum(
                    1 for expected in EXPECTED_PARAGRAPHS
                    if any(expected in actual for actual in p_texts_inside)
                )
                print(f"FAIL: Component 2 — Only {found_count}/6 paragraphs inside <section>. Found {len(p_texts_inside)} <p> tags inside.")
        else:
            print(f"FAIL: Component 2 — No <section class=\"articles\"> block found to check nesting")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Paragraph content is preserved intact (0.3 points)
    # All 6 original paragraphs must still exist in the file with exact text
    try:
        all_p_tags = re.findall(r'<p>(.*?)</p>', content, re.DOTALL)
        all_p_texts = [t.strip() for t in all_p_tags]

        preserved_count = sum(
            1 for expected in EXPECTED_PARAGRAPHS
            if any(expected in actual for actual in all_p_texts)
        )

        # Also verify section is inside <main> (structural correctness)
        section_in_main = bool(re.search(
            r'<main>.*<section\s+class\s*=\s*["\']articles["\']\s*>.*</section>.*</main>',
            content, re.DOTALL
        ))

        if preserved_count == 6 and section_in_main:
            print(f"PASS: Component 3 — All 6 paragraphs preserved, section inside <main> (0.3 pts)")
            total_score += 0.3
        elif preserved_count == 6:
            print(f"FAIL: Component 3 — Paragraphs preserved but <section> not inside <main>")
        else:
            print(f"FAIL: Component 3 — Only {preserved_count}/6 paragraphs preserved in file")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
