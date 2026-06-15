"""
FINAL REWARD SCRIPT - SUCCESS
Task: VS Code keeps flagging vendor-prefixed rules like `-webkit-box` as warnings in my legacy stylesheet; how can I turn off these CSS vendor prefix warnings?
Generated: 2025-09-12 00:09:52
Status: success
Model: azure-o3
Total Steps: 13
"""

import json
import os
import re
from pathlib import Path

"""
Reward script for the task:
"VS Code keeps flagging vendor-prefixed rules like `-webkit-box` as warnings in my legacy
stylesheet; how can I turn off these CSS vendor prefix warnings?"

Verification logic
------------------
1.  Look for any VS Code *settings.json* that could control linting either on user level
    (~/.config/Code/User/settings.json, etc.) or at a workspace level (any
    */.vscode/settings.json* under $HOME).
2.  Parse every discovered *settings.json* – tolerant of `//` comments and trailing
    commas – to obtain a Python dict.  If full JSON parsing fails, fall back to a
    regex line-by-line scan so we never miss a valid key.
3.  Keys of interest:
        css.lint.vendorPrefix   (main requirement – 0-1.0 pts)
        scss.lint.vendorPrefix  (optional – +0.5 pts)
        less.lint.vendorPrefix  (optional – +0.5 pts)
    A key counts as *disabled* when its value (case-insensitive) is any of:
        "ignore", "none", "off", "disable", "disabled"  or the boolean false.
4.  Scoring
        • If css.lint.vendorPrefix is disabled → immediate 1.0 (full success)
        • Otherwise award 0.5 for each of the SCSS / LESS keys, capping at 1.0.
5.  Output
        – Debug lines showing what was inspected/found
        – Final line strictly formatted:  REWARD: X.X
"""

# ---------- Utility helpers -------------------------------------------------

def _strip_json_comments(text: str) -> str:
    """Remove // comments and trailing commas so JSON becomes valid."""
    text = re.sub(r"//.*", "", text)                     # strip line comments
    text = re.sub(r",\s*([}\]])", r"\1", text)          # strip trailing commas
    return text


def _load_json_allow_comments(file_path: Path):
    """Load JSON allowing comments & trailing commas; return None on failure."""
    try:
        raw = file_path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"! Cannot read {file_path}: {exc}")
        return None

    for payload in (raw, _strip_json_comments(raw)):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            continue
    return None  # still not valid JSON


def _value_disables_lint(value):
    """Return True if the given JSON value means the rule is disabled."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value is False
    if isinstance(value, str):
        return value.lower() in {"ignore", "none", "off", "disable", "disabled"}
    return False

# ---------- Main verification ----------------------------------------------

def verify_vendor_prefix_settings():
    print("=== Verifying vendor-prefix lint settings ===")

    home = Path.home()

    # Known user-level settings locations
    candidates = [
        home / ".config/Code/User/settings.json",
        home / ".config/Code - Insiders/User/settings.json",
        home / ".vscode/settings.json",
    ]

    # Workspace-level *.vscode/settings.json* (depth<=6 for performance)
    for root, _dirs, files in os.walk(home):
        if "settings.json" in files and ".vscode" in root.split(os.sep):
            rel_depth = len(Path(root).relative_to(home).parts)
            if rel_depth <= 6:
                candidates.append(Path(root) / "settings.json")

    key_to_lang = {
        "css.lint.vendorPrefix": "css",
        "scss.lint.vendorPrefix": "scss",
        "less.lint.vendorPrefix": "less",
    }

    disabled_langs = set()
    inspected_files = 0

    for settings_file in candidates:
        if not settings_file.exists():
            continue
        inspected_files += 1

        data = _load_json_allow_comments(settings_file)

        if data is not None:  # parsed successfully
            for key, lang in key_to_lang.items():
                if key in data and _value_disables_lint(data[key]):
                    disabled_langs.add(lang)
        else:  # fallback regex scan so we never miss the key
            try:
                with settings_file.open("r", encoding="utf-8", errors="ignore") as fh:
                    for line in fh:
                        if line.lstrip().startswith("//"):
                            continue  # ignore comment lines
                        for key, lang in key_to_lang.items():
                            pattern = rf"\s*\"{re.escape(key)}\"\s*:\s*\"?(ignore|none|off|disable|disabled)\"?"
                            if re.search(pattern, line, flags=re.I):
                                disabled_langs.add(lang)
            except Exception as exc:
                print(f"! Could not scan {settings_file}: {exc}")

    print(f"Inspected {inspected_files} settings.json file(s).")

    # ---------------- Scoring ----------------
    score = 0.0
    if "css" in disabled_langs:
        score = 1.0
    else:
        if "scss" in disabled_langs:
            score += 0.5
        if "less" in disabled_langs:
            score += 0.5
        score = min(score, 1.0)

    # Feedback for each key
    for key, lang in [
        ("css.lint.vendorPrefix", "css"),
        ("scss.lint.vendorPrefix", "scss"),
        ("less.lint.vendorPrefix", "less"),
    ]:
        if lang in disabled_langs:
            print(f"✓ {key} disabled")
        else:
            print(f"✗ {key} not disabled")

    print(f"REWARD: {score}")
    return score

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    verify_vendor_prefix_settings()
