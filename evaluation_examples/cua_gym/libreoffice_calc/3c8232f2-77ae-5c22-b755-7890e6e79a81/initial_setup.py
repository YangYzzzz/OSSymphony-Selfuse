"""
Initial Setup: Survey data workflow - create survey.ods with 40 rows and 6 score columns (some NaN)
Task ID: osworld_multi_apps_multi_case_convert_008
Domain: libreoffice_calc (multi-app workflow)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DATA_DIR = '/home/user/data'
TASK_ID = 'osworld_multi_apps_multi_case_convert_008'
OUTPUT_ODS = f'{DATA_DIR}/survey.ods'


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
    import pandas as pd
    import numpy as np

    # Create data directory
    os.makedirs(DATA_DIR, exist_ok=True)

    # Realistic survey data: 40 respondents, 6 score columns
    np.random.seed(42)
    n = 40

    respondent_ids = [f'R{str(i).zfill(3)}' for i in range(1, n + 1)]
    ages = np.random.randint(18, 65, size=n).tolist()
    departments = [
        'Engineering', 'Marketing', 'Finance', 'HR', 'Operations',
        'Sales', 'Legal', 'Product', 'Design', 'Support'
    ]
    dept_col = [departments[i % len(departments)] for i in range(n)]
    tenure_years = np.round(np.random.uniform(0.5, 15.0, size=n), 1).tolist()

    # 6 score columns (scale 1-10), with some NaN values (~15% each)
    score_cols = ['satisfaction_score', 'engagement_score', 'productivity_score',
                  'collaboration_score', 'innovation_score', 'wellbeing_score']

    scores_data = {}
    for col in score_cols:
        raw = np.random.uniform(1.0, 10.0, size=n)
        # Introduce ~15% NaN
        mask = np.random.choice([True, False], size=n, p=[0.15, 0.85])
        raw_with_nan = raw.tolist()
        for idx in range(n):
            if mask[idx]:
                raw_with_nan[idx] = None
        scores_data[col] = raw_with_nan

    data = {
        'respondent_id': respondent_ids,
        'age': ages,
        'department': dept_col,
        'tenure_years': tenure_years,
    }
    for col in score_cols:
        data[col] = scores_data[col]

    df = pd.DataFrame(data)

    # Save as ODS
    df.to_excel(OUTPUT_ODS, index=False, engine='odf')
    print(f'Initial ODS file created: {OUTPUT_ODS}')
    print(f'Shape: {df.shape}')
    print(f'NaN count per score column:')
    for col in score_cols:
        print(f'  {col}: {df[col].isna().sum()} NaN values')

    # GUI-ready startup: open the ODS file in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{OUTPUT_ODS}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with DISPLAY=:0')


create_initial()
