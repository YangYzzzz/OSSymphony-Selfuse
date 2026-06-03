"""
Initial Setup: Create cross-references in master document subdocuments
Task ID: writer_rm_094
Domain: libreoffice_writer

Creates a LibreOffice Writer master document (SystemDoc_Master.odm) with 6
subdocuments. The Introduction.odt has placeholder text for cross-references
that the agent must replace with actual cross-references to headings in
Chapters 3, 4, and 5.
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_094'

# Subdocument directory
SUBDIR = f'{WORKDIR}/SystemDoc_Parts'


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


def create_odt(filepath, content_xml_body):
    """Create a minimal ODT file with the given content body XML."""
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
</manifest:manifest>'''

    content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:automatic-styles>
    <style:style style:name="P_bold" style:family="paragraph" style:parent-style-name="Standard">
      <style:text-properties fo:font-weight="bold" fo:font-size="11pt"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:text>
{content_xml_body}
    </office:text>
  </office:body>
</office:document-content>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:styles>
    <style:style style:name="Standard" style:family="paragraph" style:class="text"/>
    <style:style style:name="Heading" style:family="paragraph" style:parent-style-name="Standard"
                 style:class="text">
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="Heading_20_1" style:display-name="Heading 1" style:family="paragraph"
                 style:parent-style-name="Heading" style:next-style-name="Standard"
                 style:default-outline-level="1" style:class="text">
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="Heading_20_2" style:display-name="Heading 2" style:family="paragraph"
                 style:parent-style-name="Heading" style:next-style-name="Standard"
                 style:default-outline-level="2" style:class="text">
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold"/>
    </style:style>
  </office:styles>
</office:document-styles>'''

    mimetype = 'application/vnd.oasis.opendocument.text'

    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first entry, stored uncompressed
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('META-INF/manifest.xml', manifest_xml)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)

    print(f'  Created: {filepath}')


def create_subdocuments():
    """Create all 6 subdocuments."""
    os.makedirs(SUBDIR, exist_ok=True)

    # --- Introduction.odt ---
    # Contains placeholder text where cross-references should be inserted
    intro_body = '''      <text:h text:style-name="Heading_20_1" text:outline-level="1">Introduction</text:h>
      <text:p text:style-name="Standard">This master document provides a comprehensive overview of the enterprise system architecture, covering database design, security implementation, and performance optimization strategies deployed across our production infrastructure.</text:p>
      <text:p text:style-name="Standard"/>
      <text:p text:style-name="Standard">The system architecture is built upon a robust database foundation. For detailed information about the underlying data storage mechanisms and schema design patterns, please refer to [see Ch3 ref] in this document.</text:p>
      <text:p text:style-name="Standard"/>
      <text:p text:style-name="Standard">Security is a critical concern throughout the entire stack. The comprehensive security framework, including authentication protocols and encryption standards, is documented in [see Ch4 ref] which outlines the multi-layered defense strategy.</text:p>
      <text:p text:style-name="Standard"/>
      <text:p text:style-name="Standard">System performance has been extensively tested under various load conditions. The results of stress testing, capacity planning, and optimization efforts are presented in [see Ch5 ref] along with recommended scaling approaches.</text:p>
      <text:p text:style-name="Standard"/>
      <text:p text:style-name="Standard">Together, these chapters form the technical backbone of our system documentation, providing engineering teams with the reference materials needed for ongoing development and maintenance.</text:p>'''
    create_odt(f'{SUBDIR}/Introduction.odt', intro_body)

    # --- Chapter1_Overview.odt ---
    ch1_body = '''      <text:h text:style-name="Heading_20_1" text:outline-level="1">Chapter 1: System Overview</text:h>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Project Background</text:h>
      <text:p text:style-name="Standard">The Enterprise Resource Management System (ERMS) was initiated in Q3 2024 to consolidate disparate business tools into a unified platform. The project involves migrating 14 legacy applications serving approximately 2,500 daily active users across three continental regions.</text:p>
      <text:p text:style-name="Standard"/>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Architecture Principles</text:h>
      <text:p text:style-name="Standard">The system follows a microservices architecture with event-driven communication patterns. Core services include user management, inventory tracking, financial reporting, and customer relationship management. Each service maintains its own data store following the database-per-service pattern.</text:p>
      <text:p text:style-name="Standard"/>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Technology Stack</text:h>
      <text:p text:style-name="Standard">Backend services are implemented in Java 21 and Python 3.12, with Go utilized for performance-critical gateway services. The frontend is built with React 18 and TypeScript, communicating with backend services through a GraphQL API gateway.</text:p>'''
    create_odt(f'{SUBDIR}/Chapter1_Overview.odt', ch1_body)

    # --- Chapter2_Requirements.odt ---
    ch2_body = '''      <text:h text:style-name="Heading_20_1" text:outline-level="1">Chapter 2: System Requirements</text:h>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Functional Requirements</text:h>
      <text:p text:style-name="Standard">The system must support concurrent access from up to 5,000 users with sub-200ms response times for 95th percentile requests. User authentication must integrate with existing Active Directory infrastructure and support SAML 2.0 federation.</text:p>
      <text:p text:style-name="Standard"/>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Non-Functional Requirements</text:h>
      <text:p text:style-name="Standard">System availability must meet 99.95% uptime SLA measured on a rolling 30-day basis. Recovery Point Objective (RPO) is set at 15 minutes with Recovery Time Objective (RTO) of 4 hours for Tier-1 services and 24 hours for Tier-2 services.</text:p>
      <text:p text:style-name="Standard"/>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Compliance Standards</text:h>
      <text:p text:style-name="Standard">All data handling must comply with GDPR, SOC 2 Type II, and ISO 27001 requirements. Financial modules must additionally satisfy PCI DSS Level 1 certification standards for payment processing operations.</text:p>'''
    create_odt(f'{SUBDIR}/Chapter2_Requirements.odt', ch2_body)

    # --- Chapter3_Database.odt ---
    # Contains Heading 2 "Database Architecture" that the cross-reference should point to
    ch3_body = '''      <text:h text:style-name="Heading_20_1" text:outline-level="1">Chapter 3: Data Management</text:h>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Database Architecture</text:h>
      <text:p text:style-name="Standard">The database layer employs a polyglot persistence strategy with PostgreSQL 16 as the primary relational store, MongoDB 7.0 for document-oriented workloads, and Redis 7.2 for caching and session management. Each microservice owns its database schema, with cross-service data access mediated through well-defined API contracts.</text:p>
      <text:p text:style-name="Standard"/>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Data Migration Strategy</text:h>
      <text:p text:style-name="Standard">Migration from legacy Oracle 19c databases follows a strangler fig pattern, with dual-write mechanisms ensuring data consistency during the transition period. Flyway 10.0 manages schema versioning with automated rollback capabilities for failed migrations.</text:p>
      <text:p text:style-name="Standard"/>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Backup and Recovery</text:h>
      <text:p text:style-name="Standard">Automated point-in-time recovery is configured with 15-minute granularity using WAL archiving to S3-compatible object storage. Full database snapshots are taken daily and retained for 90 days, with monthly snapshots archived for 7 years to meet regulatory requirements.</text:p>'''
    create_odt(f'{SUBDIR}/Chapter3_Database.odt', ch3_body)

    # --- Chapter4_Security.odt ---
    # Contains Heading 2 "Security Protocols" that the cross-reference should point to
    ch4_body = '''      <text:h text:style-name="Heading_20_1" text:outline-level="1">Chapter 4: Security Framework</text:h>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Security Protocols</text:h>
      <text:p text:style-name="Standard">All inter-service communication is encrypted using mutual TLS with certificates managed through HashiCorp Vault. External API traffic is secured via TLS 1.3 with HSTS enforcement. OAuth 2.0 with PKCE flow handles user authentication, while service-to-service calls use short-lived JWT tokens with RS256 signing.</text:p>
      <text:p text:style-name="Standard"/>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Access Control</text:h>
      <text:p text:style-name="Standard">Role-based access control (RBAC) is implemented at both application and database levels. The authorization engine supports hierarchical roles with attribute-based policies for fine-grained resource access. All access decisions are audited with tamper-proof logging to a dedicated security event store.</text:p>
      <text:p text:style-name="Standard"/>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Incident Response</text:h>
      <text:p text:style-name="Standard">The security operations center monitors all system events using Splunk SIEM with custom correlation rules. Automated playbooks handle common incident types including brute-force attempts, anomalous data access patterns, and potential data exfiltration scenarios.</text:p>'''
    create_odt(f'{SUBDIR}/Chapter4_Security.odt', ch4_body)

    # --- Chapter5_Performance.odt ---
    # Contains Heading 2 "Performance Benchmarks" that the cross-reference should point to
    ch5_body = '''      <text:h text:style-name="Heading_20_1" text:outline-level="1">Chapter 5: Performance Engineering</text:h>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Performance Benchmarks</text:h>
      <text:p text:style-name="Standard">Load testing with Apache JMeter simulating 10,000 concurrent users demonstrated average response times of 145ms for read operations and 230ms for write operations. The system maintained stable performance up to 8,500 concurrent connections before graceful degradation, achieving 12,400 transactions per second at peak throughput.</text:p>
      <text:p text:style-name="Standard"/>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Optimization Techniques</text:h>
      <text:p text:style-name="Standard">Query performance is optimized through materialized views refreshed on 5-minute intervals for dashboard queries, and connection pooling via PgBouncer configured with 200 connections per service instance. Application-level caching uses a two-tier strategy with local Caffeine caches backed by distributed Redis clusters.</text:p>
      <text:p text:style-name="Standard"/>
      <text:h text:style-name="Heading_20_2" text:outline-level="2">Capacity Planning</text:h>
      <text:p text:style-name="Standard">Current infrastructure supports projected growth through Q4 2026 based on linear extrapolation of user acquisition trends. Horizontal scaling is automated via Kubernetes HPA with custom metrics from Prometheus, targeting 70% CPU utilization across application pods with burst capacity to 150% of baseline.</text:p>'''
    create_odt(f'{SUBDIR}/Chapter5_Performance.odt', ch5_body)


def create_master_document():
    """Create the master document (ODM) that links all subdocuments."""
    # An ODM file is essentially an ODT with text:section elements
    # pointing to subdocuments, with a different mimetype
    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text-master" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
</manifest:manifest>'''

    content_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:automatic-styles/>
  <office:body>
    <office:text>
      <text:h text:style-name="Heading_20_1" text:outline-level="1">Enterprise System Technical Documentation</text:h>
      <text:p>Master document for the ERMS project technical reference.</text:p>
      <text:p/>
      <text:section text:name="Introduction" text:protected="false">
        <text:section-source xlink:href="SystemDoc_Parts/Introduction.odt" text:section-name="" text:filter-name="writer8"/>
      </text:section>
      <text:section text:name="Chapter1" text:protected="false">
        <text:section-source xlink:href="SystemDoc_Parts/Chapter1_Overview.odt" text:section-name="" text:filter-name="writer8"/>
      </text:section>
      <text:section text:name="Chapter2" text:protected="false">
        <text:section-source xlink:href="SystemDoc_Parts/Chapter2_Requirements.odt" text:section-name="" text:filter-name="writer8"/>
      </text:section>
      <text:section text:name="Chapter3" text:protected="false">
        <text:section-source xlink:href="SystemDoc_Parts/Chapter3_Database.odt" text:section-name="" text:filter-name="writer8"/>
      </text:section>
      <text:section text:name="Chapter4" text:protected="false">
        <text:section-source xlink:href="SystemDoc_Parts/Chapter4_Security.odt" text:section-name="" text:filter-name="writer8"/>
      </text:section>
      <text:section text:name="Chapter5" text:protected="false">
        <text:section-source xlink:href="SystemDoc_Parts/Chapter5_Performance.odt" text:section-name="" text:filter-name="writer8"/>
      </text:section>
    </office:text>
  </office:body>
</office:document-content>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:styles>
    <style:style style:name="Standard" style:family="paragraph" style:class="text"/>
    <style:style style:name="Heading" style:family="paragraph" style:parent-style-name="Standard"
                 style:class="text">
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="Heading_20_1" style:display-name="Heading 1" style:family="paragraph"
                 style:parent-style-name="Heading" style:next-style-name="Standard"
                 style:default-outline-level="1" style:class="text">
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="Heading_20_2" style:display-name="Heading 2" style:family="paragraph"
                 style:parent-style-name="Heading" style:next-style-name="Standard"
                 style:default-outline-level="2" style:class="text">
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold"/>
    </style:style>
  </office:styles>
</office:document-styles>'''

    mimetype = 'application/vnd.oasis.opendocument.text-master'
    master_path = f'{WORKDIR}/SystemDoc_Master.odm'

    with zipfile.ZipFile(master_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('META-INF/manifest.xml', manifest_xml)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)

    print(f'Master document created: {master_path}')


def main():
    # Create all subdocuments
    print('Creating subdocuments...')
    create_subdocuments()

    # Create master document
    print('Creating master document...')
    create_master_document()

    # Open the master document in LibreOffice Writer
    master_path = f'{WORKDIR}/SystemDoc_Master.odm'
    launch_gui(f'libreoffice --writer "{master_path}"', delay_sec=3.0)
    print(f'GUI_READY: launched LibreOffice Writer with {master_path} on DISPLAY=:0')


main()
