#!/usr/bin/env bash
set -euo pipefail

# --------------------------------------------------------------------
#  INITIAL SET-UP  – no playlist opened, just bring VLC up in default
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

echo "[initial_setup] Closing any running VLC instance …"
pkill vlc || true

# (No vlcrc edits required for baseline)

echo "[initial_setup] Launching vanilla VLC …"
DISPLAY=:0 vlc >/dev/null 2>&1 &
sleep 1
echo "[initial_setup] Baseline ready."