"""
Initial Setup: Configure VSCode pre-save code transformation pipeline
Task ID: vscode_gf5_036
Domain: vscode

Creates ~/projects/python-lib with a messy Python file,
installs isort/black, ensures Python extension is present,
and opens VSCode with NO formatting configuration.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_036'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-lib')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
SETTINGS_PATH = os.path.join(VSCODE_DIR, 'settings.json')
MESSY_PATH = os.path.join(SRC_DIR, 'messy.py')


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
    # 1. Create project directory structure
    os.makedirs(SRC_DIR, exist_ok=True)
    os.makedirs(VSCODE_DIR, exist_ok=True)

    # 2. Create __init__.py for the package
    with open(os.path.join(SRC_DIR, '__init__.py'), 'w') as f:
        f.write('"""Python library for data processing utilities."""\n')

    # 3. Create messy.py with unsorted imports and inconsistent formatting
    messy_content = '''\
import  sys
from collections import OrderedDict
import os
import json
from pathlib import Path
import re
from typing import List,Dict,Optional
import datetime
from dataclasses import dataclass
import math
from enum import Enum

class   Priority(Enum):
    LOW = 1
    MEDIUM=2
    HIGH =  3
    CRITICAL = 4

@dataclass
class  TaskItem:
    title:str
    assignee:  str
    priority:Priority
    due_date:Optional[datetime.date]=None
    tags:List[str]=None

    def __post_init__(self):
        if self.tags  is None:
            self.tags=[]

class   ProjectTracker:
    """Tracks project tasks and generates reports."""

    def __init__(self,project_name:str,  base_dir:str="/tmp/projects"):
        self.project_name=project_name
        self.base_dir = Path(base_dir)
        self.tasks:List[TaskItem]=[]
        self._log_file  =  self.base_dir / f"{project_name}_log.json"
        self.metadata:Dict[str,str] = OrderedDict()

    def add_task(self,title:str,assignee:str,
                 priority:Priority=Priority.MEDIUM,
                 due_date:Optional[datetime.date]=None)->TaskItem:
        task=TaskItem(title=title,assignee=assignee,
                      priority=priority,due_date=due_date)
        self.tasks.append(task)
        return  task

    def get_high_priority(self)->List[TaskItem]:
        return [t for t in self.tasks if t.priority.value>=Priority.HIGH.value]

    def  summary_stats(self)->Dict[str,int]:
        stats={}
        for  p in Priority:
            count=len([t for t in self.tasks if t.priority==p])
            stats[p.name]=count
        stats["total"]=len(self.tasks)
        return stats

    def export_report(self,output_path:Optional[str]=None)->str:
        if output_path is  None:
            output_path=str(self.base_dir/"report.json")
        os.makedirs(os.path.dirname(output_path),exist_ok=True)
        report={
            "project":self.project_name,
            "generated_at":datetime.datetime.now().isoformat(),
            "total_tasks":len(self.tasks),
            "high_priority_count":len(self.get_high_priority()),
            "stats":self.summary_stats(),
        }
        with open(output_path,"w") as f:
            json.dump(report,f,indent=2)
        return  output_path

    def filter_by_tags(self,  tags:List[str])->List[TaskItem]:
        pattern=re.compile("|".join(tags),re.IGNORECASE)
        return [t for t in self.tasks
                if any(pattern.search(tag) for tag in t.tags)]

    def calculate_workload(self)->Dict[str,float]:
        workload:Dict[str,float]={}
        for task in self.tasks:
            weight=math.log2(task.priority.value+1)
            if task.assignee  not in workload:
                workload[task.assignee]=0.0
            workload[task.assignee]+=weight
        return  dict(sorted(workload.items(),key=lambda x:x[1],reverse=True))


def  main():
    tracker=ProjectTracker("alpha-release")
    tracker.add_task("Design API schema","Sarah Chen",Priority.HIGH,
                     datetime.date(2025,4,15))
    tracker.add_task("Write unit tests","Marcus Johnson",Priority.MEDIUM)
    tracker.add_task("Deploy staging env","Priya Patel",Priority.CRITICAL,
                     datetime.date(2025,3,30))
    tracker.add_task("Update docs","Alex Rivera",Priority.LOW)
    tracker.add_task("Security audit","Jordan Kim",Priority.HIGH,
                     datetime.date(2025,4,1))

    print(f"Project: {tracker.project_name}")
    print(f"Stats: {tracker.summary_stats()}")
    print(f"High priority: {len(tracker.get_high_priority())} tasks")
    report_path=tracker.export_report()
    print(f"Report saved: {report_path}")

if __name__=="__main__":
    main()
'''
    with open(MESSY_PATH, 'w') as f:
        f.write(messy_content)

    # 4. Create a simple README
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write('# Python Lib\n\nA data processing utilities library for the Alpha team.\n\n'
                '## Setup\n\n```bash\npip install -r requirements.txt\n```\n')

    # 5. Create requirements.txt
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write('isort>=5.12.0\nblack>=23.0.0\npytest>=7.0.0\n')

    # 6. Create .vscode/settings.json with NO formatting config
    initial_settings = {
        "python.analysis.typeCheckingMode": "basic",
        "editor.tabSize": 4,
        "editor.insertSpaces": True,
        "files.trimTrailingWhitespace": True
    }
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(initial_settings, f, indent=4)

    print(f'Project created: {PROJECT_DIR}')
    print(f'Messy file: {MESSY_PATH}')
    print(f'Settings (no formatting config): {SETTINGS_PATH}')

    # 7. Install isort and black
    subprocess.run(['pip3', 'install', 'isort', 'black'], capture_output=True)
    print('Installed isort and black')

    # 8. Install Python and Black formatter extensions
    subprocess.run(['code', '--install-extension', 'ms-python.python', '--force'],
                   capture_output=True)
    subprocess.run(['code', '--install-extension', 'ms-python.black-formatter', '--force'],
                   capture_output=True)
    subprocess.run(['code', '--install-extension', 'ms-python.isort', '--force'],
                   capture_output=True)
    print('Installed VSCode extensions: ms-python.python, ms-python.black-formatter, ms-python.isort')

    # 9. Open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
