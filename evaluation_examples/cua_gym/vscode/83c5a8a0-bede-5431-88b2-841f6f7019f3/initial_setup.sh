#!/usr/bin/env bash
# File: setup_initial_hello_task.sh
# Purpose: Prepare a VS Code workspace that requires the user to
#          create src/hello.py and insert the say_hello() function.

set -euo pipefail

echo "==========  Preparing initial VS Code task environment  =========="

# -------------------------------------------------------------------
# 1. Define workspace location
# -------------------------------------------------------------------
WORKSPACE="$HOME/quick_hello_task"
echo "Workspace directory: $WORKSPACE"

# Start clean every time the script is executed
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

# -------------------------------------------------------------------
# 2. Create realistic starter content
# -------------------------------------------------------------------
cat > "$WORKSPACE/README.md" << 'EOF'
# Quick Hello Task

Create `src/hello.py` and add a `say_hello()` function that prints
`Hello, VS Code!`.
EOF

# A minimal Python entry point that will later import the new function
cat > "$WORKSPACE/main.py" << 'EOF'
"""
Starter file for the Quick Hello Task.
After creating src/hello.py with say_hello(), modify the import below.
"""
# from src.hello import say_hello   # <-- Will work after you create the file

if __name__ == "__main__":
    print("Run `say_hello()` after you implement it.")
EOF

# -------------------------------------------------------------------
# 3. Provide a workspace-level Python snippet to speed things up
#    Users can type `sayhello` + <Tab> to expand the boilerplate.
# -------------------------------------------------------------------
mkdir -p "$WORKSPACE/.vscode/snippets"
cat > "$WORKSPACE/.vscode/snippets/python.json" << 'EOF'
{
    "Say Hello Function": {
        "prefix": "sayhello",
        "body": [
            "def say_hello():",
            "    print(\"Hello, VS Code!\")"
        ],
        "description": "Quickly insert a say_hello() function"
    }
}
EOF

# -------------------------------------------------------------------
# 4. Add task marker so graders / users know the objective
# -------------------------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" << 'EOF'
Task:
1. Create a file named src/hello.py
2. Use the 'sayhello' snippet OR regular IntelliSense to add:
       def say_hello():
           print("Hello, VS Code!")
3. Save the file.

Keyboard-only hint: 
- Ctrl+N or Ctrl+K, Ctrl+O to open src directory, then Ctrl+N to make new file.
- Type "sayhello" → Tab to expand the snippet, then Ctrl+S.
EOF

# -------------------------------------------------------------------
# 5. Basic verification
# -------------------------------------------------------------------
[[ -d "$WORKSPACE/src" ]] || { echo "ERROR: src directory not created." ; exit 1; }
[[ -f "$WORKSPACE/.vscode/snippets/python.json" ]] || { echo "ERROR: snippet not found." ; exit 1; }
echo "Initial verification passed ✔"

# -------------------------------------------------------------------
# 6. Open VS Code on the workspace
# -------------------------------------------------------------------
echo "Opening VS Code..."
code "$WORKSPACE" &

echo "==========  Initial setup complete. VS Code is ready. =========="