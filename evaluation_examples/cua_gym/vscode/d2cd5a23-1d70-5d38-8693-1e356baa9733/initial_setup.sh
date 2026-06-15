#!/usr/bin/env bash
# initial_setup.sh
# Purpose: Prepare a workspace with deeply-nested JS code and make sure
#          “Bracket Pair Colorizer 2” is NOT installed so the user
#          can perform the installation task in VS Code.

set -euo pipefail

echo "=== Bracket-Pair Colorizer TASK: Initial Setup ==="

# 1. Workspace location
WORKSPACE="$HOME/vscode_bracket_colorizer_task"
echo "Workspace directory: $WORKSPACE"

# 2. Re-create clean workspace
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src"

# 3. Provide a nested JavaScript file that begs for bracket colors
cat > "$WORKSPACE/src/nested.js" << 'EOF'
function outer() {
    function levelOne() {
        function levelTwo() {
            if (true) {
                const obj = {
                    key1: [1, 2, 3].map(n => {
                        return () => {
                            console.log("Level three:", n);
                        };
                    }),
                    key2: (() => {
                        return function deep() {
                            return { value: "Deeply nested!" };
                        };
                    })()
                };
                return obj;
            }
        }
        return levelTwo();
    }
    return levelOne();
}
outer();
EOF
echo "Created sample file: src/nested.js"

# 4. Create a task hint for the user
echo "Install the VS Code extension: Bracket Pair Colorizer 2" \
  > "$WORKSPACE/.task_info.txt"

# 5. Ensure the extension is NOT installed
echo "Ensuring the extension 'CoenraadS.bracket-pair-colorizer-2' is not installed..."
if code --list-extensions | grep -q 'CoenraadS.bracket-pair-colorizer-2'; then
    code --uninstall-extension CoenraadS.bracket-pair-colorizer-2 --force
    echo "Existing extension removed."
else
    echo "Extension was not present."
fi

# Verification
if code --list-extensions | grep -q 'CoenraadS.bracket-pair-colorizer-2'; then
    echo "ERROR: Extension still present after attempted removal"; exit 1
fi
echo "Verification passed: Extension is NOT installed."

# 6. Open VS Code for the user
echo "Opening VS Code..."
code "$WORKSPACE" &

echo "=== Initial setup complete. Ready for user action. ==="