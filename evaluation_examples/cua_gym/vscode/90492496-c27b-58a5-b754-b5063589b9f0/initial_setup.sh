#!/usr/bin/env bash
# File: setup_initial_stage_all.sh
set -euo pipefail

echo "=== VS Code – Stage-All Task ► Initial state builder ==="

# ---------------------------------------------------------------------------
# 1. Workspace & basic project structure
# ---------------------------------------------------------------------------
WORKSPACE="$HOME/vscode_stage_all_task"
echo "Creating workspace at: $WORKSPACE"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/src" "$WORKSPACE/styles"
cd "$WORKSPACE"

# src/app.ts  (initial version)
cat > src/app.ts <<'EOF'
export function greet(name: string): string {
  return `Hello, ${name}!`;
}
EOF

# styles/site.css (initial version)
cat > styles/site.css <<'EOF'
body {
  margin: 0;
  font-family: Arial, sans-serif;
}
EOF

# ---------------------------------------------------------------------------
# 2. Git repository initialisation & first commit
# ---------------------------------------------------------------------------
git init
git config user.name  "VSCode Task User"
git config user.email "task@example.com"
git add .
git commit -m "Initial project scaffold"

# ---------------------------------------------------------------------------
# 3. Simulate user edits that MUST be staged later
# ---------------------------------------------------------------------------
echo "// TODO: add farewell"         >> src/app.ts
echo "h2 { color: royalblue; }"     >> styles/site.css

# ---------------------------------------------------------------------------
# 4. Verification – exactly two modified (unstaged) files must exist
# ---------------------------------------------------------------------------
echo "Verifying modified-but-unstaged files…"
EXPECTED_MODS=2
ACTUAL_MODS=$(git status --porcelain | grep '^ M' | wc -l)

if [[ $ACTUAL_MODS -ne $EXPECTED_MODS ]]; then
  echo "ERROR: Expected $EXPECTED_MODS modified files, found $ACTUAL_MODS." >&2
  exit 1
fi
git status --short
echo "✓ Verification successful – workspace ready."

# ---------------------------------------------------------------------------
# 5. Task hint for the learner
# ---------------------------------------------------------------------------
cat > .task_info.txt <<'EOF'
TASK: Stage every modified file at once.
HINTS:
  • Source Control sidebar ► click the “+” icon next to “Changes”.
  • …or press: Ctrl+Shift+G  then A   (Git: Stage All Changes command).
  • …or open Command Palette (Ctrl+Shift+P) ► “Git: Stage All Changes”.
EOF

# ---------------------------------------------------------------------------
# 6. Open VS Code pointed at the workspace
# ---------------------------------------------------------------------------
echo "Launching VS Code…"
code "$WORKSPACE" &

echo "=== Initial setup complete – perform the Stage-All action in VS Code. ==="