#!/usr/bin/env python3
"""
Test fate engine with detailed debug output.
Run: python3 test_fate.py
"""

from datetime import datetime
from qi_link.fate_engine import FateEngine

def debug_zi_wei_formula(day: int, bureau: int):
    """Debug the Zi Wei placement formula step by step."""
    YIN = 3  # 寅 = 3 (1-based)
    branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    print(f"\n【紫微安星 - Day {day}, {['','','水二','木三','金四','土五','火六'][bureau]}局】")
    
    quotient = day // bureau
    remainder = day % bureau
    
    print(f"  {day} / {bureau} = {quotient} 餘 {remainder}")
    
    if remainder == 0:
        position_1based = YIN + quotient - 1
        print(f"  整除: 寅({YIN}) + {quotient} - 1 = {position_1based}")
    else:
        add_on = bureau - remainder
        new_quotient = quotient + 1
        base_position = YIN + new_quotient - 1
        
        print(f"  補數={add_on}, 新商={new_quotient}, 基礎位置={base_position}")
        
        if new_quotient % 2 == 1:
            position_1based = base_position + add_on
            print(f"  奇數商順數: {base_position} + {add_on} = {position_1based}")
        else:
            position_1based = base_position - add_on
            print(f"  偶數商逆數: {base_position} - {add_on} = {position_1based}")
    
    position_0based = (position_1based - 1) % 12
    print(f"  紫微位置: {branches[position_0based]}")
    
    return position_0based


def verify_tian_fu_table():
    """Verify Tian Fu placement table."""
    print("\n" + "="*60)
    print("【天府對照表驗證 - 紫府同宮只在寅/申】")
    print("="*60)
    
    branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # Standard Tian Fu table
    tian_fu_map = {
        0: 4, 1: 3, 2: 2, 3: 1, 4: 0,
        5: 11, 6: 10, 7: 9, 8: 8, 9: 7, 10: 6, 11: 5
    }
    
    print("\n紫微位置 → 天府位置:")
    for zi_wei, tian_fu in tian_fu_map.items():
        same = " (紫府同宮!)" if zi_wei == tian_fu else ""
        print(f"  {branches[zi_wei]} → {branches[tian_fu]}{same}")

def test_birth(year, month, day, hour, minute=0, label=""):
    print(f"\n{'='*70}")
    print(f"【測試】 {label if label else f'{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}'}")
    print('='*70)
    
    engine = FateEngine()
    birth = datetime(year, month, day, hour, minute)
    fate = engine.calculate_fate(birth)
    extra = fate.extra_data
    
    print(f"\n【八字 Four Pillars】")
    print(f"  {fate.year_stem_branch} {fate.month_stem_branch} {fate.day_stem_branch} {fate.hour_stem_branch}")
    
    print(f"\n【農曆 Lunar】")
    print(f"  {fate.lunar_year}年 {fate.lunar_month}月 {fate.lunar_day}日")
    
    print(f"\n【命宮 Life Palace】")
    print(f"  {extra.get('life_palace_branch')}宮 (index: {extra.get('life_palace_idx')})")
    
    print(f"\n【五行局 Bureau】")
    print(f"  {extra.get('wu_xing_ju')} (數字: {extra.get('bureau')})")
    
    # Debug the Zi Wei calculation
    debug_zi_wei_formula(fate.lunar_day, extra.get('bureau', 3))
    
    print(f"\n【實際計算結果】")
    print(f"  紫微在: {extra.get('zi_wei_position')}宮")
    print(f"  天府在: {extra.get('tian_fu_position')}宮")
    
    print(f"\n【命宮主星】")
    stars = extra.get('all_major_stars', [])
    if stars:
        print(f"  {' + '.join(stars)}")
    else:
        print("  (空宮)")
    
    print(f"\n【年干四化】({fate.year_stem_branch[0]})")
    for hua, star in extra.get('si_hua', {}).items():
        in_life = " ← 在命宮!" if star in stars else ""
        print(f"  {star}{hua}{in_life}")
    
    print(f"\n【十四主星分布】")
    life_palace = extra.get('life_palace_branch')
    for star, pos in extra.get('star_positions', {}).items():
        marker = " ← 命宮" if pos == life_palace else ""
        print(f"  {star}: {pos}宮{marker}")

if __name__ == "__main__":
    print("="*70)
    print("Zi Wei Dou Shu Algorithm Test")
    print("="*70)
    
    # Verify Tian Fu table first
    verify_tian_fu_table()
    
    # Test a few days for 木三局 to verify pattern
    print("\n" + "="*70)
    print("Wood-3 Bureau Star Placement")
    print("="*70)
    for day in [1, 2, 3, 6, 9, 15, 17, 18]:
        debug_zi_wei_formula(day, 3)
    
    # Your birth date: 1993-01-09 00:30 (子時)
    test_birth(1993, 1, 9, 0, 30, "1993-01-09 Zi Hour (Your Birth)")
