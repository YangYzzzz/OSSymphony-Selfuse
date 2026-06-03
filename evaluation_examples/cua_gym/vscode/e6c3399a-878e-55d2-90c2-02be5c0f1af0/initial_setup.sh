#!/usr/bin/env bash
###############################################################################
# Initial Setup Script
# Purpose : Create a realistic data-science repo that lacks the Jupyter
#           extension so the user’s task is to install it.
###############################################################################
set -euo pipefail

echo "===== VS Code Jupyter-Extension Task : Initial Setup ====="

# -----------------------------------------------------------------------------
# 0. Variables
# -----------------------------------------------------------------------------
WORKSPACE="$HOME/datascience_repo"          # Folder that will be opened in VS Code
VSCODE_USER_DIR="$HOME/.config/Code/User"   # User-level VS Code config (Linux/macOS)
NOTEBOOK="$WORKSPACE/notebooks/EDA.ipynb"   # Sample notebook path
EXTENSION_ID="ms-toolsai.jupyter"           # Official Jupyter extension ID

# -----------------------------------------------------------------------------
# 1. Clean slate (re-run safety)
# -----------------------------------------------------------------------------
echo "Cleaning any previous state…"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/notebooks"
mkdir -p "$WORKSPACE/.vscode"
mkdir -p "$VSCODE_USER_DIR"   # Ensure dir exists for later checks

# -----------------------------------------------------------------------------
# 2. Ensure the Jupyter extension is *NOT* installed
#    (If already installed on this box, uninstall it so the task is genuine.)
# -----------------------------------------------------------------------------
if code --list-extensions | grep -q "$EXTENSION_ID"; then
  echo "Jupyter extension already installed → uninstalling to create task scenario"
  code --uninstall-extension "$EXTENSION_ID" || true
else
  echo "Confirmed Jupyter extension is NOT installed."
fi

# -----------------------------------------------------------------------------
# 3. Create a minimal sample notebook (valid JSON)
# -----------------------------------------------------------------------------
cat > "$NOTEBOOK" <<'EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["# Exploratory Data Analysis"]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": ["import pandas as pd\n", "pd.DataFrame({'A':[1,2,3]})"]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.x"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF
echo "Sample notebook created at $NOTEBOOK"

# -----------------------------------------------------------------------------
# 4. Workspace settings – intentionally *no* Jupyter recommendation
# -----------------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  "recommendations": [
    "ms-python.python"           // Python extension only
  ]
}
EOF

# -----------------------------------------------------------------------------
# 5. Task marker (human-readable)
# -----------------------------------------------------------------------------
echo "Install the official 'Jupyter' extension (ms-toolsai.jupyter) to run notebooks." > "$WORKSPACE/.task_info.txt"

# -----------------------------------------------------------------------------
# 6. Open VS Code
# -----------------------------------------------------------------------------
echo "Opening VS Code…"
code "$WORKSPACE" &

echo "===== Initial setup complete. VS Code opened without the Jupyter extension ====="