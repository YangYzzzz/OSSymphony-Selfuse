#!/usr/bin/env bash
# File: init_setup.sh
set -euo pipefail

echo "===== VS Code Matplotlib Inline-Plot Task: Initial State ====="

# Absolute workspace path (must match task spec verbatim)
WORKSPACE="/home/user/plots"

echo "Creating/Resetting workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/.vscode"

###############################################################################
# 1.  Sample Python file that opens a Matplotlib figure with plt.show()
###############################################################################
cat > "$WORKSPACE/analysis.py" << 'EOF'
import matplotlib.pyplot as plt
import numpy as np

# Simple sine wave plot
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure()
plt.plot(x, y, label="sin(x)")
plt.title("Sine Wave")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

# This call opens an external window when the backend isn't "inline"
plt.show()
EOF
echo "Created: $WORKSPACE/analysis.py"

###############################################################################
# 2.  VS Code workspace settings – backend deliberately *not* inline
###############################################################################
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
    // Default setting — causes plots to pop out in an external window
    "python.plotting.backend": "auto"
}
EOF
echo "Created: $WORKSPACE/.vscode/settings.json (backend set to 'auto')"

###############################################################################
# 3.  Task marker for the learner
###############################################################################
cat > "$WORKSPACE/.task_info.txt" << 'EOF'
TASK: Configure VS Code so every Matplotlib chart renders inline.
Hint: Search for "Matplotlib Backend" in the Python extension settings.
EOF
echo "Created: $WORKSPACE/.task_info.txt"

###############################################################################
# 4.  Launch VS Code pointing at the workspace
###############################################################################
echo "Opening VS Code..."
code "$WORKSPACE" &

###############################################################################
# 5.  Verification
###############################################################################
sleep 2   # give VS Code a moment to start
if grep -q '"python.plotting.backend": "auto"' "$WORKSPACE/.vscode/settings.json"; then
    echo "Verified: backend is currently 'auto' (external window expected)."
else
    echo "Initial verification failed – settings.json not as expected." >&2
    exit 1
fi

echo "===== Initial state ready – user should switch backend to 'inline' ====="