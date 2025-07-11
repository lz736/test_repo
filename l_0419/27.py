from flask import Flask, request, jsonify, Response
import os
from volcenginesdkarkruntime import Ark
import json
import base64

app = Flask(__name__)

# 初始化Ark客户端，推荐用环境变量存储API Key
client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.getenv("ARK_API_KEY", "d802b8de-3c68-4cf2-8ae2-9fb769d0592a")
)

def validate_image_size(image_url, max_size_mb=10):
    """验证图片大小，防止过大的图片导致问题"""
    try:
        if image_url.startswith('data:image/'):
            # base64图片，估算大小
            base64_data = image_url.split(',', 1)[1] if ',' in image_url else image_url
            estimated_size_mb = len(base64_data) * 0.75 / (1024 * 1024)  # base64大约比原文件大33%

            print(f"🔍 检测到base64图片，估算大小: {estimated_size_mb:.3f}MB")

            if estimated_size_mb > max_size_mb:
                print(f"⚠️ 图片太大: {estimated_size_mb:.1f}MB > {max_size_mb}MB")
                return False, f"图片太大({estimated_size_mb:.1f}MB)，请使用小于{max_size_mb}MB的图片"

            print(f"✅ 图片大小合适: {estimated_size_mb:.3f}MB")
            return True, None

        print("🌐 网络图片，跳过大小检查")
        return True, None  # 网络图片暂不检查

    except Exception as e:
        print(f"❌ 图片大小验证异常: {e}")
        return False, f"图片大小验证失败: {str(e)}"

def get_image_content(img_path_or_url):
    """处理图片，支持本地文件和网络链接"""
    if img_path_or_url.startswith('http://') or img_path_or_url.startswith('https://'):
        # 网络图片直接返回URL
        return {"type": "image_url", "image_url": {"url": img_path_or_url}}
    else:
        # 本地图片转base64（服务端不应该处理客户端本地文件）
        print("⚠️ 服务端不应该直接访问客户端本地文件")
        return None

def get_model_for_content(messages):
    """根据消息内容选择合适的模型"""
    # 检查是否包含图片
    for message in messages:
        if isinstance(message.get('content'), list):
            for content_item in message['content']:
                if content_item.get('type') == 'image_url':
                    return "doubao-seed-1-6-250615"  # 图片模型
    return "deepseek-v3-250324"  # 文本模型

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    messages = data.get('messages')
    question = data.get('question')
    image_url = data.get('image_url')  # 支持单独的图片参数
    stream = data.get('stream', False)
    model = data.get('model')  # 允许客户端指定模型

    if messages:
        # 如果有多轮对话，直接用
        pass
    elif question:
        # 构建单轮对话
        content = question

        # 如果有图片，构建多模态内容
        if image_url:
            print(f"处理图片: {image_url[:100]}...")  # 只打印前100个字符

            # 验证图片大小
            try:
                size_ok, size_error = validate_image_size(image_url)
                if not size_ok:
                    print(f"❌ 图片大小验证失败: {size_error}")
                    return jsonify({'error': size_error}), 400
                else:
                    print("✅ 图片大小验证通过")
            except Exception as e:
                print(f"❌ 图片大小验证异常: {e}")
                return jsonify({'error': f'图片验证失败: {str(e)}'}), 400

            # 检查是否是base64格式的图片（客户端已处理）
            try:
                if image_url.startswith('data:image/'):
                    print("✅ 检测到base64格式图片")
                    image_content = {"type": "image_url", "image_url": {"url": image_url}}
                else:
                    print("🌐 处理网络图片")
                    # 网络图片
                    image_content = get_image_content(image_url)
                    if image_content is None:
                        print("❌ 图片处理失败")
                        return jsonify({'error': '图片处理失败'}), 400
            except Exception as e:
                print(f"❌ 图片内容处理异常: {e}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': f'图片内容处理失败: {str(e)}'}), 400

            content = [
                {"type": "text", "text": question},
                image_content
            ]
            print("✅ 多模态内容构建完成")

        messages = [
            {"role": "system", "content": "你是人工智能助手."},
            {"role": "user", "content": content},
        ]
    else:
        return jsonify({'error': '缺少 question 或 messages'}), 400

    # 自动选择模型（如果客户端没有指定）
    if not model:
        model = get_model_for_content(messages)

    # 保存历史对话到 json 文件
    history_file = 'chat_history.json'
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
        history.append(messages)
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('保存历史对话失败:', e)

    try:
        if stream:
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
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            reply = completion.choices[0].message.content

            # 将助手回复添加到消息历史中（用于多轮对话）
            if reply:
                messages.append({"role": "assistant", "content": reply})

            return jsonify({
                'reply': reply,
                'model': model,
                'messages': messages  # 返回完整的对话历史
            })
    except Exception as e:
        import traceback
        print("后端异常：", e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 启动图片聊天服务器...")
    print("📡 服务地址: http://127.0.0.1:5000")
    print("🖼️ 支持本地图片和网络图片")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
