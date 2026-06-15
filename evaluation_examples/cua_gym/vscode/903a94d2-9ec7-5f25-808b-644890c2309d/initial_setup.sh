#!/usr/bin/env bash
# -----------------------------------------------
#  create_work_env.sh
#  Sets up the initial C++ workspace that still
#  needs a .vscode/tasks.json to expose Makefile
#  targets in the Ctrl+Shift+B picker.
# -----------------------------------------------
set -euo pipefail

echo "⏳  Creating initial C++ workspace …"

WORKSPACE="$HOME/workspace/my-app"
SRC_DIR="$WORKSPACE/src"

# (Re)create workspace structure
rm -rf "$WORKSPACE"
mkdir -p "$SRC_DIR"

# ------------------------------------------------
# 1.  Sample source file
# ------------------------------------------------
cat > "$SRC_DIR/main.cpp" << 'EOF'
#include <iostream>

int main() {
    std::cout << "Hello from my-app!" << std::endl;
    return 0;
}
EOF

# ------------------------------------------------
# 2.  Makefile with four classic targets
#     (notice TABs before recipe lines)
# ------------------------------------------------
cat > "$WORKSPACE/Makefile" << 'EOF'
CC=g++
CFLAGS=-Wall -g
SRC=src/main.cpp
BIN=bin/myapp

build:
\t@mkdir -p bin
\t$(CC) $(CFLAGS) $(SRC) -o $(BIN)

install: build
\t@echo "Installing $(BIN) to /usr/local/bin (simulated)"

test: build
\t@echo "Running tests … (simulated)"

clean:
\trm -rf bin
EOF

# ------------------------------------------------
# 3.  VS Code helper files (NO tasks.json yet)
# ------------------------------------------------
mkdir -p "$WORKSPACE/.vscode"

# IntelliSense configuration (cpptools extension)
cat > "$WORKSPACE/.vscode/c_cpp_properties.json" << 'EOF'
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": ["${workspaceFolder}/**"],
            "compilerPath": "/usr/bin/g++",
            "cStandard": "c11",
            "cppStandard": "c++17",
            "intelliSenseMode": "linux-gcc-x64"
        }
    ],
    "version": 4
}
EOF

# Extension recommendation
cat > "$WORKSPACE/.vscode/extensions.json" << 'EOF'
{
    "recommendations": ["ms-vscode.cpptools"]
}
EOF

# Task reminder for the learner / evaluator
echo "Create .vscode/tasks.json exposing the Makefile targets install, build, test, and clean." \
  > "$WORKSPACE/.task_info.txt"

echo "✅  Initial workspace ready: $WORKSPACE"
echo "   (No build tasks defined yet)"

# ------------------------------------------------
# 4.  Launch VS Code so the user can start working
# ------------------------------------------------
code "$WORKSPACE" &>/dev/null &
sleep 2
echo "🚀  VS Code opened. Press Ctrl+Shift+B and note that no custom build tasks exist."