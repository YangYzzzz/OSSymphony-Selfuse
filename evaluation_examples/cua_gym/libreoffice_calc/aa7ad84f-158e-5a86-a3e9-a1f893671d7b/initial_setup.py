"""
Initial Setup: Grade Analyzer - Multi-app code/script task
Task ID: osworld_multi_apps_code_script_output_005
Domain: libreoffice_calc (multi-app: code/script + spreadsheet)

Creates:
  - /home/user/data/grades.csv       (30-row grade data)
  - /home/user/scripts/grade_analyzer.py  (stub script with TODOs)
  - /home/user/data/grades_summary.ods   (spreadsheet with headers, empty C1)

MUST NOT exist:
  - /home/user/data/grade_report.txt  (created by agent after running script)
  - C1 in grades_summary.ods must be empty (agent fills it)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_script_output_005'
DATA_DIR = f'{WORKDIR}/data'
SCRIPTS_DIR = f'{WORKDIR}/scripts'


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


def create_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    print(f'Directories created: {DATA_DIR}, {SCRIPTS_DIR}')


def create_grades_csv():
    csv_path = f'{DATA_DIR}/grades.csv'
    rows = [
        ("student", "subject", "score"),
        ("Alice Chen", "Math", 88),
        ("Alice Chen", "Science", 92),
        ("Alice Chen", "English", 85),
        ("Bob Martinez", "Math", 76),
        ("Bob Martinez", "Science", 81),
        ("Bob Martinez", "History", 73),
        ("Carol Johnson", "Math", 95),
        ("Carol Johnson", "English", 90),
        ("Carol Johnson", "History", 88),
        ("David Kim", "Science", 62),
        ("David Kim", "English", 58),
        ("David Kim", "PE", 75),
        ("Emma Davis", "Math", 79),
        ("Emma Davis", "Science", 83),
        ("Emma Davis", "PE", 91),
        ("Frank Wilson", "Math", 55),
        ("Frank Wilson", "History", 48),
        ("Frank Wilson", "PE", 67),
        ("Grace Lee", "Science", 97),
        ("Grace Lee", "English", 94),
        ("Grace Lee", "History", 92),
        ("Henry Brown", "Math", 71),
        ("Henry Brown", "English", 68),
        ("Henry Brown", "PE", 82),
        ("Iris Taylor", "Math", 84),
        ("Iris Taylor", "Science", 78),
        ("Iris Taylor", "History", 80),
        ("Jack Anderson", "English", 89),
        ("Jack Anderson", "History", 65),
        ("Jack Anderson", "PE", 77),
    ]
    import csv
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f'grades.csv created: {csv_path} ({len(rows)-1} data rows)')


def create_grade_analyzer_stub():
    script_path = f'{SCRIPTS_DIR}/grade_analyzer.py'
    script_content = '''"""
