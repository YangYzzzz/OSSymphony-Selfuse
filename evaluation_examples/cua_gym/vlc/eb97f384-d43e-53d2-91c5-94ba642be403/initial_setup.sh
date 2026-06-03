#!/usr/bin/env bash
set -euo pipefail

VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"; touch "$VLCRC"

ensure_kv() {
  local key="$1"; local value="$2"
  if grep -qE "^[#;]?\s*${key}\s*=" "$VLCRC"; then
    sed -i "s|^[#;]?\s*${key}\s*=.*|${key}=${value}|g" "$VLCRC"
  else
    printf "
%s=%s
" "$key" "$value" >> "$VLCRC"
  fi
}

# 1) Close VLC BEFORE file operations
echo "[initial_setup] Closing any running VLC instances …"
pkill vlc || true

# 2)  No vlcrc modifications – baseline environment only
echo "[initial_setup] No configuration changes – creating clean baseline"

# 3) Launch VLC so the evaluator sees the baseline state
echo "[initial_setup] Launching VLC in the background"
DISPLAY=:0 vlc >/dev/null 2>&1 &
sleep 1
echo "[initial_setup] Baseline ready"