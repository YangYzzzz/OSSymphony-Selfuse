#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
#  initial_setup.sh  –  baseline state (single VLC process only)
# ------------------------------------------------------------------

VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"; touch "$VLCRC"

# Idempotent helper
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

# ------------------------------------------------------------------
# 1) Configuration ‒ keep default single-instance behaviour
# ------------------------------------------------------------------
ensure_kv "one-instance-when-started-from-file" "1"
echo "[initial_setup] Ensured single-instance mode (baseline)."

# ------------------------------------------------------------------
# 2) Launch a SINGLE VLC process (audio only) – baseline state
# ------------------------------------------------------------------
echo "[initial_setup] Launching baseline VLC with audio only …"
vlc "/home/user/Music/audio.mp3" >/dev/null 2>&1 &
sleep 0.5
echo "[initial_setup] Baseline ready – only one VLC process is running."