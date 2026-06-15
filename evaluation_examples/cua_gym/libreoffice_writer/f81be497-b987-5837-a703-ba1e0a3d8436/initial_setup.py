"""
Initial Setup: Create master document with subdocuments in incorrect order
Task ID: writer_rm_084
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_084'

# Subdocument content - realistic academic paper sections
SUBDOC_CONTENT = {
    'Abstract.odt': {
        'title': 'Abstract',
        'body': [
            'This paper presents a comprehensive analysis of machine learning approaches for predicting '
            'urban traffic congestion patterns in metropolitan areas. Using a dataset of 2.3 million GPS '
            'records collected over 18 months from the Seoul Metropolitan Transport Network, we evaluate '
            'the performance of gradient boosted trees, recurrent neural networks, and graph attention '
            'networks for short-term and medium-term traffic flow prediction.',
            'Our results demonstrate that graph attention networks achieve superior performance for '
            'intersection-level predictions (RMSE 4.23, MAE 2.87), while gradient boosted trees remain '
            'competitive for corridor-level aggregations. We further propose a hybrid ensemble approach '
            'that reduces prediction error by 12.4% compared to individual models.',
            'Keywords: traffic prediction, graph neural networks, ensemble learning, urban mobility'
        ]
    },
    'Introduction.odt': {
        'title': 'Introduction',
        'body': [
            'Urban traffic congestion costs the global economy an estimated $1.4 trillion annually in '
            'lost productivity, excess fuel consumption, and environmental degradation (INRIX, 2024). '
            'As metropolitan populations continue to grow, intelligent transportation systems (ITS) that '
            'can accurately predict and mitigate congestion have become a critical infrastructure priority.',
            'Traditional traffic prediction models relied on statistical methods such as ARIMA and Kalman '
            'filtering, which assume linear temporal dependencies and struggle to capture the complex '
            'spatiotemporal interactions inherent in urban road networks. The advent of deep learning has '
            'opened new avenues for modeling these nonlinear relationships.',
            'Recent advances in graph neural networks (GNNs) have shown particular promise for traffic '
            'prediction tasks, as they naturally encode the topological structure of road networks. '
            'However, most existing studies evaluate models on limited datasets or simplified network '
            'configurations that do not reflect real-world operational conditions.',
            'In this paper, we address three key research questions: (1) How do state-of-the-art deep '
            'learning architectures compare for multi-horizon traffic prediction? (2) Can graph-based '
            'models effectively leverage network topology for improved accuracy? (3) Does ensemble '
            'combination of heterogeneous models yield consistent improvements across prediction horizons?'
        ]
    },
    'References.odt': {
        'title': 'References',
        'body': [
            '[1] Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In '
            'Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and '
            'Data Mining (pp. 785-794).',
            '[2] Li, Y., Yu, R., Shahabi, C., & Liu, Y. (2018). Diffusion convolutional recurrent '
            'neural network: Data-driven traffic forecasting. In International Conference on Learning '
            'Representations.',
            '[3] Velickovic, P., Cucurull, G., Casanova, A., Romero, A., Lio, P., & Bengio, Y. (2018). '
            'Graph attention networks. In International Conference on Learning Representations.',
            '[4] Wu, Z., Pan, S., Long, G., Jiang, J., & Zhang, C. (2019). Graph WaveNet for deep '
            'spatial-temporal graph modeling. In Proceedings of the Twenty-Eighth International Joint '
            'Conference on Artificial Intelligence (pp. 1907-1913).',
            '[5] Zheng, C., Fan, X., Wang, C., & Qi, J. (2020). GMAN: A graph multi-attention network '
            'for traffic prediction. In Proceedings of the AAAI Conference on Artificial Intelligence, '
            '34(01), 1234-1241.',
            '[6] Jiang, W., & Luo, J. (2022). Graph neural network for traffic forecasting: A survey. '
            'Expert Systems with Applications, 207, 117921.',
            '[7] INRIX (2024). Global Traffic Scorecard. INRIX Research.',
            '[8] Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. Neural Computation, '
            '9(8), 1735-1780.'
        ]
    },
    'Methods.odt': {
        'title': 'Methods',
        'body': [
            '3.1 Data Collection and Preprocessing',
            'Traffic flow data was collected from 847 loop detectors and 1,203 GPS-equipped buses '
            'operating within the Seoul Metropolitan Area between January 2023 and June 2024. Raw '
            'data was aggregated into 5-minute intervals, yielding approximately 2.3 million records '
            'per detector over the study period.',
            'Missing values (approximately 3.2% of all records) were imputed using a spatiotemporal '
            'kriging approach that leverages both temporal autocorrelation and spatial proximity. '
            'Outliers exceeding three standard deviations from the rolling 24-hour mean were flagged '
            'and reviewed manually.',
            '3.2 Model Architectures',
            'We evaluate three model families: (a) XGBoost with engineered temporal and spatial '
            'features, (b) a stacked LSTM architecture with attention mechanism, and (c) a Graph '
            'Attention Network (GAT) operating on the road network adjacency graph.',
            '3.3 Evaluation Protocol',
            'Models were evaluated using a rolling-origin cross-validation scheme with a 30-day '
            'training window and prediction horizons of 15, 30, and 60 minutes. Performance metrics '
            'include RMSE, MAE, and MAPE computed at both intersection and corridor levels.'
        ]
    },
    'Results.odt': {
        'title': 'Results',
        'body': [
            '4.1 Intersection-Level Predictions',
            'Table 1 summarizes the prediction performance across all models and horizons at the '
            'intersection level. The GAT model achieves the lowest RMSE (4.23) and MAE (2.87) for '
            'the 15-minute horizon, representing a 7.8% improvement over the LSTM baseline.',
            'For the 60-minute horizon, the performance gap narrows considerably, with XGBoost '
            'achieving competitive results (RMSE 8.91 vs. GAT 8.54). This suggests that the '
            'topological advantages of graph-based models diminish for longer prediction windows.',
            '4.2 Corridor-Level Aggregations',
            'When predictions are aggregated to the corridor level, XGBoost demonstrates marginally '
            'superior performance (RMSE 3.12) compared to GAT (RMSE 3.28) for the 15-minute horizon. '
            'This finding is consistent with the hypothesis that spatial smoothing reduces the advantage '
            'of fine-grained topology modeling.',
            '4.3 Ensemble Performance',
            'The proposed hybrid ensemble, which combines predictions from all three model families '
            'using a learned weighting scheme, achieves consistent improvements across all horizons '
            'and granularity levels. The ensemble reduces RMSE by 12.4% compared to the best individual '
            'model at the intersection level.'
        ]
    },
    'Conclusion.odt': {
        'title': 'Conclusion',
        'body': [
            'This study provides a comprehensive evaluation of machine learning approaches for urban '
            'traffic prediction using a large-scale real-world dataset from the Seoul Metropolitan '
            'Transport Network. Our findings highlight the complementary strengths of different model '
            'architectures across prediction horizons and spatial granularities.',
            'Graph attention networks demonstrate clear advantages for short-term, intersection-level '
            'predictions by effectively leveraging road network topology. However, simpler gradient '
            'boosted tree models remain competitive for longer horizons and aggregated predictions, '
            'suggesting that practitioners should consider the specific use case when selecting models.',
            'The hybrid ensemble approach consistently outperforms individual models, indicating that '
            'model diversity is a valuable asset for traffic prediction systems. Future work should '
            'explore the integration of external data sources such as weather, events, and social media '
            'signals to further improve prediction accuracy.'
        ]
    }
}

def create_odt(filepath, title, body_paragraphs):
    """Create an ODF text document (.odt) using odfpy."""
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H
    from odf.style import Style, TextProperties, ParagraphProperties

    doc = OpenDocumentText()

    # Create heading style
    heading_style = Style(name="HeadingStyle", family="paragraph")
    heading_style.addElement(TextProperties(attributes={
        'fontsize': '16pt',
        'fontweight': 'bold'
    }))
    heading_style.addElement(ParagraphProperties(attributes={
        'margintop': '0.3cm',
        'marginbottom': '0.2cm'
    }))
    doc.styles.addElement(heading_style)

    # Add title as heading
    h = H(outlinelevel=1, text=title)
    doc.text.addElement(h)

    # Add body paragraphs
    for para_text in body_paragraphs:
        p = P(text=para_text)
        doc.text.addElement(p)

    doc.save(filepath)


def create_odm(filepath, subdoc_names):
    """
    Create an ODF master document (.odm) that links to subdocuments.
    ODM is essentially an ODT with text:section elements that reference subdocs.
    """
    from odf.opendocument import OpenDocumentText
    from odf.text import P, Section, SectionSource

    # Create as text document, we'll save as .odm
    doc = OpenDocumentText()

    # Add a title paragraph
    title_p = P(text='Research Paper - Machine Learning for Urban Traffic Prediction')
    doc.text.addElement(title_p)

    # Add sections that link to subdocuments
    for i, subdoc_name in enumerate(subdoc_names):
        section_name = subdoc_name.replace('.odt', '')

        # Create a section with a link to the subdocument
        section = Section(name=section_name)

        # Add section source pointing to the subdocument
        section_source = SectionSource()
        section_source.setAttribute('href', subdoc_name)
        section_source.setAttribute('filtername', 'writer8')
        section_source.setAttribute('sectionname', section_name)
        section.addElement(section_source)

        # Add placeholder text so the section isn't empty
        p = P(text=f'[Content from {subdoc_name}]')
        section.addElement(p)

        doc.text.addElement(section)

    doc.save(filepath)

    # Rename extension from .odt to .odm if needed (odfpy saves as .odt by default)
    # Actually, we need to modify the mimetype inside the zip to be the master doc type
    # The ODM mimetype is 'application/vnd.oasis.opendocument.text-master'

    # Fix the mimetype in the saved file
    import tempfile
    temp_path = filepath + '.tmp'

    with zipfile.ZipFile(filepath, 'r') as zin:
        with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'mimetype':
                    # Replace mimetype with master document type
                    zout.writestr(item, 'application/vnd.oasis.opendocument.text-master')
                elif item.filename == 'content.xml':
                    # Fix the content.xml to use proper xlink:href for sections
                    content = data.decode('utf-8')
                    # The section sources need xlink:href attributes
                    for subdoc_name in subdoc_names:
                        section_name = subdoc_name.replace('.odt', '')
                        # Fix href to use xlink:href
                        content = content.replace(
                            f'text:section-source text:href="{subdoc_name}"',
                            f'text:section-source xlink:href="{subdoc_name}"'
                        )
                    zout.writestr(item, content.encode('utf-8'))
                else:
                    zout.writestr(item, data)

    shutil.move(temp_path, filepath)


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
    # Create subdocument .odt files
    for filename, content in SUBDOC_CONTENT.items():
        filepath = os.path.join(WORKDIR, filename)
        create_odt(filepath, content['title'], content['body'])
        print(f'Created subdocument: {filepath}')

    # Create master document with INITIAL order (References in wrong position - 3rd)
    initial_order = [
        'Abstract.odt',
        'Introduction.odt',
        'References.odt',      # Incorrectly placed here (should be last)
        'Methods.odt',
        'Results.odt',
        'Conclusion.odt'
    ]

    odm_path = os.path.join(WORKDIR, 'Paper_Master.odm')
    create_odm(odm_path, initial_order)
    print(f'Created master document: {odm_path}')

    # GUI-ready: open the master document in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{odm_path}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with Paper_Master.odm')


create_initial()
