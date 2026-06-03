#!/usr/bin/env bash
set -euo pipefail

# --------------------------------------------------------------------
# VLC configuration helpers (nothing changed for the baseline build)
# --------------------------------------------------------------------
VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"; touch "$VLCRC"

ensure_kv() {
  local key="$1"; local value="$2"
  if grep -qE "^[#;]?\s*${key}\s*=" "$VLCRC"; then
    sed -i "s|^[#;]?\s*${key}\s*=.*|${key}=${value}|g" "$VLCRC"
  else
    printf "\n%s=%s\n" "$key" "$value" >> "$VLCRC"
  fi
}

echo "[initial_setup] Closing any running VLC instances …"
pkill vlc || true

# --------------------------------------------------------------------
# No vlcrc changes are needed for baseline.
# --------------------------------------------------------------------

echo "[initial_setup] Launching vanilla VLC (no media) …"
DISPLAY=:0 vlc >/dev/null 2>&1 &

echo "[initial_setup] Baseline environment ready."