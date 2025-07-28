# kimi_request.py

import os
import requests
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取 API Key
KIMI_API_KEY = os.getenv("KIMI_API_KEY")
if not KIMI_API_KEY:
    raise ValueError("❌ 请在 .env 文件中设置 KIMI_API_KEY")

# Kimi 云端 API 地址
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"

# 请求头
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {KIMI_API_KEY}"
}

def call_kimi(prompt: str, model="moonshot-v1-32k", temperature=0.7) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "stream": False
    }

    try:
        response = requests.post(KIMI_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"].strip()

        # 如果输出中包含“不确定”或“未提及”，触发补充提示
        if any(term in result for term in ["不确定", "未提及", "无法判断"]):
            followup = prompt + "\n\n请在已有基础上尝试提供进一步判断，必要时参考数据泄露场景下的风险，并给出更清晰的判断结论。"
            payload["messages"] = [{"role": "user", "content": followup}]
            response = requests.post(KIMI_API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"].strip()

        return result

    except requests.exceptions.HTTPError as e:
        return f"❌ HTTP 错误：{e} - {response.text}"
    except Exception as e:
        return f"❌ 其他错误：{str(e)}"
