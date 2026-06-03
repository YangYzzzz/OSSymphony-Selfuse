"""
FINAL REWARD SCRIPT - SUCCESS
Task: When I’m updating our Markdown documentation, I’d like a visual guide to keep each line under control—could you help me add a 60-character ruler in VS Code?
Generated: 2025-09-11 17:09:06
Status: success
Model: azure-o3
Total Steps: 10
"""

import json
import pathlib
import re
import os


def _strip_jsonc(text: str) -> str:
    """Remove // line comments, /* block comments */ and dangling commas so the
    file can be parsed as proper JSON. VS Code settings.json often contains such
    comments, so we must sanitise before json.loads()."""

    # Remove block comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    # Remove line comments
    text = re.sub(r"//.*", "", text)
    # Remove dangling commas (a comma followed only by whitespace/new-line and a
    # closing brace/bracket)
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return text


def _load_settings(path: pathlib.Path):
    """Load a VS Code-style settings.json file (which may contain comments)."""
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(_strip_jsonc(raw))
        return data
    except Exception as exc:
        print(f"    ✗ Failed to parse {path}: {exc}")
        return None


def _collect_columns(rulers):
    """Normalise the various ruler specifications to integer columns.

    VS Code allows e.g. 80 or { "column": 80 }."""
    columns = []
    if isinstance(rulers, list):
        for item in rulers:
            if isinstance(item, (int, float)):
                columns.append(int(item))
            elif isinstance(item, dict):
                col = item.get("column")
                if isinstance(col, (int, float)):
                    columns.append(int(col))
    return columns


def _extract_rulers(settings: dict):
    """Return a tuple (global_columns, markdown_columns)."""
    global_cols, md_cols = [], []

    if not isinstance(settings, dict):
        return global_cols, md_cols

    # Global rulers
    if "editor.rulers" in settings:
        global_cols = _collect_columns(settings["editor.rulers"])

    # Language-specific overrides live under keys like "[markdown]"
    for key, subsection in settings.items():
        if isinstance(key, str) and key.strip().lower() == "[markdown]" and isinstance(subsection, dict):
            if "editor.rulers" in subsection:
                md_cols = _collect_columns(subsection["editor.rulers"])

    return global_cols, md_cols


def verify_task():
    """Verify the presence of a 60-character ruler for Markdown in VS Code."""

    print("================ VS Code 60-Character Ruler Verification ================")

    home = pathlib.Path.home()

    # Most common locations for settings.json on Linux (VS Code / OSS / Insiders / portable)
    default_paths = [
        home / ".config/Code/User/settings.json",
        home / ".config/Code - OSS/User/settings.json",
        home / ".config/Code - Insiders/User/settings.json",
        home / ".vscode/settings.json",
    ]

    # Dynamically discover any other settings.json inside a *Code* folder
    dynamic_paths = [p for p in home.rglob("settings.json") if "Code" in str(p)]

    # Deduplicate while preserving order
    candidate_paths = list(dict.fromkeys(default_paths + dynamic_paths))

    inspected_files = 0
    has_60_markdown = False  # 60-column rule explicitly for Markdown
    has_60_global = False    # 60-column rule applies globally (covers Markdown)
    has_near_60 = False      # ruler very close to 60 (55-65) – partial credit

    for path in candidate_paths:
        if not path.exists():
            continue

        inspected_files += 1
        print(f"\n→ Inspecting: {path}")

        settings = _load_settings(path)
        if settings is None:
            continue

        global_cols, md_cols = _extract_rulers(settings)
        print(f"    Global rulers   : {global_cols}")
        print(f"    Markdown rulers : {md_cols}")

        if 60 in md_cols:
            has_60_markdown = True
        if 60 in global_cols:
            has_60_global = True

        combined = global_cols + md_cols
        if any(55 <= c <= 65 for c in combined):
            has_near_60 = True

    # -------------------- Scoring logic --------------------
    score = 0.0

    if has_60_markdown or has_60_global:
        # Exact 60-column ruler found (either Markdown-specific or global)
        score = 1.0
        if has_60_markdown:
            print("✓ 60-character ruler found specifically for Markdown.")
        else:
            print("✓ 60-character global ruler found (applies to Markdown as well).")
    elif has_near_60:
        # Close but not exact → partial credit
        score = 0.5
        print("△ Ruler near 60 characters detected (within ±5 columns), but not exactly 60.")
    else:
        print("✗ No 60-character ruler (or near-60) found in VS Code settings.")

    if inspected_files == 0:
        # Could not locate any settings.json – cannot verify task
        print("✗ No VS Code settings.json files were found – verification inconclusive.")
        score = 0.0

    print(f"\nREWARD: {score}")
    return score


if __name__ == "__main__":
    verify_task()
