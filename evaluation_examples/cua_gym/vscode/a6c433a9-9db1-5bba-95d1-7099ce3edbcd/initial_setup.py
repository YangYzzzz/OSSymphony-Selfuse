"""
Initial Setup: Configure C/C++ extension clang-tidy static analysis
Task ID: vscode_lang_092
Domain: vscode
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_092'
WORKSPACE = f'{WORKDIR}/workspace'
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


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
    # Create workspace directory
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create a C++ source file with some readability and performance issues
    # (These would trigger clang-tidy warnings once enabled)
    cpp_content = """\
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>

using namespace std;

// Function with readability issues: magic numbers, poor naming
int f(int x, int y) {
    int z = x * 42 + y * 17;
    if (z > 100) {
        return z - 3;
    } else {
        return z + 7;
    }
}

// Class with readability issues
class data_processor {
public:
    data_processor(string n, int c) : name(n), count(c) {}

    // Performance issue: passing string by value instead of const reference
    void process(string input) {
        for (int i = 0; i < input.size(); i++) {
            cout << input[i];
        }
        cout << endl;
    }

    // Performance issue: unnecessary copy in range-for
    void summarize(vector<string> items) {
        for (string item : items) {
            cout << item << " ";
        }
        cout << endl;
    }

    // Readability issue: complex boolean expression
    bool check(int a, int b, int c) {
        return (a > 0 && b > 0 && c > 0 && a + b > c && a + c > b && b + c > a) || (a == 0 && b == 0 && c == 0);
    }

    string get_name() { return name; }
    int get_count() { return count; }

private:
    string name;
    int count;
};

// Performance issue: inefficient container usage
void find_duplicates(vector<int> nums) {
    vector<int> seen;
    vector<int> duplicates;
    for (int i = 0; i < nums.size(); i++) {
        bool found = false;
        for (int j = 0; j < seen.size(); j++) {
            if (seen[j] == nums[i]) {
                found = true;
                break;
            }
        }
        if (found) {
            duplicates.push_back(nums[i]);
        } else {
            seen.push_back(nums[i]);
        }
    }
    for (int i = 0; i < duplicates.size(); i++) {
        cout << "Duplicate: " << duplicates[i] << endl;
    }
}

int main() {
    data_processor dp("TestProcessor", 5);

    string test_input = "Hello, World!";
    dp.process(test_input);

    vector<string> items = {"alpha", "beta", "gamma", "delta"};
    dp.summarize(items);

    cout << "Triangle check: " << dp.check(3, 4, 5) << endl;
    cout << "Result: " << f(10, 20) << endl;

    vector<int> numbers = {1, 2, 3, 4, 2, 5, 3, 6, 7, 8, 1};
    find_duplicates(numbers);

    return 0;
}
"""
    with open(os.path.join(WORKSPACE, 'main.cpp'), 'w') as fh:
        fh.write(cpp_content)

    # Create a simple CMakeLists.txt
    cmake_content = """\
cmake_minimum_required(VERSION 3.10)
project(StaticAnalysisDemo LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
add_executable(demo main.cpp)
"""
    with open(os.path.join(WORKSPACE, 'CMakeLists.txt'), 'w') as fh:
        fh.write(cmake_content)

    # Create a header file
    header_content = """\
#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <vector>

// Utility function declarations
std::string to_upper(std::string s);
double compute_average(std::vector<double> values);
bool is_palindrome(std::string s);

#endif // UTILS_H
"""
    with open(os.path.join(WORKSPACE, 'utils.h'), 'w') as fh:
        fh.write(header_content)

    # Ensure VSCode settings directory exists with clean settings (no clang-tidy config)
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as fh:
                import re
                content = fh.read()
                content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                settings = json.loads(content)
        except (json.JSONDecodeError, Exception):
            settings = {}

    # Remove any existing clang-tidy settings to ensure clean initial state
    keys_to_remove = [k for k in settings if 'clangTidy' in k or 'codeAnalysis' in k.lower()]
    for k in keys_to_remove:
        del settings[k]

    # Also ensure C_Cpp settings don't have codeAnalysis
    if 'C_Cpp.codeAnalysis.clangTidy.enabled' in settings:
        del settings['C_Cpp.codeAnalysis.clangTidy.enabled']
    if 'C_Cpp.codeAnalysis.clangTidy.checks.enabled' in settings:
        del settings['C_Cpp.codeAnalysis.clangTidy.checks.enabled']

    with open(SETTINGS_PATH, 'w') as fh:
        json.dump(settings, fh, indent=4)
    print(f'VSCode settings cleaned: {SETTINGS_PATH}')

    # Make sure there is NO .clang-tidy file in the workspace
    clang_tidy_path = os.path.join(WORKSPACE, '.clang-tidy')
    if os.path.exists(clang_tidy_path):
        os.remove(clang_tidy_path)

    print(f'Initial workspace created: {WORKSPACE}')

    # Launch VSCode with the workspace
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
