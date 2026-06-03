"""
Initial Setup: Event log JSON data in a LibreOffice Writer .odt document
Task ID: osworld_multi_apps_json_reformat_writer_011
Domain: libreoffice_writer

Creates /home/user/Documents/event_log.odt containing a raw JSON array of 20 event
log entries (10 INFO, 6 WARN, 4 ERROR) with nested metadata objects.
The agent must reformat this into a structured Writer document.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user/Documents'
TASK_ID = 'event_log'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odt'


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
    # Make sure the Documents folder exists
    os.makedirs(WORKDIR, exist_ok=True)

    # Define 20 realistic event log entries: 10 INFO, 6 WARN, 4 ERROR
    entries = [
        # --- INFO entries ---
        {
            "event_id": "EVT-001",
            "timestamp": "2025-03-15T08:02:11Z",
            "level": "INFO",
            "component": "AuthService",
            "message": "User 'alice.morgan' logged in successfully.",
            "metadata": {"session_id": "s-8f3k2a", "ip_address": "192.168.1.45"}
        },
        {
            "event_id": "EVT-002",
            "timestamp": "2025-03-15T08:05:33Z",
            "level": "INFO",
            "component": "DataPipeline",
            "message": "Batch job BJ-2203 completed. 1500 records processed.",
            "metadata": {"job_id": "BJ-2203", "duration_sec": 42, "records": 1500}
        },
        {
            "event_id": "EVT-003",
            "timestamp": "2025-03-15T08:11:47Z",
            "level": "INFO",
            "component": "NotificationService",
            "message": "Email digest sent to 342 subscribers.",
            "metadata": {"campaign_id": "CAMP-091", "sent_count": 342}
        },
        {
            "event_id": "EVT-004",
            "timestamp": "2025-03-15T08:18:05Z",
            "level": "INFO",
            "component": "AuthService",
            "message": "Password reset completed for user 'bob.chen'.",
            "metadata": {"user_id": "U-4471", "method": "email_link"}
        },
        {
            "event_id": "EVT-005",
            "timestamp": "2025-03-15T08:25:19Z",
            "level": "INFO",
            "component": "ReportGenerator",
            "message": "Monthly financial report generated successfully.",
            "metadata": {"report_id": "RPT-0315", "pages": 18, "format": "PDF"}
        },
        {
            "event_id": "EVT-006",
            "timestamp": "2025-03-15T08:33:44Z",
            "level": "INFO",
            "component": "DataPipeline",
            "message": "Incremental sync from CRM completed.",
            "metadata": {"sync_id": "SYNC-7712", "new_records": 87, "updated_records": 23}
        },
        {
            "event_id": "EVT-007",
            "timestamp": "2025-03-15T08:44:02Z",
            "level": "INFO",
            "component": "InventoryService",
            "message": "Stock replenishment order placed for SKU-9034.",
            "metadata": {"sku": "SKU-9034", "quantity": 500, "supplier": "Nexus Supply Co."}
        },
        {
            "event_id": "EVT-008",
            "timestamp": "2025-03-15T08:51:28Z",
            "level": "INFO",
            "component": "SchedulerService",
            "message": "Scheduled maintenance window started.",
            "metadata": {"window_id": "MW-114", "duration_min": 30}
        },
        {
            "event_id": "EVT-009",
            "timestamp": "2025-03-15T09:03:15Z",
            "level": "INFO",
            "component": "AuthService",
            "message": "API token refreshed for service account 'svc-analytics'.",
            "metadata": {"service_account": "svc-analytics", "token_expiry": "2025-04-15"}
        },
        {
            "event_id": "EVT-010",
            "timestamp": "2025-03-15T09:12:40Z",
            "level": "INFO",
            "component": "ReportGenerator",
            "message": "Weekly KPI dashboard published to stakeholders.",
            "metadata": {"dashboard_id": "DASH-0315W", "recipients": 15}
        },
        # --- WARN entries ---
        {
            "event_id": "EVT-011",
            "timestamp": "2025-03-15T09:22:07Z",
            "level": "WARN",
            "component": "DataPipeline",
            "message": "Batch job BJ-2204 took longer than expected (threshold: 60s).",
            "metadata": {"job_id": "BJ-2204", "duration_sec": 78, "threshold_sec": 60}
        },
        {
            "event_id": "EVT-012",
            "timestamp": "2025-03-15T09:35:55Z",
            "level": "WARN",
            "component": "InventoryService",
            "message": "Stock level for SKU-1122 below reorder threshold.",
            "metadata": {"sku": "SKU-1122", "current_stock": 12, "reorder_threshold": 50}
        },
        {
            "event_id": "EVT-013",
            "timestamp": "2025-03-15T09:48:33Z",
            "level": "WARN",
            "component": "AuthService",
            "message": "3 consecutive failed login attempts for user 'carol.white'.",
            "metadata": {"user_id": "U-3382", "attempts": 3, "ip_address": "203.0.113.7"}
        },
        {
            "event_id": "EVT-014",
            "timestamp": "2025-03-15T10:02:44Z",
            "level": "WARN",
            "component": "SchedulerService",
            "message": "Scheduled job CRON-047 missed its trigger window.",
            "metadata": {"job_name": "CRON-047", "expected_at": "2025-03-15T10:00:00Z", "delay_sec": 164}
        },
        {
            "event_id": "EVT-015",
            "timestamp": "2025-03-15T10:18:09Z",
            "level": "WARN",
            "component": "NotificationService",
            "message": "Email delivery rate dropped below 95% for campaign CAMP-092.",
            "metadata": {"campaign_id": "CAMP-092", "delivery_rate": 0.918, "threshold": 0.95}
        },
        {
            "event_id": "EVT-016",
            "timestamp": "2025-03-15T10:31:22Z",
            "level": "WARN",
            "component": "DataPipeline",
            "message": "Duplicate records detected in incoming feed from ERP system.",
            "metadata": {"feed_id": "FEED-ERP-03", "duplicate_count": 14, "total_records": 630}
        },
        # --- ERROR entries ---
        {
            "event_id": "EVT-017",
            "timestamp": "2025-03-15T10:47:58Z",
            "level": "ERROR",
            "component": "DataPipeline",
            "message": "Failed to connect to external data source. Connection refused.",
            "metadata": {
                "error_code": "CONN_REFUSED",
                "host": "feeds.external-vendor.com",
                "port": 5432,
                "retry_count": 3,
                "stack_trace": "ConnectionError at pipeline/connector.py:88"
            }
        },
        {
            "event_id": "EVT-018",
            "timestamp": "2025-03-15T11:04:13Z",
            "level": "ERROR",
            "component": "ReportGenerator",
            "message": "Report generation failed due to missing template file.",
            "metadata": {
                "error_code": "FILE_NOT_FOUND",
                "template_path": "/templates/monthly_finance.html",
                "affected_user": "david.torres",
                "retry_count": 1,
                "stack_trace": "FileNotFoundError at reports/generator.py:214"
            }
        },
        {
            "event_id": "EVT-019",
            "timestamp": "2025-03-15T11:22:37Z",
            "level": "ERROR",
            "component": "AuthService",
            "message": "Database query timed out during user authentication.",
            "metadata": {
                "error_code": "DB_TIMEOUT",
                "query_id": "QRY-88412",
                "timeout_ms": 5000,
                "affected_user": "emily.nakamura",
                "stack_trace": "TimeoutError at auth/db_handler.py:57"
            }
        },
        {
            "event_id": "EVT-020",
            "timestamp": "2025-03-15T11:45:02Z",
            "level": "ERROR",
            "component": "InventoryService",
            "message": "Failed to update stock count. Constraint violation in database.",
            "metadata": {
                "error_code": "DB_CONSTRAINT_VIOLATION",
                "sku": "SKU-5588",
                "attempted_value": -5,
                "affected_user": "system",
                "stack_trace": "IntegrityError at inventory/db.py:132"
            }
        },
    ]

    # Build the raw JSON text to embed in the ODT document
    json_text = json.dumps(entries, indent=2, ensure_ascii=False)

    # Use odfpy to create an ODT file containing only the raw JSON
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.text import P, Span

    doc = OpenDocumentText()

    # Define a monospace style for the JSON block
    mono_style = Style(name="MonoText", family="paragraph")
    mono_style.addElement(TextProperties(fontname="Courier New", fontsize="10pt"))
    mono_style.addElement(ParagraphProperties(marginleft="0in"))
    doc.automaticstyles.addElement(mono_style)

    # Add a heading paragraph
    heading_style = Style(name="HeadingText", family="paragraph")
    heading_style.addElement(TextProperties(fontname="Liberation Sans", fontsize="14pt", fontweight="bold"))
    doc.automaticstyles.addElement(heading_style)

    heading_para = P(stylename="HeadingText")
    heading_para.addText("Event Log Data (Raw JSON)")
    doc.text.addElement(heading_para)

    empty_para = P()
    doc.text.addElement(empty_para)

    # Split JSON into lines, each as a separate paragraph
    for line in json_text.split('\n'):
        p = P(stylename="MonoText")
        p.addText(line)
        doc.text.addElement(p)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open event_log.odt in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with event_log.odt and DISPLAY=:0')


create_initial()
