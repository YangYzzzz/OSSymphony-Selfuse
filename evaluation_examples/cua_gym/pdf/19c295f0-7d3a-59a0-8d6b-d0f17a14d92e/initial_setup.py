"""
Initial Setup: Create a 10-page academic article PDF with headings, paragraphs, bold/italic text, and footnotes.
Task ID: pdf_mbc_065
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/article.pdf'


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Build a 10-page academic article using PyMuPDF Story (HTML-based layout)
    html_content = """
<html>
<body>
<h1 style="font-size:22px; text-align:center;">Adaptive Neural Network Architectures for Real-Time Climate Modeling:<br/>A Comprehensive Multi-Scale Analysis</h1>
<p style="text-align:center; font-size:11px;"><b>Dr. Elena Vasquez</b><sup>1</sup>, <b>Prof. Rajesh Krishnamurthy</b><sup>2</sup>, <b>Dr. Sarah Mitchell</b><sup>1</sup>, <b>Dr. Tomasz Kowalski</b><sup>3</sup></p>
<p style="text-align:center; font-size:10px;"><i>1. Department of Atmospheric Sciences, Stanford University</i><br/><i>2. Institute for Computational Earth Science, ETH Zurich</i><br/><i>3. Faculty of Environmental Engineering, Warsaw University of Technology</i></p>

<h1 style="font-size:16px;">Abstract</h1>
<p style="font-size:11px; text-align:justify;">Climate modeling remains one of the most computationally demanding scientific endeavors of the twenty-first century. Traditional numerical weather prediction models, while physically grounded, require enormous computational resources and often struggle to capture sub-grid scale processes accurately. In this paper, we present <b>ClimateNet-3</b>, a novel deep learning framework that integrates multi-resolution convolutional neural networks with physics-informed loss functions to achieve real-time climate predictions at unprecedented spatial and temporal resolutions. Our approach combines the representational power of neural architectures with the physical constraints encoded in governing atmospheric equations, producing forecasts that are both data-driven and physically consistent. Experiments conducted on ERA5 reanalysis data spanning 1979 to 2023 demonstrate that ClimateNet-3 achieves a <b>34% reduction</b> in root mean square error for 72-hour temperature forecasts compared to the operational European Centre for Medium-Range Weather Forecasts model, while requiring only <i>one-fifteenth</i> of the computational resources. Furthermore, ensemble predictions generated through our stochastic dropout mechanism provide well-calibrated uncertainty estimates that outperform traditional ensemble methods in reliability diagrams across all forecast lead times examined.</p>

<p style="font-size:10px;"><i>Keywords: deep learning, climate modeling, neural networks, physics-informed machine learning, weather prediction, ensemble forecasting</i></p>

<h1 style="font-size:16px;">1. Introduction</h1>
<p style="font-size:11px; text-align:justify;">The accurate prediction of atmospheric phenomena across multiple spatial and temporal scales represents a fundamental challenge in earth system science. Since the pioneering work of Vilhelm Bjerknes in the early twentieth century and the subsequent development of numerical weather prediction by Lewis Fry Richardson, the field has undergone transformative changes driven by advances in computational power and observational capabilities. Modern operational weather forecasting systems, such as the Integrated Forecasting System operated by the European Centre for Medium-Range Weather Forecasts and the Global Forecast System maintained by the United States National Weather Service, rely on sophisticated numerical models that discretize the governing equations of atmospheric dynamics onto computational grids.</p>

<p style="font-size:11px; text-align:justify;">However, these conventional approaches face several fundamental limitations that constrain their predictive capability. First, the chaotic nature of atmospheric dynamics imposes inherent limits on deterministic predictability, as demonstrated by Edward Lorenz in his seminal 1963 paper on atmospheric convection. Second, sub-grid scale processes such as turbulent mixing, cloud microphysics, and convective precipitation must be parameterized using simplified representations that introduce systematic biases. Third, the computational cost of running high-resolution global simulations remains prohibitive for many operational and research applications, particularly in developing nations where infrastructure constraints limit access to high-performance computing resources.</p>

