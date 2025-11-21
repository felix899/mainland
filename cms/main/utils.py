import json
from typing import Optional, Tuple

import requests
from django.conf import settings


def generate_content_with_perplexity(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    呼叫 Perplexity AI API，依照提示詞產生內容。

    回傳 (content, error)：
        - 成功：("產生的文字內容", None)
        - 失敗：(None, "錯誤訊息")
    """
    api_key = getattr(settings, "PERPLEXITY_API_KEY", "") or ""
    model = getattr(settings, "PERPLEXITY_MODEL", "llama-3.1-sonar-small-128k-online")

    if not api_key:
        return None, "PERPLEXITY_API_KEY 未設定，請確認 settings.py 或環境變數。"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # 比照舊專案用途：為套餐描述產生繁體中文的說明
    system_prompt = (
        "你是一位專業的旅遊行程與度假套餐文案編輯，請使用繁體中文，語氣專業、自然、具吸引力。"
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        # 套票描述文字，一般 100–250 字即可，預留足夠空間
        "max_tokens": 800,
    }

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=60,
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # 儘量從回應內容中取出詳細錯誤訊息
            try:
                err_data = response.json()
                err_msg = (
                    err_data.get("error", {}).get("message")
                    or err_data.get("message")
                    or response.text
                )
            except Exception:
                err_msg = response.text or str(e)
            return None, f"HTTP {response.status_code}: {err_msg}"

        data = response.json()
        choices = data.get("choices") or []
        if not choices:
            return None, "API 回應中沒有 choices，請稍後再試。"

        message = choices[0].get("message") or {}
        content = message.get("content")
        if not isinstance(content, str):
            return None, "API 回應格式異常，無法取得文字內容。"
        return content.strip(), None
    except Exception as e:
        return None, f"呼叫 Perplexity API 時發生錯誤：{str(e)}"


