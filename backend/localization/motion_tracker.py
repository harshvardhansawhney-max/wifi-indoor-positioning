"""Motion tracking and movement analysis."""
import numpy as np
from collections import deque
from typing import List, Tuple, Optional
from logger import logger
from datetime import datetime, timedelta


class MotionTracker:
    """Track movement patterns and estimate velocity/direction."""

    def __init__(self, window_size: int = 10):
        self.position_history = deque(maxlen=window_size)
        self.timestamp_history = deque(maxlen=window_size)
        self.window_size = window_size
        self.movement_state = "stationary"
        self.movement_threshold = 0.2  # meters

    def update_position(self, x: float, y: float, timestamp: Optional[datetime] = None):
        """Update position history."""
        if timestamp is None:
            timestamp = datetime.now()

        self.position_history.append((x, y))
        self.timestamp_history.append(timestamp)

        self._update_movement_state()

    def _update_movement_state(self):
        """Determine if user is moving or stationary."""
        if len(self.position_history) < 3:
            self.movement_state = "stationary"
            return

        # Calculate variance in recent positions
        positions = np.array(list(self.position_history))
        variance = np.var(positions, axis=0)
        total_variance = np.sum(variance)

        if total_variance > self.movement_threshold:
            self.movement_state = "moving"
        else:
            self.movement_state = "stationary"

    def get_velocity(self) -> float:
        """Estimate current velocity in m/s."""
        if len(self.position_history) < 2 or len(self.timestamp_history) < 2:
            return 0.0

        # Use last two positions
        x1, y1 = self.position_history[-2]
        x2, y2 = self.position_history[-1]
        distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        t1 = self.timestamp_history[-2]
        t2 = self.timestamp_history[-1]
        time_diff = (t2 - t1).total_seconds()

        if time_diff > 0:
            velocity = distance / time_diff
            return velocity
        return 0.0

    def get_direction(self) -> Optional[float]:
        """Get movement direction in degrees (0-360)."""
        if len(self.position_history) < 2:
            return None

        # Use least squares to fit direction vector
        positions = np.array(list(self.position_history))
        times = np.arange(len(positions))

        # Fit line through positions
        coeffs = np.polyfit(times, positions[:, 0], 1)  # x direction
        dx = coeffs[0]
        coeffs = np.polyfit(times, positions[:, 1], 1)  # y direction
        dy = coeffs[0]

        # Calculate angle
        angle = np.arctan2(dy, dx) * 180 / np.pi
        return float((angle + 360) % 360)

    def get_trajectory(self, window_size: Optional[int] = None) -> List[Tuple[float, float]]:
        """Get recent trajectory."""
        if window_size is None:
            window_size = len(self.position_history)

        return list(self.position_history)[-window_size:]

    def detect_room_change(self, room_a: str, room_b: str) -> bool:
        """Detect if user changed rooms."""
        return room_a != room_b

    def estimate_dwell_time(self) -> timedelta:
        """Estimate how long user stayed in current position."""
        if len(self.timestamp_history) < 1:
            return timedelta(0)

        first_time = self.timestamp_history[0]
        last_time = self.timestamp_history[-1]
        return last_time - first_time

    def clear_history(self):
        """Clear position history."""
        self.position_history.clear()
        self.timestamp_history.clear()
        self.movement_state = "stationary"
