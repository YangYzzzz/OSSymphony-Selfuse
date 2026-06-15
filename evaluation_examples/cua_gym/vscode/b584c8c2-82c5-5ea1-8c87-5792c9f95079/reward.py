"""
Reward Script: Set up VSCode workspace for Java Spring Boot project
Task ID: vscode_we_088
Domain: vscode
Scoring:
  Component 1 (0.30): Java Extension Pack installed
  Component 2 (0.25): java.jdt.ls.java.home configured
  Component 3 (0.25): java.configuration.maven.userSettings configured
  Component 4 (0.20): spring-boot.ls.checkJVM set to false
"""

import os
import json
import re

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings.json: {e}")
        return {}


def check_extension_installed(extension_id):
    """Check if a VSCode extension is installed by scanning the extensions dir."""
    extensions_dir = os.path.join(HOME, ".vscode", "extensions")
    if not os.path.isdir(extensions_dir):
        return False
    # Extension folders are named like publisher.name-version
    prefix = extension_id.lower()
    for entry in os.listdir(extensions_dir):
        if entry.lower().startswith(prefix):
            return True
    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Java Extension Pack is installed (0.30 points)
    try:
        ext_id = "vscjava.vscode-java-pack"
        installed = check_extension_installed(ext_id)
        if installed:
            print(f"PASS: Component 1 - Extension '{ext_id}' is installed (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - Extension '{ext_id}' not found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Load settings for Components 2-4
    settings = load_settings()
    print(f"DEBUG: Loaded settings keys: {list(settings.keys())}")

    # Component 2: java.jdt.ls.java.home is set to /usr/lib/jvm/java-17-openjdk (0.25 points)
    try:
        java_home = settings.get("java.jdt.ls.java.home")
        expected_java_home = "/usr/lib/jvm/java-17-openjdk"
        if java_home == expected_java_home:
            print(f"PASS: Component 2 - java.jdt.ls.java.home = '{java_home}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - java.jdt.ls.java.home expected '{expected_java_home}', found '{java_home}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: java.configuration.maven.userSettings is set to ~/.m2/settings.xml (0.25 points)
    try:
        maven_settings = settings.get("java.configuration.maven.userSettings")
        expected_maven = "~/.m2/settings.xml"
        if maven_settings == expected_maven:
            print(f"PASS: Component 3 - java.configuration.maven.userSettings = '{maven_settings}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - java.configuration.maven.userSettings expected '{expected_maven}', found '{maven_settings}'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: spring-boot.ls.checkJVM is set to false (0.20 points)
    try:
        check_jvm = settings.get("spring-boot.ls.checkJVM")
        if check_jvm is False:
            print(f"PASS: Component 4 - spring-boot.ls.checkJVM = {check_jvm} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 - spring-boot.ls.checkJVM expected False, found {check_jvm!r}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
