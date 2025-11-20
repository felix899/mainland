# 大陸層級快速開始指南

## 🎯 新增功能概述

系統已成功添加「大陸」（Continent）層級！

**新的層級結構：**
```
🌏 大陸 (Continent)
  └── 🌍 國家 (Country)
      └── 📍 城市 (City)
          └── 📦 套票 (Package)
```

## 🚀 快速開始（3 步驟）

### 步驟 1：執行數據庫遷移

```bash
cd cms
python manage.py migrate
```

預期輸出：
```
Running migrations:
  Applying main.0012_continent_alter_country_slug_country_continent_and_more... OK
```

### 步驟 2：添加大陸數據

運行自動填充腳本：

```bash
cd cms
python populate_continents.py
```

這將自動創建 7 個大陸：
- ✅ 亞洲 (Asia)
- ✅ 歐洲 (Europe)
- ✅ 北美洲 (North America)
- ✅ 南美洲 (South America)
- ✅ 非洲 (Africa)
- ✅ 大洋洲 (Oceania)
- ⚪ 南極洲 (Antarctica) - 默認禁用

### 步驟 3：為國家分配大陸

**選項 A：使用自動腳本（推薦）**

```bash
cd cms
python assign_countries_to_continents.py
```

該腳本會自動為常見國家分配對應的大陸。

**選項 B：手動在管理後台設置**

1. 訪問：http://127.0.0.1:8000/admin/main/country/
2. 編輯每個國家
3. 選擇「所屬大陸」
4. 保存

## 📝 新的 URL 結構

### URL 示例

| 功能 | URL 格式 | 示例 |
|------|---------|------|
| 所有套票 | `/packages/` | http://127.0.0.1:8000/packages/ |
| 按大陸 | `/packages/<continent>/` | http://127.0.0.1:8000/packages/asia/ |
| 按國家 | `/packages/<continent>/<country>/` | http://127.0.0.1:8000/packages/asia/japan/ |
| 按城市 | `/packages/<continent>/<country>/<city>/` | http://127.0.0.1:8000/packages/asia/japan/okinawa/ |
| 套票詳情 | `/packages/<continent>/<country>/<city>/<package>/` | http://127.0.0.1:8000/packages/asia/japan/okinawa/diving-course/ |

### 在模板中使用

**舊的方式（已過時）：**
```django
{% url 'main:package_detail' country_slug city_slug package_slug %}
```

**新的方式：**
```django
{% url 'main:package_detail' continent_slug country_slug city_slug package_slug %}
```

或使用對象：
```django
{% url 'main:package_detail' 
    package.city.country.continent.slug 
    package.city.country.slug 
    package.city.slug 
    package.slug 
%}
```

## 🎨 管理後台新功能

### 大陸管理
- 路徑：`/admin/main/continent/`
- 功能：
  - 添加/編輯大陸
  - 設置大陸名稱（中英文）
  - 上傳大陸圖片
  - 編寫富文本描述
  - 啟用/禁用大陸

### 國家管理（已更新）
- 路徑：`/admin/main/country/`
- 新增：
  - 「所屬大陸」字段
  - 按大陸篩選國家
  - 按「大陸 → 國家」排序

### 套票管理（已更新）
- 路徑：`/admin/main/package/`
- 新增：
  - 按大陸篩選套票
  - 多層級篩選：大陸 → 國家 → 城市

## 🎯 前端顯示

套票列表頁面 (`package_list.html`) 現在會顯示：
- 🌏 大陸徽章（綠色）
- 🌍 國家徽章（紫色）
- 📍 城市徽章（藍色）

示例：
```
📦 沖繩潛水課程
[潛水課程] [📍 沖繩] [🌍 日本] [🌏 亞洲] [⭐ 精選]
```

## 🔧 技術細節

### 新增的模型字段

**Continent 模型：**
```python
- name (CharField): 大陸名稱
- name_en (CharField): 英文名稱
- slug (SlugField): URL 代碼
- description (RichTextField): 大陸描述
- image (ImageField): 大陸圖片
- is_active (BooleanField): 是否啟用
```

