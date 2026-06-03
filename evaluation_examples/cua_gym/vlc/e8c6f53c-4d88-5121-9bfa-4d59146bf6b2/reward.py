"""
FINAL REWARD SCRIPT - SUCCESS
Task: Load subtitle file /home/user/Videos/movie_subtitles.srt with video.
Generated: 2025-09-13 10:54:09
Status: success
Model: azure-o3
Total Steps: 16
"""

import os
import xml.etree.ElementTree as ET

def locate_status_xml_files():
    """Recursively walk the user's home directory to discover any status.xml files created by VLC's HTTP interface."""
    home = os.path.expanduser('~')
    status_files = []
    for root, dirs, files in os.walk(home):
        if 'status.xml' in files:
            status_files.append(os.path.join(root, 'status.xml'))
    return status_files


def is_vlc_playing(root):
    """Return True if <state>playing</state> appears in the parsed XML tree."""
    return root.findtext('state', default='').strip().lower() == 'playing'


def subtitle_file_loaded(root, expected_sub_path):
    """Return True if any <info> tag's text ends with the expected subtitle path (case-insensitive)."""
    expected_lower = expected_sub_path.lower()

    # Primary check: inside a dedicated 'Subtitles' category (most common location)
    for cat in root.findall('.//category'):
        if cat.get('name', '').strip().lower() == 'subtitles':
            for info in cat.findall('info'):
                if info.text and info.text.strip().lower().endswith(expected_lower):
                    return True

    # Fallback: scan every <info> tag in case VLC structures differ
    for info in root.findall('.//info'):
        if info.text and info.text.strip().lower().endswith(expected_lower):
            return True
    return False


def verify_task():
    expected_subtitle_path = '/home/user/Videos/movie_subtitles.srt'

    status_files = locate_status_xml_files()
    print(f"Discovered {len(status_files)} status.xml file(s) for inspection.")

    playing_detected = False   # True when any VLC instance is in 'playing' state
    subtitle_detected = False  # True when the required subtitle is loaded in a playing instance

    for status_path in status_files:
        try:
            root = ET.parse(status_path).getroot()
        except Exception as e:
            print(f"Skipping unreadable file {status_path}: {e}")
            continue

        if is_vlc_playing(root):
            playing_detected = True
            if subtitle_file_loaded(root, expected_subtitle_path):
                subtitle_detected = True
                print(f"✓ Subtitle path matches in {status_path}")
                break  # Both conditions satisfied; no need to continue scanning
            else:
                print(f"Found 'playing' state in {status_path} but subtitle path does not match.")
        else:
            print(f"VLC instance represented by {status_path} is not playing.")

    # Progressive scoring – award points only for actual achievements
    score = 0.0
    if playing_detected:
        score += 0.4
        print("✓ Detected VLC in 'playing' state (0.4 points)")
    else:
        print("✗ No VLC instance in 'playing' state detected (0 points)")

    if subtitle_detected:
        score += 0.6
        print("✓ Expected subtitle file is loaded (0.6 points)")
    else:
        print("✗ Expected subtitle file is NOT loaded (0 points)")

    # Clamp score to the [0,1] interval and round for neatness
    score = round(min(score, 1.0), 2)
    print(f"REWARD: {score}")
    return score

if __name__ == '__main__':
    verify_task()
