#!/usr/bin/env python3
"""
修复版服务器 - 专门解决Base64图片问题
"""

from flask import Flask, request, jsonify, Response
import os
from volcenginesdkarkruntime import Ark
import json
import sys

app = Flask(__name__)

# 初始化Ark客户端
client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.getenv("ARK_API_KEY", "d802b8de-3c68-4cf2-8ae2-9fb769d0592a")
)

def log(message):
    """简单的日志函数"""
    print(message, flush=True)
    sys.stdout.flush()

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/ask', methods=['POST'])
def ask():
    log("\n🔥 收到新请求")
    
    try:
        data = request.get_json()
        messages = data.get('messages')
        question = data.get('question')
        image_url = data.get('image_url')
        stream = data.get('stream', False)
        model = data.get('model')
        
        log(f"📝 问题: {question}")
        log(f"🖼️ 图片: {'有' if image_url else '无'}")
        
        # 构建消息
        if messages:
            log("✅ 使用现有消息")
        elif question:
            log("🔧 构建新消息")
            
            if image_url:
                log("🖼️ 处理图片...")
                
                # 简单的大小检查
                if image_url.startswith('data:image/'):
                    log("📊 Base64图片")
                    base64_part = image_url.split(',', 1)[1] if ',' in image_url else image_url
                    size_mb = len(base64_part) * 0.75 / (1024 * 1024)
                    log(f"📏 估算大小: {size_mb:.3f}MB")
                    
                    if size_mb > 10:
                        log(f"❌ 图片太大: {size_mb:.1f}MB")
                        return jsonify({'error': f'图片太大({size_mb:.1f}MB)'}), 400
                    
                    log("✅ 大小检查通过")
                else:
                    log("🌐 网络图片")
                
                # 构建多模态内容
                content = [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
                log("✅ 多模态内容构建完成")
            else:
                content = question
                log("✅ 文本内容")
            
            messages = [
                {"role": "system", "content": "你是人工智能助手."},
                {"role": "user", "content": content},
            ]
            log("✅ 消息构建完成")
        else:
            log("❌ 缺少问题")
            return jsonify({'error': '缺少 question 或 messages'}), 400
        
        # 选择模型
        if not model:
            has_image = False
            for message in messages:
                if isinstance(message.get('content'), list):
                    for item in message['content']:
                        if item.get('type') == 'image_url':
                            has_image = True
                            break
            model = "doubao-seed-1-6-250615" if has_image else "deepseek-v3-250324"
        
        log(f"🤖 使用模型: {model}")
        
        # 调用AI
        log("📡 调用AI...")
        
        if stream:
            log("🌊 流式模式")
            def generate():
                stream_resp = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True,
                )
                for chunk in stream_resp:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            return Response(generate(), mimetype='text/plain')
        else:
            log("📄 非流式模式")
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            reply = completion.choices[0].message.content
            log(f"✅ AI回复成功: {len(reply)} 字符")
            
            return jsonify({
                'reply': reply,
                'model': model
            })
            
    except Exception as e:
        log(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    log("🚀 启动修复版服务器...")
    log("📡 地址: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
