# Django Free Format 表格使用範例
# 這個文件展示如何使用 JSONField 來存儲各種格式的表格資料

"""
=== 方案一：JSONField（已實現，推薦使用）===
"""

# 範例 1：價格表格
price_table_example = {
    "title": "套票價格表",
    "headers": ["房間種類", "佔半房", "單人房", "備註"],
    "rows": [
        {
            "room_type": "Bungalow Room",
            "half_room_price": "13,790",
            "single_room_price": "16,390",
            "note": "海景房"
        },
        {
            "room_type": "Deluxe Room",
            "half_room_price": "15,790",
            "single_room_price": "18,390",
            "note": "豪華房"
        }
    ],
    "currency": "TWD",
    "last_updated": "2024-01-15"
}

# 範例 2：行程安排表格
itinerary_table_example = {
    "title": "行程安排",
    "days": [
        {
            "day": 1,
            "date": "2024-02-01",
            "activities": [
                {"time": "09:00", "activity": "機場接機", "location": "機場"},
                {"time": "12:00", "activity": "午餐", "location": "酒店餐廳"},
                {"time": "15:00", "activity": "潛水裝備檢查", "location": "潛水中心"}
            ]
        },
        {
            "day": 2,
            "date": "2024-02-02",
            "activities": [
                {"time": "08:00", "activity": "早餐", "location": "酒店"},
                {"time": "09:30", "activity": "第一潛", "location": "珊瑚礁"},
                {"time": "14:00", "activity": "第二潛", "location": "沉船遺址"}
            ]
        }
    ]
}

# 範例 3：裝備清單表格
equipment_table_example = {
    "title": "裝備清單",
    "categories": [
        {
            "category": "基本裝備",
            "items": [
                {"name": "面鏡", "included": True, "note": "高品質矽膠面鏡"},
                {"name": "呼吸管", "included": True, "note": "乾式呼吸管"},
                {"name": "蛙鞋", "included": True, "note": "開放式蛙鞋"}
            ]
        },
        {
            "category": "安全裝備",
            "items": [
                {"name": "BCD", "included": True, "note": "自動充氣BCD"},
                {"name": "調節器", "included": True, "note": "雙管調節器"},
                {"name": "潛水錶", "included": False, "note": "可租借"}
            ]
        }
    ]
}

"""
=== 在 Django 中使用範例 ===
"""

def example_usage():
    """展示如何在 Django 中使用 Free Format 表格"""
    
    # 假設您有一個 Package 實例
    # package = Package.objects.get(id=1)
    
    # 設置價格表格
    # package.set_table_data(price_table_example)
    # package.save()
    
    # 添加單行資料
    # package.add_table_row({
    #     "room_type": "Suite Room",
    #     "half_room_price": "20,790",
    #     "single_room_price": "25,390",
    #     "note": "套房"
    # })
    # package.save()
    
    # 取得表格資料
    # table_data = package.get_table_data()
    # rows = package.get_table_rows()
    
    pass

"""
=== 其他方案（參考）===
"""

# 方案二：TextField + JSON 字符串
# 優點：相容性好，所有資料庫都支援
# 缺點：需要手動序列化/反序列化，查詢較困難

# 方案三：使用第三方套件 django-jsonfield
# 優點：功能豐富
# 缺點：需要額外安裝，增加依賴

# 方案四：創建關聯表
# 優點：結構化，查詢效率高
# 缺點：不夠靈活，需要預定義結構

"""
=== 在模板中顯示範例 ===
"""

template_example = """
<!-- 在 Django 模板中顯示價格表格 -->
{% if package.free_format_table %}
<div class="price-table">
    <h3>{{ package.free_format_table.title }}</h3>
    <table class="table">
        <thead>
            <tr>
                {% for header in package.free_format_table.headers %}
                <th>{{ header }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in package.free_format_table.rows %}
            <tr>
                <td>{{ row.room_type }}</td>
                <td>{{ row.half_room_price }}</td>
                <td>{{ row.single_room_price }}</td>
                <td>{{ row.note }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endif %}
"""

"""
=== 在 Admin 中的使用 ===
"""
admin_usage_example = """
在 Django Admin 中，JSONField 會自動提供一個 JSON 編輯器，
您可以：

1. 直接編輯 JSON 格式的資料
2. 使用提供的便利方法來操作表格
3. 在 Admin 界面中預覽表格內容

注意：建議在 Admin 中添加自定義 Widget 來提供更好的編輯體驗。
"""

