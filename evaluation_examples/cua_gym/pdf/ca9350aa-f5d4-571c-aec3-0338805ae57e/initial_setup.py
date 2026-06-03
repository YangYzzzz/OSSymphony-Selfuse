"""
Initial Setup: Create a 16-page academic paper PDF with default/empty metadata
Task ID: pdf_res_015
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_015'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/my_paper.pdf'


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

    # Page dimensions (Letter size)
    W, H = 612, 792
    MARGIN_LEFT = 72
    MARGIN_RIGHT = W - 72
    MARGIN_TOP = 72
    MARGIN_BOTTOM = H - 72
    TEXT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT

    # ---- Page 1: Title Page ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(W/2 - 200, 200),
                     "Deep Learning for Natural Language",
                     fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(W/2 - 160, 230),
                     "Processing: A Survey",
                     fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(W/2 - 100, 300),
                     "Alice Zhang, Bob Smith",
                     fontsize=14, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(W/2 - 130, 330),
                     "Department of Computer Science",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(W/2 - 100, 350),
                     "Stanford University",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))

    abstract_text = (
        "Abstract -- This survey provides a comprehensive overview of deep learning techniques "
        "applied to natural language processing (NLP). We review the evolution from traditional "
        "methods to modern transformer-based architectures, examining key advances in language "
        "modeling, machine translation, sentiment analysis, question answering, and text "
        "generation. We discuss the role of attention mechanisms, pre-trained language models "
        "such as BERT, GPT, and T5, and their impact on downstream NLP tasks. Finally, we "
        "identify open challenges and promising future directions in the field."
    )
    page.insert_textbox(pymupdf.Rect(MARGIN_LEFT, 420, MARGIN_RIGHT, 600),
                        abstract_text, fontsize=10, fontname="tiit",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- Page 2: Table of Contents ----
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + 20),
                     "Table of Contents", fontsize=16, fontname="hebo")
    toc_entries = [
        ("1. Introduction", "3"),
        ("2. Background and Related Work", "4"),
        ("   2.1 Traditional NLP Methods", "4"),
        ("   2.2 Neural Network Foundations", "5"),
        ("3. Word Embeddings and Representations", "6"),
        ("   3.1 Word2Vec and GloVe", "6"),
        ("   3.2 Contextual Embeddings", "7"),
        ("4. Recurrent Neural Networks for NLP", "8"),
        ("   4.1 LSTM and GRU Architectures", "8"),
        ("   4.2 Sequence-to-Sequence Models", "9"),
        ("5. The Transformer Architecture", "10"),
        ("   5.1 Self-Attention Mechanism", "10"),
        ("   5.2 Multi-Head Attention", "11"),
        ("6. Pre-trained Language Models", "12"),
        ("   6.1 BERT and Variants", "12"),
        ("   6.2 GPT Family", "13"),
        ("   6.3 T5 and Encoder-Decoder Models", "13"),
        ("7. Applications and Benchmarks", "14"),
        ("8. Challenges and Future Directions", "15"),
        ("9. Conclusion", "16"),
        ("References", "16"),
    ]
    y = MARGIN_TOP + 60
    for entry, pg in toc_entries:
        page.insert_text(pymupdf.Point(MARGIN_LEFT + 10, y),
                         entry, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(MARGIN_RIGHT - 20, y),
                         pg, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 18

    # Section content for pages 3-16
    sections = [
        ("1. Introduction",
         "Natural language processing has undergone a remarkable transformation over the past "
         "decade, driven primarily by advances in deep learning. Traditional rule-based and "
         "statistical approaches, while foundational, struggled to capture the nuanced patterns "
         "inherent in human language. The introduction of neural network models, particularly "
         "deep architectures, has fundamentally changed the landscape of NLP research and "
         "applications.\n\n"
         "This survey aims to provide a structured overview of the major developments in deep "
         "learning for NLP. We trace the evolution from early word embeddings through recurrent "
         "networks to the transformer architecture that dominates current research. Our goal is "
         "to offer both newcomers and experienced practitioners a reference for understanding "
         "the field's trajectory and current state of the art.\n\n"
         "The organization of this paper is as follows. Section 2 reviews background material "
         "and related work. Section 3 discusses word embeddings and representation learning. "
         "Section 4 covers recurrent neural networks. Section 5 introduces the transformer. "
         "Section 6 examines pre-trained language models. Section 7 surveys applications, and "
         "Section 8 discusses challenges and future directions."),

        ("2. Background and Related Work",
         "2.1 Traditional NLP Methods\n\n"
         "Before the neural revolution, NLP relied heavily on hand-crafted features, "
         "rule-based parsing, and statistical models. Bag-of-words representations, TF-IDF "
         "weighting, and n-gram language models formed the backbone of text processing "
         "systems. Named entity recognition employed conditional random fields (CRFs), while "
         "syntactic parsing used probabilistic context-free grammars (PCFGs).\n\n"
         "These approaches achieved reasonable performance on well-defined tasks but required "
         "extensive feature engineering and domain expertise. They struggled with capturing "
         "long-range dependencies and generalizing across domains. The labor-intensive nature "
         "of feature design became a significant bottleneck as the scale of NLP applications grew."),

        ("2.2 Neural Network Foundations (cont.)",
         "The application of neural networks to NLP began with simple feed-forward "
         "architectures for language modeling, introduced by Bengio et al. in 2003. These "
         "models learned distributed representations of words, demonstrating that neural "
         "approaches could capture syntactic and semantic relationships without explicit "
         "feature engineering.\n\n"
         "The key insight was that words could be represented as dense, low-dimensional "
         "vectors in a continuous space, where geometric proximity reflected semantic "
         "similarity. This laid the groundwork for the representation learning revolution "
         "that would follow. Early experiments showed that even shallow networks could "
         "learn useful word associations, such as the relationship between countries and "
         "their capitals, or verb tenses."),

        ("3. Word Embeddings and Representations",
         "3.1 Word2Vec and GloVe\n\n"
         "Mikolov et al. (2013) introduced Word2Vec, which efficiently learned word vectors "
         "from large corpora using either the Continuous Bag-of-Words (CBOW) or Skip-gram "
         "architecture. The resulting embeddings captured remarkable analogical relationships, "
         "famously demonstrating that vec('king') - vec('man') + vec('woman') approximated "
         "vec('queen').\n\n"
         "Pennington et al. (2014) proposed GloVe (Global Vectors for Word Representation), "
         "which combined the advantages of global matrix factorization methods with local "
         "context window methods. GloVe constructs a word-word co-occurrence matrix from the "
         "corpus and learns embeddings by factorizing this matrix. Both methods produce "
         "static embeddings, meaning each word has a single vector regardless of context."),

        ("3.2 Contextual Embeddings (cont.)",
         "The limitation of static embeddings became apparent when dealing with polysemous "
         "words. For example, the word 'bank' has different meanings in 'river bank' versus "
         "'savings bank', yet static embeddings assign a single representation.\n\n"
         "Peters et al. (2018) addressed this with ELMo (Embeddings from Language Models), "
         "which generated context-dependent word representations using a bidirectional LSTM "
         "language model. ELMo produces different vectors for the same word depending on its "
         "surrounding context, significantly improving performance on tasks such as question "
         "answering, textual entailment, and sentiment analysis. This marked a paradigm shift "
         "toward contextualized representations that would culminate in transformer-based models."),

        ("4. Recurrent Neural Networks for NLP",
         "4.1 LSTM and GRU Architectures\n\n"
         "Recurrent neural networks (RNNs) process sequential data by maintaining a hidden "
         "state that captures information from previous time steps. However, vanilla RNNs "
         "suffer from the vanishing gradient problem, making it difficult to learn long-range "
         "dependencies.\n\n"
         "Long Short-Term Memory (LSTM) networks, introduced by Hochreiter and Schmidhuber "
         "(1997), addressed this with gating mechanisms that control information flow. The "
         "forget gate, input gate, and output gate allow LSTMs to selectively retain or "
         "discard information over many time steps. Gated Recurrent Units (GRUs), proposed "
         "by Cho et al. (2014), simplified the LSTM architecture while maintaining comparable "
         "performance, using only reset and update gates."),

        ("4.2 Sequence-to-Sequence Models (cont.)",
         "Sutskever et al. (2014) introduced the sequence-to-sequence (Seq2Seq) framework, "
         "which uses an encoder RNN to compress the input sequence into a fixed-length vector "
         "and a decoder RNN to generate the output sequence. This architecture became the "
         "foundation for neural machine translation.\n\n"
         "Bahdanau et al. (2015) extended Seq2Seq with an attention mechanism that allows "
         "the decoder to focus on different parts of the input sequence at each decoding step. "
         "This eliminated the information bottleneck of fixed-length encoding and significantly "
         "improved translation quality, especially for long sentences. The attention mechanism "
         "would prove to be one of the most important innovations in NLP."),

        ("5. The Transformer Architecture",
         "5.1 Self-Attention Mechanism\n\n"
         "Vaswani et al. (2017) introduced the Transformer in their landmark paper 'Attention "
         "Is All You Need.' The key innovation was replacing recurrence entirely with "
         "self-attention, allowing the model to process all positions in a sequence "
         "simultaneously.\n\n"
         "Self-attention computes a weighted sum of value vectors, where the weights are "
         "determined by the compatibility between query and key vectors. Given input "
         "representations X, the attention function is:\n\n"
         "   Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V\n\n"
         "where Q = XW_Q, K = XW_K, V = XW_V are linear projections. This mechanism allows "
         "each position to attend to all other positions, capturing both local and global "
         "dependencies without the sequential constraint of RNNs."),

        ("5.2 Multi-Head Attention (cont.)",
         "Multi-head attention extends self-attention by running h parallel attention "
         "functions with different learned projections. The outputs are concatenated and "
         "projected:\n\n"
         "   MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W_O\n"
         "   where head_i = Attention(QW_Q^i, KW_K^i, VW_V^i)\n\n"
         "This allows the model to jointly attend to information from different representation "
         "subspaces at different positions. In practice, transformers use 8 or 16 attention "
         "heads, with each head operating on a reduced dimensionality.\n\n"
         "The transformer also incorporates positional encoding (since self-attention is "
         "permutation-invariant), residual connections, layer normalization, and position-wise "
         "feed-forward networks. These components together create a powerful architecture that "
         "has become the de facto standard for NLP."),

        ("6. Pre-trained Language Models",
         "6.1 BERT and Variants\n\n"
         "Devlin et al. (2019) introduced BERT (Bidirectional Encoder Representations from "
         "Transformers), which pre-trains a deep bidirectional transformer using masked "
         "language modeling (MLM) and next sentence prediction (NSP). BERT revolutionized "
         "NLP by demonstrating that a single pre-trained model could be fine-tuned to achieve "
         "state-of-the-art results on 11 different NLP tasks.\n\n"
         "Subsequent variants include RoBERTa (Liu et al., 2019), which optimized BERT's "
         "training procedure; ALBERT (Lan et al., 2020), which reduced parameters through "
         "factorized embeddings; and DeBERTa (He et al., 2021), which introduced disentangled "
         "attention. DistilBERT (Sanh et al., 2019) applied knowledge distillation to create "
         "a smaller, faster model retaining 97% of BERT's performance."),

        ("6.2 GPT Family / 6.3 T5 and Encoder-Decoder Models",
         "The GPT (Generative Pre-trained Transformer) series from OpenAI takes a different "
         "approach, using autoregressive language modeling with a decoder-only transformer. "
         "GPT-2 (Radford et al., 2019) demonstrated impressive text generation capabilities. "
         "GPT-3 (Brown et al., 2020), with 175 billion parameters, showed that scaling model "
         "size enables few-shot and zero-shot learning across diverse tasks.\n\n"
         "Raffel et al. (2020) proposed T5 (Text-to-Text Transfer Transformer), which frames "
         "all NLP tasks as text-to-text problems using an encoder-decoder architecture. This "
         "unified framework simplifies multi-task learning and transfer. T5 demonstrated that "
         "scaling compute, data, and model size systematically improves performance. Subsequent "
         "work by Chung et al. (2022) introduced Flan-T5, which further improved T5 through "
         "instruction tuning on a diverse mixture of tasks."),

        ("7. Applications and Benchmarks",
         "Deep learning has transformed virtually every NLP application area:\n\n"
         "Machine Translation: Neural MT systems based on transformers (e.g., MarianMT, mBART) "
         "have achieved near-human translation quality for high-resource language pairs.\n\n"
         "Sentiment Analysis: Pre-trained models fine-tuned on labeled data consistently "
         "outperform traditional methods on benchmark datasets such as SST-2 and IMDb.\n\n"
         "Question Answering: Models like BERT and UnifiedQA achieve strong performance on "
         "SQuAD, Natural Questions, and TriviaQA benchmarks.\n\n"
         "Text Summarization: Abstractive summarization using BART, PEGASUS, and T5 generates "
         "fluent summaries that capture key information from source documents.\n\n"
         "Named Entity Recognition: BiLSTM-CRF and transformer-based taggers achieve F1 scores "
         "above 90% on CoNLL benchmarks.\n\n"
         "Key benchmarks include GLUE, SuperGLUE, SQuAD, WMT, and the recently proposed "
         "BIG-bench for evaluating large language models."),

        ("8. Challenges and Future Directions",
         "Despite remarkable progress, several challenges remain:\n\n"
         "Computational Cost: Training large models requires significant GPU/TPU resources, "
         "raising concerns about environmental impact and accessibility. Efficient training "
         "methods such as mixed precision, gradient checkpointing, and model parallelism "
         "help but do not fully solve the problem.\n\n"
         "Bias and Fairness: Pre-trained models can amplify societal biases present in "
         "training data. Active research areas include bias detection, debiasing techniques, "
         "and fairness-aware training.\n\n"
         "Interpretability: Transformer models remain largely opaque. Attention visualization, "
         "probing classifiers, and mechanistic interpretability are promising but incomplete.\n\n"
         "Multilinguality: While multilingual models (mBERT, XLM-R) have improved cross-lingual "
         "transfer, low-resource languages remain underserved.\n\n"
         "Reasoning: Current models struggle with multi-step logical reasoning, mathematical "
         "problem solving, and causal inference. Chain-of-thought prompting and neurosymbolic "
         "approaches are active research directions."),

        ("9. Conclusion / References",
         "This survey has traced the evolution of deep learning techniques for NLP, from "
         "early word embeddings through recurrent networks to the transformer architecture "
         "and pre-trained language models that define the current state of the art. The "
         "field continues to advance rapidly, with new architectures, training methods, and "
         "applications emerging regularly.\n\n"
         "As models grow in scale and capability, addressing challenges around efficiency, "
         "fairness, and interpretability becomes increasingly important. We believe that the "
         "combination of continued architectural innovation, responsible development practices, "
         "and interdisciplinary collaboration will drive the next wave of breakthroughs in "
         "natural language processing.\n\n"
         "References\n\n"
         "[1] Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural machine translation by "
         "jointly learning to align and translate. ICLR 2015.\n"
         "[2] Brown, T. et al. (2020). Language models are few-shot learners. NeurIPS 2020.\n"
         "[3] Devlin, J. et al. (2019). BERT: Pre-training of deep bidirectional "
         "transformers for language understanding. NAACL 2019.\n"
         "[4] Hochreiter, S. & Schmidhuber, J. (1997). Long short-term memory. "
         "Neural Computation, 9(8).\n"
         "[5] Mikolov, T. et al. (2013). Efficient estimation of word representations "
         "in vector space. ICLR Workshop 2013.\n"
         "[6] Pennington, J., Socher, R., & Manning, C.D. (2014). GloVe: Global vectors "
         "for word representation. EMNLP 2014.\n"
         "[7] Peters, M. et al. (2018). Deep contextualized word representations. NAACL 2018.\n"
         "[8] Raffel, C. et al. (2020). Exploring the limits of transfer learning with a "
         "unified text-to-text transformer. JMLR 2020.\n"
         "[9] Vaswani, A. et al. (2017). Attention is all you need. NeurIPS 2017.\n"),
    ]

    for title, body in sections:
        page = doc.new_page(width=W, height=H)
        # Section title
        page.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + 20),
                         title, fontsize=14, fontname="hebo", color=(0, 0, 0))
        # Section body
        page.insert_textbox(
            pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 45, MARGIN_RIGHT, MARGIN_BOTTOM),
            body, fontsize=10, fontname="helv", color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY
        )

    # Set NO metadata intentionally (default/empty)
    doc.set_metadata({
        "title": "",
        "author": "",
        "subject": "",
        "keywords": "",
        "creator": "",
        "producer": "",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {pymupdf.open(OUTPUT).page_count}')

    # Open the PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
