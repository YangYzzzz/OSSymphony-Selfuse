#!/usr/bin/env bash
# ------------------------------------------------------------------
# create_task_env.sh
# ------------------------------------------------------------------
# Prepares a workspace where the user still needs to generate an
# MIT LICENSE file via the “LICENSE Template Generator” extension.
# ------------------------------------------------------------------
set -euo pipefail

echo "🔧  Setting up VS Code LICENSE-generation task …"

# ------------------------------------------------------------------
# 1. Create workspace skeleton
# ------------------------------------------------------------------
WORKSPACE="$HOME/vscode_license_task"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/src" "$WORKSPACE/.vscode"

echo "# Acme Project"                        >  "$WORKSPACE/README.md"
echo "console.log('Hello, world');"          >  "$WORKSPACE/src/index.js"

# ------------------------------------------------------------------
# 2. Recommend the extension (so VS Code prompts user to install it)
#    ⚠️  We DO NOT force-install the extension here in case the
#       marketplace is unreachable.  It is only *recommended*.
# ------------------------------------------------------------------
cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  // VS Code will prompt the user to install the recommeded extension.
  "recommendations": [
    "pragmaticjenkins.license-template-generator" // “LICENSE Template Generator” v1.3.4
  ]
}
EOF
echo "🧩  Extension recommendation written → .vscode/extensions.json"

# ------------------------------------------------------------------
# 3. Create task description for human user (not used by VS Code)
# ------------------------------------------------------------------
cat > "$WORKSPACE/.task_info.txt" <<'EOF'
TASK: Use the “LICENSE Template Generator” (v1.3.4) to create a new
LICENSE file in the workspace root:
  • Choose “MIT” as the license type
  • Ensure the header reads:   Copyright © 2024 Acme Corp
EOF

# ------------------------------------------------------------------
# 4. Verification of initial state
# ------------------------------------------------------------------
if [[ -f "$WORKSPACE/LICENSE" ]]; then
  echo "❌  A LICENSE file already exists – this should be an empty start."
  exit 1
fi
echo "✅  Verified: No LICENSE file exists yet."

# ------------------------------------------------------------------
# 5. Launch VS Code so the user can complete the task
# ------------------------------------------------------------------
echo "🚀  Opening VS Code…"
code "$WORKSPACE" &> /dev/null &
sleep 2
echo "✅  Workspace ready: $WORKSPACE"