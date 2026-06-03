"""
Reward Script: Set up workspace trust settings to restrict untrusted workspaces
Task ID: vscode_lp_094
Domain: vscode
Scoring:
  Component 1 (0.25) - Trust prompt/banner settings configured
  Component 2 (0.25) - Untrusted file/empty window restrictions
  Component 3 (0.25) - Task and debugging restrictions
  Component 4 (0.25) - Extension and auto-detect restrictions
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify workspace trust settings are configured to restrict untrusted workspaces.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Precondition: workspace trust must be enabled (true in both initial and golden)
    if not settings.get("security.workspace.trust.enabled", False):
        print("FAIL: Precondition - security.workspace.trust.enabled is not true")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Trust prompt and banner settings (0.25 points)
    # Golden adds: startupPrompt="always", banner="always"
    # These are NOT present in initial_env
    try:
        comp1_score = 0.0
        startup_prompt = settings.get("security.workspace.trust.startupPrompt")
        banner = settings.get("security.workspace.trust.banner")

        if startup_prompt == "always":
            comp1_score += 0.125
            print(f"PASS: startupPrompt is 'always'")
        else:
            print(f"FAIL: Expected startupPrompt='always', found: {startup_prompt}")

        if banner == "always":
            comp1_score += 0.125
            print(f"PASS: banner is 'always'")
        else:
            print(f"FAIL: Expected banner='always', found: {banner}")

        if comp1_score > 0:
            print(f"PASS: Component 1 - Trust prompt/banner ({comp1_score} pts)")
            total_score += comp1_score
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Untrusted file and empty window restrictions (0.25 points)
    # Golden adds: emptyWindow=false, untrustedFiles="prompt"
    try:
        comp2_score = 0.0
        empty_window = settings.get("security.workspace.trust.emptyWindow")
        untrusted_files = settings.get("security.workspace.trust.untrustedFiles")

        if empty_window is False:  # Must be explicitly False, not absent
            comp2_score += 0.125
            print(f"PASS: emptyWindow is false")
        else:
            print(f"FAIL: Expected emptyWindow=false, found: {empty_window}")

        if untrusted_files == "prompt":
            comp2_score += 0.125
            print(f"PASS: untrustedFiles is 'prompt'")
        else:
            print(f"FAIL: Expected untrustedFiles='prompt', found: {untrusted_files}")

        if comp2_score > 0:
            print(f"PASS: Component 2 - Untrusted file/empty window ({comp2_score} pts)")
            total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Task and debugging restrictions (0.25 points)
    # Golden adds: task.allowAutomaticTasks="off", debug.allowBreakpointsEverywhere=false,
    #              terminal.integrated.allowWorkspaceConfiguration=false
    try:
        comp3_score = 0.0
        auto_tasks = settings.get("task.allowAutomaticTasks")
        debug_bp = settings.get("debug.allowBreakpointsEverywhere")
        terminal_ws = settings.get("terminal.integrated.allowWorkspaceConfiguration")

        checks_passed = 0
        if auto_tasks == "off":
            checks_passed += 1
            print(f"PASS: task.allowAutomaticTasks is 'off'")
        else:
            print(f"FAIL: Expected task.allowAutomaticTasks='off', found: {auto_tasks}")

        if debug_bp is False:
            checks_passed += 1
            print(f"PASS: debug.allowBreakpointsEverywhere is false")
        else:
            print(f"FAIL: Expected debug.allowBreakpointsEverywhere=false, found: {debug_bp}")

        if terminal_ws is False:
            checks_passed += 1
            print(f"PASS: terminal.integrated.allowWorkspaceConfiguration is false")
        else:
            print(f"FAIL: Expected terminal.integrated.allowWorkspaceConfiguration=false, found: {terminal_ws}")

        comp3_score = (checks_passed / 3) * 0.25
        if comp3_score > 0:
            print(f"PASS: Component 3 - Task/debug restrictions ({comp3_score:.4f} pts)")
            total_score += comp3_score
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Auto-detect and extension restrictions (0.25 points)
    # Golden adds: npm.autoDetect="off", task.autoDetect="off",
    #              extensions.supportUntrustedWorkspaces={}
    try:
        comp4_score = 0.0
        npm_detect = settings.get("npm.autoDetect")
        task_detect = settings.get("task.autoDetect")
        ext_untrusted = settings.get("extensions.supportUntrustedWorkspaces")

        checks_passed = 0
        if npm_detect == "off":
            checks_passed += 1
            print(f"PASS: npm.autoDetect is 'off'")
        else:
            print(f"FAIL: Expected npm.autoDetect='off', found: {npm_detect}")

        if task_detect == "off":
            checks_passed += 1
            print(f"PASS: task.autoDetect is 'off'")
        else:
            print(f"FAIL: Expected task.autoDetect='off', found: {task_detect}")

        if isinstance(ext_untrusted, dict):
            checks_passed += 1
            print(f"PASS: extensions.supportUntrustedWorkspaces is configured (dict)")
        else:
            print(f"FAIL: Expected extensions.supportUntrustedWorkspaces as dict, found: {ext_untrusted}")

        comp4_score = (checks_passed / 3) * 0.25
        if comp4_score > 0:
            print(f"PASS: Component 4 - Auto-detect/extension restrictions ({comp4_score:.4f} pts)")
            total_score += comp4_score
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
