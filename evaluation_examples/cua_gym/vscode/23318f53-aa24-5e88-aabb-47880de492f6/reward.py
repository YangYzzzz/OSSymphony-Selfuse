"""
Reward Script: Install Markdown All in One extension and insert TOC in README.md
Task ID: vscode_stu_074
Domain: vscode
Scoring:
  - Component 1 (0.40): Markdown All in One extension is installed
  - Component 2 (0.35): README.md contains a table of contents block with link entries
  - Component 3 (0.25): TOC covers all document headings
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_074'
README_PATH = os.path.join(WORKDIR, 'README.md')


def get_installed_extensions():
    """Get list of installed VSCode extensions by reading the extensions directory."""
    extensions_dir = os.path.expanduser('~/.vscode/extensions')
    if not os.path.isdir(extensions_dir):
        return []
    return os.listdir(extensions_dir)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Markdown All in One extension is installed (0.40 points)
    # Check via `code --list-extensions` output AND extension directory
    try:
        ext_dirs = get_installed_extensions()
        # Extension folder names look like: yzhang.markdown-all-in-one-<version>
        ext_found = any('markdown-all-in-one' in d.lower() for d in ext_dirs)

        if not ext_found:
            # Fallback: check ~/.vscode/extensions directory with broader search
            alt_ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
            if os.path.isdir(alt_ext_dir):
                alt_dirs = os.listdir(alt_ext_dir)
                ext_found = any('markdown-all-in-one' in d.lower() for d in alt_dirs)

        if ext_found:
            print(f"PASS: Component 1 -- Markdown All in One extension is installed (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 -- Markdown All in One extension NOT found. Dirs: {ext_dirs[:5]}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: README.md contains a table of contents (0.35 points)
    # A TOC is a block of lines with markdown links like "- [Heading](#anchor)"
    try:
        if not os.path.exists(README_PATH):
            print(f"FAIL: Component 2 -- README.md not found at {README_PATH}")
        else:
            with open(README_PATH, 'r') as f:
                content = f.read()

            # Pattern for TOC entries: lines like "- [Text](#anchor)" or "  - [Text](#anchor)"
            toc_pattern = re.compile(r'^\s*-\s+\[.+\]\(#.+\)\s*$', re.MULTILINE)
            toc_entries = toc_pattern.findall(content)

            if len(toc_entries) >= 3:
                print(f"PASS: Component 2 -- TOC found with {len(toc_entries)} entries (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 -- Expected TOC entries (>=3), found {len(toc_entries)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: TOC covers all document headings (0.25 points)
    # Extract all ## and ### headings from the document body (outside the TOC block)
    # and verify they appear as links in the TOC
    try:
        if not os.path.exists(README_PATH):
            print(f"FAIL: Component 3 -- README.md not found")
        else:
            with open(README_PATH, 'r') as f:
                content = f.read()

            # Extract headings from the document (## and ### level)
            heading_pattern = re.compile(r'^(#{2,3})\s+(.+)$', re.MULTILINE)
            headings = heading_pattern.findall(content)
            heading_texts = [h[1].strip() for h in headings]

            # Extract TOC anchor links
            toc_link_pattern = re.compile(r'^\s*-\s+\[(.+?)\]\(#(.+?)\)\s*$', re.MULTILINE)
            toc_links = toc_link_pattern.findall(content)
            toc_link_texts = [t[0].strip() for t in toc_links]

            if len(heading_texts) == 0:
                print(f"FAIL: Component 3 -- No headings found in document")
            else:
                # Check how many headings are covered by the TOC
                covered = 0
                for heading in heading_texts:
                    if heading in toc_link_texts:
                        covered += 1

                coverage_ratio = covered / len(heading_texts)
                if coverage_ratio >= 0.8:
                    print(f"PASS: Component 3 -- TOC covers {covered}/{len(heading_texts)} headings ({coverage_ratio:.0%}) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 -- TOC only covers {covered}/{len(heading_texts)} headings ({coverage_ratio:.0%})")
                    missing = [h for h in heading_texts if h not in toc_link_texts]
                    print(f"  Missing: {missing[:5]}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
