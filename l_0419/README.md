# 方舟AI图像识别API

基于火山引擎方舟的AI图像识别API服务，支持图像分析和对话功能。

## 功能特性

- 🖼️ 图像识别和分析
- 💬 支持多轮对话
- ⚡ 支持流式输出
- 🔧 RESTful API接口
- 📚 自动生成API文档

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务

```bash
python app.py
```

服务将在 `http://localhost:8000` 启动

## API接口

### 1. 健康检查
- **GET** `/`
- 返回服务状态信息

### 2. 普通聊天接口
- **POST** `/chat`
- 支持图像+文本的对话

请求体示例：
```json
{
  "messages": [
    {
      "image_url": "https://example.com/image.jpg",
      "text": "这张图片是什么？"
    }
  ],
  "stream": false
}
```

### 3. 流式聊天接口
- **POST** `/chat/stream`
- 支持实时流式输出

请求体示例：
```json
{
  "messages": [
    {
      "image_url": "https://example.com/image.jpg",
      "text": "这张图片是什么？"
    }
  ]
}
```

## 测试API

运行测试客户端：
```bash
python test_client.py
```

## API文档

启动服务后，访问以下地址查看自动生成的API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 使用示例

### Python客户端示例

```python
import requests

# 普通聊天
response = requests.post("http://localhost:8000/chat", json={
    "messages": [
        {
            "image_url": "https://example.com/image.jpg",
            "text": "这是什么地方？"
        }
    ],
    "stream": False
})
print(response.json())

# 流式聊天
response = requests.post("http://localhost:8000/chat/stream", json={
    "messages": [
        {
            "image_url": "https://example.com/image.jpg",
            "text": "这是什么地方？"
        }
    ]
}, stream=True)

for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        if line_str.startswith('data: '):
            data_str = line_str[6:]
            if data_str == '[DONE]':
                break
            print(data_str, end='', flush=True)
```

### cURL示例

```bash
# 普通聊天
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "image_url": "https://example.com/image.jpg",
        "text": "这是什么地方？"
      }
    ],
    "stream": false
  }'

# 流式聊天
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "image_url": "https://example.com/image.jpg",
        "text": "这是什么地方？"
      }
    ]
  }'
```

## 配置说明

在 `app.py` 中可以修改以下配置：
- `base_url`: 方舟API的基础URL
- `api_key`: 您的方舟API密钥
- `model`: 使用的模型名称

## 注意事项

1. 确保您的方舟API密钥有效且有足够的配额
2. 图片URL必须是可公开访问的
3. 建议在生产环境中使用环境变量管理API密钥
4. 流式接口适合长文本输出，普通接口适合短回复 