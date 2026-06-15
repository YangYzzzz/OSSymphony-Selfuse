"""
initial_setup.py — pdf_cross_067

Creates ~/Documents/renovation_report.pdf:
  A 6-page PDF report describing 5 renovation areas with before/after
  satisfaction scores and renovation costs.

The agent is then expected to:
  1. Read renovation_report.pdf
  2. Create renovation_showcase.odp with 6 slides (title + 5 comparison slides)
  3. Export it to renovation_showcase.pdf
"""

import os
import subprocess
import time

try:
    import fitz  # PyMuPDF
except ImportError:
    subprocess.run(["pip3", "install", "pymupdf"], check=True)
    import fitz


# ---------------------------------------------------------------------------
# Renovation data (matches task context exactly)
# ---------------------------------------------------------------------------
RENOVATION_AREAS = [
    {"area": "Lobby",            "cost": "$50,000", "before": 65, "after": 92},
    {"area": "Cafeteria",        "cost": "$35,000", "before": 58, "after": 88},
    {"area": "Conference Rooms", "cost": "$28,000", "before": 70, "after": 95},
    {"area": "Parking",          "cost": "$45,000", "before": 55, "after": 85},
    {"area": "Restrooms",        "cost": "$22,000", "before": 60, "after": 90},
]

DOCS_DIR = os.path.expanduser("~/Documents")
PDF_PATH = os.path.join(DOCS_DIR, "renovation_report.pdf")


