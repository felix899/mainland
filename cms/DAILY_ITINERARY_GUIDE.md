# 每天行程功能使用指南

## 概述

此功能讓您可以為每個套票添加詳細的每天行程安排，並為每個行程添加多張相片。相片使用 Django-Filer 進行管理，提供強大的媒體管理功能。

## 資料模型結構

### 1. DailyItinerary（每天行程）

每天行程模型包含以下欄位：

#### 基本資訊
- **package**: 所屬套票（必填）
- **day_number**: 天數（必填），例如：1、2、3
- **title**: 行程標題（必填），例如：「抵達馬爾代夫」、「環島遊覽」
- **description**: 行程描述（必填），使用富文本編輯器

#### 時間資訊
- **start_time**: 開始時間（選填），例如：09:00
- **end_time**: 結束時間（選填），例如：17:00

#### 地點資訊
- **location**: 地點名稱（選填）
- **location_address**: 地點地址（選填）

#### 詳細資訊
- **meal_info**: 餐食資訊（選填），例如：「早餐、午餐、晚餐」
- **accommodation**: 住宿資訊（選填），例如：「五星級度假村」
- **transportation**: 交通方式（選填），例如：「專車接送」、「渡輪」
- **notes**: 備註說明（選填），使用富文本編輯器

#### 顯示設定
- **display_order**: 顯示順序（預設為 0），數字越小越靠前
- **is_active**: 是否啟用

### 2. ItineraryImage（行程相片）

行程相片模型使用 Django-Filer 管理圖片：

- **itinerary**: 所屬行程（必填）
- **image**: 行程相片（必填），使用 Django-Filer 的圖片選擇器
- **caption**: 相片說明（選填）
- **display_order**: 顯示順序（預設為 0）
- **is_featured**: 是否為主要相片（每個行程只能有一張主要相片）
- **is_active**: 是否啟用

## 在 Django Admin 中使用

### 方法一：在套票編輯頁面中直接添加

1. 進入 Django Admin 後台
2. 找到「套票」模組，點擊要編輯的套票
3. 滾動到「每天行程」區塊
4. 點擊「新增每天行程」
5. 填寫行程資訊：
   - 天數（例如：1）
   - 標題（例如：「第一天：抵達與入住」）
   - 行程描述（使用富文本編輯器）
   - 其他選填資訊
6. 在行程下方的「行程相片」區塊中：
   - 點擊「新增行程相片」
   - 點擊圖片欄位旁的「選擇」按鈕，使用 Django-Filer 選擇或上傳圖片
   - 填寫相片說明
   - 設定顯示順序
   - 勾選「是否為主要相片」（如果這是行程的主要相片）
7. 儲存套票

### 方法二：在每天行程管理頁面中添加

1. 進入 Django Admin 後台
2. 找到「每天行程」模組
3. 點擊「新增每天行程」
4. 選擇所屬套票
5. 填寫行程資訊
6. 在下方「行程相片」區塊中添加相片
7. 儲存

### 方法三：在行程相片管理頁面中添加

1. 進入 Django Admin 後台
2. 找到「行程相片」模組
3. 點擊「新增行程相片」
4. 選擇所屬行程
5. 選擇或上傳圖片
6. 填寫相片說明
7. 儲存

## Django-Filer 圖片管理功能

### 上傳新圖片

1. 在圖片欄位旁點擊「選擇」按鈕
2. 在彈出視窗中點擊「上傳」標籤
3. 點擊「選擇檔案」按鈕選擇圖片
4. 或直接拖曳圖片到上傳區域
5. 上傳完成後自動選擇該圖片

### 選擇已存在的圖片

1. 在圖片欄位旁點擊「選擇」按鈕
2. 在彈出視窗中瀏覽資料夾
3. 點擊想要使用的圖片
4. 點擊「選擇」按鈕

### 圖片資料夾管理

Django-Filer 支援建立資料夾來組織圖片：

1. 進入 Django Admin 後台
2. 找到「Filer」→「資料夾」
3. 可以建立多層資料夾結構
4. 建議為不同套票或行程建立專屬資料夾

## 在前端範本中使用

### 顯示所有每天行程

```django
{% for itinerary in package.daily_itineraries.all %}
  <div class="daily-itinerary">
    <h3>第{{ itinerary.day_number }}天：{{ itinerary.title }}</h3>
    
    {% if itinerary.start_time or itinerary.end_time %}
    <p class="time">
      {% if itinerary.start_time %}{{ itinerary.start_time }}{% endif %}
      {% if itinerary.end_time %} - {{ itinerary.end_time }}{% endif %}
    </p>
    {% endif %}
    
    {% if itinerary.location %}
    <p class="location">📍 {{ itinerary.location }}</p>
    {% endif %}
    
    <div class="description">
      {{ itinerary.description|safe }}
    </div>
    
    {% if itinerary.meal_info %}
    <p class="meal">🍽️ {{ itinerary.meal_info }}</p>
    {% endif %}
    
    {% if itinerary.accommodation %}
    <p class="accommodation">🏨 {{ itinerary.accommodation }}</p>
    {% endif %}
    
    {% if itinerary.transportation %}
    <p class="transportation">🚗 {{ itinerary.transportation }}</p>
    {% endif %}
    
    <!-- 顯示行程相片 -->
    {% if itinerary.images.all %}
    <div class="itinerary-images">
      {% for image in itinerary.images.all %}
        {% if image.is_active %}
        <div class="image-item {% if image.is_featured %}featured{% endif %}">
          <img src="{{ image.image.url }}" alt="{{ image.caption }}">
          {% if image.caption %}
          <p class="caption">{{ image.caption }}</p>
          {% endif %}
        </div>
        {% endif %}
      {% endfor %}
    </div>
    {% endif %}
  </div>
{% endfor %}
```

