"""
Initial Setup: Create a 10-page color paper PDF with colorful figures on pages 4-6
Task ID: pdf_res_052
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_052'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/color_paper.pdf'

A4_W, A4_H = 595, 842


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


def add_text_page(doc, title, body_lines, page_num_label):
    """Add a text-heavy page typical of an academic paper."""
    page = doc.new_page(width=A4_W, height=A4_H)
    # Title / section heading
    page.insert_text(pymupdf.Point(72, 60), title, fontsize=16, fontname="hebo", color=(0, 0, 0))
    # Body text
    y = 95
    for line in body_lines:
        if y > A4_H - 60:
            break
        page.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 14
    # Page number
    page.insert_text(pymupdf.Point(A4_W / 2 - 10, A4_H - 30),
                     str(page_num_label), fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    return page


def add_figure_page(doc, title, page_num_label):
    """Add a page with colorful figures and charts."""
    page = doc.new_page(width=A4_W, height=A4_H)
    # Section heading
    page.insert_text(pymupdf.Point(72, 55), title, fontsize=14, fontname="hebo", color=(0, 0, 0))

    shape = page.new_shape()

    if page_num_label == 4:
        # Page 4: Bar chart with colorful bars
        page.insert_text(pymupdf.Point(72, 85), "Figure 1: Quarterly Revenue by Region (in $M)",
                         fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.5))
        colors = [
            (0.2, 0.4, 0.8),   # blue
            (0.9, 0.3, 0.1),   # red-orange
            (0.1, 0.7, 0.3),   # green
            (0.8, 0.6, 0.0),   # gold
        ]
        labels = ["North America", "Europe", "Asia-Pacific", "Latin America"]
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        bar_data = [
            [45, 52, 38, 22],
            [48, 55, 42, 25],
            [51, 50, 47, 28],
            [55, 58, 51, 30],
        ]
        base_x, base_y = 100, 350
        bar_w = 18
        group_gap = 30
        for qi, q_vals in enumerate(bar_data):
            gx = base_x + qi * (len(colors) * bar_w + group_gap)
            for ri, val in enumerate(q_vals):
                bx = gx + ri * bar_w
                bh = val * 3.5
                rect = pymupdf.Rect(bx, base_y - bh, bx + bar_w - 2, base_y)
                shape.draw_rect(rect)
                shape.finish(color=colors[ri], fill=colors[ri], width=0.5)
            page.insert_text(pymupdf.Point(gx + 20, base_y + 15), quarters[qi],
                             fontsize=8, fontname="helv", color=(0, 0, 0))
        # Legend
        for i, (lbl, clr) in enumerate(zip(labels, colors)):
            lx = 100 + i * 120
            ly = 390
            r = pymupdf.Rect(lx, ly, lx + 10, ly + 10)
            shape.draw_rect(r)
            shape.finish(color=clr, fill=clr, width=0.5)
            page.insert_text(pymupdf.Point(lx + 14, ly + 9), lbl, fontsize=7, fontname="helv", color=(0, 0, 0))

        # Second figure: pie-like colored circles
        page.insert_text(pymupdf.Point(72, 440),
                         "Figure 2: Market Share Distribution by Product Category",
                         fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.5))
        pie_colors = [
            (0.95, 0.2, 0.2),   # red
            (0.2, 0.6, 0.95),   # blue
            (0.3, 0.85, 0.3),   # green
            (1.0, 0.75, 0.0),   # yellow
            (0.7, 0.3, 0.8),    # purple
        ]
        pie_labels = ["Enterprise Software (35%)", "Cloud Services (28%)",
                      "Hardware (18%)", "Consulting (12%)", "Support (7%)"]
        cx_base, cy_base = 200, 580
        for i, (clr, lbl) in enumerate(zip(pie_colors, pie_labels)):
            angle = i * 72
            import math
            ox = cx_base + 60 * math.cos(math.radians(angle))
            oy = cy_base + 60 * math.sin(math.radians(angle))
            shape.draw_circle(pymupdf.Point(ox, oy), 30 + i * 3)
            shape.finish(color=clr, fill=clr, width=1)
            page.insert_text(pymupdf.Point(350, 500 + i * 16), lbl,
                             fontsize=8, fontname="helv", color=clr)

    elif page_num_label == 5:
        # Page 5: Scatter plot and heatmap-style grid
        page.insert_text(pymupdf.Point(72, 85),
                         "Figure 3: Correlation Between R&D Spending and Patent Output",
                         fontsize=11, fontname="hebo", color=(0.5, 0.1, 0.1))
        # Scatter dots
        import random
        random.seed(42)
        scatter_colors = [
            (0.9, 0.2, 0.2),   # red cluster
            (0.2, 0.2, 0.9),   # blue cluster
            (0.1, 0.8, 0.2),   # green cluster
        ]
        cluster_labels = ["Biotech", "IT", "Manufacturing"]
        for ci, clr in enumerate(scatter_colors):
            cx = 180 + ci * 100
            cy = 220
            for _ in range(15):
                dx = random.gauss(0, 25)
                dy = random.gauss(0, 25)
                shape.draw_circle(pymupdf.Point(cx + dx, cy + dy), 4)
                shape.finish(color=clr, fill=clr, width=0.5)
        for i, (lbl, clr) in enumerate(zip(cluster_labels, scatter_colors)):
            lx = 100 + i * 140
            shape.draw_circle(pymupdf.Point(lx, 320), 4)
            shape.finish(color=clr, fill=clr, width=0.5)
            page.insert_text(pymupdf.Point(lx + 8, 323), lbl,
                             fontsize=8, fontname="helv", color=(0, 0, 0))
        # Axes
        shape.draw_line(pymupdf.Point(100, 110), pymupdf.Point(100, 300))
        shape.finish(color=(0, 0, 0), width=1)
        shape.draw_line(pymupdf.Point(100, 300), pymupdf.Point(480, 300))
        shape.finish(color=(0, 0, 0), width=1)
        page.insert_text(pymupdf.Point(250, 315), "R&D Spending ($M)",
                         fontsize=8, fontname="helv", color=(0, 0, 0))

        # Heatmap grid
        page.insert_text(pymupdf.Point(72, 380),
                         "Figure 4: Performance Heatmap Across Departments",
                         fontsize=11, fontname="hebo", color=(0.5, 0.1, 0.1))
        depts = ["Sales", "Eng", "Mktg", "Ops", "HR"]
        metrics = ["Revenue", "Efficiency", "Growth", "Satisfaction"]
        random.seed(55)
        for ri, metric in enumerate(metrics):
            page.insert_text(pymupdf.Point(72, 425 + ri * 40), metric,
                             fontsize=7, fontname="helv", color=(0, 0, 0))
            for ci, dept in enumerate(depts):
                val = random.random()
                # Gradient: red (low) -> yellow (mid) -> green (high)
                r = max(0, min(1, 2 * (1 - val)))
                g = max(0, min(1, 2 * val))
                b = 0.1
                rect = pymupdf.Rect(140 + ci * 55, 410 + ri * 40, 140 + ci * 55 + 50, 410 + ri * 40 + 35)
                shape.draw_rect(rect)
                shape.finish(color=(0.3, 0.3, 0.3), fill=(r, g, b), width=0.5)
                page.insert_text(pymupdf.Point(rect.x0 + 12, rect.y0 + 22),
                                 f"{val:.2f}", fontsize=8, fontname="hebo", color=(1, 1, 1))
        for ci, dept in enumerate(depts):
            page.insert_text(pymupdf.Point(140 + ci * 55 + 8, 405), dept,
                             fontsize=7, fontname="hebo", color=(0, 0, 0))

    elif page_num_label == 6:
        # Page 6: Line chart and stacked area
        page.insert_text(pymupdf.Point(72, 85),
                         "Figure 5: Monthly Active Users by Platform (2024-2025)",
                         fontsize=11, fontname="hebo", color=(0.0, 0.3, 0.5))
        line_colors = [
            (0.0, 0.5, 0.9),   # blue - Desktop
            (0.9, 0.4, 0.0),   # orange - Mobile
            (0.5, 0.0, 0.8),   # purple - Tablet
        ]
        line_labels = ["Desktop", "Mobile", "Tablet"]
        import random
        random.seed(99)
        # Draw axes
        ox, oy = 100, 320
        shape.draw_line(pymupdf.Point(ox, 110), pymupdf.Point(ox, oy))
        shape.finish(color=(0, 0, 0), width=1)
        shape.draw_line(pymupdf.Point(ox, oy), pymupdf.Point(490, oy))
        shape.finish(color=(0, 0, 0), width=1)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for i, m in enumerate(months):
            page.insert_text(pymupdf.Point(ox + 10 + i * 32, oy + 12), m,
                             fontsize=6, fontname="helv", color=(0, 0, 0))
        for li, clr in enumerate(line_colors):
            pts = []
            base = 150 + li * 40
            for i in range(12):
                x = ox + 15 + i * 32
                y = oy - (base + random.randint(-20, 30)) * 1.1
                pts.append(pymupdf.Point(x, y))
            for i in range(len(pts) - 1):
                shape.draw_line(pts[i], pts[i + 1])
                shape.finish(color=clr, width=2)
            for pt in pts:
                shape.draw_circle(pt, 3)
                shape.finish(color=clr, fill=clr, width=0.5)
        for i, (lbl, clr) in enumerate(zip(line_labels, line_colors)):
            lx = 120 + i * 130
            shape.draw_line(pymupdf.Point(lx, 340), pymupdf.Point(lx + 20, 340))
            shape.finish(color=clr, width=2)
            page.insert_text(pymupdf.Point(lx + 25, 343), lbl,
                             fontsize=8, fontname="helv", color=(0, 0, 0))

        # Color gradient area
        page.insert_text(pymupdf.Point(72, 400),
                         "Figure 6: Adoption Rate Gradient by Region",
                         fontsize=11, fontname="hebo", color=(0.0, 0.3, 0.5))
        for i in range(20):
            frac = i / 19.0
            r = frac
            g = 0.2 + 0.5 * (1 - frac)
            b = 1.0 - frac
            rect = pymupdf.Rect(100 + i * 20, 430, 100 + (i + 1) * 20, 530)
            shape.draw_rect(rect)
            shape.finish(color=(r, g, b), fill=(r, g, b), width=0)
        page.insert_text(pymupdf.Point(100, 548), "Low Adoption",
                         fontsize=8, fontname="helv", color=(0, 0.7, 1))
        page.insert_text(pymupdf.Point(420, 548), "High Adoption",
                         fontsize=8, fontname="helv", color=(1, 0.2, 0))

        # Colorful table
        page.insert_text(pymupdf.Point(72, 590),
                         "Table 3: Regional Performance Summary",
                         fontsize=10, fontname="hebo", color=(0, 0, 0))
        headers = ["Region", "Users (K)", "Revenue ($M)", "Growth (%)"]
        header_clr = (0.15, 0.3, 0.6)
        for ci, h in enumerate(headers):
            rect = pymupdf.Rect(80 + ci * 120, 605, 80 + (ci + 1) * 120, 625)
            shape.draw_rect(rect)
            shape.finish(color=header_clr, fill=header_clr, width=0.5)
            page.insert_text(pymupdf.Point(rect.x0 + 5, 620), h,
                             fontsize=8, fontname="hebo", color=(1, 1, 1))
        table_data = [
            ["North America", "1,245", "87.3", "+12.4"],
            ["Europe", "982", "64.1", "+8.7"],
            ["Asia-Pacific", "1,567", "52.8", "+22.1"],
            ["Latin America", "431", "18.4", "+15.3"],
        ]
        row_colors = [(0.95, 0.95, 1.0), (1, 1, 1)]
        for ri, row in enumerate(table_data):
            bg = row_colors[ri % 2]
            for ci, val in enumerate(row):
                rect = pymupdf.Rect(80 + ci * 120, 625 + ri * 20, 80 + (ci + 1) * 120, 625 + (ri + 1) * 20)
                shape.draw_rect(rect)
                shape.finish(color=(0.7, 0.7, 0.7), fill=bg, width=0.3)
                page.insert_text(pymupdf.Point(rect.x0 + 5, rect.y1 - 5), val,
                                 fontsize=8, fontname="helv", color=(0, 0, 0))

    shape.commit()
    # Page number
    page.insert_text(pymupdf.Point(A4_W / 2 - 10, A4_H - 30),
                     str(page_num_label), fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
    return page


def create_initial():
    os.makedirs(PAPERS_DIR, exist_ok=True)
    doc = pymupdf.open()

    # Page 1: Title page / Abstract
    add_text_page(doc, "Analyzing Cross-Regional Market Dynamics in Cloud Computing",
                  [
                      "Authors: Elena Rodriguez, James Wei, Priya Sharma, David Okonkwo",
                      "Department of Business Analytics, Stanford Graduate School of Business",
                      "",
                      "Abstract",
                      "",
                      "This paper presents a comprehensive analysis of cloud computing market dynamics across",
                      "four major geographic regions: North America, Europe, Asia-Pacific, and Latin America.",
                      "Using a dataset of 2,847 enterprise deployments spanning 2020-2025, we examine adoption",
                      "patterns, revenue trajectories, and competitive positioning of major cloud service providers.",
                      "Our findings reveal significant heterogeneity in adoption rates, with Asia-Pacific showing",
                      "the highest compound annual growth rate (CAGR) of 22.1%, while North America maintains",
                      "the largest absolute market share at 38.4%. We introduce a novel multi-factor regression",
                      "model that accounts for regulatory environment, infrastructure maturity, and workforce",
                      "digital literacy as predictors of enterprise cloud adoption. The model achieves an R-squared",
                      "of 0.87, substantially outperforming prior approaches. Our results have implications for",
                      "technology firms seeking to optimize their go-to-market strategies and for policymakers",
                      "aiming to accelerate digital transformation in their jurisdictions.",
                      "",
                      "Keywords: cloud computing, market dynamics, regional analysis, enterprise adoption,",
                      "digital transformation, technology strategy",
                      "",
                      "1. Introduction",
                      "",
                      "The global cloud computing market has experienced unprecedented growth over the past",
                      "decade, reaching an estimated $623 billion in total addressable market by 2025. However,",
                      "this growth has been unevenly distributed across geographic regions, creating both",
                      "opportunities and challenges for technology providers and enterprise customers alike.",
                      "",
                      "Prior research has largely focused on aggregate global trends or single-country case",
                      "studies, leaving a gap in our understanding of cross-regional dynamics. Specifically,",
                      "existing frameworks fail to account for the interplay between regulatory environments,",
                      "infrastructure readiness, and cultural factors that shape adoption patterns.",
                      "",
                      "In this paper, we address this gap by conducting a systematic cross-regional analysis",
                      "of cloud computing adoption patterns. Our contributions are threefold: (1) we compile",
                      "the most comprehensive dataset of enterprise cloud deployments to date, (2) we develop",
                      "a multi-factor predictive model that captures regional heterogeneity, and (3) we derive",
                      "actionable insights for market entry and expansion strategies.",
                  ], 1)

    # Page 2: Literature Review
    add_text_page(doc, "2. Literature Review",
                  [
                      "",
                      "2.1 Cloud Computing Adoption Theories",
                      "",
                      "The Technology Acceptance Model (TAM) proposed by Davis (1989) remains the most widely",
                      "cited framework for understanding technology adoption at the individual level. However,",
                      "enterprise-level adoption decisions involve additional factors including organizational",
                      "readiness, competitive pressure, and regulatory compliance requirements.",
                      "",
                      "Rogers' Diffusion of Innovation (DOI) theory provides a complementary lens, particularly",
                      "useful for understanding the S-curve adoption patterns observed in different regions.",
                      "Tornatzky and Fleischer's TOE framework integrates technological, organizational, and",
                      "environmental contexts to explain enterprise technology adoption decisions.",
                      "",
                      "2.2 Regional Market Studies",
                      "",
                      "Chen et al. (2023) analyzed cloud adoption in the Asia-Pacific region, identifying",
                      "government digital transformation initiatives as the primary driver of growth. Their",
                      "study of 340 enterprises in six countries found that regulatory clarity increased",
                      "adoption probability by 34% controlling for firm size and industry.",
                      "",
                      "Mueller and Schmidt (2024) examined the European market with particular attention to",
                      "GDPR's impact on cloud deployment choices. They reported a 12% shift toward European",
                      "cloud providers in the period 2020-2023, driven primarily by data residency concerns.",
                      "",
                      "Santos and Oliveira (2023) provided the first comprehensive study of Latin American",
                      "cloud markets, documenting rapid growth in Brazil and Mexico while identifying",
                      "infrastructure gaps in smaller economies as key barriers to adoption.",
                      "",
                      "2.3 Predictive Modeling Approaches",
                      "",
                      "Prior quantitative analyses of cloud market dynamics have employed various approaches,",
                      "including time-series forecasting (Gupta & Jain, 2022), panel regression (Kim et al.,",
                      "2023), and machine learning methods (Zhou & Wang, 2024). However, none of these",
                      "studies attempted to model cross-regional heterogeneity in a unified framework.",
                      "",
                      "Our approach builds on the panel regression methodology of Kim et al. while",
                      "incorporating region-specific fixed effects and interaction terms that capture the",
                      "unique dynamics of each geographic market.",
                  ], 2)

    # Page 3: Methodology
    add_text_page(doc, "3. Methodology",
                  [
                      "",
                      "3.1 Data Collection",
                      "",
                      "Our dataset comprises 2,847 enterprise cloud deployment records collected from three",
                      "primary sources: (1) structured surveys administered to CTO/CIO-level executives at",
                      "Fortune 2000 companies, (2) public financial disclosures and technology spending",
                      "reports, and (3) anonymized telemetry data provided by three major cloud service",
                      "providers under non-disclosure agreements.",
                      "",
                      "The data spans the period January 2020 through December 2025, with quarterly",
                      "granularity for financial metrics and monthly granularity for usage statistics.",
                      "Geographic coverage includes 42 countries across four macro-regions.",
                      "",
                      "3.2 Variables and Measurement",
                      "",
                      "Dependent variable: Cloud Adoption Index (CAI) - a composite measure combining",
                      "workload migration percentage, cloud spend as proportion of IT budget, and number",
                      "of cloud-native applications deployed.",
                      "",
                      "Independent variables:",
                      "  - Regulatory Environment Score (RES): 1-10 scale based on 14 policy dimensions",
                      "  - Infrastructure Maturity Index (IMI): composite of broadband penetration, data",
                      "    center density, and network latency metrics",
                      "  - Workforce Digital Literacy (WDL): derived from OECD PIAAC data and regional",
                      "    equivalents for non-OECD countries",
                      "  - Competitive Intensity (CI): Herfindahl-Hirschman Index of cloud provider",
                      "    market concentration in each region",
                      "",
                      "3.3 Model Specification",
                      "",
                      "We employ a hierarchical panel regression model with region-specific random",
                      "intercepts and slopes:",
                      "",
                      "  CAI_it = alpha_r + beta_1r * RES_it + beta_2r * IMI_it + beta_3r * WDL_it",
                      "           + beta_4 * CI_it + gamma * X_it + epsilon_it",
                      "",
                      "where r denotes region and X_it represents a vector of firm-level controls",
                      "including industry sector, firm size, and years since cloud adoption initiation.",
                  ], 3)

    # Pages 4-6: Colorful figures
    add_figure_page(doc, "4. Results", 4)
    add_figure_page(doc, "4. Results (continued)", 5)
    add_figure_page(doc, "4. Results (continued)", 6)

    # Page 7: Discussion
    add_text_page(doc, "5. Discussion",
                  [
                      "",
                      "5.1 Interpretation of Key Findings",
                      "",
                      "Our analysis reveals several noteworthy patterns in cross-regional cloud adoption",
                      "dynamics. First, the Asia-Pacific region's exceptional growth rate of 22.1% CAGR",
                      "is driven primarily by government-led digital transformation initiatives in China,",
                      "India, and Southeast Asian nations. The Regulatory Environment Score emerges as the",
                      "strongest predictor in this region (beta = 0.43, p < 0.001).",
                      "",
                      "In contrast, North America's adoption patterns are best predicted by Competitive",
                      "Intensity (beta = 0.38, p < 0.001), suggesting that market dynamics rather than",
                      "regulatory factors drive enterprise decisions in mature markets.",
                      "",
                      "The European market presents a unique case where Infrastructure Maturity shows",
                      "a non-linear relationship with adoption, with a distinct plateau effect above",
                      "IMI scores of 7.5. We attribute this to the GDPR-induced shift toward data",
                      "sovereignty solutions, which has temporarily dampened adoption velocity despite",
                      "excellent infrastructure availability.",
                      "",
                      "5.2 Practical Implications",
                      "",
                      "For cloud service providers, our findings suggest differentiated go-to-market",
                      "strategies are essential. In high-growth markets like Asia-Pacific, partnerships",
                      "with government agencies and investment in local compliance capabilities should",
                      "be prioritized. In mature markets, competitive differentiation through specialized",
                      "industry solutions and hybrid cloud architectures will be more impactful.",
                      "",
                      "For enterprise customers, our model provides a decision framework for evaluating",
                      "cloud deployment strategies across different geographies. The regional coefficients",
                      "can be used to estimate expected adoption trajectories and benchmark organizational",
                      "progress against industry trends.",
                  ], 7)

    # Page 8: Discussion continued
    add_text_page(doc, "5. Discussion (continued)",
                  [
                      "",
                      "5.3 Theoretical Contributions",
                      "",
                      "Our work extends the TOE framework in several important ways. First, we demonstrate",
                      "that the environmental context is not monolithic but exhibits significant regional",
                      "variation that must be explicitly modeled. The region-specific slopes in our",
                      "hierarchical model capture this heterogeneity, improving predictive accuracy by",
                      "23% compared to pooled regression approaches.",
                      "",
                      "Second, we introduce the concept of regulatory-infrastructure interaction effects,",
                      "showing that the impact of regulatory clarity on adoption is contingent on",
                      "infrastructure maturity levels. This insight reconciles seemingly contradictory",
                      "findings in prior regional studies.",
                      "",
                      "5.4 Limitations",
                      "",
                      "Several limitations should be noted. First, our dataset, while comprehensive,",
                      "may underrepresent small and medium enterprises (SMEs) that do not appear in",
                      "Fortune 2000 listings or major cloud provider records. SME adoption patterns",
                      "may differ substantially from large enterprise behavior.",
                      "",
                      "Second, the rapid pace of change in cloud computing means our model coefficients",
                      "may shift as new technologies (e.g., edge computing, quantum computing services)",
                      "reshape the competitive landscape.",
                      "",
                      "Third, while we account for regulatory environment as a predictor, we do not",
                      "model the endogenous relationship between cloud adoption and subsequent",
                      "regulatory changes, which may create feedback loops in some jurisdictions.",
                      "",
                      "5.5 Future Research Directions",
                      "",
                      "Future work should extend this analysis to include SME data and explore",
                      "industry-specific adoption models. Additionally, longitudinal studies tracking",
                      "the same enterprises over time would enable causal inference methods that",
                      "go beyond our current correlational approach.",
                  ], 8)

    # Page 9: Conclusion
    add_text_page(doc, "6. Conclusion",
                  [
                      "",
                      "This paper has presented a comprehensive cross-regional analysis of cloud computing",
                      "market dynamics using a novel dataset of 2,847 enterprise deployments. Our hierarchical",
                      "panel regression model reveals significant heterogeneity in the drivers of cloud",
                      "adoption across North America, Europe, Asia-Pacific, and Latin America.",
                      "",
                      "Key findings include: (1) regulatory environment is the dominant predictor in",
                      "emerging markets, while competitive intensity drives adoption in mature markets;",
                      "(2) infrastructure maturity has a non-linear relationship with adoption in Europe,",
                      "influenced by data sovereignty concerns; (3) workforce digital literacy serves as",
                      "a universal enabler across all regions but has the strongest marginal impact in",
                      "Latin America.",
                      "",
                      "Our multi-factor model achieves an R-squared of 0.87, substantially outperforming",
                      "prior approaches and providing a practical tool for technology firms and policymakers",
                      "seeking to understand and influence cloud adoption trajectories.",
                      "",
                      "As the cloud computing landscape continues to evolve rapidly, ongoing monitoring",
                      "and model refinement will be essential. We release our regional benchmark data and",
                      "model implementation code to facilitate replication and extension of this work.",
                      "",
                      "",
                      "Acknowledgments",
                      "",
                      "We thank the three cloud service providers who provided anonymized telemetry data",
                      "under non-disclosure agreements. This research was supported by the Stanford",
                      "Institute for Economic Policy Research and the National Science Foundation",
                      "(Grant No. IIS-2024-1847).",
                  ], 9)

    # Page 10: References
    add_text_page(doc, "References",
                  [
                      "",
                      "Chen, L., Huang, Y., & Park, S. (2023). Government-led digital transformation and",
                      "  cloud adoption in Asia-Pacific economies. MIS Quarterly, 47(2), 521-548.",
                      "",
                      "Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance",
                      "  of information technology. MIS Quarterly, 13(3), 319-340.",
                      "",
                      "Gupta, R., & Jain, A. (2022). Forecasting cloud computing market trends: A comparative",
                      "  study of time-series methods. Technological Forecasting and Social Change, 178, 121572.",
                      "",
                      "Kim, J., Lee, D., & Tanaka, K. (2023). Panel regression analysis of enterprise cloud",
                      "  adoption across OECD countries. Information Systems Research, 34(1), 189-212.",
                      "",
                      "Mueller, T., & Schmidt, H. (2024). The GDPR effect: How data privacy regulation shapes",
                      "  cloud deployment decisions in Europe. European Journal of IS, 33(2), 178-196.",
                      "",
                      "Rogers, E. M. (2003). Diffusion of Innovations (5th ed.). Free Press.",
                      "",
                      "Santos, A., & Oliveira, M. (2023). Cloud computing adoption in Latin America: Drivers,",
                      "  barriers, and the infrastructure gap. Journal of Global Information Technology Management,",
                      "  26(4), 289-312.",
                      "",
                      "Tornatzky, L. G., & Fleischer, M. (1990). The Processes of Technological Innovation.",
                      "  Lexington Books.",
                      "",
                      "Zhou, W., & Wang, X. (2024). Machine learning approaches to cloud market prediction:",
                      "  A multi-region comparative study. Decision Support Systems, 167, 113945.",
                  ], 10)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
