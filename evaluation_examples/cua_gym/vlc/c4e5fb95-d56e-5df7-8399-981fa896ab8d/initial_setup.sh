#!/usr/bin/env bash
set -euo pipefail

# --------------------------------------------------------------------
# VLC configuration helper
# --------------------------------------------------------------------
VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"; touch "$VLCRC"
ensure_kv() {
  local key="$1" value="$2"
  if grep -qE "^[#;]?\s*${key}\s*=" "$VLCRC"; then
    sed -i "s|^[#;]?\s*${key}\s*=.*|${key}=${value}|g" "$VLCRC"
  else
    printf "\n%s=%s\n" "$key" "$value" >> "$VLCRC"
  fi
}

echo "[initial_setup] Preparing clean baseline …"

# 1) Close VLC BEFORE any file operations
pkill vlc || true

# 2) Baseline file / env preparation
echo "[initial_setup] Removing previously-captured poster (if any)."
rm -f "/home/user/Desktop/movie_poster.bmp"

# Re-establish default snapshot configuration so evaluator
# has a known starting point
ensure_kv "snapshot-path"   "$HOME/Pictures"
ensure_kv "snapshot-format" "png"
ensure_kv "snapshot-prefix" "vlcsnap"

echo "[initial_setup] Baseline snapshot settings written to vlcrc."

# 3) Relaunch VLC so the evaluator sees vanilla behaviour
DISPLAY=:0 vlc >/dev/null 2>&1 & disown
sleep 0.5
echo "[initial_setup] Baseline complete."