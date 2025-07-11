#!/usr/bin/env python3
"""
Web聊天界面 - 类似ChatGPT的界面
"""

from flask import Flask, render_template, request, jsonify, session
import os
import requests
import base64
import uuid
from datetime import datetime

# 导入PIL用于图片压缩
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用于session

# 后端API地址
BACKEND_URL = "http://127.0.0.1:5000/ask"

def compress_uploaded_image(file_data, file_ext, max_size_kb=500):
    """压缩上传的图片数据"""
    try:
        # 检查原始大小
        original_size_kb = len(file_data) / 1024
        print(f"📏 原始图片大小: {original_size_kb:.1f} KB")

        if original_size_kb <= max_size_kb:
            print("✅ 图片大小合适，无需压缩")
            return file_data, False

        if not PIL_AVAILABLE:
            print("⚠️ PIL不可用，强制压缩失败")
            # 如果图片太大且无法压缩，返回错误
            if original_size_kb > 2000:  # 超过2MB就拒绝
                raise Exception("图片太大且无法压缩，请安装Pillow或使用更小的图片")
            return file_data, False

        # 使用PIL压缩
        from io import BytesIO

        print(f"🔧 开始压缩图片...")

        # 打开图片
        img = Image.open(BytesIO(file_data))
        print(f"📐 原始尺寸: {img.width}x{img.height}")

        # 转换为RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')

        # 逐步压缩
        quality = 85
        scale = 1.0

        while quality > 15:  # 降低最低质量限制
            # 调整尺寸
            if scale < 1.0:
                new_size = (int(img.width * scale), int(img.height * scale))
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            else:
                resized_img = img

            # 保存到内存
            buffer = BytesIO()
            resized_img.save(buffer, format='JPEG', quality=quality)
            compressed_data = buffer.getvalue()
            compressed_size_kb = len(compressed_data) / 1024

            print(f"🔍 尝试: 质量={quality}, 缩放={scale:.1f}, 大小={compressed_size_kb:.1f}KB")

            # 检查大小
            if compressed_size_kb <= max_size_kb:
                print(f"✅ 压缩成功: {compressed_size_kb:.1f} KB")
                return compressed_data, True

            # 调整参数 - 更激进的压缩
            if quality > 50:
                quality -= 20
            elif scale > 0.5:
                scale -= 0.3
                quality = 85
            elif quality > 25:
                quality -= 10
            else:
                quality -= 5

        # 返回最后的压缩结果
        print(f"⚠️ 使用最大压缩: {len(compressed_data) / 1024:.1f} KB")
        return compressed_data, True

    except Exception as e:
        print(f"压缩失败: {e}")
        return file_data, False

def compress_image_if_needed(img_path, max_size_kb=800):
    """压缩图片如果需要"""
    if not os.path.exists(img_path):
        return None, False, "文件不存在"
    
    file_size = os.path.getsize(img_path)
    file_size_kb = file_size / 1024
    
    if file_size_kb <= max_size_kb:
        return img_path, False, "无需压缩"
    
    if not PIL_AVAILABLE:
        return None, False, "需要安装Pillow进行压缩"
    
    try:
        name, ext = os.path.splitext(img_path)
        compressed_path = f"{name}_compressed.jpg"
        
        with Image.open(img_path) as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            quality = 85
            scale = 1.0
            
            while quality > 20:
                if scale < 1.0:
                    new_width = int(img.width * scale)
                    new_height = int(img.height * scale)
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    resized_img = img
                
                resized_img.save(compressed_path, 'JPEG', quality=quality)
                compressed_size = os.path.getsize(compressed_path)
                compressed_size_kb = compressed_size / 1024
                
                if compressed_size_kb <= max_size_kb:
                    return compressed_path, True, f"压缩成功: {compressed_size_kb:.1f} KB"
                
                if quality > 60:
                    quality -= 15
                elif scale > 0.6:
                    scale -= 0.2
                    quality = 85
                else:
                    quality -= 10
            
            return compressed_path, True, "最大压缩"
            
    except Exception as e:
        return None, False, f"压缩失败: {e}"

def process_image(img_path_or_url):
    """处理图片，支持本地文件和网络链接"""
    if img_path_or_url.startswith('http://') or img_path_or_url.startswith('https://'):
        return {"type": "image_url", "image_url": {"url": img_path_or_url}}, "网络图片"
    else:
        # 尝试多个可能的路径
        possible_paths = [
            img_path_or_url,
            os.path.join('.', img_path_or_url),
            os.path.join('l_0419', img_path_or_url),
            os.path.abspath(img_path_or_url)
        ]
        
        actual_path = None
        for path in possible_paths:
            if os.path.exists(path):
                actual_path = path
                break
        
        if actual_path is None:
            return None, f"图片文件不存在: {img_path_or_url}"
        
        # 检查并压缩图片
        processed_path, was_compressed, message = compress_image_if_needed(actual_path)
        
        if processed_path is None:
            return None, message
        
        # 读取处理后的图片
        try:
            with open(processed_path, 'rb') as f:
                img_bytes = f.read()
            
            ext = os.path.splitext(processed_path)[-1][1:] or 'png'
            b64 = base64.b64encode(img_bytes).decode('utf-8')
            
            # 清理临时文件
            if was_compressed and os.path.exists(processed_path):
                os.remove(processed_path)
            
            return {"type": "image_url", "image_url": {"url": f"data:image/{ext};base64,{b64}"}}, message
            
        except Exception as e:
            return None, f"读取图片失败: {e}"

