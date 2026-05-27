"""Calibration data collector."""
import json
from datetime import datetime
from pathlib import Path
from logger import logger
from typing import List, Dict


class DataCollector:
    """Collect and manage calibration data."""

    def __init__(self, output_dir: str = "./datasets/labeled"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.current_session = None
        self.samples = []

    def start_session(self, room: str, point_id: int):
        """Start collecting samples at a point."""
        self.current_session = {
            "room": room,
            "point_id": point_id,
            "started_at": datetime.now().isoformat(),
            "samples": [],
        }
        logger.info(f"Started collecting samples in {room}")

    def add_sample(self, signal_data: Dict):
        """Add a signal sample."""
        if self.current_session:
            self.current_session["samples"].append(signal_data)
            logger.debug(f"Added sample: {len(self.current_session['samples'])} total")

    def end_session(self) -> Dict:
        """End collection session and save data."""
        if not self.current_session:
            return {"status": "error", "message": "No active session"}

        self.current_session["ended_at"] = datetime.now().isoformat()
        room = self.current_session["room"]
        num_samples = len(self.current_session["samples"])

        # Save to file
        filename = self.output_dir / f"{room}_{self.current_session['point_id']}_{datetime.now().timestamp()}.json"
        with open(filename, "w") as f:
            json.dump(self.current_session, f, indent=2)

        logger.info(f"Saved {num_samples} samples to {filename}")
        self.samples.append(self.current_session)
        self.current_session = None

        return {
            "status": "success",
            "room": room,
            "samples_collected": num_samples,
            "file": str(filename),
        }

    def export_dataset(self, output_path: str):
        """Export all collected samples as training dataset."""
        try:
            with open(output_path, "w") as f:
                json.dump(self.samples, f, indent=2)
            logger.info(f"Exported {len(self.samples)} sessions to {output_path}")
            return {"status": "success", "path": output_path, "sessions": len(self.samples)}
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return {"status": "error", "message": str(e)}
