"""
Fate Engine - The Astrology Layer (倪師版)
==========================================

Zi Wei Dou Shu calculation engine - ACCURATE VERSION
Based on 中州派/三合派 methodology with correct star placement.

Key Algorithm:
1. Calculate Life Palace position (命宮地支)
2. Determine Wu Xing Ju (五行局)
3. Locate Zi Wei Star (紫微定位)
4. Locate Tian Fu Star (天府定位) - symmetric to Zi Wei
5. Place all 14 stars using relative offsets
"""

from datetime import datetime
from typing import Optional, List, Tuple, Dict

from lunar_python import Lunar, Solar

from qi_link.exceptions import CalendarConversionError, InvalidBirthDataError
from qi_link.models import Element, FateProfile, MajorStar


class FateEngine:
    """
    Accurate Zi Wei Dou Shu calculation engine.
    
    地支索引 (1-based for traditional calculation):
    子=1, 丑=2, 寅=3, 卯=4, 辰=5, 巳=6, 
    午=7, 未=8, 申=9, 酉=10, 戌=11, 亥=12
    
    For internal array (0-based):
    子=0, 丑=1, 寅=2, 卯=3, 辰=4, 巳=5,
    午=6, 未=7, 申=8, 酉=9, 戌=10, 亥=11
    """

    # 地支名稱 (0-indexed)
    BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 天干名稱
    STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    
    # 天干五行
    STEM_ELEMENTS = {
        "甲": Element.WOOD, "乙": Element.WOOD,
        "丙": Element.FIRE, "丁": Element.FIRE,
        "戊": Element.EARTH, "己": Element.EARTH,
        "庚": Element.METAL, "辛": Element.METAL,
        "壬": Element.WATER, "癸": Element.WATER,
    }
    
    # 地支五行
    BRANCH_ELEMENTS = {
        "子": Element.WATER, "丑": Element.EARTH, "寅": Element.WOOD, "卯": Element.WOOD,
        "辰": Element.EARTH, "巳": Element.FIRE, "午": Element.FIRE, "未": Element.EARTH,
        "申": Element.METAL, "酉": Element.METAL, "戌": Element.EARTH, "亥": Element.WATER,
    }

    # 五行局表 (年干, 命宮地支) -> 局數
    # 水二局=2, 木三局=3, 金四局=4, 土五局=5, 火六局=6
    WU_XING_JU = {
        # 甲己年
        "甲子": 2, "甲丑": 6, "甲寅": 6, "甲卯": 5, "甲辰": 5, "甲巳": 3,
        "甲午": 3, "甲未": 5, "甲申": 5, "甲酉": 4, "甲戌": 4, "甲亥": 2,
        "己子": 2, "己丑": 6, "己寅": 6, "己卯": 5, "己辰": 5, "己巳": 3,
        "己午": 3, "己未": 5, "己申": 5, "己酉": 4, "己戌": 4, "己亥": 2,
        # 乙庚年
        "乙子": 4, "乙丑": 4, "乙寅": 2, "乙卯": 2, "乙辰": 6, "乙巳": 6,
        "乙午": 5, "乙未": 5, "乙申": 3, "乙酉": 3, "乙戌": 5, "乙亥": 5,
        "庚子": 4, "庚丑": 4, "庚寅": 2, "庚卯": 2, "庚辰": 6, "庚巳": 6,
        "庚午": 5, "庚未": 5, "庚申": 3, "庚酉": 3, "庚戌": 5, "庚亥": 5,
        # 丙辛年
        "丙子": 5, "丙丑": 5, "丙寅": 4, "丙卯": 4, "丙辰": 2, "丙巳": 2,
        "丙午": 6, "丙未": 6, "丙申": 5, "丙酉": 5, "丙戌": 3, "丙亥": 3,
        "辛子": 5, "辛丑": 5, "辛寅": 4, "辛卯": 4, "辛辰": 2, "辛巳": 2,
        "辛午": 6, "辛未": 6, "辛申": 5, "辛酉": 5, "辛戌": 3, "辛亥": 3,
        # 丁壬年
        "丁子": 3, "丁丑": 3, "丁寅": 5, "丁卯": 5, "丁辰": 4, "丁巳": 4,
        "丁午": 2, "丁未": 2, "丁申": 6, "丁酉": 6, "丁戌": 5, "丁亥": 5,
        "壬子": 3, "壬丑": 3, "壬寅": 5, "壬卯": 5, "壬辰": 4, "壬巳": 4,
        "壬午": 2, "壬未": 2, "壬申": 6, "壬酉": 6, "壬戌": 5, "壬亥": 5,
        # 戊癸年
        "戊子": 6, "戊丑": 6, "戊寅": 5, "戊卯": 5, "戊辰": 3, "戊巳": 3,
        "戊午": 5, "戊未": 5, "戊申": 2, "戊酉": 2, "戊戌": 6, "戊亥": 6,
        "癸子": 6, "癸丑": 6, "癸寅": 5, "癸卯": 5, "癸辰": 3, "癸巳": 3,
        "癸午": 5, "癸未": 5, "癸申": 2, "癸酉": 2, "癸戌": 6, "癸亥": 6,
    }
    
    # 局名
    JU_NAMES = {2: "水二局", 3: "木三局", 4: "金四局", 5: "土五局", 6: "火六局"}

    # 紫微星安星表 (倪師終極版)
    # Key: (局數, 農曆日) -> 紫微所在地支 (0-indexed: 子=0...亥=11)
    # 這是根據傳統安星訣整理的完整表
    ZI_WEI_TABLE = {}
    
    # 四化表
    SI_HUA = {
        "甲": {"化祿": "廉貞", "化權": "破軍", "化科": "武曲", "化忌": "太陽"},
        "乙": {"化祿": "天機", "化權": "天梁", "化科": "紫微", "化忌": "太陰"},
        "丙": {"化祿": "天同", "化權": "天機", "化科": "文昌", "化忌": "廉貞"},
        "丁": {"化祿": "太陰", "化權": "天同", "化科": "天機", "化忌": "巨門"},
        "戊": {"化祿": "貪狼", "化權": "太陰", "化科": "右弼", "化忌": "天機"},
        "己": {"化祿": "武曲", "化權": "貪狼", "化科": "天梁", "化忌": "文曲"},
        "庚": {"化祿": "太陽", "化權": "武曲", "化科": "太陰", "化忌": "天同"},
        "辛": {"化祿": "巨門", "化權": "太陽", "化科": "文曲", "化忌": "文昌"},
        "壬": {"化祿": "天梁", "化權": "紫微", "化科": "左輔", "化忌": "武曲"},
        "癸": {"化祿": "破軍", "化權": "巨門", "化科": "太陰", "化忌": "貪狼"},
    }

    def __init__(self):
        """Initialize with complete Zi Wei lookup table."""
        self._build_zi_wei_table()

    def _build_zi_wei_table(self):
        """
        Build Zi Wei placement table using 倪師公式.
        
        算法邏輯:
        1. quotient = day // bureau
        2. remainder = day % bureau
        3. 如果整除 (remainder == 0):
           - 位置 = 寅(3) + quotient - 1 (1-based)
        4. 如果不整除:
           - add_on = bureau - remainder (需要補多少)
           - new_quotient = quotient + 1
           - base_position = 寅(3) + new_quotient - 1
           - 核心口訣：商數起宮，單數順數，雙數逆數
           - 如果 new_quotient 是奇數: 順數 (加) add_on
           - 如果 new_quotient 是偶數: 逆數 (減) add_on
        """
        YIN = 3  # 寅 = 3 (1-based)
        
        for bureau in [2, 3, 4, 5, 6]:
            for day in range(1, 31):
                quotient = day // bureau
                remainder = day % bureau
                
                if remainder == 0:
                    # 整除：從寅順數 quotient 位
                    position_1based = YIN + quotient - 1
                else:
                    # 不整除：需要補數
                    add_on = bureau - remainder
                    new_quotient = quotient + 1
                    
                    # 基礎位置
                    base_position = YIN + new_quotient - 1
                    
                    # 核心口訣：商數起宮，單數順數，雙數逆數
                    if new_quotient % 2 == 1:  # 奇數 (單數): 順數
                        position_1based = base_position + add_on
                    else:  # 偶數 (雙數): 逆數
                        position_1based = base_position - add_on
                
                # 轉換到 0-based (子=0, 丑=1, ..., 亥=11)
                # 1-based: 子=1, 丑=2, ..., 亥=12
                position_0based = (position_1based - 1) % 12
                
                self.ZI_WEI_TABLE[(bureau, day)] = position_0based

    def get_zi_wei_location(self, lunar_day: int, bureau: int) -> int:
        """
        獲取紫微星位置 (0-indexed).
        
        Args:
            lunar_day: 農曆日 (1-30)
            bureau: 五行局 (2,3,4,5,6)
        
        Returns:
            地支索引 (0=子, 1=丑, 2=寅, ...)
        """
        day = min(max(lunar_day, 1), 30)
        return self.ZI_WEI_TABLE.get((bureau, day), 2)

    # 紫微天府對照表 (標準安星法)
    # 紫府同宮只在寅(2)和申(8)！
    # 0-indexed: 子=0, 丑=1, 寅=2, 卯=3, 辰=4, 巳=5, 午=6, 未=7, 申=8, 酉=9, 戌=10, 亥=11
    TIAN_FU_MAP = {
        0: 4,   # 紫微子 → 天府辰
        1: 3,   # 紫微丑 → 天府卯
        2: 2,   # 紫微寅 → 天府寅 (紫府同宮!)
        3: 1,   # 紫微卯 → 天府丑
        4: 0,   # 紫微辰 → 天府子
        5: 11,  # 紫微巳 → 天府亥
        6: 10,  # 紫微午 → 天府戌
        7: 9,   # 紫微未 → 天府酉
        8: 8,   # 紫微申 → 天府申 (紫府同宮!)
        9: 7,   # 紫微酉 → 天府未
        10: 6,  # 紫微戌 → 天府午
        11: 5,  # 紫微亥 → 天府巳
    }

    def get_tian_fu_location(self, zi_wei_idx: int) -> int:
        """
        獲取天府星位置 (使用標準對照表).
        
        紫府同宮只在寅宮和申宮！
        其他宮位紫微獨坐，天府另有固定位置。
        
        Args:
            zi_wei_idx: 紫微位置 (0-indexed)
        
        Returns:
            天府位置 (0-indexed)
        """
        return self.TIAN_FU_MAP.get(zi_wei_idx, 4)

    def place_all_stars(self, zi_wei_idx: int, tian_fu_idx: int) -> Dict[str, int]:
        """
        安放所有14顆主星.
        
        紫微系 (逆時針): 紫微, 天機(-1), 太陽(-3), 武曲(-4), 天同(-5), 廉貞(-8)
        天府系 (順時針): 天府, 太陰(+1), 貪狼(+2), 巨門(+3), 天相(+4), 天梁(+5), 七殺(+6), 破軍(+10)
        """
        positions = {}
        
        # 紫微系 (逆時針分布)
        positions["紫微"] = zi_wei_idx
        positions["天機"] = (zi_wei_idx - 1) % 12
        positions["太陽"] = (zi_wei_idx - 3) % 12
        positions["武曲"] = (zi_wei_idx - 4) % 12
        positions["天同"] = (zi_wei_idx - 5) % 12
        positions["廉貞"] = (zi_wei_idx - 8) % 12
        
        # 天府系 (順時針分布)
        positions["天府"] = tian_fu_idx
        positions["太陰"] = (tian_fu_idx + 1) % 12
        positions["貪狼"] = (tian_fu_idx + 2) % 12
        positions["巨門"] = (tian_fu_idx + 3) % 12
        positions["天相"] = (tian_fu_idx + 4) % 12
        positions["天梁"] = (tian_fu_idx + 5) % 12
        positions["七殺"] = (tian_fu_idx + 6) % 12
        positions["破軍"] = (tian_fu_idx + 10) % 12
        
        return positions

    def get_life_palace_branch(self, lunar_month: int, hour_idx: int) -> int:
        """
        計算命宮地支.
        
        算法: 從寅(2)起正月，順數到生月，再逆數到生時
        公式: (寅 + 月 - 1 - 時) % 12
        
        Args:
            lunar_month: 農曆月 (1-12)
            hour_idx: 時辰索引 (0=子時, 1=丑時, ...)
        
        Returns:
            命宮地支索引 (0-indexed)
        """
        # 寅是索引2
        yin_idx = 2
        # 從寅順數到生月的位置
        month_pos = (yin_idx + lunar_month - 1) % 12
        # 從該位置逆數生時
        life_palace = (month_pos - hour_idx) % 12
        return life_palace

    def calculate_fate(self, birth_datetime: datetime) -> FateProfile:
        """Calculate complete fate profile."""
        self._validate_birth_datetime(birth_datetime)

        try:
            # 1. 農曆轉換
            solar = Solar.fromDate(birth_datetime)
            lunar = solar.getLunar()
            eight_char = lunar.getEightChar()

            # 2. 八字
            year_pillar = eight_char.getYear()
            month_pillar = eight_char.getMonth()
            day_pillar = eight_char.getDay()
            hour_pillar = eight_char.getTime()
            
            year_stem = year_pillar[0] if year_pillar else "甲"
            
            # 3. 農曆日月
            lunar_month = abs(lunar.getMonth())
            lunar_day = lunar.getDay()
            
            # 4. 時辰索引
            hour_idx = self._get_hour_index(birth_datetime.hour)
            
            # 5. 命宮地支
            life_palace_idx = self.get_life_palace_branch(lunar_month, hour_idx)
            life_palace_branch = self.BRANCHES[life_palace_idx]
            
            # 6. 五行局
            ju_key = year_stem + life_palace_branch
            bureau = self.WU_XING_JU.get(ju_key, 3)
            ju_name = self.JU_NAMES.get(bureau, "木三局")
            
            # 7. 紫微位置
            zi_wei_idx = self.get_zi_wei_location(lunar_day, bureau)
            
            # 8. 天府位置
            tian_fu_idx = self.get_tian_fu_location(zi_wei_idx)
            
            # 9. 安放所有星
            star_positions = self.place_all_stars(zi_wei_idx, tian_fu_idx)
            
            # 10. 命宮主星
            stars_in_life_palace = [
                star for star, pos in star_positions.items() 
                if pos == life_palace_idx
            ]
            
            # 排序 (按重要性)
            star_priority = ["紫微", "天府", "武曲", "貪狼", "天機", "太陽", "太陰", 
                           "天同", "廉貞", "巨門", "天相", "天梁", "七殺", "破軍"]
            stars_in_life_palace.sort(
                key=lambda s: star_priority.index(s) if s in star_priority else 99
            )
            
            # 11. 四化
            si_hua = self.SI_HUA.get(year_stem, {})
            si_hua_in_life = {}
            for hua_type, star_name in si_hua.items():
                if star_name in stars_in_life_palace:
                    si_hua_in_life[hua_type] = star_name
            
            # 12. 主星 (MajorStar enum)
            primary_star = self._get_major_star_enum(stars_in_life_palace[0] if stars_in_life_palace else "紫微")
            
            # 13. 五行分布
            element_dist = self._calculate_element_distribution(
                year_pillar, month_pillar, day_pillar, hour_pillar
            )
            
            # 14. 日主五行
            day_stem = day_pillar[0] if day_pillar else "甲"
            inherent_element = self.STEM_ELEMENTS.get(day_stem, Element.WOOD)

            return FateProfile(
                birth_datetime=birth_datetime,
                lunar_year=lunar.getYear(),
                lunar_month=lunar_month,
                lunar_day=lunar_day,
                lunar_hour=hour_idx,
                year_stem_branch=year_pillar,
                month_stem_branch=month_pillar,
                day_stem_branch=day_pillar,
                hour_stem_branch=hour_pillar,
                major_star=primary_star,
                life_palace=f"命宮在{life_palace_branch}",
                inherent_element=inherent_element,
                element_distribution=element_dist,
                extra_data={
                    "life_palace_branch": life_palace_branch,
                    "life_palace_idx": life_palace_idx,
                    "wu_xing_ju": ju_name,
                    "bureau": bureau,
                    "zi_wei_position": self.BRANCHES[zi_wei_idx],
                    "tian_fu_position": self.BRANCHES[tian_fu_idx],
                    "all_major_stars": stars_in_life_palace,
                    "star_positions": {k: self.BRANCHES[v] for k, v in star_positions.items()},
                    "si_hua": si_hua,
                    "si_hua_in_life": si_hua_in_life,
                }
            )

        except Exception as e:
            if isinstance(e, (InvalidBirthDataError, CalendarConversionError)):
                raise
            raise CalendarConversionError(
                message=f"Failed to calculate fate: {str(e)}",
                details={"birth_datetime": str(birth_datetime)},
            )

    def _get_hour_index(self, hour: int) -> int:
        """Convert 24-hour to 時辰 index (0=子, 1=丑, ...)"""
        if hour == 23:
            return 0
        return ((hour + 1) // 2) % 12

    def _get_major_star_enum(self, star_name: str) -> MajorStar:
        """Convert star name to MajorStar enum."""
        mapping = {
            "紫微": MajorStar.ZI_WEI, "天機": MajorStar.TIAN_JI,
            "太陽": MajorStar.TAI_YANG, "武曲": MajorStar.WU_QU,
            "天同": MajorStar.TIAN_TONG, "廉貞": MajorStar.LIAN_ZHEN,
            "天府": MajorStar.TIAN_FU, "太陰": MajorStar.TAI_YIN,
            "貪狼": MajorStar.TAN_LANG, "巨門": MajorStar.JU_MEN,
            "天相": MajorStar.TIAN_XIANG, "天梁": MajorStar.TIAN_LIANG,
            "七殺": MajorStar.QI_SHA, "破軍": MajorStar.PO_JUN,
        }
        return mapping.get(star_name, MajorStar.ZI_WEI)

    def _calculate_element_distribution(self, *pillars) -> dict:
        """Calculate element distribution from pillars."""
        distribution = {e: 0 for e in Element}
        for pillar in pillars:
            if len(pillar) >= 2:
                stem, branch = pillar[0], pillar[1]
                if stem in self.STEM_ELEMENTS:
                    distribution[self.STEM_ELEMENTS[stem]] += 1
                if branch in self.BRANCH_ELEMENTS:
                    distribution[self.BRANCH_ELEMENTS[branch]] += 1
        return distribution

    def _validate_birth_datetime(self, dt: datetime) -> None:
        """Validate birth datetime."""
        if dt.year < 1900:
            raise InvalidBirthDataError(message="Birth year must be 1900 or later")
        if dt > datetime.now():
            raise InvalidBirthDataError(message="Birth date cannot be in the future")

    def get_star_description(self, star: MajorStar, extra_data: dict = None) -> dict:
        """Get star description with roast."""
        descriptions = {
            MajorStar.ZI_WEI: {"name": "紫微", "english": "Emperor Star", "roast": "Control freak with a God complex."},
            MajorStar.TIAN_JI: {"name": "天機", "english": "Heavenly Secret", "roast": "Overthinks ordering coffee."},
            MajorStar.TAI_YANG: {"name": "太陽", "english": "Sun Star", "roast": "Everyone's sunshine, nobody's priority."},
            MajorStar.WU_QU: {"name": "武曲", "english": "Warrior Star", "roast": "You trust money more than people. Smart."},
            MajorStar.TIAN_TONG: {"name": "天同", "english": "Heavenly Unity", "roast": "Allergic to conflict."},
            MajorStar.LIAN_ZHEN: {"name": "廉貞", "english": "Chastity Star", "roast": "Drama follows you like a loyal dog."},
            MajorStar.TIAN_FU: {"name": "天府", "english": "Heavenly Treasury", "roast": "Security is your religion."},
            MajorStar.TAI_YIN: {"name": "太陰", "english": "Moon Star", "roast": "Trust issues are just pattern recognition."},
            MajorStar.TAN_LANG: {"name": "貪狼", "english": "Greedy Wolf", "roast": "You want to be a monk and a billionaire. Same time."},
            MajorStar.JU_MEN: {"name": "巨門", "english": "Giant Gate", "roast": "Truth-teller or troublemaker? Line is thin."},
            MajorStar.TIAN_XIANG: {"name": "天相", "english": "Heavenly Minister", "roast": "Professional people-pleaser."},
            MajorStar.TIAN_LIANG: {"name": "天梁", "english": "Heavenly Beam", "roast": "Everyone's therapist, nobody's patient."},
            MajorStar.QI_SHA: {"name": "七殺", "english": "Seven Killings", "roast": "Born rebel. Authority is just a suggestion."},
            MajorStar.PO_JUN: {"name": "破軍", "english": "Army Breaker", "roast": "You leave a trail of chaos and call it progress."},
        }
        return descriptions.get(star, descriptions[MajorStar.ZI_WEI])
