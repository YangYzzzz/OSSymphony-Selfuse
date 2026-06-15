#!/usr/bin/env bash
set -euo pipefail

################################################################################
# Initial Setup Script : "django_night_owl_initial.sh"
# Purpose  : Prepare a Django-style workspace and force VS Code to use a light
#            color theme so the user is motivated to switch to “Night Owl”.
################################################################################

echo "🛠  Preparing initial Night-Owl theme task ..."

# ------------------------------------------------------------------------------
# 1. Define helper variables
# ------------------------------------------------------------------------------
# Detect correct VS Code user-settings location (Linux/macOS/Windows WSL).
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    VSCODE_USER_DIR="$HOME/.config/Code/User"
else
    # Fallback for WSL or non-standard; adjust if necessary.
    VSCODE_USER_DIR="$HOME/.config/Code/User"
fi

WORKSPACE="$HOME/django_night_owl_project"
PROJECT_NAME="midnight_blog"

echo "VS Code user settings dir : $VSCODE_USER_DIR"
echo "Workspace dir             : $WORKSPACE"

# ------------------------------------------------------------------------------
# 2. Create workspace & sample Django-style structure
# ------------------------------------------------------------------------------
echo "📂 Creating Django-like project ..."
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/$PROJECT_NAME"
mkdir -p "$WORKSPACE/$PROJECT_NAME/templates"
mkdir -p "$WORKSPACE/$PROJECT_NAME/static/css"

# Simple Django-flavoured files
cat > "$WORKSPACE/manage.py" <<'EOF'
#!/usr/bin/env python
# Dummy manage.py for illustration only
if __name__ == "__main__":
    print("Hello Django Midnight World")
EOF

cat > "$WORKSPACE/$PROJECT_NAME/urls.py" <<'EOF'
from django.urls import path
urlpatterns = []
EOF

cat > "$WORKSPACE/requirements.txt" <<'EOF'
Django>=4.0
EOF

# ------------------------------------------------------------------------------
# 3. Force an eye-blinding light theme in user settings
# ------------------------------------------------------------------------------
echo "🎨 Applying bright theme to user settings ..."

mkdir -p "$VSCODE_USER_DIR"
SETTINGS_JSON="$VSCODE_USER_DIR/settings.json"

# If settings.json exists, preserve everything except the theme, otherwise create.
if command -v jq >/dev/null 2>&1 && [[ -f "$SETTINGS_JSON" ]]; then
    jq '.["workbench.colorTheme"]="Default Light+"' "$SETTINGS_JSON" > "${SETTINGS_JSON}.tmp"
    mv "${SETTINGS_JSON}.tmp" "$SETTINGS_JSON"
else
    cat > "$SETTINGS_JSON" <<'EOF'
{
  "workbench.colorTheme": "Default Light+",
  "editor.fontSize": 14
}
EOF
fi

# ------------------------------------------------------------------------------
# 4. Verification (ensure theme is NOT Night Owl)
# ------------------------------------------------------------------------------
CURRENT_THEME=$(jq -r '."workbench.colorTheme"' "$SETTINGS_JSON" 2>/dev/null || echo "Unknown")
echo "✅ Current theme after setup: $CURRENT_THEME"

if [[ "$CURRENT_THEME" == "Night Owl" ]]; then
    echo "❌ Theme is already Night Owl – initial state invalid."
    exit 1
fi

# ------------------------------------------------------------------------------
# 5. Task marker – tells the user what to do
# ------------------------------------------------------------------------------
echo "Change the VS Code color theme to \"Night Owl\" for better night coding." \
  > "$WORKSPACE/.TASK_INSTRUCTIONS.txt"

# ------------------------------------------------------------------------------
# 6. Open VS Code on the prepared workspace
# ------------------------------------------------------------------------------
echo "🚀 Launching VS Code ..."
code "$WORKSPACE" &

echo "🟢 Initial setup complete – VS Code is running with a bright theme."