<p style="font-size:11px; text-align:justify;">Recent advances in deep learning have opened new possibilities for addressing these challenges. The success of neural networks in domains such as computer vision, natural language processing, and protein structure prediction has inspired a growing body of research applying similar techniques to atmospheric science. Notable contributions include the work of Weyn et al. on convolutional neural networks for medium-range forecasting, Bi et al. on the Pangu-Weather model, and Lam et al. on the GraphCast architecture, each demonstrating that data-driven approaches can achieve forecast skill comparable to or exceeding that of physics-based models for specific variables and lead times.</p>

<h2 style="font-size:13px;">1.1 Motivation and Research Questions</h2>
<p style="font-size:11px; text-align:justify;">Despite these encouraging results, several critical questions remain unanswered in the current literature. Most existing neural weather prediction models operate at relatively coarse spatial resolutions, typically ranging from 0.25 to 1.0 degrees latitude-longitude, which limits their ability to resolve mesoscale and microscale phenomena that are essential for regional climate impact assessments. Furthermore, the physical consistency of predictions generated by purely data-driven models remains a concern, as these systems may produce atmospheric states that violate fundamental conservation laws or exhibit unrealistic feature correlations.</p>

<p style="font-size:11px; text-align:justify;">This paper addresses these gaps by proposing ClimateNet-3, a hybrid architecture that incorporates three key innovations. First, we introduce a <b>multi-resolution feature pyramid network</b> that processes atmospheric variables at multiple spatial scales simultaneously, enabling the model to capture both large-scale circulation patterns and localized weather phenomena. Second, we develop a <b>physics-informed loss function</b> that penalizes violations of atmospheric conservation laws during training, ensuring that predicted states remain physically plausible. Third, we implement a <b>stochastic ensemble generation mechanism</b> based on Monte Carlo dropout that produces calibrated probabilistic forecasts without the computational overhead of running multiple deterministic model instances.</p>

<h2 style="font-size:13px;">1.2 Contributions</h2>
<p style="font-size:11px; text-align:justify;">The principal contributions of this work are fourfold: (a) the design and implementation of a multi-resolution neural architecture specifically optimized for atmospheric prediction tasks, (b) the formulation of differentiable physics-based constraints that can be seamlessly integrated into standard deep learning training pipelines, (c) a comprehensive evaluation framework that assesses both deterministic skill and probabilistic calibration across multiple variables and forecast horizons, and (d) a detailed computational efficiency analysis demonstrating the practical feasibility of deploying such models in resource-constrained operational settings.</p>

<h1 style="font-size:16px;">2. Related Work</h1>
<p style="font-size:11px; text-align:justify;">The application of machine learning to weather and climate prediction has a rich history spanning several decades. Early approaches focused on statistical post-processing of numerical model output, including model output statistics and analog methods for improving local forecasts. The advent of deep learning in the 2010s catalyzed a paradigm shift, with researchers exploring increasingly sophisticated neural architectures for direct weather prediction.</p>

<h2 style="font-size:13px;">2.1 Neural Weather Prediction Models</h2>
<p style="font-size:11px; text-align:justify;">The first generation of neural weather prediction models primarily employed fully connected networks or simple convolutional architectures operating on gridded atmospheric data. Dueben and Bauer (2018) demonstrated that a relatively simple convolutional network could produce skillful 500 hPa geopotential height forecasts at lead times up to five days. Weyn et al. (2020) extended this approach by introducing a cubed-sphere remapping technique that mitigated the geometric distortions inherent in latitude-longitude grids, achieving competitive performance with operational models for several upper-air variables.</p>

<p style="font-size:11px; text-align:justify;">Subsequent developments introduced more advanced architectures. Rasp and Thuerey (2021) applied a modified ResNet architecture to learn the full dynamics of a simplified atmospheric model, while Keisler (2022) explored graph neural networks as an alternative to convolutional approaches. The Pangu-Weather model developed by Bi et al. (2023) employed a three-dimensional Earth-specific transformer architecture that achieved state-of-the-art deterministic forecast skill across multiple variables and pressure levels. Concurrently, Lam et al. (2023) proposed GraphCast, which used message-passing neural networks on a multi-mesh representation of the globe, demonstrating superior performance to the High Resolution Forecast model of ECMWF for 90% of evaluated targets.</p>

