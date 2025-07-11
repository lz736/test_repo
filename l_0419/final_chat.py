#!/usr/bin/env python3
"""
最终版聊天界面 - 确保能正常工作
"""

from flask import Flask, request, jsonify
import requests
import base64
import json

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI聊天助手</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .chat-container {
            width: 90%; max-width: 600px; height: 80vh;
            background: white; border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            display: flex; flex-direction: column; overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 20px; text-align: center;
        }
        .messages {
            flex: 1; padding: 20px; overflow-y: auto; background: #f8f9fa;
        }
        .message {
            margin: 15px 0; padding: 12px 16px; border-radius: 18px; max-width: 80%;
            word-wrap: break-word;
        }
        .user { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; margin-left: auto; text-align: right;
        }
        .assistant { 
            background: white; color: #333; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .input-area {
            padding: 20px; background: white; border-top: 1px solid #eee;
            display: flex; gap: 10px; align-items: flex-end;
        }
        .input-group { flex: 1; display: flex; flex-direction: column; gap: 10px; }
        input[type="text"] {
            padding: 12px; border: 2px solid #eee; border-radius: 25px;
            outline: none; font-size: 16px;
        }
        input[type="text"]:focus { border-color: #667eea; }
        input[type="file"] { 
            padding: 8px; border: 1px solid #ddd; border-radius: 8px;
            font-size: 14px;
        }
        button {
            padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 25px; cursor: pointer;
            font-size: 16px; transition: transform 0.2s;
        }
        button:hover { transform: scale(1.05); }
        button:disabled { background: #ccc; cursor: not-allowed; transform: none; }
        .loading { text-align: center; color: #666; padding: 10px; }
        .error { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 8px; margin: 10px 0; }
        .image-preview { max-width: 200px; border-radius: 8px; margin: 5px 0; }
        .file-info { font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h2>🤖 AI聊天助手</h2>
            <p>支持文本和图片聊天</p>
        </div>
        
        <div class="messages" id="messages">
            <div class="message assistant">
                👋 你好！我是AI助手，可以帮你回答问题和分析图片。
            </div>
        </div>
        
        <div class="input-area">
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="输入消息..." 
                       onkeypress="if(event.key==='Enter') sendMessage()">
                <input type="file" id="fileInput" accept="image/*" onchange="handleFile(event)">
                <div class="file-info" id="fileInfo"></div>
            </div>
            <button id="sendBtn" onclick="sendMessage()">发送</button>
        </div>
        
        <div id="loading" class="loading" style="display:none;">
            🤔 AI正在思考中...
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
                html += '<img src="' + imageUrl + '" class="image-preview"><br>';
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
            div.textContent = '❌ ' + msg;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }

        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
            document.getElementById('sendBtn').disabled = show;
        }

        function handleFile(event) {
            const file = event.target.files[0];
            if (!file) return;

            // 检查文件大小 (2MB限制)
            if (file.size > 2 * 1024 * 1024) {
                showError('图片文件太大，请选择小于2MB的图片');
                event.target.value = '';
                return;
            }

            // 读取文件
            const reader = new FileReader();
            reader.onload = function(e) {
                selectedImage = e.target.result;
                const sizeKB = Math.round(file.size / 1024);
                document.getElementById('fileInfo').textContent = 
                    '📷 已选择: ' + file.name + ' (' + sizeKB + 'KB)';
            };
            reader.readAsDataURL(file);
        }

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message && !selectedImage) return;

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
                    addMessage(data.reply, 'assistant');
                } else {
                    showError(data.error || '发送失败');
                }
            } catch (error) {
                showError('网络错误: ' + error.message);
            } finally {
                showLoading(false);
                selectedImage = null;
                document.getElementById('fileInput').value = '';
                document.getElementById('fileInfo').textContent = '';
            }
        }
    </script>
</body>
</html>
    '''

@app.route('/api/chat', methods=['POST'])
def chat():
    print("\\n🔥 收到聊天请求")
    
    try:
        data = request.get_json()
        message = data.get('message', '')
        image_data = data.get('image', '')
        
        print(f"💬 消息: {message}")
        print(f"🖼️ 图片: {'有' if image_data else '无'}")
        
        # 构建API请求
        if image_data:
            content = [
                {"type": "text", "text": message},
                {"type": "image_url", "image_url": {"url": image_data}}
            ]
        else:
            content = message
        
        api_data = {
            "messages": [
                {"role": "system", "content": "你是一个友好的AI助手。"},
                {"role": "user", "content": content}
            ],
            "stream": False
        }
        
        print("📡 调用后端API...")
        response = requests.post("http://127.0.0.1:5000/ask", json=api_data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', '抱歉，我无法回答。')
            
            print(f"✅ 获得回复: {len(reply)} 字符")
            
            return jsonify({
                'success': True,
                'reply': reply
            })
        else:
            print(f"❌ API错误: {response.status_code}")
            return jsonify({'error': 'AI服务暂时不可用'}), 500
            
    except Exception as e:
        print(f"❌ 异常: {e}")
        return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    print("🚀 启动最终版聊天界面...")
    print("📡 访问地址: http://127.0.0.1:9001")
    print("🖼️ 支持图片上传和文本聊天")
    print("⚠️ 图片大小限制: 2MB")
    print("=" * 50)
    
    app.run(host='127.0.0.1', port=9001, debug=True)
