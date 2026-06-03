"""
Reward Script: Configure Remote - Containers devcontainer for Python data science environment
Task ID: vscode_gf1_081
Domain: vscode (devcontainer configuration)
Scoring:
  - Component 1: devcontainer.json uses Dockerfile-based build (0.15)
  - Component 2: runArgs has GPU and memory config (0.20)
  - Component 3: forwardPorts has 8888 and 6006 (0.15)
  - Component 4: remoteUser/containerUser set to vscode (0.15)
  - Component 5: Dockerfile installs PyTorch, JupyterLab, TensorBoard (0.20)
  - Component 6: Dockerfile creates vscode user with sudo access (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf1_081'
DEVCONTAINER_DIR = os.path.join(WORKDIR, 'projects', 'data-science', '.devcontainer')
DEVCONTAINER_JSON = os.path.join(DEVCONTAINER_DIR, 'devcontainer.json')
DOCKERFILE = os.path.join(DEVCONTAINER_DIR, 'Dockerfile')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load devcontainer.json
    try:
        with open(DEVCONTAINER_JSON, 'r') as f:
            content = f.read()
        # Strip JSONC comments if present
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content_clean = re.sub(r'/\*.*?\*/', '', content_clean, flags=re.DOTALL)
        config = json.loads(content_clean)
    except Exception as e:
        print(f"CRITICAL: Cannot load devcontainer.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load Dockerfile
    try:
        with open(DOCKERFILE, 'r') as f:
            dockerfile_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot load Dockerfile: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: devcontainer.json uses Dockerfile-based build (0.15 points)
    # Initial state uses "image" field directly; golden uses "build.dockerfile"
    try:
        build_section = config.get('build', {})
        dockerfile_in_build = isinstance(build_section, dict) and 'dockerfile' in build_section
        # Also accept "dockerFile" (alternative casing) at top level
        dockerfile_at_top = bool(config.get('dockerFile') or config.get('dockerfile'))
        has_dockerfile_build = dockerfile_in_build or dockerfile_at_top

        if has_dockerfile_build:
            print(f"PASS: Component 1 - Dockerfile-based build configured (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - No Dockerfile-based build found. Config keys: {list(config.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: runArgs has GPU (--gpus all) and memory (--memory=8g) config (0.20 points)
    # Initial state has no runArgs at all
    try:
        run_args = config.get('runArgs', [])
        if not isinstance(run_args, list):
            run_args = []
        run_args_str = ' '.join(str(a) for a in run_args)

        has_gpu = '--gpus' in run_args_str
        has_memory = '--memory' in run_args_str and '8g' in run_args_str.lower()

        if has_gpu and has_memory:
            print(f"PASS: Component 2 - GPU and memory config in runArgs (0.20 pts)")
            total_score += 0.20
        elif has_gpu:
            print(f"PARTIAL: Component 2 - GPU config found but memory missing (0.10 pts)")
            total_score += 0.10
        elif has_memory:
            print(f"PARTIAL: Component 2 - Memory config found but GPU missing (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 - No GPU or memory config in runArgs. runArgs: {run_args}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: forwardPorts has 8888 (Jupyter) and 6006 (TensorBoard) (0.15 points)
    # Initial state has no forwardPorts
    try:
        forward_ports = config.get('forwardPorts', [])
        if not isinstance(forward_ports, list):
            forward_ports = []
        # Convert to ints for comparison
        port_ints = []
        for p in forward_ports:
            try:
                port_ints.append(int(p))
            except (ValueError, TypeError):
                pass

        has_jupyter = 8888 in port_ints
        has_tensorboard = 6006 in port_ints

        if has_jupyter and has_tensorboard:
            print(f"PASS: Component 3 - Ports 8888 and 6006 forwarded (0.15 pts)")
            total_score += 0.15
        elif has_jupyter or has_tensorboard:
            print(f"PARTIAL: Component 3 - Only one port found: {port_ints} (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 3 - forwardPorts missing 8888 and 6006. Found: {port_ints}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: remoteUser and/or containerUser set to "vscode" (0.15 points)
    # Initial state has neither field
    try:
        remote_user = config.get('remoteUser', '')
        container_user = config.get('containerUser', '')

        has_remote_user = remote_user == 'vscode'
        has_container_user = container_user == 'vscode'

        if has_remote_user and has_container_user:
            print(f"PASS: Component 4 - Both remoteUser and containerUser set to 'vscode' (0.15 pts)")
            total_score += 0.15
        elif has_remote_user or has_container_user:
            print(f"PARTIAL: Component 4 - Only one user field set (0.10 pts). remoteUser={remote_user}, containerUser={container_user}")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 - Neither remoteUser nor containerUser set to 'vscode'. remoteUser={remote_user}, containerUser={container_user}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Dockerfile installs CUDA PyTorch, JupyterLab, TensorBoard (0.20 points)
    # Initial Dockerfile has none of these
    try:
        dl = dockerfile_content.lower()
        has_pytorch = 'torch' in dl or 'pytorch' in dl
        has_jupyterlab = 'jupyterlab' in dl or 'jupyter' in dl
        has_tensorboard = 'tensorboard' in dl

        matches = sum([has_pytorch, has_jupyterlab, has_tensorboard])

        if matches == 3:
            print(f"PASS: Component 5 - Dockerfile installs PyTorch, JupyterLab, TensorBoard (0.20 pts)")
            total_score += 0.20
        elif matches >= 2:
            print(f"PARTIAL: Component 5 - {matches}/3 packages found (0.13 pts)")
            total_score += 0.13
        elif matches == 1:
            print(f"PARTIAL: Component 5 - {matches}/3 packages found (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 5 - No PyTorch/JupyterLab/TensorBoard in Dockerfile")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Dockerfile creates vscode user with sudo access (0.15 points)
    # Initial Dockerfile has no user creation or sudo
    try:
        has_sudo_pkg = 'sudo' in dockerfile_content and ('apt-get' in dockerfile_content or 'apk' in dockerfile_content)
        has_user_create = 'useradd' in dockerfile_content or 'adduser' in dockerfile_content
        has_sudo_group = 'sudo' in dockerfile_content and ('usermod' in dockerfile_content or 'addgroup' in dockerfile_content or 'sudoers' in dockerfile_content)
        has_vscode_user = 'vscode' in dockerfile_content

        if has_sudo_pkg and has_user_create and has_vscode_user and has_sudo_group:
            print(f"PASS: Component 6 - Dockerfile creates vscode user with sudo access (0.15 pts)")
            total_score += 0.15
        elif has_user_create and has_vscode_user:
            print(f"PARTIAL: Component 6 - vscode user created but sudo config incomplete (0.10 pts)")
            total_score += 0.10
        elif has_sudo_pkg:
            print(f"PARTIAL: Component 6 - sudo installed but user creation missing (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 - No vscode user or sudo config found in Dockerfile")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(DEVCONTAINER_JSON):
    print(f"File not found: {DEVCONTAINER_JSON}")
    print("REWARD: 0.0")
elif not os.path.exists(DOCKERFILE):
    print(f"File not found: {DOCKERFILE}")
    print("REWARD: 0.0")
else:
    verify_task()
