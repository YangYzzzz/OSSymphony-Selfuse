"""
Initial Setup: Create a photo essay document from a video
Task ID: osworld_multi_apps_media_image_009
Domain: multi_apps (ffmpeg, GIMP, LibreOffice Writer)

Creates:
  - /home/user/videos/travel_vlog.mp4 (4-minute travel video)
  - /home/user/documents/ (empty directory for output)
  - Opens a terminal with the video directory visible
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_media_image_009'
VIDEO_DIR = f'{WORKDIR}/videos'
VIDEO_FILE = f'{VIDEO_DIR}/travel_vlog.mp4'
DOCUMENTS_DIR = f'{WORKDIR}/documents'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_video():
    """Create a realistic 4-minute travel vlog video using ffmpeg."""
    os.makedirs(VIDEO_DIR, exist_ok=True)

    if os.path.isfile(VIDEO_FILE):
        print(f'Video already exists: {VIDEO_FILE}')
        return

    print('Creating travel_vlog.mp4 (4 minutes)...')

    # Create a visually interesting 4-minute video with color gradients and movement
    # Uses lavfi (libavfilter virtual input) to generate synthetic video
    # The video will have changing colors to simulate a travel vlog
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi',
        '-i', (
            'color=c=0x4a90d9:size=1280x720:duration=240:rate=24,'
            'drawtext=text=\'Travel Vlog\':fontcolor=white:fontsize=48:'
            'x=(w-text_w)/2:y=(h-text_h)/2:enable=\'between(t,0,5)\','
            'drawtext=text=\'Day 1 - Arrival\':fontcolor=yellow:fontsize=36:'
            'x=40:y=40:enable=\'between(t,10,30)\','
            'drawtext=text=\'Day 1 - City Tour\':fontcolor=yellow:fontsize=36:'
            'x=40:y=40:enable=\'between(t,35,65)\','
            'drawtext=text=\'Day 2 - Mountains\':fontcolor=white:fontsize=36:'
            'x=40:y=40:enable=\'between(t,70,100)\','
            'drawtext=text=\'Day 2 - Sunset View\':fontcolor=orange:fontsize=36:'
            'x=40:y=40:enable=\'between(t,105,135)\','
            'drawtext=text=\'Day 3 - Beach Morning\':fontcolor=cyan:fontsize=36:'
            'x=40:y=40:enable=\'between(t,140,170)\','
            'drawtext=text=\'Day 3 - Local Market\':fontcolor=white:fontsize=36:'
            'x=40:y=40:enable=\'between(t,175,205)\','
            'drawtext=text=\'Day 4 - Departure\':fontcolor=yellow:fontsize=36:'
            'x=40:y=40:enable=\'between(t,210,240)\''
        ),
        '-f', 'lavfi',
        '-i', 'sine=frequency=440:duration=240',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-crf', '28',
        '-c:a', 'aac',
        '-b:a', '64k',
        '-t', '240',
        VIDEO_FILE
    ]

    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'ffmpeg error: {result.stderr}')
        # Fallback: simpler video generation
        simple_cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', 'testsrc2=size=1280x720:duration=240:rate=24',
            '-f', 'lavfi',
            '-i', 'sine=frequency=440:duration=240',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-crf', '28',
            '-c:a', 'aac',
            '-b:a', '64k',
            '-t', '240',
            VIDEO_FILE
        ]
        result2 = subprocess.run(simple_cmd, capture_output=True, text=True)
        if result2.returncode != 0:
            print(f'Fallback ffmpeg error: {result2.stderr}')
            raise RuntimeError('Failed to create video file')
    print(f'Video created: {VIDEO_FILE}')


def create_documents_dir():
    """Create the documents directory (empty, agent will create travel_essay.odt here)."""
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    print(f'Documents directory created: {DOCUMENTS_DIR}')
    # Ensure NO pre-existing travel_essay.odt or PDF
    for fname in ['travel_essay.odt', 'travel_essay.pdf']:
        fpath = os.path.join(DOCUMENTS_DIR, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)
            print(f'Removed pre-existing: {fpath}')


def check_tools():
    """Verify required tools are installed on the VM."""
    for tool in ['ffmpeg', 'gimp']:
        result = subprocess.run(['which', tool], capture_output=True, text=True)
        if result.returncode == 0:
            print(f'Tool available: {tool} -> {result.stdout.strip()}')
        else:
            print(f'WARNING: Tool not found: {tool}')


def create_initial():
    check_tools()
    create_video()
    create_documents_dir()

    # GUI-ready: Open file manager at the videos directory
    launch_gui(f'nautilus "{VIDEO_DIR}"', delay_sec=1.5)
    print('GUI_READY: launched nautilus file manager at videos directory with DISPLAY=:0')


create_initial()
