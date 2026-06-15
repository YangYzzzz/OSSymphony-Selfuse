"""
Reward Script: Generate a table of contents for documentation.md using Markdown All in One
Task ID: vscode_lp_029
Domain: vscode
Scoring:
  - Component 1 (0.3): TOC block exists near the top of the file
  - Component 2 (0.35): TOC contains links to all ## level sections
  - Component 3 (0.35): TOC contains indented links to ### sub-sections
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_029'


def verify_task(file_path):
    """
    Verify that a table of contents was generated in the Markdown file.
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

    lines = content.split('\n')

    # Find where actual content sections start (first ## heading)
    first_h2_index = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('## ') and not stripped.startswith('## Table of Contents'):
            first_h2_index = i
            break

    if first_h2_index is None:
        print("FAIL: No ## headings found in file")
        print("REWARD: 0.0")
        return 0.0

    # Extract the header portion (before first real ## section) to look for TOC
    header_section = '\n'.join(lines[:first_h2_index])

    # Collect all ## and ### headings from the document body (after the TOC area)
    h2_headings = []
    h3_headings = []
    for line in lines[first_h2_index:]:
        stripped = line.strip()
        if stripped.startswith('### '):
            h3_headings.append(stripped[4:].strip())
        elif stripped.startswith('## '):
            h2_headings.append(stripped[3:].strip())

    # Component 1: TOC block exists near the top (0.3 points)
    # Look for markdown list items with links in the header section
    # TOC items look like: - [Text](#anchor) or  - [Text](#anchor)
    toc_link_pattern = re.compile(r'^\s*[-*]\s+\[.+?\]\(#.+?\)', re.MULTILINE)
    toc_links = toc_link_pattern.findall(header_section)

    try:
        if len(toc_links) >= 3:
            print(f"PASS: Component 1 — TOC block found with {len(toc_links)} entries (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — TOC block not found or too few entries ({len(toc_links)} links in header)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: TOC covers all ## sections (0.35 points)
    # Check that each ## heading has a corresponding TOC link
    try:
        matched_h2 = 0
        for heading in h2_headings:
            # Generate expected anchor: lowercase, spaces to hyphens, strip non-alphanumeric
            anchor = heading.lower().replace(' ', '-')
            anchor = re.sub(r'[^a-z0-9\-]', '', anchor)
            # Check if any TOC link references this heading (by text or anchor)
            heading_found = False
            for link in toc_links:
                # Extract link text and anchor from markdown link
                link_match = re.search(r'\[(.+?)\]\(#(.+?)\)', link)
                if link_match:
                    link_text = link_match.group(1).strip()
                    link_anchor = link_match.group(2).strip()
                    # Match by anchor similarity or text similarity
                    if (anchor in link_anchor or link_anchor in anchor or
                            heading.lower() == link_text.lower()):
                        heading_found = True
                        break
            if heading_found:
                matched_h2 += 1

        if len(h2_headings) > 0:
            h2_ratio = matched_h2 / len(h2_headings)
            if h2_ratio >= 0.9:
                print(f"PASS: Component 2 — {matched_h2}/{len(h2_headings)} ## sections in TOC (0.35 pts)")
                total_score += 0.35
            elif h2_ratio >= 0.5:
                partial = round(0.35 * h2_ratio, 2)
                print(f"PARTIAL: Component 2 — {matched_h2}/{len(h2_headings)} ## sections in TOC ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — only {matched_h2}/{len(h2_headings)} ## sections in TOC")
        else:
            print("FAIL: Component 2 — no ## headings found in document")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: TOC covers ### sub-sections with indentation (0.35 points)
    # Check that ### headings appear as indented items in the TOC
    try:
        # Indented TOC items have leading whitespace (2+ spaces or tab)
        indented_links = [link for link in toc_links if re.match(r'\s{2,}[-*]', link)]

        matched_h3 = 0
        for heading in h3_headings:
            anchor = heading.lower().replace(' ', '-')
            anchor = re.sub(r'[^a-z0-9\-]', '', anchor)
            heading_found = False
            for link in toc_links:
                link_match = re.search(r'\[(.+?)\]\(#(.+?)\)', link)
                if link_match:
                    link_text = link_match.group(1).strip()
                    link_anchor = link_match.group(2).strip()
                    if (anchor in link_anchor or link_anchor in anchor or
                            heading.lower() == link_text.lower()):
                        heading_found = True
                        break
            if heading_found:
                matched_h3 += 1

        if len(h3_headings) > 0:
            h3_ratio = matched_h3 / len(h3_headings)
            # Also check that there are indented items (sub-sections should be indented)
            has_indentation = len(indented_links) >= 1
            if h3_ratio >= 0.9 and has_indentation:
                print(f"PASS: Component 3 — {matched_h3}/{len(h3_headings)} ### sub-sections in TOC, "
                      f"{len(indented_links)} indented entries (0.35 pts)")
                total_score += 0.35
            elif h3_ratio >= 0.5:
                partial = round(0.35 * h3_ratio, 2)
                print(f"PARTIAL: Component 3 — {matched_h3}/{len(h3_headings)} ### sub-sections in TOC ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — only {matched_h3}/{len(h3_headings)} ### sub-sections in TOC")
        else:
            print("FAIL: Component 3 — no ### headings found in document")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.md'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
