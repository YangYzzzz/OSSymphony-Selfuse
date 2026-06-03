#!/usr/bin/env bash
set -euo pipefail

############################################################
#  INITIAL SET-UP SCRIPT  – baseline environment only
############################################################

VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"; touch "$VLCRC"

# Idempotent helper (unused here but required in template)
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

########################################################################
# Prepare expected video file (assume evaluator already provides it).  #
# If it does not exist, create a small placeholder so that the path    #
# always resolves. This keeps the script idempotent and re-runnable.   #
########################################################################
VIDEO_SRC="/home/user/Desktop/lecture.mp4"
if [[ ! -f "$VIDEO_SRC" ]]; then
  echo "[initial_setup] '$VIDEO_SRC' not found – creating 1-byte placeholder."
  : > "$VIDEO_SRC"
fi

echo "[initial_setup] Environment ready – launching VLC."
DISPLAY=:0 vlc >/dev/null 2>&1 &