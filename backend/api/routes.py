"""API route definitions."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database.session import get_db
from database import models
from logger import logger
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api")


# Pydantic schemas
class SignalCreate(BaseModel):
    ap_mac: str
    ap_ssid: str
    rssi: float
    frequency: int
    channel: int
    signal_quality: float


class LocationUpdate(BaseModel):
    room: str
    x_coord: float
    y_coord: float
    confidence: float
    movement_state: str


class CalibrationPointCreate(BaseModel):
    room: str
    x_coord: float
    y_coord: float
    num_samples: int = 10


# Signal endpoints
@router.post("/signals/upload")
async def upload_signal(signal: SignalCreate, db: Session = Depends(get_db)):
    """Upload WiFi signal measurement."""
    try:
        db_signal = models.Signal(
            ap_mac=signal.ap_mac,
            ap_ssid=signal.ap_ssid,
            rssi=signal.rssi,
            frequency=signal.frequency,
            channel=signal.channel,
            signal_quality=signal.signal_quality,
        )
        db.add(db_signal)
        db.commit()
        db.refresh(db_signal)
        return {"id": db_signal.id, "status": "recorded"}
    except Exception as e:
        logger.error(f"Signal upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/signals/live")
async def get_live_signals(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent signal measurements."""
    try:
        signals = db.query(models.Signal).order_by(models.Signal.timestamp.desc()).limit(limit).all()
        return [{"ap_mac": s.ap_mac, "rssi": s.rssi, "timestamp": s.timestamp} for s in signals]
    except Exception as e:
        logger.error(f"Failed to retrieve signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/signals/history")
async def get_signal_history(ap_mac: str, limit: int = 100, db: Session = Depends(get_db)):
    """Get signal history for specific AP."""
    try:
        signals = (
            db.query(models.Signal)
            .filter(models.Signal.ap_mac == ap_mac)
            .order_by(models.Signal.timestamp.desc())
            .limit(limit)
            .all()
        )
        return signals
    except Exception as e:
        logger.error(f"Failed to retrieve signal history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Location endpoints
@router.post("/location/update")
async def update_location(location: LocationUpdate, db: Session = Depends(get_db)):
    """Update current location."""
    try:
        db_location = models.Location(
            room=location.room,
            x_coord=location.x_coord,
            y_coord=location.y_coord,
            confidence=location.confidence,
            movement_state=location.movement_state,
            model_version="v1.0",
        )
        db.add(db_location)
        db.commit()
        return {"status": "updated"}
    except Exception as e:
        logger.error(f"Location update failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/location/current")
async def get_current_location(db: Session = Depends(get_db)):
    """Get current location prediction."""
    try:
        location = db.query(models.Location).order_by(models.Location.timestamp.desc()).first()
        if not location:
            return {"room": "unknown", "confidence": 0.0}
        return {
            "room": location.room,
            "x": location.x_coord,
            "y": location.y_coord,
            "confidence": location.confidence,
            "movement_state": location.movement_state,
        }
    except Exception as e:
        logger.error(f"Failed to get current location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/location/history")
async def get_location_history(limit: int = 50, db: Session = Depends(get_db)):
    """Get location history."""
    try:
        locations = db.query(models.Location).order_by(models.Location.timestamp.desc()).limit(limit).all()
        return locations
    except Exception as e:
        logger.error(f"Failed to retrieve location history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Calibration endpoints
@router.post("/calibration/start")
async def start_calibration(house_name: str, db: Session = Depends(get_db)):
    """Start calibration process."""
    try:
        house = models.HouseProfile(
            name=house_name,
            calibration_status="in_progress",
        )
        db.add(house)
        db.commit()
        return {"calibration_id": house.id, "status": "started"}
    except Exception as e:
        logger.error(f"Calibration start failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
