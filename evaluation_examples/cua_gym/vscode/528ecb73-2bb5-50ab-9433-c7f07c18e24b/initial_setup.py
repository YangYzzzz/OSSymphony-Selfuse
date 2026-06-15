"""
Initial Setup: Configure c_cpp_properties.json for C project with include path and C17 standard
Task ID: vscode_lang_079
Domain: vscode

Creates a C project with custom headers in include/ directory.
NO .vscode/c_cpp_properties.json exists — the agent must create it.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_079'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'


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
    os.makedirs(f'{PROJECT_DIR}/include', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)

    # --- Custom header: include/sensor_utils.h ---
    with open(f'{PROJECT_DIR}/include/sensor_utils.h', 'w') as f:
        f.write("""#ifndef SENSOR_UTILS_H
#define SENSOR_UTILS_H

#include <stdint.h>

typedef struct {
    uint16_t sensor_id;
    float temperature;
    float humidity;
    uint32_t timestamp;
} SensorReading;

/**
 * Initialize sensor subsystem with the given configuration.
 * Returns 0 on success, negative error code on failure.
 */
int sensor_init(uint16_t device_id, uint32_t sample_rate_hz);

/**
 * Read the latest sensor data into the provided struct.
 */
int sensor_read(SensorReading *reading);

/**
 * Calibrate sensor offset using a known reference temperature.
 */
void sensor_calibrate(float reference_temp);

/**
 * Shut down the sensor subsystem and release resources.
 */
void sensor_shutdown(void);

#endif /* SENSOR_UTILS_H */
""")

    # --- Custom header: include/data_logger.h ---
    with open(f'{PROJECT_DIR}/include/data_logger.h', 'w') as f:
        f.write("""#ifndef DATA_LOGGER_H
#define DATA_LOGGER_H

#include <stdio.h>
#include <stdbool.h>

#define MAX_LOG_ENTRIES 4096
#define LOG_FILENAME_MAX 256

typedef enum {
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_INFO,
    LOG_LEVEL_WARNING,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_CRITICAL
} LogLevel;

typedef struct {
    char filename[LOG_FILENAME_MAX];
    FILE *file_handle;
    LogLevel min_level;
    bool timestamps_enabled;
    unsigned long entry_count;
} DataLogger;

/**
 * Create a new data logger writing to the specified file.
 */
DataLogger *logger_create(const char *filename, LogLevel min_level);

/**
 * Write a log entry at the given level.
 */
int logger_write(DataLogger *logger, LogLevel level, const char *message);

/**
 * Flush pending log entries to disk.
 */
void logger_flush(DataLogger *logger);

/**
 * Close and destroy the logger, releasing all resources.
 */
void logger_destroy(DataLogger *logger);

#endif /* DATA_LOGGER_H */
""")

    # --- Main source file: src/main.c ---
    with open(f'{PROJECT_DIR}/src/main.c', 'w') as f:
        f.write("""#include <stdio.h>
#include <stdlib.h>
#include "sensor_utils.h"
#include "data_logger.h"

#define SAMPLE_INTERVAL_MS 500
#define DEVICE_ID 0x1A3F
#define SAMPLE_RATE 100

int main(void) {
    printf("Sensor Data Collection System v2.1\\n");
    printf("===================================\\n\\n");

    // Initialize the data logger
    DataLogger *logger = logger_create("/var/log/sensor_data.log", LOG_LEVEL_INFO);
    if (!logger) {
        fprintf(stderr, "Error: Failed to initialize data logger\\n");
        return EXIT_FAILURE;
    }

    // Initialize sensor hardware
    int status = sensor_init(DEVICE_ID, SAMPLE_RATE);
    if (status < 0) {
        fprintf(stderr, "Error: Sensor initialization failed (code %d)\\n", status);
        logger_write(logger, LOG_LEVEL_CRITICAL, "Sensor init failed");
        logger_destroy(logger);
        return EXIT_FAILURE;
    }

    logger_write(logger, LOG_LEVEL_INFO, "System initialized successfully");

    // Calibrate with known room temperature reference
    sensor_calibrate(22.5f);
    logger_write(logger, LOG_LEVEL_INFO, "Calibration complete (ref=22.5C)");

    // Read and log sensor data
    SensorReading reading;
    for (int i = 0; i < 10; i++) {
        if (sensor_read(&reading) == 0) {
            char msg[128];
            snprintf(msg, sizeof(msg),
                     "Sensor %04X: temp=%.2fC humidity=%.1f%% ts=%u",
                     reading.sensor_id, reading.temperature,
                     reading.humidity, reading.timestamp);
            logger_write(logger, LOG_LEVEL_INFO, msg);
            printf("Reading %d: %.2f C, %.1f%%\\n",
                   i + 1, reading.temperature, reading.humidity);
        } else {
            logger_write(logger, LOG_LEVEL_WARNING, "Failed to read sensor");
        }
    }

    // Cleanup
    sensor_shutdown();
    logger_flush(logger);
    logger_write(logger, LOG_LEVEL_INFO, "System shutdown complete");
    logger_destroy(logger);

    printf("\\nData collection complete. See log for details.\\n");
    return EXIT_SUCCESS;
}
""")

    # --- Makefile ---
    with open(f'{PROJECT_DIR}/Makefile', 'w') as f:
        f.write("""CC = gcc
CFLAGS = -Wall -Wextra -std=c17 -I./include
SRCDIR = src
OBJDIR = obj
TARGET = sensor_collector

SOURCES = $(wildcard $(SRCDIR)/*.c)
OBJECTS = $(SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJECTS)
\t$(CC) $(CFLAGS) -o $@ $^

$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
\t$(CC) $(CFLAGS) -c $< -o $@

$(OBJDIR):
\tmkdir -p $(OBJDIR)

clean:
\trm -rf $(OBJDIR) $(TARGET)
""")

    # --- README ---
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# Sensor Data Collection System

A lightweight C application for reading environmental sensor data
and logging it with configurable verbosity levels.

## Building

```bash
make
```

## Requirements

- GCC with C17 support
- Custom sensor hardware library (linked externally)

## Project Structure

```
vscode_lang_079/
├── include/
│   ├── sensor_utils.h    # Sensor hardware interface
│   └── data_logger.h     # Logging facility
├── src/
│   └── main.c            # Entry point
├── Makefile
└── README.md
```
""")

    # Explicitly do NOT create .vscode/c_cpp_properties.json — that's the agent's task
    print(f'Initial C project created at: {PROJECT_DIR}')
    print(f'  include/sensor_utils.h')
    print(f'  include/data_logger.h')
    print(f'  src/main.c')
    print(f'  Makefile')
    print(f'  README.md')
    print(f'  NO .vscode/c_cpp_properties.json — agent must create it')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
