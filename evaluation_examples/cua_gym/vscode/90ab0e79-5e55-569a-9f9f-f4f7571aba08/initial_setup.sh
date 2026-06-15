#!/usr/bin/env bash
# ------------------------------------------------
# Initial VS Code workspace preparation script
# ------------------------------------------------
set -euo pipefail

echo "=== Creating initial ML workspace ==="

WORKSPACE="/home/user/ml-projects"

# 1. Re-create a clean workspace
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"

# 2. Add a small Python file that produces a NumPy array
cat > "$WORKSPACE/arrays.py" <<'EOF'
import numpy as np

def main():
    a = np.random.rand(5, 5)
    print("Generated NumPy array:")
    print(a)

if __name__ == "__main__":
    main()
EOF

# 3. Pin NumPy in requirements (optional for user to install)
echo "numpy==1.26.4" > "$WORKSPACE/requirements.txt"

# 4. Minimal VS Code folder – **no** Python/Jupyter extension yet
mkdir -p "$WORKSPACE/.vscode"
cat > "$WORKSPACE/.vscode/settings.json" <<'EOF'
{
    // Starting point – Data Viewer not yet available
    "python.analysis.typeCheckingMode": "off"
}
EOF

# 5. Task marker so the user knows what to do
echo "TASK: Install Python & Jupyter extensions so Data Viewer works with NumPy arrays." \
  > "$WORKSPACE/.task_info.txt"

# 6. Verification
if [[ -d "$WORKSPACE" && -f "$WORKSPACE/arrays.py" ]]; then
  echo "Verification OK: workspace and sample file created."
else
  echo "Verification FAILED: workspace not set up correctly." >&2
  exit 1
fi

# 7. Open VS Code so the user can complete the task
code "$WORKSPACE" &
echo "VS Code launched. The environment is ready for the user to enable the Data Viewer."