### 使用 easy-thumbnails 生成縮圖

```django
{% load thumbnail %}

{% for image in itinerary.images.all %}
  {% if image.is_active %}
  <div class="image-item">
    <!-- 生成 300x300 的縮圖 -->
    <img src="{% thumbnail image.image 300x300 crop %}" alt="{{ image.caption }}">
    
    <!-- 原始圖片連結 -->
    <a href="{{ image.image.url }}">查看原圖</a>
  </div>
  {% endif %}
{% endfor %}
```

### 只顯示主要相片

```django
{% for itinerary in package.daily_itineraries.all %}
  <div class="daily-itinerary">
    <h3>第{{ itinerary.day_number }}天：{{ itinerary.title }}</h3>
    
    <!-- 顯示主要相片 -->
    {% with featured_image=itinerary.images.filter|first %}
      {% if featured_image %}
      <img src="{{ featured_image.image.url }}" alt="{{ featured_image.caption }}">
      {% endif %}
    {% endwith %}
  </div>
{% endfor %}
```

## 資料庫查詢範例

### 取得套票的所有行程（按天數排序）

```python
itineraries = package.daily_itineraries.filter(is_active=True).order_by('day_number', 'display_order')
```

### 取得某個行程的所有啟用相片（按順序）

```python
images = itinerary.images.filter(is_active=True).order_by('display_order', 'created_at')
```

### 取得某個行程的主要相片

```python
featured_image = itinerary.images.filter(is_active=True, is_featured=True).first()
```

### 計算套票的總天數

```python
total_days = package.daily_itineraries.filter(is_active=True).count()
```

## 最佳實踐

1. **天數編號**: 建議使用連續數字（1, 2, 3...），避免跳號
2. **顯示順序**: 如果同一天有多個行程，使用 `display_order` 控制顯示順序
3. **主要相片**: 每個行程建議設定一張主要相片，用於縮略圖顯示
4. **圖片命名**: 在 Django-Filer 中為圖片使用有意義的名稱
5. **資料夾組織**: 為每個套票或目的地建立專屬資料夾
6. **圖片大小**: 建議上傳高解析度圖片，使用 easy-thumbnails 自動生成所需尺寸
7. **備註說明**: 善用 `notes` 欄位記錄特別注意事項

## 進階功能

### 複製套票時自動複製行程

在 `Package.copy_package()` 方法中添加複製行程的邏輯：

```python
# 在 models.py 的 Package.copy_package() 方法中添加
for itinerary in self.daily_itineraries.all():
    new_itinerary = DailyItinerary.objects.create(
        package=new_package,
        day_number=itinerary.day_number,
        title=itinerary.title,
        description=itinerary.description,
        start_time=itinerary.start_time,
        end_time=itinerary.end_time,
        location=itinerary.location,
        location_address=itinerary.location_address,
        meal_info=itinerary.meal_info,
        accommodation=itinerary.accommodation,
        transportation=itinerary.transportation,
        notes=itinerary.notes,
        display_order=itinerary.display_order,
        is_active=itinerary.is_active
    )
    # 複製相片（Django-Filer 的圖片會被參照，不會複製實體檔案）
    for image in itinerary.images.all():
        ItineraryImage.objects.create(
            itinerary=new_itinerary,
            image=image.image,
            caption=image.caption,
            display_order=image.display_order,
            is_featured=image.is_featured,
            is_active=image.is_active
        )
```

## 疑難排解

### 問題：無法上傳圖片

**解決方案**：
1. 檢查 `settings.py` 中的 `MEDIA_ROOT` 和 `MEDIA_URL` 設定
2. 確認媒體目錄有寫入權限
3. 檢查 `urls.py` 是否正確配置媒體文件服務

### 問題：縮圖無法顯示

**解決方案**：
1. 確認已安裝 `easy-thumbnails`
2. 檢查 `settings.py` 中的縮圖設定
3. 確認有 Pillow 套件

### 問題：多張主要相片

**解決方案**：
模型的 `save()` 方法已處理此問題，每次設定主要相片時會自動取消同一行程的其他主要相片。

## 相關文件

- [Django-Filer 官方文檔](https://django-filer.readthedocs.io/)
- [Easy Thumbnails 文檔](https://easy-thumbnails.readthedocs.io/)
- [CKEditor 文檔](https://django-ckeditor.readthedocs.io/)

## 更新日誌

- 2024-11-10: 初始版本，新增每天行程和相片管理功能


