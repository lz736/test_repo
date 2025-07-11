#!/usr/bin/env python3
"""
简单调试脚本 - 找出本地图片问题
"""

import requests
import json
import os
import base64

# 尝试导入PIL
try:
    from PIL import Image
    print("✅ PIL库可用")
except ImportError:
    print("❌ PIL库不可用")
    exit(1)

SERVER_URL = "http://127.0.0.1:5000/ask"

def create_tiny_image():
    """创建一个超小的测试图片"""
    img = Image.new('RGB', (50, 50), color='blue')
    img.save('tiny_test.jpg', 'JPEG', quality=95)
    size = os.path.getsize('tiny_test.jpg')
    print(f"✅ 创建超小测试图片: tiny_test.jpg ({size} 字节)")
    return 'tiny_test.jpg'

def test_step_by_step():
    """逐步测试每个环节"""
    print("🔍 逐步调试...")
    
    # 步骤1: 创建小图片
    print("\n📋 步骤1: 创建测试图片")
    img_path = create_tiny_image()
    
    # 步骤2: 读取图片
    print("\n📋 步骤2: 读取图片文件")
    try:
        with open(img_path, 'rb') as f:
            img_bytes = f.read()
        print(f"✅ 成功读取图片: {len(img_bytes)} 字节")
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return False
    
    # 步骤3: 转换base64
    print("\n📋 步骤3: 转换为base64")
    try:
        b64 = base64.b64encode(img_bytes).decode('utf-8')
        print(f"✅ Base64转换成功: {len(b64)} 字符")
    except Exception as e:
        print(f"❌ Base64转换失败: {e}")
        return False
    
    # 步骤4: 构建数据URL
    print("\n📋 步骤4: 构建数据URL")
    try:
        data_url = f"data:image/jpeg;base64,{b64}"
        print(f"✅ 数据URL构建成功: {len(data_url)} 字符")
        print(f"🔍 URL前缀: {data_url[:50]}...")
    except Exception as e:
        print(f"❌ 数据URL构建失败: {e}")
        return False
    
    # 步骤5: 测试服务器连接
    print("\n📋 步骤5: 测试服务器连接")
    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        print("✅ 服务器连接正常")
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return False
    
    # 步骤6: 发送简单文本请求
    print("\n📋 步骤6: 测试文本请求")
    try:
        data = {"question": "你好", "stream": False}
        response = requests.post(SERVER_URL, json=data, timeout=15)
        print(f"📡 文本请求状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 文本请求成功: {result.get('reply', '')[:50]}...")
        else:
            print(f"❌ 文本请求失败: {response.text}")
    except Exception as e:
        print(f"❌ 文本请求异常: {e}")
    
    # 步骤7: 发送图片请求
    print("\n📋 步骤7: 测试图片请求")
    try:
        data = {
            "question": "这是什么颜色？",
            "image_url": data_url,
            "stream": False
        }
        
        print("📡 发送图片请求...")
        response = requests.post(SERVER_URL, json=data, timeout=30)
        
        print(f"📡 图片请求状态: {response.status_code}")
        print(f"📄 响应头: {dict(response.headers)}")
        print(f"📄 响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', '无回复')
            model = result.get('model', '未知')
            print(f"✅ 图片请求成功!")
            print(f"🤖 使用模型: {model}")
            print(f"💬 AI回复: {reply}")
            return True
        else:
            print(f"❌ 图片请求失败")
            return False
            
    except Exception as e:
        print(f"❌ 图片请求异常: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 清理测试文件
        if os.path.exists(img_path):
            os.remove(img_path)
            print("🗑️ 清理测试文件")

if __name__ == "__main__":
    print("🚀 开始逐步调试")
    print("=" * 60)
    
    success = test_step_by_step()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 调试成功! 本地图片功能正常")
    else:
        print("❌ 调试发现问题，请查看上面的错误信息")
