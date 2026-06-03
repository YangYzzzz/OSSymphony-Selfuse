"""
Initial Setup: Multi-file document processing workflow with automation spec
Task ID: osworld_multi_apps_doc_follow_instructions_012
Domain: libreoffice_calc (multi-app: Calc + Writer)

Creates:
  - /home/user/Documents/automation_spec.odt  (14-step spec)
  - /home/user/Documents/data_a.ods           (source data file A)
  - /home/user/Documents/data_b.ods           (source data file B)
  - /home/user/Documents/data_c.ods           (source data file C)
  - /home/user/Documents/summary_template.odt (Writer report template)

Does NOT create: consolidated.ods, summary_report.odt, PDFs, completion_log.txt
(those are the expected outputs the agent must produce)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
DOCS_DIR = '/home/user/Documents'
TASK_ID = 'osworld_multi_apps_doc_follow_instructions_012'

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


def create_documents_dir():
    os.makedirs(DOCS_DIR, exist_ok=True)
    print(f'Documents directory ensured: {DOCS_DIR}')


def create_automation_spec():
    """Create the 14-step automation specification document as ODT."""
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.text import H, P, Span, List, ListItem

    doc = OpenDocumentText()

    # --- Define styles ---
    heading1_style = Style(name="Heading1", family="paragraph", parentstylename="Heading_20_1")
    doc.automaticstyles.addElement(heading1_style)

    body_style = Style(name="Body", family="paragraph")
    body_pp = ParagraphProperties(marginbottom="0.2cm")
    body_style.addElement(body_pp)
    doc.automaticstyles.addElement(body_style)

    bold_style = Style(name="Bold", family="text")
    bold_tp = TextProperties(fontweight="bold")
    bold_style.addElement(bold_tp)
    doc.automaticstyles.addElement(bold_style)

    # --- Title ---
    h_title = H(outlinelevel=1, text="Batch Data Processing Automation Specification")
    doc.text.addElement(h_title)

    # --- Introduction ---
    p_intro = P(text="This document specifies a 14-step automated workflow for processing "
                      "three departmental data files and compiling the results into a consolidated "
                      "report. Execute each step in sequence and verify completion before proceeding.")
    doc.text.addElement(p_intro)

    p_files = P(text="")
    doc.text.addElement(p_files)

    p_files2 = P(text="Source files (located in /home/user/Documents/):")
    doc.text.addElement(p_files2)

    for fname in ["data_a.ods  (Sales Department data)",
                  "data_b.ods  (Operations Department data)",
                  "data_c.ods  (HR Department data)"]:
        p = P(text=f"  - {fname}")
        doc.text.addElement(p)

    doc.text.addElement(P(text=""))

    # --- 14 Steps ---
    h_steps = H(outlinelevel=2, text="Processing Steps")
    doc.text.addElement(h_steps)

    steps = [
        ("Step 1: Standardize Column Names",
         "Open each source file (data_a.ods, data_b.ods, data_c.ods). "
         "Rename columns to a unified schema: 'ID', 'Name', 'Category', 'Amount', 'Date', 'Status'. "
         "Save each file after renaming."),

        ("Step 2: Merge All Data",
         "Create a new spreadsheet file: /home/user/Documents/consolidated.ods. "
         "Copy all data rows (excluding headers) from data_a.ods, data_b.ods, and data_c.ods "
         "into a single sheet named 'Data'. Add a unified header row as the first row: "
         "'ID', 'Name', 'Category', 'Amount', 'Date', 'Status'. "
         "Add a 'Source' column (column G) indicating which file each row came from (A, B, or C)."),

        ("Step 3: Apply Formula - Total Amount",
         "In consolidated.ods, add a new sheet named 'Summary'. "
         "In cell B2, enter a SUMIF formula that calculates the total Amount "
         "for all rows where Source='A'. Label cell A2 with 'Total Amount - Source A'. "
         "In B3, SUMIF for Source='B', label A3 'Total Amount - Source B'. "
         "In B4, SUMIF for Source='C', label A4 'Total Amount - Source C'."),

        ("Step 4: Apply Formula - Count Records",
         "In the Summary sheet of consolidated.ods, "
         "in cell B6 enter a COUNTIF formula for total records from Source='A'. Label A6 'Record Count - Source A'. "
         "In B7, COUNTIF for Source='B', label A7 'Record Count - Source B'. "
         "In B8, COUNTIF for Source='C', label A8 'Record Count - Source C'."),

        ("Step 5: Apply Formula - Average Amount",
         "In the Summary sheet, in cell B10 enter an AVERAGEIF formula for average Amount "
         "where Source='A'. Label A10 'Avg Amount - Source A'. "
         "Repeat for Source B in B11 (label A11) and Source C in B12 (label A12)."),

        ("Step 6: Apply Formula - Max and Min Values",
         "In the Summary sheet, in cell B14 enter a MAX formula over all Amount values "
         "in the Data sheet column D. Label A14 'Maximum Amount'. "
         "In B15 enter a MIN formula over all Amount values. Label A15 'Minimum Amount'."),

        ("Step 7: Apply Formula - Grand Total",
         "In the Summary sheet, in cell B17 enter a SUM formula that adds B2+B3+B4 "
         "(total amount across all sources). Label A17 'Grand Total Amount'. "
         "In B18 enter a SUM formula that adds B6+B7+B8 (total record count). Label A18 'Total Records'."),

        ("Step 8: Create Charts",
         "In consolidated.ods, create a new sheet named 'Charts'. "
         "Create a bar chart showing Total Amount by Source (using data from Summary B2:B4). "
         "Place the chart starting at cell A2 with title 'Amount by Source'. "
         "Create a pie chart showing Record Count distribution by Source (using Summary B6:B8). "
         "Place the pie chart starting at cell A20 with title 'Record Distribution'."),

        ("Step 9: Generate Writer Summary Report",
         "Open /home/user/Documents/summary_template.odt. Save it as "
         "/home/user/Documents/summary_report.odt. "
         "Replace all placeholder tokens in the template with actual data from consolidated.ods: "
         "  {{TOTAL_A}} -> value from Summary!B2, "
         "  {{TOTAL_B}} -> value from Summary!B3, "
         "  {{TOTAL_C}} -> value from Summary!B4, "
         "  {{COUNT_A}} -> value from Summary!B6, "
         "  {{COUNT_B}} -> value from Summary!B7, "
         "  {{COUNT_C}} -> value from Summary!B8, "
         "  {{GRAND_TOTAL}} -> value from Summary!B17, "
         "  {{TOTAL_RECORDS}} -> value from Summary!B18, "
         "  {{MAX_AMOUNT}} -> value from Summary!B14, "
         "  {{MIN_AMOUNT}} -> value from Summary!B15."),

        ("Step 10: Apply Formatting to Report",
         "In summary_report.odt, format the document as follows: "
         "Make all section headings (lines starting with a capital letter followed by a colon) bold. "
         "Set the font for the entire document to Liberation Serif, size 12pt. "
         "Add a page header with text 'Batch Processing Report - Confidential'. "
         "Add page numbers in the footer."),

        ("Step 11: Add Hyperlinks Between Report Sections",
         "In summary_report.odt, insert a bookmark named 'summary_section' at the Summary Statistics heading. "
         "Insert a bookmark named 'detail_section' at the Detailed Breakdown heading. "
         "After the introduction paragraph, add a line 'Jump to: Summary Statistics | Detailed Breakdown' "
         "where each phrase is a hyperlink pointing to the respective bookmark."),

        ("Step 12: Validate Totals",
         "Verify that the Grand Total Amount in Summary!B17 of consolidated.ods equals "
         "the sum of all individual Amount values in the Data sheet column D. "
         "Verify that Total Records in Summary!B18 equals the total number of data rows "
         "(excluding the header) in the Data sheet. "
         "If any discrepancy is found, note it for the completion log."),

        ("Step 13: Export Both Files as PDFs",
         "Export consolidated.ods as PDF: save to /home/user/Documents/consolidated.pdf. "
         "Export summary_report.odt as PDF: save to /home/user/Documents/summary_report.pdf. "
         "Use LibreOffice's built-in PDF export (File > Export as PDF or the equivalent macro command). "
         "Verify both PDF files exist after export."),

        ("Step 14: Write Completion Log",
         "Create a plain text file at /home/user/Desktop/completion_log.txt. "
         "Write the following information to the file: "
         "  - Timestamp of completion (current date and time) "
         "  - File sizes in bytes: consolidated.ods, summary_report.odt, "
         "    consolidated.pdf, summary_report.pdf "
         "  - Any discrepancies found during Step 12 validation (or 'No discrepancies found') "
         "  - Status: COMPLETE "
         "Format each item on a separate line with a label."),
    ]

    for i, (title, desc) in enumerate(steps, 1):
        p_space = P(text="")
        doc.text.addElement(p_space)

        h_step = H(outlinelevel=3, text=title)
        doc.text.addElement(h_step)

        p_desc = P(text=desc)
        doc.text.addElement(p_desc)

    spec_path = os.path.join(DOCS_DIR, 'automation_spec.odt')
    doc.save(spec_path)
    print(f'automation_spec.odt created: {spec_path}')
    return spec_path


def create_data_file_ods(filename, dept, source_label, records):
    """Create a source data ODS file with department-specific column names."""
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.style import Style, TextProperties
    from odf.table import Table, TableRow, TableCell, TableColumn
    from odf.text import P

    doc = OpenDocumentSpreadsheet()
    table = Table(name="Sheet1")
    doc.spreadsheet.addElement(table)

    # Department-specific column naming (different names that need to be standardized)
    col_schemas = {
        'A': ['EmployeeID', 'FullName',   'ProductLine',  'SalesAmount', 'TransactionDate', 'ApprovalStatus'],
        'B': ['OpID',       'PersonName', 'ServiceType',  'Cost',         'RecordDate',      'WorkflowStatus'],
        'C': ['StaffNum',   'StaffName',  'JobCategory',  'TotalPay',     'PayDate',         'HRStatus'],
    }
    cols = col_schemas[source_label]

    def make_cell(value):
        tc = TableCell()
        tc.addElement(P(text=str(value)))
        return tc

    # Header row
    hrow = TableRow()
    for col in cols:
        hrow.addElement(make_cell(col))
    table.addElement(hrow)

    # Data rows
    for rec in records:
        drow = TableRow()
        for val in rec:
            drow.addElement(make_cell(val))
        table.addElement(drow)

    out_path = os.path.join(DOCS_DIR, filename)
    doc.save(out_path)
    print(f'{filename} created: {out_path}')
    return out_path


def create_summary_template():
    """Create the Writer summary report template with placeholder tokens."""
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.text import H, P, Span

    doc = OpenDocumentText()

    bold_style = Style(name="BoldText", family="text")
    bold_tp = TextProperties(fontweight="bold")
    bold_style.addElement(bold_tp)
    doc.automaticstyles.addElement(bold_style)

    # Title
    doc.text.addElement(H(outlinelevel=1, text="Batch Data Processing Summary Report"))
    doc.text.addElement(P(text=""))

    # Introduction
    doc.text.addElement(H(outlinelevel=2, text="Introduction:"))
    doc.text.addElement(P(text=(
        "This report summarizes the results of the automated batch processing workflow "
        "executed on the departmental data files. The processing covered three source files "
        "from the Sales, Operations, and HR departments."
    )))
    doc.text.addElement(P(text=""))

    # Summary Statistics section
    doc.text.addElement(H(outlinelevel=2, text="Summary Statistics:"))
    doc.text.addElement(P(text="The following statistics were computed from the consolidated dataset:"))
    doc.text.addElement(P(text=""))
    doc.text.addElement(P(text="Total Amount - Source A:    {{TOTAL_A}}"))
    doc.text.addElement(P(text="Total Amount - Source B:    {{TOTAL_B}}"))
    doc.text.addElement(P(text="Total Amount - Source C:    {{TOTAL_C}}"))
    doc.text.addElement(P(text="Grand Total Amount:         {{GRAND_TOTAL}}"))
    doc.text.addElement(P(text=""))
    doc.text.addElement(P(text="Record Count - Source A:    {{COUNT_A}}"))
    doc.text.addElement(P(text="Record Count - Source B:    {{COUNT_B}}"))
    doc.text.addElement(P(text="Record Count - Source C:    {{COUNT_C}}"))
    doc.text.addElement(P(text="Total Records:              {{TOTAL_RECORDS}}"))
    doc.text.addElement(P(text=""))
    doc.text.addElement(P(text="Maximum Amount:             {{MAX_AMOUNT}}"))
    doc.text.addElement(P(text="Minimum Amount:             {{MIN_AMOUNT}}"))
    doc.text.addElement(P(text=""))

    # Detailed Breakdown section
    doc.text.addElement(H(outlinelevel=2, text="Detailed Breakdown:"))
    doc.text.addElement(P(text=(
        "The data from Source A represents the Sales department transactions, "
        "including all approved and pending entries for the reporting period."
    )))
    doc.text.addElement(P(text=(
        "Source B data covers operational costs from the Operations department, "
        "including service contracts, maintenance records, and workflow items."
    )))
    doc.text.addElement(P(text=(
        "Source C represents HR payroll data including staff compensation, "
        "benefits, and related HR processing items."
    )))
    doc.text.addElement(P(text=""))

    # Validation Notes
    doc.text.addElement(H(outlinelevel=2, text="Validation Notes:"))
    doc.text.addElement(P(text=(
        "All source totals have been validated against the consolidated figures. "
        "The grand total matches the sum of individual source totals. "
        "Record counts have been verified against source file row counts."
    )))
    doc.text.addElement(P(text=""))

    # Conclusion
    doc.text.addElement(H(outlinelevel=2, text="Conclusion:"))
    doc.text.addElement(P(text=(
        "The batch processing workflow has been completed successfully. "
        "All 14 processing steps were executed in sequence. "
        "Output files have been generated as specified."
    )))

    tmpl_path = os.path.join(DOCS_DIR, 'summary_template.odt')
    doc.save(tmpl_path)
    print(f'summary_template.odt created: {tmpl_path}')
    return tmpl_path


def create_data_files():
    """Create the three source data ODS files with realistic business data."""

    # Source A: Sales Department
    records_a = [
        ['SA-001', 'Emma Rodriguez',     'Enterprise License',   45230.00, '2025-01-15', 'Approved'],
        ['SA-002', 'James Whitfield',    'Consulting Services',  12800.00, '2025-01-22', 'Approved'],
        ['SA-003', 'Priya Nair',         'Software Package',     8950.00,  '2025-02-03', 'Pending'],
        ['SA-004', 'David Kim',          'Hardware Bundle',      31500.00, '2025-02-10', 'Approved'],
        ['SA-005', 'Sofia Andersson',    'Training Package',     5200.00,  '2025-02-18', 'Approved'],
        ['SA-006', 'Michael Chen',       'Enterprise License',   42700.00, '2025-03-01', 'Pending'],
        ['SA-007', 'Aisha Okonkwo',      'Support Contract',     9600.00,  '2025-03-08', 'Approved'],
        ['SA-008', 'Lucas Fernandez',    'Consulting Services',  15400.00, '2025-03-15', 'Approved'],
        ['SA-009', 'Natasha Petrov',     'Software Package',     7350.00,  '2025-03-22', 'Rejected'],
        ['SA-010', 'Benjamin Osei',      'Hardware Bundle',      28900.00, '2025-04-01', 'Approved'],
        ['SA-011', 'Claire Dubois',      'Training Package',     4800.00,  '2025-04-08', 'Approved'],
        ['SA-012', 'Raj Krishnamurthy',  'Enterprise License',   51200.00, '2025-04-15', 'Approved'],
    ]

    # Source B: Operations Department
    records_b = [
        ['OP-001', 'Marcus Thompson',    'Facility Maintenance',  8750.00,  '2025-01-10', 'Completed'],
        ['OP-002', 'Linda Yuen',         'IT Infrastructure',    22300.00,  '2025-01-20', 'In Progress'],
        ['OP-003', 'Carlos Vega',        'Logistics Contract',   16800.00,  '2025-02-05', 'Completed'],
        ['OP-004', 'Hannah Schmidt',     'Security Services',     6400.00,  '2025-02-12', 'Completed'],
        ['OP-005', 'Tunde Adeyemi',      'Facility Maintenance',  9100.00,  '2025-02-25', 'Pending'],
        ['OP-006', 'Grace Nakamura',     'IT Infrastructure',    19600.00,  '2025-03-05', 'Completed'],
        ['OP-007', 'Pierre Moreau',      'Catering Contract',     3200.00,  '2025-03-14', 'Completed'],
        ['OP-008', 'Yuki Tanaka',        'Logistics Contract',   14500.00,  '2025-03-20', 'In Progress'],
        ['OP-009', 'Isabella Costa',     'Security Services',     7800.00,  '2025-04-02', 'Completed'],
        ['OP-010', 'Kwame Mensah',       'IT Infrastructure',    25700.00,  '2025-04-10', 'Completed'],
    ]

    # Source C: HR Department
    records_c = [
        ['HR-001', 'Sarah Chen',         'Engineering',          85000.00,  '2025-01-31', 'Processed'],
        ['HR-002', 'Alex Müller',         'Marketing',            72000.00,  '2025-01-31', 'Processed'],
        ['HR-003', 'Nina Patel',          'Operations',           68500.00,  '2025-01-31', 'Processed'],
        ['HR-004', 'Jason Brooks',        'Engineering',          91000.00,  '2025-02-28', 'Processed'],
        ['HR-005', 'Fatima Al-Hassan',    'Finance',              78000.00,  '2025-02-28', 'Processed'],
        ['HR-006', 'Tom Becker',          'HR',                   65000.00,  '2025-02-28', 'Pending'],
        ['HR-007', 'Olivia Martin',       'Engineering',          88500.00,  '2025-03-31', 'Processed'],
        ['HR-008', 'Samuel Obi',          'Sales',                74000.00,  '2025-03-31', 'Processed'],
        ['HR-009', 'Mei-Ling Zhou',       'Operations',           71000.00,  '2025-03-31', 'Processed'],
        ['HR-010', 'Dmitri Sokolov',      'Finance',              82000.00,  '2025-04-30', 'Processed'],
        ['HR-011', 'Amara Diallo',        'Marketing',            69500.00,  '2025-04-30', 'Processed'],
    ]

    create_data_file_ods('data_a.ods', 'Sales', 'A', records_a)
    create_data_file_ods('data_b.ods', 'Operations', 'B', records_b)
    create_data_file_ods('data_c.ods', 'HR', 'C', records_c)


def main():
    create_documents_dir()

    # Ensure Desktop exists
    desktop_dir = os.path.join(WORKDIR, 'Desktop')
    os.makedirs(desktop_dir, exist_ok=True)

    # Create all initial files
    create_data_files()
    spec_path = create_automation_spec()
    create_summary_template()

    # Verify files exist
    expected_files = [
        os.path.join(DOCS_DIR, 'automation_spec.odt'),
        os.path.join(DOCS_DIR, 'data_a.ods'),
        os.path.join(DOCS_DIR, 'data_b.ods'),
        os.path.join(DOCS_DIR, 'data_c.ods'),
        os.path.join(DOCS_DIR, 'summary_template.odt'),
    ]
    for f in expected_files:
        if os.path.exists(f):
            print(f'  [OK] {f} ({os.path.getsize(f)} bytes)')
        else:
            print(f'  [MISSING] {f}')

    # Ensure no leftover golden artifacts exist
    golden_artifacts = [
        os.path.join(DOCS_DIR, 'consolidated.ods'),
        os.path.join(DOCS_DIR, 'summary_report.odt'),
        os.path.join(DOCS_DIR, 'consolidated.pdf'),
        os.path.join(DOCS_DIR, 'summary_report.pdf'),
        os.path.join(WORKDIR, 'Desktop', 'completion_log.txt'),
    ]
    for f in golden_artifacts:
        if os.path.exists(f):
            os.remove(f)
            print(f'  [REMOVED golden artifact] {f}')

    # GUI-ready startup: open automation_spec.odt in Writer so the agent can read it
    launch_gui(f'libreoffice --writer "{spec_path}"', delay_sec=2.0)
    # Also open the file manager showing Documents folder
    launch_gui(f'nautilus "{DOCS_DIR}"', delay_sec=1.0)

    print('GUI_READY: launched LibreOffice Writer with automation_spec.odt and Nautilus')


main()
