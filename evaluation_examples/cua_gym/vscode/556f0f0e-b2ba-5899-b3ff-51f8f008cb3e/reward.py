"""
Reward Script: Configure a custom terminal profile 'K8s-Prod' in VSCode
Task ID: vscode_ops_058
Domain: vscode
Scoring:
  Component 1 (0.25): K8s-Prod profile exists in terminal.integrated.profiles.linux
  Component 2 (0.25): Profile path is /bin/bash
  Component 3 (0.25): Profile env has KUBECONFIG set to /home/user/.kube/prod.config
  Component 4 (0.25): Profile args achieve cd to /home/user/k8s (via --init-file or direct args)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_058'

SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load VSCode settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Get the profiles section
    profiles = settings.get('terminal.integrated.profiles.linux', {})

    # Component 1: K8s-Prod profile exists (0.25 points)
    try:
        if 'K8s-Prod' in profiles:
            print(f"PASS: Component 1 — 'K8s-Prod' profile exists in terminal.integrated.profiles.linux (0.25 pts)")
            total_score += 0.25
        else:
            # Case-insensitive search as fallback
            found = False
            for key in profiles:
                if key.lower() == 'k8s-prod':
                    print(f"FAIL: Component 1 — Profile found as '{key}' but expected exact name 'K8s-Prod'")
                    found = True
                    break
            if not found:
                print(f"FAIL: Component 1 — 'K8s-Prod' profile not found. Available profiles: {list(profiles.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get the profile details (needed for remaining components)
    profile = profiles.get('K8s-Prod', {})

    # Component 2: Profile path is /bin/bash (0.25 points)
    try:
        profile_path = profile.get('path', '')
        if profile_path == '/bin/bash':
            print(f"PASS: Component 2 — Profile path is '/bin/bash' (0.25 pts)")
            total_score += 0.25
        elif profile_path == 'bash':
            # Acceptable alternative
            print(f"PASS: Component 2 — Profile path is 'bash' (acceptable) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected path '/bin/bash', found: '{profile_path}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Profile env has KUBECONFIG=/home/user/.kube/prod.config (0.25 points)
    try:
        env = profile.get('env', {})
        kubeconfig = env.get('KUBECONFIG', '')
        if kubeconfig == '/home/user/.kube/prod.config':
            print(f"PASS: Component 3 — KUBECONFIG env set to '/home/user/.kube/prod.config' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected KUBECONFIG='/home/user/.kube/prod.config', found: '{kubeconfig}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Profile achieves cd to /home/user/k8s (0.25 points)
    # The task says "changes to the /home/user/k8s directory"
    # This can be done via:
    #   a) args: ["--init-file", "<script>"] where script does "cd /home/user/k8s"
    #   b) args: ["-c", "cd /home/user/k8s && exec bash"]
    #   c) Some other mechanism
    # We check for the presence of args that reference /home/user/k8s or an init file that does cd
    try:
        args = profile.get('args', [])
        cd_verified = False

        # Check 1: args contain direct reference to /home/user/k8s
        args_str = json.dumps(args)
        if '/home/user/k8s' in args_str:
            cd_verified = True

        # Check 2: args reference an init-file, check if that file does cd /home/user/k8s
        if not cd_verified and '--init-file' in args:
            init_file_idx = args.index('--init-file')
            if init_file_idx + 1 < len(args):
                init_file_path = args[init_file_idx + 1]
                try:
                    with open(init_file_path, 'r') as f:
                        init_content = f.read()
                    if '/home/user/k8s' in init_content:
                        cd_verified = True
                except Exception:
                    pass

        # Check 3: cwd property in the profile
        if not cd_verified:
            cwd = profile.get('cwd', '')
            if cwd == '/home/user/k8s':
                cd_verified = True

        if cd_verified:
            print(f"PASS: Component 4 — Profile configured to change to /home/user/k8s directory (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — No mechanism found to cd to /home/user/k8s. args: {args}, cwd: {profile.get('cwd', 'not set')}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
