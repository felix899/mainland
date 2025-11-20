from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # 套票列表頁面
    path('packages/', views.package_list, name='package_list'),
    
    # 按大陸篩選套票列表
    path('packages/<slug:continent_slug>/', views.package_list_by_continent, name='package_list_by_continent'),
    
    # 按國家篩選套票列表
    path('packages/<slug:continent_slug>/<slug:country_slug>/', views.package_list_by_country, name='package_list_by_country'),
    
    # 按城市篩選套票列表
    path('packages/<slug:continent_slug>/<slug:country_slug>/<slug:city_slug>/', views.package_list_by_city, name='package_list_by_city'),
    
    # 套票詳情頁面（新的 slug 結構）
    path('packages/<slug:continent_slug>/<slug:country_slug>/<slug:city_slug>/<slug:package_slug>/', views.package_detail, name='package_detail'),

    # 每天行程 PDF 下載
    path(
        'packages/<slug:continent_slug>/<slug:country_slug>/<slug:city_slug>/<slug:package_slug>/daily-itinerary.pdf',
        views.package_daily_itinerary_pdf,
        name='package_daily_itinerary_pdf',
    ),
]


