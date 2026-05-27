"""Performance benchmarks."""
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from signal_processing.preprocessor import SignalPreprocessor
from localization.motion_tracker import MotionTracker


def benchmark_signal_processing():
    """Benchmark signal processing."""
    preprocessor = SignalPreprocessor()

    signals = [{"ap_mac": f"00:11:22:33:44:{i:02x}", "rssi": -50 - i} for i in range(100)]

    start = time.time()
    for _ in range(1000):
        preprocessor.extract_features(signals)
    end = time.time()

    avg_time = (end - start) / 1000 * 1000  # Convert to ms
    print(f"Feature extraction: {avg_time:.2f}ms per call")
    assert avg_time < 10, f"Feature extraction too slow: {avg_time}ms"


def benchmark_motion_tracking():
    """Benchmark motion tracking."""
    tracker = MotionTracker()

    start = time.time()
    for i in range(1000):
        tracker.update_position(i, i)
    end = time.time()

    avg_time = (end - start) / 1000 * 1000  # Convert to ms
    print(f"Position update: {avg_time:.2f}ms per call")
    assert avg_time < 1, f"Position update too slow: {avg_time}ms"


if __name__ == "__main__":
    print("Running performance benchmarks...")
    benchmark_signal_processing()
    benchmark_motion_tracking()
    print("All benchmarks passed!")
