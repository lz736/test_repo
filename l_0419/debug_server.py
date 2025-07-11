#!/usr/bin/env python3
"""
调试版服务端 - 简化版本用于找出问题
"""

from flask import Flask, request, jsonify, Response
import os
from volcenginesdkarkruntime import Ark
import json
import base64
import traceback

app = Flask(__name__)

# 初始化Ark客户端
client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.getenv("ARK_API_KEY", "d802b8de-3c68-4cf2-8ae2-9fb769d0592a")
)

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': '服务器运行正常'})

@app.route('/ask', methods=['POST'])
def ask():
    print("\n" + "="*50)
    print("📥 收到请求")
    
    try:
        # 获取请求数据
        data = request.get_json()
        print(f"📋 请求数据键: {list(data.keys()) if data else 'None'}")
        
        messages = data.get('messages')
        question = data.get('question')
        image_url = data.get('image_url')
        stream = data.get('stream', False)
        model = data.get('model')
        
        print(f"💬 问题: {question}")
        print(f"🖼️ 图片URL: {image_url[:100] if image_url else 'None'}...")
        print(f"📨 消息数量: {len(messages) if messages else 0}")
        
        # 构建消息
        if messages:
            print("✅ 使用现有消息")
            pass
        elif question:
            print("🔧 构建新消息")
            content = question
            
            if image_url:
                print("🖼️ 检测到图片，构建多模态内容")
                
                # 检查图片大小
                if image_url.startswith('data:image/'):
                    base64_data = image_url.split(',', 1)[1] if ',' in image_url else image_url
                    estimated_size_mb = len(base64_data) * 0.75 / (1024 * 1024)
                    print(f"📏 估算图片大小: {estimated_size_mb:.3f}MB")
                    
                    if estimated_size_mb > 10:
                        print(f"❌ 图片太大: {estimated_size_mb:.1f}MB")
                        return jsonify({'error': f'图片太大({estimated_size_mb:.1f}MB)'}), 400
                    
                    print("✅ 图片大小合适")
                    image_content = {"type": "image_url", "image_url": {"url": image_url}}
                else:
                    print("🌐 网络图片")
                    image_content = {"type": "image_url", "image_url": {"url": image_url}}
                
                content = [
                    {"type": "text", "text": question},
                    image_content
                ]
                print("✅ 多模态内容构建完成")
            
            messages = [
                {"role": "system", "content": "你是人工智能助手."},
                {"role": "user", "content": content},
            ]
            print(f"✅ 消息构建完成，内容类型: {type(content)}")
        else:
            print("❌ 缺少问题或消息")
            return jsonify({'error': '缺少 question 或 messages'}), 400
        
        # 选择模型
        if not model:
            # 检查是否包含图片
            has_image = False
            for message in messages:
                if isinstance(message.get('content'), list):
                    for content_item in message['content']:
                        if content_item.get('type') == 'image_url':
                            has_image = True
                            break
            
            model = "doubao-seed-1-6-250615" if has_image else "deepseek-v3-250324"
        
        print(f"🤖 选择模型: {model}")
        
        # 调用AI
        print("📡 调用AI...")
        try:
            if stream:
                print("🌊 流式模式")
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
                print("📄 非流式模式")
                completion = client.chat.completions.create(
                    model=model,
                    messages=messages,
                )
                reply = completion.choices[0].message.content
                print(f"✅ AI回复成功: {reply[:100]}...")
                
                return jsonify({
                    'reply': reply,
                    'model': model,
                    'messages': messages
                })
                
        except Exception as ai_error:
            print(f"❌ AI调用失败: {ai_error}")
            traceback.print_exc()
            return jsonify({'error': f'AI调用失败: {str(ai_error)}'}), 500
            
    except Exception as e:
        print(f"❌ 服务端异常: {e}")
        traceback.print_exc()
        return jsonify({'error': f'服务端错误: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 启动调试服务器...")
    print("📡 地址: http://127.0.0.1:5000")
    print("🔧 调试模式: 开启")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False)  # 关闭Flask调试避免重复输出
