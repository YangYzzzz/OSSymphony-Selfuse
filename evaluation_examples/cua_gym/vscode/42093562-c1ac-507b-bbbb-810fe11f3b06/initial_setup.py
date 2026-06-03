"""
Initial Setup: Create VSCode workspace with C++ project for build task configuration
Task ID: vscode_lang_084
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_084'
PROJECT_DIR = f'{WORKDIR}/projects/cppapp'
VSCODE_DIR = f'{PROJECT_DIR}/.vscode'


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
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/build/debug', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/build/release', exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # Create a realistic main.cpp
    main_cpp = '''\
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <string>
#include <cmath>

struct SensorReading {
    std::string sensor_id;
    double temperature;
    double humidity;
    long timestamp;
};

class WeatherStation {
private:
    std::string station_name;
    std::vector<SensorReading> readings;

public:
    WeatherStation(const std::string& name) : station_name(name) {}

    void add_reading(const SensorReading& reading) {
        readings.push_back(reading);
    }

    double average_temperature() const {
        if (readings.empty()) return 0.0;
        double sum = std::accumulate(readings.begin(), readings.end(), 0.0,
            [](double acc, const SensorReading& r) { return acc + r.temperature; });
        return sum / readings.size();
    }

    double max_humidity() const {
        if (readings.empty()) return 0.0;
        auto it = std::max_element(readings.begin(), readings.end(),
            [](const SensorReading& a, const SensorReading& b) {
                return a.humidity < b.humidity;
            });
        return it->humidity;
    }

    void print_summary() const {
        std::cout << "=== Weather Station: " << station_name << " ===" << std::endl;
        std::cout << "Total readings: " << readings.size() << std::endl;
        std::cout << "Average temperature: " << average_temperature() << " C" << std::endl;
        std::cout << "Max humidity: " << max_humidity() << " %" << std::endl;

        #ifndef NDEBUG
        std::cout << "[DEBUG] Individual readings:" << std::endl;
        for (const auto& r : readings) {
            std::cout << "  Sensor " << r.sensor_id
                      << ": temp=" << r.temperature
                      << ", humidity=" << r.humidity << std::endl;
        }
        #endif
    }
};

int main() {
    WeatherStation station("Downtown Observatory");

    station.add_reading({"TH-001", 23.5, 65.2, 1711929600});
    station.add_reading({"TH-002", 24.1, 58.7, 1711933200});
    station.add_reading({"TH-001", 22.8, 71.3, 1711936800});
    station.add_reading({"TH-003", 25.0, 54.9, 1711940400});
    station.add_reading({"TH-002", 23.3, 62.1, 1711944000});

    station.print_summary();

    return 0;
}
'''
    with open(f'{PROJECT_DIR}/main.cpp', 'w') as f:
        f.write(main_cpp)

    # Create a basic settings.json (no tasks.json - that's the task)
    import json
    settings = {
        "C_Cpp.default.cppStandard": "c++17",
        "editor.tabSize": 4,
        "editor.formatOnSave": True,
        "files.associations": {
            "*.cpp": "cpp",
            "*.h": "cpp"
        }
    }
    with open(f'{VSCODE_DIR}/settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

    # Do NOT create tasks.json - that is what the agent must do
    print(f'Initial project created: {PROJECT_DIR}')
    print(f'main.cpp created: {PROJECT_DIR}/main.cpp')
    print(f'NO tasks.json exists (agent must create it)')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
