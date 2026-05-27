"""Unit tests for signal processing."""
import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from signal_processing.preprocessor import SignalPreprocessor


class TestSignalPreprocessor:
    """Test signal preprocessing."""

    @pytest.fixture
    def preprocessor(self):
        return SignalPreprocessor()

    def test_normalize_rssi(self, preprocessor):
        """Test RSSI normalization."""
        rssi_values = [-100, -50, -30]
        normalized = preprocessor.normalize_rssi(rssi_values)

        assert normalized.min() >= 0
        assert normalized.max() <= 1
        assert len(normalized) == 3

    def test_smooth_signal(self, preprocessor):
        """Test signal smoothing."""
        values = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        smoothed = preprocessor.smooth_signal(values, window_size=3)

        assert len(smoothed) < len(values)
        # Smoothed signal should have less variance
        assert np.std(smoothed) <= np.std(values)

    def test_remove_outliers(self, preprocessor):
        """Test outlier removal."""
        values = [1, 1, 1, 1, 10, 1, 1, 1]  # 10 is outlier
        cleaned = preprocessor.remove_outliers(values, threshold=2.0)

        assert len(cleaned) < len(values)
        assert 10 not in cleaned

    def test_extract_features(self, preprocessor):
        """Test feature extraction."""
        signals = [
            {"ap_mac": "00:11:22:33:44:55", "rssi": -50},
            {"ap_mac": "00:11:22:33:44:55", "rssi": -52},
            {"ap_mac": "AA:BB:CC:DD:EE:FF", "rssi": -60},
        ]
        features = preprocessor.extract_features(signals)

        assert "00:11:22:33:44:55_mean" in features
        assert "AA:BB:CC:DD:EE:FF_mean" in features

    def test_kalman_filter(self, preprocessor):
        """Test Kalman filtering."""
        measurements = [-50, -51, -49, -50, -52, -51, -50]
        filtered = preprocessor.apply_kalman_filter(measurements)

        assert len(filtered) == len(measurements)
        # Filtered signal should be smoother (less variance)
        assert np.std(filtered) <= np.std(measurements)
