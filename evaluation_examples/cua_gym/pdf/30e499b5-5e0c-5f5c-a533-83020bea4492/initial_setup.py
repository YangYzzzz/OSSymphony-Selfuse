"""
Initial Setup: Bash script merge PDFs by folder task
Task ID: pdf_cross_094
Domain: pdf

Creates:
- ~/Documents/projects/ with 4 subdirectories containing PDF files
- ~/scripts/ directory (empty, no merge script yet)
- ~/Documents/merged_output/ (empty directory)
- Opens nautilus file manager on ~/Documents/projects/
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'

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


def create_pdf(path, title, pages_content):
    """Create a PDF with realistic content using pymupdf."""
    import pymupdf

    doc = pymupdf.open()
    for page_num, (heading, body_lines) in enumerate(pages_content):
        page = doc.new_page(width=595, height=842)

        # Draw a light header bar
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(0, 0, 595, 60))
        shape.finish(color=(0.2, 0.4, 0.7), fill=(0.2, 0.4, 0.7), width=0)
        shape.commit()

        # Title in header
        page.insert_text(
            pymupdf.Point(36, 38),
            title,
            fontsize=14,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Page heading
        page.insert_text(
            pymupdf.Point(36, 85),
            heading,
            fontsize=16,
            fontname="hebo",
            color=(0.1, 0.2, 0.5),
        )

        # Horizontal divider
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(36, 95), pymupdf.Point(559, 95))
        shape2.finish(color=(0.2, 0.4, 0.7), width=1.5)
        shape2.commit()

        # Body text
        y = 120
        for line in body_lines:
            if line.startswith("**") and line.endswith("**"):
                # Bold subheading
                page.insert_text(
                    pymupdf.Point(36, y),
                    line.strip("*"),
                    fontsize=11,
                    fontname="hebo",
                    color=(0, 0, 0),
                )
            else:
                rect = pymupdf.Rect(36, y, 559, y + 40)
                page.insert_textbox(
                    rect,
                    line,
                    fontsize=10,
                    fontname="helv",
                    color=(0.1, 0.1, 0.1),
                    align=pymupdf.TEXT_ALIGN_LEFT,
                )
            y += 20
            if y > 790:
                break

        # Footer
        page.insert_text(
            pymupdf.Point(36, 820),
            f"Page {page_num + 1}",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.save(path)
    doc.close()


def create_initial():
    projects_dir = f"{WORKDIR}/Documents/projects"
    scripts_dir = f"{WORKDIR}/scripts"
    output_dir = f"{WORKDIR}/Documents/merged_output"

    # Create directories
    for d in [projects_dir, scripts_dir, output_dir]:
        os.makedirs(d, exist_ok=True)

    # ---- alpha/ : 3 PDFs (Quarterly reports) ----
    alpha_dir = f"{projects_dir}/alpha"
    os.makedirs(alpha_dir, exist_ok=True)

    create_pdf(f"{alpha_dir}/report_q1.pdf", "Alpha Division - Q1 Report", [
        ("Q1 2024 Performance Overview", [
            "**Executive Summary**",
            "Alpha Division delivered strong growth in Q1 2024 with revenue reaching $2.4M.",
            "The team expanded from 18 to 24 engineers, accelerating delivery timelines.",
            "**Key Metrics**",
            "Revenue: $2,400,000 (+15% YoY)",
            "Operating Margin: 22%",
            "Customer Satisfaction Score: 4.7/5.0",
            "**Product Updates**",
            "Launched version 3.2 of core platform with improved API throughput.",
            "Onboarded 12 new enterprise clients including TechCorp and GlobalSys.",
        ]),
        ("Q1 Financials", [
            "**Revenue Breakdown**",
            "Software Licenses: $1,200,000",
            "Professional Services: $800,000",
            "Support Contracts: $400,000",
            "**Expenses**",
            "Personnel: $980,000",
            "Infrastructure: $210,000",
            "Marketing: $150,000",
            "**Net Profit: $860,000**",
        ]),
    ])

    create_pdf(f"{alpha_dir}/report_q2.pdf", "Alpha Division - Q2 Report", [
        ("Q2 2024 Performance Overview", [
            "**Executive Summary**",
            "Q2 saw continued growth momentum with stronger enterprise sales performance.",
            "New product launch in June contributed $340K incremental revenue.",
            "**Key Metrics**",
            "Revenue: $2,780,000 (+16% QoQ)",
            "New Clients: 17",
            "Churn Rate: 2.1%",
            "**Highlights**",
            "Partnership signed with DataStream Inc. for joint go-to-market strategy.",
            "Engineering team achieved 98.9% platform uptime across all regions.",
        ]),
    ])

    create_pdf(f"{alpha_dir}/report_q3.pdf", "Alpha Division - Q3 Report", [
        ("Q3 2024 Performance Overview", [
            "**Executive Summary**",
            "Q3 represented the strongest quarter in company history with $3.1M revenue.",
            "The APAC expansion exceeded targets with 8 new enterprise contracts.",
            "**Key Metrics**",
            "Revenue: $3,100,000 (+11.5% QoQ)",
            "Customer Retention: 94.2%",
            "NPS Score: 68",
            "**Strategy Update**",
            "Board approved additional $500K investment in AI-driven features.",
        ]),
        ("Q3 Product Roadmap Update", [
            "**Completed Milestones**",
            "- Real-time analytics dashboard (shipped Aug 15)",
            "- Multi-tenant access control overhaul",
            "- REST API v4 with GraphQL support",
            "**Upcoming Q4 Deliverables**",
            "- Predictive analytics module (due Nov 30)",
            "- Salesforce integration connector",
            "- Mobile application v2.0",
        ]),
    ])

    # ---- beta/ : 2 PDFs (Budget documents) ----
    beta_dir = f"{projects_dir}/beta"
    os.makedirs(beta_dir, exist_ok=True)

    create_pdf(f"{beta_dir}/budget_2024.pdf", "Beta Project - 2024 Budget", [
        ("2024 Annual Budget Plan", [
            "**Overview**",
            "This document outlines the approved budget allocation for Beta Project FY2024.",
            "Total budget approved by finance committee: $4,200,000",
            "**Department Allocations**",
            "Engineering & Development: $1,800,000 (42.9%)",
            "Sales & Marketing: $950,000 (22.6%)",
            "Customer Success: $620,000 (14.8%)",
            "Operations & IT: $430,000 (10.2%)",
            "Finance & Legal: $400,000 (9.5%)",
        ]),
        ("2024 Budget by Quarter", [
            "**Q1 Budget: $980,000**",
            "Personnel onboarding, infrastructure setup, marketing campaign launch.",
            "**Q2 Budget: $1,050,000**",
            "Peak hiring season, trade shows, product launch costs.",
            "**Q3 Budget: $1,100,000**",
            "APAC expansion costs, conference sponsorships.",
            "**Q4 Budget: $1,070,000**",
            "Year-end bonuses, contract renewals, planning for FY2025.",
        ]),
        ("Budget Assumptions & Risks", [
            "**Key Assumptions**",
            "Headcount growth of 15% YoY based on pipeline forecasts.",
            "SaaS infrastructure costs grow at 8% per additional customer.",
            "Marketing ROI of 3.2x based on historical campaign data.",
            "**Identified Risks**",
            "Currency fluctuation for APAC region (±5% exposure).",
            "Potential regulatory compliance costs in EU markets.",
            "Supply chain delays affecting hardware procurement timeline.",
        ]),
    ])

    create_pdf(f"{beta_dir}/budget_2025.pdf", "Beta Project - 2025 Budget", [
        ("2025 Annual Budget Plan", [
            "**Overview**",
            "FY2025 budget reflects aggressive growth targets and market expansion strategy.",
            "Total proposed budget: $5,800,000 (+38% vs FY2024)",
            "**Key Investment Areas**",
            "AI/ML capabilities build-out: $800,000 new investment",
            "International market entry (LATAM): $450,000",
            "Customer Success scaling: +6 headcount",
            "**Approval Status: PENDING Board Review**",
            "Next review date: January 15, 2025",
        ]),
    ])

    # ---- gamma/ : 4 PDFs (Project plans) ----
    gamma_dir = f"{projects_dir}/gamma"
    os.makedirs(gamma_dir, exist_ok=True)

    create_pdf(f"{gamma_dir}/plan_a.pdf", "Gamma Initiative - Plan A", [
        ("Plan A: Conservative Growth Strategy", [
            "**Objective**",
            "Maintain current market position while optimizing profitability.",
            "Target 8-10% organic revenue growth through existing customer expansion.",
            "**Execution Approach**",
            "Focus on upselling advanced features to existing 240 enterprise accounts.",
            "Reduce CAC by 20% through improved inbound marketing.",
            "Increase support team capacity to improve NPS from 68 to 75.",
        ]),
        ("Plan A: Resource Requirements", [
            "**Headcount Plan**",
            "Current: 82 FTEs",
            "End of Year Target: 94 FTEs (+12)",
            "New Roles: 4 Engineers, 3 CSMs, 2 Sales, 2 Marketing, 1 Finance",
            "**Budget Requirement: $4,800,000**",
            "This represents a 14% increase over FY2024 actual spend.",
        ]),
    ])

    create_pdf(f"{gamma_dir}/plan_b.pdf", "Gamma Initiative - Plan B", [
        ("Plan B: Moderate Expansion Strategy", [
            "**Objective**",
            "Expand into 2 new verticals: Healthcare and Financial Services.",
            "Target 20-25% revenue growth through new logo acquisition.",
            "**Execution Approach**",
            "Build dedicated vertical sales teams for Healthcare and FinServ.",
            "Develop industry-specific product configurations and compliance features.",
            "Partner with 3 system integrators in each vertical.",
        ]),
    ])

    create_pdf(f"{gamma_dir}/plan_c.pdf", "Gamma Initiative - Plan C", [
        ("Plan C: Aggressive Expansion Strategy", [
            "**Objective**",
            "Capture 15% market share in SMB segment through product-led growth.",
            "Launch self-serve product tier with freemium model.",
            "**Execution Approach**",
            "Build self-serve infrastructure: automated onboarding, in-product trials.",
            "Reduce time-to-value from 14 days to 3 days.",
            "Community-led growth: developer advocacy, open-source components.",
        ]),
        ("Plan C: Financial Projections", [
            "**Revenue Targets**",
            "Year 1: $6,200,000 (45% growth)",
            "Year 2: $9,500,000 (53% growth)",
            "Year 3: $14,200,000 (49% growth)",
            "**Investment Required: $7,200,000 over 3 years**",
            "IRR projection: 34% based on comparable SaaS benchmarks.",
        ]),
    ])

    create_pdf(f"{gamma_dir}/plan_d.pdf", "Gamma Initiative - Plan D", [
        ("Plan D: Partnership & Acquisition Strategy", [
            "**Objective**",
            "Accelerate growth through strategic partnerships and selective M&A.",
            "Identify 2-3 acquisition targets in adjacent markets.",
            "**Target Acquisition Profiles**",
            "Company size: $2-8M ARR, complementary technology stack.",
            "Geography: North America or Western Europe.",
            "Synergy potential: cross-sell to combined customer base.",
        ]),
    ])

    # ---- delta/ : 1 PDF (Summary document) ----
    delta_dir = f"{projects_dir}/delta"
    os.makedirs(delta_dir, exist_ok=True)

    create_pdf(f"{delta_dir}/summary.pdf", "Delta Project - Executive Summary", [
        ("Executive Summary: Delta Project 2024", [
            "**Project Overview**",
            "Delta Project is a cross-functional initiative to modernize legacy infrastructure",
            "and migrate all services to cloud-native architecture by Q4 2024.",
            "**Current Status: ON TRACK**",
            "Phase 1 (Assessment): Completed Q1 2024",
            "Phase 2 (Design): Completed Q2 2024",
            "Phase 3 (Migration): In Progress - 67% complete",
            "Phase 4 (Validation): Scheduled Q4 2024",
            "**Business Impact**",
            "Expected 35% reduction in infrastructure costs post-migration.",
            "Improved deployment frequency from bi-weekly to daily releases.",
        ]),
        ("Delta Project: Key Stakeholders & Contacts", [
            "**Executive Sponsor**",
            "Sarah Mitchell - Chief Technology Officer",
            "sarah.mitchell@company.com | (415) 555-0182",
            "**Project Manager**",
            "David Nakamura - Senior Program Manager",
            "david.nakamura@company.com | (415) 555-0247",
            "**Technical Lead**",
            "Priya Sharma - Principal Cloud Architect",
            "priya.sharma@company.com | (415) 555-0319",
            "**Steering Committee Meetings**",
            "Bi-weekly Fridays, 10:00 AM PST | Conference Room B / Zoom",
        ]),
    ])

    print(f"Created PDF files in {projects_dir}")
    print(f"  alpha/: report_q1.pdf, report_q2.pdf, report_q3.pdf")
    print(f"  beta/:  budget_2024.pdf, budget_2025.pdf")
    print(f"  gamma/: plan_a.pdf, plan_b.pdf, plan_c.pdf, plan_d.pdf")
    print(f"  delta/: summary.pdf")
    print(f"Created empty: {scripts_dir}")
    print(f"Created empty: {output_dir}")

    # GUI-ready startup: open nautilus file manager on projects directory
    launch_gui(f'nautilus "{projects_dir}"', delay_sec=2.0)
    print(f"GUI_READY: launched nautilus on {projects_dir} with DISPLAY=:0")


create_initial()
