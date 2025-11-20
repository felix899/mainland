# Django 富文本編輯器使用範例
# 這個文件展示如何使用 CKEditor 富文本編輯器

"""
=== CKEditor 富文本編輯器功能 ===
"""

# 已實現的功能：
# 1. 基本文字格式化（粗體、斜體、底線等）
# 2. 段落和列表
# 3. 連結和錨點
# 4. 圖片上傳和插入
# 5. 表格創建和編輯
# 6. 字體和顏色設定
# 7. 特殊字符和表情符號
# 8. 源代碼編輯

"""
=== 在模型中的使用 ===
"""

# 1. RichTextField - 基本富文本編輯器
# from ckeditor.fields import RichTextField
# content = RichTextField(verbose_name="內容")

# 2. RichTextUploadingField - 支援圖片上傳的富文本編輯器
# from ckeditor_uploader.fields import RichTextUploadingField
# content = RichTextUploadingField(verbose_name="內容")

# 3. 使用不同的配置
# content = RichTextUploadingField(config_name='basic')  # 基本工具列
# content = RichTextUploadingField(config_name='table')  # 表格專用工具列
# content = RichTextUploadingField(config_name='default')  # 完整工具列

"""
=== 已更新的模型欄位 ===
"""

# Country 模型：
# - description: 國家描述（完整富文本編輯器）

# City 模型：
# - description: 城市描述（完整富文本編輯器）

# PackageType 模型：
# - description: 套票種類描述（完整富文本編輯器）
# - price_include_item: 價格包含項目（基本富文本編輯器）
# - price_exclude_item: 價格不包含項目（基本富文本編輯器）
# - flight_info: 航班信息（基本富文本編輯器）
# - tips: 小貼士（基本富文本編輯器）

# Package 模型：
# - description: 套票描述（完整富文本編輯器）
# - rich_text_table: 富文本表格（表格專用編輯器）

"""
=== 在模板中的顯示 ===
"""

template_example = """
<!-- 在 Django 模板中顯示富文本內容 -->
{% load static %}

<div class="package-description">
    {{ package.description|safe }}
</div>

<div class="package-table">
    {{ package.rich_text_table|safe }}
</div>

<!-- 如果需要自定義樣式 -->
<style>
    .package-description h1,
    .package-description h2,
    .package-description h3 {
        color: #2c3e50;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    .package-description table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    
    .package-description table th,
    .package-description table td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    
    .package-description table th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    
    .package-description img {
        max-width: 100%;
        height: auto;
        margin: 10px 0;
    }
</style>
"""

"""
=== CKEditor 配置說明 ===
"""

config_explanation = """
# CKEditor 配置檔位於 settings.py 中：

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 完整工具列
        'height': 300,
        'width': '100%',
        # 包含所有功能：格式化、連結、圖片、表格等
    },
    'basic': {
        'toolbar': 'Basic',  # 基本工具列
        'height': 200,
        'width': '100%',
        # 只包含基本格式化功能
    },
    'table': {
        'toolbar': 'Custom',  # 自定義工具列
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['Table', 'Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'height': 250,
        'width': '100%',
        # 專為表格編輯設計的工具列
    }
}
"""

"""
=== 在 Admin 中的使用 ===
"""

admin_usage = """
在 Django Admin 中，富文本欄位會自動顯示為 CKEditor 界面：

1. 文字格式化：選擇文字後使用工具列按鈕
2. 插入圖片：點擊圖片按鈕，可以上傳或選擇已有圖片
3. 創建表格：點擊表格按鈕，選擇行列數
4. 插入連結：選擇文字後點擊連結按鈕
5. 源代碼編輯：點擊 Source 按鈕查看/編輯 HTML 代碼

上傳的圖片會自動儲存在 MEDIA_ROOT/uploads/ 目錄中。
"""

"""
=== 安全注意事項 ===
"""

security_notes = """
使用富文本編輯器時需要注意：

1. 在模板中使用 |safe 過濾器時要小心 XSS 攻擊
2. 建議使用 bleach 套件來清理 HTML 內容
3. 限制上傳檔案的類型和大小
4. 定期檢查上傳的檔案內容

範例：
from django.utils.html import strip_tags
from bleach import clean

# 清理 HTML 內容
safe_content = clean(package.description, tags=['p', 'br', 'strong', 'em', 'img'])
"""

"""
=== 進階功能 ===
"""

advanced_features = """
可以進一步自定義 CKEditor：

1. 添加自定義插件
2. 修改工具列配置
3. 添加自定義樣式
4. 整合第三方服務（如 YouTube、Google Maps）

範例配置：
CKEDITOR_CONFIGS = {
    'advanced': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
            ['Find', 'Replace', '-', 'SelectAll', '-', 'Scayt'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],
            '/',
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl', 'Language'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe'],
            '/',
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'About']
        ],
        'height': 400,
        'width': '100%',
        'extraPlugins': 'codesnippet,widget,dialog',
        'codeSnippet_theme': 'monokai',
    }
}
"""

