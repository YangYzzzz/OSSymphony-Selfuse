#!/usr/bin/env bash
# File: ~/vscode_backup_task_init.sh
#
# Purpose:
#   1. Create a small workspace that asks the user to output the
#      installed-extension list to ~/vscode-backup/exts.txt
#   2. Open VS Code on that workspace so the user can perform the task
#
# Usage:
#   chmod +x ~/vscode_backup_task_init.sh
#   ~/vscode_backup_task_init.sh
#
set -euo pipefail

echo "==> Preparing VS Code extension-backup task (initial state)…"

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
WS="$HOME/vscode_backup_task"          # Workspace folder
BACKUP_DIR="$HOME/vscode-backup"       # Where the exts.txt must go
EXT_LIST_FILE="$BACKUP_DIR/exts.txt"   # Target file

# ------------------------------------------------------------------
# Clean / create directories
# ------------------------------------------------------------------
rm -rf "$WS"
mkdir -p "$WS"
mkdir -p "$BACKUP_DIR"       # keep the dir, but remove any previous file
rm -f  "$EXT_LIST_FILE"

# ------------------------------------------------------------------
# Populate workspace with helpful info
# ------------------------------------------------------------------
cat > "$WS/README.md" <<'EOF'
# VS Code – Backup Installed Extensions

Goal:
Generate a **plain-text** list of every extension currently installed
(including versions) and save it here:

    ~/vscode-backup/exts.txt

Quickest way (inside a terminal):

    code --list-extensions --show-versions > ~/vscode-backup/exts.txt
EOF

echo "Generate the extension list into ~/vscode-backup/exts.txt" \
  > "$WS/.task_info.txt"

# ------------------------------------------------------------------
# Verify initial conditions
# ------------------------------------------------------------------
if [[ -e "$EXT_LIST_FILE" ]]; then
  echo "ERROR: $EXT_LIST_FILE already exists – it should NOT exist at task start." >&2
  exit 1
fi

echo "Initial state looks good – opening VS Code…"

# ------------------------------------------------------------------
# Open VS Code on the workspace
# ------------------------------------------------------------------
code "$WS" &>/dev/null &

echo "VS Code launched on $WS"
echo "============================================================"
echo "Task: produce ~/vscode-backup/exts.txt with the extension list"