"""
Initial Setup: Create 4 ODT chapter files for a multi-author technical report.
Task ID: writer_rm_085
Domain: libreoffice_writer

Each author uses slightly different heading styles and fonts.
No master document exists yet.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_085'

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


def create_odt_chapter(filepath, heading1_font, heading2_font, body_font,
                       heading1_size, heading2_size, body_size,
                       title, sections_data):
    """Create an ODT file with custom heading/body styles per author."""
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.text import P, H

    doc = OpenDocumentText()

    # Define Heading 1 style
    h1_style = Style(name="AuthorHeading1", family="paragraph")
    h1_style.addElement(TextProperties(
        fontname=heading1_font,
        fontsize=f"{heading1_size}pt",
        fontweight="bold",
        color="#000000"
    ))
    h1_style.addElement(ParagraphProperties(
        margintop="0.3in",
        marginbottom="0.15in"
    ))
    doc.styles.addElement(h1_style)

    # Define Heading 2 style
    h2_style = Style(name="AuthorHeading2", family="paragraph")
    h2_style.addElement(TextProperties(
        fontname=heading2_font,
        fontsize=f"{heading2_size}pt",
        fontweight="bold",
        fontstyle="italic",
        color="#333333"
    ))
    h2_style.addElement(ParagraphProperties(
        margintop="0.2in",
        marginbottom="0.1in"
    ))
    doc.styles.addElement(h2_style)

    # Define Body Text style
    body_style = Style(name="AuthorBody", family="paragraph")
    body_style.addElement(TextProperties(
        fontname=body_font,
        fontsize=f"{body_size}pt",
        color="#000000"
    ))
    body_style.addElement(ParagraphProperties(
        margintop="0.05in",
        marginbottom="0.05in"
    ))
    doc.styles.addElement(body_style)

    # Add chapter title (Heading 1)
    h = H(outlinelevel=1, stylename=h1_style, text=title)
    doc.text.addElement(h)

    # Add sections
    for section_title, paragraphs in sections_data:
        h2 = H(outlinelevel=2, stylename=h2_style, text=section_title)
        doc.text.addElement(h2)
        for para_text in paragraphs:
            p = P(stylename=body_style, text=para_text)
            doc.text.addElement(p)

    doc.save(filepath)
    print(f"Created: {filepath}")


def create_initial():
    # Chapter 1: Chen - Networking (Arial-based)
    create_odt_chapter(
        filepath=os.path.join(WORKDIR, "Chen_Networking.odt"),
        heading1_font="Arial", heading2_font="Arial", body_font="Arial",
        heading1_size=18, heading2_size=14, body_size=11,
        title="Chapter 1: Network Architecture and Protocols",
        sections_data=[
            ("1.1 TCP/IP Stack Overview", [
                "Modern network architectures rely heavily on the TCP/IP protocol stack, which provides reliable end-to-end communication across heterogeneous networks. The layered approach allows each protocol to operate independently while maintaining interoperability.",
                "The transport layer, primarily governed by TCP and UDP, handles segmentation, flow control, and error recovery. TCP's three-way handshake ensures connection establishment before data transfer begins, while UDP offers lightweight, connectionless communication for latency-sensitive applications.",
                "Recent advances in QUIC protocol have challenged traditional TCP dominance by combining transport and encryption layers, reducing connection setup latency from three round-trips to just one."
            ]),
            ("1.2 Software-Defined Networking", [
                "Software-Defined Networking (SDN) separates the control plane from the data plane, enabling centralized network management through programmable controllers. OpenFlow, the most widely adopted SDN protocol, provides a standardized interface between controllers and switches.",
                "The benefits of SDN include simplified network configuration, improved traffic engineering, and the ability to implement complex policies through software rather than hardware-specific configurations.",
                "Enterprise adoption of SDN has accelerated with the rise of cloud computing, where dynamic workload placement requires flexible network topology management."
            ]),
            ("1.3 Network Security Considerations", [
                "Network security remains a critical concern as attack surfaces expand with IoT and edge computing deployments. Zero-trust architectures have emerged as a response, requiring authentication and authorization for every network access request regardless of source location.",
                "Encryption at the network layer using IPsec or at the transport layer using TLS 1.3 provides confidentiality and integrity guarantees. Certificate management and key rotation policies must be carefully designed to prevent single points of failure."
            ])
        ]
    )

    # Chapter 2: Patel - Security (Times New Roman-based)
    create_odt_chapter(
        filepath=os.path.join(WORKDIR, "Patel_Security.odt"),
        heading1_font="Times New Roman", heading2_font="Times New Roman", body_font="Times New Roman",
        heading1_size=20, heading2_size=15, body_size=12,
        title="Chapter 2: Cybersecurity Frameworks and Practices",
        sections_data=[
            ("2.1 Threat Landscape Analysis", [
                "The cybersecurity threat landscape has evolved dramatically over the past decade. Advanced Persistent Threats (APTs) represent state-sponsored or highly organized groups that conduct prolonged, targeted attacks against specific organizations or industries.",
                "Ransomware attacks have become increasingly sophisticated, with double-extortion tactics where attackers both encrypt data and threaten to release sensitive information publicly. The average ransom payment exceeded $800,000 in 2024, with recovery costs often exceeding $4.5 million.",
                "Supply chain attacks, exemplified by the SolarWinds compromise, highlight the need for comprehensive vendor risk management and software bill of materials (SBOM) tracking."
            ]),
            ("2.2 Authentication and Access Control", [
                "Multi-factor authentication (MFA) has become a baseline security requirement. Modern implementations combine knowledge factors (passwords), possession factors (hardware tokens or mobile devices), and inherence factors (biometrics) to create robust identity verification.",
                "Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC) provide structured approaches to authorization. ABAC offers finer granularity by evaluating multiple attributes including user role, resource type, time of access, and environmental conditions."
            ]),
            ("2.3 Incident Response Planning", [
                "Effective incident response requires a documented plan covering detection, containment, eradication, recovery, and post-incident analysis. Organizations should conduct tabletop exercises quarterly and full-scale simulations annually.",
                "Security Operations Centers (SOCs) serve as the frontline defense, utilizing SIEM tools to correlate events across disparate systems. The mean time to detect (MTTD) and mean time to respond (MTTR) are key performance indicators for SOC effectiveness.",
                "Digital forensics capabilities ensure evidence preservation for potential legal proceedings while enabling root cause analysis to prevent recurrence of similar incidents."
            ])
        ]
    )

    # Chapter 3: Garcia - Database (Courier New-based)
    create_odt_chapter(
        filepath=os.path.join(WORKDIR, "Garcia_Database.odt"),
        heading1_font="Courier New", heading2_font="Courier New", body_font="Courier New",
        heading1_size=16, heading2_size=13, body_size=10,
        title="Chapter 3: Database Systems and Data Management",
        sections_data=[
            ("3.1 Relational Database Design", [
                "Relational database design follows normalization principles to minimize redundancy and dependency anomalies. Third Normal Form (3NF) eliminates transitive dependencies, while Boyce-Codd Normal Form (BCNF) addresses additional edge cases involving candidate keys.",
                "Index design significantly impacts query performance. B-tree indexes support range queries efficiently, while hash indexes provide O(1) lookup for equality predicates. Covering indexes that include all columns referenced by a query eliminate the need for table lookups entirely.",
                "Partitioning strategies, including horizontal partitioning (sharding) and vertical partitioning, enable databases to scale beyond single-server capacity. Consistent hashing algorithms distribute data evenly while minimizing redistribution during cluster changes."
            ]),
            ("3.2 NoSQL and NewSQL Systems", [
                "NoSQL databases address limitations of relational systems for specific workloads. Document stores like MongoDB offer schema flexibility, key-value stores like Redis provide sub-millisecond latency, and graph databases like Neo4j excel at relationship-heavy queries.",
                "The CAP theorem dictates that distributed systems can guarantee at most two of three properties: consistency, availability, and partition tolerance. Most modern systems offer tunable consistency levels, allowing applications to choose the appropriate trade-off.",
                "NewSQL systems like CockroachDB and Google Spanner aim to combine the scalability of NoSQL with ACID transaction guarantees, using distributed consensus protocols like Raft or Paxos."
            ]),
            ("3.3 Data Pipeline Architecture", [
                "Modern data pipelines follow the Extract-Transform-Load (ETL) or Extract-Load-Transform (ELT) paradigm. Cloud-native ELT approaches leverage the processing power of data warehouses like Snowflake or BigQuery, pushing transformations closer to the data.",
                "Stream processing frameworks such as Apache Kafka Streams and Apache Flink enable real-time data processing with exactly-once semantics. Event-driven architectures built on these frameworks support complex event processing and real-time analytics."
            ])
        ]
    )

    # Chapter 4: Kim - Frontend (Liberation Sans-based)
    create_odt_chapter(
        filepath=os.path.join(WORKDIR, "Kim_Frontend.odt"),
        heading1_font="Liberation Sans", heading2_font="Liberation Sans", body_font="Liberation Sans",
        heading1_size=19, heading2_size=14, body_size=11,
        title="Chapter 4: Frontend Architecture and User Experience",
        sections_data=[
            ("4.1 Component-Based Architecture", [
                "Modern frontend development centers on component-based architecture, where user interfaces are composed of reusable, self-contained components. React, Vue, and Angular each implement this paradigm with different philosophies regarding state management and rendering strategies.",
                "Server-side rendering (SSR) and static site generation (SSG) frameworks like Next.js and Nuxt.js improve initial page load performance and search engine optimization. Hybrid approaches allow developers to choose rendering strategy per route.",
                "Web Components, the browser-native component model, provide framework-agnostic encapsulation through Shadow DOM, Custom Elements, and HTML Templates. Adoption is growing as browser support matures and interoperability becomes increasingly important."
            ]),
            ("4.2 State Management Patterns", [
                "Application state management remains one of the most challenging aspects of frontend development. Flux architecture and its derivatives (Redux, Vuex, NgRx) provide unidirectional data flow, making state changes predictable and debuggable.",
                "Server state management libraries like React Query and SWR simplify data fetching by providing caching, background refetching, and optimistic updates. These tools reduce the need for complex client-side state management for data that originates from APIs."
            ]),
            ("4.3 Performance Optimization", [
                "Frontend performance optimization encompasses multiple strategies: code splitting reduces initial bundle size, lazy loading defers non-critical resources, and tree shaking eliminates unused code during the build process.",
                "Core Web Vitals (LCP, FID, CLS) provide standardized metrics for measuring user experience. Largest Contentful Paint should occur within 2.5 seconds, First Input Delay should be under 100 milliseconds, and Cumulative Layout Shift should remain below 0.1.",
                "Progressive Web Applications (PWAs) leverage service workers for offline capability, push notifications for re-engagement, and web app manifests for installability, bridging the gap between web and native mobile experiences."
            ])
        ]
    )

    print(f"All 4 chapter files created in {WORKDIR}")

    # Open a file manager to show the files, and also open one chapter for context
    launch_gui(f'nautilus "{WORKDIR}"', delay_sec=2.0)
    print('GUI_READY: launched file manager with DISPLAY=:0')


create_initial()
