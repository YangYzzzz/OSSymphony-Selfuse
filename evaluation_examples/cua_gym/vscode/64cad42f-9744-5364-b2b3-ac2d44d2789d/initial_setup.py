"""
Initial Setup: Create a C++ project structure for VSCode build task creation
Task ID: vscode_lang_087
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_087'
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
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/include', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/build', exist_ok=True)

    # --- include/utils.h ---
    with open(f'{PROJECT_DIR}/include/utils.h', 'w') as f:
        f.write("""#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <vector>

namespace utils {

std::string trim(const std::string& str);
std::vector<std::string> split(const std::string& str, char delimiter);
int clamp(int value, int min_val, int max_val);

}  // namespace utils

#endif  // UTILS_H
""")

    # --- include/parser.h ---
    with open(f'{PROJECT_DIR}/include/parser.h', 'w') as f:
        f.write("""#ifndef PARSER_H
#define PARSER_H

#include <string>
#include <map>
#include <vector>

class ConfigParser {
public:
    ConfigParser();
    bool loadFromFile(const std::string& filepath);
    std::string getValue(const std::string& section, const std::string& key) const;
    std::vector<std::string> getSections() const;

private:
    std::map<std::string, std::map<std::string, std::string>> sections_;
    std::string currentSection_;
    bool parseLine(const std::string& line);
};

#endif  // PARSER_H
""")

    # --- src/main.cpp ---
    with open(f'{PROJECT_DIR}/src/main.cpp', 'w') as f:
        f.write("""#include <iostream>
#include <string>
#include "utils.h"
#include "parser.h"

int main(int argc, char* argv[]) {
    std::cout << "Configuration File Processor v1.2" << std::endl;
    std::cout << "=================================" << std::endl;

    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <config_file>" << std::endl;
        return 1;
    }

    std::string configPath = argv[1];
    std::string trimmedPath = utils::trim(configPath);

    ConfigParser parser;
    if (!parser.loadFromFile(trimmedPath)) {
        std::cerr << "Error: Could not load config file: " << trimmedPath << std::endl;
        return 1;
    }

    auto sections = parser.getSections();
    std::cout << "Found " << sections.size() << " sections:" << std::endl;
    for (const auto& section : sections) {
        std::cout << "  [" << section << "]" << std::endl;
    }

    std::string dbHost = parser.getValue("database", "host");
    std::string dbPort = parser.getValue("database", "port");
    if (!dbHost.empty()) {
        int port = std::stoi(dbPort);
        port = utils::clamp(port, 1024, 65535);
        std::cout << "Database: " << dbHost << ":" << port << std::endl;
    }

    return 0;
}
""")

    # --- src/utils.cpp ---
    with open(f'{PROJECT_DIR}/src/utils.cpp', 'w') as f:
        f.write("""#include "utils.h"
#include <algorithm>
#include <sstream>

namespace utils {

std::string trim(const std::string& str) {
    size_t first = str.find_first_not_of(" \\t\\n\\r");
    if (first == std::string::npos) return "";
    size_t last = str.find_last_not_of(" \\t\\n\\r");
    return str.substr(first, last - first + 1);
}

std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    std::istringstream stream(str);
    std::string token;
    while (std::getline(stream, token, delimiter)) {
        std::string trimmed = trim(token);
        if (!trimmed.empty()) {
            tokens.push_back(trimmed);
        }
    }
    return tokens;
}

int clamp(int value, int min_val, int max_val) {
    if (value < min_val) return min_val;
    if (value > max_val) return max_val;
    return value;
}

}  // namespace utils
""")

    # --- src/parser.cpp ---
    with open(f'{PROJECT_DIR}/src/parser.cpp', 'w') as f:
        f.write("""#include "parser.h"
#include "utils.h"
#include <fstream>
#include <iostream>

ConfigParser::ConfigParser() : currentSection_("default") {}

bool ConfigParser::loadFromFile(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cerr << "Cannot open file: " << filepath << std::endl;
        return false;
    }

    std::string line;
    int lineNum = 0;
    while (std::getline(file, line)) {
        lineNum++;
        line = utils::trim(line);
        if (line.empty() || line[0] == '#' || line[0] == ';') {
            continue;
        }
        if (!parseLine(line)) {
            std::cerr << "Warning: Could not parse line " << lineNum << ": " << line << std::endl;
        }
    }
    return true;
}

bool ConfigParser::parseLine(const std::string& line) {
    if (line.front() == '[' && line.back() == ']') {
        currentSection_ = line.substr(1, line.size() - 2);
        currentSection_ = utils::trim(currentSection_);
        return true;
    }

    size_t eqPos = line.find('=');
    if (eqPos == std::string::npos) return false;

    std::string key = utils::trim(line.substr(0, eqPos));
    std::string value = utils::trim(line.substr(eqPos + 1));
    sections_[currentSection_][key] = value;
    return true;
}

std::string ConfigParser::getValue(const std::string& section, const std::string& key) const {
    auto secIt = sections_.find(section);
    if (secIt == sections_.end()) return "";
    auto keyIt = secIt->second.find(key);
    if (keyIt == secIt->second.end()) return "";
    return keyIt->second;
}

std::vector<std::string> ConfigParser::getSections() const {
    std::vector<std::string> result;
    for (const auto& pair : sections_) {
        result.push_back(pair.first);
    }
    return result;
}
""")

    # --- NO .vscode/tasks.json --- (task requires creating it)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'  src/main.cpp, src/utils.cpp, src/parser.cpp')
    print(f'  include/utils.h, include/parser.h')
    print(f'  build/ (empty)')

    # GUI-ready: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
