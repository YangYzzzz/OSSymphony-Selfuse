"""
FINAL REWARD SCRIPT - SUCCESS
Task: Whenever I launch VS Code, I’d love it to automatically open a fresh JavaScript file named “app.js” in /home/user/playground so I can start coding right away—could you help me set that up?
Generated: 2025-09-11 19:03:27
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import re
import pathlib


def verify_task():
    """Verify that VS Code will automatically open ~/playground/app.js.

    The verification checks five concrete requirements and awards
    progressive points for each:
      1. The target file ~/playground/app.js exists                (0.20)
      2. A wrapper script ~/.local/bin/code-auto-open is executable (0.35)
      3. The wrapper script explicitly references the app.js path   (0.15)
      4. ~/.bashrc contains alias  code='code-auto-open'            (0.15)
      5. ~/.local/bin precedes /usr/bin in the PATH (wrapper wins)  (0.15)

    A perfect setup yields 1.0, partial setup yields a proportionate score.
    """

    # Weight for each requirement
    weights = {
        'file_exists':      0.20,
        'wrapper_exists':   0.35,
        'wrapper_correct':  0.15,
        'bashrc_alias':     0.15,
        'path_priority':    0.15,
    }

    total_score = 0.0
    home = pathlib.Path.home()
    app_js_path = home / 'playground' / 'app.js'
    wrapper_path = home / '.local' / 'bin' / 'code-auto-open'
    bashrc_path = home / '.bashrc'

    # 1. app.js exists
    if app_js_path.is_file():
        print(f"✓ app.js exists at {app_js_path}")
        total_score += weights['file_exists']
    else:
        print("✗ app.js not found in ~/playground")

    # 2. Wrapper script exists and is executable
    wrapper_content = ''
    if wrapper_path.exists() and os.access(wrapper_path, os.X_OK):
        print(f"✓ Wrapper script exists and is executable: {wrapper_path}")
        total_score += weights['wrapper_exists']
        wrapper_content = wrapper_path.read_text(errors='ignore')
    else:
        if not wrapper_path.exists():
            print("✗ Wrapper script code-auto-open not found in ~/.local/bin")
        else:
            print("✗ Wrapper script found but is NOT executable")

    # 3. Wrapper script must reference the correct app.js path
    if wrapper_content:
        escaped = re.escape(str(app_js_path))
        if re.search(escaped, wrapper_content):
            print("✓ Wrapper script correctly references ~/playground/app.js")
            total_score += weights['wrapper_correct']
        else:
            print("✗ Wrapper script does NOT reference ~/playground/app.js")

    # 4. .bashrc must alias code to wrapper
    if bashrc_path.exists():
        bashrc_text = bashrc_path.read_text(errors='ignore')
        if re.search(r"alias\s+code=['\"]code-auto-open['\"]", bashrc_text):
            print("✓ .bashrc contains alias code='code-auto-open'")
            total_score += weights['bashrc_alias']
        else:
            print("✗ .bashrc is missing alias code='code-auto-open'")
    else:
        print("✗ .bashrc not found – cannot verify alias")

    # 5. PATH priority: ~/.local/bin must precede /usr/bin so alias dominates
    path_parts = os.environ.get('PATH', '').split(':')
    local_bin = str(home / '.local' / 'bin')
    if local_bin in path_parts:
        if '/usr/bin' in path_parts and path_parts.index(local_bin) < path_parts.index('/usr/bin'):
            print("✓ ~/.local/bin appears BEFORE /usr/bin in PATH")
            total_score += weights['path_priority']
        elif '/usr/bin' not in path_parts:
            print("✓ ~/.local/bin present in PATH and /usr/bin absent – acceptable")
            total_score += weights['path_priority']
        else:
            print("✗ ~/.local/bin is AFTER /usr/bin in PATH – wrapper may be shadowed")
    else:
        print("✗ ~/.local/bin not found in PATH")

    # Clamp & round score
    final_score = round(min(total_score, 1.0), 2)
    print(f"Total score: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()
