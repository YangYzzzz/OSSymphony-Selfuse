"""
Initial Setup: VSCode open with assignment.c shown as Plain Text language mode
Task ID: vscode_stu_012
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_012'
OUTPUT = f'{WORKDIR}/{TASK_ID}.c'

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


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
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_initial():
    # Create a realistic C assignment file
    c_content = """\
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 100
#define NAME_LEN 64

typedef struct {
    char name[NAME_LEN];
    int student_id;
    float gpa;
} Student;

Student roster[MAX_STUDENTS];
int roster_count = 0;

void add_student(const char *name, int id, float gpa) {
    if (roster_count >= MAX_STUDENTS) {
        fprintf(stderr, "Error: roster is full\\n");
        return;
    }
    strncpy(roster[roster_count].name, name, NAME_LEN - 1);
    roster[roster_count].name[NAME_LEN - 1] = '\\0';
    roster[roster_count].student_id = id;
    roster[roster_count].gpa = gpa;
    roster_count++;
}

void print_roster(void) {
    printf("%-30s %-10s %-6s\\n", "Name", "ID", "GPA");
    printf("----------------------------------------------\\n");
    for (int i = 0; i < roster_count; i++) {
        printf("%-30s %-10d %-6.2f\\n",
               roster[i].name,
               roster[i].student_id,
               roster[i].gpa);
    }
}

float calculate_average_gpa(void) {
    if (roster_count == 0) return 0.0f;
    float sum = 0.0f;
    for (int i = 0; i < roster_count; i++) {
        sum += roster[i].gpa;
    }
    return sum / roster_count;
}

int main(int argc, char *argv[]) {
    add_student("Sarah Chen", 10234, 3.85f);
    add_student("Marcus Johnson", 10412, 3.62f);
    add_student("Priya Patel", 10587, 3.91f);
    add_student("James O'Brien", 10103, 3.44f);
    add_student("Yuki Tanaka", 10678, 3.78f);

    printf("CS201 - Data Structures Roster\\n\\n");
    print_roster();
    printf("\\nAverage GPA: %.2f\\n", calculate_average_gpa());

    return 0;
}
"""
    os.makedirs(WORKDIR, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(c_content)
    print(f'Initial file created: {OUTPUT}')

    # Force VSCode to treat *.c files as plain text so the status bar shows "Plain Text"
    update_settings({
        "files.associations": {
            "*.c": "plaintext"
        }
    })
    print(f'VSCode settings updated: *.c mapped to plaintext')

    # Launch VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
