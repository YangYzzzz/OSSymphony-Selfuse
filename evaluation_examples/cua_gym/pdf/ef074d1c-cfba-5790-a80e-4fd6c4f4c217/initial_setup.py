"""
Initial Setup: Create two versions of a technical specification PDF for structural comparison.
Task ID: pdf_cr_080
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DESKTOP = f'{WORKDIR}/Desktop'
TASK_ID = 'pdf_cr_080'
V1_PATH = f'{DESKTOP}/spec_v1.pdf'
V2_PATH = f'{DESKTOP}/spec_v2.pdf'


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


def create_v1():
    """Create spec_v1.pdf - Technical Specification v1 (8 pages)."""
    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 200), "CloudSync Platform", fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 240), "Technical Specification Document", fontsize=18, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 280), "Version 1.0", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 320), "Prepared by: Engineering Division", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 345), "Date: March 15, 2025", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 370), "Status: Draft", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    # Add a line separator
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 160), pymupdf.Point(540, 160))
    shape.finish(color=(0.1, 0.1, 0.4), width=2)
    shape.commit()
    # External link on title page
    page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(72, 400, 300, 420), "uri": "https://cloudsync.example.com/docs"})
    page.insert_text(pymupdf.Point(72, 415), "Documentation Portal", fontsize=10, fontname="helv", color=(0, 0, 0.8))

    # --- Page 2: Table of Contents ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Table of Contents", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    toc_entries = [
        "1. Introduction ....................................... 3",
        "2. System Architecture ................................ 4",
        "3. API Reference ...................................... 5",
        "4. Security Protocols ................................. 6",
        "5. Data Models ........................................ 7",
        "6. Deployment Guide ................................... 8",
    ]
    y = 110
    for entry in toc_entries:
        page.insert_text(pymupdf.Point(90, y), entry, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 22

    # --- Page 3: Introduction ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "1. Introduction", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    intro_text = (
        "CloudSync Platform is a distributed cloud synchronization service designed to provide "
        "real-time data replication across geographically dispersed data centers. The platform "
        "supports both structured and unstructured data formats with guaranteed consistency levels "
        "ranging from eventual to strong consistency.\n\n"
        "The system is built on a microservices architecture using Kubernetes for orchestration "
        "and employs Apache Kafka for event streaming. All inter-service communication is secured "
        "via mutual TLS authentication.\n\n"
        "Key features include:\n"
        "- Real-time bidirectional sync across up to 12 regions\n"
        "- Automatic conflict resolution using vector clocks\n"
        "- Sub-millisecond latency for intra-region operations\n"
        "- 99.99% availability SLA with automatic failover"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 500), intro_text, fontsize=11, fontname="helv", color=(0, 0, 0))
    # Add a highlight annotation on this page
    instances = page.search_for("mutual TLS authentication")
    for inst in instances:
        annot = page.add_highlight_annot(inst)
        annot.set_colors(stroke=(1, 1, 0))
        annot.update()
    # Add a sticky note
    annot = page.add_text_annot(pymupdf.Point(500, 100), "Review this section for accuracy", icon="Note")
    annot.set_colors(stroke=(1, 0.8, 0))
    annot.update()
    # Internal link text (link added after all pages exist)
    page.insert_text(pymupdf.Point(72, 525), "See: System Architecture (next page)", fontsize=10, fontname="heit", color=(0, 0, 0.7))

    # --- Page 4: System Architecture ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "2. System Architecture", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    arch_text = (
        "The CloudSync architecture follows a layered design pattern:\n\n"
        "Layer 1 - Gateway: HAProxy load balancers distribute incoming traffic across "
        "the API gateway cluster running Envoy proxies.\n\n"
        "Layer 2 - Services: Core business logic is implemented as stateless microservices "
        "deployed in Kubernetes pods. Services include SyncEngine, ConflictResolver, "
        "MetadataManager, and DataRouter.\n\n"
        "Layer 3 - Messaging: Apache Kafka brokers handle all asynchronous communication "
        "between services using topic-based publish-subscribe patterns.\n\n"
        "Layer 4 - Storage: PostgreSQL for metadata, Apache Cassandra for distributed "
        "data storage, and Redis for caching and session management."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 450), arch_text, fontsize=11, fontname="helv", color=(0, 0, 0))
    # Draw a simple architecture diagram placeholder box
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(100, 480, 500, 700))
    shape.finish(color=(0.5, 0.5, 0.5), fill=(0.95, 0.95, 0.95), width=1)
    shape.commit()
    page.insert_text(pymupdf.Point(220, 600), "[Architecture Diagram]", fontsize=14, fontname="heit", color=(0.5, 0.5, 0.5))

    # --- Page 5: API Reference ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "3. API Reference", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    api_text = (
        "POST /api/v1/sync/initiate\n"
        "  Description: Initiates a new synchronization session\n"
        "  Parameters: source_region (string), target_region (string),\n"
        "              data_type (string), consistency_level (string)\n"
        "  Response: 200 OK with session_id\n\n"
        "GET /api/v1/sync/status/{session_id}\n"
        "  Description: Returns current sync status\n"
        "  Response: 200 OK with status object\n\n"
        "DELETE /api/v1/sync/{session_id}\n"
        "  Description: Cancels an active sync session\n"
        "  Response: 204 No Content\n\n"
        "PUT /api/v1/config/region\n"
        "  Description: Updates region configuration\n"
        "  Parameters: region_id (string), settings (object)\n"
        "  Response: 200 OK"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 550), api_text, fontsize=10, fontname="cour", color=(0, 0, 0))
    # URI link
    page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(72, 560, 350, 580), "uri": "https://api.cloudsync.example.com/swagger"})
    page.insert_text(pymupdf.Point(72, 575), "Full API Documentation (Swagger)", fontsize=10, fontname="helv", color=(0, 0, 0.8))

    # --- Page 6: Security Protocols ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "4. Security Protocols", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    sec_text = (
        "Authentication:\n"
        "All API requests require OAuth 2.0 bearer tokens issued by the CloudSync Identity "
        "Provider. Token lifetime is configurable (default: 3600 seconds).\n\n"
        "Encryption:\n"
        "- Data in transit: TLS 1.3 with AES-256-GCM cipher suite\n"
        "- Data at rest: AES-256-CBC with per-tenant key rotation every 90 days\n"
        "- Key management: HashiCorp Vault with auto-unseal via AWS KMS\n\n"
        "Access Control:\n"
        "Role-based access control (RBAC) with predefined roles:\n"
        "  - Admin: Full platform management\n"
        "  - Operator: Sync operations and monitoring\n"
        "  - Viewer: Read-only dashboard access\n"
        "  - Auditor: Compliance and audit log access"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 500), sec_text, fontsize=11, fontname="helv", color=(0, 0, 0))
    # Underline annotation
    instances = page.search_for("TLS 1.3 with AES-256-GCM")
    for inst in instances:
        annot = page.add_underline_annot(inst)
        annot.update()

    # --- Page 7: Data Models ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "5. Data Models", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    dm_text = (
        "SyncRecord Schema:\n"
        "  record_id: UUID (primary key)\n"
        "  source_region: VARCHAR(64)\n"
        "  target_region: VARCHAR(64)\n"
        "  data_hash: CHAR(64) - SHA-256\n"
        "  created_at: TIMESTAMP WITH TIME ZONE\n"
        "  updated_at: TIMESTAMP WITH TIME ZONE\n"
        "  status: ENUM('pending','active','completed','failed')\n"
        "  retry_count: INTEGER DEFAULT 0\n\n"
        "ConflictLog Schema:\n"
        "  conflict_id: UUID (primary key)\n"
        "  record_id: UUID (foreign key -> SyncRecord)\n"
        "  conflict_type: VARCHAR(32)\n"
        "  resolution_strategy: VARCHAR(32)\n"
        "  resolved_at: TIMESTAMP WITH TIME ZONE\n"
        "  resolution_details: JSONB"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 500), dm_text, fontsize=10, fontname="cour", color=(0, 0, 0))

    # --- Page 8: Deployment Guide ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "6. Deployment Guide", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    deploy_text = (
        "Prerequisites:\n"
        "- Kubernetes cluster v1.28+ with minimum 6 worker nodes\n"
        "- Helm v3.12+ installed\n"
        "- PostgreSQL 15+ with replication enabled\n"
        "- Apache Kafka 3.5+ cluster with 3+ brokers\n\n"
        "Installation Steps:\n"
        "1. Clone the deployment repository\n"
        "2. Configure environment variables in values.yaml\n"
        "3. Run: helm install cloudsync ./charts/cloudsync\n"
        "4. Verify pods: kubectl get pods -n cloudsync\n"
        "5. Run health check: curl http://gateway:8080/healthz\n\n"
        "Monitoring:\n"
        "Prometheus metrics are exposed on port 9090. Grafana dashboards are "
        "available in the monitoring/ directory of the repository."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 500), deploy_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # Form field on the last page - a feedback text field
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "reviewer_name"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 550, 450, 575)
    widget.text_fontsize = 11
    widget.fill_color = (0.95, 0.95, 0.95)
    widget.border_color = (0.3, 0.3, 0.3)
    page.add_widget(widget)
    page.insert_text(pymupdf.Point(72, 568), "Reviewer Name:", fontsize=11, fontname="hebo", color=(0, 0, 0))

    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    widget.field_name = "approved"
    widget.field_value = "Off"
    widget.rect = pymupdf.Rect(200, 590, 220, 610)
    widget.border_color = (0, 0, 0)
    page.add_widget(widget)
    page.insert_text(pymupdf.Point(72, 605), "Approved:", fontsize=11, fontname="hebo", color=(0, 0, 0))

    # Add internal links now that all pages exist
    doc[2].insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(72, 510, 300, 530), "page": 3, "to": pymupdf.Point(72, 72)})

    # Set TOC
    toc = [
        [1, "Introduction", 3],
        [1, "System Architecture", 4],
        [1, "API Reference", 5],
        [1, "Security Protocols", 6],
        [1, "Data Models", 7],
        [1, "Deployment Guide", 8],
    ]
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "CloudSync Platform Technical Specification",
        "author": "Elena Rodriguez",
        "subject": "Technical Specification",
        "keywords": "cloudsync, distributed, synchronization, API",
        "creator": "CloudSync Engineering",
        "producer": "PyMuPDF",
    })

    doc.save(V1_PATH)
    doc.close()
    print(f'Created: {V1_PATH}')


def create_v2():
    """Create spec_v2.pdf - Technical Specification v2 (9 pages) with various differences."""
    doc = pymupdf.open()

    # --- Page 1: Title Page (modified metadata, version) ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 200), "CloudSync Platform", fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 240), "Technical Specification Document", fontsize=18, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 280), "Version 2.0", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 320), "Prepared by: Engineering Division", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 345), "Date: June 20, 2025", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 370), "Status: Final", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 160), pymupdf.Point(540, 160))
    shape.finish(color=(0.1, 0.1, 0.4), width=2)
    shape.commit()
    # Same link as v1
    page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(72, 400, 300, 420), "uri": "https://cloudsync.example.com/docs"})
    page.insert_text(pymupdf.Point(72, 415), "Documentation Portal", fontsize=10, fontname="helv", color=(0, 0, 0.8))
    # NEW link in v2
    page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(72, 430, 300, 450), "uri": "https://cloudsync.example.com/changelog"})
    page.insert_text(pymupdf.Point(72, 445), "Changelog", fontsize=10, fontname="helv", color=(0, 0, 0.8))

    # --- Page 2: Table of Contents (updated with new section) ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "Table of Contents", fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.4))
    toc_entries = [
        "1. Introduction ....................................... 3",
        "2. System Architecture ................................ 4",
        "3. API Reference ...................................... 5",
        "4. Security Protocols ................................. 6",
        "5. Data Models ........................................ 7",
        "6. Performance Benchmarks ............................. 8",
        "7. Deployment Guide ................................... 9",
    ]
    y = 110
    for entry in toc_entries:
        page.insert_text(pymupdf.Point(90, y), entry, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 22

    # --- Page 3: Introduction (modified text) ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "1. Introduction", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    intro_text = (
        "CloudSync Platform is a next-generation distributed cloud synchronization service "
        "designed to provide real-time data replication across geographically dispersed data "
        "centers. The platform supports both structured and unstructured data formats with "
        "guaranteed consistency levels ranging from eventual to strong consistency.\n\n"
        "The system is built on a microservices architecture using Kubernetes for orchestration "
        "and employs Apache Kafka for event streaming. All inter-service communication is secured "
        "via mutual TLS authentication with certificate pinning.\n\n"
        "Key features include:\n"
        "- Real-time bidirectional sync across up to 24 regions\n"
        "- Automatic conflict resolution using hybrid logical clocks\n"
        "- Sub-millisecond latency for intra-region operations\n"
        "- 99.999% availability SLA with automatic failover\n"
        "- Built-in data compression reducing bandwidth by up to 60%"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 520), intro_text, fontsize=11, fontname="helv", color=(0, 0, 0))
    # Different annotations: highlight annotation on different text
    instances = page.search_for("certificate pinning")
    for inst in instances:
        annot = page.add_highlight_annot(inst)
        annot.set_colors(stroke=(1, 1, 0))
        annot.update()
    # Sticky note with different text
    annot = page.add_text_annot(pymupdf.Point(500, 100), "Updated for v2.0 release", icon="Note")
    annot.set_colors(stroke=(0, 0.8, 0))
    annot.update()
    # Additional freetext annotation in v2
    annot = page.add_freetext_annot(
        pymupdf.Rect(72, 530, 350, 560),
        "NEW: Added compression feature details",
        fontsize=9, fontname="helv",
        text_color=(0, 0.4, 0), fill_color=(0.9, 1, 0.9),
    )
    annot.update()
    # Internal link text (link added after all pages exist)
    page.insert_text(pymupdf.Point(72, 585), "See: System Architecture (next page)", fontsize=10, fontname="heit", color=(0, 0, 0.7))

    # --- Page 4: System Architecture (same as v1) ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "2. System Architecture", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    arch_text = (
        "The CloudSync architecture follows a layered design pattern:\n\n"
        "Layer 1 - Gateway: HAProxy load balancers distribute incoming traffic across "
        "the API gateway cluster running Envoy proxies.\n\n"
        "Layer 2 - Services: Core business logic is implemented as stateless microservices "
        "deployed in Kubernetes pods. Services include SyncEngine, ConflictResolver, "
        "MetadataManager, and DataRouter.\n\n"
        "Layer 3 - Messaging: Apache Kafka brokers handle all asynchronous communication "
        "between services using topic-based publish-subscribe patterns.\n\n"
        "Layer 4 - Storage: PostgreSQL for metadata, Apache Cassandra for distributed "
        "data storage, and Redis for caching and session management."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 450), arch_text, fontsize=11, fontname="helv", color=(0, 0, 0))
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(100, 480, 500, 700))
    shape.finish(color=(0.5, 0.5, 0.5), fill=(0.95, 0.95, 0.95), width=1)
    shape.commit()
    page.insert_text(pymupdf.Point(220, 600), "[Architecture Diagram]", fontsize=14, fontname="heit", color=(0.5, 0.5, 0.5))

    # --- Page 5: API Reference (modified - added new endpoint) ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "3. API Reference", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    api_text = (
        "POST /api/v2/sync/initiate\n"
        "  Description: Initiates a new synchronization session\n"
        "  Parameters: source_region (string), target_region (string),\n"
        "              data_type (string), consistency_level (string),\n"
        "              compression (boolean, default: true)\n"
        "  Response: 200 OK with session_id\n\n"
        "GET /api/v2/sync/status/{session_id}\n"
        "  Description: Returns current sync status\n"
        "  Response: 200 OK with status object\n\n"
        "DELETE /api/v2/sync/{session_id}\n"
        "  Description: Cancels an active sync session\n"
        "  Response: 204 No Content\n\n"
        "PUT /api/v2/config/region\n"
        "  Description: Updates region configuration\n"
        "  Parameters: region_id (string), settings (object)\n"
        "  Response: 200 OK\n\n"
        "GET /api/v2/metrics/performance\n"
        "  Description: Returns real-time performance metrics\n"
        "  Response: 200 OK with metrics object"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 600), api_text, fontsize=10, fontname="cour", color=(0, 0, 0))
    page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(72, 610, 350, 630), "uri": "https://api.cloudsync.example.com/v2/swagger"})
    page.insert_text(pymupdf.Point(72, 625), "Full API Documentation (Swagger v2)", fontsize=10, fontname="helv", color=(0, 0, 0.8))

    # --- Page 6: Security Protocols (modified) ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "4. Security Protocols", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    sec_text = (
        "Authentication:\n"
        "All API requests require OAuth 2.0 bearer tokens issued by the CloudSync Identity "
        "Provider. Token lifetime is configurable (default: 1800 seconds). Refresh tokens "
        "are now supported for seamless session management.\n\n"
        "Encryption:\n"
        "- Data in transit: TLS 1.3 with AES-256-GCM cipher suite\n"
        "- Data at rest: AES-256-GCM with per-tenant key rotation every 30 days\n"
        "- Key management: HashiCorp Vault with auto-unseal via AWS KMS\n"
        "- Client-side encryption: Optional end-to-end encryption for sensitive payloads\n\n"
        "Access Control:\n"
        "Role-based access control (RBAC) with predefined roles:\n"
        "  - Admin: Full platform management\n"
        "  - Operator: Sync operations and monitoring\n"
        "  - Developer: API access and testing\n"
        "  - Viewer: Read-only dashboard access\n"
        "  - Auditor: Compliance and audit log access"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 540), sec_text, fontsize=11, fontname="helv", color=(0, 0, 0))
    instances = page.search_for("TLS 1.3 with AES-256-GCM")
    for inst in instances:
        annot = page.add_underline_annot(inst)
        annot.update()
    # Additional annotation in v2
    instances = page.search_for("end-to-end encryption")
    for inst in instances:
        annot = page.add_highlight_annot(inst)
        annot.set_colors(stroke=(0, 1, 0))
        annot.update()

    # --- Page 7: Data Models (same as v1) ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "5. Data Models", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    dm_text = (
        "SyncRecord Schema:\n"
        "  record_id: UUID (primary key)\n"
        "  source_region: VARCHAR(64)\n"
        "  target_region: VARCHAR(64)\n"
        "  data_hash: CHAR(64) - SHA-256\n"
        "  created_at: TIMESTAMP WITH TIME ZONE\n"
        "  updated_at: TIMESTAMP WITH TIME ZONE\n"
        "  status: ENUM('pending','active','completed','failed')\n"
        "  retry_count: INTEGER DEFAULT 0\n\n"
        "ConflictLog Schema:\n"
        "  conflict_id: UUID (primary key)\n"
        "  record_id: UUID (foreign key -> SyncRecord)\n"
        "  conflict_type: VARCHAR(32)\n"
        "  resolution_strategy: VARCHAR(32)\n"
        "  resolved_at: TIMESTAMP WITH TIME ZONE\n"
        "  resolution_details: JSONB"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 500), dm_text, fontsize=10, fontname="cour", color=(0, 0, 0))

    # --- Page 8: Performance Benchmarks (NEW in v2) ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "6. Performance Benchmarks", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    perf_text = (
        "The following benchmarks were conducted on a 6-node Kubernetes cluster "
        "with 32 vCPUs and 128GB RAM per node:\n\n"
        "Throughput:\n"
        "  - Intra-region: 150,000 sync operations/second\n"
        "  - Cross-region (same continent): 45,000 ops/second\n"
        "  - Cross-region (intercontinental): 12,000 ops/second\n\n"
        "Latency (p99):\n"
        "  - Intra-region: 0.8ms\n"
        "  - Cross-region (same continent): 45ms\n"
        "  - Cross-region (intercontinental): 180ms\n\n"
        "Availability:\n"
        "  - Measured over 12 months: 99.9994%\n"
        "  - Mean time to recovery: 12 seconds\n"
        "  - Automatic failover success rate: 100%"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 500), perf_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # --- Page 9: Deployment Guide (same content as v1 page 8) ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "7. Deployment Guide", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    deploy_text = (
        "Prerequisites:\n"
        "- Kubernetes cluster v1.28+ with minimum 6 worker nodes\n"
        "- Helm v3.12+ installed\n"
        "- PostgreSQL 15+ with replication enabled\n"
        "- Apache Kafka 3.5+ cluster with 3+ brokers\n\n"
        "Installation Steps:\n"
        "1. Clone the deployment repository\n"
        "2. Configure environment variables in values.yaml\n"
        "3. Run: helm install cloudsync ./charts/cloudsync\n"
        "4. Verify pods: kubectl get pods -n cloudsync\n"
        "5. Run health check: curl http://gateway:8080/healthz\n\n"
        "Monitoring:\n"
        "Prometheus metrics are exposed on port 9090. Grafana dashboards are "
        "available in the monitoring/ directory of the repository."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 500), deploy_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # Form fields on the last page (modified from v1)
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "reviewer_name"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 550, 450, 575)
    widget.text_fontsize = 11
    widget.fill_color = (0.95, 0.95, 0.95)
    widget.border_color = (0.3, 0.3, 0.3)
    page.add_widget(widget)
    page.insert_text(pymupdf.Point(72, 568), "Reviewer Name:", fontsize=11, fontname="hebo", color=(0, 0, 0))

    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
    widget.field_name = "approved"
    widget.field_value = "Off"
    widget.rect = pymupdf.Rect(200, 590, 220, 610)
    widget.border_color = (0, 0, 0)
    page.add_widget(widget)
    page.insert_text(pymupdf.Point(72, 605), "Approved:", fontsize=11, fontname="hebo", color=(0, 0, 0))

    # NEW form field in v2
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "review_date"
    widget.field_value = ""
    widget.rect = pymupdf.Rect(200, 625, 450, 650)
    widget.text_fontsize = 11
    widget.fill_color = (0.95, 0.95, 0.95)
    widget.border_color = (0.3, 0.3, 0.3)
    page.add_widget(widget)
    page.insert_text(pymupdf.Point(72, 643), "Review Date:", fontsize=11, fontname="hebo", color=(0, 0, 0))

    # Add internal links now that all pages exist
    doc[2].insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(72, 570, 300, 590), "page": 3, "to": pymupdf.Point(72, 72)})

    # Set TOC (updated)
    toc = [
        [1, "Introduction", 3],
        [1, "System Architecture", 4],
        [1, "API Reference", 5],
        [1, "Security Protocols", 6],
        [1, "Data Models", 7],
        [1, "Performance Benchmarks", 8],
        [1, "Deployment Guide", 9],
    ]
    doc.set_toc(toc)

    # Set metadata (changed author, subject)
    doc.set_metadata({
        "title": "CloudSync Platform Technical Specification",
        "author": "Elena Rodriguez, Kai Tanaka",
        "subject": "Technical Specification v2",
        "keywords": "cloudsync, distributed, synchronization, API, performance",
        "creator": "CloudSync Engineering",
        "producer": "PyMuPDF",
    })

    doc.save(V2_PATH)
    doc.close()
    print(f'Created: {V2_PATH}')


def main():
    os.makedirs(DESKTOP, exist_ok=True)
    create_v1()
    create_v2()

    # Open both PDFs in Evince for the agent
    launch_gui(f'evince "{V1_PATH}"', delay_sec=2.0)
    launch_gui(f'evince "{V2_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with both spec PDFs')


main()
