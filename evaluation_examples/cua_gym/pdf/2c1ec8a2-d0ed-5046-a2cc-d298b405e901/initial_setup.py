"""
Initial Setup: Create safety_data_sheet.pdf (8 pages) on ~/Desktop.
Task ID: pdf_basic_133
Domain: pdf

Task: Open ~/Desktop/safety_data_sheet.pdf in Evince, navigate to page 3,
      and add a red highlight over 'DANGER: Highly flammable'. Add an underline
      to 'Keep away from heat sources' on the same page. Save the document.

This script:
  1. Creates a realistic 8-page Safety Data Sheet (SDS) PDF.
  2. Ensures 'DANGER: Highly flammable' and 'Keep away from heat sources'
     appear on page 3 with NO annotations (the task is to add them).
  3. Places it at ~/Desktop/safety_data_sheet.pdf.
  4. Opens the PDF in Evince at page 3.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DESKTOP = os.path.expanduser("~/Desktop")
os.makedirs(DESKTOP, exist_ok=True)

PDF_PATH = os.path.join(DESKTOP, "safety_data_sheet.pdf")

# ---------------------------------------------------------------------------
# GUI launcher
# ---------------------------------------------------------------------------
def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


# ---------------------------------------------------------------------------
# Helper: draw a section header bar
# ---------------------------------------------------------------------------
def draw_header_bar(page, y0, y1, color=(0.15, 0.25, 0.55)):
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(36, y0, 576, y1))
    shape.finish(fill=color, color=None)
    shape.commit()


# ---------------------------------------------------------------------------
# Helper: insert wrapped text block
# ---------------------------------------------------------------------------
def insert_textbox(page, rect, text, fontsize=10, fontname="helv", color=(0, 0, 0), align=0):
    page.insert_textbox(
        rect,
        text,
        fontsize=fontsize,
        fontname=fontname,
        color=color,
        align=align,
    )


# ---------------------------------------------------------------------------
# Page 1: Product Identification & Composition
# ---------------------------------------------------------------------------
def build_page1(doc):
    page = doc.new_page(width=612, height=792)

    # Title header
    draw_header_bar(page, 36, 80, (0.12, 0.20, 0.50))
    page.insert_text(pymupdf.Point(48, 65), "SAFETY DATA SHEET", fontsize=18, fontname="hebo", color=(1, 1, 1))

    # Document info
    page.insert_text(pymupdf.Point(36, 100), "Product Name: PyroClean Industrial Solvent 750", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(36, 116), "SDS Number: SDS-PC750-2024", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(36, 132), "Revision Date: January 15, 2024", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(36, 148), "Version: 4.2", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(36, 164), "Supersedes: Version 4.1 dated March 2023", fontsize=10, fontname="helv")

    draw_header_bar(page, 185, 200, (0.12, 0.20, 0.50))
    page.insert_text(pymupdf.Point(40, 196), "SECTION 1: PRODUCT AND COMPANY IDENTIFICATION", fontsize=9, fontname="hebo", color=(1, 1, 1))

    page.insert_textbox(
        pymupdf.Rect(36, 208, 576, 340),
        "Product Identifier: PyroClean Industrial Solvent 750\n"
        "Trade Names: PC-750, PyroClean 750 Concentrate\n"
        "Chemical Family: Aliphatic Hydrocarbons / Petroleum Distillates\n"
        "CAS Number: 64742-88-7\n"
        "UN Number: UN1268 — Petroleum Distillates, n.o.s.\n\n"
        "Manufacturer / Distributor:\n"
        "  ChemSafe Industrial Products Inc.\n"
        "  4200 Industrial Park Road, Suite 300\n"
        "  Houston, TX 77084, USA\n"
        "  Tel: +1 (832) 555-0181\n"
        "  Emergency: +1 (800) 555-CHEM (24 hrs)\n"
        "  Website: www.chemsafe-industrial.com",
        fontsize=10, fontname="helv",
    )

    draw_header_bar(page, 360, 375, (0.12, 0.20, 0.50))
    page.insert_text(pymupdf.Point(40, 371), "SECTION 2: COMPOSITION / INFORMATION ON INGREDIENTS", fontsize=9, fontname="hebo", color=(1, 1, 1))

    # Table header
    draw_header_bar(page, 383, 396, (0.70, 0.75, 0.85))
    page.insert_text(pymupdf.Point(40, 393), "Component", fontsize=9, fontname="hebo")
    page.insert_text(pymupdf.Point(220, 393), "CAS No.", fontsize=9, fontname="hebo")
    page.insert_text(pymupdf.Point(320, 393), "% w/w", fontsize=9, fontname="hebo")
    page.insert_text(pymupdf.Point(420, 393), "OSHA PEL", fontsize=9, fontname="hebo")

    rows = [
        ("Petroleum naphtha", "8030-30-6", "55–65%", "400 ppm TWA"),
        ("n-Heptane", "142-82-5", "15–25%", "500 ppm TWA"),
        ("Isopropyl alcohol", "67-63-0", "8–12%", "400 ppm TWA"),
        ("Ethyl acetate", "141-78-6", "3–7%", "400 ppm TWA"),
        ("Proprietary additives", "Trade Secret", "<2%", "N/A"),
    ]
    for i, (comp, cas, pct, pel) in enumerate(rows):
        y = 408 + i * 15
        bg = (0.94, 0.95, 0.97) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(36, y - 3, 576, y + 11))
        shape.finish(fill=bg, color=None)
        shape.commit()
        page.insert_text(pymupdf.Point(40, y + 8), comp, fontsize=8, fontname="helv")
        page.insert_text(pymupdf.Point(220, y + 8), cas, fontsize=8, fontname="helv")
        page.insert_text(pymupdf.Point(320, y + 8), pct, fontsize=8, fontname="helv")
        page.insert_text(pymupdf.Point(420, y + 8), pel, fontsize=8, fontname="helv")

    # Footer
    page.insert_text(pymupdf.Point(36, 758), f"PyroClean Industrial Solvent 750 — SDS-PC750-2024 — Page 1 of 8", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(500, 758), "CONFIDENTIAL", fontsize=8, fontname="hebo", color=(0.6, 0.1, 0.1))


# ---------------------------------------------------------------------------
# Page 2: Physical/Chemical Properties
# ---------------------------------------------------------------------------
def build_page2(doc):
    page = doc.new_page(width=612, height=792)

    draw_header_bar(page, 36, 55)
    page.insert_text(pymupdf.Point(40, 50), "SAFETY DATA SHEET — SDS-PC750-2024", fontsize=11, fontname="hebo", color=(1, 1, 1))

    draw_header_bar(page, 65, 80)
    page.insert_text(pymupdf.Point(40, 76), "SECTION 9: PHYSICAL AND CHEMICAL PROPERTIES", fontsize=9, fontname="hebo", color=(1, 1, 1))

    props = [
        ("Appearance:", "Clear, colorless to pale yellow liquid"),
        ("Odor:", "Petroleum/hydrocarbon, mild aromatic"),
        ("Odor threshold:", "Approximately 50 ppm"),
        ("pH:", "Not applicable"),
        ("Boiling point:", "90–210°C (194–410°F) at 1 atm"),
        ("Flash point:", "< 23°C (73°F) (closed cup, Pensky-Martens)"),
        ("Evaporation rate:", "Faster than n-butyl acetate (ref = 1.0)"),
        ("Flammability:", "Highly flammable liquid and vapor"),
        ("Explosive limits (LEL):", "0.7% v/v"),
        ("Explosive limits (UEL):", "8.0% v/v"),
        ("Vapor pressure:", "15–40 mmHg at 20°C"),
        ("Vapor density:", "3.5 (air = 1); vapors are heavier than air"),
        ("Relative density:", "0.72–0.77 g/mL at 20°C"),
        ("Solubility in water:", "Negligible (<0.01% at 20°C)"),
        ("Partition coefficient:", "log Kow = 3.5–5.5 (estimated)"),
        ("Auto-ignition temperature:", "240°C (464°F)"),
        ("Viscosity:", "1.2–2.1 cSt at 40°C"),
        ("Molecular weight:", "~100–140 g/mol (mixture)"),
    ]

    for i, (prop, val) in enumerate(props):
        y = 100 + i * 22
        bg = (0.95, 0.96, 0.98) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(36, y, 576, y + 20))
        shape.finish(fill=bg, color=None)
        shape.commit()
        page.insert_text(pymupdf.Point(40, y + 14), prop, fontsize=9, fontname="hebo")
        page.insert_text(pymupdf.Point(190, y + 14), val, fontsize=9, fontname="helv")

    draw_header_bar(page, 502, 517)
    page.insert_text(pymupdf.Point(40, 513), "SECTION 10: STABILITY AND REACTIVITY", fontsize=9, fontname="hebo", color=(1, 1, 1))

    page.insert_textbox(
        pymupdf.Rect(36, 525, 576, 640),
        "Chemical stability: Stable under normal storage and handling conditions.\n"
        "Conditions to avoid: Heat, sparks, open flames, static discharge, and incompatible materials.\n"
        "Incompatible materials: Strong oxidizing agents, acids, bases, halogens.\n"
        "Hazardous decomposition: CO, CO2, and unburned hydrocarbons upon combustion.\n"
        "Hazardous polymerization: Will not occur under normal conditions.",
        fontsize=9, fontname="helv",
    )

    page.insert_text(pymupdf.Point(36, 770), "PyroClean Industrial Solvent 750 — SDS-PC750-2024 — Page 2 of 8", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))


# ---------------------------------------------------------------------------
# Page 3: Hazard Identification (contains the target text)
# ---------------------------------------------------------------------------
def build_page3(doc):
    """Page 3 contains 'DANGER: Highly flammable' and 'Keep away from heat sources'."""
    page = doc.new_page(width=612, height=792)

    draw_header_bar(page, 36, 55)
    page.insert_text(pymupdf.Point(40, 50), "SAFETY DATA SHEET — SDS-PC750-2024", fontsize=11, fontname="hebo", color=(1, 1, 1))

    draw_header_bar(page, 65, 80)
    page.insert_text(pymupdf.Point(40, 76), "SECTION 2: HAZARD IDENTIFICATION (GHS / OSHA HCS 2012)", fontsize=9, fontname="hebo", color=(1, 1, 1))

    # GHS Classification box
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 90, 576, 106))
    shape.finish(fill=(0.95, 0.90, 0.85), color=(0.6, 0.3, 0.1), width=1)
    shape.commit()
    page.insert_text(pymupdf.Point(40, 102), "GHS Classification — Flammable Liquids, Category 2 | Aspiration Hazard, Category 1 | Specific Target Organ Toxicity — Single Exposure, Category 3", fontsize=7.5, fontname="hebo", color=(0.5, 0.2, 0.0))

    # ---- SIGNAL WORD: DANGER ----
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 114, 576, 152))
    shape.finish(fill=(0.98, 0.93, 0.90), color=(0.70, 0.10, 0.10), width=1.5)
    shape.commit()

    page.insert_text(pymupdf.Point(48, 132), "SIGNAL WORD:", fontsize=11, fontname="hebo", color=(0.60, 0.10, 0.10))
    # The key text 'DANGER: Highly flammable' — this is what the agent must highlight
    page.insert_text(pymupdf.Point(165, 132), "DANGER: Highly flammable", fontsize=12, fontname="hebo", color=(0.80, 0.05, 0.05))
    page.insert_text(pymupdf.Point(48, 148), "liquid and vapor. Fatal if swallowed and enters airways.", fontsize=9, fontname="helv", color=(0.30, 0.05, 0.05))

    # GHS Pictograms note
    page.insert_text(pymupdf.Point(36, 168), "GHS Pictograms: Flame (GHS02), Exclamation Mark (GHS07), Health Hazard (GHS08)", fontsize=8.5, fontname="helv", color=(0.2, 0.2, 0.2))

    draw_header_bar(page, 180, 195, (0.70, 0.10, 0.10))
    page.insert_text(pymupdf.Point(40, 191), "HAZARD STATEMENTS", fontsize=9, fontname="hebo", color=(1, 1, 1))

    hazards = [
        ("H225", "Highly flammable liquid and vapor."),
        ("H304", "May be fatal if swallowed and enters airways."),
        ("H315", "Causes skin irritation."),
        ("H336", "May cause drowsiness or dizziness."),
        ("H361", "Suspected of damaging fertility or the unborn child."),
        ("H373", "May cause damage to organs through prolonged or repeated exposure."),
    ]

    for i, (code, text) in enumerate(hazards):
        y = 205 + i * 18
        bg = (0.98, 0.94, 0.94) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(36, y, 576, y + 16))
        shape.finish(fill=bg, color=None)
        shape.commit()
        page.insert_text(pymupdf.Point(40, y + 11), code, fontsize=9, fontname="hebo", color=(0.7, 0.1, 0.1))
        page.insert_text(pymupdf.Point(80, y + 11), text, fontsize=9, fontname="helv")

    draw_header_bar(page, 318, 333, (0.10, 0.40, 0.20))
    page.insert_text(pymupdf.Point(40, 329), "PRECAUTIONARY STATEMENTS — PREVENTION", fontsize=9, fontname="hebo", color=(1, 1, 1))

    precautions_prevention = [
        ("P201", "Obtain special instructions before use."),
        ("P202", "Do not handle until all safety precautions have been read and understood."),
        ("P210", "Keep away from heat sources, hot surfaces, sparks, open flames and other ignition sources."),
        ("P233", "Keep container tightly closed."),
        ("P240", "Ground and bond container and receiving equipment."),
        ("P241", "Use explosion-proof electrical equipment."),
        ("P242", "Use only non-sparking tools."),
        ("P243", "Take precautionary measures against static discharge."),
        ("P260", "Do not breathe vapors or spray."),
        ("P271", "Use only outdoors or in a well-ventilated area."),
    ]

    for i, (code, text) in enumerate(precautions_prevention):
        y = 342 + i * 16
        bg = (0.93, 0.97, 0.93) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(36, y, 576, y + 14))
        shape.finish(fill=bg, color=None)
        shape.commit()
        page.insert_text(pymupdf.Point(40, y + 10), code, fontsize=8.5, fontname="hebo", color=(0.05, 0.35, 0.15))
        page.insert_text(pymupdf.Point(80, y + 10), text, fontsize=8.5, fontname="helv")

    draw_header_bar(page, 508, 523, (0.10, 0.35, 0.55))
    page.insert_text(pymupdf.Point(40, 519), "PRECAUTIONARY STATEMENTS — RESPONSE", fontsize=9, fontname="hebo", color=(1, 1, 1))

    response_precautions = [
        ("P301+P310", "IF SWALLOWED: Immediately call a POISON CENTER or doctor/physician."),
        ("P303+P361+P353", "IF ON SKIN OR HAIR: Remove/take off clothing. Rinse skin with water."),
        ("P304+P340", "IF INHALED: Remove person to fresh air and keep comfortable for breathing."),
        ("P370+P378", "In case of fire: Use appropriate media for extinction."),
    ]

    for i, (code, text) in enumerate(response_precautions):
        y = 532 + i * 16
        bg = (0.91, 0.94, 0.98) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(36, y, 576, y + 14))
        shape.finish(fill=bg, color=None)
        shape.commit()
        page.insert_text(pymupdf.Point(40, y + 10), code, fontsize=8.5, fontname="hebo", color=(0.05, 0.15, 0.50))
        page.insert_text(pymupdf.Point(140, y + 10), text, fontsize=8.5, fontname="helv")

    draw_header_bar(page, 600, 615, (0.40, 0.10, 0.55))
    page.insert_text(pymupdf.Point(40, 611), "PRECAUTIONARY STATEMENTS — STORAGE", fontsize=9, fontname="hebo", color=(1, 1, 1))

    storage_precautions = [
        # The key text 'Keep away from heat sources' — this is what the agent must underline
        ("P403+P235", "Keep away from heat sources. Store in a cool, well-ventilated place."),
        ("P405", "Store locked up. Protect from light and direct sunlight."),
        ("P233", "Keep container tightly closed when not in use."),
    ]

    for i, (code, text) in enumerate(storage_precautions):
        y = 624 + i * 16
        bg = (0.96, 0.93, 0.98) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(36, y, 576, y + 14))
        shape.finish(fill=bg, color=None)
        shape.commit()
        page.insert_text(pymupdf.Point(40, y + 10), code, fontsize=8.5, fontname="hebo", color=(0.35, 0.05, 0.45))
        page.insert_text(pymupdf.Point(120, y + 10), text, fontsize=8.5, fontname="helv")

    page.insert_text(pymupdf.Point(36, 770), "PyroClean Industrial Solvent 750 — SDS-PC750-2024 — Page 3 of 8", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))


# ---------------------------------------------------------------------------
# Page 4: First Aid Measures
# ---------------------------------------------------------------------------
def build_page4(doc):
    page = doc.new_page(width=612, height=792)

    draw_header_bar(page, 36, 55)
    page.insert_text(pymupdf.Point(40, 50), "SAFETY DATA SHEET — SDS-PC750-2024", fontsize=11, fontname="hebo", color=(1, 1, 1))

    draw_header_bar(page, 65, 80)
    page.insert_text(pymupdf.Point(40, 76), "SECTION 4: FIRST AID MEASURES", fontsize=9, fontname="hebo", color=(1, 1, 1))

    page.insert_textbox(
        pymupdf.Rect(36, 90, 576, 320),
        "Eye Contact:\n"
        "  Immediately flush eyes with large amounts of water for at least 15 minutes. Hold eyelids open\n"
        "  during flushing. Remove contact lenses if present and easy to do without further injury.\n"
        "  Seek immediate medical attention if irritation persists.\n\n"
        "Skin Contact:\n"
        "  Remove contaminated clothing immediately. Wash skin thoroughly with soap and water for at\n"
        "  least 15 minutes. Seek medical attention if irritation, redness or swelling develops.\n\n"
        "Inhalation:\n"
        "  Remove victim to fresh air immediately. Keep warm and quiet. Administer oxygen if breathing\n"
        "  is difficult. If not breathing, give artificial respiration. Seek immediate medical attention.\n\n"
        "Ingestion:\n"
        "  DO NOT induce vomiting (aspiration hazard — fatal if enters airways).\n"
        "  Immediately call poison control center or physician. Do not give anything by mouth to an\n"
        "  unconscious or convulsing person. If vomiting occurs spontaneously, keep head below hips.",
        fontsize=9, fontname="helv",
    )

    draw_header_bar(page, 335, 350)
    page.insert_text(pymupdf.Point(40, 346), "SECTION 5: FIREFIGHTING MEASURES", fontsize=9, fontname="hebo", color=(1, 1, 1))

    page.insert_textbox(
        pymupdf.Rect(36, 358, 576, 560),
        "Suitable Extinguishing Media:\n"
        "  Dry chemical, CO2, foam, or water spray (fog). Do not use a direct water stream — it will\n"
        "  scatter the burning liquid and spread the fire.\n\n"
        "Special Hazards:\n"
        "  Highly flammable liquid and vapor. Vapors may travel to remote ignition sources and flash\n"
        "  back. Vapors are heavier than air and may accumulate in low-lying areas. Vapor/air mixtures\n"
        "  are explosive.\n\n"
        "Protective Equipment for Firefighters:\n"
        "  Wear SCBA (self-contained breathing apparatus) and full protective equipment (bunker gear).\n"
        "  Cool fire-exposed containers with water. Withdraw immediately if rising sound from venting\n"
        "  device or discolouration of tank. Notify local emergency services (911 or equivalent).\n\n"
        "Specific Hazards Arising from the Chemical:\n"
        "  Combustion generates CO, CO2, and partial oxidation products.",
        fontsize=9, fontname="helv",
    )

    page.insert_text(pymupdf.Point(36, 770), "PyroClean Industrial Solvent 750 — SDS-PC750-2024 — Page 4 of 8", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))


# ---------------------------------------------------------------------------
# Page 5: Handling, Storage & Disposal
# ---------------------------------------------------------------------------
def build_page5(doc):
    page = doc.new_page(width=612, height=792)

    draw_header_bar(page, 36, 55)
    page.insert_text(pymupdf.Point(40, 50), "SAFETY DATA SHEET — SDS-PC750-2024", fontsize=11, fontname="hebo", color=(1, 1, 1))

    draw_header_bar(page, 65, 80)
    page.insert_text(pymupdf.Point(40, 76), "SECTION 7: HANDLING AND STORAGE", fontsize=9, fontname="hebo", color=(1, 1, 1))

    page.insert_textbox(
        pymupdf.Rect(36, 90, 576, 340),
        "Handling Precautions:\n"
        "  Handle in well-ventilated areas. Avoid breathing vapors or mists. Avoid contact with eyes,\n"
        "  skin and clothing. Use only with adequate ventilation or respiratory protection.\n"
        "  Use proper grounding and bonding to prevent electrostatic discharge.\n"
        "  Prohibit smoking, open flames and other ignition sources in work area.\n"
        "  Wear appropriate PPE as described in Section 8.\n\n"
        "Storage Requirements:\n"
        "  Store in a cool, dry, well-ventilated location away from incompatible materials.\n"
        "  Keep containers tightly closed and upright. Protect from heat, direct sunlight,\n"
        "  and oxidizing agents. Recommended storage temperature: 5–30°C (41–86°F).\n"
        "  Maximum recommended storage period: 24 months from date of manufacture.\n\n"
        "Disposal Considerations:\n"
        "  Dispose in accordance with all applicable federal, state, and local regulations.\n"
        "  Do not flush to drain or sewer. Incinerate in a licensed facility.",
        fontsize=9, fontname="helv",
    )

    draw_header_bar(page, 355, 370)
    page.insert_text(pymupdf.Point(40, 366), "SECTION 8: EXPOSURE CONTROLS / PERSONAL PROTECTION", fontsize=9, fontname="hebo", color=(1, 1, 1))

    page.insert_textbox(
        pymupdf.Rect(36, 380, 576, 600),
        "Exposure Limits:\n"
        "  Petroleum naphtha: OSHA PEL 400 ppm TWA | ACGIH TLV 300 ppm TWA\n"
        "  n-Heptane: OSHA PEL 500 ppm TWA | ACGIH TLV 400 ppm TWA\n"
        "  Isopropyl alcohol: OSHA PEL 400 ppm TWA | ACGIH TLV 200 ppm TWA\n\n"
        "Engineering Controls:\n"
        "  Provide local exhaust ventilation to maintain airborne concentrations below exposure limits.\n"
        "  Install eye wash stations and safety showers in areas where product is used.\n\n"
        "Personal Protective Equipment (PPE):\n"
        "  Respiratory: Chemical cartridge half-mask (OV cartridges) for brief exposures;\n"
        "               SCBA for large spills or emergencies.\n"
        "  Hand Protection: Nitrile rubber gloves, minimum 0.38 mm thickness (8 mil).\n"
        "  Eye/Face Protection: Chemical splash goggles; face shield for large volumes.\n"
        "  Skin Protection: Chemical-resistant coveralls; rubber boots.",
        fontsize=9, fontname="helv",
    )

    page.insert_text(pymupdf.Point(36, 770), "PyroClean Industrial Solvent 750 — SDS-PC750-2024 — Page 5 of 8", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))


# ---------------------------------------------------------------------------
# Page 6: Toxicological Information
# ---------------------------------------------------------------------------
def build_page6(doc):
    page = doc.new_page(width=612, height=792)

    draw_header_bar(page, 36, 55)
    page.insert_text(pymupdf.Point(40, 50), "SAFETY DATA SHEET — SDS-PC750-2024", fontsize=11, fontname="hebo", color=(1, 1, 1))

    draw_header_bar(page, 65, 80)
    page.insert_text(pymupdf.Point(40, 76), "SECTION 11: TOXICOLOGICAL INFORMATION", fontsize=9, fontname="hebo", color=(1, 1, 1))

    page.insert_textbox(
        pymupdf.Rect(36, 90, 576, 450),
        "Acute Toxicity:\n"
        "  Oral (rat) LD50: > 5000 mg/kg (low acute oral toxicity)\n"
        "  Dermal (rabbit) LD50: > 2000 mg/kg\n"
        "  Inhalation (rat) LC50 (4h): > 5 mg/L\n\n"
        "Skin Corrosion/Irritation:\n"
        "  Classified as skin irritant (Category 2). Prolonged or repeated contact causes dermatitis.\n"
        "  Defatting of skin may occur with extended exposure.\n\n"
        "Eye Damage/Irritation:\n"
        "  Causes mild to moderate eye irritation. No serious damage expected with prompt first aid.\n\n"
        "Sensitisation:\n"
        "  Not classified as a skin or respiratory sensitizer based on available data.\n\n"
        "Mutagenicity:\n"
        "  Not considered to be mutagenic based on available data.\n\n"
        "Carcinogenicity:\n"
        "  IARC Group 1: Not listed. OSHA Carcinogen List: Not listed.\n"
        "  NTP: Not listed as known or reasonably anticipated carcinogen.\n\n"
        "Reproductive Toxicity:\n"
        "  Suspected reproductive hazard based on animal studies at high doses.\n"
        "  Category 2 (H361). Minimize exposure during pregnancy.\n\n"
        "STOT — Single Exposure:\n"
        "  Category 3 (H336). Narcotic effects at high concentrations.\n"
        "  Symptoms: headache, dizziness, nausea, disorientation.\n\n"
        "Aspiration Hazard:\n"
        "  Category 1 (H304). Aspiration into the lungs can cause chemical pneumonitis or death.",
        fontsize=9, fontname="helv",
    )

    page.insert_text(pymupdf.Point(36, 770), "PyroClean Industrial Solvent 750 — SDS-PC750-2024 — Page 6 of 8", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))


# ---------------------------------------------------------------------------
# Page 7: Environmental & Regulatory Information
# ---------------------------------------------------------------------------
def build_page7(doc):
    page = doc.new_page(width=612, height=792)

    draw_header_bar(page, 36, 55)
    page.insert_text(pymupdf.Point(40, 50), "SAFETY DATA SHEET — SDS-PC750-2024", fontsize=11, fontname="hebo", color=(1, 1, 1))

    draw_header_bar(page, 65, 80)
    page.insert_text(pymupdf.Point(40, 76), "SECTION 12: ECOLOGICAL INFORMATION", fontsize=9, fontname="hebo", color=(1, 1, 1))

    page.insert_textbox(
        pymupdf.Rect(36, 90, 576, 300),
        "Ecotoxicity:\n"
        "  Fish LC50 (96h, Pimephales promelas): 2.4 mg/L — Aquatic Toxicity Category 2\n"
        "  Daphnia EC50 (48h): 0.83 mg/L\n"
        "  Algae NOEC (72h): 0.01 mg/L\n\n"
        "Persistence and Degradability:\n"
        "  Readily biodegradable in aerobic conditions (OECD 301B: 85% in 28 days).\n"
        "  Recalcitrant under anaerobic conditions. Not expected to persist.\n\n"
        "Bioaccumulative Potential:\n"
        "  log Kow 3.5–5.5 suggests potential for bioaccumulation. Monitor bioaccumulation\n"
        "  in aquatic food chains with prolonged exposures.\n\n"
        "Mobility in Soil:\n"
        "  Low mobility; adsorbs to organic matter and soils. Does not migrate to groundwater\n"
        "  at significant rates under normal conditions.",
        fontsize=9, fontname="helv",
    )

    draw_header_bar(page, 315, 330)
    page.insert_text(pymupdf.Point(40, 326), "SECTION 15: REGULATORY INFORMATION", fontsize=9, fontname="hebo", color=(1, 1, 1))

    page.insert_textbox(
        pymupdf.Rect(36, 340, 576, 590),
        "US Federal Regulations:\n"
        "  TSCA (Toxic Substances Control Act): All components are listed on TSCA Inventory.\n"
        "  CERCLA RQ: Reportable quantity 1 lb (as petroleum distillate mixture).\n"
        "  SARA Section 302: Not listed as extremely hazardous substance.\n"
        "  SARA Section 311/312: Immediate health; Delayed health; Fire hazard.\n"
        "  SARA Section 313: Reporting required (n-Heptane, Ethyl Acetate).\n\n"
        "California Proposition 65:\n"
        "  Contains compounds listed under Prop 65: WARNING — This product can expose you\n"
        "  to chemicals including benzene (trace impurity), which is known to the State of\n"
        "  California to cause cancer.\n\n"
        "International Regulations:\n"
        "  EU Regulation (EC) No 1272/2008 (CLP): Classified as Flam. Liq. 2; H225.\n"
        "  ADR/RID/IMDG: UN1268, Class 3, Packing Group II.\n"
        "  IATA Dangerous Goods: 3, UN1268, PG II.",
        fontsize=9, fontname="helv",
    )

    page.insert_text(pymupdf.Point(36, 770), "PyroClean Industrial Solvent 750 — SDS-PC750-2024 — Page 7 of 8", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))


# ---------------------------------------------------------------------------
# Page 8: Document History & Revision
# ---------------------------------------------------------------------------
def build_page8(doc):
    page = doc.new_page(width=612, height=792)

    draw_header_bar(page, 36, 55)
    page.insert_text(pymupdf.Point(40, 50), "SAFETY DATA SHEET — SDS-PC750-2024", fontsize=11, fontname="hebo", color=(1, 1, 1))

    draw_header_bar(page, 65, 80)
    page.insert_text(pymupdf.Point(40, 76), "SECTION 16: OTHER INFORMATION", fontsize=9, fontname="hebo", color=(1, 1, 1))

    page.insert_text(pymupdf.Point(36, 95), "Revision History:", fontsize=10, fontname="hebo")

    revisions = [
        ("4.2", "January 2024", "Updated GHS classifications per 7th edition ATP."),
        ("4.1", "March 2023", "Added Prop 65 warnings. Updated SARA 313 reportable components."),
        ("4.0", "August 2022", "Full reformatting to GHS/HCS 2012 16-section format."),
        ("3.5", "June 2021", "Updated toxicological data per new REACH dossier."),
        ("3.4", "November 2020", "Revised emergency contact numbers."),
        ("3.3", "February 2019", "Added EU CLP classification."),
        ("3.2", "April 2018", "Revised flash point data from new testing."),
        ("3.1", "September 2017", "Initial GHS transition version."),
    ]

    # Table header
    draw_header_bar(page, 105, 118, (0.70, 0.75, 0.85))
    page.insert_text(pymupdf.Point(40, 114), "Version", fontsize=9, fontname="hebo")
    page.insert_text(pymupdf.Point(110, 114), "Date", fontsize=9, fontname="hebo")
    page.insert_text(pymupdf.Point(210, 114), "Changes", fontsize=9, fontname="hebo")

    for i, (ver, date, change) in enumerate(revisions):
        y = 126 + i * 18
        bg = (0.95, 0.96, 0.98) if i % 2 == 0 else (1, 1, 1)
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(36, y, 576, y + 16))
        shape.finish(fill=bg, color=None)
        shape.commit()
        page.insert_text(pymupdf.Point(40, y + 11), ver, fontsize=8.5, fontname="helv")
        page.insert_text(pymupdf.Point(110, y + 11), date, fontsize=8.5, fontname="helv")
        page.insert_text(pymupdf.Point(210, y + 11), change, fontsize=8.5, fontname="helv")

    page.insert_textbox(
        pymupdf.Rect(36, 280, 576, 460),
        "Disclaimer:\n"
        "The information provided in this Safety Data Sheet is based on data believed to be accurate\n"
        "at the time of revision. ChemSafe Industrial Products Inc. makes no warranty, expressed or\n"
        "implied, and assumes no responsibility for the accuracy or completeness of the information\n"
        "contained herein. Conditions of use are beyond our control; ChemSafe Industrial Products Inc.\n"
        "expressly disclaims any and all liability arising from the use, misuse, or reliance upon this\n"
        "information.\n\n"
        "This SDS is intended only as a guide to the appropriate precautionary handling of the material\n"
        "by properly trained personnel. It is not intended to be, nor should be construed as, a warranty\n"
        "or quality specification. Additional information on safe handling, storage, and disposal may be\n"
        "obtained from local regulatory agencies.\n\n"
        "Prepared by: ChemSafe Regulatory Affairs Department\n"
        "Next Review Date: January 2026",
        fontsize=9, fontname="helv",
    )

    # Footer
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(36, 745, 576, 760))
    shape.finish(fill=(0.12, 0.20, 0.50), color=None)
    shape.commit()
    page.insert_text(pymupdf.Point(40, 756), "PyroClean Industrial Solvent 750 — SDS-PC750-2024 — Page 8 of 8 — © 2024 ChemSafe Industrial Products Inc.", fontsize=7.5, fontname="helv", color=(1, 1, 1))


# ---------------------------------------------------------------------------
# Main: build the PDF
# ---------------------------------------------------------------------------
def create_initial():
    doc = pymupdf.open()

    build_page1(doc)
    build_page2(doc)
    build_page3(doc)
    build_page4(doc)
    build_page5(doc)
    build_page6(doc)
    build_page7(doc)
    build_page8(doc)

    doc.save(PDF_PATH)
    doc.close()
    print(f"Created: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")

    # Verify the target text strings exist on page 3
    verify_doc = pymupdf.open(PDF_PATH)
    p3 = verify_doc[2]
    text = p3.get_text()
    verify_doc.close()
    if "DANGER: Highly flammable" in text:
        print("OK: 'DANGER: Highly flammable' found on page 3")
    else:
        print("WARNING: 'DANGER: Highly flammable' NOT found on page 3!")
    if "Keep away from heat sources" in text:
        print("OK: 'Keep away from heat sources' found on page 3")
    else:
        print("WARNING: 'Keep away from heat sources' NOT found on page 3!")

    # Open in Evince at page 3 (0-indexed page 2 = displayed page 3)
    launch_gui(f'evince --page-index=2 "{PDF_PATH}"', delay_sec=2.0)
    print("Evince opened at page 3")


create_initial()
