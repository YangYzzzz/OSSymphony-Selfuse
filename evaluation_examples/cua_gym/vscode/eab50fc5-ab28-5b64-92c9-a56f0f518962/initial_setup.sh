#!/usr/bin/env bash
# -------------------------------------------------------------
#  VS Code Task – Initial State
#  Goal: Create a Django-style workspace where the Pylint
#        extension is INSTALLED and actively linting.
# -------------------------------------------------------------
set -euo pipefail

echo "========== VS Code – Initial Pylint ENABLED state =========="

# ------------------------------------------------------------------
# 1. Create a realistic Django-style workspace
# ------------------------------------------------------------------
WORKSPACE="$HOME/django_refactor_project"
echo "Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/myapp"
mkdir -p "$WORKSPACE/.vscode"

# Basic Django-style files (very tiny stubs)
cat > "$WORKSPACE/manage.py" <<'EOF'
#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django not installed") from exc
    execute_from_command_line(sys.argv)
if __name__ == '__main__':
    main()
EOF

cat > "$WORKSPACE/myapp/__init__.py" <<'EOF'
# Django app init
EOF

cat > "$WORKSPACE/myapp/views.py" <<'EOF'
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world!")
EOF

# ------------------------------------------------------------------
# 2. VS Code workspace settings – Pylint explicitly ENABLED
# ------------------------------------------------------------------
SETTINGS_FILE="$WORKSPACE/.vscode/settings.json"
cat > "$SETTINGS_FILE" <<'EOF'
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.pythonPath": "python3",
  "editor.formatOnSave": false
}
EOF
echo "Created VS Code settings with pylintEnabled = true"

# ------------------------------------------------------------------
# 3. Ensure Pylint extension is installed
# ------------------------------------------------------------------
echo "Installing required VS Code extensions (if not yet present)..."
code --install-extension ms-python.python --force >/dev/null
code --install-extension ms-python.pylint --force  >/dev/null
echo "Extensions installed (ms-python.python, ms-python.pylint)"

# ------------------------------------------------------------------
# 4. Verification
# ------------------------------------------------------------------
echo -n "Verifying Pylint extension is present... "
if code --list-extensions | grep -q "^ms-python.pylint$"; then
    echo "OK"
else
    echo "FAILED – extension missing" && exit 1
fi

echo -n "Verifying settings.json has pylintEnabled = true... "
if grep -q '"python.linting.pylintEnabled": *true' "$SETTINGS_FILE"; then
    echo "OK"
else
    echo "FAILED – setting not found" && exit 1
fi

# ------------------------------------------------------------------
# 5. Open VS Code in this workspace
# ------------------------------------------------------------------
echo "Opening VS Code – you should see Pylint diagnostics/pop-ups..."
code "$WORKSPACE" &

echo "========== Initial setup complete =========="