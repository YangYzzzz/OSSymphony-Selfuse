#!/usr/bin/env bash
# ==============================================
# VS Code Task – INITIAL STATE
# Goal:  User must PERMANENTLY delete
#        src/assets/greetings.txt from Explorer
#        *and* have that deletion appear as a
#        STAGED change in the Source-Control view.
# ==============================================
set -euo pipefail

echo "🛠  Preparing initial workspace …"

# ------------------------------------------------------------------
# 1. Workspace & basic Git repo
# ------------------------------------------------------------------
WORKSPACE="$HOME/vscode_delete_task"
REPO="$WORKSPACE"
if [ -d "$WORKSPACE" ]; then
  echo "⚠️  Removing old workspace at $WORKSPACE"
  rm -rf "$WORKSPACE"
fi
mkdir -p "$WORKSPACE/src/assets"

# ------------------------------------------------------------------
# 2. Populate files
# ------------------------------------------------------------------
cat > "$WORKSPACE/src/assets/greetings.txt" <<'EOF'
Hello, VS Code!
You will delete me soon.
EOF

cat > "$WORKSPACE/README.md" <<'EOF'
# Delete Task

Delete `src/assets/greetings.txt` permanently from the VS Code Explorer.
The deletion must show up **staged** in Source Control.
EOF

# ------------------------------------------------------------------
# 3. Initialise Git
# ------------------------------------------------------------------
cd "$WORKSPACE"
git init -q
git config user.name  "Delete Task Bot"
git config user.email "delete@task.local"

git add .
git commit -q -m "Initial commit with greetings file"

echo "✅  Git repository initialised and clean"

# ------------------------------------------------------------------
# 4. VS Code workspace-level settings
#    - Skip delete confirmation
#    - Enable smart commit (helps users commit quickly later)
# ------------------------------------------------------------------
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  // No confirmation dialogue when deleting
  "explorer.confirmDelete": false,
  // Convenience – not strictly required for the task
  "git.enableSmartCommit": true
}
EOF

# ------------------------------------------------------------------
# 5. Task instructions (helper file for graders / users)
# ------------------------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
TASK: In VS Code Explorer, permanently delete:
      src/assets/greetings.txt
      The file's removal must appear AUTOMATICALLY
      in the Git view under "STAGED CHANGES".
EOF

# ------------------------------------------------------------------
# 6. Verification of initial state
# ------------------------------------------------------------------
if git status --porcelain | grep -q .; then
  echo "❌  Initial workspace is NOT clean. Aborting."
  exit 1
fi
echo "✅  Verification passed – clean working tree"

# ------------------------------------------------------------------
# 7. Open VS Code
# ------------------------------------------------------------------
echo "🚀  Opening VS Code …"
code "$WORKSPACE" &

echo "🟢  Initial setup complete.  Ready for user action."