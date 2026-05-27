# Research References & Resources

## Overview

This document provides research papers, tools, and resources for WiFi-based indoor positioning and human activity recognition.

## Key Research Papers

### WiFi Sensing & Localization

1. **DeepFi: Deep Learning for Indoor Fingerprinting using CSI**
   - Authors: Guo et al.
   - Year: 2021
   - Focus: CSI-based deep learning for indoor positioning
   - Link: https://arxiv.org/abs/2106.07297

2. **WiTrack: Through-Wall Motion Tracking Using Wi-Fi Signals**
   - Authors: Adib & Katabi (MIT)
   - Year: 2013
   - Focus: Device-free WiFi-based motion tracking
   - Innovations: Through-wall tracking, no special hardware

3. **Chronos: Sub-Nanosecond Time of Flight on Commercial WiFi Cards**
   - Authors: Witrisal et al.
   - Year: 2015
   - Focus: Time-of-flight based localization
   - Key: High-precision timing without special hardware

4. **SpotFi: Decimeter Level Localization Using WiFi**
   - Authors: Kotaru et al.
   - Year: 2015
   - Focus: Sub-meter accuracy with standard WiFi
   - Method: CSI phase information exploitation

5. **WiSee: WiFi-Based People Detection**
   - Authors: Kellogg et al.
   - Year: 2014
   - Focus: Human activity recognition from WiFi signals
   - Applications: Gesture detection, fall detection

6. **RF-Pose: Pose Estimation from RF Signals**
   - Authors: Zhao et al. (MIT)
   - Year: 2018
   - Focus: Human pose estimation using WiFi
   - Innovation: 3D body tracking without vision

7. **WiFi-Based Occupancy Detection**
   - Multiple studies on room-level occupancy from passive WiFi
   - Focus: Energy efficiency, smart buildings
   - Accuracy: 85-95% typical

### Signal Processing for RF Localization

8. **RSSI-Based Indoor Positioning: A Survey**
   - Comprehensive review of RSSI-based methods
   - Covers: Fingerprinting, trilateration, hybrid approaches

9. **Kalman Filtering for RF Tracking**
   - Classical signal processing approach
   - Used for smoothing noisy measurements

10. **Deep Learning for Wireless Localization**
    - Surveys deep neural network approaches
    - Models: CNN, LSTM, Transformer

## Open Source Projects & Tools

### WiFi CSI Capture

1. **CSIKit** - https://github.com/seemoo-lab/csikit
   - Python toolkit for WiFi CSI
   - Supports Intel 5300, Qualcomm, Nexmon
   - Multi-platform support

2. **Nexmon CSI** - https://github.com/seemoo-lab/nexmon_csi
   - CSI extraction on various WiFi chipsets
   - Focus: ARM-based devices

3. **Intel 5300 CSI Tool** - https://github.com/dhalperi/linux-80211n-csitool
   - Original CSI extraction tool
   - Linux kernel module

### ML Frameworks

1. **PyTorch** - https://pytorch.org
   - Deep learning framework
   - Used for LSTM, CNN, Transformers

2. **TensorFlow** - https://tensorflow.org
   - Alternative deep learning framework
   - Mobile support via TFLite

3. **scikit-learn** - https://scikit-learn.org
   - Traditional ML (Random Forest, SVM, etc.)
   - Feature scaling, model selection

4. **XGBoost** - https://xgboost.readthedocs.io
   - Gradient boosting
   - Often used for RF localization

### Signal Processing

1. **NumPy** - https://numpy.org
   - Numerical computing
   - Array operations, statistics

2. **SciPy** - https://scipy.org
   - Advanced signal processing
   - Filtering, interpolation, transforms

3. **pandas** - https://pandas.pydata.org
   - Data manipulation
   - Time series analysis

### Visualization

1. **Recharts** - https://recharts.org
   - React charting library
   - Real-time data visualization

2. **Konva.js** - https://konvajs.org
   - Canvas drawing library
   - Interactive floor plan maps

3. **Plotly** - https://plotly.com
   - Interactive visualizations
   - 3D plotting support

## Datasets

### Public Datasets

1. **UJIIndoorLoc** - WiFi fingerprinting dataset
   - Multiple buildings, thousands of samples
   - Link: http://archive.ics.uci.edu/ml/datasets/UJIIndoorLoc

2. **TUT Indoor Positioning Database**
   - Tampere University of Technology
   - Multi-building WiFi measurements

3. **Microsoft Indoor Dataset**
   - Large-scale indoor positioning data
   - Multiple buildings and floors

### Creating Custom Datasets

- Use provided `scripts/collect_calibration_data.py`
- Collect data at known locations
- Label with room/coordinates
- Export as JSON for training

## Hardware Recommendations

### WiFi Adapters

1. **Intel 5300** (recommended for CSI)
   - CSI extraction capability
   - Legacy but well-documented

2. **Qualcomm Atheros (AR9271, etc.)**
   - Monitor mode support
   - CSI extraction available

3. **MediaTek MT7612U**
   - Modern USB WiFi adapter
   - Monitor mode support

### Edge Devices

1. **Raspberry Pi 4**
   - Model: 4GB+ recommended
   - WiFi interface available
   - Runs backend efficiently

