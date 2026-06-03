"""
Initial Setup: Set up a webdev project with JavaScript files, no ESLint.
Task ID: vscode_stu_060
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_060'
PROJECT_DIR = f'{WORKDIR}/webdev/project'

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
    # 1. Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # 2. Create realistic JavaScript files for a web development class project

    # index.html
    with open(os.path.join(PROJECT_DIR, 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Grade Tracker</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="app">
        <h1>Student Grade Tracker</h1>
        <div id="grade-form">
            <input type="text" id="student-name" placeholder="Student Name">
            <input type="number" id="grade-input" placeholder="Grade">
            <button onclick="addGrade()">Add Grade</button>
        </div>
        <div id="grade-list"></div>
        <div id="statistics"></div>
    </div>
    <script src="app.js"></script>
    <script src="utils.js"></script>
</body>
</html>
""")

    # app.js - main application logic with some intentional lint issues
    with open(os.path.join(PROJECT_DIR, 'app.js'), 'w') as f:
        f.write("""// Student Grade Tracker - Main Application
const students = [];

function addGrade() {
    var nameInput = document.getElementById('student-name');
    var gradeInput = document.getElementById('grade-input');

    var name = nameInput.value.trim();
    var grade = parseInt(gradeInput.value);

    if (name == '') {
        alert('Please enter a student name');
        return;
    }

    if (isNaN(grade) || grade < 0 || grade > 100) {
        alert('Please enter a valid grade between 0 and 100');
        return;
    }

    students.push({ name: name, grade: grade });
    renderGrades();
    updateStatistics();

    nameInput.value = '';
    gradeInput.value = '';
}

function renderGrades() {
    var list = document.getElementById('grade-list');
    list.innerHTML = '<h2>Grades</h2>';

    for (var i = 0; i < students.length; i++) {
        var item = document.createElement('div');
        item.className = 'grade-item';
        item.innerHTML = '<span>' + students[i].name + '</span><span>' + students[i].grade + '</span>';
        list.appendChild(item);
    }
}

function updateStatistics() {
    if (students.length == 0) return;

    var total = 0;
    var highest = students[0].grade;
    var lowest = students[0].grade;

    for (var i = 0; i < students.length; i++) {
        total += students[i].grade;
        if (students[i].grade > highest) highest = students[i].grade;
        if (students[i].grade < lowest) lowest = students[i].grade;
    }

    var average = total / students.length;
    var statsDiv = document.getElementById('statistics');
    statsDiv.innerHTML = '<h2>Statistics</h2>' +
        '<p>Average: ' + average.toFixed(2) + '</p>' +
        '<p>Highest: ' + highest + '</p>' +
        '<p>Lowest: ' + lowest + '</p>' +
        '<p>Total Students: ' + students.length + '</p>';
}

function deleteGrade(index) {
    students.splice(index, 1);
    renderGrades();
    updateStatistics();
}
""")

    # utils.js - utility functions with some lint issues
    with open(os.path.join(PROJECT_DIR, 'utils.js'), 'w') as f:
        f.write("""// Utility functions for Student Grade Tracker

function formatDate(date) {
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var year = date.getFullYear();
    return month + '/' + day + '/' + year;
}

function validateEmail(email) {
    var regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    return regex.test(email);
}

function calculateLetterGrade(score) {
    if (score >= 90) return 'A';
    if (score >= 80) return 'B';
    if (score >= 70) return 'C';
    if (score >= 60) return 'D';
    return 'F';
}

function sortStudents(studentArray, sortBy) {
    var sorted = studentArray.slice();
    if (sortBy == 'name') {
        sorted.sort(function(a, b) {
            return a.name.localeCompare(b.name);
        });
    } else if (sortBy == 'grade') {
        sorted.sort(function(a, b) {
            return b.grade - a.grade;
        });
    }
    return sorted;
}

function exportToCSV(data) {
    var csv = 'Name,Grade,Letter Grade\\n';
    for (var i = 0; i < data.length; i++) {
        csv += data[i].name + ',' + data[i].grade + ',' + calculateLetterGrade(data[i].grade) + '\\n';
    }
    return csv;
}
""")

    # styles.css
    with open(os.path.join(PROJECT_DIR, 'styles.css'), 'w') as f:
        f.write("""/* Student Grade Tracker Styles */

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
}

#app {
    background: white;
    border-radius: 8px;
    padding: 30px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
    color: #333;
    text-align: center;
}

#grade-form {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

input[type="text"],
input[type="number"] {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    flex: 1;
}

button {
    padding: 8px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}

.grade-item {
    display: flex;
    justify-content: space-between;
    padding: 8px;
    border-bottom: 1px solid #eee;
}
""")

    # package.json
    with open(os.path.join(PROJECT_DIR, 'package.json'), 'w') as f:
        json.dump({
            "name": "student-grade-tracker",
            "version": "1.0.0",
            "description": "A simple student grade tracking application for web development class",
            "main": "app.js",
            "scripts": {
                "start": "open index.html"
            },
            "author": "Web Development Student",
            "license": "MIT"
        }, f, indent=2)

    # 3. Ensure NO .eslintrc.json exists (negative constraint)
    eslintrc_path = os.path.join(PROJECT_DIR, '.eslintrc.json')
    if os.path.exists(eslintrc_path):
        os.remove(eslintrc_path)

    # 4. Ensure ESLint extension is NOT installed
    try:
        subprocess.run(['code', '--uninstall-extension', 'dbaeumer.vscode-eslint'],
                       capture_output=True, timeout=30)
    except Exception:
        pass

    print(f'Initial project created at: {PROJECT_DIR}')

    # 5. Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
