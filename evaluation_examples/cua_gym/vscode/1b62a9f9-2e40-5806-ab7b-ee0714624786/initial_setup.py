"""
Initial Setup: Set up Black formatter for Python project in VSCode
Task ID: vscode_wf_020
Domain: vscode

Creates ~/project with several .py files with inconsistent formatting.
Ensures Python extension is installed. Black is NOT installed.
No formatting-related VSCode settings exist.
Opens VSCode with ~/project.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_020'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
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


def create_project_files():
    """Create ~/project with several .py files having inconsistent formatting."""
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # File 1: main.py - inconsistent indentation and spacing
    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write('''import sys
import os
from utils import  calculate_metrics, load_data
from models import  TrainingPipeline

def main():
    data_path=sys.argv[1] if len(sys.argv)>1 else "data/sales_2024.csv"
    output_dir=sys.argv[2] if len(sys.argv)>2 else "reports"

    print(f"Loading data from {data_path}...")
    raw_data=load_data(data_path)

    if raw_data is None:
        print("Error: Could not load data file.",file=sys.stderr)
        sys.exit(1)

    pipeline=TrainingPipeline(
        learning_rate=0.001,batch_size=32,
        epochs=50,
        validation_split=0.2
    )

    metrics=calculate_metrics(raw_data)
    for  key,value in metrics.items():
        print(f"  {key}: {value:.4f}")

    os.makedirs(output_dir,exist_ok=True)
    pipeline.run(raw_data,output_dir)
    print("Training complete.")


if __name__=="__main__":
    main()
''')

    # File 2: utils.py - long lines and inconsistent spacing
    with open(os.path.join(PROJECT_DIR, 'utils.py'), 'w') as f:
        f.write('''import csv
import statistics
from datetime import datetime,timedelta
from typing import Dict,List,Optional,Tuple

def load_data(filepath: str) -> Optional[List[Dict]]:
    """Load CSV data from the given filepath and return as list of dicts."""
    try:
        with open(filepath,'r') as f:
            reader=csv.DictReader(f)
            records=[row for row in reader]
        print(f"Loaded {len(records)} records from {filepath}")
        return records
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Unexpected error reading {filepath}: {e}")
        return None


def calculate_metrics( data:List[Dict] )->Dict[str,float]:
    """Calculate summary statistics for the sales data."""
    revenues=[float(row.get("revenue",0)) for row in data if row.get("revenue")]
    quantities=[int(row.get("quantity",0)) for row in data if row.get("quantity")]

    result = {
        "total_revenue":sum(revenues),
        "mean_revenue":statistics.mean(revenues) if revenues else 0.0,
        "median_revenue":statistics.median(revenues) if revenues else 0.0,
        "std_revenue":statistics.stdev(revenues) if len(revenues)>1 else 0.0,
        "total_quantity":sum(quantities),
        "mean_quantity":statistics.mean(quantities) if quantities else 0.0,
        "record_count":len(data),
    }
    return result


def filter_by_date_range(data:List[Dict], start_date:str, end_date:str)->List[Dict]:
    """Filter records to those within the given date range (inclusive)."""
    start=datetime.strptime(start_date,"%Y-%m-%d")
    end=datetime.strptime(end_date,"%Y-%m-%d")
    filtered=[]
    for row in data:
        row_date=datetime.strptime(row.get("date","1970-01-01"),"%Y-%m-%d")
        if start<=row_date<=end:
            filtered.append(row)
    return filtered


def generate_report_filename(prefix:str="report")->str:
    """Generate a timestamped report filename."""
    now=datetime.now()
    return f"{prefix}_{now.strftime(\'%Y%m%d_%H%M%S\')}.csv"
''')

    # File 3: models.py - mixed formatting
    with open(os.path.join(PROJECT_DIR, 'models.py'), 'w') as f:
        f.write('''import os
import json
import random
from typing import Dict,List,Any,Optional

class TrainingPipeline:
    """A simple ML training pipeline for sales forecasting."""

    def __init__(self,learning_rate:float=0.001,batch_size:int=32,epochs:int=100,validation_split:float=0.2):
        self.learning_rate=learning_rate
        self.batch_size=batch_size
        self.epochs=epochs
        self.validation_split=validation_split
        self.history: List[Dict[str,float]]=[]
        self.best_loss=float("inf")

    def _split_data(self,data:List[Dict])->tuple:
        """Split data into training and validation sets."""
        random.shuffle(data)
        split_idx=int(len(data)*(1-self.validation_split))
        return data[:split_idx],data[split_idx:]

    def _train_epoch(self,train_data:List[Dict],epoch:int)->Dict[str,float]:
        """Simulate one training epoch."""
        base_loss=1.0/(epoch+1)
        noise=random.uniform(-0.05,0.05)
        loss=max(0.01,base_loss+noise)
        accuracy=min(0.99,1.0-loss+random.uniform(0,0.1))
        return {"epoch":epoch,"loss":round(loss,4),"accuracy":round(accuracy,4)}

    def run(self,data:List[Dict],output_dir:str)->None:
        """Execute the full training pipeline."""
        train_data,val_data=self._split_data(data)
        print(f"Training with {len(train_data)} samples, validating with {len(val_data)}")

        for epoch in range(self.epochs):
            metrics=self._train_epoch(train_data,epoch)
            self.history.append(metrics)
            if metrics["loss"]<self.best_loss:
                self.best_loss=metrics["loss"]
                self._save_checkpoint(output_dir,epoch)

        self._save_results(output_dir)

    def _save_checkpoint(self,output_dir:str,epoch:int)->None:
        checkpoint_path=os.path.join(output_dir,"best_model.json")
        with open(checkpoint_path,"w") as f:
            json.dump({"epoch":epoch,"loss":self.best_loss,"lr":self.learning_rate},f,indent=2)

    def _save_results(self,output_dir:str)->None:
        results_path=os.path.join(output_dir,"training_results.json")
        with open(results_path,"w") as f:
            json.dump({"history":self.history,"config":{"lr":self.learning_rate,"batch_size":self.batch_size,"epochs":self.epochs}},f,indent=2)
        print(f"Results saved to {results_path}")
''')

    # File 4: config.py - configuration constants with bad formatting
    with open(os.path.join(PROJECT_DIR, 'config.py'), 'w') as f:
        f.write('''"""Project configuration constants."""

DATABASE_URL="postgresql://localhost:5432/sales_db"
API_KEY="sk-proj-abc123def456"
MAX_RETRIES=3
TIMEOUT_SECONDS=30
LOG_LEVEL="INFO"
CACHE_TTL=3600

COLUMN_MAPPING={
    "date":"transaction_date",
    "revenue":"total_revenue",
    "quantity":"items_sold",
    "product":"product_name",
    "region":"sales_region",
}

REGIONS=["North America","Europe","Asia Pacific","Latin America","Middle East"]
PRODUCT_CATEGORIES=["Electronics","Clothing","Food & Beverage","Home & Garden","Sports"]

def get_config()->dict:
    return {
        "database_url":DATABASE_URL,
        "api_key":API_KEY,
        "max_retries":MAX_RETRIES,
        "timeout":TIMEOUT_SECONDS,
        "log_level":LOG_LEVEL,
        "cache_ttl":CACHE_TTL,
    }
''')

    print(f"Project files created in {PROJECT_DIR}")


def ensure_clean_settings():
    """Ensure VSCode settings exist but do NOT contain formatting config."""
    os.makedirs(VSCODE_USER, exist_ok=True)
    settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            settings = {}

    # Remove any formatting-related keys that should not exist initially
    keys_to_remove = [
        '[python]',
        'black-formatter.args',
        'python.formatting.provider',
        'editor.defaultFormatter',
        'editor.formatOnSave',
    ]
    for key in keys_to_remove:
        settings.pop(key, None)

    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f"VSCode settings cleaned at {SETTINGS_PATH}")


def ensure_black_not_installed():
    """Make sure black is not installed."""
    subprocess.run(['pip3', 'uninstall', '-y', 'black'], capture_output=True)
    subprocess.run(['pip', 'uninstall', '-y', 'black'], capture_output=True)
    print("Ensured black is not installed")


def main():
    create_project_files()
    ensure_clean_settings()
    ensure_black_not_installed()

    # Launch VSCode with the project folder
    launch_gui('code "/home/user/project"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with ~/project and DISPLAY=:0')


main()
