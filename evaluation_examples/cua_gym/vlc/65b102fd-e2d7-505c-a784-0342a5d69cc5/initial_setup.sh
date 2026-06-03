#!/usr/bin/env bash
set -euo pipefail

# Path to the per-user VLC configuration file
VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"; touch "$VLCRC"

# Idempotent key-value helper (not used for this task yet, but kept for baseline)
ensure_kv() {
  local key="$1"; local value="$2"
  if grep -qE "^[#;]?\s*${key}\s*=" "$VLCRC"; then
    sed -i "s|^[#;]?\s*${key}\s*=.*|${key}=${value}|g" "$VLCRC"
  else
    printf "\n%s=%s\n" "$key" "$value" >> "$VLCRC"
  fi
}

echo "[initial_setup] Closing any running VLC instance ..."
pkill vlc || true

# ---------------------------------------------------------------------------
# (2)  No vlcrc changes or media downloads are required for the baseline state
# ---------------------------------------------------------------------------

echo "[initial_setup] Launching clean VLC session ..."
DISPLAY=:0 vlc >/dev/null 2>&1 &
sleep 0.5
echo "[initial_setup] Done – baseline environment ready."