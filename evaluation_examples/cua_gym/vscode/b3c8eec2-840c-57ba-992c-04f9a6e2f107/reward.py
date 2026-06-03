"""
FINAL REWARD SCRIPT - SUCCESS
Task: My new teammate only speaks Russian, so I need the entire VS Code interface to show up in Russian—how can I switch the display language accordingly?
Generated: 2025-09-11 17:05:44
Status: success
Model: azure-o3
Total Steps: 9
"""

import pathlib
import json
import subprocess
import glob


def verify_vs_code_russian_interface():
    """Reward script that checks whether VS Code’s interface has been switched to Russian.

    Scoring (progressive):
        • 0.5 pts – locale.json exists in a standard VS Code location and sets "locale" to "ru" (or starts with ru)
        • 0.5 pts – Russian language-pack extension (ms-ceintl.vscode-language-pack-ru) is installed
        • 1.0  pts – both conditions satisfied
    """

    total_score = 0.0
    max_score = 1.0

    home = pathlib.Path.home()

    print("------------ VS Code Russian Interface Verification ------------")

    # -------------------------------------------------------------
    # Part 1  locale.json must set locale → "ru"
    # -------------------------------------------------------------
    locale_paths = [
        home / ".config/Code/User/locale.json",          # Standard VS Code
        home / ".config/Code - OSS/User/locale.json",    # Code-OSS builds
        home / ".config/VSCodium/User/locale.json",      # VSCodium
        home / ".vscode/locale.json",                    # Fallback (rare)
    ]

    locale_is_ru = False
    for path in locale_paths:
        if path.exists():
            try:
                with path.open(encoding="utf-8") as fh:
                    data = json.load(fh)
                locale_value = str(data.get("locale", "")).lower()
                print(f"Found locale.json at {path} with locale='{locale_value}'")
                if locale_value.startswith("ru"):
                    locale_is_ru = True
                else:
                    print(" locale.json does not set Russian locale.")
            except Exception as e:
                print(f" Error reading/parsing {path}: {e}")
            break  # stop after first present locale.json

    if locale_is_ru:
        print("✓ locale.json correctly sets VS Code UI to Russian (0.5 pts)")
        total_score += 0.5
    else:
        print("✗ locale.json missing or not set to Russian (0 pts)")

    # -------------------------------------------------------------
    # Part 2  Russian language-pack extension must be installed
    # -------------------------------------------------------------
    ext_id = "ms-ceintl.vscode-language-pack-ru"
    ext_installed = False

    # Method A – use CLI if available
    for cli in ("code", "codium", "code-oss"):
        try:
            res = subprocess.run([cli, "--list-extensions"], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True, check=False)
            if res.returncode == 0:
                listed = [ln.strip().lower() for ln in res.stdout.splitlines() if ln.strip()]
                if ext_id in listed:
                    print(f"✓ Extension '{ext_id}' found via '{cli} --list-extensions'")
                    ext_installed = True
                    break
                else:
                    print(f" Extension not listed via '{cli}'.")
        except FileNotFoundError:
            # CLI variant not installed – ignore
            continue
        except Exception as e:
            print(f" Error executing '{cli}': {e}")

    # Method B – fall back to filesystem inspection
    if not ext_installed:
        ext_dirs = [
            home / ".vscode/extensions",
            home / ".vscode-server/extensions",
            home / ".vscodium/extensions",
            home / ".vscode-oss/extensions",
        ]
        for base in ext_dirs:
            if base.exists():
                pattern = str(base / f"{ext_id}*")
                matches = glob.glob(pattern)
                if matches:
                    print(f"✓ Extension directory found: {matches[0]}")
                    ext_installed = True
                    break
                else:
                    print(f" No matching extension directories in {base}")
            else:
                print(f" Directory {base} does not exist (skipped)")

    if ext_installed:
        print("✓ Russian language-pack extension installed (0.5 pts)")
        total_score += 0.5
    else:
        print("✗ Russian language-pack extension NOT installed (0 pts)")

    # -------------------------------------------------------------
    final_score = min(total_score, max_score)
    print("--------------------------------------------------------------")
    print(f"TOTAL SCORE: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_vs_code_russian_interface()
