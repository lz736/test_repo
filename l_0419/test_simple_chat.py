#!/usr/bin/env python3
"""
测试简化版聊天界面
"""

import requests
import base64
import os

def test_simple_chat():
    """测试简化版聊天"""
    print("🧪 测试简化版Web聊天界面")
    print("=" * 50)
    
    # 检查服务器
    try:
        response = requests.get("http://127.0.0.1:8001/", timeout=5)
        print(f"✅ 简化版服务器状态: {response.status_code}")
    except Exception as e:
        print(f"❌ 简化版服务器连接失败: {e}")
        return False
    
    # 测试文本聊天
    print("\n💬 测试文本聊天...")
    try:
        data = {
            "message": "你好，请简单介绍一下自己",
            "image_data": "",
            "image_filename": ""
        }
        response = requests.post("http://127.0.0.1:8001/api/simple_chat", json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 文本聊天成功!")
                print(f"🤖 AI回复: {result.get('reply', '')[:100]}...")
            else:
                print(f"❌ 文本聊天失败: {result.get('error')}")
        else:
            print(f"❌ 文本聊天HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 文本聊天异常: {e}")
    
    # 测试图片聊天
    print("\n🖼️ 测试图片聊天...")
    test_image = "123.png"
    
    if not os.path.exists(test_image):
        print(f"❌ 测试图片不存在: {test_image}")
        return False
    
    try:
        # 读取图片并转换为base64
        with open(test_image, 'rb') as f:
            img_data = f.read()
        
        # 检查图片大小
        img_size_mb = len(img_data) / (1024 * 1024)
        print(f"📏 图片大小: {img_size_mb:.1f} MB")
        
        if img_size_mb > 5:
            print("⚠️ 图片太大，跳过测试")
            return True
        
        # 转换为base64
        b64_data = base64.b64encode(img_data).decode('utf-8')
        data_url = f"data:image/png;base64,{b64_data}"
        
        print(f"📊 Base64长度: {len(data_url)}")
        
        # 发送请求
        data = {
            "message": "请分析这张图片",
            "image_data": data_url,
            "image_filename": test_image
        }
        
        response = requests.post("http://127.0.0.1:8001/api/simple_chat", json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 图片聊天成功!")
                print(f"🤖 AI回复: {result.get('reply', '')[:100]}...")
                print(f"🔧 使用模型: {result.get('model', '未知')}")
                return True
            else:
                print(f"❌ 图片聊天失败: {result.get('error')}")
                return False
        else:
            print(f"❌ 图片聊天HTTP错误: {response.status_code}")
            print(f"📄 错误内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 图片聊天异常: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_chat()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 简化版聊天界面测试成功!")
        print("💡 现在可以在浏览器中访问: http://127.0.0.1:8001")
        print("📱 支持直接选择图片文件进行聊天")
    else:
        print("❌ 简化版聊天界面测试失败")
        print("🔧 请检查:")
        print("   1. 后端API服务器是否运行 (python 27.py)")
        print("   2. 图片文件是否存在且小于5MB")
        print("   3. 网络连接是否正常")
