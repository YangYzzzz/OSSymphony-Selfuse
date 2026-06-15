"""
Initial Setup: Create a 15-page NLP survey PDF with references on pages 12-15
Task ID: pdf_res_021
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_021'
PAPERS_DIR = f'{WORKDIR}/papers'
OUTPUT = f'{PAPERS_DIR}/nlp_survey.pdf'


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


# ── APA-style references (approx 45) ──
REFERENCES = [
    "Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30, 5998-6008.",
    "Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. Proceedings of NAACL-HLT, 4171-4186.",
    "Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., & Askell, A. (2020). Language models are few-shot learners. Advances in Neural Information Processing Systems, 33, 1877-1901.",
    "Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). Language models are unsupervised multitask learners. OpenAI Blog, 1(8), 9.",
    "Peters, M. E., Neumann, M., Iyyer, M., Gardner, M., Clark, C., Lee, K., & Zettlemoyer, L. (2018). Deep contextualized word representations. Proceedings of NAACL-HLT, 2227-2237.",
    "Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis, M., Zettlemoyer, L., & Stoyanov, V. (2019). RoBERTa: A robustly optimized BERT pretraining approach. arXiv preprint arXiv:1907.11692.",
    "Yang, Z., Dai, Z., Yang, Y., Carbonell, J., Salakhutdinov, R., & Le, Q. V. (2019). XLNet: Generalized autoregressive pretraining for language understanding. Advances in NeurIPS, 32, 5753-5763.",
    "Lan, Z., Chen, M., Goodman, S., Gimpel, K., Sharma, P., & Soricut, R. (2020). ALBERT: A lite BERT for self-supervised learning of language representations. Proceedings of ICLR.",
    "Clark, K., Luong, M. T., Le, Q. V., & Manning, C. D. (2020). ELECTRA: Pre-training text encoders as discriminators rather than generators. Proceedings of ICLR.",
    "Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., & Liu, P. J. (2020). Exploring the limits of transfer learning with a unified text-to-text transformer. Journal of Machine Learning Research, 21(140), 1-67.",
    "Lewis, M., Liu, Y., Goyal, N., Ghazvininejad, M., Mohamed, A., Levy, O., Stoyanov, V., & Zettlemoyer, L. (2020). BART: Denoising sequence-to-sequence pre-training for natural language generation, translation, and comprehension. Proceedings of ACL, 7871-7880.",
    "Conneau, A., Khandelwal, K., Goyal, N., Chaudhary, V., Wenzek, G., Guzman, F., Grave, E., Ott, M., Zettlemoyer, L., & Stoyanov, V. (2020). Unsupervised cross-lingual representation learning at scale. Proceedings of ACL, 8440-8451.",
    "Sanh, V., Debut, L., Chaumond, J., & Wolf, T. (2019). DistilBERT, a distilled version of BERT: Smaller, faster, cheaper and lighter. arXiv preprint arXiv:1910.01108.",
    "Wang, A., Singh, A., Michael, J., Hill, F., Levy, O., & Bowman, S. R. (2018). GLUE: A multi-task benchmark and analysis platform for natural language understanding. Proceedings of ICLR.",
    "Rajpurkar, P., Zhang, J., Lopyrev, K., & Liang, P. (2016). SQuAD: 100,000+ questions for machine comprehension of text. Proceedings of EMNLP, 2383-2392.",
    "Rajpurkar, P., Jia, R., & Liang, P. (2018). Know what you don't know: Unanswerable questions for SQuAD. Proceedings of ACL, 784-789.",
    "Mikolov, T., Sutskever, I., Chen, K., Corrado, G., & Dean, J. (2013). Distributed representations of words and phrases and their compositionality. Advances in NeurIPS, 26, 3111-3119.",
    "Pennington, J., Socher, R., & Manning, C. D. (2014). GloVe: Global vectors for word representation. Proceedings of EMNLP, 1532-1543.",
    "Bojanowski, P., Grave, E., Joulin, A., & Mikolov, T. (2017). Enriching word vectors with subword information. Transactions of the ACL, 5, 135-146.",
    "Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. Neural Computation, 9(8), 1735-1780.",
    "Cho, K., van Merrienboer, B., Gulcehre, C., Bahdanau, D., Bougares, F., Schwenk, H., & Bengio, Y. (2014). Learning phrase representations using RNN encoder-decoder for statistical machine translation. Proceedings of EMNLP, 1724-1734.",
    "Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural machine translation by jointly learning to align and translate. Proceedings of ICLR.",
    "Luong, M. T., Pham, H., & Manning, C. D. (2015). Effective approaches to attention-based neural machine translation. Proceedings of EMNLP, 1412-1421.",
    "Kim, Y. (2014). Convolutional neural networks for sentence classification. Proceedings of EMNLP, 1746-1751.",
    "Socher, R., Perelygin, A., Wu, J., Chuang, J., Manning, C. D., Ng, A. Y., & Potts, C. (2013). Recursive deep models for semantic compositionality over a sentiment treebank. Proceedings of EMNLP, 1631-1642.",
    "Zhang, X., Zhao, J., & LeCun, Y. (2015). Character-level convolutional networks for text classification. Advances in NeurIPS, 28, 649-657.",
    "Sutskever, I., Vinyals, O., & Le, Q. V. (2014). Sequence to sequence learning with neural networks. Advances in NeurIPS, 27, 3104-3112.",
    "Wu, Y., Schuster, M., Chen, Z., Le, Q. V., Norouzi, M., Macherey, W., Krikun, M., Cao, Y., Gao, Q., & Macherey, K. (2016). Google's neural machine translation system: Bridging the gap between human and machine translation. arXiv preprint arXiv:1609.08144.",
    "Gehring, J., Auli, M., Grangier, D., Yarats, D., & Dauphin, Y. N. (2017). Convolutional sequence to sequence learning. Proceedings of ICML, 1243-1252.",
    "Zoph, B., & Le, Q. V. (2017). Neural architecture search with reinforcement learning. Proceedings of ICLR.",
    "Howard, J., & Ruder, S. (2018). Universal language model fine-tuning for text classification. Proceedings of ACL, 328-339.",
    "Lample, G., & Conneau, A. (2019). Cross-lingual language model pretraining. Advances in NeurIPS, 32, 7059-7069.",
    "Sun, C., Qiu, X., Xu, Y., & Huang, X. (2019). How to fine-tune BERT for text classification. China National Conference on Chinese Computational Linguistics, 194-206.",
    "Dong, L., Yang, N., Wang, W., Wei, F., Liu, X., Wang, Y., Gao, J., Zhou, M., & Hon, H. W. (2019). Unified language model pre-training for natural language understanding and generation. Advances in NeurIPS, 32, 13063-13075.",
    "Kitaev, N., Kaiser, L., & Levskaya, A. (2020). Reformer: The efficient transformer. Proceedings of ICLR.",
    "Beltagy, I., Peters, M. E., & Cohan, A. (2020). Longformer: The long-document transformer. arXiv preprint arXiv:2004.05150.",
    "Zaheer, M., Guruganesh, G., Dubey, K. A., Ainslie, J., Alberti, C., Ontanon, S., Pham, P., Ravula, A., Wang, Q., & Yang, L. (2020). Big Bird: Transformers for longer sequences. Advances in NeurIPS, 33, 17283-17297.",
    "He, P., Liu, X., Gao, J., & Chen, W. (2021). DeBERTa: Decoding-enhanced BERT with disentangled attention. Proceedings of ICLR.",
    "Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts, A., Barham, P., Chung, H. W., Sutton, C., & Gehrmann, S. (2023). PaLM: Scaling language modeling with pathways. Journal of Machine Learning Research, 24(240), 1-113.",
    "Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M. A., Lacroix, T., Roziere, B., Goyal, N., Hambro, E., & Azhar, F. (2023). LLaMA: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971.",
    "Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., & Ray, A. (2022). Training language models to follow instructions with human feedback. Advances in NeurIPS, 35, 27730-27744.",
    "Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. V., & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. Advances in NeurIPS, 35, 24824-24837.",
    "Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large language models are zero-shot reasoners. Advances in NeurIPS, 35, 22199-22213.",
    "Wang, X., Wei, J., Schuurmans, D., Le, Q. V., Chi, E., Narang, S., Chowdhery, A., & Zhou, D. (2023). Self-consistency improves chain of thought reasoning in language models. Proceedings of ICLR.",
    "Zhong, W., Cui, Y., Qiu, X., & Huang, X. (2023). Comprehensive evaluation of ChatGPT on reasoning, hallucination, and interactivity. arXiv preprint arXiv:2302.04023.",
]


def create_initial():
    os.makedirs(PAPERS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions
    W, H = 612, 792  # US Letter
    LEFT = 72
    RIGHT = W - 72
    TOP = 72
    BOT = H - 72
    TEXT_W = RIGHT - LEFT

    # ──────── Page 1: Title page ────────
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(W / 2 - 180, 200),
                     "A Comprehensive Survey of",
                     fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(W / 2 - 220, 235),
                     "Natural Language Processing Methods",
                     fontsize=20, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(W / 2 - 200, 270),
                     "and Recent Advances (2013-2023)",
                     fontsize=20, fontname="hebo", color=(0, 0, 0))

    authors_text = (
        "Elena Marchetti, Rajesh Krishnamurthy, Sarah O'Brien,\n"
        "Wei-Lin Zhang, and Carlos Gutierrez-Navarro"
    )
    page.insert_textbox(pymupdf.Rect(LEFT, 320, RIGHT, 380),
                        authors_text,
                        fontsize=12, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_CENTER)

    page.insert_textbox(pymupdf.Rect(LEFT, 400, RIGHT, 440),
                        "Department of Computer Science, Stanford University\nStanford, CA 94305",
                        fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3),
                        align=pymupdf.TEXT_ALIGN_CENTER)

    abstract = (
        "Abstract: This survey provides a comprehensive overview of recent advances in natural language "
        "processing, covering neural network architectures, pre-trained language models, and their applications "
        "across diverse NLP tasks. We review the evolution from traditional word embeddings to large-scale "
        "transformer-based models, analyze key benchmarks and evaluation methodologies, and discuss emerging "
        "challenges including model interpretability, computational efficiency, and ethical considerations. "
        "Our analysis covers over 200 publications from 2013 to 2023, identifying major trends and future "
        "research directions in the field."
    )
    page.insert_textbox(pymupdf.Rect(LEFT, 480, RIGHT, 650),
                        abstract,
                        fontsize=10, fontname="tiit", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_textbox(pymupdf.Rect(LEFT, 670, RIGHT, 700),
                        "Keywords: natural language processing, transformers, pre-trained models, deep learning, survey",
                        fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2),
                        align=pymupdf.TEXT_ALIGN_LEFT)

    # ──────── Helper to add section pages ────────
    def add_section_page(title, body_paragraphs):
        p = doc.new_page(width=W, height=H)
        y = TOP
        p.insert_text(pymupdf.Point(LEFT, y + 16), title,
                      fontsize=16, fontname="hebo", color=(0, 0, 0))
        y += 36
        shape = p.new_shape()
        shape.draw_line(pymupdf.Point(LEFT, y), pymupdf.Point(RIGHT, y))
        shape.finish(color=(0, 0, 0), width=0.5)
        shape.commit()
        y += 12
        for para in body_paragraphs:
            rect = pymupdf.Rect(LEFT, y, RIGHT, BOT - 20)
            excess = p.insert_textbox(rect, para,
                                      fontsize=10, fontname="helv",
                                      color=(0, 0, 0),
                                      align=pymupdf.TEXT_ALIGN_JUSTIFY)
            # estimate how much vertical space was used
            lines_approx = max(1, len(para) // 75)
            y += lines_approx * 13 + 8
            if y > BOT - 40:
                break
        # page number
        p.insert_text(pymupdf.Point(W / 2 - 5, BOT + 15),
                      str(doc.page_count),
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))
        return p

    # ──────── Pages 2-11: Survey content ────────

    # Page 2: Introduction
    add_section_page("1. Introduction", [
        "Natural language processing (NLP) has experienced remarkable progress over the past decade, "
        "driven primarily by advances in deep learning and the availability of large-scale text corpora. "
        "The field has transitioned from rule-based and statistical methods to neural network approaches "
        "that learn rich representations directly from data, achieving unprecedented performance across "
        "a wide range of language understanding and generation tasks.",
        "The introduction of the transformer architecture by Vaswani et al. (2017) marked a paradigm "
        "shift, enabling models to capture long-range dependencies through self-attention mechanisms. "
        "Subsequent pre-trained language models such as BERT (Devlin et al., 2019), GPT-2 (Radford et al., "
        "2019), and their successors have established new state-of-the-art results on virtually every NLP "
        "benchmark, demonstrating that large-scale unsupervised pre-training followed by task-specific "
        "fine-tuning is a highly effective paradigm.",
        "This survey aims to provide a structured overview of these developments, categorizing methods by "
        "their architectural innovations, training objectives, and application domains. We cover word "
        "embeddings, recurrent neural networks, convolutional approaches, transformer-based models, and "
        "the latest large language models, offering both historical context and forward-looking analysis.",
    ])

    # Page 3: Word Embeddings
    add_section_page("2. Word Embeddings and Distributed Representations", [
        "The idea of representing words as dense vectors in a continuous space has been foundational to "
        "modern NLP. Early work by Mikolov et al. (2013) introduced Word2Vec, which learns word vectors "
        "by predicting context words (Skip-gram) or target words from context (CBOW). These embeddings "
        "capture semantic relationships, such that vector arithmetic reveals analogies (e.g., king - man + woman = queen).",
        "GloVe (Pennington et al., 2014) approached word representation learning from a different angle, "
        "factorizing the word co-occurrence matrix to produce vectors that encode both local and global "
        "statistical information. FastText (Bojanowski et al., 2017) extended these ideas by incorporating "
        "subword information, allowing the model to generate representations for out-of-vocabulary words "
        "by composing character n-gram vectors.",
        "Despite their success, static embeddings suffer from a fundamental limitation: each word receives "
        "a single representation regardless of context. The word 'bank' has the same vector whether it refers "
        "to a financial institution or a river bank. This motivated the development of contextualized "
        "representations, which we discuss in subsequent sections.",
    ])

    # Page 4: RNNs and Sequence Models
    add_section_page("3. Recurrent Neural Networks and Sequence Models", [
        "Recurrent neural networks (RNNs) process sequences one token at a time, maintaining a hidden state "
        "that theoretically captures information from all previous tokens. However, vanilla RNNs suffer from "
        "vanishing and exploding gradient problems, limiting their ability to model long-range dependencies.",
        "Long Short-Term Memory (LSTM) networks (Hochreiter & Schmidhuber, 1997) address this through gating "
        "mechanisms that control information flow. The Gated Recurrent Unit (GRU) (Cho et al., 2014) offers "
        "a simplified alternative with comparable performance. Bidirectional variants process sequences in "
        "both directions, capturing future context as well.",
        "The encoder-decoder framework (Sutskever et al., 2014) enabled sequence-to-sequence learning, with "
        "applications in machine translation, summarization, and dialogue systems. The addition of attention "
        "mechanisms (Bahdanau et al., 2015; Luong et al., 2015) allowed decoders to selectively focus on "
        "relevant encoder states, dramatically improving translation quality and interpretability.",
    ])

    # Page 5: CNNs for NLP
    add_section_page("4. Convolutional Approaches to NLP", [
        "Convolutional neural networks (CNNs), originally developed for computer vision, have been successfully "
        "adapted for text classification and other NLP tasks. Kim (2014) demonstrated that a simple CNN with "
        "one layer of convolution over word vectors achieves strong results on sentence classification benchmarks.",
        "Character-level CNNs (Zhang et al., 2015) operate directly on character sequences, avoiding the need "
        "for word-level tokenization and handling morphological variations naturally. Convolutional sequence-to-sequence "
        "models (Gehring et al., 2017) showed that CNNs can match or exceed RNN-based approaches for machine "
        "translation while offering significant computational advantages through parallelization.",
        "While transformers have largely supplanted CNNs in most NLP applications, convolutional components "
        "continue to play important roles in hybrid architectures and remain competitive for certain tasks "
        "where local feature detection is paramount.",
    ])

    # Page 6: Transformer Architecture
    add_section_page("5. The Transformer Architecture", [
        "The transformer architecture (Vaswani et al., 2017) revolutionized NLP by replacing recurrence with "
        "multi-head self-attention, enabling parallel computation across all positions in a sequence. The model "
        "consists of an encoder-decoder structure with residual connections and layer normalization.",
        "Self-attention computes a weighted sum of all input positions, where weights are determined by the "
        "compatibility between query and key vectors. Multi-head attention allows the model to jointly attend "
        "to information from different representation subspaces, capturing diverse patterns of dependency.",
        "Positional encoding, either sinusoidal or learned, provides the model with sequence order information "
        "that would otherwise be lost due to the permutation-invariant nature of attention. The transformer's "
        "ability to process sequences in parallel, combined with its capacity to model long-range dependencies, "
        "has made it the dominant architecture in modern NLP.",
    ])

    # Page 7: Pre-trained Language Models
    add_section_page("6. Pre-trained Language Models", [
        "The pre-train-then-fine-tune paradigm, popularized by ELMo (Peters et al., 2018) and scaled dramatically "
        "with BERT (Devlin et al., 2019), has become the standard approach in NLP. Pre-training on large unlabeled "
        "corpora enables models to learn general linguistic knowledge that transfers effectively to downstream tasks.",
        "BERT's masked language modeling (MLM) objective and next sentence prediction (NSP) task enable bidirectional "
        "representation learning. RoBERTa (Liu et al., 2019) showed that careful hyperparameter tuning and larger "
        "pre-training data significantly improve performance. ALBERT (Lan et al., 2020) reduced model size through "
        "factorized embedding parameterization and cross-layer parameter sharing.",
        "ELECTRA (Clark et al., 2020) introduced a novel replaced token detection objective that is more sample "
        "efficient than MLM. XLNet (Yang et al., 2019) combined autoregressive and bidirectional modeling through "
        "permutation language modeling. These diverse pre-training objectives reflect ongoing research into "
        "the most effective strategies for learning transferable representations.",
    ])

    # Page 8: Seq2Seq Pre-training
    add_section_page("7. Sequence-to-Sequence Pre-training and Generation", [
        "While BERT-style models excel at understanding tasks, sequence-to-sequence (seq2seq) pre-trained models "
        "address both understanding and generation. T5 (Raffel et al., 2020) frames all NLP tasks as text-to-text "
        "problems, achieving strong performance across classification, translation, and summarization.",
        "BART (Lewis et al., 2020) uses a denoising autoencoder objective with flexible corruption schemes, "
        "excelling at text generation tasks. UniLM (Dong et al., 2019) unifies different pre-training objectives "
        "within a single transformer architecture.",
        "Cross-lingual models such as XLM-R (Conneau et al., 2020) extend pre-training to multiple languages, "
        "enabling zero-shot cross-lingual transfer. These models demonstrate that a single model can serve as "
        "a universal foundation for diverse NLP tasks across languages, reducing the need for language-specific "
        "engineering and labeled data.",
    ])

    # Page 9: Efficient Transformers
    add_section_page("8. Efficient Transformer Architectures", [
        "Standard transformers have O(n^2) attention complexity, limiting their application to long documents. "
        "Several approaches address this limitation. Reformer (Kitaev et al., 2020) uses locality-sensitive "
        "hashing to reduce attention complexity to O(n log n).",
        "Longformer (Beltagy et al., 2020) combines local windowed attention with global attention on selected "
        "tokens, achieving linear complexity. BigBird (Zaheer et al., 2020) uses a combination of random, "
        "windowed, and global attention patterns. These efficient variants enable processing of documents "
        "with thousands or tens of thousands of tokens.",
        "DeBERTa (He et al., 2021) introduces disentangled attention that separately encodes content and "
        "position information, along with an enhanced mask decoder for pre-training. The model achieves "
        "strong results on the SuperGLUE benchmark while maintaining computational efficiency through "
        "careful architectural choices.",
    ])

    # Page 10: Large Language Models
    add_section_page("9. Large Language Models and In-Context Learning", [
        "The GPT series demonstrated that scaling language models yields emergent capabilities. GPT-3 (Brown "
        "et al., 2020) showed that sufficiently large models can perform tasks through in-context learning, "
        "using only natural language descriptions and a few examples provided in the prompt.",
        "PaLM (Chowdhery et al., 2023) and LLaMA (Touvron et al., 2023) pushed the boundaries of scale and "
        "efficiency, demonstrating strong performance across diverse benchmarks. The alignment of language "
        "models with human preferences through reinforcement learning from human feedback (RLHF) (Ouyang "
        "et al., 2022) has proven critical for making these models useful and safe.",
        "Chain-of-thought prompting (Wei et al., 2022) revealed that LLMs can perform complex reasoning "
        "when prompted to show intermediate steps. Zero-shot chain-of-thought (Kojima et al., 2022) and "
        "self-consistency (Wang et al., 2023) further improved reasoning capabilities without requiring "
        "task-specific demonstrations.",
    ])

    # Page 11: Challenges and Future Directions
    add_section_page("10. Challenges and Future Directions", [
        "Despite remarkable progress, several challenges remain in NLP. Model interpretability continues to "
        "be a significant concern, as transformer-based models operate as black boxes. Hallucination in "
        "large language models, where models generate plausible but factually incorrect text (Zhong et al., "
        "2023), poses risks for real-world deployment.",
        "Computational efficiency remains a critical issue. Training large language models requires enormous "
        "computational resources, raising concerns about environmental impact and accessibility. Research "
        "into model compression, knowledge distillation (Sanh et al., 2019), and efficient architectures "
        "aims to democratize access to powerful NLP capabilities.",
        "Evaluation methodology is another area requiring attention. Current benchmarks (Wang et al., 2018; "
        "Rajpurkar et al., 2016, 2018) may not adequately capture model capabilities and limitations. "
        "Developing comprehensive evaluation frameworks that assess robustness, fairness, and real-world "
        "utility remains an important direction for future research.",
        "Neural architecture search (Zoph & Le, 2017) and automated machine learning promise to further "
        "accelerate progress by discovering optimal model configurations. Transfer learning techniques "
        "(Howard & Ruder, 2018; Lample & Conneau, 2019; Sun et al., 2019) continue to evolve, enabling "
        "more effective knowledge sharing across tasks and domains.",
    ])

    # ──────── Pages 12-15: References ────────
    refs_per_page = [12, 12, 11, 10]  # total = 45
    ref_idx = 0
    for page_num_offset, count in enumerate(refs_per_page):
        p = doc.new_page(width=W, height=H)
        y = TOP
        if page_num_offset == 0:
            p.insert_text(pymupdf.Point(LEFT, y + 16), "References",
                          fontsize=16, fontname="hebo", color=(0, 0, 0))
            y += 36
            shape = p.new_shape()
            shape.draw_line(pymupdf.Point(LEFT, y), pymupdf.Point(RIGHT, y))
            shape.finish(color=(0, 0, 0), width=0.5)
            shape.commit()
            y += 12

        for i in range(count):
            if ref_idx >= len(REFERENCES):
                break
            ref_text = f"[{ref_idx + 1}] {REFERENCES[ref_idx]}"
            rect = pymupdf.Rect(LEFT, y, RIGHT, y + 55)
            p.insert_textbox(rect, ref_text,
                             fontsize=9, fontname="helv",
                             color=(0, 0, 0),
                             align=pymupdf.TEXT_ALIGN_LEFT)
            y += 50
            ref_idx += 1

        # page number
        p.insert_text(pymupdf.Point(W / 2 - 5, BOT + 15),
                      str(doc.page_count),
                      fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # ── Set TOC ──
    toc = [
        [1, "Abstract", 1],
        [1, "1. Introduction", 2],
        [1, "2. Word Embeddings and Distributed Representations", 3],
        [1, "3. Recurrent Neural Networks and Sequence Models", 4],
        [1, "4. Convolutional Approaches to NLP", 5],
        [1, "5. The Transformer Architecture", 6],
        [1, "6. Pre-trained Language Models", 7],
        [1, "7. Sequence-to-Sequence Pre-training and Generation", 8],
        [1, "8. Efficient Transformer Architectures", 9],
        [1, "9. Large Language Models and In-Context Learning", 10],
        [1, "10. Challenges and Future Directions", 11],
        [1, "References", 12],
    ]
    doc.set_toc(toc)

    # ── Metadata ──
    doc.set_metadata({
        "title": "A Comprehensive Survey of Natural Language Processing Methods and Recent Advances (2013-2023)",
        "author": "Elena Marchetti, Rajesh Krishnamurthy, Sarah O'Brien, Wei-Lin Zhang, Carlos Gutierrez-Navarro",
        "subject": "NLP Survey",
        "keywords": "NLP, transformers, BERT, GPT, deep learning, survey",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Launch Evince to open the PDF
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