<h2 style="font-size:13px;">2.2 Physics-Informed Machine Learning</h2>
<p style="font-size:11px; text-align:justify;">The integration of physical constraints into neural network training has emerged as a promising strategy for improving the generalization and physical realism of data-driven models. Raissi et al. (2019) introduced Physics-Informed Neural Networks, which embed governing differential equations directly into the loss function. Beucler et al. (2021) applied similar principles to atmospheric convection parameterization, demonstrating that conservation-constrained networks produced physically consistent tendencies while maintaining prediction accuracy. De Burgh-Day and Leeuwenburg (2023) provided a comprehensive review of machine learning for numerical weather prediction, highlighting the importance of physical constraints for ensuring reliable long-range predictions.</p>

<h1 style="font-size:16px;">3. Methodology</h1>
<p style="font-size:11px; text-align:justify;">In this section, we present the technical details of the ClimateNet-3 framework, including the multi-resolution architecture, the physics-informed training procedure, and the ensemble generation mechanism.</p>

<h2 style="font-size:13px;">3.1 Multi-Resolution Feature Pyramid Network</h2>
<p style="font-size:11px; text-align:justify;">The core of ClimateNet-3 is a feature pyramid network adapted for spherical atmospheric data. The input to the model consists of a tensor of atmospheric state variables defined on a regular latitude-longitude grid at 0.1-degree resolution, encompassing <b>37 pressure levels</b> and <b>78 surface and upper-air variables</b>. The architecture processes this input through a series of encoding and decoding stages at progressively coarser and finer resolutions, respectively.</p>

<p style="font-size:11px; text-align:justify;">At the encoding stage, the input tensor passes through four resolution blocks, each consisting of three residual convolutional layers followed by a spatial downsampling operation. We employ strided convolutions with a factor of two for downsampling, reducing the spatial resolution from 0.1 degrees to 0.2, 0.4, 0.8, and 1.6 degrees at successive levels. Each resolution block uses group normalization and the Gaussian Error Linear Unit activation function, which we found to provide more stable training dynamics compared to batch normalization and the Rectified Linear Unit in our preliminary experiments.</p>

<p style="font-size:11px; text-align:justify;">The decoder mirrors the encoder structure, using transposed convolutions for upsampling and incorporating skip connections from the corresponding encoder levels. At each decoder stage, features from the encoder are concatenated with the upsampled features before processing through residual blocks. This architecture enables the model to maintain fine-grained spatial information while leveraging multi-scale contextual features for prediction.</p>

<h2 style="font-size:13px;">3.2 Physics-Informed Loss Function</h2>
<p style="font-size:11px; text-align:justify;">A distinguishing feature of ClimateNet-3 is its training objective, which combines a standard data-fidelity term with differentiable approximations of fundamental atmospheric conservation laws. The total loss function is defined as a weighted combination of four components.</p>

<p style="font-size:11px; text-align:justify;">The <b>data fidelity loss</b> measures the discrepancy between predicted and observed atmospheric states using a latitude-weighted mean squared error that accounts for the convergence of meridians toward the poles. The <b>mass conservation constraint</b> penalizes predictions that violate the continuity equation by computing the divergence of the predicted mass flux field and comparing it to the observed tendency of surface pressure. The <b>energy conservation constraint</b> enforces approximate conservation of total atmospheric energy by penalizing large deviations in the vertically integrated sum of kinetic energy, potential energy, and internal energy between consecutive time steps. The <b>moisture conservation constraint</b> ensures that the predicted hydrological cycle remains balanced by penalizing discrepancies between the vertically integrated moisture flux convergence and the predicted precipitation minus evaporation field.</p>

<h2 style="font-size:13px;">3.3 Stochastic Ensemble Generation</h2>
<p style="font-size:11px; text-align:justify;">To generate probabilistic forecasts, we employ a Monte Carlo dropout approach in which dropout layers with a retention probability of 0.95 remain active during inference. By performing <i>N</i> forward passes with different dropout masks, we obtain an ensemble of <i>N</i> predictions that sample the model's epistemic uncertainty. We use <i>N</i> = 50 in all experiments reported here, as sensitivity analyses indicated diminishing returns in forecast reliability beyond this ensemble size.</p>

