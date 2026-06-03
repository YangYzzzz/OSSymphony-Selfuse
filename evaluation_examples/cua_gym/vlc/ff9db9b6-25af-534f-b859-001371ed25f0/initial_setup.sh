#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------
# VLC configuration helpers (required boiler-plate, even if unused here)
# ---------------------------------------------------------------------
VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"; touch "$VLCRC"
ensure_kv() {
  local key="$1"; local value="$2"
  if grep -qE "^[#;]?\s*${key}\s*=" "$VLCRC"; then
    sed -i "s|^[#;]?\s*${key}\s*=.*|${key}=${value}|g" "$VLCRC"
  else
    printf "\n%s=%s\n" "$key" "$value" >>"$VLCRC"
  fi
}

# ---------------------------------------------------------------------
# 1) Close any running VLC instances BEFORE we touch files
# ---------------------------------------------------------------------
echo "[initial_setup] Shutting down any running VLC instances …"
pkill vlc || true

# ---------------------------------------------------------------------
# 2) Baseline file preparations
#    – We expect a landscape source video called landscape.mp4 to exist
#      on the Desktop (that is what the grader will supply).  Nothing
#      is changed here, we only log the current state.
# ---------------------------------------------------------------------
INPUT="/home/user/Desktop/landscape.mp4"
if [[ -f "$INPUT" ]]; then
  echo "[initial_setup] Source video found: $INPUT"
else
  echo "[initial_setup] WARNING: $INPUT not found (grader will probably supply it)."
fi

# ---------------------------------------------------------------------
# 3) Launch VLC (clean baseline state) for the evaluator
# ---------------------------------------------------------------------
echo "[initial_setup] Launching VLC in the background …"
DISPLAY=:0 vlc >/dev/null 2>&1 & disown