"""
Reward Script: Rename React component 'UserCard' to 'ProfileCard' across all files
Task ID: vscode_web_031
Domain: vscode
Scoring:
  Component 1 (0.20): File renamed from UserCard.tsx to ProfileCard.tsx
  Component 2 (0.20): Component definition renamed (interface + const + export)
  Component 3 (0.40): Import statements updated in all 6 importing files
  Component 4 (0.20): JSX usages updated in all 6 importing files
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_031'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-app', 'src')

# Files that import UserCard (besides the definition file itself)
IMPORTING_FILES = [
    os.path.join(PROJECT_DIR, 'App.tsx'),
    os.path.join(PROJECT_DIR, 'components', 'UserCardList.tsx'),
    os.path.join(PROJECT_DIR, 'pages', 'Dashboard.tsx'),
    os.path.join(PROJECT_DIR, 'pages', 'TeamPage.tsx'),
    os.path.join(PROJECT_DIR, 'pages', 'AdminPanel.tsx'),
    os.path.join(PROJECT_DIR, 'pages', 'SearchResults.tsx'),
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    old_file = os.path.join(PROJECT_DIR, 'components', 'UserCard.tsx')
    new_file = os.path.join(PROJECT_DIR, 'components', 'ProfileCard.tsx')

    # Component 1: File renamed from UserCard.tsx to ProfileCard.tsx (0.20 points)
    try:
        old_exists = os.path.exists(old_file)
        new_exists = os.path.exists(new_file)
        if new_exists and not old_exists:
            print(f"PASS: Component 1 -- ProfileCard.tsx exists, UserCard.tsx removed (0.20 pts)")
            total_score += 0.20
        elif new_exists and old_exists:
            print(f"FAIL: Component 1 -- Both ProfileCard.tsx and UserCard.tsx exist (old not removed)")
        elif not new_exists and old_exists:
            print(f"FAIL: Component 1 -- UserCard.tsx still exists, ProfileCard.tsx not found")
        else:
            print(f"FAIL: Component 1 -- Neither UserCard.tsx nor ProfileCard.tsx found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Component definition renamed inside ProfileCard.tsx (0.20 points)
    # Check: interface ProfileCardProps, const ProfileCard, export default ProfileCard
    try:
        if not os.path.exists(new_file):
            print(f"FAIL: Component 2 -- ProfileCard.tsx does not exist, cannot check definition")
        else:
            with open(new_file, 'r') as f:
                content = f.read()

            checks = {
                'interface': bool(re.search(r'interface\s+ProfileCardProps', content)),
                'const': bool(re.search(r'const\s+ProfileCard', content)),
                'export': bool(re.search(r'export\s+default\s+ProfileCard', content)),
            }
            # Also verify NO old name references remain
            has_old_ref = bool(re.search(r'\bUserCard\b', content))

            passed = sum(checks.values())
            if passed == 3 and not has_old_ref:
                print(f"PASS: Component 2 -- Definition fully renamed: interface={checks['interface']}, const={checks['const']}, export={checks['export']} (0.20 pts)")
                total_score += 0.20
            elif passed == 3 and has_old_ref:
                # Partial: renamed but still has old references
                print(f"PARTIAL: Component 2 -- Definition renamed but old 'UserCard' references remain (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 -- Definition not fully renamed: interface={checks['interface']}, const={checks['const']}, export={checks['export']}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Import statements updated in all 6 importing files (0.40 points)
    # Each file contributes 0.40/6 ~= 0.0667 points
    try:
        import_score = 0.0
        per_file = 0.40 / len(IMPORTING_FILES)
        for fpath in IMPORTING_FILES:
            fname = os.path.relpath(fpath, PROJECT_DIR)
            if not os.path.exists(fpath):
                print(f"FAIL: Component 3 -- {fname} not found")
                continue
            with open(fpath, 'r') as f:
                content = f.read()
            # Check import uses ProfileCard, not UserCard as the component import
            has_new_import = bool(re.search(r"import\s+ProfileCard\s+from\s+['\"].*ProfileCard['\"]", content))
            has_old_import = bool(re.search(r"import\s+UserCard\s+from\s+['\"].*UserCard['\"]", content))

            if has_new_import and not has_old_import:
                print(f"PASS: Component 3 -- {fname} import updated to ProfileCard ({per_file:.4f} pts)")
                import_score += per_file
            elif has_new_import and has_old_import:
                print(f"FAIL: Component 3 -- {fname} has both old and new imports")
            else:
                print(f"FAIL: Component 3 -- {fname} still imports UserCard (old={has_old_import}, new={has_new_import})")

        if import_score > 0:
            total_score += import_score
        print(f"Component 3 subtotal: {import_score:.4f}/0.40")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: JSX usages updated in all 6 importing files (0.20 points)
    # Check that <ProfileCard is used and <UserCard is not
    try:
        jsx_score = 0.0
        per_file = 0.20 / len(IMPORTING_FILES)
        for fpath in IMPORTING_FILES:
            fname = os.path.relpath(fpath, PROJECT_DIR)
            if not os.path.exists(fpath):
                print(f"FAIL: Component 4 -- {fname} not found")
                continue
            with open(fpath, 'r') as f:
                content = f.read()
            has_new_jsx = bool(re.search(r'<ProfileCard[\s/>]', content))
            has_old_jsx = bool(re.search(r'<UserCard[\s/>]', content))

            if has_new_jsx and not has_old_jsx:
                print(f"PASS: Component 4 -- {fname} JSX updated to <ProfileCard> ({per_file:.4f} pts)")
                jsx_score += per_file
            elif has_new_jsx and has_old_jsx:
                print(f"FAIL: Component 4 -- {fname} has both old and new JSX usages")
            else:
                print(f"FAIL: Component 4 -- {fname} still uses <UserCard> (old={has_old_jsx}, new={has_new_jsx})")

        if jsx_score > 0:
            total_score += jsx_score
        print(f"Component 4 subtotal: {jsx_score:.4f}/0.20")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
