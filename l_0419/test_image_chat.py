#!/usr/bin/env python3
"""
图片聊天功能测试脚本
支持本地图片和网络图片链接
"""

import requests
import json
import os
import base64

# 服务器配置
SERVER_URL = "http://127.0.0.1:5000/ask"

def test_image_chat():
    """测试图片聊天功能"""
    print("🧪 图片聊天功能测试")
    print("=" * 50)
    
    # 测试用例
    test_cases = [
        {
            "name": "网络图片测试",
            "image_url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg",
            "question": "这张图片显示的是什么地方？请详细描述一下。"
        },
        {
            "name": "本地图片测试（如果存在）",
            "image_url": "./test_image.jpg",  # 需要用户提供测试图片
            "question": "请分析这张图片的内容"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 测试 {i}: {test_case['name']}")
        print(f"🖼️ 图片: {test_case['image_url']}")
        print(f"❓ 问题: {test_case['question']}")
        
        # 跳过不存在的本地文件
        if not test_case['image_url'].startswith('http') and not os.path.exists(test_case['image_url']):
            print("⏭️ 跳过：本地图片文件不存在")
            continue
        
        # 发送请求
        data = {
            "question": test_case['question'],
            "image_url": test_case['image_url'],
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
        
        print("-" * 30)

def test_multi_turn_with_image():
    """测试包含图片的多轮对话"""
    print("\n🔄 多轮图片对话测试")
    print("=" * 50)
    
    # 初始化对话
    messages = [
        {"role": "system", "content": "你是一个专业的图片分析助手。"}
    ]
    
    # 第一轮：发送图片
    image_content = {
        "type": "image_url",
        "image_url": {"url": "https://ark-project.tos-cn-beijing.ivolces.com/images/view.jpeg"}
    }
    
    messages.append({
        "role": "user",
        "content": [
            {"type": "text", "text": "请简单描述这张图片"},
            image_content
        ]
    })
    
    data = {
        "messages": messages,
        "stream": False
    }
    
    try:
        print("📡 第一轮：发送图片分析请求...")
        response = requests.post(SERVER_URL, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply')
            model = result.get('model', '未知模型')
            
            print(f"✅ 第一轮成功！使用模型: {model}")
            print(f"🤖 AI回复: {reply}")
            
            # 更新消息历史
            if 'messages' in result:
                messages = result['messages']
            else:
                messages.append({"role": "assistant", "content": reply})
            
            # 第二轮：基于图片继续对话
            messages.append({
                "role": "user",
                "content": "能告诉我更多关于这个地方的历史背景吗？"
            })
            
            data = {
                "messages": messages,
                "stream": False
            }
            
            print("\n📡 第二轮：继续对话...")
            response = requests.post(SERVER_URL, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                reply = result.get('reply')
                model = result.get('model', '未知模型')
                
                print(f"✅ 第二轮成功！使用模型: {model}")
                print(f"🤖 AI回复: {reply}")
            else:
                print(f"❌ 第二轮失败: HTTP {response.status_code}")
        else:
            print(f"❌ 第一轮失败: HTTP {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    print("🚀 启动图片聊天功能测试")
    print("⚠️ 请确保服务器已启动 (python 27.py)")
    print()
    
    # 基础图片聊天测试
    test_image_chat()
    
    # 多轮对话测试
    test_multi_turn_with_image()
    
    print("\n🎉 测试完成！")
