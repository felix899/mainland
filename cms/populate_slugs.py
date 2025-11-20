#!/usr/bin/env python
"""
為現有的 Country、City 和 Package 模型自動生成 slug 的腳本

使用方法：
    cd cms
    python populate_slugs.py
"""

import os
import sys
import django

# 設定 Django 環境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')
django.setup()

from django.utils.text import slugify
from main.models import Country, City, Package


def populate_country_slugs():
    """為所有國家添加 slug"""
    print("\n========== 處理國家 slug ==========")
    countries_updated = 0
    countries_need_manual = []
    
    for country in Country.objects.all():
        if country.slug:
            print(f"✓ {country.name} 已有 slug: {country.slug}")
            continue
            
        if country.name_en:
            country.slug = slugify(country.name_en)
            
            # 確保唯一性
            original_slug = country.slug
            counter = 1
            while Country.objects.filter(slug=country.slug).exclude(id=country.id).exists():
                country.slug = f"{original_slug}-{counter}"
                counter += 1
            
            country.save()
            print(f"✓ 已設定 {country.name} 的 slug: {country.slug}")
            countries_updated += 1
        else:
            countries_need_manual.append(country)
            print(f"⚠ 警告：{country.name} 沒有英文名稱，無法自動生成 slug")
    
    print(f"\n已更新 {countries_updated} 個國家的 slug")
    if countries_need_manual:
        print(f"需要手動設定 slug 的國家：{len(countries_need_manual)} 個")
        for country in countries_need_manual:
            print(f"  - {country.name} (ID: {country.id})")


def populate_city_slugs():
    """為所有城市添加 slug"""
    print("\n========== 處理城市 slug ==========")
    cities_updated = 0
    cities_need_manual = []
    
    for city in City.objects.all():
        if city.slug:
            print(f"✓ {city.name} ({city.country.name}) 已有 slug: {city.slug}")
            continue
            
        if city.name_en:
            city.slug = slugify(city.name_en)
            
            # 確保在同一國家內唯一
            original_slug = city.slug
            counter = 1
            while City.objects.filter(slug=city.slug, country=city.country).exclude(id=city.id).exists():
                city.slug = f"{original_slug}-{counter}"
                counter += 1
            
            city.save()
            print(f"✓ 已設定 {city.name} ({city.country.name}) 的 slug: {city.slug}")
            cities_updated += 1
        else:
            cities_need_manual.append(city)
            print(f"⚠ 警告：{city.name} ({city.country.name}) 沒有英文名稱，無法自動生成 slug")
    
    print(f"\n已更新 {cities_updated} 個城市的 slug")
    if cities_need_manual:
        print(f"需要手動設定 slug 的城市：{len(cities_need_manual)} 個")
        for city in cities_need_manual:
            print(f"  - {city.name} ({city.country.name}, ID: {city.id})")


def populate_package_slugs():
    """為所有套票添加 slug"""
    print("\n========== 處理套票 slug ==========")
    packages_updated = 0
    
    for package in Package.objects.all():
        if package.slug:
            city_name = package.city.name if package.city else "無城市"
            print(f"✓ {package.name} ({city_name}) 已有 slug: {package.slug}")
            continue
        
        # 嘗試從名稱生成 slug
        base_slug = slugify(package.name)
        
        # 如果中文名稱無法生成有效的 slug，使用 ID
        if not base_slug or base_slug == '':
            base_slug = f"package-{package.id}"
            print(f"⚠ {package.name} 的名稱無法生成 slug，使用 ID: {base_slug}")
        
        # 確保在同一城市內唯一
        slug = base_slug
        counter = 1
        while Package.objects.filter(slug=slug, city=package.city).exclude(id=package.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        package.slug = slug
        package.save()
        
        city_name = package.city.name if package.city else "無城市"
        print(f"✓ 已設定 {package.name} ({city_name}) 的 slug: {package.slug}")
        packages_updated += 1
    
    print(f"\n已更新 {packages_updated} 個套票的 slug")


def verify_slugs():
    """驗證所有模型都有 slug"""
    print("\n========== 驗證 slug ==========")
    
    countries_without_slug = Country.objects.filter(slug='').count()
    cities_without_slug = City.objects.filter(slug='').count()
    packages_without_slug = Package.objects.filter(slug='').count()
    
    total_countries = Country.objects.count()
    total_cities = City.objects.count()
    total_packages = Package.objects.count()
    
    print(f"國家：{total_countries - countries_without_slug}/{total_countries} 已有 slug")
    print(f"城市：{total_cities - cities_without_slug}/{total_cities} 已有 slug")
    print(f"套票：{total_packages - packages_without_slug}/{total_packages} 已有 slug")
    
    if countries_without_slug == 0 and cities_without_slug == 0 and packages_without_slug == 0:
        print("\n✓ 所有模型都已有 slug！")
        return True
    else:
        print("\n⚠ 仍有模型缺少 slug，請檢查上述輸出")
        return False


def main():
    """主函數"""
    print("========================================")
    print("    自動填充 Slug 腳本")
    print("========================================")
    
    try:
        populate_country_slugs()
        populate_city_slugs()
        populate_package_slugs()
        
        if verify_slugs():
            print("\n========== 完成 ==========")
            print("所有 slug 已成功生成！")
            print("\n下一步：")
            print("1. 檢查 Django Admin 確認 slug 是否正確")
            print("2. 訪問套票列表頁面測試新的 URL 結構")
            print("3. 如有需要，在 Admin 中手動調整 slug")
        else:
            print("\n========== 注意 ==========")
            print("部分模型仍缺少 slug，請在 Django Admin 中手動設定")
    
    except Exception as e:
        print(f"\n錯誤：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

