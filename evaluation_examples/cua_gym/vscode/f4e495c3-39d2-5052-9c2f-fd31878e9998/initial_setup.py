"""
Initial Setup: Set up a C project with main.c for debugging configuration task
Task ID: vscode_stu_065
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_065'
PROJECT_DIR = os.path.join(WORKDIR, 'cs201', 'project')


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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a realistic main.c file
    main_c_content = """\
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 50
#define NAME_LEN 64

typedef struct {
    char name[NAME_LEN];
    int id;
    float gpa;
} Student;

static int count = 0;
static Student roster[MAX_STUDENTS];

void add_student(const char *name, int id, float gpa) {
    if (count >= MAX_STUDENTS) {
        fprintf(stderr, "Error: roster is full\\n");
        return;
    }
    strncpy(roster[count].name, name, NAME_LEN - 1);
    roster[count].name[NAME_LEN - 1] = '\\0';
    roster[count].id = id;
    roster[count].gpa = gpa;
    count++;
}

void print_roster(void) {
    printf("%-20s %8s %6s\\n", "Name", "ID", "GPA");
    printf("--------------------------------------\\n");
    for (int i = 0; i < count; i++) {
        printf("%-20s %8d %6.2f\\n",
               roster[i].name, roster[i].id, roster[i].gpa);
    }
    printf("\\nTotal students: %d\\n", count);
}

float average_gpa(void) {
    if (count == 0) return 0.0f;
    float sum = 0.0f;
    for (int i = 0; i < count; i++) {
        sum += roster[i].gpa;
    }
    return sum / count;
}

int main(void) {
    add_student("Alice Wang", 10234, 3.85);
    add_student("Brian Torres", 10412, 3.42);
    add_student("Carmen Liu", 10587, 3.91);
    add_student("Derek Patel", 10603, 3.15);
    add_student("Elena Novak", 10789, 3.67);

    print_roster();
    printf("\\nAverage GPA: %.2f\\n", average_gpa());

    return 0;
}
"""
    main_c_path = os.path.join(PROJECT_DIR, 'main.c')
    with open(main_c_path, 'w') as f:
        f.write(main_c_content)
    print(f'Created: {main_c_path}')

    # Ensure NO .vscode directory exists (clean state)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)
    print('Ensured no .vscode directory exists')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
