# main.py
import os
from typing import List, AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# ✅ 依赖：pip install "volcengine-python-sdk[ark]" fastapi "uvicorn[standard]"
from volcenginesdkarkruntime import AsyncArk   # 官方异步客户端

API_KEY = os.getenv("ARK_API_KEY")            # export ARK_API_KEY=xxx
MODEL_ID = "deepseek-v3"                      # 也可以替换为你创建的 Endpoint ID

if not API_KEY:
    raise RuntimeError("请先在环境变量中设置 ARK_API_KEY")

ark = AsyncArk(api_key=API_KEY)
app = FastAPI(title="DeepSeek v3 Streaming Demo")

# ---------- 数据模型 ----------
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# ---------- 辅助函数 ----------
def sse_format(data: str) -> str:
    """把普通文本包装成 SSE 帧"""
    return f"data: {data}\n\n"

# ---------- 路由 ----------
@app.post("/chat")
async def chat(req: ChatRequest):
    """
    流式返回 deepseek-v3 的回答。
    curl 调用示例:
    curl -N -H "Content-Type: application/json" -d '{"messages':[{"role":"user","content":"你好"}]}' http://localhost:8000/chat
    """
    try:
        # 🔑 stream=True 即可获得逐块输出 :contentReference[oaicite:0]{index=0}
        stream = await ark.chat.completions.create(
            model=MODEL_ID,
            messages=[m.dict() for m in req.messages],
            stream=True,
        )
    except Exception as e:  # 常见原因：Model ID/鉴权错误
        raise HTTPException(status_code=500, detail=str(e))

    async def event_generator() -> AsyncGenerator[str, None]:
        """把 SDK 的异步流转成 SSE 数据流"""
        async for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta.content
            if delta:
                # 每个 token 都立即推送给前端
                yield sse_format(delta)
        # 约定以 “[DONE]” 结尾，方便前端关闭连接
        yield sse_format("[DONE]")

    # 返回 text/event-stream
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# 可选：健康检查
@app.get("/")
async def root():
    return {"msg": "DeepSeek-v3 FastAPI server is running"}
