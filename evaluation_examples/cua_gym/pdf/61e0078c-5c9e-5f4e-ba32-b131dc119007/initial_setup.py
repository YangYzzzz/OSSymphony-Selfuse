"""
Initial Setup: Create a 30-page workshop slides PDF with conference header banners
Task ID: pdf_res_076
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_076'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/workshop_slides.pdf'

# Page dimensions (Letter size)
PAGE_W = 612
PAGE_H = 792
BANNER_H = 100  # conference header banner height

# Slide titles for 30 pages of a realistic workshop
SLIDE_TITLES = [
    "Workshop on Scalable Machine Learning Systems",
    "Agenda & Overview",
    "Keynote: The Future of Distributed Training",
    "Background & Motivation",
    "Related Work in Large-Scale ML",
    "System Architecture Overview",
    "Data Pipeline Design",
    "Distributed Training Framework",
    "Model Parallelism Strategies",
    "Gradient Compression Techniques",
    "Communication-Efficient Methods",
    "Fault Tolerance & Checkpointing",
    "Experiment Setup & Benchmarks",
    "Results: Throughput Analysis",
    "Results: Convergence Speed",
    "Results: Cost Efficiency",
    "Ablation Studies",
    "Case Study: ImageNet at Scale",
    "Case Study: Language Model Pre-training",
    "Case Study: Recommendation Systems",
    "Scaling Laws & Observations",
    "Resource Allocation Strategies",
    "Energy Efficiency Considerations",
    "Hardware Utilization Metrics",
    "Comparison with Existing Platforms",
    "Limitations & Future Directions",
    "Open Source Contributions",
    "Community Engagement",
    "Q&A Session",
    "Thank You & Contact Information",
]

SPEAKER_NAMES = [
    "Dr. Elena Rodriguez",
    "Prof. Kenji Watanabe",
    "Dr. Aisha Patel",
    "Marcus Chen",
    "Dr. Sofia Lindqvist",
]

BODY_TEXTS = [
    "Scaling machine learning models to billions of parameters requires rethinking traditional training paradigms. "
    "Our approach combines data parallelism with efficient gradient synchronization across heterogeneous clusters.",

    "This session covers the complete agenda including keynotes, technical presentations, "
    "and hands-on demonstrations of our distributed training toolkit.",

    "The shift from single-GPU to multi-node training introduces challenges in communication overhead, "
    "memory management, and fault recovery that demand novel solutions.",

    "Modern deep learning workloads require efficient utilization of GPU clusters spanning "
    "multiple data centers with varying network topologies and hardware configurations.",

    "We survey existing frameworks including PyTorch Distributed, Horovod, DeepSpeed, and Megatron-LM, "
    "analyzing their trade-offs in scalability, ease of use, and performance.",

    "Our architecture separates the control plane from the data plane, enabling independent scaling "
    "of scheduling, monitoring, and data movement components.",

    "The data pipeline handles 50TB+ datasets with on-the-fly augmentation, sharding, "
    "and prefetching to maintain GPU utilization above 92% during training.",

    "We implement a hybrid parallelism strategy combining ZeRO Stage 3 with pipeline parallelism "
    "to efficiently train 175B parameter models on 1024 GPUs.",

    "Model parallelism splits transformer layers across devices using optimized NCCL collectives "
    "with overlap of computation and communication.",

    "Our gradient compression achieves 100x reduction in communication volume "
    "with less than 0.3% accuracy degradation across standard benchmarks.",

    "AllReduce operations are optimized using a hierarchical ring topology "
    "that exploits intra-node NVLink and inter-node InfiniBand interconnects.",

    "Automated checkpointing saves model state every 500 iterations with asynchronous writes, "
    "enabling recovery from node failures within 45 seconds.",

    "Benchmark configuration: 256 NVIDIA A100 GPUs, 200Gbps InfiniBand, "
    "training GPT-3 class models with 175 billion parameters.",

    "Peak throughput of 2.4 PetaFLOPS sustained across 256 GPUs, "
    "representing 78% of theoretical hardware maximum.",

    "Our system achieves state-of-the-art convergence with 40% fewer training steps "
    "compared to baseline distributed training configurations.",

    "Training cost reduced from $4.6M to $2.1M for a 175B parameter model, "
    "primarily through improved GPU utilization and reduced communication overhead.",

    "Ablation studies reveal that gradient compression contributes 35% of total speedup, "
    "while pipeline scheduling optimizations account for 28%.",

    "ImageNet training on 1000 classes completed in 11.2 minutes using 2048 GPUs, "
    "achieving 76.8% top-1 accuracy matching single-GPU baselines.",

    "Pre-training a 70B language model on 2T tokens completed in 14 days "
    "using our optimized pipeline across 512 A100 GPUs.",

    "Recommendation model training on 10B interaction records achieves "
    "real-time feature updates with sub-millisecond inference latency.",

    "We observe near-linear scaling up to 4096 GPUs for transformer architectures, "
    "with efficiency dropping to 0.85x beyond 8192 GPUs.",

    "Dynamic resource allocation reduces idle GPU time by 34% through predictive "
    "workload scheduling and elastic cluster resizing.",

    "Total energy consumption reduced by 42% through workload-aware power management "
    "and carbon-optimized scheduling across data centers.",

    "Average GPU utilization improved from 61% to 89% through memory-efficient "
    "attention mechanisms and dynamic batch sizing.",

    "Compared to Megatron-LM and DeepSpeed, our system achieves 1.3x higher throughput "
    "with 25% lower memory footprint for equivalent model sizes.",

    "Current limitations include limited support for heterogeneous GPU clusters "
    "and challenges with very long sequence lengths exceeding 128K tokens.",

    "All core components released under Apache 2.0 license at github.com/scalable-ml-systems, "
    "with 3,200+ stars and 180+ contributors.",

    "Monthly community meetups, annual workshop, and active Discord server "
    "with 5,000+ members from industry and academia.",

    "We welcome questions on architecture, benchmarks, deployment, and future roadmap. "
    "Please use the Q&A microphone or submit questions via the conference app.",

    "Thank you for attending. Contact: workshop@scalable-ml.org | "
    "Twitter: @ScalableML | Papers and code at scalable-ml.org/resources",
]

CONFERENCE_NAME = "ICML 2025 Workshop on Scalable ML Systems"


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
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    for i in range(30):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        shape = page.new_shape()

        # --- Conference header banner (top 100 points) ---
        # Dark blue banner background
        banner_rect = pymupdf.Rect(0, 0, PAGE_W, BANNER_H)
        shape.draw_rect(banner_rect)
        shape.finish(color=(0.05, 0.1, 0.3), fill=(0.05, 0.1, 0.3), width=0)

        # Thin gold accent line at bottom of banner
        shape.draw_line(pymupdf.Point(0, BANNER_H - 2), pymupdf.Point(PAGE_W, BANNER_H - 2))
        shape.finish(color=(0.85, 0.65, 0.13), width=2)

        shape.commit()

        # Conference name in banner
        page.insert_text(
            pymupdf.Point(36, 40),
            CONFERENCE_NAME,
            fontsize=14,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Page number in banner (right side)
        page.insert_text(
            pymupdf.Point(PAGE_W - 80, 40),
            f"Slide {i + 1}/30",
            fontsize=10,
            fontname="helv",
            color=(0.8, 0.8, 0.8),
        )

        # Date in banner
        page.insert_text(
            pymupdf.Point(36, 70),
            "July 21-27, 2025 | Vancouver, Canada",
            fontsize=9,
            fontname="helv",
            color=(0.85, 0.85, 0.85),
        )

        # --- Slide content below banner ---
        # Slide title
        page.insert_text(
            pymupdf.Point(50, 140),
            SLIDE_TITLES[i],
            fontsize=20,
            fontname="hebo",
            color=(0.1, 0.1, 0.3),
        )

        # Horizontal rule under title
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(50, 155), pymupdf.Point(PAGE_W - 50, 155))
        shape2.finish(color=(0.2, 0.4, 0.7), width=1.5)
        shape2.commit()

        # Speaker name
        speaker = SPEAKER_NAMES[i % len(SPEAKER_NAMES)]
        page.insert_text(
            pymupdf.Point(50, 180),
            f"Presented by {speaker}",
            fontsize=11,
            fontname="heit",
            color=(0.4, 0.4, 0.4),
        )

        # Body text in textbox
        body_rect = pymupdf.Rect(50, 210, PAGE_W - 50, PAGE_H - 80)
        page.insert_textbox(
            body_rect,
            BODY_TEXTS[i],
            fontsize=12,
            fontname="helv",
            color=(0.15, 0.15, 0.15),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

        # Footer
        page.insert_text(
            pymupdf.Point(50, PAGE_H - 40),
            "Confidential - Workshop Materials",
            fontsize=8,
            fontname="heit",
            color=(0.6, 0.6, 0.6),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
