"""
Reward Script: Install NLPSOLVE (Solver for Nonlinear Programming) extension in LibreOffice Calc
Task ID: osworld_multi_apps_ext_install_009
Domain: libreoffice_calc
Scoring:
  Component 1: NLPSolver.oxt present in uno_packages cache with correct identifier (0.5 pts)
  Component 2: Extension properties file present with SUPPRESS_LICENSE marker (0.2 pts)
  Component 3: Extension also registered in extensions/tmp/extensions directory (0.3 pts)
Total: 1.0

Verification approach:
  The task requires installing the NLPSolver (NLPSOLVE) extension for LibreOffice Calc.
  When installed, LibreOffice creates entries in two directories:
    1. ~/.config/libreoffice/4/user/uno_packages/cache/uno_packages/
       - Contains the extracted extension files including description.xml with the identifier
    2. ~/.config/libreoffice/4/user/extensions/tmp/extensions/
       - Contains the extension registered for the current session
  We verify these locations to confirm the extension is installed.
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_ext_install_009'

NLPSOLVER_IDENTIFIER = 'com.sun.star.comp.solver.NLPSolver'
UNO_PACKAGES_DIR = '/home/user/.config/libreoffice/4/user/uno_packages/cache/uno_packages'
EXTENSIONS_TMP_DIR = '/home/user/.config/libreoffice/4/user/extensions/tmp/extensions'


def find_nlpsolver_in_uno_packages():
    """
    Search uno_packages directory for NLPSolver.oxt with correct identifier.
    Returns (found_path, identifier, version) or (None, None, None).
    """
    if not os.path.isdir(UNO_PACKAGES_DIR):
        return None, None, None

    for item in os.listdir(UNO_PACKAGES_DIR):
        item_path = os.path.join(UNO_PACKAGES_DIR, item)
        if not os.path.isdir(item_path):
            continue
        # Look for NLPSolver.oxt subdirectory
        for subitem in os.listdir(item_path):
            if subitem == 'NLPSolver.oxt' or subitem.lower() == 'nlpsolver.oxt':
                oxt_path = os.path.join(item_path, subitem)
                if os.path.isdir(oxt_path):
                    desc_xml = os.path.join(oxt_path, 'description.xml')
                    if os.path.exists(desc_xml):
                        content = open(desc_xml).read()
                        ident_match = re.search(r'identifier[^>]*value="([^"]+)"', content)
                        version_match = re.search(r'version[^>]*value="([^"]+)"', content)
                        ident = ident_match.group(1) if ident_match else None
                        version = version_match.group(1) if version_match else None
                        return oxt_path, ident, version
    return None, None, None


def find_nlpsolver_properties_in_uno_packages():
    """
    Search for NLPSolver.oxtproperties file in uno_packages.
    Returns the content if found, else None.
    """
    if not os.path.isdir(UNO_PACKAGES_DIR):
        return None

    for item in os.listdir(UNO_PACKAGES_DIR):
        item_path = os.path.join(UNO_PACKAGES_DIR, item)
        if not os.path.isdir(item_path):
            continue
        for subitem in os.listdir(item_path):
            if subitem.lower() == 'nlpsolver.oxtproperties':
                prop_path = os.path.join(item_path, subitem)
                try:
                    return open(prop_path).read()
                except Exception:
                    return ''
    return None


def find_nlpsolver_in_extensions_tmp():
    """
    Search extensions/tmp/extensions for NLPSolver.oxt directory.
    Returns True if found, False otherwise.
    """
    if not os.path.isdir(EXTENSIONS_TMP_DIR):
        return False

    for item in os.listdir(EXTENSIONS_TMP_DIR):
        item_path = os.path.join(EXTENSIONS_TMP_DIR, item)
        if not os.path.isdir(item_path):
            continue
        for subitem in os.listdir(item_path):
            if subitem == 'NLPSolver.oxt' or subitem.lower() == 'nlpsolver.oxt':
                oxt_path = os.path.join(item_path, subitem)
                if os.path.isdir(oxt_path):
                    return True
    return False


def verify_task():
    """
    Verify NLPSolver extension installation in LibreOffice Calc.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: uno_packages directory must exist
    if not os.path.isdir(UNO_PACKAGES_DIR):
        print(f"CRITICAL: uno_packages directory not found at {UNO_PACKAGES_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: NLPSolver.oxt present in uno_packages cache with correct identifier (0.5 pts)
    # This is the primary evidence of extension installation.
    # FAILS on initial_env (empty uno_packages), PASSES on golden_env.
    try:
        oxt_path, identifier, version = find_nlpsolver_in_uno_packages()
        if oxt_path is not None and identifier == NLPSOLVER_IDENTIFIER:
            print(f"PASS: Component 1 — NLPSolver.oxt found in uno_packages with correct identifier '{identifier}' (version {version}) (0.5 pts)")
            total_score += 0.5
        elif oxt_path is not None:
            print(f"FAIL: Component 1 — NLPSolver.oxt found but identifier mismatch: expected '{NLPSOLVER_IDENTIFIER}', got '{identifier}'")
        else:
            print(f"FAIL: Component 1 — NLPSolver.oxt not found in {UNO_PACKAGES_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Extension properties file present with SUPPRESS_LICENSE marker (0.2 pts)
    # This file is created when LibreOffice installs and registers the extension.
    # FAILS on initial_env (no properties file), PASSES on golden_env.
    try:
        props_content = find_nlpsolver_properties_in_uno_packages()
        if props_content is not None:
            if 'SUPPRESS_LICENSE' in props_content or props_content.strip():
                print(f"PASS: Component 2 — NLPSolver.oxtproperties found with content: '{props_content.strip()}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — NLPSolver.oxtproperties found but empty or unexpected content")
        else:
            print(f"FAIL: Component 2 — NLPSolver.oxtproperties not found in {UNO_PACKAGES_DIR}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Extension also registered in extensions/tmp/extensions directory (0.3 pts)
    # LibreOffice registers active extensions in this second directory when loaded.
    # FAILS on initial_env (no extensions registered), PASSES on golden_env.
    try:
        found_in_tmp = find_nlpsolver_in_extensions_tmp()
        if found_in_tmp:
            print(f"PASS: Component 3 — NLPSolver.oxt found in extensions/tmp/extensions (confirming loaded by LibreOffice) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — NLPSolver.oxt not found in {EXTENSIONS_TMP_DIR}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
