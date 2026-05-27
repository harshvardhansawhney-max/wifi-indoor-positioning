# System Architecture

## Overview

The WiFi Indoor Positioning system is a multi-layered architecture combining signal processing, machine learning, and real-time visualization.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  React Dashboard | Floor Plan Mapping | Real-Time Visualization │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ WebSocket/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ API Endpoints│  │ ML Inference │  │ WebSocket    │          │
│  │ & Services   │  │ & Training   │  │ Server       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Localization Engine                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Room         │  │ Coordinate   │  │ Motion       │          │
│  │ Classifier   │  │ Estimator    │  │ Tracker      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Signal Processing Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ WiFi Scanner │  │ Preprocessor │  │ Feature      │          │
│  │              │  │ (Kalman etc) │  │ Extraction   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Hardware Interface                            │
│  WiFi Adapters | CSI Capture | Network Interfaces              │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Signal Collection Layer

**Responsibility**: Scan WiFi networks and collect signal measurements

**Components**:
- `WifiScanner`: Platform-specific WiFi network scanning
- Supports Linux (nmcli), Windows (netsh), macOS (airport)
- Captures RSSI, frequency, channel, signal quality
- Optional CSI capture for advanced analysis

**Output**: Raw signal measurements

### 2. Signal Processing Layer

**Responsibility**: Clean, normalize, and extract features from signals

**Components**:
- `SignalPreprocessor`: 
  - RSSI normalization (map to 0-1 range)
  - Moving average smoothing
  - Outlier detection (z-score method)
  - Kalman filtering for temporal smoothing
  - Feature extraction (mean, std, min, max, range)
  - Fingerprint generation for locations

**Algorithms**:
- Kalman filter for smooth tracking
- Z-score outlier detection
- Sliding window feature computation

**Output**: Clean signal features and fingerprints

### 3. Localization Engine

#### A. Room Classification

**Model**: Random Forest Classifier
- Input: Signal fingerprint (RSSI vector)
- Output: Room prediction + confidence
- Features: Per-AP RSSI statistics

**Performance**: >85% accuracy target

#### B. Coordinate Estimation

**Methods**:
1. **Trilateration**: Uses path loss model to convert RSSI to distance, then trilaterate
2. **Weighted Centroid**: Weights router positions by signal strength

**Path Loss Model**: RSSI = a - n * 10 * log10(distance)

**Output**: (X, Y) coordinates + confidence

#### C. Motion Tracking

**Capabilities**:
- Position history tracking (sliding window)
- Velocity estimation (distance/time)
- Direction calculation (arctan of position delta)
- Movement state detection (moving/stationary)
- Dwell time calculation
- Trajectory analysis

### 4. Machine Learning Pipeline

**Training Flow**:
1. Collect calibration data at known points
2. Extract features from signals
3. Train models:
   - Room classifier (Random Forest, XGBoost)
   - Coordinate regressor (Neural network optional)
   - Motion model (LSTM optional)
4. Validate on test set
5. Save models and metrics
6. Deploy for inference

**Supported Models**:
- Random Forest (primary)
- XGBoost
- LightGBM
- LSTM (optional)
- Transformer (experimental)

**Inference**: <100ms per prediction

### 5. Real-Time Backend

**Technology**: FastAPI + Uvicorn + WebSockets

**Responsibilities**:
- REST API endpoints for signals, locations, calibration
- WebSocket streaming for live updates
- Model inference requests
- State management
- Database operations
- Logging and monitoring

**Performance**:
- <500ms position update latency
- >100 Hz message throughput
- <15% CPU usage
- <500MB memory

### 6. Frontend Dashboard

**Technology**: React + Tailwind CSS + Framer Motion

**Pages**:
- **Dashboard**: System overview, current status, recent signals
- **Live Tracking**: Real-time position on floor plan, movement trail
- **Signal Analytics**: RSSI graphs, signal quality, channel utilization
- **Training**: Model training controls and evaluation
- **Calibration**: Guided setup wizard
- **Settings**: Privacy, WiFi config, advanced options

**Features**:
- Interactive floor plan (Konva.js)
- Live charts (Recharts)
- Real-time updates (WebSocket)
- Responsive design
- Dark mode + Glassmorphism

## Database Schema

### Tables

1. **signals**: Raw WiFi measurements
   - timestamp, ap_mac, rssi, frequency, channel, signal_quality

2. **locations**: Predicted positions
   - timestamp, room, x_coord, y_coord, confidence, movement_state

3. **calibration_points**: Training locations
   - room, coordinates, collected_samples, status

4. **models**: ML model metadata
   - name, type, architecture, accuracy, path, is_active

5. **house_profiles**: Environment configuration
   - name, floor_plan, dimensions, rooms, routers, calibration_status

6. **settings**: Application configuration
   - key, value, data_type

## Data Flow

1. **Signal Collection**
   ```
   WiFi Hardware → WifiScanner → Signal objects
   ```

2. **Signal Processing**
   ```
   Signal objects → Preprocessor → Clean features
   ```

3. **Localization**
   ```
   Features → RoomClassifier → Room prediction
   Features → CoordinateEstimator → (X, Y) position
   (X, Y, History) → MotionTracker → Velocity, direction
   ```

4. **Backend Inference**
   ```
   API Request → Model Inference → Location prediction
   Location → Database storage + WebSocket broadcast
   ```

5. **Frontend Visualization**
   ```
   WebSocket stream → Store update → Component re-render
   → Display on floor plan + charts
   ```

## Calibration Workflow

```
1. Environment Scan
   ↓
2. Floor Plan Setup (upload, define rooms, place routers)
   ↓
3. Training Point Collection (user stands at points, system records signals)
   ↓
4. Dataset Generation (aggregate samples, create labeled dataset)
   ↓
5. Model Training (train room classifier, coordinate estimator)
   ↓
6. Validation (test accuracy, show error heatmaps)
   ↓
7. Save Profile (save models, floor plan, configuration)
```

## Privacy & Security

- **Local-First**: Data stored locally by default
- **Encrypted Database**: SQLite with encryption
- **No Cloud Tracking**: Explicit opt-in required
- **User Consent**: Clear permission system
- **Data Control**: Export and delete capabilities
- **Secure WebSockets**: TLS/SSL ready

## Deployment Options

1. **Development**: Local Python + Node.js servers
2. **Docker**: Containerized services
3. **Edge Devices**: Raspberry Pi, Jetson optimization
4. **Cloud**: Optional cloud sync (disabled by default)

## Performance Targets

| Metric | Target | Current |
|--------|--------|----------|
| Position Update Latency | <500ms | TBD |
| Room Classification Accuracy | >85% | TBD |
| CPU Usage | <15% | TBD |
| Memory Usage | <500MB | TBD |
| Inference Latency | <100ms | TBD |
| WebSocket Throughput | >100 Hz | TBD |

## Future Extensions

- Multi-person detection
- Gesture recognition
- 3D localization
- BLE/UWB integration
- Federated learning
- Smart home integration (MQTT, Home Assistant)
