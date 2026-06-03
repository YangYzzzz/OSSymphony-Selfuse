"""
Initial Setup: Create a master-style document with TOC, captioned figures and tables
Task ID: writer_rm_078
Domain: libreoffice_writer

Creates a LibreOffice Writer document with:
- A Table of Contents at the beginning
- 6 sections (simulating subdocuments) with captioned figures and tables
- NO list of figures or list of tables (that's the task)
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_078'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odt'

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

def kill_libreoffice():
    """Kill any existing LibreOffice processes."""
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(2)

def create_document_via_uno():
    """Create the document using LibreOffice UNO macro."""

    macro_script = r'''
import uno
import time
import os
import sys

def connect_to_lo():
    """Connect to running LibreOffice instance."""
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", localContext)
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    return desktop, smgr, ctx

def create_initial_document():
    desktop, smgr, ctx = connect_to_lo()

    # Create new Writer document
    doc = desktop.loadComponentFromURL(
        "private:factory/swriter", "_blank", 0, ())
    text = doc.getText()
    cursor = text.createTextCursor()

    # --- Document Title ---
    cursor.setPropertyValue("ParaStyleName", "Heading 1")
    text.insertString(cursor, "Research Report: Advanced Data Analytics in Healthcare Systems", False)
    text.insertControlCharacter(cursor, 0, False)  # PARAGRAPH_BREAK

    # Reset to default paragraph
    cursor.setPropertyValue("ParaStyleName", "Default Paragraph Style")
    text.insertString(cursor, "", False)

    # --- Insert Table of Contents ---
    toc = doc.createInstance("com.sun.star.text.ContentIndex")
    toc.setPropertyValue("CreateFromOutline", True)
    toc.setPropertyValue("Level", 3)
    toc.setPropertyValue("Title", "Table of Contents")
    text.insertTextContent(cursor, toc, False)
    text.insertControlCharacter(cursor, 0, False)

    # ==========================================
    # Section 1: Introduction
    # ==========================================
    cursor.setPropertyValue("ParaStyleName", "Heading 1")
    text.insertString(cursor, "1. Introduction", False)
    text.insertControlCharacter(cursor, 0, False)

    cursor.setPropertyValue("ParaStyleName", "Default Paragraph Style")
    text.insertString(cursor, "The healthcare industry has undergone a significant transformation in recent years, driven by the adoption of advanced data analytics and artificial intelligence. This report examines the current state of data-driven decision making in healthcare systems across multiple institutions.", False)
    text.insertControlCharacter(cursor, 0, False)

    text.insertString(cursor, "Our research spans six major healthcare networks, encompassing over 200 facilities and serving approximately 15 million patients annually. The findings presented here represent three years of collaborative research between academic institutions and healthcare providers.", False)
    text.insertControlCharacter(cursor, 0, False)

    # Figure 1 - Insert a text frame to simulate a figure with caption
    # We use the caption sequence mechanism
    cursor.setPropertyValue("ParaStyleName", "Default Paragraph Style")
    text.insertString(cursor, "[Figure placeholder: Healthcare Analytics Framework Diagram]", False)
    text.insertControlCharacter(cursor, 0, False)

    # Insert Figure caption using sequence field
    cursor.setPropertyValue("ParaStyleName", "Default Paragraph Style")
    figField1 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    figField1.setPropertyValue("SubType", 0)  # SEQUENCE
    figField1.setPropertyValue("NumberingType", 4)  # ARABIC

    # Create or get the Figure number variable
    masters = doc.getTextFieldMasters()
    fig_master_name = "com.sun.star.text.fieldmaster.SetExpression.Figure"
    if not masters.hasByName(fig_master_name):
        fig_master = doc.createInstance("com.sun.star.text.fieldmaster.SetExpression")
        fig_master.setPropertyValue("Name", "Figure")
        fig_master.setPropertyValue("SubType", 1)  # SEQUENCE

    figField1.setPropertyValue("Content", "Figure")
    figField1.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Figure ", False)
    text.insertTextContent(cursor, figField1, False)
    text.insertString(cursor, ": Healthcare Analytics Framework Overview", False)
    text.insertControlCharacter(cursor, 0, False)

    # Table 1
    cursor.setPropertyValue("ParaStyleName", "Default Paragraph Style")
    table1 = doc.createInstance("com.sun.star.text.TextTable")
    table1.initialize(4, 3)
    text.insertTextContent(cursor, table1, False)

    table1.getCellByPosition(0, 0).setString("Institution")
    table1.getCellByPosition(1, 0).setString("Patients (millions)")
    table1.getCellByPosition(2, 0).setString("Analytics Maturity")
    table1.getCellByPosition(0, 1).setString("Metro Health Network")
    table1.getCellByPosition(1, 1).setValue(4.2)
    table1.getCellByPosition(2, 1).setString("Advanced")
    table1.getCellByPosition(0, 2).setString("Valley Medical Center")
    table1.getCellByPosition(1, 2).setValue(2.8)
    table1.getCellByPosition(2, 2).setString("Intermediate")
    table1.getCellByPosition(0, 3).setString("Coastal Healthcare Group")
    table1.getCellByPosition(1, 3).setValue(3.5)
    table1.getCellByPosition(2, 3).setString("Advanced")

    text.insertControlCharacter(cursor, 0, False)

    # Table caption
    tblMasterName = "com.sun.star.text.fieldmaster.SetExpression.Table"
    if not masters.hasByName(tblMasterName):
        tbl_master = doc.createInstance("com.sun.star.text.fieldmaster.SetExpression")
        tbl_master.setPropertyValue("Name", "Table")
        tbl_master.setPropertyValue("SubType", 1)

    tblField1 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    tblField1.setPropertyValue("SubType", 0)
    tblField1.setPropertyValue("NumberingType", 4)
    tblField1.setPropertyValue("Content", "Table")
    tblField1.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Table ", False)
    text.insertTextContent(cursor, tblField1, False)
    text.insertString(cursor, ": Healthcare Network Overview", False)
    text.insertControlCharacter(cursor, 0, False)

    # ==========================================
    # Section 2: Methodology
    # ==========================================
    cursor.setPropertyValue("ParaStyleName", "Heading 1")
    text.insertString(cursor, "2. Methodology", False)
    text.insertControlCharacter(cursor, 0, False)

    cursor.setPropertyValue("ParaStyleName", "Default Paragraph Style")
    text.insertString(cursor, "Our research methodology combines quantitative analysis of electronic health records with qualitative assessments of clinical workflows. We employed a mixed-methods approach that included retrospective data analysis, prospective observational studies, and structured interviews with healthcare professionals.", False)
    text.insertControlCharacter(cursor, 0, False)

    text.insertString(cursor, "Data collection occurred between January 2023 and December 2025, with quarterly benchmarking assessments conducted at each participating institution. Statistical analysis was performed using R version 4.3 and Python 3.11 with the scikit-learn and TensorFlow frameworks.", False)
    text.insertControlCharacter(cursor, 0, False)

    # Figure 2
    text.insertString(cursor, "[Figure placeholder: Research Methodology Flowchart]", False)
    text.insertControlCharacter(cursor, 0, False)

    figField2 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    figField2.setPropertyValue("SubType", 0)
    figField2.setPropertyValue("NumberingType", 4)
    figField2.setPropertyValue("Content", "Figure")
    figField2.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Figure ", False)
    text.insertTextContent(cursor, figField2, False)
    text.insertString(cursor, ": Research Methodology and Data Collection Process", False)
    text.insertControlCharacter(cursor, 0, False)

    # Table 2
    table2 = doc.createInstance("com.sun.star.text.TextTable")
    table2.initialize(5, 4)
    text.insertTextContent(cursor, table2, False)

    table2.getCellByPosition(0, 0).setString("Phase")
    table2.getCellByPosition(1, 0).setString("Duration")
    table2.getCellByPosition(2, 0).setString("Sample Size")
    table2.getCellByPosition(3, 0).setString("Method")
    table2.getCellByPosition(0, 1).setString("Phase 1: Data Collection")
    table2.getCellByPosition(1, 1).setString("6 months")
    table2.getCellByPosition(2, 1).setString("50,000 records")
    table2.getCellByPosition(3, 1).setString("Retrospective")
    table2.getCellByPosition(0, 2).setString("Phase 2: Analysis")
    table2.getCellByPosition(1, 2).setString("4 months")
    table2.getCellByPosition(2, 2).setString("45,000 records")
    table2.getCellByPosition(3, 2).setString("Statistical")
    table2.getCellByPosition(0, 3).setString("Phase 3: Validation")
    table2.getCellByPosition(1, 3).setString("3 months")
    table2.getCellByPosition(2, 3).setString("10,000 records")
    table2.getCellByPosition(3, 3).setString("Prospective")
    table2.getCellByPosition(0, 4).setString("Phase 4: Reporting")
    table2.getCellByPosition(1, 4).setString("2 months")
    table2.getCellByPosition(2, 4).setString("N/A")
    table2.getCellByPosition(3, 4).setString("Synthesis")

    text.insertControlCharacter(cursor, 0, False)

    tblField2 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    tblField2.setPropertyValue("SubType", 0)
    tblField2.setPropertyValue("NumberingType", 4)
    tblField2.setPropertyValue("Content", "Table")
    tblField2.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Table ", False)
    text.insertTextContent(cursor, tblField2, False)
    text.insertString(cursor, ": Research Phases and Parameters", False)
    text.insertControlCharacter(cursor, 0, False)

    # ==========================================
    # Section 3: Patient Outcome Analysis
    # ==========================================
    cursor.setPropertyValue("ParaStyleName", "Heading 1")
    text.insertString(cursor, "3. Patient Outcome Analysis", False)
    text.insertControlCharacter(cursor, 0, False)

    cursor.setPropertyValue("ParaStyleName", "Default Paragraph Style")
    text.insertString(cursor, "Analysis of patient outcomes across participating institutions revealed significant improvements in key performance indicators following the implementation of analytics-driven protocols. Emergency department wait times decreased by an average of 23%, while readmission rates dropped by 15% within the first year of implementation.", False)
    text.insertControlCharacter(cursor, 0, False)

    # Figure 3
    text.insertString(cursor, "[Figure placeholder: Patient Outcome Trends 2023-2025]", False)
    text.insertControlCharacter(cursor, 0, False)

    figField3 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    figField3.setPropertyValue("SubType", 0)
    figField3.setPropertyValue("NumberingType", 4)
    figField3.setPropertyValue("Content", "Figure")
    figField3.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Figure ", False)
    text.insertTextContent(cursor, figField3, False)
    text.insertString(cursor, ": Patient Outcome Improvement Trends (2023-2025)", False)
    text.insertControlCharacter(cursor, 0, False)

    # Table 3
    table3 = doc.createInstance("com.sun.star.text.TextTable")
    table3.initialize(4, 4)
    text.insertTextContent(cursor, table3, False)

    table3.getCellByPosition(0, 0).setString("Metric")
    table3.getCellByPosition(1, 0).setString("Baseline")
    table3.getCellByPosition(2, 0).setString("Year 1")
    table3.getCellByPosition(3, 0).setString("Year 3")
    table3.getCellByPosition(0, 1).setString("ED Wait Time (min)")
    table3.getCellByPosition(1, 1).setValue(142)
    table3.getCellByPosition(2, 1).setValue(118)
    table3.getCellByPosition(3, 1).setValue(109)
    table3.getCellByPosition(0, 2).setString("30-Day Readmission %")
    table3.getCellByPosition(1, 2).setValue(18.5)
    table3.getCellByPosition(2, 2).setValue(16.2)
    table3.getCellByPosition(3, 2).setValue(15.7)
    table3.getCellByPosition(0, 3).setString("Patient Satisfaction")
    table3.getCellByPosition(1, 3).setValue(72)
    table3.getCellByPosition(2, 3).setValue(81)
    table3.getCellByPosition(3, 3).setValue(87)

    text.insertControlCharacter(cursor, 0, False)

    tblField3 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    tblField3.setPropertyValue("SubType", 0)
    tblField3.setPropertyValue("NumberingType", 4)
    tblField3.setPropertyValue("Content", "Table")
    tblField3.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Table ", False)
    text.insertTextContent(cursor, tblField3, False)
    text.insertString(cursor, ": Key Patient Outcome Metrics", False)
    text.insertControlCharacter(cursor, 0, False)

    # ==========================================
    # Section 4: Predictive Modeling Results
    # ==========================================
    cursor.setPropertyValue("ParaStyleName", "Heading 1")
    text.insertString(cursor, "4. Predictive Modeling Results", False)
    text.insertControlCharacter(cursor, 0, False)

    cursor.setPropertyValue("ParaStyleName", "Default Paragraph Style")
    text.insertString(cursor, "Machine learning models trained on structured EHR data demonstrated promising accuracy in predicting adverse events. The gradient boosting classifier achieved an AUC of 0.89 for sepsis prediction, while the deep learning model for cardiac event risk stratification reached an AUC of 0.91.", False)
    text.insertControlCharacter(cursor, 0, False)

    # Figure 4
    text.insertString(cursor, "[Figure placeholder: ROC Curves for Predictive Models]", False)
    text.insertControlCharacter(cursor, 0, False)

    figField4 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    figField4.setPropertyValue("SubType", 0)
    figField4.setPropertyValue("NumberingType", 4)
    figField4.setPropertyValue("Content", "Figure")
    figField4.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Figure ", False)
    text.insertTextContent(cursor, figField4, False)
    text.insertString(cursor, ": ROC Curves for Predictive Models", False)
    text.insertControlCharacter(cursor, 0, False)

    # Figure 5
    text.insertString(cursor, "[Figure placeholder: Feature Importance Analysis]", False)
    text.insertControlCharacter(cursor, 0, False)

    figField5 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    figField5.setPropertyValue("SubType", 0)
    figField5.setPropertyValue("NumberingType", 4)
    figField5.setPropertyValue("Content", "Figure")
    figField5.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Figure ", False)
    text.insertTextContent(cursor, figField5, False)
    text.insertString(cursor, ": Feature Importance Rankings for Sepsis Prediction Model", False)
    text.insertControlCharacter(cursor, 0, False)

    # Table 4
    table4 = doc.createInstance("com.sun.star.text.TextTable")
    table4.initialize(5, 3)
    text.insertTextContent(cursor, table4, False)

    table4.getCellByPosition(0, 0).setString("Model")
    table4.getCellByPosition(1, 0).setString("AUC")
    table4.getCellByPosition(2, 0).setString("F1 Score")
    table4.getCellByPosition(0, 1).setString("Logistic Regression")
    table4.getCellByPosition(1, 1).setValue(0.76)
    table4.getCellByPosition(2, 1).setValue(0.71)
    table4.getCellByPosition(0, 2).setString("Random Forest")
    table4.getCellByPosition(1, 2).setValue(0.84)
    table4.getCellByPosition(2, 2).setValue(0.79)
    table4.getCellByPosition(0, 3).setString("Gradient Boosting")
    table4.getCellByPosition(1, 3).setValue(0.89)
    table4.getCellByPosition(2, 3).setValue(0.83)
    table4.getCellByPosition(0, 4).setString("Deep Learning (LSTM)")
    table4.getCellByPosition(1, 4).setValue(0.91)
    table4.getCellByPosition(2, 4).setValue(0.86)

    text.insertControlCharacter(cursor, 0, False)

    tblField4 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    tblField4.setPropertyValue("SubType", 0)
    tblField4.setPropertyValue("NumberingType", 4)
    tblField4.setPropertyValue("Content", "Table")
    tblField4.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Table ", False)
    text.insertTextContent(cursor, tblField4, False)
    text.insertString(cursor, ": Predictive Model Performance Comparison", False)
    text.insertControlCharacter(cursor, 0, False)

    # ==========================================
    # Section 5: Cost-Benefit Analysis
    # ==========================================
    cursor.setPropertyValue("ParaStyleName", "Heading 1")
    text.insertString(cursor, "5. Cost-Benefit Analysis", False)
    text.insertControlCharacter(cursor, 0, False)

    cursor.setPropertyValue("ParaStyleName", "Default Paragraph Style")
    text.insertString(cursor, "Implementation of analytics platforms required significant upfront investment, ranging from $2.5 million to $8.7 million depending on institution size. However, the return on investment was realized within 18-24 months for five of the six participating networks.", False)
    text.insertControlCharacter(cursor, 0, False)

    # Figure 6
    text.insertString(cursor, "[Figure placeholder: Cost-Benefit Timeline Chart]", False)
    text.insertControlCharacter(cursor, 0, False)

    figField6 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    figField6.setPropertyValue("SubType", 0)
    figField6.setPropertyValue("NumberingType", 4)
    figField6.setPropertyValue("Content", "Figure")
    figField6.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Figure ", False)
    text.insertTextContent(cursor, figField6, False)
    text.insertString(cursor, ": Return on Investment Timeline by Institution", False)
    text.insertControlCharacter(cursor, 0, False)

    # Table 5
    table5 = doc.createInstance("com.sun.star.text.TextTable")
    table5.initialize(4, 3)
    text.insertTextContent(cursor, table5, False)

    table5.getCellByPosition(0, 0).setString("Institution")
    table5.getCellByPosition(1, 0).setString("Investment ($M)")
    table5.getCellByPosition(2, 0).setString("ROI Period (months)")
    table5.getCellByPosition(0, 1).setString("Metro Health Network")
    table5.getCellByPosition(1, 1).setValue(8.7)
    table5.getCellByPosition(2, 1).setValue(18)
    table5.getCellByPosition(0, 2).setString("Valley Medical Center")
    table5.getCellByPosition(1, 2).setValue(3.2)
    table5.getCellByPosition(2, 2).setValue(22)
    table5.getCellByPosition(0, 3).setString("Coastal Healthcare Group")
    table5.getCellByPosition(1, 3).setValue(5.4)
    table5.getCellByPosition(2, 3).setValue(20)

    text.insertControlCharacter(cursor, 0, False)

    tblField5 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    tblField5.setPropertyValue("SubType", 0)
    tblField5.setPropertyValue("NumberingType", 4)
    tblField5.setPropertyValue("Content", "Table")
    tblField5.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Table ", False)
    text.insertTextContent(cursor, tblField5, False)
    text.insertString(cursor, ": Investment and ROI Summary", False)
    text.insertControlCharacter(cursor, 0, False)

    # ==========================================
    # Section 6: Conclusions and Recommendations
    # ==========================================
    cursor.setPropertyValue("ParaStyleName", "Heading 1")
    text.insertString(cursor, "6. Conclusions and Recommendations", False)
    text.insertControlCharacter(cursor, 0, False)

    cursor.setPropertyValue("ParaStyleName", "Default Paragraph Style")
    text.insertString(cursor, "The findings of this comprehensive study demonstrate that data analytics implementation in healthcare systems yields measurable improvements across clinical, operational, and financial dimensions. Institutions that adopted a phased approach with strong clinical governance achieved the best outcomes.", False)
    text.insertControlCharacter(cursor, 0, False)

    text.insertString(cursor, "We recommend that healthcare organizations prioritize investment in analytics infrastructure, focusing initially on high-impact areas such as sepsis prediction and readmission prevention. Staff training and change management programs are essential for successful adoption.", False)
    text.insertControlCharacter(cursor, 0, False)

    # Figure 7
    text.insertString(cursor, "[Figure placeholder: Implementation Roadmap]", False)
    text.insertControlCharacter(cursor, 0, False)

    figField7 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    figField7.setPropertyValue("SubType", 0)
    figField7.setPropertyValue("NumberingType", 4)
    figField7.setPropertyValue("Content", "Figure")
    figField7.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Figure ", False)
    text.insertTextContent(cursor, figField7, False)
    text.insertString(cursor, ": Recommended Implementation Roadmap", False)
    text.insertControlCharacter(cursor, 0, False)

    # Table 6
    table6 = doc.createInstance("com.sun.star.text.TextTable")
    table6.initialize(4, 3)
    text.insertTextContent(cursor, table6, False)

    table6.getCellByPosition(0, 0).setString("Priority")
    table6.getCellByPosition(1, 0).setString("Recommendation")
    table6.getCellByPosition(2, 0).setString("Expected Impact")
    table6.getCellByPosition(0, 1).setString("High")
    table6.getCellByPosition(1, 1).setString("Implement sepsis prediction")
    table6.getCellByPosition(2, 1).setString("15-20% mortality reduction")
    table6.getCellByPosition(0, 2).setString("High")
    table6.getCellByPosition(1, 2).setString("Deploy readmission risk model")
    table6.getCellByPosition(2, 2).setString("12-18% readmission reduction")
    table6.getCellByPosition(0, 3).setString("Medium")
    table6.getCellByPosition(1, 3).setString("Automate clinical documentation")
    table6.getCellByPosition(2, 3).setString("30% time savings")

    text.insertControlCharacter(cursor, 0, False)

    tblField6 = doc.createInstance("com.sun.star.text.textfield.SetExpression")
    tblField6.setPropertyValue("SubType", 0)
    tblField6.setPropertyValue("NumberingType", 4)
    tblField6.setPropertyValue("Content", "Table")
    tblField6.setPropertyValue("NumberFormat", 0)
    text.insertString(cursor, "Table ", False)
    text.insertTextContent(cursor, tblField6, False)
    text.insertString(cursor, ": Strategic Recommendations Summary", False)
    text.insertControlCharacter(cursor, 0, False)

    # Update the TOC
    toc.update()

    # Save as ODT
    from com.sun.star.beans import PropertyValue
    props = []
    p1 = PropertyValue()
    p1.Name = "FilterName"
    p1.Value = "writer8"
    props.append(p1)
    p2 = PropertyValue()
    p2.Name = "Overwrite"
    p2.Value = True
    props.append(p2)

    import unohelper
    url = unohelper.systemPathToFileUrl("/home/user/writer_rm_078.odt")
    doc.store(url, tuple(props))
    print("Document saved to /home/user/writer_rm_078.odt")

    # Close document
    doc.close(True)

create_initial_document()
'''

    # Write the UNO macro script to a temp file
    with open('/tmp/uno_create_initial.py', 'w') as f:
        f.write(macro_script)

    return macro_script


def create_document_headless():
    """Alternative approach: Use LibreOffice macro via command line."""

    # Create a Python script that uses UNO in headless mode
    script = '''#!/usr/bin/env python3
import subprocess
import sys
import os
import time

# Start LibreOffice in listening mode if not already running
lo_proc = subprocess.Popen(
    ['soffice', '--headless', '--norestore',
     '--accept=socket,host=localhost,port=2002;urp;StarOffice.ServiceManager'],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    env={**os.environ, 'DISPLAY': ':0'}
)
time.sleep(5)

# Now connect via UNO
import uno

localContext = uno.getComponentContext()
resolver = localContext.ServiceManager.createInstanceWithContext(
    "com.sun.star.bridge.UnoUrlResolver", localContext)

# Try connecting a few times
connected = False
for attempt in range(10):
    try:
        ctx = resolver.resolve(
            "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        connected = True
        break
    except:
        time.sleep(2)

if not connected:
    print("ERROR: Could not connect to LibreOffice")
    sys.exit(1)

smgr = ctx.ServiceManager
desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
'''
    return script


def create_initial_document_odf():
    """Create the initial document using odfpy library for ODF format."""
    from odf.opendocument import OpenDocumentText
    from odf import text as odftext
    from odf import table as odftable
    from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties, TableCellProperties, TableProperties
    from odf.text import P, H, Span, SequenceDecl, SequenceDecls, Sequence, TableOfContent, TableOfContentSource, IndexTitleTemplate, TableOfContentEntryTemplate, IndexSourceStyles, IndexSourceStyle

    doc = OpenDocumentText()

    # --- Create styles ---
    # Heading 1 style
    h1style = Style(name="Heading_1", family="paragraph", parentstylename="Heading")
    h1style.addElement(TextProperties(fontsize="18pt", fontweight="bold"))
    h1style.addElement(ParagraphProperties(margintop="0.4in", marginbottom="0.2in"))
    doc.styles.addElement(h1style)

    # Caption style
    capstyle = Style(name="Caption", family="paragraph")
    capstyle.addElement(TextProperties(fontsize="10pt", fontstyle="italic"))
    capstyle.addElement(ParagraphProperties(margintop="0.05in", marginbottom="0.15in"))
    doc.styles.addElement(capstyle)

    # Table style
    tstyle = Style(name="DataTable", family="table")
    tstyle.addElement(TableProperties(width="6.5in", align="margins"))
    doc.automaticstyles.addElement(tstyle)

    tcol_style = Style(name="DataTable.Col", family="table-column")
    tcol_style.addElement(TableColumnProperties(columnwidth="2.16in"))
    doc.automaticstyles.addElement(tcol_style)

    tcell_style = Style(name="DataTable.Cell", family="table-cell")
    tcell_style.addElement(TableCellProperties(padding="0.04in", border="0.05pt solid #000000"))
    doc.automaticstyles.addElement(tcell_style)

    # Sequence declarations for Figure and Table numbering
    seqdecls = SequenceDecls()
    seqdecls.addElement(SequenceDecl(attributes={'displayoutlinelevel': '0', 'name': 'Figure'}))
    seqdecls.addElement(SequenceDecl(attributes={'displayoutlinelevel': '0', 'name': 'Table'}))
    doc.text.addElement(seqdecls)

    # --- Document Title ---
    title = H(outlinelevel=1, text="Research Report: Advanced Data Analytics in Healthcare Systems")
    doc.text.addElement(title)

    # --- Table of Contents ---
    toc = TableOfContent(name="Table of Contents", protected=True)
    tocsrc = TableOfContentSource(outlinelevel=3)
    toc.addElement(tocsrc)
    doc.text.addElement(toc)

    # Helper functions
    fig_counter = [0]
    tbl_counter = [0]

    def add_heading(text_str, level=1):
        h = H(outlinelevel=level, text=text_str)
        doc.text.addElement(h)

    def add_paragraph(text_str):
        p = P(text=text_str)
        doc.text.addElement(p)

    def add_figure_caption(caption_text):
        fig_counter[0] += 1
        p = P(stylename="Caption")
        p.addText("Figure ")
        seq = Sequence(name="Figure", formula="oor:Figure+1")
        seq.addText(str(fig_counter[0]))
        p.addElement(seq)
        p.addText(f": {caption_text}")
        doc.text.addElement(p)

    def add_table_caption(caption_text):
        tbl_counter[0] += 1
        p = P(stylename="Caption")
        p.addText("Table ")
        seq = Sequence(name="Table", formula="oor:Table+1")
        seq.addText(str(tbl_counter[0]))
        p.addElement(seq)
        p.addText(f": {caption_text}")
        doc.text.addElement(p)

    def add_data_table(headers, rows):
        ncols = len(headers)
        nrows = len(rows) + 1
        tbl = odftable.Table(name=f"DataTable{tbl_counter[0]+1}", stylename="DataTable")
        for _ in range(ncols):
            tbl.addElement(odftable.TableColumn(stylename="DataTable.Col"))
        # Header row
        tr = odftable.TableRow()
        for h in headers:
            tc = odftable.TableCell(stylename="DataTable.Cell", valuetype="string")
            tc.addElement(P(text=h))
            tr.addElement(tc)
        tbl.addElement(tr)
        # Data rows
        for row in rows:
            tr = odftable.TableRow()
            for val in row:
                tc = odftable.TableCell(stylename="DataTable.Cell", valuetype="string")
                tc.addElement(P(text=str(val)))
                tr.addElement(tc)
            tbl.addElement(tr)
        doc.text.addElement(tbl)

    # ==========================================
    # Section 1: Introduction
    # ==========================================
    add_heading("1. Introduction")
    add_paragraph("The healthcare industry has undergone a significant transformation in recent years, driven by the adoption of advanced data analytics and artificial intelligence. This report examines the current state of data-driven decision making in healthcare systems across multiple institutions.")
    add_paragraph("Our research spans six major healthcare networks, encompassing over 200 facilities and serving approximately 15 million patients annually. The findings presented here represent three years of collaborative research between academic institutions and healthcare providers.")

    add_paragraph("[Figure placeholder: Healthcare Analytics Framework Diagram]")
    add_figure_caption("Healthcare Analytics Framework Overview")

    add_data_table(
        ["Institution", "Patients (millions)", "Analytics Maturity"],
        [
            ["Metro Health Network", "4.2", "Advanced"],
            ["Valley Medical Center", "2.8", "Intermediate"],
            ["Coastal Healthcare Group", "3.5", "Advanced"],
        ]
    )
    add_table_caption("Healthcare Network Overview")

    # ==========================================
    # Section 2: Methodology
    # ==========================================
    add_heading("2. Methodology")
    add_paragraph("Our research methodology combines quantitative analysis of electronic health records with qualitative assessments of clinical workflows. We employed a mixed-methods approach that included retrospective data analysis, prospective observational studies, and structured interviews with healthcare professionals.")
    add_paragraph("Data collection occurred between January 2023 and December 2025, with quarterly benchmarking assessments conducted at each participating institution. Statistical analysis was performed using R version 4.3 and Python 3.11 with the scikit-learn and TensorFlow frameworks.")

    add_paragraph("[Figure placeholder: Research Methodology Flowchart]")
    add_figure_caption("Research Methodology and Data Collection Process")

    add_data_table(
        ["Phase", "Duration", "Sample Size", "Method"],
        [
            ["Phase 1: Data Collection", "6 months", "50,000 records", "Retrospective"],
            ["Phase 2: Analysis", "4 months", "45,000 records", "Statistical"],
            ["Phase 3: Validation", "3 months", "10,000 records", "Prospective"],
            ["Phase 4: Reporting", "2 months", "N/A", "Synthesis"],
        ]
    )
    add_table_caption("Research Phases and Parameters")

    # ==========================================
    # Section 3: Patient Outcome Analysis
    # ==========================================
    add_heading("3. Patient Outcome Analysis")
    add_paragraph("Analysis of patient outcomes across participating institutions revealed significant improvements in key performance indicators following the implementation of analytics-driven protocols. Emergency department wait times decreased by an average of 23%, while readmission rates dropped by 15% within the first year of implementation.")

    add_paragraph("[Figure placeholder: Patient Outcome Trends 2023-2025]")
    add_figure_caption("Patient Outcome Improvement Trends (2023-2025)")

    add_data_table(
        ["Metric", "Baseline", "Year 1", "Year 3"],
        [
            ["ED Wait Time (min)", "142", "118", "109"],
            ["30-Day Readmission %", "18.5", "16.2", "15.7"],
            ["Patient Satisfaction", "72", "81", "87"],
        ]
    )
    add_table_caption("Key Patient Outcome Metrics")

    # ==========================================
    # Section 4: Predictive Modeling Results
    # ==========================================
    add_heading("4. Predictive Modeling Results")
    add_paragraph("Machine learning models trained on structured EHR data demonstrated promising accuracy in predicting adverse events. The gradient boosting classifier achieved an AUC of 0.89 for sepsis prediction, while the deep learning model for cardiac event risk stratification reached an AUC of 0.91.")

    add_paragraph("[Figure placeholder: ROC Curves for Predictive Models]")
    add_figure_caption("ROC Curves for Predictive Models")

    add_paragraph("[Figure placeholder: Feature Importance Analysis]")
    add_figure_caption("Feature Importance Rankings for Sepsis Prediction Model")

    add_data_table(
        ["Model", "AUC", "F1 Score"],
        [
            ["Logistic Regression", "0.76", "0.71"],
            ["Random Forest", "0.84", "0.79"],
            ["Gradient Boosting", "0.89", "0.83"],
            ["Deep Learning (LSTM)", "0.91", "0.86"],
        ]
    )
    add_table_caption("Predictive Model Performance Comparison")

    # ==========================================
    # Section 5: Cost-Benefit Analysis
    # ==========================================
    add_heading("5. Cost-Benefit Analysis")
    add_paragraph("Implementation of analytics platforms required significant upfront investment, ranging from $2.5 million to $8.7 million depending on institution size. However, the return on investment was realized within 18-24 months for five of the six participating networks.")

    add_paragraph("[Figure placeholder: Cost-Benefit Timeline Chart]")
    add_figure_caption("Return on Investment Timeline by Institution")

    add_data_table(
        ["Institution", "Investment ($M)", "ROI Period (months)"],
        [
            ["Metro Health Network", "8.7", "18"],
            ["Valley Medical Center", "3.2", "22"],
            ["Coastal Healthcare Group", "5.4", "20"],
        ]
    )
    add_table_caption("Investment and ROI Summary")

    # ==========================================
    # Section 6: Conclusions and Recommendations
    # ==========================================
    add_heading("6. Conclusions and Recommendations")
    add_paragraph("The findings of this comprehensive study demonstrate that data analytics implementation in healthcare systems yields measurable improvements across clinical, operational, and financial dimensions. Institutions that adopted a phased approach with strong clinical governance achieved the best outcomes.")
    add_paragraph("We recommend that healthcare organizations prioritize investment in analytics infrastructure, focusing initially on high-impact areas such as sepsis prediction and readmission prevention. Staff training and change management programs are essential for successful adoption.")

    add_paragraph("[Figure placeholder: Implementation Roadmap]")
    add_figure_caption("Recommended Implementation Roadmap")

    add_data_table(
        ["Priority", "Recommendation", "Expected Impact"],
        [
            ["High", "Implement sepsis prediction", "15-20% mortality reduction"],
            ["High", "Deploy readmission risk model", "12-18% readmission reduction"],
            ["Medium", "Automate clinical documentation", "30% time savings"],
        ]
    )
    add_table_caption("Strategic Recommendations Summary")

    # Save
    doc.save(OUTPUT)
    print(f"Initial document created: {OUTPUT}")


# Main execution
create_initial_document_odf()

# Open in LibreOffice Writer
launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
print(f'GUI_READY: launched LibreOffice Writer with DISPLAY=:0')
