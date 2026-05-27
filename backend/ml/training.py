"""ML model training pipeline."""
import numpy as np
from typing import Tuple, Dict
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import joblib
from logger import logger
from config import settings


class ModelTrainer:
    """Train and evaluate ML models."""

    def __init__(self):
        self.model = None
        self.scaler = None
        self.metrics = {}

    def train_room_classifier(self, X: np.ndarray, y: np.ndarray,
                              test_size: float = 0.2, random_state: int = 42) -> Dict:
        """Train room classification model."""
        try:
            logger.info(f"Training room classifier with {len(X)} samples")

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )

            # Normalize features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=random_state,
                n_jobs=-1
            )
            self.model.fit(X_train_scaled, y_train)

            # Evaluate
            y_pred = self.model.predict(X_test_scaled)
            self.metrics = {
                "accuracy": float(accuracy_score(y_test, y_pred)),
                "precision": float(precision_score(y_test, y_pred, average="weighted", zero_division=0)),
                "recall": float(recall_score(y_test, y_pred, average="weighted", zero_division=0)),
                "f1_score": float(f1_score(y_test, y_pred, average="weighted", zero_division=0)),
            }

            logger.info(f"Training completed - Accuracy: {self.metrics['accuracy']:.4f}")
            return self.metrics
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise

    def save_model(self, model_name: str):
        """Save trained model."""
        try:
            model_dir = Path(settings.MODEL_PATH)
            model_dir.mkdir(parents=True, exist_ok=True)

            model_path = model_dir / f"{model_name}.pkl"
            scaler_path = model_dir / f"{model_name}_scaler.pkl"

            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)

            logger.info(f"Model saved to {model_path}")
            return str(model_path)
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            raise

    def load_model(self, model_name: str):
        """Load trained model."""
        try:
            model_dir = Path(settings.MODEL_PATH)
            model_path = model_dir / f"{model_name}.pkl"
            scaler_path = model_dir / f"{model_name}_scaler.pkl"

            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)

            logger.info(f"Model loaded from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
