#!/usr/bin/env bash
set -euo pipefail

###############################################################################
#  VS Code Web-Component Validation Task – INITIAL STATE
#  ----------------------------------------------------
#  1. Creates a small project using custom elements (<my-button>, <my-card>)
#  2. Does NOT configure VS Code to recognise those tags
#  3. Opens the workspace so red validation squiggles are visible
###############################################################################

echo "[INIT] Preparing Web-Component validation workspace …"

# Workspace location ----------------------------------------------------------
WORKSPACE="$HOME/webcomponents_project"
echo "[INIT] Workspace path: $WORKSPACE"

# (Re)create a clean workspace
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/.vscode"

# Sample HTML that triggers the warnings --------------------------------------
cat > "$WORKSPACE/index.html" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Web Components Demo</title>
  <script type="module" src="components.js"></script>
</head>
<body>
  <!-- The two lines below will have red squiggles in VS Code initially -->
  <my-button label="Click me"></my-button>
  <my-card title="Hello Web Components">
    <p>This is a custom card component.</p>
  </my-card>
</body>
</html>
EOF
echo "[INIT] Created index.html with <my-button> and <my-card>."

# Dummy JS file so project looks realistic ------------------------------------
cat > "$WORKSPACE/components.js" <<'EOF'
export class MyButton extends HTMLElement {
  connectedCallback() {
    this.textContent = this.getAttribute('label') || 'button';
  }
}
export class MyCard extends HTMLElement {
  connectedCallback() {
    this.innerHTML = \`<div class="card"><h3>\${this.getAttribute('title')}</h3><slot></slot></div>\`;
  }
}

customElements.define('my-button', MyButton);
customElements.define('my-card',   MyCard);
EOF

# Minimal workspace settings (no customData yet) ------------------------------
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
  // Intentionally empty so VS Code shows the default validation warnings.
}
EOF
echo "[INIT] Added empty .vscode/settings.json"

# Verification ----------------------------------------------------------------
if grep -q "<my-button" "$WORKSPACE/index.html"; then
  echo "[INIT] Verification passed: custom tags present in HTML."
else
  echo "[INIT] Verification FAILED: index.html missing custom tags!" >&2
  exit 1
fi

# Open VS Code ----------------------------------------------------------------
echo "[INIT] Opening VS Code – you should still see red squiggles for the custom tags."
code "$WORKSPACE" &

echo "[INIT] Initial setup completed."