"""
Initial Setup: Interleave pages from two PDFs to create a bilingual document
Task ID: pdf_ro_026
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_026'
DOCS_DIR = f'{WORKDIR}/Documents'

ENGLISH_PDF = f'{DOCS_DIR}/english.pdf'
SPANISH_PDF = f'{DOCS_DIR}/spanish.pdf'

# Topics for 10 chapters - each page covers the same topic in both languages
TOPICS_EN = [
    ("Chapter 1: Introduction to Sustainable Energy",
     "The global transition to sustainable energy represents one of the most significant "
     "shifts in modern industrial history. As fossil fuel reserves diminish and climate "
     "change accelerates, nations worldwide are investing heavily in renewable energy "
     "sources including solar, wind, hydroelectric, and geothermal power. This document "
     "explores the key technologies, economic implications, and policy frameworks that "
     "are shaping the future of energy production and consumption."),
    ("Chapter 2: Solar Power Technologies",
     "Solar photovoltaic (PV) systems have experienced dramatic cost reductions over the "
     "past decade, with module prices falling by approximately 89% since 2010. Modern "
     "monocrystalline silicon panels achieve efficiencies of 20-22% in commercial "
     "applications. Concentrated solar power (CSP) plants use mirrors to focus sunlight "
     "and generate steam for turbines, offering built-in thermal energy storage."),
    ("Chapter 3: Wind Energy Systems",
     "Onshore wind farms now generate electricity at costs competitive with natural gas "
     "in many regions. Modern turbines feature rotor diameters exceeding 150 meters and "
     "hub heights of 100+ meters. Offshore wind installations, while more expensive, "
     "benefit from stronger and more consistent wind patterns. The global installed wind "
     "capacity reached 906 GW by the end of 2023."),
    ("Chapter 4: Hydroelectric Power",
     "Hydroelectric generation remains the largest source of renewable electricity "
     "worldwide, accounting for approximately 16% of global electricity production. "
     "Large-scale dams like the Three Gorges Dam in China produce over 22,500 MW. "
     "Run-of-river systems and pumped-storage hydropower provide flexible generation "
     "without the environmental impact of large reservoirs."),
    ("Chapter 5: Energy Storage Solutions",
     "Lithium-ion battery costs have declined by 97% since 1991, reaching approximately "
     "$139 per kWh in 2023. Grid-scale battery installations are growing rapidly, with "
     "projects like the Moss Landing facility in California providing 400 MW / 1,600 MWh "
     "of storage capacity. Alternative technologies include flow batteries, compressed "
     "air energy storage, and green hydrogen production."),
    ("Chapter 6: Smart Grid Infrastructure",
     "The modernization of electrical grids is essential for integrating variable renewable "
     "energy sources. Smart grid technologies include advanced metering infrastructure (AMI), "
     "distribution automation, demand response systems, and real-time monitoring. "
     "These systems enable bidirectional power flow and optimize energy distribution "
     "across increasingly complex networks."),
    ("Chapter 7: Electric Transportation",
     "The electrification of transportation is accelerating globally. Electric vehicle "
     "sales exceeded 14 million units in 2023, representing 18% of all car sales. "
     "Charging infrastructure is expanding rapidly, with over 2.7 million public charging "
     "points installed worldwide. Fleet electrification of buses, trucks, and delivery "
     "vehicles is emerging as a major growth segment."),
    ("Chapter 8: Policy and Regulation",
     "Government policies play a critical role in accelerating the energy transition. "
     "Carbon pricing mechanisms now operate in 73 jurisdictions covering 23% of global "
     "greenhouse gas emissions. Renewable portfolio standards, feed-in tariffs, and "
     "tax incentives have proven effective in driving clean energy deployment. The "
     "Paris Agreement framework continues to guide international climate commitments."),
    ("Chapter 9: Economic Impact",
     "The renewable energy sector employed 13.7 million people globally in 2022, "
     "with solar PV being the largest employer at 4.9 million jobs. Investment in "
     "clean energy reached $1.8 trillion in 2023, surpassing fossil fuel investment "
     "for the first time. The levelized cost of energy from renewables is now lower "
     "than new fossil fuel plants in most markets worldwide."),
    ("Chapter 10: Future Outlook",
     "Emerging technologies such as perovskite solar cells, floating offshore wind, "
     "and advanced nuclear reactors promise to further expand clean energy options. "
     "The International Energy Agency projects that renewables will account for over "
     "90% of new electricity capacity additions through 2030. Achieving net-zero "
     "emissions by 2050 will require unprecedented investment and international cooperation."),
]

TOPICS_ES = [
    ("Capitulo 1: Introduccion a la Energia Sostenible",
     "La transicion global hacia la energia sostenible representa uno de los cambios mas "
     "significativos en la historia industrial moderna. A medida que las reservas de "
     "combustibles fosiles disminuyen y el cambio climatico se acelera, las naciones de "
     "todo el mundo estan invirtiendo fuertemente en fuentes de energia renovable, "
     "incluyendo solar, eolica, hidroelectrica y geotermica. Este documento explora las "
     "tecnologias clave, las implicaciones economicas y los marcos politicos."),
    ("Capitulo 2: Tecnologias de Energia Solar",
     "Los sistemas solares fotovoltaicos (FV) han experimentado reducciones dramaticas de "
     "costos durante la ultima decada, con precios de modulos cayendo aproximadamente un "
     "89% desde 2010. Los paneles modernos de silicio monocristalino alcanzan eficiencias "
     "del 20-22% en aplicaciones comerciales. Las plantas de energia solar concentrada "
     "(CSP) utilizan espejos para concentrar la luz solar y generar vapor para turbinas."),
    ("Capitulo 3: Sistemas de Energia Eolica",
     "Los parques eolicos terrestres ahora generan electricidad a costos competitivos con "
     "el gas natural en muchas regiones. Las turbinas modernas cuentan con diametros de "
     "rotor que superan los 150 metros y alturas de buje de mas de 100 metros. Las "
     "instalaciones eolicas marinas, aunque mas costosas, se benefician de patrones de "
     "viento mas fuertes y consistentes. La capacidad eolica mundial alcanzo 906 GW."),
    ("Capitulo 4: Energia Hidroelectrica",
     "La generacion hidroelectrica sigue siendo la mayor fuente de electricidad renovable "
     "a nivel mundial, representando aproximadamente el 16% de la produccion mundial de "
     "electricidad. Las grandes presas como la Presa de las Tres Gargantas en China "
     "producen mas de 22,500 MW. Los sistemas de pasada y el almacenamiento por bombeo "
     "proporcionan generacion flexible sin el impacto ambiental de grandes embalses."),
    ("Capitulo 5: Soluciones de Almacenamiento de Energia",
     "Los costos de las baterias de iones de litio han disminuido un 97% desde 1991, "
     "alcanzando aproximadamente $139 por kWh en 2023. Las instalaciones de baterias a "
     "escala de red estan creciendo rapidamente, con proyectos como Moss Landing en "
     "California proporcionando 400 MW / 1,600 MWh de capacidad. Las tecnologias "
     "alternativas incluyen baterias de flujo e hidrogeno verde."),
    ("Capitulo 6: Infraestructura de Redes Inteligentes",
     "La modernizacion de las redes electricas es esencial para integrar fuentes de "
     "energia renovable variable. Las tecnologias de redes inteligentes incluyen "
     "infraestructura de medicion avanzada (AMI), automatizacion de distribucion, "
     "sistemas de respuesta a la demanda y monitoreo en tiempo real. Estos sistemas "
     "permiten el flujo de energia bidireccional y optimizan la distribucion."),
    ("Capitulo 7: Transporte Electrico",
     "La electrificacion del transporte se esta acelerando a nivel mundial. Las ventas "
     "de vehiculos electricos superaron los 14 millones de unidades en 2023, "
     "representando el 18% de todas las ventas de automoviles. La infraestructura de "
     "carga se esta expandiendo rapidamente, con mas de 2.7 millones de puntos de "
     "carga publicos instalados en todo el mundo."),
    ("Capitulo 8: Politica y Regulacion",
     "Las politicas gubernamentales juegan un papel critico en la aceleracion de la "
     "transicion energetica. Los mecanismos de fijacion de precios del carbono ahora "
     "operan en 73 jurisdicciones que cubren el 23% de las emisiones mundiales de gases "
     "de efecto invernadero. Los estandares de cartera renovable, las tarifas de "
     "alimentacion y los incentivos fiscales han demostrado ser efectivos."),
    ("Capitulo 9: Impacto Economico",
     "El sector de energia renovable empleo a 13.7 millones de personas a nivel mundial "
     "en 2022, siendo la energia solar fotovoltaica el mayor empleador con 4.9 millones "
     "de empleos. La inversion en energia limpia alcanzo $1.8 billones en 2023, superando "
     "la inversion en combustibles fosiles por primera vez. El costo nivelado de la "
     "energia renovable es ahora mas bajo que las nuevas plantas de combustibles fosiles."),
    ("Capitulo 10: Perspectivas Futuras",
     "Las tecnologias emergentes como las celdas solares de perovskita, la eolica marina "
     "flotante y los reactores nucleares avanzados prometen ampliar aun mas las opciones "
     "de energia limpia. La Agencia Internacional de Energia proyecta que las renovables "
     "representaran mas del 90% de las adiciones de nueva capacidad electrica hasta 2030. "
     "Alcanzar emisiones netas cero para 2050 requerira inversion e cooperacion sin precedentes."),
]


def create_pdf(filepath, topics, lang_label):
    """Create a 10-page PDF document with chapter content."""
    doc = pymupdf.open()

    for i, (title, body) in enumerate(topics):
        page = doc.new_page(width=595, height=842)  # A4

        # Header bar
        shape = page.new_shape()
        header_rect = pymupdf.Rect(0, 0, 595, 60)
        shape.draw_rect(header_rect)
        if lang_label == "English":
            shape.finish(color=(0, 0, 0.5), fill=(0, 0.2, 0.6))
        else:
            shape.finish(color=(0.5, 0, 0), fill=(0.6, 0.15, 0))
        shape.commit()

        # Language label in header
        page.insert_text(
            pymupdf.Point(72, 38),
            f"{lang_label} Edition",
            fontsize=14,
            fontname="hebo",
            color=(1, 1, 1),
        )

        # Page number in header
        page.insert_text(
            pymupdf.Point(490, 38),
            f"Page {i + 1}",
            fontsize=12,
            fontname="helv",
            color=(1, 1, 1),
        )

        # Chapter title
        page.insert_text(
            pymupdf.Point(72, 110),
            title,
            fontsize=18,
            fontname="hebo",
            color=(0, 0, 0),
        )

        # Horizontal rule
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(72, 120), pymupdf.Point(523, 120))
        shape2.finish(color=(0.4, 0.4, 0.4), width=1)
        shape2.commit()

        # Body text
        text_rect = pymupdf.Rect(72, 145, 523, 780)
        page.insert_textbox(
            text_rect,
            body,
            fontsize=11,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Footer
        page.insert_text(
            pymupdf.Point(72, 820),
            f"Sustainable Energy Report 2024 - {lang_label}",
            fontsize=8,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(filepath)
    doc.close()
    print(f"Created {filepath} with {len(topics)} pages")


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Create the English PDF (10 pages)
    create_pdf(ENGLISH_PDF, TOPICS_EN, "English")

    # Create the Spanish PDF (10 pages)
    create_pdf(SPANISH_PDF, TOPICS_ES, "Spanish")

    # Open file manager showing Documents directory so agent can see files
    launch_gui(f'nautilus "{DOCS_DIR}"', delay_sec=2.0)

    # Open english.pdf in Evince so agent can inspect
    launch_gui(f'evince "{ENGLISH_PDF}"', delay_sec=2.0)

    print(f'Initial files created in {DOCS_DIR}')
    print('GUI_READY: launched Nautilus and Evince with DISPLAY=:0')


create_initial()
