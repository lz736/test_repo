#!/usr/bin/env python3
"""
调试本地图片问题
"""

import requests
import json
import os
import base64
from PIL import Image
import io

SERVER_URL = "http://127.0.0.1:5000/ask"

def create_small_test_image():
    """创建一个小的测试图片"""
    # 创建一个简单的测试图片
    img = Image.new('RGB', (100, 100), color='red')
    img.save('small_test.jpg', 'JPEG', quality=90)
    print("✅ 创建小测试图片: small_test.jpg")
    return 'small_test.jpg'

def test_small_image():
    """测试小图片"""
    print("🧪 测试小图片...")
    
    # 创建小图片
    small_img = create_small_test_image()
    
    # 转换为base64
    with open(small_img, 'rb') as f:
        img_bytes = f.read()
    
    b64 = base64.b64encode(img_bytes).decode('utf-8')
    image_data_url = f"data:image/jpeg;base64,{b64}"
    
    print(f"📏 图片大小: {len(img_bytes)} 字节")
    print(f"📊 Base64大小: {len(b64)} 字符")
    
    # 发送请求
    data = {
        "question": "这是什么颜色的图片？",
        "image_url": image_data_url,
        "stream": False
    }
    
    try:
        print("📡 发送请求...")
        response = requests.post(SERVER_URL, json=data, timeout=30)
        
        print(f"📡 响应状态: {response.status_code}")
        print(f"📄 响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', '无回复')
            model = result.get('model', '未知模型')
            
            print(f"✅ 成功!")
            print(f"🤖 模型: {model}")
            print(f"💬 回复: {reply}")
            return True
        else:
            print(f"❌ 失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False
    finally:
        # 清理测试文件
        if os.path.exists(small_img):
            os.remove(small_img)
            print("🗑️ 清理测试文件")

def test_compressed_original():
    """测试压缩后的原图片"""
    print("\n🔧 测试压缩后的原图片...")
    
    if not os.path.exists('123.png'):
        print("❌ 原图片不存在")
        return False
    
    # 压缩原图片
    try:
        with Image.open('123.png') as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # 大幅压缩
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=30)
            img_bytes = buffer.getvalue()
            
            print(f"📏 压缩后大小: {len(img_bytes) / 1024:.1f} KB")
            
            # 转换为base64
            b64 = base64.b64encode(img_bytes).decode('utf-8')
            image_data_url = f"data:image/jpeg;base64,{b64}"
            
            print(f"📊 Base64大小: {len(b64) / 1024:.1f} KB")
            
            # 发送请求
            data = {
                "question": "请简单描述这张图片",
                "image_url": image_data_url,
                "stream": False
            }
            
            print("📡 发送请求...")
            response = requests.post(SERVER_URL, json=data, timeout=60)
            
            print(f"📡 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                reply = result.get('reply', '无回复')
                model = result.get('model', '未知模型')
                
                print(f"✅ 成功!")
                print(f"🤖 模型: {model}")
                print(f"💬 回复: {reply[:200]}...")
                return True
            else:
                print(f"❌ 失败: {response.status_code}")
                print(f"错误: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False

if __name__ == "__main__":
    print("🔍 调试本地图片问题")
    print("=" * 50)
    
    # 检查服务器
    try:
        requests.get("http://127.0.0.1:5000/", timeout=5)
        print("✅ 服务器运行正常")
    except:
        print("❌ 服务器未运行")
        exit(1)
    
    # 测试小图片
    success1 = test_small_image()
    
    # 测试压缩的原图片
    success2 = test_compressed_original()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 本地图片功能正常!")
    elif success1:
        print("✅ 小图片正常，大图片需要更多压缩")
    else:
        print("❌ 本地图片功能有问题")
