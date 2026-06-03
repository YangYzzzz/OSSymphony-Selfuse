"""
Initial Setup: matrix_multiply.py with empty function + input matrix files on Desktop
Task ID: osworld_multi_apps_vscode_run_capture_004
Domain: multi_apps (VSCode + OS)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_vscode_run_capture_004'


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
    os.makedirs(WORKDIR, exist_ok=True)

    # --- matrix_a.txt ---
    # A 3x3 matrix with comma-separated rows
    matrix_a_content = """\
1,2,3
4,5,6
7,8,9
"""
    matrix_a_path = os.path.join(WORKDIR, 'matrix_a.txt')
    with open(matrix_a_path, 'w') as f:
        f.write(matrix_a_content)
    print(f'Created: {matrix_a_path}')

    # --- matrix_b.txt ---
    # A 3x3 matrix with comma-separated rows
    matrix_b_content = """\
9,8,7
6,5,4
3,2,1
"""
    matrix_b_path = os.path.join(WORKDIR, 'matrix_b.txt')
    with open(matrix_b_path, 'w') as f:
        f.write(matrix_b_content)
    print(f'Created: {matrix_b_path}')

    # --- matrix_multiply.py ---
    # Script with empty multiply_matrices() function body
    script_content = """\
"""
    script_content = '''\
import os

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")


def read_matrix(filename):
    """Read a matrix from a comma-separated text file."""
    matrix = []
    filepath = os.path.join(DESKTOP, filename)
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                row = [int(x) for x in line.split(",")]
                matrix.append(row)
    return matrix


def multiply_matrices(a, b):
    """Multiply two matrices a and b.
    Returns the result matrix, or None if dimensions are incompatible.
    """
    # TODO: Implement matrix multiplication
    pass


def write_result(matrix, filename):
    """Write the result matrix to a text file on the Desktop."""
    filepath = os.path.join(DESKTOP, filename)
    with open(filepath, "w") as f:
        for row in matrix:
            f.write(",".join(str(x) for x in row) + "\\n")


if __name__ == "__main__":
    matrix_a = read_matrix("matrix_a.txt")
    matrix_b = read_matrix("matrix_b.txt")
    result = multiply_matrices(matrix_a, matrix_b)
    if result is None:
        print("Error: incompatible matrix dimensions")
    else:
        for row in result:
            print(",".join(str(x) for x in row))
        write_result(result, "result_matrix.txt")
'''

    script_path = os.path.join(WORKDIR, 'matrix_multiply.py')
    with open(script_path, 'w') as f:
        f.write(script_content)
    print(f'Created: {script_path}')

    # Ensure result_matrix.txt does NOT exist (task asks agent to create it)
    result_path = os.path.join(WORKDIR, 'result_matrix.txt')
    if os.path.exists(result_path):
        os.remove(result_path)
        print(f'Removed pre-existing: {result_path}')

    # GUI-ready startup: open matrix_multiply.py in VSCode
    launch_gui(f'code "{script_path}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with matrix_multiply.py on DISPLAY=:0')


create_initial()