<p style="font-size:11px; text-align:justify;">The ensemble mean provides the deterministic forecast, while the ensemble spread serves as a flow-dependent measure of forecast uncertainty. We further calibrate the ensemble using a rank histogram recalibration procedure applied independently to each variable and grid point, which corrects for any residual under- or over-dispersion in the raw ensemble.</p>

<h1 style="font-size:16px;">4. Experimental Setup</h1>
<p style="font-size:11px; text-align:justify;">All experiments were conducted using the ERA5 reanalysis dataset produced by the European Centre for Medium-Range Weather Forecasts, which provides hourly estimates of atmospheric variables on a 0.25-degree regular latitude-longitude grid from 1979 to the present. We interpolated the ERA5 data to a 0.1-degree grid using bilinear interpolation for continuous variables and nearest-neighbor interpolation for discrete variables such as land-sea mask.</p>

<h2 style="font-size:13px;">4.1 Data Preparation</h2>
<p style="font-size:11px; text-align:justify;">The training dataset comprised six-hourly atmospheric snapshots from January 1979 through December 2017, yielding approximately 57,000 training samples. The validation set covered January 2018 through December 2019, and the test set spanned January 2020 through December 2023. This temporal split ensures that the model's performance is evaluated on data from a period not used during training or hyperparameter optimization, including the anomalous conditions associated with the 2020-2021 La Nina event and the exceptional European heat waves of 2022 and 2023.</p>

<p style="font-size:11px; text-align:justify;">Input variables included temperature, specific humidity, geopotential, and wind components at all 37 standard pressure levels from 1000 hPa to 1 hPa, along with surface variables including two-meter temperature, ten-meter wind components, mean sea level pressure, total column water vapor, and total precipitation. All variables were standardized using the training set mean and standard deviation, computed independently for each variable, pressure level, and calendar month to account for the annual cycle.</p>

<h2 style="font-size:13px;">4.2 Training Configuration</h2>
<p style="font-size:11px; text-align:justify;">The model was trained using the AdamW optimizer with an initial learning rate of 3 x 10<sup>-4</sup>, weight decay of 10<sup>-5</sup>, and a cosine annealing learning rate schedule with warm restarts. Training was distributed across 64 NVIDIA A100 GPUs using data parallelism, with a global batch size of 128 and gradient accumulation over two steps. The physics-informed loss weights were set to 1.0 for data fidelity, 0.1 for mass conservation, 0.05 for energy conservation, and 0.05 for moisture conservation, based on a grid search over the validation set. Total training required approximately <b>96 hours</b>, corresponding to roughly 200 epochs through the training dataset.</p>

<h1 style="font-size:16px;">5. Results and Discussion</h1>
<p style="font-size:11px; text-align:justify;">We evaluate ClimateNet-3 against three baseline systems: the operational High Resolution Forecast model of ECMWF, the Pangu-Weather model, and the GraphCast model. All evaluations are performed on the held-out test set covering 2020 to 2023, using standard verification metrics including root mean square error, anomaly correlation coefficient, and the continuous ranked probability score for probabilistic assessments.</p>

<h2 style="font-size:13px;">5.1 Deterministic Forecast Skill</h2>
<p style="font-size:11px; text-align:justify;">Table 1 presents the root mean square error for 500 hPa geopotential height predictions at lead times of 24, 72, 120, and 240 hours. ClimateNet-3 achieves the lowest RMSE at all lead times, with particularly pronounced improvements at the 72-hour and 120-hour horizons where sub-grid scale processes become increasingly important for forecast evolution. At the 72-hour lead time, ClimateNet-3 produces a global RMSE of <b>48.3 m</b> compared to 73.1 m for HRES, 52.7 m for Pangu-Weather, and 50.1 m for GraphCast, representing a 34% improvement over the operational model.</p>

