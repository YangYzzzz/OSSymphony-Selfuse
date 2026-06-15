"""
Initial Setup: Open VSCode with a file that has non-UTF-8 encoding
Task ID: vscode_stu_044
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_044'
OUTPUT = f'{WORKDIR}/{TASK_ID}.py'

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
    # Create a realistic Python file with characters that differ between
    # Latin-1 and UTF-8 encodings. We write it in Latin-1 (ISO-8859-1)
    # so VSCode will detect it as a non-UTF-8 file.
    content = '''\
# -*- coding: latin-1 -*-
"""
Student Grade Report Generator
Universit\xe9 de Montr\xe9al - D\xe9partement d\'Informatique
Course: INF2010 - Structures de donn\xe9es et algorithmes
Semester: Automne 2025

Author: \xc9milie Th\xe9r\xe8se Dub\xe9
Description: Generates semester grade reports for students
             enrolled in computer science courses.
"""

import csv
from datetime import datetime


class StudentRecord:
    """Repr\xe9sentation d\'un \xe9tudiant et ses r\xe9sultats."""

    def __init__(self, student_id, name, program):
        self.student_id = student_id
        self.name = name
        self.program = program
        self.grades = {}
        self.attendance = 0.0

    def add_grade(self, assignment, score, max_score):
        """Ajouter une note pour un devoir ou examen."""
        self.grades[assignment] = {
            "score": score,
            "max_score": max_score,
            "percentage": round((score / max_score) * 100, 2)
        }

    def calculate_final_grade(self):
        """Calculer la note finale pond\xe9r\xe9e."""
        if not self.grades:
            return 0.0
        weights = {
            "Devoir 1": 0.10,
            "Devoir 2": 0.10,
            "Devoir 3": 0.10,
            "Examen Intra": 0.30,
            "Examen Final": 0.40,
        }
        total = 0.0
        for assignment, data in self.grades.items():
            weight = weights.get(assignment, 0.0)
            total += data["percentage"] * weight
        return round(total, 2)

    def get_letter_grade(self):
        """Convertir le pourcentage en note litt\xe9rale."""
        final = self.calculate_final_grade()
        if final >= 90:
            return "A+"
        elif final >= 85:
            return "A"
        elif final >= 80:
            return "A-"
        elif final >= 77:
            return "B+"
        elif final >= 73:
            return "B"
        elif final >= 70:
            return "B-"
        elif final >= 65:
            return "C+"
        elif final >= 60:
            return "C"
        elif final >= 50:
            return "D"
        else:
            return "\xc9chec"  # Fail


def generate_report(students):
    """G\xe9n\xe9rer le rapport de notes du semestre."""
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("RAPPORT DE NOTES - AUTOMNE 2025")
    report_lines.append("Universit\xe9 de Montr\xe9al")
    report_lines.append("INF2010 - Structures de donn\xe9es et algorithmes")
    report_lines.append("=" * 60)
    report_lines.append("")

    for student in students:
        final = student.calculate_final_grade()
        letter = student.get_letter_grade()
        report_lines.append(f"  {student.name} ({student.student_id})")
        report_lines.append(f"    Programme: {student.program}")
        report_lines.append(f"    Note finale: {final}% ({letter})")
        report_lines.append(f"    Pr\xe9sence: {student.attendance}%")
        report_lines.append("")

    report_lines.append("-" * 60)
    avg = sum(s.calculate_final_grade() for s in students) / len(students)
    report_lines.append(f"Moyenne de la classe: {avg:.2f}%")
    report_lines.append(f"Nombre d\'\xe9tudiants: {len(students)}")
    report_lines.append(f"Date du rapport: {datetime.now().strftime(\'%Y-%m-%d\')}")
    report_lines.append("=" * 60)

    return "\\n".join(report_lines)


def main():
    """Point d\'entr\xe9e principal du programme."""
    students = [
        StudentRecord("20231001", "Fr\xe9d\xe9ric Gagn\xe9", "B.Sc. Informatique"),
        StudentRecord("20231002", "Am\xe9lie Lafreni\xe8re", "B.Sc. Math-Info"),
        StudentRecord("20231003", "S\xe9bastien Pr\xe9vost", "B.Sc. Informatique"),
        StudentRecord("20231004", "Val\xe9rie C\xf4t\xe9", "B.Sc. G\xe9nie logiciel"),
        StudentRecord("20231005", "Ren\xe9 Beaupr\xe9", "B.Sc. Informatique"),
    ]

    # Ajouter les notes
    grades_data = [
        ("Devoir 1",     [85, 92, 78, 88, 70]),
        ("Devoir 2",     [90, 88, 65, 95, 72]),
        ("Devoir 3",     [82, 95, 70, 91, 68]),
        ("Examen Intra", [75, 89, 60, 82, 55]),
        ("Examen Final", [80, 93, 58, 87, 62]),
    ]

    for assignment, scores in grades_data:
        for student, score in zip(students, scores):
            student.add_grade(assignment, score, 100)

    # D\xe9finir la pr\xe9sence
    attendance = [92.5, 98.0, 75.0, 95.5, 80.0]
    for student, att in zip(students, attendance):
        student.attendance = att

    report = generate_report(students)
    print(report)


if __name__ == "__main__":
    main()
'''

    # Write the file in Latin-1 encoding so VSCode detects non-UTF-8
    with open(OUTPUT, 'w', encoding='latin-1') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')
    print(f'File encoding: Latin-1 (ISO-8859-1)')

    # Open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
