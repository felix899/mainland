from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Prefetch
from django.conf import settings
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .models import Package, PackageType, City, Country, Continent, Period, Hotel, RoomType, RoomPrice, RoomImage, DailyItinerary, ItineraryImage

# Create your views here.

def package_list(request):
    """顯示所有套票的測試頁面"""
    packages = Package.objects.filter(is_active=True).select_related(
        'package_type', 'city', 'city__country', 'city__country__continent'
    ).prefetch_related(
        'tags',
        'periods',
        'periods__hotels',
        'periods__hotels__room_types',
        'periods__hotels__room_types__prices',
        'periods__hotels__room_types__images',
        'daily_itineraries',
        'daily_itineraries__images'
    )
    
    context = {
        'packages': packages,
        'total_count': packages.count(),
        'page_title': '所有套票'
    }
    return render(request, 'main/package_list.html', context)


def package_list_by_continent(request, continent_slug):
    """按大陸篩選套票列表"""
    continent = get_object_or_404(Continent, slug=continent_slug, is_active=True)
    packages = Package.objects.filter(
        is_active=True,
        city__country__continent=continent
    ).select_related(
        'package_type', 'city', 'city__country', 'city__country__continent'
    ).prefetch_related(
        'tags',
        'periods',
        'periods__hotels',
        'periods__hotels__room_types',
        'periods__hotels__room_types__prices',
        'periods__hotels__room_types__images',
        'daily_itineraries',
        'daily_itineraries__images'
    )
    
    context = {
        'packages': packages,
        'total_count': packages.count(),
        'continent': continent,
        'page_title': f'{continent.name} - 套票列表'
    }
    return render(request, 'main/package_list.html', context)


def package_list_by_country(request, continent_slug, country_slug):
    """按國家篩選套票列表"""
    continent = get_object_or_404(Continent, slug=continent_slug, is_active=True)
    country = get_object_or_404(Country, slug=country_slug, continent=continent, is_active=True)
    packages = Package.objects.filter(
        is_active=True,
        city__country=country
    ).select_related(
        'package_type', 'city', 'city__country', 'city__country__continent'
    ).prefetch_related(
        'tags',
        'periods',
        'periods__hotels',
        'periods__hotels__room_types',
        'periods__hotels__room_types__prices',
        'periods__hotels__room_types__images',
        'daily_itineraries',
        'daily_itineraries__images'
    )
    
    context = {
        'packages': packages,
        'total_count': packages.count(),
        'continent': continent,
        'country': country,
        'page_title': f'{country.name} ({continent.name}) - 套票列表'
    }
    return render(request, 'main/package_list.html', context)


def package_list_by_city(request, continent_slug, country_slug, city_slug):
    """按城市篩選套票列表"""
    continent = get_object_or_404(Continent, slug=continent_slug, is_active=True)
    country = get_object_or_404(Country, slug=country_slug, continent=continent, is_active=True)
    city = get_object_or_404(City, slug=city_slug, country=country, is_active=True)
    packages = Package.objects.filter(
        is_active=True,
        city=city
    ).select_related(
        'package_type', 'city', 'city__country', 'city__country__continent'
    ).prefetch_related(
        'tags',
        'periods',
        'periods__hotels',
        'periods__hotels__room_types',
        'periods__hotels__room_types__prices',
        'periods__hotels__room_types__images',
        'daily_itineraries',
        'daily_itineraries__images'
    )
    
    context = {
        'packages': packages,
        'total_count': packages.count(),
        'continent': continent,
        'country': country,
        'city': city,
        'page_title': f'{city.name} ({country.name}, {continent.name}) - 套票列表'
    }
    return render(request, 'main/package_list.html', context)


