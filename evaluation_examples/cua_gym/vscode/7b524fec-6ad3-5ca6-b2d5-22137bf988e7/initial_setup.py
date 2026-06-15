"""
Initial Setup: Create a Streamlit project with app.py for VSCode debugging task
Task ID: vscode_py_085
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_085'
PROJECT_DIR = f'{WORKDIR}/streamlit_project'

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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create app.py — a realistic Streamlit dashboard
    app_py_content = '''"""
Sales Analytics Dashboard
A Streamlit application for visualizing quarterly sales data.
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Quarterly Sales Analytics Dashboard")
st.markdown("---")


@st.cache_data
def load_sales_data():
    """Generate sample sales data for demonstration."""
    regions = ["North America", "Europe", "Asia Pacific", "Latin America"]
    products = ["Enterprise Suite", "Professional", "Starter", "Custom Solutions"]
    reps = [
        "Sarah Chen", "Marcus Johnson", "Elena Rodriguez",
        "James Kim", "Priya Patel", "Thomas Weber",
        "Aisha Mohammed", "David Park", "Sofia Andersson",
        "Ryan O\'Brien",
    ]

    records = []
    base_date = datetime(2025, 1, 1)
    for i in range(200):
        sale_date = base_date + timedelta(days=random.randint(0, 364))
        region = random.choice(regions)
        product = random.choice(products)
        rep = random.choice(reps)
        units = random.randint(1, 50)
        unit_price = {
            "Enterprise Suite": 2500,
            "Professional": 800,
            "Starter": 200,
            "Custom Solutions": 5000,
        }[product]
        revenue = units * unit_price
        records.append({
            "Date": sale_date,
            "Region": region,
            "Product": product,
            "Sales Rep": rep,
            "Units": units,
            "Revenue": revenue,
        })
    return pd.DataFrame(records)


data = load_sales_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=data["Region"].unique(),
    default=data["Region"].unique(),
)
selected_products = st.sidebar.multiselect(
    "Select Products",
    options=data["Product"].unique(),
    default=data["Product"].unique(),
)

# Apply filters
filtered_data = data[
    (data["Region"].isin(selected_regions))
    & (data["Product"].isin(selected_products))
]

# KPI metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue", f"${filtered_data[\'Revenue\'].sum():,.0f}")
with col2:
    st.metric("Total Units Sold", f"{filtered_data[\'Units\'].sum():,}")
with col3:
    st.metric("Avg Deal Size", f"${filtered_data[\'Revenue\'].mean():,.0f}")
with col4:
    st.metric("Number of Deals", f"{len(filtered_data):,}")

st.markdown("---")

# Revenue by region
st.subheader("Revenue by Region")
revenue_by_region = (
    filtered_data.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
)
st.bar_chart(revenue_by_region)

# Monthly trend
st.subheader("Monthly Revenue Trend")
filtered_data["Month"] = filtered_data["Date"].dt.to_period("M").astype(str)
monthly_revenue = filtered_data.groupby("Month")["Revenue"].sum()
st.line_chart(monthly_revenue)

# Top sales reps
st.subheader("Top Sales Representatives")
top_reps = (
    filtered_data.groupby("Sales Rep")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
st.dataframe(top_reps.reset_index(), use_container_width=True)

# Raw data
with st.expander("View Raw Data"):
    st.dataframe(filtered_data, use_container_width=True)
'''
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_py_content)

    # Create a requirements.txt
    requirements_content = """streamlit>=1.28.0
pandas>=2.0.0
"""
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    # Create a README for the project
    readme_content = """# Sales Analytics Dashboard

A Streamlit-based dashboard for visualizing quarterly sales performance data.

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
streamlit run app.py
```

The dashboard will be accessible at http://localhost:8501
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # Create a simple .gitignore
    gitignore_content = """__pycache__/
*.pyc
.env
venv/
.streamlit/
"""
    with open(os.path.join(PROJECT_DIR, '.gitignore'), 'w') as f:
        f.write(gitignore_content)

    # Ensure NO .vscode/launch.json exists (this is what the agent must create)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    launch_json_path = os.path.join(vscode_dir, 'launch.json')
    if os.path.exists(launch_json_path):
        os.remove(launch_json_path)

    print(f'Streamlit project created at: {PROJECT_DIR}')
    print(f'  app.py: {os.path.join(PROJECT_DIR, "app.py")}')
    print(f'  .vscode/launch.json: DOES NOT EXIST (task requirement)')

    # Install streamlit in the system Python so it's available
    subprocess.run(
        ['pip3', 'install', 'streamlit', 'pandas'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
