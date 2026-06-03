"""
Reward Script: Configure Java compiler settings in VSCode for Java 17 + preview features
Task ID: vscode_lang_070
Domain: vscode
Scoring:
  - Component 1 (0.35): java.configuration.runtimes contains JDK 17 entry
  - Component 2 (0.25): java.compile.nullAnalysis.mode == "automatic"
  - Component 3 (0.40): pom.xml has --enable-preview in maven-compiler-plugin
"""

import os
import json
import re
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_070'

SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
POM_PATH = os.path.join(WORKDIR, TASK_ID, 'pom.xml')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
        return json.loads(cleaned)
    except Exception as e:
        print(f"ERROR: Cannot load settings from {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings.json
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: java.configuration.runtimes contains JDK 17 entry (0.35 points)
    # This must be absent in initial_env and present in golden_env
    try:
        runtimes = settings.get("java.configuration.runtimes")
        if isinstance(runtimes, list) and len(runtimes) > 0:
            # Check if any runtime entry references Java 17
            jdk17_found = False
            for rt in runtimes:
                if not isinstance(rt, dict):
                    continue
                name = str(rt.get("name", "")).lower()
                path = str(rt.get("path", "")).lower()
                # Accept JavaSE-17 or similar naming, or path containing java-17
                if "17" in name or "17" in path:
                    jdk17_found = True
                    break
            if jdk17_found:
                print(f"PASS: Component 1 — java.configuration.runtimes contains JDK 17 entry (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — java.configuration.runtimes exists but no JDK 17 entry found. Entries: {runtimes}")
        else:
            print(f"FAIL: Component 1 — java.configuration.runtimes is missing or empty. Value: {runtimes}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: java.compile.nullAnalysis.mode == "automatic" (0.25 points)
    # This must be absent in initial_env and present in golden_env
    try:
        null_mode = settings.get("java.compile.nullAnalysis.mode")
        if null_mode is not None and str(null_mode).lower() == "automatic":
            print(f"PASS: Component 2 — java.compile.nullAnalysis.mode is 'automatic' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — java.compile.nullAnalysis.mode expected 'automatic', found: {null_mode}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: pom.xml has --enable-preview in maven-compiler-plugin compilerArgs (0.40 points)
    # This must be absent in initial_env pom.xml and present in golden_env pom.xml
    try:
        if not os.path.exists(POM_PATH):
            print(f"FAIL: Component 3 — pom.xml not found at {POM_PATH}")
        else:
            tree = ET.parse(POM_PATH)
            root = tree.getroot()
            # Maven POM namespace
            ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

            enable_preview_found = False

            # Search for --enable-preview in compilerArgs within maven-compiler-plugin
            for plugin in root.findall('.//m:plugin', ns):
                artifact = plugin.find('m:artifactId', ns)
                if artifact is not None and artifact.text == 'maven-compiler-plugin':
                    # Look for compilerArgs/arg containing --enable-preview
                    for arg in plugin.findall('.//m:compilerArgs/m:arg', ns):
                        if arg.text and '--enable-preview' in arg.text:
                            enable_preview_found = True
                            break
                    # Also check compilerArguments or any compilerArg pattern
                    if not enable_preview_found:
                        for arg in plugin.findall('.//m:compilerArgument', ns):
                            if arg.text and '--enable-preview' in arg.text:
                                enable_preview_found = True
                                break

            if not enable_preview_found:
                # Fallback: check raw text of pom.xml for --enable-preview
                with open(POM_PATH, 'r') as f:
                    pom_content = f.read()
                if '--enable-preview' in pom_content:
                    enable_preview_found = True

            if enable_preview_found:
                print(f"PASS: Component 3 — pom.xml contains --enable-preview flag (0.40 pts)")
                total_score += 0.40
            else:
                print(f"FAIL: Component 3 — pom.xml does not contain --enable-preview flag")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
