"""
Initial Setup: Create a 10-page resource guide PDF with 15 hyperlinks scattered across pages.
Task ID: pdf_mbc_077
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_077'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/resource_guide.pdf'


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
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # Define hyperlinks to scatter across 10 pages (15 total)
    # Format: (page_index, url, display_text, y_position)
    hyperlinks = [
        # Page 1 (index 0) - Introduction - 2 links
        (0, "https://www.python.org/downloads/", "Python Official Downloads"),
        (0, "https://docs.python.org/3/tutorial/index.html", "Python Tutorial"),
        # Page 2 (index 1) - Web Development - 2 links
        (1, "https://flask.palletsprojects.com/en/3.0.x/", "Flask Documentation"),
        (1, "https://www.djangoproject.com/start/overview/", "Django Overview"),
        # Page 3 (index 2) - Data Science - 2 links
        (2, "https://numpy.org/doc/stable/user/quickstart.html", "NumPy Quickstart"),
        (2, "https://pandas.pydata.org/docs/getting_started/", "Pandas Getting Started"),
        # Page 4 (index 3) - Machine Learning - 1 link
        (3, "https://scikit-learn.org/stable/getting_started.html", "Scikit-learn Guide"),
        # Page 5 (index 4) - Cloud Computing - 2 links
        (4, "https://aws.amazon.com/getting-started/", "AWS Getting Started"),
        (4, "https://cloud.google.com/docs/overview", "Google Cloud Overview"),
        # Page 6 (index 5) - DevOps - 1 link
        (5, "https://docs.docker.com/get-started/", "Docker Getting Started"),
        # Page 7 (index 6) - Security - 2 links
        (6, "https://owasp.org/www-project-top-ten/", "OWASP Top Ten"),
        (6, "https://www.nist.gov/cyberframework", "NIST Cybersecurity Framework"),
        # Page 8 (index 7) - Databases - 1 link
        (7, "https://www.postgresql.org/docs/current/tutorial.html", "PostgreSQL Tutorial"),
        # Page 9 (index 8) - Version Control - 1 link
        (8, "https://git-scm.com/book/en/v2", "Pro Git Book"),
        # Page 10 (index 9) - Further Reading - 1 link
        (9, "https://github.com/public-apis/public-apis", "Public APIs Collection"),
    ]

    # Page content for each of the 10 pages
    page_content = [
        {
            "title": "Technology Resource Guide",
            "subtitle": "A Comprehensive Collection of Developer Resources",
            "section": "1. Introduction to Programming",
            "body": (
                "Welcome to the Technology Resource Guide. This document compiles essential "
                "resources for software developers at all experience levels. Whether you are "
                "just beginning your programming journey or looking to expand your skill set, "
                "the curated links and references in this guide will help you navigate the vast "
                "landscape of modern software development.\n\n"
                "Python remains one of the most versatile programming languages available today. "
                "Its clean syntax and extensive standard library make it ideal for beginners, "
                "while its powerful ecosystem supports advanced applications in web development, "
                "data science, and machine learning."
            ),
        },
        {
            "title": "2. Web Development Frameworks",
            "body": (
                "Web development continues to evolve rapidly, with new frameworks and tools "
                "emerging regularly. Two of the most popular Python web frameworks are Flask "
                "and Django, each suited to different project requirements.\n\n"
                "Flask is a lightweight micro-framework that gives developers flexibility in "
                "choosing components. It is ideal for small to medium applications and APIs. "
                "Django, on the other hand, follows the batteries-included philosophy, providing "
                "an ORM, authentication system, admin panel, and much more out of the box.\n\n"
                "When selecting a framework, consider your project's scale, your team's "
                "experience, and the specific features you need. Both frameworks have excellent "
                "community support and comprehensive documentation."
            ),
        },
        {
            "title": "3. Data Science Essentials",
            "body": (
                "Data science has become a critical capability for organizations across all "
                "industries. The Python data science ecosystem provides powerful tools for "
                "data manipulation, analysis, and visualization.\n\n"
                "NumPy provides the foundation for numerical computing in Python, offering "
                "efficient array operations and mathematical functions. Building on NumPy, "
                "Pandas offers high-level data structures like DataFrames that simplify data "
                "cleaning, transformation, and analysis tasks.\n\n"
                "Together, these libraries form the backbone of most data science workflows, "
                "from initial data exploration to feature engineering for machine learning models."
            ),
        },
        {
            "title": "4. Machine Learning",
            "body": (
                "Machine learning enables computers to learn patterns from data without being "
                "explicitly programmed for each scenario. The field has seen tremendous growth "
                "in recent years, driven by increases in computational power and data availability.\n\n"
                "Scikit-learn is the most widely used machine learning library in Python. It "
                "provides a consistent interface for classification, regression, clustering, "
                "and dimensionality reduction algorithms. The library also includes utilities "
                "for model evaluation, cross-validation, and hyperparameter tuning.\n\n"
                "For production deployments, consider the full pipeline from data preprocessing "
                "to model serving, including monitoring and retraining strategies."
            ),
        },
        {
            "title": "5. Cloud Computing Platforms",
            "body": (
                "Cloud computing has fundamentally changed how organizations build and deploy "
                "applications. Major cloud providers offer a wide range of services, from basic "
                "virtual machines to managed AI/ML platforms.\n\n"
                "Amazon Web Services (AWS) leads the market with the broadest service catalog. "
                "Their getting started guides cover everything from setting up an account to "
                "deploying complex distributed architectures.\n\n"
                "Google Cloud Platform (GCP) provides particularly strong offerings in data "
                "analytics and machine learning, leveraging Google's expertise in these domains. "
                "Their documentation includes hands-on tutorials and architecture guides."
            ),
        },
        {
            "title": "6. DevOps and Containerization",
            "body": (
                "DevOps practices bridge the gap between software development and IT operations, "
                "emphasizing automation, continuous integration, and continuous deployment.\n\n"
                "Docker has revolutionized application deployment by enabling containerization. "
                "Containers package an application with all its dependencies into a standardized "
                "unit, ensuring consistent behavior across development, testing, and production "
                "environments.\n\n"
                "Adopting containerization improves deployment reliability, simplifies scaling, "
                "and enables microservices architectures. Combined with orchestration tools like "
                "Kubernetes, teams can manage complex distributed systems efficiently."
            ),
        },
        {
            "title": "7. Cybersecurity Resources",
            "body": (
                "Security is a critical concern for every software project. Understanding common "
                "vulnerabilities and implementing proper defenses protects both your organization "
                "and your users.\n\n"
                "The OWASP Top Ten provides an authoritative list of the most critical web "
                "application security risks. Updated regularly, it serves as a benchmark for "
                "security assessments and developer training programs.\n\n"
                "The NIST Cybersecurity Framework offers a comprehensive approach to managing "
                "cybersecurity risk. It provides standards, guidelines, and best practices that "
                "organizations of all sizes can adopt to improve their security posture."
            ),
        },
        {
            "title": "8. Database Technologies",
            "body": (
                "Choosing the right database technology is one of the most important architectural "
                "decisions in any software project. The landscape includes relational databases, "
                "NoSQL solutions, and specialized systems for specific use cases.\n\n"
                "PostgreSQL is a powerful open-source relational database known for its reliability, "
                "feature richness, and standards compliance. Its tutorial covers fundamental "
                "concepts including SQL syntax, data types, and query optimization.\n\n"
                "When evaluating database options, consider factors like data structure, query "
                "patterns, scalability requirements, and consistency guarantees."
            ),
        },
        {
            "title": "9. Version Control with Git",
            "body": (
                "Version control is an essential skill for every developer. Git has become the "
                "de facto standard for source code management, used by teams of all sizes from "
                "individual developers to large enterprises.\n\n"
                "The Pro Git book is the definitive resource for learning Git. It covers "
                "everything from basic commands to advanced topics like rebasing, cherry-picking, "
                "and managing complex branching strategies.\n\n"
                "Effective use of version control improves collaboration, enables code review, "
                "and provides a safety net for experimenting with new features without risking "
                "the stability of your main codebase."
            ),
        },
        {
            "title": "10. Further Reading and Community Resources",
            "body": (
                "The software development community is remarkably open and collaborative. "
                "Countless developers contribute to open-source projects, write tutorials, and "
                "share their knowledge through blogs, conferences, and online forums.\n\n"
                "Public API collections are invaluable resources for developers building "
                "applications that integrate with external services. These curated lists help "
                "you discover APIs for weather data, financial information, social media, and "
                "hundreds of other categories.\n\n"
                "Stay curious, keep learning, and contribute back to the community. The best "
                "way to grow as a developer is to build projects, collaborate with others, and "
                "continuously expand your knowledge."
            ),
        },
    ]

    # Create all 10 pages
    for page_idx in range(10):
        page = doc.new_page(width=595, height=842)  # A4
        content = page_content[page_idx]

        y = 60

        # Title
        if page_idx == 0:
            # First page: main title + subtitle
            page.insert_text(
                pymupdf.Point(72, y),
                content["title"],
                fontsize=22,
                fontname="hebo",
                color=(0.0, 0.2, 0.5),
            )
            y += 30
            page.insert_text(
                pymupdf.Point(72, y),
                content["subtitle"],
                fontsize=12,
                fontname="heit",
                color=(0.4, 0.4, 0.4),
            )
            y += 30

            # Horizontal rule
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(523, y))
            shape.finish(color=(0.0, 0.2, 0.5), width=1.5)
            shape.commit()
            y += 20

            # Section heading
            page.insert_text(
                pymupdf.Point(72, y),
                content["section"],
                fontsize=16,
                fontname="hebo",
                color=(0.1, 0.1, 0.1),
            )
            y += 25
        else:
            # Other pages: section title
            page.insert_text(
                pymupdf.Point(72, y),
                content["title"],
                fontsize=18,
                fontname="hebo",
                color=(0.0, 0.2, 0.5),
            )
            y += 15
            # Horizontal rule
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(523, y))
            shape.finish(color=(0.0, 0.2, 0.5), width=1.0)
            shape.commit()
            y += 20

        # Body text
        body_rect = pymupdf.Rect(72, y, 523, 650)
        page.insert_textbox(
            body_rect,
            content["body"],
            fontsize=11,
            fontname="helv",
            color=(0.15, 0.15, 0.15),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Page number at bottom
        page.insert_text(
            pymupdf.Point(280, 800),
            f"- {page_idx + 1} -",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    # Now insert hyperlinks on the appropriate pages
    # We place link text and link annotations near the bottom of the body area
    link_y_offsets = {}  # track y offset per page
    for page_idx, url, display_text in hyperlinks:
        page = doc[page_idx]
        if page_idx not in link_y_offsets:
            link_y_offsets[page_idx] = 670
        else:
            link_y_offsets[page_idx] += 22

        y_pos = link_y_offsets[page_idx]

        # Insert bullet and label
        page.insert_text(
            pymupdf.Point(82, y_pos),
            f"\u2022 ",
            fontsize=10,
            fontname="helv",
            color=(0.2, 0.2, 0.2),
        )

        # Insert the display text as a link
        link_x = 95
        page.insert_text(
            pymupdf.Point(link_x, y_pos),
            display_text,
            fontsize=10,
            fontname="helv",
            color=(0.0, 0.3, 0.8),
        )

        # Calculate approximate text width for the link rect
        text_width = len(display_text) * 5.5  # rough estimate
        link_rect = pymupdf.Rect(link_x, y_pos - 10, link_x + text_width, y_pos + 3)

        # Insert the URI link
        page.insert_link({
            "kind": pymupdf.LINK_URI,
            "from": link_rect,
            "uri": url,
        })

    # Set metadata
    doc.set_metadata({
        "title": "Technology Resource Guide",
        "author": "Olivia Martinez",
        "subject": "Developer Resources and Learning Materials",
        "keywords": "programming, python, web development, data science, cloud, devops",
        "creator": "Resource Guide Team",
    })

    # Set table of contents
    toc = [
        [1, "Introduction to Programming", 1],
        [1, "Web Development Frameworks", 2],
        [1, "Data Science Essentials", 3],
        [1, "Machine Learning", 4],
        [1, "Cloud Computing Platforms", 5],
        [1, "DevOps and Containerization", 6],
        [1, "Cybersecurity Resources", 7],
        [1, "Database Technologies", 8],
        [1, "Version Control with Git", 9],
        [1, "Further Reading and Community Resources", 10],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Make sure links.txt does NOT exist
    links_path = f'{DOCUMENTS}/links.txt'
    if os.path.exists(links_path):
        os.remove(links_path)
        print(f'Removed pre-existing {links_path}')

    # GUI-ready startup: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
