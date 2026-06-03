#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Initial Setup Script for “Create first commit” VS Code task
# -----------------------------------------------------------------------------
# This script:
#   1. Creates a sample project in ~/projects/notes-app
#   2. Initializes a Git repository and STAGES every file (but does NOT commit)
#   3. Opens the workspace in VS Code so the user can create the first commit
# -----------------------------------------------------------------------------
set -euo pipefail

echo "=== Preparing initial Git workspace for VS Code task ==="

# ----------------------------------------------------------------------------- 
# 1. Define workspace location
# -----------------------------------------------------------------------------
WORKSPACE="$HOME/projects/notes-app"

# Clean up any previous run
rm -rf "$WORKSPACE"

# ----------------------------------------------------------------------------- 
# 2. Create project structure & sample files
# -----------------------------------------------------------------------------
echo "--- Creating project structure ---"
mkdir -p "$WORKSPACE/src" "$WORKSPACE/docs"

cat > "$WORKSPACE/README.md" << 'EOF'
# Notes App
A simple command-line notes application.
EOF

cat > "$WORKSPACE/src/main.py" << 'EOF'
#!/usr/bin/env python3
def main():
    print("Welcome to Notes App")
if __name__ == "__main__":
    main()
EOF
chmod +x "$WORKSPACE/src/main.py"

cat > "$WORKSPACE/.gitignore" << 'EOF'
__pycache__/
EOF

# ----------------------------------------------------------------------------- 
# 3. Initialize Git repo and stage all files
# -----------------------------------------------------------------------------
echo "--- Initialising Git repository ---"
cd "$WORKSPACE"
git init -q

# Configure dummy user if not already configured
git config user.name  "VSCode Test User"
git config user.email "testuser@example.com"

echo "--- Staging all files ---"
git add .

# Verification: ensure everything is staged but uncommitted
if [[ -n "$(git diff --cached --name-only)" ]] && [[ -z "$(git log --oneline)" ]]; then
    echo "✔ Files are staged and ready to commit"
else
    echo "✖ Unexpected Git state" >&2
    exit 1
fi

# ----------------------------------------------------------------------------- 
# 4. Open VS Code to let the user perform the task
# -----------------------------------------------------------------------------
echo "--- Launching VS Code ---"
code "$WORKSPACE" &

echo "=== Initial setup complete ==="
echo "Task: In VS Code Source Control panel, enter commit message “first commit” and click Commit."