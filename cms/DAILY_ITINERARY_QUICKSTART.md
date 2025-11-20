# 每天行程功能快速開始

## 已完成的設定

✅ 資料庫模型已創建
- `DailyItinerary`（每天行程）
- `ItineraryImage`（行程相片）

✅ Django-Filer 已設定並整合

✅ Admin 管理介面已配置
- 支援在套票中直接編輯每天行程
- 支援拖曳上傳多張相片
- 自動生成縮圖預覽

✅ 資料庫遷移已應用

## 快速使用步驟

### 1. 啟動開發伺服器

```bash
cd cms
python manage.py runserver
```

### 2. 進入 Admin 後台

訪問 `http://127.0.0.1:8000/admin/`

### 3. 為套票添加每天行程

**方法 A：在套票編輯頁面中**
1. 選擇「套票」→ 選擇一個套票
2. 滾動到「每天行程」區塊
3. 點擊「新增每天行程」
4. 填寫資訊：
   - 天數：1
   - 標題：第一天：抵達與入住
   - 行程描述：（使用富文本編輯器）
   - 開始時間：14:00
   - 結束時間：18:00
   - 地點：度假村
   - 餐食資訊：晚餐
   - 住宿資訊：五星級度假村
   - 交通方式：專車接送
5. 在下方「行程相片」區塊：
   - 點擊「新增行程相片」
   - 點擊圖片欄位的「選擇」按鈕
   - 上傳或選擇圖片
   - 填寫相片說明
   - 勾選「是否為主要相片」
6. 儲存

**方法 B：直接管理**
1. 選擇「每天行程」
2. 點擊「新增每天行程」
3. 選擇所屬套票
4. 填寫其他資訊並儲存

### 4. 管理圖片資料夾（選用）

1. 進入「Filer」→「Folders」
2. 建立資料夾結構：
   ```
   - 套票圖片
     - 馬爾代夫
       - 第1天
       - 第2天
     - 沖繩
       - 第1天
       - 第2天
   ```
3. 在上傳圖片時選擇對應資料夾

## 主要功能特色

### 📅 完整的行程資訊
- 天數、標題、描述
- 開始/結束時間
- 地點和地址
- 餐食、住宿、交通資訊
- 備註說明

### 📷 強大的圖片管理
- 使用 Django-Filer 管理所有圖片
- 支援多張圖片（無限制）
- 自動生成縮圖
- 資料夾分類管理
- 圖片可重複使用
- 設定主要相片

### 🎯 易用的管理介面
- 巢狀內聯編輯
- 拖曳排序
- 即時預覽
- 批量操作
- 圖片縮圖顯示

### 🔄 複製功能
- 複製套票時自動複製所有行程
- 複製行程時自動複製所有相片
- 圖片使用參照，不佔用額外空間

## 在前端顯示

### 基本範例

在模板中使用：

```django
<!-- 顯示所有每天行程 -->
{% for itinerary in package.daily_itineraries.all %}
  {% if itinerary.is_active %}
  <div class="day-itinerary">
    <h3>第{{ itinerary.day_number }}天：{{ itinerary.title }}</h3>
    
    <!-- 主要相片 -->
    {% with featured=itinerary.images.filter.first %}
      {% if featured %}
      <img src="{{ featured.image.url }}" alt="{{ featured.caption }}">
      {% endif %}
    {% endwith %}
    
    <!-- 行程描述 -->
    <div>{{ itinerary.description|safe }}</div>
    
    <!-- 相片集 -->
    <div class="image-gallery">
      {% for img in itinerary.images.all %}
        {% if img.is_active %}
        <img src="{{ img.image.url }}" alt="{{ img.caption }}">
        {% endif %}
      {% endfor %}
    </div>
  </div>
  {% endif %}
{% endfor %}
```

### 使用縮圖

```django
{% load thumbnail %}

{% for img in itinerary.images.all %}
  <!-- 生成 400x300 的縮圖 -->
  <img src="{% thumbnail img.image 400x300 crop %}" alt="{{ img.caption }}">
{% endfor %}
```

## 資料結構

```
Package（套票）
  └── DailyItinerary（每天行程）
        ├── day_number: 1
        ├── title: "第一天：抵達"
        ├── description: "..."
        ├── start_time: "14:00"
        ├── end_time: "18:00"
        ├── location: "度假村"
        ├── meal_info: "晚餐"
        ├── accommodation: "五星級度假村"
        ├── transportation: "專車接送"
        └── ItineraryImage（行程相片）× N
              ├── image: FilerImageField
              ├── caption: "抵達度假村"
              ├── display_order: 0
              └── is_featured: True
```

## 常見問題

**Q: 可以上傳多少張相片？**
A: 沒有限制，但建議每個行程 3-10 張為佳。

**Q: 圖片會重複儲存嗎？**
A: 不會。Django-Filer 使用參照系統，同一張圖片可在多處使用。

**Q: 如何調整圖片顯示順序？**
A: 使用 `display_order` 欄位，數字越小越靠前。

**Q: 如何設定主要相片？**
A: 勾選 `is_featured`，系統會自動取消同一行程的其他主要相片。

**Q: 可以複製行程嗎？**
A: 複製套票時會自動複製所有行程和相片。

## 下一步

閱讀完整文檔：`DAILY_ITINERARY_GUIDE.md`

包含：
- 詳細的模型欄位說明
- 進階查詢範例
- 前端整合完整範例
- 最佳實踐建議
- 疑難排解

## 需要幫助？

- 檢查 Django 日誌：`python manage.py runserver`
- 執行系統檢查：`python manage.py check`
- 查看 Django-Filer 文檔：https://django-filer.readthedocs.io/

---

🎉 **恭喜！每天行程功能已準備就緒！**


