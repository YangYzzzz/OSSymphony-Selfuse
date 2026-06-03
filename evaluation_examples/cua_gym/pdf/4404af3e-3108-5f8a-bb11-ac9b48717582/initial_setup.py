"""
Initial Setup: Create a 22-page user guide PDF with 4 chapters, no TOC or bookmarks.
Task ID: pdf_gf2_030
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_030'
OUTPUT = f'{WORKDIR}/Documents/user_guide.pdf'

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


# Chapter definitions: (title, start_page_0indexed, num_pages, sections)
CHAPTERS = [
    {
        "title": "Getting Started",
        "start": 0,   # page 1 (0-indexed: 0)
        "pages": 5,   # pages 1-5
        "sections": [
            ("Welcome to the User Guide", [
                "Welcome to our comprehensive software platform. This guide will walk you through everything you need to know to get up and running quickly. Whether you are a first-time user or transitioning from another system, this documentation covers all the essential topics.",
                "Our platform is designed to streamline your workflow and improve productivity. It integrates seamlessly with existing tools and provides a modern, intuitive interface for managing your projects and teams.",
            ]),
            ("System Requirements", [
                "Before installing the software, ensure your system meets the following minimum requirements: a 64-bit operating system (Windows 10+, macOS 12+, or Ubuntu 20.04+), at least 8 GB of RAM, 2 GB of available disk space, and a stable internet connection for cloud-based features.",
                "For optimal performance, we recommend 16 GB of RAM and an SSD drive. The application also supports GPU acceleration for data visualization tasks if a compatible NVIDIA or AMD graphics card is installed.",
            ]),
            ("Installation Procedure", [
                "Download the installer from the official website at https://platform.example.com/downloads. Choose the appropriate version for your operating system. Run the installer and follow the on-screen prompts. The default installation directory is recommended for most users.",
                "After installation, launch the application and complete the initial configuration wizard. You will be asked to create an account or sign in with your existing credentials. The wizard will also guide you through connecting to your organization's workspace.",
            ]),
            ("First Steps After Installation", [
                "Once the software is installed, start by creating your first project. Navigate to the Dashboard and click 'New Project'. Enter a project name, select a template, and invite your team members. The project workspace will be created automatically.",
                "Explore the sidebar navigation to familiarize yourself with the main sections: Dashboard, Projects, Reports, and Settings. Each section has its own contextual help available by pressing F1 or clicking the help icon in the top-right corner.",
            ]),
            ("Troubleshooting Common Setup Issues", [
                "If the application fails to launch after installation, try clearing the cache folder located at ~/.platform/cache and restart. On Windows, you may need to run the application as Administrator for the first launch.",
                "For network connectivity issues, check your firewall settings and ensure that ports 443 and 8443 are open for outbound traffic. Contact your IT department if you are behind a corporate proxy that may need additional configuration.",
            ]),
        ]
    },
    {
        "title": "Core Features",
        "start": 5,   # page 6 (0-indexed: 5)
        "pages": 6,   # pages 6-11
        "sections": [
            ("Dashboard Overview", [
                "The Dashboard is your central hub for monitoring project progress and team activity. It displays real-time metrics including task completion rates, upcoming deadlines, and resource utilization. Widgets can be customized by dragging and dropping them into your preferred layout.",
                "Key performance indicators are displayed prominently at the top: active projects (currently 12), pending tasks (47), team members online (8), and overall completion rate (73%). Click any metric to drill down into detailed analytics.",
            ]),
            ("Project Management", [
                "Create and manage projects using our flexible project structure. Each project supports multiple workstreams, milestones, and task dependencies. Use the Gantt chart view for timeline planning or switch to the Kanban board for agile workflows.",
                "Projects can be organized into portfolios for executive-level tracking. Set project budgets, track actual vs planned expenditures, and generate variance reports. The platform supports both waterfall and agile methodologies with configurable stage gates.",
            ]),
            ("Collaboration Tools", [
                "Real-time collaboration features include document co-editing, threaded discussions, and @mention notifications. Share files up to 500 MB directly within project channels. Version history is maintained for all shared documents.",
                "Schedule meetings directly from the platform using the integrated calendar. Meeting notes are automatically linked to the relevant project context. Video conferencing is supported through integration with Zoom, Teams, and Google Meet.",
            ]),
            ("Reporting and Analytics", [
                "Generate comprehensive reports using the built-in report builder. Choose from over 30 pre-built templates or create custom reports using the drag-and-drop interface. Reports can be scheduled for automatic generation and distribution via email.",
                "Analytics dashboards provide insights into team productivity, resource allocation, and project health scores. Historical data is retained for 24 months, enabling trend analysis and predictive planning. Export reports in PDF, Excel, or CSV formats.",
            ]),
            ("Data Import and Export", [
                "Import data from CSV, Excel, JSON, and XML files using the Data Import wizard. The platform automatically maps columns and validates data types. Conflict resolution options include skip, overwrite, and merge strategies.",
                "Export functionality supports bulk operations across multiple projects. Create custom export templates to include only the fields you need. Scheduled exports can be configured to run daily, weekly, or monthly to a designated cloud storage location.",
            ]),
            ("Search and Filtering", [
                "The global search bar supports full-text search across all projects, documents, and communications. Use advanced filters to narrow results by date range, project, assignee, status, and custom fields. Saved searches can be pinned to the sidebar for quick access.",
                "Filter presets allow teams to create standardized views for common queries such as 'My Overdue Tasks', 'This Week's Deliverables', or 'Unassigned High-Priority Items'. Filters are combinable using AND/OR logic with nested conditions.",
            ]),
        ]
    },
    {
        "title": "Advanced Settings",
        "start": 11,  # page 12 (0-indexed: 11)
        "pages": 6,   # pages 12-17
        "sections": [
            ("User Roles and Permissions", [
                "The platform supports a granular role-based access control (RBAC) system. Default roles include Administrator, Project Manager, Team Member, and Viewer. Custom roles can be created to match your organization's specific access requirements.",
                "Permissions are defined at both the global and project levels. Global permissions control access to administrative functions like user management and billing. Project permissions control who can view, edit, or delete project-specific content.",
            ]),
            ("Workflow Automation", [
                "Create automated workflows using the visual workflow builder. Triggers include task status changes, due date arrivals, form submissions, and webhook events. Actions can include sending notifications, updating fields, creating tasks, and calling external APIs.",
                "Common automation recipes include: auto-assigning tasks based on workload balancing, escalating overdue items to managers, sending weekly digest emails, and archiving completed projects after a specified retention period.",
            ]),
            ("Integration Configuration", [
                "Connect the platform to over 200 third-party services through our integration marketplace. Popular integrations include Slack, Jira, GitHub, Salesforce, and Google Workspace. Each integration can be configured at the organization or project level.",
                "For custom integrations, use the REST API or webhook system. API authentication supports both OAuth 2.0 and API key methods. Rate limits are set to 1000 requests per minute for standard plans and 5000 for enterprise plans.",
            ]),
            ("Security and Compliance", [
                "Data encryption is enforced at rest (AES-256) and in transit (TLS 1.3). Multi-factor authentication (MFA) can be required for all users or specific role groups. Single sign-on (SSO) is supported via SAML 2.0 and OpenID Connect protocols.",
                "Audit logs record all user actions including logins, data modifications, and permission changes. Logs are retained for 7 years to meet regulatory compliance requirements. Export audit data for external SIEM system integration.",
            ]),
            ("Backup and Recovery", [
                "Automated backups run every 6 hours with a 90-day retention policy. Point-in-time recovery is available for the last 30 days with 1-hour granularity. Cross-region backup replication ensures data durability even in the event of a regional outage.",
                "Manual backups can be triggered from the Administration panel. Backup files are encrypted and stored in geographically distributed data centers. Recovery time objectives (RTO) are under 4 hours for full system restoration.",
            ]),
            ("Performance Tuning", [
                "Optimize system performance by configuring cache settings, database connection pools, and worker thread counts. The platform provides a built-in performance monitor that tracks response times, memory usage, and CPU utilization.",
                "For large organizations with over 10,000 users, consider enabling horizontal scaling and load balancing. The platform supports Kubernetes-based deployment for auto-scaling. Database sharding can be configured for datasets exceeding 1 TB.",
            ]),
        ]
    },
    {
        "title": "FAQs",
        "start": 17,  # page 18 (0-indexed: 17)
        "pages": 5,   # pages 18-22
        "sections": [
            ("Account and Billing Questions", [
                "Q: How do I reset my password?\nA: Click 'Forgot Password' on the login page and enter your registered email address. A password reset link will be sent within 5 minutes. If you have MFA enabled, you will also need to verify with your second factor.",
                "Q: Can I change my subscription plan mid-cycle?\nA: Yes, you can upgrade at any time and the cost will be prorated for the remaining billing period. Downgrades take effect at the start of the next billing cycle.",
                "Q: How do I add additional users to my organization?\nA: Navigate to Settings > User Management > Invite Users. Enter the email addresses and select the appropriate role. Each new user will receive an invitation email with setup instructions.",
            ]),
            ("Technical Questions", [
                "Q: What browsers are supported?\nA: The platform supports the latest two major versions of Chrome, Firefox, Safari, and Edge. Internet Explorer is not supported. For the best experience, we recommend Google Chrome.",
                "Q: Can I use the platform offline?\nA: Limited offline functionality is available through the desktop application. Changes made offline are synced automatically when an internet connection is restored. Some features like real-time collaboration require an active connection.",
                "Q: What is the maximum file upload size?\nA: Individual files can be up to 500 MB. For larger files, use the chunked upload API or contact support for a temporary limit increase.",
            ]),
            ("Feature Requests and Support", [
                "Q: How do I submit a feature request?\nA: Use the Feedback button in the bottom-right corner of any page to submit suggestions. Feature requests are reviewed monthly by the product team and popular requests are added to the public roadmap.",
                "Q: What support channels are available?\nA: Standard plans include email support with 24-hour response times. Professional plans add live chat during business hours. Enterprise plans include dedicated account management and 24/7 phone support.",
                "Q: Where can I find video tutorials?\nA: Visit our Learning Center at https://learn.platform.example.com for over 100 video tutorials organized by topic. New tutorials are added monthly covering both new features and advanced techniques.",
            ]),
            ("Data and Privacy", [
                "Q: Where is my data stored?\nA: Data is stored in AWS data centers in the region you selected during setup (US-East, EU-West, or AP-Southeast). Data never leaves your selected region unless you explicitly enable cross-region features.",
                "Q: Can I export all my data?\nA: Yes, full data export is available from Settings > Data Management > Export All. The export includes projects, tasks, files, and communication history in a machine-readable JSON format. GDPR-compliant data portability is fully supported.",
                "Q: How long is deleted data retained?\nA: Soft-deleted items remain in the trash for 30 days and can be restored by any Administrator. After 30 days, data is permanently removed from all active systems. Backup copies may persist for up to 90 days per the retention policy.",
            ]),
            ("Troubleshooting Common Issues", [
                "Q: The application is running slowly. What should I do?\nA: First, check your internet connection speed. Clear your browser cache and disable any browser extensions that might interfere. If the issue persists, contact support with your browser console logs.",
                "Q: I cannot access a project that was shared with me.\nA: Verify that the project owner has granted you the appropriate permissions. Check your email for the invitation link and ensure you are logged in with the correct account. Contact the project administrator if the issue persists.",
                "Q: Notifications are not being delivered.\nA: Check your notification preferences in Settings > Notifications. Ensure that email notifications are enabled and that our domain (notifications@platform.example.com) is whitelisted in your email provider. Also verify your browser allows push notifications from our site.",
            ]),
        ]
    },
]


def create_initial():
    doc = pymupdf.open()

    # Create all 22 pages with chapter content
    for chapter in CHAPTERS:
        for page_idx in range(chapter["pages"]):
            page = doc.new_page(width=595, height=842)  # A4

            y_pos = 72  # top margin

            # Chapter title on first page of each chapter
            if page_idx == 0:
                page.insert_text(
                    pymupdf.Point(72, y_pos),
                    chapter["title"],
                    fontsize=24,
                    fontname="hebo",  # Helvetica Bold
                    color=(0.1, 0.2, 0.5),
                )
                y_pos += 40
                # Separator line
                shape = page.new_shape()
                shape.draw_line(pymupdf.Point(72, y_pos), pymupdf.Point(523, y_pos))
                shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
                shape.commit()
                y_pos += 25

            # Section content for this page
            if page_idx < len(chapter["sections"]):
                section_title, paragraphs = chapter["sections"][page_idx]

                # Section title
                page.insert_text(
                    pymupdf.Point(72, y_pos),
                    section_title,
                    fontsize=14,
                    fontname="hebo",
                    color=(0.2, 0.2, 0.2),
                )
                y_pos += 25

                # Paragraphs
                for para in paragraphs:
                    rect = pymupdf.Rect(72, y_pos, 523, y_pos + 200)
                    excess = page.insert_textbox(
                        rect,
                        para,
                        fontsize=10,
                        fontname="helv",
                        color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY,
                    )
                    y_pos += 120

            # Page number at bottom
            page_num = chapter["start"] + page_idx + 1
            page.insert_text(
                pymupdf.Point(280, 800),
                str(page_num),
                fontsize=9,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )

    # Verify page count
    assert doc.page_count == 22, f"Expected 22 pages, got {doc.page_count}"

    # No TOC / no bookmarks — this is the initial state
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 22')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
