#!/usr/bin/env bash
###############################################################################
# initial_setup.sh – prepares ~/dev/bot-app in an unfinished state            #
###############################################################################
set -euo pipefail

echo "🛠  Preparing initial workspace for VS Code plugin-manager task..."

# ------------------------------------------------------------------ #
# 1. Create clean workspace skeleton                                 #
# ------------------------------------------------------------------ #
WORKSPACE="$HOME/dev/bot-app"
echo "📂 Creating workspace at: $WORKSPACE"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE/src/plugins"      # real plugins dir
mkdir -p "$WORKSPACE/src/utils"        # utils dir (plugins.js missing)
mkdir -p "$WORKSPACE/.vscode"

# ------------------------------------------------------------------ #
# 2. Seed minimal Node.js project                                    #
# ------------------------------------------------------------------ #
cat > "$WORKSPACE/package.json" << 'EOF'
{
  "name": "bot-app",
  "version": "0.1.0",
  "type": "module",
  "main": "src/index.js",
  "dependencies": {
    "express": "^4.19.2"
  },
  "scripts": {
    "start": "node src/index.js"
  }
}
EOF

cat > "$WORKSPACE/src/index.js" << 'EOF'
import express from 'express';
import { pluginMiddleware } from './utils/plugins.js'; // <--- NOT YET PRESENT

const app = express();
app.use(pluginMiddleware());          // this will fail until user adds file

app.get('/', (req, res) => res.send('Bot-App root OK'));
app.listen(3000, () => console.log('Listening on http://localhost:3000'));
EOF

# ------------------------------------------------------------------ #
# 3. VS Code settings – intentionally minimal (needs update)         #
# ------------------------------------------------------------------ #
cat > "$WORKSPACE/.vscode/settings.json" << 'EOF'
{
  // TODO: Configure Prettier once plugin-manager file is added
}
EOF

# ------------------------------------------------------------------ #
# 4. Task hint for the learner                                       #
# ------------------------------------------------------------------ #
cat > "$WORKSPACE/.TASK_INFO.txt" << 'EOF'
⚠️  Missing file: src/utils/plugins.js
   – Must register "auth" and "logger" plugins and compose middleware.

VS Code settings also need Prettier v10.1.0 configuration.
EOF

# ------------------------------------------------------------------ #
# 5. Quick verification                                              #
# ------------------------------------------------------------------ #
if [[ -f "$WORKSPACE/src/utils/plugins.js" ]]; then
  echo "❌ plugins.js already exists – initial state invalid"; exit 1;
else
  echo "✅ Verified: plugins.js is NOT present (as expected)."
fi

# ------------------------------------------------------------------ #
# 6. Open VS Code                                                    #
# ------------------------------------------------------------------ #
echo "🚀 Launching VS Code..."
code "$WORKSPACE" &>/dev/null &
sleep 2
echo "✅ Initial setup complete – workspace opened in VS Code."