"""
Initial Setup: Enable minimap in VSCode
Task ID: vscode_stu_015
Domain: vscode

Creates a long Python file and configures VSCode with minimap disabled.
Opens VSCode with the file so the agent can enable the minimap.
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_015'
OUTPUT = f'{WORKDIR}/{TASK_ID}.py'

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")


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


def load_settings():
    try:
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_settings(updates: dict):
    settings = load_settings()
    settings.update(updates)
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def create_long_python_file():
    """Create a realistic long Python file that benefits from minimap navigation."""
    content = '''"""
Data Analytics Pipeline - Sales Performance Report Generator
============================================================
This module processes quarterly sales data, generates performance metrics,
and creates summary reports for the executive team.
"""

import os
import csv
import json
import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


# ── Configuration ──────────────────────────────────────────────────────

DATABASE_PATH = "/var/data/sales/quarterly_reports.db"
OUTPUT_DIR = "/home/user/reports"
FISCAL_YEAR_START_MONTH = 4
REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]
CURRENCY_SYMBOLS = {"USD": "$", "EUR": "\\u20ac", "GBP": "\\u00a3", "JPY": "\\u00a5"}


# ── Data Models ────────────────────────────────────────────────────────

class SalesRecord:
    """Represents a single sales transaction."""

    def __init__(self, transaction_id: str, date: str, region: str,
                 product_line: str, amount: float, currency: str,
                 sales_rep: str, customer_id: str):
        self.transaction_id = transaction_id
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.region = region
        self.product_line = product_line
        self.amount = amount
        self.currency = currency
        self.sales_rep = sales_rep
        self.customer_id = customer_id

    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "date": self.date.strftime("%Y-%m-%d"),
            "region": self.region,
            "product_line": self.product_line,
            "amount": self.amount,
            "currency": self.currency,
            "sales_rep": self.sales_rep,
            "customer_id": self.customer_id,
        }

    def __repr__(self):
        return f"SalesRecord({self.transaction_id}, {self.region}, {self.amount})"


class PerformanceMetric:
    """Aggregated performance metrics for a region or product line."""

    def __init__(self, name: str):
        self.name = name
        self.total_revenue = 0.0
        self.transaction_count = 0
        self.unique_customers = set()
        self.monthly_totals = defaultdict(float)

    @property
    def average_deal_size(self) -> float:
        if self.transaction_count == 0:
            return 0.0
        return self.total_revenue / self.transaction_count

    @property
    def customer_count(self) -> int:
        return len(self.unique_customers)

    def add_transaction(self, record: SalesRecord):
        self.total_revenue += record.amount
        self.transaction_count += 1
        self.unique_customers.add(record.customer_id)
        month_key = record.date.strftime("%Y-%m")
        self.monthly_totals[month_key] += record.amount

    def growth_rate(self, period1: str, period2: str) -> Optional[float]:
        val1 = self.monthly_totals.get(period1, 0)
        val2 = self.monthly_totals.get(period2, 0)
        if val1 == 0:
            return None
        return ((val2 - val1) / val1) * 100


# ── Data Loading ───────────────────────────────────────────────────────

def load_sales_data(filepath: str) -> List[SalesRecord]:
    """Load sales records from a CSV file."""
    records = []
    if not os.path.exists(filepath):
        print(f"Warning: Data file not found at {filepath}")
        return records

    with open(filepath, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                record = SalesRecord(
                    transaction_id=row["id"],
                    date=row["date"],
                    region=row["region"],
                    product_line=row["product"],
                    amount=float(row["amount"]),
                    currency=row.get("currency", "USD"),
                    sales_rep=row["rep"],
                    customer_id=row["customer"],
                )
                records.append(record)
            except (KeyError, ValueError) as e:
                print(f"Skipping malformed row: {e}")
    return records


def load_targets(filepath: str) -> Dict[str, float]:
    """Load quarterly sales targets from JSON."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)


# ── Analysis Functions ─────────────────────────────────────────────────

def analyze_by_region(records: List[SalesRecord]) -> Dict[str, PerformanceMetric]:
    """Aggregate sales data by geographic region."""
    metrics = {}
    for record in records:
        if record.region not in metrics:
            metrics[record.region] = PerformanceMetric(record.region)
        metrics[record.region].add_transaction(record)
    return metrics


def analyze_by_product(records: List[SalesRecord]) -> Dict[str, PerformanceMetric]:
    """Aggregate sales data by product line."""
    metrics = {}
    for record in records:
        if record.product_line not in metrics:
            metrics[record.product_line] = PerformanceMetric(record.product_line)
        metrics[record.product_line].add_transaction(record)
    return metrics


def identify_top_performers(records: List[SalesRecord],
                            top_n: int = 5) -> List[Tuple[str, float]]:
    """Find the top N sales representatives by total revenue."""
    rep_totals = defaultdict(float)
    for record in records:
        rep_totals[record.sales_rep] += record.amount
    sorted_reps = sorted(rep_totals.items(), key=lambda x: x[1], reverse=True)
    return sorted_reps[:top_n]


