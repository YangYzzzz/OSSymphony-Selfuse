"""
Reward Script: Add trusted macro file location in LibreOffice
Task ID: calc_mcp_021
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): SecureURL entry exists in registrymodifications.xcu
  Component 2 (0.3): The path is exactly 'file:///home/user/trusted_macros'
  Component 3 (0.2): The trusted_macros directory exists at /home/user/trusted_macros
                      AND the SecureURL references it (compound check)
"""

import os
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'calc_mcp_021'
CONFIG_PATH = os.path.join(
    WORKDIR, '.config', 'libreoffice', '4', 'user', 'registrymodifications.xcu'
)
EXPECTED_PATH = 'file:///home/user/trusted_macros'
EXPECTED_OOR_PATH = '/org.openoffice.Office.Common/Security/Scripting'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task():
    """
    Verify that '/home/user/trusted_macros' has been added as a trusted
    file location in LibreOffice Macro Security settings.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: registrymodifications.xcu must exist
    if not os.path.exists(CONFIG_PATH):
        print(f"CRITICAL: Config file not found: {CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the XCU file to find SecureURL entries
    # The file is XML with oor: namespace items
    secure_urls = []
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        # The XCU file uses namespaces. Parse carefully.
        # We look for items with oor:path containing Security/Scripting
        # and prop oor:name="SecureURL"
        # The structure is:
        # <item oor:path="/org.openoffice.Office.Common/Security/Scripting">
        #   <prop oor:name="SecureURL" ...>
        #     <value><it>file:///home/user/trusted_macros</it></value>
        #   </prop>
        # </item>

        # Since the XML uses oor: namespace prefixes, use string parsing
        # to be robust against namespace declaration variations
        import re

        # Find all items related to Security/Scripting SecureURL
        # Pattern: item with path containing Security/Scripting and name SecureURL
        # Then extract <it>...</it> values inside
        secure_url_found = False
        # Look for the SecureURL property block
        pattern = r'<[^>]*path="[^"]*Security/Scripting"[^>]*>.*?<[^>]*name="SecureURL"[^>]*>.*?<value>(.*?)</value>'
        matches = re.findall(pattern, content, re.DOTALL)

        for match in matches:
            secure_url_found = True
            # Extract individual <it>...</it> entries
            it_pattern = r'<it>(.*?)</it>'
            urls = re.findall(it_pattern, match)
            secure_urls.extend(urls)

        if not secure_url_found:
            # Also try the oor: prefixed variant
            pattern2 = r'<oor:item[^>]*path="[^"]*Security/Scripting"[^>]*>.*?<oor:prop[^>]*name="SecureURL"[^>]*>.*?<value>(.*?)</value>'
            matches2 = re.findall(pattern2, content, re.DOTALL)
            for match in matches2:
                secure_url_found = True
                it_pattern = r'<it>(.*?)</it>'
                urls = re.findall(it_pattern, match)
                secure_urls.extend(urls)

        print(f"INFO: Found SecureURL entries: {secure_urls}")
        print(f"INFO: SecureURL block found: {secure_url_found}")

    except Exception as e:
        print(f"ERROR: Failed to parse config file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: SecureURL entry exists with at least one trusted path (0.5 points)
    # This checks that ANY SecureURL configuration was added.
    # On initial_env, there is no SecureURL entry at all, so this FAILS.
    try:
        if len(secure_urls) > 0:
            print(f"PASS: Component 1 - SecureURL has {len(secure_urls)} trusted path(s) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - No trusted paths found in SecureURL")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: The exact path 'file:///home/user/trusted_macros' is present (0.3 points)
    # Verifies the specific path from the task instruction.
    try:
        if EXPECTED_PATH in secure_urls:
            print(f"PASS: Component 2 - Exact path '{EXPECTED_PATH}' found in SecureURL (0.3 pts)")
            total_score += 0.3
        else:
            # Also check without trailing slash or with variations
            found_match = False
            for url in secure_urls:
                normalized = url.rstrip('/')
                if normalized == EXPECTED_PATH.rstrip('/'):
                    found_match = True
                    break
            if found_match:
                print(f"PASS: Component 2 - Path '{EXPECTED_PATH}' found (with normalization) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - Expected '{EXPECTED_PATH}' not in {secure_urls}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: The trusted_macros directory exists AND is referenced in SecureURL (0.2 points)
    # Compound check: both the directory and the config entry must be correct.
    # On initial_env, even though the directory may exist, the SecureURL does NOT reference it.
    try:
        dir_exists = os.path.isdir('/home/user/trusted_macros')
        path_in_config = EXPECTED_PATH in secure_urls or any(
            url.rstrip('/') == EXPECTED_PATH.rstrip('/') for url in secure_urls
        )
        if dir_exists and path_in_config:
            print(f"PASS: Component 3 - Directory exists AND referenced in SecureURL (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 - dir_exists={dir_exists}, path_in_config={path_in_config}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_calc")
verify_task()
