#!/usr/bin/env python3
"""Train ML models for indoor positioning."""
import sys
from pathlib import Path
import numpy as np
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from ml.training import ModelTrainer
from logger import logger
from config import settings


def load_calibration_data(data_dir: str = "./datasets/labeled") -> tuple:
    """Load calibration data from directory."""
    logger.info(f"Loading calibration data from {data_dir}")
    
    data_dir = Path(data_dir)
    X = []
    y = []
    rooms = set()
    
    # Load all JSON files
    for file in data_dir.glob("*.json"):
        try:
            with open(file) as f:
                data = json.load(f)
                room = data["room"]
                rooms.add(room)
                
                # Extract features from samples
                for sample in data.get("samples", []):
                    # Simple feature: RSSI from each AP
                    features = [sample.get(f"rssi", -100) for _ in range(10)]  # Placeholder
                    X.append(features)
                    y.append(room)
        except Exception as e:
            logger.error(f"Failed to load {file}: {e}")
    
    if not X:
        logger.error("No calibration data found")
        return None, None, None
    
    room_list = sorted(list(rooms))
    y_encoded = np.array([room_list.index(r) for r in y])
    X = np.array(X)
    
    logger.info(f"Loaded {len(X)} samples from {len(rooms)} rooms")
    return X, y_encoded, room_list


def train_models(X: np.ndarray, y: np.ndarray, rooms: list):
    """Train ML models."""
    logger.info("Starting model training...")
    
    trainer = ModelTrainer()
    
    # Train room classifier
    metrics = trainer.train_room_classifier(X, y)
    
    logger.info(f"Training completed with metrics: {metrics}")
    
    # Save model
    model_path = trainer.save_model("room_classifier_v1")
    logger.info(f"Model saved to {model_path}")
    
    return trainer, metrics


def main():
    """Main training script."""
    logger.info("WiFi Indoor Positioning - Model Training")
    logger.info("="*50)
    
    # Load data
    X, y, rooms = load_calibration_data()
    if X is None:
        logger.error("No data to train on")
        return
    
    # Train models
    trainer, metrics = train_models(X, y, rooms)
    
    # Log results
    logger.info("\nTraining Results:")
    logger.info(f"  Accuracy: {metrics['accuracy']:.4f}")
    logger.info(f"  Precision: {metrics['precision']:.4f}")
    logger.info(f"  Recall: {metrics['recall']:.4f}")
    logger.info(f"  F1 Score: {metrics['f1_score']:.4f}")
    
    logger.info("\n✅ Training complete!")


if __name__ == "__main__":
    main()
