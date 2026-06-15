"""
Initial Setup: Create a 7-page academic paper PDF for ink annotation task
Task ID: pdf_res_055
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_055'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/review_copy.pdf'


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

    # --- Page dimensions ---
    W, H = 595, 842  # A4

    # ---- Content for a realistic 7-page academic paper ----

    # Page 1: Title page
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(W/2 - 180, 180),
                     "Efficient Transformer Architectures for",
                     fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(W/2 - 160, 210),
                     "Long-Range Sequence Modeling",
                     fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(W/2 - 120, 270),
                     "Elena Kowalski, James Park, Mei-Lin Zhou",
                     fontsize=12, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(W/2 - 140, 295),
                     "Department of Computer Science, Westfield University",
                     fontsize=10, fontname="heit", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(W/2 - 80, 320),
                     "{ekowalski, jpark, mzhou}@westfield.edu",
                     fontsize=10, fontname="cour", color=(0, 0, 0.6))

    abstract_text = (
        "Abstract. We present a novel attention mechanism that reduces the quadratic "
        "complexity of standard transformers to near-linear scaling for long sequences. "
        "Our approach, Sparse Adaptive Attention (SAA), dynamically selects relevant "
        "token subsets using a learned routing function, achieving comparable accuracy "
        "to full attention while processing sequences up to 16,384 tokens efficiently. "
        "Experiments on language modeling, document classification, and long-range "
        "reasoning benchmarks demonstrate that SAA achieves 2.3x speedup over "
        "FlashAttention-2 with less than 0.5% accuracy degradation. We release our "
        "implementation and pretrained models for reproducibility."
    )
    rect = pymupdf.Rect(72, 380, W - 72, 560)
    page.insert_textbox(rect, abstract_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 590), "Keywords:", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(135, 590),
                     " transformers, attention mechanism, efficiency, long-range dependencies",
                     fontsize=10, fontname="helv", color=(0, 0, 0))

    # Page 2: Introduction
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "1  Introduction", fontsize=14, fontname="hebo")
    intro_text = (
        "The transformer architecture has become the dominant paradigm for sequence "
        "modeling tasks across natural language processing, computer vision, and "
        "scientific computing. However, the self-attention mechanism at its core "
        "requires O(n^2) time and memory with respect to sequence length n, creating "
        "a fundamental bottleneck for applications involving long documents, genomic "
        "sequences, or high-resolution images.\n\n"
        "Several approaches have been proposed to address this limitation. Linear "
        "attention methods replace the softmax kernel with feature maps that enable "
        "computation in O(n) time, but often sacrifice modeling quality. Sparse "
        "attention patterns such as local windows, dilated attention, and block-sparse "
        "formulations reduce complexity to O(n sqrt(n)) but rely on fixed patterns "
        "that may miss important long-range dependencies.\n\n"
        "In this paper, we propose Sparse Adaptive Attention (SAA), a mechanism that "
        "learns to dynamically route each query to its most relevant key-value pairs. "
        "Unlike static sparse patterns, SAA adapts its connectivity at inference time, "
        "enabling both local and global information flow as needed by the input. Our "
        "routing function is differentiable and trained end-to-end, requiring no "
        "separate routing network or auxiliary losses.\n\n"
        "Our contributions are threefold:\n"
        "  (1) We introduce a differentiable top-k routing mechanism for attention.\n"
        "  (2) We provide theoretical analysis showing SAA preserves approximation.\n"
        "  (3) We demonstrate empirical gains on five benchmarks."
    )
    rect = pymupdf.Rect(72, 95, W - 72, H - 72)
    page.insert_textbox(rect, intro_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 3: Main contributions (Section 2 - Method)
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "2  Method", fontsize=14, fontname="hebo")
    page.insert_text(pymupdf.Point(72, 100), "2.1  Sparse Adaptive Attention", fontsize=12, fontname="hebo")
    method_text = (
        "Given an input sequence X of length n with embedding dimension d, standard "
        "multi-head attention computes Q = XW_Q, K = XW_K, V = XW_V and produces "
        "output O = softmax(QK^T / sqrt(d_k))V. The bottleneck is the n x n attention "
        "matrix computation.\n\n"
        "SAA replaces full attention with a learned routing step. For each query q_i, "
        "we compute a routing score r_i = sigma(q_i W_r) over all positions, then "
        "select the top-k positions with highest scores. Only these k key-value pairs "
        "participate in the attention computation for q_i.\n\n"
        "Formally, let S_i = TopK(r_i, k) be the set of selected indices. The output "
        "for position i is: o_i = sum_{j in S_i} alpha_{ij} v_j, where alpha_{ij} = "
        "softmax_j(q_i k_j^T / sqrt(d_k)) for j in S_i.\n\n"
        "The routing function W_r is a learnable d x n projection trained jointly with "
        "the attention parameters. To maintain differentiability through the discrete "
        "top-k operation, we use the straight-through estimator during backpropagation "
        "and add a soft entropy regularization term to encourage diverse routing."
    )
    rect = pymupdf.Rect(72, 118, W - 72, 420)
    page.insert_textbox(rect, method_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 440), "2.2  Complexity Analysis", fontsize=12, fontname="hebo")
    complexity_text = (
        "With k selected positions per query, the attention computation requires "
        "O(nk) time and memory, compared to O(n^2) for full attention. When k = "
        "O(sqrt(n)), this yields O(n^{3/2}) complexity. In practice, we find that "
        "k = 128 suffices for sequences up to 16,384 tokens, giving effectively "
        "linear scaling with a small constant factor.\n\n"
        "The routing computation itself requires O(nd) per query for score computation "
        "and O(n log k) for the top-k selection, both subquadratic in n. The total "
        "per-layer complexity is O(n(d + k*d_k + n) ) which simplifies to O(n^2) in "
        "the worst case but is O(nk) in practice since k << n.\n\n"
        "Memory efficiency is equally important. SAA stores only the selected indices "
        "and their attention weights, reducing the memory footprint from O(n^2) to "
        "O(nk) per layer per head. This enables processing of sequences that would "
        "cause out-of-memory errors with standard attention on typical GPU hardware."
    )
    rect = pymupdf.Rect(72, 460, W - 72, H - 72)
    page.insert_textbox(rect, complexity_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 4: More contributions (Section 2.3 + Section 3)
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "2.3  Multi-Scale Routing", fontsize=12, fontname="hebo")
    multiscale_text = (
        "To capture dependencies at multiple granularities, we extend SAA with "
        "multi-scale routing. The input sequence is hierarchically pooled at scales "
        "1x, 2x, and 4x, producing representations at different resolutions. Each "
        "attention head operates at a specific scale, with some heads attending to "
        "fine-grained local tokens and others attending to coarse-grained summaries "
        "of distant regions.\n\n"
        "This design is inspired by multi-resolution analysis in signal processing "
        "and allows the model to maintain high-fidelity local attention while "
        "efficiently capturing global context. The routing function at each scale "
        "is independently parameterized, enabling scale-specific attention patterns.\n\n"
        "We allocate half the attention heads to 1x scale (local), a quarter to 2x "
        "(medium-range), and a quarter to 4x (long-range). This allocation was "
        "determined through ablation studies reported in Section 4.3."
    )
    rect = pymupdf.Rect(72, 95, W - 72, 340)
    page.insert_textbox(rect, multiscale_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 360), "3  Experimental Setup", fontsize=14, fontname="hebo")
    setup_text = (
        "We evaluate SAA on five benchmarks spanning language modeling, classification, "
        "and long-range reasoning tasks:\n\n"
        "  - WikiText-103: Standard language modeling benchmark with long documents.\n"
        "  - Long Range Arena (LRA): Suite of synthetic long-range reasoning tasks.\n"
        "  - SCROLLS: Document-level NLU benchmark with contexts up to 50K tokens.\n"
        "  - PG-19: Book-level language modeling with very long sequences.\n"
        "  - HotpotQA: Multi-hop question answering requiring cross-document reasoning.\n\n"
        "All models use a 12-layer transformer with 8 attention heads, hidden "
        "dimension 768, and feedforward dimension 3072. We train with AdamW optimizer, "
        "learning rate 3e-4 with cosine decay, batch size 32, and gradient clipping "
        "at 1.0. Training runs for 100K steps on 8 A100 GPUs."
    )
    rect = pymupdf.Rect(72, 385, W - 72, H - 72)
    page.insert_textbox(rect, setup_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 5: Results
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "4  Results", fontsize=14, fontname="hebo")
    page.insert_text(pymupdf.Point(72, 100), "4.1  Main Results", fontsize=12, fontname="hebo")
    results_text = (
        "Table 1 summarizes our main results across all benchmarks. SAA consistently "
        "matches or exceeds the performance of efficient attention baselines while "
        "maintaining significant speedup over full attention.\n\n"
        "On WikiText-103, SAA achieves a perplexity of 18.3, compared to 18.1 for "
        "full attention and 19.2 for Performer. On LRA, our average accuracy of 61.4% "
        "is within 0.3% of full attention (61.7%) and substantially higher than "
        "Linear Attention (58.2%). The SCROLLS benchmark shows the largest gains, "
        "with SAA achieving 42.1 ROUGE-L compared to 38.7 for Longformer.\n\n"
        "Throughput measurements confirm the efficiency benefits: at sequence length "
        "8192, SAA processes 2.3x more tokens per second than FlashAttention-2, and "
        "the gap widens to 3.8x at sequence length 16384. Memory consumption is "
        "reduced by 4.1x at the longest sequences tested."
    )
    rect = pymupdf.Rect(72, 118, W - 72, 380)
    page.insert_textbox(rect, results_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 400), "4.2  Throughput Comparison", fontsize=12, fontname="hebo")
    throughput_text = (
        "We measure end-to-end training throughput on a single A100-80GB GPU across "
        "varying sequence lengths. At n=2048, all methods achieve similar throughput "
        "since attention is not yet the bottleneck. At n=4096, SAA provides 1.5x "
        "speedup over full attention. The advantage grows to 2.3x at n=8192 and "
        "3.8x at n=16384, where full attention exhausts GPU memory entirely.\n\n"
        "Compared to FlashAttention-2, which optimizes the IO complexity of full "
        "attention through memory-aware tiling, SAA provides further gains by "
        "reducing the arithmetic complexity itself. The two optimizations are "
        "complementary: applying FlashAttention-2 to SAA's sparse attention "
        "computation yields an additional 1.2x speedup."
    )
    rect = pymupdf.Rect(72, 420, W - 72, H - 72)
    page.insert_textbox(rect, throughput_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 6: Ablations
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "4.3  Ablation Studies", fontsize=12, fontname="hebo")
    ablation_text = (
        "We conduct ablation studies to understand the contribution of each component.\n\n"
        "Routing mechanism: Replacing learned routing with random selection degrades "
        "WikiText-103 perplexity from 18.3 to 20.7, confirming that adaptive routing "
        "is essential. Using hash-based routing (as in Reformer) achieves 19.1, better "
        "than random but worse than learned routing.\n\n"
        "Number of selected keys (k): Performance is robust across k in [64, 256], "
        "with k=128 offering the best accuracy-efficiency tradeoff. Below k=32, "
        "accuracy degrades significantly. Above k=256, the efficiency gains diminish "
        "while accuracy plateaus.\n\n"
        "Multi-scale routing: Removing multi-scale routing (using only 1x scale) "
        "reduces LRA accuracy from 61.4% to 59.8%, particularly affecting the "
        "Pathfinder and Image tasks that require integrating spatial information "
        "across long distances.\n\n"
        "Entropy regularization: Without the entropy term, routing collapses to "
        "attending only to nearby tokens within 5 training epochs, degrading to a "
        "local attention pattern. The regularization strength lambda=0.01 balances "
        "diversity with task-driven specialization."
    )
    rect = pymupdf.Rect(72, 95, W - 72, 500)
    page.insert_textbox(rect, ablation_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 520), "5  Related Work", fontsize=14, fontname="hebo")
    related_text = (
        "Efficient transformers have been extensively studied. Performer uses random "
        "feature maps for linear attention. Linformer projects keys and values to "
        "lower dimensions. BigBird and Longformer combine local and global attention "
        "patterns. FlashAttention and FlashAttention-2 optimize IO complexity without "
        "changing the attention mechanism. Our work differs by learning adaptive "
        "sparse patterns that change based on the input."
    )
    rect = pymupdf.Rect(72, 540, W - 72, H - 72)
    page.insert_textbox(rect, related_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 7: Conclusion and References
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "6  Conclusion", fontsize=14, fontname="hebo")
    conclusion_text = (
        "We presented Sparse Adaptive Attention (SAA), a learned routing mechanism "
        "that dynamically selects relevant key-value pairs for each query in "
        "transformer attention. SAA achieves near-linear complexity while preserving "
        "the modeling quality of full attention. Our multi-scale extension enables "
        "efficient capture of both local and global dependencies.\n\n"
        "Across five benchmarks, SAA matches full attention accuracy with 2.3-3.8x "
        "throughput improvements and 4x memory reduction. These gains enable training "
        "and inference on sequences up to 16K tokens on standard hardware, opening "
        "new possibilities for long-document understanding and generation tasks.\n\n"
        "Future work includes extending SAA to cross-attention in encoder-decoder "
        "models and exploring its application to vision transformers with "
        "high-resolution inputs."
    )
    rect = pymupdf.Rect(72, 95, W - 72, 340)
    page.insert_textbox(rect, conclusion_text, fontsize=10, fontname="helv",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 370), "References", fontsize=14, fontname="hebo")
    references = [
        "[1] Vaswani, A. et al. Attention is All You Need. NeurIPS 2017.",
        "[2] Kitaev, N. et al. Reformer: The Efficient Transformer. ICLR 2020.",
        "[3] Katharopoulos, A. et al. Transformers are RNNs. ICML 2020.",
        "[4] Beltagy, I. et al. Longformer: The Long-Document Transformer. 2020.",
        "[5] Zaheer, M. et al. Big Bird: Transformers for Longer Sequences. NeurIPS 2020.",
        "[6] Dao, T. et al. FlashAttention: Fast and Memory-Efficient Attention. NeurIPS 2022.",
        "[7] Dao, T. FlashAttention-2: Faster Attention with Better Parallelism. 2023.",
        "[8] Choromanski, K. et al. Rethinking Attention with Performers. ICLR 2021.",
        "[9] Wang, S. et al. Linformer: Self-Attention with Linear Complexity. 2020.",
        "[10] Xiong, Y. et al. Nystromformer: A Nystrom-Based Algorithm. AAAI 2021.",
    ]
    y = 395
    for ref in references:
        page.insert_text(pymupdf.Point(72, y), ref, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 18

    # Set metadata
    doc.set_metadata({
        "title": "Efficient Transformer Architectures for Long-Range Sequence Modeling",
        "author": "Elena Kowalski, James Park, Mei-Lin Zhou",
        "subject": "Computer Science - Machine Learning",
        "keywords": "transformers, attention, efficiency, sparse attention",
        "creator": "LaTeX",
        "producer": "pdfTeX-1.40.25",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
