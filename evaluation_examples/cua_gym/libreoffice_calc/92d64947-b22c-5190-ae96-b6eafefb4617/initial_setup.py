"""
Initial Setup: Set up Thunderbird Inbox with 5 emails from reports@analytics.com
Task ID: osworld_multi_apps_email_file_convert_006
Domain: multi_apps (Thunderbird + OS file operations + LibreOffice Calc)

Initial state:
- Thunderbird Inbox has 5 emails from reports@analytics.com (within past 30 days)
- Attachments: 3 PDFs and 2 .ods spreadsheet files
- /home/user/analytics_files/ does NOT exist (agent must create it)
- /home/user/analytics_index.ods does NOT exist
- Thunderbird is open showing the Inbox
"""

import os
import shlex
import subprocess
import time
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mailbox
import io
import zipfile
import shutil
import configparser

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_file_convert_006'


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


def create_minimal_pdf_bytes(title: str, content_lines: list) -> bytes:
    """Create a minimal but valid PDF as bytes."""
    # Minimal PDF structure with text content
    lines_text = ""
    y = 700
    for line in content_lines:
        escaped = line.replace('(', r'\(').replace(')', r'\)')
        lines_text += f"BT /F1 12 Tf 72 {y} Td ({escaped}) Tj ET\n"
        y -= 20

    content_stream = f"""/Title ({title})
BT /F1 18 Tf 72 750 Td ({title}) Tj ET
{lines_text}"""
    stream_bytes = content_stream.encode('latin-1')
    stream_len = len(stream_bytes)

    pdf_parts = []
    offsets = []

    header = b"%PDF-1.4\n"
    pdf_parts.append(header)
    current_offset = len(header)

    # Object 1: Catalog
    obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    offsets.append(current_offset)
    pdf_parts.append(obj1)
    current_offset += len(obj1)

    # Object 2: Pages
    obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    offsets.append(current_offset)
    pdf_parts.append(obj2)
    current_offset += len(obj2)

    # Object 3: Page
    obj3 = b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    offsets.append(current_offset)
    pdf_parts.append(obj3)
    current_offset += len(obj3)

    # Object 4: Content stream
    stream_header = f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode('latin-1')
    stream_footer = b"\nendstream\nendobj\n"
    offsets.append(current_offset)
    pdf_parts.append(stream_header + stream_bytes + stream_footer)
    current_offset += len(stream_header) + stream_len + len(stream_footer)

    # Object 5: Font
    obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    offsets.append(current_offset)
    pdf_parts.append(obj5)
    current_offset += len(obj5)

    # Cross-reference table
    xref_offset = current_offset
    xref = f"xref\n0 6\n0000000000 65535 f \n"
    for off in offsets:
        xref += f"{off:010d} 00000 n \n"

    trailer = f"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n"

    pdf_parts.append(xref.encode('latin-1'))
    pdf_parts.append(trailer.encode('latin-1'))

    return b"".join(pdf_parts)


