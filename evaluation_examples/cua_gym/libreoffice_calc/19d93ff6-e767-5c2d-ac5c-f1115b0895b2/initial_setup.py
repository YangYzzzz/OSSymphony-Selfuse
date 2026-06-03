"""
Initial Setup: Create a research dataset description PDF with minimal metadata
Task ID: pdf_mbc_016
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_016'
RESEARCH_DIR = f'{WORKDIR}/Research'
OUTPUT = f'{RESEARCH_DIR}/dataset_description.pdf'


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
    os.makedirs(RESEARCH_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ---- Page 1: Title & Abstract ----
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Title
    page1.insert_text(
        pymupdf.Point(72, 60),
        "Global Urban Air Quality Monitoring Dataset (GUAQM-2024)",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # Subtitle / authors
    page1.insert_text(
        pymupdf.Point(72, 90),
        "Version 2.3 — Released January 2024",
        fontsize=11,
        fontname="tiit",
        color=(0.3, 0.3, 0.3),
    )

    page1.insert_text(
        pymupdf.Point(72, 115),
        "Prepared by: Dr. Elena Vasquez, Dr. Ravi Anand, Dr. Mei-Lin Chen",
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
    )

    # Horizontal line
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 130), pymupdf.Point(540, 130))
    shape.finish(color=(0.6, 0.6, 0.6), width=1)
    shape.commit()

    # Abstract
    page1.insert_text(
        pymupdf.Point(72, 155),
        "Abstract",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )

    abstract_text = (
        "The Global Urban Air Quality Monitoring Dataset (GUAQM-2024) is a comprehensive, "
        "multi-year collection of atmospheric pollutant measurements gathered from 847 monitoring "
        "stations across 142 cities in 38 countries. The dataset spans the period from January 2019 "
        "through December 2023 and includes hourly measurements of six criteria pollutants: "
        "particulate matter (PM2.5 and PM10), nitrogen dioxide (NO2), sulfur dioxide (SO2), carbon "
        "monoxide (CO), and ground-level ozone (O3). Each record is georeferenced and accompanied "
        "by meteorological covariates including temperature, relative humidity, wind speed, wind "
        "direction, and atmospheric pressure. Data quality flags indicate the level of validation "
        "applied to each measurement. This dataset supports research in environmental epidemiology, "
        "urban planning, climate science, and machine learning applications for air quality forecasting."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 175, 540, 380),
        abstract_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Section: Dataset Overview
    page1.insert_text(
        pymupdf.Point(72, 405),
        "1. Dataset Overview",
        fontsize=14,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    overview_text = (
        "The GUAQM-2024 dataset contains approximately 32.7 million individual measurement records "
        "organized in a hierarchical structure by region, city, and monitoring station. The primary "
        "data files are provided in Apache Parquet format for efficient querying, with supplementary "
        "CSV exports available for compatibility with common statistical software.\n\n"
        "Temporal Coverage: 2019-01-01 to 2023-12-31\n"
        "Temporal Resolution: Hourly (UTC-aligned)\n"
        "Spatial Coverage: 142 cities across 38 countries\n"
        "Number of Stations: 847 active monitoring stations\n"
        "Total Records: ~32.7 million validated observations\n"
        "File Format: Apache Parquet (primary), CSV (supplementary)\n"
        "Total Size: 4.8 GB (Parquet), 18.2 GB (CSV)"
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 425, 540, 700),
        overview_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # ---- Page 2: Data Schema & Quality ----
    page2 = doc.new_page(width=612, height=792)

    page2.insert_text(
        pymupdf.Point(72, 60),
        "2. Data Schema",
        fontsize=14,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    schema_text = (
        "Each observation record contains the following fields:\n\n"
        "  station_id       (string)    Unique station identifier, e.g. 'BJ-HAI-003'\n"
        "  timestamp        (datetime)  ISO 8601 UTC timestamp\n"
        "  pm25             (float)     PM2.5 concentration (ug/m3)\n"
        "  pm10             (float)     PM10 concentration (ug/m3)\n"
        "  no2              (float)     NO2 concentration (ppb)\n"
        "  so2              (float)     SO2 concentration (ppb)\n"
        "  co               (float)     CO concentration (ppm)\n"
        "  o3               (float)     O3 concentration (ppb)\n"
        "  temperature      (float)     Ambient temperature (Celsius)\n"
        "  humidity         (float)     Relative humidity (%)\n"
        "  wind_speed       (float)     Wind speed (m/s)\n"
        "  wind_direction   (float)     Wind direction (degrees, 0-360)\n"
        "  pressure         (float)     Atmospheric pressure (hPa)\n"
        "  quality_flag     (int)       0=raw, 1=automated QC, 2=manual QC, 3=validated\n"
        "  city             (string)    City name\n"
        "  country_iso      (string)    ISO 3166-1 alpha-2 country code\n"
        "  latitude         (float)     Station latitude (WGS84)\n"
        "  longitude        (float)     Station longitude (WGS84)\n"
        "  elevation_m      (float)     Station elevation in meters above sea level"
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 80, 540, 430),
        schema_text,
        fontsize=9,
        fontname="cour",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    page2.insert_text(
        pymupdf.Point(72, 455),
        "3. Data Quality Assurance",
        fontsize=14,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    quality_text = (
        "All measurements undergo a three-stage quality assurance pipeline:\n\n"
        "Stage 1 — Automated Range Checks: Observations falling outside physically plausible "
        "ranges are flagged. For example, PM2.5 values below 0 or above 1000 ug/m3 are marked "
        "as suspect. Approximately 2.1% of raw observations fail range checks.\n\n"
        "Stage 2 — Statistical Outlier Detection: A rolling 24-hour median absolute deviation "
        "(MAD) filter identifies statistical outliers. Records deviating more than 5 MAD units "
        "from the local median are flagged for review. This stage captures sensor malfunctions "
        "and transient interference events.\n\n"
        "Stage 3 — Expert Validation: A subset of flagged records is reviewed by domain experts "
        "at partner institutions. Approximately 15,000 records per year undergo manual review, "
        "with inter-annotator agreement exceeding 94%."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 475, 540, 740),
        quality_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # ---- Page 3: Coverage & Citation ----
    page3 = doc.new_page(width=612, height=792)

    page3.insert_text(
        pymupdf.Point(72, 60),
        "4. Geographic Coverage",
        fontsize=14,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    coverage_text = (
        "The dataset includes monitoring stations from the following regions:\n\n"
        "East Asia: Beijing, Shanghai, Tokyo, Seoul, Osaka, Taipei (198 stations)\n"
        "South Asia: Delhi, Mumbai, Dhaka, Lahore, Kolkata (127 stations)\n"
        "Southeast Asia: Bangkok, Jakarta, Manila, Ho Chi Minh City (86 stations)\n"
        "Europe: London, Paris, Berlin, Madrid, Rome, Warsaw (142 stations)\n"
        "North America: New York, Los Angeles, Toronto, Mexico City (103 stations)\n"
        "South America: Sao Paulo, Buenos Aires, Bogota, Lima (68 stations)\n"
        "Africa: Lagos, Nairobi, Cairo, Johannesburg, Accra (54 stations)\n"
        "Middle East: Dubai, Riyadh, Istanbul, Tehran (42 stations)\n"
        "Oceania: Sydney, Melbourne, Auckland (27 stations)\n\n"
        "Station selection criteria included: (a) continuous operation for at least 3 years, "
        "(b) calibration records available, (c) data sharing agreement with the GUAQM consortium, "
        "and (d) measurement of at least 4 of the 6 criteria pollutants."
    )
    page3.insert_textbox(
        pymupdf.Rect(72, 80, 540, 380),
        coverage_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    page3.insert_text(
        pymupdf.Point(72, 405),
        "5. File Organization",
        fontsize=14,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    file_org_text = (
        "guaqm-2024/\n"
        "  ├── data/\n"
        "  │   ├── parquet/\n"
        "  │   │   ├── east_asia/    (198 station files)\n"
        "  │   │   ├── south_asia/   (127 station files)\n"
        "  │   │   ├── europe/       (142 station files)\n"
        "  │   │   └── ...           (other regions)\n"
        "  │   └── csv/\n"
        "  │       └── (same structure as parquet/)\n"
        "  ├── metadata/\n"
        "  │   ├── stations.json     (station coordinates & attributes)\n"
        "  │   ├── calibration/      (per-station calibration logs)\n"
        "  │   └── quality_reports/  (monthly QA summaries)\n"
        "  ├── docs/\n"
        "  │   ├── dataset_description.pdf  (this document)\n"
        "  │   ├── codebook.xlsx\n"
        "  │   └── changelog.md\n"
        "  └── LICENSE.txt"
    )
    page3.insert_textbox(
        pymupdf.Rect(72, 425, 540, 680),
        file_org_text,
        fontsize=9,
        fontname="cour",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Citation
    page3.insert_text(
        pymupdf.Point(72, 705),
        "6. Citation",
        fontsize=14,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    citation_text = (
        "Vasquez, E., Anand, R., & Chen, M.-L. (2024). Global Urban Air Quality Monitoring "
        "Dataset (GUAQM-2024), v2.3. DOI: 10.5281/zenodo.9876543"
    )
    page3.insert_textbox(
        pymupdf.Rect(72, 725, 540, 770),
        citation_text,
        fontsize=10,
        fontname="tiit",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Set minimal metadata — basic creation info only
    # DO NOT set dc:rights, dc:language, or dc:publisher
    doc.set_metadata({
        "title": "GUAQM-2024 Dataset Description",
        "author": "Elena Vasquez, Ravi Anand, Mei-Lin Chen",
        "creator": "PyMuPDF",
        "producer": "PyMuPDF",
        "subject": "Air quality monitoring dataset documentation",
    })

    # Add a simple TOC
    toc = [
        [1, "Abstract", 1],
        [1, "1. Dataset Overview", 1],
        [1, "2. Data Schema", 2],
        [1, "3. Data Quality Assurance", 2],
        [1, "4. Geographic Coverage", 3],
        [1, "5. File Organization", 3],
        [1, "6. Citation", 3],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
