"""
Reward Script: Emmet abbreviation expansion in VSCode
Task ID: vscode_prod_046
Domain: vscode
Scoring:
  Component 1 (0.25): <div class="container"> element exists
  Component 2 (0.25): <ul class="nav"> exists inside container
  Component 3 (0.30): 5 <li class="item"> elements inside the ul
  Component 4 (0.20): Each li has <a> with text "Link 1" through "Link 5"
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_046'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'website', 'index.html')


def verify_task(file_path):
    """
    Verify that the Emmet abbreviation 'div.container>ul.nav>li.item*5>a{Link $}'
    has been expanded into the HTML file.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the HTML file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: <div class="container"> element exists (0.25 points)
    # This element should NOT exist in the initial file (no navigation structure)
    try:
        container_pattern = re.compile(r'<div\s+class=["\']container["\']', re.IGNORECASE)
        container_match = container_pattern.search(content)
        if container_match:
            print(f"PASS: Component 1 -- <div class=\"container\"> found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- <div class=\"container\"> not found in file")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: <ul class="nav"> exists inside the container (0.25 points)
    try:
        # Check that ul.nav appears after div.container in the content
        container_to_end = content[container_match.start():] if container_match else ""
        ul_pattern = re.compile(r'<ul\s+class=["\']nav["\']', re.IGNORECASE)
        ul_match = ul_pattern.search(container_to_end)
        if ul_match:
            print(f"PASS: Component 2 -- <ul class=\"nav\"> found inside container (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- <ul class=\"nav\"> not found inside container div")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: 5 <li class="item"> elements exist (0.30 points)
    try:
        li_pattern = re.compile(r'<li\s+class=["\']item["\']', re.IGNORECASE)
        li_matches = li_pattern.findall(content)
        li_count = len(li_matches)
        if li_count == 5:
            print(f"PASS: Component 3 -- Found exactly 5 <li class=\"item\"> elements (0.30 pts)")
            total_score += 0.30
        elif li_count > 0:
            # Partial credit: proportional to how many of 5 are present
            partial = 0.30 * (min(li_count, 5) / 5.0)
            print(f"PARTIAL: Component 3 -- Found {li_count}/5 <li class=\"item\"> elements ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No <li class=\"item\"> elements found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Each <li> contains <a> with text "Link 1" through "Link 5" (0.20 points)
    try:
        # Find all <a> tags with "Link N" text inside li.item elements
        # Pattern: <li class="item"><a ...>Link N</a></li>
        link_pattern = re.compile(
            r'<li\s+class=["\']item["\']>\s*<a[^>]*>\s*Link\s+(\d+)\s*</a>',
            re.IGNORECASE
        )
        link_matches = link_pattern.findall(content)
        found_numbers = set(int(n) for n in link_matches)
        expected_numbers = {1, 2, 3, 4, 5}

        if found_numbers == expected_numbers:
            print(f"PASS: Component 4 -- All 5 links (Link 1-5) found with correct text (0.20 pts)")
            total_score += 0.20
        elif len(found_numbers) > 0:
            matched = found_numbers & expected_numbers
            partial = 0.20 * (len(matched) / 5.0)
            print(f"PARTIAL: Component 4 -- Found links: {sorted(found_numbers)}, expected 1-5 ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No <a> tags with 'Link N' text found inside li.item elements")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
