"""Coordinate estimation using trilateration and neural networks."""
import numpy as np
from typing import Tuple
from scipy.optimize import minimize
from logger import logger


class CoordinateEstimator:
    """Estimate X, Y coordinates from signal measurements."""

    def __init__(self):
        self.router_positions = {}  # {ap_mac: (x, y)}
        self.path_loss_model = {}  # {ap_mac: (a, n)}

    def set_router_positions(self, routers: Dict[str, Tuple[float, float]]):
        """Set known router positions."""
        self.router_positions = routers
        logger.info(f"Set {len(routers)} router positions")

    def calibrate_path_loss(self, ap_mac: str, measured_rssi: List[float],
                            known_distances: List[float]):
        """Calibrate path loss model for an AP."""
        try:
            rssi_array = np.array(measured_rssi)
            distance_array = np.array(known_distances)

            # Path loss model: RSSI = a - n * 10 * log10(distance)
            # Fit parameters a and n
            def error_function(params):
                a, n = params
                predicted_rssi = a - n * 10 * np.log10(distance_array)
                return np.sum((rssi_array - predicted_rssi) ** 2)

            result = minimize(error_function, [0, 2], method="Nelder-Mead")
            a, n = result.x
            self.path_loss_model[ap_mac] = (a, n)
            logger.info(f"Calibrated path loss for {ap_mac}: a={a:.2f}, n={n:.2f}")
        except Exception as e:
            logger.error(f"Path loss calibration failed: {e}")

    def rssi_to_distance(self, ap_mac: str, rssi: float) -> float:
        """Convert RSSI to distance using path loss model."""
        if ap_mac not in self.path_loss_model:
            return 10.0  # Default distance

        a, n = self.path_loss_model[ap_mac]
        distance = 10 ** ((a - rssi) / (10 * n))
        return max(0.1, distance)  # Minimum 0.1m

    def trilaterate(self, signal_rssi: Dict[str, float]) -> Tuple[float, float, float]:
        """Estimate coordinates using trilateration."""
        if not self.router_positions or not signal_rssi:
            return 0.0, 0.0, 0.0

        # Get distances from RSSI
        distances = {}
        for ap_mac, rssi in signal_rssi.items():
            if ap_mac in self.router_positions:
                distances[ap_mac] = self.rssi_to_distance(ap_mac, rssi)

        if len(distances) < 2:
            return 0.0, 0.0, 0.0

        # Minimize error function
        def error_function(position):
            x, y = position
            error = 0
            for ap_mac, distance in distances.items():
                router_x, router_y = self.router_positions[ap_mac]
                calculated_distance = np.sqrt((x - router_x) ** 2 + (y - router_y) ** 2)
                error += (calculated_distance - distance) ** 2
            return error

        # Initial guess: center of router positions
        initial_x = np.mean([pos[0] for pos in self.router_positions.values()])
        initial_y = np.mean([pos[1] for pos in self.router_positions.values()])

        result = minimize(error_function, [initial_x, initial_y], method="Nelder-Mead")
        x, y = result.x

        # Calculate confidence based on residual error
        confidence = 1.0 / (1.0 + result.fun)  # Sigmoid-like confidence
        confidence = min(1.0, confidence)

        return float(x), float(y), float(confidence)

    def weighted_centroid(self, signal_rssi: Dict[str, float]) -> Tuple[float, float, float]:
        """Estimate coordinates using weighted centroid."""
        if not self.router_positions or not signal_rssi:
            return 0.0, 0.0, 0.0

        weights = {}
        total_weight = 0

        for ap_mac, rssi in signal_rssi.items():
            if ap_mac in self.router_positions:
                # Weight inversely proportional to distance
                distance = self.rssi_to_distance(ap_mac, rssi)
                weight = 1.0 / (distance + 0.1)  # Avoid division by zero
                weights[ap_mac] = weight
                total_weight += weight

        if total_weight == 0:
            return 0.0, 0.0, 0.0

        # Calculate weighted centroid
        weighted_x = sum(
            weight * self.router_positions[ap_mac][0] for ap_mac, weight in weights.items()
        ) / total_weight
        weighted_y = sum(
            weight * self.router_positions[ap_mac][1] for ap_mac, weight in weights.items()
        ) / total_weight

        confidence = min(1.0, total_weight / len(self.router_positions))

        return float(weighted_x), float(weighted_y), float(confidence)
