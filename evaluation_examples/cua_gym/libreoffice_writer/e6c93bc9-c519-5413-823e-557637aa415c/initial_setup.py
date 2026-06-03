"""
Initial Setup: Thesis document with tracked changes in Chapters 2 and 3
Task ID: writer_acad_037
Domain: libreoffice_writer

Creates a thesis-style document with:
- Chapter 1 (no tracked changes, just context)
- Chapter 2 with multiple tracked insertions and deletions
- Chapter 3 with multiple tracked insertions and deletions
"""

import os
import shlex
import subprocess
import time
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from lxml import etree
import copy

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_037'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'

AUTHOR = 'Dr. Elena Rodriguez'
DATE = '2026-03-15T10:30:00Z'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


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


def make_run_element(text, font_name='Times New Roman', font_size_pt=12, bold=False, italic=False):
    """Create a w:r element with run properties and text."""
    r = parse_xml(f'<w:r {nsdecls("w")}><w:t xml:space="preserve">{text}</w:t></w:r>')
    rpr = parse_xml(f'<w:rPr {nsdecls("w")}></w:rPr>')
    if font_name:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}"/>')
        rpr.append(rFonts)
    if font_size_pt:
        sz = parse_xml(f'<w:sz {nsdecls("w")} w:val="{font_size_pt * 2}"/>')
        rpr.append(sz)
    if bold:
        rpr.append(parse_xml(f'<w:b {nsdecls("w")}/>'))
    if italic:
        rpr.append(parse_xml(f'<w:i {nsdecls("w")}/>'))
    r.insert(0, rpr)
    return r


def make_ins_element(text, author=AUTHOR, date=DATE, **kwargs):
    """Create a w:ins revision mark wrapping a run."""
    ins = parse_xml(
        f'<w:ins {nsdecls("w")} w:id="{id(text) % 100000}" '
        f'w:author="{author}" w:date="{date}"/>'
    )
    r = make_run_element(text, **kwargs)
    ins.append(r)
    return ins


def make_del_element(original_text, author=AUTHOR, date=DATE, **kwargs):
    """Create a w:del revision mark wrapping a deleted run."""
    del_elem = parse_xml(
        f'<w:del {nsdecls("w")} w:id="{id(original_text) % 100000}" '
        f'w:author="{author}" w:date="{date}"/>'
    )
    r = make_run_element('placeholder', **kwargs)
    # Replace w:t with w:delText
    t_elem = r.find(qn('w:t'))
    r.remove(t_elem)
    del_text = parse_xml(
        f'<w:delText {nsdecls("w")} xml:space="preserve">{original_text}</w:delText>'
    )
    r.append(del_text)
    del_elem.append(r)
    return del_elem


def add_normal_paragraph(body, text, font_size_pt=12, bold=False, alignment=None,
                          space_before=None, space_after=None, heading_level=None):
    """Add a normal paragraph with a single run."""
    p = parse_xml(f'<w:p {nsdecls("w")}></w:p>')
    ppr = parse_xml(f'<w:pPr {nsdecls("w")}></w:pPr>')

    if heading_level is not None:
        pStyle = parse_xml(f'<w:pStyle {nsdecls("w")} w:val="Heading{heading_level}"/>')
        ppr.append(pStyle)

    if alignment:
        jc = parse_xml(f'<w:jc {nsdecls("w")} w:val="{alignment}"/>')
        ppr.append(jc)

    if space_before is not None:
        spacing = ppr.find(qn('w:spacing'))
        if spacing is None:
            spacing = parse_xml(f'<w:spacing {nsdecls("w")} w:before="{space_before}"/>')
            ppr.append(spacing)
        else:
            spacing.set(qn('w:before'), str(space_before))

    if space_after is not None:
        spacing = ppr.find(qn('w:spacing'))
        if spacing is None:
            spacing = parse_xml(f'<w:spacing {nsdecls("w")} w:after="{space_after}"/>')
            ppr.append(spacing)
        else:
            spacing.set(qn('w:after'), str(space_after))

    p.insert(0, ppr)

    r = make_run_element(text, font_size_pt=font_size_pt, bold=bold)
    p.append(r)
    body.append(p)
    return p


