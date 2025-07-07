import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def test_health():
    """测试API健康状态"""
    response = requests.get(f"{BASE_URL}/")
    print("健康检查:", response.json())
    return response.json()

def test_chat():
    """测试普通聊天接口"""
    data = {
        "messages": [
            {
                "image_url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg",
                "text": "这是哪里？"
            }
        ],
        "stream": False
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=data)
    print("普通聊天响应:", response.json())
    return response.json()

def test_stream_chat():
    """测试流式聊天接口"""
    data = {
        "messages": [
            {
                "image_url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg",
                "text": "这是哪里？"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/chat/stream", json=data, stream=True)
    print("流式聊天响应:")
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            if line_str.startswith('data: '):
                data_str = line_str[6:]  # 移除 'data: ' 前缀
                if data_str == '[DONE]':
                    break
                try:
                    data_json = json.loads(data_str)
                    print(data_json['content'], end='', flush=True)
                except json.JSONDecodeError:
                    continue
    print()  # 换行

if __name__ == "__main__":
    print("=== 测试方舟AI图像识别API ===\n")
    
    # 测试健康检查
    test_health()
    print()
    
    # 测试普通聊天
    test_chat()
    print()
    
    # 测试流式聊天
    test_stream_chat() 