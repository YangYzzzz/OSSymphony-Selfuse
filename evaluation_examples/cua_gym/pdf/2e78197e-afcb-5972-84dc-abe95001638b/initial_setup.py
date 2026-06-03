"""
Initial Setup: Create the pre-task state for inventory valuation report task.
Task ID: pdf_fin_090
Domain: pdf

Initial state: /home/user/finance/ directory exists with some context files.
The agent must create the inventory_valuation.pdf from scratch.
No PDF exists yet - that is the task.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
FINANCE_DIR = f'{WORKDIR}/finance'

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
    # 1. Create the finance directory
    os.makedirs(FINANCE_DIR, exist_ok=True)

    # 2. Create a context file that provides inventory data the agent might reference
    # This gives the agent context about what data to include
    inventory_data = """Inventory Data Export - March 31, 2024
Company: Meridian Manufacturing Inc.
Valuation Method: FIFO (First-In, First-Out)

Category Breakdown Target:
  Raw Materials: ~35% of total value
  Work-in-Progress (WIP): ~25% of total value
  Finished Goods: ~40% of total value

Item Records:
Code     | Description                    | Category        | Qty   | Unit Cost
---------|--------------------------------|-----------------|-------|----------
RM-1001  | Steel Sheet 4x8 Grade A       | Raw Materials   | 500   | $28.50
RM-1002  | Copper Wire 12AWG 500ft       | Raw Materials   | 380   | $45.75
RM-1003  | Aluminum Extrusion T6          | Raw Materials   | 220   | $62.30
RM-1004  | Polycarbonate Resin 25kg      | Raw Materials   | 340   | $38.90
RM-1005  | Stainless Steel Rod 316L       | Raw Materials   | 200   | $54.20
WP-2001  | Machined Housing Assembly      | WIP             | 95    | $142.50
WP-2002  | Circuit Board Sub-Assembly     | WIP             | 240   | $67.80
WP-2003  | Welded Frame Unit              | WIP             | 55    | $235.00
WP-2004  | Painted Enclosure Panel        | WIP             | 150   | $89.60
FG-3001  | Industrial Sensor Module X200  | Finished Goods  | 140   | $185.00
FG-3002  | Power Distribution Unit PD-50  | Finished Goods  | 60    | $420.00
FG-3003  | Control Panel CP-100           | Finished Goods  | 42    | $310.50
FG-3004  | Thermal Management Kit TM-30   | Finished Goods  | 75    | $156.75
FG-3005  | Signal Converter SC-15         | Finished Goods  | 110   | $98.40
FG-3006  | Monitoring Gateway MG-10       | Finished Goods  | 28    | $545.00

Notes:
- Total Value = Quantity x Unit Cost for each line item
- Report should include pie chart showing category distribution
- All items valued using FIFO method
"""
    with open(f'{FINANCE_DIR}/inventory_data_q1_2024.txt', 'w') as f:
        f.write(inventory_data)

    print(f'Initial state created: {FINANCE_DIR}/')
    print(f'Context file: {FINANCE_DIR}/inventory_data_q1_2024.txt')

    # 3. Open a terminal and file manager for the agent
    launch_gui(f'nautilus "{FINANCE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched file manager with DISPLAY=:0')

create_initial()
