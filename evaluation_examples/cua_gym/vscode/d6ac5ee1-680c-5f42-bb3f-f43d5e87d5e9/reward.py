"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m pairing with teammates in Madrid and need Visual Studio Code’s interface to show everything in Spanish—how do I change the display language?
Generated: 2025-09-11 17:25:23
Status: success
Model: azure-o3
Total Steps: 7
"""

# Reward script: Verify Visual Studio Code interface set to Spanish
# Author: Automated Reward Script Generator
# Description: This script awards up to 1.0 points for setting
# VS Code’s UI language to Spanish.  It checks two independent, real
# indicators:
#   1. A locale override configured to an "es*" value (0.5 pts)
#   2. The Spanish language-pack extension installed (0.5 pts)
# A perfect score (1.0) is given only when BOTH are true.

import json
import os
import re
from pathlib import Path
from typing import List, Tuple

# -------------------------------------------------------------
# Helper – read JSON/JSONC (handles // and /* */ comments)
# -------------------------------------------------------------

def load_jsonc(path: Path):
    """Load a JSON/JSONC file (strips // and /* */ comments)."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    # Remove /* … */ block comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    # Remove // comments
    text = re.sub(r"//.*", "", text)
    # Remove trailing commas that break json.loads
    text = re.sub(r",\s*(\]|\})", r"\1", text)
    return json.loads(text)

# -------------------------------------------------------------
# Check 1 – locale override   (0.5 points)
# -------------------------------------------------------------

def scan_locale_files() -> Tuple[bool, bool]:
    """Return (spanish_locale_found, any_locale_found)."""
    home = Path.home()
    # Common VS Code variants
    variants = [
        "Code",            # Stable
        "Code - OSS",      # OSS build
        "Code - Insiders", # Insiders
        "VSCodium",        # VSCodium
    ]
    candidate_paths: List[Path] = [home/".vscode"/"argv.json"]
    for variant in variants:
        candidate_paths.append(home/".config"/variant/"User"/"locale.json")

    spanish = False
    any_locale = False

    for lf in candidate_paths:
        if not lf.exists():
            continue
        try:
            data = load_jsonc(lf)
        except Exception as e:
            print(f"  ✗ Could not parse {lf}: {e}")
            continue
        if isinstance(data, dict):
            locale_val = data.get("locale")
            if locale_val:
                any_locale = True
                print(f"  • locale='{locale_val}' found in {lf}")
                if str(locale_val).lower().startswith("es"):
                    spanish = True
    return spanish, any_locale

# -------------------------------------------------------------
# Check 2 – language-pack extension   (0.5 points)
# -------------------------------------------------------------

def scan_language_packs() -> Tuple[bool, List[Path]]:
    home = Path.home()
    ext_roots = [
        home/".vscode"/"extensions",              # Local extensions
        home/".vscode-server"/"extensions",       # Remote (SSH / WSL)
        home/".vscode-server-insiders"/"extensions",
        home/".vscode-test"/"extensions",          # Test harness
    ]
    hits: List[Path] = []
    for root in ext_roots:
        if not root.exists():
            continue
        for d in root.iterdir():
            if not d.is_dir():
                continue
            name = d.name.lower()
            if (
                "vscode-language-pack-es" in name or
                ("language-pack" in name and ("-es" in name or ".es" in name))
            ):
                hits.append(d)
    return bool(hits), hits

# -------------------------------------------------------------
# Main verification logic
# -------------------------------------------------------------

def verify_task() -> float:
    print("=== VS Code Spanish Display Language Verification ===")
    total_score = 0.0

    # -------- Locale check --------
    spanish_locale, any_locale = scan_locale_files()
    if spanish_locale:
        print("✓ Spanish locale configured (0.5 pts)")
        total_score += 0.5
    else:
        if any_locale:
            print("✗ Locale override present but not Spanish (0 pts)")
        else:
            print("✗ No locale override found (0 pts)")

    # -------- Extension check --------
    pack_found, pack_paths = scan_language_packs()
    if pack_found:
        for p in pack_paths:
            print(f"✓ Spanish language pack installed: {p.name} (0.5 pts)")
        total_score += 0.5
    else:
        print("✗ Spanish language pack extension not found (0 pts)")

    # Cap score at 1.0
    total_score = min(total_score, 1.0)

    print(f"\nFinal Score: {total_score}/1.0")
    print(f"REWARD: {total_score}")
    return total_score

# Execute when run as a script
if __name__ == "__main__":
    verify_task()

