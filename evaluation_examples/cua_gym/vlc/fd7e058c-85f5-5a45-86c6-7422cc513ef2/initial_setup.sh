#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
#  VLC baseline – no special media loaded
# ---------------------------------------------------------------------------

VLCRC="$HOME/.config/vlc/vlcrc"
mkdir -p "$(dirname "$VLCRC")"; touch "$VLCRC"
ensure_kv() {
  # Generic helper kept for compliance – no keys edited in baseline
  local key="$1"; local value="$2"
  if grep -qE "^[#;]?\s*${key}\s*=" "$VLCRC"; then
    sed -i "s|^[#;]?\s*${key}\s*=.*|${key}=${value}|g" "$VLCRC"
  else
    printf "
%s=%s
" "$key" "$value" >> "$VLCRC"
  fi
}

echo "[initial_setup] Closing any running VLC instance …"
pkill vlc || true

# No vlcrc modifications required for baseline
echo "[initial_setup] Launching vanilla VLC GUI …"
DISPLAY=:0 vlc >/dev/null 2>&1 &

# Give GUI a brief moment to appear (useful during manual debugging)
sleep 0.5
echo "[initial_setup] Baseline ready."