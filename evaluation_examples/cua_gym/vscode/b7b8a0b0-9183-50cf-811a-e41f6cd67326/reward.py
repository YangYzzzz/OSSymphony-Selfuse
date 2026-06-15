"""
Reward Script: Use Emmet's 'Wrap with Abbreviation' to wrap existing list items with a <ul> tag.
Task ID: vscode_code_057
Domain: vs_code
Scoring:
  - Component 1: <ul> tag wraps all <li> items (0.5 points)
  - Component 2: All 4 <li> items (Milk, Eggs, Bread, Butter) are preserved inside <ul> (0.3 points)
  - Component 3: <ul> is correctly nested inside <div class="shopping-list"> and <div> structure preserved (0.2 points)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_057'
FILE_PATH = '/home/user/web/list.html'


def verify_task(file_path):
    """
    Verify that the <li> items in list.html are wrapped in a <ul> tag.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: <ul> tag wraps all <li> items (0.5 points)
    # The task requires wrapping all <li> items with a <ul> tag.
    # In the initial file, the <li> items are NOT inside a <ul> tag.
    # In the golden file, a <ul> tag wraps all four <li> items.
    try:
        # Check that a <ul> tag exists containing at least one <li> item
        ul_with_li_pattern = re.compile(r'<ul[^>]*>.*?<li', re.DOTALL | re.IGNORECASE)
        has_ul_wrapping_li = bool(ul_with_li_pattern.search(content))

        if has_ul_wrapping_li:
            print("PASS: Component 1 — <ul> tag found wrapping <li> items (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 — expected <ul> tag wrapping <li> items, not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 <li> items (Milk, Eggs, Bread, Butter) are preserved inside <ul> (0.3 points)
    # Verifies that the task didn't lose any list items during the wrapping.
    # This check FAILS on initial because there is no <ul> containing these items.
    try:
        # Find the <ul> block content
        ul_block_match = re.search(r'<ul[^>]*>(.*?)</ul>', content, re.DOTALL | re.IGNORECASE)
        if ul_block_match:
            ul_content = ul_block_match.group(1)
            expected_items = ['Milk', 'Eggs', 'Bread', 'Butter']
            all_present = all(item in ul_content for item in expected_items)

            if all_present:
                print("PASS: Component 2 — All 4 list items (Milk, Eggs, Bread, Butter) preserved inside <ul> (0.3 pts)")
                total_score += 0.3
            else:
                missing = [item for item in expected_items if item not in ul_content]
                print(f"FAIL: Component 2 — Missing list items inside <ul>: {missing}")
        else:
            print("FAIL: Component 2 — No <ul> block found; cannot verify list items are inside <ul>")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Structural integrity — <ul> is inside <div class="shopping-list"> and
    # no stray <li> items exist outside <ul> (0.2 points)
    # Ensures the entire wrapping is correct: the <ul> must be inside the div, and there
    # must not be <li> items floating outside any <ul>.
    try:
        # Check <ul> is inside div.shopping-list
        div_block_match = re.search(
            r'<div\s+class=["\']shopping-list["\']>(.*?)</div>',
            content, re.DOTALL | re.IGNORECASE
        )

        div_content = div_block_match.group(1) if div_block_match else ''
        ul_in_div_match = re.search(r'<ul[^>]*>(.*?)</ul>', div_content, re.DOTALL | re.IGNORECASE)
        div_without_ul = div_content.replace(ul_in_div_match.group(0), '') if ul_in_div_match else div_content
        stray_li_count = len(re.findall(r'<li', div_without_ul, re.IGNORECASE))

        # Pass if: div exists, <ul> exists in div, and no <li> items are outside the <ul>
        if div_block_match and ul_in_div_match and stray_li_count == 0:
            print("PASS: Component 3 — <ul> correctly nested inside <div class='shopping-list'> with no stray <li> items outside <ul> (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — div found: {bool(div_block_match)}, <ul> in div: {bool(ul_in_div_match)}, stray <li> count outside <ul>: {stray_li_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
