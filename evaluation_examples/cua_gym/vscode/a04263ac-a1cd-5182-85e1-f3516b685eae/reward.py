"""
Reward Script: Create devcontainer configuration for ml-project
Task ID: vscode_gf5_027
Domain: vscode
Scoring:
  - Component 1: devcontainer.json exists and is valid JSON (0.15)
  - Component 2: Python 3.10 base image reference (0.20)
  - Component 3: CUDA 11.8 toolkit configuration (0.20)
  - Component 4: postCreateCommand installs requirements.txt (0.15)
  - Component 5: forwardPorts includes 8888 (0.15)
  - Component 6: Python and Jupyter extensions configured (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_027'
DEVCONTAINER_PATH = os.path.join(WORKDIR, 'projects', 'ml-project', '.devcontainer', 'devcontainer.json')


def check_python310_image(config):
    """Check if config references a Python 3.10 base image. Returns (bool, detail_str)."""
    image_val = config.get('image', '')
    if isinstance(image_val, str) and image_val:
        if 'python' in image_val.lower() and ('3.10' in image_val or '3-10' in image_val):
            return (True, image_val)

    build_val = config.get('build', {})
    if isinstance(build_val, dict):
        build_str = json.dumps(build_val).lower()
        if 'python' in build_str and ('3.10' in build_str or '3-10' in build_str):
            return (True, str(build_val))

    return (False, f"image={image_val}, build={config.get('build', {})}")


def check_cuda_118(config):
    """Check if config includes CUDA 11.8 toolkit. Returns (bool, detail_str)."""
    features = config.get('features', {})
    if isinstance(features, dict):
        for feat_key, feat_val in features.items():
            if 'cuda' in feat_key.lower() or 'nvidia' in feat_key.lower():
                feat_str = json.dumps(feat_val) if isinstance(feat_val, dict) else str(feat_val)
                if '11.8' in feat_str or '11-8' in feat_str:
                    return (True, f"{feat_key}: {feat_val}")

    image_val = config.get('image', '')
    if isinstance(image_val, str) and 'cuda' in image_val.lower() and '11.8' in image_val:
        return (True, f"image contains cuda 11.8: {image_val}")

    config_str = json.dumps(config)
    if 'cuda' in config_str.lower() and '11.8' in config_str:
        return (True, "cuda 11.8 found in config")

    return (False, "CUDA 11.8 not found in features or image")


def check_post_create_command(config):
    """Check postCreateCommand installs requirements.txt. Returns (bool, detail_str)."""
    post_cmd = config.get('postCreateCommand', '')
    if isinstance(post_cmd, str):
        if 'pip install' in post_cmd.lower() and 'requirements' in post_cmd.lower():
            return (True, post_cmd)
    elif isinstance(post_cmd, list):
        cmd_joined = ' '.join(str(x) for x in post_cmd).lower()
        if 'pip install' in cmd_joined and 'requirements' in cmd_joined:
            return (True, str(post_cmd))
    return (False, f"postCreateCommand: {post_cmd}")


def get_extensions(config):
    """Extract extensions list from config. Returns list."""
    customizations = config.get('customizations', {})
    if isinstance(customizations, dict):
        vscode_custom = customizations.get('vscode', {})
        if isinstance(vscode_custom, dict):
            exts = vscode_custom.get('extensions', [])
            if isinstance(exts, list) and len(exts) > 0:
                return exts
    # Legacy top-level key
    exts = config.get('extensions', [])
    if isinstance(exts, list):
        return exts
    return []


def verify_task(file_path):
    """
    Verify devcontainer configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: File must exist and be valid JSON
    if not os.path.exists(file_path):
        print(f"CRITICAL: devcontainer.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Handle JSONC (JSON with comments) — strip // comments
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        config = json.loads(cleaned)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse devcontainer.json as JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: devcontainer.json has valid devcontainer structure (0.15 points)
    try:
        if isinstance(config, dict) and len(config) >= 2:
            print(f"PASS: Component 1 — devcontainer.json valid JSON with {len(config)} top-level keys (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — insufficient structure: {list(config.keys()) if isinstance(config, dict) else type(config)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Python 3.10 base image (0.20 points)
    try:
        passed, detail = check_python310_image(config)
        if passed:
            print(f"PASS: Component 2 — Python 3.10 base image: {detail} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Python 3.10 not found. {detail}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: CUDA 11.8 toolkit (0.20 points)
    try:
        passed, detail = check_cuda_118(config)
        if passed:
            print(f"PASS: Component 3 — CUDA 11.8 toolkit: {detail} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: postCreateCommand installs requirements.txt (0.15 points)
    try:
        passed, detail = check_post_create_command(config)
        if passed:
            print(f"PASS: Component 4 — postCreateCommand: {detail} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — {detail}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: forwardPorts includes 8888 (0.15 points)
    try:
        forward_ports = config.get('forwardPorts', [])
        if isinstance(forward_ports, list) and 8888 in forward_ports:
            print(f"PASS: Component 5 — forwardPorts includes 8888: {forward_ports} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — forwardPorts missing 8888. Found: {forward_ports}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Python and Jupyter VS Code extensions (0.15 points)
    try:
        extensions = get_extensions(config)
        ext_lower = [str(e).lower() for e in extensions]

        has_python = any('python' in e and ('ms-python' in e or 'python.python' in e) for e in ext_lower)
        has_jupyter = any('jupyter' in e for e in ext_lower)

        if has_python and has_jupyter:
            print(f"PASS: Component 6 — Python and Jupyter extensions: {extensions} (0.15 pts)")
            total_score += 0.15
        elif has_python or has_jupyter:
            which = "Python" if has_python else "Jupyter"
            missing = "Jupyter" if has_python else "Python"
            print(f"PARTIAL: Component 6 — {which} found, {missing} missing: {extensions} (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 6 — No Python or Jupyter extensions. Found: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(DEVCONTAINER_PATH):
    print(f"File not found: {DEVCONTAINER_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(DEVCONTAINER_PATH)
