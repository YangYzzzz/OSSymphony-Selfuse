"""
Reward Script: Set up Stable Baselines3 RL library in /home/user/sb3
Task ID: osworld_multi_apps_vscode_env_setup_009
Domain: os / vscode (environment setup)
Scoring:
  Component 1 (0.30): /home/user/sb3 exists and is a git repo cloned from DLR-RM/stable-baselines3
  Component 2 (0.35): stable_baselines3 and gymnasium packages are importable (installed)
  Component 3 (0.35): torch is installed AND 'from stable_baselines3 import PPO' works (PPO importable)
Total: 1.0
"""

import os
import sys
import importlib

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_env_setup_009'
SB3_DIR = '/home/user/sb3'
EXPECTED_REMOTE = 'https://github.com/DLR-RM/stable-baselines3'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: /home/user/sb3 exists as a git repo cloned from DLR-RM/stable-baselines3 (0.30 points)
    # This checks both that the repo was cloned AND that it is from the correct source.
    try:
        # Check directory exists
        if not os.path.isdir(SB3_DIR):
            print(f"FAIL: Component 1 — /home/user/sb3 directory does not exist")
        else:
            # Check it is a git repo with the correct remote
            git_dir = os.path.join(SB3_DIR, '.git')
            if not os.path.isdir(git_dir):
                print(f"FAIL: Component 1 — /home/user/sb3 exists but has no .git directory")
            else:
                # Read the git config to check remote URL
                git_config_path = os.path.join(git_dir, 'config')
                remote_ok = False
                if os.path.isfile(git_config_path):
                    with open(git_config_path, 'r') as f:
                        git_config = f.read()
                    # Check the remote URL
                    if 'DLR-RM/stable-baselines3' in git_config:
                        remote_ok = True

                if remote_ok:
                    # Additionally verify that key repo files are present
                    key_files = ['setup.py', 'stable_baselines3', 'README.md']
                    missing = [f for f in key_files if not os.path.exists(os.path.join(SB3_DIR, f))]
                    if missing:
                        print(f"FAIL: Component 1 — git repo found but missing key files: {missing}")
                    else:
                        print(f"PASS: Component 1 — /home/user/sb3 is a valid clone of DLR-RM/stable-baselines3 (0.30 pts)")
                        total_score += 0.30
                else:
                    print(f"FAIL: Component 1 — /home/user/sb3 git repo does not have expected remote (DLR-RM/stable-baselines3)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: stable_baselines3 and gymnasium packages are importable (0.35 points)
    # Both must be installed and importable.
    try:
        sb3_ok = False
        gym_ok = False

        try:
            import stable_baselines3
            sb3_version = getattr(stable_baselines3, '__version__', 'unknown')
            sb3_ok = True
            print(f"PASS: stable_baselines3 importable (version: {sb3_version})")
        except ImportError as ie:
            print(f"FAIL: stable_baselines3 not importable: {ie}")

        try:
            import gymnasium
            gym_version = getattr(gymnasium, '__version__', 'unknown')
            gym_ok = True
            print(f"PASS: gymnasium importable (version: {gym_version})")
        except ImportError as ie:
            print(f"FAIL: gymnasium not importable: {ie}")

        if sb3_ok and gym_ok:
            print(f"PASS: Component 2 — stable_baselines3 and gymnasium both installed and importable (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — not all required packages are importable (sb3={sb3_ok}, gymnasium={gym_ok})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: torch is installed AND 'from stable_baselines3 import PPO' works (0.35 points)
    # The task specifies creating a PPO model, which requires torch.
    try:
        torch_ok = False
        ppo_ok = False

        try:
            import torch
            torch_version = getattr(torch, '__version__', 'unknown')
            torch_ok = True
            print(f"PASS: torch importable (version: {torch_version})")
        except ImportError as ie:
            print(f"FAIL: torch not importable: {ie}")

        try:
            from stable_baselines3 import PPO
            # Verify PPO class is a class (not just a name)
            if isinstance(PPO, type) or callable(PPO):
                ppo_ok = True
                print(f"PASS: from stable_baselines3 import PPO succeeded (class: {PPO})")
            else:
                print(f"FAIL: PPO is not a callable class: {PPO}")
        except ImportError as ie:
            print(f"FAIL: from stable_baselines3 import PPO failed: {ie}")

        if torch_ok and ppo_ok:
            print(f"PASS: Component 3 — torch installed and PPO importable from stable_baselines3 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — torch={torch_ok}, ppo_importable={ppo_ok}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


verify_task()
