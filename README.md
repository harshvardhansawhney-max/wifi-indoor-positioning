# Wi-Fi Indoor Positioning & Human Movement Detection Platform

**A privacy-focused, real-time indoor localization system using Wi-Fi signal sensing, machine learning, and RF signal analysis.**

## 🎯 Project Overview

This platform estimates room-level occupancy, approximate indoor coordinates, and movement patterns using RSSI and CSI data from Wi-Fi networks. It combines signal processing, machine learning, and interactive visualization for real-time indoor localization.

## ✨ Key Features

- **Real-Time Indoor Localization** - Room classification + coordinate estimation
- **Movement Tracking** - Direction, speed, and trajectory analysis
- **Signal Analytics** - RSSI visualization, signal fingerprinting, CSI analysis
- **Machine Learning Pipeline** - Multi-model support (RF, XGBoost, LSTM, Transformers)
- **Interactive House Mapping** - Floor plan upload, room definition, live positioning
- **Calibration Workflow** - Guided onboarding wizard for environment setup
- **Privacy-First Design** - Local storage, encrypted DB, no cloud tracking
- **Real-Time Dashboard** - Futuristic UI with Glassmorphism, dark mode, animations
- **Cross-Platform Support** - Linux, macOS, Windows, Raspberry Pi, Jetson
- **WebSocket Streaming** - Live updates, sub-500ms latency

## 🏗️ Architecture

```
Signal Collection → Signal Processing → Localization Engine → ML Pipeline → Real-Time Backend → Frontend Dashboard
     (WiFi RSSI)   (Feature Extraction)  (Room + Coords)    (Inference)    (FastAPI + WS)   (React/Electron)
```

### Core Components

1. **Signal Collection** - Python/Scapy for WiFi scanning
2. **Signal Processing** - NumPy/SciPy for feature extraction
3. **Localization Engine** - Room classification, trilateration, motion tracking
4. **ML Pipeline** - PyTorch/TensorFlow with multiple architectures
5. **Backend** - FastAPI + WebSockets + SQLite
6. **Frontend** - React + Tailwind + Framer Motion + Electron

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)
- WiFi capable device (Linux preferred for WiFi scanning)

### Development Setup

```bash
# Clone repository
git clone https://github.com/harshvardhansawhney-max/wifi-indoor-positioning.git
cd wifi-indoor-positioning

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install

# Run development servers
# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend
cd frontend && npm start
```

### Docker Setup

```bash
docker-compose -f docker/docker-compose.yml up -d
```

## 📋 Project Structure

```
wifi-indoor-positioning/
├── backend/                    # FastAPI backend service
│   ├── api/                    # REST endpoints
│   ├── services/               # Business logic
│   ├── signal_processing/      # Feature extraction
│   ├── localization/           # Room & coordinate prediction
│   ├── ml/                     # Model training & inference
│   ├── database/               # SQLite ORM models
│   ├── ws/                     # WebSocket handlers
│   ├── utils/                  # Utilities
│   ├── main.py                 # Entry point
│   ├── config.py               # Configuration
│   ├── requirements.txt         # Dependencies
│   └── .env.example            # Environment variables
│
├── frontend/                   # React + Electron frontend
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Page layouts
│   │   ├── hooks/              # Custom React hooks
│   │   ├── store/              # State management (Redux)
│   │   ├── services/           # API & WebSocket clients
│   │   ├── charts/             # Chart components
│   │   ├── map/                # Floor plan & mapping
│   │   ├── styles/             # Tailwind + animations
│   │   └── App.tsx
│   ├── public/                 # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── webpack.config.js
│
├── models/                     # ML models
│   ├── checkpoints/            # Saved model weights
│   ├── exports/                # ONNX/TorchScript exports
│   └── training/               # Training scripts
│
├── datasets/                   # Training data
│   ├── raw/                    # Raw WiFi scans
│   ├── processed/              # Processed features
│   └── labeled/                # Labeled calibration data
│
├── calibration/                # Calibration workflows
│   ├── wizard.py               # Wizard logic
│   └── data_collector.py       # Sample collection
│
├── tests/                      # Test suites
│   ├── backend/                # Backend tests
│   ├── frontend/               # Frontend tests
│   ├── integration/            # Integration tests
│   └── performance/            # Performance benchmarks
│
├── scripts/                    # Utility scripts
│   ├── setup.sh                # Installation script
│   ├── train_model.py          # Model training
│   └── export_model.py         # Model export
│
├── docker/                     # Docker configuration
│   ├── docker-compose.yml      # Service orchestration
│   ├── Dockerfile.backend      # Backend image
│   └── Dockerfile.frontend     # Frontend image
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md         # System design
│   ├── API.md                  # API reference
│   ├── CALIBRATION.md          # Calibration guide
│   ├── INSTALLATION.md         # Setup instructions
│   ├── PRIVACY.md              # Privacy policy
│   └── RESEARCH.md             # Research references
│
├── .gitignore
├── .env.example
├── LICENSE
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in backend:

```bash
# Backend
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./app.db

