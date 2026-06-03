"""
FINAL REWARD SCRIPT - SUCCESS
Task: Create new playlist from all .mp4 files in /home/user/Movies/ directory.
Generated: 2025-09-13 12:17:49
Status: success
Model: azure-o3
Total Steps: 11
"""

import os
import re
import xml.etree.ElementTree as ET
import urllib.parse

"""
Reward Script: Verify creation of a playlist that contains ALL .mp4 files
located inside /home/user/Movies/ (recursively).

Scoring Strategy (progressive):
  • 1.0  – Playlist covers 100% of Movies .mp4 files
  • 0.6  – Playlist covers ≥80% but <100%
  • 0-0.6 – Linear scale for 0-80% coverage
  • 0.0  – No playlist files found OR zero coverage

No points are given for mere file existence; coverage is determined by
actually parsing playlist contents and matching them (by absolute path or
basename) against the Movies directory files.
"""

MOVIE_DIR = "/home/user/Movies"
PLAYLIST_SEARCH_ROOT = "/home/user"          # search user-space only
IGNORE_PATH_SUFFIXES = ["/vlc/ml.xspf"]       # default VLC media-library list

# ─────────────────────────── Helper Functions ────────────────────────────

def get_mp4_files(directory: str):
    """Return absolute paths of all .mp4 files under *directory* (recursive)."""
    mp4s = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(".mp4"):
                mp4s.append(os.path.join(root, f))
    return sorted(mp4s)


def _parse_m3u(path):
    entries = []
    with open(path, "r", errors="ignore") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                entries.append(line)
    return entries


def _parse_pls(path):
    entries = []
    with open(path, "r", errors="ignore") as fh:
        for line in fh:
            line = line.strip()
            if line.lower().startswith("file") and "=" in line:
                entries.append(line.split("=", 1)[1].strip())
    return entries


def _parse_xspf(path):
    entries = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        ns = {"def": root.tag.split("}")[0].strip("{")} if "}" in root.tag else {}
        xpath = ".//def:location" if ns else ".//location"
        for loc in root.findall(xpath, ns):
            if loc.text:
                entries.append(loc.text.strip())
    except Exception as e:
        # Malformed or unreadable playlist – ignore gracefully
        print(f"Error parsing XSPF '{path}': {e}")
    return entries


def read_playlist(path):
    """Return cleaned list of file references contained in *path*."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".m3u", ".m3u8"):
        raw = _parse_m3u(path)
    elif ext == ".pls":
        raw = _parse_pls(path)
    elif ext == ".xspf":
        raw = _parse_xspf(path)
    else:
        return []

    cleaned = []
    base_dir = os.path.dirname(path)
    for ref in raw:
        if not ref:
            continue
        # handle URI format: file:///absolute/path
        if ref.startswith("file:///"):
            cleaned.append(urllib.parse.unquote(ref[len("file://"):]))
            continue
        # skip non-file URIs (http, https, etc.)
        if re.match(r"^[a-zA-Z]+://", ref):
            continue
        # resolve relative paths against playlist location
        if not os.path.isabs(ref):
            ref = os.path.abspath(os.path.join(base_dir, ref))
        cleaned.append(ref)
    return cleaned


def find_playlist_files(search_root):
    candidates = []
    for root, _, files in os.walk(search_root):
        for f in files:
            if f.lower().endswith((".m3u", ".m3u8", ".pls", ".xspf")):
                full = os.path.join(root, f)
                if any(full.endswith(suffix) for suffix in IGNORE_PATH_SUFFIXES):
                    continue  # ignore VLC internal media library list
                candidates.append(full)
    return candidates


def compute_coverage(movie_files, playlist_refs):
    """Return a *set* of movie_files that are referenced by the playlist."""
    movie_set = set(movie_files)
    basename_map = {os.path.basename(p): p for p in movie_files}
    covered = set()

    for ref in playlist_refs:
        if not ref.lower().endswith(".mp4"):
            continue  # only care about mp4 references
        if ref in movie_set:
            covered.add(ref)
        else:
            # try matching by basename (handles relative paths, etc.)
            bn = os.path.basename(ref)
            if bn in basename_map:
                covered.add(basename_map[bn])
    return covered

# ───────────────────────────── Verification ─────────────────────────────

def verify_task():
    print("Starting verification for 'Create new playlist from all .mp4 files in /home/user/Movies/'...")

    movie_files = get_mp4_files(MOVIE_DIR)
    if not movie_files:
        print(f"✗ No .mp4 files found in {MOVIE_DIR}. Cannot verify task.")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Detected {len(movie_files)} .mp4 file(s) that must appear in the playlist.")

    playlist_files = find_playlist_files(PLAYLIST_SEARCH_ROOT)
    if not playlist_files:
        print("✗ No playlist files (.m3u/.m3u8/.pls/.xspf) found under /home/user.")
        print("REWARD: 0.0")
        return 0.0
    print(f"✓ Found {len(playlist_files)} playlist candidate(s) to inspect.")

    best_ratio = 0.0
    for pl in playlist_files:
        refs = read_playlist(pl)
        covered = compute_coverage(movie_files, refs)
        ratio = len(covered) / len(movie_files)
        print(f"  • {pl}: covers {len(covered)}/{len(movie_files)} movie file(s) – {ratio*100:.1f}%")
        if ratio > best_ratio:
            best_ratio = ratio

    # Progressive scoring
    if best_ratio >= 1.0 - 1e-9:          # full coverage
        score = 1.0
    elif best_ratio >= 0.8:              # 80–99% coverage
        score = 0.6
    else:                                # 0–79% → linear up to 0.6
        score = 0.6 * (best_ratio / 0.8)

    print(f"Best coverage achieved: {best_ratio*100:.1f}% -> Final score {score}")
    print(f"REWARD: {score}")
    return score


if __name__ == "__main__":
    verify_task()
