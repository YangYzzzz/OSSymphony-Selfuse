"""
Reward Script: Verify Emmet wrap with <ul class="nav-list"> around three <li> elements
Task ID: vscode_lp_027
Domain: vscode
Scoring:
  Component 1 (0.4): <ul class="nav-list"> exists inside <nav class="primary-nav">
  Component 2 (0.3): All three <li> items (Home, Projects, Contact) are children of <ul class="nav-list">
  Component 3 (0.3): Rest of HTML content is preserved intact
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_027'


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

    # Component 1: <ul class="nav-list"> exists inside <nav class="primary-nav"> (0.4 points)
    # This checks the core task requirement: a <ul> with class 'nav-list' was added inside the nav.
    try:
        # Extract the <nav class="primary-nav"> block
        nav_match = re.search(
            r'<nav\s+class=["\']primary-nav["\']>(.*?)</nav>',
            content,
            re.DOTALL
        )
        if nav_match:
            nav_content = nav_match.group(1)
            # Check for <ul class="nav-list"> inside the nav block
            ul_match = re.search(
                r'<ul\s+class=["\']nav-list["\']>',
                nav_content
            )
            if ul_match:
                print("PASS: Component 1 — <ul class='nav-list'> found inside <nav class='primary-nav'> (0.4 pts)")
                total_score += 0.4
            else:
                print("FAIL: Component 1 — <ul class='nav-list'> not found inside <nav class='primary-nav'>")
        else:
            print("FAIL: Component 1 — <nav class='primary-nav'> block not found in HTML")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All three <li> items are children of <ul class="nav-list"> (0.3 points)
    # Verifies that the three nav items are correctly wrapped inside the new <ul>
    try:
        # Extract content between <ul class="nav-list"> and its closing </ul> inside nav
        if nav_match:
            nav_content = nav_match.group(1)
            ul_block_match = re.search(
                r'<ul\s+class=["\']nav-list["\']>(.*?)</ul>',
                nav_content,
                re.DOTALL
            )
            if ul_block_match:
                ul_content = ul_block_match.group(1)
                items_found = re.findall(r'<li>(.*?)</li>', ul_content)
                expected_items = ['Home', 'Projects', 'Contact']
                items_text = [item.strip() for item in items_found]
                if items_text == expected_items:
                    print(f"PASS: Component 2 — All 3 <li> items ({items_text}) are inside <ul class='nav-list'> (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Expected {expected_items} inside <ul class='nav-list'>, found {items_text}")
            else:
                print("FAIL: Component 2 — Could not find <ul class='nav-list'>...</ul> block in nav")
        else:
            print("FAIL: Component 2 — nav block not found (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Rest of HTML is preserved (0.3 points)
    # Verifies the task didn't corrupt other parts of the file.
    # We check key structural elements that must still be present.
    try:
        checks_passed = 0
        checks_total = 6

        # Check <title>
        if '<title>Portfolio Navigation</title>' in content:
            checks_passed += 1
        else:
            print("FAIL: Component 3 sub-check — <title> tag missing or changed")

        # Check header h1
        if '<h1>Creative Studio</h1>' in content:
            checks_passed += 1
        else:
            print("FAIL: Component 3 sub-check — <h1> tag missing or changed")

        # Check hero section
        if '<h2>Welcome to Our Studio</h2>' in content:
            checks_passed += 1
        else:
            print("FAIL: Component 3 sub-check — hero h2 missing or changed")

        # Check services section with its own <ul class="service-list">
        if '<ul class="service-list">' in content:
            checks_passed += 1
        else:
            print("FAIL: Component 3 sub-check — service-list <ul> missing or changed")

        # Check footer
        if '2025 Creative Studio' in content:
            checks_passed += 1
        else:
            print("FAIL: Component 3 sub-check — footer text missing or changed")

        # Check that the three service <li> items are still present in service-list
        service_ul_match = re.search(
            r'<ul\s+class=["\']service-list["\']>(.*?)</ul>',
            content,
            re.DOTALL
        )
        if service_ul_match:
            service_items = re.findall(r'<li>(.*?)</li>', service_ul_match.group(1))
            service_text = [item.strip() for item in service_items]
            if service_text == ['Web Design', 'Brand Identity', 'Mobile Development']:
                checks_passed += 1
            else:
                print(f"FAIL: Component 3 sub-check — service items changed: {service_text}")
        else:
            print("FAIL: Component 3 sub-check — service-list section not found")

        # Award points only if ALL sub-checks pass (this is a preservation check)
        # This component only contributes to score difference if the file is corrupted
        # in golden vs initial. Since both should have these elements, we use this as
        # a gated integrity check that only matters in combination with Component 1+2.
        # Actually, to ensure initial scores 0.0, we need this check to be conditional
        # on Component 1 passing (the task-introduced change).
        if checks_passed == checks_total and total_score > 0:
            print(f"PASS: Component 3 — All {checks_total} integrity checks passed (0.3 pts)")
            total_score += 0.3
        elif checks_passed < checks_total:
            print(f"FAIL: Component 3 — {checks_passed}/{checks_total} integrity checks passed")
        else:
            print(f"FAIL: Component 3 — Integrity OK but task-change components not met, no points awarded")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
