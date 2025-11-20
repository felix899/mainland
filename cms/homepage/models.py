from django.db import models
from filer.fields.image import FilerImageField


class HomepageSettings(models.Model):
    """
    首頁設定：用來上傳首頁 Hero 圖片等設定。
    建議在後台只建立一筆資料，勾選「啟用」即可。
    """

    title = models.CharField("名稱", max_length=100, default="首頁設定")
    # 保留原本單一 hero_image 欄位（避免破壞既有資料）
    hero_image = FilerImageField(
        verbose_name="（舊）單一 Hero 圖片",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    is_active = models.BooleanField("啟用", default=True)

    class Meta:
        verbose_name = "首頁設定"
        verbose_name_plural = "首頁設定"

    def __str__(self) -> str:
        return self.title


class HeroSlide(models.Model):
    """
    首頁 Hero 輪播圖片。
    每一張圖片有標題與連結網址，可設定排序與啟用狀態。
    """

    settings = models.ForeignKey(
        HomepageSettings,
        verbose_name="首頁設定",
        on_delete=models.CASCADE,
        related_name="slides",
    )
    title = models.CharField("標題", max_length=200, blank=True)
    link_url = models.URLField("連結網址", blank=True)
    image = FilerImageField(
        verbose_name="圖片",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    order = models.PositiveIntegerField("排序", default=0)
    is_active = models.BooleanField("啟用", default=True)

    class Meta:
        verbose_name = "Hero 圖片"
        verbose_name_plural = "Hero 圖片"
        ordering = ["order", "id"]

    def __str__(self) -> str:
        base = self.title or "Hero 圖片"
        return f"{base} #{self.pk}" if self.pk else base

