"""WiFi signal scanning."""
import asyncio
from typing import List, Dict
from datetime import datetime
from logger import logger
from config import settings


class WifiScanner:
    """WiFi network scanner."""

    def __init__(self):
        self.interface = settings.WIFI_INTERFACE
        self.rssi_threshold = settings.RSSI_THRESHOLD
        self.scan_interval = settings.SCAN_INTERVAL
        self.is_scanning = False

    async def scan_networks(self) -> List[Dict]:
        """Scan nearby WiFi networks."""
        try:
            # Import platform-specific scanner
            if "linux" in sys.platform:
                return await self._scan_linux()
            elif "win" in sys.platform:
                return await self._scan_windows()
            elif "darwin" in sys.platform:
                return await self._scan_macos()
        except Exception as e:
            logger.error(f"WiFi scan failed: {e}")
            return []

    async def _scan_linux(self) -> List[Dict]:
        """Scan WiFi networks on Linux."""
        import subprocess

        try:
            # Use nmcli or iw
            result = await asyncio.to_thread(
                subprocess.run,
                ["nmcli", "dev", "wifi", "list"],
                capture_output=True,
                text=True,
            )

            networks = []
            for line in result.stdout.split("\n")[1:]:
                if not line.strip():
                    continue

                parts = line.split()
                if len(parts) >= 7:
                    networks.append(
                        {
                            "ssid": parts[0],
                            "mac": parts[1],
                            "mode": parts[2],
                            "channel": int(parts[3]),
                            "rate": int(parts[4]),
                            "signal": int(parts[5]),
                            "bars": parts[6],
                        }
                    )

            return networks
        except Exception as e:
            logger.error(f"Linux WiFi scan failed: {e}")
            return []

    async def _scan_windows(self) -> List[Dict]:
        """Scan WiFi networks on Windows."""
        import subprocess

        try:
            result = await asyncio.to_thread(
                subprocess.run,
                ["netsh", "wlan", "show", "networks"],
                capture_output=True,
                text=True,
            )
            # Parse output
            return []
        except Exception as e:
            logger.error(f"Windows WiFi scan failed: {e}")
            return []

    async def _scan_macos(self) -> List[Dict]:
        """Scan WiFi networks on macOS."""
        import subprocess

        try:
            result = await asyncio.to_thread(
                subprocess.run,
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
                capture_output=True,
                text=True,
            )

            networks = []
            for line in result.stdout.split("\n")[1:]:
                if not line.strip():
                    continue

                parts = line.split()
                if len(parts) >= 7:
                    networks.append(
                        {
                            "ssid": parts[0],
                            "mac": parts[1],
                            "rssi": int(parts[2]),
                            "channel": int(parts[3]),
                            "ht": parts[4],
                            "cc": parts[5],
                            "security": " ".join(parts[6:]),
                        }
                    )

            return networks
        except Exception as e:
            logger.error(f"macOS WiFi scan failed: {e}")
            return []

    async def start_scanning(self):
        """Start continuous WiFi scanning."""
        self.is_scanning = True
        logger.info("WiFi scanning started")

        while self.is_scanning:
            try:
                networks = await self.scan_networks()
                yield networks
                await asyncio.sleep(self.scan_interval)
            except Exception as e:
                logger.error(f"Scanning error: {e}")
                await asyncio.sleep(self.scan_interval)

    def stop_scanning(self):
        """Stop WiFi scanning."""
        self.is_scanning = False
        logger.info("WiFi scanning stopped")
