"""
FINAL REWARD SCRIPT - SUCCESS
Task: Stream concert https://music.example.com/live/concert123.m3u8 using VLC.
Generated: 2025-09-13 12:02:19
Status: success
Model: azure-o3
Total Steps: 15
"""

import os
import pathlib
import xml.etree.ElementTree as ET


def find_status_xml(max_depth: int = 3) -> pathlib.Path | None:
    """Locate the status.xml file saved by the evaluation framework.

    Search order:
    1. Environment variables (STATUS_XML_PATH, VLC_STATUS_XML, STATUS_XML)
    2. Direct common locations: ./status.xml, /tmp/status.xml, ~/status.xml
    3. Shallow (≤ max_depth) search inside $HOME and /tmp to avoid heavy I/O
    """
    # 1. Environment-provided paths
    for var in ("STATUS_XML_PATH", "VLC_STATUS_XML", "STATUS_XML"):
        env_path = os.getenv(var)
        if env_path and pathlib.Path(env_path).exists():
            return pathlib.Path(env_path)

    # 2. Direct candidates
    direct_candidates = [
        pathlib.Path(os.getcwd()) / "status.xml",
        pathlib.Path("/tmp/status.xml"),
        pathlib.Path.home() / "status.xml",
    ]
    for candidate in direct_candidates:
        if candidate.exists():
            return candidate

    # 3. Shallow recursive search ($HOME and /tmp)
    for root in (pathlib.Path.home(), pathlib.Path("/tmp")):
        if not root.exists():
            continue
        for current_root, dirs, files in os.walk(root):
            if "status.xml" in files:
                return pathlib.Path(current_root) / "status.xml"
            # prune search once depth exceeds max_depth
            depth = len(pathlib.Path(current_root).relative_to(root).parts)
            if depth >= max_depth:
                dirs[:] = []
    return None


def parse_status_xml(xml_path: pathlib.Path) -> dict:
    """Extract <state>, meta/url and meta/filename from status.xml."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    info = {"state": None, "url": None, "filename": None}

    state_elem = root.find(".//state")
    if state_elem is not None and state_elem.text:
        info["state"] = state_elem.text.strip()

    for meta in root.findall('.//information/category[@name="meta"]/info'):
        name = meta.attrib.get("name")
        if name in ("url", "filename"):
            info[name] = (meta.text or "").strip()
    return info


def verify_task() -> float:
    """Verify that VLC is streaming the specified concert stream."""
    print("=== VLC Concert Stream Verification ===")
    expected_suffix = "music.example.com/live/concert123.m3u8"
    total_score = 0.0

    # Locate status.xml
    status_xml_path = find_status_xml()
    if status_xml_path is None:
        print("✗ status.xml could not be found. VLC playback info missing.")
        print("REWARD: 0.0")
        return 0.0

    print(f"✓ Found status.xml at {status_xml_path}")

    # Parse XML
    try:
        info = parse_status_xml(status_xml_path)
    except Exception as err:
        print(f"✗ Failed to parse status.xml: {err}")
        print("REWARD: 0.0")
        return 0.0

    # Requirement 1: state must be 'playing'
    if info.get("state") == "playing":
        print("✓ VLC state is 'playing'")
        total_score += 0.5
    else:
        print(f"✗ VLC state is not 'playing' (found: {info.get('state')})")

    # Requirement 2: URL / filename suffix must match expected stream
    source = info.get("url") or info.get("filename") or ""
    if source.endswith(expected_suffix):
        print(f"✓ Media source matches expected suffix: {source}")
        total_score += 0.5
    else:
        print(f"✗ Media source does not match expected stream. Found: {source}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()