Grade Analyzer - reads grades.csv and produces a summary report.
"""
import csv
from collections import defaultdict

DATA_FILE = '/home/user/data/grades.csv'
REPORT_FILE = '/home/user/data/grade_report.txt'


def load_data(filepath):
    """Load CSV data into a list of dicts."""
    data = []
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'student': row['student'],
                'subject': row['subject'],
                'score': float(row['score'])
            })
    return data


def get_top_students(data, n):
    """Return the top N students by average score.
    Returns a list of (student_name, average_score) tuples, sorted descending.

    TODO: Implement this function.
    """
    pass


def subject_average(data):
    """Return a dict mapping subject -> average score across all students.

    TODO: Implement this function.
    """
    pass


def failing_students(data, passing_score):
    """Return a list of student names whose average score is below passing_score.

    TODO: Implement this function.
    """
    pass


def main():
    data = load_data(DATA_FILE)

    # Compute class average
    all_scores = [row['score'] for row in data]
    class_avg = round(sum(all_scores) / len(all_scores), 2)

    # Get top 3 students
    top3 = get_top_students(data, 3)

    # Subject averages
    subj_avgs = subject_average(data)

    # Failing students (below 60)
    failing = failing_students(data, 60)

    # Build report lines
    lines = []
    lines.append("=== Grade Report ===")
    lines.append(f"Class Average: {class_avg}")
    lines.append("")
    lines.append("Top 3 Students:")
    for name, avg in top3:
        lines.append(f"  {name}: {round(avg, 2)}")
    lines.append("")
    lines.append("Subject Averages:")
    for subj in sorted(subj_avgs.keys()):
        lines.append(f"  {subj}: {round(subj_avgs[subj], 2)}")
    lines.append("")
    lines.append("Failing Students (avg < 60):")
    if failing:
        for name in failing:
            lines.append(f"  {name}")
    else:
        lines.append("  None")

    report = "\\n".join(lines)
    print(report)

    with open(REPORT_FILE, 'w') as f:
        f.write(report + "\\n")
    print(f"\\nReport saved to {REPORT_FILE}")


if __name__ == '__main__':
    main()
'''
    with open(script_path, 'w') as f:
        f.write(script_content)
    print(f'grade_analyzer.py stub created: {script_path}')


def create_grades_summary_ods():
    """Create grades_summary.ods with headers but empty C1."""
    ods_path = f'{DATA_DIR}/grades_summary.ods'

    # Use subprocess to create ODS via Python with odfpy
    python_code = f'''
import sys
try:
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.table import Table, TableRow, TableCell
    from odf.text import P
    from odf.style import Style, TextProperties, TableCellProperties
    doc = OpenDocumentSpreadsheet()
    sheet = Table(name="Summary")
    doc.spreadsheet.addElement(sheet)
    # Row 1: headers
    row1 = TableRow()
    sheet.addElement(row1)
    for val in ["Metric", "Value", "Class Average"]:
        cell = TableCell(valuetype="string")
        cell.addElement(P(text=val))
        row1.addElement(cell)
    # Row 2: class average row - C2 also empty
    row2 = TableRow()
    sheet.addElement(row2)
    for val in ["Class Average", "", ""]:
        cell = TableCell(valuetype="string")
        cell.addElement(P(text=val))
        row2.addElement(cell)
    doc.save("{ods_path}")
    print("ODS created via odfpy")
except ImportError:
    # Fallback: create using openpyxl as .xlsx then convert, or just create a minimal ODS manually
    print("odfpy not available, creating minimal ODS manually")
    import struct, zipfile, io
    # Create a minimal ODS (OpenDocument Spreadsheet) ZIP archive
    content_xml = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
  xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  office:version="1.2">
  <office:body>
    <office:spreadsheet>
      <table:table table:name="Summary">
        <table:table-row>
          <table:table-cell office:value-type="string"><text:p>Metric</text:p></table:table-cell>
          <table:table-cell office:value-type="string"><text:p>Value</text:p></table:table-cell>
          <table:table-cell office:value-type="string"><text:p>Class Average</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell office:value-type="string"><text:p>Class Average</text:p></table:table-cell>
          <table:table-cell/>
          <table:table-cell/>
        </table:table-row>
      </table:table>
    </office:spreadsheet>
  </office:body>
</office:document-content>"""
    manifest_xml = """<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.spreadsheet" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="META-INF/manifest.xml"/>
</manifest:manifest>"""
    mimetype = "application/vnd.oasis.opendocument.spreadsheet"
    with zipfile.ZipFile("{ods_path}", "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("mimetype", mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr("content.xml", content_xml)
        zf.writestr("META-INF/manifest.xml", manifest_xml)
    print("ODS created via manual ZIP")
'''
    result = subprocess.run(['python3', '-c', python_code], capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f'Warning: ODS creation: {result.stderr.strip()}')
    print(f'grades_summary.ods created: {ods_path}')


def cleanup_report_if_exists():
    """Ensure grade_report.txt does NOT exist initially."""
    report_path = f'{DATA_DIR}/grade_report.txt'
    if os.path.exists(report_path):
        os.remove(report_path)
        print(f'Removed pre-existing grade_report.txt')


def main():
    create_directories()
    create_grades_csv()
    create_grade_analyzer_stub()
    create_grades_summary_ods()
    cleanup_report_if_exists()

    # Verify files exist
    import glob
    files = glob.glob(f'{DATA_DIR}/*') + glob.glob(f'{SCRIPTS_DIR}/*')
    print('\nFiles created:')
    for f in sorted(files):
        print(f'  {f}')

    # GUI-ready startup: open the ODS file in LibreOffice Calc and the script in a text editor
    ods_path = f'{DATA_DIR}/grades_summary.ods'
    script_path = f'{SCRIPTS_DIR}/grade_analyzer.py'
    launch_gui(f'libreoffice --calc "{ods_path}"', delay_sec=2.0)
    launch_gui(f'gedit "{script_path}"', delay_sec=1.5)
    print('GUI_READY: launched LibreOffice Calc (grades_summary.ods) and gedit (grade_analyzer.py) with DISPLAY=:0')


main()
