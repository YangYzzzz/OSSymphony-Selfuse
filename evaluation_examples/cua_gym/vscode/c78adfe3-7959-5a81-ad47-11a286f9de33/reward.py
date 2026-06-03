"""
Reward Script: Verify Emmet abbreviation expansion in HTML file
Task ID: vscode_stu_068
Domain: vscode
Scoring:
  Component 1 (0.3): div with class 'container' exists inside body
  Component 2 (0.2): ul element exists inside the container div
  Component 3 (0.3): Exactly 5 li elements with class 'item' inside ul
  Component 4 (0.2): Correct nesting structure (div.container > ul > li.item)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_068'


def verify_task(file_path):
    """
    Verify Emmet abbreviation expansion with progressive scoring.
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

    # Parse the HTML to find body content
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if not body_match:
        print("FAIL: No <body> tag found in HTML")
        print("REWARD: 0.0")
        return 0.0

    body_content = body_match.group(1).strip()

    # Component 1: div with class 'container' exists inside body (0.3 points)
    # This should FAIL on initial (empty body) and PASS on golden
    try:
        div_pattern = re.search(r'<div\s+class\s*=\s*["\']container["\'][^>]*>', body_content)
        if div_pattern:
            print(f"PASS: Component 1 — div.container found inside body (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No div with class 'container' found inside body")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ul element exists inside the container div (0.2 points)
    try:
        # Extract content between <div class="container"> and its closing </div>
        div_content_match = re.search(
            r'<div\s+class\s*=\s*["\']container["\'][^>]*>(.*?)</div>',
            body_content, re.DOTALL
        )
        if div_content_match:
            div_inner = div_content_match.group(1)
            ul_match = re.search(r'<ul[^>]*>', div_inner)
            if ul_match:
                print(f"PASS: Component 2 — ul element found inside div.container (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — No ul element found inside div.container")
        else:
            print(f"FAIL: Component 2 — Cannot extract div.container content")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exactly 5 li elements with class 'item' inside ul (0.3 points)
    try:
        # Find all li elements with class 'item' inside the body
        li_items = re.findall(r'<li\s+class\s*=\s*["\']item["\'][^>]*>', body_content)
        li_count = len(li_items)
        if li_count == 5:
            print(f"PASS: Component 3 — Found exactly 5 li.item elements (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected 5 li.item elements, found {li_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Correct nesting structure div.container > ul > li.item (0.2 points)
    # Verify that the li.item elements are specifically inside ul inside div.container
    try:
        if div_content_match:
            div_inner = div_content_match.group(1)
            # Find ul content
            ul_content_match = re.search(r'<ul[^>]*>(.*?)</ul>', div_inner, re.DOTALL)
            if ul_content_match:
                ul_inner = ul_content_match.group(1)
                nested_li_items = re.findall(r'<li\s+class\s*=\s*["\']item["\'][^>]*>', ul_inner)
                if len(nested_li_items) == 5:
                    print(f"PASS: Component 4 — Correct nesting: div.container > ul > 5x li.item (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 — Found {len(nested_li_items)} li.item inside ul (expected 5)")
            else:
                print(f"FAIL: Component 4 — No ul content found inside div.container")
        else:
            print(f"FAIL: Component 4 — No div.container found for nesting check")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.html'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
