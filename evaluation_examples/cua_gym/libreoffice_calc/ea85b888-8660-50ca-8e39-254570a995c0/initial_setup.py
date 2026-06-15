"""
Initial Setup: Desktop Cleanup and Document Organization
Task ID: osworld_multi_apps_doc_desktop_organize_008
Domain: multi_apps (os + libreoffice_calc + libreoffice_writer)

Creates 30 mixed files on the Desktop representing a cluttered workspace.
Files span personal (invoices, letters, CVs), work (reports, spreadsheets,
presentations), code (scripts, notebooks), media (images), and archive types.
No folder organization is present in the initial state.
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_doc_desktop_organize_008'


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
    os.makedirs(DESKTOP, exist_ok=True)

    # --- Personal: Finance files (invoices) ---
    Path(f'{DESKTOP}/invoice_consulting_march2024.pdf.txt').write_text(
        "INVOICE\n\nFrom: Sarah Chen Consulting\nTo: Meridian Tech Solutions\n"
        "Invoice #: INV-2024-0312\nDate: March 12, 2024\nDue: April 12, 2024\n\n"
        "Services: IT Strategy Consulting - Q1 2024\nHours: 24 @ $150/hr\n"
        "Subtotal: $3,600.00\nTax (8%): $288.00\nTotal: $3,888.00\n\n"
        "Payment via bank transfer to Account: 4521-887-223\n"
    )

    Path(f'{DESKTOP}/invoice_freelance_design_jan2024.pdf.txt').write_text(
        "INVOICE\n\nFrom: Marcus Johnson Design Studio\nTo: BlueWave Creative Agency\n"
        "Invoice #: MJD-0124-07\nDate: January 18, 2024\nDue: February 17, 2024\n\n"
        "Logo redesign package: $2,200.00\nSocial media assets (20 pieces): $800.00\n"
        "Total: $3,000.00\n\nBank: First National Bank\nAccount: 7734-552-109\n"
    )

    Path(f'{DESKTOP}/tax_return_2023_draft.txt').write_text(
        "TAX RETURN DRAFT - 2023\n\nTaxpayer: Elena Rodriguez\nSSN: XXX-XX-4521\n"
        "Filing Status: Single\nGross Income: $87,450.00\nDeductions: $13,850.00\n"
        "Taxable Income: $73,600.00\nFederal Tax Owed: $12,420.00\n"
        "Withholdings: $14,100.00\nRefund: $1,680.00\n\nStatus: DRAFT - needs review\n"
    )

    # --- Personal: Letters ---
    Path(f'{DESKTOP}/cover_letter_software_engineer.txt').write_text(
        "Dear Hiring Manager,\n\nI am writing to express my strong interest in the "
        "Senior Software Engineer position at DataFlow Systems. With 7 years of "
        "experience in backend development and distributed systems, I am confident "
        "in my ability to contribute meaningfully to your engineering team.\n\n"
        "At my current role at Apex Technologies, I led the migration of our "
        "monolithic application to microservices, reducing deployment time by 60%.\n\n"
        "Sincerely,\nDavid Park\n415-223-8874\ndavid.park@email.com\n"
    )

    Path(f'{DESKTOP}/letter_landlord_repairs_notice.txt').write_text(
        "April 3, 2024\n\nDear Mr. Thompson,\n\nI am writing regarding the ongoing "
        "maintenance issues at my rental property located at 1247 Oak Street, Unit 3B.\n\n"
        "As discussed on March 28th, the following repairs remain unaddressed:\n"
        "- Leaking kitchen faucet (reported Feb 15)\n"
        "- Broken heating unit in bedroom (reported Feb 28)\n"
        "- Damaged bathroom tiles (reported Mar 5)\n\n"
        "Please arrange repairs within 14 days per our lease agreement.\n\n"
        "Regards,\nJessica Williams\n"
    )

    Path(f'{DESKTOP}/recommendation_letter_michael_chen.txt').write_text(
        "To Whom It May Concern,\n\nI write with great enthusiasm to recommend "
        "Michael Chen for admission to the Master of Computer Science program.\n\n"
        "Michael worked as a research assistant in my lab for two years, demonstrating "
        "exceptional skills in machine learning and data analysis. His work on our "
        "natural language processing project resulted in a paper accepted at NeurIPS 2023.\n\n"
        "Michael is among the top 5% of students I have supervised in 15 years.\n\n"
        "Prof. Amanda Foster\nDepartment of Computer Science\nState University\n"
    )

    # --- Personal: CVs ---
    Path(f'{DESKTOP}/resume_sarah_chen_2024.txt').write_text(
        "SARAH CHEN\n415-887-2234 | sarah.chen@email.com | linkedin.com/in/sarahchen\n\n"
        "SUMMARY\nSenior Data Scientist with 6 years experience in ML/AI solutions.\n\n"
        "EXPERIENCE\nLead Data Scientist | Apex Analytics | 2021-Present\n"
        "- Built recommendation engine serving 2M+ users (15% CTR improvement)\n"
        "- Led team of 5 data scientists\n\n"
        "Data Scientist | NeuroTech | 2018-2021\n"
        "- Developed NLP pipeline reducing manual review by 40%\n\n"
        "EDUCATION\nMS Computer Science, Stanford University, 2018\n"
        "BS Mathematics, UC Berkeley, 2016\n"
    )

    Path(f'{DESKTOP}/cv_james_okafor_marketing.txt').write_text(
        "JAMES OKAFOR\nMarketing Director\njames.okafor@email.com | 312-445-7823\n\n"
        "PROFESSIONAL SUMMARY\n10+ years in B2B marketing, specializing in demand "
        "generation and brand strategy.\n\n"
        "WORK HISTORY\nMarketing Director | GlobalEdge Inc | 2020-Present\n"
        "- Increased qualified leads by 78% through ABM campaigns\n"
        "- Managed $3.2M annual marketing budget\n\n"
        "Senior Marketing Manager | CloudFirst | 2016-2020\n"
        "- Launched 12 product campaigns, average 35% pipeline contribution\n\n"
        "MBA, Northwestern University Kellogg School, 2014\n"
    )

    # --- Work: Reports ---
    Path(f'{DESKTOP}/quarterly_sales_report_q1_2024.txt').write_text(
        "Q1 2024 SALES REPORT\nRegion: North America\nPrepared by: Sales Analytics Team\n\n"
        "EXECUTIVE SUMMARY\nTotal Q1 Revenue: $4.82M (vs Q1 2023: $3.97M, +21.4%)\n\n"
        "KEY METRICS\n- New Customers: 142 (target: 120)\n"
        "- Average Deal Size: $33,943\n- Win Rate: 34%\n"
        "- Pipeline Generated: $18.4M\n\n"
        "TOP PERFORMERS\n1. Western Region: $1.92M (39.8% of total)\n"
        "2. Eastern Region: $1.64M\n3. Central: $1.26M\n\n"
        "RECOMMENDATIONS\nFocus Q2 investment on enterprise segment (82% of revenue).\n"
    )

    Path(f'{DESKTOP}/annual_performance_review_2023.txt').write_text(
        "ANNUAL PERFORMANCE REVIEW 2023\nEmployee: Marcus Johnson\nDept: Engineering\n"
        "Manager: Dr. Lisa Park\nReview Period: Jan-Dec 2023\n\n"
        "PERFORMANCE RATINGS (1-5 scale)\nTechnical Skills: 4.5\n"
        "Communication: 4.0\nLeadership: 3.8\nDelivery: 4.2\nOverall: 4.1\n\n"
        "ACHIEVEMENTS\n- Delivered Project Phoenix 2 weeks ahead of schedule\n"
        "- Mentored 3 junior engineers\n- Reduced system latency by 35%\n\n"
        "GOALS FOR 2024\n1. Complete AWS Solutions Architect certification\n"
        "2. Lead cross-functional team on Platform v3\n"
    )

    Path(f'{DESKTOP}/market_analysis_saas_sector_2024.txt').write_text(
        "MARKET ANALYSIS: SaaS Sector 2024\nAnalyst: Jennifer Walsh, CFA\n"
        "Date: March 2024\n\n"
        "MARKET OVERVIEW\nGlobal SaaS market: $232B (2024E), CAGR 11.7% (2024-2029)\n\n"
        "KEY TRENDS\n1. AI Integration: 87% of vendors adding AI features\n"
        "2. Security Focus: Compliance spending up 24% YoY\n"
        "3. Vertical SaaS: Healthcare/fintech driving 40% of new ARR\n\n"
        "COMPETITIVE LANDSCAPE\nTop 5 players hold 38% of market share.\n"
        "Mid-market consolidation accelerating (32 acquisitions in 2023).\n\n"
        "RECOMMENDATION: Overweight enterprise SaaS, underweight SMB-focused.\n"
    )

    # --- Work: Spreadsheets ---
    Path(f'{DESKTOP}/budget_tracking_2024.csv').write_text(
        "Category,Q1_Budget,Q1_Actual,Q2_Budget,Q2_Forecast\n"
        "Personnel,450000,447230,460000,462100\n"
        "Marketing,85000,78430,92000,89500\n"
        "Infrastructure,32000,34210,35000,36800\n"
        "R&D,120000,115670,125000,128400\n"
        "Travel,18000,12340,20000,15600\n"
        "Software Licenses,25000,24780,26000,26200\n"
        "Office Supplies,8000,7230,8500,7800\n"
        "Training,15000,11250,16000,14200\n"
        "Contingency,20000,5430,22000,18000\n"
        "Total,773000,736570,804500,798600\n"
    )

    Path(f'{DESKTOP}/employee_data_export_march2024.csv').write_text(
        "EmployeeID,Name,Department,Title,Salary,StartDate,Location\n"
        "E001,Sarah Chen,Engineering,Senior Engineer,95000,2021-03-15,San Francisco\n"
        "E002,Marcus Johnson,Marketing,Marketing Manager,78000,2020-06-01,New York\n"
        "E003,Elena Rodriguez,Finance,Financial Analyst,72000,2022-01-10,Chicago\n"
        "E004,David Park,Engineering,Software Engineer,88000,2021-09-20,San Francisco\n"
        "E005,Jessica Williams,HR,HR Business Partner,68000,2019-11-05,Boston\n"
        "E006,James Okafor,Sales,Account Executive,65000,2023-02-14,New York\n"
        "E007,Amanda Foster,Engineering,Tech Lead,105000,2018-07-22,San Francisco\n"
        "E008,Michael Chen,Product,Product Manager,98000,2020-04-08,New York\n"
    )

    # --- Work: Presentations ---
    Path(f'{DESKTOP}/product_roadmap_2024_presentation_draft.txt').write_text(
        "PRODUCT ROADMAP 2024 - PRESENTATION DRAFT\n\n"
        "Slide 1: Title - 'DataFlow Platform: 2024 Roadmap'\n"
        "Presenter: Michael Chen, Product\n\n"
        "Slide 2: Executive Summary\n"
        "- Q1: Infrastructure hardening & security audit\n"
        "- Q2: API v3 launch + Developer Portal\n"
        "- Q3: ML Pipeline integration\n"
        "- Q4: Enterprise features & compliance\n\n"
        "Slide 3: Q1 Priorities\n"
        "- Zero-downtime deployment\n- SOC2 Type II certification\n"
        "- Performance: 99.99% uptime SLA\n\n"
        "Slide 4: Q2 - API v3\nBreaking changes: removed deprecated endpoints\n"
        "New: GraphQL support, webhook management, improved rate limiting\n\n"
        "Slide 5: Revenue Impact\nProjected ARR from new features: $2.4M\n"
    )

    Path(f'{DESKTOP}/investor_pitch_deck_notes.txt').write_text(
        "INVESTOR PITCH DECK - SPEAKER NOTES\nCompany: Nexus Analytics\nRound: Series A\n\n"
        "Slide 1 - Hook: '83% of business decisions lack real-time data'\n\n"
        "Slide 2 - Problem\n"
        "- Data silos across 7 avg enterprise tools\n"
        "- Analytics lag: 3-5 day delay to actionable insight\n"
        "- Cost: $4.2M avg annual lost productivity\n\n"
        "Slide 3 - Solution\nNexus unifies data from 200+ connectors in real-time.\n"
        "Setup in <1 day vs 6-month enterprise BI projects.\n\n"
        "Slide 4 - Traction\nARR: $2.8M | Customers: 47 | NPS: 72\n"
        "Growth: 15% MoM for past 8 months\n\n"
        "Ask: $8M for 18-month runway. Use of funds: 60% eng, 30% sales, 10% ops.\n"
    )

    # --- Code: Scripts ---
    Path(f'{DESKTOP}/data_pipeline_etl.py').write_text(
        "#!/usr/bin/env python3\n"
        "\"\"\"ETL pipeline for customer data processing.\"\"\"\n\n"
        "import pandas as pd\nimport psycopg2\nfrom datetime import datetime\n"
        "import logging\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)\n\n"
        "DB_CONFIG = {\n    'host': 'db.internal.company.com',\n"
        "    'database': 'analytics_prod',\n    'user': 'etl_service',\n"
        "    'port': 5432\n}\n\n"
        "def extract_customers(conn):\n"
        "    query = \"\"\"\n        SELECT c.id, c.name, c.email, c.created_at,\n"
        "               COUNT(o.id) as order_count, SUM(o.total) as lifetime_value\n"
        "        FROM customers c\n        LEFT JOIN orders o ON c.id = o.customer_id\n"
        "        WHERE c.created_at >= '2024-01-01'\n        GROUP BY c.id\n    \"\"\"\n"
        "    return pd.read_sql(query, conn)\n\n"
        "def transform(df):\n"
        "    df['ltv_segment'] = pd.cut(df['lifetime_value'],\n"
        "        bins=[0, 500, 2000, 10000, float('inf')],\n"
        "        labels=['Low', 'Medium', 'High', 'VIP'])\n"
        "    df['days_since_join'] = (datetime.now() - pd.to_datetime(df['created_at'])).dt.days\n"
        "    return df\n\n"
        "if __name__ == '__main__':\n    logger.info('Starting ETL pipeline')\n"
    )

    Path(f'{DESKTOP}/deploy_script_production.sh').write_text(
        "#!/bin/bash\n# Production deployment script\n# Usage: ./deploy_script_production.sh [version]\n\n"
        "VERSION=${1:-latest}\nAPP_NAME='dataflow-api'\nCLUSTER='prod-k8s-us-west-2'\n\n"
        "set -e\nset -o pipefail\n\n"
        "echo \"Deploying $APP_NAME version $VERSION to $CLUSTER\"\n\n"
        "# Pre-deployment checks\nkubectl get pods -n production | grep $APP_NAME\n\n"
        "# Pull and tag image\ndocker pull registry.company.com/$APP_NAME:$VERSION\ndocker tag registry.company.com/$APP_NAME:$VERSION $APP_NAME:current\n\n"
        "# Deploy via helm\nhelm upgrade $APP_NAME ./charts/$APP_NAME \\\n"
        "  --namespace production \\\n  --set image.tag=$VERSION \\\n"
        "  --set replicas=3 \\\n  --wait --timeout 10m\n\n"
        "echo \"Deployment complete. Running smoke tests...\"\npython3 tests/smoke_test.py --env production\n"
    )

    Path(f'{DESKTOP}/api_client_library.js').write_text(
        "/**\n * Nexus Analytics API Client Library v2.3.1\n"
        " * @description JavaScript client for Nexus Analytics REST API\n"
        " */\n\n"
        "const BASE_URL = 'https://api.nexusanalytics.com/v2';\n\n"
        "class NexusClient {\n  constructor(apiKey, options = {}) {\n"
        "    this.apiKey = apiKey;\n    this.timeout = options.timeout || 30000;\n"
        "    this.retries = options.retries || 3;\n  }\n\n"
        "  async getMetrics(params) {\n"
        "    const response = await fetch(`${BASE_URL}/metrics`, {\n"
        "      method: 'GET',\n      headers: { 'Authorization': `Bearer ${this.apiKey}` },\n"
        "    });\n    return response.json();\n  }\n\n"
        "  async createReport(config) {\n"
        "    const response = await fetch(`${BASE_URL}/reports`, {\n"
        "      method: 'POST',\n      headers: {\n"
        "        'Authorization': `Bearer ${this.apiKey}`,\n"
        "        'Content-Type': 'application/json'\n      },\n"
        "      body: JSON.stringify(config)\n    });\n    return response.json();\n  }\n}\n\n"
        "module.exports = NexusClient;\n"
    )

    Path(f'{DESKTOP}/database_migration_v4.sql').write_text(
        "-- Database Migration: v3 -> v4\n-- Date: 2024-03-01\n-- Author: Elena Rodriguez\n\n"
        "BEGIN;\n\n"
        "-- Add audit trail columns\nALTER TABLE customers\n"
        "  ADD COLUMN created_by VARCHAR(100),\n"
        "  ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "  ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE;\n\n"
        "-- Create new analytics table\nCREATE TABLE usage_metrics (\n"
        "  id SERIAL PRIMARY KEY,\n  user_id INTEGER REFERENCES users(id),\n"
        "  event_type VARCHAR(50) NOT NULL,\n  event_data JSONB,\n"
        "  occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,\n"
        "  session_id VARCHAR(100)\n);\n\n"
        "CREATE INDEX idx_usage_metrics_user_event ON usage_metrics(user_id, event_type);\n"
        "CREATE INDEX idx_usage_metrics_occurred ON usage_metrics(occurred_at);\n\n"
        "COMMIT;\n"
    )

    # --- Code: Notebooks ---
    Path(f'{DESKTOP}/customer_churn_analysis.ipynb.txt').write_text(
        "JUPYTER NOTEBOOK: Customer Churn Analysis\n"
        "Author: James Okafor | Date: March 2024\n\n"
        "CELL 1: Import libraries\nimport pandas as pd\nimport numpy as np\n"
        "from sklearn.ensemble import RandomForestClassifier\n"
        "from sklearn.model_selection import train_test_split\n\n"
        "CELL 2: Load data\ndf = pd.read_csv('customer_data_2023.csv')\n"
        "print(f'Dataset: {df.shape[0]} customers, {df.shape[1]} features')\n"
        "# Dataset: 15,234 customers, 28 features\n\n"
        "CELL 3: Feature engineering\n"
        "df['days_since_last_login'] = (pd.Timestamp.now() - pd.to_datetime(df['last_login'])).dt.days\n"
        "df['avg_monthly_spend'] = df['total_spend'] / df['months_active']\n\n"
        "CELL 4: Model training\nX = df.drop(['customer_id', 'churned'], axis=1)\ny = df['churned']\n"
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\n"
        "model = RandomForestClassifier(n_estimators=200, random_state=42)\nmodel.fit(X_train, y_train)\n\n"
        "CELL 5: Results\nAccuracy: 0.847, AUC-ROC: 0.923\nTop features: days_since_last_login, avg_monthly_spend\n"
    )

    Path(f'{DESKTOP}/revenue_forecasting_model.ipynb.txt').write_text(
        "JUPYTER NOTEBOOK: Revenue Forecasting Model\n"
        "Author: Jennifer Walsh | Date: Feb 2024\n\n"
        "CELL 1: Setup\nimport pandas as pd\nimport numpy as np\n"
        "from prophet import Prophet\nimport matplotlib.pyplot as plt\n\n"
        "CELL 2: Load historical data\ndf = pd.read_csv('revenue_2021_2023.csv')\n"
        "# 36 months of monthly revenue data\n# Range: $1.2M - $4.8M\n\n"
        "CELL 3: Prepare for Prophet\ndf_prophet = df.rename(columns={'month': 'ds', 'revenue': 'y'})\n"
        "df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])\n\n"
        "CELL 4: Fit model\nm = Prophet(yearly_seasonality=True, weekly_seasonality=False)\n"
        "m.add_regressor('marketing_spend')\nm.fit(df_prophet)\n\n"
        "CELL 5: Forecast\nfuture = m.make_future_dataframe(periods=12, freq='M')\n"
        "forecast = m.predict(future)\nprint('2024 Q1 Forecast: $5.2M')\n"
    )

    # --- Media: Images ---
    Path(f'{DESKTOP}/product_screenshot_dashboard.png.txt').write_text(
        "IMAGE METADATA: product_screenshot_dashboard.png\n"
        "Resolution: 1920x1080px | Format: PNG | Size: 2.3MB\n"
        "Created: 2024-03-10 14:23:07\n"
        "Content: Screenshot of DataFlow Analytics Dashboard\n"
        "Shows: Revenue chart, KPI widgets, user activity heatmap\n"
        "For use in: Product documentation, investor deck slide 8\n"
    )

    Path(f'{DESKTOP}/team_photo_offsite_2024.jpg.txt').write_text(
        "IMAGE METADATA: team_photo_offsite_2024.jpg\n"
        "Resolution: 4032x3024px | Format: JPEG | Size: 8.7MB\n"
        "Created: 2024-02-14 16:45:22\n"
        "Location: Lake Tahoe Retreat Center\n"
        "Content: Engineering team Q1 offsite photo\n"
        "Attendees: 23 team members (see roster sheet for names)\n"
        "Photographer: Amanda Foster\n"
    )

    Path(f'{DESKTOP}/logo_nexus_analytics_v3.svg.txt').write_text(
        "SVG IMAGE: logo_nexus_analytics_v3.svg\n"
        "Dimensions: 400x120px | Format: SVG | Version: 3.0\n"
        "Colors: Primary #2B4FAD, Secondary #48C7E2, Text #1A1A2E\n"
        "Created: 2024-01-05 by Marcus Johnson Design Studio\n"
        "Elements: Hexagonal icon, wordmark 'Nexus Analytics'\n"
        "Usage: Official logo for all company materials\n"
        "Approved by: CEO David Park, 2024-01-08\n"
    )

    Path(f'{DESKTOP}/architecture_diagram_v2.png.txt').write_text(
        "IMAGE METADATA: architecture_diagram_v2.png\n"
        "Resolution: 2560x1440px | Format: PNG | Size: 1.1MB\n"
        "Created: 2024-02-28 by Elena Rodriguez\n"
        "Content: System architecture diagram for DataFlow Platform v4\n"
        "Shows: Microservices (API Gateway, Auth, Analytics, Notification)\n"
        "Data stores: PostgreSQL, Redis, S3, Elasticsearch\n"
        "Infrastructure: AWS EKS, CloudFront CDN\n"
    )

    # --- Archives ---
    Path(f'{DESKTOP}/project_assets_2023_backup.zip.txt').write_text(
        "ARCHIVE INFO: project_assets_2023_backup.zip\n"
        "Size: 847MB | Created: 2024-01-02 | Files: 1,247\n"
        "Contents:\n"
        "  - /designs/ (423 files, Figma exports, mockups)\n"
        "  - /documentation/ (156 files, PRDs, specs, ADRs)\n"
        "  - /data/ (89 files, CSVs, JSON exports)\n"
        "  - /code/ (579 files, source snapshots)\n"
        "Compression: Deflate | Encrypted: No\n"
        "MD5: a3f7b8c9d4e2f1a0b7c6d5e4f3a2b1c0\n"
    )

    Path(f'{DESKTOP}/legacy_codebase_archive.tar.gz.txt').write_text(
        "ARCHIVE INFO: legacy_codebase_archive.tar.gz\n"
        "Size: 2.3GB | Created: 2023-12-15 | Files: 8,432\n"
        "Contents: Full git repository of DataFlow v1 and v2\n"
        "  - v1 (2020-2021): Monolithic Django application\n"
        "  - v2 (2022-2023): Migration to microservices (partial)\n"
        "Archive type: TAR + gzip | Checksum: SHA256\n"
        "SHA256: 7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d\n"
        "Notes: Keep for compliance/audit purposes. Do not delete.\n"
    )

    Path(f'{DESKTOP}/client_deliverables_q4_2023.zip.txt').write_text(
        "ARCHIVE INFO: client_deliverables_q4_2023.zip\n"
        "Size: 156MB | Created: 2023-12-29 | Files: 234\n"
        "Contents:\n"
        "  Meridian Tech - Final dashboard implementation\n"
        "  BlueWave Creative - Custom reporting module\n"
        "  GlobalEdge Inc - Data integration connectors\n"
        "  DataCore Systems - API documentation + SDK\n"
        "Delivery status: All delivered and signed off by clients\n"
        "Contact: jennifer.walsh@company.com for access requests\n"
    )

    # --- Additional mixed files to reach 30 total ---
    Path(f'{DESKTOP}/meeting_notes_board_review_march2024.txt').write_text(
        "BOARD REVIEW MEETING NOTES\nDate: March 28, 2024\nAttendees: CEO, CFO, CTO, 4 Board Members\n\n"
        "AGENDA ITEMS\n\n1. Q1 Financial Review\nRevenue: $4.82M (+21.4% YoY)\n"
        "Gross Margin: 72% (up from 68%)\nBurn Rate: $1.1M/month\nRunway: 22 months\n\n"
        "2. Product Update\nMLM Platform launch: May 15 (on track)\n"
        "Enterprise pipeline: $12.4M (8 deals >$500K)\n\n"
        "3. Hiring\nApproved: 12 new eng headcount for H2 2024\n\n"
        "4. Next Steps\n- CFO to finalize Q2 forecast by April 10\n"
        "- CEO to update investor deck with Q1 metrics\n"
    )

    Path(f'{DESKTOP}/config_server_production.yaml.txt').write_text(
        "# Production Server Configuration\n# Last updated: 2024-03-01\n# Owner: Platform Team\n\n"
        "server:\n  host: 0.0.0.0\n  port: 8443\n  workers: 16\n  timeout: 30\n\n"
        "database:\n  primary:\n    host: db-primary.internal\n    port: 5432\n"
        "    name: dataflow_prod\n    pool_size: 50\n  replica:\n"
        "    host: db-replica.internal\n    port: 5432\n    pool_size: 30\n\n"
        "cache:\n  redis:\n    host: redis.internal\n    port: 6379\n    db: 0\n"
        "    max_connections: 100\n\nmonitoring:\n  enabled: true\n"
        "  metrics_port: 9090\n  log_level: INFO\n"
    )

    Path(f'{DESKTOP}/system_requirements_document.txt').write_text(
        "SYSTEM REQUIREMENTS DOCUMENT\nProject: DataFlow Platform v4\n"
        "Version: 1.3 | Date: Feb 2024 | Author: Michael Chen\n\n"
        "1. FUNCTIONAL REQUIREMENTS\n\n1.1 Data Ingestion\n"
        "- System SHALL support 200+ data source connectors\n"
        "- System SHALL process minimum 10,000 events/second per tenant\n"
        "- System SHALL provide real-time streaming with <500ms latency\n\n"
        "1.2 Analytics Engine\n"
        "- System SHALL support SQL and NoSQL query interfaces\n"
        "- System SHALL complete dashboard queries in <2 seconds (P95)\n\n"
        "2. NON-FUNCTIONAL REQUIREMENTS\n"
        "- Availability: 99.99% uptime SLA\n- Security: SOC2 Type II compliant\n"
        "- Scalability: Handle 10x traffic spikes without degradation\n"
    )

    Path(f'{DESKTOP}/personal_journal_project_notes.txt').write_text(
        "PROJECT NOTES - Personal Reference\nUpdated: March 30, 2024\n\n"
        "CURRENT PRIORITIES\n1. Finish ML pipeline PR by Friday\n"
        "2. Review David's architecture doc (due Tuesday)\n"
        "3. Prep for board demo March 28\n\n"
        "IDEAS TO EXPLORE\n- Using vector DB for customer similarity search\n"
        "- Async job queue for heavy report generation\n"
        "- GraphQL subscriptions for real-time dashboard updates\n\n"
        "BLOCKERS\n- Waiting on DevOps for staging env access\n"
        "- Need legal review of data processing agreement\n\n"
        "UPCOMING DEADLINES\nApril 5: Q1 retrospective presentation\n"
        "April 12: Invoice to Meridian Tech (INV-2024-0412)\n"
    )

    Path(f'{DESKTOP}/onboarding_checklist_new_hire.txt').write_text(
        "NEW HIRE ONBOARDING CHECKLIST\nEmployee: [To Be Filled]\nStart Date: [TBD]\nManager: Amanda Foster\n\n"
        "WEEK 1: Setup\n[ ] Laptop provisioned with required software\n"
        "[ ] GitHub access granted\n[ ] Slack channels joined (#engineering, #product, #all-hands)\n"
        "[ ] Meeting with manager and skip-level\n[ ] Security training completed\n\n"
        "WEEK 2: Orientation\n[ ] Architecture walkthrough with Tech Lead\n"
        "[ ] First PR submitted and merged\n[ ] Customer empathy session with CS team\n\n"
        "WEEK 3-4: Ramp Up\n[ ] Assigned to starter project\n"
        "[ ] 30-day check-in with manager\n[ ] OKR alignment meeting\n"
    )

    Path(f'{DESKTOP}/financial_projection_model.xlsx.txt').write_text(
        "SPREADSHEET: financial_projection_model.xlsx\n"
        "Created: 2024-02-10 | Author: Jennifer Walsh CFO\n\n"
        "SHEET 1: Income Statement (Monthly, 24 months)\n"
        "Revenue drivers: Subscription, Professional Services, Usage\n"
        "2024 Total ARR Projection: $21.4M\n2025 Total ARR Projection: $38.7M\n\n"
        "SHEET 2: Balance Sheet\nCurrent Assets: $8.2M cash\nTotal Liabilities: $1.1M\n\n"
        "SHEET 3: Cash Flow\nOperating CF 2024E: $(4.8M) (investment phase)\n"
        "Break-even projected: Q3 2025\n\n"
        "SHEET 4: Sensitivity Analysis\nScenario Low/Base/High with key variable toggles\n"
        "Key assumption: 15% monthly growth rate (base case)\n"
    )

    print(f'Initial Desktop files created: 30 files in {DESKTOP}')
    print('Files cover: Personal (Finance, Letters, CVs), Work (Reports, Spreadsheets, Presentations),')
    print('             Code (Scripts, Notebooks), Media (Images), Archives')

    # GUI-ready startup: open Nautilus file manager showing the Desktop
    launch_gui(f'nautilus "{DESKTOP}"', delay_sec=2.0)
    print('GUI_READY: Launched Nautilus file manager showing Desktop with DISPLAY=:0')


create_initial()
