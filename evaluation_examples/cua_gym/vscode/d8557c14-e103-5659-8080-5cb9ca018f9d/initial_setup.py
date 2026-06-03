"""
Initial Setup: Create a C project workspace for macOS-style LLDB debugging
Task ID: vscode_td_092
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_092'
PROJECT_DIR = f'{WORKDIR}/projects/macos-app'
SRC_DIR = f'{PROJECT_DIR}/src'


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
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/build', exist_ok=True)

    # --- Makefile ---
    makefile_content = """CC = gcc
CFLAGS = -Wall -Wextra -g -std=c11
SRCDIR = src
BUILDDIR = build
TARGET = $(BUILDDIR)/app

SOURCES = $(wildcard $(SRCDIR)/*.c)
OBJECTS = $(patsubst $(SRCDIR)/%.c, $(BUILDDIR)/%.o, $(SOURCES))

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJECTS)
\t$(CC) $(CFLAGS) -o $@ $^

$(BUILDDIR)/%.o: $(SRCDIR)/%.c | $(BUILDDIR)
\t$(CC) $(CFLAGS) -c -o $@ $<

$(BUILDDIR):
\tmkdir -p $(BUILDDIR)

clean:
\trm -rf $(BUILDDIR)/*
"""
    with open(f'{PROJECT_DIR}/Makefile', 'w') as f:
        f.write(makefile_content)

    # --- src/main.c ---
    main_c = """#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

#define MAX_ITEMS 100

typedef struct {
    char name[64];
    double price;
    int quantity;
} InventoryItem;

static InventoryItem inventory[MAX_ITEMS];
static int item_count = 0;

void add_item(const char *name, double price, int quantity) {
    if (item_count >= MAX_ITEMS) {
        fprintf(stderr, "Inventory full\\n");
        return;
    }
    snprintf(inventory[item_count].name, sizeof(inventory[item_count].name), "%s", name);
    inventory[item_count].price = price;
    inventory[item_count].quantity = quantity;
    item_count++;
}

void print_inventory(void) {
    printf("%-20s %10s %8s %12s\\n", "Item", "Price", "Qty", "Total");
    printf("%-20s %10s %8s %12s\\n", "----", "-----", "---", "-----");
    double grand_total = 0.0;
    for (int i = 0; i < item_count; i++) {
        double total = inventory[i].price * inventory[i].quantity;
        grand_total += total;
        printf("%-20s %10.2f %8d %12.2f\\n",
               inventory[i].name, inventory[i].price,
               inventory[i].quantity, total);
    }
    printf("\\n%-20s %10s %8s %12.2f\\n", "Grand Total", "", "", grand_total);
}

int main(int argc, char *argv[]) {
    printf("Inventory Management System v%s\\n\\n", get_version());

    add_item("Wireless Mouse", 29.99, 150);
    add_item("Mechanical Keyboard", 89.95, 75);
    add_item("USB-C Hub", 45.50, 200);
    add_item("Monitor Stand", 34.99, 120);
    add_item("Webcam HD", 59.99, 90);

    print_inventory();

    double avg = calculate_average(29.99 * 150 + 89.95 * 75 + 45.50 * 200
                                   + 34.99 * 120 + 59.99 * 90, 5);
    printf("\\nAverage item total: $%.2f\\n", avg);

    return 0;
}
"""
    with open(f'{SRC_DIR}/main.c', 'w') as f:
        f.write(main_c)

    # --- src/utils.h ---
    utils_h = """#ifndef UTILS_H
#define UTILS_H

const char *get_version(void);
double calculate_average(double sum, int count);
int clamp_int(int value, int min_val, int max_val);

#endif /* UTILS_H */
"""
    with open(f'{SRC_DIR}/utils.h', 'w') as f:
        f.write(utils_h)

    # --- src/utils.c ---
    utils_c = """#include "utils.h"

static const char *VERSION = "1.2.0";

const char *get_version(void) {
    return VERSION;
}

double calculate_average(double sum, int count) {
    if (count == 0) return 0.0;
    return sum / (double)count;
}

int clamp_int(int value, int min_val, int max_val) {
    if (value < min_val) return min_val;
    if (value > max_val) return max_val;
    return value;
}
"""
    with open(f'{SRC_DIR}/utils.c', 'w') as f:
        f.write(utils_c)

    # --- .gitignore ---
    gitignore = """build/
*.o
*.d
.DS_Store
"""
    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write(gitignore)

    # --- README.md ---
    readme = """# macOS Inventory App

A simple inventory management system written in C.

## Building

```bash
make
```

## Running

```bash
./build/app
```

## Cleaning

```bash
make clean
```
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    # Ensure NO .vscode directory exists (task requires creating launch.json)
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial project created at: {PROJECT_DIR}')
    print(f'Files: Makefile, src/main.c, src/utils.c, src/utils.h, .gitignore, README.md')
    print(f'No .vscode/launch.json exists (task requires creating it)')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
