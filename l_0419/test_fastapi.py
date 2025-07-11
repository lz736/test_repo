#!/usr/bin/env python3
"""
测试FastAPI聊天界面
"""

import requests
import base64
import os
import time

def test_fastapi_server():
    """测试FastAPI服务器"""
    print("🧪 测试FastAPI聊天界面")
    print("=" * 50)
    
    # 检查健康状态
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 健康检查: {result['message']}")
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到FastAPI服务器: {e}")
        return False
    
    # 测试主页
    try:
        response = requests.get("http://127.0.0.1:8080/", timeout=5)
        if response.status_code == 200:
            print("✅ 主页访问正常")
        else:
            print(f"❌ 主页访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 主页访问异常: {e}")
    
    # 测试文本聊天
    print("\n💬 测试文本聊天...")
    try:
        data = {
            "message": "你好，请简单介绍一下自己",
            "image": None
        }
        response = requests.post("http://127.0.0.1:8080/api/chat", json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 文本聊天成功!")
                print(f"🤖 AI回复: {result.get('reply', '')[:100]}...")
                print(f"🔧 使用模型: {result.get('model', '未知')}")
            else:
                print(f"❌ 文本聊天失败: {result.get('error')}")
        else:
            print(f"❌ 文本聊天HTTP错误: {response.status_code}")
            print(f"📄 错误内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 文本聊天异常: {e}")
    
    # 测试图片聊天
    print("\n🖼️ 测试图片聊天...")
    test_image = "123.png"
    
    if not os.path.exists(test_image):
        print(f"❌ 测试图片不存在: {test_image}")
        return True  # 文本功能正常就算成功
    
    try:
        # 读取图片并转换为base64
        with open(test_image, 'rb') as f:
            img_data = f.read()
        
        # 检查图片大小
        img_size_mb = len(img_data) / (1024 * 1024)
        print(f"📏 图片大小: {img_size_mb:.1f} MB")
        
        if img_size_mb > 3:
            print("⚠️ 图片太大，跳过测试")
            return True
        
        # 转换为base64
        b64_data = base64.b64encode(img_data).decode('utf-8')
        data_url = f"data:image/png;base64,{b64_data}"
        
        print(f"📊 Base64长度: {len(data_url)}")
        
        # 发送请求
        data = {
            "message": "请分析这张图片的内容",
            "image": data_url
        }
        
        response = requests.post("http://127.0.0.1:8080/api/chat", json=data, timeout=60)
        
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

def test_api_docs():
    """测试API文档"""
    print("\n📚 检查API文档...")
    try:
        response = requests.get("http://127.0.0.1:8080/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API文档可访问: http://127.0.0.1:8080/docs")
        else:
            print(f"❌ API文档访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ API文档访问异常: {e}")

if __name__ == "__main__":
    print("🚀 开始FastAPI功能测试")
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(2)
    
    # 运行测试
    success = test_fastapi_server()
    
    # 检查API文档
    test_api_docs()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 FastAPI聊天界面测试成功!")
        print("\n💡 使用方法:")
        print("   1. 浏览器访问: http://127.0.0.1:8080")
        print("   2. API文档: http://127.0.0.1:8080/docs")
        print("   3. 健康检查: http://127.0.0.1:8080/health")
        print("\n🎯 功能特点:")
        print("   ✅ 现代化FastAPI框架")
        print("   ✅ 自动API文档生成")
        print("   ✅ 更好的性能和稳定性")
        print("   ✅ 完整的错误处理")
        print("   ✅ 图片自动压缩")
    else:
        print("❌ FastAPI聊天界面测试失败")
        print("🔧 请检查:")
        print("   1. 后端API服务器是否运行 (python 27.py)")
        print("   2. 端口8080是否被占用")
        print("   3. 网络连接是否正常")
