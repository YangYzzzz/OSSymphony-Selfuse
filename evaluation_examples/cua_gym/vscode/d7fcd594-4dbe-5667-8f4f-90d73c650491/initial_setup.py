"""
Initial Setup: Set word wrap column to 80 in VSCode for essay.txt
Task ID: vscode_edit_047
Domain: vs_code

Creates ~/Desktop/essay.txt with long paragraphs (lines > 200 chars).
VSCode settings have editor.wordWrap = "on" (viewport wrap), but
editor.wordWrapColumn is NOT set to 80 and editor.wordWrap is NOT
"wordWrapColumn". The agent must change these settings.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_047'
DESKTOP = f'{WORKDIR}/Desktop'
ESSAY_PATH = f'{DESKTOP}/essay.txt'
VSCODE_USER = f'{WORKDIR}/.config/Code/User'
SETTINGS_PATH = f'{VSCODE_USER}/settings.json'


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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Handle JSONC comments
        import re
        content_clean = re.sub(r'//[^\n]*', '', content)
        return json.loads(content_clean)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_settings(settings: dict):
    os.makedirs(VSCODE_USER, exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # 1. Create Desktop directory if needed
    os.makedirs(DESKTOP, exist_ok=True)

    # 2. Create essay.txt with long-line paragraphs (lines > 200 chars)
    essay_content = """\
The Industrial Revolution, which began in Britain during the late 18th century and spread across Europe and North America throughout the 19th century, fundamentally transformed every aspect of human society, from the organization of labor and production to the very fabric of daily life, social structures, and the relationship between humanity and the natural world.

Economic historians have long debated the precise causes and consequences of this remarkable period of change, with some emphasizing the role of technological innovation, particularly the steam engine invented by James Watt in 1769, while others point to the accumulation of capital, the enclosure of common lands, or the expansion of global trade networks as equally or more decisive factors in driving the transition from agrarian to industrial economies.

The transformation of textile manufacturing, especially the mechanization of cotton spinning and weaving through inventions such as the spinning jenny, the water frame, and the power loom, stands as perhaps the most emblematic development of the early Industrial Revolution, concentrating production in large factories and displacing thousands of skilled artisans who had previously worked in their own homes or small workshops scattered across the countryside.

Urbanization accelerated at an unprecedented pace as workers migrated from rural areas to factory towns like Manchester, Birmingham, and Leeds, creating overcrowded and often squalid living conditions that shocked contemporary observers and reformers, who documented the miserable circumstances of the new industrial working class in reports, novels, and parliamentary investigations that eventually contributed to the passage of social reform legislation.

The environmental consequences of industrialization, though not fully understood or appreciated at the time, were equally profound and lasting, as coal-burning factories filled the air with smoke and soot, rivers became polluted with industrial waste and raw sewage from growing urban populations, and the extraction of raw materials reshaped landscapes across the coalfields and iron-producing regions of Britain, Belgium, Germany, and the eastern United States.

Scientific and technological progress during this era was not limited to manufacturing but extended to transportation, communication, agriculture, and medicine, with the development of the railway network, the telegraph, new agricultural machinery, and advances in public health and sanitation all contributing to a broader transformation of material conditions that, despite its uneven and often brutal social costs, ultimately laid the foundation for the dramatic improvements in living standards experienced by subsequent generations in the industrialized world.

Philosophers, economists, and social theorists of the 19th century grappled with the meaning and direction of these sweeping changes, producing an extraordinary range of responses from the laissez-faire liberalism of Adam Smith and his successors, who celebrated the wealth-generating power of free markets and the division of labor, to the socialist and communist critiques of Karl Marx and Friedrich Engels, who analyzed industrial capitalism as a system built on the exploitation of workers and predicted its eventual overthrow by a revolutionary proletariat.

The legacy of the Industrial Revolution remains deeply contested and highly relevant in the 21st century, as debates about automation, globalization, inequality, and climate change echo many of the fundamental tensions and transformations of that earlier period, reminding us that technological and economic revolutions always carry profound social, political, and environmental implications that extend far beyond the immediate gains in productivity and material output that first attract attention and investment.
"""

    with open(ESSAY_PATH, "w") as f:
        f.write(essay_content)
    print(f"Created essay file: {ESSAY_PATH}")

    # 3. Configure VSCode settings: wordWrap = "on" (viewport wrap), no wordWrapColumn = 80
    settings = load_settings()
    # Set wordWrap to "on" (wraps at viewport width, NOT at a specific column)
    settings["editor.wordWrap"] = "on"
    # Explicitly do NOT set editor.wordWrapColumn to 80
    # Remove any pre-existing wordWrapColumn or wordWrap = wordWrapColumn settings
    settings.pop("editor.wordWrapColumn", None)
    # Make sure wordWrap is NOT "wordWrapColumn"
    if settings.get("editor.wordWrap") == "wordWrapColumn":
        settings["editor.wordWrap"] = "on"
    write_settings(settings)
    print(f"VSCode settings configured: editor.wordWrap = 'on' (viewport)")
    print(f"Settings path: {SETTINGS_PATH}")

    # 4. GUI-ready startup: open essay.txt in VSCode
    launch_gui(f'code "{ESSAY_PATH}"', delay_sec=3.0)
    print(f"GUI_READY: launched VSCode with {ESSAY_PATH} on DISPLAY=:0")


create_initial()
