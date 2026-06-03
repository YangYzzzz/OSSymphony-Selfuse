#!/usr/bin/env bash
set -euo pipefail

echo "[initial_setup] Preparing baseline VLC environment …"

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
echo "[initial_setup] Closed any running VLC instances."

# 2) Baseline file operations (none needed – leave defaults untouched)
echo "[initial_setup] No changes to vlcrc, keeping stock subtitle settings."

# 3) Launch VLC for baseline evaluation
DISPLAY=:0 vlc >/dev/null 2>&1 &
echo "[initial_setup] VLC launched (baseline)."