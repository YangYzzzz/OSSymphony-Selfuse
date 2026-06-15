#!/usr/bin/env bash
set -euo pipefail

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

echo "[initial_setup] Cleaning up any previous conversion output …"
rm -f /home/user/Desktop/cd_quality.wav || true

# Sample source to convert later
SRC="/home/user/Desktop/source_audio.mp3"
if [[ ! -f "$SRC" ]]; then
  echo "[initial_setup] Downloading small sample MP3 …"
  curl -L -o "$SRC" \
    https://file-examples.com/storage/fe66c16e9f9c5a3f3b51d27/2017/11/file_example_MP3_700KB.mp3
fi

# 3) Launch VLC or leave environment ready for evaluation
echo "[initial_setup] Launching VLC to establish baseline state …"
DISPLAY=:0 vlc >/dev/null 2>&1 &