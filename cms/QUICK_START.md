# 快速開始 - URL Slug 遷移

## 完成的更新

✅ **模型更新**：為 Country、City、Package 添加了 slug 欄位
✅ **URL 路由**：更新為階層式結構（國家/城市/套票）
✅ **視圖函數**：新增按國家和城市篩選的視圖
✅ **管理界面**：Admin 支持編輯和自動生成 slug
✅ **模板更新**：更新為使用新的 URL 結構

## 新的 URL 範例

```
/packages/                                  # 所有套票
/packages/japan/                           # 日本的套票
/packages/japan/okinawa/                   # 沖繩的套票
/packages/japan/okinawa/beginner-course/  # 具體套票
```

## 立即執行（重要）

### 1. 執行數據庫遷移
```bash
cd cms
python manage.py migrate main
```

### 2. 自動填充現有數據的 slug
```bash
cd cms
python populate_slugs.py
```

### 3. 檢查結果
1. 訪問 Django Admin
2. 檢查 Country、City、Package 的 slug 欄位
3. 訪問套票列表頁面測試

## 注意事項

- **國家和城市**需要有英文名稱（name_en）才能自動生成 slug
- **套票**會從名稱自動生成，中文名稱會使用 package-{id} 格式
- 所有 slug 在其範圍內（國家全局/城市內/套票內）必須唯一

## 需要更多信息？

查看 `cms/main/URL_MIGRATION_GUIDE.md` 獲取完整說明。

