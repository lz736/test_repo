#!/usr/bin/env python3
"""
测试自动图片压缩功能
"""

import sys
import os
sys.path.append('.')

# 导入我们修改后的函数
from test_ark_api import get_image_content, compress_image_if_needed
import requests

SERVER_URL = "http://127.0.0.1:5000/ask"

def test_image_compression():
    """测试图片压缩功能"""
    print("🧪 测试自动图片压缩功能")
    print("=" * 60)
    
    # 检查测试图片
    test_image = "123.png"
    if not os.path.exists(test_image):
        print(f"❌ 测试图片不存在: {test_image}")
        return False
    
    # 显示原始文件信息
    original_size = os.path.getsize(test_image)
    print(f"📁 原始图片: {test_image}")
    print(f"📏 原始大小: {original_size / 1024:.1f} KB ({original_size / (1024*1024):.1f} MB)")
    
    # 测试压缩功能
    print("\n🔧 测试图片压缩...")
    compressed_path, was_compressed = compress_image_if_needed(test_image, max_size_kb=500)
    
    if was_compressed:
        compressed_size = os.path.getsize(compressed_path)
        print(f"✅ 压缩成功!")
        print(f"📁 压缩后文件: {compressed_path}")
        print(f"📏 压缩后大小: {compressed_size / 1024:.1f} KB")
        print(f"📊 压缩比: {(1 - compressed_size/original_size)*100:.1f}%")
    else:
        print("ℹ️ 无需压缩或压缩失败")
    
    return compressed_path, was_compressed

def test_image_processing():
    """测试完整的图片处理流程"""
    print("\n🔄 测试完整图片处理流程...")
    
    # 测试图片处理
    test_image = "123.png"
    image_content = get_image_content(test_image)
    
    if image_content is None:
        print("❌ 图片处理失败")
        return False
    
    print("✅ 图片处理成功")
    
    # 检查base64大小
    if 'image_url' in image_content and 'url' in image_content['image_url']:
        url = image_content['image_url']['url']
        if url.startswith('data:image/'):
            base64_data = url.split(',', 1)[1] if ',' in url else url
            base64_size_kb = len(base64_data) / 1024
            print(f"📊 Base64大小: {base64_size_kb:.1f} KB")
            
            if base64_size_kb > 1000:  # 1MB
                print("⚠️ Base64数据较大，可能影响传输速度")
            else:
                print("✅ Base64大小合适")
    
    return True

def test_api_call():
    """测试API调用"""
    print("\n📡 测试API调用...")
    
    try:
        # 检查服务器是否运行
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
    except:
        print("❌ 服务器未运行，请先启动: python 27.py")
        return False
    
    # 测试图片API调用
    data = {
        "question": "请简单描述这张图片",
        "image_url": "123.png",  # 让客户端处理
        "stream": False
    }
    
    try:
        # 手动处理图片
        image_content = get_image_content("123.png")
        if image_content is None:
            print("❌ 图片处理失败")
            return False
        
        # 构建请求数据
        data = {
            "question": "请简单描述这张图片",
            "image_url": image_content['image_url']['url'],
            "stream": False
        }
        
        print("📤 发送API请求...")
        response = requests.post(SERVER_URL, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', '无回复')
            model = result.get('model', '未知模型')
            
            print(f"✅ API调用成功!")
            print(f"🤖 使用模型: {model}")
            print(f"💬 AI回复: {reply[:200]}...")
            return True
        else:
            print(f"❌ API调用失败: HTTP {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API调用异常: {e}")
        return False

def cleanup_temp_files():
    """清理临时文件"""
    print("\n🗑️ 清理临时文件...")
    temp_files = [f for f in os.listdir('.') if f.endswith('_compressed.jpg')]
    
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
            print(f"🗑️ 删除临时文件: {temp_file}")
        except:
            print(f"⚠️ 无法删除: {temp_file}")

if __name__ == "__main__":
    print("🚀 开始自动图片压缩功能测试")
    print("📋 测试项目:")
    print("   1. 图片压缩功能")
    print("   2. 图片处理流程") 
    print("   3. API调用测试")
    print("   4. 临时文件清理")
    
    success_count = 0
    total_tests = 4
    
    # 测试1: 图片压缩
    try:
        compressed_path, was_compressed = test_image_compression()
        success_count += 1
    except Exception as e:
        print(f"❌ 压缩测试失败: {e}")
    
    # 测试2: 图片处理
    try:
        if test_image_processing():
            success_count += 1
    except Exception as e:
        print(f"❌ 处理测试失败: {e}")
    
    # 测试3: API调用
    try:
        if test_api_call():
            success_count += 1
    except Exception as e:
        print(f"❌ API测试失败: {e}")
    
    # 测试4: 清理
    try:
        cleanup_temp_files()
        success_count += 1
    except Exception as e:
        print(f"❌ 清理失败: {e}")
    
    # 总结
    print("\n" + "=" * 60)
    print(f"🎯 测试完成: {success_count}/{total_tests} 项通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过! 自动压缩功能正常工作")
        print("\n💡 使用方法:")
        print("   1. 启动服务器: python 27.py")
        print("   2. 启动客户端: python test_ark_api.py")
        print("   3. 输入: img:123.png 分析这张图片")
        print("   4. 系统会自动压缩大图片")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
        
        if success_count == 0:
            print("\n🔧 可能的解决方案:")
            print("   1. 安装Pillow: pip install Pillow")
            print("   2. 确保123.png文件存在")
            print("   3. 启动服务器: python 27.py")
