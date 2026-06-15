"""
Initial Setup: Create a 15-page user guide PDF with ~12 embedded images
Task ID: pdf_pw_048
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import struct
import zlib

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_048'
PUBLISH_DIR = f'{WORKDIR}/publishing'
OUTPUT = f'{PUBLISH_DIR}/accessible_guide.pdf'


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


def create_simple_png(width, height, color_rgb, label=""):
    """Create a simple solid-color PNG image in memory with optional label-like variation."""
    import io

    r, g, b = color_rgb
    # Create raw pixel data (RGB rows with filter byte)
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # filter byte: None
        for x in range(width):
            # Add slight gradient for visual interest
            rr = min(255, r + (x * 20 // width))
            gg = min(255, g + (y * 20 // height))
            bb = b
            raw_data += struct.pack('BBB', rr, gg, bb)

    # PNG construction
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(chunk) & 0xFFFFFFFF)
        return struct.pack('>I', len(data)) + chunk + crc

    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = make_chunk(b'IHDR', ihdr_data)
    compressed = zlib.compress(raw_data)
    idat = make_chunk(b'IDAT', compressed)
    iend = make_chunk(b'IEND', b'')

    return signature + ihdr + idat + iend


def create_initial():
    os.makedirs(PUBLISH_DIR, exist_ok=True)

    doc = pymupdf.open()
    W, H = 612, 792  # Letter size

    # Define guide content structure
    guide_title = "DataVault Analytics Platform"
    guide_subtitle = "User Guide v3.2"

    # Generate distinct images for embedding
    image_specs = [
        (320, 200, (41, 98, 163), "Dashboard Overview Screenshot"),
        (280, 180, (76, 153, 76), "Navigation Panel Diagram"),
        (250, 160, (163, 73, 41), "Alert Configuration Icon"),
        (300, 190, (120, 60, 150), "Report Builder Interface"),
        (260, 170, (60, 130, 130), "Data Import Wizard"),
        (280, 200, (170, 130, 40), "Chart Editor Screenshot"),
        (320, 180, (50, 80, 140), "User Permissions Matrix"),
        (240, 160, (140, 50, 80), "API Integration Diagram"),
        (300, 200, (80, 120, 60), "Scheduling Console"),
        (280, 170, (100, 100, 160), "Export Settings Panel"),
        (260, 190, (150, 100, 50), "Collaboration Features"),
        (300, 180, (60, 100, 120), "Mobile View Screenshot"),
    ]

    images_data = []
    for w, h, color, label in image_specs:
        images_data.append(create_simple_png(w, h, color, label))

    img_index = 0

    # --- Page 1: Title Page ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(W/2 - 160, 200), guide_title, fontsize=28, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_text(pymupdf.Point(W/2 - 80, 250), guide_subtitle, fontsize=18, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(W/2 - 100, 310), "Prepared by DataVault Inc.", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(W/2 - 70, 340), "March 2025 Edition", fontsize=12, fontname="heit", color=(0.5, 0.5, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(100, 270), pymupdf.Point(W - 100, 270))
    shape.finish(color=(0.16, 0.38, 0.64), width=2)
    shape.commit()

    # --- Page 2: Table of Contents ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "Table of Contents", fontsize=22, fontname="hebo", color=(0.16, 0.38, 0.64))
    toc_items = [
        "1. Getting Started .......................... 3",
        "2. Dashboard Overview ...................... 4",
        "3. Navigation and Layout ................... 5",
        "4. Alert Configuration ..................... 6",
        "5. Report Builder .......................... 7",
        "6. Data Import and Export .................. 8",
        "7. Chart Editor ............................ 9",
        "8. User Permissions ........................ 10",
        "9. API Integration ......................... 11",
        "10. Scheduling Tasks ....................... 12",
        "11. Collaboration Features ................. 13",
        "12. Mobile Access .......................... 14",
        "13. Troubleshooting ........................ 15",
    ]
    y = 120
    for item in toc_items:
        page.insert_text(pymupdf.Point(90, y), item, fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
        y += 28

    # --- Page 3: Getting Started ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "1. Getting Started", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    getting_started_text = (
        "Welcome to DataVault Analytics Platform. This guide will walk you through "
        "the key features and functionalities of the platform. DataVault provides "
        "enterprise-grade analytics with real-time data processing, customizable "
        "dashboards, and advanced reporting capabilities.\n\n"
        "To begin, log in to your DataVault account at https://app.datavault.io "
        "using your corporate credentials. First-time users should complete the "
        "onboarding wizard which will configure your default workspace settings, "
        "connect to your primary data sources, and set up notification preferences.\n\n"
        "System Requirements:\n"
        "- Modern web browser (Chrome 90+, Firefox 88+, Edge 90+, Safari 14+)\n"
        "- Minimum screen resolution: 1280 x 720\n"
        "- Stable internet connection (minimum 5 Mbps)\n"
        "- JavaScript enabled"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 500), getting_started_text,
                        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 4: Dashboard Overview (Image 1) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "2. Dashboard Overview", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 180),
        "The main dashboard provides a comprehensive view of your key performance "
        "indicators and recent activity. Widgets can be rearranged by dragging, and "
        "each widget supports drill-down functionality for deeper analysis.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    # Image 1: Dashboard screenshot
    img_rect = pymupdf.Rect(146, 200, 466, 400)
    page.insert_image(img_rect, stream=images_data[0])
    page.insert_textbox(pymupdf.Rect(72, 420, 540, 560),
        "The dashboard displays real-time metrics including total revenue ($2.4M this quarter), "
        "active user count (15,832), conversion rate (3.7%), and server uptime (99.97%). "
        "Use the date range selector in the top-right corner to adjust the reporting period. "
        "Click any metric card to view its detailed trend chart.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    img_index = 1

    # --- Page 5: Navigation (Image 2) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "3. Navigation and Layout", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 170),
        "The navigation panel on the left side provides quick access to all major "
        "sections of the platform. It can be collapsed for more workspace area.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    img_rect = pymupdf.Rect(166, 185, 446, 365)
    page.insert_image(img_rect, stream=images_data[1])
    page.insert_textbox(pymupdf.Rect(72, 380, 540, 520),
        "The sidebar navigation includes sections for Dashboard, Reports, Data Sources, "
        "Alerts, Settings, and Help. Each section expands to show sub-items. The search "
        "bar at the top of the navigation allows quick access to any feature. You can "
        "customize the order of navigation items in Settings > Interface > Navigation.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 6: Alert Configuration (Image 3) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "4. Alert Configuration", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 180),
        "DataVault allows you to configure custom alerts based on metric thresholds, "
        "anomaly detection, or scheduled conditions. Alerts can be delivered via email, "
        "Slack, Microsoft Teams, or webhook.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    img_rect = pymupdf.Rect(176, 195, 426, 355)
    page.insert_image(img_rect, stream=images_data[2])
    page.insert_textbox(pymupdf.Rect(72, 370, 540, 530),
        "To create a new alert, navigate to Alerts > Create New. Specify the metric "
        "to monitor, set the threshold condition (above, below, or percentage change), "
        "and choose the notification channel. You can also set quiet hours during which "
        "non-critical alerts will be suppressed. Alert history is available under "
        "Alerts > History for the past 90 days.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 7: Report Builder (Image 4) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "5. Report Builder", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 170),
        "The Report Builder enables you to create custom analytical reports "
        "with drag-and-drop components, SQL queries, and template-based layouts.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    img_rect = pymupdf.Rect(156, 185, 456, 375)
    page.insert_image(img_rect, stream=images_data[3])
    page.insert_textbox(pymupdf.Rect(72, 390, 540, 560),
        "Reports support multiple visualization types including bar charts, line graphs, "
        "pie charts, scatter plots, and heat maps. Data can be filtered, grouped, and "
        "aggregated using the query panel. Completed reports can be scheduled for "
        "automatic delivery or exported in PDF, Excel, or CSV format. The template "
        "gallery contains over 50 pre-built report designs for common use cases.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 8: Data Import (Image 5) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "6. Data Import and Export", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 190),
        "DataVault supports importing data from multiple sources including CSV files, "
        "databases (PostgreSQL, MySQL, MongoDB), cloud storage (S3, GCS, Azure Blob), "
        "and third-party APIs (Salesforce, HubSpot, Stripe).",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    img_rect = pymupdf.Rect(176, 205, 436, 375)
    page.insert_image(img_rect, stream=images_data[4])
    page.insert_textbox(pymupdf.Rect(72, 390, 540, 550),
        "The Data Import Wizard guides you through connecting to your data source, "
        "mapping fields, setting data types, and configuring refresh schedules. "
        "Automated data validation checks for missing values, format inconsistencies, "
        "and duplicate records. Import jobs can be monitored in the Jobs queue.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 9: Chart Editor (Image 6) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "7. Chart Editor", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 170),
        "The Chart Editor provides an interactive canvas for creating and customizing "
        "data visualizations with real-time preview and formatting controls.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    img_rect = pymupdf.Rect(166, 185, 446, 385)
    page.insert_image(img_rect, stream=images_data[5])
    page.insert_textbox(pymupdf.Rect(72, 400, 540, 570),
        "Customize chart appearance including colors, labels, axes, legends, and "
        "gridlines. The editor supports conditional formatting where data points "
        "change color based on value thresholds. Charts can include trend lines, "
        "moving averages, and forecast projections. Interactive features like tooltips "
        "and click-through actions are configurable in the Interactivity panel.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 10: User Permissions (Image 7) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "8. User Permissions", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 180),
        "Role-based access control (RBAC) allows administrators to define granular "
        "permissions for each user role. DataVault provides predefined roles and "
        "supports custom role creation.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    img_rect = pymupdf.Rect(146, 195, 466, 375)
    page.insert_image(img_rect, stream=images_data[6])
    page.insert_textbox(pymupdf.Rect(72, 390, 540, 560),
        "The permission matrix shows access levels for each role across different "
        "features: View, Edit, Create, Delete, and Admin. Default roles include "
        "Viewer (read-only), Analyst (view + create reports), Editor (full content "
        "access), and Administrator (all permissions including user management). "
        "Audit logs track all permission changes for compliance purposes.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 11: API Integration (Image 8) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "9. API Integration", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 170),
        "DataVault offers a comprehensive REST API for programmatic access to all "
        "platform features. API keys can be generated in Settings > API.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    img_rect = pymupdf.Rect(186, 185, 426, 345)
    page.insert_image(img_rect, stream=images_data[7])
    page.insert_textbox(pymupdf.Rect(72, 360, 540, 550),
        "The API documentation includes endpoints for data queries, report generation, "
        "user management, and alert configuration. Rate limits are set at 1,000 "
        "requests per minute for standard plans and 10,000 for enterprise. "
        "SDKs are available for Python, JavaScript, Java, and Go. The integration "
        "diagram above shows the typical architecture for embedding DataVault "
        "analytics into external applications.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 12: Scheduling (Image 9) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "10. Scheduling Tasks", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 180),
        "Automate recurring operations such as data refreshes, report generation, "
        "and data exports using the Scheduling Console. Schedules support cron "
        "expressions and natural language time specifications.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    img_rect = pymupdf.Rect(156, 195, 456, 395)
    page.insert_image(img_rect, stream=images_data[8])
    page.insert_textbox(pymupdf.Rect(72, 410, 540, 560),
        "The scheduling console displays all active jobs with their frequency, "
        "last run status, and next scheduled execution. Failed jobs trigger "
        "automatic retry with configurable backoff. The calendar view shows "
        "scheduled tasks overlaid on a weekly or monthly timeline.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 13: Export Settings (Image 10) and Collaboration (Image 11) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "11. Collaboration Features", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 170),
        "DataVault supports real-time collaboration on reports and dashboards. "
        "Multiple team members can view and edit shared workspaces simultaneously.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    # Image 10: Export settings
    img_rect = pymupdf.Rect(72, 185, 352, 355)
    page.insert_image(img_rect, stream=images_data[9])
    page.insert_text(pymupdf.Point(72, 370), "Export Settings Panel", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))
    # Image 11: Collaboration
    img_rect = pymupdf.Rect(72, 400, 332, 590)
    page.insert_image(img_rect, stream=images_data[10])
    page.insert_text(pymupdf.Point(72, 605), "Team Collaboration Interface", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))
    page.insert_textbox(pymupdf.Rect(350, 400, 540, 600),
        "Shared workspaces include commenting, @mentions, and version history. "
        "Changes are tracked with full audit trails. Team leads can lock "
        "sections to prevent accidental edits during review periods.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 14: Mobile Access (Image 12) ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "12. Mobile Access", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 180),
        "Access your DataVault dashboards and reports from any mobile device "
        "using the responsive web interface or the dedicated iOS and Android apps.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))
    img_rect = pymupdf.Rect(156, 195, 456, 375)
    page.insert_image(img_rect, stream=images_data[11])
    page.insert_textbox(pymupdf.Rect(72, 390, 540, 560),
        "The mobile view automatically adapts dashboard layouts for smaller screens. "
        "Key features available on mobile include viewing dashboards, receiving push "
        "notifications for alerts, approving data access requests, and sharing reports "
        "via messaging apps. Offline mode caches recently viewed dashboards for "
        "access without internet connectivity.",
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # --- Page 15: Troubleshooting ---
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "13. Troubleshooting", fontsize=20, fontname="hebo", color=(0.16, 0.38, 0.64))
    troubleshooting_text = (
        "Common Issues and Solutions:\n\n"
        "Dashboard Not Loading:\n"
        "- Clear browser cache and cookies\n"
        "- Verify internet connection stability\n"
        "- Check if ad-blockers are interfering\n"
        "- Try incognito/private browsing mode\n\n"
        "Data Import Failures:\n"
        "- Verify source credentials are current\n"
        "- Check file format matches expected schema\n"
        "- Ensure file size is under 500MB limit\n"
        "- Review import logs for specific error codes\n\n"
        "Slow Report Generation:\n"
        "- Reduce date range or apply more filters\n"
        "- Optimize SQL queries (use EXPLAIN ANALYZE)\n"
        "- Consider pre-aggregating large datasets\n"
        "- Contact support for query optimization review\n\n"
        "Permission Denied Errors:\n"
        "- Confirm your role has required access level\n"
        "- Ask workspace admin to review permissions\n"
        "- Check if resource is in a restricted folder\n\n"
        "Contact Support:\n"
        "- Email: support@datavault.io\n"
        "- Live Chat: Available Mon-Fri 8AM-8PM EST\n"
        "- Phone: +1 (888) 555-DATA (3282)\n"
        "- Documentation: https://docs.datavault.io"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 700), troubleshooting_text,
                        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15))

    # Set TOC
    toc = [
        [1, "Getting Started", 3],
        [1, "Dashboard Overview", 4],
        [1, "Navigation and Layout", 5],
        [1, "Alert Configuration", 6],
        [1, "Report Builder", 7],
        [1, "Data Import and Export", 8],
        [1, "Chart Editor", 9],
        [1, "User Permissions", 10],
        [1, "API Integration", 11],
        [1, "Scheduling Tasks", 12],
        [1, "Collaboration Features", 13],
        [1, "Mobile Access", 14],
        [1, "Troubleshooting", 15],
    ]
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "DataVault Analytics Platform - User Guide",
        "author": "DataVault Documentation Team",
        "subject": "User Guide for DataVault Analytics Platform v3.2",
        "keywords": "analytics, dashboard, reporting, data, guide",
        "creator": "DataVault Inc.",
        "producer": "PyMuPDF",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 15')

    # Verify images
    verify_doc = pymupdf.open(OUTPUT)
    total_images = 0
    for i in range(verify_doc.page_count):
        imgs = verify_doc[i].get_images()
        if imgs:
            print(f'  Page {i+1}: {len(imgs)} image(s)')
            total_images += len(imgs)
    print(f'Total images: {total_images}')
    verify_doc.close()

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
