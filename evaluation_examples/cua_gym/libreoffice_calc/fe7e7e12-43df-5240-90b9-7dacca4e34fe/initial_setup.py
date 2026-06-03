"""
Initial Setup: study_material.pdf with 20 pages, no annotations
Task ID: pdf_adv_139
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user/Documents'
TASK_ID = 'study_material'
OUTPUT = f'{WORKDIR}/{TASK_ID}.pdf'


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
    # Ensure Documents directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()  # new empty PDF

    # Realistic study material content organized as a 20-page document
    chapters = [
        ("Chapter 1: Introduction to Cellular Biology", [
            "Cell theory forms the fundamental basis of modern biology. All living organisms are composed of one or more cells, and the cell is considered the basic unit of life. This chapter provides an overview of cell structure and function.",
            "The discovery of cells dates back to 1665 when Robert Hooke first observed cork cells under a microscope. Later, Matthias Schleiden (1838) and Theodor Schwann (1839) formulated the cell theory, which was expanded by Rudolf Virchow in 1855 with the principle that all cells arise from pre-existing cells.",
            "Cells are broadly classified into two types: prokaryotic cells (found in bacteria and archaea) and eukaryotic cells (found in plants, animals, fungi, and protists). The key distinction is the presence of a membrane-bound nucleus in eukaryotic cells.",
        ]),
        ("Chapter 1: Cell Membrane Structure", [
            "The plasma membrane is a selectively permeable barrier that encloses the cell contents. It is composed primarily of a phospholipid bilayer with embedded proteins. The fluid mosaic model, proposed by Singer and Nicolson in 1972, describes this arrangement.",
            "Phospholipids have a hydrophilic (water-loving) head and hydrophobic (water-fearing) tail. In aqueous environments, they spontaneously arrange into a bilayer with hydrophilic heads facing outward and hydrophobic tails facing inward.",
            "Membrane proteins serve various functions including transport, signal transduction, enzymatic activity, cell recognition, and structural support. Integral proteins span the membrane while peripheral proteins are loosely attached to the surface.",
        ]),
        ("Chapter 2: DNA and Genetic Information", [
            "Deoxyribonucleic acid (DNA) is the molecular carrier of genetic information in all living organisms. The double-helix structure of DNA was first described by James Watson and Francis Crick in 1953, based on X-ray crystallography data produced by Rosalind Franklin.",
            "DNA is composed of nucleotides, each containing a deoxyribose sugar, a phosphate group, and one of four nitrogenous bases: adenine (A), thymine (T), guanine (G), and cytosine (C). Base pairing rules dictate that A pairs with T, and G pairs with C.",
            "The genetic information encoded in DNA is organized into genes, which serve as templates for the synthesis of RNA and ultimately proteins. The human genome contains approximately 3 billion base pairs and around 20,000-25,000 protein-coding genes.",
        ]),
        ("Chapter 2: DNA Replication", [
            "DNA replication is the process by which a cell duplicates its genetic material before cell division. It is semi-conservative, meaning each new DNA molecule contains one original strand and one newly synthesized strand.",
            "The process begins at specific sequences called origins of replication. In prokaryotes, there is typically one origin, while eukaryotic chromosomes have multiple origins to speed up replication. The replication fork is the site where the two parental DNA strands are separated.",
            "Key enzymes involved in DNA replication include helicase (unwinds the double helix), primase (synthesizes RNA primers), DNA polymerase III (synthesizes new DNA strands), DNA polymerase I (removes RNA primers and replaces them with DNA), and DNA ligase (seals nicks in the sugar-phosphate backbone).",
        ]),
        ("Chapter 3: Protein Synthesis", [
            "Protein synthesis, also called translation, is the process by which the genetic code is used to produce proteins. It involves two main stages: transcription (DNA to mRNA) and translation (mRNA to protein).",
            "During transcription, RNA polymerase binds to the promoter region of a gene and unwinds the DNA double helix. It then synthesizes a complementary mRNA strand using one DNA strand as a template. The mRNA undergoes processing (5' capping, 3' polyadenylation, and splicing of introns) before leaving the nucleus.",
            "Translation occurs at ribosomes in the cytoplasm. The mRNA sequence is read in triplets called codons, each specifying a particular amino acid. Transfer RNA (tRNA) molecules carry amino acids to the ribosome, matching their anticodon to the complementary mRNA codon.",
        ]),
        ("Chapter 3: Enzyme Function", [
            "Enzymes are biological catalysts that accelerate chemical reactions without being consumed in the process. Most enzymes are proteins, although some RNA molecules (ribozymes) also have catalytic activity.",
            "The active site of an enzyme is the region where substrate molecules bind and undergo chemical transformation. The lock-and-key model describes the high specificity of enzyme-substrate interactions, while the induced fit model suggests that both enzyme and substrate undergo conformational changes upon binding.",
            "Enzyme activity is influenced by factors including temperature, pH, substrate concentration, enzyme concentration, and the presence of inhibitors or activators. Competitive inhibitors compete with the substrate for the active site, while non-competitive inhibitors bind to allosteric sites and reduce enzyme efficiency.",
        ]),
        ("Chapter 4: Cell Division and Mitosis", [
            "Cell division is essential for growth, repair, and reproduction. In eukaryotes, somatic cells divide by mitosis, which produces two genetically identical daughter cells. Mitosis is divided into four phases: prophase, metaphase, anaphase, and telophase, followed by cytokinesis.",
            "During prophase, chromosomes condense and become visible, the nuclear envelope breaks down, and the mitotic spindle begins to form from microtubules. Sister chromatids (identical copies produced during DNA replication) are held together at the centromere.",
            "In metaphase, chromosomes align along the cell's equatorial plate (metaphase plate). Anaphase begins when sister chromatids are separated and pulled toward opposite poles of the cell. Telophase involves nuclear envelope reformation around each set of chromosomes, followed by cytokinesis (division of the cytoplasm).",
        ]),
        ("Chapter 4: Meiosis and Sexual Reproduction", [
            "Meiosis is a specialized form of cell division that produces four genetically diverse haploid cells from one diploid parent cell. It consists of two rounds of division: meiosis I (reductional division) and meiosis II (equational division).",
            "Crossing over (recombination) occurs during prophase I, when homologous chromosomes exchange segments at points called chiasmata. This process increases genetic diversity by creating new combinations of alleles. Independent assortment of chromosomes also contributes to genetic variation.",
            "Fertilization of a haploid egg by a haploid sperm restores the diploid chromosome number. Sexual reproduction generates greater genetic diversity than asexual reproduction, which is an important evolutionary advantage in changing environments.",
        ]),
        ("Chapter 5: Photosynthesis", [
            "Photosynthesis is the process by which photoautotrophs (primarily plants, algae, and cyanobacteria) convert light energy into chemical energy stored in glucose. The overall equation is: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2.",
            "Photosynthesis occurs in chloroplasts, which contain an elaborate membrane system. The light-dependent reactions take place in the thylakoid membranes, while the Calvin cycle (light-independent reactions) occurs in the stroma. Chlorophyll and other pigments in the thylakoid membranes absorb light energy.",
            "During the light-dependent reactions, water molecules are split (photolysis), releasing oxygen as a byproduct. The energy captured is used to generate ATP and NADPH, which power the Calvin cycle. In the Calvin cycle, CO2 is fixed into organic molecules through a series of enzyme-catalyzed reactions.",
        ]),
        ("Chapter 5: Cellular Respiration", [
            "Cellular respiration is the process by which cells break down organic molecules to release energy in the form of ATP. The complete oxidation of glucose yields a theoretical maximum of 38 ATP molecules, although in practice, the yield is closer to 30-32 ATP.",
            "Cellular respiration occurs in three main stages: glycolysis (in the cytoplasm), the Krebs cycle (in the mitochondrial matrix), and oxidative phosphorylation (in the inner mitochondrial membrane). Glycolysis breaks down glucose into two pyruvate molecules, producing 2 ATP and 2 NADH.",
            "The electron transport chain (ETC) is a series of protein complexes embedded in the inner mitochondrial membrane. Electrons from NADH and FADH2 are passed through the chain, releasing energy used to pump protons across the membrane. ATP synthase uses the proton gradient to synthesize ATP through chemiosmosis.",
        ]),
        ("Chapter 6: Genetics and Inheritance", [
            "Genetics is the study of heredity and variation in organisms. Gregor Mendel's experiments with pea plants in the 1850s-1860s established the fundamental principles of inheritance, although his work was not widely recognized until after his death.",
            "Mendel's law of segregation states that each organism carries two alleles for each trait, and these alleles separate during gamete formation. The law of independent assortment states that alleles for different traits are inherited independently of one another (when genes are on different chromosomes).",
            "Dominance relationships between alleles can be complete (one allele masks the other), incomplete (heterozygotes have an intermediate phenotype), or codominant (both alleles are fully expressed in heterozygotes). Sex-linked traits are encoded on sex chromosomes and show different inheritance patterns in males and females.",
        ]),
        ("Chapter 6: Mutations and Evolution", [
            "Mutations are changes in the DNA sequence that can alter gene function. Point mutations affect a single nucleotide and include substitutions, insertions, and deletions. Chromosomal mutations involve changes in chromosome structure or number.",
            "Mutations can be spontaneous (occurring naturally during DNA replication or repair) or induced by mutagens (physical agents like UV radiation, chemical agents like alkylating agents, or biological agents like certain viruses). Many mutations are neutral, but some can be beneficial or harmful.",
            "Natural selection acts on phenotypic variation to favor individuals with traits that enhance survival and reproduction in a given environment. Over generations, beneficial traits increase in frequency while harmful traits decrease. This process, combined with genetic drift, mutation, and gene flow, drives evolutionary change.",
        ]),
        ("Chapter 7: Nervous System", [
            "The nervous system is responsible for rapid communication and coordination in animals. In vertebrates, it is divided into the central nervous system (CNS: brain and spinal cord) and the peripheral nervous system (PNS: cranial and spinal nerves).",
            "Neurons are the functional units of the nervous system. A typical neuron consists of a cell body (soma), dendrites that receive signals, and an axon that transmits signals. The synapse is the junction between neurons where chemical or electrical signals are transmitted.",
            "Action potentials are electrical signals that travel along the axon. They are generated when the membrane potential reaches a threshold, causing voltage-gated Na+ channels to open. The action potential propagates along the axon by a wave of depolarization and repolarization, and is terminated by the refractory period.",
        ]),
        ("Chapter 7: Immune System", [
            "The immune system defends the body against pathogens, foreign substances, and abnormal cells. It consists of innate immunity (non-specific, rapid response) and adaptive immunity (specific, slower response with immunological memory).",
            "Key cells of the immune system include neutrophils and macrophages (phagocytosis), natural killer cells (target infected or tumor cells), T lymphocytes (cell-mediated immunity), and B lymphocytes (antibody-mediated or humoral immunity). Dendritic cells serve as antigen-presenting cells linking innate and adaptive immunity.",
            "B cells produce antibodies (immunoglobulins) that specifically bind to antigens. T helper cells (CD4+) coordinate immune responses by releasing cytokines, while cytotoxic T cells (CD8+) directly kill infected cells. Memory cells formed during an immune response provide faster protection upon re-exposure to the same pathogen.",
        ]),
        ("Chapter 8: Ecology Fundamentals", [
            "Ecology is the scientific study of interactions among organisms and between organisms and their environment. Ecological organization is studied at multiple levels: individual, population, community, ecosystem, biome, and biosphere.",
            "A population consists of individuals of the same species living in a defined area. Population dynamics are influenced by birth rate, death rate, immigration, and emigration. Populations can exhibit exponential growth (J-curve) when resources are unlimited, or logistic growth (S-curve) when limited by carrying capacity.",
            "Communities are assemblages of interacting species. Key ecological relationships include predation, competition, mutualism, commensalism, and parasitism. The concept of ecological niches describes the role and position of a species within its community.",
        ]),
        ("Chapter 8: Ecosystem Dynamics", [
            "Ecosystems are functional units that include all living organisms in an area and their abiotic environment. Energy flows through ecosystems in one direction (from producers to consumers to decomposers), while matter (chemical elements) cycles through biotic and abiotic components.",
            "Primary productivity is the rate at which autotrophs (producers) convert light or chemical energy into organic compounds. Net primary productivity (NPP) is the energy remaining after subtracting the amount used in cellular respiration. NPP varies widely across ecosystem types.",
            "Nutrient cycles (biogeochemical cycles) describe how chemical elements move through ecosystems. Key cycles include the carbon cycle, nitrogen cycle, phosphorus cycle, and water cycle. Human activities have significantly altered many of these cycles, leading to environmental problems such as climate change and eutrophication.",
        ]),
        ("Chapter 9: Human Physiology", [
            "Human physiology examines the mechanisms by which the body maintains homeostasis — a stable internal environment essential for survival. Major organ systems work together in coordinated ways to regulate body temperature, blood pH, blood glucose, and fluid balance.",
            "The endocrine system regulates long-term body functions through hormones secreted by glands such as the pituitary, thyroid, adrenal glands, pancreas, and gonads. Hormones travel through the bloodstream and exert effects on target tissues via specific receptors.",
            "The cardiovascular system delivers nutrients and oxygen to tissues while removing waste products. The heart pumps blood through a closed system of arteries, capillaries, and veins. Blood pressure is regulated by cardiac output, peripheral resistance, and blood volume.",
        ]),
        ("Chapter 9: Digestive and Excretory Systems", [
            "The digestive system breaks down food into nutrients that can be absorbed and used by cells. Digestion involves both mechanical (chewing, peristalsis) and chemical (enzymatic) processes. Key organs include the mouth, esophagus, stomach, small intestine, large intestine, liver, gallbladder, and pancreas.",
            "The liver plays a central role in metabolism, producing bile for fat digestion, metabolizing carbohydrates, proteins, and lipids, detoxifying substances, and synthesizing plasma proteins. The liver also stores glycogen, vitamins, and minerals.",
            "The excretory system removes metabolic waste products from the body. The kidneys filter blood to produce urine, removing nitrogenous waste (primarily urea), excess salts, and water. Each kidney contains about one million nephrons, the functional units responsible for filtration, reabsorption, and secretion.",
        ]),
        ("Chapter 10: Review and Summary", [
            "This chapter summarizes the key concepts covered throughout the study material. Biology is the science of life, and the topics covered — from molecular biology to ecology — all connect to form a comprehensive understanding of living systems.",
            "Core themes include: the cell as the basic unit of life, the flow of genetic information from DNA to RNA to protein, energy transformation in photosynthesis and respiration, the mechanisms of inheritance and evolution, and the organization of living systems from molecules to the biosphere.",
            "Understanding these principles provides a foundation for advanced study in medicine, ecology, biotechnology, and many other fields. The dynamic nature of biology means that new discoveries continually refine and expand our knowledge of the living world.",
        ]),
        ("Chapter 10: Practice Questions", [
            "1. Describe the structure of the plasma membrane and explain how its structure relates to its function as a selectively permeable barrier.\n2. Compare and contrast mitosis and meiosis, including the significance of each process for the organism.\n3. Explain how the electron transport chain in mitochondria generates ATP through chemiosmosis.",
            "4. Describe the process of DNA replication, including the roles of the key enzymes involved.\n5. What is the significance of crossing over during meiosis I, and how does it contribute to genetic diversity?\n6. Explain the concept of enzyme specificity and describe how competitive and non-competitive inhibitors affect enzyme activity.",
            "7. Compare the roles of B cells and T cells in the adaptive immune response.\n8. Describe the carbon cycle, identifying the major processes that move carbon between its various reservoirs.\n9. Explain how natural selection leads to evolutionary change in a population over multiple generations.\n10. What is homeostasis, and how do the nervous and endocrine systems work together to maintain it?",
        ]),
    ]

    page_width, page_height = 612, 792  # letter size

    for i, (chapter_title, paragraphs) in enumerate(chapters):
        page = doc.new_page(width=page_width, height=page_height)

        y = 72  # start 1 inch from top

        # Chapter title
        page.insert_text(
            pymupdf.Point(72, y),
            chapter_title,
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0.5),
        )
        y += 30

        # Page number
        page.insert_text(
            pymupdf.Point(page_width - 100, page_height - 40),
            f"Page {i + 1} of 20",
            fontsize=9,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        # Body paragraphs
        for para in paragraphs:
            rect = pymupdf.Rect(72, y, page_width - 72, page_height - 60)
            page.insert_textbox(
                rect,
                para + "\n\n",
                fontsize=11,
                fontname="helv",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )
            y += 175  # approximate paragraph height

        # Horizontal rule at bottom of content area
        shape = page.new_shape()
        shape.draw_line(
            pymupdf.Point(72, page_height - 56),
            pymupdf.Point(page_width - 72, page_height - 56)
        )
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
