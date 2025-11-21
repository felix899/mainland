from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from filer.fields.image import FilerImageField

# Create your models here.

class Continent(models.Model):
    """大陸模型"""
    name = models.CharField(max_length=100, verbose_name="大陸名稱")
    name_en = models.CharField(max_length=100, verbose_name="英文名稱", blank=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL 代碼", help_text="用於 URL 的英文代碼，例如：asia, europe", blank=True)
    description = RichTextUploadingField(verbose_name="大陸描述", blank=True, config_name='default')
    image = models.ImageField(upload_to='continents/', verbose_name="大陸圖片", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "大陸"
        verbose_name_plural = "大陸"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name_en:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:package_list_by_continent', kwargs={'continent_slug': self.slug})

class Country(models.Model):
    """國家模型"""
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE, verbose_name="所屬大陸", blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="國家名稱")
    name_en = models.CharField(max_length=100, verbose_name="英文名稱", blank=True)
    slug = models.SlugField(max_length=100, verbose_name="URL 代碼", help_text="用於 URL 的英文代碼，例如：japan, thailand", blank=True)
    description = RichTextUploadingField(verbose_name="國家描述", blank=True, config_name='default')
    image = models.ImageField(upload_to='countries/', verbose_name="國家圖片", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "國家"
        verbose_name_plural = "國家"
        ordering = ['name']
        unique_together = [['continent', 'name'], ['continent', 'slug']]

    def __str__(self):
        return f"{self.name} ({self.continent.name})" if self.continent else self.name
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name_en:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.continent:
            return reverse('main:package_list_by_country', kwargs={
                'continent_slug': self.continent.slug,
                'country_slug': self.slug
            })
        return reverse('main:package_list')

class Period(models.Model):
    """期間模型"""
    package = models.ForeignKey('Package', on_delete=models.CASCADE, verbose_name="所屬套票", related_name='periods')
    period_text = models.CharField(max_length=200, verbose_name="期間文字", help_text="例如：第1天、第2-3天等")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "期間"
        verbose_name_plural = "期間"
        ordering = ['package', 'period_text']

    def __str__(self):
        return f"{self.package.name} - {self.period_text}"


class Hotel(models.Model):
    """酒店模型"""
    period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name="所屬期間", related_name='hotels')
    hotel_name = models.CharField(max_length=200, verbose_name="酒店名稱")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "酒店"
        verbose_name_plural = "酒店"
        ordering = ['period', 'hotel_name']

    def __str__(self):
        return f"{self.hotel_name} ({self.period.period_text})"


class RoomType(models.Model):
    """房型模型"""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name="所屬酒店", related_name='room_types')
    room_type_name = models.CharField(max_length=100, verbose_name="房型名稱", help_text="例如：標準房、豪華房等")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "房型"
        verbose_name_plural = "房型"
        ordering = ['hotel', 'room_type_name']

    def __str__(self):
        return f"{self.hotel.hotel_name} - {self.room_type_name}"


class RoomPrice(models.Model):
    """房間價格模型"""
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name="所屬房型", related_name='prices')
    price = models.CharField(max_length=100, verbose_name="價格", help_text="房間價格")
    price_description = models.CharField(max_length=200, verbose_name="價格說明", blank=True, help_text="例如：旺季價格、淡季價格等")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "房間價格"
        verbose_name_plural = "房間價格"
        ordering = ['room_type', 'price']

    def __str__(self):
        description = f" ({self.price_description})" if self.price_description else ""
        return f"{self.room_type.room_type_name} - {self.price}{description}"


