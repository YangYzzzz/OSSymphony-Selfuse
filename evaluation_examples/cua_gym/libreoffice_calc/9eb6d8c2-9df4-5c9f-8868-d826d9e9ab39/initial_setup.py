"""
Initial Setup: Create a 12-page portrait Letter PDF handout
Task ID: pdf_gf2_046
Domain: pdf (libreoffice_calc in config, but actual task is PDF manipulation)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_gf2_046'
OUTPUT = f'{WORKDIR}/handout.pdf'

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
    try:
        import pymupdf
    except ImportError:
        subprocess.check_call(['pip3', 'install', 'PyMuPDF'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import pymupdf

    os.makedirs(WORKDIR, exist_ok=True)

    # Page dimensions: portrait Letter
    W, H = 612, 792

    doc = pymupdf.open()

    # Content for 12 handout pages — a realistic training workshop handout
    pages_content = [
        {
            "title": "Data Analytics Workshop",
            "subtitle": "Module 1: Introduction to Data Pipelines",
            "body": (
                "Welcome to the Meridian Corp Data Analytics Workshop series. This handout "
                "accompanies the live training session held at the San Francisco campus.\n\n"
                "In this module, we will cover the fundamentals of data pipeline architecture, "
                "including ingestion, transformation, and delivery stages. By the end of this "
                "session, you will be able to design a basic ETL workflow using our internal "
                "tooling stack.\n\n"
                "Prerequisites: Basic SQL proficiency, familiarity with Python 3.x, and access "
                "to the Meridian Analytics Platform (MAP) staging environment."
            ),
        },
        {
            "title": "Data Pipeline Architecture",
            "subtitle": "Module 1 — Section 1.1",
            "body": (
                "A data pipeline is a series of processing steps that move data from source "
                "systems to analytical destinations. The three primary stages are:\n\n"
                "1. Ingestion — Collecting raw data from APIs, databases, file drops, and "
                "streaming sources such as Apache Kafka or AWS Kinesis.\n\n"
                "2. Transformation — Cleaning, normalizing, and enriching data. Common tools "
                "include Apache Spark, dbt, and pandas-based scripts.\n\n"
                "3. Delivery — Loading processed data into warehouses (Snowflake, BigQuery) "
                "or serving layers (Redis, Elasticsearch) for downstream consumption."
            ),
        },
        {
            "title": "Ingestion Patterns",
            "subtitle": "Module 1 — Section 1.2",
            "body": (
                "Batch ingestion pulls data at scheduled intervals — hourly, daily, or weekly. "
                "It is suitable for historical analysis and reporting where real-time freshness "
                "is not required.\n\n"
                "Streaming ingestion processes events continuously. Kafka topics feed into Flink "
                "or Spark Structured Streaming jobs that emit results with sub-second latency.\n\n"
                "Change Data Capture (CDC) tracks row-level changes in source databases using "
                "tools like Debezium. CDC bridges batch and streaming by providing incremental "
                "updates without full table scans.\n\n"
                "Recommended reading: Chapter 3 of 'Designing Data-Intensive Applications' "
                "by Martin Kleppmann."
            ),
        },
        {
            "title": "Transformation Best Practices",
            "subtitle": "Module 1 — Section 1.3",
            "body": (
                "Schema validation should occur at the earliest possible stage. Use JSON Schema "
                "or Avro schemas to reject malformed records before they propagate downstream.\n\n"
                "Idempotency is critical — rerunning a transformation on the same input should "
                "produce identical output. This enables safe retries after transient failures.\n\n"
                "Partition your data by date or region to enable parallel processing and efficient "
                "incremental updates. Avoid full-table rewrites when only a small partition changed.\n\n"
                "Testing: Write unit tests for transformation logic and integration tests that "
                "validate end-to-end pipeline correctness against known fixture data."
            ),
        },
        {
            "title": "Data Quality Monitoring",
            "subtitle": "Module 2: Observability and Alerting",
            "body": (
                "Module 2 focuses on ensuring data quality through automated monitoring and "
                "alerting. Poor data quality silently degrades downstream analytics, dashboards, "
                "and machine learning models.\n\n"
                "Key metrics to monitor:\n"
                "- Row count trends (sudden drops indicate ingestion failures)\n"
                "- Null rate per column (spikes suggest schema changes at source)\n"
                "- Value distribution shifts (statistical drift may signal data corruption)\n"
                "- Freshness (SLA: data should arrive within 2 hours of generation)\n\n"
                "Tools: Great Expectations, Monte Carlo, dbt tests, custom SQL assertions."
            ),
        },
        {
            "title": "Alerting Configuration",
            "subtitle": "Module 2 — Section 2.1",
            "body": (
                "Effective alerting requires clear ownership and escalation paths. Each pipeline "
                "should have a designated on-call engineer who receives PagerDuty notifications.\n\n"
                "Alert severity levels at Meridian Corp:\n"
                "- P1 (Critical): Revenue-impacting data outage — response within 15 minutes\n"
                "- P2 (High): SLA breach on key datasets — response within 1 hour\n"
                "- P3 (Medium): Quality degradation — response within 4 hours\n"
                "- P4 (Low): Non-urgent anomalies — addressed during business hours\n\n"
                "Avoid alert fatigue by tuning thresholds and suppressing known maintenance windows."
            ),
        },
        {
            "title": "Dashboard Design Principles",
            "subtitle": "Module 2 — Section 2.2",
            "body": (
                "Dashboards should answer specific questions, not display every available metric. "
                "Follow the inverted pyramid: the most critical KPIs appear at the top.\n\n"
                "Color encoding: Use red/amber/green sparingly and consistently. Red always means "
                "action required. Avoid using color as the sole differentiator (accessibility).\n\n"
                "Refresh cadence should match data freshness. A real-time dashboard on hourly data "
                "creates false expectations. Clearly label the last-updated timestamp.\n\n"
                "Recommended tools: Grafana for operational dashboards, Looker for business "
                "intelligence, Jupyter notebooks for ad-hoc exploratory analysis."
            ),
        },
        {
            "title": "Security and Access Control",
            "subtitle": "Module 3: Data Governance",
            "body": (
                "Module 3 addresses governance, compliance, and security requirements for "
                "analytical data systems. All Meridian Corp data assets must comply with SOC 2 "
                "Type II and GDPR regulations.\n\n"
                "Role-Based Access Control (RBAC) is enforced through our IAM integration. "
                "Analysts receive read-only access to curated datasets. Engineers have write "
                "access to staging environments but require approval for production changes.\n\n"
                "Personally Identifiable Information (PII) must be hashed or tokenized before "
                "entering the analytics warehouse. Use the PII-Scanner library to detect and "
                "flag sensitive fields automatically."
            ),
        },
        {
            "title": "Data Retention Policies",
            "subtitle": "Module 3 — Section 3.1",
            "body": (
                "Retention policies balance storage costs against analytical and compliance needs.\n\n"
                "Meridian Corp standard retention tiers:\n"
                "- Hot storage (0–90 days): Full granularity in Snowflake, fast query access\n"
                "- Warm storage (90 days–2 years): Compressed Parquet in S3, queryable via Athena\n"
                "- Cold archive (2–7 years): Glacier Deep Archive, retrieval within 12 hours\n"
                "- Deletion (>7 years): Automated purge unless regulatory hold applies\n\n"
                "GDPR right-to-erasure requests must be processed within 30 days. Maintain a "
                "deletion audit log for compliance verification."
            ),
        },
        {
            "title": "Hands-On Exercise",
            "subtitle": "Lab 1: Building Your First Pipeline",
            "body": (
                "In this lab, you will build a batch ingestion pipeline that:\n\n"
                "1. Reads CSV files from an S3 landing zone (s3://meridian-raw/sales/)\n"
                "2. Validates schema using Great Expectations\n"
                "3. Transforms and enriches records with dbt models\n"
                "4. Loads results into the analytics warehouse (Snowflake)\n"
                "5. Triggers a Grafana alert if row count drops below threshold\n\n"
                "Estimated time: 45 minutes\n\n"
                "Starter code is available in the workshop Git repository under /labs/lab01/. "
                "Clone the repo and follow the README instructions."
            ),
        },
        {
            "title": "Hands-On Exercise",
            "subtitle": "Lab 2: Streaming Pipeline with Kafka",
            "body": (
                "Lab 2 extends the batch pipeline with a real-time streaming component.\n\n"
                "Objectives:\n"
                "- Configure a Kafka producer that emits simulated clickstream events\n"
                "- Build a Flink SQL job that aggregates events into 5-minute windows\n"
                "- Write windowed results to a Redis cache for low-latency dashboard queries\n"
                "- Set up a Monte Carlo monitor on the streaming output table\n\n"
                "Estimated time: 60 minutes\n\n"
                "Note: The Kafka cluster is shared. Use your assigned topic prefix (your-name-*) "
                "to avoid collisions with other workshop participants."
            ),
        },
        {
            "title": "Workshop Summary and Next Steps",
            "subtitle": "Thank You for Attending",
            "body": (
                "Key takeaways from today's workshop:\n\n"
                "- Data pipelines have three stages: ingestion, transformation, delivery\n"
                "- Idempotency and schema validation prevent costly downstream errors\n"
                "- Automated quality monitoring catches issues before stakeholders do\n"
                "- Governance and access control are non-negotiable in production systems\n\n"
                "Next steps:\n"
                "- Complete Lab 2 if you haven't finished during the session\n"
                "- Review the supplementary materials in Confluence (search 'DA Workshop 2025')\n"
                "- Sign up for Module 4: Advanced ML Feature Engineering (June 10–11)\n\n"
                "Questions? Contact the Data Platform team at data-platform@meridian-corp.com "
                "or via the #data-help Slack channel."
            ),
        },
    ]

    for i, content in enumerate(pages_content):
        page = doc.new_page(width=W, height=H)

        # Title
        page.insert_text(
            pymupdf.Point(72, 80),
            content["title"],
            fontsize=22,
            fontname="hebo",
            color=(0.1, 0.2, 0.5),
        )

        # Subtitle
        page.insert_text(
            pymupdf.Point(72, 110),
            content["subtitle"],
            fontsize=14,
            fontname="heit",
            color=(0.3, 0.3, 0.3),
        )

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 125), pymupdf.Point(540, 125))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()

        # Body text
        body_rect = pymupdf.Rect(72, 145, 540, 720)
        page.insert_textbox(
            body_rect,
            content["body"],
            fontsize=11,
            fontname="tiro",
            color=(0, 0, 0),
            align=0,  # left-aligned
        )

        # Page number footer
        page.insert_text(
            pymupdf.Point(290, 760),
            f"— {i + 1} —",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Header: company name
        page.insert_text(
            pymupdf.Point(72, 40),
            "Meridian Corp — Internal Training",
            fontsize=8,
            fontname="helv",
            color=(0.6, 0.6, 0.6),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 12')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
