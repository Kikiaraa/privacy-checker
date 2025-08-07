import os
import requests
import json

def call_zhipu(prompt):
    """
    调用智谱清言GLM-4 API
    """
    api_key = os.getenv("ZHIPU_API_KEY")
    if not api_key:
        raise ValueError("未设置 ZHIPU_API_KEY 环境变量")

    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "glm-4",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 2000,
        "temperature": 0.1,
        "top_p": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return "API 返回格式异常"
            
    except requests.exceptions.RequestException as e:
        return f"请求失败: {str(e)}"
    except KeyError as e:
        return f"解析响应失败: {str(e)}"