<p style="font-size:11px; text-align:justify;">The performance advantage of ClimateNet-3 is even more pronounced in the tropics, where convective processes dominate the atmospheric energy budget and traditional parameterization schemes introduce substantial errors. For tropical two-meter temperature forecasts at 72 hours, ClimateNet-3 achieves an RMSE of <b>1.12 K</b> compared to 1.89 K for HRES, a 41% reduction. We attribute this improvement to the multi-resolution architecture's ability to capture the hierarchical structure of tropical convective organization, from individual thunderstorm cells at the finest resolution to planetary-scale wave patterns at the coarsest level.</p>

<h2 style="font-size:13px;">5.2 Probabilistic Forecast Calibration</h2>
<p style="font-size:11px; text-align:justify;">The reliability of probabilistic forecasts is assessed using rank histograms and reliability diagrams computed for 500 hPa temperature predictions. A perfectly calibrated ensemble produces a uniform rank histogram, indicating that the observed value is equally likely to fall in any rank position within the ensemble. The raw ClimateNet-3 ensemble exhibits slight under-dispersion at short lead times, manifested as a U-shaped rank histogram, but this bias is effectively corrected by the rank histogram recalibration procedure. After recalibration, the ensemble achieves reliability diagram slopes within 2% of the ideal diagonal for all lead times up to 240 hours, outperforming the 50-member ECMWF ensemble in terms of both spread-skill relationship and probabilistic skill scores.</p>

<h2 style="font-size:13px;">5.3 Computational Efficiency</h2>
<p style="font-size:11px; text-align:justify;">One of the most compelling advantages of ClimateNet-3 is its computational efficiency during inference. Generating a single deterministic 240-hour forecast on a single NVIDIA A100 GPU requires approximately <b>45 seconds</b>, compared to approximately <b>11 minutes</b> for a comparable forecast from the HRES model running on 1,024 CPU cores. Even the full 50-member ensemble can be generated in under 40 minutes on a single GPU, compared to the several hours required for the ECMWF ensemble on dedicated supercomputing infrastructure. This dramatic reduction in computational cost opens the possibility of deploying high-quality weather prediction systems in resource-constrained settings, including developing countries and disaster response scenarios where rapid forecast generation is critical.</p>

<h2 style="font-size:13px;">5.4 Regional Analysis</h2>
<p style="font-size:11px; text-align:justify;">To assess the geographical distribution of forecast improvements, we decomposed the global RMSE statistics into six major climate regions: the Arctic (north of 60 degrees North), Northern Hemisphere midlatitudes (30 to 60 degrees North), tropics (30 degrees South to 30 degrees North), Southern Hemisphere midlatitudes (30 to 60 degrees South), the Antarctic (south of 60 degrees South), and a separate maritime category covering all ocean grid points. This regional decomposition reveals substantial heterogeneity in model performance that is obscured by global averages.</p>

<p style="font-size:11px; text-align:justify;">In the Northern Hemisphere midlatitudes, where the density of observational data is highest and the baroclinic wave dynamics are well captured by both data-driven and physics-based models, ClimateNet-3 achieves a modest but statistically significant improvement of 12% in 500 hPa geopotential height RMSE compared to HRES. However, in the Southern Hemisphere midlatitudes, where observational coverage is sparser and the annular mode of variability dominates the large-scale circulation, the improvement increases to 28%. This larger improvement in data-sparse regions suggests that the neural network effectively leverages spatial correlations to compensate for reduced observational constraints, a capability that is less available to data assimilation systems used in operational numerical weather prediction.</p>

<p style="font-size:11px; text-align:justify;">The Arctic region presents a particularly interesting case study. Climate change has amplified warming in the polar regions at approximately twice the global average rate, a phenomenon known as Arctic amplification. This has led to rapid changes in sea ice extent and thickness that affect atmospheric circulation patterns throughout the Northern Hemisphere. ClimateNet-3 demonstrates a 38% reduction in two-meter temperature RMSE over the Arctic at 120-hour lead times, suggesting that the model has learned to represent the complex ice-atmosphere feedbacks that challenge conventional parameterization approaches. Notably, this improvement is most pronounced during the autumn freeze-up season, when the transition between open water and ice coverage introduces highly nonlinear dynamics that are difficult to capture with simple sea ice models.</p>

