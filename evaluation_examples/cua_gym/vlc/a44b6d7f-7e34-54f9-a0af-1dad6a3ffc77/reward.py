"""
FINAL REWARD SCRIPT - SUCCESS
Task: Add all .mp3 files from /home/user/Music/Rock/ to active playlist.
Generated: 2025-09-13 11:52:26
Status: success
Model: azure-o3
Total Steps: 18
"""

import os
import glob
import xml.etree.ElementTree as ET
import urllib.parse
import pathlib

# ----------------- Helper Functions -----------------

def gather_mp3_basenames(rock_dir: str):
    """Return list of *.mp3 file basenames inside the given Rock directory (recursive).
    The comparison is case-insensitive for the extension."""
    basenames = []
    if not os.path.isdir(rock_dir):
        return basenames
    for path in pathlib.Path(rock_dir).rglob('*'):
        if path.is_file() and path.suffix.lower() == '.mp3':
            basenames.append(path.name)
    return basenames


def locate_status_xml():
    """Locate status.xml dumped by the framework (depth-limited search).
    Returns the first path found or None if not present."""
    # Most-likely locations (checked in order)
    candidates = [
        os.environ.get('STATUS_XML_PATH'),                                      # explicit override
        os.path.expanduser('~/.local/share/vlc/status.xml'),
        os.path.expanduser('~/.config/vlc/status.xml'),
        '/workspace/status.xml',
        '/tmp/status.xml',                                                     # framework often uses /tmp
        os.path.join(os.getcwd(), 'status.xml'),
    ]
    for cand in candidates:
        if cand and os.path.isfile(cand):
            return cand

    # Fallback: depth-limited search under a few roots (max depth 4 to remain efficient)
    for base in [os.path.expanduser('~'), '/workspace', '/tmp']:
        for root, dirs, files in os.walk(base):
            if 'status.xml' in files:
                return os.path.join(root, 'status.xml')
            if root.count(os.sep) - base.count(os.sep) > 4:  # prune deep dirs
                dirs[:] = []
    return None


def extract_playing_basename(xml_root):
    """Extract the basename of the currently playing media from status.xml.
    Prioritises <info name="filename">, falls back to "url". Returns None if not found."""
    if xml_root is None:
        return None
    for info in xml_root.findall('.//info'):
        name_attr = info.attrib.get('name', '')
        if name_attr in ('filename', 'url') and info.text:
            text = info.text.strip()
            if name_attr == 'url':
                # Strip file:// scheme if present and unquote URL encoding
                if text.startswith('file://'):
                    text = text[7:]
                text = urllib.parse.unquote(text)
            return os.path.basename(text)
    return None

# ----------------- Main Verification -----------------

def verify_vlc_rock_playlist():
    """Verify that VLC is playing an .mp3 file from /home/user/Music/Rock/ .
    Progressive scoring: 0.5 for correct state, 0.5 for correct source."""

    print('--- Reward Verification: VLC Rock Playlist ---')
    score = 0.0
    max_score = 1.0

    # 1. Collect reference mp3 filenames
    rock_dir = '/home/user/Music/Rock'
    rock_mp3s = gather_mp3_basenames(rock_dir)
    print(f'Located {len(rock_mp3s)} mp3 files in {rock_dir}')

    # 2. Find the status.xml that the evaluator saved
    status_path = locate_status_xml()
    if not status_path:
        print('✗ status.xml not found. Cannot verify playback.')
        print('REWARD: 0.0')
        return 0.0
    print(f'Using status.xml at: {status_path}')

    # 3. Parse the XML safely
    try:
        xml_root = ET.parse(status_path).getroot()
    except Exception as e:
        print(f'✗ Failed to parse status.xml: {e}')
        print('REWARD: 0.0')
        return 0.0

    # 4. Check that VLC is in the "playing" state
    state_elem = xml_root.find('state')
    state_value = state_elem.text.strip() if state_elem is not None and state_elem.text else ''
    print(f'Playback state: "{state_value}"')
    if state_value == 'playing':
        score += 0.5
        print('✓ VLC is currently playing (0.5)')
    else:
        print('✗ VLC is not in playing state (0 points)')

    # 5. Verify that the currently playing file comes from Rock directory
    playing_basename = extract_playing_basename(xml_root)
    if playing_basename:
        print(f'Currently playing file: {playing_basename}')
    else:
        print('✗ Could not determine currently playing media from status.xml')

    if playing_basename and playing_basename in rock_mp3s:
        score += 0.5
        print('✓ Playing file is an .mp3 from Rock directory (0.5)')
    else:
        if playing_basename:
            print('✗ Playing file is not inside Rock directory list (0 points)')

    # 6. Final score (capped to 1.0)
    final_score = round(min(score, max_score), 2)
    print(f'Final computed score: {final_score}')
    print(f'REWARD: {final_score}')
    return final_score

# --------------- Execute when run standalone ---------------
if __name__ == '__main__':
    verify_vlc_rock_playlist()
