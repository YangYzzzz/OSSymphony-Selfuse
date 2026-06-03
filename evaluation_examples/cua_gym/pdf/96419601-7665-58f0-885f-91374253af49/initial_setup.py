"""
Initial Setup: Create a 22-page academic research paper PDF with metadata.
Task ID: pdf_ro_010
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_010'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/research_paper.pdf'


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


# --- Academic paper content (realistic) ---
TITLE = "Machine Learning in Healthcare"
AUTHOR = "Dr. Sarah Thompson"

ABSTRACT = (
    "The integration of machine learning (ML) techniques into healthcare has shown remarkable "
    "promise in improving patient outcomes, optimizing clinical workflows, and enabling early "
    "disease detection. This paper provides a comprehensive review of the current state of ML "
    "applications across multiple healthcare domains, including medical imaging, electronic health "
    "records (EHR) analysis, drug discovery, and genomics. We examine both supervised and "
    "unsupervised learning paradigms and their applicability to various clinical scenarios. "
    "Our analysis of 157 peer-reviewed studies published between 2018 and 2025 reveals significant "
    "improvements in diagnostic accuracy, particularly in radiology and pathology. We also discuss "
    "the challenges of model interpretability, data privacy, regulatory compliance, and the ethical "
    "implications of automated decision-making in clinical settings. Finally, we propose a framework "
    "for responsible deployment of ML systems in healthcare that balances innovation with patient safety."
)

SECTIONS = {
    "1. Introduction": [
        "Healthcare systems worldwide face unprecedented challenges driven by aging populations, "
        "rising costs, and increasing complexity of medical decision-making. The volume of clinical "
        "data generated daily has grown exponentially, with estimates suggesting that the healthcare "
        "industry produces approximately 30% of the world's data volume. Traditional analytical "
        "approaches are insufficient to extract meaningful patterns from this vast and heterogeneous "
        "data landscape.",

        "Machine learning, a subset of artificial intelligence (AI), offers powerful tools for "
        "discovering hidden patterns in large datasets. Unlike rule-based systems that require "
        "explicit programming of decision criteria, ML algorithms learn from data to make predictions "
        "or classifications. This capability is particularly valuable in healthcare, where the "
        "relationships between variables are often complex, nonlinear, and not well understood.",

        "The adoption of ML in healthcare has accelerated significantly since 2018, driven by "
        "advances in deep learning architectures, the availability of large-scale medical datasets, "
        "and increasing computational power through GPU and TPU clusters. Regulatory agencies, "
        "including the U.S. Food and Drug Administration (FDA), have approved over 520 AI/ML-enabled "
        "medical devices as of 2024, signaling growing confidence in these technologies.",

        "This review aims to provide a comprehensive assessment of the current landscape of ML in "
        "healthcare, examining both the technical foundations and clinical applications. We analyze "
        "the strengths and limitations of different ML approaches across key healthcare domains and "
        "identify the critical success factors for translating research innovations into clinical practice.",
    ],
    "2. Background and Related Work": [
        "The application of computational methods to healthcare data has a history spanning several "
        "decades. Early expert systems in the 1970s and 1980s, such as MYCIN for bacterial infection "
        "diagnosis, demonstrated the potential of rule-based reasoning in clinical contexts. However, "
        "these systems were limited by their dependence on manually curated knowledge bases and their "
        "inability to handle uncertainty effectively.",

        "The emergence of statistical learning methods in the 1990s marked a significant shift toward "
        "data-driven approaches. Bayesian networks, support vector machines, and random forests were "
        "applied to various clinical prediction tasks with moderate success. Chen et al. (2017) "
        "demonstrated that gradient-boosted decision trees could predict hospital readmissions with "
        "an AUC of 0.78, outperforming traditional logistic regression models.",

        "The deep learning revolution, catalyzed by Krizhevsky et al.'s ImageNet breakthrough in 2012, "
        "transformed the landscape of medical image analysis. Convolutional neural networks (CNNs) "
        "achieved radiologist-level performance in detecting diabetic retinopathy (Gulshan et al., 2016), "
        "skin cancer (Esteva et al., 2017), and pneumonia from chest X-rays (Rajpurkar et al., 2017). "
        "These results generated enormous enthusiasm for AI in healthcare.",

        "Recent advances in transformer architectures and foundation models have further expanded the "
        "possibilities. Large language models (LLMs) trained on biomedical corpora have shown impressive "
        "capabilities in clinical note summarization, medical question answering, and even generating "
        "differential diagnoses. Med-PaLM 2 achieved expert-level performance on USMLE-style questions, "
        "scoring 86.5% on the MedQA benchmark.",
    ],
    "3. Methodology": [
        "Our systematic review followed the PRISMA guidelines for reporting systematic reviews. We "
        "conducted a comprehensive literature search across PubMed, IEEE Xplore, Google Scholar, and "
        "the Cochrane Library for publications between January 2018 and October 2025. Search terms "
        "included combinations of 'machine learning,' 'deep learning,' 'artificial intelligence,' "
        "'healthcare,' 'clinical,' 'medical,' and domain-specific terms.",

        "Inclusion criteria required that studies: (1) applied ML techniques to healthcare data, "
        "(2) reported quantitative evaluation metrics, (3) used clinical or clinically-relevant datasets, "
        "and (4) were published in peer-reviewed venues. We excluded purely theoretical papers, "
        "editorials, and studies with sample sizes below 100 for supervised learning tasks.",

        "From an initial pool of 2,847 papers, we identified 157 studies meeting all inclusion criteria "
        "after title/abstract screening and full-text review. Two independent reviewers assessed each "
        "paper using a standardized extraction form capturing: ML algorithm type, dataset characteristics, "
        "evaluation metrics, clinical domain, sample size, and reported performance.",

        "We categorized studies into six primary domains: medical imaging (n=52), EHR analysis (n=34), "
        "drug discovery (n=23), genomics and precision medicine (n=21), natural language processing for "
        "clinical text (n=15), and wearable/sensor data analysis (n=12). Each domain was analyzed "
        "independently for trends in methodology, performance, and clinical impact.",
    ],
    "4. Medical Imaging Applications": [
        "Medical imaging represents the most mature domain for ML applications in healthcare, accounting "
        "for over 75% of FDA-approved AI/ML medical devices. Deep learning models, particularly CNNs and "
        "their variants, have demonstrated remarkable capabilities across multiple imaging modalities.",

        "In radiology, Wang et al. (2023) developed a multi-task CNN that simultaneously detects 14 "
        "thoracic pathologies from chest X-rays with a mean AUC of 0.924. The model was validated on "
        "an external dataset of 48,000 images from three hospitals, demonstrating robust generalization. "
        "Similarly, McKinney et al. (2020) showed that an AI system for breast cancer screening reduced "
        "false positives by 5.7% and false negatives by 9.4% compared to expert radiologists.",

        "Pathology has seen significant advances through whole-slide image analysis. Lu et al. (2021) "
        "introduced CLAM, a weakly supervised framework for computational pathology that achieves "
        "state-of-the-art results on renal cell carcinoma subtyping (AUC 0.987) and non-small cell "
        "lung cancer subtyping (AUC 0.963) without requiring pixel-level annotations.",

        "Ophthalmology has been an early adopter of AI imaging tools. The IDx-DR system became the "
        "first FDA-authorized AI diagnostic device in 2018, capable of detecting more-than-mild "
        "diabetic retinopathy with a sensitivity of 87.2% and specificity of 90.7%. Subsequent "
        "studies have expanded AI capabilities to detect glaucoma, age-related macular degeneration, "
        "and retinal vein occlusion from fundus photographs.",

        "Despite these achievements, challenges remain in medical imaging AI. Dataset bias, limited "
        "generalization across scanners and patient populations, and the 'black box' nature of deep "
        "learning models continue to be significant concerns. Shortcut learning, where models rely "
        "on spurious correlations rather than clinically meaningful features, has been documented in "
        "multiple studies and may undermine the reliability of AI imaging tools in real-world settings.",
    ],
    "5. Electronic Health Record Analysis": [
        "Electronic health records contain rich longitudinal patient data including diagnoses, "
        "medications, laboratory values, vital signs, and clinical notes. ML models trained on EHR "
        "data have shown promise for clinical prediction, risk stratification, and treatment optimization.",

        "Rajkomar et al. (2018) demonstrated that deep learning models applied to de-identified EHR "
        "data from 216,221 hospitalizations could predict in-hospital mortality with an AUC of 0.95, "
        "30-day unplanned readmission with an AUC of 0.77, and prolonged length of stay with an AUC "
        "of 0.86. The models outperformed traditional early warning scores across all prediction tasks.",

        "More recently, temporal deep learning architectures have improved prediction of clinical "
        "deterioration. Li et al. (2023) proposed a temporal attention network that processes irregular "
        "time-series EHR data and achieves an AUC of 0.89 for sepsis onset prediction with a 6-hour "
        "lead time, outperforming the qSOFA score (AUC 0.71) and MEWS (AUC 0.73).",

        "Natural language processing of clinical notes has emerged as a critical complement to "
        "structured EHR analysis. Transformer-based models fine-tuned on clinical text can extract "
        "social determinants of health, adverse drug events, and disease progression markers that "
        "are often recorded only in free-text notes. ClinicalBERT and BioBERT have become foundational "
        "models for this domain.",

        "Key challenges in EHR-based ML include missing data, class imbalance (rare events like "
        "cardiac arrest), temporal distribution shift as clinical practices evolve, and interoperability "
        "issues across different EHR vendors. Federated learning approaches have been proposed to "
        "enable multi-institutional model training while preserving patient privacy.",
    ],
    "6. Drug Discovery and Development": [
        "The pharmaceutical industry has increasingly adopted ML to accelerate drug discovery pipelines "
        "and reduce the estimated $2.6 billion cost and 12-year timeline for bringing a new drug to "
        "market. ML applications span the entire drug development lifecycle, from target identification "
        "to clinical trial optimization.",

        "Virtual screening using graph neural networks (GNNs) has shown particular promise. Stokes et "
        "al. (2020) used a directed message-passing neural network to screen 107 million molecules and "
        "identified halicin, a novel antibiotic effective against pan-resistant Acinetobacter baumannii "
        "infections. This was one of the first examples of ML-driven de novo antibiotic discovery.",

        "Generative models for molecular design have evolved rapidly. Variational autoencoders (VAEs) "
        "and generative adversarial networks (GANs) can propose novel molecular structures with desired "
        "pharmacological properties. Zhavoronkov et al. (2019) demonstrated that a generative model "
        "could design a novel DDR1 kinase inhibitor in 21 days, compared to the typical years-long "
        "medicinal chemistry optimization process.",

        "AlphaFold2's breakthrough in protein structure prediction in 2020 has had transformative "
        "implications for structure-based drug design. The ability to accurately predict protein "
        "folding enables more precise identification of drug binding sites and prediction of drug-protein "
        "interactions. The AlphaFold Protein Structure Database now contains predicted structures for "
        "over 200 million proteins.",
    ],
    "7. Genomics and Precision Medicine": [
        "ML techniques have become indispensable tools in genomics, enabling the analysis of complex "
        "genetic data at scale. Applications range from variant calling and genome annotation to "
        "polygenic risk scoring and pharmacogenomics.",

        "DeepVariant (Poplin et al., 2018), a CNN-based variant caller, transforms the variant calling "
        "problem into an image classification task and achieves higher accuracy than traditional "
        "statistical methods like GATK HaplotypeCaller. The approach has been extended to handle "
        "long-read sequencing data from Oxford Nanopore and PacBio platforms.",

        "Polygenic risk scores (PRS) constructed using ML methods have improved prediction of complex "
        "diseases. Khera et al. (2018) developed genome-wide PRS for coronary artery disease, atrial "
        "fibrillation, type 2 diabetes, inflammatory bowel disease, and breast cancer. Individuals in "
        "the top percentile of PRS for coronary artery disease had a 4.8-fold increased risk compared "
        "to the general population.",

        "Single-cell RNA sequencing (scRNA-seq) generates high-dimensional data that is ideally suited "
        "for ML analysis. Deep learning methods for cell type annotation, trajectory inference, and "
        "gene regulatory network reconstruction have become standard tools in single-cell genomics. "
        "scBERT and scGPT represent the emerging class of foundation models trained on large-scale "
        "single-cell data.",
    ],
    "8. Wearable Devices and Remote Monitoring": [
        "The proliferation of consumer wearable devices and medical-grade sensors has created new "
        "opportunities for continuous health monitoring using ML. Smartwatches, fitness trackers, and "
        "medical patches generate streams of physiological data that can be analyzed for early "
        "detection of health anomalies.",

        "The Apple Heart Study enrolled over 400,000 participants and demonstrated that a deep learning "
        "algorithm for atrial fibrillation detection from photoplethysmography (PPG) signals achieved "
        "a positive predictive value of 84%. Subsequent studies have expanded wearable-based detection "
        "to include sleep apnea, fall detection, and glucose level estimation.",

        "Remote patient monitoring (RPM) systems powered by ML can analyze data from multiple sensors "
        "to predict clinical deterioration in home settings. The COVID-19 pandemic accelerated adoption "
        "of RPM, with several studies showing that ML-based analysis of pulse oximetry, heart rate, "
        "and respiratory rate data could identify patients at risk of clinical worsening 24-48 hours "
        "before symptom deterioration.",
    ],
    "9. Challenges and Limitations": [
        "Despite significant progress, several fundamental challenges must be addressed before ML can "
        "be widely deployed in clinical practice. These challenges span technical, regulatory, ethical, "
        "and practical dimensions.",

        "Data quality and bias remain critical concerns. ML models trained on data from specific "
        "institutions or populations may not generalize well to different settings. Obermeyer et al. "
        "(2019) demonstrated that a widely used commercial algorithm for healthcare resource allocation "
        "exhibited significant racial bias, systematically underestimating the health needs of Black "
        "patients. This finding highlighted the urgent need for fairness-aware ML in healthcare.",

        "Model interpretability is essential for clinical adoption. Clinicians need to understand why "
        "a model makes a particular prediction to integrate AI recommendations into their decision-making "
        "workflow. While attention mechanisms and gradient-based attribution methods provide some insights, "
        "the interpretability of complex deep learning models remains an active research challenge.",

        "Regulatory frameworks are still evolving. The FDA's proposed regulatory framework for AI/ML-based "
        "software as a medical device (SaMD) introduces concepts like 'predetermined change control plans' "
        "to accommodate the iterative nature of ML model updates. However, questions about liability, "
        "transparency, and post-market surveillance remain largely unresolved.",

        "Implementation challenges are often underestimated. Integrating ML systems into clinical workflows "
        "requires significant infrastructure investment, change management, and ongoing monitoring. Studies "
        "have shown that even well-validated models can fail in deployment due to distribution shift, "
        "workflow friction, and alert fatigue among clinicians.",
    ],
    "10. Ethical Considerations": [
        "The deployment of ML in healthcare raises profound ethical questions. Informed consent for the "
        "use of patient data in ML model training must be balanced against the potential benefits of "
        "data-driven healthcare improvements. The General Data Protection Regulation (GDPR) and similar "
        "laws impose strict requirements on data processing, but the boundaries of acceptable use for "
        "AI training remain contested.",

        "Algorithmic transparency and accountability are particularly important in healthcare, where "
        "decisions can have life-or-death consequences. The 'right to explanation' enshrined in some "
        "regulatory frameworks requires that patients and clinicians can understand the basis for "
        "automated recommendations. This creates tension with the use of complex deep learning models "
        "whose decision processes are inherently difficult to explain.",

        "The potential for ML to exacerbate health disparities is a serious concern. If training data "
        "disproportionately represents certain demographic groups, the resulting models may perform "
        "poorly for underrepresented populations. Proactive measures, including diverse dataset curation, "
        "subgroup performance evaluation, and continuous monitoring for bias, are essential.",
    ],
    "11. Proposed Framework for Responsible ML Deployment": [
        "Based on our analysis of the literature and documented deployment experiences, we propose a "
        "comprehensive framework for responsible ML deployment in healthcare. The framework consists "
        "of five pillars: clinical validation, technical robustness, ethical oversight, regulatory "
        "compliance, and continuous monitoring.",

        "Clinical validation extends beyond traditional accuracy metrics. We recommend prospective "
        "clinical trials comparing ML-assisted decision-making with standard care, assessment of "
        "clinical workflow integration, and evaluation of patient outcomes rather than intermediate "
        "technical metrics alone. The SPIRIT-AI and CONSORT-AI guidelines provide a foundation for "
        "reporting AI clinical trials.",

        "Technical robustness encompasses dataset documentation (datasheets for datasets), model "
        "cards describing performance characteristics and known limitations, regular stress testing "
        "against adversarial inputs and distribution shifts, and formal verification where feasible. "
        "Organizations should maintain ML registries that track model versions, training data, and "
        "performance metrics over time.",

        "Ethical oversight should be embedded throughout the ML lifecycle. We recommend establishing "
        "AI ethics committees that include clinicians, patients, ethicists, and data scientists. "
        "Regular audits for bias and fairness should be mandated, with clear processes for addressing "
        "identified disparities.",
    ],
    "12. Future Directions": [
        "Several emerging trends are likely to shape the future of ML in healthcare. Multimodal "
        "learning, which integrates diverse data types (imaging, genomics, EHR, wearables), promises "
        "more holistic patient assessment. Recent work by Acosta et al. (2022) demonstrated that "
        "multimodal models combining radiology images with clinical notes improved diagnostic accuracy "
        "by 12% compared to unimodal approaches.",

        "Foundation models for healthcare represent a paradigm shift from task-specific models to "
        "general-purpose medical AI. Models like GatorTron, trained on over 90 billion words of clinical "
        "text, and BiomedCLIP, trained on 15 million figure-caption pairs from biomedical papers, are "
        "enabling few-shot and zero-shot learning for diverse clinical tasks.",

        "Federated learning and privacy-preserving ML techniques will address the critical barrier of "
        "data fragmentation across healthcare institutions. The MELLODDY project demonstrated that "
        "federated learning across 10 pharmaceutical companies improved predictive models for drug "
        "discovery without sharing proprietary data.",

        "Causal ML methods that go beyond prediction to enable causal inference from observational "
        "data will be increasingly important for treatment effect estimation and clinical decision "
        "support. Recent advances in counterfactual reasoning and instrumental variable approaches "
        "show promise for addressing confounding in retrospective clinical data.",
    ],
    "13. Conclusion": [
        "Machine learning has emerged as a transformative force in healthcare, with demonstrated "
        "impact across medical imaging, clinical prediction, drug discovery, and genomics. Our "
        "systematic review of 157 studies reveals consistent improvements in diagnostic accuracy "
        "and clinical efficiency when ML tools are properly developed and validated.",

        "However, the path from research prototype to clinical deployment remains challenging. "
        "Technical hurdles including data quality, model generalization, and interpretability must "
        "be addressed alongside ethical concerns about bias, transparency, and patient autonomy. "
        "Regulatory frameworks must evolve to keep pace with rapid technological advancement while "
        "maintaining rigorous safety standards.",

        "We believe that the responsible deployment framework proposed in this paper provides a "
        "structured approach to realizing the benefits of ML in healthcare while mitigating risks. "
        "By prioritizing clinical validation, technical robustness, ethical oversight, and continuous "
        "monitoring, healthcare organizations can navigate the complex landscape of medical AI with "
        "confidence.",

        "The future of healthcare will be shaped by the thoughtful integration of human expertise "
        "and machine intelligence. As ML models become more capable and our understanding of their "
        "limitations deepens, we are moving toward a healthcare system that is more accurate, more "
        "efficient, and more equitable. The journey is just beginning, and the potential for "
        "transformative impact on human health has never been greater.",
    ],
}

REFERENCES = [
    "Acosta, J. N., et al. (2022). Multimodal biomedical AI. Nature Medicine, 28, 1773-1784.",
    "Chen, T., et al. (2017). Hospital readmission prediction using gradient-boosted trees. BMC Medical Informatics and Decision Making, 17(1), 88.",
    "Esteva, A., et al. (2017). Dermatologist-level classification of skin cancer. Nature, 542, 115-118.",
    "Gulshan, V., et al. (2016). Development and validation of a deep learning algorithm for detection of diabetic retinopathy. JAMA, 316(22), 2402-2410.",
    "Khera, A. V., et al. (2018). Genome-wide polygenic scores for common diseases. Nature Genetics, 50, 1219-1224.",
    "Krizhevsky, A., et al. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.",
    "Li, Q., et al. (2023). Temporal attention networks for sepsis prediction from irregular EHR time-series. Journal of Biomedical Informatics, 138, 104281.",
    "Lu, M. Y., et al. (2021). Data-efficient and weakly supervised computational pathology. Nature Biomedical Engineering, 5, 555-570.",
    "McKinney, S. M., et al. (2020). International evaluation of an AI system for breast cancer screening. Nature, 577, 89-94.",
    "Obermeyer, Z., et al. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. Science, 366(6464), 447-453.",
    "Poplin, R., et al. (2018). A universal SNP and small-indel variant caller using deep neural networks. Nature Biotechnology, 36, 983-987.",
    "Rajkomar, A., et al. (2018). Scalable and accurate deep learning with electronic health records. npj Digital Medicine, 1, 18.",
    "Rajpurkar, P., et al. (2017). CheXNet: Radiologist-level pneumonia detection on chest X-rays. arXiv:1711.05225.",
    "Stokes, J. M., et al. (2020). A deep learning approach to antibiotic discovery. Cell, 180(4), 688-702.",
    "Wang, X., et al. (2023). Multi-task thoracic disease classification from chest X-rays. IEEE Transactions on Medical Imaging, 42(3), 789-801.",
    "Zhavoronkov, A., et al. (2019). Deep learning enables rapid identification of potent DDR1 kinase inhibitors. Nature Biotechnology, 37, 1038-1040.",
]


def create_initial():
    import pymupdf

    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 540
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 720
    TEXT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT

    # --- Title page (page 1) ---
    page = doc.new_page(width=W, height=H)
    # Title
    page.insert_text(pymupdf.Point(MARGIN_LEFT, 200), TITLE,
                     fontsize=24, fontname="hebo", color=(0, 0, 0.4))
    # Author
    page.insert_text(pymupdf.Point(MARGIN_LEFT, 260), AUTHOR,
                     fontsize=14, fontname="tiit", color=(0, 0, 0))
    # Affiliation
    page.insert_text(pymupdf.Point(MARGIN_LEFT, 285),
                     "Department of Computer Science, Stanford University",
                     fontsize=11, fontname="tiro", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(MARGIN_LEFT, 305),
                     "Center for Biomedical Informatics Research",
                     fontsize=11, fontname="tiro", color=(0.3, 0.3, 0.3))
    # Date
    page.insert_text(pymupdf.Point(MARGIN_LEFT, 340),
                     "November 15, 2025",
                     fontsize=11, fontname="tiro", color=(0.3, 0.3, 0.3))
    # Abstract heading
    page.insert_text(pymupdf.Point(MARGIN_LEFT, 400), "Abstract",
                     fontsize=14, fontname="hebo", color=(0, 0, 0))
    # Abstract text
    abs_rect = pymupdf.Rect(MARGIN_LEFT, 420, MARGIN_RIGHT, MARGIN_BOTTOM)
    page.insert_textbox(abs_rect, ABSTRACT,
                        fontsize=10, fontname="tiro", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Content pages ---
    # We need to fill exactly 22 pages total (including title page)
    current_page = None
    y_pos = 0

    def new_content_page():
        nonlocal current_page, y_pos
        current_page = doc.new_page(width=W, height=H)
        y_pos = MARGIN_TOP
        # Page number
        pnum = doc.page_count
        current_page.insert_text(pymupdf.Point(W / 2 - 10, H - 30),
                                 str(pnum), fontsize=9, fontname="tiro",
                                 color=(0.5, 0.5, 0.5))
        # Header line
        shape = current_page.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN_LEFT, 55),
                        pymupdf.Point(MARGIN_RIGHT, 55))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()
        # Header text
        current_page.insert_text(pymupdf.Point(MARGIN_LEFT, 50),
                                 "Machine Learning in Healthcare",
                                 fontsize=8, fontname="tiit",
                                 color=(0.5, 0.5, 0.5))
        return current_page

    def ensure_space(needed):
        nonlocal current_page, y_pos
        if current_page is None or y_pos + needed > MARGIN_BOTTOM:
            new_content_page()

    def write_section_heading(heading_text):
        nonlocal y_pos
        ensure_space(40)
        y_pos += 15
        current_page.insert_text(pymupdf.Point(MARGIN_LEFT, y_pos),
                                 heading_text, fontsize=14, fontname="hebo",
                                 color=(0, 0, 0.3))
        y_pos += 10

    def write_paragraph(text):
        nonlocal current_page, y_pos
        # Estimate height needed
        chars_per_line = 85
        lines_needed = max(1, len(text) // chars_per_line + 1)
        height_needed = lines_needed * 13 + 8

        ensure_space(min(height_needed, 80))

        rect = pymupdf.Rect(MARGIN_LEFT, y_pos, MARGIN_RIGHT, MARGIN_BOTTOM)
        rc = current_page.insert_textbox(
            rect, text,
            fontsize=10, fontname="tiro", color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY
        )
        # rc < 0 means all text fit; rc > 0 means excess text didn't fit

        # Calculate actual height used
        actual_lines = lines_needed
        actual_height = actual_lines * 13 + 8
        y_pos += actual_height

    # Write all sections
    for section_title, paragraphs in SECTIONS.items():
        write_section_heading(section_title)
        for para in paragraphs:
            write_paragraph(para)

    # --- References section ---
    write_section_heading("References")
    for i, ref in enumerate(REFERENCES, 1):
        ref_text = f"[{i}] {ref}"
        ensure_space(30)
        rect = pymupdf.Rect(MARGIN_LEFT, y_pos, MARGIN_RIGHT, y_pos + 30)
        current_page.insert_textbox(
            rect, ref_text,
            fontsize=9, fontname="tiro", color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT
        )
        y_pos += 28

    # Pad to exactly 22 pages if needed
    while doc.page_count < 22:
        p = doc.new_page(width=W, height=H)
        pnum = doc.page_count
        p.insert_text(pymupdf.Point(W / 2 - 10, H - 30),
                      str(pnum), fontsize=9, fontname="tiro",
                      color=(0.5, 0.5, 0.5))
        # Header
        shape = p.new_shape()
        shape.draw_line(pymupdf.Point(MARGIN_LEFT, 55),
                        pymupdf.Point(MARGIN_RIGHT, 55))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()
        p.insert_text(pymupdf.Point(MARGIN_LEFT, 50),
                      "Machine Learning in Healthcare",
                      fontsize=8, fontname="tiit",
                      color=(0.5, 0.5, 0.5))
        # Filler content for appendix pages
        p.insert_text(pymupdf.Point(MARGIN_LEFT, MARGIN_TOP),
                      f"Appendix {chr(64 + doc.page_count - 20) if doc.page_count > 20 else ''}",
                      fontsize=14, fontname="hebo", color=(0, 0, 0.3))
        appendix_content = (
            "This appendix contains supplementary materials including detailed statistical "
            "analyses, additional figures, and extended data tables supporting the findings "
            "presented in the main text. All supplementary data has been made available in "
            "the online repository accompanying this publication."
        )
        rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 25, MARGIN_RIGHT, MARGIN_BOTTOM)
        p.insert_textbox(rect, appendix_content,
                         fontsize=10, fontname="tiro", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # If we have more than 22 pages, trim
    while doc.page_count > 22:
        doc.delete_page(doc.page_count - 1)

    # Set metadata
    doc.set_metadata({
        "title": TITLE,
        "author": AUTHOR,
        "subject": "Systematic review of machine learning applications in healthcare",
        "keywords": "machine learning, healthcare, deep learning, medical imaging, EHR",
        "creator": "Academic Publishing System",
        "producer": "PyMuPDF",
        "creationDate": "D:20251115120000",
        "modDate": "D:20251115120000",
    })

    # Add table of contents
    toc = []
    for i, section_title in enumerate(SECTIONS.keys()):
        toc.append([1, section_title, min(i + 2, 22)])
    toc.append([1, "References", min(len(SECTIONS) + 2, 22)])
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 22')

    # Verify
    doc2 = pymupdf.open(OUTPUT)
    print(f'Verified page count: {doc2.page_count}')
    print(f'Metadata title: {doc2.metadata.get("title")}')
    print(f'Metadata author: {doc2.metadata.get("author")}')
    doc2.close()

    # Open in Evince for GUI
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