class RoomImage(models.Model):
    """房間圖片模型"""
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name="所屬房型", related_name='images')
    image = models.ImageField(upload_to='room_images/', verbose_name="房間圖片")
    image_description = models.CharField(max_length=200, verbose_name="圖片說明", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "房間圖片"
        verbose_name_plural = "房間圖片"
        ordering = ['room_type', 'created_at']

    def __str__(self):
        description = f" - {self.image_description}" if self.image_description else ""
        return f"{self.room_type.room_type_name}{description}"
class City(models.Model):
    """城市模型"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="所屬國家")
    name = models.CharField(max_length=100, verbose_name="城市名稱")
    name_en = models.CharField(max_length=100, verbose_name="英文名稱", blank=True)
    slug = models.SlugField(max_length=100, verbose_name="URL 代碼", help_text="用於 URL 的英文代碼，例如：okinawa, tokyo", blank=True)
    description = RichTextUploadingField(verbose_name="城市描述", blank=True, config_name='default')
    image = models.ImageField(upload_to='cities/', verbose_name="城市圖片", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = "城市"
        ordering = ['name']
        unique_together = [['country', 'name'], ['country', 'slug']]

    def __str__(self):
        return f"{self.name} ({self.country.name})"
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name_en:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.country and self.country.continent:
            return reverse('main:package_list_by_city', kwargs={
                'continent_slug': self.country.continent.slug,
                'country_slug': self.country.slug,
                'city_slug': self.slug
            })
        return reverse('main:package_list')


class PackageType(models.Model):
    """套票種類模型 - 簡單的分類標籤"""
    name = models.CharField(max_length=100, verbose_name="套票種類名稱", help_text="例如：潛水課程、船潛、岸潛等")
    icon = models.CharField(max_length=50, verbose_name="圖示", blank=True, help_text="使用 Font Awesome 圖示類別")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "套票種類"
        verbose_name_plural = "套票種類"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('package_type_detail', kwargs={'pk': self.pk})


class PackageTag(models.Model):
    """套票特色標籤模型"""
    name = models.CharField(max_length=50, verbose_name="標籤名稱")
    color = models.CharField(max_length=7, default="#007bff", verbose_name="標籤顏色", help_text="使用十六進位顏色代碼")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
 

    class Meta:
        verbose_name = "套票特色標籤"
        verbose_name_plural = "套票特色標籤"
        ordering = ['name']

    def __str__(self):
        return self.name


class Package(models.Model):
    """套票模型"""
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE, verbose_name="套票種類")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所屬城市", blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name="套票名稱")
    slug = models.SlugField(max_length=200, verbose_name="URL 代碼", help_text="用於 URL 的英文代碼，例如：beginner-diving-course", blank=True)
    subtitle = models.CharField(max_length=300, verbose_name="副標題", blank=True)
    description = RichTextUploadingField(verbose_name="套票描述", config_name='default')
    ai_prompt_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="AI 提示詞（描述）",
        help_text="輸入提示詞讓 AI 自動生成套票描述"
    )
    price = models.CharField(max_length=100, verbose_name="套票價格", blank=True, null=True)
    
    # 套票詳細資訊
    price_include_item = RichTextUploadingField(verbose_name="價格包含項目", blank=True, config_name='basic')
    price_exclude_item = RichTextUploadingField(verbose_name="價格不包含項目", blank=True, config_name='basic')
    price_vaild_date = models.DateField(verbose_name="價格有效日期", blank=True, null=True)
    flight_info = RichTextUploadingField(verbose_name="航班信息", blank=True, config_name='basic')
    tips = RichTextUploadingField(verbose_name="小貼士", blank=True, config_name='basic')
    
    # 特色標籤
    tags = models.ManyToManyField(PackageTag, verbose_name="套票特色", blank=True)
    
    # 圖片
    main_image = models.ImageField(upload_to='packages/', verbose_name="主要圖片")
    
    # 狀態
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    is_featured = models.BooleanField(default=False, verbose_name="是否精選")
    is_secondary_featured = models.BooleanField(
        default=False,
        verbose_name="是否為次要精選",
        help_text="選擇後會在首頁的次要精選區塊顯示",
    )
    
    # 時間戳記
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")
    
    # 富文本表格編輯器
    rich_text_table_one = RichTextUploadingField(
        verbose_name="價格表一", 
        blank=True, 
        null=True,
        config_name='table',
        help_text="使用富文本編輯器創建表格，支援圖片、連結等豐富內容"
    )
    
    # 富文本表格編輯器
    rich_text_table = RichTextUploadingField(
        verbose_name="價格表二", 
        blank=True, 
        null=True,
        config_name='table',
        help_text="使用富文本編輯器創建表格，支援圖片、連結等豐富內容"
    )

    rich_text_table_three = RichTextUploadingField(
        verbose_name="備用表格", 
        blank=True, 
        null=True,
        config_name='table',
        help_text="使用富文本編輯器創建表格，支援圖片、連結等豐富內容"
    )

    class Meta:
        verbose_name = "套票"
        verbose_name_plural = "套票"
        ordering = ['-created_at']
        unique_together = [['city', 'slug']]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # 自動生成 slug，如果沒有提供的話
            base_slug = slugify(self.name) if not self.name.isascii() else slugify(self.name)
            if not base_slug:
                base_slug = f"package-{self.pk or ''}"
            self.slug = base_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.city and self.city.country and self.city.country.continent:
            return reverse('main:package_detail', kwargs={
                'continent_slug': self.city.country.continent.slug,
                'country_slug': self.city.country.slug,
                'city_slug': self.city.slug,
                'package_slug': self.slug
            })
        return reverse('main:package_list')

    def get_discount_percentage(self):
        """計算折扣百分比"""
        if self.original_price and self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return round(discount, 0)
        return 0

    @property
    def country(self):
        """取得所屬國家"""
        return self.city.country if self.city else None
    
    def copy_package(self, new_name=None, new_slug=None):
        """複製套票"""
        # 創建新的套票實例
        new_package = Package(
            package_type=self.package_type,
            city=self.city,
            name=new_name or f"{self.name} (複製)",
            slug=new_slug or f"{self.slug}-copy" if self.slug else None,
            subtitle=self.subtitle,
            description=self.description,
            price=self.price,
            price_include_item=self.price_include_item,
            price_exclude_item=self.price_exclude_item,
            price_vaild_date=self.price_vaild_date,
            flight_info=self.flight_info,
            tips=self.tips,
            main_image=self.main_image,
            is_active=False,  # 複製的套票預設為非啟用狀態
            is_featured=False,  # 複製的套票預設為非精選
            is_secondary_featured=False,  # 複製的套票預設為非次要精選
            rich_text_table_one=self.rich_text_table_one,
            rich_text_table=self.rich_text_table,
            rich_text_table_three=self.rich_text_table_three,
        )
        new_package.save()
        
        # 複製標籤
        new_package.tags.set(self.tags.all())
        
        # 複製期間資訊
        for period in self.periods.all():
            new_period = Period.objects.create(
                package=new_package,
                period_text=period.period_text,
                is_active=period.is_active
            )
            # 複製酒店資訊
            for hotel in period.hotels.all():
                new_hotel = Hotel.objects.create(
                    period=new_period,
                    hotel_name=hotel.hotel_name,
                    is_active=hotel.is_active
                )
                # 複製房型資訊
                for room_type in hotel.room_types.all():
                    new_room_type = RoomType.objects.create(
                        hotel=new_hotel,
                        room_type_name=room_type.room_type_name,
                        is_active=room_type.is_active
                    )
                    # 複製價格資訊
                    for price in room_type.prices.all():
                        RoomPrice.objects.create(
                            room_type=new_room_type,
                            price=price.price,
                            price_description=price.price_description,
                            is_active=price.is_active
                        )
                    # 複製圖片資訊
                    for image in room_type.images.all():
                        RoomImage.objects.create(
                            room_type=new_room_type,
                            image=image.image,
                            image_description=image.image_description,
                            is_active=image.is_active
                        )
        
        # 複製每天行程資訊
        for itinerary in self.daily_itineraries.all():
            new_itinerary = DailyItinerary.objects.create(
                package=new_package,
                day_number=itinerary.day_number,
                title=itinerary.title,
                description=itinerary.description,
                meal_info=itinerary.meal_info,
                accommodation=itinerary.accommodation,
                transportation=itinerary.transportation,
                notes=itinerary.notes,
                display_order=itinerary.display_order,
                is_active=itinerary.is_active
            )
            # 複製行程相片（Django-Filer 的圖片會被參照，不會複製實體檔案）
            for image in itinerary.images.all():
                ItineraryImage.objects.create(
                    itinerary=new_itinerary,
                    image=image.image,
                    caption=image.caption,
                    display_order=image.display_order,
                    is_featured=image.is_featured,
                    is_active=image.is_active
                )
        
        return new_package


class DailyItinerary(models.Model):
    """每天行程模型"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name="所屬套票", related_name='daily_itineraries')
    day_number = models.PositiveIntegerField(verbose_name="天數", help_text="例如：1、2、3 等")
    title = models.CharField(max_length=200, verbose_name="行程標題", help_text="例如：抵達馬爾代夫、環島遊覽等")
    description = models.TextField(verbose_name="行程描述", help_text="詳細描述當天的活動安排")
    
    # 額外資訊
    meal_info = models.CharField(max_length=200, verbose_name="餐食資訊", blank=True, help_text="例如：早餐、午餐、晚餐")
    accommodation = models.CharField(max_length=200, verbose_name="住宿資訊", blank=True, help_text="當晚住宿地點")
    transportation = models.CharField(max_length=200, verbose_name="交通方式", blank=True, help_text="例如：專車接送、渡輪等")
    notes = models.TextField(verbose_name="備註說明", blank=True, help_text="其他重要事項或提醒")
    
    # 狀態
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    display_order = models.PositiveIntegerField(verbose_name="顯示順序", default=0, help_text="數字越小越靠前")
    
    # 時間戳記
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "每天行程"
        verbose_name_plural = "每天行程"
        ordering = ['package', 'day_number', 'display_order']
        unique_together = [['package', 'day_number']]

    def __str__(self):
        return f"{self.package.name} - 第{self.day_number}天：{self.title}"


class ItineraryImage(models.Model):
    """行程相片模型 - 使用 Django-Filer 管理"""
    itinerary = models.ForeignKey(DailyItinerary, on_delete=models.CASCADE, verbose_name="所屬行程", related_name='images')
    image = FilerImageField(
        on_delete=models.CASCADE,
        verbose_name="行程相片",
        related_name="itinerary_images",
        help_text="使用 Django-Filer 管理的相片"
    )
    caption = models.CharField(max_length=200, verbose_name="相片說明", blank=True, help_text="相片的簡短描述")
    display_order = models.PositiveIntegerField(verbose_name="顯示順序", default=0, help_text="數字越小越靠前")
    is_featured = models.BooleanField(default=False, verbose_name="是否為主要相片", help_text="每個行程可以設定一張主要相片")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    
    # 時間戳記
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "行程相片"
        verbose_name_plural = "行程相片"
        ordering = ['itinerary', 'display_order', 'created_at']

    def __str__(self):
        caption_text = f" - {self.caption}" if self.caption else ""
        return f"{self.itinerary.title} 相片{caption_text}"

    def save(self, *args, **kwargs):
        # 如果設為主要相片，則將同一行程的其他相片取消主要相片狀態
        if self.is_featured:
            ItineraryImage.objects.filter(
                itinerary=self.itinerary,
                is_featured=True
            ).exclude(pk=self.pk).update(is_featured=False)
        super().save(*args, **kwargs)
    
