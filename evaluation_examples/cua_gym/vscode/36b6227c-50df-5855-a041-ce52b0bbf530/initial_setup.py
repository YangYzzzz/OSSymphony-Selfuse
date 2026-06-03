"""
Initial Setup: Create a C project workspace in VSCode with no custom snippets
Task ID: vscode_lang_094
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_094'
PROJECT_DIR = f'{WORKDIR}/c_project'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SNIPPETS_DIR = os.path.join(VSCODE_USER, 'snippets')

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
    # Create a realistic C project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'src'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'include'), exist_ok=True)

    # Create main.c
    main_c = """\
#include <stdio.h>
#include "utils.h"
#include "config.h"

int main(int argc, char *argv[]) {
    printf("Temperature Sensor Monitor v1.2\\n");

    sensor_config_t cfg = load_default_config();
    if (argc > 1) {
        cfg.sample_rate = atoi(argv[1]);
    }

    double readings[MAX_READINGS];
    int count = collect_readings(readings, cfg.sample_rate);

    double avg = compute_average(readings, count);
    printf("Average temperature: %.2f C\\n", avg);

    return 0;
}
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'main.c'), 'w') as f:
        f.write(main_c)

    # Create utils.h with manually typed include guard
    utils_h = """\
#ifndef UTILS_H
#define UTILS_H

#define MAX_READINGS 1024

double compute_average(double *data, int n);
double compute_stddev(double *data, int n);
int collect_readings(double *out, int sample_rate);
void filter_outliers(double *data, int *n, double threshold);

#endif
"""
    with open(os.path.join(PROJECT_DIR, 'include', 'utils.h'), 'w') as f:
        f.write(utils_h)

    # Create config.h with manually typed include guard
    config_h = """\
#ifndef CONFIG_H
#define CONFIG_H

typedef struct {
    int sample_rate;
    int max_retries;
    double timeout_sec;
    char device_path[256];
} sensor_config_t;

sensor_config_t load_default_config(void);
int save_config(const char *path, const sensor_config_t *cfg);

#endif
"""
    with open(os.path.join(PROJECT_DIR, 'include', 'config.h'), 'w') as f:
        f.write(config_h)

    # Create utils.c
    utils_c = """\
#include "utils.h"
#include <math.h>
#include <stdlib.h>

double compute_average(double *data, int n) {
    if (n <= 0) return 0.0;
    double sum = 0.0;
    for (int i = 0; i < n; i++) {
        sum += data[i];
    }
    return sum / n;
}

double compute_stddev(double *data, int n) {
    double avg = compute_average(data, n);
    double sum_sq = 0.0;
    for (int i = 0; i < n; i++) {
        double diff = data[i] - avg;
        sum_sq += diff * diff;
    }
    return sqrt(sum_sq / n);
}

int collect_readings(double *out, int sample_rate) {
    /* Stub: simulate sensor readings */
    int count = sample_rate * 10;
    if (count > MAX_READINGS) count = MAX_READINGS;
    for (int i = 0; i < count; i++) {
        out[i] = 20.0 + (rand() % 100) / 10.0;
    }
    return count;
}

void filter_outliers(double *data, int *n, double threshold) {
    double avg = compute_average(data, *n);
    int write_idx = 0;
    for (int i = 0; i < *n; i++) {
        if (fabs(data[i] - avg) <= threshold) {
            data[write_idx++] = data[i];
        }
    }
    *n = write_idx;
}
"""
    with open(os.path.join(PROJECT_DIR, 'src', 'utils.c'), 'w') as f:
        f.write(utils_c)

    # Create a Makefile
    makefile = """\
CC = gcc
CFLAGS = -Wall -Wextra -I../include -std=c11
LDFLAGS = -lm

SRC = src/main.c src/utils.c
OBJ = $(SRC:.c=.o)
TARGET = sensor_monitor

all: $(TARGET)

$(TARGET): $(SRC)
\t$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
\trm -f $(TARGET) $(OBJ)

.PHONY: all clean
"""
    with open(os.path.join(PROJECT_DIR, 'Makefile'), 'w') as f:
        f.write(makefile)

    # Create a new empty header file (for the user to test the snippet on)
    new_header = """\
/* New sensor types - TODO: add header guard */

"""
    with open(os.path.join(PROJECT_DIR, 'include', 'sensor_types.h'), 'w') as f:
        f.write(new_header)

    # Ensure NO custom C snippets exist
    c_snippet_path = os.path.join(SNIPPETS_DIR, 'c.json')
    if os.path.exists(c_snippet_path):
        os.remove(c_snippet_path)

    print(f'C project created at: {PROJECT_DIR}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
