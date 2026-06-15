"""
Initial Setup: formatted_refs.odt with 5 APA references (no DOI lines)
Task ID: osworld_multi_apps_doi_resolve_writer_004
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import P, Span, LineBreak

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_004'
OUTPUT = f'{WORKDIR}/formatted_refs.odt'


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
    doc = OpenDocumentText()

    # Define a normal paragraph style
    normal_style = Style(name="NormalRef", family="paragraph")
    normal_style.addElement(ParagraphProperties(
        attributes={
            "marginleft": "0in",
            "textindent": "-0.5in",
            "marginright": "0in",
            "marginbottom": "0.1in",
            "margintop": "0in",
        }
    ))
    normal_style.addElement(TextProperties(attributes={
        "fontsize": "12pt",
        "fontfamily": "Times New Roman",
    }))
    doc.styles.addElement(normal_style)

    # 5 APA-formatted references WITHOUT any DOI lines
    references = [
        (
            "Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., "
            "Kaiser, Ł., & Polosukhin, I. "
            "Attention Is All You Need. "
            "In "
            "Advances in Neural Information Processing Systems, 30. "
            "(2017)."
        ),
        (
            "Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. "
            "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. "
            "In "
            "Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers) "
            "(pp. 4171–4186). Association for Computational Linguistics. "
            "(2019)."
        ),
        (
            "Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., "
            "Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., "
            "Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D., Wu, J., Winter, C., … Amodei, D. "
            "Language Models are Few-Shot Learners. "
            "In "
            "Advances in Neural Information Processing Systems, 33 "
            "(pp. 1877–1901). Curran Associates, Inc. "
            "(2020)."
        ),
        (
            "Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., "
            "Zhang, C., Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J., Kelton, F., "
            "Miller, L., Simens, M., Askell, A., Welinder, P., Christiano, P. F., Leike, J., & Lowe, R. "
            "Training language models to follow instructions with human feedback. "
            "In "
            "Advances in Neural Information Processing Systems, 35 "
            "(pp. 27730–27744). Curran Associates, Inc. "
            "(2022)."
        ),
        (
            "Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., "
            "Rozière, B., Goyal, N., Hambro, E., Azhar, F., Rodriguez, A., Joulin, A., Grave, E., & Lample, G. "
            "LLaMA: Open and Efficient Foundation Language Models. "
            "arXiv preprint arXiv:2302.13971. "
            "(2023)."
        ),
    ]

    for ref_text in references:
        p = P(stylename="NormalRef", text=ref_text)
        doc.text.addElement(p)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