2. **NVIDIA Jetson Nano**
   - GPU acceleration
   - More powerful inference
   - ~$99 cost

3. **Intel NUC**
   - Compact desktop
   - Dual core+ CPU
   - Good for production

## Algorithms Overview

### Trilateration

```
Given: WiFi APs at positions (x1,y1), (x2,y2), (x3,y3)
Measured: Distance d1, d2, d3 from RSSI

Find: Position (x,y) that minimizes:
  E = (x-x1)² + (y-y1)² - d1²
    + (x-x2)² + (y-y2)² - d2²
    + (x-x3)² + (y-y3)² - d3²
```

### RSSI Path Loss Model

```
RSSI(d) = RSSI(d0) - 10n*log10(d/d0)

Where:
  d = distance (meters)
  d0 = reference distance (typically 1m)
  n = path loss exponent (typically 2-4)
  RSSI(d0) = signal strength at reference distance
```

### Fingerprinting

```
1. Calibration Phase:
   - Collect RSSI at known locations
   - Create fingerprint database

2. Positioning Phase:
   - Measure RSSI from user location
   - Compare against database
   - Find closest match (KNN) or probability (ML)
```

### Machine Learning Pipeline

```
Data Collection
    ↓
Feature Extraction
    ↓
Training/Validation Split
    ↓
Model Training
    ↓
Hyperparameter Tuning
    ↓
Evaluation
    ↓
Deployment
```

## Implementation Tips

### Signal Processing

1. **Outlier Detection**
   - Use z-score method (threshold: 2-3)
   - Remove extreme values
   - Robust statistics

2. **Smoothing**
   - Moving average (window: 5-10 samples)
   - Kalman filter (better for dynamics)
   - EWMA for online smoothing

3. **Feature Scaling**
   - StandardScaler (zero mean, unit variance)
   - MinMaxScaler (0-1 range)
   - RobustScaler (resistant to outliers)

### Model Selection

| Task | Model | Pros | Cons |
|------|-------|------|------|
| Room Classification | Random Forest | Fast, interpretable | May overfit |
| Room Classification | XGBoost | High accuracy | Complex |
| Coordinate Regression | Neural Network | Flexible | Needs tuning |
| Motion Prediction | LSTM | Temporal modeling | Slower |
| Real-time | Random Forest | Low latency | Lower accuracy |

### Accuracy Improvement

1. **Collect More Data**
   - More calibration points
   - Different times of day
   - Various user heights

2. **Feature Engineering**
   - Use more APs
   - Calculate per-AP statistics
   - Use CSI if available

3. **Model Ensembling**
   - Combine multiple models
   - Weighted averaging
   - Stacking

4. **Environmental Adaptation**
   - Periodic recalibration
   - Incremental learning
   - Seasonal adjustments

## Performance Benchmarking

### Metrics

- **Accuracy**: (TP + TN) / Total
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1 Score**: 2 * (Precision * Recall) / (Precision + Recall)
- **Position Error**: Root Mean Square Error (RMSE)

### Typical Results

| Approach | Room Accuracy | Position RMSE |
|----------|---------------|---------------|
| Simple Fingerprinting | 75-80% | 5-10m |
| RSSI + ML | 85-90% | 2-5m |
| CSI + Deep Learning | 92-98% | 0.5-2m |
| Fusion (WiFi + IMU) | 95%+ | <1m |

## Research Directions

### Emerging Areas

1. **WiFi Sensing 802.11bf**
   - New standard for sensing
   - Higher sampling rates
   - Better accuracy

2. **Federated Learning**
   - Distributed training
   - Privacy-preserving
   - Collaborative improvements

3. **Semantic Segmentation**
   - Room type recognition
   - Furniture detection
   - Space understanding

4. **Multi-Sensor Fusion**
   - WiFi + BLE + UWB
   - WiFi + IMU + Bluetooth
   - Hybrid approaches

## Conferences & Venues

- **SIGCOMM**: Systems and networking
- **NSDI**: Networked systems design/implementation
- **MobiCom**: Mobile computing and networking
- **IPSN**: Information processing in sensor networks
- **PerCom**: Pervasive computing and communications

## Learning Resources

### Online Courses

- MIT 6.888: Wireless Network Analysis (OpenCourseWare)
- Stanford EE359: Wireless Communications (YouTube)
- Fast.ai: Practical Deep Learning

### Books

- "Wireless Communications" by Andrea Goldsmith
- "Deep Learning" by Goodfellow, Bengio, Courville
- "Pattern Recognition and Machine Learning" by Bishop

### Blogs & Articles

- MIT News: Regular RF sensing research updates
- Papers With Code: Implementation details
- ArXiv: Pre-prints of latest research

## Contributing to Research

Ways to contribute:

1. **Dataset Collection**
   - Collect in diverse environments
   - Share anonymously
   - Help validate models

2. **Algorithm Implementation**
   - Implement new methods
   - Compare approaches
   - Publish results

3. **Hardware Experiments**
   - Test on new devices
   - Report performance
   - Identify limitations

4. **Model Development**
   - Train better models
   - Publish weights
   - Document improvements

---

**Last Updated**: May 2026
**Maintained By**: Community Contributors
