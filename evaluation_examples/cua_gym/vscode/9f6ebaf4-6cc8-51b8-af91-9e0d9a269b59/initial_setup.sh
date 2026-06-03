#!/usr/bin/env bash
# ==============================================================
# VS Code Flask task – initial state (no requirements.txt)
# ==============================================================

set -euo pipefail

echo "▶ Setting up initial Flask project task..."

# --------------------------------------------------------------
# 1. Workspace location
# --------------------------------------------------------------
WORKSPACE="$HOME/vscode_flask_task"
if [ -d "$WORKSPACE" ]; then
  echo "   - Removing previous workspace at $WORKSPACE"
  rm -rf "$WORKSPACE"
fi
mkdir -p "$WORKSPACE/app"

# --------------------------------------------------------------
# 2. Project scaffold (minimal Flask app)
# --------------------------------------------------------------
cat > "$WORKSPACE/app/__init__.py" <<'PY'
from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello, Flask!"

    return app
PY

cat > "$WORKSPACE/README.md" <<'MD'
# Flask VS Code Task

Open VS Code → integrated terminal →  
`touch requirements.txt` (or `echo .. > requirements.txt`) and add: