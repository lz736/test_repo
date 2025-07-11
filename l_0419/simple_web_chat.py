#!/usr/bin/env python3
"""
简化版Web聊天界面 - 解决图片上传问题
"""

from flask import Flask, render_template, request, jsonify
import requests
import base64
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB限制

# 后端API地址
BACKEND_URL = "http://127.0.0.1:5000/ask"

@app.route('/')
def index():
    """主页面"""
    return '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI聊天助手</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; }
        .chat-area { height: 400px; border: 1px solid #ddd; padding: 10px; overflow-y: auto; margin-bottom: 20px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #e3f2fd; text-align: right; }
        .assistant { background: #f1f8e9; }
        .input-area { display: flex; gap: 10px; align-items: flex-end; }
        .input-area input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .input-area input[type="file"] { padding: 5px; }
        .input-area button { padding: 10px 20px; background: #2196f3; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .input-area button:hover { background: #1976d2; }
        .loading { text-align: center; color: #666; }
        .error { color: red; background: #ffebee; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .image-preview { max-width: 200px; border-radius: 5px; margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI聊天助手</h1>
        <div class="chat-area" id="chatArea">
            <div class="message assistant">👋 你好！我是AI助手，可以帮你回答问题和分析图片。</div>
        </div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="输入消息..." onkeypress="if(event.key==='Enter') sendMessage()">
            <input type="file" id="fileInput" accept="image/*" onchange="handleFileSelect(event)">
            <button onclick="sendMessage()">发送</button>
        </div>
        <div id="loading" class="loading" style="display:none;">AI正在思考中...</div>
    </div>

    <script>
        let selectedImageData = null;
        let selectedFileName = null;

        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (!file) return;

            // 检查文件大小 (5MB限制)
            if (file.size > 5 * 1024 * 1024) {
                showError('图片文件太大，请选择小于5MB的图片');
                event.target.value = '';
                return;
            }

            // 读取文件
            const reader = new FileReader();
            reader.onload = function(e) {
                selectedImageData = e.target.result;
                selectedFileName = file.name;
                showMessage('📷 已选择图片: ' + file.name, 'user');
            };
            reader.readAsDataURL(file);
        }

        function showMessage(content, type) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + type;
            
            if (type === 'user' && selectedImageData && content.includes('📷')) {
                messageDiv.innerHTML = content + '<br><img src="' + selectedImageData + '" class="image-preview">';
            } else {
                messageDiv.textContent = content;
            }
            
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        function showError(message) {
            const chatArea = document.getElementById('chatArea');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.textContent = '❌ ' + message;
            chatArea.appendChild(errorDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
        }

        async function sendMessage() {
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            
            if (!message && !selectedImageData) {
                return;
            }

            // 显示用户消息
            if (message) {
                showMessage(message, 'user');
            }

            // 清空输入
            messageInput.value = '';
            
            // 显示加载状态
            showLoading(true);

            try {
                const response = await fetch('/api/simple_chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message || '请分析这张图片',
                        image_data: selectedImageData,
                        image_filename: selectedFileName
                    })
                });

                const data = await response.json();

                if (data.success) {
                    showMessage(data.reply, 'assistant');
                } else {
                    showError(data.error || '发送失败');
                }
            } catch (error) {
                showError('网络错误: ' + error.message);
            } finally {
                showLoading(false);
                // 清除选择的图片
                selectedImageData = null;
                selectedFileName = null;
                document.getElementById('fileInput').value = '';
            }
        }
    </script>
</body>
</html>
    '''

@app.route('/api/simple_chat', methods=['POST'])
def simple_chat():
    """简化的聊天API"""
    print("\n🔥 收到聊天请求")
    
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        image_data = data.get('image_data', '')
        image_filename = data.get('image_filename', '')
        
        print(f"💬 消息: {message}")
        print(f"🖼️ 图片: {'有' if image_data else '无'}")
        
        if not message and not image_data:
            return jsonify({'error': '请输入消息或选择图片'}), 400
        
        # 构建API请求
        if image_data:
            # 有图片的情况
            content = [
                {"type": "text", "text": message},
                {"type": "image_url", "image_url": {"url": image_data}}
            ]
            print(f"📊 图片数据长度: {len(image_data)}")
        else:
            # 纯文本
            content = message
        
        api_messages = [
            {"role": "system", "content": "你是一个友好的AI助手。"},
            {"role": "user", "content": content}
        ]
        
        # 调用后端API
        print("📡 调用后端API...")
        api_data = {"messages": api_messages, "stream": False}
        
        response = requests.post(BACKEND_URL, json=api_data, timeout=60)
        print(f"📡 后端响应: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', '抱歉，我无法回答这个问题。')
            model = result.get('model', '未知模型')
            
            print(f"✅ 成功获取回复: {len(reply)} 字符")
            
            return jsonify({
                'success': True,
                'reply': reply,
                'model': model
            })
        else:
            print(f"❌ 后端API错误: {response.text}")
            return jsonify({'error': f'API调用失败: {response.status_code}'}), 500
            
    except Exception as e:
        print(f"❌ 聊天异常: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 启动简化版Web聊天界面...")
    print("📡 访问地址: http://127.0.0.1:8001")
    print("🖼️ 支持图片上传和文本聊天")
    print("⚠️ 图片大小限制: 5MB")
    print("=" * 50)
    
    try:
        app.run(host='127.0.0.1', port=8001, debug=False)
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        import traceback
        traceback.print_exc()
