"""
Initial Setup: Create 8 PDF research papers in ~/Research/Papers
Task ID: osworld_multi_apps_pdf_author_extract_007
Domain: multi_apps (PDF + LibreOffice Calc)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_author_extract_007'
PAPERS_DIR = f'{WORKDIR}/Research/Papers'

# Paper data: (filename, title, first_author, institution, abstract_snippet)
PAPERS = [
    (
        "touchtables_hci2024.pdf",
        "TouchTables: Collaborative Data Exploration on Large Interactive Surfaces",
        "Aisha Mahmoud",
        "Carnegie Mellon University",
        "We present TouchTables, a multi-user collaborative visualization system designed for large touch-enabled displays. Our approach leverages simultaneous multi-touch input to enable co-located teams to explore complex datasets."
    ),
    (
        "distributed_fs_osdi2023.pdf",
        "CacheFS: Adaptive Caching Strategies for Distributed File Systems",
        "Brian Kowalski",
        "MIT CSAIL",
        "Modern distributed file systems face increasing pressure from latency-sensitive workloads. We introduce CacheFS, a novel adaptive caching layer that dynamically adjusts eviction policies based on observed access patterns."
    ),
    (
        "gesture_recognition_chi2024.pdf",
        "GestureLens: Understanding Mid-Air Hand Gestures in Cluttered Environments",
        "Chen Wei",
        "Tsinghua University",
        "Mid-air gesture recognition remains challenging in real-world deployments due to background clutter and user variability. GestureLens introduces a transformer-based approach trained on a diverse corpus of naturalistic gestures."
    ),
    (
        "memory_mgmt_sosp2023.pdf",
        "HybridMem: Tiered Memory Management for CXL-Attached Persistent Memory",
        "Diana Okonkwo",
        "University of Cambridge",
        "The emergence of CXL-attached persistent memory introduces new opportunities and challenges for OS memory management. We propose HybridMem, a tiered memory manager that transparently migrates pages between DRAM and CXL-PM."
    ),
    (
        "accessibility_uist2024.pdf",
        "SpeakEasy: Low-Latency Screen Reader Navigation for Complex Web Interfaces",
        "Elena Vasquez",
        "Stanford University",
        "Screen readers often struggle with dynamically updated web content, causing significant navigation overhead for blind users. SpeakEasy introduces a predictive pre-loading strategy that reduces latency by 62% in controlled studies."
    ),
    (
        "network_sched_nsdi2024.pdf",
        "FlowWeaver: Priority-Aware Network Scheduling in Multi-Tenant Data Centers",
        "Farhan Iqbal",
        "ETH Zurich",
        "Multi-tenant data centers must balance competing traffic flows from thousands of concurrent tenants. FlowWeaver proposes a priority-aware scheduling framework that enforces latency SLOs without sacrificing aggregate throughput."
    ),
    (
        "vr_locomotion_vrst2023.pdf",
        "StepSync: Reducing Cybersickness Through Gait-Matched Virtual Locomotion",
        "Grace Nakamura",
        "University of Tokyo",
        "Cybersickness remains a significant barrier to prolonged VR use. StepSync synchronizes virtual camera movement with the user's physical gait patterns, measured via lightweight inertial sensors, to achieve perceptual congruence."
    ),
    (
        "storage_osdi2024.pdf",
        "LogForge: Write-Optimized Storage for Time-Series Sensor Data at Scale",
        "Henrik Sorensen",
        "DTU - Technical University of Denmark",
        "Industrial IoT deployments generate billions of sensor readings per day, demanding efficient ingestion and query performance. LogForge introduces a write-optimized log-structured storage engine specifically designed for time-series workloads."
    ),
]


def create_pdf(filepath, title, first_author, institution, abstract):
    """Create a realistic-looking research paper PDF using fpdf2."""
    from fpdf import FPDF

    class ResearchPDF(FPDF):
        def header(self):
            self.set_font('Helvetica', 'B', 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, 'Research Paper', align='R', ln=True)
            self.ln(2)

        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', '', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Page {self.page_no()}', align='C')

    pdf = ResearchPDF()
    pdf.set_margins(25, 20, 25)
    pdf.add_page()

    # Title
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 10, title, align='C')
    pdf.ln(6)

    # Authors section
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 8, first_author, align='C', ln=True)

    pdf.set_font('Helvetica', 'I', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, institution, align='C', ln=True)
    pdf.ln(8)

    # Horizontal rule
    pdf.set_draw_color(180, 180, 180)
    pdf.line(25, pdf.get_y(), 185, pdf.get_y())
    pdf.ln(6)

    # Abstract
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 7, 'Abstract', ln=True)
    pdf.ln(2)

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 6, abstract, align='J')
    pdf.ln(6)

    # Introduction section
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, '1. Introduction', ln=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', '', 10)
    intro_text = (
        f"The work presented in this paper addresses a fundamental challenge in "
        f"the field. Prior research has demonstrated the importance of systematic "
        f"approaches to this problem domain. We extend these efforts by introducing "
        f"a novel methodology that improves upon state-of-the-art techniques. "
        f"Our contributions include: (1) a comprehensive analysis of existing approaches, "
        f"(2) a new framework for evaluation, and (3) an empirical study with "
        f"participants drawn from diverse backgrounds."
    )
    pdf.multi_cell(0, 6, intro_text, align='J')
    pdf.ln(6)

    # Related Work
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, '2. Related Work', ln=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', '', 10)
    related_text = (
        "Several prior works have explored related themes. Smith et al. [1] proposed "
        "an early framework, while Johnson and Lee [2] extended this work with "
        "a more scalable architecture. More recently, Wang et al. [3] demonstrated "
        "the feasibility of real-time operation in resource-constrained settings. "
        "Our work builds on these foundations and addresses limitations that "
        "remained unresolved in prior literature."
    )
    pdf.multi_cell(0, 6, related_text, align='J')
    pdf.ln(6)

    # Methodology
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, '3. Methodology', ln=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', '', 10)
    method_text = (
        "Our approach consists of three main components. First, we collect data "
        "through a structured protocol designed to minimize confounds. Second, "
        "we apply our novel algorithm to transform raw inputs into structured "
        "representations. Third, we validate outputs against ground truth using "
        "both automated metrics and expert human evaluation. "
        "Each component was carefully designed to ensure reproducibility and generalizability."
    )
    pdf.multi_cell(0, 6, method_text, align='J')
    pdf.ln(6)

    # Conclusion
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 7, '4. Conclusion', ln=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', '', 10)
    conclusion_text = (
        "In this paper we presented a novel approach to the problem at hand. "
        "Our experiments show significant improvements over baseline methods. "
        "Future work will explore extensions to additional domains and larger-scale deployments. "
        "We release our code and dataset to support reproducibility."
    )
    pdf.multi_cell(0, 6, conclusion_text, align='J')

    pdf.output(filepath)


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app on the VM display without blocking script exit."""
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
    # Create directory structure
    os.makedirs(PAPERS_DIR, exist_ok=True)
    print(f'Created directory: {PAPERS_DIR}')

    # Install fpdf2 if needed
    subprocess.run(
        ['pip3', 'install', 'fpdf2', '--quiet'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Create PDF files
    for filename, title, author, institution, abstract in PAPERS:
        filepath = os.path.join(PAPERS_DIR, filename)
        create_pdf(filepath, title, author, institution, abstract)
        print(f'Created PDF: {filepath}')

    # Make sure ~/hci_sys_authors.xlsx does NOT exist (pre-task state)
    output_xlsx = f'{WORKDIR}/hci_sys_authors.xlsx'
    if os.path.exists(output_xlsx):
        os.remove(output_xlsx)
        print(f'Removed pre-existing: {output_xlsx}')

    print(f'All {len(PAPERS)} PDFs created in {PAPERS_DIR}')

    # GUI-ready startup: open Nautilus at the Papers directory
    launch_gui(f'nautilus "{PAPERS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus at ~/Research/Papers with DISPLAY=:0')


create_initial()
