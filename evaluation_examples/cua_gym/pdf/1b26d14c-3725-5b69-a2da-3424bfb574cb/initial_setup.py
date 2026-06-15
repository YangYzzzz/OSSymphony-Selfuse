"""
Initial Setup: Create a reviewed PDF with various annotations
Task ID: pdf_cr_054
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'pdf_cr_054'
OUTPUT = f'{DESKTOP}/reviewed.pdf'


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
    os.makedirs(DESKTOP, exist_ok=True)

    # Remove any pre-existing annotation_report.txt (must NOT exist in initial)
    report_path = f'{DESKTOP}/annotation_report.txt'
    if os.path.exists(report_path):
        os.remove(report_path)

    # Create a multi-page PDF with realistic content
    doc = pymupdf.open()

    # --- Page 1: Project Status Report ---
    page1 = doc.new_page(width=595, height=842)
    page1.insert_text(pymupdf.Point(72, 60), "Quarterly Project Status Report", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))
    page1.insert_text(pymupdf.Point(72, 90), "Prepared by: Engineering Division", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page1.insert_text(pymupdf.Point(72, 110), "Date: March 15, 2025", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))

    # Draw a separator line
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(72, 125), pymupdf.Point(523, 125))
    shape1.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape1.commit()

    section1 = (
        "1. Executive Summary\n\n"
        "The Aurora Platform migration project has reached a critical milestone this quarter. "
        "All core backend services have been successfully containerized and deployed to the new "
        "Kubernetes cluster. The team completed 87% of planned deliverables, exceeding the target "
        "of 80%. Performance benchmarks show a 34% improvement in API response times compared to "
        "the legacy monolithic architecture.\n\n"
        "Key challenges remain in the data migration pipeline, particularly around the conversion "
        "of legacy XML-based configurations to the new YAML format. The estimated completion date "
        "for full migration is now June 30, 2025, representing a two-week delay from the original "
        "timeline due to unexpected schema incompatibilities discovered during integration testing."
    )
    page1.insert_textbox(pymupdf.Rect(72, 140, 523, 400), section1, fontsize=11, fontname="helv", color=(0, 0, 0))

    section1b = (
        "2. Resource Allocation\n\n"
        "Current team composition includes 12 full-time engineers, 3 DevOps specialists, and "
        "2 QA leads. Budget utilization stands at 72% with $1.2M remaining from the allocated "
        "$4.3M annual budget. Hardware procurement for the staging environment cluster was "
        "completed under budget at $340,000 versus the estimated $425,000.\n\n"
        "The hiring pipeline for two additional senior backend engineers is progressing, with "
        "final-round interviews scheduled for the first week of April. Contractor engagement "
        "for the security audit has been approved and will commence on April 15, 2025."
    )
    page1.insert_textbox(pymupdf.Rect(72, 410, 523, 680), section1b, fontsize=11, fontname="helv", color=(0, 0, 0))

    section1c = (
        "3. Risk Assessment\n\n"
        "Three high-priority risks have been identified: dependency on the deprecated OAuth 1.0 "
        "library which reaches end-of-life in Q3 2025, potential capacity constraints during peak "
        "load scenarios exceeding 50,000 concurrent users, and the unresolved licensing dispute "
        "with the GeoSpatial data provider affecting the mapping module."
    )
    page1.insert_textbox(pymupdf.Rect(72, 690, 523, 820), section1c, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 2: Technical Details ---
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text(pymupdf.Point(72, 60), "4. Technical Architecture Review", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    tech_text = (
        "The revised architecture employs a microservices pattern with 14 independently "
        "deployable services communicating via gRPC and Apache Kafka event streams. Each service "
        "maintains its own PostgreSQL database instance, enforcing strict bounded contexts.\n\n"
        "Service mesh implementation using Istio provides automatic mTLS encryption between "
        "services, circuit breaking, and distributed tracing through Jaeger integration. The "
        "observability stack includes Prometheus for metrics collection, Grafana for dashboarding, "
        "and the ELK stack for centralized logging.\n\n"
        "The API gateway layer, built on Kong, handles rate limiting, authentication token "
        "validation, and request routing. Current throughput capacity is measured at 12,000 "
        "requests per second under synthetic load testing conditions."
    )
    page2.insert_textbox(pymupdf.Rect(72, 80, 523, 320), tech_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(72, 340), "5. Deployment Pipeline Metrics", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    deploy_text = (
        "The CI/CD pipeline processes an average of 47 deployments per week across all "
        "environments. Mean time to production for a committed change is 2.3 hours, down from "
        "8.7 hours in the previous quarter. Rollback frequency has decreased to 3.2% of "
        "deployments, compared to 11.5% during the initial migration phase.\n\n"
        "Automated test coverage has improved to 89% for unit tests and 76% for integration "
        "tests. The end-to-end test suite covers 42 critical user journeys and executes in "
        "approximately 18 minutes on the parallel test infrastructure."
    )
    page2.insert_textbox(pymupdf.Rect(72, 360, 523, 560), deploy_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    page2.insert_text(pymupdf.Point(72, 580), "6. Security Compliance", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    security_text = (
        "SOC 2 Type II audit preparation is 65% complete. All critical findings from the "
        "preliminary assessment have been remediated. Remaining items include documentation "
        "of incident response procedures and completion of the vendor risk assessment for "
        "three new SaaS integrations added during the migration.\n\n"
        "Vulnerability scanning using Snyk and Trivy has been integrated into the build "
        "pipeline. Zero critical CVEs remain unpatched in production dependencies. Four medium "
        "severity findings are scheduled for remediation in the next sprint cycle."
    )
    page2.insert_textbox(pymupdf.Rect(72, 600, 523, 810), security_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 3: Financial Summary and Next Steps ---
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text(pymupdf.Point(72, 60), "7. Financial Summary", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    fin_text = (
        "Total expenditure for Q1 2025: $1,087,500. This includes personnel costs of $892,000, "
        "infrastructure expenses of $143,500, and tooling/licensing costs of $52,000. The "
        "projected annual run rate remains within the approved $4.3M budget envelope.\n\n"
        "Cost optimization initiatives have yielded a 22% reduction in cloud compute costs "
        "through right-sizing of underutilized instances and implementation of spot instance "
        "strategies for non-critical workloads. Annual savings are estimated at $186,000."
    )
    page3.insert_textbox(pymupdf.Rect(72, 80, 523, 280), fin_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    page3.insert_text(pymupdf.Point(72, 300), "8. Action Items and Next Steps", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))

    action_text = (
        "Priority action items for Q2 2025:\n\n"
        "a) Complete data migration pipeline validation by April 30\n"
        "b) Finalize OAuth 2.0 library upgrade across all services by May 15\n"
        "c) Execute full-scale load testing simulating 75,000 concurrent users\n"
        "d) Submit SOC 2 Type II audit documentation package by June 1\n"
        "e) Onboard two senior backend engineers and integrate into sprint teams\n"
        "f) Resolve GeoSpatial data provider licensing by May 31\n"
        "g) Deploy canary release framework for production traffic management\n\n"
        "The next project review is scheduled for June 20, 2025. All workstream leads are "
        "expected to provide updated status reports by June 15."
    )
    page3.insert_textbox(pymupdf.Rect(72, 320, 523, 620), action_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # Save the base document first
    doc.save(OUTPUT)
    doc.close()

    # Re-open and add annotations
    doc = pymupdf.open(OUTPUT)

    # --- Page 1 Annotations ---
    p1 = doc[0]

    # Annotation 1: Highlight "87%" on page 1 in yellow
    instances = p1.search_for("87% of planned deliverables")
    if instances:
        annot = p1.add_highlight_annot(instances[0])
        annot.set_colors(stroke=(1, 1, 0))  # yellow
        annot.set_info(content="Excellent achievement rate")
        annot.update()

    # Annotation 2: Sticky note about the delay
    annot = p1.add_text_annot(
        pymupdf.Point(500, 350),
        "Need to discuss the two-week delay with stakeholders",
        icon="Note"
    )
    annot.set_colors(stroke=(1, 0.65, 0))  # orange
    annot.update()

    # Annotation 3: Rectangle around Risk Assessment section header
    annot = p1.add_rect_annot(pymupdf.Rect(65, 685, 280, 710))
    annot.set_colors(stroke=(1, 0, 0))  # red
    annot.set_border(width=2)
    annot.set_info(content="High priority section")
    annot.update()

    # Annotation 4: Underline "deprecated OAuth 1.0"
    instances = p1.search_for("deprecated OAuth 1.0")
    if instances:
        annot = p1.add_underline_annot(instances[0])
        annot.set_colors(stroke=(0, 0, 1))  # blue
        annot.set_info(content="Urgent: library reaches EOL soon")
        annot.update()

    # --- Page 2 Annotations ---
    p2 = doc[1]

    # Annotation 5: Highlight "12,000 requests per second" in green
    instances = p2.search_for("12,000 requests per second")
    if instances:
        annot = p2.add_highlight_annot(instances[0])
        annot.set_colors(stroke=(0, 1, 0))  # green
        annot.set_info(content="Impressive throughput metric")
        annot.update()

    # Annotation 6: Sticky note about test coverage
    annot = p2.add_text_annot(
        pymupdf.Point(480, 480),
        "Target is 95% unit test coverage by Q3",
        icon="Comment"
    )
    annot.set_colors(stroke=(0, 0, 1))  # blue
    annot.update()

    # Annotation 7: Rectangle around "Zero critical CVEs"
    instances = p2.search_for("Zero critical CVEs")
    if instances:
        annot = p2.add_rect_annot(pymupdf.Rect(instances[0].x0 - 3, instances[0].y0 - 3,
                                                  instances[0].x1 + 3, instances[0].y1 + 3))
        annot.set_colors(stroke=(0, 0.5, 0))  # dark green
        annot.set_border(width=1.5)
        annot.set_info(content="Good security posture")
        annot.update()

    # Annotation 8: Underline "SOC 2 Type II"
    instances = p2.search_for("SOC 2 Type II")
    if instances:
        annot = p2.add_underline_annot(instances[0])
        annot.set_colors(stroke=(0.5, 0, 0.5))  # purple
        annot.set_info(content="Compliance deadline approaching")
        annot.update()

    # --- Page 3 Annotations ---
    p3 = doc[2]

    # Annotation 9: Highlight "$186,000" savings in yellow
    instances = p3.search_for("$186,000")
    if instances:
        annot = p3.add_highlight_annot(instances[0])
        annot.set_colors(stroke=(1, 1, 0))  # yellow
        annot.set_info(content="Significant cost savings")
        annot.update()

    # Annotation 10: Sticky note about load testing
    annot = p3.add_text_annot(
        pymupdf.Point(490, 430),
        "Coordinate with infrastructure team for load test scheduling",
        icon="Note"
    )
    annot.set_colors(stroke=(1, 0, 0))  # red
    annot.update()

    # Annotation 11: Underline "June 20, 2025"
    instances = p3.search_for("June 20, 2025")
    if instances:
        annot = p3.add_underline_annot(instances[0])
        annot.set_colors(stroke=(0, 0, 0))  # black
        annot.set_info(content="Calendar reminder set")
        annot.update()

    doc.save(OUTPUT, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
