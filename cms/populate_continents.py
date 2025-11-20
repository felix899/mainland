#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速填充大陸數據的腳本
執行方式：python manage.py shell < populate_continents.py
或：python populate_continents.py
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

from main.models import Continent

def populate_continents():
    """填充基本的大陸數據"""
    
    continents_data = [
        {
            'name': '亞洲',
            'name_en': 'Asia',
            'slug': 'asia',
            'is_active': True,
        },
        {
            'name': '歐洲',
            'name_en': 'Europe',
            'slug': 'europe',
            'is_active': True,
        },
        {
            'name': '北美洲',
            'name_en': 'North America',
            'slug': 'north-america',
            'is_active': True,
        },
        {
            'name': '南美洲',
            'name_en': 'South America',
            'slug': 'south-america',
            'is_active': True,
        },
        {
            'name': '非洲',
            'name_en': 'Africa',
            'slug': 'africa',
            'is_active': True,
        },
        {
            'name': '大洋洲',
            'name_en': 'Oceania',
            'slug': 'oceania',
            'is_active': True,
        },
        {
            'name': '南極洲',
            'name_en': 'Antarctica',
            'slug': 'antarctica',
            'is_active': False,  # 默認禁用，因為較少潛水套票
        },
    ]
    
    print("開始填充大陸數據...")
    print("-" * 50)
    
    created_count = 0
    updated_count = 0
    
    for data in continents_data:
        continent, created = Continent.objects.get_or_create(
            slug=data['slug'],
            defaults=data
        )
        
        if created:
            print(f"[+] 創建：{continent.name} ({continent.name_en})")
            created_count += 1
        else:
            # 更新現有記錄
            for key, value in data.items():
                setattr(continent, key, value)
            continent.save()
            print(f"[*] 更新：{continent.name} ({continent.name_en})")
            updated_count += 1
    
    print("-" * 50)
    print(f"完成！創建了 {created_count} 個大陸，更新了 {updated_count} 個大陸。")
    print(f"總共有 {Continent.objects.count()} 個大陸。")
    print()
    print("下一步：")
    print("1. 進入管理後台：http://127.0.0.1:8000/admin/main/continent/")
    print("2. 為每個國家設置所屬大陸")
    print("3. 測試新的 URL 結構")

if __name__ == '__main__':
    populate_continents()

