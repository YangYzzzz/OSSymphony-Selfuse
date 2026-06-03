#!/usr/bin/env bash
# /home/user/project/.vscode_task_initial.sh
# Purpose : Create a workspace at /home/user/project with a Python file
#           whose lines 11-17 need two extra spaces of indentation.

set -euo pipefail

echo "==============  VS Code Indentation Task – Initial State  =============="

# --------------------------------------------------------------------------
# 1. Re-create the exact workspace directory structure
# --------------------------------------------------------------------------
WORKSPACE="/home/user/project"
echo "Re-creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE"

# --------------------------------------------------------------------------
# 2. Create main.py with incorrectly-indented lines 11-17
# --------------------------------------------------------------------------
cat > "$WORKSPACE/main.py" << 'EOF'
def calculate(numbers):
    total = 0
    for n in numbers:
        total += n
    average = total / len(numbers)
    info = {
        "total": total,
        "average": average,
        "count": len(numbers)
        }
print("Computation complete")
return info

def main():
numbers = [1, 2, 3, 4, 5]
result = calculate(numbers)
print(result)

if __name__ == "__main__":
    main()
EOF
echo "Created main.py with intentionally bad indentation (lines 11-17)."

# --------------------------------------------------------------------------
# 3. Create a short README so the workspace feels realistic
# --------------------------------------------------------------------------
echo "# Sample Project" > "$WORKSPACE/README.md"

# --------------------------------------------------------------------------
# 4. Verification – show the problematic lines
# --------------------------------------------------------------------------
echo
echo ">>> Showing lines 11-17 that need fixing:"
sed -n '11,17p' "$WORKSPACE/main.py" | nl -ba
echo

# --------------------------------------------------------------------------
# 5. Task marker – lets the learner know what to do
# --------------------------------------------------------------------------
echo "Add two spaces of indentation to lines 11 through 17 in main.py" \
  > "$WORKSPACE/.task_info.txt"

# --------------------------------------------------------------------------
# 6. Open VS Code on the workspace
# --------------------------------------------------------------------------
echo "Opening VS Code ..."
code "$WORKSPACE" &

echo "======================================================================="
echo "Initial environment ready – perform the indentation fix in VS Code."