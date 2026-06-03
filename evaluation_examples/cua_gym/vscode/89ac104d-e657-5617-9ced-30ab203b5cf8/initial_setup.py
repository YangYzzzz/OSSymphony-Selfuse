"""
Initial Setup: Save the currently open file in VSCode
Task ID: vscode_stu_005
Domain: vscode

Creates a realistic Python file (main.py), opens it in VSCode,
then types additional text via Xlib to create unsaved changes (dot indicator on tab).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_005'
MAIN_PY = f'{WORKDIR}/main.py'


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


def send_keys_xlib(keys_sequence):
    """Send keystrokes using Xlib (since xdotool is not available)."""
    import Xlib
    from Xlib import X, display, XK
    from Xlib.ext import xtest

    d = display.Display(":0")
    time.sleep(0.1)

    key_map = {
        'Return': 'Return',
        'End': 'End',
        'ctrl': 'Control_L',
    }

    for action in keys_sequence:
        if action == 'sleep':
            time.sleep(0.3)
            continue
        if isinstance(action, tuple) and action[0] == 'sleep':
            time.sleep(action[1])
            continue
        if isinstance(action, tuple) and action[0] == 'type':
            # Type a string character by character
            text = action[1]
            for ch in text:
                keysym = XK.string_to_keysym(ch)
                if keysym == 0:
                    # Try direct character lookup
                    keysym = ord(ch)
                keycode = d.keysym_to_keycode(keysym)
                if keycode:
                    # Check if shift is needed
                    need_shift = ch.isupper() or ch in '!@#$%^&*()_+{}|:"<>?~'
                    if need_shift:
                        shift_code = d.keysym_to_keycode(XK.string_to_keysym('Shift_L'))
                        xtest.fake_input(d, X.KeyPress, shift_code)
                        d.sync()
                    xtest.fake_input(d, X.KeyPress, keycode)
                    d.sync()
                    time.sleep(0.02)
                    xtest.fake_input(d, X.KeyRelease, keycode)
                    d.sync()
                    if need_shift:
                        xtest.fake_input(d, X.KeyRelease, shift_code)
                        d.sync()
                    time.sleep(0.02)
            continue
        if isinstance(action, tuple) and action[0] == 'combo':
            # Press modifier+key combo
            modifier_name, key_name = action[1], action[2]
            mod_keysym = XK.string_to_keysym(key_map.get(modifier_name, modifier_name))
            key_keysym = XK.string_to_keysym(key_map.get(key_name, key_name))
            mod_keycode = d.keysym_to_keycode(mod_keysym)
            key_keycode = d.keysym_to_keycode(key_keysym)
            xtest.fake_input(d, X.KeyPress, mod_keycode)
            d.sync()
            time.sleep(0.05)
            xtest.fake_input(d, X.KeyPress, key_keycode)
            d.sync()
            time.sleep(0.05)
            xtest.fake_input(d, X.KeyRelease, key_keycode)
            d.sync()
            xtest.fake_input(d, X.KeyRelease, mod_keycode)
            d.sync()
            time.sleep(0.1)
            continue
        if isinstance(action, str):
            # Press single key
            keysym = XK.string_to_keysym(key_map.get(action, action))
            keycode = d.keysym_to_keycode(keysym)
            if keycode:
                xtest.fake_input(d, X.KeyPress, keycode)
                d.sync()
                time.sleep(0.05)
                xtest.fake_input(d, X.KeyRelease, keycode)
                d.sync()
                time.sleep(0.1)

    d.close()


def create_initial():
    # Create a realistic Python file that a student might be working on
    content = '''"""
Student Grade Calculator
Course: CS201 - Data Structures
Author: Jamie Park
Date: 2026-03-28
"""

import statistics


def load_grades():
    """Load student grades from the gradebook."""
    gradebook = {
        "Alice Wang": [92, 88, 95, 91, 87],
        "Ben Torres": [78, 82, 75, 80, 85],
        "Chloe Kim": [95, 97, 93, 98, 96],
        "David Osei": [65, 70, 72, 68, 74],
        "Elena Petrov": [88, 85, 90, 82, 87],
        "Frank Nguyen": [91, 89, 94, 90, 88],
        "Grace Liu": [73, 78, 80, 76, 71],
        "Hassan Ali": [86, 84, 88, 90, 85],
    }
    return gradebook


def calculate_average(grades):
    """Calculate the average of a list of grades."""
    return statistics.mean(grades)


def calculate_letter_grade(average):
    """Convert numeric average to letter grade."""
    if average >= 93:
        return "A"
    elif average >= 90:
        return "A-"
    elif average >= 87:
        return "B+"
    elif average >= 83:
        return "B"
    elif average >= 80:
        return "B-"
    elif average >= 77:
        return "C+"
    elif average >= 73:
        return "C"
    elif average >= 70:
        return "C-"
    elif average >= 67:
        return "D+"
    elif average >= 60:
        return "D"
    else:
        return "F"


def generate_report(gradebook):
    """Generate a summary report for all students."""
    print("=" * 55)
    print(f"{'Student':<20} {'Average':>8} {'Grade':>6}")
    print("-" * 55)

    averages = []
    for student, grades in sorted(gradebook.items()):
        avg = calculate_average(grades)
        letter = calculate_letter_grade(avg)
        averages.append(avg)
        print(f"{student:<20} {avg:>8.1f} {letter:>6}")

    print("-" * 55)
    class_avg = statistics.mean(averages)
    print(f"{'Class Average':<20} {class_avg:>8.1f}")
    print(f"{'Highest':<20} {max(averages):>8.1f}")
    print(f"{'Lowest':<20} {min(averages):>8.1f}")
    print("=" * 55)


if __name__ == "__main__":
    grades = load_grades()
    generate_report(grades)
'''

    os.makedirs(WORKDIR, exist_ok=True)
    with open(MAIN_PY, 'w') as f:
        f.write(content)
    print(f'Initial file created: {MAIN_PY}')

    # Open the file in VSCode
    launch_gui(f'code "{MAIN_PY}"', delay_sec=5.0)
    print('VSCode launched with main.py')

    # Wait for VSCode to fully load the file
    time.sleep(3.0)

    # Use Xlib to send keystrokes to create unsaved changes
    # Move to end of file (Ctrl+End), add a new line with a comment
    send_keys_xlib([
        ('combo', 'ctrl', 'End'),       # Go to end of file
        ('sleep', 0.5),
        'Return',                         # New line
        ('sleep', 0.3),
        ('type', '# TODO: Add export to CSV functionality'),  # Type new text
        ('sleep', 0.5),
    ])

    print('Typed additional text to create unsaved changes (dot on tab)')
    print('GUI_READY: launched VSCode with DISPLAY=:0, file has unsaved modifications')


create_initial()
