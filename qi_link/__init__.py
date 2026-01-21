"""
Qi-Link: The DePIN Fengshui Node
================================

A Cyber-Metaphysics application combining traditional Chinese Astrology 
(Zi Wei Dou Shu) with real-time hardware diagnostics to generate 
AI-powered corrective energy talismans.

Destiny (Time) + Fortune (Space) = Corrective Energy (Talisman)
"""

__version__ = "1.0.0"
__author__ = "Qi-Link Project"

from qi_link.models import (
    Element,
    EnergyState,
    EnvironmentReading,
    FateProfile,
    Diagnosis,
    TalismanMetadata,
)
from qi_link.sensor_array import SensorArray
from qi_link.fate_engine import FateEngine
from qi_link.alchemist import Alchemist
from qi_link.ether_link import EtherLink
from qi_link.talisman_generator import TalismanGenerator
from qi_link.location_service import LocationService

__all__ = [
    "Element",
    "EnergyState",
    "EnvironmentReading",
    "FateProfile",
    "Diagnosis",
    "TalismanMetadata",
    "SensorArray",
    "FateEngine",
    "Alchemist",
    "EtherLink",
    "TalismanGenerator",
    "LocationService",
]

