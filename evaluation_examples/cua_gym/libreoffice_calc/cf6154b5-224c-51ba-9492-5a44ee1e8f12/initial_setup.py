"""
Initial Setup: Temperature sensor data in ODS format (pre-task state)
Task ID: osworld_multi_apps_code_script_output_012
Domain: libreoffice_calc (multi-app: calc + scripting + plotting)

Creates:
  - /home/user/data/sensor_data.ods  (3 sensors, 15-min readings over 7 days = 2016 rows)
  - /home/user/data/  directory
  - /home/user/scripts/  directory (empty — agent must create sensor_analysis.py)
  - /home/user/Desktop/  directory (empty — agent must create sensor_trends.png)

Does NOT create:
  - sensor_data.csv (agent must export from ODS)
  - sensor_analysis.py (agent must write it)
  - processed_sensor.csv (agent must generate it)
  - sensor_trends.png (agent must generate it)
"""

import os
import shlex
import subprocess
import time
import random
from datetime import datetime, timedelta

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_script_output_012'
DATA_DIR = f'{WORKDIR}/data'
SCRIPTS_DIR = f'{WORKDIR}/scripts'
DESKTOP_DIR = f'{WORKDIR}/Desktop'
ODS_OUTPUT = f'{DATA_DIR}/sensor_data.ods'


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
    # -----------------------------------------------------------------------
    # 1. Create required directories
    # -----------------------------------------------------------------------
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(DESKTOP_DIR, exist_ok=True)
    print(f"Directories created: {DATA_DIR}, {SCRIPTS_DIR}, {DESKTOP_DIR}")

    # -----------------------------------------------------------------------
    # 2. Generate realistic 7-day temperature/humidity sensor data
    #    3 sensors × 15-min intervals over 7 days = 3 × 672 = 2016 rows
    # -----------------------------------------------------------------------
    try:
        from odf.opendocument import OpenDocumentSpreadsheet
        from odf.table import Table, TableRow, TableCell
        from odf.text import P
        from odf.style import Style, TextProperties, TableCellProperties
        from odf.namespaces import OFFICENS
        import odf.number

        doc = OpenDocumentSpreadsheet()
        table = Table(name="SensorData")

        # Write header row
        header_row = TableRow()
        for col_name in ["timestamp", "sensor_id", "temperature", "humidity"]:
            cell = TableCell(valuetype="string")
            cell.addElement(P(text=col_name))
            header_row.addElement(cell)
        table.addElement(header_row)

        # Generate 7 days of 15-minute interval data
        start_time = datetime(2024, 1, 15, 0, 0, 0)
        sensors = [
            ("SENSOR_A", 22.0, 0.8, 45.0, 2.0),   # (id, base_temp, temp_noise, base_hum, hum_noise)
            ("SENSOR_B", 18.5, 1.2, 60.0, 3.5),
            ("SENSOR_C", 25.5, 0.6, 38.0, 1.5),
        ]

        random.seed(42)
        row_count = 0
        num_intervals = 7 * 24 * 4  # 672 intervals per sensor

        for interval_idx in range(num_intervals):
            ts = start_time + timedelta(minutes=15 * interval_idx)
            ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")

            # Diurnal variation: sine wave approximation
            hour_frac = ts.hour + ts.minute / 60.0
            diurnal = 3.0 * (0.5 - abs(hour_frac - 14.0) / 24.0)

            for sensor_id, base_temp, temp_noise, base_hum, hum_noise in sensors:
                # Temperature with diurnal cycle + noise
                temperature = round(base_temp + diurnal + random.gauss(0, temp_noise), 2)
                # Introduce a few anomalies (about 1% of readings)
                if random.random() < 0.01:
                    temperature += random.choice([-8.0, 9.5, -7.5, 10.0])
                    temperature = round(temperature, 2)

                humidity = round(base_hum + random.gauss(0, hum_noise), 2)
                humidity = max(20.0, min(95.0, humidity))

                data_row = TableRow()

                # timestamp (string)
                c_ts = TableCell(valuetype="string")
                c_ts.addElement(P(text=ts_str))
                data_row.addElement(c_ts)

                # sensor_id (string)
                c_sid = TableCell(valuetype="string")
                c_sid.addElement(P(text=sensor_id))
                data_row.addElement(c_sid)

                # temperature (float)
                c_temp = TableCell(valuetype="float",
                                   attributes={
                                       (OFFICENS, "value"): str(temperature)
                                   })
                c_temp.addElement(P(text=str(temperature)))
                data_row.addElement(c_temp)

                # humidity (float)
                c_hum = TableCell(valuetype="float",
                                  attributes={
                                      (OFFICENS, "value"): str(humidity)
                                  })
                c_hum.addElement(P(text=str(humidity)))
                data_row.addElement(c_hum)

                table.addElement(data_row)
                row_count += 1

        doc.spreadsheet.addElement(table)
        doc.save(ODS_OUTPUT)
        print(f"ODS file created: {ODS_OUTPUT} ({row_count} data rows)")

    except ImportError:
        # Fallback: generate as XLSX then tell user
        print("odfpy not available, falling back to XLSX-based ODS creation via subprocess")
        _create_ods_via_csv_fallback()

    # -----------------------------------------------------------------------
    # 3. GUI-ready startup — open sensor_data.ods in LibreOffice Calc
    # -----------------------------------------------------------------------
    launch_gui(f'libreoffice --calc "{ODS_OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: LibreOffice Calc opened with sensor_data.ods (DISPLAY=:0)')


def _create_ods_via_csv_fallback():
    """Fallback: create CSV then convert to ODS via LibreOffice headless."""
    import csv

    csv_path = f'{DATA_DIR}/sensor_data_temp.csv'
    start_time = datetime(2024, 1, 15, 0, 0, 0)
    sensors = [
        ("SENSOR_A", 22.0, 0.8, 45.0, 2.0),
        ("SENSOR_B", 18.5, 1.2, 60.0, 3.5),
        ("SENSOR_C", 25.5, 0.6, 38.0, 1.5),
    ]
    random.seed(42)
    num_intervals = 7 * 24 * 4

    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "humidity"])
        for interval_idx in range(num_intervals):
            ts = start_time + timedelta(minutes=15 * interval_idx)
            ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
            hour_frac = ts.hour + ts.minute / 60.0
            diurnal = 3.0 * (0.5 - abs(hour_frac - 14.0) / 24.0)
            for sensor_id, base_temp, temp_noise, base_hum, hum_noise in sensors:
                temperature = round(base_temp + diurnal + random.gauss(0, temp_noise), 2)
                if random.random() < 0.01:
                    temperature += random.choice([-8.0, 9.5, -7.5, 10.0])
                    temperature = round(temperature, 2)
                humidity = round(max(20.0, min(95.0, base_hum + random.gauss(0, hum_noise))), 2)
                writer.writerow([ts_str, sensor_id, temperature, humidity])

    # Convert CSV to ODS using LibreOffice headless
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    result = subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "ods", "--outdir", DATA_DIR, csv_path],
        env=env, capture_output=True, text=True, timeout=60
    )
    print(f"LibreOffice conversion: {result.stdout} {result.stderr}")
    # Rename if needed
    converted = f'{DATA_DIR}/sensor_data_temp.ods'
    if os.path.exists(converted):
        os.rename(converted, ODS_OUTPUT)
        print(f"Renamed to {ODS_OUTPUT}")
    os.remove(csv_path)


create_initial()
