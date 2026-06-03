"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m trying to track down a stubborn bug in my Rust project, and a teammate handed me a custom VS Code add-on to help; how do I install the local extension file that’s sitting at /home/user/temp/debug-tool.vsix?
Generated: 2025-09-11 13:20:17
Status: success
Model: azure-o3
Total Steps: 12
"""

import os
import json
import zipfile
from pathlib import Path
from typing import Dict, Optional, List

# Path where the teammate placed the local VSIX file (given in task description)
VSIX_PATH = Path('/home/user/temp/debug-tool.vsix')

# --------------- Helper Functions ---------------

def parse_vsix_manifest(vsix_path: Path) -> Optional[Dict[str, str]]:
    """Extracts & returns {publisher, name, version} from a VSIX archive.
    Returns None if the file is missing or the manifest is unreadable."""
    if not vsix_path.is_file():
        return None
    try:
        with zipfile.ZipFile(vsix_path, 'r') as zf:
            # Find *package.json* inside the archive (usually extension/package.json)
            candidates = [n for n in zf.namelist() if n.lower().endswith('package.json')]
            if not candidates:
                return None
            # Use the shortest found path (most likely the real manifest)
            pkg_path = sorted(candidates, key=len)[0]
            data = json.loads(zf.read(pkg_path).decode('utf-8', errors='replace'))
        return {
            'publisher': data.get('publisher'),
            'name': data.get('name'),
            'version': data.get('version')
        }
    except Exception:
        # Any problem reading/parsing = manifest unavailable
        return None

def collect_installed_extensions() -> List[Dict[str, str]]:
    """Collect all installed VS Code extensions in common locations.
    Returns a list of {publisher, name, version, path}."""
    home = Path.home()
    extension_roots = [
        home / '.vscode' / 'extensions',                # Desktop VS Code
        home / '.vscode-server' / 'extensions',         # VS Code SSH/Server
        home / '.vscode-server-insiders' / 'extensions',
        home / '.vscode-test' / 'extensions',
        home / '.vscode-oss' / 'extensions',
        home / '.cursor-server' / 'extensions'          # Cursor (browser-based VS Code)
    ]

    installed: List[Dict[str, str]] = []
    for root in extension_roots:
        if not root.is_dir():
            continue
        for ext_dir in root.iterdir():
            if not ext_dir.is_dir():
                continue
            pkg_file = ext_dir / 'package.json'
            if not pkg_file.is_file():
                continue
            try:
                data = json.loads(pkg_file.read_text(encoding='utf-8', errors='replace'))
                installed.append({
                    'publisher': data.get('publisher'),
                    'name': data.get('name'),
                    'version': data.get('version'),
                    'path': str(ext_dir)
                })
            except Exception:
                # Ignore unreadable or malformed package.json files
                continue
    return installed

# --------------- Verification Logic ---------------

def verify_task(vsix_path: Path = VSIX_PATH) -> float:
    print("--- Verifying local VS Code extension installation ---")
    max_score = 1.0
    score = 0.0

    # Requirement 1: The VSIX file is present (0.3 pts)
    if vsix_path.is_file():
        score += 0.3
        print(f"✓ VSIX file found at {vsix_path} (+0.3)")
    else:
        print(f"✗ VSIX file not found at {vsix_path} (0 pts)")

    # Requirement 2: Successfully parse the VSIX manifest (0.1 pts)
    manifest = parse_vsix_manifest(vsix_path)
    if manifest and all(manifest.values()):
        score += 0.1
        print(f"✓ Parsed VSIX manifest: {manifest} (+0.1)")
    else:
        if vsix_path.is_file():
            print("✗ Could not parse VSIX manifest (0 pts)")
        manifest = None  # Ensure later logic knows manifest is unavailable

    # Requirement 3: Extension is installed (0.4 pts)
    installed_exts = collect_installed_extensions()
    print(f"Found {len(installed_exts)} installed extension(s) to inspect")

    def is_match(ext: Dict[str, str]) -> bool:
        if manifest:
            return ext['publisher'] == manifest['publisher'] and ext['name'] == manifest['name']
        # Fallback if manifest couldn’t be read: match on canonical name
        return ext['name'] and ext['name'].lower() == 'debug-tool'

    match_ext = next((ext for ext in installed_exts if is_match(ext)), None)
    if match_ext:
        score += 0.4
        print(f"✓ Matching extension installed at {match_ext['path']} (+0.4)")
    else:
        print("✗ Matching extension not found among installed extensions (0 pts)")

    # Requirement 4: Installed version matches VSIX version (0.2 pts)
    if manifest and match_ext and manifest['version'] == match_ext.get('version'):
        score += 0.2
        print(f"✓ Installed version matches VSIX version ({manifest['version']}) (+0.2)")
    elif match_ext and manifest:
        print(f"⚠ Version mismatch: VSIX {manifest['version']} vs installed {match_ext.get('version')} (0 pts)")
    elif match_ext and not manifest:
        # Manifest unavailable – award partial credit for installation but can’t compare versions
        score += 0.1
        print("⚠ Unable to verify version match (manifest unavailable) (+0.1)")

    # Clamp final score between 0 and 1
    score = min(max_score, score)
    print(f"TOTAL SCORE: {score}/{max_score}")
    print(f"REWARD: {score}")
    return score

# --------------- Script Entrypoint ---------------
if __name__ == '__main__':
    verify_task()
