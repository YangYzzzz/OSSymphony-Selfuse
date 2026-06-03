#!/usr/bin/env bash
# ------------------------------------------------------------------
#  create_initial_state.sh
# ------------------------------------------------------------------
#  Prepares the workspace for the VS Code task:
#  “Replace every instance of the word ‘database’ with ‘db’ in
#   /home/user/app/config.py”.
#
#  1. Creates a realistic Flask‐style project structure.
#  2. Populates /home/user/app/config.py with multiple occurrences
#     of the word “database”.
#  3. Opens VS Code on /home/user/app so the user can carry out the
#     replacement using the GUI.
#  4. Verifies that the word “database” is indeed present prior to
#     the task.
# ------------------------------------------------------------------
set -euo pipefail

echo ">>> [SETUP] Creating initial workspace ..."

# Absolute path demanded by the task
WORKSPACE="/home/user/app"

# Fresh start (do NOT use ~ or \$HOME – honour exact path)
if [ -d "$WORKSPACE" ]; then
    echo "    Removing existing workspace at $WORKSPACE (clean slate)"
    rm -rf "$WORKSPACE"
fi
mkdir -p "$WORKSPACE"

# ------------------------------------------------------------------
# Create realistic Flask project files
# ------------------------------------------------------------------
cat > "$WORKSPACE/config.py" << 'EOF'
"""
Flask configuration module.
The word 'database' deliberately appears several times and
needs to be shortened to 'db'.
"""

import os

class Config:
    # Main database URI
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.sqlite3")

    # Enable/disable tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Another random configuration referencing 'database'
    CUSTOM_DATABASE_TIMEOUT = 30
EOF

cat > "$WORKSPACE/app.py" << 'EOF'
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
EOF

echo ">>> [SETUP] Project files generated."

# ------------------------------------------------------------------
# Verification – confirm "database" exists so the task makes sense
# ------------------------------------------------------------------
if grep -q "database" "$WORKSPACE/config.py"; then
    echo ">>> [VERIFY] 'database' occurrences detected (as expected)."
else
    echo ">>> [ERROR] Expected word 'database' not found in config.py!"
    exit 1
fi

# ------------------------------------------------------------------
# Optional task hint for the user (not required by grading)
# ------------------------------------------------------------------
echo "Replace every instance of the word 'database' with 'db' in config.py" \
    > "$WORKSPACE/.task_info.txt"

# ------------------------------------------------------------------
# Open VS Code
# ------------------------------------------------------------------
echo ">>> [VS CODE] Opening VS Code on $WORKSPACE ..."
code "$WORKSPACE" &

echo ">>> [DONE] Initial environment ready. Perform the replacement in VS Code."