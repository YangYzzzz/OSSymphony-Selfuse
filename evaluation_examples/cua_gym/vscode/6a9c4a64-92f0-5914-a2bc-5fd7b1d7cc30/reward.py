"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m giving my editor a facelift—how can I set /home/user/workspace/assets/bg.jpg as the background image in VS Code?
Generated: 2025-09-11 23:20:30
Status: success
Model: azure-o3
Total Steps: 14
"""

import json
import os
import pathlib
import re
from typing import List, Union

"""
Reward Verification Script  
Task: Verify that VS Code has been configured to use
       /home/user/workspace/assets/bg.jpg as the editor background.

Scoring (progressive):
  • 0.3 pts  – background image file exists
  • 0.4 pts  – that image path (absolute **or** relative) is referenced in any
               VS Code settings.json (user or workspace)
  • 0.3 pts  – background extension is enabled
               ("background.enabled": true  OR  non-empty
                "background.customImages" array)

Returns exactly 1.0 when the configuration is perfect and proportionally less
for partial completion.  Diagnostic messages are printed for transparency.
The last line is always:  REWARD: X.X
"""

BG_IMAGE_ABS = "/home/user/workspace/assets/bg.jpg"        # canonical path
BG_IMAGE_TAIL = "assets/bg.jpg"                              # suffix for rel. refs
MAX_SCORE = 1.0

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def gather_settings_files() -> List[pathlib.Path]:
    """Collect plausible VS Code settings.json files (user + workspace)."""
    files: List[pathlib.Path] = []

    # User-level settings (Linux path)
    user_settings = pathlib.Path.home() / ".config/Code/User/settings.json"
    if user_settings.exists():
        files.append(user_settings)

    # Workspace-level settings – any  .vscode/settings.json  under workspace
    workspace_root = pathlib.Path("/home/user/workspace")
    if workspace_root.exists():
        for p in workspace_root.rglob("settings.json"):
            if p.parent.name == ".vscode":
                files.append(p)

    return files


def read_json_or_text(p: pathlib.Path) -> Union[dict, str]:
    """Load a settings.json file; return dict if JSON, else raw text."""
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return p.read_text(errors="ignore")


def recursive_iter(obj):
    """Recursively yield every (key, value) pair in nested dict/list structures."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k, v
            yield from recursive_iter(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from recursive_iter(item)


def contains_image_path(value: str) -> bool:
    """True if *value* references our background image (abs/rel/var forms)."""
    if not isinstance(value, str):
        return False
    return (
        BG_IMAGE_ABS in value or
        BG_IMAGE_TAIL in value or
        re.search(r"assets[/\\]bg\.jpg", value) is not None
    )

# ---------------------------------------------------------------------------
# Main verification logic
# ---------------------------------------------------------------------------

def verify_background_configuration() -> float:
    total_score = 0.0

    # 1) Background image file existence
    if pathlib.Path(BG_IMAGE_ABS).is_file():
        print(f"✓ Background image exists at {BG_IMAGE_ABS} (0.3 pts)")
        total_score += 0.3
    else:
        print(f"✗ Background image NOT found at {BG_IMAGE_ABS}")

    # 2) Inspect VS Code settings files
    settings_files = gather_settings_files()
    print(f"Inspecting {len(settings_files)} settings.json file(s)…")

    image_referenced = False
    background_enabled = False

    for sfile in settings_files:
        data = read_json_or_text(sfile)

        if isinstance(data, dict):
            # direct high-level keys
            if data.get("background.enabled", False):
                background_enabled = True
            imgs = data.get("background.customImages")
            if isinstance(imgs, list) and imgs:
                background_enabled = True
                if any(contains_image_path(v) for v in imgs):
                    image_referenced = True

            # deep recursive search (catch nested or unusual placements)
            for k, v in recursive_iter(data):
                if k == "background.enabled" and v is True:
                    background_enabled = True
                if isinstance(k, str) and contains_image_path(k):
                    image_referenced = True
                if isinstance(v, str) and contains_image_path(v):
                    image_referenced = True
        else:  # raw text fallback
            text = data
            if re.search(r'"background\\.enabled"\s*:\s*true', text):
                background_enabled = True
            if contains_image_path(text):
                image_referenced = True

    # 2a) Image path referenced
    if image_referenced:
        print("✓ Image path referenced in VS Code settings (0.4 pts)")
        total_score += 0.4
    else:
        print("✗ Image path NOT referenced in any settings.json file")

    # 2b) Background extension enabled
    if background_enabled:
        print("✓ Background extension is enabled (0.3 pts)")
        total_score += 0.3
    else:
        print('✗ Background extension NOT enabled (missing "background.enabled": true)')

    # Clamp & report
    total_score = min(total_score, MAX_SCORE)
    print(f"Total score: {total_score}/{MAX_SCORE}")
    print(f"REWARD: {total_score}")
    return total_score


if __name__ == "__main__":
    verify_background_configuration()

