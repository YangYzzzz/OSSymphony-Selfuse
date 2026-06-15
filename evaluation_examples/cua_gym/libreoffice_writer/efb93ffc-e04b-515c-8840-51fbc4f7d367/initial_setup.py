"""
Initial Setup: Create python_tutorial.odt on Desktop with mixed Python code and explanatory text
Task ID: osworld_multi_apps_code_to_writer_file_001
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.text import P
from odf.style import Style, TextProperties, ParagraphProperties
from odf import style as odf_style

WORKDIR = '/home/user/Desktop'  # VM path — file goes on Desktop
TASK_ID = 'osworld_multi_apps_code_to_writer_file_001'
OUTPUT = f'{WORKDIR}/python_tutorial.odt'


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
    os.makedirs(WORKDIR, exist_ok=True)

    doc = OpenDocumentText()

    # Define a monospace style for code lines (optional, makes it look like a tutorial)
    code_style = Style(name="CodeStyle", family="paragraph")
    code_style.addElement(TextProperties(fontname="Courier New", fontsize="11pt"))
    doc.styles.addElement(code_style)

    # 40 lines: alternating Python code lines and English explanatory text
    # The content is a Python tutorial mixing code examples with explanations
    lines = [
        # Line 1: explanation
        ("text", "This tutorial demonstrates how to work with data in Python using basic programming constructs."),
        # Line 2: code
        ("code", "import os"),
        # Line 3: explanation
        ("text", "The os module provides a way of using operating system dependent functionality."),
        # Line 4: code
        ("code", "import sys"),
        # Line 5: explanation
        ("text", "We also import sys to access system-specific parameters and functions during runtime."),
        # Line 6: code
        ("code", "import math"),
        # Line 7: explanation
        ("text", "The math module provides access to mathematical functions defined by the C standard."),
        # Line 8: code
        ("code", "data = [3, 7, 12, 5, 9, 14, 2, 8, 11, 6]"),
        # Line 9: explanation
        ("text", "Here we define a list of integer values that we will process throughout this tutorial."),
        # Line 10: code
        ("code", "total = 0"),
        # Line 11: explanation
        ("text", "We initialize a variable called total to accumulate the sum of the numbers."),
        # Line 12: code
        ("code", "def calculate_average(numbers):"),
        # Line 13: explanation
        ("text", "This function takes a list of numbers and returns their arithmetic mean."),
        # Line 14: code
        ("code", "    if len(numbers) == 0:"),
        # Line 15: explanation
        ("text", "We first check whether the list is empty to avoid a division by zero error."),
        # Line 16: code
        ("code", "        return 0"),
        # Line 17: explanation
        ("text", "If the list has no elements we return zero as a safe default value."),
        # Line 18: code
        ("code", "    result = sum(numbers) / len(numbers)"),
        # Line 19: explanation
        ("text", "Otherwise we compute the sum divided by the count to get the average."),
        # Line 20: code
        ("code", "    return result"),
        # Line 21: explanation
        ("text", "The function returns the computed result to the caller."),
        # Line 22: code
        ("code", "for item in data:"),
        # Line 23: explanation
        ("text", "We iterate over each element in the data list using a for loop."),
        # Line 24: code
        ("code", "    total = total + item"),
        # Line 25: explanation
        ("text", "During each iteration we add the current item value to our running total."),
        # Line 26: code
        ("code", "average = calculate_average(data)"),
        # Line 27: explanation
        ("text", "After the loop we call our function to compute the average of the dataset."),
        # Line 28: code
        ("code", "print('Data:', data)"),
        # Line 29: explanation
        ("text", "We print the original data list to verify the values we are working with."),
        # Line 30: code
        ("code", "print('Total:', total)"),
        # Line 31: explanation
        ("text", "We print the accumulated total to confirm our summation loop worked correctly."),
        # Line 32: code
        ("code", "print('Average:', average)"),
        # Line 33: explanation
        ("text", "Printing the average shows us the central tendency of the dataset."),
        # Line 34: code
        ("code", "if average > 7:"),
        # Line 35: explanation
        ("text", "Now we check whether the computed average exceeds the threshold value of seven."),
        # Line 36: code
        ("code", "    print('Above threshold')"),
        # Line 37: explanation
        ("text", "If the average is above the threshold we display a message indicating this result."),
        # Line 38: code
        ("code", "max_value = max(data)"),
        # Line 39: explanation
        ("text", "We also find the maximum value in the dataset for additional statistical insight."),
        # Line 40: code
        ("code", "print('Max:', max_value)"),
    ]

    for line_type, line_text in lines:
        if line_type == "code":
            p = P(stylename="CodeStyle", text=line_text)
        else:
            p = P(text=line_text)
        doc.text.addElement(p)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the .odt file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
