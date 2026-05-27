"""Database models."""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, Boolean, Text
from sqlalchemy.sql import func
from .base import Base


class Signal(Base):
    """WiFi signal measurement."""

    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, server_default=func.now(), index=True)
    ap_mac = Column(String(17), index=True)  # MAC address
    ap_ssid = Column(String(32))
    rssi = Column(Float)
    frequency = Column(Integer)  # MHz
    channel = Column(Integer)
    signal_quality = Column(Float)
    noise_level = Column(Float, nullable=True)
    data_rate = Column(Float, nullable=True)
    is_csi = Column(Boolean, default=False)
    csi_data = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)


class Location(Base):
    """Predicted location."""

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, server_default=func.now(), index=True)
    room = Column(String(50), index=True)
    x_coord = Column(Float)
    y_coord = Column(Float)
    z_coord = Column(Float, nullable=True)
    confidence = Column(Float)  # 0.0-1.0
    movement_state = Column(String(20))  # stationary, walking, moving
    speed = Column(Float, nullable=True)  # m/s
    direction = Column(Float, nullable=True)  # degrees
    raw_prediction = Column(JSON)
    model_version = Column(String(20))


class CalibrationPoint(Base):
    """Calibration reference point."""

    __tablename__ = "calibration_points"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    room = Column(String(50), index=True)
    x_coord = Column(Float)
    y_coord = Column(Float)
    z_coord = Column(Float, nullable=True)
    num_samples = Column(Integer)
    collected_samples = Column(JSON)  # List of signal arrays
    status = Column(String(20))  # pending, collected, processed
    notes = Column(Text, nullable=True)


class Model(Base):
    """Trained ML model metadata."""

    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    model_type = Column(String(50))  # room_classifier, coordinate_estimator, motion_tracker
    architecture = Column(String(50))  # random_forest, xgboost, lstm, etc.
    version = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    trained_at = Column(DateTime, nullable=True)
    accuracy = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    model_path = Column(String(255))
    training_config = Column(JSON)
    performance_metrics = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=False)


class HouseProfile(Base):
    """House/environment configuration."""

    __tablename__ = "house_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    floor_plan_path = Column(String(255), nullable=True)
    width_meters = Column(Float)  # Floor plan width
    height_meters = Column(Float)  # Floor plan height
    rooms = Column(JSON)  # List of room definitions
    routers = Column(JSON)  # List of router locations
    calibration_status = Column(String(20))  # pending, in_progress, completed
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)


class Settings(Base):
    """Application settings."""

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True)
    value = Column(Text)
    data_type = Column(String(20))  # string, integer, float, boolean, json
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
