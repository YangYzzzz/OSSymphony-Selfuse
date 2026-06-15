"""
Initial Setup: Create a 10-page accessibility research paper PDF with 4 embedded figures, no alt text.
Task ID: pdf_res_020
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import struct
import zlib

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf


WORKDIR = '/home/user'
TASK_ID = 'pdf_res_020'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/accessibility_paper.pdf'


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


def create_simple_png(width, height, r, g, b, label=""):
    """Create a simple PNG image in memory with a colored background and optional label pattern."""
    import io

    # Create raw pixel data - simple colored rectangle with a border
    rows = []
    for y in range(height):
        row = bytearray()
        for x in range(width):
            # Draw a border
            if x < 3 or x >= width - 3 or y < 3 or y >= height - 3:
                row.extend([40, 40, 40])  # dark gray border
            # Draw a simple cross pattern in center area for visual interest
            elif abs(x - width // 2) < 2 or abs(y - height // 2) < 2:
                row.extend([min(r + 40, 255), min(g + 40, 255), min(b + 40, 255)])
            # Draw some grid lines
            elif x % 40 == 0 or y % 40 == 0:
                row.extend([max(r - 30, 0), max(g - 30, 0), max(b - 30, 0)])
            else:
                row.extend([r, g, b])
        rows.append(bytes(row))

    # Build PNG manually
    def make_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    ihdr = make_chunk(b'IHDR', ihdr_data)

    raw_data = b''
    for row in rows:
        raw_data += b'\x00' + row  # filter byte 0 (None) per row

    compressed = zlib.compress(raw_data)
    idat = make_chunk(b'IDAT', compressed)
    iend = make_chunk(b'IEND', b'')

    return signature + ihdr + idat + iend


def create_initial():
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    margin_left = 72
    margin_right = 540
    text_width = margin_right - margin_left

    # =========================================================
    # PAGE 1: Title page
    # =========================================================
    page = doc.new_page(width=W, height=H)
    y = 120

    # Title
    page.insert_text(pymupdf.Point(W / 2 - 180, y), "Advancing Digital Accessibility:",
                     fontsize=18, fontname="hebo", color=(0, 0, 0))
    y += 26
    page.insert_text(pymupdf.Point(W / 2 - 200, y), "A Comprehensive Analysis of Image",
                     fontsize=18, fontname="hebo", color=(0, 0, 0))
    y += 26
    page.insert_text(pymupdf.Point(W / 2 - 190, y), "Alt Text Implementation in PDFs",
                     fontsize=18, fontname="hebo", color=(0, 0, 0))
    y += 50

    # Authors
    authors = [
        ("Dr. Elena Vasquez", "Department of Computer Science, Stanford University"),
        ("Prof. James Whitfield", "School of Information, University of Michigan"),
        ("Dr. Aisha Patel", "Accessibility Research Lab, MIT"),
    ]
    for name, affil in authors:
        page.insert_text(pymupdf.Point(W / 2 - 120, y), name,
                         fontsize=12, fontname="hebo", color=(0, 0, 0))
        y += 16
        page.insert_text(pymupdf.Point(W / 2 - 160, y), affil,
                         fontsize=9, fontname="tiit", color=(0.3, 0.3, 0.3))
        y += 24

    y += 20
    # Abstract
    page.insert_text(pymupdf.Point(margin_left, y), "Abstract",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 20

    abstract = (
        "Digital accessibility remains a critical challenge in modern document management systems. "
        "This paper presents a comprehensive analysis of alternative text (alt text) implementation "
        "strategies for images embedded in Portable Document Format (PDF) files. Through an empirical "
        "study involving 2,847 PDF documents from academic, governmental, and corporate sources, we "
        "evaluate the current state of image accessibility. Our findings reveal that only 12.3% of "
        "analyzed documents contain adequate alt text for all embedded images, while 67.8% contain "
        "no alt text whatsoever. We propose a taxonomy of alt text quality metrics and introduce "
        "AutoAlt, an automated framework for generating contextually appropriate alternative text "
        "descriptions. Experimental results demonstrate that AutoAlt achieves a BLEU score of 0.847 "
        "and human preference rating of 4.2/5.0 when compared against professionally authored "
        "descriptions. Our work contributes to the ongoing effort to make digital documents "
        "universally accessible in compliance with WCAG 2.1 AA standards and Section 508 requirements."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 160)
    page.insert_textbox(rect, abstract, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 170

    page.insert_text(pymupdf.Point(margin_left, y),
                     "Keywords: accessibility, alt text, PDF, screen readers, WCAG, assistive technology",
                     fontsize=9, fontname="tiit", color=(0.3, 0.3, 0.3))

    # =========================================================
    # PAGE 2: Introduction
    # =========================================================
    page = doc.new_page(width=W, height=H)
    y = 72

    page.insert_text(pymupdf.Point(margin_left, y), "1. Introduction",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 22

    intro_text = (
        "The World Health Organization estimates that approximately 2.2 billion people globally "
        "have some form of visual impairment, ranging from mild to complete blindness. For these "
        "individuals, accessing visual content in digital documents presents significant barriers "
        "to education, employment, and civic participation. Alternative text descriptions serve as "
        "the primary mechanism for conveying image content to users who rely on screen readers and "
        "other assistive technologies.\n\n"
        "The Portable Document Format (PDF), developed by Adobe Systems and standardized as ISO 32000, "
        "has become the de facto standard for document exchange across academic, governmental, and "
        "corporate environments. Despite the format's support for accessibility features through "
        "tagged PDF structures, the implementation of image alt text remains inconsistent and often "
        "entirely absent. This gap in accessibility creates a digital divide that disproportionately "
        "affects individuals with visual impairments.\n\n"
        "Previous research by Morrison et al. (2021) examined alt text patterns in web content, "
        "finding that approximately 23% of images on the top 1,000 websites lacked any alternative "
        "text. However, the situation in PDF documents is considerably less studied, despite PDFs "
        "accounting for an estimated 35% of all digital documents shared in professional settings "
        "(Henderson & Park, 2022).\n\n"
        "In this paper, we address three research questions: (RQ1) What is the current state of "
        "alt text implementation across different document sectors? (RQ2) What quality metrics "
        "can effectively evaluate alt text descriptions? (RQ3) Can automated methods generate "
        "alt text of sufficient quality for practical deployment?"
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 450)
    page.insert_textbox(rect, intro_text, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 460

    page.insert_text(pymupdf.Point(margin_left, y), "Our contributions are threefold:",
                     fontsize=10, fontname="tiro", color=(0, 0, 0))
    y += 18
    contributions = [
        "1. A large-scale empirical analysis of 2,847 PDF documents across three sectors",
        "2. A taxonomy of alt text quality metrics with inter-rater reliability scores",
        "3. AutoAlt, an automated framework achieving near-human performance in alt text generation",
    ]
    for c in contributions:
        page.insert_text(pymupdf.Point(margin_left + 20, y), c,
                         fontsize=10, fontname="tiro", color=(0, 0, 0))
        y += 16

    # =========================================================
    # PAGE 3: Related Work
    # =========================================================
    page = doc.new_page(width=W, height=H)
    y = 72

    page.insert_text(pymupdf.Point(margin_left, y), "2. Related Work",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 22

    related_text = (
        "2.1 Web Accessibility Standards\n\n"
        "The Web Content Accessibility Guidelines (WCAG) published by the World Wide Web Consortium "
        "(W3C) provide the foundational framework for digital accessibility. WCAG 2.1, released in "
        "June 2018, establishes four principles: perceivable, operable, understandable, and robust "
        "(POUR). Guideline 1.1 specifically addresses text alternatives, requiring that all non-text "
        "content has a text alternative that serves an equivalent purpose.\n\n"
        "2.2 PDF Accessibility\n\n"
        "The PDF/UA (Universal Accessibility) standard, formalized as ISO 14289-1:2014, extends "
        "general accessibility principles to the PDF format. Chisholm and Vanderheiden (2019) "
        "conducted a systematic review of PDF accessibility tools, finding that while authoring "
        "tools have improved significantly, retroactive remediation of existing documents remains "
        "the primary challenge. Brady and López (2020) developed a taxonomy of PDF accessibility "
        "barriers, identifying image alt text as the most frequently encountered issue in their "
        "analysis of 500 governmental documents.\n\n"
        "2.3 Automated Image Description\n\n"
        "Recent advances in computer vision and natural language processing have enabled automated "
        "image captioning systems. Show and Tell (Vinyals et al., 2015) and its successor Show, "
        "Attend and Tell (Xu et al., 2015) pioneered the encoder-decoder approach using CNNs and "
        "RNNs. More recently, transformer-based models such as BLIP-2 (Li et al., 2023) and "
        "GPT-4V (OpenAI, 2023) have demonstrated remarkable capability in generating detailed "
        "image descriptions. However, the application of these models specifically to document "
        "accessibility contexts has received limited attention.\n\n"
        "2.4 Alt Text Quality Assessment\n\n"
        "Evaluating the quality of alternative text descriptions remains an open challenge. "
        "Stangl et al. (2020) proposed a framework distinguishing between objective descriptions "
        "(what is visually present) and subjective interpretations (what the image means in context). "
        "Salisbury et al. (2017) found that context-dependent descriptions were significantly more "
        "useful for screen reader users than generic object-level descriptions."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 530)
    page.insert_textbox(rect, related_text, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # =========================================================
    # PAGE 4: Methodology + Figure 1
    # =========================================================
    page = doc.new_page(width=W, height=H)
    y = 72

    page.insert_text(pymupdf.Point(margin_left, y), "3. Methodology",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 22

    method_text = (
        "3.1 Data Collection\n\n"
        "We assembled a corpus of 2,847 PDF documents from three sectors: academic publications "
        "(n=1,203), governmental reports (n=892), and corporate documents (n=752). Academic papers "
        "were sampled from arXiv, PubMed Central, and IEEE Xplore, covering publications from "
        "2019 to 2024. Governmental documents were collected from federal, state, and municipal "
        "websites across 12 countries. Corporate documents included annual reports, technical "
        "manuals, and marketing materials from Fortune 500 companies.\n\n"
        "3.2 Analysis Framework\n\n"
        "Each document was analyzed using a custom Python toolkit built on PyMuPDF and pikepdf. "
        "The analysis pipeline extracted all embedded images, checked for the presence of tagged "
        "structure elements, and evaluated any existing alt text against our quality metrics. "
        "Figure 1 illustrates our analysis pipeline architecture."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 220)
    page.insert_textbox(rect, method_text, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 230

    # Figure 1: Analysis pipeline diagram (blue-toned)
    fig1_data = create_simple_png(400, 180, 70, 130, 200)
    img_rect = pymupdf.Rect(margin_left + 30, y, margin_right - 30, y + 180)
    page.insert_image(img_rect, stream=fig1_data)
    y += 190
    page.insert_text(pymupdf.Point(margin_left + 60, y),
                     "Figure 1: Document analysis pipeline architecture showing the",
                     fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 14
    page.insert_text(pymupdf.Point(margin_left + 60, y),
                     "multi-stage extraction and evaluation workflow.",
                     fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 24

    more_method = (
        "3.3 Quality Metrics\n\n"
        "We developed a five-dimensional quality assessment framework for alt text evaluation: "
        "(1) Accuracy - does the description correctly identify the image content; "
        "(2) Completeness - does it convey all essential information; "
        "(3) Conciseness - is it appropriately brief without losing meaning; "
        "(4) Context - does it relate to the surrounding document content; "
        "(5) Actionability - does it enable the reader to understand the image's purpose."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 110)
    page.insert_textbox(rect, more_method, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # =========================================================
    # PAGE 5: Results + Figure 2
    # =========================================================
    page = doc.new_page(width=W, height=H)
    y = 72

    page.insert_text(pymupdf.Point(margin_left, y), "4. Results",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 22

    results_text = (
        "4.1 Current State of Alt Text Implementation\n\n"
        "Our analysis reveals a concerning landscape of image accessibility across all three "
        "sectors examined. Of the 2,847 documents analyzed, containing a total of 18,392 embedded "
        "images, only 2,264 images (12.3%) had any form of alternative text. The distribution "
        "varied significantly across sectors, as shown in Figure 2."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 90)
    page.insert_textbox(rect, results_text, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 100

    # Figure 2: Bar chart showing alt text coverage (green-toned)
    fig2_data = create_simple_png(420, 200, 80, 170, 100)
    img_rect = pymupdf.Rect(margin_left + 20, y, margin_right - 20, y + 200)
    page.insert_image(img_rect, stream=fig2_data)
    y += 210
    page.insert_text(pymupdf.Point(margin_left + 40, y),
                     "Figure 2: Alt text coverage rates across academic, governmental,",
                     fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 14
    page.insert_text(pymupdf.Point(margin_left + 40, y),
                     "and corporate document sectors (n=2,847 documents).",
                     fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 24

    more_results = (
        "Academic publications had the lowest alt text adoption rate at 8.7%, followed by "
        "corporate documents at 11.2% and governmental reports at 19.4%. The higher rate in "
        "governmental documents likely reflects the regulatory pressure from Section 508 of the "
        "Rehabilitation Act, which mandates accessibility for federal electronic information.\n\n"
        "Among documents that did contain alt text, we found significant quality variation. "
        "Using our five-dimensional quality framework, the mean score was 2.8 out of 5.0, "
        "with accuracy scoring highest (3.4) and context scoring lowest (2.1)."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 130)
    page.insert_textbox(rect, more_results, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # =========================================================
    # PAGE 6: More Results + Figure 3
    # =========================================================
    page = doc.new_page(width=W, height=H)
    y = 72

    page.insert_text(pymupdf.Point(margin_left, y),
                     "4.2 Quality Assessment Results",
                     fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20

    quality_text = (
        "To evaluate the quality of existing alt text, three trained annotators independently "
        "rated a random sample of 500 image-alt text pairs using our five-dimensional framework. "
        "Inter-rater reliability was measured using Fleiss' kappa, yielding a value of 0.78, "
        "indicating substantial agreement.\n\n"
        "The distribution of quality scores across dimensions is presented in Figure 3. Notable "
        "patterns emerged: accuracy scores were relatively high, indicating that when alt text was "
        "provided, it generally described the correct content. However, context scores were "
        "consistently low, suggesting that authors failed to connect image descriptions to the "
        "surrounding narrative."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 140)
    page.insert_textbox(rect, quality_text, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 150

    # Figure 3: Quality score distribution (orange-toned)
    fig3_data = create_simple_png(380, 190, 210, 140, 70)
    img_rect = pymupdf.Rect(margin_left + 40, y, margin_right - 40, y + 190)
    page.insert_image(img_rect, stream=fig3_data)
    y += 200
    page.insert_text(pymupdf.Point(margin_left + 50, y),
                     "Figure 3: Distribution of alt text quality scores across the",
                     fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 14
    page.insert_text(pymupdf.Point(margin_left + 50, y),
                     "five evaluation dimensions (n=500 image-alt text pairs).",
                     fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 24

    more_quality = (
        "A particularly concerning finding was the prevalence of placeholder alt text. Approximately "
        "18.3% of images with alt text contained generic descriptions such as 'image', 'figure', "
        "or 'chart' without any meaningful content description. These placeholder texts technically "
        "satisfy automated accessibility checkers but provide no useful information to assistive "
        "technology users.\n\n"
        "We also observed that image type significantly influenced alt text quality. Photographs "
        "received the highest quality scores (mean 3.2), while charts and graphs received the "
        "lowest (mean 2.3), likely because describing data visualizations requires understanding "
        "both the visual representation and the underlying data."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 140)
    page.insert_textbox(rect, more_quality, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # =========================================================
    # PAGE 7: AutoAlt Framework
    # =========================================================
    page = doc.new_page(width=W, height=H)
    y = 72

    page.insert_text(pymupdf.Point(margin_left, y), "5. The AutoAlt Framework",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 22

    autoalt_text = (
        "Based on our analysis findings, we developed AutoAlt, an automated framework for "
        "generating contextually appropriate alternative text for images in PDF documents. "
        "The framework operates in three stages:\n\n"
        "Stage 1: Image Extraction and Classification\n"
        "The framework extracts all embedded images from the PDF using PyMuPDF's image extraction "
        "API. Each image is classified into one of six categories: photograph, chart/graph, "
        "diagram, table image, icon/logo, and decorative. A fine-tuned ResNet-50 classifier "
        "achieves 94.2% accuracy on this task.\n\n"
        "Stage 2: Context Extraction\n"
        "Surrounding text is extracted within a 500-token window of each image's position. "
        "This context is combined with any existing captions, figure references, and section "
        "headings to form a context vector. Named Entity Recognition identifies key terms that "
        "should appear in the alt text description.\n\n"
        "Stage 3: Description Generation\n"
        "A multimodal language model (BLIP-2 fine-tuned on our curated dataset of 15,000 "
        "image-description pairs) generates the alt text. The model takes as input both the "
        "image and the extracted context, producing descriptions that are both visually accurate "
        "and contextually relevant. Post-processing ensures descriptions meet length guidelines "
        "(typically 125 characters or fewer for simple images, up to 250 for complex ones).\n\n"
        "The complete framework is implemented in Python and processes an average PDF document "
        "(15 pages, 4-6 images) in approximately 12 seconds on a single NVIDIA A100 GPU."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 400)
    page.insert_textbox(rect, autoalt_text, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # =========================================================
    # PAGE 8: Evaluation + Figure 4
    # =========================================================
    page = doc.new_page(width=W, height=H)
    y = 72

    page.insert_text(pymupdf.Point(margin_left, y), "6. Evaluation",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 22

    eval_text = (
        "6.1 Automated Metrics\n\n"
        "We evaluated AutoAlt against three baselines: (1) a template-based approach using image "
        "classification labels, (2) a vanilla BLIP-2 model without fine-tuning or context, and "
        "(3) GPT-4V with a carefully crafted prompt. Evaluation was conducted on a held-out test "
        "set of 1,200 image-description pairs.\n\n"
        "AutoAlt achieved a BLEU-4 score of 0.847, METEOR score of 0.612, and CIDEr score of "
        "1.834. These results significantly outperform the template-based baseline (BLEU-4: 0.312) "
        "and vanilla BLIP-2 (BLEU-4: 0.687). Performance was competitive with GPT-4V (BLEU-4: "
        "0.891), while requiring substantially less computational resources. Figure 4 shows the "
        "comparative performance across all metrics."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 160)
    page.insert_textbox(rect, eval_text, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 170

    # Figure 4: Comparison chart (purple-toned)
    fig4_data = create_simple_png(420, 200, 150, 100, 190)
    img_rect = pymupdf.Rect(margin_left + 20, y, margin_right - 20, y + 200)
    page.insert_image(img_rect, stream=fig4_data)
    y += 210
    page.insert_text(pymupdf.Point(margin_left + 30, y),
                     "Figure 4: Comparative performance of alt text generation methods",
                     fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 14
    page.insert_text(pymupdf.Point(margin_left + 30, y),
                     "across BLEU-4, METEOR, and CIDEr metrics (n=1,200 test pairs).",
                     fontsize=9, fontname="tiit", color=(0.2, 0.2, 0.2))
    y += 24

    eval_text2 = (
        "6.2 Human Evaluation\n\n"
        "We conducted a human evaluation with 24 participants, including 8 individuals who "
        "regularly use screen readers. Participants rated generated alt text on a 5-point Likert "
        "scale across our five quality dimensions. AutoAlt received a mean rating of 4.2/5.0, "
        "compared to 4.5/5.0 for human-authored descriptions and 3.1/5.0 for the template "
        "baseline. Screen reader users rated AutoAlt descriptions as 'helpful' or 'very helpful' "
        "in 87% of cases."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 110)
    page.insert_textbox(rect, eval_text2, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # =========================================================
    # PAGE 9: Discussion
    # =========================================================
    page = doc.new_page(width=W, height=H)
    y = 72

    page.insert_text(pymupdf.Point(margin_left, y), "7. Discussion",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 22

    discussion_text = (
        "Our findings highlight several important implications for the digital accessibility "
        "community. The low rate of alt text implementation (12.3%) across all sectors suggests "
        "that current approaches to encouraging accessibility compliance are insufficient. While "
        "regulatory frameworks like Section 508 and the European Accessibility Act provide legal "
        "mandates, the enforcement mechanisms and technical support available to document authors "
        "remain inadequate.\n\n"
        "The quality analysis reveals that even when alt text is provided, it frequently fails to "
        "meet the needs of assistive technology users. The prevalence of placeholder text (18.3%) "
        "is particularly problematic, as it creates a false sense of compliance while providing "
        "no actual benefit. Accessibility auditing tools should be enhanced to detect and flag "
        "such low-quality descriptions.\n\n"
        "AutoAlt demonstrates that automated approaches can generate alt text of near-human quality, "
        "particularly when contextual information is incorporated. However, several limitations "
        "must be acknowledged:\n\n"
        "First, the framework performs best on common image types (photographs, simple charts) "
        "and struggles with highly specialized technical diagrams, particularly in engineering "
        "and medical domains. Second, cultural context and implicit visual knowledge remain "
        "challenging for automated systems. Third, the computational requirements, while modest "
        "compared to general-purpose models, may still be prohibitive for individual users.\n\n"
        "We envision AutoAlt as a tool to assist document authors rather than replace human "
        "judgment. The framework can provide initial descriptions that authors review and refine, "
        "significantly reducing the time and effort required to make documents accessible. "
        "Integration into popular document authoring tools (Microsoft Word, Adobe Acrobat, "
        "LibreOffice) would maximize adoption and impact.\n\n"
        "7.1 Ethical Considerations\n\n"
        "Automated alt text generation raises important ethical questions about accuracy and "
        "representation. Incorrect descriptions could mislead users, while biased training data "
        "could perpetuate stereotypes in generated text. We recommend that all automated "
        "descriptions be clearly marked as machine-generated and that human review be "
        "incorporated into production workflows."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 530)
    page.insert_textbox(rect, discussion_text, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # =========================================================
    # PAGE 10: Conclusion + References
    # =========================================================
    page = doc.new_page(width=W, height=H)
    y = 72

    page.insert_text(pymupdf.Point(margin_left, y), "8. Conclusion",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 22

    conclusion_text = (
        "This paper has presented a comprehensive analysis of image alt text implementation in "
        "PDF documents and introduced AutoAlt, an automated framework for generating accessible "
        "image descriptions. Our key findings are: (1) alt text implementation remains alarmingly "
        "low across all sectors, with only 12.3% of images having any form of alternative text; "
        "(2) existing alt text frequently falls short of quality standards, particularly in "
        "contextual relevance; and (3) automated generation approaches, when incorporating document "
        "context, can achieve near-human quality at a fraction of the cost.\n\n"
        "Future work will focus on extending AutoAlt to support multilingual alt text generation, "
        "improving performance on specialized technical imagery, and conducting longitudinal "
        "studies to assess the framework's impact on document accessibility in real-world settings."
    )
    rect = pymupdf.Rect(margin_left, y, margin_right, y + 160)
    page.insert_textbox(rect, conclusion_text, fontsize=10, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 170

    page.insert_text(pymupdf.Point(margin_left, y), "References",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 20

    references = [
        "Brady, S., & López, R. (2020). A taxonomy of PDF accessibility barriers. ACM ASSETS, 112-124.",
        "Chisholm, W., & Vanderheiden, G. (2019). PDF accessibility tools: A systematic review. UAIS, 18(3), 401-418.",
        "Henderson, T., & Park, J. (2022). Digital document formats in professional communication. JCMC, 27(4), 1-19.",
        "Li, J., et al. (2023). BLIP-2: Bootstrapping language-image pre-training. ICML 2023.",
        "Morrison, A., et al. (2021). The state of web image accessibility. W4A, Article 12.",
        "OpenAI. (2023). GPT-4V Technical Report. arXiv:2303.08774.",
        "Salisbury, E., et al. (2017). Toward scalable social alt text. CSCW, 1-30.",
        "Stangl, A., et al. (2020). Person, shoes, tree. CHI 2020, 1-15.",
        "Vinyals, O., et al. (2015). Show and tell: A neural image caption generator. CVPR, 3156-3164.",
        "Xu, K., et al. (2015). Show, attend and tell: Neural image caption generation. ICML, 2048-2057.",
    ]
    for ref in references:
        rect = pymupdf.Rect(margin_left, y, margin_right, y + 28)
        page.insert_textbox(rect, ref, fontsize=8.5, fontname="tiro", color=(0, 0, 0))
        y += 28

    # Save the document
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Pages: 10, Figures: 4 (no alt text)')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
