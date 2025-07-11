#!/usr/bin/env python3
"""
测试Web界面的文件上传功能
"""

import requests
import os

def test_file_upload():
    """测试文件上传API"""
    print("🧪 测试Web界面文件上传功能")
    print("=" * 50)
    
    # 检查测试图片
    test_image = "123.png"
    if not os.path.exists(test_image):
        print(f"❌ 测试图片不存在: {test_image}")
        return False
    
    # 检查Web服务器
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print("✅ Web服务器运行正常")
    except:
        print("❌ Web服务器未运行，请先启动: python web_chat.py")
        return False
    
    # 测试文件上传
    print(f"\n📤 测试上传文件: {test_image}")
    
    try:
        with open(test_image, 'rb') as f:
            files = {'file': (test_image, f, 'image/png')}
            response = requests.post("http://127.0.0.1:8000/api/upload", files=files, timeout=30)
        
        print(f"📡 上传响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 文件上传成功!")
                print(f"📁 文件名: {result.get('filename')}")
                print(f"📏 文件大小: {result.get('size') / 1024:.1f} KB")
                print(f"🔧 是否压缩: {'是' if result.get('compressed') else '否'}")
                print(f"📊 Base64长度: {len(result.get('data_url', ''))}")
                
                # 测试聊天API
                print(f"\n💬 测试图片聊天...")
                chat_data = {
                    "message": "请分析这张图片",
                    "image_data_url": result.get('data_url'),
                    "image_filename": result.get('filename')
                }
                
                chat_response = requests.post("http://127.0.0.1:8000/api/chat", 
                                            json=chat_data, timeout=60)
                
                print(f"📡 聊天响应状态: {chat_response.status_code}")
                
                if chat_response.status_code == 200:
                    chat_result = chat_response.json()
                    if chat_result.get('success'):
                        print("✅ 图片聊天成功!")
                        ai_message = chat_result.get('ai_message', {})
                        print(f"🤖 AI回复: {ai_message.get('content', '')[:100]}...")
                        print(f"🔧 使用模型: {ai_message.get('model', '未知')}")
                        return True
                    else:
                        print(f"❌ 图片聊天失败: {chat_result.get('error')}")
                        return False
                else:
                    print(f"❌ 聊天请求失败: {chat_response.text}")
                    return False
            else:
                print(f"❌ 上传失败: {result.get('error')}")
                return False
        else:
            print(f"❌ 上传请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_web_interface():
    """测试Web界面基本功能"""
    print("\n🌐 测试Web界面基本功能")
    
    try:
        # 测试主页
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ 主页访问正常")
        else:
            print(f"❌ 主页访问失败: {response.status_code}")
            return False
        
        # 测试文本聊天
        chat_data = {
            "message": "你好，请简单介绍一下自己",
            "image_data_url": "",
            "image_filename": ""
        }
        
        response = requests.post("http://127.0.0.1:8000/api/chat", json=chat_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 文本聊天功能正常")
                ai_message = result.get('ai_message', {})
                print(f"🤖 AI回复: {ai_message.get('content', '')[:50]}...")
                return True
            else:
                print(f"❌ 文本聊天失败: {result.get('error')}")
                return False
        else:
            print(f"❌ 文本聊天请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Web界面测试异常: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始Web界面功能测试")
    
    # 测试基本功能
    web_ok = test_web_interface()
    
    # 测试文件上传
    upload_ok = test_file_upload() if web_ok else False
    
    print("\n" + "=" * 50)
    print("📊 测试结果:")
    print(f"   🌐 Web界面: {'✅ 正常' if web_ok else '❌ 异常'}")
    print(f"   📤 文件上传: {'✅ 正常' if upload_ok else '❌ 异常'}")
    
    if web_ok and upload_ok:
        print("\n🎉 所有功能测试通过!")
        print("💡 现在可以在浏览器中访问: http://127.0.0.1:8000")
        print("📱 支持拖拽上传图片进行聊天")
    else:
        print("\n⚠️ 部分功能异常，请检查:")
        if not web_ok:
            print("   - 确保Web服务器正常启动")
            print("   - 检查后端API服务器是否运行")
        if not upload_ok:
            print("   - 检查图片文件是否存在")
            print("   - 确保Pillow库已安装")
