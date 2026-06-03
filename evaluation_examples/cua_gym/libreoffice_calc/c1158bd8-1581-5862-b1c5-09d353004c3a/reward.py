"""
Reward Script: Java Environment Configuration and Maven Build
Task ID: osworld_multi_apps_sys_config_007
Domain: os (system configuration)
Scoring:
  - Component 1: JAVA_HOME=/opt/jdk-17 set in ~/.bashrc (0.25 pts)
  - Component 2: $JAVA_HOME/bin added to PATH in ~/.bashrc (0.25 pts)
  - Component 3: Maven installed via apt-get (check mvn binary and dpkg status file) (0.25 pts)
  - Component 4: mvn compile succeeded — target/classes/ has .class files (0.25 pts)
"""

import os
import re
import stat

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_sys_config_007'
BASHRC_PATH = '/home/user/.bashrc'
JAVA_APP_DIR = '/home/user/projects/java_app'


def verify_task():
    """
    Verify Java environment configuration and Maven build completion.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Read .bashrc content (needed for components 1 and 2)
    try:
        with open(BASHRC_PATH, 'r') as f:
            bashrc_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {BASHRC_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: JAVA_HOME=/opt/jdk-17 is set in ~/.bashrc (0.25 points)
    # Task requires: add "export JAVA_HOME=/opt/jdk-17" to ~/.bashrc
    try:
        # Check for JAVA_HOME assignment pointing to /opt/jdk-17
        # Matches: export JAVA_HOME=/opt/jdk-17  OR  JAVA_HOME=/opt/jdk-17
        java_home_pattern = re.compile(
            r'(export\s+)?JAVA_HOME\s*=\s*/opt/jdk-17\s*$',
            re.MULTILINE
        )
        java_home_found = java_home_pattern.search(bashrc_content) is not None
        if java_home_found:
            print("PASS: Component 1 — JAVA_HOME=/opt/jdk-17 found in ~/.bashrc (0.25 pts)")
            total_score += 0.25
        else:
            # Show what JAVA_HOME lines exist (if any)
            java_home_lines = [
                line.strip() for line in bashrc_content.splitlines()
                if 'JAVA_HOME' in line and not line.strip().startswith('#')
            ]
            print(f"FAIL: Component 1 — JAVA_HOME=/opt/jdk-17 not found in ~/.bashrc")
            print(f"  Existing JAVA_HOME lines: {java_home_lines}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: $JAVA_HOME/bin added to PATH in ~/.bashrc (0.25 points)
    # Task requires: export PATH=$JAVA_HOME/bin:$PATH  (or equivalent)
    try:
        # Check for PATH modification that includes JAVA_HOME/bin
        path_pattern = re.compile(
            r'(export\s+)?PATH\s*=.*\$JAVA_HOME[/\\]bin.*',
            re.MULTILINE
        )
        path_java_home_found = path_pattern.search(bashrc_content) is not None
        if path_java_home_found:
            print("PASS: Component 2 — $JAVA_HOME/bin added to PATH in ~/.bashrc (0.25 pts)")
            total_score += 0.25
        else:
            # Also check for hardcoded /opt/jdk-17/bin path in PATH export
            path_pattern_hardcoded = re.compile(
                r'(export\s+)?PATH\s*=.*/opt/jdk-17/bin.*',
                re.MULTILINE
            )
            path_hardcoded_found = path_pattern_hardcoded.search(bashrc_content) is not None
            if path_hardcoded_found:
                print("PASS: Component 2 — /opt/jdk-17/bin added to PATH in ~/.bashrc (0.25 pts)")
                total_score += 0.25
            else:
                path_lines = [
                    line.strip() for line in bashrc_content.splitlines()
                    if 'PATH' in line and 'jdk' in line.lower() and not line.strip().startswith('#')
                ]
                print(f"FAIL: Component 2 — $JAVA_HOME/bin not added to PATH in ~/.bashrc")
                print(f"  Existing PATH/jdk lines: {path_lines}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Maven is installed (0.25 points)
    # Task requires: sudo apt-get install maven
    # Verification: check that the mvn binary exists and is executable,
    # and the dpkg info file confirms installation (no subprocess needed)
    try:
        mvn_binary = '/usr/bin/mvn'
        dpkg_info_file = '/var/lib/dpkg/info/maven.list'

        mvn_exists = os.path.isfile(mvn_binary)
        mvn_executable = False
        if mvn_exists:
            file_stat = os.stat(mvn_binary)
            mvn_executable = bool(file_stat.st_mode & stat.S_IXUSR)

        dpkg_installed = os.path.isfile(dpkg_info_file)

        if mvn_exists and mvn_executable and dpkg_installed:
            print(f"PASS: Component 3 — Maven installed: {mvn_binary} is executable, dpkg info file present (0.25 pts)")
            total_score += 0.25
        elif mvn_exists and mvn_executable:
            print(f"PASS: Component 3 — Maven binary exists and is executable at {mvn_binary} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Maven not installed")
            print(f"  mvn binary exists: {mvn_exists}, executable: {mvn_executable}, dpkg info: {dpkg_installed}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: mvn compile succeeded — target/classes directory contains .class files (0.25 points)
    # Task requires: run `mvn compile` in /home/user/projects/java_app/ and it succeeds
    try:
        target_classes_dir = os.path.join(JAVA_APP_DIR, 'target', 'classes')
        target_classes_exists = os.path.isdir(target_classes_dir)
        if not target_classes_exists:
            print(f"FAIL: Component 4 — target/classes/ directory not found at {target_classes_dir}")
            print("  This indicates mvn compile has not been run successfully")
        else:
            # Find .class files recursively
            class_files = []
            for root, dirs, files in os.walk(target_classes_dir):
                for f in files:
                    if f.endswith('.class'):
                        class_files.append(os.path.join(root, f))

            classes_found = len(class_files) > 0
            if classes_found:
                total_score += 0.25
                print(f"PASS: Component 4 — mvn compile succeeded: {len(class_files)} .class file(s) in target/classes/ (0.25 pts)")
                for cf in class_files[:5]:  # show up to 5
                    print(f"  Found: {cf}")
            else:
                print(f"FAIL: Component 4 — target/classes/ exists but contains no .class files")
                print(f"  Directory contents: {os.listdir(target_classes_dir)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
