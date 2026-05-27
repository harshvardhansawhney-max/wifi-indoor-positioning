"""Room classification using RSSI fingerprinting."""
import numpy as np
from typing import List, Dict, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from logger import logger


class RoomClassifier:
    """Classify user location into rooms using ML."""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.room_labels = []
        self.ap_list = []

    def train(self, X: np.ndarray, y: np.ndarray, room_labels: List[str], ap_list: List[str]):
        """Train room classifier."""
        try:
            self.room_labels = room_labels
            self.ap_list = ap_list

            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            self.is_trained = True
            logger.info(f"Room classifier trained with {len(X)} samples")
        except Exception as e:
            logger.error(f"Failed to train room classifier: {e}")
            raise

    def predict(self, signal_features: np.ndarray) -> Tuple[str, float]:
        """Predict room from signal features."""
        if not self.is_trained:
            logger.warning("Model not trained")
            return "unknown", 0.0

        try:
            # Reshape if needed
            if signal_features.ndim == 1:
                signal_features = signal_features.reshape(1, -1)

            X_scaled = self.scaler.transform(signal_features)
            prediction = self.model.predict(X_scaled)[0]
            probabilities = self.model.predict_proba(X_scaled)[0]
            confidence = float(np.max(probabilities))

            room = self.room_labels[prediction] if prediction < len(self.room_labels) else "unknown"
            return room, confidence
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return "unknown", 0.0

    def predict_probabilities(self, signal_features: np.ndarray) -> Dict[str, float]:
        """Get probability distribution across rooms."""
        if not self.is_trained:
            return {}

        try:
            if signal_features.ndim == 1:
                signal_features = signal_features.reshape(1, -1)

            X_scaled = self.scaler.transform(signal_features)
            probabilities = self.model.predict_proba(X_scaled)[0]

            return {room: float(prob) for room, prob in zip(self.room_labels, probabilities)}
        except Exception as e:
            logger.error(f"Failed to get probabilities: {e}")
            return {}

    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores."""
        if not self.is_trained:
            return {}

        return {ap: float(importance) for ap, importance in zip(self.ap_list, self.model.feature_importances_)}
