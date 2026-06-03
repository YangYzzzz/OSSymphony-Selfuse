"""
Reward Script: Install kubectl and verify the installation
Task ID: osworld_multi_apps_cli_path_fix_010
Domain: os (CLI/system)
Scoring:
  - Component 1: kubectl binary exists at a standard system path (0.4 pts)
  - Component 2: kubectl is executable and reports a valid version (0.4 pts)
  - Component 3: ~/.bashrc contains a PATH export that includes kubectl's directory (0.2 pts)
"""

import os
import subprocess
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_cli_path_fix_010'

# Known standard install locations for kubectl
KUBECTL_CANDIDATE_PATHS = [
    '/usr/local/bin/kubectl',
    '/usr/bin/kubectl',
    '/snap/bin/kubectl',
    '/opt/kubectl/kubectl',
    '/home/user/.local/bin/kubectl',
    '/home/user/bin/kubectl',
]

BASHRC_PATH = '/home/user/.bashrc'


def verify_task():
    """
    Verify that kubectl was installed and added to PATH.
    Returns a progressive float between 0.0 and 1.0.
    """
    total_score = 0.0

    # ----------------------------------------------------------------
    # Component 1: kubectl binary exists at a standard system path (0.4 pts)
    # This FAILS on initial_env (no kubectl) and PASSES on golden_env
    # ----------------------------------------------------------------
    try:
        kubectl_path = None

        # First check well-known paths
        for candidate in KUBECTL_CANDIDATE_PATHS:
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                kubectl_path = candidate
                break

        # Also try `which kubectl` in case it's in another location
        if kubectl_path is None:
            result = subprocess.run(
                ['which', 'kubectl'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                candidate = result.stdout.strip()
                if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                    kubectl_path = candidate

        if kubectl_path is not None:
            print(f"PASS: Component 1 — kubectl binary found at {kubectl_path} (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — kubectl binary not found in any standard path")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: kubectl is executable and reports a valid version (0.4 pts)
    # This FAILS on initial_env (kubectl not installed) and PASSES on golden_env
    # ----------------------------------------------------------------
    try:
        # Run `kubectl version --client` using the full path or relying on PATH
        env_with_path = os.environ.copy()
        env_with_path['PATH'] = '/usr/local/bin:/usr/bin:/bin:' + env_with_path.get('PATH', '')

        result = subprocess.run(
            ['kubectl', 'version', '--client'],
            capture_output=True,
            text=True,
            env=env_with_path,
            timeout=15
        )
        combined_output = result.stdout + result.stderr

        # Look for a version string like "v1.XX.Y" or "Client Version: v..."
        version_match = re.search(r'v\d+\.\d+\.\d+', combined_output)
        if result.returncode == 0 and version_match:
            version_str = version_match.group(0)
            print(f"PASS: Component 2 — kubectl version --client succeeded, version: {version_str} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — kubectl version --client failed or no version string. "
                  f"returncode={result.returncode}, output={combined_output[:200]}")
    except FileNotFoundError:
        print("FAIL: Component 2 — kubectl binary not found in PATH during execution")
    except subprocess.TimeoutExpired:
        print("FAIL: Component 2 — kubectl version --client timed out")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: ~/.bashrc contains a PATH export for kubectl's directory (0.2 pts)
    # The task context says: "kubectl is installed, added to PATH in ~/.bashrc"
    # This FAILS on initial_env (no such export) and PASSES on golden_env
    # ----------------------------------------------------------------
    try:
        if not os.path.isfile(BASHRC_PATH):
            print(f"FAIL: Component 3 — {BASHRC_PATH} not found")
        else:
            with open(BASHRC_PATH, 'r') as f:
                bashrc_content = f.read()

            # Check for an export PATH line that includes a directory containing kubectl
            # Common patterns: export PATH="$PATH:/usr/local/bin"
            #                  export PATH=/usr/local/bin:$PATH
            #                  PATH=$PATH:/usr/local/bin
            path_export_pattern = re.search(
                r'export\s+PATH\s*=.*(/usr/local/bin|/usr/bin|/snap/bin|\.local/bin)',
                bashrc_content
            )
            # Also catch simpler PATH= assignments
            if path_export_pattern is None:
                path_export_pattern = re.search(
                    r'PATH\s*=.*(/usr/local/bin|/usr/bin|/snap/bin|\.local/bin)',
                    bashrc_content
                )

            if path_export_pattern:
                print(f"PASS: Component 3 — ~/.bashrc contains PATH export: "
                      f"'{path_export_pattern.group(0).strip()}' (0.2 pts)")
                total_score += 0.2
            else:
                print("FAIL: Component 3 — ~/.bashrc does not contain a PATH export for kubectl's directory")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