@app.route('/')
def index():
    """主页面"""
    if 'chat_id' not in session:
        session['chat_id'] = str(uuid.uuid4())
    if 'messages' not in session:
        session['messages'] = []
    return render_template('chat.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """文件上传API"""
    print("\n🔥 收到文件上传请求")
    try:
        if 'file' not in request.files:
            print("❌ 请求中没有文件")
            return jsonify({'error': '没有选择文件'}), 400

        file = request.files['file']
        print(f"📁 文件名: {file.filename}")

        if file.filename == '':
            print("❌ 文件名为空")
            return jsonify({'error': '没有选择文件'}), 400

        # 检查文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        print(f"📄 文件扩展名: {file_ext}")

        if file_ext not in allowed_extensions:
            print(f"❌ 不支持的文件格式: {file_ext}")
            return jsonify({'error': '不支持的文件格式'}), 400

        # 读取文件数据
        print("📖 开始读取文件数据...")
        file_data = file.read()
        print(f"📏 文件数据大小: {len(file_data)} 字节")

        # 压缩图片如果需要
        print("🔧 开始压缩图片...")
        compressed_data, was_compressed = compress_uploaded_image(file_data, file_ext)
        print(f"✅ 压缩完成，是否压缩: {was_compressed}")

        # 转换为base64
        print("📊 转换为base64...")
        import base64
        b64_data = base64.b64encode(compressed_data).decode('utf-8')
        data_url = f"data:image/{file_ext};base64,{b64_data}"
        print(f"📊 Base64长度: {len(b64_data)}")

        result = {
            'success': True,
            'data_url': data_url,
            'filename': file.filename,
            'size': len(compressed_data),
            'compressed': was_compressed
        }
        print("✅ 文件上传处理完成")
        return jsonify(result)

    except Exception as e:
        print(f"❌ 文件上传异常: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'文件上传失败: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天API"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        image_data_url = data.get('image_data_url', '')
        image_filename = data.get('image_filename', '')

        if not message and not image_data_url:
            return jsonify({'error': '请输入消息或上传图片'}), 400
        
        # 初始化session消息
        if 'messages' not in session:
            session['messages'] = []
        
        # 构建用户消息
        user_message = {
            'id': str(uuid.uuid4()),
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().strftime('%H:%M'),
            'image': None
        }

        # 处理图片
        image_content = None
        if image_data_url:
            # 直接使用前端上传的base64数据
            image_content = {"type": "image_url", "image_url": {"url": image_data_url}}
            user_message['image'] = image_filename
            user_message['image_data_url'] = image_data_url
        
        # 添加用户消息到session
        session['messages'].append(user_message)
        
        # 构建API请求
        if image_content:
            content = [
                {"type": "text", "text": message or "请分析这张图片"},
                image_content
            ]
        else:
            content = message
        
        api_messages = [
            {"role": "system", "content": "你是一个友好的AI助手。"},
            {"role": "user", "content": content}
        ]
        
        # 调用后端API
        api_data = {
            "messages": api_messages,
            "stream": False
        }
        
        response = requests.post(BACKEND_URL, json=api_data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', '抱歉，我无法回答这个问题。')
            model = result.get('model', '未知模型')
            
            # 构建AI回复消息
            ai_message = {
                'id': str(uuid.uuid4()),
                'role': 'assistant',
                'content': reply,
                'timestamp': datetime.now().strftime('%H:%M'),
                'model': model
            }
            
            # 添加AI消息到session
            session['messages'].append(ai_message)
            session.modified = True
            
            return jsonify({
                'success': True,
                'user_message': user_message,
                'ai_message': ai_message
            })
        else:
            error_msg = f"API调用失败: {response.status_code}"
            return jsonify({'error': error_msg}), 500
            
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """清空聊天记录"""
    session['messages'] = []
    session.modified = True
    return jsonify({'success': True})

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """获取聊天记录"""
    messages = session.get('messages', [])
    return jsonify({'messages': messages})

if __name__ == '__main__':
    print("🚀 启动Web聊天界面...")
    print("📡 访问地址: http://127.0.0.1:8000")
    print("🖼️ 支持图片上传和文本聊天")
    print("🔧 调试模式: 开启")
    print("=" * 50)

    # 检查依赖
    try:
        import flask
        print("✅ Flask已安装")
    except ImportError:
        print("❌ Flask未安装")
        exit(1)

    try:
        from PIL import Image
        print("✅ Pillow已安装")
    except ImportError:
        print("⚠️ Pillow未安装，图片压缩功能不可用")

    # 启动服务器
    try:
        app.run(host='127.0.0.1', port=8000, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        import traceback
        traceback.print_exc()