def create_ods_bytes(sheet_title: str, headers: list, data_rows: list) -> bytes:
    """Create a minimal valid ODS (OpenDocument Spreadsheet) as bytes."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype - must be first, uncompressed
        zf.writestr(
            zipfile.ZipInfo('mimetype'),
            'application/vnd.oasis.opendocument.spreadsheet',
            compress_type=zipfile.ZIP_STORED
        )

        # meta.xml
        meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    office:version="1.3">
  <office:meta>
    <meta:initial-creator>Analytics Team</meta:initial-creator>
    <meta:creation-date>2026-02-15T10:00:00</meta:creation-date>
  </office:meta>
</office:document-meta>'''
        zf.writestr('meta.xml', meta_xml)

        # settings.xml
        settings_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-settings xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    office:version="1.3">
  <office:settings/>
</office:document-settings>'''
        zf.writestr('settings.xml', settings_xml)

        # styles.xml
        styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.3">
  <office:styles/>
  <office:automatic-styles/>
  <office:master-styles/>
</office:document-styles>'''
        zf.writestr('styles.xml', styles_xml)

        # Build content.xml with table rows
        def make_cell(value):
            val_str = str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            return f'<table:table-cell office:value-type="string"><text:p>{val_str}</text:p></table:table-cell>'

        rows_xml = ''
        # Header row
        header_cells = ''.join(make_cell(h) for h in headers)
        rows_xml += f'<table:table-row>{header_cells}</table:table-row>\n'
        # Data rows
        for row in data_rows:
            data_cells = ''.join(make_cell(v) for v in row)
            rows_xml += f'<table:table-row>{data_cells}</table:table-row>\n'

        content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.3">
  <office:automatic-styles/>
  <office:body>
    <office:spreadsheet>
      <table:table table:name="{sheet_title}">
        {rows_xml}
      </table:table>
    </office:spreadsheet>
  </office:body>
</office:document-content>'''
        zf.writestr('content.xml', content_xml)

        # manifest.xml
        manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
    manifest:version="1.3">
  <manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.spreadsheet"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="settings.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''
        zf.writestr('META-INF/manifest.xml', manifest_xml)

    buf.seek(0)
    return buf.read()


def create_email_with_attachment(from_addr, to_addr, subject, body,
                                  attachment_filename, attachment_bytes,
                                  mime_type, date_str):
    """Create a MIME email with a single attachment."""
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg['Date'] = date_str
    msg['Message-ID'] = f'<analytics-{abs(hash(subject)) % 10**10}@analytics.com>'

    msg.attach(MIMEText(body, 'plain'))

    maintype, subtype = mime_type.split('/', 1)
    part = MIMEBase(maintype, subtype)
    part.set_payload(attachment_bytes)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
    msg.attach(part)

    return msg


def get_thunderbird_profile_dir():
    """Find the Thunderbird default-release profile directory."""
    tb_base = os.path.expanduser('~/.thunderbird')

    if not os.path.exists(tb_base):
        os.makedirs(tb_base, exist_ok=True)

    profiles_ini = os.path.join(tb_base, 'profiles.ini')
    profile_dir = None

    if os.path.exists(profiles_ini):
        config = configparser.ConfigParser()
        config.read(profiles_ini)
        for section in config.sections():
            if section.startswith('Profile'):
                path_val = config.get(section, 'Path', fallback=None)
                is_relative = config.get(section, 'IsRelative', fallback='0')
                if path_val:
                    if is_relative == '1':
                        candidate = os.path.join(tb_base, path_val)
                    else:
                        candidate = path_val
                    if os.path.isdir(candidate):
                        profile_dir = candidate
                        break

    if not profile_dir:
        # Fallback: find any .default-release dir
        for entry in os.listdir(tb_base):
            candidate = os.path.join(tb_base, entry)
            if os.path.isdir(candidate) and ('default' in entry):
                profile_dir = candidate
                break

    if not profile_dir:
        # Create a new profile
        profile_dir = os.path.join(tb_base, 'analytics.default')
        os.makedirs(profile_dir, exist_ok=True)
        with open(profiles_ini, 'w') as f:
            f.write('[General]\nStartWithLastProfile=1\nVersion=2\n\n'
                    '[Profile0]\nName=default\nIsRelative=1\nPath=analytics.default\nDefault=1\n')

    return profile_dir


# Define 5 emails with dates within past 30 days from 2026-03-06
# Dates range: 2026-02-10 to 2026-03-04
EMAILS_DATA = [
    {
        'date_str': 'Tue, 10 Feb 2026 09:15:00 +0000',
        'date_prefix': '20260210',
        'subject': 'Q4 2025 Revenue Summary Report',
        'body': '''Dear Team,

Please find attached the Q4 2025 Revenue Summary Report in PDF format.
This report covers all revenue streams for the fourth quarter of fiscal year 2025.

Key highlights:
- Total revenue: $4.2M (up 12% YoY)
- Top performing region: North America
- New client acquisitions: 47

Please review and reach out with any questions.

Best regards,
Analytics Team
reports@analytics.com''',
        'filename': 'q4_2025_revenue_summary.pdf',
        'mime_type': 'application/pdf',
        'type': 'PDF',
        'pdf_content': [
            'Q4 2025 Revenue Summary',
            'Period: October - December 2025',
            '',
            'Revenue Breakdown by Region:',
            'North America:    $1,850,000',
            'Europe:           $1,120,000',
            'Asia Pacific:       $780,000',
            'Latin America:      $350,000',
            'Middle East:        $100,000',
            '',
            'Total Revenue:    $4,200,000',
            'YoY Growth:       +12.3%',
            '',
            'Client Metrics:',
            'New Clients:      47',
            'Retained Clients: 312',
            'Churn Rate:       2.1%',
        ]
    },
    {
        'date_str': 'Mon, 17 Feb 2026 14:30:00 +0000',
        'date_prefix': '20260217',
        'subject': 'January 2026 Web Traffic Analytics',
        'body': '''Hi,

Attached is the January 2026 Web Traffic Analytics spreadsheet.
This file contains daily traffic data, conversion rates, and source breakdown.

Summary:
- Total sessions: 2.4M
- Bounce rate: 38.2%
- Top traffic source: Organic Search (54%)

Best,
Analytics Team''',
        'filename': 'jan_2026_web_traffic.ods',
        'mime_type': 'application/vnd.oasis.opendocument.spreadsheet',
        'type': 'ODS',
        'headers': ['Date', 'Sessions', 'Users', 'Bounce_Rate', 'Avg_Session_Duration', 'Source'],
        'data_rows': [
            ['2026-01-01', '72450', '58320', '37.8%', '3m 24s', 'Organic'],
            ['2026-01-02', '68900', '55120', '38.1%', '3m 18s', 'Organic'],
            ['2026-01-03', '71200', '57340', '37.5%', '3m 31s', 'Direct'],
            ['2026-01-04', '79800', '64200', '36.9%', '3m 45s', 'Paid Search'],
            ['2026-01-05', '83200', '67100', '36.2%', '4m 02s', 'Social'],
            ['2026-01-06', '76500', '61430', '38.4%', '3m 28s', 'Email'],
            ['2026-01-07', '69100', '55700', '39.1%', '3m 15s', 'Organic'],
            ['2026-01-08', '74300', '59800', '37.6%', '3m 38s', 'Organic'],
            ['2026-01-09', '77800', '62500', '37.0%', '3m 52s', 'Referral'],
            ['2026-01-10', '80100', '64300', '36.5%', '4m 01s', 'Paid Search'],
            ['2026-01-11', '84600', '68200', '35.8%', '4m 12s', 'Social'],
            ['2026-01-12', '78900', '63400', '37.2%', '3m 44s', 'Organic'],
        ]
    },
    {
        'date_str': 'Wed, 19 Feb 2026 11:00:00 +0000',
        'date_prefix': '20260219',
        'subject': 'February 2026 Marketing Campaign Performance',
        'body': '''Hello,

Please find the attached PDF report on February 2026 Marketing Campaign Performance.
This covers all active campaigns, spend, ROI, and conversion data.

Key findings:
- Email campaign achieved 24% open rate
- Paid search ROAS: 4.2x
- Top converting landing page: /product-demo

Regards,
Analytics Team
reports@analytics.com''',
        'filename': 'feb_2026_marketing_campaign.pdf',
        'mime_type': 'application/pdf',
        'type': 'PDF',
        'pdf_content': [
            'February 2026 Marketing Campaign Report',
            'Period: February 1-19, 2026',
            '',
            'Campaign Overview:',
            'Total Campaigns Active:   8',
            'Total Budget Spent:       $125,400',
            'Total Conversions:        3,842',
            'Average CPA:              $32.64',
            '',
            'Email Marketing:',
            'Emails Sent:              48,000',
            'Open Rate:                24.3%',
            'Click Rate:               5.8%',
            'Conversions:              1,245',
            '',
            'Paid Search (Google Ads):',
            'Total Spend:              $45,200',
            'Clicks:                   12,400',
            'Conversions:              1,890',
            'ROAS:                     4.2x',
            '',
            'Social Media Ads:',
            'Total Spend:              $28,600',
            'Impressions:              2.1M',
            'Conversions:              707',
        ]
    },
    {
        'date_str': 'Fri, 28 Feb 2026 16:45:00 +0000',
        'date_prefix': '20260228',
        'subject': 'Customer Retention Analysis Q1 2026',
        'body': '''Hi Team,

Attached is the Q1 2026 Customer Retention Analysis spreadsheet.
This dataset includes customer cohort data, retention rates, and LTV calculations.

Highlights:
- 90-day retention: 68.4%
- Average LTV: $1,240
- Highest retention cohort: Enterprise (84.2%)

Best,
Analytics Team''',
        'filename': 'customer_retention_q1_2026.ods',
        'mime_type': 'application/vnd.oasis.opendocument.spreadsheet',
        'type': 'ODS',
        'headers': ['Customer_ID', 'Segment', 'Cohort_Month', 'Days_Since_Signup',
                    'Retained_30d', 'Retained_90d', 'LTV_USD'],
        'data_rows': [
            ['C-10421', 'Enterprise', '2025-10', '120', 'Yes', 'Yes', '2850.00'],
            ['C-10422', 'SMB', '2025-10', '120', 'Yes', 'Yes', '890.00'],
            ['C-10423', 'Startup', '2025-10', '120', 'Yes', 'No', '340.00'],
            ['C-10424', 'Enterprise', '2025-11', '90', 'Yes', 'Yes', '3100.00'],
            ['C-10425', 'SMB', '2025-11', '90', 'Yes', 'Yes', '1120.00'],
            ['C-10426', 'Startup', '2025-11', '90', 'No', 'No', '150.00'],
            ['C-10427', 'Enterprise', '2025-11', '90', 'Yes', 'Yes', '2740.00'],
            ['C-10428', 'SMB', '2025-12', '60', 'Yes', 'Yes', '980.00'],
            ['C-10429', 'Startup', '2025-12', '60', 'Yes', 'No', '280.00'],
            ['C-10430', 'Enterprise', '2025-12', '60', 'Yes', 'Yes', '3450.00'],
            ['C-10431', 'SMB', '2026-01', '30', 'Yes', 'N/A', '420.00'],
            ['C-10432', 'Startup', '2026-01', '30', 'No', 'N/A', '0.00'],
        ]
    },
    {
        'date_str': 'Wed, 04 Mar 2026 10:20:00 +0000',
        'date_prefix': '20260304',
        'subject': 'March 2026 Executive Dashboard Report',
        'body': '''Dear Stakeholders,

Please find attached the March 2026 Executive Dashboard PDF.
This report contains KPI summaries, trend analysis, and forecasts for Q1 2026.

Dashboard Highlights:
- MRR reached $890K (record high)
- NPS score: 72 (up from 68 last quarter)
- Support ticket resolution time: 4.2 hours avg

Best regards,
Analytics Team
reports@analytics.com''',
        'filename': 'march_2026_executive_dashboard.pdf',
        'mime_type': 'application/pdf',
        'type': 'PDF',
        'pdf_content': [
            'March 2026 Executive Dashboard',
            'Period: March 1-4, 2026 (Week 1)',
            '',
            'Key Performance Indicators:',
            'Monthly Recurring Revenue (MRR):  $890,000',
            'Annual Recurring Revenue (ARR):   $10.68M',
            'Total Active Customers:           1,847',
            'Net Promoter Score (NPS):         72',
            '',
            'Growth Metrics:',
            'MRR Growth (MoM):                 +8.5%',
            'New MRR (New Customers):          $78,400',
            'Expansion MRR (Upsells):          $42,100',
            'Churned MRR:                      -$15,200',
            '',
            'Operational KPIs:',
            'Avg Support Resolution Time:      4.2 hours',
            'First Response Time:              45 minutes',
            'Customer Satisfaction Score:      4.6/5.0',
            'Active Trials (Conversion track): 234',
        ]
    },
]


def setup_thunderbird_inbox():
    """Set up Thunderbird Local Folders Inbox with 5 emails."""
    profile_dir = get_thunderbird_profile_dir()
    print(f"Using Thunderbird profile: {profile_dir}")

    mail_dir = os.path.join(profile_dir, 'Mail', 'Local Folders')
    os.makedirs(mail_dir, exist_ok=True)

    inbox_path = os.path.join(mail_dir, 'Inbox')

    # Clear existing Inbox
    if os.path.exists(inbox_path):
        os.remove(inbox_path)
    inbox_msf = inbox_path + '.msf'
    if os.path.exists(inbox_msf):
        os.remove(inbox_msf)

    # Build mbox content with all 5 emails
    mbox_content = ''
    for edata in EMAILS_DATA:
        # Create attachment bytes
        if edata['type'] == 'PDF':
            attach_bytes = create_minimal_pdf_bytes(
                edata['subject'],
                edata.get('pdf_content', [edata['subject']])
            )
        else:  # ODS
            attach_bytes = create_ods_bytes(
                edata['filename'].replace('.ods', '').replace('_', ' ').title(),
                edata['headers'],
                edata['data_rows']
            )

        msg = create_email_with_attachment(
            from_addr='Analytics Reports <reports@analytics.com>',
            to_addr='user@localhost',
            subject=edata['subject'],
            body=edata['body'],
            attachment_filename=edata['filename'],
            attachment_bytes=attach_bytes,
            mime_type=edata['mime_type'],
            date_str=edata['date_str']
        )

        msg_str = msg.as_string()
        # mbox format: each message starts with "From " separator line
        mbox_content += f"From reports@analytics.com {edata['date_str']}\n"
        mbox_content += msg_str
        mbox_content += '\n\n'

    # Write Inbox mbox file
    with open(inbox_path, 'w') as f:
        f.write(mbox_content)

    # Create empty .msf index file (Thunderbird summary file — empty forces re-index)
    with open(inbox_msf, 'w') as f:
        f.write('// <!-- <mdb:mork:z v="1.4"/> -->\n')

    print(f"Inbox mbox created: {inbox_path}")
    print(f"  Contains {len(EMAILS_DATA)} emails from reports@analytics.com")
    for edata in EMAILS_DATA:
        print(f"  - [{edata['date_prefix']}] {edata['subject']} ({edata['filename']})")


def create_initial():
    """Create the initial state for the task."""

    # 1. Remove target directories if they exist (should not be present initially)
    analytics_dir = os.path.join(WORKDIR, 'analytics_files')
    if os.path.exists(analytics_dir):
        shutil.rmtree(analytics_dir)
        print(f"Removed pre-existing analytics_files directory: {analytics_dir}")

    # 2. Remove analytics_index.ods if it exists
    index_ods = os.path.join(WORKDIR, 'analytics_index.ods')
    if os.path.exists(index_ods):
        os.remove(index_ods)
        print(f"Removed pre-existing analytics_index.ods")

    # 3. Set up Thunderbird Inbox with 5 emails from reports@analytics.com
    setup_thunderbird_inbox()

    # 4. Kill any existing Thunderbird instance and relaunch
    subprocess.run(['pkill', '-f', 'thunderbird'], capture_output=True)
    time.sleep(1.5)

    # 5. Launch Thunderbird to show the Inbox
    launch_gui('thunderbird', delay_sec=3.0)

    print('\nInitial state created successfully:')
    print(f'  Thunderbird Inbox: 5 emails from reports@analytics.com')
    print(f'  Attachments: 3 PDFs + 2 ODS spreadsheets')
    print(f'  /home/user/analytics_files/ does NOT exist (agent must create)')
    print(f'  /home/user/analytics_index.ods does NOT exist (agent must create)')
    print('GUI_READY: launched Thunderbird with DISPLAY=:0')


create_initial()
