"""
Initial Setup: Create a research paper PDF with empty Subject and Keywords metadata
Task ID: pdf_mbc_008
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_008'
RESEARCH_DIR = f'{WORKDIR}/Research'
OUTPUT = f'{RESEARCH_DIR}/paper_v2.pdf'


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
    os.makedirs(RESEARCH_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page1 = doc.new_page(width=595, height=842)
    page1.insert_text(
        pymupdf.Point(297 - 150, 200),
        "Quantum Computing Applications",
        fontsize=22,
        fontname="hebo",
        color=(0, 0, 0.4),
    )
    page1.insert_text(
        pymupdf.Point(297 - 100, 240),
        "in Modern Cryptography",
        fontsize=22,
        fontname="hebo",
        color=(0, 0, 0.4),
    )
    # Author line
    page1.insert_text(
        pymupdf.Point(297 - 60, 310),
        "Prof. Alan Rivera",
        fontsize=14,
        fontname="tiit",
        color=(0.2, 0.2, 0.2),
    )
    # Institution
    page1.insert_text(
        pymupdf.Point(297 - 120, 340),
        "Department of Computer Science",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(297 - 100, 360),
        "Stanford University, CA 94305",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    # Date
    page1.insert_text(
        pymupdf.Point(297 - 50, 410),
        "March 2026",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # --- Page 2: Abstract & Introduction ---
    page2 = doc.new_page(width=595, height=842)
    y = 72

    page2.insert_text(pymupdf.Point(72, y), "Abstract", fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 30

    abstract_text = (
        "This paper explores the transformative impact of quantum computing on modern "
        "cryptographic systems. As quantum processors continue to advance in qubit count "
        "and coherence time, the security foundations of widely deployed encryption schemes "
        "face unprecedented challenges. We examine the current state of quantum algorithms "
        "capable of breaking RSA and elliptic curve cryptography, and survey emerging "
        "post-quantum cryptographic alternatives including lattice-based, code-based, and "
        "hash-based approaches. Our analysis covers both theoretical vulnerabilities and "
        "practical timelines for quantum threats to existing infrastructure."
    )
    rect = pymupdf.Rect(72, y, 523, y + 120)
    page2.insert_textbox(rect, abstract_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 140

    page2.insert_text(pymupdf.Point(72, y), "1. Introduction", fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 25

    intro_text = (
        "The advent of quantum computing represents a paradigm shift in computational "
        "capability. Unlike classical computers that process information in binary bits, "
        "quantum computers leverage superposition and entanglement to perform certain "
        "calculations exponentially faster. Shor's algorithm, published in 1994, "
        "demonstrated that a sufficiently powerful quantum computer could factor large "
        "integers in polynomial time, directly threatening the RSA cryptosystem that "
        "underpins much of modern internet security.\n\n"
        "Recent developments at Google, IBM, and several startups have brought us closer "
        "to fault-tolerant quantum computing. Google's Willow processor achieved below-threshold "
        "quantum error correction in December 2024, marking a critical milestone. IBM's "
        "roadmap projects 100,000-qubit systems by 2033. These advances have elevated "
        "the urgency of transitioning to quantum-resistant cryptographic standards.\n\n"
        "The National Institute of Standards and Technology (NIST) finalized its first set "
        "of post-quantum cryptographic standards in August 2024, selecting CRYSTALS-Kyber "
        "for key encapsulation and CRYSTALS-Dilithium for digital signatures. Both are "
        "lattice-based schemes believed to resist quantum attacks."
    )
    rect = pymupdf.Rect(72, y, 523, y + 280)
    page2.insert_textbox(rect, intro_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 3: Background on Quantum Computing ---
    page3 = doc.new_page(width=595, height=842)
    y = 72

    page3.insert_text(pymupdf.Point(72, y), "2. Quantum Computing Fundamentals", fontsize=14,
                      fontname="hebo", color=(0, 0, 0))
    y += 25

    bg_text = (
        "Quantum computing harnesses quantum mechanical phenomena to process information "
        "in fundamentally new ways. The basic unit of quantum information, the qubit, can "
        "exist in a superposition of states |0> and |1> simultaneously. When multiple qubits "
        "are entangled, the combined system can represent 2^n states at once, enabling "
        "massive parallelism for specific problem types.\n\n"
        "Key quantum gates include the Hadamard gate (H), which creates superposition; "
        "the CNOT gate, which entangles two qubits; and phase gates that manipulate "
        "relative phases. These elementary operations compose into quantum circuits that "
        "implement algorithms such as Shor's factoring algorithm and Grover's search "
        "algorithm.\n\n"
        "Current quantum hardware falls into several categories: superconducting qubits "
        "(IBM, Google), trapped ions (IonQ, Quantinuum), photonic systems (Xanadu, PsiQuantum), "
        "and neutral atoms (QuEra, Atom Computing). Each approach offers different trade-offs "
        "in terms of gate fidelity, qubit connectivity, and scalability."
    )
    rect = pymupdf.Rect(72, y, 523, y + 250)
    page3.insert_textbox(rect, bg_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 270

    page3.insert_text(pymupdf.Point(72, y), "2.1 Shor's Algorithm", fontsize=12,
                      fontname="hebo", color=(0, 0, 0))
    y += 22

    shor_text = (
        "Shor's algorithm exploits the quantum Fourier transform to find the period of a "
        "function, which can then be used to factor large integers. Given an n-bit integer N, "
        "the algorithm runs in O((log N)^3) time, compared to the sub-exponential time required "
        "by the best classical algorithms (e.g., the General Number Field Sieve). For RSA-2048, "
        "classical factoring would require approximately 10^23 operations, while Shor's "
        "algorithm on a fault-tolerant quantum computer would need roughly 4,000 logical qubits "
        "and 10^10 gates."
    )
    rect = pymupdf.Rect(72, y, 523, y + 110)
    page3.insert_textbox(rect, shor_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 4: Post-Quantum Cryptography ---
    page4 = doc.new_page(width=595, height=842)
    y = 72

    page4.insert_text(pymupdf.Point(72, y), "3. Post-Quantum Cryptography", fontsize=14,
                      fontname="hebo", color=(0, 0, 0))
    y += 25

    pqc_text = (
        "Post-quantum cryptography (PQC) encompasses cryptographic algorithms that are "
        "believed to be secure against attacks by both classical and quantum computers. "
        "Several families of PQC algorithms have been developed:\n\n"
        "Lattice-based cryptography relies on the hardness of problems such as Learning With "
        "Errors (LWE) and its ring variant (RLWE). CRYSTALS-Kyber and CRYSTALS-Dilithium, "
        "both standardized by NIST, are lattice-based. These schemes offer relatively small "
        "key sizes and fast operations compared to other PQC families.\n\n"
        "Code-based cryptography, originating from McEliece's 1978 proposal, derives security "
        "from the difficulty of decoding random linear codes. While offering strong security "
        "guarantees, code-based schemes typically require larger public keys (hundreds of "
        "kilobytes to megabytes).\n\n"
        "Hash-based signatures (e.g., SPHINCS+) provide security based solely on the "
        "collision resistance of hash functions. These are considered the most conservative "
        "choice, as their security assumptions are well-understood, but they produce larger "
        "signatures than lattice-based alternatives."
    )
    rect = pymupdf.Rect(72, y, 523, y + 300)
    page4.insert_textbox(rect, pqc_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 5: Conclusion & References ---
    page5 = doc.new_page(width=595, height=842)
    y = 72

    page5.insert_text(pymupdf.Point(72, y), "4. Conclusion", fontsize=14,
                      fontname="hebo", color=(0, 0, 0))
    y += 25

    conclusion_text = (
        "The transition to post-quantum cryptography is not merely a theoretical exercise "
        "but an urgent practical necessity. With quantum computing advancing rapidly, "
        "organizations must begin planning their migration strategies now. The NIST "
        "standardization process has provided a solid foundation, but significant work "
        "remains in implementation, testing, and deployment at scale.\n\n"
        "Key recommendations include: (1) conducting cryptographic inventories to identify "
        "vulnerable systems, (2) implementing crypto-agility to facilitate future algorithm "
        "transitions, (3) adopting hybrid approaches that combine classical and post-quantum "
        "algorithms during the transition period, and (4) investing in quantum-safe key "
        "management infrastructure."
    )
    rect = pymupdf.Rect(72, y, 523, y + 180)
    page5.insert_textbox(rect, conclusion_text, fontsize=10, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)
    y += 200

    page5.insert_text(pymupdf.Point(72, y), "References", fontsize=14,
                      fontname="hebo", color=(0, 0, 0))
    y += 25

    references = [
        "[1] P. Shor, \"Algorithms for quantum computation: discrete logarithms and factoring,\" FOCS 1994.",
        "[2] NIST, \"Post-Quantum Cryptography Standardization,\" FIPS 203/204/205, August 2024.",
        "[3] R. Avanzi et al., \"CRYSTALS-Kyber: Algorithm Specifications,\" NIST PQC Round 3, 2022.",
        "[4] L. Ducas et al., \"CRYSTALS-Dilithium: Digital Signatures from Module Lattices,\" 2021.",
        "[5] D. J. Bernstein et al., \"SPHINCS+: Stateless Hash-Based Signatures,\" 2022.",
        "[6] Google Quantum AI, \"Below-threshold error correction with Willow,\" Nature, Dec 2024.",
        "[7] IBM, \"IBM Quantum Development Roadmap,\" 2025.",
        "[8] D. Moody et al., \"Status Report on the Third Round of the NIST PQC Process,\" NIST IR 8413.",
    ]
    for ref in references:
        rect = pymupdf.Rect(72, y, 523, y + 22)
        page5.insert_textbox(rect, ref, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 22

    # Set metadata: Author is set, Subject and Keywords are empty
    doc.set_metadata({
        "title": "Quantum Computing Applications in Modern Cryptography",
        "author": "Prof. Alan Rivera",
        "subject": "",
        "keywords": "",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    # Table of contents / bookmarks
    toc = [
        [1, "Abstract", 2],
        [1, "1. Introduction", 2],
        [1, "2. Quantum Computing Fundamentals", 3],
        [2, "2.1 Shor's Algorithm", 3],
        [1, "3. Post-Quantum Cryptography", 4],
        [1, "4. Conclusion", 5],
        [1, "References", 5],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