<h2 style="font-size:13px;">5.5 Extreme Weather Events</h2>
<p style="font-size:11px; text-align:justify;">A critical test for any weather prediction system is its ability to forecast extreme events, which have disproportionate societal and economic impacts. We evaluate ClimateNet-3 on four high-impact events from the test period: the January 2021 Spanish cold wave, the June 2021 Pacific Northwest heat dome, the July 2021 Western European floods, and the February 2023 Turkey-Syria earthquake-triggered winter storm. For each event, we assess the model's ability to predict anomalous conditions using the Anomaly Correlation Coefficient computed over the affected region.</p>

<p style="font-size:11px; text-align:justify;">For the Pacific Northwest heat dome, which set all-time temperature records across British Columbia, Washington, and Oregon, ClimateNet-3 produced useful forecasts with ACC exceeding 0.6 at lead times up to 8 days, compared to 5 days for HRES and 6 days for GraphCast. The model correctly identified the persistent omega blocking pattern responsible for the extreme heat, and ensemble members provided early indications of the potential for record-breaking temperatures beginning at the 10-day forecast horizon. Analysis of the attention maps within the multi-resolution architecture reveals that the model focused on the upstream Pacific sea surface temperature gradient and the subtropical jet stream position as key precursors, consistent with the meteorological analysis conducted after the event.</p>

<p style="font-size:11px; text-align:justify;">The Western European floods presented a different challenge, requiring accurate prediction of mesoscale precipitation patterns in complex terrain. ClimateNet-3 achieved a probability of detection of 0.78 for 24-hour accumulated precipitation exceeding 100 mm at 48-hour lead time, compared to 0.65 for HRES. The false alarm ratio was comparable between the two systems at approximately 0.3, indicating that the improved detection did not come at the cost of increased false positives. The ensemble probability of extreme precipitation exceeding observed values reached 40% at the 72-hour horizon, providing actionable warning information for emergency management authorities.</p>

<h2 style="font-size:13px;">5.6 Sensitivity Analysis</h2>
<p style="font-size:11px; text-align:justify;">We conducted ablation experiments to quantify the contribution of each architectural component to the overall forecast skill. Removing the physics-informed loss terms resulted in a 15% degradation in RMSE at the 120-hour lead time and a 23% degradation at 240 hours, confirming that the physical constraints are essential for maintaining forecast quality at extended ranges. Removing the multi-resolution architecture in favor of a single-resolution encoder-decoder produced a 9% degradation at all lead times, with the most pronounced impact on precipitation forecasts where the interaction between different spatial scales is particularly important.</p>

<p style="font-size:11px; text-align:justify;">The stochastic ensemble generation mechanism was compared against two alternative approaches for uncertainty quantification: a deep ensemble of five independently trained models and a variational inference approach using flipout layers. The Monte Carlo dropout method achieved comparable reliability to the deep ensemble while requiring only one-fifth of the training computational cost. The variational inference approach produced well-calibrated ensembles but at the expense of a 7% reduction in deterministic forecast skill, likely due to the additional regularization imposed by the variational objective. These results support our choice of Monte Carlo dropout as the most practical approach for operational ensemble generation.</p>

<h1 style="font-size:16px;">6. Limitations and Future Work</h1>
<p style="font-size:11px; text-align:justify;">While ClimateNet-3 demonstrates strong overall performance, several limitations warrant discussion. First, the model's skill degrades more rapidly than physics-based models for extended-range forecasts beyond 10 days, suggesting that the learned dynamics may not fully capture the slow-evolving components of the climate system such as stratospheric processes and ocean-atmosphere coupling. Second, the training dataset is limited to the ERA5 reanalysis period beginning in 1979, which may not adequately represent the full range of natural climate variability, including rare extreme events. Third, the current architecture is designed for global atmospheric prediction and does not account for regional-scale processes such as urban heat islands, orographic effects in complex terrain, or land-atmosphere feedbacks in heterogeneous landscapes.</p>