# WiFi
WIFI_INTERFACE=wlan0
SCAN_INTERVAL=2
RSSI_THRESHOLD=-100

# ML
MODEL_PATH=./models/checkpoints
INFERENCE_DEVICE=cpu  # or cuda

# API
API_HOST=0.0.0.0
API_PORT=8000
API_CORS_ORIGINS=http://localhost:3000

# WebSocket
WS_HOST=0.0.0.0
WS_PORT=8001

# Privacy
ENABLE_CLOUD_SYNC=False
LOCAL_STORAGE_ONLY=True
ENCRYPT_DATABASE=True
```

## 📊 Performance Targets

- ✅ Position update latency: **< 500 ms**
- ✅ Room classification accuracy: **> 85%**
- ✅ CPU usage: **< 15%**
- ✅ Memory usage: **< 500 MB**
- ✅ Inference latency: **< 100 ms**
- ✅ WebSocket message throughput: **> 100 Hz**

## 🔐 Privacy & Security

- ✅ **Local-first architecture** - Data stored locally by default
- ✅ **Encrypted database** - SQLite with encryption
- ✅ **No cloud tracking** - Explicit opt-in only
- ✅ **User consent** - Clear permission system
- ✅ **Data export/delete** - Full user control
- ✅ **Secure WebSockets** - TLS/SSL ready
- ✅ **Role-based access** - Permission system

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - Detailed system design
- [API Reference](docs/API.md) - REST & WebSocket endpoints
- [Calibration Guide](docs/CALIBRATION.md) - Setup workflow
- [Installation Guide](docs/INSTALLATION.md) - Platform-specific setup
- [Privacy Policy](docs/PRIVACY.md) - Data handling
- [Research References](docs/RESEARCH.md) - Academic papers & resources

## 🧪 Testing

```bash
# Backend tests
cd backend && pytest tests/ -v

# Frontend tests
cd frontend && npm test

# Integration tests
pytest tests/integration/ -v

# Performance benchmarks
python tests/performance/benchmark.py
```

## 🚀 Deployment

### Docker Compose

```bash
cd docker
docker-compose up -d
```

### Manual Deployment

See [Installation Guide](docs/INSTALLATION.md)

## 🔬 Research & References

This project is based on research in:
- Wi-Fi sensing and RF localization
- Device-free human activity recognition
- CSI-based occupancy detection
- Indoor positioning systems
- Passive RF tomography

See [Research References](docs/RESEARCH.md) for papers and tools.

## 🎓 Advanced Features (Coming Soon)

- [ ] Multi-person detection
- [ ] Gesture recognition (waving, sitting, standing)
- [ ] Edge AI (Raspberry Pi, Jetson)
- [ ] Smart home integration (MQTT, Home Assistant)
- [ ] 3D localization
- [ ] BLE/UWB support
- [ ] Federated learning

## 🤝 Contributing

Contributions welcome! Please:
1. Create a feature branch
2. Follow code style guides
3. Add tests
4. Submit pull request

## 📄 License

MIT License - See LICENSE file

## ⚠️ Disclaimer

This system is designed for indoor positioning and movement detection with explicit user consent. Ensure compliance with local regulations regarding RF monitoring and location tracking. Always provide clear privacy notices to users.

## 📧 Contact

For questions or support, open an issue on GitHub.

---

**Status:** 🚧 Under Development
**Latest Version:** 0.1.0
**Last Updated:** May 2026
