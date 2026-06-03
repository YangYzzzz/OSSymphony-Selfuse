#!/usr/bin/env bash
set -euo pipefail
#
#  prepare_cpp_refactor.sh
#  -----------------------
#  Creates a C++-centric workspace in which the “Pylance” extension is
#  installed and enabled.  The user’s task will be to disable it.
#

echo ">> Creating initial workspace …"

WORKSPACE="$HOME/vscode_cpp_refactor"       # freely chosen path
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src" "$WORKSPACE/scripts" "$WORKSPACE/.vscode"

# ---------------------------------------------------------------------
# Sample C++ code (main focus of current work)
# ---------------------------------------------------------------------
cat > "$WORKSPACE/src/main.cpp" <<'EOF'
#include <iostream>

int main() {
    std::cout << "Hello C++ Refactor!" << std::endl;
    return 0;
}
EOF

# ---------------------------------------------------------------------
# Stray Python file (causes Pylance to kick in and hog CPU)
# ---------------------------------------------------------------------
cat > "$WORKSPACE/scripts/analysis.py" <<'EOF'
def add(a, b):
    return a + b
EOF

# ---------------------------------------------------------------------
# README describing the situation
# ---------------------------------------------------------------------
cat > "$WORKSPACE/README.md" <<'EOF'
# C++ Refactor Workspace

You are currently focused on a large C++ refactor.  
Unfortunately, the “Pylance” Python language server continues to scan
every Python file in the workspace and eats a lot of CPU.

TASK: Temporarily disable the **Pylance** extension until you return to
Python development.
EOF

# ---------------------------------------------------------------------
# C++-related workspace settings (to underline the C++ context)
# ---------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
    "files.associations": {
        "*.h": "cpp",
        "*.hpp": "cpp"
    },
    "C_Cpp.intelliSenseEngine": "Default"
}
EOF

# ---------------------------------------------------------------------
# Ensure Pylance is present and enabled
# ---------------------------------------------------------------------
if ! code --list-extensions | grep -q '^ms-python.vscode-pylance$'; then
    echo ">> Pylance not detected – attempting to install..."
    if code --install-extension ms-python.vscode-pylance --force; then
        echo ">> Pylance successfully installed."
    else
        echo "!! WARNING: Could not install Pylance.  Continuing anyway."
    fi
else
    echo ">> Pylance already installed."
fi

# Verify presence
if code --list-extensions | grep -q '^ms-python.vscode-pylance$'; then
    echo ">> Verification OK: Pylance is enabled."
else
    echo "!! Verification FAILED: Pylance is not found.  Task may not behave as expected." >&2
fi

# ---------------------------------------------------------------------
# Small marker file that the grader / user can open
# ---------------------------------------------------------------------
echo "Disable the 'Pylance' extension (ms-python.vscode-pylance) via the Extensions view." \
    > "$WORKSPACE/.task_info.txt"

# ---------------------------------------------------------------------
# Open VS Code
# ---------------------------------------------------------------------
echo ">> Opening VS Code on $WORKSPACE"
code "$WORKSPACE" &

echo ">> Initial setup complete."