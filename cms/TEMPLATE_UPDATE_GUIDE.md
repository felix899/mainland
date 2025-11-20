# 模板和視圖更新指南

## 概述
本次更新同步了 views.py 和 package_detail.html 模板，以支援新的酒店/房型/價格/圖片結構。

## Views.py 更新

### 所有視圖函數都已更新
所有的套票查詢視圖現在都包含完整的預加載查詢，以優化性能：

```python
.prefetch_related(
    'tags',
    'periods',
    'periods__hotels',
    'periods__hotels__room_types',
    'periods__hotels__room_types__prices',
    'periods__hotels__room_types__images'
)
```

### 更新的視圖函數：
1. `package_list()` - 所有套票列表
2. `package_list_by_continent()` - 按大陸篩選
3. `package_list_by_country()` - 按國家篩選
4. `package_list_by_city()` - 按城市篩選
5. `package_detail()` - 套票詳情頁面

## Package_detail.html 模板更新

### 新的顯示結構

模板現在以清晰的層級結構顯示所有資訊：

#### 層級 1: 期間 (Period)
```html
📅 第1天、第2天...
```
- 顯示期間文字
- 橙色邊框容器

#### 層級 2: 酒店 (Hotel)
```html
🏨 酒店名稱
```
- 顯示酒店名稱
- 灰色背景容器

#### 層級 3: 房型 (RoomType)
```html
🛏️ 房型名稱
```
- 顯示房型名稱
- 白色背景，左側橙色邊框

#### 層級 4A: 房間圖片 (RoomImage)
- 響應式網格布局（最小 200px 寬度）
- 圖片高度 150px
- 可點擊放大查看
- 顯示圖片說明

#### 層級 4B: 房間價格 (RoomPrice)
```html
💰 價格：
價格金額 | 價格說明（例如：旺季、淡季）
```
- 金色高亮背景
- 顯示價格和說明
- 垂直排列多個價格

### 樣式特點

1. **視覺層級清晰**
   - 使用不同背景色區分層級
   - Emoji 圖標增強識別度
   - 適當的間距和邊框

2. **響應式設計**
   - 圖片使用網格布局
   - 自動適應不同螢幕寬度

3. **互動功能**
   - 點擊圖片可在新分頁開啟
   - 滑鼠懸停效果

4. **空狀態處理**
   - 無酒店：顯示「此期間暫無酒店資訊」
   - 無房型：顯示「此酒店暫無房型資訊」
   - 無價格：顯示「暫無價格資訊」

### 顏色方案

| 元素 | 顏色 | 用途 |
|------|------|------|
| 期間標題 | `#fbb700` | 主要強調色 |
| 期間邊框 | `#fbb700` | 區塊邊界 |
| 酒店標題 | `#f17431` | 次要強調色 |
| 酒店背景 | `#f9f9f9` | 淺灰色背景 |
| 房型背景 | `white` | 白色背景 |
| 房型左邊框 | `#fbb700` | 視覺引導 |
| 價格背景 | `#fffbf0` | 淡黃色高亮 |
| 價格邊框 | `#fbb700` | 價格框線 |
| 價格金額 | `#f17431` | 價格文字 |

## 範例顯示結構

### 單一完整範例
```
📅 第1天

  🏨 海濱度假村
  
    🛏️ 標準房
    
      [圖片1] [圖片2] [圖片3]
      
      💰 價格：
      TWD 5,000 | 淡季價格
      TWD 8,000 | 旺季價格
      TWD 6,500 | 週末價格
    
    🛏️ 豪華海景房
    
      [圖片1] [圖片2]
      
      💰 價格：
      TWD 10,000 | 淡季價格
      TWD 15,000 | 旺季價格
```

## 資料流程

```
View (views.py)
  └─ prefetch_related() 預加載所有相關資料
      └─ Template (package_detail.html)
          └─ 使用嵌套迴圈顯示層級結構
              1. {% for period in package.periods.all %}
              2.   {% for hotel in period.hotels.all %}
              3.     {% for room_type in hotel.room_types.all %}
              4.       {% for image in room_type.images.all %}
              5.       {% for price in room_type.prices.all %}
```

## 性能優化

### 使用 prefetch_related
避免 N+1 查詢問題，一次性加載所有相關資料：

```python
# ❌ 不好的做法（會產生大量查詢）
package.periods.all()  # 1次查詢
for period in periods:
    period.hotels.all()  # N次查詢
    
# ✅ 好的做法（只需要幾次查詢）
Package.objects.prefetch_related(
    'periods__hotels__room_types__prices',
    'periods__hotels__room_types__images'
)
```

## 活動狀態過濾

所有層級都支援 `is_active` 過濾：
- Period: `{% if period.is_active %}`
- Hotel: `{% if hotel.is_active %}`
- RoomType: `{% if room_type.is_active %}`
- RoomPrice: `{% if price.is_active %}`
- RoomImage: `{% if image.is_active %}`

## 測試建議

1. **建立測試資料**：
   - 創建包含多個期間的套票
   - 每個期間添加多個酒店
   - 每個酒店添加多個房型
   - 每個房型添加多個價格和圖片

2. **測試場景**：
   - 空狀態顯示是否正確
   - 圖片點擊放大功能
   - 響應式布局在不同螢幕寬度
   - 價格說明顯示
   - is_active 過濾是否正確

3. **效能測試**：
   - 檢查 Django Debug Toolbar 的查詢次數
   - 應該只有少量查詢（約 5-10 次）

## 相容性

- ✅ 支援沒有資料的情況（顯示提示訊息）
- ✅ 支援部分欄位為空（例如：無圖片、無價格說明）
- ✅ 向後相容舊資料
- ✅ 響應式設計支援手機、平板、桌面

## 未來擴展建議

1. **圖片畫廊**：可以加入 Lightbox 功能
2. **價格排序**：可以按價格高低排序顯示
3. **房型比較**：可以添加房型對比功能
4. **收藏功能**：可以讓用戶收藏喜歡的房型
5. **即時查詢**：整合 WhatsApp 直接查詢特定房型

