"""
Domain Models
=============

Pydantic models for type-safe data structures representing the
metaphysical and physical layers of Qi-Link.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, computed_field


# =============================================================================
# ENUMERATIONS
# =============================================================================


class Element(str, Enum):
    """The Five Elements (Wu Xing) of Chinese metaphysics."""

    METAL = "metal"  # 金 - Structure, precision, clarity
    WOOD = "wood"  # 木 - Growth, expansion, flexibility
    WATER = "water"  # 水 - Wisdom, adaptability, flow
    FIRE = "fire"  # 火 - Passion, transformation, energy
    EARTH = "earth"  # 土 - Stability, nourishment, grounding

    @property
    def chinese(self) -> str:
        """Return Chinese character for the element."""
        mapping = {
            "metal": "金",
            "wood": "木",
            "water": "水",
            "fire": "火",
            "earth": "土",
        }
        return mapping[self.value]

    @property
    def color(self) -> str:
        """Return associated color hex code."""
        mapping = {
            "metal": "#C0C0C0",  # Silver
            "wood": "#228B22",  # Forest Green
            "water": "#1E90FF",  # Dodger Blue
            "fire": "#FF4500",  # Orange Red
            "earth": "#DAA520",  # Golden Rod
        }
        return mapping[self.value]

    @property
    def generates(self) -> "Element":
        """Return the element this one generates (生)."""
        cycle = {
            "metal": Element.WATER,
            "water": Element.WOOD,
            "wood": Element.FIRE,
            "fire": Element.EARTH,
            "earth": Element.METAL,
        }
        return cycle[self.value]

    @property
    def controls(self) -> "Element":
        """Return the element this one controls (剋)."""
        cycle = {
            "metal": Element.WOOD,
            "wood": Element.EARTH,
            "water": Element.FIRE,
            "fire": Element.METAL,
            "earth": Element.WATER,
        }
        return cycle[self.value]


class EnergyState(str, Enum):
    """Energy state classifications."""

    EXCESS = "excess"  # 太過 - Too much
    BALANCED = "balanced"  # 平衡 - Just right
    DEFICIENT = "deficient"  # 不足 - Too little


class MajorStar(str, Enum):
    """Major Stars (主星) in Zi Wei Dou Shu."""

    ZI_WEI = "紫微"  # Purple Star - Emperor
    TIAN_JI = "天機"  # Heavenly Secret
    TAI_YANG = "太陽"  # Sun
    WU_QU = "武曲"  # Martial Music
    TIAN_TONG = "天同"  # Heavenly Unity
    LIAN_ZHEN = "廉貞"  # Chastity
    TIAN_FU = "天府"  # Heavenly Treasury
    TAI_YIN = "太陰"  # Moon
    TAN_LANG = "貪狼"  # Greedy Wolf
    JU_MEN = "巨門"  # Giant Gate
    TIAN_XIANG = "天相"  # Heavenly Minister
    TIAN_LIANG = "天梁"  # Heavenly Beam
    QI_SHA = "七殺"  # Seven Killings
    PO_JUN = "破軍"  # Army Breaker


# =============================================================================
# DATA MODELS
# =============================================================================


class EnvironmentReading(BaseModel):
    """Real-time environmental readings from the DePIN sensor array."""

    timestamp: datetime = Field(default_factory=datetime.now)

    # Yang Energy - CPU Temperature
    cpu_temperature: float = Field(
        ...,
        ge=0,
        le=150,
        description="CPU temperature in Celsius",
    )
    temperature_state: EnergyState = Field(
        ...,
        description="Classified temperature energy state",
    )

    # Qi Flow - Network Latency
    network_latency_ms: float = Field(
        ...,
        ge=0,
        description="Network latency in milliseconds",
    )
    qi_flow_state: EnergyState = Field(
        ...,
        description="Classified Qi flow state",
    )

    # Ambient Vibe - Entropy
    entropy_hash: str = Field(
        ...,
        min_length=64,
        max_length=64,
        description="256-bit entropy hash",
    )
    entropy_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Entropy volatility score 0-100",
    )

    # System Stats
    cpu_usage_percent: float = Field(..., ge=0, le=100)
    memory_usage_percent: float = Field(..., ge=0, le=100)
    system_uptime_hours: float = Field(..., ge=0)

    @computed_field
    @property
    def dominant_environment_element(self) -> Element:
        """Derive dominant element from environment readings."""
        # High temp = Fire, Low temp = Water
        if self.temperature_state == EnergyState.EXCESS:
            return Element.FIRE
        elif self.temperature_state == EnergyState.DEFICIENT:
            return Element.WATER

        # High latency = Earth (stagnation), Low = Wood (smooth flow)
        if self.qi_flow_state == EnergyState.EXCESS:
            return Element.EARTH
        elif self.qi_flow_state == EnergyState.DEFICIENT:
            return Element.WOOD

        # Balanced state - derive from entropy
        entropy_element_map = [
            Element.METAL,
            Element.WATER,
            Element.WOOD,
            Element.FIRE,
            Element.EARTH,
        ]
        return entropy_element_map[self.entropy_score % 5]


class FateProfile(BaseModel):
    """User's astrological profile derived from birth data."""

    birth_datetime: datetime
    lunar_year: int
    lunar_month: int
    lunar_day: int
    lunar_hour: int

    # Heavenly Stems and Earthly Branches
    year_stem_branch: str = Field(..., description="年柱")
    month_stem_branch: str = Field(..., description="月柱")
    day_stem_branch: str = Field(..., description="日柱")
    hour_stem_branch: str = Field(..., description="時柱")

    # Zi Wei Dou Shu
    major_star: MajorStar = Field(..., description="命宮主星")
    life_palace: str = Field(..., description="命宮")

    # Five Elements Analysis
    inherent_element: Element = Field(
        ...,
        description="User's dominant birth element",
    )
    
    # Extra data for advanced calculations
    extra_data: Optional[dict] = Field(
        default=None,
        description="Additional Zi Wei data: all stars, si hua, wu xing ju",
    )
    
    element_distribution: dict[Element, int] = Field(
        default_factory=dict,
        description="Count of each element in chart",
    )

    @computed_field
    @property
    def weakest_element(self) -> Element:
        """Find the element most lacking in the chart."""
        if not self.element_distribution:
            return Element.EARTH
        return min(self.element_distribution, key=self.element_distribution.get)

    @computed_field
    @property
    def strongest_element(self) -> Element:
        """Find the most dominant element in the chart."""
        if not self.element_distribution:
            return self.inherent_element
        return max(self.element_distribution, key=self.element_distribution.get)


