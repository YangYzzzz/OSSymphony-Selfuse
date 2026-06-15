"""
Reward Script: Fix broken image link in Markdown tutorial
Task ID: vscode_rf_037
Domain: vscode
Scoring:
  Component 1 (0.5): Broken image path on line 45 is fixed from ./imgs/arch.png to ./images/arch.png
  Component 2 (0.3): All 4 image references point to valid paths under ./images/
  Component 3 (0.2): Document integrity preserved (content not accidentally altered)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_037'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'docs', 'tutorial.md')
IMAGES_DIR = os.path.join(WORKDIR, 'projects', 'docs', 'images')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Broken image path on line 45 is fixed (0.5 points)
    # Initial state has: ![Architecture](./imgs/arch.png)
    # Golden state has:  ![Architecture](./images/arch.png)
    # We check that the broken path './imgs/arch.png' is NO LONGER present
    # AND the correct path './images/arch.png' IS present in an Architecture image reference
    try:
        has_broken_path = '](./imgs/arch.png)' in content
        has_fixed_path = '![Architecture](./images/arch.png)' in content

        if not has_broken_path and has_fixed_path:
            print(f"PASS: Component 1 — Broken image path fixed to ./images/arch.png (0.5 pts)")
            total_score += 0.5
        elif has_broken_path:
            print(f"FAIL: Component 1 — Broken path ./imgs/arch.png still present")
        elif not has_fixed_path:
            print(f"FAIL: Component 1 — Fixed path ./images/arch.png not found (may have been changed to something else)")
        else:
            print(f"FAIL: Component 1 — Unexpected state")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 image references point to valid paths (0.3 points)
    # Expected images: overview.png, arch.png, workflow.png, deployment.png
    # All should reference ./images/<name>.png
    try:
        # Find all markdown image references
        image_refs = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        expected_images = {'overview.png', 'arch.png', 'workflow.png', 'deployment.png'}
        valid_count = 0

        for alt_text, img_path in image_refs:
            # Check if the referenced file actually exists
            # Resolve relative path from the document's directory
            basename = os.path.basename(img_path)
            if basename in expected_images:
                # Check path points to ./images/ directory
                if img_path.startswith('./images/') and os.path.exists(os.path.join(IMAGES_DIR, basename)):
                    valid_count += 1

        if valid_count == 4:
            print(f"PASS: Component 2 — All 4 image references point to valid ./images/ paths (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Only {valid_count}/4 image references are valid ./images/ paths")
            # Print details
            for alt_text, img_path in image_refs:
                basename = os.path.basename(img_path)
                if basename in expected_images:
                    is_valid = img_path.startswith('./images/') and os.path.exists(os.path.join(IMAGES_DIR, basename))
                    print(f"  [{alt_text}]({img_path}) -> {'VALID' if is_valid else 'INVALID'}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Document integrity preserved (0.2 points)
    # Verify key structural elements still exist:
    # - The title heading
    # - 2 fenced code blocks (python and bash)
    # - 5 blockquotes (lines starting with >)
    # - 3 nested bullet lists
    # We check that the fix didn't accidentally delete or corrupt content.
    # NOTE: We only award points if Component 1 also passed (the fix was applied),
    # to ensure this doesn't score on an unmodified initial file.
    try:
        has_title = '# Building a Modern Web Application' in content
        # Count fenced code blocks
        code_blocks = re.findall(r'```(\w+)', content)
        has_python_block = 'python' in code_blocks
        has_bash_block = 'bash' in code_blocks
        # Count blockquotes (lines starting with >)
        blockquote_lines = [l for l in lines if l.strip().startswith('>')]
        has_enough_blockquotes = len(blockquote_lines) >= 5
        # Check nested lists exist (lines with deeper indentation like "    -" or "      -")
        nested_items = [l for l in lines if re.match(r'^    - ', l) or re.match(r'^      - ', l)]
        has_nested_lists = len(nested_items) >= 5

        integrity_ok = (has_title and has_python_block and has_bash_block
                       and has_enough_blockquotes and has_nested_lists)

        # Only award if the fix was actually applied (prevents scoring on unchanged initial)
        if integrity_ok and not has_broken_path and has_fixed_path:
            print(f"PASS: Component 3 — Document integrity preserved (0.2 pts)")
            print(f"  Title: present, Code blocks: python={has_python_block} bash={has_bash_block}")
            print(f"  Blockquotes: {len(blockquote_lines)}, Nested list items: {len(nested_items)}")
            total_score += 0.2
        elif not integrity_ok:
            print(f"FAIL: Component 3 — Document integrity compromised")
            print(f"  Title: {has_title}, Python block: {has_python_block}, Bash block: {has_bash_block}")
            print(f"  Blockquotes: {len(blockquote_lines)} (need >=5), Nested items: {len(nested_items)} (need >=5)")
        else:
            print(f"FAIL: Component 3 — Fix not applied, cannot award integrity points")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
