#!/usr/bin/env bash
#============================================================
#  VS Code Flask Scaffold – INITIAL STATE
#------------------------------------------------------------
#  Creates a workspace that still needs:
#   • src/app.py
#   • src/templates/ folder
#   • .vscode/launch.json debug configuration
#
#  A human learner will open VS Code, add those pieces,
#  then press F5 to run the server.
#============================================================
set -euo pipefail

echo "📦  Preparing initial Flask-scaffold task …"

#------------------------------------------------------------
# Workspace layout
#------------------------------------------------------------
WORKSPACE="$HOME/vscode_flask_task"
rm -rf "$WORKSPACE"           # start clean every run
mkdir -p "$WORKSPACE/src"     # create empty src directory
mkdir -p "$WORKSPACE/.vscode" # but no launch.json yet

# Basic project files
echo "# VS Code Flask Scaffold Task" > "$WORKSPACE/README.md"
echo "Flask==2.3.3"           > "$WORKSPACE/requirements.txt"

# Short task reminder for the learner
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
Your mission:
1. Under src/ create app.py with a minimal “Hello, Flask!” application.
2. Inside src/ create templates/ for Jinja2 templates (e.g. index.html).
3. Add .vscode/launch.json so that F5 (Python → Flask) runs the server.
Hints:
• Use “Python: Flask” debug template in the Command Palette (⇧⌘P / Ctrl+Shift+P).
• Set FLASK_APP to "src.app" in the launch configuration.
EOF

#------------------------------------------------------------
# Verification of initial state
#------------------------------------------------------------
echo "🔍  Verifying initial state …"
if [ -e "$WORKSPACE/src/app.py" ]; then
  echo "⚠️  app.py should NOT exist yet – removing."
  rm -f "$WORKSPACE/src/app.py"
fi
echo "   Expected empty src/:"
ls -R "$WORKSPACE/src" || true

echo "✅  Initial workspace ready at $WORKSPACE"

#------------------------------------------------------------
# Open VS Code for the learner
#------------------------------------------------------------
code "$WORKSPACE" & disown