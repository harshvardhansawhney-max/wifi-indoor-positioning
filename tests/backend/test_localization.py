"""Unit tests for localization."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from localization.room_classifier import RoomClassifier
from localization.coordinate_estimator import CoordinateEstimator
from localization.motion_tracker import MotionTracker


class TestRoomClassifier:
    """Test room classification."""

    @pytest.fixture
    def classifier(self):
        return RoomClassifier()

    def test_prediction_untrained(self, classifier):
        """Test prediction on untrained model."""
        features = [1, 2, 3, 4]
        room, confidence = classifier.predict(features)

        assert room == "unknown"
        assert confidence == 0.0


class TestCoordinateEstimator:
    """Test coordinate estimation."""

    @pytest.fixture
    def estimator(self):
        return CoordinateEstimator()

    def test_set_router_positions(self, estimator):
        """Test setting router positions."""
        routers = {
            "00:11:22:33:44:55": (0, 0),
            "AA:BB:CC:DD:EE:FF": (10, 0),
            "11:22:33:44:55:66": (10, 10),
        }
        estimator.set_router_positions(routers)

        assert len(estimator.router_positions) == 3

    def test_trilateration_no_routers(self, estimator):
        """Test trilateration with no routers."""
        signal_rssi = {"00:11:22:33:44:55": -50}
        x, y, confidence = estimator.trilaterate(signal_rssi)

        assert x == 0.0
        assert y == 0.0
        assert confidence == 0.0


class TestMotionTracker:
    """Test motion tracking."""

    @pytest.fixture
    def tracker(self):
        return MotionTracker()

    def test_update_position(self, tracker):
        """Test position update."""
        tracker.update_position(0, 0)
        tracker.update_position(1, 1)
        tracker.update_position(2, 2)

        assert len(tracker.position_history) == 3

    def test_velocity_calculation(self, tracker):
        """Test velocity estimation."""
        from datetime import datetime, timedelta

        now = datetime.now()
        tracker.update_position(0, 0, now)
        tracker.update_position(1, 1, now + timedelta(seconds=1))

        velocity = tracker.get_velocity()
        assert velocity > 0

    def test_direction_calculation(self, tracker):
        """Test direction estimation."""
        tracker.update_position(0, 0)
        tracker.update_position(1, 0)  # Move east

        direction = tracker.get_direction()
        assert direction is not None
