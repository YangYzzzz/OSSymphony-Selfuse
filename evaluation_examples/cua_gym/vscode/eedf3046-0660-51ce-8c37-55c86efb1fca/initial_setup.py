"""
Initial Setup: Move all three .txt files from docs/drafts/ into docs/final/
Task ID: vscode_file_013
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_013'
PROJECT_DIR = f'{WORKDIR}/project'


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
    docs_drafts = os.path.join(PROJECT_DIR, 'docs', 'drafts')
    docs_final = os.path.join(PROJECT_DIR, 'docs', 'final')
    src_dir = os.path.join(PROJECT_DIR, 'src')

    os.makedirs(docs_drafts, exist_ok=True)
    os.makedirs(docs_final, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)

    # Create report.txt
    report_content = """Quarterly Performance Report - Q1 2025
========================================

Executive Summary
-----------------
This report covers the operational performance for Q1 2025 across all
business units. Overall revenue grew by 12.4% compared to Q1 2024,
driven primarily by the expansion of the enterprise product line.

Key Metrics:
  - Total Revenue: $4.2M (up from $3.7M)
  - New Customers Acquired: 87
  - Customer Retention Rate: 94.2%
  - Net Promoter Score: 68

Department Highlights:
  Engineering shipped 3 major feature releases on schedule.
  Sales exceeded quarterly targets by 8.3%.
  Customer Success resolved 99.1% of tickets within SLA.

Recommendations:
  1. Increase hiring in the engineering department (2 senior backend roles).
  2. Expand marketing spend in Asia-Pacific by 15%.
  3. Continue investment in the self-service portal to reduce support load.

Prepared by: Sarah Chen, VP of Operations
Date: March 31, 2025
"""

    # Create summary.txt
    summary_content = """Project Alpha — Executive Summary
===================================

Project Overview
----------------
Project Alpha is a 6-month initiative to migrate the legacy data
pipeline from on-premise infrastructure to a cloud-native architecture
using Kubernetes and managed database services.

Scope:
  - Migrate 14 ETL jobs to Apache Airflow on GKE
  - Replace Oracle DB with Cloud Spanner for OLTP workloads
  - Implement real-time data streaming via Pub/Sub + Dataflow

Timeline:
  Phase 1 (Jan–Feb 2025): Infrastructure setup and test migration
  Phase 2 (Mar–Apr 2025): Parallel run — old and new systems
  Phase 3 (May–Jun 2025): Full cutover and decommission legacy systems

Budget: $320,000 approved
Current Spend: $187,500 (58.6% of budget)

Status: ON TRACK
Risk Level: MEDIUM — Spanner schema migration still in progress.

Primary Contact: Marcus Johnson, Tech Lead
Last Updated: 2025-03-28
"""

    # Create notes.txt
    notes_content = """Meeting Notes — Product Roadmap Review
========================================

Date: April 3, 2025
Attendees: Lisa Park, David Reyes, Anika Osei, Tom Nguyen, Sarah Chen

Agenda Items Discussed:
-----------------------

1. Q2 Feature Priorities
   - Dashboard redesign is the top priority; target launch May 15.
   - API rate-limiting feature pushed to Q3 due to dependency on
     auth service refactor.
   - Mobile app offline mode: design review scheduled for April 10.

2. Technical Debt
   - Agreed to allocate 20% of sprint capacity to debt reduction.
   - Top items: legacy session management, deprecated API v1 endpoints.

3. Customer Feedback Integration
   - Lisa will compile the top 10 feature requests from Zendesk by April 7.
   - Product team to triage and assign owners in next planning session.

4. Next Steps
   - David: finalize mobile offline mode requirements doc by April 8.
   - Anika: schedule API auth refactor kick-off with backend team.
   - Tom: share updated dashboard mockups in Slack by April 5.
   - Sarah: book exec review for Q2 roadmap — target April 14.

Next Meeting: April 10, 2025 at 2:00 PM PST
"""

    # Create main.py
    main_py_content = '''#!/usr/bin/env python3
"""
main.py — Entry point for the project data pipeline.

This module orchestrates the ETL workflow by loading configuration,
establishing database connections, and running the defined pipeline stages.
"""

import argparse
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run the project data pipeline.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/pipeline.yaml"),
        help="Path to the pipeline configuration file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without executing pipeline stages.",
    )
    parser.add_argument(
        "--stage",
        choices=["extract", "transform", "load", "all"],
        default="all",
        help="Pipeline stage to execute.",
    )
    return parser.parse_args()


def load_config(config_path: Path) -> dict:
    """Load and validate pipeline configuration from YAML file."""
    if not config_path.exists():
        logger.error("Config file not found: %s", config_path)
        sys.exit(1)

    try:
        import yaml  # type: ignore
        with config_path.open() as f:
            config = yaml.safe_load(f)
        logger.info("Loaded configuration from %s", config_path)
        return config
    except Exception as exc:
        logger.error("Failed to load config: %s", exc)
        sys.exit(1)


def run_pipeline(config: dict, stage: str, dry_run: bool) -> int:
    """Execute the specified pipeline stage(s)."""
    stages = ["extract", "transform", "load"] if stage == "all" else [stage]

    for s in stages:
        logger.info("Starting stage: %s", s)
        if dry_run:
            logger.info("[DRY-RUN] Skipping execution of stage: %s", s)
            continue
        # TODO: Implement actual stage handlers
        logger.info("Stage completed: %s", s)

    return 0


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    return run_pipeline(config, args.stage, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
'''

    # Write files
    with open(os.path.join(docs_drafts, 'report.txt'), 'w') as f:
        f.write(report_content)

    with open(os.path.join(docs_drafts, 'summary.txt'), 'w') as f:
        f.write(summary_content)

    with open(os.path.join(docs_drafts, 'notes.txt'), 'w') as f:
        f.write(notes_content)

    with open(os.path.join(src_dir, 'main.py'), 'w') as f:
        f.write(main_py_content)

    print(f'Project structure created at: {PROJECT_DIR}')
    print(f'  docs/drafts/ -> report.txt, summary.txt, notes.txt')
    print(f'  docs/final/  -> (empty)')
    print(f'  src/         -> main.py')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder on DISPLAY=:0')


create_initial()
