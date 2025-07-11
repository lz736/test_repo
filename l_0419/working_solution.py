#!/usr/bin/env python3
"""
完整工作的图片聊天解决方案
包含自动压缩功能
"""

import requests
import json
import os
import base64

# 导入PIL用于图片压缩
try:
    from PIL import Image
    PIL_AVAILABLE = True
    print("✅ 图片压缩功能可用")
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ 图片压缩功能不可用，请安装: pip install Pillow")

SERVER_URL = "http://127.0.0.1:5000/ask"

def compress_and_convert_image(img_path, max_size_kb=500):
    """
    压缩并转换图片为base64
    返回: (data_url, success, message)
    """
    if not os.path.exists(img_path):
        return None, False, f"文件不存在: {img_path}"
    
    original_size = os.path.getsize(img_path)
    print(f"📏 原始文件: {original_size / 1024:.1f} KB")
    
    try:
        # 如果文件已经很小，直接转换
        if original_size <= max_size_kb * 1024:
            with open(img_path, 'rb') as f:
                img_bytes = f.read()
            ext = os.path.splitext(img_path)[-1][1:] or 'png'
            b64 = base64.b64encode(img_bytes).decode('utf-8')
            data_url = f"data:image/{ext};base64,{b64}"
            return data_url, True, "无需压缩"
        
        # 需要压缩
        if not PIL_AVAILABLE:
            return None, False, "文件太大且无法压缩，请安装Pillow"
        
        print(f"🔧 开始压缩...")
        
        with Image.open(img_path) as img:
            # 转换为RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # 逐步压缩
            quality = 85
            scale = 1.0
            
            while quality > 20:
                # 调整尺寸
                if scale < 1.0:
                    new_size = (int(img.width * scale), int(img.height * scale))
                    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                else:
                    resized_img = img
                
                # 保存到内存
                import io
                buffer = io.BytesIO()
                resized_img.save(buffer, format='JPEG', quality=quality)
                img_bytes = buffer.getvalue()
                
                # 检查大小
                if len(img_bytes) <= max_size_kb * 1024:
                    b64 = base64.b64encode(img_bytes).decode('utf-8')
                    data_url = f"data:image/jpeg;base64,{b64}"
                    compressed_size = len(img_bytes) / 1024
                    print(f"✅ 压缩成功: {compressed_size:.1f} KB (质量:{quality})")
                    return data_url, True, f"压缩成功: {compressed_size:.1f} KB"
                
                # 调整参数
                if quality > 60:
                    quality -= 15
                elif scale > 0.6:
                    scale -= 0.2
                    quality = 85
                else:
                    quality -= 10
            
            # 最后尝试
            b64 = base64.b64encode(img_bytes).decode('utf-8')
            data_url = f"data:image/jpeg;base64,{b64}"
            return data_url, True, "最大压缩"
            
    except Exception as e:
        return None, False, f"处理失败: {e}"

def chat_with_image(question, image_path_or_url):
    """
    发送图片聊天请求
    """
    print(f"\n💬 问题: {question}")
    print(f"🖼️ 图片: {image_path_or_url}")
    
    # 处理图片
    if image_path_or_url.startswith('http://') or image_path_or_url.startswith('https://'):
        # 网络图片
        print("🌐 使用网络图片")
        image_url = image_path_or_url
    else:
        # 本地图片
        print("📁 处理本地图片...")
        image_url, success, message = compress_and_convert_image(image_path_or_url)
        
        if not success:
            print(f"❌ 图片处理失败: {message}")
            return False
        
        print(f"✅ 图片处理成功: {message}")
    
    # 发送请求
    data = {
        "question": question,
        "image_url": image_url,
        "stream": False
    }
    
    try:
        print("📡 发送请求...")
        response = requests.post(SERVER_URL, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', '无回复')
            model = result.get('model', '未知模型')
            
            print(f"✅ 请求成功!")
            print(f"🤖 使用模型: {model}")
            print(f"💬 AI回复: {reply}")
            return True
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 图片聊天助手")
    print("=" * 50)
    
    # 检查服务器
    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        print("✅ 服务器连接正常")
    except:
        print("❌ 服务器未运行，请先启动服务器:")
        print("   python 27.py")
        return
    
    print("\n💡 使用说明:")
    print("   - 输入 'exit' 退出")
    print("   - 输入 'test' 运行测试")
    print("   - 输入图片路径和问题，用空格分隔")
    print("   - 例如: 123.png 这是什么图片？")
    print("   - 例如: https://example.com/image.jpg 分析这张图")
    
    while True:
        try:
            user_input = input("\n请输入: ").strip()
            
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("👋 再见!")
                break
            
            if user_input.lower() == 'test':
                # 运行测试
                print("\n🧪 运行测试...")
                
                # 测试1: 网络图片
                success1 = chat_with_image(
                    "这张图片显示什么？",
                    "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg"
                )
                
                # 测试2: 本地图片（如果存在）
                if os.path.exists('123.png'):
                    success2 = chat_with_image("分析这张图片", "123.png")
                else:
                    print("⏭️ 跳过本地图片测试（123.png不存在）")
                    success2 = True
                
                if success1 and success2:
                    print("\n🎉 所有测试通过!")
                else:
                    print("\n⚠️ 部分测试失败")
                continue
            
            # 解析用户输入
            parts = user_input.split(' ', 1)
            if len(parts) != 2:
                print("❌ 格式错误，请输入: 图片路径 问题")
                continue
            
            image_path, question = parts
            chat_with_image(question, image_path)
            
        except KeyboardInterrupt:
            print("\n👋 再见!")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    main()
