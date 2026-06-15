"""
Initial Setup: Create short story .txt files and open Chrome with epub tool info
Task ID: osworld_multi_apps_misc_068
Domain: multi_apps (OS + Chrome)
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_misc_068'
STORIES_DIR = f'{WORKDIR}/Documents/ShortStories'


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


def create_initial():
    # Create the ShortStories directory
    os.makedirs(STORIES_DIR, exist_ok=True)

    # Story 1: The Beginning
    story1 = """\
The Beginning

It was a morning unlike any other when Elara first discovered the old map tucked behind the
loose brick in her grandmother's attic. The parchment crinkled softly as she unfolded it,
releasing a scent of cedar and something else — something ancient.

"What is this?" she whispered to no one in particular.

The map showed the coastline of an island she had never heard of, marked with a red X
deep in its forested interior. Around the edges, tiny handwritten notes warned of tides,
currents, and something called the Warden's Path.

Elara had always been a careful, sensible person. She worked at the county library,
catalogued historical documents, and never took risks without thorough research. But holding
that map, she felt a pull she could not explain — a certainty that whatever lay at that X
was meant for her to find.

She took out her notebook and began to write down everything she observed.
"""

    # Story 2: Middle Ground
    story2 = """\
Middle Ground

Three days into her journey, Elara found herself on a creaking ferry crossing to the island.
The other passengers were locals heading home — fishermen with weathered faces, a schoolteacher
with a box of textbooks, a teenager glued to his phone despite the weak signal.

She had managed to locate the island on a 1952 nautical chart borrowed from the library archives.
It was called Vethara Isle, and aside from a brief mention in a 1920s expedition log, it had
scarcely appeared in any document she could find.

Her research had turned up one other clue: a photograph of a woman standing beside a carved
stone doorway, labeled simply "V. I., 1931." The woman had her grandmother's eyes.

The ferry docked at a small pier just as the afternoon light turned golden.
A sign read: VETHARA ISLE — POPULATION 84.

The schoolteacher noticed Elara studying the sign.
"Visitor?" he asked.
"Yes," she said. "I'm looking for something."
He smiled. "Aren't we all."
"""

    # Story 3: The Twist
    story3 = """\
The Twist

The forest was nothing like Elara had imagined. She had pictured dense, dramatic jungle — vines
and shadows. Instead, the interior of Vethara Isle was a calm woodland of silver birch and pine,
with a path worn smooth by decades of quiet footsteps.

She followed the map carefully, counting landmarks: a split boulder, a stream crossing,
three tall pines in a triangular formation. After two hours, she arrived at a small clearing.

At its center stood a stone structure — not dramatic, not towering. Just a low, square room,
no larger than a garden shed, with the carved doorway from the photograph.

Inside, on a wooden shelf, were forty-seven notebooks. Each one bore a name on its cover.
The last one on the shelf bore her name: ELARA VOSS.

She sat down slowly and opened it.
The first line read: "If you are reading this, the map reached you as intended. Welcome, Keeper."

The handwriting was her grandmother's.
"""

    # Story 4: Final Chapter
    story4 = """\
Final Chapter

For three days, Elara read. The notebook explained everything: the Keepers were a loose network
of archivists and researchers who had, since the early 1900s, quietly preserved records of
communities at risk of erasure — villages threatened by floods, languages dying out, histories
that powerful interests wanted forgotten.

Her grandmother, Marta Voss, had been the fourteenth Keeper. The stone room was a backup archive,
a place the network used when digital storage felt too fragile, too easily deleted.

Elara's notebook, pre-filled with her grandmother's notes, was both an invitation and a dossier.
It showed where the network needed her most: three projects, each one matching her professional
expertise almost too precisely.

She stepped outside into the late afternoon light. The ferry would come back in the morning.

She took out her own notebook — the blank one she always carried — and began to write her first
entry as Keeper. She didn't know yet what she would choose to preserve, or how long the work
would take. She knew only that it mattered, and that someone had believed, years before she was
ready, that she was the right person to do it.

That, she decided, was enough of a beginning.
"""

    # Write all story files
    Path(f'{STORIES_DIR}/The_Beginning.txt').write_text(story1)
    print(f'Created: {STORIES_DIR}/The_Beginning.txt')

    Path(f'{STORIES_DIR}/Middle_Ground.txt').write_text(story2)
    print(f'Created: {STORIES_DIR}/Middle_Ground.txt')

    Path(f'{STORIES_DIR}/The_Twist.txt').write_text(story3)
    print(f'Created: {STORIES_DIR}/The_Twist.txt')

    Path(f'{STORIES_DIR}/Final_Chapter.txt').write_text(story4)
    print(f'Created: {STORIES_DIR}/Final_Chapter.txt')

    print(f'All story files created in: {STORIES_DIR}')

    # Kill any existing Chrome instances before launching (avoid duplicates)
    subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True)
    time.sleep(1.5)

    # Launch Chrome with tabs showing EPUB conversion tools
    # Open Chrome with epub-related search/tool pages
    launch_gui(
        'google-chrome --new-window '
        '"https://github.com/nicowillis/txt2epub" '
        '"https://github.com/aerkalov/ebooklib" '
        '"https://calibre-ebook.com/download_linux"',
        delay_sec=3.0
    )

    # Open Nautilus file manager showing the ShortStories folder
    launch_gui(f'nautilus "{STORIES_DIR}"', delay_sec=2.0)

    print('GUI_READY: launched Chrome with epub tool tabs and Nautilus file manager')


create_initial()
