#!/usr/bin/env python3
"""Collect and label calibration data interactively."""
import sys
from pathlib import Path
import asyncio
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.path.insert(0, str(Path(__file__).parent.parent / "calibration"))

from logger import logger
from data_collector import DataCollector
from signal_processing.scanner import WifiScanner


async def collect_calibration_samples():
    """Interactive calibration sample collection."""
    logger.info("WiFi Indoor Positioning - Calibration Data Collector")
    logger.info("="*50)
    
    collector = DataCollector()
    scanner = WifiScanner()
    
    print("\nCalibration Instructions:")
    print("1. Stand at a marked location in your house")
    print("2. System will collect WiFi signal samples")
    print("3. Repeat for all rooms\n")
    
    rooms = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Office"]
    
    for room_idx, room in enumerate(rooms, 1):
        print(f"\n[{room_idx}/{len(rooms)}] Collecting data for: {room}")
        
        num_samples = int(input(f"Number of samples to collect [10]: ") or "10")
        
        # Start session
        collector.start_session(room, room_idx)
        logger.info(f"Started collecting {num_samples} samples in {room}")
        
        # Collect samples
        for i in range(num_samples):
            try:
                # Scan networks
                networks = await scanner.scan_networks()
                
                if networks:
                    # Create sample
                    sample = {
                        "timestamp": datetime.now().isoformat(),
                        "networks": networks,
                    }
                    collector.add_sample(sample)
                    logger.info(f"  Sample {i+1}/{num_samples} collected ({len(networks)} APs)")
                    print(f"  ✓ Sample {i+1}/{num_samples} - {len(networks)} APs detected")
                
                # Wait between samples
                await asyncio.sleep(2)
            
            except Exception as e:
                logger.error(f"Sample collection failed: {e}")
                print(f"  ✗ Error: {e}")
        
        # End session
        result = collector.end_session()
        logger.info(f"Session result: {result}")
        print(f"\n  Saved: {result['file']}")
        
        # Ask to continue
        if room_idx < len(rooms):
            input("\nPress Enter to continue to next room...")
    
    # Export dataset
    dataset_path = "./datasets/labeled/calibration_dataset.json"
    export_result = collector.export_dataset(dataset_path)
    
    logger.info(f"Dataset export: {export_result}")
    print(f"\n✅ Calibration complete!")
    print(f"Dataset saved to: {dataset_path}")
    print(f"Total sessions: {export_result['sessions']}")


if __name__ == "__main__":
    try:
        asyncio.run(collect_calibration_samples())
    except KeyboardInterrupt:
        logger.info("\nCalibration cancelled by user")
        print("\nCancelled.")
    except Exception as e:
        logger.error(f"Calibration error: {e}")
        print(f"Error: {e}")
        sys.exit(1)
