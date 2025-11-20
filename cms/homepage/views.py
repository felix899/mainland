from django.shortcuts import render

from main.models import Package, Continent
from .models import HomepageSettings


def home_page_view(request):
    """
    首頁視圖
    顯示所有活動的套票和大陸資訊
    """
    # 獲取所有活動的套票
    packages = (
        Package.objects.filter(is_active=True, is_featured=True)
        .select_related(
            "package_type", "city", "city__country", "city__country__continent"
        )
        .prefetch_related("tags")[:6]  # 只顯示前 6 個套票
    )

    secondary_featured_packages = (
        Package.objects.filter(is_active=True, is_secondary_featured=True)
        .select_related(
            "package_type", "city", "city__country", "city__country__continent"
        )
        .prefetch_related("tags")
        .order_by("-updated_at", "-created_at")[:4]
    )

    # 獲取所有活動的大陸
    continents = Continent.objects.filter(is_active=True).order_by("name")

    # 讀取首頁設定與 Hero 輪播圖片
    settings_obj = (
        HomepageSettings.objects.filter(is_active=True)
        .prefetch_related("slides__image")
        .first()
    )
    hero_slides = []
    if settings_obj:
        hero_slides = settings_obj.slides.filter(
            is_active=True, image__isnull=False
        ).order_by("order", "id")

    context = {
        "packages": packages,
        "continents": continents,
        "secondary_featured_packages": secondary_featured_packages,
        "page_title": "首頁",
        "hero_slides": hero_slides,
    }
    return render(request, "homepage/home.html", context)

