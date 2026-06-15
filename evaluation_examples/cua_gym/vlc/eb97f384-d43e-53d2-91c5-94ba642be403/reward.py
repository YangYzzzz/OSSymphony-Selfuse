"""
FINAL REWARD SCRIPT - SUCCESS
Task: Set extensions database to /home/user/.config/vlc/extensions.db.
Generated: 2025-09-13 08:26:05
Status: success
Model: azure-o3
Total Steps: 3
"""

import os

def verify_extensions_database(expected_path:str) -> float:
    """Verify that the key 'extensions-database' in VLC's vlcrc file is set to
    exactly the expected path.  
    Scoring rules:
        • 1.0 – key exists and value matches expected_path exactly (success)  
        • 0.3 – key exists but value is different (partial)  
        • 0.0 – key missing or unreadable file (failure)
    The function prints diagnostic output for each step and finally prints the
    score in the required format:  "REWARD: X.X".
    """

    vlcrc_path = os.path.expanduser("~/.config/vlc/vlcrc")
    print(f"Checking vlcrc at: {vlcrc_path}")

    # ---------- Pre-check ----------
    if not os.path.exists(vlcrc_path):
        print("✗ vlcrc file does not exist – cannot verify setting")
        reward = 0.0
        print(f"REWARD: {reward}")
        return reward

    correct_value = False
    wrong_value_found = False

    # ---------- Parse vlcrc ----------
    try:
        with open(vlcrc_path, "r", encoding="utf-8", errors="ignore") as fh:
            for raw_line in fh:
                line = raw_line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                # Look specifically for the key of interest
                if line.startswith('extensions-database'):
                    key, _, value = line.partition('=')
                    # Remove any inline comment that might trail after value
                    value_clean = value.split('#')[0].strip()

                    if value_clean == expected_path:
                        correct_value = True
                        print("✓ extensions-database is correctly set")
                    else:
                        wrong_value_found = True
                        print(f"✗ extensions-database found, but value is '{value_clean}', expected '{expected_path}'")
                    # No need to continue scanning once we processed the key
                    break
    except Exception as exc:
        print(f"✗ Error reading vlcrc: {exc}")
        reward = 0.0
        print(f"REWARD: {reward}")
        return reward

    # ---------- Scoring ----------
    if correct_value:
        reward = 1.0
    elif wrong_value_found:
        reward = 0.3
    else:
        print("✗ extensions-database key not found in vlcrc")
        reward = 0.0

    print(f"REWARD: {reward}")
    return reward

# -------------------
# Main execution path
# -------------------
if __name__ == "__main__":
    # Expected absolute path for the extensions database as per task
    EXPECTED_PATH = "/home/user/.config/vlc/extensions.db"
    verify_extensions_database(EXPECTED_PATH)
