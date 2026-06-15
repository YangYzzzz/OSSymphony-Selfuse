"""
Initial Setup: Create chapter PDF files for pdftk merging task
Task ID: pdf_basic_146
Domain: pdf

Creates three PDF files on the Desktop:
  - chapter1.pdf (20 pages) - Introduction and Background
  - chapter2.pdf (25 pages) - Main Analysis
  - chapter3.pdf (18 pages) - Conclusions

The agent must use pdftk to combine them into volume1.pdf with blank pages between chapters.
"""

import os
import shlex
import subprocess
import time
import pymupdf  # PyMuPDF

WORKDIR = '/home/user/Desktop'
TASK_ID = 'pdf_basic_146'

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


def create_chapter_pdf(output_path: str, chapter_num: int, num_pages: int,
                       chapter_title: str, chapter_intro: str, sections: list):
    """Create a realistic chapter PDF with given number of pages."""
    doc = pymupdf.open()

    # Color scheme
    title_color = (0.1, 0.2, 0.5)     # dark navy
    heading_color = (0.2, 0.4, 0.6)   # medium blue
    text_color = (0.1, 0.1, 0.1)      # near black
    page_num_color = (0.4, 0.4, 0.4)  # gray

    pages_created = 0

    # Page 1: Chapter title page
    page = doc.new_page(width=612, height=792)  # US Letter
    # Title
    page.insert_text(
        pymupdf.Point(72, 200),
        f"Chapter {chapter_num}",
        fontsize=14,
        fontname="hebo",
        color=heading_color,
    )
    page.insert_text(
        pymupdf.Point(72, 240),
        chapter_title,
        fontsize=24,
        fontname="hebo",
        color=title_color,
    )
    # Decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 270), pymupdf.Point(540, 270))
    shape.finish(color=heading_color, width=2)
    shape.commit()
    # Intro text
    intro_rect = pymupdf.Rect(72, 290, 540, 500)
    page.insert_textbox(
        intro_rect,
        chapter_intro,
        fontsize=11,
        fontname="helv",
        color=text_color,
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    # Page number
    page.insert_text(
        pymupdf.Point(540, 770),
        "1",
        fontsize=9,
        fontname="helv",
        color=page_num_color,
    )
    pages_created += 1

    # Generate remaining pages with section content
    section_idx = 0
    page_num = 2

    # Content paragraphs for body pages
    body_paragraphs = [
        "The empirical evidence gathered over the course of this study reveals several "
        "significant patterns in the data. When examining the longitudinal trends, we observe "
        "a consistent correlation between the primary variables under consideration. This "
        "finding aligns with the theoretical framework established in prior literature.",

        "Furthermore, the quantitative analysis demonstrates that the variance in observed "
        "outcomes can be attributed to three primary factors. First, the underlying structural "
        "characteristics of the sample population show considerable heterogeneity. Second, "
        "external environmental conditions exert measurable influence on the dependent "
        "variables. Third, methodological considerations must be accounted for when "
        "interpreting these results.",

        "A closer examination of the cross-sectional data reveals important subgroup "
        "differences that merit further investigation. The disaggregated analysis shows "
        "that while overall trends are consistent, specific demographic segments exhibit "
        "markedly different response patterns. These nuances have important implications "
        "for both theoretical development and practical applications.",

        "The statistical models employed in this analysis were selected based on their "
        "suitability for the data structure and research questions at hand. Ordinary least "
        "squares regression was used for continuous outcome variables, while logistic "
        "regression was applied for binary outcomes. All models were evaluated for "
        "goodness of fit and diagnostic assumptions were verified.",

        "Robustness checks were performed by varying the model specifications and using "
        "alternative estimation techniques. The core findings remained stable across "
        "these different approaches, providing confidence in the reliability of the "
        "results. Sensitivity analyses also confirmed that the conclusions are not "
        "driven by outliers or influential observations.",

        "The implications of these findings extend beyond the immediate scope of this "
        "study. Policy makers and practitioners in the field can draw on these results "
        "to inform decision-making processes. The evidence suggests that targeted "
        "interventions would yield the most effective outcomes when focused on the "
        "identified key drivers of change.",

        "Limitations of the current analysis should be noted. The cross-sectional design "
        "precludes causal inference, and selection bias may affect the generalizability "
        "of the findings. Future research employing longitudinal or experimental designs "
        "would provide stronger causal evidence for the relationships identified here.",

        "Comparative analysis with similar studies conducted in other contexts reveals "
        "both commonalities and divergences. The convergent findings across multiple "
        "studies strengthen confidence in the core conclusions, while divergent results "
        "highlight the importance of contextual factors and suggest areas for further "
        "theoretical development.",
    ]

    while pages_created < num_pages:
        page = doc.new_page(width=612, height=792)

        # Section header (every few pages)
        y_pos = 72
        if section_idx < len(sections) and (page_num - 1) % 3 == 0:
            page.insert_text(
                pymupdf.Point(72, y_pos),
                sections[section_idx % len(sections)],
                fontsize=13,
                fontname="hebo",
                color=heading_color,
            )
            section_idx += 1
            # Underline
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, y_pos + 5), pymupdf.Point(400, y_pos + 5))
            shape.finish(color=heading_color, width=0.5)
            shape.commit()
            y_pos += 25

        # Body text
        para_idx = (pages_created - 1) % len(body_paragraphs)
        text_rect = pymupdf.Rect(72, y_pos, 540, 740)
        page.insert_textbox(
            text_rect,
            body_paragraphs[para_idx] + "\n\n" + body_paragraphs[(para_idx + 1) % len(body_paragraphs)],
            fontsize=11,
            fontname="helv",
            color=text_color,
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Page number
        page.insert_text(
            pymupdf.Point(540, 770),
            str(page_num),
            fontsize=9,
            fontname="helv",
            color=page_num_color,
        )

        pages_created += 1
        page_num += 1

    doc.save(output_path)
    doc.close()
    print(f"  Created {output_path} ({pages_created} pages)")


def create_initial():
    os.makedirs(WORKDIR, exist_ok=True)

    # --- Chapter 1: Introduction and Background (20 pages) ---
    create_chapter_pdf(
        output_path=f'{WORKDIR}/chapter1.pdf',
        chapter_num=1,
        num_pages=20,
        chapter_title="Introduction and Theoretical Background",
        chapter_intro=(
            "This chapter establishes the foundational concepts and theoretical framework "
            "that underpin the entire volume. We begin by surveying the historical development "
            "of the field, tracing key milestones from the seminal works of the early researchers "
            "to contemporary developments. The theoretical models introduced here will be "
            "referenced throughout the subsequent chapters as we apply them to the empirical "
            "analysis and draw conclusions about their practical implications."
        ),
        sections=[
            "1.1 Historical Overview and Context",
            "1.2 Theoretical Framework",
            "1.3 Key Concepts and Definitions",
            "1.4 Research Objectives and Scope",
            "1.5 Organization of the Volume",
        ]
    )

    # --- Chapter 2: Main Analysis (25 pages) ---
    create_chapter_pdf(
        output_path=f'{WORKDIR}/chapter2.pdf',
        chapter_num=2,
        num_pages=25,
        chapter_title="Empirical Analysis and Findings",
        chapter_intro=(
            "Building on the theoretical foundations established in Chapter 1, this chapter "
            "presents the core empirical analysis of the study. We describe the data collection "
            "methodology, analytical procedures, and statistical methods employed. The central "
            "findings are presented systematically, organized by research question. Each finding "
            "is interpreted in light of existing theory, and its significance for both theoretical "
            "advancement and practical application is discussed in detail."
        ),
        sections=[
            "2.1 Data Collection and Sample Characteristics",
            "2.2 Descriptive Statistics and Preliminary Analysis",
            "2.3 Primary Regression Models",
            "2.4 Subgroup Analysis and Heterogeneity",
            "2.5 Robustness Checks and Sensitivity Analysis",
            "2.6 Discussion of Key Findings",
        ]
    )

    # --- Chapter 3: Conclusions (18 pages) ---
    create_chapter_pdf(
        output_path=f'{WORKDIR}/chapter3.pdf',
        chapter_num=3,
        num_pages=18,
        chapter_title="Conclusions and Future Directions",
        chapter_intro=(
            "This concluding chapter synthesizes the findings from the preceding analysis "
            "and situates them within the broader scholarly conversation. We revisit the "
            "research questions posed at the outset and evaluate the extent to which they "
            "have been addressed. The contributions of this work to the field are highlighted, "
            "followed by a candid discussion of limitations and avenues for future research. "
            "Practical implications for practitioners and policy makers are also outlined."
        ),
        sections=[
            "3.1 Summary of Principal Findings",
            "3.2 Theoretical Contributions",
            "3.3 Practical Implications",
            "3.4 Limitations and Caveats",
            "3.5 Future Research Directions",
        ]
    )

    # Verify all files created
    for fname in ['chapter1.pdf', 'chapter2.pdf', 'chapter3.pdf']:
        fpath = f'{WORKDIR}/{fname}'
        if os.path.exists(fpath):
            doc = pymupdf.open(fpath)
            print(f"Verified: {fname} — {doc.page_count} pages, {os.path.getsize(fpath)} bytes")
            doc.close()
        else:
            print(f"ERROR: {fname} not found!")

    print(f'\nInitial files created in {WORKDIR}')
    print('NOTE: volume1.pdf does NOT exist yet (task is to create it)')

    # GUI: open file manager on Desktop so agent can see the files
    launch_gui(f'nautilus {WORKDIR}', delay_sec=1.5)
    # Also open one of the chapter files in evince so the agent knows the context
    launch_gui(f'evince "{WORKDIR}/chapter1.pdf"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus and Evince with DISPLAY=:0')


create_initial()
