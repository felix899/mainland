# URL 結構遷移指南

## 新的 URL 結構

此更新將套票的 URL 從基於 ID 的結構改為基於 slug 的階層式結構。

### 舊的 URL 結構
```
/packages/                     # 套票列表
/packages/123/                 # 套票詳情（使用 ID）
```

### 新的 URL 結構
```
/packages/                                  # 所有套票列表
/packages/japan/                           # 日本的所有套票
/packages/japan/okinawa/                   # 沖繩的所有套票
/packages/japan/okinawa/beginner-course/  # 具體套票詳情（使用 slug）
```

## 遷移步驟

### 1. 執行數據庫遷移
```bash
cd cms
python manage.py migrate main
```

### 2. 為現有數據添加 slug

您需要為現有的國家、城市和套票添加 slug 值。有兩種方法：

#### 方法 A：透過 Django Admin 手動添加
1. 登入 Django Admin
2. 編輯每個國家、城市和套票
3. 在 slug 欄位中輸入適當的英文代碼（會自動從英文名稱生成）

#### 方法 B：使用 Django Shell 批量添加
```bash
cd cms
python manage.py shell
```

然後執行以下 Python 代碼：

```python
from django.utils.text import slugify
from main.models import Country, City, Package

# 為所有國家添加 slug
for country in Country.objects.all():
    if not country.slug and country.name_en:
        country.slug = slugify(country.name_en)
        country.save()
        print(f"已設定 {country.name} 的 slug: {country.slug}")
    elif not country.slug:
        # 如果沒有英文名稱，使用拼音或手動設定
        print(f"警告：{country.name} 沒有英文名稱，請手動設定 slug")

# 為所有城市添加 slug
for city in City.objects.all():
    if not city.slug and city.name_en:
        city.slug = slugify(city.name_en)
        city.save()
        print(f"已設定 {city.name} 的 slug: {city.slug}")
    elif not city.slug:
        print(f"警告：{city.name} 沒有英文名稱，請手動設定 slug")

# 為所有套票添加 slug
for package in Package.objects.all():
    if not package.slug:
        # 嘗試從名稱生成 slug
        base_slug = slugify(package.name)
        if not base_slug:
            # 如果中文名稱無法生成 slug，使用 ID
            base_slug = f"package-{package.id}"
        
        # 確保 slug 唯一
        slug = base_slug
        counter = 1
        while Package.objects.filter(slug=slug, city=package.city).exclude(id=package.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        package.slug = slug
        package.save()
        print(f"已設定 {package.name} 的 slug: {package.slug}")

print("完成！")
```

### 3. 驗證設定

檢查所有模型都有 slug：

```python
from main.models import Country, City, Package

print("沒有 slug 的國家：", Country.objects.filter(slug='').count())
print("沒有 slug 的城市：", City.objects.filter(slug='').count())
print("沒有 slug 的套票：", Package.objects.filter(slug='').count())
```

## 注意事項

1. **Slug 唯一性**：
   - 國家的 slug 在全局範圍內必須唯一
   - 城市的 slug 在同一國家內必須唯一
   - 套票的 slug 在同一城市內必須唯一

2. **Slug 格式**：
   - 只能包含小寫字母、數字和連字符（-）
   - 建議使用英文，例如：`japan`、`okinawa`、`beginner-diving-course`

3. **SEO 友善**：
   - 使用描述性的 slug，有助於搜索引擎優化
   - 避免使用過長的 slug

4. **向後兼容**：
   - 如果需要保持舊的 ID 訪問方式，需要額外添加重定向規則

## 管理界面更新

Django Admin 已更新，現在會：
- 在列表中顯示 slug 欄位
- 在編輯表單中顯示 slug 欄位
- 自動從英文名稱生成 slug（prepopulated_fields）

## 模型變更摘要

### Country
- 新增：`slug` 欄位（SlugField, unique=True）
- 更新：`save()` 方法會自動從 `name_en` 生成 slug
- 更新：`get_absolute_url()` 使用新的 URL 結構

### City
- 新增：`slug` 欄位（SlugField）
- 更新：`unique_together` 包含 `['country', 'slug']`
- 更新：`save()` 方法會自動從 `name_en` 生成 slug
- 更新：`get_absolute_url()` 使用新的 URL 結構

### Package
- 新增：`slug` 欄位（SlugField）
- 更新：`unique_together` 包含 `['city', 'slug']`
- 更新：`save()` 方法會自動從 `name` 生成 slug
- 更新：`get_absolute_url()` 使用新的 URL 結構

## URL 路由更新

新增的 URL patterns：

```python
# 套票列表頁面
path('packages/', views.package_list, name='package_list')

# 按國家篩選套票列表
path('packages/<slug:country_slug>/', views.package_list_by_country, name='package_list_by_country')

# 按城市篩選套票列表
path('packages/<slug:country_slug>/<slug:city_slug>/', views.package_list_by_city, name='package_list_by_city')

# 套票詳情頁面
path('packages/<slug:country_slug>/<slug:city_slug>/<slug:package_slug>/', views.package_detail, name='package_detail')
```

## View 更新

新增的 views：
- `package_list_by_country(request, country_slug)` - 按國家篩選
- `package_list_by_city(request, country_slug, city_slug)` - 按城市篩選
- `package_detail(request, country_slug, city_slug, package_slug)` - 套票詳情（更新為使用 slug）

## 問題排查

### 問題：訪問套票詳情頁面時出現 404
**解決方案**：確保該套票及其相關的城市和國家都有正確的 slug 值。

### 問題：Slug 重複錯誤
**解決方案**：確保在同一範圍內（國家全局、城市內國家、套票內城市）slug 是唯一的。

### 問題：中文套票名稱無法生成 slug
**解決方案**：為套票手動設定英文 slug，或者使用描述性的英文短語。

## 範例

### 日本沖繩潛水套票範例

```python
# 創建國家
country = Country.objects.create(
    name="日本",
    name_en="Japan",
    slug="japan"  # 會自動從 name_en 生成
)

# 創建城市
city = City.objects.create(
    country=country,
    name="沖繩",
    name_en="Okinawa",
    slug="okinawa"  # 會自動從 name_en 生成
)

# 創建套票
package = Package.objects.create(
    city=city,
    name="初級潛水課程",
    slug="beginner-diving-course",  # 需要手動設定英文 slug
    package_type=package_type,
    # ... 其他欄位
)
```

訪問 URL：`/packages/japan/okinawa/beginner-diving-course/`

