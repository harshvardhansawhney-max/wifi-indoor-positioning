# Installation Guide

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Git
- WiFi-capable device (Linux preferred for WiFi scanning)
- ~2GB free disk space

## Linux Installation

### 1. Install System Dependencies

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install -y \
  python3.11 \
  python3-pip \
  python3-venv \
  node-js \
  npm \
  wireless-tools \
  build-essential
```

**Fedora**:
```bash
sudo dnf install -y \
  python3.11 \
  python3-pip \
  nodejs \
  npm \
  wireless-tools \
  gcc
```

### 2. Clone Repository

```bash
git clone https://github.com/harshvardhansawhney-max/wifi-indoor-positioning.git
cd wifi-indoor-positioning
```

### 3. Run Installation Script

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Or manual setup:

```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Frontend setup
cd frontend
npm install
cd ..
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your WiFi interface and settings
nano .env
```

### 5. Initialize Database

```bash
cd backend
source venv/bin/activate
python -c "from database.session import init_db; init_db()"
cd ..
```

## Windows Installation

### 1. Install Prerequisites

- Download Python 3.11+ from https://python.org
- Download Node.js 18+ from https://nodejs.org
- Install Git from https://git-scm.com

### 2. Clone Repository

```bash
git clone https://github.com/harshvardhansawhney-max/wifi-indoor-positioning.git
cd wifi-indoor-positioning
```

### 3. Setup Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### 4. Setup Frontend

```bash
cd frontend
npm install
cd ..
```

### 5. Configure Environment

```bash
copy .env.example .env
# Edit .env with Notepad or VS Code
```

## macOS Installation

### 1. Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Dependencies

```bash
brew install python@3.11 node
```

### 3. Clone and Setup

```bash
git clone https://github.com/harshvardhansawhney-max/wifi-indoor-positioning.git
cd wifi-indoor-positioning

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Frontend
cd frontend
npm install
cd ..
```

## Docker Installation

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### Setup

```bash
git clone https://github.com/harshvardhansawhney-max/wifi-indoor-positioning.git
cd wifi-indoor-positioning

# Copy and edit environment
cp .env.example .env

# Start services
docker-compose -f docker/docker-compose.yml up -d
```

### Verify Installation

```bash
# Check services
docker-compose ps

# View logs
docker-compose logs -f
```

## Running the Application

### Development Mode

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm start
```

Access dashboard at `http://localhost:3000`

### Production Mode

Using Docker Compose:
```bash
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up
```

## WiFi Scanning Setup

### Linux

Enable monitor mode (required for WiFi scanning):

```bash
# List interfaces
iwconfig

# Enable monitor mode
sudo airmon-ng start wlan0

# Or using iw
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
```

### Windows

Windows uses WinAPI for WiFi scanning (integrated in `signal_processing/scanner.py`)

### macOS

macOS uses airport utility:
```bash
/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s
```

## Troubleshooting

### Port Already in Use

```bash
# Change ports in .env
API_PORT=8001
API_CORS_ORIGINS=http://localhost:3001
```

### Database Lock

```bash
# Remove old database
rm backend/app.db

# Reinitialize
cd backend
python -c "from database.session import init_db; init_db()"
```

### WiFi Scanning Not Working

- Verify WiFi interface: `iwconfig` or `ip link show`
- Check permissions: May need `sudo` on Linux
- Verify monitor mode enabled on Linux

### Frontend Not Connecting to Backend

- Check API URL in `.env`
- Verify backend is running: `curl http://localhost:8000/api/health`
- Check CORS settings in backend

## Next Steps

1. **Calibrate System**: Open http://localhost:3000 → Calibration
2. **Upload Floor Plan**: Add your house layout
3. **Collect Training Data**: Walk around and collect samples
4. **Train Models**: Start model training
5. **Monitor Live Position**: View real-time tracking

## Getting Help

- Check documentation in `/docs`
- Review logs in `/logs`
- Open issue on GitHub
