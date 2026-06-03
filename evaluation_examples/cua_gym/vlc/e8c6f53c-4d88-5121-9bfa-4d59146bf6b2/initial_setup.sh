#!/usr/bin/env bash
set -euo pipefail

echo "[initial_setup] Preparing clean baseline – NO external subtitles"

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

# 1) Close VLC BEFORE file operations
pkill vlc || true

# 2) File operations
#    Make sure no permanent external subtitle file is configured.
ensure_kv "sub-file" ""

echo "[initial_setup] Baseline ready – launching VLC without subtitles"

# 3) Launch VLC (background, silent)
DISPLAY=:0 vlc >/dev/null 2>&1 &