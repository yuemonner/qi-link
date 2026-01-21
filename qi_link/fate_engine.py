"""
Fate Engine - The Astrology Layer
=================================

Zi Wei Dou Shu (紫微斗數) calculation engine that interprets
birth data to derive the user's cosmic blueprint.
"""

from datetime import datetime
from typing import Optional

from lunar_python import Lunar, Solar

from qi_link.exceptions import CalendarConversionError, InvalidBirthDataError
from qi_link.models import Element, FateProfile, MajorStar


class FateEngine:
    """
    Astrology calculation engine using Zi Wei Dou Shu principles.

    Converts birth datetime into:
    - Four Pillars (八字)
    - Life Palace position
    - Major Star assignment
    - Five Elements distribution
    """

    # Heavenly Stems (天干) and their elements
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    STEM_ELEMENTS = {
        "甲": Element.WOOD,
        "乙": Element.WOOD,
        "丙": Element.FIRE,
        "丁": Element.FIRE,
        "戊": Element.EARTH,
        "己": Element.EARTH,
        "庚": Element.METAL,
        "辛": Element.METAL,
        "壬": Element.WATER,
        "癸": Element.WATER,
    }

    # Earthly Branches (地支) and their elements
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    BRANCH_ELEMENTS = {
        "子": Element.WATER,
        "丑": Element.EARTH,
        "寅": Element.WOOD,
        "卯": Element.WOOD,
        "辰": Element.EARTH,
        "巳": Element.FIRE,
        "午": Element.FIRE,
        "未": Element.EARTH,
        "申": Element.METAL,
        "酉": Element.METAL,
        "戌": Element.EARTH,
        "亥": Element.WATER,
    }

    # Twelve Palaces (十二宮)
    PALACES = [
        "命宮",
        "兄弟宮",
        "夫妻宮",
        "子女宮",
        "財帛宮",
        "疾厄宮",
        "遷移宮",
        "交友宮",
        "官祿宮",
        "田宅宮",
        "福德宮",
        "父母宮",
    ]

    # Major Stars (主星) mapping based on birth factors
    MAJOR_STAR_CYCLE = [
        MajorStar.ZI_WEI,
        MajorStar.TIAN_JI,
        MajorStar.TAI_YANG,
        MajorStar.WU_QU,
        MajorStar.TIAN_TONG,
        MajorStar.LIAN_ZHEN,
        MajorStar.TIAN_FU,
        MajorStar.TAI_YIN,
        MajorStar.TAN_LANG,
        MajorStar.JU_MEN,
        MajorStar.TIAN_XIANG,
        MajorStar.TIAN_LIANG,
        MajorStar.QI_SHA,
        MajorStar.PO_JUN,
    ]

    # Star to Element associations
    STAR_ELEMENTS = {
        MajorStar.ZI_WEI: Element.EARTH,
        MajorStar.TIAN_JI: Element.WOOD,
        MajorStar.TAI_YANG: Element.FIRE,
        MajorStar.WU_QU: Element.METAL,
        MajorStar.TIAN_TONG: Element.WATER,
        MajorStar.LIAN_ZHEN: Element.FIRE,
        MajorStar.TIAN_FU: Element.EARTH,
        MajorStar.TAI_YIN: Element.WATER,
        MajorStar.TAN_LANG: Element.WOOD,
        MajorStar.JU_MEN: Element.WATER,
        MajorStar.TIAN_XIANG: Element.WATER,
        MajorStar.TIAN_LIANG: Element.EARTH,
        MajorStar.QI_SHA: Element.METAL,
        MajorStar.PO_JUN: Element.WATER,
    }

    def __init__(self):
        """Initialize the Fate Engine."""
        pass

    def calculate_fate(self, birth_datetime: datetime) -> FateProfile:
        """Calculate complete fate profile from birth datetime."""
        self._validate_birth_datetime(birth_datetime)

        try:
            solar = Solar.fromDate(birth_datetime)
            lunar = solar.getLunar()
            eight_char = lunar.getEightChar()

            year_pillar = eight_char.getYear()
            month_pillar = eight_char.getMonth()
            day_pillar = eight_char.getDay()
            hour_pillar = eight_char.getTime()

            element_dist = self._calculate_element_distribution(
                year_pillar, month_pillar, day_pillar, hour_pillar
            )

            day_stem = day_pillar[0] if day_pillar else "甲"
            inherent_element = self.STEM_ELEMENTS.get(day_stem, Element.WOOD)

            life_palace = self._calculate_life_palace(lunar)
            major_star = self._calculate_major_star(lunar, life_palace)

            return FateProfile(
                birth_datetime=birth_datetime,
                lunar_year=lunar.getYear(),
                lunar_month=lunar.getMonth(),
                lunar_day=lunar.getDay(),
                lunar_hour=self._get_lunar_hour(birth_datetime.hour),
                year_stem_branch=year_pillar,
                month_stem_branch=month_pillar,
                day_stem_branch=day_pillar,
                hour_stem_branch=hour_pillar,
                major_star=major_star,
                life_palace=life_palace,
                inherent_element=inherent_element,
                element_distribution=element_dist,
            )

        except Exception as e:
            if isinstance(e, (InvalidBirthDataError, CalendarConversionError)):
                raise
            raise CalendarConversionError(
                message=f"Failed to calculate fate: {str(e)}",
                details={"birth_datetime": str(birth_datetime)},
            )

    def _validate_birth_datetime(self, dt: datetime) -> None:
        """Validate birth datetime is reasonable."""
        now = datetime.now()
        if dt.year < 1900:
            raise InvalidBirthDataError(
                message="Birth year must be 1900 or later",
                details={"year": dt.year},
            )
        if dt > now:
            raise InvalidBirthDataError(
                message="Birth date cannot be in the future",
                details={"birth_datetime": str(dt)},
            )

    def _calculate_element_distribution(
        self, year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str
    ) -> dict[Element, int]:
        """Count elements present in the Four Pillars."""
        distribution = {e: 0 for e in Element}
        for pillar in [year_pillar, month_pillar, day_pillar, hour_pillar]:
            if len(pillar) >= 2:
                stem = pillar[0]
                branch = pillar[1]
                if stem in self.STEM_ELEMENTS:
                    distribution[self.STEM_ELEMENTS[stem]] += 1
                if branch in self.BRANCH_ELEMENTS:
                    distribution[self.BRANCH_ELEMENTS[branch]] += 1
        return distribution

    def _calculate_life_palace(self, lunar: Lunar) -> str:
        """Calculate Life Palace (命宮) position."""
        month = lunar.getMonth()
        hour = lunar.getTimeZhi()
        hour_index = self.EARTHLY_BRANCHES.index(hour) if hour in self.EARTHLY_BRANCHES else 0
        palace_index = (2 + month - hour_index) % 12
        return self.PALACES[palace_index] if palace_index < len(self.PALACES) else "命宮"

    def _calculate_major_star(self, lunar: Lunar, life_palace: str) -> MajorStar:
        """Determine the Major Star in the Life Palace."""
        lunar_day = lunar.getDay()
        palace_index = self.PALACES.index(life_palace) if life_palace in self.PALACES else 0
        star_index = (lunar_day + palace_index) % len(self.MAJOR_STAR_CYCLE)
        return self.MAJOR_STAR_CYCLE[star_index]

    def _get_lunar_hour(self, hour: int) -> int:
        """Convert 24-hour format to Chinese double-hour (時辰)."""
        adjusted = (hour + 1) % 24
        return adjusted // 2

    def get_star_description(self, star: MajorStar) -> dict:
        """Get detailed description of a Major Star."""
        descriptions = {
            MajorStar.ZI_WEI: {"name": "紫微星", "english": "Purple Star", "element": Element.EARTH, "nature": "Emperor energy - leadership, authority, dignity", "keywords": ["領導", "權威", "尊貴"]},
            MajorStar.TIAN_JI: {"name": "天機星", "english": "Heavenly Secret", "element": Element.WOOD, "nature": "Intelligence, adaptability, strategic thinking", "keywords": ["智慧", "機變", "策略"]},
            MajorStar.TAI_YANG: {"name": "太陽星", "english": "Sun Star", "element": Element.FIRE, "nature": "Radiance, generosity, public recognition", "keywords": ["光明", "慷慨", "名聲"]},
            MajorStar.WU_QU: {"name": "武曲星", "english": "Martial Music", "element": Element.METAL, "nature": "Discipline, wealth, determination", "keywords": ["剛毅", "財富", "決斷"]},
            MajorStar.TIAN_TONG: {"name": "天同星", "english": "Heavenly Unity", "element": Element.WATER, "nature": "Harmony, enjoyment, emotional depth", "keywords": ["和諧", "享樂", "情感"]},
            MajorStar.LIAN_ZHEN: {"name": "廉貞星", "english": "Chastity Star", "element": Element.FIRE, "nature": "Passion, complexity, transformation", "keywords": ["熱情", "複雜", "蛻變"]},
            MajorStar.TIAN_FU: {"name": "天府星", "english": "Heavenly Treasury", "element": Element.EARTH, "nature": "Stability, resources, contentment", "keywords": ["穩定", "資源", "滿足"]},
            MajorStar.TAI_YIN: {"name": "太陰星", "english": "Moon Star", "element": Element.WATER, "nature": "Intuition, mystery, hidden wealth", "keywords": ["直覺", "神秘", "暗財"]},
            MajorStar.TAN_LANG: {"name": "貪狼星", "english": "Greedy Wolf", "element": Element.WOOD, "nature": "Desire, charm, versatility", "keywords": ["慾望", "魅力", "多才"]},
            MajorStar.JU_MEN: {"name": "巨門星", "english": "Giant Gate", "element": Element.WATER, "nature": "Speech, analysis, hidden matters", "keywords": ["口才", "分析", "暗事"]},
            MajorStar.TIAN_XIANG: {"name": "天相星", "english": "Heavenly Minister", "element": Element.WATER, "nature": "Service, balance, diplomacy", "keywords": ["服務", "平衡", "外交"]},
            MajorStar.TIAN_LIANG: {"name": "天梁星", "english": "Heavenly Beam", "element": Element.EARTH, "nature": "Protection, wisdom, longevity", "keywords": ["庇護", "智慧", "長壽"]},
            MajorStar.QI_SHA: {"name": "七殺星", "english": "Seven Killings", "element": Element.METAL, "nature": "Power, courage, breakthrough", "keywords": ["威權", "勇氣", "突破"]},
            MajorStar.PO_JUN: {"name": "破軍星", "english": "Army Breaker", "element": Element.WATER, "nature": "Change, destruction for renewal, pioneering", "keywords": ["變動", "破舊立新", "開創"]},
        }
        return descriptions.get(star, {"name": star.value, "english": "Unknown Star", "element": Element.EARTH, "nature": "Unknown", "keywords": []})

