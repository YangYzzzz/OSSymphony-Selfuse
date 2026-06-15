#!/usr/bin/env bash
set -euo pipefail

echo "================  VS Code – AUTO-OPEN  SETUP (INITIAL STATE)  ================"

# 1. Create the playground folder that the user normally works in
echo "[*] Creating workspace folder:  /home/user/playground"
mkdir -p "/home/user/playground"

# 2. Put some placeholder content in the folder so it looks realistic
cat > "/home/user/playground/README.md" <<'EOF'
# Playground
This is your personal JavaScript sandbox.  
The goal of this task is to make VS Code automatically open a **fresh**
file called **app.js** here every time it starts.
EOF

# 3. Make sure **app.js** does NOT exist yet – the user will create it later
rm -f "/home/user/playground/app.js"

# 4. Clean up any previous alias/wrapper so the feature is *not* active yet
sed -i '/# >>> VS CODE AUTO APP\.JS START >>>/,/# <<< VS CODE AUTO APP\.JS END <<</d' ~/.bashrc 2>/dev/null || true
rm -f ~/.local/bin/code-auto-open 2>/dev/null || true

# 5. Drop a small task-reminder file
echo "Goal: Configure VS Code so that each launch automatically opens /home/user/playground/app.js" \
    > "/home/user/playground/TASK.md"

# 6. Final user message
echo "[✓] Initial environment ready."
echo "    - /home/user/playground exists"
echo "    - No special VS Code auto-open behaviour yet"

# 7. Open VS Code *normally* to show the current behaviour (no auto file)
code "/home/user/playground" &

sleep 2
echo "VS Code started WITHOUT automatically opening app.js – task still pending."