"""
Reward Script: Transform CSS class selectors from kebab-case to camelCase
Task ID: vscode_edit_090
Domain: vs_code
Scoring:
  Component 1: All 10 camelCase class selectors present                              — 0.50 points
  Component 2a: All 10 kebab-case selectors removed                                 — 0.30 points
  Component 2b: CSS property values preserved (gated: only when kebab are removed)  — 0.20 points
  Total: 1.00

Note: Component 2b is gated behind Component 2a to ensure property preservation
is only scored after the actual task change (selector renaming) has occurred.
This prevents scoring pre-existing conditions.
"""

import os
import re

WORKDIR = '/home/user/Desktop'
FILE_PATH = os.path.join(WORKDIR, 'refactor.css')

# Ground truth: required camelCase class names after task
EXPECTED_CAMEL = [
    '.mainContainer',
    '.navBar',
    '.sidePanel',
    '.contentArea',
    '.footerSection',
    '.btnPrimary',
    '.cardHeader',
    '.listItem',
    '.formGroup',
    '.modalBody',
]

# Original kebab-case names that must NOT exist after task
ORIGINAL_KEBAB = [
    '.main-container',
    '.nav-bar',
    '.side-panel',
    '.content-area',
    '.footer-section',
    '.btn-primary',
    '.card-header',
    '.list-item',
    '.form-group',
    '.modal-body',
]

# Spot-check: CSS properties that must be preserved — these are inside rule blocks
# and should be unchanged by the kebab-to-camelCase conversion
PRESERVED_PROPERTIES = [
    'display: flex',
    'background-color: #f4f6f9',
    'background-color: #1a1a2e',
    'width: 240px',
    'padding: 10px 20px',
    'font-weight: 700',
    'margin-bottom: 18px',
    'max-height: 60vh',
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the file — if missing, return 0.0 immediately
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        print(f"INFO: Loaded file '{file_path}' ({len(content)} bytes)")
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------
    # Component 1: All 10 camelCase class selectors are present (0.50 points)
    # Each successfully converted selector earns 0.05 points (10 * 0.05 = 0.50).
    # FAILS on initial_env (no camelCase selectors exist).
    # PASSES on golden_env (all 10 are converted).
    # -------------------------------------------------------
    try:
        found_camel = []
        missing_camel = []

        for cls in EXPECTED_CAMEL:
            # Match the class selector at start of a CSS rule block,
            # allowing for optional whitespace/newline before '{'
            pattern = re.escape(cls) + r'\s*\{'
            if re.search(pattern, content):
                found_camel.append(cls)
            else:
                missing_camel.append(cls)

        if missing_camel:
            print(f"FAIL: Component 1 — Missing camelCase selectors: {missing_camel}")
            print(f"      Found {len(found_camel)}/10")
            # Award partial credit for each found selector
            if found_camel:
                partial_pts = len(found_camel) * 0.05
                print(f"PARTIAL: Component 1 — {len(found_camel)}/10 selectors converted ({partial_pts:.2f} pts)")
                total_score += partial_pts
        if not missing_camel:
            comp1_pts = len(found_camel) * 0.05
            print(f"PASS: Component 1 — All 10 camelCase selectors present ({comp1_pts:.2f} pts)")
            total_score += comp1_pts

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------
    # Component 2a: All kebab-case class names removed (0.30 points)
    # Each removed kebab selector earns 0.03 points (10 * 0.03 = 0.30).
    # FAILS on initial_env (all kebab selectors are still present).
    # PASSES on golden_env (all 10 are renamed away).
    # -------------------------------------------------------
    try:
        remaining_kebab = []
        removed_kebab = []

        for cls in ORIGINAL_KEBAB:
            pattern = re.escape(cls) + r'\s*\{'
            if re.search(pattern, content):
                remaining_kebab.append(cls)
            else:
                removed_kebab.append(cls)

        if remaining_kebab:
            print(f"FAIL: Component 2a — Kebab-case selectors still present: {remaining_kebab}")
            print(f"      Removed {len(removed_kebab)}/10")
            if removed_kebab:
                partial_pts = len(removed_kebab) * 0.03
                print(f"PARTIAL: Component 2a — {len(removed_kebab)}/10 kebab selectors removed ({partial_pts:.2f} pts)")
                total_score += partial_pts
        if not remaining_kebab:
            comp2a_pts = len(removed_kebab) * 0.03
            print(f"PASS: Component 2a — All 10 kebab-case selectors removed ({comp2a_pts:.2f} pts)")
            total_score += comp2a_pts

    except Exception as e:
        print(f"ERROR: Component 2a — {e}")

    # -------------------------------------------------------
    # Component 2b: CSS property values preserved (0.20 points)
    # Gated: only evaluated when all kebab-case selectors have been removed.
    # This ensures property preservation is never scored independently of the
    # task change (it is not a pre-existing condition that earns points).
    # SKIPPED on initial_env (kebab selectors still present, gate not passed).
    # PASSES on golden_env (all kebab gone, properties intact).
    # -------------------------------------------------------
    try:
        if not remaining_kebab:
            missing_props = []
            for prop in PRESERVED_PROPERTIES:
                if prop not in content:
                    missing_props.append(prop)

            if not missing_props:
                print(f"PASS: Component 2b — All spot-checked CSS properties preserved (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2b — Missing/altered CSS properties: {missing_props}")
        else:
            print(f"SKIP: Component 2b — Skipped (kebab selectors still present; gate not passed)")

    except Exception as e:
        print(f"ERROR: Component 2b — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
