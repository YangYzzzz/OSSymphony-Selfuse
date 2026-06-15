#!/usr/bin/env bash
###############################################################################
# Initial Setup Script
#   1. Creates workspace folder /home/user/scripts        (if it doesn't exist)
#   2. Populates it with a realistic file (backup.sh) and a README
#   3. ENSURES deploy.sh does NOT exist (so the user has to create it)
#   4. Launches VS Code opening /home/user/scripts
###############################################################################
set -euo pipefail

echo "=== VS Code Task – Initial Setup ==="

TARGET_DIR="/home/user/scripts"
DEPLOY_FILE="$TARGET_DIR/deploy.sh"

# 1. Create workspace directory structure
echo "Creating workspace directory: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

# 2. Populate with sample content
echo "Generating sample files ..."
cat > "$TARGET_DIR/backup.sh" << 'EOF'
#!/usr/bin/env bash
# Simple backup script
tar -czf "$HOME"/backup_$(date +"%Y%m%d").tar.gz "$HOME"/important_data
EOF
chmod +x "$TARGET_DIR/backup.sh"

cat > "$TARGET_DIR/README.md" << 'EOF'
# Scripts Workspace

This folder will eventually contain various automation scripts for the web
application. Your task: add **deploy.sh** to handle deployment steps.
EOF

# 3. GUARANTEE deploy.sh is absent
if [[ -e "$DEPLOY_FILE" ]]; then
  echo "Removing existing deploy.sh to create the task scenario."
  rm -f "$DEPLOY_FILE"
fi

# Verification step
if [[ -e "$DEPLOY_FILE" ]]; then
  echo "[ERROR] deploy.sh still exists. Setup invalid." >&2
  exit 1
else
  echo "[OK] Verified that deploy.sh is NOT present."
fi

# Optional task hint file (not required by VS Code; purely instructional)
echo "Create a new shell script named 'deploy.sh' in this folder." > "$TARGET_DIR/.task_info.txt"

# 4. Open VS Code
echo "Opening VS Code ..."
code "$TARGET_DIR" &

echo "=== Initial setup complete. VS Code should now display the workspace without deploy.sh ==="