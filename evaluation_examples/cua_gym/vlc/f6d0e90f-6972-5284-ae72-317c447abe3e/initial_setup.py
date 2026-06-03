"""
Initial Setup: Configure VLC Media Library with two scan paths
Task ID: vlc_playlist_073
Domain: vlc
"""

import os
import re
import shlex
import sqlite3
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vlc_playlist_073'
VLCRC_PATH = os.path.expanduser('~/.config/vlc/vlcrc')
ML_DB_DIR = os.path.expanduser('~/.local/share/vlc/medialibrary')
ML_DB_PATH = os.path.join(ML_DB_DIR, 'ml.db')


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


def kill_vlc():
    """Kill VLC if running."""
    subprocess.run(["pkill", "-f", "vlc"], capture_output=True)
    time.sleep(2)


def set_vlcrc_option(key: str, value: str):
    """Set a vlcrc option. Uncomments the key if commented out."""
    with open(VLCRC_PATH, "r") as f:
        content = f.read()
    pattern = re.compile(rf'^(#?\s*){re.escape(key)}=.*$', re.MULTILINE)
    replacement = f'{key}={value}'
    if pattern.search(content):
        content = pattern.sub(replacement, content)
    else:
        content += f'\n{key}={value}\n'
    with open(VLCRC_PATH, "w") as f:
        f.write(content)


def create_directories():
    """Create the Music directories with some sample media files."""
    dirs = [
        os.path.expanduser('~/Music/Current'),
        os.path.expanduser('~/Music/Old_Library'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # Create some sample audio files in each directory using ffmpeg
    for d, files in [
        (dirs[0], ['jazz_morning.mp3', 'ambient_focus.mp3', 'classical_evening.mp3']),
        (dirs[1], ['retro_hits_2019.mp3', 'old_favorites.mp3']),
    ]:
        for fname in files:
            fpath = os.path.join(d, fname)
            if not os.path.exists(fpath):
                subprocess.run([
                    'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
                    '-t', '3', '-q:a', '9', '-y', fpath
                ], capture_output=True)

    print('Directories and sample media created')


def create_medialibrary_db():
    """Create VLC medialibrary SQLite database with two entry points."""
    os.makedirs(ML_DB_DIR, exist_ok=True)

    # Remove existing db if any
    if os.path.exists(ML_DB_PATH):
        os.remove(ML_DB_PATH)

    conn = sqlite3.connect(ML_DB_PATH)
    c = conn.cursor()

    # Create the Settings table (stores DB model version)
    c.execute('''CREATE TABLE IF NOT EXISTS Settings (
        db_model_version INTEGER NOT NULL DEFAULT 0
    )''')
    c.execute('INSERT INTO Settings (db_model_version) VALUES (17)')

    # Create the Folder table (entry points / scan paths)
    c.execute('''CREATE TABLE IF NOT EXISTS Folder (
        id_folder INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE ON CONFLICT FAIL,
        name TEXT,
        is_banned INTEGER NOT NULL DEFAULT 0,
        nb_audio INTEGER NOT NULL DEFAULT 0,
        nb_video INTEGER NOT NULL DEFAULT 0,
        is_present INTEGER NOT NULL DEFAULT 1,
        is_removable INTEGER NOT NULL DEFAULT 0
    )''')

    # Insert the two scan paths
    music_current = os.path.expanduser('~/Music/Current/')
    music_old = os.path.expanduser('~/Music/Old_Library/')

    c.execute('INSERT INTO Folder (path, name, is_banned, nb_audio, nb_video, is_present, is_removable) VALUES (?, ?, 0, 3, 0, 1, 0)',
              (music_current, 'Current'))
    c.execute('INSERT INTO Folder (path, name, is_banned, nb_audio, nb_video, is_present, is_removable) VALUES (?, ?, 0, 2, 0, 1, 0)',
              (music_old, 'Old_Library'))

    # Create Media table (for discovered media files)
    c.execute('''CREATE TABLE IF NOT EXISTS Media (
        id_media INTEGER PRIMARY KEY AUTOINCREMENT,
        type INTEGER NOT NULL,
        subtype INTEGER NOT NULL DEFAULT 0,
        duration INTEGER NOT NULL DEFAULT -1,
        play_count INTEGER UNSIGNED NOT NULL DEFAULT 0,
        last_played_date INTEGER UNSIGNED,
        real_last_played_date INTEGER UNSIGNED,
        insertion_date INTEGER UNSIGNED,
        release_date INTEGER UNSIGNED,
        title TEXT COLLATE NOCASE,
        filename TEXT COLLATE NOCASE,
        is_favorite INTEGER NOT NULL DEFAULT 0,
        is_present INTEGER NOT NULL DEFAULT 1,
        device_id INTEGER,
        nb_playlists INTEGER UNSIGNED NOT NULL DEFAULT 0,
        folder_id INTEGER UNSIGNED,
        import_type INTEGER UNSIGNED NOT NULL,
        group_id INTEGER UNSIGNED,
        forced_title INTEGER NOT NULL DEFAULT 0,
        artist_id INTEGER,
        genre_id INTEGER,
        track_number INTEGER UNSIGNED,
        album_id INTEGER UNSIGNED,
        disc_number INTEGER UNSIGNED,
        lyrics TEXT
    )''')

    # Create File table
    c.execute('''CREATE TABLE IF NOT EXISTS File (
        id_file INTEGER PRIMARY KEY AUTOINCREMENT,
        media_id INTEGER DEFAULT NULL,
        playlist_id INTEGER DEFAULT NULL,
        mrl TEXT,
        type INTEGER NOT NULL,
        last_modification_date INTEGER UNSIGNED,
        size INTEGER UNSIGNED,
        folder_id INTEGER UNSIGNED,
        is_removable INTEGER NOT NULL,
        is_external INTEGER NOT NULL,
        is_network INTEGER NOT NULL
    )''')

    conn.commit()
    conn.close()
    print(f'Medialibrary database created at {ML_DB_PATH}')


def setup():
    # Kill VLC first (before modifying config)
    kill_vlc()

    # Create directories and sample files
    create_directories()

    # Enable media library in vlcrc
    set_vlcrc_option('media-library', '1')
    print('Media library enabled in vlcrc')

    # Create the medialibrary database with scan paths
    create_medialibrary_db()

    # Verify
    conn = sqlite3.connect(ML_DB_PATH)
    c = conn.cursor()
    c.execute('SELECT path, name FROM Folder WHERE is_banned = 0')
    rows = c.fetchall()
    conn.close()
    print(f'Scan paths configured: {rows}')

    # Launch VLC
    launch_gui('vlc', delay_sec=3.0)
    print('GUI_READY: launched VLC with DISPLAY=:0')


setup()
