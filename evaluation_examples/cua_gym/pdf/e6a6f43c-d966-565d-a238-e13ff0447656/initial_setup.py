"""
Initial Setup: Create 8 PDF files with varying metadata in /home/user/papers/batch/
Task ID: pdf_res_084
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf  # PyMuPDF

WORKDIR = '/home/user'
BATCH_DIR = f'{WORKDIR}/papers/batch'

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

# PDF definitions: (filename, title, author, subject, keywords, num_pages, content_lines_per_page)
PDF_SPECS = [
    {
        "filename": "neural_networks_survey.pdf",
        "title": "A Comprehensive Survey of Neural Network Architectures",
        "author": "Dr. Elena Vasquez",
        "subject": "Deep Learning",
        "keywords": "neural networks, deep learning, survey, architectures",
        "pages": [
            ("A Comprehensive Survey of Neural Network Architectures",
             [
                 "Abstract: This paper presents a thorough review of modern neural network",
                 "architectures including convolutional, recurrent, and transformer-based models.",
                 "We analyze performance benchmarks across multiple domains and identify key",
                 "design patterns that have driven recent breakthroughs in the field.",
                 "",
                 "1. Introduction",
                 "The rapid evolution of neural network architectures over the past decade has",
                 "fundamentally transformed machine learning research and applications.",
             ]),
            ("2. Background and Related Work",
             [
                 "Early neural network research dates back to the perceptron model proposed",
                 "by Rosenblatt in 1958. Since then, architectures have grown increasingly",
                 "complex, from multi-layer perceptrons to modern transformer networks.",
                 "",
                 "2.1 Convolutional Neural Networks",
                 "CNNs introduced spatial hierarchies through learnable filters, achieving",
                 "state-of-the-art results in image classification tasks.",
             ]),
        ],
    },
    {
        "filename": "quantum_computing_review.pdf",
        "title": "Quantum Computing: Current State and Future Directions",
        "author": "Prof. Hiroshi Tanaka",
        "subject": "Quantum Computing",
        "keywords": "quantum computing, qubits, quantum algorithms",
        "pages": [
            ("Quantum Computing: Current State and Future Directions",
             [
                 "Abstract: We examine the current landscape of quantum computing hardware",
                 "and software, evaluating progress toward practical quantum advantage.",
                 "Our analysis covers superconducting, trapped-ion, and photonic platforms.",
                 "",
                 "1. Introduction",
                 "Quantum computing promises exponential speedups for certain computational",
                 "problems, including integer factorization and unstructured search.",
             ]),
        ],
    },
    {
        "filename": "climate_modeling_advances.pdf",
        "title": "Recent Advances in Global Climate Modeling",
        "author": "Dr. Sarah Okonkwo",
        "subject": "Climate Science",
        "keywords": "climate modeling, global warming, earth systems",
        "pages": [
            ("Recent Advances in Global Climate Modeling",
             [
                 "Abstract: This paper reviews developments in high-resolution climate models",
                 "that incorporate ocean-atmosphere coupling, ice sheet dynamics, and carbon",
                 "cycle feedbacks to improve long-term projection accuracy.",
                 "",
                 "1. Introduction",
                 "Climate models have become indispensable tools for understanding future",
                 "environmental changes and informing policy decisions.",
             ]),
            ("2. Methodology",
             [
                 "We compare outputs from CMIP6 models against observational datasets",
                 "spanning 1950-2025, focusing on temperature, precipitation, and sea level.",
                 "",
                 "2.1 Model Configurations",
                 "Each model was run at 25km horizontal resolution with 85 vertical levels.",
             ]),
            ("3. Results and Discussion",
             [
                 "Our analysis reveals significant improvements in regional precipitation",
                 "patterns when ocean eddy-resolving components are included.",
                 "",
                 "3.1 Temperature Projections",
                 "Global mean surface temperature projections show a likely range of 2.1-3.5C",
                 "warming above pre-industrial levels by 2100 under SSP2-4.5.",
             ]),
        ],
    },
    {
        "filename": "robotics_manipulation.pdf",
        "title": "Dexterous Manipulation in Robotics: A Learning-Based Approach",
        "author": "Dr. Marcus Weber",
        "subject": "Robotics",
        "keywords": "robotics, manipulation, reinforcement learning, dexterous",
        "pages": [
            ("Dexterous Manipulation in Robotics",
             [
                 "Abstract: We propose a reinforcement learning framework for dexterous",
                 "robotic manipulation that achieves human-level performance on 12 benchmark",
                 "tasks including in-hand rotation, precision grasping, and tool use.",
                 "",
                 "1. Introduction",
                 "Robotic manipulation of diverse objects remains one of the grand challenges",
                 "in robotics, requiring fine motor control and adaptive planning.",
             ]),
            ("2. Method",
             [
                 "Our approach combines a hierarchical policy architecture with curriculum",
                 "learning to progressively increase task difficulty during training.",
                 "",
                 "2.1 Policy Architecture",
                 "The policy network consists of a spatial attention module followed by",
                 "a recurrent controller that outputs joint torque commands.",
             ]),
        ],
    },
    {
        "filename": "nlp_transformers_efficiency.pdf",
        "title": "Efficient Transformer Models for Natural Language Processing",
        "author": "Dr. Amara Osei",
        "subject": "Natural Language Processing",
        "keywords": "transformers, NLP, efficiency, attention mechanisms",
        "pages": [
            ("Efficient Transformer Models for NLP",
             [
                 "Abstract: We analyze recent approaches to reducing the computational cost",
                 "of transformer models while preserving language understanding capabilities.",
                 "Techniques surveyed include sparse attention, knowledge distillation,",
                 "quantization, and dynamic token pruning.",
                 "",
                 "1. Introduction",
                 "Large language models based on the transformer architecture have achieved",
                 "remarkable results but require substantial computational resources.",
             ]),
        ],
    },
    {
        "filename": "medical_imaging_ai.pdf",
        "title": "AI-Assisted Medical Imaging: Diagnostic Accuracy and Clinical Integration",
        "author": "Dr. Priya Sharma",
        "subject": "Medical AI",
        "keywords": "medical imaging, AI diagnostics, radiology, clinical trials",
        "pages": [
            ("AI-Assisted Medical Imaging",
             [
                 "Abstract: This study evaluates the diagnostic accuracy of AI systems",
                 "across five imaging modalities: X-ray, CT, MRI, ultrasound, and PET.",
                 "We report results from 23 clinical validation studies involving 150,000+",
                 "patient images from 14 medical centers worldwide.",
                 "",
                 "1. Introduction",
                 "AI-powered diagnostic tools have shown promise in detecting abnormalities",
                 "in medical images with accuracy comparable to expert radiologists.",
             ]),
            ("2. Clinical Studies Overview",
             [
                 "Our meta-analysis covers studies published between 2020 and 2025,",
                 "selecting those with prospective validation cohorts of at least 500 patients.",
                 "",
                 "Table 1: Study Characteristics",
                 "  Modality    | Studies | Total Patients | Mean AUC",
                 "  X-ray       |    7    |    45,200      |  0.943",
                 "  CT          |    6    |    38,100      |  0.967",
                 "  MRI         |    5    |    32,500      |  0.951",
             ]),
            ("3. Discussion and Conclusions",
             [
                 "AI diagnostic systems consistently achieved high sensitivity and specificity",
                 "across all imaging modalities, with particularly strong performance in",
                 "chest X-ray interpretation and brain MRI analysis.",
                 "",
                 "Key limitations include dataset bias, regulatory challenges, and the need",
                 "for ongoing monitoring of model performance in clinical deployment.",
             ]),
        ],
    },
    {
        "filename": "blockchain_scalability.pdf",
        "title": "Scalability Solutions for Blockchain Networks",
        "author": "Dr. Liam Chen",
        "subject": "Blockchain Technology",
        "keywords": "blockchain, scalability, layer-2, consensus",
        "pages": [
            ("Scalability Solutions for Blockchain Networks",
             [
                 "Abstract: We evaluate major scalability approaches for public blockchain",
                 "networks including sharding, rollups, state channels, and sidechains.",
                 "Performance benchmarks show 100-1000x throughput improvements are achievable",
                 "without compromising decentralization or security guarantees.",
                 "",
                 "1. Introduction",
                 "Public blockchain networks face a fundamental trilemma between scalability,",
                 "security, and decentralization that limits mainstream adoption.",
             ]),
            ("2. Layer-2 Solutions",
             [
                 "Layer-2 protocols process transactions off the main chain while inheriting",
                 "its security guarantees through cryptographic proofs or dispute resolution.",
                 "",
                 "2.1 Optimistic Rollups",
                 "Transactions are assumed valid and only challenged via fraud proofs during",
                 "a dispute window, achieving 10-100x throughput gains.",
             ]),
        ],
    },
    {
        "filename": "autonomous_vehicles_safety.pdf",
        "title": "Safety Validation Framework for Autonomous Vehicles",
        "author": "Dr. Fatima Al-Rashid",
        "subject": "Autonomous Driving",
        "keywords": "autonomous vehicles, safety validation, self-driving",
        "pages": [
            ("Safety Validation Framework for Autonomous Vehicles",
             [
                 "Abstract: We present a comprehensive safety validation framework for",
                 "Level 4 autonomous vehicles combining simulation testing, closed-course",
                 "evaluation, and structured on-road assessment across diverse conditions.",
                 "",
                 "1. Introduction",
                 "Demonstrating the safety of autonomous vehicles requires rigorous testing",
                 "methodologies that cover the vast space of possible driving scenarios.",
             ]),
        ],
    },
]


def create_pdf(spec):
    """Create a single PDF file from a specification dictionary."""
    doc = pymupdf.open()

    for page_title, lines in spec["pages"]:
        page = doc.new_page(width=595, height=842)  # A4

        # Title
        page.insert_text(
            pymupdf.Point(72, 72),
            page_title,
            fontsize=16,
            fontname="hebo",
            color=(0, 0, 0),
        )

        # Separator line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
        shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape.commit()

        # Content lines
        y = 110
        for line in lines:
            if line == "":
                y += 10
                continue
            page.insert_text(
                pymupdf.Point(72, y),
                line,
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
            )
            y += 16

    # Set metadata
    doc.set_metadata({
        "title": spec["title"],
        "author": spec["author"],
        "subject": spec["subject"],
        "keywords": spec["keywords"],
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    output_path = os.path.join(BATCH_DIR, spec["filename"])
    doc.save(output_path)
    doc.close()
    print(f"  Created: {output_path} ({len(spec['pages'])} pages)")


def create_initial():
    os.makedirs(BATCH_DIR, exist_ok=True)

    print("Creating 8 PDF files in /home/user/papers/batch/...")
    for spec in PDF_SPECS:
        create_pdf(spec)

    print(f"\nTotal files created: {len(PDF_SPECS)}")

    # Launch file manager showing the batch directory
    launch_gui(f'nautilus "{BATCH_DIR}"', delay_sec=2.0)
    print(f'GUI_READY: launched nautilus showing {BATCH_DIR}')


create_initial()