def create_renovation_report():
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = fitz.open()

    # ------------------------------------------------------------------
    # Page 1 — Cover / Executive Summary
    # ------------------------------------------------------------------
    page = doc.new_page(width=612, height=792)
    y = 80

    # Title
    page.insert_text(
        (50, y), "Office Renovation Report 2024",
        fontsize=28, fontname="helv", color=(0.1, 0.2, 0.5)
    )
    y += 50
    page.insert_text(
        (50, y), "Before & After Comparison — Satisfaction Analysis",
        fontsize=16, fontname="helv", color=(0.3, 0.3, 0.3)
    )
    y += 60

    # Horizontal rule (drawn as a thin rectangle)
    page.draw_rect(fitz.Rect(50, y, 562, y + 2), color=(0.2, 0.4, 0.7), fill=(0.2, 0.4, 0.7))
    y += 20

    page.insert_text(
        (50, y), "Executive Summary",
        fontsize=18, fontname="helv", color=(0.1, 0.2, 0.5)
    )
    y += 30

    summary_lines = [
        "This report summarises the impact of the 2024 office renovation programme",
        "across five key areas. Satisfaction scores were collected via anonymous",
        "staff surveys (scale 0–100) before and after each renovation phase.",
        "",
        "Total renovation investment: $180,000",
        "Areas renovated: 5",
        "Average satisfaction improvement: +29 points",
    ]
    for line in summary_lines:
        page.insert_text((50, y), line, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 16

    y += 20
    # Summary table header
    page.insert_text((50, y), "Area Overview", fontsize=14, fontname="helv",
                     color=(0.1, 0.2, 0.5))
    y += 25

    # Table header row
    cols = [50, 200, 340, 420, 500]
    headers = ["Area", "Cost", "Before (%)", "After (%)", "Change"]
    for i, h in enumerate(headers):
        page.insert_text((cols[i], y), h, fontsize=10, fontname="helv",
                         color=(1, 1, 1))
        page.draw_rect(
            fitz.Rect(cols[i] - 3, y - 14, (cols[i + 1] - 3 if i < 4 else 570), y + 4),
            color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5)
        )
    y += 20

    for idx, area in enumerate(RENOVATION_AREAS):
        bg = (0.93, 0.96, 1.0) if idx % 2 == 0 else (1, 1, 1)
        page.draw_rect(fitz.Rect(47, y - 12, 570, y + 6), color=bg, fill=bg)
        change = area["after"] - area["before"]
        row = [
            area["area"],
            area["cost"],
            f"{area['before']}%",
            f"{area['after']}%",
            f"+{change}%",
        ]
        for i, val in enumerate(row):
            page.insert_text((cols[i], y), val, fontsize=10, fontname="helv",
                             color=(0, 0, 0))
        y += 20

    doc.save(PDF_PATH)

    # ------------------------------------------------------------------
    # Pages 2–6 — One detailed page per renovation area
    # ------------------------------------------------------------------
    for area in RENOVATION_AREAS:
        page = doc.new_page(width=612, height=792)
        y = 60

        # Area title banner
        page.draw_rect(fitz.Rect(0, 40, 612, 100), color=(0.1, 0.2, 0.5),
                       fill=(0.1, 0.2, 0.5))
        page.insert_text((30, 78), f"Renovation Area: {area['area']}",
                         fontsize=22, fontname="helv", color=(1, 1, 1))
        y = 130

        # Cost
        page.insert_text((50, y), f"Renovation Cost: {area['cost']}",
                         fontsize=14, fontname="helv", color=(0.2, 0.2, 0.2))
        y += 40

        # Before / After section headers
        page.draw_rect(fitz.Rect(50, y, 280, y + 30), color=(0.85, 0.1, 0.1),
                       fill=(0.85, 0.1, 0.1))
        page.insert_text((60, y + 20), "BEFORE Renovation",
                         fontsize=13, fontname="helv", color=(1, 1, 1))

        page.draw_rect(fitz.Rect(320, y, 560, y + 30), color=(0.1, 0.65, 0.2),
                       fill=(0.1, 0.65, 0.2))
        page.insert_text((330, y + 20), "AFTER Renovation",
                         fontsize=13, fontname="helv", color=(1, 1, 1))
        y += 55

        # Satisfaction scores
        page.insert_text((80, y), f"Satisfaction Score: {area['before']}%",
                         fontsize=20, fontname="helv", color=(0.7, 0.1, 0.1))
        page.insert_text((340, y), f"Satisfaction Score: {area['after']}%",
                         fontsize=20, fontname="helv", color=(0.1, 0.55, 0.1))
        y += 50

        # Improvement callout
        improvement = area["after"] - area["before"]
        page.draw_rect(fitz.Rect(150, y, 460, y + 50), color=(0.95, 0.95, 0.7),
                       fill=(0.95, 0.95, 0.7))
        page.insert_text((165, y + 15),
                         f"Satisfaction improvement: +{improvement} points",
                         fontsize=14, fontname="helv", color=(0.2, 0.2, 0))
        page.insert_text((165, y + 35),
                         f"Percentage gain: +{improvement}%",
                         fontsize=12, fontname="helv", color=(0.2, 0.2, 0))
        y += 80

        # Description blurb
        descs = {
            "Lobby": [
                "The lobby was completely redesigned with modern aesthetics,",
                "improved lighting, and comfortable seating arrangements.",
                "The reception desk was relocated to improve traffic flow.",
            ],
            "Cafeteria": [
                "New kitchen equipment, improved ventilation, and an expanded",
                "seating area transformed the cafeteria experience.",
                "A variety of healthy food options were added to the menu.",
            ],
            "Conference Rooms": [
                "State-of-the-art AV equipment, ergonomic furniture, and",
                "soundproofing upgrades elevated the meeting experience.",
                "Booking systems were also digitalised for convenience.",
            ],
            "Parking": [
                "Additional bays, improved lighting, and a new ticketing system",
                "drastically reduced staff complaints about parking access.",
                "EV charging stations were added as a sustainability measure.",
            ],
            "Restrooms": [
                "Full refurbishment with modern fixtures, automatic fittings,",
                "and improved ventilation addressed longstanding concerns.",
                "Touchless dispensers and sensor-activated lighting were installed.",
            ],
        }
        for line in descs.get(area["area"], []):
            page.insert_text((50, y), line, fontsize=11, fontname="helv",
                             color=(0, 0, 0))
            y += 16

    doc.save(PDF_PATH)
    doc.close()
    print(f"Created: {PDF_PATH}")
    return PDF_PATH


def launch_evince(pdf_path):
    """Open the PDF in Evince so the agent can see the source document."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        ["evince", pdf_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(2)


if __name__ == "__main__":
    pdf_path = create_renovation_report()
    launch_evince(pdf_path)
    print("Setup complete. Agent should now create renovation_showcase.odp from the PDF.")
