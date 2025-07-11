#!/usr/bin/env python3
"""
FastAPI版聊天界面 - 替代Flask
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import uvicorn
from typing import Optional
import base64
import os

app = FastAPI(title="AI聊天助手", description="支持文本和图片聊天的AI助手")

# 请求模型
class ChatRequest(BaseModel):
    message: str
    image: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    reply: Optional[str] = None
    error: Optional[str] = None
    model: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def index():
    """主页面"""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI聊天助手 - FastAPI版</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .chat-container {
            width: 90%; max-width: 700px; height: 85vh;
            background: white; border-radius: 20px; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            display: flex; flex-direction: column; overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 25px; text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header h1 { font-size: 28px; margin-bottom: 8px; }
        .header p { opacity: 0.9; font-size: 16px; }
        .messages {
            flex: 1; padding: 25px; overflow-y: auto; background: #f8f9fa;
            scroll-behavior: smooth;
        }
        .message {
            margin: 20px 0; padding: 15px 20px; border-radius: 20px; max-width: 80%;
            word-wrap: break-word; animation: fadeIn 0.3s ease-in;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .user { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; margin-left: auto; text-align: right;
            border-bottom-right-radius: 5px;
        }
        .assistant { 
            background: white; color: #333; 
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            border-bottom-left-radius: 5px;
        }
        .input-area {
            padding: 25px; background: white; border-top: 1px solid #eee;
            display: flex; gap: 15px; align-items: flex-end;
        }
        .input-group { 
            flex: 1; display: flex; flex-direction: column; gap: 12px; 
        }
        input[type="text"] {
            padding: 15px 20px; border: 2px solid #e1e5e9; border-radius: 25px;
            outline: none; font-size: 16px; transition: all 0.3s;
        }
        input[type="text"]:focus { 
            border-color: #667eea; 
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        input[type="file"] { 
            padding: 10px 15px; border: 2px solid #e1e5e9; border-radius: 15px;
            font-size: 14px; background: #f8f9fa;
        }
        button {
            padding: 15px 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 25px; cursor: pointer;
            font-size: 16px; font-weight: 600; transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        button:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        button:disabled { 
            background: #ccc; cursor: not-allowed; transform: none; 
            box-shadow: none;
        }
        .loading { 
            text-align: center; color: #667eea; padding: 15px; 
            font-weight: 500;
        }
        .error { 
            background: #fee; color: #c53030; padding: 15px; 
            border-radius: 10px; margin: 15px 0; border-left: 4px solid #c53030;
        }
        .image-preview { 
            max-width: 250px; border-radius: 10px; margin: 8px 0; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.1); cursor: pointer;
            transition: transform 0.3s;
        }
        .image-preview:hover { transform: scale(1.02); }
        .file-info { 
            font-size: 13px; color: #667eea; background: #f0f4ff; 
            padding: 8px 12px; border-radius: 8px; display: inline-block;
        }
        .typing-indicator {
            display: flex; align-items: center; gap: 5px; color: #667eea;
        }
        .typing-dot {
            width: 8px; height: 8px; border-radius: 50%; background: #667eea;
            animation: typing 1.4s infinite ease-in-out;
        }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h1>🤖 AI聊天助手</h1>
            <p>FastAPI版 - 支持文本和图片聊天</p>
        </div>
        
        <div class="messages" id="messages">
            <div class="message assistant">
                👋 你好！我是AI助手，可以帮你回答问题和分析图片。<br>
                <small style="opacity: 0.8;">💡 提示：可以上传图片进行分析，支持JPG、PNG等格式</small>
            </div>
        </div>
        
        <div class="input-area">
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="输入你的问题..." 
                       onkeypress="if(event.key==='Enter' && !event.shiftKey) { event.preventDefault(); sendMessage(); }">
                <input type="file" id="fileInput" accept="image/*" onchange="handleFile(event)">
                <div class="file-info" id="fileInfo" style="display: none;"></div>
            </div>
            <button id="sendBtn" onclick="sendMessage()">发送</button>
        </div>
        
        <div id="loading" class="loading" style="display:none;">
            <div class="typing-indicator">
                <span>AI正在思考</span>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    </div>

    <script>
        let selectedImage = null;

        function addMessage(content, type, imageUrl = null) {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = 'message ' + type;
            
            let html = '';
            if (imageUrl) {
                html += '<img src="' + imageUrl + '" class="image-preview" onclick="window.open(this.src, \'_blank\')" title="点击查看大图"><br>';
            }
            html += content;
            
            div.innerHTML = html;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }

        function showError(msg) {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = 'error';
            div.innerHTML = '❌ ' + msg;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }

        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
            document.getElementById('sendBtn').disabled = show;
            if (show) {
                document.getElementById('sendBtn').textContent = '发送中...';
            } else {
                document.getElementById('sendBtn').textContent = '发送';
            }
        }

        function handleFile(event) {
            const file = event.target.files[0];
            if (!file) {
                selectedImage = null;
                document.getElementById('fileInfo').style.display = 'none';
                return;
            }

            // 检查文件类型
            if (!file.type.startsWith('image/')) {
                showError('请选择图片文件');
                event.target.value = '';
                return;
            }

            // 检查文件大小 (3MB限制)
            if (file.size > 3 * 1024 * 1024) {
                showError('图片文件太大，请选择小于3MB的图片');
                event.target.value = '';
                return;
            }

            // 读取并压缩图片
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image();
                img.onload = function() {
                    // 压缩图片
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    
                    // 计算新尺寸 (最大1000px)
                    let { width, height } = img;
                    const maxDim = 1000;
                    
                    if (width > maxDim || height > maxDim) {
                        if (width > height) {
                            height = (height * maxDim) / width;
                            width = maxDim;
                        } else {
                            width = (width * maxDim) / height;
                            height = maxDim;
                        }
                    }
                    
                    canvas.width = width;
                    canvas.height = height;
                    
                    // 绘制并压缩
                    ctx.drawImage(img, 0, 0, width, height);
                    selectedImage = canvas.toDataURL('image/jpeg', 0.8);
                    
                    // 显示文件信息
                    const sizeKB = Math.round(selectedImage.length * 0.75 / 1024);
                    const fileInfo = document.getElementById('fileInfo');
                    fileInfo.innerHTML = '📷 ' + file.name + ' (压缩后: ' + sizeKB + 'KB)';
                    fileInfo.style.display = 'block';
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message && !selectedImage) {
                input.focus();
                return;
            }

            // 显示用户消息
            if (selectedImage) {
                addMessage(message || '请分析这张图片', 'user', selectedImage);
            } else {
                addMessage(message, 'user');
            }

            // 清空输入
            input.value = '';
            showLoading(true);

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message || '请分析这张图片',
                        image: selectedImage
                    })
                });

                const data = await response.json();

                if (data.success) {
                    let replyText = data.reply;
                    if (data.model) {
                        replyText += '<br><small style="opacity: 0.7;">🤖 ' + data.model + '</small>';
                    }
                    addMessage(replyText, 'assistant');
                } else {
                    showError(data.error || '发送失败，请重试');
                }
            } catch (error) {
                showError('网络连接失败: ' + error.message);
            } finally {
                showLoading(false);
                // 清除选择的图片
                selectedImage = null;
                document.getElementById('fileInput').value = '';
                document.getElementById('fileInfo').style.display = 'none';
                input.focus();
            }
        }

        // 页面加载完成后聚焦输入框
        window.addEventListener('load', function() {
            document.getElementById('messageInput').focus();
        });
    </script>
</body>
</html>
    """

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天API"""
    print(f"\n🔥 收到聊天请求")
    print(f"💬 消息: {request.message}")
    print(f"🖼️ 图片: {'有' if request.image else '无'}")
    
    try:
        # 构建API请求
        if request.image:
            content = [
                {"type": "text", "text": request.message},
                {"type": "image_url", "image_url": {"url": request.image}}
            ]
            print(f"📊 图片数据长度: {len(request.image)}")
        else:
            content = request.message
        
        api_data = {
            "messages": [
                {"role": "system", "content": "你是一个友好、专业的AI助手。请用简洁明了的语言回答问题。"},
                {"role": "user", "content": content}
            ],
            "stream": False
        }
        
        print("📡 调用后端API...")
        response = requests.post("http://127.0.0.1:5000/ask", json=api_data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', '抱歉，我无法回答这个问题。')
            model = result.get('model', '未知模型')
            
            print(f"✅ 获得回复: {len(reply)} 字符")
            print(f"🤖 使用模型: {model}")
            
            return ChatResponse(
                success=True,
                reply=reply,
                model=model
            )
        else:
            print(f"❌ API错误: {response.status_code}")
            print(f"📄 错误内容: {response.text}")
            raise HTTPException(status_code=500, detail="AI服务暂时不可用")
            
    except requests.exceptions.Timeout:
        print("❌ API请求超时")
        raise HTTPException(status_code=504, detail="AI服务响应超时，请稍后重试")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到AI服务")
        raise HTTPException(status_code=503, detail="AI服务暂时不可用，请检查后端服务器")
    except Exception as e:
        print(f"❌ 异常: {e}")
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "FastAPI聊天服务运行正常"}

if __name__ == "__main__":
    print("🚀 启动FastAPI聊天界面...")
    print("📡 访问地址: http://127.0.0.1:8080")
    print("🖼️ 支持图片上传和文本聊天")
    print("⚡ 使用FastAPI，性能更优")
    print("=" * 50)

    try:
        # 检查依赖
        import uvicorn
        print("✅ uvicorn已安装")

        import fastapi
        print("✅ fastapi已安装")

        # 启动服务器
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8080,
            log_level="info",
            access_log=True,
            reload=False
        )
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请安装: pip install fastapi uvicorn")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
