import json

from django.contrib import admin
import nested_admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect, JsonResponse

from .models import (
    Continent,
    Country,
    City,
    PackageType,
    PackageTag,
    Package,
    Period,
    Hotel,
    RoomType,
    RoomPrice,
    RoomImage,
    DailyItinerary,
    ItineraryImage,
)
from .utils import generate_content_with_perplexity

# Register your models here.

@admin.register(Continent)
class ContinentAdmin(admin.ModelAdmin):
    """大陸管理界面"""
    list_display = ['name', 'name_en', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'name_en', 'slug']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name_en',)}
    ordering = ['name']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """國家管理界面"""
    list_display = ['name', 'continent', 'name_en', 'slug', 'is_active', 'created_at']
    list_filter = ['continent', 'is_active', 'created_at']
    search_fields = ['name', 'name_en', 'slug']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name_en',)}
    ordering = ['continent__name', 'name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """城市管理界面"""
    list_display = ['name', 'country', 'name_en', 'slug', 'is_active', 'created_at']
    list_filter = ['country', 'is_active', 'created_at']
    search_fields = ['name', 'name_en', 'slug', 'country__name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name_en',)}
    ordering = ['country__name', 'name']


@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    """套票種類管理界面"""
    list_display = ['name', 'icon', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']


@admin.register(PackageTag)
class PackageTagAdmin(admin.ModelAdmin):
    """套票特色標籤管理界面"""
    list_display = ['name', 'color', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['color', 'is_active']
    ordering = ['name']


@admin.register(Package)
class PackageAdmin(nested_admin.NestedModelAdmin):
    """套票管理界面"""
    change_form_template = "admin/main/package/change_form.html"
    list_display = ['name', 'slug', 'city', 'package_type', 'price', 'is_active', 'is_featured', 'is_secondary_featured', 'created_at', 'copy_package_link']
    list_filter = ['city__country__continent', 'city__country', 'city', 'package_type', 'is_active', 'is_featured', 'is_secondary_featured', 'created_at']
    search_fields = ['name', 'slug', 'subtitle', 'package_type__name', 'city__name', 'city__country__name']
    list_editable = ['price', 'is_active', 'is_featured', 'is_secondary_featured']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    filter_horizontal = ['tags']
    prepopulated_fields = {'slug': ('name',)}
    actions = ['copy_selected_packages']
    
    fieldsets = (
        ('基本資訊', {
            'fields': ('city', 'package_type', 'name', 'slug', 'subtitle', 'ai_prompt_description', 'description', 'price')
        }),
        ('圖片', {
            'fields': ('main_image',)
        }),
        ('詳細資訊', {
            'fields': ('price_include_item', 'price_exclude_item', 'flight_info', 'tips'),
            'description': '套票的詳細說明資訊'
        }),
        ('特色標籤', {
            'fields': ('tags',)
        }),
        ('價格表一', {
            'fields': ('rich_text_table_one',),
            'description': '使用富文本編輯器創建表格，支援圖片、連結等豐富內容'
        }),
        ('價格表二', {
            'fields': ('rich_text_table',),
            'description': '使用富文本編輯器創建表格，支援圖片、連結等豐富內容'
        }),
        ('行程表', {
            'fields': ('rich_text_table_three',),
            'description': '使用富文本編輯器創建表格，支援圖片、連結等豐富內容'
        }),
        ('狀態設定', {
            'fields': ('is_active', 'is_featured', 'is_secondary_featured')
        }),
        ('時間戳記', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = []
    
    def copy_package_link(self, obj):
        """複製套票連結"""
        if obj.pk:
            url = reverse('admin:main_package_copy', args=[obj.pk])
            return format_html(
                '<a class="button" href="{}" style="background-color: #28a745; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">複製套票</a>',
                url
            )
        return '-'
    copy_package_link.short_description = '複製套票'
    copy_package_link.allow_tags = True
    
    def copy_selected_packages(self, request, queryset):
        """批量複製選中的套票"""
        copied_count = 0
        for package in queryset:
            try:
                new_package = package.copy_package()
                copied_count += 1
            except Exception as e:
                self.message_user(request, f'複製套票 "{package.name}" 時發生錯誤: {str(e)}', level=messages.ERROR)
        
        if copied_count > 0:
            self.message_user(request, f'成功複製了 {copied_count} 個套票', level=messages.SUCCESS)
        else:
            self.message_user(request, '沒有套票被複製', level=messages.WARNING)
    
    copy_selected_packages.short_description = '複製選中的套票'
    
    def get_urls(self):
        """添加自定義URL"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:package_id>/copy/',
                self.admin_site.admin_view(self.copy_package_view),
                name='main_package_copy',
            ),
            path(
                '<int:package_id>/generate-ai-description/',
                self.admin_site.admin_view(self.generate_ai_description_view),
                name='main_package_generate_ai_description',
            ),
        ]
        return custom_urls + urls
    
    def copy_package_view(self, request, package_id):
        """複製套票視圖"""
        try:
            package = Package.objects.get(pk=package_id)
            new_package = package.copy_package()
            self.message_user(request, f'套票 "{package.name}" 已成功複製為 "{new_package.name}"', level=messages.SUCCESS)
            return HttpResponseRedirect(reverse('admin:main_package_change', args=[new_package.pk]))
        except Package.DoesNotExist:
            self.message_user(request, '套票不存在', level=messages.ERROR)
            return HttpResponseRedirect(reverse('admin:main_package_changelist'))
        except Exception as e:
            self.message_user(request, f'複製套票時發生錯誤: {str(e)}', level=messages.ERROR)
            return HttpResponseRedirect(reverse('admin:main_package_changelist'))

    def generate_ai_description_view(self, request, package_id):
        """
        處理 AI 自動生成套票描述的請求

        參考舊專案 sns.PackageAdmin.generate_ai_description_view 的行為，
        但改為使用 main.utils.generate_content_with_perplexity，並將詳細錯誤訊息回傳前端。
        """
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': '只接受 POST 請求'}, status=405)

        try:
            package = Package.objects.get(pk=package_id)
        except Package.DoesNotExist:
            return JsonResponse({'success': False, 'error': '找不到指定的套票'}, status=404)

        try:
            if request.body:
                data = json.loads(request.body)
                ai_prompt = (data.get('ai_prompt') or '').strip()
            else:
                return JsonResponse(
                    {'success': False, 'error': '請求資料為空'},
                    status=400,
                )
        except json.JSONDecodeError as e:
            return JsonResponse(
                {'success': False, 'error': f'無效的請求資料格式：{str(e)}'},
                status=400,
            )

        if not ai_prompt:
            return JsonResponse(
                {'success': False, 'error': '請先輸入 AI 提示詞'},
                status=400,
            )

        # 呼叫 Perplexity API
        generated_content, error = generate_content_with_perplexity(ai_prompt)

        if generated_content:
            package.description = generated_content
            package.save()
            return JsonResponse(
                {'success': True, 'content': generated_content},
                status=200,
            )

        # 失敗時將詳細錯誤訊息帶回前端，方便除錯
        return JsonResponse(
            {
                'success': False,
                'error': error or 'AI 生成內容失敗，請檢查 API 設定或稍後再試',
            },
            status=500,
        )


# ========== 嵌套 Inline 配置 ==========

# 第四層：房間價格和圖片 Inline
class RoomPriceInline(nested_admin.NestedStackedInline):
    """房間價格內聯"""
    model = RoomPrice
    extra = 1
    fieldsets = (
        ('價格資訊', {
            'fields': ('price', 'price_description', 'is_active')
        }),
    )
    classes = ['collapse']


class RoomImageInline(nested_admin.NestedStackedInline):
    """房間圖片內聯"""
    model = RoomImage
    extra = 1
    fieldsets = (
        ('圖片資訊', {
            'fields': ('image', 'image_description', 'is_active')
        }),
    )
    classes = ['collapse']


# 第三層：房型 Inline
class RoomTypeInline(nested_admin.NestedStackedInline):
    """房型內聯"""
    model = RoomType
    extra = 1
    fieldsets = (
        ('房型資訊', {
            'fields': ('room_type_name', 'is_active')
        }),
    )
    inlines = [RoomPriceInline, RoomImageInline]
    show_change_link = True
    classes = ['collapse']


# 第二層：酒店 Inline
class HotelInline(nested_admin.NestedStackedInline):
    """酒店內聯"""
    model = Hotel
    extra = 1
    fieldsets = (
        ('酒店資訊', {
            'fields': ('hotel_name', 'is_active')
        }),
    )
    inlines = [RoomTypeInline]
    show_change_link = True


# 第一層：期間 Inline
class PeriodInline(nested_admin.NestedStackedInline):
    """期間內聯"""
    model = Period
    extra = 1
    fieldsets = (
        ('期間資訊', {
            'fields': ('period_text', 'is_active')
        }),
    )
    inlines = [HotelInline]
    show_change_link = True


# ========== 獨立 Admin 配置 ==========

@admin.register(RoomPrice)
class RoomPriceAdmin(admin.ModelAdmin):
    """房間價格管理界面"""
    list_display = ['room_type', 'price', 'price_description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['room_type__room_type_name', 'price', 'price_description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['room_type', 'price']


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    """房間圖片管理界面"""
    list_display = ['room_type', 'image', 'image_description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['room_type__room_type_name', 'image_description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['room_type', 'created_at']


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    """房型管理界面"""
    list_display = ['room_type_name', 'hotel', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['room_type_name', 'hotel__hotel_name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['hotel', 'room_type_name']
    inlines = [RoomPriceInline, RoomImageInline]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """酒店管理界面"""
    list_display = ['hotel_name', 'period', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['hotel_name', 'period__period_text', 'period__package__name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['period', 'hotel_name']
    inlines = [RoomTypeInline]


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    """期間管理界面"""
    list_display = ['period_text', 'package', 'is_active', 'created_at']
    list_filter = ['package', 'is_active', 'created_at']
    search_fields = ['period_text', 'package__name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['package', 'period_text']
    fieldsets = (
        ('基本資訊', {
            'fields': ('package', 'period_text')
        }),
        ('狀態', {
            'fields': ('is_active',)
        }),
        ('時間戳記', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [HotelInline]


# ========== 每天行程管理配置 ==========

# 行程相片 Inline
class ItineraryImageInline(nested_admin.NestedTabularInline):
    """行程相片內聯"""
    model = ItineraryImage
    extra = 1
    fields = ('image', 'caption', 'display_order', 'is_featured', 'is_active')
    readonly_fields = []
    ordering = ['display_order', 'created_at']


# 每天行程 Inline（用於套票管理中）
class DailyItineraryInline(nested_admin.NestedStackedInline):
    """每天行程內聯"""
    model = DailyItinerary
    extra = 1
    fieldsets = (
        ('基本資訊', {
            'fields': ('day_number', 'title', 'description')
        }),
        ('詳細資訊', {
            'fields': ('meal_info', 'accommodation', 'transportation', 'notes'),
        }),
        ('顯示設定', {
            'fields': ('display_order', 'is_active'),
        }),
    )
    inlines = [ItineraryImageInline]


# 將期間資訊和每天行程作為套票的內聯編輯，實現完整的嵌套結構
PackageAdmin.inlines = [PeriodInline, DailyItineraryInline]