**Country 模型更新：**
```python
+ continent (ForeignKey): 所屬大陸（可選）
+ unique_together: [['continent', 'name'], ['continent', 'slug']]
```

### 新增的視圖

```python
def package_list_by_continent(request, continent_slug):
    """按大陸篩選套票列表"""
    # ...
```

### 數據庫查詢優化

所有視圖都使用 `select_related` 優化查詢：
```python
.select_related('package_type', 'city', 'city__country', 'city__country__continent')
```

## ⚠️ 注意事項

### 1. 向後兼容性
- `Country.continent` 字段為 `null=True, blank=True`
- 現有數據不會報錯，但需要盡快為所有國家分配大陸

### 2. URL 必須完整
確保每個套票的層級都完整：
```
套票 → 城市 → 國家 → 大陸
```

如果任何一層缺失，URL 將回退到基本列表頁。

### 3. Slug 唯一性
- 大陸的 slug 全局唯一
- 國家的 slug 在同一大陸內唯一
- 城市的 slug 在同一國家內唯一
- 套票的 slug 在同一城市內唯一

## 📊 檢查數據完整性

### 檢查未分配大陸的國家

在 Django shell 中：
```python
python manage.py shell

from main.models import Country
unassigned = Country.objects.filter(continent__isnull=True)
print(f"未分配大陸的國家: {unassigned.count()}")
for country in unassigned:
    print(f"  - {country.name}")
```

### 檢查數據統計

```python
from main.models import Continent, Country, City, Package

print(f"大陸數量: {Continent.objects.count()}")
print(f"國家數量: {Country.objects.count()}")
print(f"城市數量: {City.objects.count()}")
print(f"套票數量: {Package.objects.count()}")

# 按大陸統計國家
for continent in Continent.objects.all():
    count = Country.objects.filter(continent=continent).count()
    print(f"{continent.name}: {count} 個國家")
```

## 🐛 故障排除

### 問題 1：URL 無法訪問（404 錯誤）

**原因：** 國家未分配大陸

**解決：**
```bash
python assign_countries_to_continents.py
```

### 問題 2：套票詳情頁顯示「查看詳情」按鈕不可用

**原因：** 缺少 slug 或大陸關聯

**解決：**
1. 確保大陸有 slug
2. 確保國家已關聯大陸並有 slug
3. 確保城市有 slug
4. 確保套票有 slug

### 問題 3：遷移失敗

**錯誤示例：**
```
django.db.utils.IntegrityError: UNIQUE constraint failed
```

**解決：**
1. 檢查是否有重複的 slug
2. 刪除 `db.sqlite3` 並重新遷移（僅限測試環境）
3. 或手動修復重複數據

## 📚 相關文件

- **詳細指南：** `CONTINENT_MIGRATION_GUIDE.md`
- **模型定義：** `main/models.py`
- **URL 配置：** `main/urls.py`
- **視圖函數：** `main/views.py`
- **管理後台：** `main/admin.py`
- **填充腳本：**
  - `populate_continents.py` - 創建大陸
  - `assign_countries_to_continents.py` - 分配國家

## ✅ 驗證清單

完成以下步驟後，您的系統就完全配置好了：

- [ ] 執行數據庫遷移
- [ ] 運行 `populate_continents.py`
- [ ] 運行 `assign_countries_to_continents.py`（或手動分配）
- [ ] 檢查所有國家都已分配大陸
- [ ] 測試大陸列表 URL
- [ ] 測試國家列表 URL
- [ ] 測試城市列表 URL
- [ ] 測試套票詳情 URL
- [ ] 檢查套票列表頁面顯示正確
- [ ] 檢查管理後台功能正常

## 🎉 完成！

恭喜！您的潛水套票管理系統現在支持大陸層級了！

如有任何問題，請查看 `CONTINENT_MIGRATION_GUIDE.md` 獲取更詳細的信息。

