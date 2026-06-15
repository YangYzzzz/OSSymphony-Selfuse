#!/usr/bin/env bash
#
#  data_science_initial.sh
#  -------------------------------------------------------------
#  Prepares an "unsaved" VS Code workspace that the learner will
#  have to save as /home/user/analytics/data-science.code-workspace
#  -------------------------------------------------------------

set -euo pipefail

echo "=== [1/6] Preparing directory structure  ====================="
WORKDIR="/home/user/analytics"
NOTEBOOK_DIR="$WORKDIR/notebooks"
DATA_DIR="$WORKDIR/data"
VSCODE_DIR="$WORKDIR/.vscode"

# Start clean every time
rm -rf "$WORKDIR"
mkdir -p "$NOTEBOOK_DIR" "$DATA_DIR" "$VSCODE_DIR"

echo "=== [2/6] Creating sample notebooks & data ==================="
cat > "$NOTEBOOK_DIR/experiment_01.ipynb" <<'EOF'
{
 "cells": [],
 "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
 "nbformat": 4,
 "nbformat_minor": 2
}
EOF

cat > "$DATA_DIR/iris.csv" <<'EOF'
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
EOF

echo "=== [3/6] Adding minimal workspace settings =================="
cat > "$VSCODE_DIR/settings.json" <<'EOF'
{
  "python.languageServer": "Pylance",
  "jupyter.askForKernelRestart": false
}
EOF

echo "=== [4/6] Ensuring no existing workspace file exists ========="
WORKSPACE_FILE="$WORKDIR/data-science.code-workspace"
rm -f "$WORKSPACE_FILE"  # Must not exist in the **initial** state

echo "=== [5/6] Writing task instructions =========================="
cat > "$WORKDIR/.task_info.txt" <<'EOF'
VS Code Task:
Save the current folder as a workspace by choosing:
  File → Save Workspace As…
and store it as   data-science.code-workspace   in /home/user/analytics/
EOF
echo "   → Instruction file created: $WORKDIR/.task_info.txt"

echo "=== [6/6] Launching VS Code =================================="
if command -v code >/dev/null 2>&1; then
    # Open the *folder* (not a .code-workspace file) so user must save it
    code "$WORKDIR" &
    echo "VS Code launched with folder: $WORKDIR"
else
    echo "ERROR: 'code' (VS Code CLI) not found in PATH." >&2
    exit 1
fi