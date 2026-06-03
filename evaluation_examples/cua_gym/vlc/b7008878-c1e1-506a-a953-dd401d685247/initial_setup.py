"""
Initial Setup: Create a large VLC playlist with 50+ tracks and open VLC playing a different track.
Task ID: vlc_playlist_048
Domain: vlc
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_048'
MUSIC_DIR = f'{WORKDIR}/Music'
PLAYLIST_FILE = f'{WORKDIR}/{TASK_ID}.m3u'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    env["VLC_VERBOSE"] = "-1"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Kill any existing VLC instances
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)

    # Create music directory
    os.makedirs(MUSIC_DIR, exist_ok=True)

    # Define 55 track names across different categories
    track_names = [
        # Ambient tracks (1-10)
        "ambient_sunrise_01", "ambient_sunrise_02", "ambient_ocean_01",
        "ambient_ocean_02", "ambient_forest_01", "ambient_rain_01",
        "ambient_thunder_01", "ambient_wind_01", "ambient_night_01",
        "ambient_morning_01",
        # Chill tracks (11-20)
        "chill_lounge_01", "chill_lounge_02", "chill_cafe_01",
        "chill_cafe_02", "chill_evening_01", "chill_sunset_01",
        "chill_garden_01", "chill_breeze_01", "chill_waves_01",
        "chill_moonlight_01",
        # Deep focus tracks (21-30) - target is deep_focus_03 at index 24
        "deep_focus_01", "deep_focus_02", "deep_focus_alpha_01",
        "deep_focus_beta_01", "deep_focus_03", "deep_focus_04",
        "deep_focus_gamma_01", "deep_focus_05", "deep_focus_delta_01",
        "deep_focus_06",
        # Electronic tracks (31-40)
        "electronic_pulse_01", "electronic_pulse_02", "electronic_wave_01",
        "electronic_drift_01", "electronic_glow_01", "electronic_spark_01",
        "electronic_echo_01", "electronic_bloom_01", "electronic_haze_01",
        "electronic_flow_01",
        # Piano tracks (41-50)
        "piano_nocturne_01", "piano_nocturne_02", "piano_sonata_01",
        "piano_etude_01", "piano_prelude_01", "piano_waltz_01",
        "piano_ballad_01", "piano_reverie_01", "piano_serenade_01",
        "piano_lullaby_01",
        # Jazz tracks (51-55)
        "jazz_smooth_01", "jazz_swing_01", "jazz_blues_01",
        "jazz_bossa_01", "jazz_cool_01",
    ]

    # Generate short silent mp3 files for each track using ffmpeg
    for name in track_names:
        filepath = f"{MUSIC_DIR}/{name}.mp3"
        if True:  # Always recreate to ensure correct duration
            # Create a 60-second mp3 with unique frequency
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi",
                "-i", f"sine=frequency={220 + track_names.index(name) * 10}:duration=60",
                "-q:a", "9",
                "-metadata", f"title={name}",
                filepath
            ], capture_output=True, check=True)

    print(f"Created {len(track_names)} audio tracks in {MUSIC_DIR}")

    # Create M3U playlist file
    with open(PLAYLIST_FILE, 'w') as f:
        f.write("#EXTM3U\n")
        for name in track_names:
            f.write(f"#EXTINF:60,{name}\n")
            f.write(f"{MUSIC_DIR}/{name}.mp3\n")

    print(f"Created playlist: {PLAYLIST_FILE}")

    # Launch VLC with the playlist, start playing the first track (ambient_sunrise_01)
    # Use HTTP interface for control, and show playlist panel
    launch_gui(
        f'vlc --extraintf=http --http-password=password --http-port=8080 '
        f'--started-from-file --playlist-autostart '
        f'"{PLAYLIST_FILE}"',
        delay_sec=3.0
    )

    # Use HTTP interface to skip to a specific track (not deep_focus_03)
    # Play "chill_lounge_01" (track index 10) as the currently playing track
    import requests
    import xml.etree.ElementTree as ET

    # Retry loop to wait for VLC HTTP interface to be ready
    for attempt in range(10):
        try:
            time.sleep(2)
            resp = requests.get(
                "http://localhost:8080/requests/playlist.xml",
                auth=("", "password"),
                timeout=5
            )
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                for leaf in root.iter('leaf'):
                    name = leaf.get('name', '')
                    if 'chill_lounge_01' in name:
                        track_id = leaf.get('id')
                        if track_id:
                            requests.get(
                                f"http://localhost:8080/requests/status.xml?command=pl_play&id={track_id}",
                                auth=("", "password"),
                                timeout=5
                            )
                            print(f"Now playing: chill_lounge_01 (id={track_id})")
                            break
                break  # success
        except Exception as e:
            print(f"HTTP attempt {attempt+1} failed: {e}")
            if attempt == 9:
                print("Warning: Could not set current track via HTTP after 10 attempts")

    # Toggle playlist view to make it visible (Ctrl+L)
    try:
        subprocess.run([
            "xdotool", "key", "--delay", "100", "ctrl+l"
        ], env={"DISPLAY": ":0", "PATH": os.environ.get("PATH", "/usr/bin")},
           capture_output=True, timeout=5)
        time.sleep(1)
        print("Toggled playlist panel visibility")
    except Exception as e:
        print(f"Warning: xdotool not available or failed: {e}")

    print(f"Initial file created: {PLAYLIST_FILE}")
    print("GUI_READY: launched VLC with DISPLAY=:0, playlist visible, playing chill_lounge_01")


create_initial()
