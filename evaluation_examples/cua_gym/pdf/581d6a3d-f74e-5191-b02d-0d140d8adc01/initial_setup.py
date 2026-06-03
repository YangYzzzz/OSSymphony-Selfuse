"""
Initial Setup: Copy annotations from source PDF page 5 to target PDF page 5
Task ID: pdf_fm_048
Domain: pdf

Creates:
  - /home/user/Documents/source_review.pdf (10 pages, 4 annotations on page 5)
  - /home/user/Documents/target_review.pdf (10 pages, no annotations)
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_fm_048'
SOURCE_PDF = f'{DOCS_DIR}/source_review.pdf'
TARGET_PDF = f'{DOCS_DIR}/target_review.pdf'


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


def create_review_pdf(output_path, title_prefix):
    """Create a 10-page academic review document."""
    doc = pymupdf.open()

    # Page content for a research paper review
    pages_content = [
        {
            "title": f"{title_prefix} - Peer Review Report",
            "subtitle": "Manuscript: Adaptive Neural Architecture Search for Edge Computing",
            "body": (
                "Reviewer ID: R-2847\n"
                "Date of Review: March 15, 2025\n"
                "Journal: IEEE Transactions on Neural Networks and Learning Systems\n"
                "Manuscript ID: TNNLS-2025-P-03421\n\n"
                "This document contains the complete peer review for the above manuscript. "
                "The review covers technical soundness, novelty, clarity of presentation, "
                "experimental rigor, and relevance to the journal scope.\n\n"
                "Overall Recommendation: Major Revision\n"
                "Confidence Level: High (4/5)"
            ),
        },
        {
            "title": "1. Summary of the Paper",
            "body": (
                "The authors propose a novel framework called EdgeNAS that performs neural "
                "architecture search specifically optimized for deployment on edge devices with "
                "constrained computational resources. The key contributions include:\n\n"
                "1) A hardware-aware search space that incorporates latency and memory constraints "
                "directly into the architecture search process.\n\n"
                "2) A differentiable optimization objective that jointly minimizes classification "
                "error and inference latency on target hardware.\n\n"
                "3) A progressive search strategy that starts with a compact base architecture and "
                "gradually expands complexity only when performance gains justify the additional "
                "computational cost.\n\n"
                "The framework is evaluated on CIFAR-10, CIFAR-100, and ImageNet datasets, "
                "with deployment benchmarks on Raspberry Pi 4, NVIDIA Jetson Nano, and ARM "
                "Cortex-M7 microcontrollers."
            ),
        },
        {
            "title": "2. Technical Soundness",
            "body": (
                "The mathematical formulation of the search space is generally sound. The "
                "bi-level optimization approach (Equation 3) correctly separates architecture "
                "parameters from weight parameters. However, I have concerns about:\n\n"
                "- The approximation used in Theorem 1 assumes Lipschitz continuity of the loss "
                "landscape, which may not hold for all candidate operations, particularly "
                "attention-based blocks.\n\n"
                "- The hardware cost model in Section 3.2 uses a linear approximation of latency, "
                "but real hardware exhibits non-linear behavior due to memory hierarchy effects "
                "and operator fusion in inference engines.\n\n"
                "- The convergence proof in Appendix A relies on a fixed learning rate schedule, "
                "but the experiments use cosine annealing. This discrepancy should be addressed.\n\n"
                "The experimental setup is thorough with appropriate baselines (DARTS, ProxylessNAS, "
                "FBNet, MnasNet) and the statistical analysis includes confidence intervals."
            ),
        },
        {
            "title": "3. Novelty and Significance",
            "body": (
                "The novelty of this work is moderate. While hardware-aware NAS is not new "
                "(MnasNet, FBNet, ProxylessNAS), the progressive search strategy combined with "
                "direct hardware profiling represents a meaningful incremental contribution.\n\n"
                "The most significant contribution is the adaptive complexity expansion mechanism "
                "(Section 4.1), which allows the search to discover architectures that are Pareto-optimal "
                "in the accuracy-latency tradeoff space. This is demonstrated convincingly in "
                "Figure 5 and Table 3.\n\n"
                "However, the paper would benefit from a more thorough comparison with recent "
                "one-shot NAS methods (BigNAS, OFA) and training-free NAS approaches (NASWOT, "
                "ZenNAS), which have shown strong results with significantly reduced search costs.\n\n"
                "The practical impact is substantial for the edge computing community, as the "
                "discovered architectures achieve state-of-the-art accuracy with 2.3x lower "
                "latency compared to MobileNetV3 on the Jetson Nano benchmark."
            ),
        },
        {
            "title": "4. Experimental Evaluation",
            "body": (
                "The experimental section is comprehensive but has several areas for improvement:\n\n"
                "Table 2 Results Summary:\n"
                "  Model          | CIFAR-10 | CIFAR-100 | ImageNet Top-1 | Latency (ms)\n"
                "  EdgeNAS-Small  | 97.2%    | 83.4%     | 76.8%          | 4.2\n"
                "  EdgeNAS-Medium | 97.6%    | 85.1%     | 78.3%          | 8.7\n"
                "  EdgeNAS-Large  | 97.8%    | 86.2%     | 79.1%          | 15.3\n"
                "  MobileNetV3    | 97.1%    | 82.9%     | 75.2%          | 9.8\n"
                "  EfficientNet-B0| 97.3%    | 84.0%     | 77.1%          | 12.1\n\n"
                "Specific concerns:\n"
                "- The search cost comparison in Table 4 should include GPU hours, not just wall-clock "
                "time, as different methods use different numbers of GPUs.\n"
                "- The ablation study (Section 5.3) removes components independently but does not "
                "explore interactions between components.\n"
                "- Standard deviations are reported for only 3 runs. The community standard for "
                "NAS papers is typically 5 independent runs."
            ),
        },
        {
            "title": "5. Clarity and Presentation",
            "body": (
                "The paper is generally well-written with clear mathematical notation. The figures "
                "are informative, particularly Figure 3 showing the progressive search visualization.\n\n"
                "Areas for improvement:\n\n"
                "- Section 3.1 introduces too much notation at once. Consider breaking it into "
                "subsections for readability.\n\n"
                "- The related work section (Section 2) could be restructured to better highlight "
                "the gap this paper fills. Currently, it reads more like a survey than a motivation "
                "for the proposed approach.\n\n"
                "- Figure 4 is too small to read clearly. The legend overlaps with data points in "
                "the Pareto frontier plot.\n\n"
                "- Several grammatical issues:\n"
                "  * Page 3, line 12: 'is comprised of' should be 'comprises'\n"
                "  * Page 7, line 4: 'less parameters' should be 'fewer parameters'\n"
                "  * Page 9, line 21: dangling modifier in the sentence about convergence"
            ),
        },
        {
            "title": "6. Reproducibility Assessment",
            "body": (
                "The authors provide sufficient implementation details for reproducing the main "
                "results:\n\n"
                "- Search hyperparameters are listed in Table 5 (Appendix B)\n"
                "- Training recipes follow the standard ImageNet protocol\n"
                "- Code is promised to be released upon acceptance\n\n"
                "However, I have concerns about reproducibility of the hardware benchmarks:\n"
                "- The latency measurements depend heavily on the specific software stack "
                "(TensorRT version, CUDA version, driver version). These should be documented.\n"
                "- The Raspberry Pi benchmarks use a custom TFLite delegate that is not publicly "
                "available, making these results difficult to verify independently.\n"
                "- Thermal throttling can significantly impact latency on edge devices. The paper "
                "does not mention any thermal management during benchmarking."
            ),
        },
        {
            "title": "7. Minor Issues and Suggestions",
            "body": (
                "1. The paper claims 'real-time' performance (Abstract, line 3) but does not "
                "define what real-time means in this context. A frame rate threshold should be "
                "specified.\n\n"
                "2. Reference [23] appears to be a preprint that has since been published. "
                "Please update the citation.\n\n"
                "3. The comparison with EfficientNet uses the original training recipe from the "
                "2019 paper. Consider comparing against EfficientNetV2 with the updated training "
                "protocol for a fairer comparison.\n\n"
                "4. Table 3: Memory consumption should be reported in addition to latency, as "
                "edge devices are often memory-constrained.\n\n"
                "5. The transfer learning experiments (Section 5.4) only cover classification. "
                "It would strengthen the paper to show that the discovered architectures transfer "
                "well to detection or segmentation tasks.\n\n"
                "6. Consider adding an energy consumption comparison, as this is increasingly "
                "important for sustainable edge AI deployment."
            ),
        },
        {
            "title": "8. Questions for the Authors",
            "body": (
                "Q1: How sensitive is the search outcome to the choice of target hardware? If "
                "the search is performed on Jetson Nano, do the discovered architectures also "
                "perform well on Raspberry Pi, or is a separate search needed?\n\n"
                "Q2: The progressive expansion mechanism adds complexity to the search process. "
                "What is the overhead compared to a fixed search space of equivalent size?\n\n"
                "Q3: Have you experimented with knowledge distillation to further improve the "
                "compact architectures discovered by EdgeNAS-Small?\n\n"
                "Q4: The paper mentions that the search space includes attention operations. "
                "What percentage of the final architectures actually use attention, and in which "
                "layers?\n\n"
                "Q5: Could the progressive expansion strategy be combined with weight sharing "
                "approaches to reduce search cost further?"
            ),
        },
        {
            "title": "9. Final Recommendation",
            "body": (
                "This paper presents a solid contribution to the hardware-aware NAS literature "
                "with practical relevance for edge deployment. The progressive search strategy "
                "is interesting and the experimental results are promising.\n\n"
                "However, the paper requires major revisions to address:\n"
                "1. The theoretical gap between convergence proof assumptions and actual training\n"
                "2. Additional baselines with recent one-shot and training-free NAS methods\n"
                "3. More rigorous statistical analysis with 5+ independent runs\n"
                "4. Better documentation of hardware benchmarking conditions\n\n"
                "I recommend Major Revision. The core idea is sound and the paper has potential "
                "to make a significant impact, but the current version has notable gaps in both "
                "theory and experimentation that need to be addressed.\n\n"
                "Score: 5.5/10 (Borderline - Lean Reject, but could become Accept with revisions)\n"
                "Confidence: 4/5 (I am familiar with this area of research)"
            ),
        },
    ]

    for i, page_info in enumerate(pages_content):
        page = doc.new_page(width=595, height=842)  # A4

        # Title
        page.insert_text(
            pymupdf.Point(72, 60),
            page_info["title"],
            fontsize=16,
            fontname="hebo",
            color=(0, 0, 0.5),
        )

        # Horizontal rule under title
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(523, 70))
        shape.finish(color=(0, 0, 0.5), width=1)
        shape.commit()

        # Subtitle if present
        y_start = 90
        if "subtitle" in page_info:
            page.insert_text(
                pymupdf.Point(72, y_start),
                page_info["subtitle"],
                fontsize=11,
                fontname="tiit",
                color=(0.3, 0.3, 0.3),
            )
            y_start += 25

        # Body text
        rect = pymupdf.Rect(72, y_start, 523, 790)
        page.insert_textbox(
            rect,
            page_info["body"],
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Page number at bottom
        page.insert_text(
            pymupdf.Point(280, 820),
            f"Page {i + 1} of 10",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(output_path)
    doc.close()
    return output_path


def add_annotations_to_source(source_path):
    """Add 4 annotations to page 5 (index 4) of the source PDF:
    2 highlights and 2 sticky notes."""
    import tempfile, shutil
    doc = pymupdf.open(source_path)
    page = doc[4]  # Page 5 (0-indexed = 4)

    # Highlight 1: Yellow highlight on "experimental section is comprehensive"
    instances = page.search_for("experimental section is comprehensive")
    if instances:
        highlight = page.add_highlight_annot(instances[0])
        highlight.set_colors(stroke=(1, 1, 0))  # Yellow
        highlight.set_info(content="Key claim - needs evidence", title="Reviewer")
        highlight.update()
    else:
        highlight = page.add_highlight_annot(pymupdf.Rect(72, 100, 400, 115))
        highlight.set_colors(stroke=(1, 1, 0))
        highlight.set_info(content="Key claim - needs evidence", title="Reviewer")
        highlight.update()

    # Highlight 2: Green highlight on "search cost comparison"
    instances2 = page.search_for("search cost comparison")
    if instances2:
        highlight2 = page.add_highlight_annot(instances2[0])
        highlight2.set_colors(stroke=(0, 1, 0))  # Green
        highlight2.set_info(content="Good methodological point", title="Reviewer")
        highlight2.update()
    else:
        highlight2 = page.add_highlight_annot(pymupdf.Rect(72, 400, 350, 415))
        highlight2.set_colors(stroke=(0, 1, 0))
        highlight2.set_info(content="Good methodological point", title="Reviewer")
        highlight2.update()

    # Sticky Note 1: Comment about Table 2
    note1 = page.add_text_annot(
        pymupdf.Point(480, 180),
        "The results in Table 2 look promising, but please verify the latency "
        "measurements were taken under controlled thermal conditions.",
        icon="Comment",
    )
    note1.set_colors(stroke=(1, 0.8, 0))  # Orange
    note1.set_info(title="Reviewer A")
    note1.update()

    # Sticky Note 2: Comment about standard deviations
    note2 = page.add_text_annot(
        pymupdf.Point(480, 500),
        "Three runs is insufficient for statistical significance. Please increase "
        "to at least 5 independent runs with different random seeds.",
        icon="Note",
    )
    note2.set_colors(stroke=(1, 0, 0))  # Red
    note2.set_info(title="Reviewer A")
    note2.update()

    # Save to temp file then replace (can't save in-place without incremental)
    tmp = source_path + '.tmp'
    doc.save(tmp)
    doc.close()
    shutil.move(tmp, source_path)


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Create source_review.pdf with content
    print("Creating source_review.pdf...")
    create_review_pdf(SOURCE_PDF, "SOURCE")

    # Add annotations to page 5 of source
    print("Adding annotations to source_review.pdf page 5...")
    add_annotations_to_source(SOURCE_PDF)

    # Verify annotations
    doc = pymupdf.open(SOURCE_PDF)
    page = doc[4]
    annot_count = 0
    for annot in page.annots():
        annot_count += 1
        print(f"  Annotation: type={annot.type[1]}, rect={annot.rect}")
    doc.close()
    print(f"Source page 5 has {annot_count} annotations.")

    # Create target_review.pdf (same structure, no annotations)
    print("Creating target_review.pdf...")
    create_review_pdf(TARGET_PDF, "TARGET")

    # Verify no annotations on target
    doc = pymupdf.open(TARGET_PDF)
    for i in range(doc.page_count):
        page = doc[i]
        for annot in page.annots():
            print(f"WARNING: target has annotation on page {i+1}: {annot.type[1]}")
    doc.close()
    print(f"Target PDF created with no annotations.")

    print(f"Initial files created:")
    print(f"  Source: {SOURCE_PDF}")
    print(f"  Target: {TARGET_PDF}")

    # GUI-ready: open the target file (the one the agent needs to modify)
    # and also open the source file
    launch_gui(f'evince "{SOURCE_PDF}"', delay_sec=2.0)
    launch_gui(f'evince "{TARGET_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched Evince for both source and target PDFs with DISPLAY=:0')


create_initial()
