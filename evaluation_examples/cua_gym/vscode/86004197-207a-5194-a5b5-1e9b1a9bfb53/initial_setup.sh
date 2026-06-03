#!/usr/bin/env bash
###############################################################################
# initial_setup.sh – Prepares workspace where “foo” must be bulk–replaced
###############################################################################
set -euo pipefail

echo "🛠  Preparing VS Code bulk-replace task (initial state)…"

# -----------------------------------------------------------------------------
# 1. Create workspace skeleton
# -----------------------------------------------------------------------------
WORKSPACE="$HOME/foo_to_bar_project"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src/utils" "$WORKSPACE/.vscode"

# -----------------------------------------------------------------------------
# 2. Node project boiler-plate
# -----------------------------------------------------------------------------
cat > "$WORKSPACE/package.json" << 'EOF'
{
  "name": "foo-to-bar-demo",
  "version": "1.0.0",
  "description": "Demo project for bulk replacing 'foo' with 'bar' in VS Code",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "author": "Demo",
  "license": "MIT"
}
EOF

cat > "$WORKSPACE/index.js" << 'EOF'
/**
 * Entry file – intentionally contains the word foo but should NOT be changed
 */
function greet() {
  console.log("foo should stay here in index.js!");
}
greet();
EOF

# -----------------------------------------------------------------------------
# 3. Target file that really needs editing
# -----------------------------------------------------------------------------
cat > "$WORKSPACE/src/utils/replaceFoo.js" << 'EOF'
/**
 * Utility that still uses the legacy word "foo" 😱
 * All instances of "foo" in THIS file must become "bar".
 */

export function transform(input) {
  // Simple example usage
  const fooRegex = /foo/g;
  return input.replace(fooRegex, "foo").toUpperCase() + " foo!!!";
}

// Another stray usage
const foo = "foo-will-change";
console.log(foo);
EOF

# -----------------------------------------------------------------------------
# 4. One more decoy file that should remain untouched
# -----------------------------------------------------------------------------
cat > "$WORKSPACE/src/utils/helper.js" << 'EOF'
// This file also mentions foo but should NOT be affected
export const sample = "keep foo here";
EOF

# -----------------------------------------------------------------------------
# 5. VS Code configuration – recommend Prettier and set default formatter
# -----------------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/extensions.json" << 'EOF'
{
  "recommendations": [
    "esbenp.prettier-vscode"   // v9.12.0
  ]
}
EOF

cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "prettier.singleQuote": true
}
EOF

# -----------------------------------------------------------------------------
# 6. Verification snapshot (should show multiple “foo” in target file)
# -----------------------------------------------------------------------------
FOO_COUNT=$(grep -o "foo" "$WORKSPACE/src/utils/replaceFoo.js" | wc -l)
echo "👉 Initial count of 'foo' in replaceFoo.js: $FOO_COUNT (expected > 0)"
if [ "$FOO_COUNT" -eq 0 ]; then
  echo "ERROR: No occurrences of 'foo' created – aborting."
  exit 1
fi

# -----------------------------------------------------------------------------
# 7. Task marker file – visible in Explorer
# -----------------------------------------------------------------------------
cat > "$WORKSPACE/TASK_INSTRUCTIONS.txt" << 'EOF'
VS Code Task – Bulk Replace
------------------------------------------------
Goal: Using Ctrl+Shift+H (Search & Replace in Files),
replace every occurrence of "foo" with "bar" ONLY in:
   /src/utils/replaceFoo.js

• Be sure “files to include” filter is set to **src/utils/replaceFoo.js**
• Leave all other files (index.js, helper.js, …) unchanged
• Save the file (Prettier will format automatically)
EOF

# -----------------------------------------------------------------------------
# 8. Open workspace in VS Code for the user
# -----------------------------------------------------------------------------
echo "🚀 Opening VS Code…"
code "$WORKSPACE" &

echo "✅ Initial setup complete."