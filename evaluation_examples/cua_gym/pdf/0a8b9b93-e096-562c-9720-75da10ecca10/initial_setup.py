"""
Initial Setup: Create three thesis chapter PDF files for merging task
Task ID: pdf_res_006
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_006'
THESIS_DIR = f'{WORKDIR}/thesis'

# Page dimensions (A4)
A4_W, A4_H = 595, 842
MARGIN = 72
TEXT_W = A4_W - 2 * MARGIN


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


def add_text_page(doc, title, body_paragraphs, page_number):
    """Add a page with a title and body paragraphs."""
    page = doc.new_page(width=A4_W, height=A4_H)

    # Title
    page.insert_text(
        pymupdf.Point(MARGIN, MARGIN + 20),
        title,
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Underline below title
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN, MARGIN + 30), pymupdf.Point(A4_W - MARGIN, MARGIN + 30))
    shape.finish(color=(0.3, 0.3, 0.3), width=1)
    shape.commit()

    # Body text
    y_pos = MARGIN + 60
    rect = pymupdf.Rect(MARGIN, y_pos, A4_W - MARGIN, A4_H - MARGIN - 40)
    full_text = "\n\n".join(body_paragraphs)
    page.insert_textbox(
        rect,
        full_text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page number footer
    page.insert_text(
        pymupdf.Point(A4_W / 2 - 10, A4_H - MARGIN + 20),
        str(page_number),
        fontsize=10,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    return page


def create_intro_pdf():
    """Create chapter3_intro.pdf with 4 pages of introduction content."""
    doc = pymupdf.open()

    pages_content = [
        {
            "title": "Chapter 3: Introduction",
            "body": [
                "The rapid advancement of deep learning architectures has fundamentally transformed the landscape of natural language processing over the past decade. From the early successes of recurrent neural networks to the paradigm shift introduced by transformer-based models, the field has witnessed unprecedented improvements in machine comprehension and generation of human language.",
                "This chapter provides a comprehensive overview of the theoretical foundations and practical implications of large-scale language models in scientific text analysis. We examine the intersection of computational linguistics and domain-specific knowledge extraction, with particular emphasis on biomedical literature processing.",
                "The motivation for this research stems from the exponential growth of published scientific literature, which has made manual review and synthesis practically impossible for individual researchers. According to recent estimates from the National Library of Medicine, over 1.5 million new articles are indexed in PubMed annually, creating an urgent need for automated analysis tools.",
            ],
        },
        {
            "title": "3.1 Background and Motivation",
            "body": [
                "The challenge of processing large-scale scientific corpora has been recognized by the research community since the early 2000s. Initial approaches relied on keyword-based search and simple statistical methods, such as term frequency-inverse document frequency (TF-IDF), to identify relevant documents within vast repositories.",
                "However, these methods suffered from significant limitations including their inability to capture semantic relationships between concepts, their sensitivity to vocabulary variations, and their poor performance when dealing with domain-specific terminology that often carries meanings different from everyday language.",
                "The emergence of word embeddings, pioneered by Mikolov et al. in 2013 with the Word2Vec architecture, represented a crucial advancement. By mapping words into continuous vector spaces where semantic similarity corresponded to geometric proximity, these models enabled computational approaches to capture nuanced linguistic relationships for the first time.",
                "Subsequent developments including GloVe, FastText, and contextual embeddings from ELMo further refined these representations, laying the groundwork for the transformer revolution that would follow in 2017 with the publication of the seminal 'Attention Is All You Need' paper by Vaswani and colleagues.",
            ],
        },
        {
            "title": "3.1.2 Prior Work in Biomedical NLP",
            "body": [
                "The application of natural language processing to biomedical texts has a rich history predating the deep learning era. Early systems such as MetaMap, developed at the National Library of Medicine, utilized rule-based approaches combined with the Unified Medical Language System (UMLS) to extract medical concepts from clinical narratives.",
                "The introduction of BioBERT by Lee et al. in 2019 demonstrated that domain-specific pre-training could substantially improve performance on biomedical NLP benchmarks compared to general-purpose models. Trained on PubMed abstracts and PMC full-text articles, BioBERT achieved state-of-the-art results on named entity recognition, relation extraction, and question answering tasks.",
                "More recent work has explored the development of even larger domain-specific models. PubMedBERT, SciBERT, and BioGPT represent different points along the spectrum of model architectures and pre-training strategies, each offering distinct advantages for specific downstream applications.",
                "Despite these advances, significant challenges remain in accurately processing the complex multi-modal content found in modern scientific publications, including tables, figures, mathematical equations, and specialized notations that are poorly handled by text-only models.",
            ],
        },
        {
            "title": "3.1.3 Research Questions",
            "body": [
                "Building on the foundations established in the preceding sections, this thesis addresses three primary research questions that collectively aim to advance the state of automated scientific literature analysis:",
                "RQ1: How can transformer-based architectures be adapted to effectively process the heterogeneous structure of scientific documents, including sectional organization, citation networks, and cross-referencing patterns?",
                "RQ2: What pre-training strategies and data curation methods yield the most robust domain-specific language representations for biomedical text, as measured by downstream task performance across multiple benchmarks?",
                "RQ3: To what extent can automated systems achieve reliable extraction of quantitative findings and experimental parameters from published research, and what are the practical implications for systematic review workflows?",
                "These questions are addressed through a series of experiments detailed in the subsequent methods and results chapters, utilizing a novel dataset of 47,000 annotated biomedical articles spanning oncology, cardiology, and neuroscience domains.",
            ],
        },
    ]

    for i, pc in enumerate(pages_content):
        add_text_page(doc, pc["title"], pc["body"], i + 1)

    output = f'{THESIS_DIR}/chapter3_intro.pdf'
    doc.save(output)
    doc.close()
    print(f'Created: {output} ({4} pages)')


def create_methods_pdf():
    """Create chapter3_methods.pdf with 6 pages of methods content."""
    doc = pymupdf.open()

    pages_content = [
        {
            "title": "3.2 Methods",
            "body": [
                "This section describes the experimental methodology employed in our investigation of transformer-based scientific document processing. Our approach encompasses four key components: dataset construction and annotation, model architecture design, training procedures, and evaluation protocols.",
                "All experiments were conducted on a computing cluster equipped with eight NVIDIA A100 GPUs (80GB VRAM each), running Ubuntu 22.04 LTS with CUDA 12.1 and PyTorch 2.1. Training was managed using the Hugging Face Transformers library version 4.35, with DeepSpeed ZeRO Stage 3 for memory-efficient distributed training.",
                "Statistical analyses were performed using R version 4.3.1 and Python's SciPy library. Significance testing employed two-tailed paired t-tests with Bonferroni correction for multiple comparisons, with alpha set at 0.05.",
            ],
        },
        {
            "title": "3.2.1 Dataset Construction",
            "body": [
                "The primary dataset, designated BioSciCorpus-47K, was assembled from three sources: PubMed Central Open Access subset (32,500 articles), bioRxiv preprints (9,800 articles), and manually curated clinical trial reports from ClinicalTrials.gov (4,700 documents).",
                "Document selection criteria required: (a) publication date between January 2018 and December 2023, (b) availability of full text in structured XML or HTML format, (c) presence of at least one quantitative results table, and (d) classification within the target medical domains of oncology (ICD-10: C00-D49), cardiology (I00-I99), or neuroscience (G00-G99).",
                "Annotation was performed by a team of twelve trained annotators, comprising four PhD candidates in biomedical informatics and eight research assistants with backgrounds in biology or medicine. The annotation schema included 23 entity types and 15 relation types, designed in consultation with domain experts and validated through two rounds of pilot annotation.",
                "Inter-annotator agreement was measured using Cohen's kappa coefficient, achieving kappa = 0.83 for entity recognition and kappa = 0.76 for relation extraction, indicating substantial agreement. Disagreements were resolved through adjudication by senior annotators with domain expertise.",
            ],
        },
        {
            "title": "3.2.2 Model Architecture",
            "body": [
                "Our proposed architecture, SciDocTransformer (SDT), extends the standard transformer encoder with three modifications tailored to scientific document processing: hierarchical position encoding, section-aware attention masks, and citation context integration.",
                "The hierarchical position encoding scheme replaces the conventional sinusoidal or learned position embeddings with a two-level system that captures both token-level position within a sentence and sentence-level position within a section. This enables the model to distinguish between tokens that occupy similar positions in different structural contexts.",
                "The section-aware attention mechanism introduces learnable section embeddings that are added to the key and query projections in the self-attention layers. Each section type (abstract, introduction, methods, results, discussion, references) receives a unique embedding, allowing the model to modulate attention patterns based on document structure.",
                "Citation context integration is achieved through a cross-attention module that attends to representations of cited documents when available. This module operates at the sentence level, with each sentence containing a citation receiving additional context from the referenced paper's abstract representation.",
            ],
        },
        {
            "title": "3.2.3 Training Procedure",
            "body": [
                "Model training followed a two-phase approach: domain-adaptive pre-training followed by task-specific fine-tuning. This strategy has been shown to be more effective than direct fine-tuning from general-purpose checkpoints.",
                "Phase 1 (Domain-Adaptive Pre-training): Starting from the RoBERTa-large checkpoint (355M parameters), we performed masked language modeling on the BioSciCorpus-47K for 200,000 steps with a batch size of 256 sequences (each 512 tokens). The learning rate followed a linear warmup over 10,000 steps to a peak of 2e-5, followed by cosine decay. Masking probability was set to 15% with whole-word masking enabled.",
                "Phase 2 (Task-Specific Fine-tuning): For each downstream task, the pre-trained model was fine-tuned for 50 epochs with early stopping (patience of 5 epochs based on validation F1 score). Task-specific hyperparameters were optimized using Optuna with 100 trials per task. Key hyperparameter ranges included: learning rate [1e-6, 5e-5], batch size {16, 32, 64}, and dropout rate [0.1, 0.3].",
                "Data augmentation during fine-tuning included: (a) back-translation using MarianMT models for 20% of training examples, (b) entity-preserving synonym replacement using UMLS, and (c) random section shuffling to improve robustness to non-standard document structures.",
            ],
        },
        {
            "title": "3.2.4 Evaluation Protocol",
            "body": [
                "Model performance was evaluated across five benchmark tasks designed to assess different aspects of scientific document understanding: named entity recognition (NER), relation extraction (RE), document classification, summarization, and quantitative data extraction.",
                "For NER, we used the standard BIO tagging scheme and reported entity-level F1 scores following the CoNLL evaluation script. Evaluation was performed on four established biomedical NER datasets: BC5CDR (chemical and disease entities), JNLPBA (gene and protein entities), NCBI-disease (disease entities), and our newly created BioSciNER-2K subset.",
                "Relation extraction was evaluated using the ChemProt dataset, BioRED, and a custom evaluation set of 2,000 annotated abstracts from BioSciCorpus-47K. Micro-averaged precision, recall, and F1 scores were reported.",
                "Document classification experiments used the HoC (Hallmarks of Cancer) dataset and a three-way classification task on BioSciCorpus-47K articles by medical subdomain. Performance was measured using macro-averaged F1 and Matthews Correlation Coefficient (MCC).",
                "All reported results represent the mean and standard deviation across five random seeds (42, 123, 256, 512, 1024) to account for training stochasticity.",
            ],
        },
        {
            "title": "3.2.5 Baseline Comparisons",
            "body": [
                "To contextualize the performance of SciDocTransformer, we compared against six established baselines spanning different model families and training paradigms:",
                "BERT-base and BERT-large: General-purpose transformer models pre-trained on BookCorpus and English Wikipedia. These represent the standard baseline for transfer learning in NLP.",
                "BioBERT v1.1: Pre-trained on PubMed abstracts and PMC full-text articles, starting from BERT-base. This model is the most widely adopted domain-specific baseline in biomedical NLP.",
                "PubMedBERT: Pre-trained from scratch exclusively on PubMed abstracts, using a vocabulary derived from the biomedical domain. Unlike BioBERT, this model does not initialize from general-domain weights.",
                "SciBERT: Pre-trained on a multi-domain scientific corpus from Semantic Scholar, covering computer science and biomedical papers. This model tests the benefit of broader scientific pre-training.",
                "GPT-4 (few-shot): The latest commercial large language model from OpenAI, evaluated in 5-shot prompting mode. This baseline assesses the capability of general-purpose generative models on our tasks without task-specific training.",
                "Each baseline was fine-tuned using the same hyperparameter search protocol as SciDocTransformer to ensure fair comparison.",
            ],
        },
    ]

    for i, pc in enumerate(pages_content):
        add_text_page(doc, pc["title"], pc["body"], i + 5)

    output = f'{THESIS_DIR}/chapter3_methods.pdf'
    doc.save(output)
    doc.close()
    print(f'Created: {output} ({6} pages)')


def create_results_pdf():
    """Create chapter3_results.pdf with 5 pages of results content."""
    doc = pymupdf.open()

    pages_content = [
        {
            "title": "3.3 Results",
            "body": [
                "This section presents the experimental results obtained from our evaluation of SciDocTransformer across the five benchmark tasks described in the methods section. We first report aggregate performance metrics, followed by detailed analyses of individual tasks, ablation studies, and qualitative error analysis.",
                "Overall, SciDocTransformer achieved state-of-the-art performance on four of the five evaluation tasks, with improvements ranging from 1.2 to 4.7 F1 points over the strongest baseline. The most substantial gains were observed on tasks requiring cross-section reasoning and citation-aware context integration.",
                "Table 3.1 presents the aggregate performance comparison across all models and tasks. Statistical significance was established using paired bootstrap resampling with 10,000 iterations.",
            ],
        },
        {
            "title": "3.3.1 Named Entity Recognition Results",
            "body": [
                "On the four NER benchmarks, SciDocTransformer achieved an average F1 score of 91.3, compared to 89.6 for PubMedBERT (the strongest baseline) and 87.2 for BioBERT. The improvement was statistically significant on three of four datasets (p < 0.01).",
                "Performance on BC5CDR was particularly strong, with F1 scores of 94.1 for chemical entities and 90.8 for disease entities. This represents a 2.3-point improvement over PubMedBERT on disease entities, likely attributable to the hierarchical position encoding capturing contextual patterns specific to disease mentions in results sections.",
                "The JNLPBA dataset proved most challenging, with all models achieving lower F1 scores due to the high ambiguity of gene and protein entity boundaries. SciDocTransformer scored 82.7 F1, only marginally above PubMedBERT's 82.1, suggesting that our architectural modifications provide limited benefit for this particular entity type.",
                "Notably, GPT-4 in the 5-shot setting achieved competitive NER performance (85.4 average F1) despite not being specifically fine-tuned, demonstrating the emerging capability of large generative models for structured extraction tasks.",
            ],
        },
        {
            "title": "3.3.2 Relation Extraction Results",
            "body": [
                "Relation extraction experiments revealed the most substantial performance differences between SciDocTransformer and baseline models. On the ChemProt dataset, SDT achieved 79.8 micro-F1, surpassing PubMedBERT by 4.7 points and BioBERT by 6.2 points.",
                "Analysis of per-relation-type performance showed that SDT particularly excelled at identifying inhibitor (CPR:4) and substrate (CPR:6) relations, which often require understanding context spanning multiple sentences. The section-aware attention mechanism contributed most to this improvement, as confirmed by our ablation study (Section 3.4.1).",
                "On BioRED, which includes novel relation types not present in training data, SDT achieved 72.3 micro-F1 compared to 69.1 for PubMedBERT. This improvement in cross-relation generalization suggests that the citation context integration module helps the model acquire more transferable relational representations.",
                "Error analysis revealed that the most common failure mode across all models was the misclassification of indirect regulatory relationships as direct physical interactions. This confusion accounted for approximately 34% of all false positives in the ChemProt evaluation.",
            ],
        },
        {
            "title": "3.3.3 Document Classification and Summarization",
            "body": [
                "Document classification results on the Hallmarks of Cancer (HoC) dataset showed SDT achieving 88.9 macro-F1, a 1.8-point improvement over SciBERT (87.1) which was the strongest baseline for this task. The Matthews Correlation Coefficient was 0.872 for SDT versus 0.854 for SciBERT.",
                "The three-way subdomain classification task on BioSciCorpus-47K was performed with high accuracy by all transformer models, with SDT achieving 96.2% accuracy and 95.8 macro-F1. The most common misclassification was between cardiology and neuroscience articles discussing cerebrovascular conditions, which share substantial medical vocabulary.",
                "Summarization was evaluated using ROUGE-1, ROUGE-2, and ROUGE-L metrics on a held-out set of 500 articles from BioSciCorpus-47K. SDT achieved ROUGE-1/2/L scores of 49.3/21.7/44.8, representing modest improvements of 0.8/0.4/0.6 points over PubMedBERT. Human evaluation of 100 randomly sampled summaries showed that SDT-generated summaries were preferred by domain experts in 62% of pairwise comparisons against the strongest baseline.",
                "The quantitative data extraction task, which required models to identify and normalize experimental measurements from results sections, showed SDT achieving 76.4 F1, a 3.1-point improvement over PubMedBERT. This task particularly benefited from the hierarchical position encoding, which helped the model distinguish between measurements reported in different experimental contexts.",
            ],
        },
        {
            "title": "3.3.4 Ablation Study and Analysis",
            "body": [
                "To understand the individual contributions of each architectural modification, we conducted a systematic ablation study removing one component at a time from the full SciDocTransformer model. Results are averaged across all five evaluation tasks.",
                "Removing the hierarchical position encoding reduced average F1 by 1.8 points, with the largest impact on document classification (-2.4) and quantitative data extraction (-2.9). This confirms that structural position information is particularly valuable for tasks requiring document-level understanding.",
                "Ablating the section-aware attention masks resulted in a 2.1-point F1 decrease overall, with relation extraction suffering the most (-3.8 points). This finding validates our hypothesis that section context significantly modulates the interpretation of entity relationships in scientific text.",
                "Removing the citation context integration module had a comparatively smaller impact (-0.9 average F1), but showed notable effects on relation extraction (-1.7) and summarization (-1.4). The limited impact on NER (-0.3) suggests that citation context primarily benefits higher-level semantic tasks.",
                "Combining all three ablations (equivalent to standard RoBERTa-large with domain-adaptive pre-training only) resulted in a 3.6-point average F1 reduction, confirming that the architectural modifications provide complementary benefits. The compound effect being less than the sum of individual ablations (4.8 points) indicates some functional overlap between components.",
            ],
        },
    ]

    for i, pc in enumerate(pages_content):
        add_text_page(doc, pc["title"], pc["body"], i + 11)

    output = f'{THESIS_DIR}/chapter3_results.pdf'
    doc.save(output)
    doc.close()
    print(f'Created: {output} ({5} pages)')


def create_initial():
    os.makedirs(THESIS_DIR, exist_ok=True)

    create_intro_pdf()
    create_methods_pdf()
    create_results_pdf()

    print(f'All initial files created in {THESIS_DIR}')

    # Open the first file in Evince for GUI readiness
    launch_gui(f'evince "{THESIS_DIR}/chapter3_intro.pdf"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
