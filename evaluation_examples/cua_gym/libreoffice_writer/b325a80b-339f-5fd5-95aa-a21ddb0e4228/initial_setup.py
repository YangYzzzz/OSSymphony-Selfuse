"""
Initial Setup: Create encyclopedia master document with subdocuments containing index entries
Task ID: writer_rm_070
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_070'
SUBDIR = f'{WORKDIR}/encyclopedia'

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

# --- Subdocument data: (filename, title, paragraphs_with_index_entries) ---
# Each paragraph is (text, [(term, start_offset, end_offset), ...])
# We'll embed AlphabeticalIndexMark elements for key terms

SUBDOCUMENTS = [
    {
        "filename": "01_astronomy.odt",
        "title": "Astronomy",
        "paragraphs": [
            ("The study of celestial objects includes planets, stars, and galaxies. Astronomy has been practiced since ancient civilizations first observed the night sky.",
             ["Astronomy", "planets", "stars", "galaxies"]),
            ("The Milky Way galaxy contains over 100 billion stars. Our solar system orbits within one of its spiral arms.",
             ["Milky Way", "solar system"]),
            ("Telescopes have revolutionized our understanding of the cosmos. The Hubble Space Telescope has captured images of distant nebulae.",
             ["Telescopes", "Hubble Space Telescope", "nebulae"]),
        ]
    },
    {
        "filename": "02_biology.odt",
        "title": "Biology",
        "paragraphs": [
            ("Biology is the scientific study of life and living organisms. It encompasses fields from molecular biology to ecology.",
             ["Biology", "molecular biology", "ecology"]),
            ("DNA contains the genetic instructions for the development of all known living organisms. The double helix structure was discovered in 1953.",
             ["DNA", "double helix", "genetic instructions"]),
            ("Photosynthesis is the process by which plants convert sunlight into chemical energy. Chlorophyll absorbs light primarily in the blue and red wavelengths.",
             ["Photosynthesis", "Chlorophyll"]),
        ]
    },
    {
        "filename": "03_chemistry.odt",
        "title": "Chemistry",
        "paragraphs": [
            ("Chemistry investigates the composition, structure, and properties of matter. The periodic table organizes elements by their atomic number.",
             ["Chemistry", "periodic table", "atomic number"]),
            ("Chemical bonds hold atoms together in molecules. Covalent bonds involve sharing electrons between atoms.",
             ["Chemical bonds", "Covalent bonds", "molecules"]),
            ("Catalysts speed up chemical reactions without being consumed. Enzymes are biological catalysts essential for metabolism.",
             ["Catalysts", "Enzymes", "metabolism"]),
        ]
    },
    {
        "filename": "04_geography.odt",
        "title": "Geography",
        "paragraphs": [
            ("Geography studies the lands, features, and inhabitants of Earth. Physical geography examines natural landforms and climate patterns.",
             ["Geography", "Physical geography", "climate"]),
            ("Tectonic plates drift slowly across the Earth's surface, causing earthquakes and volcanic eruptions along plate boundaries.",
             ["Tectonic plates", "earthquakes", "volcanic eruptions"]),
            ("The Amazon River basin contains the largest tropical rainforest on Earth, supporting extraordinary biodiversity.",
             ["Amazon River", "tropical rainforest", "biodiversity"]),
        ]
    },
    {
        "filename": "05_history.odt",
        "title": "History",
        "paragraphs": [
            ("The Renaissance marked a period of cultural rebirth in Europe beginning in the 14th century. Art, science, and philosophy flourished during this era.",
             ["Renaissance", "cultural rebirth"]),
            ("The Industrial Revolution transformed manufacturing through mechanization. Steam engines powered factories across England in the 18th century.",
             ["Industrial Revolution", "Steam engines", "mechanization"]),
            ("Ancient civilizations such as Mesopotamia and Egypt developed writing systems, agriculture, and complex social structures.",
             ["Mesopotamia", "Egypt", "writing systems", "agriculture"]),
        ]
    },
    {
        "filename": "06_mathematics.odt",
        "title": "Mathematics",
        "paragraphs": [
            ("Mathematics provides the language for describing patterns and relationships. Algebra, geometry, and calculus form the foundation of modern mathematics.",
             ["Mathematics", "Algebra", "geometry", "calculus"]),
            ("The Pythagorean theorem relates the sides of a right triangle. It remains one of the most fundamental results in Euclidean geometry.",
             ["Pythagorean theorem", "Euclidean geometry"]),
            ("Probability theory quantifies uncertainty and forms the basis of statistics. Bayesian inference updates beliefs based on new evidence.",
             ["Probability theory", "statistics", "Bayesian inference"]),
        ]
    },
    {
        "filename": "07_physics.odt",
        "title": "Physics",
        "paragraphs": [
            ("Physics explores the fundamental laws governing the universe. Newton's laws of motion describe the relationship between forces and movement.",
             ["Physics", "Newton's laws", "forces"]),
            ("Quantum mechanics describes behavior at the subatomic level. The uncertainty principle limits simultaneous knowledge of position and momentum.",
             ["Quantum mechanics", "uncertainty principle"]),
            ("Einstein's theory of relativity revolutionized our understanding of space, time, and gravity. E=mc^2 relates mass and energy.",
             ["relativity", "Einstein", "gravity"]),
        ]
    },
    {
        "filename": "08_technology.odt",
        "title": "Technology",
        "paragraphs": [
            ("The invention of the transistor in 1947 launched the electronics revolution. Integrated circuits now contain billions of transistors.",
             ["transistor", "electronics", "Integrated circuits"]),
            ("The internet connects billions of devices worldwide. The World Wide Web was invented by Tim Berners-Lee in 1989.",
             ["internet", "World Wide Web", "Tim Berners-Lee"]),
            ("Artificial intelligence aims to create systems that can learn and reason. Machine learning algorithms improve through experience with data.",
             ["Artificial intelligence", "Machine learning"]),
        ]
    },
    {
        "filename": "09_medicine.odt",
        "title": "Medicine",
        "paragraphs": [
            ("Modern medicine encompasses diagnosis, treatment, and prevention of disease. Vaccination has eradicated smallpox and controlled many infectious diseases.",
             ["Medicine", "Vaccination", "smallpox"]),
            ("Antibiotics revolutionized the treatment of bacterial infections. Alexander Fleming discovered penicillin in 1928.",
             ["Antibiotics", "penicillin", "Alexander Fleming"]),
            ("Genomic medicine uses DNA sequencing to personalize treatment. Precision medicine tailors therapies to individual genetic profiles.",
             ["Genomic medicine", "DNA sequencing", "Precision medicine"]),
        ]
    },
    {
        "filename": "10_ecology.odt",
        "title": "Ecology",
        "paragraphs": [
            ("Ecology studies the interactions between organisms and their environment. Ecosystems include biotic and abiotic components working together.",
             ["Ecology", "Ecosystems"]),
            ("Food chains describe the flow of energy through trophic levels. Producers, consumers, and decomposers form interconnected food webs.",
             ["Food chains", "trophic levels", "food webs"]),
            ("Conservation biology seeks to protect endangered species and habitats. Habitat loss remains the primary threat to global biodiversity.",
             ["Conservation biology", "endangered species", "Habitat loss"]),
        ]
    },
]


def create_odt_subdocument(filepath, title, paragraphs):
    """Create an ODT subdocument with index entries marked on key terms."""
    from odf.opendocument import OpenDocumentText
    from odf import text as odftext

    doc = OpenDocumentText()

    # Add title heading
    heading = odftext.H(outlinelevel=1, stylename="Heading_20_1")
    heading.addText(title)
    doc.text.addElement(heading)

    # Add paragraphs with index entries
    for para_text, index_terms in paragraphs:
        p = odftext.P(stylename="Text_20_body")

        # Add the paragraph text
        p.addText(para_text)

        # Add alphabetical index marks for each term (inline markers)
        for term in index_terms:
            mark = odftext.AlphabeticalIndexMark(stringvalue=term)
            p.addElement(mark)

        doc.text.addElement(p)

    doc.save(filepath)
    print(f"Created subdocument: {filepath}")


def create_master_document(master_path, subdoc_paths):
    """Create an ODM master document referencing subdocuments.

    An ODM is an ODF document with text:section elements that link to subdocuments.
    We'll build it using odfpy.
    """
    from odf.opendocument import OpenDocumentText
    from odf import text as odftext
    from odf import style as odfstyle

    doc = OpenDocumentText()

    # Add a title
    heading = odftext.H(outlinelevel=1, stylename="Heading_20_1")
    heading.addText("Encyclopedia of Knowledge")
    doc.text.addElement(heading)

    intro = odftext.P(stylename="Text_20_body")
    intro.addText("This master document compiles knowledge from ten subject areas. Each chapter covers a distinct discipline with key terms marked for indexing.")
    doc.text.addElement(intro)

    # Add sections linking to subdocuments
    for i, subdoc_path in enumerate(subdoc_paths):
        section_name = f"Section_{i+1:02d}"
        filename = os.path.basename(subdoc_path)

        # Create a text:section with a text:section-source child
        section = odftext.Section(name=section_name)

        # SectionSource holds the xlink:href to the subdocument
        section_source = odftext.SectionSource()
        section_source.setAttrNS('http://www.w3.org/1999/xlink', 'xlink:href', filename)
        section_source.setAttrNS('http://www.w3.org/1999/xlink', 'xlink:type', 'simple')
        section.addElement(section_source)

        # Add a placeholder paragraph in the section
        p = odftext.P(stylename="Text_20_body")
        p.addText(f"[Content from {filename}]")
        section.addElement(p)

        doc.text.addElement(section)

    # Save as .odm (master document)
    # odfpy saves as .odt by default; .odm has the same structure
    # but uses a different mimetype. We'll save as .odt first then fix mimetype.
    doc.save(master_path)
    print(f"Created master document: {master_path}")


def fix_odm_mimetype(filepath):
    """Convert an .odt to .odm by changing the mimetype inside the ZIP."""
    import tempfile
    temp_path = filepath + '.tmp'

    with zipfile.ZipFile(filepath, 'r') as zin:
        with zipfile.ZipFile(temp_path, 'w') as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'mimetype':
                    data = b'application/vnd.oasis.opendocument.text-master'
                zout.writestr(item, data)

    shutil.move(temp_path, filepath)
    print(f"Fixed mimetype for: {filepath}")


def create_initial():
    # Create subdocument directory
    os.makedirs(SUBDIR, exist_ok=True)

    # Create all subdocuments
    subdoc_paths = []
    for subdoc_info in SUBDOCUMENTS:
        filepath = os.path.join(SUBDIR, subdoc_info['filename'])
        create_odt_subdocument(filepath, subdoc_info['title'], subdoc_info['paragraphs'])
        subdoc_paths.append(filepath)

    # Create master document
    master_path = f'{WORKDIR}/{TASK_ID}.odm'
    create_master_document(master_path, subdoc_paths)
    fix_odm_mimetype(master_path)

    # Also create copies of subdocuments in the same directory as the master
    # (LibreOffice resolves relative paths from the master document location)
    for subdoc_info in SUBDOCUMENTS:
        src = os.path.join(SUBDIR, subdoc_info['filename'])
        dst = os.path.join(WORKDIR, subdoc_info['filename'])
        shutil.copy2(src, dst)

    print(f"Initial master document created: {master_path}")
    print(f"Subdocuments created in: {SUBDIR}")
    print(f"Subdocument copies in: {WORKDIR}")

    # GUI-ready: open master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{master_path}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with master document on DISPLAY=:0')


create_initial()