<h2 style="font-size:13px;">6.1 Interpretability and Trust</h2>
<p style="font-size:11px; text-align:justify;">A significant barrier to the operational adoption of neural weather prediction models is the limited interpretability of their predictions. Operational forecasters rely on their understanding of atmospheric dynamics to assess the plausibility of model outputs and communicate forecast uncertainty to decision-makers. While attention maps and gradient-based attribution methods provide some insight into the features driving neural network predictions, these techniques remain insufficient for building the level of trust required in high-stakes forecasting applications. Future work should explore more sophisticated interpretability techniques, including concept-based explanations that map neural network activations to physically meaningful atmospheric features such as jet streams, frontal zones, and convective systems.</p>

<h2 style="font-size:13px;">6.2 Data Assimilation Integration</h2>
<p style="font-size:11px; text-align:justify;">The current implementation of ClimateNet-3 uses ERA5 reanalysis data as both training input and initial conditions for forecasts. In an operational setting, the model would need to be initialized from real-time observations assimilated into a consistent atmospheric state estimate. Developing efficient data assimilation techniques for neural weather prediction models remains an open research challenge. Preliminary experiments with a simplified four-dimensional variational approach suggest that the differentiable nature of the neural network architecture enables gradient-based optimization of initial conditions, but further work is needed to handle the full complexity of the operational observing system, including satellite radiances, radio occultation data, and aircraft observations with irregular spatial and temporal sampling.</p>

<p style="font-size:11px; text-align:justify;">Future work will address these limitations through several avenues. We plan to extend the model to include coupled ocean and land surface components, enabling consistent multi-component earth system predictions. Additionally, we will explore the use of transfer learning techniques to adapt the global model for high-resolution regional applications, leveraging the pre-trained multi-resolution features as a starting point for fine-tuning on regional datasets.</p>

<h1 style="font-size:16px;">7. Conclusion</h1>
<p style="font-size:11px; text-align:justify;">This paper has presented ClimateNet-3, a multi-resolution physics-informed neural network for real-time climate modeling. By combining a feature pyramid architecture with differentiable atmospheric conservation constraints and a stochastic ensemble generation mechanism, ClimateNet-3 achieves state-of-the-art forecast skill while requiring a fraction of the computational resources consumed by traditional numerical weather prediction systems. Our results demonstrate that the integration of physical knowledge into deep learning architectures is not merely beneficial but essential for producing reliable atmospheric predictions, particularly for extended forecast horizons and in regions where sub-grid scale processes play a dominant role.</p>

<p style="font-size:11px; text-align:justify;">The practical implications of this work extend beyond academic research. The dramatic reduction in computational cost associated with neural weather prediction opens new possibilities for democratizing access to high-quality forecasts, supporting climate adaptation planning in vulnerable communities, and enabling rapid ensemble generation for extreme weather early warning systems. As the field continues to mature, we anticipate that hybrid approaches combining the strengths of physics-based and data-driven methods will become the standard paradigm for next-generation earth system prediction.</p>

<h1 style="font-size:16px;">References</h1>
<p style="font-size:10px;">1. Bi, K., Xie, L., Zhang, H., Chen, X., Gu, X., and Tian, Q. (2023). Accurate medium-range global weather forecasting with 3D neural networks. <i>Nature</i>, 619, 533-538.</p>
<p style="font-size:10px;">2. Beucler, T., Pritchard, M., Rasp, S., Ott, J., Baldi, P., and Gentine, P. (2021). Enforcing analytic constraints in neural networks emulating physical systems. <i>Physical Review Letters</i>, 126(9), 098302.</p>
<p style="font-size:10px;">3. De Burgh-Day, C. O. and Leeuwenburg, T. (2023). Machine learning for numerical weather and climate modelling: a review. <i>Geoscientific Model Development</i>, 16(22), 6433-6477.</p>
<p style="font-size:10px;">4. Dueben, P. D. and Bauer, P. (2018). Challenges and design choices for global weather and climate models based on machine learning. <i>Geoscientific Model Development</i>, 11(10), 3999-4009.</p>
<p style="font-size:10px;">5. Keisler, R. (2022). Forecasting global weather with graph neural networks. <i>arXiv preprint arXiv:2202.07575</i>.</p>
<p style="font-size:10px;">6. Lam, R., Sanchez-Gonzalez, A., Willson, M., et al. (2023). Learning skillful medium-range global weather forecasting. <i>Science</i>, 382(6677), 1416-1421.</p>
<p style="font-size:10px;">7. Lorenz, E. N. (1963). Deterministic nonperiodic flow. <i>Journal of Atmospheric Sciences</i>, 20(2), 130-141.</p>
<p style="font-size:10px;">8. Raissi, M., Perdikaris, P., and Karniadakis, G. E. (2019). Physics-informed neural networks: a deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. <i>Journal of Computational Physics</i>, 378, 686-707.</p>
<p style="font-size:10px;">9. Rasp, S. and Thuerey, N. (2021). Data-driven medium-range weather prediction with a Resnet pretrained on climate simulations. <i>Journal of Advances in Modeling Earth Systems</i>, 13(2), e2020MS002405.</p>
<p style="font-size:10px;">10. Weyn, J. A., Durran, D. R., and Caruana, R. (2020). Improving data-driven global weather prediction using deep convolutional neural networks on a cubed sphere. <i>Journal of Advances in Modeling Earth Systems</i>, 12(9), e2020MS002109.</p>

