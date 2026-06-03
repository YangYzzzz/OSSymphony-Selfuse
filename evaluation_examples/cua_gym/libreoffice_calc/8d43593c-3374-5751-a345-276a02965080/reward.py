"""
Reward Script: Clean up VSCode Remote SSH server cache
Task ID: vscode_fix_089
Domain: vscode / os
Scoring:
  Component 1 (0.4): Old server versions removed from ~/.vscode-server/bin/
  Component 2 (0.4): Duplicate extension versions removed from ~/.vscode-server/extensions/
  Component 3 (0.2): Current server version and .current file preserved intact
"""

import os
import re
from collections import defaultdict

VSCODE_SERVER = os.path.expanduser("~/.vscode-server")
BIN_DIR = os.path.join(VSCODE_SERVER, "bin")
EXT_DIR = os.path.join(VSCODE_SERVER, "extensions")

# The current server commit hash (from .current file)
CURRENT_COMMIT = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"

# Initial state had 5 server versions in bin/
INITIAL_BIN_COUNT = 5

# Extensions that had duplicates in initial state (ext_base -> list of versions)
# We track which extensions had multiple versions and what the latest was
INITIAL_EXTENSIONS = {
    "eamodio.gitlens": ["14.5.0", "15.0.4", "15.2.1"],
    "esbenp.prettier-vscode": ["10.1.0", "11.0.0"],
    "ms-azuretools.vscode-docker": ["1.28.0", "1.29.1"],
    "ms-python.python": ["2024.2.1", "2024.8.0", "2025.1.0"],
    "ms-python.vscode-pylance": ["2024.3.100", "2025.1.50"],
}

# Extensions that were singletons (no duplicates) - should be preserved
SINGLETON_EXTENSIONS = [
    "dbaeumer.vscode-eslint-3.0.5",
    "ms-vscode-remote.remote-ssh-0.110.1",
]


def verify_task():
    """
    Verify cleanup of VSCode Remote SSH server cache.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: .vscode-server directory must exist
    if not os.path.isdir(VSCODE_SERVER):
        print(f"CRITICAL: {VSCODE_SERVER} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Old server versions removed from bin/ (0.4 points)
    # In initial state there were 5 versions. After cleanup, only the current one should remain.
    try:
        if not os.path.isdir(BIN_DIR):
            print(f"FAIL: Component 1 -- bin/ directory does not exist")
        else:
            # List actual commit directories (exclude .current and other non-dir files)
            bin_entries = [
                e for e in os.listdir(BIN_DIR)
                if os.path.isdir(os.path.join(BIN_DIR, e)) and not e.startswith(".")
            ]
            bin_count = len(bin_entries)

            if bin_count == 1 and CURRENT_COMMIT in bin_entries:
                print(f"PASS: Component 1 -- Only current server version remains in bin/ ({bin_count} version) (0.4 pts)")
                total_score += 0.4
            elif bin_count < INITIAL_BIN_COUNT and CURRENT_COMMIT in bin_entries:
                # Partial credit: some old versions removed but not all
                removed = INITIAL_BIN_COUNT - bin_count
                if removed > 0:
                    partial = 0.4 * (removed / (INITIAL_BIN_COUNT - 1))
                    print(f"PARTIAL: Component 1 -- {removed} old versions removed, {bin_count - 1} still remain ({partial:.2f} pts)")
                    total_score += partial
            else:
                print(f"FAIL: Component 1 -- bin/ has {bin_count} versions: {bin_entries}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Duplicate extension versions removed (0.4 points)
    # Only the latest version of each extension should remain.
    try:
        if not os.path.isdir(EXT_DIR):
            print(f"FAIL: Component 2 -- extensions/ directory does not exist")
        else:
            ext_entries = [
                e for e in os.listdir(EXT_DIR)
                if os.path.isdir(os.path.join(EXT_DIR, e)) and not e.startswith(".")
            ]

            # Group extensions by base name (without version)
            ext_groups = defaultdict(list)
            version_pattern = re.compile(r'^(.+)-(\d+\.\d+\.\d+.*)$')
            for ext in ext_entries:
                m = version_pattern.match(ext)
                if m:
                    ext_groups[m.group(1)].append(m.group(2))
                else:
                    ext_groups[ext].append("")

            # Check: no extension should have more than one version
            has_duplicates = any(len(versions) > 1 for versions in ext_groups.values())

            # Count how many of the originally-duplicated extensions are now cleaned
            cleaned_count = 0
            total_dup_groups = len(INITIAL_EXTENSIONS)  # 5 groups had duplicates

            for ext_base, initial_versions in INITIAL_EXTENSIONS.items():
                current_versions = ext_groups.get(ext_base, [])
                if len(current_versions) <= 1:
                    cleaned_count += 1

            if cleaned_count == total_dup_groups and not has_duplicates:
                print(f"PASS: Component 2 -- All duplicate extensions cleaned, {len(ext_entries)} extensions remain (0.4 pts)")
                total_score += 0.4
            elif cleaned_count > 0:
                partial = 0.4 * (cleaned_count / total_dup_groups)
                print(f"PARTIAL: Component 2 -- {cleaned_count}/{total_dup_groups} duplicate groups cleaned ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- Duplicates still present. Groups: {dict(ext_groups)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Current server version and .current file preserved (0.2 points)
    # The current server binary and .current pointer must still exist after cleanup.
    try:
        current_file = os.path.join(BIN_DIR, ".current")
        current_dir = os.path.join(BIN_DIR, CURRENT_COMMIT)

        current_file_ok = (
            os.path.isfile(current_file)
            and open(current_file, "r").read().strip() == CURRENT_COMMIT
        )
        current_dir_ok = os.path.isdir(current_dir)

        # Both .current file and current server dir must be intact,
        # AND old versions must actually be removed (to differentiate from initial state)
        bin_entries = [
            e for e in os.listdir(BIN_DIR)
            if os.path.isdir(os.path.join(BIN_DIR, e)) and not e.startswith(".")
        ] if os.path.isdir(BIN_DIR) else []

        # This component only scores if cleanup actually happened (fewer versions than initial)
        cleanup_happened = len(bin_entries) < INITIAL_BIN_COUNT

        if current_file_ok and current_dir_ok and cleanup_happened:
            print(f"PASS: Component 3 -- .current file and current server version preserved after cleanup (0.2 pts)")
            total_score += 0.2
        elif not cleanup_happened:
            print(f"FAIL: Component 3 -- No cleanup detected (still {len(bin_entries)} versions), cannot credit preservation")
        else:
            issues = []
            if not current_file_ok:
                issues.append(".current file missing or wrong")
            if not current_dir_ok:
                issues.append(f"current server dir {CURRENT_COMMIT} missing")
            print(f"FAIL: Component 3 -- {', '.join(issues)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
