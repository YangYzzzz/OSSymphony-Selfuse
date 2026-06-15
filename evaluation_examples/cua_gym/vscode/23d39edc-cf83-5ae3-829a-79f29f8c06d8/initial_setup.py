"""
initial_setup.py – Create pre-task state for vscode_gf4_026.

Sets up:
  - ~/projects/python-ml-project/ with data/iris.csv
  - VSCode open with the project folder
  - Python 3.11 and extensions already installed (assumed in image)
  - No virtual environment
"""
import csv
import os
import shlex
import subprocess
import time

WORKDIR = "/home/user"
PROJECT = os.path.join(WORKDIR, "projects", "python-ml-project")
TASK_ID = "vscode_gf4_026"


def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_iris_csv(path: str):
    """Create the standard iris dataset with 150 rows."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Standard iris dataset
    iris_data = []
    # Setosa (50 samples)
    setosa_samples = [
        (5.1,3.5,1.4,0.2),(4.9,3.0,1.4,0.2),(4.7,3.2,1.3,0.2),(4.6,3.1,1.5,0.2),
        (5.0,3.6,1.4,0.2),(5.4,3.9,1.7,0.4),(4.6,3.4,1.4,0.3),(5.0,3.4,1.5,0.2),
        (4.4,2.9,1.4,0.2),(4.9,3.1,1.5,0.1),(5.4,3.7,1.5,0.2),(4.8,3.4,1.6,0.2),
        (4.8,3.0,1.4,0.1),(4.3,3.0,1.1,0.1),(5.8,4.0,1.2,0.2),(5.7,4.4,1.5,0.4),
        (5.4,3.9,1.3,0.4),(5.1,3.5,1.4,0.3),(5.7,3.8,1.7,0.3),(5.1,3.8,1.5,0.3),
        (5.4,3.4,1.7,0.2),(5.1,3.7,1.5,0.4),(4.6,3.6,1.0,0.2),(5.1,3.3,1.7,0.5),
        (4.8,3.4,1.9,0.2),(5.0,3.0,1.6,0.2),(5.0,3.4,1.6,0.4),(5.2,3.5,1.5,0.2),
        (5.2,3.4,1.4,0.2),(4.7,3.2,1.6,0.2),(4.8,3.1,1.6,0.2),(5.4,3.4,1.5,0.4),
        (5.2,4.1,1.5,0.1),(5.5,4.2,1.4,0.2),(4.9,3.1,1.5,0.2),(5.0,3.2,1.2,0.2),
        (5.5,3.5,1.3,0.2),(4.9,3.6,1.4,0.1),(4.4,3.0,1.3,0.2),(5.1,3.4,1.5,0.2),
        (5.0,3.5,1.3,0.3),(4.5,2.3,1.3,0.3),(4.4,3.2,1.3,0.2),(5.0,3.5,1.6,0.6),
        (5.1,3.8,1.9,0.4),(4.8,3.0,1.4,0.3),(5.1,3.8,1.6,0.2),(4.6,3.2,1.4,0.2),
        (5.3,3.7,1.5,0.2),(5.0,3.3,1.4,0.2),
    ]
    # Versicolor (50 samples)
    versicolor_samples = [
        (7.0,3.2,4.7,1.4),(6.4,3.2,4.5,1.5),(6.9,3.1,4.9,1.5),(5.5,2.3,4.0,1.3),
        (6.5,2.8,4.6,1.5),(5.7,2.8,4.5,1.3),(6.3,3.3,4.7,1.6),(4.9,2.4,3.3,1.0),
        (6.6,2.9,4.6,1.3),(5.2,2.7,3.9,1.4),(5.0,2.0,3.5,1.0),(5.9,3.0,4.2,1.5),
        (6.0,2.2,4.0,1.0),(6.1,2.9,4.7,1.4),(5.6,2.9,3.6,1.3),(6.7,3.1,4.4,1.4),
        (5.6,3.0,4.5,1.5),(5.8,2.7,4.1,1.0),(6.2,2.2,4.5,1.5),(5.6,2.5,3.9,1.1),
        (5.9,3.2,4.8,1.8),(6.1,2.8,4.0,1.3),(6.3,2.5,4.9,1.5),(6.1,2.8,4.7,1.2),
        (6.4,2.9,4.3,1.3),(6.6,3.0,4.4,1.4),(6.8,2.8,4.8,1.4),(6.7,3.0,5.0,1.7),
        (6.0,2.9,4.5,1.5),(5.7,2.6,3.5,1.0),(5.5,2.4,3.8,1.1),(5.5,2.4,3.7,1.0),
        (5.8,2.7,3.9,1.2),(6.0,2.7,5.1,1.6),(5.4,3.0,4.5,1.5),(6.0,3.4,4.5,1.6),
        (6.7,3.1,4.7,1.5),(6.3,2.3,4.4,1.3),(5.6,3.0,4.1,1.3),(5.5,2.5,4.0,1.3),
        (5.5,2.6,4.4,1.2),(6.1,3.0,4.6,1.4),(5.8,2.6,4.0,1.2),(5.0,2.3,3.3,1.0),
        (5.6,2.7,4.2,1.3),(5.7,3.0,4.2,1.2),(5.7,2.9,4.2,1.3),(6.2,2.9,4.3,1.3),
        (5.1,2.5,3.0,1.1),(5.7,2.8,4.1,1.3),
    ]
    # Virginica (50 samples)
    virginica_samples = [
        (6.3,3.3,6.0,2.5),(5.8,2.7,5.1,1.9),(7.1,3.0,5.9,2.1),(6.3,2.9,5.6,1.8),
        (6.5,3.0,5.8,2.2),(7.6,3.0,6.6,2.1),(4.9,2.5,4.5,1.7),(7.3,2.9,6.3,1.8),
        (6.7,2.5,5.8,1.8),(7.2,3.6,6.1,2.5),(6.5,3.2,5.1,2.0),(6.4,2.7,5.3,1.9),
        (6.8,3.0,5.5,2.1),(5.7,2.5,5.0,2.0),(5.8,2.8,5.1,2.4),(6.4,3.2,5.3,2.3),
        (6.5,3.0,5.5,1.8),(7.7,3.8,6.7,2.2),(7.7,2.6,6.9,2.3),(6.0,2.2,5.0,1.5),
        (6.9,3.2,5.7,2.3),(5.6,2.8,4.9,2.0),(7.7,2.8,6.7,2.0),(6.3,2.7,4.9,1.8),
        (6.7,3.3,5.7,2.1),(7.2,3.2,6.0,1.8),(6.2,2.8,4.8,1.8),(6.1,3.0,4.9,1.8),
        (6.4,2.8,5.6,2.1),(7.2,3.0,5.8,1.6),(7.4,2.8,6.1,1.9),(7.9,3.8,6.4,2.0),
        (6.4,2.8,5.6,2.2),(6.3,2.8,5.1,1.5),(6.1,2.6,5.6,1.4),(7.7,3.0,6.1,2.3),
        (6.3,3.4,5.6,2.4),(6.4,3.1,5.5,1.8),(6.0,3.0,4.8,1.8),(6.9,3.1,5.4,2.1),
        (6.7,3.1,5.6,2.4),(6.9,3.1,5.1,2.3),(5.8,2.7,5.1,1.9),(6.8,3.2,5.9,2.3),
        (6.7,3.3,5.7,2.5),(6.7,3.0,5.2,2.3),(6.3,2.5,5.0,1.9),(6.5,3.0,5.2,2.0),
        (6.2,3.4,5.4,2.3),(5.9,3.0,5.1,1.8),
    ]

    for s in setosa_samples:
        iris_data.append(list(s) + ["setosa"])
    for s in versicolor_samples:
        iris_data.append(list(s) + ["versicolor"])
    for s in virginica_samples:
        iris_data.append(list(s) + ["virginica"])

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sepal_length", "sepal_width", "petal_length", "petal_width", "species"])
        writer.writerows(iris_data)

    print(f"Created iris.csv with {len(iris_data)} rows")


def create_initial():
    # Create project directory structure
    os.makedirs(os.path.join(PROJECT, "data"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT, "src"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT, "notebooks"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT, ".vscode"), exist_ok=True)

    # Create iris.csv
    create_iris_csv(os.path.join(PROJECT, "data", "iris.csv"))

    # Create empty __init__.py for src package
    with open(os.path.join(PROJECT, "src", "__init__.py"), "w") as f:
        f.write("")

    # Install python3-venv so the agent can create venvs
    subprocess.run(
        "echo 'password' | sudo -S apt-get update -qq 2>/dev/null",
        shell=True, capture_output=True,
    )
    subprocess.run(
        "echo 'password' | sudo -S apt-get install -y -qq python3.10-venv 2>/dev/null",
        shell=True, capture_output=True,
    )

    # Remove any existing venv to ensure clean state
    venv_path = os.path.join(PROJECT, "venv")
    if os.path.exists(venv_path):
        import shutil
        shutil.rmtree(venv_path)

    # Open VSCode with the project
    launch_gui(f'code "{PROJECT}"', delay_sec=3.0)
    print("GUI_READY")


if __name__ == "__main__":
    create_initial()