class Diagnosis(BaseModel):
    """Metaphysical diagnosis combining fate and environment."""

    fate_profile: FateProfile
    environment: EnvironmentReading

    # Analysis Results
    imbalance_description: str = Field(
        ...,
        description="Natural language description of the imbalance",
    )
    imbalance_description_chinese: str = Field(
        ...,
        description="Chinese description of the imbalance",
    )

    # Remedy
    remedy_elements: list[Element] = Field(
        ...,
        min_length=1,
        max_length=3,
        description="Elements needed to restore balance",
    )
    remedy_description: str = Field(
        ...,
        description="Description of the corrective energy needed",
    )

    # Generated Prompt
    talisman_prompt: str = Field(
        ...,
        description="DALL-E prompt for talisman generation",
    )
    talisman_style: str = Field(
        default="Cyberpunk Taoist Talisman",
        description="Art style descriptor",
    )

    @computed_field
    @property
    def primary_remedy_element(self) -> Element:
        """Get the primary remedy element."""
        return self.remedy_elements[0]


class TalismanMetadata(BaseModel):
    """Complete metadata for a generated talisman NFT."""

    # Identity
    token_id: str = Field(..., description="Unique token identifier")
    created_at: datetime = Field(default_factory=datetime.now)

    # Location (Mock)
    location_ip: str = Field(default="192.168.1.1")
    location_region: str = Field(default="Cyber Realm")

    # Source Data
    diagnosis: Diagnosis
    image_url: str = Field(..., description="URL or path to generated image")

    # Blockchain Proof
    metadata_hash: str = Field(
        ...,
        min_length=64,
        description="Keccak256 hash of metadata",
    )
    block_number: int = Field(default=0, description="Mock block number")
    chain_id: int = Field(default=1, description="Mock chain ID (1=Ethereum)")

    @computed_field
    @property
    def opensea_attributes(self) -> list[dict]:
        """Generate OpenSea-compatible attributes."""
        return [
            {
                "trait_type": "Major Star",
                "value": self.diagnosis.fate_profile.major_star.value,
            },
            {
                "trait_type": "Inherent Element",
                "value": self.diagnosis.fate_profile.inherent_element.value,
            },
            {
                "trait_type": "Environment Element",
                "value": self.diagnosis.environment.dominant_environment_element.value,
            },
            {
                "trait_type": "Primary Remedy",
                "value": self.diagnosis.primary_remedy_element.value,
            },
            {
                "trait_type": "Entropy Score",
                "value": self.diagnosis.environment.entropy_score,
                "display_type": "number",
            },
            {
                "trait_type": "CPU Temperature",
                "value": round(self.diagnosis.environment.cpu_temperature, 1),
                "display_type": "number",
            },
            {
                "trait_type": "Network Latency",
                "value": round(self.diagnosis.environment.network_latency_ms, 1),
                "display_type": "number",
            },
        ]

