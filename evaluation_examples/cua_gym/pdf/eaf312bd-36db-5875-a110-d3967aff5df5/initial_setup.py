"""
Initial Setup: Create a 7-page web references PDF with ~25 embedded hyperlinks
Task ID: pdf_res_045
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_045'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/web_references.pdf'

# All URLs that will be embedded in the document (25 total)
URLS = [
    "https://www.w3.org/TR/html52/",
    "https://developer.mozilla.org/en-US/docs/Web/CSS",
    "https://www.ecma-international.org/publications-and-standards/standards/ecma-262/",
    "https://nodejs.org/en/about",
    "https://reactjs.org/docs/getting-started.html",
    "https://angular.io/guide/architecture",
    "https://vuejs.org/guide/introduction.html",
    "https://www.typescriptlang.org/docs/handbook/intro.html",
    "https://webpack.js.org/concepts/",
    "https://www.json.org/json-en.html",
    "https://graphql.org/learn/",
    "https://www.postgresql.org/docs/current/index.html",
    "https://redis.io/documentation",
    "https://docs.docker.com/get-started/",
    "https://kubernetes.io/docs/concepts/overview/",
    "https://aws.amazon.com/architecture/well-architected/",
    "https://cloud.google.com/architecture/framework",
    "https://www.terraform.io/docs/language/index.html",
    "https://prometheus.io/docs/introduction/overview/",
    "https://grafana.com/docs/grafana/latest/",
    "https://owasp.org/www-project-top-ten/",
    "https://letsencrypt.org/docs/",
    "https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/",
    "https://web.dev/performance/",
    "https://httparchive.org/reports/state-of-the-web",
]


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


def add_link(page, rect, uri):
    """Insert a URI link on the page at the given rect."""
    page.insert_link({
        "kind": pymupdf.LINK_URI,
        "from": rect,
        "uri": uri,
    })


def create_initial():
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()
    W, H = 612, 792  # Letter size

    # =========================================================
    # Page 1: Title page and Abstract
    # =========================================================
    p = doc.new_page(width=W, height=H)
    # Title
    p.insert_text(pymupdf.Point(72, 80), "A Comprehensive Survey of Modern Web Technologies",
                  fontsize=18, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(72, 105), "and Infrastructure Patterns for Scalable Applications",
                  fontsize=18, fontname="hebo", color=(0, 0, 0))
    # Authors
    p.insert_text(pymupdf.Point(72, 140), "Dr. Elena Vasquez, Prof. Rajesh Patel, Dr. Mei-Ling Chang",
                  fontsize=11, fontname="tiit", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(72, 158), "Department of Computer Science, Westbrook University",
                  fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(72, 174), "Published: March 2025   |   Technical Report WU-CS-2025-042",
                  fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))

    # Horizontal rule
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(72, 192), pymupdf.Point(540, 192))
    shape.finish(color=(0.6, 0.6, 0.6), width=1)
    shape.commit()

    # Abstract
    p.insert_text(pymupdf.Point(72, 220), "Abstract", fontsize=14, fontname="hebo", color=(0, 0, 0))
    abstract_text = (
        "The rapid evolution of web technologies has transformed how organizations build, deploy, and "
        "maintain software systems. This paper presents a comprehensive survey of the current landscape "
        "spanning front-end frameworks, back-end runtimes, data storage solutions, containerization "
        "platforms, cloud infrastructure, security best practices, and performance optimization "
        "techniques. We examine 25 key resources and specifications that form the foundation of "
        "modern web development, providing practitioners with a structured reference guide. Our "
        "analysis covers the HTML5 specification [1], CSS standards [2], ECMAScript language "
        "specification [3], and extends through deployment and monitoring tools. Each section "
        "includes direct references to authoritative documentation and community resources."
    )
    p.insert_textbox(pymupdf.Rect(72, 240, 540, 420), abstract_text,
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Keywords
    p.insert_text(pymupdf.Point(72, 435), "Keywords: ", fontsize=10, fontname="hebo", color=(0, 0, 0))
    p.insert_text(pymupdf.Point(130, 435),
                  "web development, front-end frameworks, cloud infrastructure, DevOps, security",
                  fontsize=10, fontname="tiit", color=(0.2, 0.2, 0.2))

    # Section 1 intro
    p.insert_text(pymupdf.Point(72, 475), "1. Introduction", fontsize=14, fontname="hebo", color=(0, 0, 0))
    intro_text = (
        "Modern web development encompasses a vast ecosystem of technologies, standards, and tools. "
        "From the foundational HTML5 specification maintained by the W3C to sophisticated container "
        "orchestration platforms, developers must navigate an increasingly complex landscape. This "
        "survey organizes these technologies into coherent categories and provides direct links to "
        "authoritative references.\n\n"
        "The HTML5 specification (https://www.w3.org/TR/html52/) remains the cornerstone of web "
        "content structure, while CSS (https://developer.mozilla.org/en-US/docs/Web/CSS) continues "
        "to evolve with new layout and styling capabilities. Together with the ECMAScript standard "
        "(https://www.ecma-international.org/publications-and-standards/standards/ecma-262/), these "
        "three technologies form the bedrock upon which all web applications are built."
    )
    p.insert_textbox(pymupdf.Rect(72, 498, 540, 720), intro_text,
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Links on page 1: URLs 0, 1, 2 (embedded in intro text)
    # We place link annotations at approximate positions where URLs appear
    r0 = pymupdf.Rect(72, 620, 350, 632)
    add_link(p, r0, URLS[0])
    r1 = pymupdf.Rect(170, 638, 490, 650)
    add_link(p, r1, URLS[1])
    r2 = pymupdf.Rect(72, 668, 540, 680)
    add_link(p, r2, URLS[2])

    # =========================================================
    # Page 2: Front-end Technologies
    # =========================================================
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(72, 60), "2. Front-end Technologies and Frameworks",
                  fontsize=14, fontname="hebo", color=(0, 0, 0))
    fe_text = (
        "The front-end ecosystem has matured significantly over the past decade. Server-side "
        "rendering, client-side hydration, and static site generation are now standard capabilities "
        "across major frameworks.\n\n"
        "2.1 Runtime Environments\n\n"
        "Node.js (https://nodejs.org/en/about) has become the de facto JavaScript runtime for "
        "server-side development and build tooling. Its event-driven, non-blocking I/O model makes "
        "it particularly well-suited for real-time applications and microservices architectures. The "
        "npm registry now hosts over 2 million packages, making it the largest software registry in "
        "the world.\n\n"
        "2.2 Component Frameworks\n\n"
        "React (https://reactjs.org/docs/getting-started.html) introduced the virtual DOM concept and "
        "component-based architecture that has influenced virtually every modern framework. With the "
        "introduction of hooks and concurrent features, React continues to push the boundaries of "
        "declarative UI development.\n\n"
        "Angular (https://angular.io/guide/architecture) provides a comprehensive, opinionated "
        "framework with built-in dependency injection, routing, and reactive forms. Its TypeScript-first "
        "approach enforces strong typing patterns that benefit large-scale enterprise applications.\n\n"
        "Vue.js (https://vuejs.org/guide/introduction.html) offers a progressive adoption model that "
        "allows teams to incrementally integrate framework features. The Composition API, introduced "
        "in Vue 3, provides improved code organization and TypeScript support."
    )
    p.insert_textbox(pymupdf.Rect(72, 80, 540, 560), fe_text,
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Links: URLs 3, 4, 5, 6
    add_link(p, pymupdf.Rect(72, 178, 330, 190), URLS[3])
    add_link(p, pymupdf.Rect(72, 268, 420, 280), URLS[4])
    add_link(p, pymupdf.Rect(72, 340, 380, 352), URLS[5])
    add_link(p, pymupdf.Rect(72, 430, 410, 442), URLS[6])

    # Section 2.3
    p.insert_text(pymupdf.Point(72, 580), "2.3 Type Systems and Build Tools",
                  fontsize=12, fontname="hebo", color=(0, 0, 0))
    ts_text = (
        "TypeScript (https://www.typescriptlang.org/docs/handbook/intro.html) has rapidly gained "
        "adoption as the preferred superset of JavaScript, providing static type checking and "
        "enhanced IDE support. Major frameworks now ship with first-class TypeScript support.\n\n"
        "Webpack (https://webpack.js.org/concepts/) remains a widely-used module bundler, though "
        "newer tools like Vite and esbuild are gaining traction for their superior build speeds."
    )
    p.insert_textbox(pymupdf.Rect(72, 600, 540, 760), ts_text,
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Links: URLs 7, 8
    add_link(p, pymupdf.Rect(72, 610, 490, 622), URLS[7])
    add_link(p, pymupdf.Rect(72, 668, 370, 680), URLS[8])

    # =========================================================
    # Page 3: Data Layer
    # =========================================================
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(72, 60), "3. Data Exchange and Storage",
                  fontsize=14, fontname="hebo", color=(0, 0, 0))
    data_text = (
        "Effective data management is critical to web application performance and reliability. This "
        "section examines the primary data exchange format, query paradigm, and storage technologies "
        "used in modern architectures.\n\n"
        "3.1 Data Formats and APIs\n\n"
        "JSON (https://www.json.org/json-en.html) has supplanted XML as the dominant data interchange "
        "format for web APIs. Its simplicity and native JavaScript compatibility make it the natural "
        "choice for REST APIs, configuration files, and inter-service communication.\n\n"
        "GraphQL (https://graphql.org/learn/) provides a flexible query language that allows clients "
        "to request exactly the data they need. By eliminating over-fetching and under-fetching "
        "problems inherent in REST architectures, GraphQL has become particularly popular in mobile "
        "and micro-frontend applications where bandwidth efficiency matters.\n\n"
        "3.2 Database Technologies\n\n"
        "PostgreSQL (https://www.postgresql.org/docs/current/index.html) continues to set the standard "
        "for relational databases with its extensibility, JSONB support, and advanced query capabilities. "
        "Features like logical replication, partitioning, and full-text search make it suitable for a "
        "wide range of workloads from OLTP to analytics.\n\n"
        "Redis (https://redis.io/documentation) serves as a versatile in-memory data structure store "
        "used for caching, session management, rate limiting, and real-time analytics. Its support for "
        "data structures like sorted sets, streams, and HyperLogLog enables sophisticated use cases "
        "beyond simple key-value caching."
    )
    p.insert_textbox(pymupdf.Rect(72, 80, 540, 560), data_text,
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Links: URLs 9, 10, 11, 12
    add_link(p, pymupdf.Rect(72, 178, 340, 190), URLS[9])
    add_link(p, pymupdf.Rect(72, 248, 300, 260), URLS[10])
    add_link(p, pymupdf.Rect(72, 348, 470, 360), URLS[11])
    add_link(p, pymupdf.Rect(72, 430, 330, 442), URLS[12])

    # =========================================================
    # Page 4: Containerization and Orchestration
    # =========================================================
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(72, 60), "4. Containerization and Orchestration",
                  fontsize=14, fontname="hebo", color=(0, 0, 0))
    container_text = (
        "Container technologies have fundamentally changed how applications are packaged, distributed, "
        "and run in production environments.\n\n"
        "4.1 Container Platforms\n\n"
        "Docker (https://docs.docker.com/get-started/) has become synonymous with application "
        "containerization. By providing a standardized way to package applications with their "
        "dependencies, Docker eliminated the 'works on my machine' problem that plagued development "
        "teams for decades. The Docker Hub registry hosts millions of container images spanning "
        "virtually every technology stack.\n\n"
        "4.2 Orchestration\n\n"
        "Kubernetes (https://kubernetes.io/docs/concepts/overview/) has emerged as the industry "
        "standard for container orchestration. Originally developed at Google and based on their "
        "internal Borg system, Kubernetes provides declarative configuration, automatic scaling, "
        "service discovery, and self-healing capabilities. The Kubernetes ecosystem includes "
        "operators, custom resource definitions, and a rich set of tools for managing complex "
        "distributed systems.\n\n"
        "Table 1 below summarizes the adoption rates of these technologies based on the 2024 "
        "Developer Survey conducted across 15,000 professional developers.\n\n"
    )
    p.insert_textbox(pymupdf.Rect(72, 80, 540, 420), container_text,
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Links: URLs 13, 14
    add_link(p, pymupdf.Rect(72, 178, 380, 190), URLS[13])
    add_link(p, pymupdf.Rect(72, 280, 430, 292), URLS[14])

    # Table: Technology Adoption
    table_data = [
        ["Technology", "Adoption Rate", "YoY Growth", "Primary Use Case"],
        ["Docker", "89%", "+3.2%", "Application packaging"],
        ["Kubernetes", "72%", "+8.1%", "Container orchestration"],
        ["PostgreSQL", "65%", "+5.4%", "Relational data storage"],
        ["Redis", "58%", "+4.7%", "Caching and sessions"],
        ["GraphQL", "34%", "+11.2%", "API query language"],
        ["Terraform", "41%", "+9.8%", "Infrastructure as Code"],
    ]
    y_start = 440
    col_widths = [120, 100, 90, 160]
    col_x = [72, 192, 292, 382]
    row_h = 22

    shape = p.new_shape()
    for i, row in enumerate(table_data):
        y = y_start + i * row_h
        for j, cell in enumerate(row):
            fn = "hebo" if i == 0 else "tiro"
            clr = (1, 1, 1) if i == 0 else (0, 0, 0)
            p.insert_text(pymupdf.Point(col_x[j] + 4, y + 15), cell,
                          fontsize=9, fontname=fn, color=clr)
        # Row background
        if i == 0:
            shape.draw_rect(pymupdf.Rect(72, y, 540, y + row_h))
            shape.finish(fill=(0.2, 0.3, 0.5), color=(0.2, 0.3, 0.5))
        else:
            shape.draw_rect(pymupdf.Rect(72, y, 540, y + row_h))
            fill = (0.95, 0.95, 0.95) if i % 2 == 0 else (1, 1, 1)
            shape.finish(fill=fill, color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    # =========================================================
    # Page 5: Cloud Infrastructure
    # =========================================================
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(72, 60), "5. Cloud Infrastructure and IaC",
                  fontsize=14, fontname="hebo", color=(0, 0, 0))
    cloud_text = (
        "Cloud computing has shifted the infrastructure paradigm from capital expenditure to "
        "operational expenditure, enabling organizations of all sizes to access enterprise-grade "
        "infrastructure on demand.\n\n"
        "5.1 Cloud Architecture Frameworks\n\n"
        "The AWS Well-Architected Framework (https://aws.amazon.com/architecture/well-architected/) "
        "provides a comprehensive set of best practices organized around six pillars: operational "
        "excellence, security, reliability, performance efficiency, cost optimization, and "
        "sustainability. These pillars help teams evaluate and improve their cloud architectures.\n\n"
        "The Google Cloud Architecture Framework (https://cloud.google.com/architecture/framework) "
        "similarly provides guidance for building reliable, performant, and secure applications on "
        "Google Cloud Platform. Both frameworks emphasize the importance of automated testing, "
        "infrastructure as code, and observability.\n\n"
        "5.2 Infrastructure as Code\n\n"
        "Terraform (https://www.terraform.io/docs/language/index.html) has become the leading "
        "infrastructure-as-code tool, supporting multiple cloud providers through a unified "
        "declarative configuration language (HCL). Its state management, plan/apply workflow, and "
        "module system enable teams to manage complex multi-cloud environments with confidence. "
        "The Terraform Registry provides thousands of pre-built modules and providers."
    )
    p.insert_textbox(pymupdf.Rect(72, 80, 540, 520), cloud_text,
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Links: URLs 15, 16, 17
    add_link(p, pymupdf.Rect(72, 198, 490, 210), URLS[15])
    add_link(p, pymupdf.Rect(72, 290, 460, 302), URLS[16])
    add_link(p, pymupdf.Rect(72, 380, 460, 392), URLS[17])

    # =========================================================
    # Page 6: Monitoring and Security
    # =========================================================
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(72, 60), "6. Monitoring, Security, and Performance",
                  fontsize=14, fontname="hebo", color=(0, 0, 0))
    sec_text = (
        "Observability and security are cross-cutting concerns that must be addressed at every layer "
        "of the technology stack.\n\n"
        "6.1 Monitoring and Observability\n\n"
        "Prometheus (https://prometheus.io/docs/introduction/overview/) is the industry-standard "
        "open-source monitoring system for cloud-native applications. Its multi-dimensional data model, "
        "powerful query language (PromQL), and pull-based architecture make it ideal for dynamic "
        "containerized environments.\n\n"
        "Grafana (https://grafana.com/docs/grafana/latest/) complements Prometheus by providing rich "
        "visualization dashboards, alerting, and support for multiple data sources. Together, Prometheus "
        "and Grafana form the monitoring stack used by the majority of Kubernetes deployments.\n\n"
        "6.2 Web Security\n\n"
        "The OWASP Top Ten (https://owasp.org/www-project-top-ten/) is the most widely referenced "
        "resource for understanding critical web application security risks. Updated periodically, it "
        "identifies threats such as injection attacks, broken authentication, security misconfiguration, "
        "and server-side request forgery.\n\n"
        "Let's Encrypt (https://letsencrypt.org/docs/) has democratized HTTPS by providing free, "
        "automated TLS certificates. Since its launch, Let's Encrypt has issued over 3 billion "
        "certificates, significantly increasing the percentage of encrypted web traffic.\n\n"
        "Cloudflare's DDoS protection documentation "
        "(https://www.cloudflare.com/learning/ddos/what-is-a-ddos-attack/) provides comprehensive "
        "guidance on understanding and mitigating distributed denial-of-service attacks. As DDoS "
        "attacks grow in both frequency and sophistication, such resources are essential for "
        "operations teams."
    )
    p.insert_textbox(pymupdf.Rect(72, 80, 540, 640), sec_text,
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Links: URLs 18, 19, 20, 21, 22
    add_link(p, pymupdf.Rect(72, 178, 440, 190), URLS[18])
    add_link(p, pymupdf.Rect(72, 258, 410, 270), URLS[19])
    add_link(p, pymupdf.Rect(72, 340, 380, 352), URLS[20])
    add_link(p, pymupdf.Rect(72, 410, 330, 422), URLS[21])
    add_link(p, pymupdf.Rect(72, 478, 540, 490), URLS[22])

    # =========================================================
    # Page 7: Performance and Conclusion
    # =========================================================
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(72, 60), "7. Performance Optimization",
                  fontsize=14, fontname="hebo", color=(0, 0, 0))
    perf_text = (
        "Web performance directly impacts user experience, conversion rates, and search engine "
        "rankings. Google's web.dev performance guide (https://web.dev/performance/) provides "
        "detailed metrics and optimization strategies including Core Web Vitals (LCP, FID, CLS), "
        "code splitting, lazy loading, and image optimization.\n\n"
        "The HTTP Archive (https://httparchive.org/reports/state-of-the-web) maintains a comprehensive "
        "record of how the web is built, tracking metrics across millions of pages including page weight, "
        "request counts, technology adoption, and performance scores over time."
    )
    p.insert_textbox(pymupdf.Rect(72, 80, 540, 300), perf_text,
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Links: URLs 23, 24
    add_link(p, pymupdf.Rect(72, 98, 360, 110), URLS[23])
    add_link(p, pymupdf.Rect(72, 170, 430, 182), URLS[24])

    # Conclusion
    p.insert_text(pymupdf.Point(72, 320), "8. Conclusion",
                  fontsize=14, fontname="hebo", color=(0, 0, 0))
    conclusion_text = (
        "This survey has presented 25 essential web technology references spanning front-end "
        "frameworks, data management, containerization, cloud infrastructure, security, and "
        "performance optimization. The web development ecosystem continues to evolve rapidly, "
        "but the foundational technologies and practices documented here provide a stable base "
        "for building modern, scalable applications.\n\n"
        "As the industry moves toward edge computing, WebAssembly, and AI-assisted development, "
        "understanding these core technologies becomes even more critical. We encourage practitioners "
        "to regularly consult the referenced documentation to stay current with best practices and "
        "emerging capabilities."
    )
    p.insert_textbox(pymupdf.Rect(72, 340, 540, 520), conclusion_text,
                     fontsize=10, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # References section
    p.insert_text(pymupdf.Point(72, 540), "References", fontsize=12, fontname="hebo", color=(0, 0, 0))
    ref_y = 560
    for i, url in enumerate(URLS):
        if ref_y > 760:
            break
        p.insert_text(pymupdf.Point(72, ref_y), f"[{i+1}] {url}",
                      fontsize=7, fontname="cour", color=(0, 0, 0.6))
        ref_y += 9

    # Set metadata
    doc.set_metadata({
        "title": "A Comprehensive Survey of Modern Web Technologies",
        "author": "Dr. Elena Vasquez, Prof. Rajesh Patel, Dr. Mei-Ling Chang",
        "subject": "Web Technology Survey",
        "keywords": "web development, front-end, cloud, security, performance",
        "creator": "Westbrook University CS Department",
        "producer": "PyMuPDF",
    })

    # Set table of contents
    toc = [
        [1, "Abstract", 1],
        [1, "1. Introduction", 1],
        [1, "2. Front-end Technologies and Frameworks", 2],
        [2, "2.1 Runtime Environments", 2],
        [2, "2.2 Component Frameworks", 2],
        [2, "2.3 Type Systems and Build Tools", 2],
        [1, "3. Data Exchange and Storage", 3],
        [2, "3.1 Data Formats and APIs", 3],
        [2, "3.2 Database Technologies", 3],
        [1, "4. Containerization and Orchestration", 4],
        [2, "4.1 Container Platforms", 4],
        [2, "4.2 Orchestration", 4],
        [1, "5. Cloud Infrastructure and IaC", 5],
        [2, "5.1 Cloud Architecture Frameworks", 5],
        [2, "5.2 Infrastructure as Code", 5],
        [1, "6. Monitoring, Security, and Performance", 6],
        [2, "6.1 Monitoring and Observability", 6],
        [2, "6.2 Web Security", 6],
        [1, "7. Performance Optimization", 7],
        [1, "8. Conclusion", 7],
        [1, "References", 7],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
