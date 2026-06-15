"""
Initial Setup: Configure C/C++ IntelliSense with compile_commands.json
Task ID: vscode_lang_088
Domain: vs_code

Creates a CMake C++ project workspace. IntelliSense uses default config.
CMakeLists.txt does NOT have CMAKE_EXPORT_COMPILE_COMMANDS.
VSCode settings do NOT have C_Cpp.default.compileCommands.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_088'
WORKSPACE = f'{WORKDIR}/workspace'
BUILD_DIR = f'{WORKSPACE}/build'
VSCODE_DIR = f'{WORKSPACE}/.vscode'
SETTINGS_PATH = f'{VSCODE_DIR}/settings.json'


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
    os.makedirs(WORKSPACE, exist_ok=True)
    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(f'{WORKSPACE}/include', exist_ok=True)
    os.makedirs(f'{WORKSPACE}/src', exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # --- CMakeLists.txt (NO CMAKE_EXPORT_COMPILE_COMMANDS) ---
    cmake_content = """\
cmake_minimum_required(VERSION 3.16)
project(SensorDataProcessor VERSION 1.2.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# External dependencies
find_package(Threads REQUIRED)

# Include directories
include_directories(${PROJECT_SOURCE_DIR}/include)

# Source files
set(SOURCES
    src/main.cpp
    src/sensor_reader.cpp
    src/data_filter.cpp
    src/signal_processor.cpp
)

# Build executable
add_executable(sensor_processor ${SOURCES})
target_link_libraries(sensor_processor Threads::Threads)

# Install rules
install(TARGETS sensor_processor DESTINATION bin)
"""
    with open(f'{WORKSPACE}/CMakeLists.txt', 'w') as f:
        f.write(cmake_content)

    # --- Header files ---
    # include/sensor_reader.h
    with open(f'{WORKSPACE}/include/sensor_reader.h', 'w') as f:
        f.write("""\
#pragma once

#include <string>
#include <vector>
#include <cstdint>

namespace sensor {

struct SensorReading {
    uint64_t timestamp_ms;
    double temperature;
    double humidity;
    double pressure;
    std::string sensor_id;
};

class SensorReader {
public:
    explicit SensorReader(const std::string& device_path);
    ~SensorReader();

    bool connect();
    void disconnect();
    bool is_connected() const;

    SensorReading read_single();
    std::vector<SensorReading> read_batch(size_t count);

    void set_sampling_rate(uint32_t hz);
    uint32_t get_sampling_rate() const;

private:
    std::string device_path_;
    bool connected_ = false;
    uint32_t sampling_rate_ = 100;
    int device_fd_ = -1;
};

} // namespace sensor
""")

    # include/data_filter.h
    with open(f'{WORKSPACE}/include/data_filter.h', 'w') as f:
        f.write("""\
#pragma once

#include "sensor_reader.h"
#include <deque>
#include <functional>

namespace sensor {

enum class FilterType {
    MovingAverage,
    Median,
    ExponentialSmoothing,
    Kalman
};

class DataFilter {
public:
    explicit DataFilter(FilterType type, size_t window_size = 10);

    SensorReading apply(const SensorReading& reading);
    std::vector<SensorReading> apply_batch(const std::vector<SensorReading>& readings);

    void reset();
    void set_alpha(double alpha);  // For exponential smoothing

private:
    FilterType type_;
    size_t window_size_;
    double alpha_ = 0.3;
    std::deque<SensorReading> buffer_;

    double moving_average(const std::deque<double>& values);
    double median_value(std::deque<double> values);
    double exponential_smooth(double current, double previous);
};

} // namespace sensor
""")

    # include/signal_processor.h
    with open(f'{WORKSPACE}/include/signal_processor.h', 'w') as f:
        f.write("""\
#pragma once

#include "data_filter.h"
#include <map>
#include <memory>
#include <thread>
#include <atomic>
#include <mutex>

namespace sensor {

struct ProcessingConfig {
    FilterType filter_type = FilterType::MovingAverage;
    size_t filter_window = 10;
    double anomaly_threshold = 3.0;   // standard deviations
    uint32_t sampling_rate_hz = 100;
    size_t batch_size = 50;
};

struct ProcessingStats {
    uint64_t total_readings = 0;
    uint64_t anomalies_detected = 0;
    double mean_temperature = 0.0;
    double mean_humidity = 0.0;
    double mean_pressure = 0.0;
};

class SignalProcessor {
public:
    SignalProcessor(const ProcessingConfig& config,
                    std::shared_ptr<SensorReader> reader);
    ~SignalProcessor();

    void start();
    void stop();
    bool is_running() const;

    ProcessingStats get_stats() const;
    std::vector<SensorReading> get_recent_anomalies(size_t count = 10) const;

    void register_anomaly_callback(std::function<void(const SensorReading&)> cb);

private:
    void processing_loop();
    bool detect_anomaly(const SensorReading& reading);
    void update_stats(const SensorReading& reading);

    ProcessingConfig config_;
    std::shared_ptr<SensorReader> reader_;
    std::unique_ptr<DataFilter> filter_;

    std::atomic<bool> running_{false};
    std::thread worker_thread_;
    mutable std::mutex stats_mutex_;
    ProcessingStats stats_;
    std::vector<SensorReading> anomaly_log_;
    std::function<void(const SensorReading&)> anomaly_callback_;
};

} // namespace sensor
""")

    # --- Source files ---
    # src/main.cpp
    with open(f'{WORKSPACE}/src/main.cpp', 'w') as f:
        f.write("""\
#include "signal_processor.h"
#include <iostream>
#include <chrono>
#include <csignal>

static std::atomic<bool> g_shutdown{false};

void signal_handler(int signum) {
    std::cout << "\\nReceived signal " << signum << ", shutting down...\\n";
    g_shutdown.store(true);
}

int main(int argc, char* argv[]) {
    std::signal(SIGINT, signal_handler);
    std::signal(SIGTERM, signal_handler);

    std::string device = "/dev/sensor0";
    if (argc > 1) {
        device = argv[1];
    }

    auto reader = std::make_shared<sensor::SensorReader>(device);
    if (!reader->connect()) {
        std::cerr << "Failed to connect to sensor at " << device << "\\n";
        return 1;
    }

    sensor::ProcessingConfig config;
    config.filter_type = sensor::FilterType::ExponentialSmoothing;
    config.filter_window = 20;
    config.anomaly_threshold = 2.5;
    config.sampling_rate_hz = 200;
    config.batch_size = 100;

    sensor::SignalProcessor processor(config, reader);

    processor.register_anomaly_callback([](const sensor::SensorReading& r) {
        std::cout << "[ANOMALY] Sensor " << r.sensor_id
                  << " T=" << r.temperature
                  << " H=" << r.humidity
                  << " P=" << r.pressure << "\\n";
    });

    processor.start();
    std::cout << "Signal processor started. Press Ctrl+C to stop.\\n";

    while (!g_shutdown.load()) {
        auto stats = processor.get_stats();
        std::cout << "\\rReadings: " << stats.total_readings
                  << " | Anomalies: " << stats.anomalies_detected
                  << " | Avg Temp: " << stats.mean_temperature
                  << std::flush;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    processor.stop();
    reader->disconnect();

    auto final_stats = processor.get_stats();
    std::cout << "\\n\\nFinal Statistics:\\n"
              << "  Total readings: " << final_stats.total_readings << "\\n"
              << "  Anomalies detected: " << final_stats.anomalies_detected << "\\n"
              << "  Mean temperature: " << final_stats.mean_temperature << "\\n"
              << "  Mean humidity: " << final_stats.mean_humidity << "\\n"
              << "  Mean pressure: " << final_stats.mean_pressure << "\\n";

    return 0;
}
""")

    # src/sensor_reader.cpp
    with open(f'{WORKSPACE}/src/sensor_reader.cpp', 'w') as f:
        f.write("""\
#include "sensor_reader.h"
#include <iostream>
#include <random>
#include <chrono>

namespace sensor {

SensorReader::SensorReader(const std::string& device_path)
    : device_path_(device_path) {}

SensorReader::~SensorReader() {
    if (connected_) {
        disconnect();
    }
}

bool SensorReader::connect() {
    // Simulated connection for development
    std::cout << "Connecting to sensor at " << device_path_ << "...\\n";
    connected_ = true;
    return true;
}

void SensorReader::disconnect() {
    connected_ = false;
    std::cout << "Disconnected from sensor.\\n";
}

bool SensorReader::is_connected() const {
    return connected_;
}

SensorReading SensorReader::read_single() {
    static std::mt19937 gen(std::random_device{}());
    static std::normal_distribution<> temp_dist(22.5, 1.5);
    static std::normal_distribution<> humid_dist(45.0, 5.0);
    static std::normal_distribution<> press_dist(1013.25, 2.0);

    auto now = std::chrono::system_clock::now();
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
        now.time_since_epoch()).count();

    return SensorReading{
        static_cast<uint64_t>(ms),
        temp_dist(gen),
        humid_dist(gen),
        press_dist(gen),
        "BME280-01"
    };
}

std::vector<SensorReading> SensorReader::read_batch(size_t count) {
    std::vector<SensorReading> readings;
    readings.reserve(count);
    for (size_t i = 0; i < count; ++i) {
        readings.push_back(read_single());
    }
    return readings;
}

void SensorReader::set_sampling_rate(uint32_t hz) {
    sampling_rate_ = hz;
}

uint32_t SensorReader::get_sampling_rate() const {
    return sampling_rate_;
}

} // namespace sensor
""")

    # src/data_filter.cpp
    with open(f'{WORKSPACE}/src/data_filter.cpp', 'w') as f:
        f.write("""\
#include "data_filter.h"
#include <algorithm>
#include <numeric>

namespace sensor {

DataFilter::DataFilter(FilterType type, size_t window_size)
    : type_(type), window_size_(window_size) {}

SensorReading DataFilter::apply(const SensorReading& reading) {
    buffer_.push_back(reading);
    if (buffer_.size() > window_size_) {
        buffer_.pop_front();
    }

    SensorReading filtered = reading;

    std::deque<double> temps, humids, pressures;
    for (const auto& r : buffer_) {
        temps.push_back(r.temperature);
        humids.push_back(r.humidity);
        pressures.push_back(r.pressure);
    }

    switch (type_) {
        case FilterType::MovingAverage:
            filtered.temperature = moving_average(temps);
            filtered.humidity = moving_average(humids);
            filtered.pressure = moving_average(pressures);
            break;
        case FilterType::Median:
            filtered.temperature = median_value(temps);
            filtered.humidity = median_value(humids);
            filtered.pressure = median_value(pressures);
            break;
        case FilterType::ExponentialSmoothing:
            if (buffer_.size() >= 2) {
                auto prev = buffer_[buffer_.size() - 2];
                filtered.temperature = exponential_smooth(reading.temperature, prev.temperature);
                filtered.humidity = exponential_smooth(reading.humidity, prev.humidity);
                filtered.pressure = exponential_smooth(reading.pressure, prev.pressure);
            }
            break;
        default:
            break;
    }

    return filtered;
}

std::vector<SensorReading> DataFilter::apply_batch(const std::vector<SensorReading>& readings) {
    std::vector<SensorReading> result;
    result.reserve(readings.size());
    for (const auto& r : readings) {
        result.push_back(apply(r));
    }
    return result;
}

void DataFilter::reset() {
    buffer_.clear();
}

void DataFilter::set_alpha(double alpha) {
    alpha_ = alpha;
}

double DataFilter::moving_average(const std::deque<double>& values) {
    return std::accumulate(values.begin(), values.end(), 0.0) / values.size();
}

double DataFilter::median_value(std::deque<double> values) {
    std::sort(values.begin(), values.end());
    size_t n = values.size();
    if (n % 2 == 0) {
        return (values[n / 2 - 1] + values[n / 2]) / 2.0;
    }
    return values[n / 2];
}

double DataFilter::exponential_smooth(double current, double previous) {
    return alpha_ * current + (1.0 - alpha_) * previous;
}

} // namespace sensor
""")

    # src/signal_processor.cpp
    with open(f'{WORKSPACE}/src/signal_processor.cpp', 'w') as f:
        f.write("""\
#include "signal_processor.h"
#include <cmath>
#include <iostream>

namespace sensor {

SignalProcessor::SignalProcessor(const ProcessingConfig& config,
                                 std::shared_ptr<SensorReader> reader)
    : config_(config), reader_(reader),
      filter_(std::make_unique<DataFilter>(config.filter_type, config.filter_window)) {
    reader_->set_sampling_rate(config.sampling_rate_hz);
}

SignalProcessor::~SignalProcessor() {
    if (running_.load()) {
        stop();
    }
}

void SignalProcessor::start() {
    running_.store(true);
    worker_thread_ = std::thread(&SignalProcessor::processing_loop, this);
}

void SignalProcessor::stop() {
    running_.store(false);
    if (worker_thread_.joinable()) {
        worker_thread_.join();
    }
}

bool SignalProcessor::is_running() const {
    return running_.load();
}

ProcessingStats SignalProcessor::get_stats() const {
    std::lock_guard<std::mutex> lock(stats_mutex_);
    return stats_;
}

std::vector<SensorReading> SignalProcessor::get_recent_anomalies(size_t count) const {
    std::lock_guard<std::mutex> lock(stats_mutex_);
    if (anomaly_log_.size() <= count) {
        return anomaly_log_;
    }
    return std::vector<SensorReading>(
        anomaly_log_.end() - count, anomaly_log_.end());
}

void SignalProcessor::register_anomaly_callback(
    std::function<void(const SensorReading&)> cb) {
    anomaly_callback_ = std::move(cb);
}

void SignalProcessor::processing_loop() {
    while (running_.load()) {
        auto batch = reader_->read_batch(config_.batch_size);
        auto filtered = filter_->apply_batch(batch);

        for (const auto& reading : filtered) {
            update_stats(reading);

            if (detect_anomaly(reading)) {
                std::lock_guard<std::mutex> lock(stats_mutex_);
                stats_.anomalies_detected++;
                anomaly_log_.push_back(reading);
                if (anomaly_callback_) {
                    anomaly_callback_(reading);
                }
            }
        }
    }
}

bool SignalProcessor::detect_anomaly(const SensorReading& reading) {
    std::lock_guard<std::mutex> lock(stats_mutex_);
    if (stats_.total_readings < 10) return false;

    double temp_dev = std::abs(reading.temperature - stats_.mean_temperature);
    return temp_dev > config_.anomaly_threshold * 1.5;
}

void SignalProcessor::update_stats(const SensorReading& reading) {
    std::lock_guard<std::mutex> lock(stats_mutex_);
    uint64_t n = ++stats_.total_readings;
    double inv_n = 1.0 / n;
    stats_.mean_temperature += (reading.temperature - stats_.mean_temperature) * inv_n;
    stats_.mean_humidity += (reading.humidity - stats_.mean_humidity) * inv_n;
    stats_.mean_pressure += (reading.pressure - stats_.mean_pressure) * inv_n;
}

} // namespace sensor
""")

    # --- Create a placeholder compile_commands.json in build/ ---
    # This simulates what CMake would generate, but is incomplete
    # (missing some include paths to match the "misses some include paths" initial state)
    compile_commands = [
        {
            "directory": f"{WORKSPACE}/build",
            "command": f"/usr/bin/g++ -std=c++17 -o CMakeFiles/sensor_processor.dir/src/main.cpp.o -c {WORKSPACE}/src/main.cpp",
            "file": f"{WORKSPACE}/src/main.cpp"
        }
    ]
    with open(f'{BUILD_DIR}/compile_commands.json', 'w') as f:
        json.dump(compile_commands, f, indent=2)

    # --- VSCode workspace settings (NO C_Cpp.default.compileCommands) ---
    vscode_settings = {
        "editor.fontSize": 14,
        "editor.tabSize": 4,
        "editor.formatOnSave": True,
        "C_Cpp.intelliSenseEngine": "default",
        "cmake.buildDirectory": "${workspaceFolder}/build",
        "files.associations": {
            "*.h": "cpp"
        }
    }
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(vscode_settings, f, indent=4)

    print(f'Initial workspace created: {WORKSPACE}')
    print(f'  CMakeLists.txt: NO CMAKE_EXPORT_COMPILE_COMMANDS')
    print(f'  settings.json: NO C_Cpp.default.compileCommands')

    # GUI-ready startup: open VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
