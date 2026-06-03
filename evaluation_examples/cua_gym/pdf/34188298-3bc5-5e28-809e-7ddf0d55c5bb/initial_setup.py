"""
Initial Setup: Create an 18-page research paper PDF with incomplete metadata
Task ID: pdf_gf2_014
Domain: pdf

The PDF has 18 pages of quantum computing research content.
Metadata is incomplete: Title and Author are empty, Subject and Keywords are absent.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_014'
DOC_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOC_DIR}/research_paper.pdf'


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
    os.makedirs(DOC_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Research paper content ---
    # Page dimensions: Letter size
    W, H = 612, 792
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 540
    MARGIN_TOP = 72
    TEXT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT

    # ---- Page 1: Title Page ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(W/2 - 180, 200), "Quantum Computing Applications",
                     fontsize=22, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(W/2 - 120, 235), "in Cryptography",
                     fontsize=22, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(W/2 - 80, 310), "Dr. James Wei",
                     fontsize=14, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(W/2 - 140, 340), "Department of Computer Science",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(W/2 - 130, 360), "Stanford University, CA 94305",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(W/2 - 70, 400), "March 2026",
                     fontsize=12, fontname="tiit", color=(0.3, 0.3, 0.3))

    # Abstract box
    rect = pymupdf.Rect(MARGIN_LEFT, 460, MARGIN_RIGHT, 700)
    abstract_text = (
        "Abstract\n\n"
        "This paper surveys the current landscape of quantum computing applications in modern "
        "cryptography, with particular emphasis on lattice-based and post-quantum cryptographic "
        "schemes. We examine the implications of Shor's algorithm on RSA and elliptic curve "
        "cryptography, analyze the NIST Post-Quantum Cryptography standardization process, and "
        "evaluate the practical readiness of quantum-resistant alternatives. Our analysis covers "
        "key encapsulation mechanisms (KEMs), digital signature schemes, and hash-based constructions. "
        "We present performance benchmarks comparing classical and post-quantum implementations across "
        "multiple hardware platforms, and discuss the challenges of transitioning existing infrastructure "
        "to quantum-safe protocols. Our findings indicate that while lattice-based schemes offer the "
        "most promising balance of security and performance, significant engineering challenges remain "
        "before widespread deployment is feasible."
    )
    page.insert_textbox(rect, abstract_text, fontsize=10, fontname="helv", color=(0, 0, 0))

    # ---- Page 2: Table of Contents ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, 90), "Table of Contents", fontsize=18, fontname="hebo")
    toc_entries = [
        ("1. Introduction", "1"),
        ("2. Background on Quantum Computing", "3"),
        ("   2.1 Quantum Gates and Circuits", "3"),
        ("   2.2 Quantum Algorithms Overview", "4"),
        ("3. Threats to Classical Cryptography", "5"),
        ("   3.1 Shor's Algorithm and RSA", "5"),
        ("   3.2 Grover's Algorithm and Symmetric Keys", "6"),
        ("4. Post-Quantum Cryptographic Schemes", "7"),
        ("   4.1 Lattice-Based Cryptography", "7"),
        ("   4.2 Code-Based Cryptography", "8"),
        ("   4.3 Hash-Based Signatures", "9"),
        ("   4.4 Multivariate Cryptography", "9"),
        ("5. NIST Standardization Process", "10"),
        ("   5.1 Round 3 Finalists", "10"),
        ("   5.2 Selected Standards", "11"),
        ("6. Performance Benchmarks", "12"),
        ("   6.1 Key Generation Timings", "12"),
        ("   6.2 Encryption/Decryption Overhead", "13"),
        ("   6.3 Signature Size Comparison", "13"),
        ("7. Implementation Challenges", "14"),
        ("   7.1 Side-Channel Attacks", "14"),
        ("   7.2 Key Size Management", "15"),
        ("8. Migration Strategies", "15"),
        ("   8.1 Hybrid Approaches", "15"),
        ("   8.2 Protocol Upgrades", "16"),
        ("9. Future Directions", "16"),
        ("10. Conclusion", "17"),
        ("References", "18"),
    ]
    y = 130
    for entry, pg_num in toc_entries:
        page.insert_text(pymupdf.Point(MARGIN_LEFT + 10, y), entry, fontsize=10, fontname="helv")
        page.insert_text(pymupdf.Point(MARGIN_RIGHT - 20, y), pg_num, fontsize=10, fontname="helv")
        y += 18

    # ---- Pages 3-17: Research content ----
    sections = [
        # Page 3: Introduction
        ("1. Introduction", [
            "The advent of quantum computing represents a paradigm shift in computational "
            "capabilities that threatens the foundational security assumptions of modern cryptographic "
            "systems. As quantum hardware continues to advance, with companies like IBM, Google, and "
            "IonQ reporting steady increases in qubit counts and coherence times, the cryptographic "
            "community faces an urgent need to develop and deploy quantum-resistant alternatives.",
            "Classical public-key cryptographic systems, including RSA, Diffie-Hellman key exchange, "
            "and elliptic curve cryptography (ECC), derive their security from the computational "
            "hardness of integer factorization and discrete logarithm problems. Shor's algorithm, "
            "published in 1994, demonstrated that a sufficiently large quantum computer could solve "
            "these problems in polynomial time, effectively rendering these cryptosystems insecure.",
            "This paper provides a comprehensive survey of quantum computing's impact on cryptographic "
            "systems and evaluates the current state of post-quantum cryptographic alternatives. We "
            "examine both the theoretical foundations and practical implementation considerations that "
            "will shape the transition to quantum-safe security infrastructure.",
        ]),
        # Page 4: Background - Quantum Gates
        ("2. Background on Quantum Computing", [
            "2.1 Quantum Gates and Circuits",
            "Quantum computing operates on quantum bits (qubits) that can exist in superposition "
            "states, enabling parallel processing of exponentially many classical states. Unlike "
            "classical bits, which are either 0 or 1, a qubit |ψ⟩ = α|0⟩ + β|1⟩ exists as a "
            "weighted combination of both states, where |α|² + |β|² = 1.",
            "Quantum gates manipulate qubits through unitary transformations. Key single-qubit gates "
            "include the Hadamard gate (H), which creates superposition from basis states, the Pauli "
            "gates (X, Y, Z) for rotations, and phase gates (S, T) for controlled phase shifts. "
            "Multi-qubit gates, particularly the CNOT (controlled-NOT) gate, enable entanglement "
            "between qubits, a fundamentally quantum phenomenon with no classical analog.",
            "Quantum circuits are constructed by composing these gates in sequence and parallel. The "
            "circuit model is universal: any unitary transformation on n qubits can be approximated "
            "to arbitrary precision using a finite set of single-qubit and CNOT gates. This "
            "universality underlies the ability of quantum computers to implement algorithms that "
            "achieve exponential speedups over classical counterparts for specific problems.",
        ]),
        # Page 5: Quantum Algorithms
        ("", [
            "2.2 Quantum Algorithms Overview",
            "The quantum computing algorithm landscape extends well beyond Shor's and Grover's "
            "algorithms. Variational Quantum Eigensolver (VQE) and Quantum Approximate Optimization "
            "Algorithm (QAOA) represent hybrid classical-quantum approaches that leverage near-term "
            "quantum devices for optimization problems. The Harrow-Hassidim-Lloyd (HHL) algorithm "
            "provides exponential speedup for solving linear systems of equations.",
            "For cryptographic applications, the most relevant algorithms are: (1) Shor's algorithm "
            "for integer factorization and discrete logarithms, (2) Grover's algorithm for unstructured "
            "search providing a quadratic speedup, (3) Simon's algorithm for finding hidden periods, "
            "and (4) the Bernstein-Vazirani algorithm for identifying hidden linear functions.",
            "Current quantum hardware limitations—including decoherence, gate errors, and limited "
            "connectivity—mean that large-scale quantum attacks on cryptographic systems remain "
            "years away. However, the 'harvest now, decrypt later' threat model, where adversaries "
            "collect encrypted data today for future quantum decryption, makes the transition to "
            "post-quantum cryptography an immediate priority.",
        ]),
        # Page 6: Shor's Algorithm and RSA
        ("3. Threats to Classical Cryptography", [
            "3.1 Shor's Algorithm and RSA",
            "Shor's algorithm factors an n-bit integer in O(n³) time using O(n) qubits, compared to "
            "the best known classical algorithm (General Number Field Sieve) which runs in "
            "sub-exponential time. For RSA-2048, classical factoring would require approximately "
            "10^20 operations, while Shor's algorithm on a fault-tolerant quantum computer would "
            "need roughly 4,000 logical qubits and 10^9 quantum gates.",
            "Recent estimates by Gidney and Ekerå (2021) have refined the resource requirements for "
            "breaking RSA-2048 to approximately 20 million noisy qubits, assuming surface code error "
            "correction with a physical error rate of 10^-3. While current quantum computers have "
            "fewer than 1,500 qubits, the trajectory of hardware development suggests this threshold "
            "could be reached within 10-15 years.",
            "The vulnerability extends beyond RSA to all schemes based on the hardness of factoring "
            "or computing discrete logarithms, including Diffie-Hellman key exchange, DSA, and ECDSA. "
            "This broad impact necessitates a wholesale transition of public-key infrastructure to "
            "quantum-resistant alternatives.",
        ]),
        # Page 7: Grover's Algorithm
        ("", [
            "3.2 Grover's Algorithm and Symmetric Keys",
            "Grover's algorithm provides a quadratic speedup for unstructured search, reducing the "
            "effective security of an n-bit symmetric key to n/2 bits against quantum adversaries. "
            "For AES-128, this means quantum security equivalent to only 64 bits—below acceptable "
            "thresholds for long-term security.",
            "The practical impact on symmetric cryptography is more nuanced than on public-key "
            "systems. Doubling key lengths (e.g., using AES-256 instead of AES-128) restores "
            "adequate security margins. Hash functions similarly maintain security with doubled "
            "output lengths, though Brassard et al.'s quantum collision-finding algorithm must also "
            "be considered for collision-resistant applications.",
            "A critical consideration is that Grover's algorithm requires sequential oracle queries "
            "and cannot be effectively parallelized. This means the practical speedup against "
            "symmetric cryptography may be significantly less than the theoretical quadratic bound, "
            "especially given the overhead of quantum error correction. Current analysis suggests "
            "that AES-256 and SHA-384/SHA-512 provide sufficient quantum resistance for most "
            "applications through at least the 2050 timeframe.",
        ]),
        # Page 8: Lattice-Based Crypto
        ("4. Post-Quantum Cryptographic Schemes", [
            "4.1 Lattice-Based Cryptography",
            "Lattice-based cryptographic schemes derive their security from the hardness of lattice "
            "problems, particularly the Learning With Errors (LWE) problem and its ring variant "
            "(Ring-LWE). These problems are believed to be hard for both classical and quantum "
            "computers, with the best known quantum algorithms providing only polynomial (not "
            "exponential) speedup.",
            "The CRYSTALS-Kyber key encapsulation mechanism, now standardized as ML-KEM (FIPS 203), "
            "achieves a favorable balance of security, key sizes, and computational efficiency. "
            "Kyber-768 provides approximately 128 bits of classical security with public keys of "
            "1,184 bytes and ciphertexts of 1,088 bytes—significantly larger than ECC equivalents "
            "but manageable for most applications.",
            "CRYSTALS-Dilithium, standardized as ML-DSA (FIPS 204), provides digital signatures "
            "based on the hardness of Module-LWE and Module-SIS problems. Dilithium signatures are "
            "larger than classical alternatives (2,420 bytes for Dilithium2 vs. 64 bytes for "
            "Ed25519) but offer strong post-quantum security guarantees with reasonable verification "
            "performance.",
        ]),
        # Page 9: Code-Based Crypto
        ("", [
            "4.2 Code-Based Cryptography",
            "Code-based cryptography, originating with McEliece's 1978 cryptosystem, bases its "
            "security on the difficulty of decoding random linear codes. The Classic McEliece "
            "scheme, a NIST Round 4 candidate, offers extremely conservative security guarantees "
            "with decades of cryptanalytic scrutiny, but suffers from very large public keys "
            "(261,120 bytes for the recommended parameter set).",
            "The BIKE (Bit Flipping Key Encapsulation) and HQC (Hamming Quasi-Cyclic) schemes use "
            "structured codes to reduce key sizes substantially while maintaining code-based "
            "security assumptions. HQC, selected as a NIST Round 4 finalist, offers public keys "
            "of approximately 2,249 bytes with 128-bit quantum security.",
            "The primary advantage of code-based schemes is their well-understood security "
            "foundations. The Syndrome Decoding Problem has resisted significant algorithmic "
            "advances since its introduction, providing high confidence in long-term security. "
            "However, the key size overhead remains a significant deployment challenge, particularly "
            "for resource-constrained environments such as IoT devices and embedded systems.",
        ]),
        # Page 10: Hash-Based and Multivariate
        ("", [
            "4.3 Hash-Based Signatures",
            "Hash-based signature schemes offer a unique advantage in post-quantum cryptography: "
            "their security relies solely on the properties of the underlying hash function, making "
            "them among the most conservative and well-understood quantum-resistant constructions. "
            "SPHINCS+, standardized as SLH-DSA (FIPS 205), provides stateless hash-based signatures "
            "suitable for general-purpose deployment.",
            "SPHINCS+ achieves small public keys (32-64 bytes) but produces relatively large "
            "signatures (7,856-49,856 bytes depending on the parameter set and optimization target). "
            "The signing process is computationally intensive, requiring many hash evaluations, "
            "though verification is significantly faster.",
            "4.4 Multivariate Cryptography",
            "Multivariate polynomial cryptography bases security on the difficulty of solving systems "
            "of multivariate quadratic equations over finite fields (the MQ problem). While some "
            "multivariate schemes like Rainbow were broken during the NIST process, the GeMSS and "
            "MAYO schemes continue to be studied as potential alternatives with compact signatures.",
        ]),
        # Page 11: NIST Standardization
        ("5. NIST Standardization Process", [
            "5.1 Round 3 Finalists",
            "The NIST Post-Quantum Cryptography standardization process, initiated in 2016, received "
            "82 submissions in Round 1. Through three rounds of evaluation, the field was narrowed "
            "based on security analysis, performance characteristics, and implementation flexibility. "
            "Round 3 finalists for key encapsulation included CRYSTALS-Kyber, NTRU, Classic McEliece, "
            "SABER, and BIKE, while signature finalists included CRYSTALS-Dilithium, FALCON, "
            "SPHINCS+, and Rainbow.",
            "The selection criteria emphasized not only theoretical security margins but also "
            "practical deployment considerations: key and signature sizes, computational overhead, "
            "side-channel resistance, and implementation complexity. The diverse set of finalists "
            "reflected NIST's strategy of maintaining algorithmic diversity to hedge against "
            "future cryptanalytic breakthroughs.",
            "The elimination of Rainbow in Round 3 following Ward Beullens' key recovery attack "
            "underscored the importance of sustained cryptanalytic effort and the risks of "
            "relying on relatively new hardness assumptions.",
        ]),
        # Page 12: Selected Standards
        ("", [
            "5.2 Selected Standards",
            "In July 2022, NIST announced the selection of four algorithms for standardization: "
            "CRYSTALS-Kyber (KEM), CRYSTALS-Dilithium (digital signature), FALCON (digital "
            "signature), and SPHINCS+ (digital signature). The final standards were published in "
            "2024 as FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), and FIPS 205 (SLH-DSA).",
            "ML-KEM (Kyber) was selected as the primary KEM standard due to its balanced profile: "
            "moderate key and ciphertext sizes, fast key generation and encapsulation, and strong "
            "security proofs based on the Module-LWE problem. Three parameter sets (ML-KEM-512, "
            "ML-KEM-768, ML-KEM-1024) provide security levels I, III, and V respectively.",
            "ML-DSA (Dilithium) was selected as the primary signature standard for general use, "
            "while SLH-DSA (SPHINCS+) serves as a conservative backup based on minimal security "
            "assumptions. FALCON, based on the NTRU lattice, provides compact signatures but "
            "requires careful implementation of Gaussian sampling to avoid side-channel leakage.",
        ]),
        # Page 13: Key Generation Timings
        ("6. Performance Benchmarks", [
            "6.1 Key Generation Timings",
            "We conducted performance benchmarks on three platforms: Intel Core i9-13900K (desktop), "
            "Apple M3 Pro (laptop), and ARM Cortex-A78 (mobile/embedded). All measurements represent "
            "median values over 10,000 iterations with warm caches.",
            "Key Generation Performance (microseconds):\n"
            "  Algorithm         | Desktop | Laptop | Mobile\n"
            "  ML-KEM-768        |    38   |   45   |   120\n"
            "  ML-DSA-65         |   125   |  148   |   380\n"
            "  SLH-DSA-SHA2-128s |   920   | 1,100  | 3,200\n"
            "  RSA-2048          | 45,000  | 52,000 | 180,000\n"
            "  ECDSA-P256        |    42   |   50   |   135",
            "Lattice-based key generation is dramatically faster than RSA and competitive with "
            "elliptic curve operations. Hash-based schemes incur significant overhead due to "
            "the construction of Merkle trees during key generation, though this is a one-time "
            "cost. The results demonstrate that post-quantum schemes need not impose unacceptable "
            "performance penalties for key generation operations.",
        ]),
        # Page 14: Encryption/Signing overhead
        ("", [
            "6.2 Encryption/Decryption Overhead",
            "Encapsulation/decapsulation timings for KEM schemes and encryption/decryption for "
            "classical comparisons reveal that ML-KEM operations are fast across all platforms, "
            "with encapsulation under 50 microseconds even on mobile hardware.",
            "Encapsulation Performance (microseconds):\n"
            "  Algorithm    | Encap | Decap\n"
            "  ML-KEM-768   |   42  |   48\n"
            "  ML-KEM-1024  |   58  |   65\n"
            "  RSA-2048 Enc |   12  |  380\n"
            "  ECDH-P256    |   85  |   85",
            "6.3 Signature Size Comparison",
            "Signature sizes vary dramatically across post-quantum schemes, with implications for "
            "bandwidth-constrained protocols like TLS handshakes and certificate chains.",
            "Signature Sizes (bytes):\n"
            "  Algorithm        | Sig Size | PK Size | SK Size\n"
            "  ML-DSA-65        |  2,420   |  1,952  |  4,032\n"
            "  SLH-DSA-128s     |  7,856   |    32   |    64\n"
            "  FALCON-512       |    666   |    897  |  1,281\n"
            "  ECDSA-P256       |     64   |     33  |    32\n"
            "  RSA-2048         |    256   |    256  |  1,024",
        ]),
        # Page 15: Side-Channel Attacks
        ("7. Implementation Challenges", [
            "7.1 Side-Channel Attacks",
            "Post-quantum implementations face significant side-channel attack surfaces that differ "
            "from classical cryptographic implementations. Lattice-based schemes are particularly "
            "vulnerable to timing attacks during polynomial multiplication and Number Theoretic "
            "Transform (NTT) operations, as well as power analysis attacks that can recover "
            "secret key coefficients.",
            "FALCON's requirement for high-precision floating-point Gaussian sampling introduces "
            "subtle timing variations that have proven difficult to eliminate. Multiple research "
            "groups have demonstrated practical side-channel attacks against naive FALCON "
            "implementations, recovering the secret key through electromagnetic emanation analysis "
            "and cache-timing measurements.",
            "Constant-time implementation strategies, including bitslicing, masked operations, and "
            "shuffling techniques, are essential for secure deployment. The NIST standards include "
            "implementation guidance addressing these concerns, and reference implementations in "
            "C and Rust provide constant-time operation for critical code paths. However, the "
            "complexity of achieving side-channel security remains a significant barrier to "
            "adoption, particularly for hardware implementations in smart cards and HSMs.",
        ]),
        # Page 16: Key Size and Migration
        ("", [
            "7.2 Key Size Management",
            "The increased key and signature sizes of post-quantum schemes create challenges for "
            "existing protocols and storage systems. TLS 1.3 handshakes with ML-KEM-768 require "
            "approximately 2.4 KB additional data compared to ECDH, potentially causing packet "
            "fragmentation and increasing handshake latency on high-latency networks.",
            "Certificate chains in PKI systems are particularly affected: a three-certificate chain "
            "using ML-DSA-65 occupies approximately 12 KB for signatures alone, compared to under "
            "1 KB for ECDSA. This impacts certificate transparency logs, OCSP responses, and "
            "bandwidth-constrained applications.",
            "8. Migration Strategies",
            "8.1 Hybrid Approaches",
            "Hybrid key agreement combines a classical key exchange (e.g., X25519) with a "
            "post-quantum KEM (e.g., ML-KEM-768), providing security against both classical and "
            "quantum adversaries. Google's CECPQ2 experiment and Cloudflare's post-quantum TLS "
            "deployment demonstrated the feasibility of hybrid approaches with minimal performance "
            "impact. The IETF has standardized hybrid key exchange for TLS 1.3, and major browser "
            "vendors have begun deployment.",
        ]),
        # Page 17: Protocol Upgrades and Future
        ("", [
            "8.2 Protocol Upgrades",
            "Transitioning existing systems to post-quantum cryptography requires coordinated "
            "upgrades across protocol stacks, certificate authorities, and client/server software. "
            "The crypto-agility principle—designing systems to support algorithm substitution without "
            "fundamental protocol changes—is essential for managing this transition.",
            "Major cloud providers (AWS, Google Cloud, Microsoft Azure) have announced post-quantum "
            "TLS support timelines, with production deployments expected by 2026-2027. The U.S. "
            "government has mandated quantum-resistant cryptography for federal systems by 2035, "
            "with transition plans required by 2028 (NSM-10).",
            "9. Future Directions",
            "Several promising research directions may further improve post-quantum cryptography: "
            "(1) structured lattice schemes with tighter security reductions, (2) isogeny-based "
            "constructions following the SIDH break, particularly CSIDH variants, (3) quantum-safe "
            "zero-knowledge proofs for privacy-preserving applications, and (4) homomorphic encryption "
            "advances enabling secure computation on quantum-vulnerable data.",
            "The intersection of quantum computing and machine learning presents both challenges "
            "(adversarial use of quantum algorithms against cryptographic primitives) and "
            "opportunities (quantum-enhanced key distribution and authentication protocols).",
        ]),
        # Page 18: Conclusion
        ("10. Conclusion", [
            "The transition to post-quantum cryptography is not merely a theoretical exercise but "
            "an urgent practical necessity. The NIST standardization process has produced mature, "
            "well-analyzed algorithms ready for deployment, with lattice-based schemes (ML-KEM, "
            "ML-DSA) offering the most favorable balance of security and performance for general "
            "use, and hash-based signatures (SLH-DSA) providing a conservative fallback.",
            "Organizations should begin migration planning immediately, adopting hybrid approaches "
            "for new deployments while inventorying existing cryptographic dependencies. The 'harvest "
            "now, decrypt later' threat makes this transition time-sensitive, even in the absence "
            "of a cryptographically relevant quantum computer.",
            "Our performance benchmarks demonstrate that post-quantum algorithms impose acceptable "
            "overhead for most applications, with the primary challenges lying in key size management "
            "and protocol adaptation rather than raw computational cost. The cryptographic community's "
            "proactive response to the quantum threat, through both theoretical advances and practical "
            "standardization, provides a solid foundation for maintaining security in the quantum era.",
        ]),
    ]

    # Page 3-18 (16 pages of content)
    for i, (heading, paragraphs) in enumerate(sections):
        page = doc.new_page(width=W, height=H)
        y = 90

        # Section heading
        if heading:
            page.insert_text(pymupdf.Point(MARGIN_LEFT, y), heading,
                             fontsize=16, fontname="hebo", color=(0, 0, 0))
            y += 30

        # Paragraphs
        for para in paragraphs:
            rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, H - 72)
            excess = page.insert_textbox(rect, para, fontsize=10, fontname="helv",
                                         color=(0, 0, 0), align=0)
            # Estimate lines used
            lines = len(para) / 75 + 1
            y += lines * 13 + 12
            if y > H - 100:
                break

        # Page number at bottom
        page.insert_text(pymupdf.Point(W/2 - 5, H - 40), str(i + 3),
                         fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Add page numbers to first two pages
    doc[0].insert_text(pymupdf.Point(W/2 - 5, H - 40), "1",
                       fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
    doc[1].insert_text(pymupdf.Point(W/2 - 5, H - 40), "2",
                       fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Set INCOMPLETE metadata (as specified in task context)
    # Title and Author are empty, Subject and Keywords are absent
    doc.set_metadata({
        "title": "",
        "author": "",
        "subject": "",
        "keywords": "",
        "creator": "",
        "producer": "PyMuPDF",
    })

    # Set a basic TOC
    toc = [
        [1, "Introduction", 3],
        [1, "Background on Quantum Computing", 4],
        [2, "Quantum Gates and Circuits", 4],
        [2, "Quantum Algorithms Overview", 5],
        [1, "Threats to Classical Cryptography", 6],
        [2, "Shor's Algorithm and RSA", 6],
        [2, "Grover's Algorithm and Symmetric Keys", 7],
        [1, "Post-Quantum Cryptographic Schemes", 8],
        [2, "Lattice-Based Cryptography", 8],
        [2, "Code-Based Cryptography", 9],
        [2, "Hash-Based Signatures", 10],
        [2, "Multivariate Cryptography", 10],
        [1, "NIST Standardization Process", 11],
        [1, "Performance Benchmarks", 13],
        [1, "Implementation Challenges", 15],
        [1, "Migration Strategies", 16],
        [1, "Future Directions", 17],
        [1, "Conclusion", 18],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 18')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
