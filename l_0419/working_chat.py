#!/usr/bin/env python3
"""
完全工作的聊天界面 - 解决所有图片问题
"""

from flask import Flask, request, jsonify
import requests
import base64
import os
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>AI聊天助手</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f2f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .chat { height: 400px; border: 1px solid #ddd; padding: 15px; overflow-y: auto; margin-bottom: 15px; background: #fafafa; }
        .message { margin: 10px 0; padding: 10px; border-radius: 8px; max-width: 80%; }
        .user { background: #007bff; color: white; margin-left: auto; text-align: right; }
        .assistant { background: #e9ecef; color: #333; }
        .input-group { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        input[type="file"] { padding: 5px; }
        button { padding: 10px 15px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .loading { text-align: center; color: #666; margin: 10px 0; }
        .error { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .image-preview { max-width: 150px; border-radius: 5px; margin: 5px 0; }
        .file-info { font-size: 12px; color: #666; margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🤖 AI聊天助手</h2>
        <div class="chat" id="chat">
            <div class="message assistant">👋 你好！我可以帮你回答问题和分析图片。</div>
        </div>
        <div class="input-group">
            <input type="text" id="messageInput" placeholder="输入消息..." onkeypress="if(event.key==='Enter') send()">
            <input type="file" id="fileInput" accept="image/*" onchange="handleFile(event)">
            <button onclick="send()">发送</button>
        </div>
        <div id="loading" class="loading" style="display:none;">🤔 AI正在思考...</div>
    </div>

    <script>
        let currentImage = null;

        function addMessage(content, type, imageUrl = null) {
            const chat = document.getElementById('chat');
            const div = document.createElement('div');
            div.className = 'message ' + type;
            
            let html = '';
            if (imageUrl) {
                html += '<img src="' + imageUrl + '" class="image-preview"><br>';
            }
            html += content;
            
            div.innerHTML = html;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        function showError(msg) {
            const chat = document.getElementById('chat');
            const div = document.createElement('div');
            div.className = 'error';
            div.textContent = '❌ ' + msg;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
        }

        function handleFile(event) {
            const file = event.target.files[0];
            if (!file) return;

            // 检查文件大小
            const maxSize = 2 * 1024 * 1024; // 2MB
            if (file.size > maxSize) {
                showError('图片太大，请选择小于2MB的图片');
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
                    
                    // 计算新尺寸
                    let { width, height } = img;
                    const maxDim = 800;
                    
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
                    const compressedDataUrl = canvas.toDataURL('image/jpeg', 0.7);
                    
                    currentImage = compressedDataUrl;
                    
                    // 显示预览
                    const sizeKB = Math.round(compressedDataUrl.length * 0.75 / 1024);
                    addMessage('📷 已选择图片: ' + file.name + ' (压缩后: ' + sizeKB + 'KB)', 'user', compressedDataUrl);
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }

        async function send() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message && !currentImage) return;

            // 显示用户消息
            if (message) {
                addMessage(message, 'user');
            }

            input.value = '';
            showLoading(true);

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message || '请分析这张图片',
                        image: currentImage
                    })
                });

                const data = await response.json();

                if (data.success) {
                    addMessage(data.reply, 'assistant');
                } else {
                    showError(data.error);
                }
            } catch (error) {
                showError('网络错误: ' + error.message);
            } finally {
                showLoading(false);
                currentImage = null;
                document.getElementById('fileInput').value = '';
            }
        }
    </script>
</body>
</html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    print("\n🔥 收到聊天请求")
    
    try:
        data = request.get_json()
        message = data.get('message', '')
        image_data = data.get('image', '')
        
        print(f"💬 消息: {message}")
        print(f"🖼️ 图片: {'有' if image_data else '无'}")
        
        if image_data:
            print(f"📊 图片数据长度: {len(image_data)}")
        
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
            model = result.get('model', '未知')
            
            print(f"✅ 获得回复: {len(reply)} 字符")
            
            return jsonify({
                'success': True,
                'reply': reply,
                'model': model
            })
        else:
            print(f"❌ API错误: {response.status_code}")
            return jsonify({'error': 'API调用失败'}), 500
            
    except Exception as e:
        print(f"❌ 异常: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 启动完全工作版聊天界面...")
    print("📡 访问地址: http://127.0.0.1:8002")
    print("🖼️ 自动压缩图片到合适大小")
    print("=" * 50)

    try:
        app.run(host='127.0.0.1', port=8002, debug=True)
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        import traceback
        traceback.print_exc()
