"""
Initial Setup: Create textbook_full.odt with 12 chapters, manual formatting only.
Task ID: osworld_multi_apps_book_splitting_nav_011
Domain: libreoffice_writer (ODT)

Creates:
  - /home/user/Documents/textbook_full.odt  (300-page textbook, manual formatting)
  - /home/user/Desktop/textbook_chapters/   (empty output folder)
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import P, H
from odf.namespaces import STYLENS

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
DESKTOP_DIR = f'{WORKDIR}/Desktop'
OUTPUT_FILE = f'{DOCS_DIR}/textbook_full.odt'
CHAPTERS_DIR = f'{DESKTOP_DIR}/textbook_chapters'


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


# Chapter structure: 12 chapters, each with 4-6 sections and 2-3 subsections per section
CHAPTER_DATA = [
    {
        "title": "Introduction to Computational Biology",
        "sections": [
            {
                "title": "Overview of Biological Systems",
                "subsections": ["Molecular Components", "Cellular Architecture", "Systems Integration"],
                "body": [
                    "Biology has undergone a profound transformation over the past several decades. The emergence of high-throughput technologies and computational tools has enabled researchers to study living systems at unprecedented scale and resolution.",
                    "Computational biology sits at the intersection of biology, mathematics, and computer science. It provides the theoretical and algorithmic foundations for analyzing complex biological data and modeling the dynamic processes that underlie life.",
                    "The field has its roots in early sequence analysis and protein structure prediction. However, the sequencing of the human genome marked a turning point, making it clear that computational approaches would be essential for making sense of the vast amounts of biological data being generated.",
                ]
            },
            {
                "title": "The Central Dogma Revisited",
                "subsections": ["DNA Replication Mechanisms", "Transcription Regulation"],
                "body": [
                    "The central dogma of molecular biology, articulated by Francis Crick in 1958, describes the flow of genetic information within a biological system. While the basic framework remains valid, our understanding of its details has grown tremendously.",
                    "Modern genomics has revealed that the genome is far more complex than originally imagined. Non-coding RNA species, epigenetic modifications, and three-dimensional chromatin organization all play critical roles in regulating gene expression.",
                ]
            },
            {
                "title": "Genomics and Proteomics Fundamentals",
                "subsections": ["Genome Sequencing Technologies", "Mass Spectrometry Applications", "Database Resources"],
                "body": [
                    "Genomics is the study of the complete set of genes and genetic elements in an organism. Modern sequencing technologies have made it possible to determine the complete genome sequence of many organisms, from bacteria to humans.",
                    "Proteomics extends genomic analysis to the protein level. The proteome is the complete set of proteins expressed by a cell or organism at a given time. Unlike the genome, which is relatively static, the proteome is highly dynamic, changing in response to cellular signals and environmental conditions.",
                ]
            },
            {
                "title": "Bioinformatics Data Formats",
                "subsections": ["Sequence Formats", "Structural Data Formats"],
                "body": [
                    "A variety of standard data formats have been developed for storing and exchanging biological information. Understanding these formats is essential for working with bioinformatics tools and databases.",
                    "FASTA format is perhaps the most widely used format for sequence data. Each entry consists of a header line beginning with > followed by the sequence name, and subsequent lines contain the actual sequence.",
                ]
            },
        ]
    },
    {
        "title": "Sequence Alignment and Database Searching",
        "sections": [
            {
                "title": "Pairwise Sequence Alignment",
                "subsections": ["Global Alignment Algorithms", "Local Alignment Methods", "Scoring Matrices"],
                "body": [
                    "Sequence alignment is one of the most fundamental operations in bioinformatics. By aligning two or more sequences, researchers can identify regions of similarity that may indicate functional, structural, or evolutionary relationships.",
                    "Global alignment attempts to align every residue of both sequences. The Needleman-Wunsch algorithm, developed in 1970, is the classic dynamic programming approach for global alignment. It guarantees finding the optimal global alignment but has quadratic time and space complexity.",
                    "Local alignment focuses on finding the best-matching subsequences within longer sequences. The Smith-Waterman algorithm, a modification of Needleman-Wunsch, finds optimal local alignments. It is particularly useful when sequences share only limited regions of similarity.",
                ]
            },
            {
                "title": "Multiple Sequence Alignment",
                "subsections": ["Progressive Alignment", "Iterative Refinement"],
                "body": [
                    "Multiple sequence alignment (MSA) extends pairwise alignment to simultaneously align three or more sequences. MSA is an essential step in comparative genomics, phylogenetic analysis, and protein family characterization.",
                    "The ClustalW algorithm introduced a progressive alignment strategy that remains widely used. It first computes pairwise alignments, builds a guide tree based on the pairwise distances, and then progressively aligns sequences according to the tree.",
                ]
            },
            {
                "title": "Database Search Algorithms",
                "subsections": ["BLAST Heuristics", "Profile-Based Methods", "Statistical Significance"],
                "body": [
                    "Database searching algorithms enable researchers to find sequences similar to a query sequence in large databases. The most widely used algorithm is BLAST (Basic Local Alignment Search Tool), developed by Altschul et al. in 1990.",
                    "BLAST uses a heuristic approach that trades some sensitivity for much greater speed compared to Smith-Waterman. It identifies short exact matches (words) and then extends these to find high-scoring segment pairs (HSPs).",
                ]
            },
            {
                "title": "Hidden Markov Models for Sequence Analysis",
                "subsections": ["HMM Architecture", "Training and Inference", "Applications to Protein Families"],
                "body": [
                    "Hidden Markov Models (HMMs) provide a probabilistic framework for modeling sequence families. They are particularly powerful for capturing position-specific patterns of conservation and variation in protein families.",
                    "A profile HMM consists of a series of match states, each corresponding to a column in the multiple alignment of the protein family. Each match state has an emission probability distribution over the 20 amino acids.",
                ]
            },
            {
                "title": "Phylogenetic Analysis",
                "subsections": ["Distance Methods", "Maximum Likelihood"],
                "body": [
                    "Phylogenetic analysis uses sequence data to reconstruct the evolutionary history of genes and organisms. Multiple alignment is the starting point for most phylogenetic methods.",
                    "Distance methods convert the multiple alignment into a matrix of pairwise distances, which are then used to build a tree. Neighbor-joining is a popular and efficient distance method that produces unrooted trees.",
                ]
            },
        ]
    },
    {
        "title": "Genome Assembly and Annotation",
        "sections": [
            {
                "title": "Whole Genome Sequencing Strategies",
                "subsections": ["Shotgun Sequencing", "Long-Read Technologies", "Hybrid Approaches"],
                "body": [
                    "Whole genome sequencing (WGS) has become a routine tool in biomedical research and clinical diagnostics. The choice of sequencing strategy depends on the size and complexity of the genome, the available resources, and the goals of the study.",
                    "Shotgun sequencing involves randomly fragmenting the genome and sequencing the resulting fragments. The sequences are then assembled computationally by finding overlapping regions.",
                ]
            },
            {
                "title": "Genome Assembly Algorithms",
                "subsections": ["Overlap-Layout-Consensus", "de Bruijn Graph Methods", "Assembly Quality Metrics"],
                "body": [
                    "Genome assembly is the computational process of reconstructing a genome sequence from the short reads produced by sequencing technologies. It is one of the most challenging problems in bioinformatics.",
                    "The overlap-layout-consensus (OLC) approach works by finding overlaps between all pairs of reads, building an overlap graph, finding a Hamiltonian path through the graph, and computing a consensus sequence.",
                ]
            },
            {
                "title": "Gene Prediction and Annotation",
                "subsections": ["Ab Initio Methods", "Evidence-Based Annotation"],
                "body": [
                    "Gene prediction is the problem of identifying the locations and structures of protein-coding genes in a genome sequence. It is a fundamental step in genome annotation.",
                    "Ab initio methods predict genes based solely on properties of the DNA sequence, using features like codon usage bias, signal sequences (promoters, splice sites), and statistical models of gene structure.",
                ]
            },
            {
                "title": "Comparative Genomics",
                "subsections": ["Synteny Analysis", "Evolutionary Rate Estimation", "Genome Rearrangements"],
                "body": [
                    "Comparative genomics uses differences and similarities between the genomes of different species to illuminate the function and evolution of genes and genomes.",
                    "Synteny analysis identifies genomic regions that are conserved in order and orientation across species. Such conserved syntenic blocks provide evidence for functional constraint and evolutionary relationships.",
                ]
            },
        ]
    },
    {
        "title": "Protein Structure Prediction",
        "sections": [
            {
                "title": "Protein Structure Basics",
                "subsections": ["Primary to Quaternary Structure", "Structural Databases", "Structure Visualization"],
                "body": [
                    "Proteins are the workhorses of the cell, carrying out the vast majority of biological functions. Understanding protein structure is fundamental to understanding protein function.",
                    "Protein structure is organized at four levels. Primary structure is the linear sequence of amino acids. Secondary structure refers to local regular structures stabilized by hydrogen bonds, principally alpha-helices and beta-strands.",
                ]
            },
            {
                "title": "Homology Modeling",
                "subsections": ["Template Selection", "Model Building", "Model Validation"],
                "body": [
                    "Homology modeling, also called comparative modeling, predicts the three-dimensional structure of a protein based on its similarity to one or more proteins of known structure (templates).",
                    "The first step in homology modeling is to identify suitable template structures. This involves searching structural databases like the PDB using sequence comparison methods.",
                ]
            },
            {
                "title": "Ab Initio Structure Prediction",
                "subsections": ["Energy Functions", "Sampling Methods", "Fragment Assembly"],
                "body": [
                    "Ab initio (or de novo) structure prediction aims to predict protein structure from sequence alone, without relying on homologous templates.",
                    "The fundamental challenge is finding the conformation that minimizes the free energy of the protein. In principle, this could be done by exhaustive sampling of all possible conformations, but the conformational space is astronomically large.",
                ]
            },
            {
                "title": "Deep Learning for Structure Prediction",
                "subsections": ["AlphaFold Architecture", "Coevolution Analysis", "Benchmarking"],
                "body": [
                    "The development of deep learning-based methods has revolutionized protein structure prediction. AlphaFold2, developed by DeepMind, achieves near-experimental accuracy for many proteins.",
                    "AlphaFold2 uses a novel neural network architecture called the Evoformer that iteratively processes multiple sequence alignment (MSA) information and pairwise residue features.",
                ]
            },
            {
                "title": "Protein-Protein Interaction Prediction",
                "subsections": ["Docking Methods", "Interface Prediction"],
                "body": [
                    "Protein-protein interactions are central to virtually all biological processes. Predicting these interactions and the structures of protein complexes is an important and challenging problem.",
                    "Computational docking methods predict the structure of protein-protein complexes given the structures of the individual proteins. Fast Fourier transform (FFT) methods are widely used for rigid-body docking.",
                ]
            },
        ]
    },
    {
        "title": "Gene Expression Analysis",
        "sections": [
            {
                "title": "Microarray Technology",
                "subsections": ["Array Design and Fabrication", "Data Acquisition", "Normalization Methods"],
                "body": [
                    "DNA microarrays revolutionized gene expression analysis in the 1990s and 2000s. They enabled researchers to measure the expression of thousands of genes simultaneously.",
                    "A microarray consists of thousands of DNA probes attached to a solid surface. RNA from cells is reverse-transcribed to cDNA, labeled with fluorescent dyes, and hybridized to the array.",
                ]
            },
            {
                "title": "RNA-Seq Analysis Pipeline",
                "subsections": ["Read Mapping", "Quantification", "Differential Expression"],
                "body": [
                    "RNA sequencing (RNA-Seq) has largely superseded microarrays for transcriptome analysis. It provides a more comprehensive and unbiased view of gene expression.",
                    "The RNA-Seq analysis pipeline begins with quality control of the raw sequencing reads. Tools like FastQC are used to assess read quality, adapter contamination, and other potential issues.",
                ]
            },
            {
                "title": "Single-Cell Transcriptomics",
                "subsections": ["Cell Capture Technologies", "Dimensionality Reduction", "Cell Type Identification"],
                "body": [
                    "Single-cell RNA sequencing (scRNA-Seq) enables transcriptomic analysis at the resolution of individual cells. This has opened up new possibilities for understanding cellular heterogeneity, development, and disease.",
                    "Several technologies are available for capturing individual cells and preparing them for sequencing. Droplet-based methods like 10x Genomics Chromium use microfluidics to encapsulate individual cells in droplets along with barcoded beads.",
                ]
            },
            {
                "title": "Regulatory Network Inference",
                "subsections": ["Co-expression Networks", "Transcription Factor Binding", "Causal Inference"],
                "body": [
                    "Gene regulatory networks (GRNs) describe the interactions between transcription factors and their target genes. Inferring these networks from expression data is an important goal of systems biology.",
                    "Co-expression networks are constructed by computing pairwise correlations between gene expression profiles. Genes with high correlation are assumed to be functionally related, often because they are regulated by the same transcription factors.",
                ]
            },
        ]
    },
    {
        "title": "Epigenomics and Chromatin Structure",
        "sections": [
            {
                "title": "Chromatin Organization",
                "subsections": ["Nucleosome Structure", "Higher-Order Chromatin Folding", "Topologically Associating Domains"],
                "body": [
                    "Chromatin is the complex of DNA and proteins that makes up chromosomes. Its organization plays a crucial role in regulating gene expression and other DNA-based processes.",
                    "The basic unit of chromatin is the nucleosome, consisting of approximately 147 base pairs of DNA wrapped around a histone octamer. Nucleosome positioning influences the accessibility of DNA to transcription factors and other regulatory proteins.",
                ]
            },
            {
                "title": "DNA Methylation Analysis",
                "subsections": ["Bisulfite Sequencing", "Methylation Patterns", "Functional Roles"],
                "body": [
                    "DNA methylation is the addition of a methyl group to the 5-carbon position of cytosine, primarily at CpG dinucleotides. It is an important epigenetic mark involved in gene silencing, imprinting, and X-chromosome inactivation.",
                    "Bisulfite sequencing is the gold standard for measuring DNA methylation. Bisulfite treatment converts unmethylated cytosines to uracil (which reads as thymine), while methylated cytosines remain unchanged.",
                ]
            },
            {
                "title": "Histone Modification Profiling",
                "subsections": ["ChIP-Seq Protocol", "Peak Calling", "Histone Code Interpretation"],
                "body": [
                    "Histone modifications are chemical modifications to histone proteins that influence chromatin structure and gene expression. They include methylation, acetylation, phosphorylation, and ubiquitination.",
                    "Chromatin immunoprecipitation followed by sequencing (ChIP-Seq) is the primary method for mapping histone modifications genome-wide. Antibodies specific to particular modifications are used to immunoprecipitate modified histones along with associated DNA.",
                ]
            },
            {
                "title": "Three-Dimensional Genome Organization",
                "subsections": ["Hi-C Technology", "Compartments and TADs", "Enhancer-Promoter Loops"],
                "body": [
                    "The three-dimensional organization of the genome in the nucleus plays an important role in gene regulation. Genes and their regulatory elements may be located far apart in the linear genome but come into close proximity in three-dimensional space.",
                    "Hi-C is a chromosome conformation capture technique that captures genome-wide chromatin interactions. Cells are crosslinked with formaldehyde, the chromatin is digested with restriction enzymes, the ends are ligated, and the resulting chimeric fragments are sequenced.",
                ]
            },
            {
                "title": "Epigenetic Inheritance",
                "subsections": ["Transgenerational Epigenetics", "Epigenetic Reprogramming"],
                "body": [
                    "Epigenetic modifications can be transmitted from parent cells to daughter cells during cell division. This epigenetic inheritance is essential for maintaining cell identity during development.",
                    "During mammalian development, there are two major waves of epigenetic reprogramming. The first occurs in primordial germ cells, erasing most epigenetic marks. The second occurs after fertilization in the early embryo.",
                ]
            },
        ]
    },
    {
        "title": "Metabolomics and Systems Biology",
        "sections": [
            {
                "title": "Metabolomics Overview",
                "subsections": ["Analytical Platforms", "Sample Preparation", "Metabolite Databases"],
                "body": [
                    "Metabolomics is the comprehensive study of small molecules (metabolites) in a biological sample. It provides a snapshot of the metabolic state of a cell, tissue, or organism.",
                    "Two main analytical platforms are used in metabolomics: nuclear magnetic resonance (NMR) spectroscopy and mass spectrometry (MS). NMR is non-destructive and can quantify metabolites without prior separation.",
                ]
            },
            {
                "title": "Flux Balance Analysis",
                "subsections": ["Stoichiometric Models", "Linear Programming", "Genome-Scale Models"],
                "body": [
                    "Flux balance analysis (FBA) is a mathematical approach for analyzing the flow of metabolites through a metabolic network. It uses stoichiometric constraints and linear programming to predict metabolic fluxes at steady state.",
                    "A stoichiometric model represents each metabolic reaction as a balance equation. The stoichiometric matrix S has rows corresponding to metabolites and columns corresponding to reactions.",
                ]
            },
            {
                "title": "Network Analysis in Systems Biology",
                "subsections": ["Scale-Free Networks", "Modularity", "Network Motifs"],
                "body": [
                    "Systems biology takes a holistic approach to understanding biological systems, focusing on interactions between components rather than individual components in isolation.",
                    "Biological networks, protein interaction networks, metabolic networks, gene regulatory networks, often have complex topological properties. Many biological networks are scale-free, meaning that the degree distribution follows a power law.",
                ]
            },
            {
                "title": "Dynamic Modeling of Biological Systems",
                "subsections": ["Ordinary Differential Equations", "Stochastic Models", "Parameter Estimation"],
                "body": [
                    "Dynamic models describe how biological systems change over time. They are essential for understanding processes like cell signaling, gene expression dynamics, and metabolic oscillations.",
                    "Ordinary differential equation (ODE) models are the most widely used approach for deterministic modeling of biological systems. Each state variable (e.g., protein concentration) is described by a differential equation.",
                ]
            },
        ]
    },
    {
        "title": "Metagenomics and Microbial Ecology",
        "sections": [
            {
                "title": "Introduction to Metagenomics",
                "subsections": ["Shotgun Metagenomics", "Amplicon Sequencing", "Sample Collection Considerations"],
                "body": [
                    "Metagenomics is the study of genetic material recovered directly from environmental samples, bypassing the need to culture individual organisms. This approach has revealed the vast diversity of microbial life.",
                    "The human gut microbiome, for example, contains trillions of microorganisms representing hundreds of species. Traditional culture-based methods could only characterize a small fraction of this diversity.",
                ]
            },
            {
                "title": "Taxonomic Profiling Methods",
                "subsections": ["16S rRNA Analysis", "Marker Gene Approaches", "Whole-Metagenome Approaches"],
                "body": [
                    "A fundamental goal of metagenomic analysis is to determine which organisms are present in a sample and in what abundance. This is called taxonomic profiling or community composition analysis.",
                    "The 16S ribosomal RNA gene is widely used as a marker for bacterial taxonomy. It contains highly conserved regions that can be used as PCR primer binding sites, flanking variable regions that carry taxonomic information.",
                ]
            },
            {
                "title": "Functional Analysis of Metagenomes",
                "subsections": ["Gene Prediction", "Pathway Enrichment", "Comparative Metagenomics"],
                "body": [
                    "Beyond identifying which organisms are present, researchers are often interested in the functional capabilities encoded in a microbial community. Functional metagenomics involves annotating the genes present in a metagenome.",
                    "Gene prediction in metagenomic data is more challenging than in complete genomes because metagenomic assemblies are fragmented and may contain partial genes.",
                ]
            },
            {
                "title": "Microbiome and Human Health",
                "subsections": ["Gut-Brain Axis", "Dysbiosis and Disease", "Therapeutic Interventions"],
                "body": [
                    "The human microbiome has been linked to many aspects of health and disease. The gut microbiome in particular is associated with metabolic disorders, inflammatory diseases, and even mental health.",
                    "Dysbiosis, an imbalance or disruption in the microbiome composition, has been associated with conditions including inflammatory bowel disease, obesity, type 2 diabetes, and autism spectrum disorder.",
                ]
            },
            {
                "title": "Environmental Metagenomics",
                "subsections": ["Soil Microbiomes", "Ocean Metagenomics"],
                "body": [
                    "Metagenomics has been applied to diverse environments, revealing the incredible diversity of microbial life across the planet.",
                    "Soil microbiomes are among the most diverse microbial communities on Earth. A single gram of soil may contain billions of microbial cells representing thousands of species.",
                ]
            },
        ]
    },
    {
        "title": "Structural Bioinformatics",
        "sections": [
            {
                "title": "Protein Structure Databases",
                "subsections": ["Protein Data Bank", "Structure Classification Databases", "Quality Assessment"],
                "body": [
                    "The Protein Data Bank (PDB) is the primary repository for three-dimensional macromolecular structures. It currently contains over 200,000 structures determined by X-ray crystallography, NMR spectroscopy, and electron microscopy.",
                    "Structure classification databases like SCOP (Structural Classification of Proteins) and CATH organize protein structures into a hierarchical classification based on their structural and evolutionary relationships.",
                ]
            },
            {
                "title": "Molecular Dynamics Simulations",
                "subsections": ["Force Fields", "Simulation Protocols", "Analysis Methods"],
                "body": [
                    "Molecular dynamics (MD) simulations model the motion of atoms in a molecular system over time by numerically integrating Newton's equations of motion.",
                    "The behavior of atoms in MD simulations is governed by force fields, mathematical descriptions of the potential energy of the system as a function of atomic positions.",
                ]
            },
            {
                "title": "Drug-Target Interaction Prediction",
                "subsections": ["Virtual Screening", "Pharmacophore Modeling", "ADMET Properties"],
                "body": [
                    "Structure-based drug discovery uses knowledge of the three-dimensional structure of biological targets to guide the design of new therapeutic molecules.",
                    "Virtual screening computationally searches large libraries of compounds to identify those that might bind to a target. Docking methods are commonly used to predict binding poses and affinities.",
                ]
            },
            {
                "title": "Cryo-EM Data Processing",
                "subsections": ["Image Acquisition", "Single-Particle Reconstruction", "Resolution Assessment"],
                "body": [
                    "Cryo-electron microscopy (cryo-EM) has emerged as a powerful technique for determining the structures of large macromolecular complexes.",
                    "Single-particle cryo-EM involves imaging thousands of individual copies of a macromolecule frozen in vitreous ice. Computational methods are then used to determine their orientations and reconstruct a three-dimensional density map.",
                ]
            },
        ]
    },
    {
        "title": "Machine Learning in Bioinformatics",
        "sections": [
            {
                "title": "Supervised Learning Methods",
                "subsections": ["Classification Algorithms", "Regression Models", "Feature Engineering"],
                "body": [
                    "Machine learning has become an indispensable tool in bioinformatics, enabling researchers to extract patterns from high-dimensional biological data and make predictions about biological systems.",
                    "Supervised learning methods learn to make predictions from labeled training data. Classification methods predict discrete class labels (e.g., disease vs. healthy), while regression methods predict continuous values (e.g., gene expression levels).",
                ]
            },
            {
                "title": "Deep Learning Architectures",
                "subsections": ["Convolutional Neural Networks", "Recurrent Networks", "Transformers and Attention"],
                "body": [
                    "Deep learning has achieved remarkable successes in bioinformatics, particularly for analyzing sequence data and predicting protein structures.",
                    "Convolutional neural networks (CNNs) are particularly effective for analyzing sequence data by applying sliding window filters to detect sequence motifs.",
                ]
            },
            {
                "title": "Genomic Variant Analysis with ML",
                "subsections": ["Variant Calling", "Pathogenicity Prediction", "Polygenic Risk Scores"],
                "body": [
                    "Machine learning is widely used for analyzing genomic variants, from calling variants in sequencing data to predicting their functional consequences.",
                    "DeepVariant, developed by Google, uses deep learning to call single nucleotide variants and indels from high-throughput sequencing data. It formulates variant calling as an image classification problem.",
                ]
            },
            {
                "title": "Multi-Omics Data Integration",
                "subsections": ["Data Fusion Strategies", "Matrix Factorization", "Network-Based Integration"],
                "body": [
                    "Modern biological studies often generate data from multiple omics platforms. Integrating these data streams is essential for a comprehensive understanding of biological systems.",
                    "Early integration concatenates features from all omics datasets before applying a single learning algorithm. This approach is simple but may not capture complex relationships between different omics layers.",
                ]
            },
            {
                "title": "Interpretability and Explainability",
                "subsections": ["Feature Importance", "Attention Visualization", "Biological Validation"],
                "body": [
                    "As machine learning models become more complex, their interpretability decreases. In biology, understanding why a model makes a prediction is often as important as the prediction itself.",
                    "Feature importance methods identify which input features most influence model predictions. For genomics models, this can reveal which sequence positions or motifs are most informative.",
                ]
            },
        ]
    },
    {
        "title": "Clinical Bioinformatics",
        "sections": [
            {
                "title": "Clinical Genomics Applications",
                "subsections": ["Rare Disease Diagnosis", "Cancer Genomics", "Pharmacogenomics"],
                "body": [
                    "Clinical bioinformatics applies computational methods to analyze genomic and other molecular data in a clinical context, with the goal of improving diagnosis, treatment, and prevention of disease.",
                    "Whole exome and whole genome sequencing are increasingly used for diagnosing rare genetic diseases. The challenge is identifying the causative variant among the millions of variants present in each individual's genome.",
                ]
            },
            {
                "title": "Electronic Health Records and Data Integration",
                "subsections": ["EHR Data Standards", "NLP for Clinical Text", "Phenotyping Algorithms"],
                "body": [
                    "Electronic health records (EHRs) contain vast amounts of information about patients' medical histories, diagnoses, treatments, and outcomes. Mining this data can reveal patterns of disease and treatment response.",
                    "HL7 FHIR (Fast Healthcare Interoperability Resources) is a standard for exchanging healthcare information electronically. It enables interoperability between different health information systems.",
                ]
            },
            {
                "title": "Precision Medicine Approaches",
                "subsections": ["Biomarker Discovery", "Treatment Stratification", "Clinical Trials Design"],
                "body": [
                    "Precision medicine aims to tailor medical treatment to the individual characteristics of each patient. Genomic information is a key component of this personalized approach.",
                    "Biomarker discovery is a central activity in precision medicine. Biomarkers are measurable indicators of biological state that can be used to diagnose disease, predict prognosis, or guide treatment decisions.",
                ]
            },
            {
                "title": "Regulatory and Ethical Considerations",
                "subsections": ["Data Privacy", "GDPR and HIPAA Compliance", "Algorithmic Bias"],
                "body": [
                    "The use of genomic and other molecular data in clinical settings raises important regulatory and ethical issues that must be carefully addressed.",
                    "Genetic data is uniquely sensitive because it is immutable, can reveal information about relatives, and may have implications for insurance, employment, and other aspects of life.",
                ]
            },
        ]
    },
    {
        "title": "Future Directions in Computational Biology",
        "sections": [
            {
                "title": "Artificial Intelligence in Drug Discovery",
                "subsections": ["Generative Models for Molecules", "Target Identification", "Clinical Trial Optimization"],
                "body": [
                    "Artificial intelligence is transforming drug discovery, accelerating every step from target identification to clinical trials.",
                    "Generative models can design novel molecules with desired properties. Variational autoencoders (VAEs) and generative adversarial networks (GANs) have been applied to generate new drug-like molecules.",
                ]
            },
            {
                "title": "Spatial Transcriptomics",
                "subsections": ["Technology Overview", "Analysis Methods", "Tissue Architecture Mapping"],
                "body": [
                    "Spatial transcriptomics combines the power of transcriptomics with information about the spatial organization of cells within tissues.",
                    "Technologies like 10x Visium and Slide-Seq enable researchers to measure gene expression while preserving spatial information. This is enabling new insights into tissue organization and cell-cell communication.",
                ]
            },
            {
                "title": "Quantum Computing Applications",
                "subsections": ["Quantum Optimization", "Quantum Machine Learning", "Current Limitations"],
                "body": [
                    "Quantum computing promises to solve certain computational problems exponentially faster than classical computers. Several applications in computational biology have been proposed.",
                    "Protein folding has been formulated as a quantum optimization problem. Quantum annealers like D-Wave have been used to find low-energy configurations of simplified protein models.",
                ]
            },
            {
                "title": "Convergence of AI and Experimental Biology",
                "subsections": ["Active Learning", "Robotic Experiments", "Closed-Loop Optimization"],
                "body": [
                    "The boundary between computational and experimental biology is becoming increasingly blurred. AI systems are being used to design experiments, interpret results, and guide subsequent experiments in a closed loop.",
                    "Active learning algorithms select the most informative experiments to perform, maximizing the information gained from each experimental iteration. This approach has been applied to protein engineering and drug discovery.",
                ]
            },
            {
                "title": "Ethical AI in Biology",
                "subsections": ["Equitable Access", "Environmental Impact", "Responsible Innovation"],
                "body": [
                    "As AI becomes increasingly powerful in biology, it is important to consider the ethical implications of these technologies and ensure they are developed and deployed responsibly.",
                    "Equitable access to genomic medicine is a major concern. Advanced genomic analyses are not equally available to all populations, potentially exacerbating health disparities.",
                ]
            },
        ]
    },
]


def setup_manual_styles(doc):
    """Create manual formatting styles (NOT heading styles) for initial env."""
    # Chapter title: bold 18pt, no heading style
    chap_style = Style(name="ChapterTitle", family="paragraph")
    chap_style.addElement(TextProperties(fontsize="18pt", fontweight="bold",
                                          fontsizeasian="18pt", fontweightasian="bold"))
    chap_style.addElement(ParagraphProperties(margintop="0.3in", marginbottom="0.1in"))
    doc.styles.addElement(chap_style)

    # Section title: bold 14pt, no heading style
    sec_style = Style(name="SectionTitle", family="paragraph")
    sec_style.addElement(TextProperties(fontsize="14pt", fontweight="bold",
                                         fontsizeasian="14pt", fontweightasian="bold"))
    sec_style.addElement(ParagraphProperties(margintop="0.2in", marginbottom="0.05in"))
    doc.styles.addElement(sec_style)

    # Subsection title: bold 12pt, no heading style
    sub_style = Style(name="SubsectionTitle", family="paragraph")
    sub_style.addElement(TextProperties(fontsize="12pt", fontweight="bold",
                                         fontsizeasian="12pt", fontweightasian="bold"))
    sub_style.addElement(ParagraphProperties(margintop="0.1in", marginbottom="0.03in"))
    doc.styles.addElement(sub_style)

    # Body text
    body_style = Style(name="BodyManual", family="paragraph")
    body_style.addElement(TextProperties(fontsize="11pt", fontsizeasian="11pt"))
    body_style.addElement(ParagraphProperties(margintop="0.04in", marginbottom="0.04in"))
    doc.styles.addElement(body_style)


def add_para(doc_text, text, style_name):
    p = P(stylename=style_name)
    p.addText(text)
    doc_text.addElement(p)


def create_initial():
    """Create textbook_full.odt with manual formatting (no heading styles)."""
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(CHAPTERS_DIR, exist_ok=True)

    doc = OpenDocumentText()
    setup_manual_styles(doc)
    text = doc.text

    for chap_idx, chapter in enumerate(CHAPTER_DATA, 1):
        # Chapter title: manual bold+large (NOT Heading 1 style)
        add_para(text, f"Chapter {chap_idx}: {chapter['title']}", "ChapterTitle")

        for sec_idx, section in enumerate(chapter['sections'], 1):
            # Section: manual bold 14pt (NOT Heading 2 style)
            add_para(text, f"{chap_idx}.{sec_idx} {section['title']}", "SectionTitle")

            # Body paragraphs
            for body_para in section['body']:
                add_para(text, body_para, "BodyManual")

            # Subsections: manual bold 12pt (NOT Heading 3 style)
            for sub_idx, subsection in enumerate(section['subsections'], 1):
                add_para(text, f"{chap_idx}.{sec_idx}.{sub_idx} {subsection}", "SubsectionTitle")
                add_para(
                    text,
                    f"This subsection covers {subsection.lower()} in depth, "
                    f"examining theoretical foundations and practical applications "
                    f"relevant to the broader context of {section['title'].lower()}.",
                    "BodyManual"
                )
                add_para(
                    text,
                    f"Research in {subsection.lower()} has advanced considerably in recent years, "
                    f"driven by improvements in computational power and the availability of large "
                    f"public datasets. Current best practices are reviewed here.",
                    "BodyManual"
                )

    doc.save(OUTPUT_FILE)
    print(f"Initial file created: {OUTPUT_FILE}")
    print(f"Output directory created (empty): {CHAPTERS_DIR}")

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT_FILE}"', delay_sec=3.0)
    print("GUI_READY: launched LibreOffice Writer with DISPLAY=:0")


create_initial()
