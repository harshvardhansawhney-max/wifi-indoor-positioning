"""Signal preprocessing and feature extraction."""
import numpy as np
from typing import List, Dict, Tuple
from scipy import signal
from scipy.ndimage import uniform_filter1d
from logger import logger


class SignalPreprocessor:
    """Preprocess and normalize WiFi signals."""

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.rssi_min = -100
        self.rssi_max = -30

    def normalize_rssi(self, rssi_values: List[float]) -> np.ndarray:
        """Normalize RSSI values to 0-1 range."""
        rssi_array = np.array(rssi_values)
        normalized = (rssi_array - self.rssi_min) / (self.rssi_max - self.rssi_min)
        return np.clip(normalized, 0, 1)

    def smooth_signal(self, values: List[float], window_size: int = None) -> np.ndarray:
        """Apply moving average smoothing."""
        if window_size is None:
            window_size = self.window_size

        if len(values) < window_size:
            return np.array(values)

        kernel = np.ones(window_size) / window_size
        smoothed = np.convolve(values, kernel, mode="valid")
        return smoothed

    def remove_outliers(self, values: List[float], threshold: float = 3.0) -> np.ndarray:
        """Remove outliers using z-score."""
        values_array = np.array(values)
        mean = np.mean(values_array)
        std = np.std(values_array)

        if std == 0:
            return values_array

        z_scores = np.abs((values_array - mean) / std)
        return values_array[z_scores < threshold]

    def extract_features(self, signals: List[Dict]) -> Dict[str, np.ndarray]:
        """Extract features from signal measurements."""
        features = {}

        # Group by AP
        ap_signals = {}
        for sig in signals:
            ap_mac = sig.get("ap_mac")
            if ap_mac not in ap_signals:
                ap_signals[ap_mac] = []
            ap_signals[ap_mac].append(sig["rssi"])

        # Calculate statistics per AP
        for ap_mac, rssi_list in ap_signals.items():
            rssi_array = np.array(rssi_list)
            features[f"{ap_mac}_mean"] = np.mean(rssi_array)
            features[f"{ap_mac}_std"] = np.std(rssi_array)
            features[f"{ap_mac}_min"] = np.min(rssi_array)
            features[f"{ap_mac}_max"] = np.max(rssi_array)
            features[f"{ap_mac}_median"] = np.median(rssi_array)
            features[f"{ap_mac}_range"] = np.max(rssi_array) - np.min(rssi_array)

        return features

    def create_fingerprint(self, signals: List[Dict]) -> np.ndarray:
        """Create signal fingerprint for location."""
        ap_rssi_map = {}

        for sig in signals:
            ap_mac = sig.get("ap_mac")
            rssi = sig.get("rssi")
            if ap_mac not in ap_rssi_map:
                ap_rssi_map[ap_mac] = []
            ap_rssi_map[ap_mac].append(rssi)

        # Average RSSI per AP
        fingerprint_dict = {ap: np.mean(rssi_list) for ap, rssi_list in ap_rssi_map.items()}

        # Sort by AP MAC for consistency
        sorted_aps = sorted(fingerprint_dict.keys())
        fingerprint = np.array([fingerprint_dict[ap] for ap in sorted_aps])

        return fingerprint

    def apply_kalman_filter(self, measurements: List[float], process_variance: float = 1e-5,
                            measurement_variance: float = 0.1) -> np.ndarray:
        """Apply Kalman filter to smooth measurements."""
        n = len(measurements)
        filtered = np.zeros(n)
        P = np.zeros(n)
        K = np.zeros(n)

        filtered[0] = measurements[0]
        P[0] = 1.0

        for k in range(1, n):
            P[k] = P[k - 1] + process_variance
            K[k] = P[k] / (P[k] + measurement_variance)
            filtered[k] = filtered[k - 1] + K[k] * (measurements[k] - filtered[k - 1])
            P[k] = (1 - K[k]) * P[k]

        return filtered
