
import json
import requests


api_url = "http://localhost:1234/v1/completions"
headers = {"Content-Type": "application/json"}
data = {
    "model": "qwen3-8b",
    "prompt": "你是谁",
    # "max_tokens": 100,
    "temperature": 0.8,
    "stream": False
}

# 发送 POST 请求
response = requests.post(api_url, headers=headers, data=json.dumps(data))

# 解析响应
if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["text"])
