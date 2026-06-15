"""
Initial Setup: Create a 15-page draft manual PDF with blank separator pages at positions 4, 8, 12.
Task ID: pdf_pw_039
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_039'
OUTPUT = f'{WORKDIR}/Documents/draft_manual.pdf'

# Ensure Documents directory exists
os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)


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


# Content for the 12 real content pages
content_pages = [
    {
        "title": "Chapter 1: Introduction to the System",
        "body": (
            "This manual provides comprehensive guidance for operating the DataFlow Pro 3000 "
            "enterprise data management system. The system was developed by Meridian Technologies "
            "to streamline data processing workflows across departments.\n\n"
            "Key features include real-time data synchronization, automated backup scheduling, "
            "role-based access control, and advanced reporting capabilities. This manual covers "
            "installation, configuration, daily operations, and troubleshooting procedures.\n\n"
            "Before proceeding, ensure you have administrator credentials and network access "
            "to the central server at your facility."
        ),
    },
    {
        "title": "Chapter 2: System Requirements",
        "body": (
            "Minimum Hardware Requirements:\n"
            "- Processor: Intel Core i5 or AMD Ryzen 5 (8th generation or newer)\n"
            "- RAM: 16 GB DDR4\n"
            "- Storage: 256 GB SSD with at least 50 GB free space\n"
            "- Network: Gigabit Ethernet or Wi-Fi 6 adapter\n"
            "- Display: 1920x1080 resolution minimum\n\n"
            "Software Prerequisites:\n"
            "- Operating System: Windows 10/11 Pro, macOS 12+, or Ubuntu 22.04 LTS\n"
            "- Java Runtime Environment 17 or later\n"
            "- PostgreSQL 14 client libraries\n"
            "- Web browser: Chrome 100+, Firefox 100+, or Edge 100+"
        ),
    },
    {
        "title": "Chapter 3: Installation Procedure",
        "body": (
            "Step 1: Download the installer package from the internal repository at "
            "https://repo.meridiantech.internal/dataflow-pro/latest.\n\n"
            "Step 2: Verify the SHA-256 checksum of the downloaded file matches the value "
            "published on the release notes page.\n\n"
            "Step 3: Run the installer with elevated privileges. On Windows, right-click "
            "and select 'Run as Administrator'. On Linux, use sudo.\n\n"
            "Step 4: Follow the installation wizard. Select 'Standard Installation' for "
            "most deployments. Choose 'Custom Installation' only if you need to modify "
            "the default database port (5432) or installation directory.\n\n"
            "Step 5: After installation completes, restart your machine to ensure all "
            "system services are properly initialized."
        ),
    },
    # Content page index 3 (will be page 5 in the PDF after separator at page 4)
    {
        "title": "Chapter 4: Initial Configuration",
        "body": (
            "After installation, launch the DataFlow Pro Configuration Wizard from the "
            "Start Menu or Applications folder.\n\n"
            "Database Connection Setup:\n"
            "- Host: Enter the IP address or hostname of your PostgreSQL server\n"
            "- Port: 5432 (default) or your custom port\n"
            "- Database Name: dataflow_prod\n"
            "- Username: df_admin\n"
            "- Password: Use the credentials provided by your IT department\n\n"
            "Network Configuration:\n"
            "- API Endpoint: https://api.meridiantech.internal:8443\n"
            "- Proxy Settings: Configure if your network requires a proxy\n"
            "- SSL Certificate: Import the organization's root CA certificate"
        ),
    },
    {
        "title": "Chapter 5: User Management",
        "body": (
            "The system supports three user roles with distinct permission levels:\n\n"
            "Administrator: Full system access including user management, configuration "
            "changes, data import/export, and audit log review. Limited to 3 accounts "
            "per installation.\n\n"
            "Manager: Can create and modify data workflows, generate reports, approve "
            "data submissions, and view team activity logs. Cannot modify system "
            "configuration or manage administrator accounts.\n\n"
            "Operator: Can execute assigned workflows, enter data, and view their own "
            "activity history. Cannot create or modify workflow definitions.\n\n"
            "To create a new user account, navigate to Settings > User Management > "
            "Add User. Fill in the required fields and assign the appropriate role."
        ),
    },
    {
        "title": "Chapter 6: Data Import and Export",
        "body": (
            "Supported Import Formats:\n"
            "- CSV (comma-separated values) with UTF-8 encoding\n"
            "- Excel (.xlsx) files up to 100,000 rows\n"
            "- JSON files conforming to the DataFlow schema v2.1\n"
            "- XML files with the provided XSD validation schema\n\n"
            "Import Procedure:\n"
            "1. Navigate to Data > Import from the main menu\n"
            "2. Select the source file or drag and drop into the upload area\n"
            "3. Map source columns to DataFlow fields using the column mapper\n"
            "4. Preview the first 100 rows to verify mapping accuracy\n"
            "5. Click 'Start Import' and monitor progress in the task queue\n\n"
            "Export options include CSV, Excel, PDF report, and direct API streaming."
        ),
    },
    # Content page index 6 (will be page 9 in the PDF after separators at 4,8)
    {
        "title": "Chapter 7: Workflow Automation",
        "body": (
            "DataFlow Pro includes a visual workflow designer for creating automated "
            "data processing pipelines.\n\n"
            "Creating a New Workflow:\n"
            "1. Open the Workflow Designer from the Tools menu\n"
            "2. Drag processing nodes from the palette onto the canvas\n"
            "3. Connect nodes by drawing lines between output and input ports\n"
            "4. Configure each node by double-clicking and setting parameters\n"
            "5. Save and publish the workflow for execution\n\n"
            "Available Node Types:\n"
            "- Data Source: Read from database, file, or API\n"
            "- Transform: Filter, aggregate, join, pivot operations\n"
            "- Validation: Schema check, range check, duplicate detection\n"
            "- Output: Write to database, generate report, send notification"
        ),
    },
    {
        "title": "Chapter 8: Reporting and Analytics",
        "body": (
            "The built-in reporting engine supports both ad-hoc queries and scheduled "
            "report generation.\n\n"
            "Creating a Report:\n"
            "1. Navigate to Reports > New Report\n"
            "2. Select a data source or saved workflow output\n"
            "3. Choose visualization type: table, bar chart, line chart, or pie chart\n"
            "4. Apply filters and grouping as needed\n"
            "5. Save the report template for future use\n\n"
            "Scheduling Reports:\n"
            "- Daily reports are generated at 06:00 AM server time\n"
            "- Weekly summaries run every Monday at 07:00 AM\n"
            "- Monthly analytics are compiled on the 1st of each month\n"
            "- Custom schedules can be defined using cron expressions"
        ),
    },
    {
        "title": "Chapter 9: Backup and Recovery",
        "body": (
            "Regular backups are essential for data protection. DataFlow Pro supports "
            "three backup strategies:\n\n"
            "Full Backup: Creates a complete snapshot of all data and configuration. "
            "Recommended weekly. Average duration: 2-4 hours depending on data volume.\n\n"
            "Incremental Backup: Captures only changes since the last backup. "
            "Recommended daily. Typical duration: 15-45 minutes.\n\n"
            "Transaction Log Backup: Continuous logging of all data modifications. "
            "Enables point-in-time recovery. Recommended for mission-critical deployments.\n\n"
            "Recovery Procedure:\n"
            "1. Stop the DataFlow Pro service\n"
            "2. Launch the Recovery Tool from the installation directory\n"
            "3. Select the backup archive to restore from\n"
            "4. Choose full recovery or point-in-time recovery\n"
            "5. Verify data integrity after restoration completes"
        ),
    },
    # Content page index 9 (will be page 13 in the PDF after separators at 4,8,12)
    {
        "title": "Chapter 10: Security Best Practices",
        "body": (
            "Follow these security guidelines to protect your DataFlow Pro installation:\n\n"
            "Authentication:\n"
            "- Enforce strong passwords (minimum 12 characters, mixed case, numbers, symbols)\n"
            "- Enable two-factor authentication for all administrator accounts\n"
            "- Set session timeout to 30 minutes of inactivity\n"
            "- Lock accounts after 5 consecutive failed login attempts\n\n"
            "Network Security:\n"
            "- Use TLS 1.3 for all client-server communication\n"
            "- Restrict API access to approved IP ranges\n"
            "- Enable audit logging for all administrative actions\n"
            "- Regularly review access logs for suspicious activity"
        ),
    },
    {
        "title": "Chapter 11: Troubleshooting Guide",
        "body": (
            "Common Issues and Solutions:\n\n"
            "Issue: Cannot connect to database\n"
            "Solution: Verify PostgreSQL service is running. Check firewall rules for "
            "port 5432. Confirm credentials in the configuration file.\n\n"
            "Issue: Import fails with 'Schema mismatch' error\n"
            "Solution: Ensure the import file matches the expected schema version. "
            "Use the Schema Validator tool to identify mismatched columns.\n\n"
            "Issue: Report generation times out\n"
            "Solution: Reduce the date range or add filters to limit data volume. "
            "Check server memory usage and increase if below 80% utilization.\n\n"
            "Issue: Workflow execution stuck in 'Pending' state\n"
            "Solution: Restart the Workflow Engine service. Check the task queue for "
            "deadlocked processes. Review node logs for error messages."
        ),
    },
    {
        "title": "Chapter 12: Appendix and Reference",
        "body": (
            "Glossary of Terms:\n"
            "- ETL: Extract, Transform, Load - the process of moving data between systems\n"
            "- RBAC: Role-Based Access Control - permission model used by DataFlow Pro\n"
            "- SLA: Service Level Agreement - uptime and performance guarantees\n"
            "- API: Application Programming Interface - programmatic system access\n\n"
            "Contact Information:\n"
            "- Technical Support: support@meridiantech.com | +1-888-555-0142\n"
            "- Sales Inquiries: sales@meridiantech.com | +1-888-555-0199\n"
            "- Emergency Hotline (24/7): +1-888-555-0911\n\n"
            "Software Version: DataFlow Pro 3.2.1 (Build 20250315)\n"
            "Manual Revision: 4.0 | Last Updated: March 2025\n"
            "Copyright 2025 Meridian Technologies, Inc. All rights reserved."
        ),
    },
]


def create_initial():
    doc = pymupdf.open()

    content_idx = 0
    for page_num in range(1, 16):  # pages 1 through 15
        page = doc.new_page(width=595, height=842)  # A4

        if page_num in (4, 8, 12):
            # Blank separator page - no content at all
            continue
        else:
            # Content page
            cp = content_pages[content_idx]
            content_idx += 1

            # Title
            page.insert_text(
                pymupdf.Point(72, 72),
                cp["title"],
                fontsize=18,
                fontname="hebo",
                color=(0.1, 0.1, 0.4),
            )

            # Horizontal rule under title
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
            shape.finish(color=(0.3, 0.3, 0.6), width=1.5)
            shape.commit()

            # Body text in a textbox
            rect = pymupdf.Rect(72, 100, 523, 780)
            page.insert_textbox(
                rect,
                cp["body"],
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 15')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
