#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Baseline / initial environment – VLC starts with an empty playlist
# ------------------------------------------------------------------
VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"; touch "$VLCRC"

# Idempotent helper (kept for completeness – no keys changed here)
ensure_kv() {
  local key="$1"; local value="$2"
  if grep -qE "^[#;]?\s*${key}\s*=" "$VLCRC"; then
    sed -i "s|^[#;]?\s*${key}\s*=.*|${key}=${value}|g" "$VLCRC"
  else
    printf "\n%s=%s\n" "$key" "$value" >> "$VLCRC"
  fi
}

echo "[initial_setup] Closing any existing VLC instance …"
pkill vlc || true

echo "[initial_setup] No configuration keys modified – starting VLC clean."
DISPLAY=:0 vlc >/dev/null 2>&1 &

# Give VLC a moment to appear, then pause to keep it silent.
sleep 1
playerctl --player=vlc pause 2>/dev/null || true
echo "[initial_setup] Baseline ready."