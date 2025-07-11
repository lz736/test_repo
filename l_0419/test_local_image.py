#!/usr/bin/env python3
"""
测试本地图片功能
"""

import requests
import json
import os
import base64

# 服务器配置
SERVER_URL = "http://127.0.0.1:5000/ask"

def test_local_image():
    """测试本地图片"""
    print("🧪 测试本地图片功能")
    print(f"📁 当前工作目录: {os.getcwd()}")
    
    # 检查图片文件是否存在
    image_path = "123.png"
    if os.path.exists(image_path):
        print(f"✅ 找到图片文件: {image_path}")
    else:
        print(f"❌ 图片文件不存在: {image_path}")
        print("📂 当前目录下的图片文件:")
        for file in os.listdir('.'):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                print(f"   - {file}")
        return
    
    # 将本地图片转换为base64
    try:
        with open(image_path, 'rb') as f:
            img_bytes = f.read()
        ext = os.path.splitext(image_path)[-1][1:] or 'png'
        b64 = base64.b64encode(img_bytes).decode('utf-8')
        image_data_url = f"data:image/{ext};base64,{b64}"
        print(f"✅ 图片转换为base64成功，大小: {len(b64)} 字符")
    except Exception as e:
        print(f"❌ 图片转换失败: {e}")
        return

    # 发送请求
    data = {
        "question": "请分析这张图片的内容",
        "image_url": image_data_url,  # 发送base64格式的图片
        "stream": False
    }
    
    try:
        print("📡 发送请求...")
        response = requests.post(SERVER_URL, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', '无回复')
            model = result.get('model', '未知模型')
            
            print(f"✅ 成功！使用模型: {model}")
            print(f"🤖 AI回复: {reply}")
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

if __name__ == "__main__":
    test_local_image()
