#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Initial VS Code task setup
# Goal for the learner:  add the folder “/home/user/shared” to the workspace.
###############################################################################

echo "=== Preparing initial workspace state ==="

# 1. Define paths -------------------------------------------------------------
WORKSPACE_ROOT="/home/user/project"
SHARED_FOLDER="/home/user/shared"
WORKSPACE_FILE="/home/user/project.code-workspace"

# 2. Clean-slate creation ------------------------------------------------------
echo "Creating workspace and shared directories..."
rm -rf "${WORKSPACE_ROOT}" "${SHARED_FOLDER}"
mkdir -p "${WORKSPACE_ROOT}" "${SHARED_FOLDER}"

# Populate the project with sample content
echo "console.log('Project main file');" > "${WORKSPACE_ROOT}/main.js"
echo "# Shared README"                    > "${SHARED_FOLDER}/README.md"

# 3. Create a .code-workspace file that ONLY contains the project folder ------
cat > "${WORKSPACE_FILE}" <<EOF
{
  "folders": [
    { "path": "/home/user/project" }
  ],
  "settings": {
    "files.exclude": {
      "**/*.tmp": true
    }
  }
}
EOF
echo "Workspace file created: ${WORKSPACE_FILE}"

# 4. Verification that shared folder is NOT yet in the workspace --------------
if jq -e '.folders[].path' "${WORKSPACE_FILE}" | grep -q "${SHARED_FOLDER}"; then
  echo "ERROR: Shared folder already present – something went wrong." >&2
  exit 1
fi
echo "Verified: shared folder is NOT in the workspace (expected initial state)."

# 5. Task instruction marker ---------------------------------------------------
echo "TASK: Add the folder \"/home/user/shared\" to the current workspace." \
  > "${WORKSPACE_ROOT}/.task_info.txt"

# 6. Launch VS Code with the workspace ----------------------------------------
echo "Opening VS Code... (initial state)"
code "${WORKSPACE_FILE}" &

echo "=== Initial setup complete – ready for user action ==="