# DeepSeek v3 FastAPI 流式对话服务

这是一个使用 FastAPI 和 DeepSeek v3 模型构建的流式对话服务。

## 功能特点

- 使用 FastAPI 构建的 RESTful API
- 支持流式输出（Server-Sent Events）
- 使用 DeepSeek v3 模型进行对话生成

## 安装依赖

```bash
pip install "volcengine-python-sdk[ark]" fastapi "uvicorn[standard]"
```

## 环境变量设置

需要设置以下环境变量：

```bash
export ARK_API_KEY=your_api_key_here
```

## 运行服务

```bash
uvicorn l_0419.21:app --reload
```

## API 使用示例

使用 curl 发送请求：

```bash
curl -N -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"你好"}]}' http://localhost:8000/chat
```