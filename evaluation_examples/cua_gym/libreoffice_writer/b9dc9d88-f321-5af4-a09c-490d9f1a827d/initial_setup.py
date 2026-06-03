"""
Initial Setup: Create a LibreOffice Writer master document with 8 chapter subdocuments.
Task ID: writer_rm_077
Domain: libreoffice_writer

Initial state: ML_Textbook_Master.odm with 8 chapter subdocuments, no title or copyright content.
"""

import os
import shlex
import subprocess
import time
import zipfile
from xml.etree import ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_077'
OUTPUT = f'{WORKDIR}/ML_Textbook_Master.odm'

# ODF namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
    'svg': 'urn:oasis:names:tc:opendocument:xmlns:svg:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'meta': 'urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
    'dc': 'urn:oasis:names:tc:opendocument:xmlns:dc:1.0',
    'chart': 'urn:oasis:names:tc:opendocument:xmlns:chart:1.0',
    'form': 'urn:oasis:names:tc:opendocument:xmlns:form:1.0',
    'config': 'urn:oasis:names:tc:opendocument:xmlns:config:1.0',
    'manifest': 'urn:oasis:names:tc:opendocument:xmlns:manifest:1.0',
    'presentation': 'urn:oasis:names:tc:opendocument:xmlns:presentation:1.0',
}

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

def create_chapter_odt(filepath, chapter_num, chapter_title, content_paragraphs):
    """Create a simple ODT chapter file using odfpy."""
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H

    doc = OpenDocumentText()
    heading = H(outlinelevel=1)
    heading.addText(f"Chapter {chapter_num}: {chapter_title}")
    doc.text.addElement(heading)

    for para_text in content_paragraphs:
        p = P()
        p.addText(para_text)
        doc.text.addElement(p)

    doc.save(filepath)

def build_content_xml_initial(chapters):
    """Build content.xml for the initial ODM (sections only, no title/copyright)."""
    # Register namespaces to get clean prefixes
    for prefix, uri in NS.items():
        ET.register_namespace(prefix, uri)

    root = ET.Element(f'{{{NS["office"]}}}document-content')
    root.set(f'{{{NS["office"]}}}version', '1.2')

    # automatic-styles (empty for initial)
    ET.SubElement(root, f'{{{NS["office"]}}}automatic-styles')

    body = ET.SubElement(root, f'{{{NS["office"]}}}body')
    text_elem = ET.SubElement(body, f'{{{NS["office"]}}}text')

    # Add section references to each chapter
    for num, title, _ in chapters:
        section = ET.SubElement(text_elem, f'{{{NS["text"]}}}section')
        section.set(f'{{{NS["text"]}}}name', f'Chapter{num}Section')
        section.set(f'{{{NS["xlink"]}}}href', f'./chapter_{num:02d}.odt')
        section.set(f'{{{NS["xlink"]}}}type', 'simple')
        section.set(f'{{{NS["xlink"]}}}show', 'embed')
        section.set(f'{{{NS["xlink"]}}}actuate', 'onLoad')

        p = ET.SubElement(section, f'{{{NS["text"]}}}p')
        p.text = f'[Subdocument: Chapter {num} - {title}]'

    return ET.tostring(root, encoding='unicode', xml_declaration=True)

def create_odm_from_content_xml(content_xml_str, output_path):
    """Create an ODM file from content.xml string."""
    # Build minimal ODF package
    import io

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text-master" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/>
</manifest:manifest>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
  xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
  xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
  office:version="1.2">
  <office:styles/>
  <office:automatic-styles/>
  <office:master-styles>
    <style:master-page style:name="Standard" style:page-layout-name="pm1"/>
  </office:master-styles>
</office:document-styles>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
  xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
  office:version="1.2">
  <office:meta/>
</office:document-meta>'''

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first and stored (not deflated)
        zf.writestr('mimetype', 'application/vnd.oasis.opendocument.text-master',
                     compress_type=zipfile.ZIP_STORED)
        zf.writestr('META-INF/manifest.xml', manifest_xml)
        zf.writestr('content.xml', content_xml_str)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)

def create_initial():
    chapters = [
        (1, "Introduction to Machine Learning", [
            "Machine learning is a subset of artificial intelligence that focuses on building systems that learn from data.",
            "This chapter introduces the fundamental concepts, terminology, and mathematical foundations required for understanding modern machine learning algorithms.",
            "We explore the distinction between supervised, unsupervised, and reinforcement learning paradigms.",
        ]),
        (2, "Linear Models and Regression", [
            "Linear regression forms the backbone of many predictive modeling techniques used in practice today.",
            "We examine ordinary least squares, ridge regression, and LASSO regularization in the context of bias-variance tradeoff.",
            "Practical applications include housing price prediction and financial forecasting models.",
        ]),
        (3, "Classification Algorithms", [
            "Classification is the task of assigning discrete labels to input instances based on learned decision boundaries.",
            "This chapter covers logistic regression, support vector machines, and decision trees with detailed mathematical derivations.",
            "We discuss evaluation metrics including accuracy, precision, recall, F1-score, and ROC-AUC curves.",
        ]),
        (4, "Neural Networks and Deep Learning", [
            "Deep learning has revolutionized the field of artificial intelligence over the past decade.",
            "We present the architecture of feedforward networks, convolutional neural networks, and recurrent neural networks.",
            "Backpropagation, gradient descent variants, and regularization techniques such as dropout and batch normalization are covered in detail.",
        ]),
        (5, "Unsupervised Learning", [
            "Unsupervised learning algorithms discover hidden patterns in data without labeled examples.",
            "K-means clustering, hierarchical clustering, and DBSCAN are examined alongside dimensionality reduction methods.",
            "Principal component analysis and t-SNE visualization techniques are presented with practical examples.",
        ]),
        (6, "Ensemble Methods", [
            "Ensemble methods combine multiple models to achieve better predictive performance than any single model.",
            "Random forests, gradient boosting machines, and AdaBoost are explored with theoretical justifications.",
            "We discuss hyperparameter tuning strategies and cross-validation procedures for ensemble models.",
        ]),
        (7, "Natural Language Processing", [
            "Natural language processing enables machines to understand, interpret, and generate human language.",
            "This chapter covers word embeddings, attention mechanisms, and transformer architectures.",
            "Applications include sentiment analysis, machine translation, and large language models such as GPT and BERT.",
        ]),
        (8, "Reinforcement Learning", [
            "Reinforcement learning trains agents to make sequential decisions by maximizing cumulative rewards.",
            "We explore Markov decision processes, Q-learning, policy gradient methods, and actor-critic architectures.",
            "Case studies include game playing, robotics control, and autonomous navigation systems.",
        ]),
    ]

    # Create chapter ODT files
    for num, title, content in chapters:
        chapter_path = f'{WORKDIR}/chapter_{num:02d}.odt'
        create_chapter_odt(chapter_path, num, title, content)
        print(f'Created: {chapter_path}')

    # Build content.xml and create ODM
    content_xml = build_content_xml_initial(chapters)
    create_odm_from_content_xml(content_xml, OUTPUT)
    print(f'Master document created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')

create_initial()