def add_tracked_paragraph(body, segments, space_after=None):
    """
    Add a paragraph with mixed normal text, insertions, and deletions.

    segments: list of tuples (type, text, kwargs)
      type: 'normal', 'ins', 'del'
    """
    p = parse_xml(f'<w:p {nsdecls("w")}></w:p>')
    ppr = parse_xml(f'<w:pPr {nsdecls("w")}></w:pPr>')
    if space_after is not None:
        spacing = parse_xml(f'<w:spacing {nsdecls("w")} w:after="{space_after}"/>')
        ppr.append(spacing)
    p.insert(0, ppr)

    for seg_type, text, kwargs in segments:
        if seg_type == 'normal':
            r = make_run_element(text, **kwargs)
            p.append(r)
        elif seg_type == 'ins':
            ins = make_ins_element(text, **kwargs)
            p.append(ins)
        elif seg_type == 'del':
            del_elem = make_del_element(text, **kwargs)
            p.append(del_elem)

    body.append(p)
    return p


def create_initial():
    doc = Document()

    # Set default style
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    # Page setup
    section = doc.sections[0]
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)

    body = doc.element.body

    # Remove any auto-generated empty paragraph
    for p in body.findall(qn('w:p')):
        body.remove(p)

    # ========== TITLE PAGE ==========
    add_normal_paragraph(body, 'Machine Learning Approaches for', font_size_pt=18, bold=True,
                         alignment='center', space_after=0)
    add_normal_paragraph(body, 'Climate Prediction Models', font_size_pt=18, bold=True,
                         alignment='center', space_after=240)
    add_normal_paragraph(body, 'A Thesis Submitted in Partial Fulfillment', font_size_pt=12,
                         alignment='center', space_after=0)
    add_normal_paragraph(body, 'of the Requirements for the Degree of', font_size_pt=12,
                         alignment='center', space_after=0)
    add_normal_paragraph(body, 'Doctor of Philosophy', font_size_pt=14, bold=True,
                         alignment='center', space_after=240)
    add_normal_paragraph(body, 'by Amara Okafor', font_size_pt=12, alignment='center', space_after=0)
    add_normal_paragraph(body, 'Department of Environmental Data Science', font_size_pt=12,
                         alignment='center', space_after=0)
    add_normal_paragraph(body, 'Pacific Northwest University', font_size_pt=12,
                         alignment='center', space_after=480)
    add_normal_paragraph(body, 'March 2026', font_size_pt=12, alignment='center', space_after=240)

    # ========== CHAPTER 1 (no tracked changes - just context) ==========
    add_normal_paragraph(body, 'Chapter 1: Introduction', font_size_pt=16, bold=True,
                         space_before=360, space_after=240)
    add_normal_paragraph(body,
        'Climate change represents one of the most pressing challenges of the twenty-first century. '
        'Accurate prediction of regional climate patterns is essential for developing effective '
        'adaptation strategies and mitigating the worst impacts of anthropogenic warming.',
        space_after=120)
    add_normal_paragraph(body,
        'Traditional numerical weather prediction models, while foundational, face inherent '
        'limitations in capturing the nonlinear dynamics of coupled atmosphere-ocean systems. '
        'Recent advances in machine learning have opened new avenues for improving prediction '
        'accuracy, particularly for medium-range and seasonal forecasting horizons.',
        space_after=120)
    add_normal_paragraph(body,
        'This thesis investigates the application of deep learning architectures to regional '
        'climate prediction, with a focus on precipitation and temperature anomaly forecasting '
        'in the Pacific Northwest region of North America.',
        space_after=240)

    # ========== CHAPTER 2 (with tracked changes) ==========
    add_normal_paragraph(body, 'Chapter 2: Literature Review', font_size_pt=16, bold=True,
                         space_before=360, space_after=240)

    # Para 2.1 - insertion in the middle
    add_tracked_paragraph(body, [
        ('normal', 'The application of neural networks to weather prediction dates back to the early 1990s, ', {}),
        ('ins', 'particularly the pioneering work of Hsieh and Tang (1998), ', {}),
        ('normal', 'when researchers first explored simple feedforward architectures for temperature forecasting.', {}),
    ], space_after=120)

    # Para 2.2 - deletion of outdated phrase
    add_tracked_paragraph(body, [
        ('normal', 'Convolutional neural networks have shown ', {}),
        ('del', 'moderate', {}),
        ('ins', 'remarkable', {}),
        ('normal', ' success in capturing spatial patterns within meteorological datasets, as demonstrated by Shi et al. (2015).', {}),
    ], space_after=120)

    # Para 2.3 - insertion at end
    add_tracked_paragraph(body, [
        ('normal', 'Recurrent architectures, including Long Short-Term Memory networks, have been widely adopted for time-series climate data due to their ability to model temporal dependencies.', {}),
        ('ins', ' More recently, transformer-based models have begun to surpass LSTM performance on benchmark datasets (Pathak et al., 2022).', {}),
    ], space_after=120)

    # Para 2.4 - deletion of a sentence
    add_tracked_paragraph(body, [
        ('normal', 'Transfer learning from large-scale atmospheric reanalysis datasets has emerged as a promising strategy for regions with limited observational data. ', {}),
        ('del', 'However, the computational cost remains prohibitively expensive for most research groups. ', {}),
        ('normal', 'ERA5 reanalysis data, in particular, has become a standard pretraining resource.', {}),
    ], space_after=120)

    # Para 2.5 - insertion replacing deletion
    add_tracked_paragraph(body, [
        ('normal', 'Ensemble methods combining ', {}),
        ('del', 'two or three', {}),
        ('ins', 'multiple diverse', {}),
        ('normal', ' neural network architectures have consistently outperformed individual models in probabilistic forecasting tasks (Rasp and Lerch, 2018).', {}),
    ], space_after=120)

    # Para 2.6 - pure insertion of new paragraph
    add_tracked_paragraph(body, [
        ('ins', 'Graph neural networks represent an emerging approach for modeling the irregular spatial structure of observational networks, offering advantages over grid-based methods (Keisler, 2022).', {}),
    ], space_after=240)

    # ========== CHAPTER 3 (with tracked changes) ==========
    add_normal_paragraph(body, 'Chapter 3: Methodology', font_size_pt=16, bold=True,
                         space_before=360, space_after=240)

    # Para 3.1 - insertion
    add_tracked_paragraph(body, [
        ('normal', 'Our experimental framework employs a ', {}),
        ('del', 'standard', {}),
        ('ins', 'modified', {}),
        ('normal', ' U-Net architecture adapted for spatiotemporal climate prediction.', {}),
    ], space_after=120)

    # Para 3.2 - deletion of a clause
    add_tracked_paragraph(body, [
        ('normal', 'The training dataset comprises 40 years of ERA5 reanalysis data at 0.25-degree spatial resolution, ', {}),
        ('del', 'restricted to the Northern Hemisphere, ', {}),
        ('normal', 'covering the period from 1979 to 2019.', {}),
    ], space_after=120)

    # Para 3.3 - insertion of methodological detail
    add_tracked_paragraph(body, [
        ('normal', 'We apply a sliding window approach with a 14-day input sequence to predict 7-day-ahead temperature and precipitation fields.', {}),
        ('ins', ' Data augmentation is performed through random temporal shifts and spatial cropping to improve generalization.', {}),
    ], space_after=120)

    # Para 3.4 - replacement
    add_tracked_paragraph(body, [
        ('normal', 'Model optimization uses the ', {}),
        ('del', 'standard Adam optimizer with a fixed learning rate of 0.001', {}),
        ('ins', 'AdamW optimizer with cosine annealing schedule and initial learning rate of 0.0003', {}),
        ('normal', ', with batch size of 32 distributed across four GPUs.', {}),
    ], space_after=120)

    # Para 3.5 - insertion of new sentence
    add_tracked_paragraph(body, [
        ('normal', 'Validation is performed using a temporal split, with 2015-2017 held out for validation and 2018-2019 reserved for final testing. ', {}),
        ('ins', 'We additionally perform five-fold cross-validation on the training period to assess model stability. ', {}),
        ('normal', 'Performance metrics include RMSE, MAE, and the Continuous Ranked Probability Score.', {}),
    ], space_after=120)

    # Para 3.6 - deletion of entire sentence
    add_tracked_paragraph(body, [
        ('normal', 'Baseline comparisons include persistence forecasts, climatological averages, and the operational GFS model output.', {}),
        ('del', ' We also include a simple linear regression baseline for reference.', {}),
    ], space_after=240)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
