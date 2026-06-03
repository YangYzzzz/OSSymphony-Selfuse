#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
#  Initial baseline – make sure NO playlist is present and just start VLC clean
# -----------------------------------------------------------------------------

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

echo "[INFO] Closing any running VLC instances …"
pkill vlc || true

# Remove any previous playlist so the baseline is empty / clean
PLAYLIST="/home/user/Desktop/MoviesPlaylist.m3u"
if [[ -f "$PLAYLIST" ]]; then
  echo "[INFO] Removing old playlist at $PLAYLIST to provide a clean baseline"
  rm -f "$PLAYLIST"
fi

echo "[INFO] Launching clean VLC session (no playlist)"
DISPLAY=:0 vlc >/dev/null 2>&1 &