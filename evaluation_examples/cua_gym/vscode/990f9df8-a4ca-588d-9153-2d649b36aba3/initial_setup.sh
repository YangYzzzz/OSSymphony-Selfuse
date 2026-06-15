#!/usr/bin/env bash
###############################################################################
# Initial Setup: Rainbow CSV Installation Task
# -------------------------------------------------------------
# This script prepares a VS Code workspace that contains a CSV file whose
# columns appear “mashed together.”  The user’s task will be to install the
# “Rainbow CSV” extension so the data is color-highlighted and easy to read.
#
# What the user will see after this script:
#   • A folder called  ~/rainbow_csv_task  opened in VS Code
#   • A large-looking CSV file (data.csv) with no syntax colouring
#   • A task note indicating:  “Install the Rainbow CSV extension”
###############################################################################
set -euo pipefail

EXTENSION_ID="mechatroner.rainbow-csv"
WORKSPACE_DIR="$HOME/rainbow_csv_task"
CSV_FILE="$WORKSPACE_DIR/data.csv"
TASK_NOTE="$WORKSPACE_DIR/.task_info.txt"

echo "=== Preparing workspace: $WORKSPACE_DIR ==="
rm -rf "$WORKSPACE_DIR"
mkdir -p "$WORKSPACE_DIR"

###############################################################################
# 1. Generate a realistic-looking CSV file (no quotes, no spaces, long lines)
###############################################################################
echo "Generating sample CSV file..."
cat > "$CSV_FILE" <<'EOF'
id,name,age,country,occupation,salary,year_started
1,Alice Johnson,31,United States,Data Scientist,134000,2016
2,Bob Lee,29,Canada,Mechanical Engineer,118500,2018
3,Carla Gómez,41,Mexico,Project Manager,98000,2010
4,David Zhang,35,China,Software Architect,152300,2014
5,Eva Müller,27,Germany,UX Designer,89000,2019
EOF

###############################################################################
# 2. Create a short task note for the learner
###############################################################################
echo "Install the VS Code extension: Rainbow CSV (ID: $EXTENSION_ID)" > "$TASK_NOTE"

###############################################################################
# 3. Verify that the Rainbow CSV extension is NOT installed
###############################################################################
echo "Checking that the extension '$EXTENSION_ID' is NOT installed (expected)..."
if code --list-extensions | grep -q "^${EXTENSION_ID}$"; then
  echo "WARNING: Extension '$EXTENSION_ID' already present. "
  echo "Uninstalling so the learner needs to install it."
  code --uninstall-extension "$EXTENSION_ID" || true
fi
echo "Extension not present – good."

###############################################################################
# 4. Open VS Code with the new workspace
###############################################################################
echo "Opening VS Code..."
code "$WORKSPACE_DIR" &

echo "=== Initial setup complete. VS Code is ready ==="