def package_detail(request, continent_slug, country_slug, city_slug, package_slug):
    """顯示單個套票詳情的測試頁面（使用 slug）"""
    continent = get_object_or_404(Continent, slug=continent_slug, is_active=True)
    country = get_object_or_404(Country, slug=country_slug, continent=continent, is_active=True)
    city = get_object_or_404(City, slug=city_slug, country=country, is_active=True)
    package = get_object_or_404(
        Package.objects.select_related('package_type', 'city', 'city__country', 'city__country__continent')
        .prefetch_related(
            'tags',
            'periods',
            'periods__hotels',
            'periods__hotels__room_types',
            'periods__hotels__room_types__prices',
            'periods__hotels__room_types__images',
            Prefetch('daily_itineraries', 
                     queryset=DailyItinerary.objects.filter(is_active=True).order_by('day_number', 'display_order')
                     .prefetch_related('images')),
        ),
        slug=package_slug,
        city=city,
        is_active=True
    )
    
    context = {
        'package': package,
        'continent': continent,
        'country': country,
        'city': city,
    }
    return render(request, 'main/package_detail.html', context)


def package_daily_itinerary_pdf(request, continent_slug, country_slug, city_slug, package_slug):
    """
    產生指定套票的「每天行程」PDF，提供桌機與手機下載使用。
    """
    continent = get_object_or_404(Continent, slug=continent_slug, is_active=True)
    country = get_object_or_404(Country, slug=country_slug, continent=continent, is_active=True)
    city = get_object_or_404(City, slug=city_slug, country=country, is_active=True)

    package = get_object_or_404(
        Package.objects.select_related('package_type', 'city', 'city__country', 'city__country__continent')
        .prefetch_related(
            Prefetch(
                'daily_itineraries',
                queryset=DailyItinerary.objects.filter(is_active=True).order_by('day_number', 'display_order')
                .prefetch_related('images'),
            ),
        ),
        slug=package_slug,
        city=city,
        is_active=True,
    )

    # 若沒有每天行程，回傳簡單提示 PDF
    daily_itineraries = list(package.daily_itineraries.all())

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    # ===== 註冊繁體中文字型（請確認字型檔路徑與檔名） =====
    # 你目前把字型放在：BASE_DIR / 'fonts' / 'NotoSansTC-Regular.ttf'
    font_path = settings.BASE_DIR / "fonts" / "NotoSansTC-Regular.ttf"
    try:
        pdfmetrics.registerFont(TTFont("NotoSansTC", str(font_path)))
        font_name = "NotoSansTC"
    except Exception:
        # 若註冊失敗則退回預設字型（英文正常，中文可能變方框）
        font_name = "Helvetica"

    styles = getSampleStyleSheet()
    # 使用自訂中文字型
    title_style = styles['Title']
    title_style.fontName = font_name
    subtitle_style = styles['Heading2']
    subtitle_style.fontName = font_name
    heading_style = styles['Heading3']
    heading_style.fontName = font_name
    body_style = styles['BodyText']
    body_style.fontName = font_name

    story = []

    # 標題
    story.append(Paragraph(f"{package.name}", title_style))
    if package.subtitle:
        story.append(Paragraph(str(package.subtitle), subtitle_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("每天行程", heading_style))
    story.append(Spacer(1, 12))

    if not daily_itineraries:
        story.append(Paragraph("此套票目前未設定每天行程。", body_style))
    else:
        for itinerary in daily_itineraries:
            day_title = f"第 {itinerary.day_number} 天：{itinerary.title}"
            story.append(Paragraph(day_title, heading_style))
            story.append(Spacer(1, 6))

            if itinerary.description:
                story.append(Paragraph(f"<b>行程描述：</b>{itinerary.description.replace('\n', '<br/>')}", body_style))
                story.append(Spacer(1, 4))

            # 餐食 / 住宿 / 交通
            if itinerary.meal_info:
                story.append(Paragraph(f"<b>餐食：</b>{itinerary.meal_info}", body_style))
            if itinerary.accommodation:
                story.append(Paragraph(f"<b>住宿：</b>{itinerary.accommodation}", body_style))
            if itinerary.transportation:
                story.append(Paragraph(f"<b>交通：</b>{itinerary.transportation}", body_style))

            if itinerary.meal_info or itinerary.accommodation or itinerary.transportation:
                story.append(Spacer(1, 4))

            if itinerary.notes:
                story.append(Paragraph(f"<b>備註：</b>{itinerary.notes.replace('\n', '<br/>')}", body_style))
                story.append(Spacer(1, 8))

            # 每天之間加上一些空白
            story.append(Spacer(1, 12))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()

    filename = f"{package.slug}_daily_itinerary.pdf"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response.write(pdf)
    return response
