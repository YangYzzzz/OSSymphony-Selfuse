"""
Reward Script: Multi-command keybinding with runCommands feature
Task ID: vscode_rrt_090
Domain: vscode
Scoring:
  Component 1 (0.2): keybinding with key ctrl+shift+b exists
  Component 2 (0.2): keybinding uses runCommands command
  Component 3 (0.2): args.commands includes workbench.action.files.saveAll
  Component 4 (0.2): args.commands includes terminal.sendSequence with npm run build
  Component 5 (0.2): commands are in correct order (saveAll before sendSequence)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
KEYBINDINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "keybindings.json")


def load_keybindings():
    """Load keybindings.json, handling optional JSONC comment prefix."""
    try:
        with open(KEYBINDINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments (// style)
        stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            # Try skipping first line (comment prefix)
            lines = content.split("\n", 1)
            if len(lines) > 1:
                return json.loads(lines[1])
            return None
    except FileNotFoundError:
        return None
    except Exception:
        return None


def find_target_keybinding(bindings):
    """Find the ctrl+shift+b keybinding entry (case-insensitive key match)."""
    if not isinstance(bindings, list):
        return None
    for entry in bindings:
        if not isinstance(entry, dict):
            continue
        key = entry.get("key", "")
        if key.lower().replace(" ", "") == "ctrl+shift+b":
            return entry
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: keybindings.json must exist and be valid JSON
    bindings = load_keybindings()
    if bindings is None:
        print("CRITICAL: Cannot load keybindings.json or file not found")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(bindings, list):
        print(f"CRITICAL: keybindings.json is not a list, got {type(bindings)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: A keybinding with key ctrl+shift+b exists (0.2 points)
    try:
        target = find_target_keybinding(bindings)
        if target is not None:
            print(f"PASS: Component 1 - ctrl+shift+b keybinding found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 - No keybinding with key ctrl+shift+b found")
            print(f"  Available keys: {[e.get('key') for e in bindings if isinstance(e, dict)]}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: The keybinding uses the runCommands command (0.2 points)
    try:
        if target is not None:
            command = target.get("command", "")
            if command.lower() == "runcommands":
                print(f"PASS: Component 2 - command is 'runCommands' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 - Expected command 'runCommands', found '{command}'")
        else:
            print(f"FAIL: Component 2 - No target keybinding to check command")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: args.commands includes workbench.action.files.saveAll (0.2 points)
    try:
        if target is not None:
            args = target.get("args", {})
            commands = args.get("commands", [])
            has_save_all = False
            for cmd in commands:
                if isinstance(cmd, str) and cmd == "workbench.action.files.saveAll":
                    has_save_all = True
                elif isinstance(cmd, dict) and cmd.get("command") == "workbench.action.files.saveAll":
                    has_save_all = True
            if has_save_all:
                print(f"PASS: Component 3 - saveAll command found in commands list (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 - workbench.action.files.saveAll not found in commands: {commands}")
        else:
            print(f"FAIL: Component 3 - No target keybinding to check commands")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: args.commands includes terminal.sendSequence with "npm run build\n" (0.2 points)
    try:
        if target is not None:
            args = target.get("args", {})
            commands = args.get("commands", [])
            has_build = False
            for cmd in commands:
                if isinstance(cmd, dict):
                    cmd_name = cmd.get("command", "")
                    cmd_args = cmd.get("args", {})
                    if cmd_name == "workbench.action.terminal.sendSequence":
                        text = cmd_args.get("text", "")
                        # Accept variations: "npm run build\n", "npm run build\r\n", etc.
                        if "npm run build" in text:
                            has_build = True
            if has_build:
                print(f"PASS: Component 4 - terminal.sendSequence with 'npm run build' found (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 - terminal.sendSequence with 'npm run build' not found in commands: {commands}")
        else:
            print(f"FAIL: Component 4 - No target keybinding to check commands")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Commands are in correct order - saveAll before sendSequence (0.2 points)
    try:
        if target is not None:
            args = target.get("args", {})
            commands = args.get("commands", [])
            save_idx = -1
            build_idx = -1
            for i, cmd in enumerate(commands):
                if isinstance(cmd, str) and cmd == "workbench.action.files.saveAll":
                    save_idx = i
                elif isinstance(cmd, dict) and cmd.get("command") == "workbench.action.files.saveAll":
                    save_idx = i
                if isinstance(cmd, dict) and cmd.get("command") == "workbench.action.terminal.sendSequence":
                    text = cmd.get("args", {}).get("text", "")
                    if "npm run build" in text:
                        build_idx = i
            if save_idx >= 0 and build_idx >= 0 and save_idx < build_idx:
                print(f"PASS: Component 5 - Correct order: saveAll (idx={save_idx}) before build (idx={build_idx}) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 5 - Incorrect order: saveAll idx={save_idx}, build idx={build_idx}")
        else:
            print(f"FAIL: Component 5 - No target keybinding to check order")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
