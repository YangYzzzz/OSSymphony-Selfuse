#!/usr/bin/env bash
# ================================
#  initial_setup.sh
#  -------------------------------
#  Prepares the workspace that still
#  needs the “2-space tabs” fix.
# ================================
set -euo pipefail

echo "🔧  Preparing initial React workspace …"

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
WORKSPACE="$HOME/react_indent_task"
VSC_DIR="$WORKSPACE/.vscode"
SETTINGS_FILE="$VSC_DIR/settings.json"

# -------------------------------------------------------------------
# Clean & re-create workspace
# -------------------------------------------------------------------
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src" "$VSC_DIR"

# -------------------------------------------------------------------
# Sample source with bad indentation (4 spaces)
# -------------------------------------------------------------------
cat > "$WORKSPACE/src/App.jsx" <<'EOF'
    import React from 'react';

    function App() {
        return (
            <div>
                <h1>Hello World</h1>
            </div>
        );
    }

    export default App;
EOF

cat > "$WORKSPACE/src/index.js" <<'EOF'
        import React from 'react';
        import ReactDOM from 'react-dom/client';
        import App from './App';

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
EOF

# -------------------------------------------------------------------
# Intentionally wrong settings (uses 4-space hard tabs)
# -------------------------------------------------------------------
cat > "$SETTINGS_FILE" <<'EOF'
{
  "editor.insertSpaces": false,
  "editor.tabSize": 4,
  "files.autoSave": "off"
}
EOF

# -------------------------------------------------------------------
# Recommend Prettier in this workspace
# -------------------------------------------------------------------
cat > "$VSC_DIR/extensions.json" <<'EOF'
{
  "recommendations": ["esbenp.prettier-vscode"]
}
EOF

# -------------------------------------------------------------------
# Ensure the correct Prettier extension version is installed
# -------------------------------------------------------------------
echo "📦  Installing Prettier v10.0.0 …"
code --install-extension esbenp.prettier-vscode@10.0.0 --force >/dev/null

# -------------------------------------------------------------------
# Verification of initial state
# -------------------------------------------------------------------
echo "✅  Initial state verification:"
echo "    - Current tabSize   : $(jq '.["editor.tabSize"]' "$SETTINGS_FILE")"
echo "    - insertSpaces      : $(jq '.["editor.insertSpaces"]' "$SETTINGS_FILE")"
echo "    - Prettier version  : $(code --list-extensions --show-versions | grep esbenp.prettier-vscode || true)"

# -------------------------------------------------------------------
# Open VS Code
# -------------------------------------------------------------------
echo "🚀  Opening VS Code — workspace is READY for the task."
code "$WORKSPACE" & disown