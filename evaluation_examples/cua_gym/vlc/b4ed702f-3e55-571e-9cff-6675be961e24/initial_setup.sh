#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# initial_setup.sh – baseline environment (VLC NOT yet tuned to the task)
# -----------------------------------------------------------------------------

VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"; touch "$VLCRC"

ensure_kv() {        # (required by spec – not used in the baseline script)
  local key="$1"; local value="$2"
  if grep -qE "^[#;]?\s*${key}\s*=" "$VLCRC"; then
    sed -i "s|^[#;]?\s*${key}\s*=.*|${key}=${value}|g" "$VLCRC"
  else
    printf "\n%s=%s\n" "$key" "$value" >> "$VLCRC"
  fi
}

echo "[initial_setup] Closing any running VLC instances …"
pkill vlc || true
sleep 0.5

# (No configuration or media changes required for baseline.)

echo "[initial_setup] Launching VLC in its default state …"
DISPLAY=:0 vlc >/dev/null 2>&1 &
sleep 1
echo "[initial_setup] Baseline ready."