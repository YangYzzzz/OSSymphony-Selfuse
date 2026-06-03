"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m about to start a new machine-learning experiment—could you help me create a fresh VS Code workspace in /home/user/ml-projects and set it up so I can visually inspect NumPy arrays in the Data Viewer?
Generated: 2025-09-12 00:06:39
Status: success
Model: azure-o3
Total Steps: 11
"""

import json
from pathlib import Path

# ===== VERIFICATION PARAMETERS =====
BASE_DIR = Path("/home/user/ml-projects")
REQUIRED_DV_SETTINGS = {
    "python.dataScience.showVariableTypes": True,
    "python.dataScience.showTableIndexColumn": True,
}
REQUIRED_EXT_RECS = {
    "ms-python.python",
    "ms-toolsai.jupyter",
}

# ===== HELPER FUNCTIONS =====

def load_json(path: Path):
    """Safely load JSON content from a file, returning None on failure."""
    try:
        return json.loads(path.read_text())
    except Exception as e:
        print(f"   ✗ Failed to parse JSON {path}: {e}")
        return None

# ===== VERIFICATION SUB-TASKS =====

def verify_vscode_directory(base_dir: Path) -> float:
    """Check that the .vscode directory with custom files exists (0.2 pts)."""
    vscode_dir = base_dir / ".vscode"
    if not vscode_dir.exists() or not vscode_dir.is_dir():
        print("✗ .vscode directory not found")
        return 0.0

    customization_files = list(vscode_dir.glob("*.json"))
    if customization_files:
        print(f"✓ .vscode directory present with {len(customization_files)} customization file(s) (0.2)")
        return 0.2
    print("✗ .vscode directory present but contains no JSON customization files")
    return 0.0

def verify_data_viewer_settings(base_dir: Path) -> float:
    """Ensure Data Viewer related settings are correctly set (0.4 pts total)."""
    settings_path = base_dir / ".vscode" / "settings.json"
    if not settings_path.exists():
        print("✗ settings.json not found")
        return 0.0

    data = load_json(settings_path)
    if data is None:
        return 0.0

    score = 0.0
    per_key = 0.4 / len(REQUIRED_DV_SETTINGS)
    for key, expected in REQUIRED_DV_SETTINGS.items():
        if data.get(key) == expected:
            print(f"✓ Setting {key} correctly set to {expected} (+{per_key:.2f})")
            score += per_key
        else:
            print(f"✗ Setting {key} missing or incorrect (expected {expected})")
    return score

def verify_extension_recommendations(base_dir: Path) -> float:
    """Check extension recommendations for Python & Jupyter (0.4 pts total)."""
    ext_path = base_dir / ".vscode" / "extensions.json"
    if not ext_path.exists():
        print("✗ extensions.json not found")
        return 0.0

    data = load_json(ext_path)
    if data is None:
        return 0.0

    recs = set(data.get("recommendations", []) if isinstance(data, dict) else [])
    score = 0.0
    per_ext = 0.4 / len(REQUIRED_EXT_RECS)
    for ext in REQUIRED_EXT_RECS:
        if ext in recs:
            print(f"✓ Extension recommendation present: {ext} (+{per_ext:.2f})")
            score += per_ext
        else:
            print(f"✗ Missing extension recommendation: {ext}")
    return score

# ===== MAIN VERIFICATION FUNCTION =====

def verify_task(base_dir: Path = BASE_DIR) -> float:
    print(f"Verifying VS Code ML workspace at {base_dir}\n")

    total_score = 0.0
    total_score += verify_vscode_directory(base_dir)
    total_score += verify_data_viewer_settings(base_dir)
    total_score += verify_extension_recommendations(base_dir)

    # Clamp to [0,1] and round for cleanliness
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nREWARD: {final_score}")
    return final_score

# ===== EXECUTE WHEN RUN AS SCRIPT =====
if __name__ == "__main__":
    verify_task()
