"""
initial_setup.py — pdf_basic_045

Creates a fillable consent_form.pdf on the Desktop with:
  - Two unchecked checkboxes:
      * "agree_terms"  (label: "I agree to the terms and conditions")
      * "consent_data" (label: "I consent to data processing")
  - Two empty text fields:
      * "date_field"      (label: "Date")
      * "full_name_field" (label: "Full Name")

The file is placed at ~/Desktop/consent_form.pdf and opened in Evince.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

DESKTOP = "/home/user/Desktop"
OUTPUT = f"{DESKTOP}/consent_form.pdf"

os.makedirs(DESKTOP, exist_ok=True)

# ---------------------------------------------------------------------------
# Build the PDF
# ---------------------------------------------------------------------------
doc = pymupdf.open()
page = doc.new_page(width=595, height=842)  # A4

# --- Title ---
page.insert_text(
    pymupdf.Point(72, 72),
    "Consent Form",
    fontsize=22,
    fontname="hebo",
    color=(0, 0, 0),
)

# --- Introduction paragraph ---
intro = (
    "Please read the following statements carefully and indicate your consent "
    "by checking the appropriate boxes. Fill in your full name and the current "
    "date before submitting this form."
)
page.insert_textbox(
    pymupdf.Rect(72, 100, 523, 160),
    intro,
    fontsize=11,
    fontname="helv",
    color=(0, 0, 0),
    align=pymupdf.TEXT_ALIGN_LEFT,
)

# --- Checkbox 1: agree_terms ---
page.insert_text(
    pymupdf.Point(100, 195),
    "I agree to the terms and conditions",
    fontsize=12,
    fontname="helv",
    color=(0, 0, 0),
)
widget_cb1 = pymupdf.Widget()
widget_cb1.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
widget_cb1.field_name = "agree_terms"
widget_cb1.field_value = "Off"   # unchecked
widget_cb1.rect = pymupdf.Rect(72, 180, 95, 203)
widget_cb1.border_color = (0, 0, 0)
widget_cb1.border_width = 1
widget_cb1.fill_color = (1, 1, 1)
page.add_widget(widget_cb1)

# --- Checkbox 2: consent_data ---
page.insert_text(
    pymupdf.Point(100, 235),
    "I consent to data processing",
    fontsize=12,
    fontname="helv",
    color=(0, 0, 0),
)
widget_cb2 = pymupdf.Widget()
widget_cb2.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
widget_cb2.field_name = "consent_data"
widget_cb2.field_value = "Off"   # unchecked
widget_cb2.rect = pymupdf.Rect(72, 220, 95, 243)
widget_cb2.border_color = (0, 0, 0)
widget_cb2.border_width = 1
widget_cb2.fill_color = (1, 1, 1)
page.add_widget(widget_cb2)

# --- Date label + field ---
page.insert_text(
    pymupdf.Point(72, 295),
    "Date:",
    fontsize=12,
    fontname="hebo",
    color=(0, 0, 0),
)
widget_date = pymupdf.Widget()
widget_date.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
widget_date.field_name = "date_field"
widget_date.field_value = ""
widget_date.rect = pymupdf.Rect(130, 278, 350, 302)
widget_date.text_fontsize = 12
widget_date.fill_color = (0.95, 0.95, 0.95)
widget_date.border_color = (0, 0, 0)
widget_date.border_width = 1
page.add_widget(widget_date)

# --- Full Name label + field ---
page.insert_text(
    pymupdf.Point(72, 340),
    "Full Name:",
    fontsize=12,
    fontname="hebo",
    color=(0, 0, 0),
)
widget_name = pymupdf.Widget()
widget_name.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
widget_name.field_name = "full_name_field"
widget_name.field_value = ""
widget_name.rect = pymupdf.Rect(160, 323, 450, 347)
widget_name.text_fontsize = 12
widget_name.fill_color = (0.95, 0.95, 0.95)
widget_name.border_color = (0, 0, 0)
widget_name.border_width = 1
page.add_widget(widget_name)

# --- Signature line ---
shape = page.new_shape()
shape.draw_line(pymupdf.Point(72, 420), pymupdf.Point(350, 420))
shape.finish(color=(0, 0, 0), width=1)
shape.commit()
page.insert_text(
    pymupdf.Point(72, 435),
    "Signature",
    fontsize=10,
    fontname="helv",
    color=(0.4, 0.4, 0.4),
)

doc.save(OUTPUT)
doc.close()

# ---------------------------------------------------------------------------
# Verify fields were written correctly
# ---------------------------------------------------------------------------
doc_verify = pymupdf.open(OUTPUT)
fields = list(doc_verify[0].widgets())
doc_verify.close()
print(f"Created {OUTPUT} with {len(fields)} form field(s):")
for f in fields:
    print(f"  field_name={f.field_name!r}, type={f.field_type_string}, value={f.field_value!r}")

assert len(fields) == 4, f"Expected 4 fields, got {len(fields)}"
names = {f.field_name for f in fields}
assert names == {"agree_terms", "consent_data", "date_field", "full_name_field"}, \
    f"Unexpected field names: {names}"
print("All fields verified. Initial setup complete.")

# ---------------------------------------------------------------------------
# Open in Evince
# ---------------------------------------------------------------------------
def launch_gui(command: str, delay_sec: float = 2.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)

launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
print("Evince launched.")
