"""
Initial Setup: survey_results.odt with JSON array of 10 survey response objects
Task ID: osworld_multi_apps_json_reformat_writer_006
Domain: libreoffice_writer

Creates /home/user/Documents/survey_results.odt containing a raw JSON array
of 10 survey response objects. No table, no formatting — just raw JSON text.
Three responses have ratings < 3 (ratings: 2, 1, 2), others have ratings 3-5.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user/Documents'
FILENAME = 'survey_results.odt'
OUTPUT = f'{WORKDIR}/{FILENAME}'


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

    # Survey data: 10 records, 3 with rating < 3 (ratings 2, 1, 2)
    survey_data = [
        {"respondent_id": "R001", "age": 34, "gender": "Female", "rating": 4, "comment": "Very satisfied with the service overall."},
        {"respondent_id": "R002", "age": 28, "gender": "Male",   "rating": 2, "comment": "Product quality was disappointing."},
        {"respondent_id": "R003", "age": 45, "gender": "Female", "rating": 5, "comment": "Excellent experience, highly recommend!"},
        {"respondent_id": "R004", "age": 22, "gender": "Male",   "rating": 3, "comment": "Average experience, nothing special."},
        {"respondent_id": "R005", "age": 31, "gender": "Non-binary", "rating": 1, "comment": "Terrible customer support, will not return."},
        {"respondent_id": "R006", "age": 55, "gender": "Female", "rating": 4, "comment": "Generally happy with my purchase."},
        {"respondent_id": "R007", "age": 39, "gender": "Male",   "rating": 5, "comment": "Outstanding quality and fast delivery."},
        {"respondent_id": "R008", "age": 26, "gender": "Female", "rating": 2, "comment": "Item arrived damaged, very unhappy."},
        {"respondent_id": "R009", "age": 48, "gender": "Male",   "rating": 3, "comment": "Decent product but overpriced."},
        {"respondent_id": "R010", "age": 33, "gender": "Female", "rating": 5, "comment": "Fantastic! Will definitely buy again."},
    ]

    json_text = json.dumps(survey_data, indent=2)

    # Use odfpy to create the ODT file with the JSON text
    from odf.opendocument import OpenDocumentText
    from odf.text import P
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf import style as odf_style

    doc = OpenDocumentText()

    # Create a monospace style for JSON
    mono_style = Style(name="JSONText", family="paragraph")
    mono_style.addElement(TextProperties(fontfamily="Courier New", fontsize="10pt"))
    doc.automaticstyles.addElement(mono_style)

    # Add the JSON as lines of text
    for line in json_text.split('\n'):
        p = P(stylename="JSONText", text=line if line else "")
        doc.text.addElement(p)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
