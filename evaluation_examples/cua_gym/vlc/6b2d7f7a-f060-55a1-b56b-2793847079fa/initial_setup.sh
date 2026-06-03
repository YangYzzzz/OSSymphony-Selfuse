#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Path & helper
###############################################################################
VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"
touch "$VLCRC"

ensure_kv() {
  local key="$1" value="$2"
  if grep -qE "^[#;]?\s*${key}\s*=" "$VLCRC"; then
    # key exists → replace
    sed -i "s|^[#;]?\s*${key}\s*=.*|${key}=${value}|g" "$VLCRC"
  else
    # key missing → append
    printf "\n%s=%s\n" "$key" "$value" >>"$VLCRC"
  fi
}

###############################################################################
# 1) Close VLC before any operations (idempotent run-safe)
###############################################################################
pkill vlc || true

###############################################################################
# 2) Baseline settings – keep watermark ON
###############################################################################
# 1 = display background cone; this is the default but we set it explicitly
echo "[initial_setup]   Enabling VLC watermark (cone) for baseline …"
ensure_kv "qt-bgcone" "1"

###############################################################################
# 3) Launch VLC so evaluator sees the unmodified baseline
###############################################################################
echo "[initial_setup]   Launching VLC …"
DISPLAY=:0 vlc >/dev/null 2>&1 &
sleep 0.5
echo "[initial_setup]   Done – baseline ready."