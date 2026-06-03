"""
Initial Setup: Create a 40-page PDF with 3 outdated bookmarks and a new_bookmarks.info file
Task ID: pdf_mbc_060
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf  # PyMuPDF


WORKDIR = '/home/user'
DOCS_DIR = os.path.join(WORKDIR, 'Documents')
OUTPUT_PDF = os.path.join(DOCS_DIR, 'guide.pdf')
OUTPUT_INFO = os.path.join(DOCS_DIR, 'new_bookmarks.info')


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    # --- Create a 40-page guide PDF ---
    doc = pymupdf.open()

    # Chapter structure for realistic content
    chapters = [
        ("Introduction to Cloud Computing", [
            "Cloud computing has revolutionized the way organizations deploy and manage their IT infrastructure.",
            "This guide provides a comprehensive overview of cloud services, architectures, and best practices.",
            "Whether you are a beginner or an experienced professional, this document will serve as a valuable reference.",
        ]),
        ("Infrastructure as a Service (IaaS)", [
            "IaaS provides virtualized computing resources over the internet.",
            "Key providers include Amazon Web Services, Microsoft Azure, and Google Cloud Platform.",
            "Users can provision virtual machines, storage, and networking on demand.",
        ]),
        ("Platform as a Service (PaaS)", [
            "PaaS offers a development and deployment environment in the cloud.",
            "Developers can build, test, and deploy applications without managing underlying infrastructure.",
            "Popular PaaS offerings include Heroku, Google App Engine, and Azure App Service.",
        ]),
        ("Software as a Service (SaaS)", [
            "SaaS delivers software applications over the internet on a subscription basis.",
            "Users access applications through a web browser without local installation.",
            "Examples include Salesforce, Google Workspace, and Microsoft 365.",
        ]),
        ("Security and Compliance", [
            "Cloud security involves policies, technologies, and controls to protect data and infrastructure.",
            "Compliance frameworks such as SOC 2, HIPAA, and GDPR must be considered.",
            "Shared responsibility models define security obligations between providers and customers.",
        ]),
        ("Cost Optimization", [
            "Effective cloud cost management requires monitoring, forecasting, and rightsizing resources.",
            "Reserved instances and savings plans can reduce long-term costs significantly.",
            "Tagging strategies and budget alerts help teams stay within financial targets.",
        ]),
        ("Migration Strategies", [
            "The six Rs of cloud migration: Rehost, Replatform, Repurchase, Refactor, Retain, and Retire.",
            "A successful migration plan includes assessment, planning, execution, and optimization phases.",
            "Hybrid cloud approaches allow gradual transition from on-premises to cloud environments.",
        ]),
        ("Monitoring and Observability", [
            "Cloud monitoring tools track resource utilization, application performance, and system health.",
            "Observability encompasses logs, metrics, and traces for comprehensive system understanding.",
            "Automated alerting and incident response streamline operations management.",
        ]),
    ]

    # Generate 40 pages with chapter content
    page_idx = 0
    for ch_idx, (title, paragraphs) in enumerate(chapters):
        # Each chapter gets ~5 pages
        for sub_page in range(5):
            page = doc.new_page(width=595, height=842)  # A4
            y = 72

            if sub_page == 0:
                # Chapter title page
                page.insert_text(
                    pymupdf.Point(72, y),
                    f"Chapter {ch_idx + 1}",
                    fontsize=14,
                    fontname="hebo",
                    color=(0.2, 0.2, 0.6),
                )
                y += 30
                page.insert_text(
                    pymupdf.Point(72, y),
                    title,
                    fontsize=20,
                    fontname="hebo",
                    color=(0, 0, 0),
                )
                y += 40
                for para in paragraphs:
                    excess = page.insert_textbox(
                        pymupdf.Rect(72, y, 523, y + 60),
                        para,
                        fontsize=11,
                        fontname="helv",
                        color=(0, 0, 0),
                    )
                    y += 70
            else:
                # Continuation pages with filler content
                page.insert_text(
                    pymupdf.Point(72, y),
                    f"{title} — Page {sub_page + 1}",
                    fontsize=12,
                    fontname="hebo",
                    color=(0.3, 0.3, 0.3),
                )
                y += 30
                body_text = (
                    f"This section continues the discussion of {title.lower()}. "
                    f"Organizations must carefully evaluate their requirements and constraints "
                    f"when implementing solutions in this area. Performance benchmarks conducted "
                    f"in Q3 2025 showed a 23% improvement in resource utilization across "
                    f"enterprise deployments. Additional considerations include scalability, "
                    f"fault tolerance, and disaster recovery planning. Teams should establish "
                    f"clear governance policies and review them quarterly to ensure alignment "
                    f"with business objectives and regulatory requirements."
                )
                page.insert_textbox(
                    pymupdf.Rect(72, y, 523, 770),
                    body_text,
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                )

            # Footer with page number
            page.insert_text(
                pymupdf.Point(280, 810),
                f"— {page_idx + 1} —",
                fontsize=9,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )
            page_idx += 1

    # Set 3 outdated bookmarks (the old TOC)
    old_toc = [
        [1, "Part I: Overview", 1],
        [1, "Part II: Services", 11],
        [1, "Part III: Operations", 26],
    ]
    doc.set_toc(old_toc)

    doc.save(OUTPUT_PDF)
    doc.close()
    print(f"Initial PDF created: {OUTPUT_PDF} ({page_idx} pages, 3 bookmarks)")

    # --- Create new_bookmarks.info in pdftk format ---
    bookmarks_info = """\
BookmarkBegin
BookmarkTitle: Introduction to Cloud Computing
BookmarkLevel: 1
BookmarkPageNumber: 1
BookmarkBegin
BookmarkTitle: Infrastructure as a Service (IaaS)
BookmarkLevel: 1
BookmarkPageNumber: 6
BookmarkBegin
BookmarkTitle: Platform as a Service (PaaS)
BookmarkLevel: 1
BookmarkPageNumber: 11
BookmarkBegin
BookmarkTitle: Software as a Service (SaaS)
BookmarkLevel: 1
BookmarkPageNumber: 16
BookmarkBegin
BookmarkTitle: Security and Compliance
BookmarkLevel: 1
BookmarkPageNumber: 21
BookmarkBegin
BookmarkTitle: Cost Optimization
BookmarkLevel: 1
BookmarkPageNumber: 26
BookmarkBegin
BookmarkTitle: Migration Strategies
BookmarkLevel: 1
BookmarkPageNumber: 31
BookmarkBegin
BookmarkTitle: Monitoring and Observability
BookmarkLevel: 1
BookmarkPageNumber: 36
"""
    with open(OUTPUT_INFO, 'w') as f:
        f.write(bookmarks_info)
    print(f"Bookmark info file created: {OUTPUT_INFO} (8 entries)")

    # Open PDF in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT_PDF}"', delay_sec=2.0)
    print("GUI_READY: launched Evince with DISPLAY=:0")


create_initial()