def calculate_quarter(date: datetime.datetime) -> str:
    """Determine fiscal quarter for a given date."""
    adjusted_month = (date.month - FISCAL_YEAR_START_MONTH) % 12
    quarter = adjusted_month // 3 + 1
    fiscal_year = date.year if date.month >= FISCAL_YEAR_START_MONTH else date.year - 1
    return f"FY{fiscal_year}-Q{quarter}"


def quarterly_summary(records: List[SalesRecord]) -> Dict[str, float]:
    """Summarize total revenue by fiscal quarter."""
    summary = defaultdict(float)
    for record in records:
        q = calculate_quarter(record.date)
        summary[q] += record.amount
    return dict(summary)


# ── Report Generation ──────────────────────────────────────────────────

def generate_text_report(region_metrics: Dict[str, PerformanceMetric],
                         product_metrics: Dict[str, PerformanceMetric],
                         top_reps: List[Tuple[str, float]],
                         output_path: str):
    """Generate a plain-text executive summary report."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write("=" * 70 + "\\n")
        f.write("QUARTERLY SALES PERFORMANCE REPORT\\n")
        f.write(f"Generated: {datetime.datetime.now().strftime(\'%Y-%m-%d %H:%M\')}\\n")
        f.write("=" * 70 + "\\n\\n")

        # Regional breakdown
        f.write("REGIONAL PERFORMANCE\\n")
        f.write("-" * 40 + "\\n")
        for name, metric in sorted(region_metrics.items()):
            f.write(f"  {name:<25} ${metric.total_revenue:>12,.2f}  "
                    f"({metric.transaction_count} deals, "
                    f"{metric.customer_count} customers)\\n")

        total_revenue = sum(m.total_revenue for m in region_metrics.values())
        f.write(f"\\n  {'TOTAL':<25} ${total_revenue:>12,.2f}\\n\\n")

        # Product breakdown
        f.write("PRODUCT LINE PERFORMANCE\\n")
        f.write("-" * 40 + "\\n")
        for name, metric in sorted(product_metrics.items()):
            f.write(f"  {name:<25} ${metric.total_revenue:>12,.2f}  "
                    f"(avg deal: ${metric.average_deal_size:,.2f})\\n")

        # Top performers
        f.write("\\nTOP SALES REPRESENTATIVES\\n")
        f.write("-" * 40 + "\\n")
        for rank, (rep, total) in enumerate(top_reps, 1):
            f.write(f"  {rank}. {rep:<25} ${total:>12,.2f}\\n")

    print(f"Report saved to {output_path}")


def generate_json_export(records: List[SalesRecord], output_path: str):
    """Export all records as JSON for downstream processing."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = [r.to_dict() for r in records]
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"JSON export saved to {output_path} ({len(data)} records)")


# ── Main Execution ─────────────────────────────────────────────────────

def main():
    """Main entry point for the sales analytics pipeline."""
    print("Starting Sales Performance Analysis...")
    print(f"Data source: {DATABASE_PATH}")
    print(f"Output directory: {OUTPUT_DIR}")

    # Load data
    records = load_sales_data(DATABASE_PATH)
    if not records:
        print("No sales records found. Generating sample data for demo...")
        records = generate_sample_data()

    print(f"Loaded {len(records)} sales records")

    # Run analyses
    region_metrics = analyze_by_region(records)
    product_metrics = analyze_by_product(records)
    top_reps = identify_top_performers(records)
    q_summary = quarterly_summary(records)

    # Generate outputs
    report_path = os.path.join(OUTPUT_DIR, "quarterly_report.txt")
    generate_text_report(region_metrics, product_metrics, top_reps, report_path)

    export_path = os.path.join(OUTPUT_DIR, "sales_export.json")
    generate_json_export(records, export_path)

    # Print quarterly summary
    print("\\nQuarterly Revenue Summary:")
    for quarter, total in sorted(q_summary.items()):
        print(f"  {quarter}: ${total:,.2f}")

    print("\\nAnalysis complete.")


def generate_sample_data() -> List[SalesRecord]:
    """Generate sample sales data for demonstration purposes."""
    import random
    random.seed(42)

    reps = ["Sarah Chen", "Marcus Johnson", "Priya Patel", "James Wilson",
            "Maria Garcia", "David Kim", "Emma Thompson", "Robert Brown"]
    products = ["Enterprise Suite", "Cloud Platform", "Data Analytics",
                "Security Pro", "DevOps Tools"]

    records = []
    for i in range(200):
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        records.append(SalesRecord(
            transaction_id=f"TXN-{i+1:05d}",
            date=f"2025-{month:02d}-{day:02d}",
            region=random.choice(REGIONS),
            product_line=random.choice(products),
            amount=round(random.uniform(5000, 150000), 2),
            currency="USD",
            sales_rep=random.choice(reps),
            customer_id=f"CUST-{random.randint(1000, 9999)}",
        ))
    return records


if __name__ == "__main__":
    main()
'''
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial Python file created: {OUTPUT}')


def create_initial():
    # Step 1: Create the long Python file
    create_long_python_file()

    # Step 2: Configure VSCode with minimap DISABLED
    update_settings({
        "editor.minimap.enabled": False
    })
    print(f'VSCode settings updated: minimap disabled')

    # Step 3: Launch VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
