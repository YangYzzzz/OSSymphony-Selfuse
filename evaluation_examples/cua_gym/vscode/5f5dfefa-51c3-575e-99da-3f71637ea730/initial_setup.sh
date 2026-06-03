#!/usr/bin/env bash
# ------------------------------------------------------------------
#  VS Code Task – Initial Setup
#  Goal:  Prepare /home/user/dev with multiple `.idea` folders that
#         are *NOT* excluded from the VS Code Explorer.
# ------------------------------------------------------------------
set -euo pipefail

echo "=== VS Code Task – Initial State Preparation ==="

# 1. Workspace root as specified in the task
WORKSPACE="/home/user/dev"

# 2. Start fresh (remove any previous attempt)
if [[ -d "$WORKSPACE" ]]; then
    echo "Removing existing workspace at $WORKSPACE"
    rm -rf "$WORKSPACE"
fi

# 3. Create realistic project structure
echo "Creating workspace structure..."
mkdir -p "$WORKSPACE"/{src,docs,subproject1/subsrc}
touch "$WORKSPACE/src/main.py"
echo "# Sample Python entry point" > "$WORKSPACE/src/main.py"
touch "$WORKSPACE/docs/README.md"

# 4. Create JetBrains `.idea` folders that should later be hidden
echo "Adding sample .idea folders..."
for dir in "$WORKSPACE" "$WORKSPACE/subproject1"; do
    mkdir -p "$dir/.idea"
    echo "placeholder" > "$dir/.idea/workspace.xml"
done

# 5. Add an empty VS Code settings file (no exclusions yet)
VSCODE_DIR="$WORKSPACE/.vscode"
mkdir -p "$VSCODE_DIR"

cat > "$VSCODE_DIR/settings.json" << 'EOF'
{
    // Workspace settings – currently nothing excludes ".idea"
    "editor.tabSize": 4,
    "files.autoSave": "off"
}
EOF
echo "Created $VSCODE_DIR/settings.json without .idea exclusion."

# 6. Task marker for the user
echo "Hide .idea folders from Explorer by configuring files.exclude" \
     > "$WORKSPACE/.task_info.txt"

# 7. Open VS Code
echo "Opening VS Code in initial state..."
code "$WORKSPACE" &

echo "=== Initial setup complete. You should see '.idea' folders in the Explorer. ==="