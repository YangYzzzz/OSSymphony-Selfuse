"""
Initial Setup: data_analysis_notes.odt with mixed Python code and prose
Task ID: osworld_multi_apps_code_to_writer_file_002
Domain: libreoffice_writer

Creates /home/user/Documents/data_analysis_notes.odt containing a pandas
data analysis walkthrough with Python code blocks intermixed with explanatory
prose, spanning approximately 3 pages.

Uses standard library only (zipfile + xml) — no odf/docx dependencies required.
"""

import os
import shlex
import subprocess
import time
import zipfile
import textwrap

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_to_writer_file_002'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS_DIR}/data_analysis_notes.odt'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app on the VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def xml_escape(text):
    """Escape XML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))


def build_odt(output_path):
    """Build an ODT file using zipfile + raw ODF XML."""

    # --- content.xml paragraphs ---
    # We collect tuples of (style_name, text) for each paragraph/line
    # Styles: "Heading_1", "Text_Body", "Source_Code"

    paragraphs = []  # list of (style, text)

    def H(text):
        paragraphs.append(('Heading_1', text))

    def P(text):
        paragraphs.append(('Text_Body', text))

    def C(text):
        paragraphs.append(('Source_Code', text))

    def blank():
        paragraphs.append(('Text_Body', ''))

    # ===== PAGE 1: Introduction & Import Setup =====
    H("Pandas Data Analysis Walkthrough")
    blank()
    P("This document walks through a complete data analysis workflow using pandas and matplotlib. "
      "We will load a sales dataset, clean and transform it, compute summary statistics, and "
      "visualize key trends. Code blocks are interspersed with explanations throughout.")
    blank()
    H("1. Setting Up the Environment")
    blank()
    P("Before we begin, we need to import the required libraries. Pandas provides the core "
      "DataFrame data structure, numpy handles numerical operations, and matplotlib is used "
      "for generating plots.")
    blank()
    C("import pandas as pd")
    C("import numpy as np")
    C("import matplotlib.pyplot as plt")
    C("import matplotlib.dates as mdates")
    C("from datetime import datetime")
    blank()
    P("With imports in place, we configure a few global settings to make outputs more readable. "
      "Setting the display precision ensures floats are shown with two decimal places, and "
      "increasing max_columns lets us see all columns in wide DataFrames.")
    blank()
    C("pd.set_option('display.precision', 2)")
    C("pd.set_option('display.max_columns', 20)")
    C("pd.set_option('display.width', 120)")
    blank()

    # ===== PAGE 2: Loading Data & Exploration =====
    H("2. Loading and Inspecting the Dataset")
    blank()
    P("The dataset is stored as a CSV file named 'sales_data_2024.csv'. It contains monthly "
      "sales records for five product categories across three regional offices. We read it "
      "with a parse_dates argument so that date columns are immediately usable as datetime objects.")
    blank()
    C("df = pd.read_csv('/home/user/data/sales_data_2024.csv', parse_dates=['date'])")
    C("print(df.head())")
    C("print(df.shape)")
    C("print(df.dtypes)")
    blank()
    P("The dataset has 1,440 rows and 7 columns: date, region, product_category, units_sold, "
      "unit_price, revenue, and discount_rate. A quick inspection with .info() confirms there "
      "are no missing values, and all numeric columns have appropriate dtypes.")
    blank()
    C("print(df.info())")
    C("print(df.describe())")
    blank()
    H("3. Data Cleaning")
    blank()
    P("Although the dataset is largely clean, we apply a few standard transformations. "
      "We strip whitespace from string columns, rename the 'product_category' column to the "
      "shorter 'category' for convenience, and derive a 'month' column from the date field.")
    blank()
    C("df['region'] = df['region'].str.strip()")
    C("df.rename(columns={'product_category': 'category'}, inplace=True)")
    C("df['month'] = df['date'].dt.to_period('M')")
    C("df['year'] = df['date'].dt.year")
    blank()
    P("We also compute a 'net_revenue' column that accounts for the discount rate, "
      "which will be used in the summary statistics section.")
    blank()
    C("df['net_revenue'] = df['revenue'] * (1 - df['discount_rate'])")
    C("print(df[['revenue', 'net_revenue']].head(10))")
    blank()

    # ===== PAGE 3: Analysis & Visualization =====
    H("4. Summary Statistics and Aggregation")
    blank()
    P("We compute total and average net revenue by region and by category using groupby. "
      "The pivot_table method provides a convenient cross-tabulation that combines both "
      "dimensions simultaneously.")
    blank()
    C("revenue_by_region = df.groupby('region')['net_revenue'].sum().reset_index()")
    C("revenue_by_category = df.groupby('category')['net_revenue'].agg(['sum', 'mean'])")
    C("print(revenue_by_region)")
    C("print(revenue_by_category)")
    blank()
    C("pivot = pd.pivot_table(df, values='net_revenue', index='region',")
    C("                       columns='category', aggfunc='sum', fill_value=0)")
    C("print(pivot)")
    blank()
    P("We also compute a monthly trend for the top-performing region, North, to see "
      "how revenue evolved over the year. The resample method is ideal for time-based aggregations.")
    blank()
    C("north_df = df[df['region'] == 'North'].copy()")
    C("north_df.set_index('date', inplace=True)")
    C("monthly_north = north_df['net_revenue'].resample('ME').sum()")
    C("print(monthly_north)")
    blank()
    H("5. Visualization")
    blank()
    P("Finally, we create a bar chart of revenue by region and a line plot of the monthly "
      "North region trend. Both figures are saved to the /home/user/output/ directory.")
    blank()
    C("def plot_revenue_by_region(data, output_path):")
    C("    fig, ax = plt.subplots(figsize=(8, 5))")
    C("    ax.bar(data['region'], data['net_revenue'], color='steelblue')")
    C("    ax.set_title('Net Revenue by Region \u2014 2024')")
    C("    ax.set_xlabel('Region')")
    C("    ax.set_ylabel('Net Revenue (USD)')")
    C("    plt.tight_layout()")
    C("    fig.savefig(output_path)")
    C("    plt.close(fig)")
    blank()
    C("plot_revenue_by_region(revenue_by_region, '/home/user/output/revenue_by_region.png')")
    blank()
    C("def plot_monthly_trend(series, output_path):")
    C("    fig, ax = plt.subplots(figsize=(10, 4))")
    C("    ax.plot(series.index, series.values, marker='o', color='darkorange')")
    C("    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))")
    C("    ax.set_title('North Region Monthly Revenue \u2014 2024')")
    C("    ax.set_xlabel('Month')")
    C("    ax.set_ylabel('Net Revenue (USD)')")
    C("    plt.tight_layout()")
    C("    fig.savefig(output_path)")
    C("    plt.close(fig)")
    blank()
    C("plot_monthly_trend(monthly_north, '/home/user/output/north_monthly_trend.png')")
    C("print('All figures saved to /home/user/output/')")
    blank()
    P("This concludes the walkthrough. The complete extracted code is available separately "
      "in analysis_code.py for direct execution.")

    # --- Build content.xml ---
    para_xml_parts = []
    for style, text in paragraphs:
        escaped = xml_escape(text)
        para_xml_parts.append(
            f'<text:p text:style-name="{style}">{escaped}</text:p>'
        )
    body_text = '\n'.join(para_xml_parts)

    content_xml = textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8"?>
    <office:document-content
      xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
      xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
      xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
      xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
      office:version="1.3">
      <office:automatic-styles>
        <style:style style:name="Heading_1" style:family="paragraph" style:parent-style-name="Heading_20_1">
          <style:text-properties fo:font-size="16pt" fo:font-weight="bold"/>
        </style:style>
        <style:style style:name="Text_Body" style:family="paragraph" style:parent-style-name="Text_Body">
          <style:text-properties fo:font-size="12pt"/>
        </style:style>
        <style:style style:name="Source_Code" style:family="paragraph" style:parent-style-name="Preformatted_20_Text">
          <style:text-properties fo:font-family="Courier New" fo:font-size="10pt"/>
        </style:style>
      </office:automatic-styles>
      <office:body>
        <office:text>
          {body_text}
        </office:text>
      </office:body>
    </office:document-content>
    """)

    # --- Build styles.xml (minimal) ---
    styles_xml = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <office:document-styles
      xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
      xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
      xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
      office:version="1.3">
      <office:styles>
        <style:style style:name="Heading_20_1" style:family="paragraph" style:class="text">
          <style:text-properties fo:font-size="16pt" fo:font-weight="bold"/>
        </style:style>
        <style:style style:name="Text_Body" style:family="paragraph" style:class="text">
          <style:text-properties fo:font-size="12pt"/>
        </style:style>
        <style:style style:name="Preformatted_20_Text" style:family="paragraph" style:class="text">
          <style:text-properties fo:font-family="Courier New" fo:font-size="10pt"/>
        </style:style>
      </office:styles>
    </office:document-styles>
    """)

    # --- Build META-INF/manifest.xml ---
    manifest_xml = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <manifest:manifest
      xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
      manifest:version="1.3">
      <manifest:file-entry manifest:full-path="/" manifest:version="1.3"
        manifest:media-type="application/vnd.oasis.opendocument.text"/>
      <manifest:file-entry manifest:full-path="content.xml"
        manifest:media-type="text/xml"/>
      <manifest:file-entry manifest:full-path="styles.xml"
        manifest:media-type="text/xml"/>
    </manifest:manifest>
    """)

    # --- Build mimetype (must be first entry, uncompressed) ---
    mimetype = "application/vnd.oasis.opendocument.text"

    # --- Write ZIP ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype MUST be first, uncompressed
        zf.writestr(zipfile.ZipInfo('mimetype'), mimetype)
        zf.writestr('META-INF/manifest.xml', manifest_xml.encode('utf-8'))
        zf.writestr('content.xml', content_xml.encode('utf-8'))
        zf.writestr('styles.xml', styles_xml.encode('utf-8'))

    print(f'Initial ODT file created: {output_path}')


def create_initial():
    build_odt(OUTPUT)

    # GUI-ready startup: open the ODT in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
