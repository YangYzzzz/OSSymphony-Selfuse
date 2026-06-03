"""
FINAL REWARD SCRIPT - SUCCESS
Task: Run two VLC processes: one for /home/user/Music/audio.mp3, one for /home/user/Videos/video.mp4.
Generated: 2025-09-13 11:48:45
Status: success
Model: azure-o3
Total Steps: 15
"""

import os
import fnmatch
import xml.etree.ElementTree as ET

"""
Reward script for VLC playback verification
Task: Two VLC instances should be running – one playing
/home/user/Music/audio.mp3 and another playing /home/user/Videos/video.mp4

Verification logic:
1. Locate all files whose name matches "status.xml" or "status*.xml" inside
   /home/user and /tmp (framework usually stores them there).
2. Parse every XML file found and extract:
      • <state> text                        → must equal "playing"
      • <info name="filename">  (optional) → used for filename match
      • <info name="url">       (optional) → used for url suffix match
3. For each target media file (audio.mp3 and video.mp4) mark it as verified
   as soon as one *playing* status XML shows either a filename OR url that
   ends with the target name (case-insensitive).
4. Scoring: 0.5 points for each verified target, max 1.0.
   Progressive scoring gives partial credit if only one of the two is
   correctly playing.
5. Print detailed diagnostics for transparency and debugging, then output
   the final reward as "REWARD: X.X".
"""

def collect_status_xml(search_roots, patterns=("status.xml", "status*.xml"), max_files=1000):
    """Recursively collect status xml files under the given roots."""
    files = []
    for root in search_roots:
        for dirpath, _, filenames in os.walk(root):
            for fn in filenames:
                # Stop early if we already have enough samples (safety)
                if len(files) >= max_files:
                    return files
                for pat in patterns:
                    if fnmatch.fnmatch(fn, pat):
                        files.append(os.path.join(dirpath, fn))
                        break
    return files

def parse_status(path):
    """Parse a VLC status.xml file and return a dict or None on error."""
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        state = (root.findtext("state") or "").strip().lower()
        meta = {}
        for info in root.findall('.//info'):
            name = info.attrib.get('name', '').lower()
            meta[name] = (info.text or '').strip()
        return {'state': state, 'meta': meta}
    except Exception as e:
        print(f"Error parsing {path}: {e}")
        return None

def verify_playback():
    # Targets we need to detect
    targets = {
        'audio.mp3': False,
        'video.mp4': False,
    }

    # Where the framework usually stores the status files
    search_roots = ['/home/user', '/tmp']

    xml_files = collect_status_xml(search_roots)
    print(f"Found {len(xml_files)} potential status xml file(s)")

    for xml_path in xml_files:
        data = parse_status(xml_path)
        if not data:
            continue  # parsing failed

        # We only care about entries that are actively playing
        if data['state'] != 'playing':
            continue

        filename = data['meta'].get('filename', '').lower()
        url      = data['meta'].get('url', '').lower()
        print(f"{xml_path}: state=playing, filename='{filename}', url='{url}'")

        for tgt in list(targets.keys()):
            if targets[tgt]:
                continue  # already verified
            if filename.endswith(tgt) or url.endswith(tgt):
                targets[tgt] = True
                print(f"✓ Matched playback for {tgt} via {xml_path}")

    # Calculate progressive score
    score = 0.0
    for tgt, found in targets.items():
        if found:
            score += 0.5
            print(f"✓ Requirement satisfied: {tgt} is playing")
        else:
            print(f"✗ Requirement NOT satisfied: {tgt} is not playing")

    score = min(score, 1.0)  # safety cap
    print(f"REWARD: {score}")
    return score

# Execute verification when the script runs as main
if __name__ == "__main__":
    verify_playback()

