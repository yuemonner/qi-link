"""
Sensor Array - The DePIN Layer
==============================

Hardware sensing module that acts as the IoT sensor node,
reading real-time machine metrics and converting them into
metaphysical energy readings.
"""

import hashlib
import platform
import subprocess
import time
from datetime import datetime
from typing import Optional

import psutil

from qi_link.config import get_settings
from qi_link.exceptions import NetworkProbeError, SensorError, TemperatureReadError
from qi_link.models import Element, EnergyState, EnvironmentReading


class SensorArray:
    """
    The DePIN Layer - Real-time hardware diagnostics converted
    into metaphysical energy readings.

    Maps physical machine states to Five Element theory:
    - CPU Temperature → Yang Energy (Fire/Water axis)
    - Network Latency → Qi Flow (Wood/Earth axis)
    - System Entropy → Ambient Vibe (Random element influence)
    """

    # Temperature thresholds in Celsius
    TEMP_HIGH_THRESHOLD = 70.0  # Fire excess
    TEMP_LOW_THRESHOLD = 40.0  # Water/Cold

    # Latency thresholds in milliseconds
    LATENCY_HIGH_THRESHOLD = 100.0  # Qi stagnation (Earth)
    LATENCY_LOW_THRESHOLD = 30.0  # Smooth flow (Wood)

    def __init__(self):
        """Initialize the sensor array."""
        self._settings = get_settings()
        self._os_type = platform.system().lower()

    def read_environment(self) -> EnvironmentReading:
        """
        Perform a complete environment scan.

        Returns:
            EnvironmentReading: Complete environmental metrics with
            metaphysical classifications.

        Raises:
            SensorError: If critical sensors fail.
        """
        timestamp = datetime.now()

        # Read all metrics
        cpu_temp = self._read_cpu_temperature()
        latency = self._measure_network_latency()
        entropy_hash, entropy_score = self._generate_entropy()
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_usage = psutil.virtual_memory().percent
        uptime_hours = self._get_system_uptime_hours()

        # Classify energy states
        temp_state = self._classify_temperature(cpu_temp)
        qi_state = self._classify_latency(latency)

        return EnvironmentReading(
            timestamp=timestamp,
            cpu_temperature=cpu_temp,
            temperature_state=temp_state,
            network_latency_ms=latency,
            qi_flow_state=qi_state,
            entropy_hash=entropy_hash,
            entropy_score=entropy_score,
            cpu_usage_percent=cpu_usage,
            memory_usage_percent=memory_usage,
            system_uptime_hours=uptime_hours,
        )

    def _read_cpu_temperature(self) -> float:
        """
        Read CPU temperature using psutil or OS-specific methods.

        On systems where temperature reading is blocked, returns a
        simulated value based on CPU usage.

        Returns:
            float: CPU temperature in Celsius.
        """
        try:
            # Try psutil sensors_temperatures (Linux)
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    # Try common sensor names
                    for sensor_name in ["coretemp", "cpu_thermal", "cpu-thermal", "k10temp"]:
                        if sensor_name in temps:
                            readings = temps[sensor_name]
                            if readings:
                                return readings[0].current

                    # Fallback to first available sensor
                    first_sensor = list(temps.values())[0]
                    if first_sensor:
                        return first_sensor[0].current

            # macOS: Use powermetrics or simulate
            if self._os_type == "darwin":
                return self._read_macos_temperature()

            # Windows: Try WMI (usually restricted)
            if self._os_type == "windows":
                return self._simulate_temperature()

        except Exception:
            pass

        # Fallback: Simulate based on CPU usage
        return self._simulate_temperature()

    def _read_macos_temperature(self) -> float:
        """Attempt to read macOS temperature or simulate."""
        try:
            # Try osx-cpu-temp if installed
            result = subprocess.run(
                ["osx-cpu-temp"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            if result.returncode == 0:
                # Parse output like "45.0°C"
                temp_str = result.stdout.strip().replace("°C", "")
                return float(temp_str)
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass

        return self._simulate_temperature()

    def _simulate_temperature(self) -> float:
        """
        Simulate CPU temperature based on usage patterns.

        Uses CPU usage to estimate temperature with realistic variance.
        """
        cpu_usage = psutil.cpu_percent(interval=0.1)

        # Base temperature + usage-based heat + random variance
        base_temp = 35.0
        usage_heat = (cpu_usage / 100.0) * 45.0  # Max 45°C from usage
        time_variance = (hash(str(time.time_ns())) % 100) / 50.0 - 1.0  # ±1°C

        return round(base_temp + usage_heat + time_variance, 1)

    def _measure_network_latency(self) -> float:
        """
        Measure network latency by pinging target.

        Returns:
            float: Round-trip time in milliseconds.
        """
        target = self._settings.ping_target
        timeout = self._settings.ping_timeout

        try:
            if self._os_type == "windows":
                cmd = ["ping", "-n", "1", "-w", str(int(timeout * 1000)), target]
            else:
                cmd = ["ping", "-c", "1", "-W", str(int(timeout)), target]

            start = time.perf_counter()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 1,
            )
            elapsed = (time.perf_counter() - start) * 1000

            if result.returncode == 0:
                # Parse actual RTT from output if possible
                output = result.stdout
                if "time=" in output:
                    # Extract time value (works for most ping outputs)
                    import re

                    match = re.search(r"time[=<](\d+\.?\d*)", output)
                    if match:
                        return float(match.group(1))
                return elapsed

        except subprocess.TimeoutExpired:
            return timeout * 1000  # Return timeout as high latency
        except Exception:
            pass

        # Fallback: simulate latency
        return self._simulate_latency()

    def _simulate_latency(self) -> float:
        """Simulate network latency with realistic patterns."""
        base_latency = 25.0
        variance = (hash(str(time.time_ns())) % 100) / 2.0  # 0-50ms variance
        return round(base_latency + variance, 1)

    def _generate_entropy(self) -> tuple[str, int]:
        """
        Generate entropy hash and volatility score.

        Combines multiple entropy sources:
        - System uptime (nanosecond precision)
        - Current timestamp (nanosecond)
        - CPU times
        - Memory stats
        - Process count (if available)

        Returns:
            tuple[str, int]: (256-bit hex hash, volatility score 0-100)
        """
        # Gather entropy sources (with graceful fallbacks)
        try:
            pid_count = len(psutil.pids())
        except (PermissionError, OSError):
            pid_count = hash(time.time_ns()) % 1000  # Fallback to pseudo-random

        try:
            disk_io = str(psutil.disk_io_counters()) if hasattr(psutil, "disk_io_counters") else ""
        except (PermissionError, OSError):
            disk_io = ""

        sources = [
            str(time.time_ns()),
            str(time.perf_counter_ns()),
            str(psutil.cpu_times()),
            str(psutil.virtual_memory()),
            disk_io,
            str(pid_count),
            str(psutil.boot_time()),
        ]

        # Combine and hash
        combined = "|".join(sources)
        entropy_hash = hashlib.sha256(combined.encode()).hexdigest()

        # Calculate volatility score from hash distribution
        # Count unique characters and their positions
        char_variance = len(set(entropy_hash))
        position_sum = sum(int(c, 16) for c in entropy_hash[:16])
        volatility_score = int((char_variance + position_sum) % 101)

        return entropy_hash, volatility_score

    def _get_system_uptime_hours(self) -> float:
        """Get system uptime in hours."""
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        return round(uptime_seconds / 3600, 2)

    def _classify_temperature(self, temp: float) -> EnergyState:
        """Classify temperature into energy state."""
        if temp >= self.TEMP_HIGH_THRESHOLD:
            return EnergyState.EXCESS
        elif temp <= self.TEMP_LOW_THRESHOLD:
            return EnergyState.DEFICIENT
        return EnergyState.BALANCED

    def _classify_latency(self, latency: float) -> EnergyState:
        """Classify latency into Qi flow state."""
        if latency >= self.LATENCY_HIGH_THRESHOLD:
            return EnergyState.EXCESS  # Stagnation
        elif latency <= self.LATENCY_LOW_THRESHOLD:
            return EnergyState.DEFICIENT  # Smooth (needs grounding)
        return EnergyState.BALANCED

    def get_live_metrics(self) -> dict:
        """
        Get live metrics for UI display.

        Returns:
            dict: Current CPU and memory usage for progress bars.
        """
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
        }

