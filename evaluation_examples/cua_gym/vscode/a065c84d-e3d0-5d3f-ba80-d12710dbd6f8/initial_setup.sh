#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial VS Code Task Setup
# 1. Creates the folder /home/user/projects
# 2. Generates /home/user/projects/backup.py with lines 14-21 indented by ONE tab
# 3. Drops a task hint file explaining what needs to be done
# 4. Verifies that the indentation is exactly one tab on lines 14-21
# 5. Opens VS Code pointed at /home/user/projects
###############################################################################

PROJECT_DIR="/home/user/projects"
PY_FILE="$PROJECT_DIR/backup.py"

echo "⏳  Preparing initial workspace …"
mkdir -p "$PROJECT_DIR"

echo "⏳  Creating source file: $PY_FILE"
# --------------------------------------------------------------------------- #
# Lines 14-21 are intentionally indented with ONE leading TAB
# --------------------------------------------------------------------------- #
cat > "$PY_FILE" <<'EOF'
import os
import shutil
from datetime import datetime


def backup(src, dest):
    """
    Simple backup function that copies all files from src to dest.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(dest, f"backup_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)

	for root, dirs, files in os.walk(src):
		rel_path = os.path.relpath(root, src)
		target_dir = os.path.join(backup_dir, rel_path)
		os.makedirs(target_dir, exist_ok=True)
		for file in files:
			full_path = os.path.join(root, file)
			shutil.copy2(full_path, os.path.join(target_dir, file))

    print(f"Backup created at {backup_dir}")


if __name__ == "__main__":
    SRC = "/home/user/data"
    DEST = "/home/user/backups"
    backup(SRC, DEST)


# End of file
EOF

echo "ℹ️  Creating task hint"
echo "VS Code Task: Shift the indentation of lines 14-21 in backup.py one TAB to the right." \
  > "$PROJECT_DIR/.task_info.txt"

###############################################################################
# QUICK VERIFICATION (initial state)
# Confirm that lines 14-21 have exactly ONE leading tab
###############################################################################
echo "🔍  Verifying initial indentation …"
wrong_lines=0
while read -r line_info; do
    line_no=$(echo "$line_info" | cut -d: -f1)
    content=$(echo "$line_info" | cut -d: -f2-)
    # Count leading TABs
    leading_tabs=$(printf "%s" "$content" | grep -oP '^\t*' | wc -c)
    if [[ $leading_tabs -ne 1 ]]; then
        echo "    ❌  Line $line_no does NOT have exactly 1 leading TAB"
        wrong_lines=$((wrong_lines+1))
    fi
done < <(sed -n '14,21p' "$PY_FILE" | nl -ba -w1 -s: | sed 's/^[ \t]*//')
if [[ $wrong_lines -eq 0 ]]; then
    echo "    ✅  All target lines have ONE leading TAB (as expected for start state)"
else
    echo "    ❌  Verification failed; aborting."
    exit 1
fi

###############################################################################
# Open VS Code
###############################################################################
echo "🚀  Launching VS Code …"
code "$PROJECT_DIR" & disown
echo "✅  Initial setup complete – perform the indentation shift in VS Code now."