import requests
import json

url = "http://localhost:11434/api/generate"
data = {
    "model": "qwen3:1.7b",
    "prompt": "你是谁",
    "stream": False
}

response = requests.post(url, json=data)
result = response.json()
print(result)
print(result['response'])
