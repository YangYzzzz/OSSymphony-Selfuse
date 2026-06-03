"""
FINAL REWARD SCRIPT - SUCCESS
Task: I exported my own collection of code snippets into a VSIX file located at /home/user/workspace/my-snippets.vsix. How can I install this package in VS Code so I can start using the snippets right away?
Generated: 2025-09-11 11:47:02
Status: success
Model: azure-o3
Total Steps: 13
"""

import json
import zipfile
from pathlib import Path

"""
Reward script for the task:
"I exported my own collection of code snippets into a VSIX file located at
 /home/user/workspace/my-snippets.vsix. How can I install this package in VS
 Code so I can start using the snippets right away?"

The script verifies four concrete things and assigns progressive scores:
 1. The VSIX file exists at the required path (0.2)
 2. The VSIX contains a readable package.json manifest with publisher & name
    information (0.2)
 3. An extension with the SAME publisher & name is present in one of VS Code’s
    standard extensions directories (0.4)
 4. That installed extension declares snippet contributions in its manifest
    (0.2)

Total score = 1.0 only when ALL of the above pass.
"""

def load_vsix_metadata(vsix_path: Path):
    """Extract important fields from the VSIX's package.json."""
    try:
        with zipfile.ZipFile(vsix_path) as zf:
            for member in zf.namelist():
                # Ignore packaging artefacts, stop at first package.json found
                if member.endswith("package.json") and not member.startswith("[Content_Types]"):
                    data = json.loads(zf.read(member).decode("utf-8"))
                    return {
                        "publisher": data.get("publisher"),
                        "name": data.get("name"),
                        "version": data.get("version"),
                        "contributes": data.get("contributes", {})
                    }
    except zipfile.BadZipFile:
        print("✗ VSIX is not a valid zip archive")
    except Exception as e:
        print("✗ Error reading VSIX manifest:", e)
    return None


def discover_installed_extensions():
    """Return a list of installed extensions from common VS Code dirs."""
    bases = [Path.home() / ".vscode/extensions", Path.home() / ".vscode-server/extensions"]
    installed = []
    for base in bases:
        if base.is_dir():
            for item in base.iterdir():
                if item.is_dir():
                    manifest = item / "package.json"
                    if manifest.exists():
                        try:
                            data = json.load(open(manifest, encoding="utf-8"))
                            installed.append({
                                "path": str(item),
                                "publisher": data.get("publisher"),
                                "name": data.get("name"),
                                "version": data.get("version"),
                                "contributes": data.get("contributes", {})
                            })
                        except Exception as e:
                            print("Error reading manifest", manifest, e)
    return installed


def verify_task():
    total = 0.0
    max_score = 1.0

    # ------------------------------------------------------------------
    # 1. VSIX existence
    vsix_path = Path("/home/user/workspace/my-snippets.vsix")
    if vsix_path.exists():
        print(f"✓ VSIX file found at {vsix_path}")
        total += 0.2
    else:
        print("✗ VSIX file is missing at the expected location")
        print(f"REWARD: {total}")
        return total  # Cannot continue without the VSIX

    # ------------------------------------------------------------------
    # 2. Manifest extraction from VSIX
    meta = load_vsix_metadata(vsix_path)
    if meta and meta.get("publisher") and meta.get("name"):
        print(f"✓ Extracted manifest from VSIX: {meta['publisher']}.{meta['name']} v{meta['version']}")
        total += 0.2
    else:
        print("✗ Failed to extract valid manifest information from VSIX")
        print(f"REWARD: {total}")
        return total

    # ------------------------------------------------------------------
    # 3. Extension installed check
    installed = discover_installed_extensions()
    print(f"Discovered {len(installed)} installed extensions")

    match = None
    for ext in installed:
        if ext["publisher"] == meta["publisher"] and ext["name"] == meta["name"]:
            match = ext
            break

    if match:
        print(
            f"✓ Extension is installed: {match['publisher']}.{match['name']} "
            f"v{match['version']} (path: {match['path']})"
        )
        total += 0.4

        # ------------------------------------------------------------------
        # 4. Verify snippet contribution
        contributes_snip = (
            match["contributes"].get("snippets")
            if isinstance(match["contributes"], dict)
            else None
        )
        if contributes_snip:
            print("✓ Extension declares snippet contributions")
            total += 0.2
        else:
            print("✗ Extension does not declare any snippet contributions")
    else:
        print("✗ Extension not found in VS Code extensions directories")

    # ------------------------------------------------------------------
    final_score = min(total, max_score)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()
