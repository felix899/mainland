#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量為國家分配大陸的腳本
執行方式：python assign_countries_to_continents.py
"""

import os
import sys
import django

# 設置 Windows 控制台編碼
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 設置 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')
django.setup()

from django.db.models import Q
from main.models import Continent, Country

def assign_countries_to_continents():
    """為國家分配對應的大陸"""
    
    # 國家到大陸的映射（請根據實際情況調整）
    country_continent_mapping = {
        # 亞洲國家
        'asia': [
            '日本', 'Japan',
            '泰國', 'Thailand',
            '馬來西亞', 'Malaysia',
            '菲律賓', 'Philippines',
            '印尼', 'Indonesia',
            '越南', 'Vietnam',
            '新加坡', 'Singapore',
            '中國', 'China',
            '台灣', 'Taiwan',
            '韓國', 'South Korea',
            '印度', 'India',
            '馬爾地夫', 'Maldives',
            '斯里蘭卡', 'Sri Lanka',
        ],
        # 歐洲國家
        'europe': [
            '英國', 'United Kingdom',
            '法國', 'France',
            '德國', 'Germany',
            '意大利', 'Italy',
            '西班牙', 'Spain',
            '希臘', 'Greece',
            '葡萄牙', 'Portugal',
            '克羅地亞', 'Croatia',
            '挪威', 'Norway',
            '冰島', 'Iceland',
            '瑞士', 'Switzerland',
            '荷蘭', 'Netherlands',
        ],
        # 北美洲國家
        'north-america': [
            '美國', 'United States',
            '加拿大', 'Canada',
            '墨西哥', 'Mexico',
            '古巴', 'Cuba',
            '牙買加', 'Jamaica',
            '巴哈馬', 'Bahamas',
            '開曼群島', 'Cayman Islands',
        ],
        # 南美洲國家
        'south-america': [
            '巴西', 'Brazil',
            '阿根廷', 'Argentina',
            '智利', 'Chile',
            '秘魯', 'Peru',
            '哥倫比亞', 'Colombia',
            '厄瓜多爾', 'Ecuador',
        ],
        # 非洲國家
        'africa': [
            '埃及', 'Egypt',
            '南非', 'South Africa',
            '肯亞', 'Kenya',
            '坦桑尼亞', 'Tanzania',
            '摩洛哥', 'Morocco',
            '莫桑比克', 'Mozambique',
        ],
        # 大洋洲國家
        'oceania': [
            '澳大利亞', 'Australia',
            '新西蘭', 'New Zealand',
            '斐濟', 'Fiji',
            '帕勞', 'Palau',
            '巴布亞新幾內亞', 'Papua New Guinea',
            '密克羅尼西亞', 'Micronesia',
            '所羅門群島', 'Solomon Islands',
        ],
    }
    
    print("開始為國家分配大陸...")
    print("=" * 60)
    
    total_assigned = 0
    total_not_found = 0
    
    for continent_slug, country_names in country_continent_mapping.items():
        try:
            continent = Continent.objects.get(slug=continent_slug)
            print(f"\n[大陸] {continent.name} ({continent.name_en})")
            print("-" * 60)
            
            assigned_in_continent = 0
            
            for country_name in country_names:
                # 嘗試按名稱或英文名稱查找國家
                countries = Country.objects.filter(
                    Q(name=country_name) | Q(name_en=country_name)
                )
                
                if countries.exists():
                    for country in countries:
                        country.continent = continent
                        country.save()
                        print(f"  [+] {country.name} -> {continent.name}")
                        assigned_in_continent += 1
                        total_assigned += 1
                else:
                    print(f"  [!] 未找到：{country_name}")
                    total_not_found += 1
            
            print(f"  小計：分配了 {assigned_in_continent} 個國家")
            
        except Continent.DoesNotExist:
            print(f"\n[錯誤] 找不到大陸 '{continent_slug}'")
            print("   請先運行 populate_continents.py 創建大陸數據")
    
    print("\n" + "=" * 60)
    print(f"完成！")
    print(f"[+] 成功分配：{total_assigned} 個國家")
    print(f"[!] 未找到：{total_not_found} 個國家")
    
    # 檢查未分配大陸的國家
    unassigned_countries = Country.objects.filter(continent__isnull=True)
    if unassigned_countries.exists():
        print(f"\n[!] 還有 {unassigned_countries.count()} 個國家未分配大陸：")
        for country in unassigned_countries:
            print(f"   - {country.name} (ID: {country.id})")
        print("\n請手動在管理後台為這些國家分配大陸。")
    else:
        print("\n[完成] 所有國家都已分配大陸！")
    
    print("\n下一步：")
    print("1. 檢查管理後台的國家列表")
    print("2. 執行數據庫遷移（如果還沒執行）：python manage.py migrate")
    print("3. 測試新的 URL 結構")

if __name__ == '__main__':
    assign_countries_to_continents()

