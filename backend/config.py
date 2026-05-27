"""Application configuration."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Project
    PROJECT_NAME: str = "WiFi Indoor Positioning"
    PROJECT_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_CORS_ORIGINS: list = os.getenv(
        "API_CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
    ).split(",")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    ENCRYPT_DATABASE: bool = os.getenv("ENCRYPT_DATABASE", "True").lower() == "true"
    DATABASE_ENCRYPTION_KEY: str = os.getenv("DATABASE_ENCRYPTION_KEY", "")

    # WiFi Configuration
    WIFI_INTERFACE: str = os.getenv("WIFI_INTERFACE", "wlan0")
    SCAN_INTERVAL: int = int(os.getenv("SCAN_INTERVAL", "2"))
    RSSI_THRESHOLD: int = int(os.getenv("RSSI_THRESHOLD", "-100"))
    CSI_ENABLED: bool = os.getenv("CSI_ENABLED", "False").lower() == "true"

    # Machine Learning
    MODEL_PATH: str = os.getenv("MODEL_PATH", "./models/checkpoints")
    INFERENCE_DEVICE: str = os.getenv("INFERENCE_DEVICE", "cpu")
    MODEL_QUANTIZATION: bool = os.getenv("MODEL_QUANTIZATION", "False").lower() == "true"
    ONNX_EXPORT: bool = os.getenv("ONNX_EXPORT", "False").lower() == "true"

    # WebSocket
    WS_HOST: str = os.getenv("WS_HOST", "0.0.0.0")
    WS_PORT: int = int(os.getenv("WS_PORT", "8001"))
    WS_PING_INTERVAL: int = int(os.getenv("WS_PING_INTERVAL", "30"))

    # Privacy
    ENABLE_CLOUD_SYNC: bool = os.getenv("ENABLE_CLOUD_SYNC", "False").lower() == "true"
    LOCAL_STORAGE_ONLY: bool = os.getenv("LOCAL_STORAGE_ONLY", "True").lower() == "true"
    ANONYMIZE_LOGS: bool = os.getenv("ANONYMIZE_LOGS", "True").lower() == "true"
    DATA_RETENTION_DAYS: int = int(os.getenv("DATA_RETENTION_DAYS", "90"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/app.log")

    # Performance
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    QUEUE_SIZE: int = int(os.getenv("QUEUE_SIZE", "1000"))
    CACHE_SIZE: int = int(os.getenv("CACHE_SIZE", "100"))

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Create necessary directories
Path(settings.MODEL_PATH).mkdir(parents=True, exist_ok=True)
Path("./logs").mkdir(parents=True, exist_ok=True)
Path("./datasets/raw").mkdir(parents=True, exist_ok=True)
Path("./datasets/processed").mkdir(parents=True, exist_ok=True)
Path("./datasets/labeled").mkdir(parents=True, exist_ok=True)
