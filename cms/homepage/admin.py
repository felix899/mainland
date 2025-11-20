from django.contrib import admin

from .models import HomepageSettings, HeroSlide


class HeroSlideInline(admin.TabularInline):
    model = HeroSlide
    extra = 1
    fields = ("order", "title", "link_url", "image", "is_active")
    ordering = ("order", "id")


@admin.register(HomepageSettings)
class HomepageSettingsAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    list_editable = ("is_active",)
    inlines = [HeroSlideInline]

    def has_add_permission(self, request):
        """
        限制後台最多只建立一筆首頁設定，避免編輯時混淆。
        若沒有任何記錄，允許新增；已有記錄時只允許編輯。
        """
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

