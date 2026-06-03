"""
Initial Setup: Create a master document with 5 subdocuments for a dissertation.
Task ID: writer_rm_054
Domain: libreoffice_writer

Creates:
  - /home/user/Introduction.odt
  - /home/user/Methodology.odt
  - /home/user/Literature_Review.odt
  - /home/user/Results.odt
  - /home/user/Conclusion.odt
  - /home/user/writer_rm_054.odm (master document linking all 5 in initial order)

Initial order: Introduction, Methodology, Literature_Review, Results, Conclusion
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil
from xml.etree import ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_054'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odm'

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


def create_odt(filepath, title, body_paragraphs):
    """Create a simple .odt file with title and body paragraphs using raw XML."""
    # ODF namespaces
    ns = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
        'svg': 'urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0',
    }

    content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:automatic-styles>
    <style:style style:name="P_Title" style:family="paragraph">
      <style:paragraph-properties fo:text-align="start" fo:margin-bottom="0.3in"/>
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="P_Body" style:family="paragraph">
      <style:paragraph-properties fo:text-align="justify" fo:margin-bottom="0.15in"/>
      <style:text-properties fo:font-size="12pt"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:p text:style-name="P_Title">{title}</text:p>
'''
    for para in body_paragraphs:
        # Escape XML special chars
        para_escaped = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        content_xml += f'      <text:p text:style-name="P_Body">{para_escaped}</text:p>\n'

    content_xml += '''    </office:text>
  </office:body>
</office:document-content>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    office:version="1.2">
  <office:meta/>
</office:document-meta>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0in" fo:margin-bottom="0.08in"/>
      <style:text-properties fo:font-size="12pt" style:font-name="Liberation Serif"/>
    </style:default-style>
  </office:styles>
</office:document-styles>'''

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
                   manifest:version="1.2">
  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/>
</manifest:manifest>'''

    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('mimetype', 'application/vnd.oasis.opendocument.text')
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
        zf.writestr('META-INF/manifest.xml', manifest_xml)

    print(f'  Created: {filepath}')


def create_odm(filepath, subdoc_filenames):
    """Create a master document (.odm) that links to the given subdocument files."""
    # Build text:section elements for each subdocument
    sections_xml = ''
    for i, fname in enumerate(subdoc_filenames):
        section_name = fname.replace('.odt', '')
        sections_xml += f'''      <text:section text:style-name="Sect{i+1}" text:name="{section_name}">
        <text:section-source xlink:href="{fname}" text:filter-name="writer8"/>
      </text:section>
'''

    content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    office:version="1.2">
  <office:automatic-styles>
'''
    for i in range(len(subdoc_filenames)):
        content_xml += f'''    <style:style style:name="Sect{i+1}" style:family="section"/>
'''
    content_xml += f'''  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:p text:style-name="Standard">Dissertation Master Document</text:p>
{sections_xml}    </office:text>
  </office:body>
</office:document-content>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    office:version="1.2">
  <office:meta/>
</office:document-meta>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0in" fo:margin-bottom="0.08in"/>
      <style:text-properties fo:font-size="12pt" style:font-name="Liberation Serif"/>
    </style:default-style>
    <style:style style:name="Standard" style:family="paragraph" style:class="text"/>
  </office:styles>
</office:document-styles>'''

    manifest_entries = '''  <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text-master" manifest:full-path="/"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
  <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/>'''

    manifest_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
                   manifest:version="1.2">
{manifest_entries}
</manifest:manifest>'''

    with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first and uncompressed
        zf.writestr('mimetype', 'application/vnd.oasis.opendocument.text-master')
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)
        zf.writestr('META-INF/manifest.xml', manifest_xml)

    print(f'  Created master document: {filepath}')


def create_initial():
    # --- Create subdocument .odt files ---
    subdocs = {
        'Introduction.odt': {
            'title': 'Chapter 1: Introduction',
            'body': [
                'The rapid advancement of artificial intelligence and machine learning technologies has fundamentally transformed the landscape of modern computational research. This dissertation examines the intersection of deep learning architectures and their applications in natural language processing, with particular emphasis on transformer-based models.',
                'The motivation for this research stems from the growing demand for more efficient and accurate language understanding systems across various domains, including healthcare informatics, financial analysis, and educational technology. Current approaches, while achieving remarkable performance benchmarks, still face significant challenges in terms of computational efficiency and interpretability.',
                'This work makes three primary contributions to the field: (1) a novel attention mechanism that reduces computational complexity from quadratic to near-linear time, (2) a comprehensive evaluation framework for measuring model robustness across diverse linguistic tasks, and (3) an interpretability module that provides human-readable explanations of model predictions.',
                'The remainder of this dissertation is organized as follows: Chapter 2 presents a thorough review of the relevant literature, Chapter 3 details our methodology, Chapter 4 reports experimental results, and Chapter 5 concludes with a discussion of implications and future directions.',
            ]
        },
        'Methodology.odt': {
            'title': 'Chapter 2: Methodology',
            'body': [
                'This chapter describes the experimental methodology employed throughout this research. Our approach combines theoretical analysis with large-scale empirical evaluation across multiple benchmark datasets.',
                'We propose a modified transformer architecture, termed EfficientFormer, which incorporates sparse attention patterns and dynamic computation allocation. The architecture consists of three main components: (a) an adaptive tokenization layer, (b) a hierarchical attention module with learned sparsity masks, and (c) a multi-task prediction head.',
                'The adaptive tokenization layer processes input text through a byte-pair encoding scheme with vocabulary size V=32,000, followed by a learned subword merging step that reduces sequence length by approximately 15% without loss of semantic information.',
                'For the hierarchical attention module, we implement a two-level attention mechanism. The first level operates on local windows of size w=64 tokens, while the second level attends to compressed representations of each window. This design reduces the overall attention complexity from O(n^2) to O(n * sqrt(n)).',
                'Training was conducted on a cluster of 8 NVIDIA A100 GPUs over approximately 72 hours, using the AdamW optimizer with a cosine learning rate schedule. Initial learning rate was set to 3e-4 with a warmup period of 2,000 steps. Batch size was 256 sequences with maximum length of 512 tokens.',
                'All experiments were evaluated on four standard benchmarks: GLUE, SuperGLUE, SQuAD 2.0, and a custom domain-specific evaluation suite covering medical, legal, and scientific text.',
            ]
        },
        'Literature_Review.odt': {
            'title': 'Chapter 3: Literature Review',
            'body': [
                'This chapter provides a comprehensive review of the existing literature relevant to our research. We organize the discussion into four main areas: foundational transformer architectures, efficient attention mechanisms, multi-task learning frameworks, and interpretability methods for neural language models.',
                'The transformer architecture, introduced by Vaswani et al. (2017), established the self-attention mechanism as a fundamental building block for sequence modeling. The original model achieved state-of-the-art performance on machine translation tasks and has since become the basis for virtually all modern language models, including BERT (Devlin et al., 2019), GPT series (Radford et al., 2018, 2019; Brown et al., 2020), and T5 (Raffel et al., 2020).',
                'Efficient attention variants have been an active area of research. Linformer (Wang et al., 2020) projects key and value matrices to lower dimensions, achieving O(n) complexity. Performer (Choromanski et al., 2020) uses random feature maps to approximate softmax attention. LongFormer (Beltagy et al., 2020) combines local windowed attention with global attention on select tokens.',
                'More recently, Flash Attention (Dao et al., 2022) optimized the memory access patterns of standard attention, achieving significant speedups without approximation. However, these methods each involve different trade-offs between accuracy, memory usage, and wall-clock time.',
                'Multi-task learning in NLP has been explored extensively. MT-DNN (Liu et al., 2019) demonstrated that shared representations across diverse tasks improve generalization. UniLM (Dong et al., 2019) unified different language modeling objectives under a single architecture.',
                'Interpretability of deep learning models remains a critical challenge. Attention visualization (Clark et al., 2019) provides some insight but has been shown to not always correlate with feature importance (Jain and Wallace, 2019). Integrated Gradients (Sundararajan et al., 2017) and SHAP (Lundberg and Lee, 2017) offer more principled attribution methods.',
            ]
        },
        'Results.odt': {
            'title': 'Chapter 4: Results',
            'body': [
                'This chapter presents the experimental results of our EfficientFormer model across all evaluation benchmarks. We compare against five strong baselines: BERT-Large, RoBERTa-Large, DeBERTa-v3, the original Transformer, and Linformer.',
                'On the GLUE benchmark, EfficientFormer achieves an average score of 89.7, outperforming BERT-Large (87.2) and matching RoBERTa-Large (89.5) while using 40% fewer FLOPs during inference. The largest gains were observed on the MNLI task (+1.3 points over RoBERTa) and QQP (+0.8 points).',
                'SuperGLUE results show EfficientFormer achieving 88.1 overall, compared to DeBERTa-v3 at 89.0 and RoBERTa-Large at 86.3. While our model slightly underperforms the best baseline on this benchmark, the efficiency gains are substantial: inference throughput increases by 2.3x on GPU and 3.1x on CPU.',
                'On SQuAD 2.0, EfficientFormer achieves an F1 score of 91.4 and exact match of 88.7, competitive with the best published results while maintaining our efficiency advantages.',
                'The domain-specific evaluation suite reveals interesting patterns. On medical text, our model achieves 94.2% accuracy compared to 91.8% for BERT-Large, suggesting that the sparse attention mechanism may be particularly well-suited for technical prose with specialized vocabulary. On legal text, performance is comparable across all models (within 0.5%), while scientific text shows a 2.1% improvement.',
                'Ablation studies confirm the contribution of each architectural component. Removing the adaptive tokenization reduces GLUE score by 1.2 points. Replacing hierarchical attention with standard attention increases FLOPs by 2.8x without improving accuracy. Removing the multi-task prediction head reduces SuperGLUE performance by 0.9 points.',
            ]
        },
        'Conclusion.odt': {
            'title': 'Chapter 5: Conclusion',
            'body': [
                'This dissertation has presented EfficientFormer, a novel transformer architecture that achieves competitive performance with state-of-the-art language models while significantly reducing computational requirements. Our three main contributions - adaptive tokenization, hierarchical sparse attention, and an interpretability module - each address important limitations of existing approaches.',
                'The key finding is that carefully designed sparse attention patterns can match or exceed the performance of full attention on most NLP benchmarks, while reducing computational complexity from O(n^2) to O(n * sqrt(n)). This has practical implications for deploying large language models in resource-constrained environments.',
                'The interpretability module demonstrated that meaningful explanations can be extracted from intermediate attention patterns without substantially impacting model performance. User studies showed that researchers found our explanations more useful than raw attention visualizations in 78% of cases.',
                'Several limitations should be acknowledged. First, our evaluation focused primarily on English-language tasks; cross-lingual performance remains to be investigated. Second, the hierarchical attention may not be optimal for tasks requiring very long-range dependencies beyond our window sizes. Third, the interpretability module adds approximately 8% overhead to inference time.',
                'Future work will explore three directions: (1) extending the architecture to handle documents exceeding 10,000 tokens, (2) applying the approach to multimodal settings combining text and vision, and (3) developing more sophisticated interpretability tools that can explain model behavior at the reasoning level rather than the token level.',
                'In summary, this work demonstrates that efficiency and accuracy need not be at odds in modern NLP. By thoughtfully designing attention mechanisms that exploit the inherent structure of natural language, we can build models that are both powerful and practical for real-world deployment.',
            ]
        },
    }

    # Create each subdocument
    for filename, content in subdocs.items():
        create_odt(
            os.path.join(WORKDIR, filename),
            content['title'],
            content['body']
        )

    # Create master document with INITIAL order
    initial_order = [
        'Introduction.odt',
        'Methodology.odt',
        'Literature_Review.odt',
        'Results.odt',
        'Conclusion.odt',
    ]
    create_odm(OUTPUT, initial_order)

    # Launch the master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with master document')


create_initial()