</body>
</html>
"""

    story = pymupdf.Story(html=html_content)
    writer = pymupdf.DocumentWriter(OUTPUT)
    content_rect = pymupdf.Rect(60, 60, 535, 782)  # margins within A4

    more = True
    while more:
        dev = writer.begin_page(pymupdf.Rect(0, 0, 595, 842))  # A4
        more, _ = story.place(content_rect)
        story.draw(dev)
        writer.end_page()

    writer.close()

    # Set metadata
    doc = pymupdf.open(OUTPUT)
    page_count = doc.page_count
    print(f'PDF has {page_count} pages')
    doc.set_metadata({
        "title": "Adaptive Neural Network Architectures for Real-Time Climate Modeling",
        "author": "Elena Vasquez, Rajesh Krishnamurthy, Sarah Mitchell, Tomasz Kowalski",
        "subject": "Deep Learning for Climate Prediction",
        "keywords": "deep learning, climate modeling, neural networks, weather prediction",
        "creator": "LaTeX with hyperref",
        "producer": "pdfTeX-1.40.25",
    })

    # Add TOC - clamp page numbers to actual page count
    pc = page_count
    toc = [
        [1, "Abstract", 1],
        [1, "1. Introduction", min(1, pc)],
        [2, "1.1 Motivation and Research Questions", min(2, pc)],
        [2, "1.2 Contributions", min(2, pc)],
        [1, "2. Related Work", min(3, pc)],
        [2, "2.1 Neural Weather Prediction Models", min(3, pc)],
        [2, "2.2 Physics-Informed Machine Learning", min(4, pc)],
        [1, "3. Methodology", min(4, pc)],
        [2, "3.1 Multi-Resolution Feature Pyramid Network", min(4, pc)],
        [2, "3.2 Physics-Informed Loss Function", min(5, pc)],
        [2, "3.3 Stochastic Ensemble Generation", min(5, pc)],
        [1, "4. Experimental Setup", min(6, pc)],
        [2, "4.1 Data Preparation", min(6, pc)],
        [2, "4.2 Training Configuration", min(6, pc)],
        [1, "5. Results and Discussion", min(7, pc)],
        [2, "5.1 Deterministic Forecast Skill", min(7, pc)],
        [2, "5.2 Probabilistic Forecast Calibration", min(7, pc)],
        [2, "5.3 Computational Efficiency", min(8, pc)],
        [2, "5.4 Regional Analysis", min(8, pc)],
        [2, "5.5 Extreme Weather Events", min(8, pc)],
        [2, "5.6 Sensitivity Analysis", min(9, pc)],
        [1, "6. Limitations and Future Work", min(9, pc)],
        [2, "6.1 Interpretability and Trust", min(9, pc)],
        [2, "6.2 Data Assimilation Integration", min(10, pc)],
        [1, "7. Conclusion", min(10, pc)],
        [1, "References", min(pc, pc)],
    ]
    doc.set_toc(toc)
    doc.saveIncr()
    doc.close()

    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
