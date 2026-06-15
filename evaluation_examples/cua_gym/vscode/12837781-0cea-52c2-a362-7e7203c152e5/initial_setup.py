"""
Initial Setup: Create a C project workspace for VSCode debugging task
Task ID: vscode_lang_078
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import stat

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_078'
PROJECT_DIR = f'{WORKDIR}/projects/mycapp'
BUILD_DIR = f'{PROJECT_DIR}/build'

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
    # Create project directory structure
    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # Create main.c with realistic C code
    main_c = '''\
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 100
#define NAME_LEN 64

typedef struct {
    char name[NAME_LEN];
    int age;
    float gpa;
} Student;

static Student roster[MAX_STUDENTS];
static int roster_count = 0;

int add_student(const char *name, int age, float gpa) {
    if (roster_count >= MAX_STUDENTS) {
        fprintf(stderr, "Error: roster is full\\n");
        return -1;
    }
    strncpy(roster[roster_count].name, name, NAME_LEN - 1);
    roster[roster_count].name[NAME_LEN - 1] = '\\0';
    roster[roster_count].age = age;
    roster[roster_count].gpa = gpa;
    roster_count++;
    return 0;
}

void print_roster(void) {
    printf("%-20s %5s %6s\\n", "Name", "Age", "GPA");
    printf("%-20s %5s %6s\\n", "----", "---", "---");
    for (int i = 0; i < roster_count; i++) {
        printf("%-20s %5d %6.2f\\n",
               roster[i].name, roster[i].age, roster[i].gpa);
    }
    printf("\\nTotal students: %d\\n", roster_count);
}

float average_gpa(void) {
    if (roster_count == 0) return 0.0f;
    float sum = 0.0f;
    for (int i = 0; i < roster_count; i++) {
        sum += roster[i].gpa;
    }
    return sum / roster_count;
}

int main(int argc, char *argv[]) {
    printf("Student Roster Manager v1.0\\n\\n");

    add_student("Alice Wang", 20, 3.85);
    add_student("Bob Martinez", 22, 3.42);
    add_student("Carol Nakamura", 21, 3.91);
    add_student("David Okonkwo", 23, 3.67);
    add_student("Eva Lindqvist", 20, 3.78);

    print_roster();
    printf("\\nAverage GPA: %.2f\\n", average_gpa());

    return 0;
}
'''
    with open(f'{PROJECT_DIR}/src/main.c', 'w') as f:
        f.write(main_c)

    # Also place main.c in project root for convenience
    with open(f'{PROJECT_DIR}/main.c', 'w') as f:
        f.write(main_c)

    # Create Makefile
    makefile = '''\
CC = gcc
CFLAGS = -Wall -Wextra -g -O0
SRCDIR = src
BUILDDIR = build
TARGET = $(BUILDDIR)/main

SOURCES = $(wildcard $(SRCDIR)/*.c)
OBJECTS = $(patsubst $(SRCDIR)/%.c,$(BUILDDIR)/%.o,$(SOURCES))

all: $(TARGET)

$(TARGET): $(OBJECTS)
\t$(CC) $(CFLAGS) -o $@ $^

$(BUILDDIR)/%.o: $(SRCDIR)/%.c | $(BUILDDIR)
\t$(CC) $(CFLAGS) -c -o $@ $<

$(BUILDDIR):
\tmkdir -p $(BUILDDIR)

clean:
\trm -rf $(BUILDDIR)/*

.PHONY: all clean
'''
    with open(f'{PROJECT_DIR}/Makefile', 'w') as f:
        f.write(makefile)

    # Create a fake compiled binary (build/main) with debug symbols marker
    # This simulates a compiled C binary existing in the build directory
    fake_binary = '#!/bin/sh\necho "Student Roster Manager v1.0"\n'
    binary_path = f'{BUILD_DIR}/main'
    with open(binary_path, 'w') as f:
        f.write(fake_binary)
    os.chmod(binary_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    # Create a simple README
    readme = '''\
# Student Roster Manager

A simple C program that manages a student roster with names, ages, and GPAs.

## Build

```
make
```

## Run

```
./build/main
```

## Debug

Use GDB or configure VSCode debugging with the C/C++ extension.
'''
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # Ensure NO .vscode/launch.json exists (the task is to create it)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json_path = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'  main.c: {PROJECT_DIR}/src/main.c')
    print(f'  Makefile: {PROJECT_DIR}/Makefile')
    print(f'  Binary: {BUILD_DIR}/main')
    print(f'  .vscode/launch.json: DOES NOT EXIST (task target)')

    # Open VSCode with the project workspace
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
