#!/usr/bin/env bash
set -euo pipefail

###############################################
# INITIAL SETUP SCRIPT — pwa_task_init.sh
###############################################
#!/usr/bin/env bash
set -euo pipefail

echo "🔧  Preparing PWA Service-Worker task (initial state)…"

# ----------------------------
# 1. Workspace skeleton
# ----------------------------
WORKSPACE="$HOME/pwa_service_worker_task"
rm -rf  "$WORKSPACE"
mkdir -p "$WORKSPACE/public" "$WORKSPACE/src" "$WORKSPACE/scripts" "$WORKSPACE/.vscode"

# ----------------------------
# 2. Application files
# ----------------------------
cat > "$WORKSPACE/public/index.html" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="manifest" href="/public/manifest.json">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>PWA Sample</title>
</head>
<body>
  <h1>PWA Sample App</h1>
  <p>Hello World – service-worker coming soon…</p>

  <script type="module" src="/src/app.js"></script>
  <script>
    /* Service-worker will 404 until the task is done */
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker
        .register('/public/sw.js')
        .then(reg => console.log('SW registered', reg))
        .catch(err => console.warn('SW registration failed (expected for now)', err));
    }
  </script>
</body>
</html>
EOF

cat > "$WORKSPACE/public/offline.html" <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Offline – PWA Sample</title>
  <style>
    body{font-family:sans-serif;text-align:center;padding-top:20vh;}
  </style>
</head>
<body>
  <h1>You are offline</h1>
  <p>Please check your connection and try again.</p>
</body>
</html>
EOF

cat > "$WORKSPACE/public/manifest.json" <<'EOF'
{
  "short_name": "PWASample",
  "name": "PWA Sample Application",
  "start_url": "/public/index.html",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": []
}
EOF

cat > "$WORKSPACE/src/app.js" <<'EOF'
console.log('🌟 App JS loaded');
EOF

# ----------------------------
# 3. Helper script shown via Command Palette
# ----------------------------
cat > "$WORKSPACE/scripts/show_sw_help.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cat <<'EOT'
========= PWA Service-Worker HOW-TO =========

Goal
  Create /public/sw.js implementing a cache-first strategy
  and serve /offline.html when the network is unavailable.

Steps
 1. Explorer (Ctrl+Shift+E) → public → New File → sw.js
 2. Paste the boilerplate code shown below.
 3. Save (Ctrl+S).
 4. Refresh the browser served by Live Server.  
    Disable network in DevTools and confirm /offline.html loads.
 5. Congrats – your PWA is now offline-ready! 🎉

Boilerplate to paste into sw.js
--------------------------------
const CACHE_NAME = 'pwa-cache-v1';
const OFFLINE_URL = '/public/offline.html';
const PRECACHE_RESOURCES = [
  '/',
  '/public/index.html',
  OFFLINE_URL,
  '/public/manifest.json',
  '/src/app.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_RESOURCES))
      .then(self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;

      return fetch(event.request)
        .then(resp => {
          const clone = resp.clone();
          caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
          return resp;
        })
        .catch(() => caches.match(OFFLINE_URL));
    })
  );
});
--------------------------------

Re-run this guide anytime:  
Ctrl+Shift+P → “Tasks: Run Task” → “PWA: Step-by-Step Service Worker Guide”
============================================
EOT
EOF
chmod +x "$WORKSPACE/scripts/show_sw_help.sh"

# ----------------------------
# 4. VS Code configuration
# ----------------------------
cat > "$WORKSPACE/.vscode/tasks.json" <<'EOF'
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "PWA: Step-by-Step Service Worker Guide",
      "type": "shell",
      "command": "${workspaceFolder}/scripts/show_sw_help.sh",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "panel": "shared"
      },
      "problemMatcher": []
    }
  ]
}
EOF

cat > "$WORKSPACE/.vscode/extensions.json" <<'EOF'
{
  "recommendations": ["ritwickdey.LiveServer"]
}
EOF

# Optional npm helper for running Live Server
cat > "$WORKSPACE/package.json" <<'EOF'
{
  "name": "pwa-sw-task",
  "version": "1.0.0",
  "scripts": {
    "start": "npx --yes live-server public --port=5500"
  }
}
EOF

# ----------------------------
# 5. Verification of initial state
# ----------------------------
if [[ -f "$WORKSPACE/public/sw.js" ]]; then
  echo "❌  sw.js should NOT exist in the initial state."
  exit 1
fi
echo "✅  Verified: sw.js is absent (as expected)."

# ----------------------------
# 6. Launch VS Code
# ----------------------------
echo "🚀  Opening workspace in VS Code…"
code "$WORKSPACE" &>/dev/null &

echo "✨  Initial setup completed."
echo "👉  In VS Code press Ctrl+Shift+P → Tasks: Run Task → PWA: Step-by-Step Service Worker Guide"