#!/usr/bin/env bash
###############################################################################
# Initial Setup Script
#   - Creates a sample C++ workspace
#   - Ensures *an older* version (1.18.3) of ms-vscode.cpptools is installed
#   - Leaves a clear task marker telling the user to install 1.18.5
#   - Opens VS Code on the workspace
###############################################################################
set -euo pipefail

echo "========== VS Code C++ CI Task – Initial State =========="

# ---------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------
WORKSPACE="$HOME/cpp_ci_task"
EXTENSION="ms-vscode.cpptools"
OLD_VERSION="1.18.3"     # deliberately NOT the required version
REQUIRED_VERSION="1.18.5"
VSCODE_CMD="code"        # VS Code CLI executable

# ---------------------------------------------------------------------------
# Clean previous runs
# ---------------------------------------------------------------------------
echo "Cleaning previous workspace (if any)…"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

# ---------------------------------------------------------------------------
# Sample project files
# ---------------------------------------------------------------------------
cat > "$WORKSPACE/src/main.cpp" << 'EOF'
#include <iostream>

int main() {
    std::cout << "CI test build OK" << std::endl;
    return 0;
}
EOF

# Minimal CMakeLists to look realistic
cat > "$WORKSPACE/CMakeLists.txt" << 'EOF'
cmake_minimum_required(VERSION 3.10)
project(ci_test)
add_executable(ci_test src/main.cpp)
EOF

# .vscode settings (uses cpptools configuration provider)
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
    "C_Cpp.default.compilerPath": "/usr/bin/clang++",
    "C_Cpp.default.cppStandard": "c++17",
    "cmake.configureOnOpen": true
}
EOF

# ---------------------------------------------------------------------------
# Extension state preparation
#   1. Remove target version if it already exists
#   2. Install an older version so the user MUST upgrade
# ---------------------------------------------------------------------------
echo "Preparing extension state…"
# 1) Remove any existing version of the extension
if $VSCODE_CMD --list-extensions | grep -q "^${EXTENSION}$"; then
    echo "Removing existing ${EXTENSION} extension to create controlled state…"
    $VSCODE_CMD --uninstall-extension "${EXTENSION}" --force
fi

# 2) Install the *older* version (requires internet unless the VSIX is cached)
echo "Installing ${EXTENSION}@${OLD_VERSION} (simulating outdated environment)…"
$VSCODE_CMD --install-extension "${EXTENSION}@${OLD_VERSION}" --force

# ---------------------------------------------------------------------------
# Verification of initial state
# ---------------------------------------------------------------------------
echo "Verifying that ONLY the old version is present…"
if $VSCODE_CMD --list-extensions --show-versions | grep -q "^${EXTENSION}@${OLD_VERSION}$"; then
    echo "✅ Correct initial state: ${EXTENSION}@${OLD_VERSION} installed."
else
    echo "❌ Initial state verification failed – exiting!"
    exit 1
fi

# ---------------------------------------------------------------------------
# Task marker – tells the user exactly what to do
# ---------------------------------------------------------------------------
echo "Install ${EXTENSION}@${REQUIRED_VERSION} via the VS Code CLI:
    code --install-extension ${EXTENSION}@${REQUIRED_VERSION} --force" \
    > "$WORKSPACE/TASK_INSTRUCTIONS.txt"

# ---------------------------------------------------------------------------
# Open VS Code on the workspace
# ---------------------------------------------------------------------------
echo "Opening VS Code with the prepared workspace…"
$VSCODE_CMD "$WORKSPACE" &

echo "========== Initial setup complete – user can now perform the task =========="