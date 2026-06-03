"""
Initial Setup: Data pipeline task - create raw CSV files and directory structure.
Task ID: osworld_multi_apps_code_batch_terminal_012
Domain: libreoffice_calc (multi-app: terminal + calc)

Creates:
  - /home/user/data/raw/  (5 CSV files with slightly inconsistent dates and missing values)
  - /home/user/data/clean/  (empty, for agent to populate)
  - /home/user/data/final/  (empty, for agent to populate)
  - /home/user/scripts/    (empty, for agent to place etl_pipeline.sh)

Does NOT create:
  - etl_pipeline.sh (agent must write this)
  - Cleaned CSV files (agent must produce these)
  - combined.csv (agent must produce this)
  - Any xlsx file (agent must open combined.csv in Calc and add summary)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_batch_terminal_012'

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
    # Create directory structure
    raw_dir = os.path.join(WORKDIR, 'data', 'raw')
    clean_dir = os.path.join(WORKDIR, 'data', 'clean')
    final_dir = os.path.join(WORKDIR, 'data', 'final')
    scripts_dir = os.path.join(WORKDIR, 'scripts')

    for d in [raw_dir, clean_dir, final_dir, scripts_dir]:
        os.makedirs(d, exist_ok=True)

    # ---------------------------------------------------------------
    # CSV file 1: sales_north_q1.csv
    # Dates in YYYY-MM-DD format, mostly clean but 2 rows with missing values
    # ---------------------------------------------------------------
    csv1 = os.path.join(raw_dir, 'sales_north_q1.csv')
    with open(csv1, 'w') as f:
        f.write('date,product,sales,region\n')
        f.write('2024-01-03,Widget A,4250.00,North\n')
        f.write('2024-01-10,Gadget Pro,8120.50,North\n')
        f.write('2024-01-17,Widget A,3980.00,North\n')
        f.write('2024-01-24,,6340.00,North\n')          # missing product
        f.write('2024-02-05,Smart Hub,11230.75,North\n')
        f.write('2024-02-14,Gadget Pro,9450.00,North\n')
        f.write('2024-02-21,Widget A,,North\n')          # missing sales
        f.write('2024-02-28,Smart Hub,10890.00,North\n')
        f.write('2024-03-06,Gadget Pro,8760.25,North\n')
        f.write('2024-03-15,Widget A,5120.00,North\n')
        f.write('2024-03-22,Smart Hub,12340.50,North\n')
        f.write('2024-03-29,Gadget Pro,9870.00,North\n')

    # ---------------------------------------------------------------
    # CSV file 2: sales_south_q1.csv
    # Dates in MM/DD/YYYY format (inconsistent)
    # ---------------------------------------------------------------
    csv2 = os.path.join(raw_dir, 'sales_south_q1.csv')
    with open(csv2, 'w') as f:
        f.write('date,product,sales,region\n')
        f.write('01/04/2024,Widget A,3870.00,South\n')
        f.write('01/11/2024,Gadget Pro,7640.00,South\n')
        f.write('01/18/2024,Smart Hub,9980.25,South\n')
        f.write('01/25/2024,Widget A,4120.50,South\n')
        f.write('02/06/2024,Gadget Pro,8550.00,South\n')
        f.write('02/13/2024,,7230.75,South\n')           # missing product
        f.write('02/20/2024,Smart Hub,10440.00,South\n')
        f.write('02/27/2024,Widget A,3960.00,South\n')
        f.write('03/05/2024,Gadget Pro,8130.50,South\n')
        f.write('03/12/2024,Smart Hub,11670.00,South\n')
        f.write('03/19/2024,Widget A,,South\n')           # missing sales
        f.write('03/26/2024,Gadget Pro,9240.00,South\n')

    # ---------------------------------------------------------------
    # CSV file 3: sales_east_q1.csv
    # Dates in DD-MM-YYYY format (inconsistent)
    # ---------------------------------------------------------------
    csv3 = os.path.join(raw_dir, 'sales_east_q1.csv')
    with open(csv3, 'w') as f:
        f.write('date,product,sales,region\n')
        f.write('05-01-2024,Widget A,4560.00,East\n')
        f.write('12-01-2024,Gadget Pro,7890.50,East\n')
        f.write('19-01-2024,Smart Hub,10120.75,East\n')
        f.write('26-01-2024,Widget A,5030.00,East\n')
        f.write('02-02-2024,Gadget Pro,8900.00,East\n')
        f.write('09-02-2024,Smart Hub,,East\n')            # missing sales
        f.write('16-02-2024,Widget A,4780.25,East\n')
        f.write('23-02-2024,Gadget Pro,9120.00,East\n')
        f.write('01-03-2024,,11340.50,East\n')             # missing product
        f.write('08-03-2024,Widget A,5460.00,East\n')
        f.write('15-03-2024,Gadget Pro,9670.00,East\n')
        f.write('22-03-2024,Smart Hub,13200.25,East\n')

    # ---------------------------------------------------------------
    # CSV file 4: sales_west_q1.csv
    # Dates in YYYY/MM/DD format (another inconsistency)
    # ---------------------------------------------------------------
    csv4 = os.path.join(raw_dir, 'sales_west_q1.csv')
    with open(csv4, 'w') as f:
        f.write('date,product,sales,region\n')
        f.write('2024/01/06,Widget A,5230.00,West\n')
        f.write('2024/01/13,Gadget Pro,9340.75,West\n')
        f.write('2024/01/20,Smart Hub,12450.00,West\n')
        f.write('2024/01/27,,7890.50,West\n')              # missing product
        f.write('2024/02/03,Widget A,5670.00,West\n')
        f.write('2024/02/10,Gadget Pro,10120.25,West\n')
        f.write('2024/02/17,Smart Hub,13560.00,West\n')
        f.write('2024/02/24,Widget A,,West\n')              # missing sales
        f.write('2024/03/02,Gadget Pro,9870.50,West\n')
        f.write('2024/03/09,Smart Hub,14230.00,West\n')
        f.write('2024/03/16,Widget A,6340.00,West\n')
        f.write('2024/03/23,Gadget Pro,10890.75,West\n')

    # ---------------------------------------------------------------
    # CSV file 5: sales_central_q1.csv
    # Dates in M/D/YYYY format (another inconsistency) + duplicate rows
    # ---------------------------------------------------------------
    csv5 = os.path.join(raw_dir, 'sales_central_q1.csv')
    with open(csv5, 'w') as f:
        f.write('date,product,sales,region\n')
        f.write('1/7/2024,Widget A,3450.00,Central\n')
        f.write('1/14/2024,Gadget Pro,6780.25,Central\n')
        f.write('1/21/2024,Smart Hub,8960.50,Central\n')
        f.write('1/28/2024,Widget A,3780.00,Central\n')
        f.write('2/4/2024,Gadget Pro,7230.00,Central\n')
        f.write('2/4/2024,Gadget Pro,7230.00,Central\n')   # duplicate row
        f.write('2/11/2024,,6540.75,Central\n')             # missing product
        f.write('2/18/2024,Widget A,4120.00,Central\n')
        f.write('2/25/2024,Smart Hub,9870.00,Central\n')
        f.write('3/3/2024,Gadget Pro,7560.50,Central\n')
        f.write('3/10/2024,Widget A,,Central\n')             # missing sales
        f.write('3/17/2024,Smart Hub,10230.25,Central\n')
        f.write('3/24/2024,Gadget Pro,8120.00,Central\n')

    print(f'Created directory structure:')
    print(f'  {raw_dir}/ (5 CSV files)')
    print(f'  {clean_dir}/ (empty)')
    print(f'  {final_dir}/ (empty)')
    print(f'  {scripts_dir}/ (empty)')

    # GUI: Open a file manager pointing to the data directory so user can see structure
    # Also open a terminal so agent can write and run the script
    launch_gui('nautilus /home/user/data', delay_sec=1.5)
    launch_gui('bash -c "xterm -e bash" ', delay_sec=1.0)

    print('GUI_READY: launched file manager and terminal with DISPLAY=:0')


create_initial()
