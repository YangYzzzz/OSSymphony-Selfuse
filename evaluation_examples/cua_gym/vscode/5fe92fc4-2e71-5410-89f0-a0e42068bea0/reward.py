"""
Reward Script: Verify Emmet abbreviation expansion in index.html
Task ID: vscode_web_006
Domain: vscode
Scoring:
  Component 1: div.container wrapper exists (0.3 pts)
  Component 2: header element inside div.container (0.2 pts)
  Component 3: main.content element inside div.container (0.3 pts)
  Component 4: footer element inside div.container (0.2 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_006'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'website', 'index.html')


def verify_task(file_path):
    """
    Verify that the Emmet abbreviation 'div.container>header+main.content+footer'
    has been expanded correctly in index.html.
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

    # Normalize whitespace for regex matching
    # We parse the HTML content to check structural elements

    # Component 1: div with class "container" exists (0.3 points)
    # The Emmet abbreviation starts with div.container, so we need a <div class="container">
    try:
        # Check for a div with class="container" (class attribute may have other classes too)
        div_container_pattern = re.compile(
            r'<div\s[^>]*class\s*=\s*["\'][^"\']*\bcontainer\b[^"\']*["\'][^>]*>',
            re.IGNORECASE | re.DOTALL
        )
        div_match = div_container_pattern.search(content)
        if div_match:
            print(f"PASS: Component 1 — Found div.container (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No <div class=\"container\"> found in file")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Extract the content inside div.container for subsequent checks
    # Find the div.container block
    div_content = ""
    try:
        # Find opening div.container tag and extract everything until its closing </div>
        # Use a simple approach: find the div.container, then find matching </div>
        container_block_pattern = re.compile(
            r'(<div\s[^>]*class\s*=\s*["\'][^"\']*\bcontainer\b[^"\']*["\'][^>]*>)(.*?)(</div>)',
            re.IGNORECASE | re.DOTALL
        )
        block_match = container_block_pattern.search(content)
        if block_match:
            div_content = block_match.group(2)
    except Exception as e:
        print(f"WARNING: Could not extract div.container content: {e}")

    # Component 2: header element inside div.container (0.2 points)
    try:
        header_pattern = re.compile(r'<header\b[^>]*>', re.IGNORECASE)
        if div_content and header_pattern.search(div_content):
            print(f"PASS: Component 2 — Found <header> inside div.container (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — No <header> found inside div.container")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: main element with class "content" inside div.container (0.3 points)
    try:
        main_content_pattern = re.compile(
            r'<main\s[^>]*class\s*=\s*["\'][^"\']*\bcontent\b[^"\']*["\'][^>]*>',
            re.IGNORECASE
        )
        if div_content and main_content_pattern.search(div_content):
            print(f"PASS: Component 3 — Found <main class=\"content\"> inside div.container (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — No <main class=\"content\"> found inside div.container")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: footer element inside div.container (0.2 points)
    try:
        footer_pattern = re.compile(r'<footer\b[^>]*>', re.IGNORECASE)
        if div_content and footer_pattern.search(div_content):
            print(f"PASS: Component 4 — Found <footer> inside div.container (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — No <footer> found inside div.container")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
