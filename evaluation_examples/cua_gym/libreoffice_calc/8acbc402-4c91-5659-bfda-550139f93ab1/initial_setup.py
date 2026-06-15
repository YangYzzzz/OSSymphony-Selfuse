"""
Initial Setup: Word frequency script with stubbed functions and article text file.
Task ID: osworld_multi_apps_code_script_output_006
Domain: os / code-script
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'osworld_multi_apps_code_script_output_006'
SCRIPTS_DIR = f'{WORKDIR}/scripts'
DATA_DIR = f'{WORKDIR}/data'
SCRIPT_PATH = f'{SCRIPTS_DIR}/word_frequency.py'
ARTICLE_PATH = f'{DATA_DIR}/article.txt'


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
    # Create required directories
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    # --- Create the stubbed word_frequency.py script ---
    script_content = '''#!/usr/bin/env python3
"""
Word Frequency Analyzer
Reads a text file and computes word frequencies.
"""

import re
import sys
from collections import Counter


def count_words(text):
    """
    Count word frequencies in text.

    Args:
        text (str): Input text to analyze.

    Returns:
        dict: A dictionary mapping word -> count (case-insensitive,
              punctuation stripped, only alphabetic tokens counted).
    """
    # TODO: Implement this function
    # - Convert text to lowercase
    # - Extract alphabetic words using regex [a-zA-Z]+
    # - Count occurrences of each word
    # - Return as a dict (or Counter)
    pass


def top_n_words(freq_dict, n):
    """
    Return the N most frequent words sorted by count descending.

    Args:
        freq_dict (dict): Word frequency dictionary from count_words().
        n (int): Number of top words to return.

    Returns:
        list: A list of (word, count) tuples sorted by count descending.
              For ties, order is unspecified.
    """
    # TODO: Implement this function
    # - Sort items from freq_dict by count descending
    # - Return the top n items as a list of (word, count) tuples
    pass


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 word_frequency.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = '/home/user/data/word_freq.txt'
    n = 10

    with open(input_file, 'r') as f:
        text = f.read()

    freq = count_words(text)
    top_words = top_n_words(freq, n)

    with open(output_file, 'w') as f:
        for word, count in top_words:
            f.write(f"{word}: {count}\\n")

    print(f"Top {n} words saved to {output_file}")


if __name__ == '__main__':
    main()
'''
    with open(SCRIPT_PATH, 'w') as f:
        f.write(script_content)
    os.chmod(SCRIPT_PATH, 0o755)
    print(f'Script created: {SCRIPT_PATH}')

    # --- Create the article.txt file (approx 500 words) ---
    article_content = '''Climate technology has emerged as one of the most important fields in modern science and engineering.
As global temperatures continue to rise, researchers and engineers are working to develop innovative
solutions that can help reduce carbon emissions and build a more sustainable future for humanity.

Solar energy represents one of the most promising areas of renewable technology. Over the past decade,
the cost of solar panels has dropped dramatically, making solar power more accessible to communities
around the world. Engineers have developed new materials and manufacturing processes that improve
the efficiency of solar cells, allowing them to convert more sunlight into usable electricity.

Wind energy is another important source of renewable power. Modern wind turbines are much larger and
more efficient than older designs, capable of generating significant amounts of electricity from
relatively modest wind speeds. Offshore wind farms have become increasingly popular, as ocean winds
tend to be stronger and more consistent than winds on land.

Energy storage technology is crucial for the widespread adoption of renewable energy. Since solar and
wind power generation depends on weather conditions, efficient energy storage systems are needed to
ensure a reliable electricity supply. Battery technology has advanced rapidly in recent years, with
new lithium-ion designs offering higher energy density and longer lifespans than previous generations.

Climate scientists study the complex interactions between the atmosphere, oceans, and land surfaces
to better understand how human activities affect global climate patterns. Their research provides
critical data that helps policymakers and engineers develop more effective strategies for reducing
carbon emissions and adapting to changing climate conditions.

The energy transition requires significant investment in new infrastructure and technology. Governments
and private companies are investing billions of dollars in research and development, hoping to
accelerate the pace of technological innovation. Many experts believe that the next decade will
see dramatic improvements in renewable energy technology, energy storage, and energy efficiency.

Transportation is also undergoing a major transformation as electric vehicles become more affordable
and practical. Modern electric cars can travel hundreds of miles on a single charge and are becoming
increasingly popular as consumers seek more sustainable transportation options. The development of
better battery technology and charging infrastructure will be essential for the continued growth
of the electric vehicle market.

Climate change presents significant challenges for agriculture and food production. Rising temperatures
and changing precipitation patterns are affecting crop yields in many regions of the world. Scientists
and farmers are working together to develop more resilient crop varieties and farming practices that
can help ensure food security in a changing climate. Technology will play an essential role in helping
agriculture adapt to these new challenges and opportunities.

Building a sustainable energy future requires collaboration between governments, research institutions,
private industry, and local communities. Each sector brings unique resources, expertise, and perspectives
that are vital for accelerating the transition to clean energy technologies and addressing the global
climate crisis effectively.
'''
    with open(ARTICLE_PATH, 'w') as f:
        f.write(article_content)
    print(f'Article created: {ARTICLE_PATH}')

    # Verify word_freq.txt does NOT exist in initial state
    word_freq_path = f'{DATA_DIR}/word_freq.txt'
    if os.path.exists(word_freq_path):
        os.remove(word_freq_path)
        print(f'Removed existing word_freq.txt to ensure clean initial state')

    # GUI-ready startup: open a terminal with the script visible
    # The agent needs to edit the Python script, so open it in a text editor
    launch_gui(f'gedit "{SCRIPT_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched gedit with word_frequency.py open on DISPLAY=:0')


create_initial()
