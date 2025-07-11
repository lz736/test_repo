#!/usr/bin/env python3
"""
调试图片上传问题
"""

import requests
import os
import time

def test_upload_step_by_step():
    """逐步测试上传过程"""
    print("🔍 逐步调试图片上传问题")
    print("=" * 60)
    
    # 步骤1: 检查服务器状态
    print("📋 步骤1: 检查Web服务器状态")
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"✅ Web服务器状态: {response.status_code}")
    except Exception as e:
        print(f"❌ Web服务器连接失败: {e}")
        return False
    
    # 步骤2: 检查后端API状态
    print("\n📋 步骤2: 检查后端API状态")
    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        print(f"✅ 后端API状态: {response.status_code}")
    except Exception as e:
        print(f"❌ 后端API连接失败: {e}")
        return False
    
    # 步骤3: 测试文本聊天
    print("\n📋 步骤3: 测试文本聊天功能")
    try:
        data = {
            "message": "你好",
            "image_data_url": "",
            "image_filename": ""
        }
        response = requests.post("http://127.0.0.1:8000/api/chat", json=data, timeout=15)
        print(f"📡 文本聊天状态: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 文本聊天正常")
            else:
                print(f"❌ 文本聊天失败: {result.get('error')}")
        else:
            print(f"❌ 文本聊天HTTP错误: {response.text}")
    except Exception as e:
        print(f"❌ 文本聊天异常: {e}")
    
    # 步骤4: 检查测试图片
    print("\n📋 步骤4: 检查测试图片")
    test_image = "123.png"
    if not os.path.exists(test_image):
        print(f"❌ 测试图片不存在: {test_image}")
        return False
    
    file_size = os.path.getsize(test_image)
    print(f"✅ 测试图片存在: {test_image}")
    print(f"📏 文件大小: {file_size / 1024:.1f} KB ({file_size / (1024*1024):.1f} MB)")
    
    # 步骤5: 测试小文件上传
    print("\n📋 步骤5: 创建并测试小图片上传")
    try:
        # 创建一个很小的测试图片
        from PIL import Image
        small_img = Image.new('RGB', (10, 10), color='red')
        small_img.save('tiny_test.jpg', 'JPEG', quality=95)
        
        small_size = os.path.getsize('tiny_test.jpg')
        print(f"✅ 创建小测试图片: tiny_test.jpg ({small_size} 字节)")
        
        # 上传小图片
        with open('tiny_test.jpg', 'rb') as f:
            files = {'file': ('tiny_test.jpg', f, 'image/jpeg')}
            print("📤 开始上传小图片...")
            response = requests.post("http://127.0.0.1:8000/api/upload", files=files, timeout=30)
        
        print(f"📡 小图片上传状态: {response.status_code}")
        print(f"📄 响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 小图片上传成功!")
                print(f"📊 返回数据大小: {len(result.get('data_url', ''))}")
            else:
                print(f"❌ 小图片上传失败: {result.get('error')}")
        else:
            print(f"❌ 小图片上传HTTP错误")
        
        # 清理
        os.remove('tiny_test.jpg')
        
    except Exception as e:
        print(f"❌ 小图片上传异常: {e}")
        import traceback
        traceback.print_exc()
    
    # 步骤6: 测试大图片上传
    print("\n📋 步骤6: 测试大图片上传")
    try:
        print(f"📤 开始上传大图片: {test_image}")
        
        with open(test_image, 'rb') as f:
            files = {'file': (test_image, f, 'image/png')}
            print("📡 发送上传请求...")
            
            # 增加超时时间
            response = requests.post("http://127.0.0.1:8000/api/upload", files=files, timeout=120)
        
        print(f"📡 大图片上传状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 大图片上传成功!")
                print(f"📁 文件名: {result.get('filename')}")
                print(f"📏 压缩后大小: {result.get('size') / 1024:.1f} KB")
                print(f"🔧 是否压缩: {'是' if result.get('compressed') else '否'}")
                print(f"📊 Base64长度: {len(result.get('data_url', ''))}")
                return True
            else:
                print(f"❌ 大图片上传失败: {result.get('error')}")
                return False
        else:
            print(f"❌ 大图片上传HTTP错误: {response.status_code}")
            print(f"📄 错误内容: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 上传超时 - 可能是图片太大或压缩时间过长")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误 - 可能是服务器崩溃或重启")
        return False
    except Exception as e:
        print(f"❌ 大图片上传异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_server_logs():
    """检查服务器是否有错误日志"""
    print("\n📋 检查服务器状态")
    
    # 检查Web服务器进程
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=2)
        print("✅ Web服务器响应正常")
    except:
        print("❌ Web服务器无响应")
    
    # 检查后端API进程
    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=2)
        print("✅ 后端API响应正常")
    except:
        print("❌ 后端API无响应")

if __name__ == "__main__":
    print("🚀 开始调试图片上传问题")
    
    # 检查服务器状态
    check_server_logs()
    
    # 逐步测试
    success = test_upload_step_by_step()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 图片上传功能正常!")
        print("💡 如果浏览器中仍有问题，请:")
        print("   1. 清除浏览器缓存")
        print("   2. 尝试刷新页面")
        print("   3. 检查浏览器控制台错误")
    else:
        print("❌ 图片上传功能异常")
        print("🔧 可能的解决方案:")
        print("   1. 重启Web服务器")
        print("   2. 检查图片文件是否损坏")
        print("   3. 尝试使用更小的图片")
        print("   4. 检查Pillow库是否正确安装")
